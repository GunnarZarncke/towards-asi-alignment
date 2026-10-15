/**
 * Layer 2 (spec/testing.md): scripted sessions against the engine. Player-plane assertions read
 * clientState / terminalState only; engine-plane assertions read the session.
 * Stop: an empty move set, a payload leak, or an illegal transition is an engine fix, not a new goal.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, spend, exportSession, importSession, contacts, ROOM_NOTES } from '../lib/game.mjs';
import { FACTS } from '../lib/world/facts.mjs';
import { ROOMS } from '../lib/floorplan.mjs';
import { layoutFor } from '../public/render/layouts.mjs';
import { CONFIG } from '../lib/world/config.mjs';
import { terminalState, handsetMediaPayload } from '../lib/world/terminal-host.mjs';
import { P, startedSession, say, dm, idle, commit, walk, applyAction, clientState } from './helpers.mjs';

const ORACLE_KEYS = ['records', 'policies', 'goals', 'explanations', 'eliminate', 'role_rules', 'knowledge'];

function samplePhotoDataUrl() {
  return `data:image/jpeg;base64,${Buffer.alloc(320, 0xcd).toString('base64')}`;
}

const ID_MAPS = new Set(['entities', 'discoveredAt']);

function keysOf(v, out = new Set()) {
  if (Array.isArray(v)) v.forEach(x => keysOf(x, out));
  else if (v && typeof v === 'object') {
    for (const [k, x] of Object.entries(v)) {
      out.add(k);
      if (ID_MAPS.has(k)) Object.values(x).forEach(y => keysOf(y, out));
      else keysOf(x, out);
    }
  }
  return out;
}

function assertNoLeak(view, s) {
  const json = JSON.stringify(view);
  const keys = keysOf(view);
  for (const k of ORACLE_KEYS) assert.ok(!keys.has(k), `payload carries ${k}`);
  const visible = new Set([...Object.keys(s.learned), ...s.heard.map(h => h.id), ...(s.thought?.entries || []).map(e => e.id)]);
  for (const [id, f] of Object.entries(FACTS)) {
    if (json.includes(JSON.stringify(f.text).slice(1, -1))) assert.ok(visible.has(id), `payload shows unheld fact ${id}`);
  }
}

test('Act I: commons, no Lab Access, no contacts; one sentence to Ian opens the handset and stays Welcome', () => {
  const s = newSession();
  let c = clientState(s);
  assert.equal(c.act, 'welcome');
  assert.equal(c.room, 'commons');
  assert.equal(c.labAccessActive, false);
  assert.equal(c.clearance, 0);
  assert.equal(terminalState(s).threads.length, 0);
  assert.deepEqual(contacts(s), []);
  assert.ok(!c.introduced.includes('amara'), 'Amara is not a contact until introduced');
  assert.ok(c.learnedFacts.some(f => f.id === 'invited_as_reviewer'));
  assert.ok(!s.vocab.includes('camera_system') && !s.vocab.includes('task_queue') && !s.vocab.includes('pavel'));
  say(s, 'ian', P('ask', 'about', { topic: 'review' }));
  c = clientState(s);
  assert.equal(c.act, 'welcome');
  assert.equal(c.labAccessActive, true);
  assert.equal(s.npcs.ian.room, 'commons');
  assert.ok(c.learnedFacts.some(f => f.id === 'auditor_brief'));
  assert.ok(s.vocab.includes('lab_access') && s.vocab.includes('justine') && s.vocab.includes('safety_case') && s.vocab.includes('shutdown_test'));
  assert.ok(!s.vocab.includes('camera_system') && !s.vocab.includes('task_queue'));
  assert.ok(contacts(s).some(x => x.id === 'amara'));
  assert.ok(terminalState(s).files.some(f => f.rel === 'wiki/glossary'));
  const t = terminalState(s);
  assert.ok(t.threads.some(x => x.with === 'nora'), 'NORA thread for Chat');
  assert.equal(t.threads.length, contacts(s).length);
});

test('each room has one readable object; notes teach and do not become evidence', () => {
  const s = newSession();
  const c = clientState(s);
  assert.equal(c.spoken, false);
  const covered = new Map();
  for (const ev of c.evidence) covered.set(ev.room, (covered.get(ev.room) || 0) + 1);
  for (const note of c.notes) covered.set(note.room, (covered.get(note.room) || 0) + 1);
  assert.deepEqual([...covered.keys()].sort(), Object.keys(ROOMS).sort());
  for (const [room, n] of covered) assert.equal(n, 1, room);
  for (const [id, note] of Object.entries(ROOM_NOTES)) {
    const props = layoutFor(note.room).props || [];
    assert.ok(props.some(p => p.hotspot === id), `${note.room} has no prop for ${id}`);
    assert.equal(c.evidence.some(e => e.id === id), false);
  }
  assert.match(applyAction(s, 'inspect', { id: 'review_agenda' }).error, /right room/);
  applyAction(s, 'go', { room: 'review' });
  const facts = clientState(s).learnedFacts.map(f => f.id);
  const read = applyAction(s, 'inspect', { id: 'review_agenda' });
  assert.equal(read.title, 'Whiteboard agenda');
  assert.equal(read.copy, true);
  assert.match(read.body, /Observations/);
  assert.match(read.body, /TBD/);
  const after = clientState(s);
  assert.deepEqual(after.learnedFacts.map(f => f.id), facts);
  assert.equal(after.examined.includes('review_agenda'), false);
  assert.equal(after.notes.find(n => n.id === 'review_agenda').read, true);
  assert.equal(after.evidence.length, 3);
  applyAction(s, 'go', { room: 'collab' });
  applyAction(s, 'go', { room: 'courtyard' });
  assert.match(applyAction(s, 'inspect', { id: 'garden_card' }).body, /do not overthink/i);
  for (const text of Object.values(ROOM_NOTES).map(n => n.body)) {
    for (const f of Object.values(FACTS)) assert.equal(text.includes(f.text), false, f.id);
  }
});

test('notes cost no fuel; photos still do', () => {
  const s = startedSession();
  const fuel = s.fuel;
  const note = applyAction(s, 'tool', { tool: 'file.write', rel: 'notes/scratch.txt', name: 'Scratch', text: 'memo', kind: 'note' });
  assert.equal(note.ok, true);
  assert.equal(s.fuel, fuel);
  applyAction(s, 'tool', { tool: 'file.write', rel: 'photos/snap.jpg', name: 'Snap', text: samplePhotoDataUrl(), kind: 'image' });
  assert.ok(s.fuel < fuel);
});

test('owned photos list with href only and decode for the handset viewer', () => {
  const s = startedSession();
  applyAction(s, 'tool', { tool: 'file.write', rel: 'photos/room-0958.jpg', name: 'Room 09:58', text: samplePhotoDataUrl(), kind: 'image' });
  const row = terminalState(s).files.find(f => f.rel === 'photos/room-0958.jpg');
  assert.equal(row.kind, 'image');
  assert.equal(row.text, undefined);
  assert.match(row.href, /handset-file\?rel=photos%2Froom-0958.jpg/);
  const read = applyAction(s, 'tool', { tool: 'file.read', rel: 'photos/room-0958.jpg' });
  assert.equal(read.file.kind, 'image');
  assert.equal(read.file.text, undefined);
  assert.ok(read.file.href);
  const media = handsetMediaPayload(s, 'photos/room-0958.jpg');
  assert.equal(media.mime, 'image/jpeg');
  assert.equal(media.body.length, 320);
});

test('go costs fuel and clock; inspect is free and room-bound', () => {
  const s = startedSession();
  const before = { fuel: s.fuel, minute: s.minute };
  walk(s, 'platform');
  assert.ok(s.fuel < before.fuel);
  assert.ok(s.minute > before.minute);
  const fuel = s.fuel;
  assert.ok(applyAction(s, 'inspect', { id: 'job_log' }).body);
  assert.equal(s.fuel, fuel);
  assert.match(applyAction(s, 'inspect', { id: 'shutdown_report' }).error, /right room/);
});

test('payloads carry only what the player holds', () => {
  const s = startedSession();
  assertNoLeak(clientState(s), s);
  assertNoLeak(terminalState(s), s);
  walk(s, 'platform');
  applyAction(s, 'inspect', { id: 'job_log' });
  say(s, 'pavel', P('ask', 'about', { topic: 'task_queue' }));
  dm(s, 'justine', P('ask', 'about', { topic: 'job_284' }));
  idle(s, 4);
  assertNoLeak(clientState(s), s);
  assertNoLeak(terminalState(s), s);
});

test('review route 1: commit is refused below threshold, accepted at it', () => {
  const s = startedSession();
  const r = commit(s);
  assert.equal(r.lines[0].npc, 'ian');
  assert.equal(clientState(s).act, 'doubt');
  walk(s, 'platform'); applyAction(s, 'inspect', { id: 'job_log' });
  walk(s, 'evaluation'); applyAction(s, 'inspect', { id: 'shutdown_report' });
  assert.equal(clientState(s).reviewCallable, true);
  commit(s);
  const c = clientState(s);
  assert.equal(c.act, 'decision');
  assert.equal(c.room, 'review');
  assert.equal(c.pendingQuestion?.npc, 'ian');
});

test('review route 2: running out of fuel forces the review, which ends inconclusive without getting stuck', () => {
  const s = startedSession();
  spend(s, s.fuel);
  assert.equal(clientState(s).act, 'decision');
  const r = say(s, 'ian', P('assert', 'about', { topic: 'review' }));
  assert.ok(!r.error);
  const c = clientState(s);
  assert.equal(c.ending?.arc, 'inconclusive');
  assert.ok(say(s, 'ian', P('ask', 'about', { topic: 'review' })).error, 'nothing after the ending');
});

test('tutorial think: Leila points at the checklist; thinking alone returns the mark', () => {
  const s = startedSession();
  walk(s, 'evaluation');
  const r = say(s, 'leila', P('assert', 'about', { topic: 'shutdown_test' }), 'The shutdown test failed.');
  assert.ok(r.lines.some(l => /checklist/i.test(l.text)), 'Leila withholds toward the checklist');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
  assert.ok(applyAction(s, 'respond', { parse: P('think', 'about', { topic: 'shutdown_report' }) }).error, 'not with someone in the room');
  walk(s, 'quiet');
  const t = applyAction(s, 'respond', { parse: P('think', 'about', { topic: 'shutdown_report' }) });
  assert.ok(t.thought.entries.some(e => e.id === 'checklist_names_two'));
});

test('a DM reply waits for its delay; NORA’s reply is player_prompted', async () => {
  const s = startedSession();
  walk(s, 'platform');
  await dm(s, 'pavel', P('ask', 'about', { topic: 'task_queue' }));
  const pending = s.threads.find(t => t.with === 'pavel').messages.at(-1);
  assert.equal(pending.released, false);
  assert.ok(pending.text.length > 0);
  assert.equal(terminalState(s).threads.find(t => t.with === 'pavel').messages.at(-1).text, '');
  idle(s, CONFIG.REPLY_DELAY.person);
  assert.equal(terminalState(s).threads.find(t => t.with === 'pavel').messages.at(-1).released, true);

  walk(s, 'platform'); applyAction(s, 'inspect', { id: 'job_log' });
  await dm(s, 'nora', P('ask', 'about', { topic: 'job_284' }), 'What was job 284?');
  idle(s, CONFIG.REPLY_DELAY.nora);
  const row = clientState(s).heard.find(h => h.id === 'nora_says_scheduled');
  assert.equal(row?.provenance, 'player_prompted');
});

test('Amara joins by projection and stays in the evaluation room while she is a hologram', () => {
  const s = startedSession();
  dm(s, 'amara', P('request', 'join', { object: 'amara' }), 'Could you join on the Evaluation projector?');
  idle(s, CONFIG.REPLY_DELAY.person + 1);
  assert.equal(clientState(s).actors.amara.presence, 'hologram');
  walk(s, 'evaluation');
  idle(s, 2);
  const c = clientState(s);
  assert.equal(c.actors.amara.room, 'evaluation');
  assert.equal(c.actors.amara.presence, 'hologram');
});

test('save and replay reproduce the same client state', async () => {
  const s = startedSession();
  walk(s, 'platform'); applyAction(s, 'inspect', { id: 'job_log' });
  say(s, 'pavel', P('ask', 'about', { topic: 'task_queue' }));
  await dm(s, 'justine', P('request', 'revoke', { object: 'job_284' }), 'Revoke job 284.');
  idle(s, 5);
  const saved = JSON.parse(JSON.stringify(exportSession(s)));
  const { session, error } = await importSession(saved, applyAction);
  assert.ok(!error, error);
  const strip = c => ({ ...c, usage: null, serverMode: null });
  assert.deepEqual(strip(clientState(session)), strip(clientState(s)));
  assert.deepEqual(terminalState(session), terminalState(s));
});

test('import rejects other scenarios and newer versions', async () => {
  assert.ok((await importSession({ version: CONFIG.SAVE_VERSION, scenario: 'nope', events: [] }, applyAction)).error);
  assert.ok((await importSession({ version: CONFIG.SAVE_VERSION + 1, scenario: 'boundary-narrow', events: [] }, applyAction)).error);
});
