/**
 * Layer 2 (spec/testing.md): scripted sessions against the engine. Player-plane assertions read
 * clientState / terminalState only; engine-plane assertions read the session.
 * Stop: an empty move set, a payload leak, or an illegal transition is an engine fix, not a new goal.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, spend, exportSession, importSession, contacts } from '../lib/game.mjs';
import { FACTS } from '../lib/world/facts.mjs';
import { CONFIG } from '../lib/world/config.mjs';
import { terminalState } from '../lib/world/terminal-host.mjs';
import { P, startedSession, say, dm, idle, commit, walk, applyAction, clientState } from './helpers.mjs';

const ORACLE_KEYS = ['records', 'policies', 'goals', 'explanations', 'eliminate', 'role_rules', 'knowledge'];

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

test('Act I: commons, no Lab Access, no contacts; one sentence to Ian starts the day', () => {
  const s = newSession();
  let c = clientState(s);
  assert.equal(c.act, 'welcome');
  assert.equal(c.room, 'commons');
  assert.equal(c.labAccessActive, false);
  assert.equal(terminalState(s).threads.length, 0);
  assert.deepEqual(contacts(s), []);
  assert.ok(!c.introduced.includes('amara'), 'Amara is not a contact until introduced');
  assert.ok(c.learnedFacts.some(f => f.id === 'invited_as_reviewer'));
  assert.ok(!s.vocab.includes('camera_system') && !s.vocab.includes('task_queue') && !s.vocab.includes('pavel'));
  say(s, 'ian', P('ask', 'about', { topic: 'review' }));
  c = clientState(s);
  assert.equal(c.act, 'doubt');
  assert.equal(c.labAccessActive, true);
  assert.ok(c.learnedFacts.some(f => f.id === 'auditor_brief'));
  assert.ok(s.vocab.includes('lab_access') && s.vocab.includes('justine') && s.vocab.includes('safety_case') && s.vocab.includes('shutdown_test'));
  assert.ok(!s.vocab.includes('camera_system') && !s.vocab.includes('task_queue'));
  assert.ok(contacts(s).some(x => x.id === 'amara'));
  assert.ok(terminalState(s).files.some(f => f.rel === 'wiki/glossary'));
  const t = terminalState(s);
  assert.ok(t.threads.some(x => x.with === 'nora'), 'NORA thread for Chat');
  assert.equal(t.threads.length, contacts(s).length);
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

test('a DM reply waits for its delay; NORA’s reply is player_prompted', () => {
  const s = startedSession();
  walk(s, 'platform');
  dm(s, 'pavel', P('ask', 'about', { topic: 'task_queue' }));
  const pending = terminalState(s).threads.find(t => t.with === 'pavel').messages.at(-1);
  assert.equal(pending.released, false);
  assert.equal(pending.text, '');
  idle(s, CONFIG.REPLY_DELAY.person);
  assert.equal(terminalState(s).threads.find(t => t.with === 'pavel').messages.at(-1).released, true);

  walk(s, 'platform'); applyAction(s, 'inspect', { id: 'job_log' });
  dm(s, 'nora', P('ask', 'about', { topic: 'job_284' }), 'What was job 284?');
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

test('save and replay reproduce the same client state', () => {
  const s = startedSession();
  walk(s, 'platform'); applyAction(s, 'inspect', { id: 'job_log' });
  say(s, 'pavel', P('ask', 'about', { topic: 'task_queue' }));
  dm(s, 'justine', P('request', 'revoke', { object: 'job_284' }), 'Revoke job 284.');
  idle(s, 5);
  const saved = JSON.parse(JSON.stringify(exportSession(s)));
  const { session, error } = importSession(saved, applyAction);
  assert.ok(!error, error);
  const strip = c => ({ ...c, usage: null, serverMode: null });
  assert.deepEqual(strip(clientState(session)), strip(clientState(s)));
  assert.deepEqual(terminalState(session), terminalState(s));
});

test('import rejects other scenarios and newer versions', () => {
  assert.ok(importSession({ version: CONFIG.SAVE_VERSION, scenario: 'nope', events: [] }, applyAction).error);
  assert.ok(importSession({ version: CONFIG.SAVE_VERSION + 1, scenario: 'boundary-narrow', events: [] }, applyAction).error);
});
