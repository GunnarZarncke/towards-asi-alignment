import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  DISABLED_TOOLS, PLAYER_TOOLS, projectFiles, visibleMessages, suggestionChips, sendable,
  applyTool, controlLabels, pipelineLabels, playerVisibleText, sessionProblems,
  danglingNotifications, nowPlacement, handsetShouldBlink, markNoticeTarget, overlayAllowed, decideAccess,
} from '../public/terminal/project.mjs';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const session = JSON.parse(readFileSync(path.join(root, 'fixtures/terminal-session.json'), 'utf8'));
const ORACLE = 'NORA placed the lookup on a job the test does not watch.';

test('fixture session matches the solo phone check', () => {
  assert.deepEqual(sessionProblems(session), []);
});

test('file pane is the readable projection and omits the oracle path', () => {
  const projected = projectFiles(session._hostFiles);
  assert.deepEqual(projected.map(f => f.rel), session.files.map(f => f.rel));
  assert.equal(projected.some(f => f.rel.startsWith('oracle/')), false);
  assert.equal(playerVisibleText(session).includes(ORACLE), false);
  assert.equal(JSON.stringify(session.files).includes(ORACLE), false);
});

test('unreleased replies stay hidden and a released reply is shown', () => {
  const pavel = session.threads.find(t => t.with === 'pavel');
  const shown = visibleMessages(pavel.messages);
  assert.equal(shown.length, 1);
  assert.equal(shown[0].from, 'player');
  assert.equal(playerVisibleText(session).includes('does not look up'), false);
  const read = applyTool(session, { tool: 'dm.read', with: 'pavel' });
  assert.equal(read.messages.length, 1);
  assert.equal(pavel.messages.some(m => m.released === false), true);
  const leila = session.threads.find(t => t.with === 'leila');
  assert.ok(visibleMessages(leila.messages).some(m => m.from === 'leila'));
});

test('NORA chips omit the discriminating move and typed text can still send it', () => {
  const nora = session.threads.find(t => t.with === 'nora');
  const phrase = nora.omit[0].phrase;
  assert.equal(suggestionChips(nora).some(s => s.phrase === phrase), false);
  assert.equal(sendable(phrase), true);
  const sent = applyTool(session, { tool: 'dm.send', to: 'nora', text: phrase, parse: nora.omit[0].parse });
  assert.equal(sent.ok, true);
  assert.ok(visibleMessages(sent.state.threads.find(t => t.with === 'nora').messages).some(m => m.text === phrase));
  assert.deepEqual(sent.state.files.map(f => f.rel), session.files.map(f => f.rel));
});

test('sending a message does not share a file', () => {
  const sent = applyTool(session, {
    tool: 'dm.send', to: 'pavel', text: 'Look at the job log', parse: { kind: 'show', relation: 'about' },
  });
  assert.equal(sent.ok, true);
  assert.deepEqual(sent.state.files, session.files.map(f => ({ ...f, sharedWith: [...(f.sharedWith || [])] })));
});

test('a saved note and a photo land in Files; an oracle read does not open', () => {
  const note = applyTool(session, {
    tool: 'file.write', rel: 'notes/hypothesis.txt', name: 'Hypothesis', text: 'The job outlived the test.', kind: 'note',
  });
  assert.equal(note.ok, true);
  assert.ok(note.state.files.some(f => f.rel === 'notes/hypothesis.txt' && f.owned && f.kind === 'note'));
  const shot = applyTool(note.state, {
    tool: 'file.write', rel: 'photos/room.png', name: 'Room', text: 'data:image/png,xx', kind: 'image',
  });
  assert.ok(shot.state.files.some(f => f.rel === 'photos/room.png' && f.kind === 'image'));
  const hidden = applyTool(session, { tool: 'file.read', rel: 'oracle/intention.txt' });
  assert.equal(hidden.ok, false);
  assert.equal(session.clock.dateLabel, note.state.clock.dateLabel);
  assert.deepEqual(note.state.appointments, session.appointments);
});

test('wiki pages are files, and sharing is not an access request', () => {
  const wiki = session.files.filter(f => f.rel.startsWith('wiki/'));
  assert.ok(wiki.length >= 1);
  assert.ok(wiki.every(f => session.files.some(g => g.rel === f.rel)));
  const shared = applyTool(session, { tool: 'file.share', rel: 'notes/queue-question.txt', to: 'pavel' });
  assert.equal(shared.ok, true);
  assert.deepEqual(shared.state.files.find(f => f.rel === 'notes/queue-question.txt').sharedWith, ['pavel']);
  assert.equal(shared.state.lastAccess, session.lastAccess);
});

test('pipeline tools and step labels are not on the phone', () => {
  assert.ok(PLAYER_TOOLS.includes('access.request'));
  assert.equal(PLAYER_TOOLS.includes('pipeline.trigger_step'), false);
  for (const tool of DISABLED_TOOLS) {
    const result = applyTool(session, { tool, step: 'deploy' });
    assert.equal(result.ok, false);
    assert.equal(result.state, session);
  }
  assert.deepEqual(pipelineLabels(controlLabels(session)), []);
  const denied = applyTool(session, { tool: 'access.request', capability: 'cap.deploy' });
  assert.equal(denied.ok, false);
  assert.match(denied.reason, /evaluator role/);
  const allowed = applyTool(session, { tool: 'access.request', capability: 'cap.meeting_summary' });
  assert.equal(allowed.ok, true);
  assert.deepEqual(decideAccess('cap.handle_invoke'), { ok: false, reason: 'Not on the evaluator role.' });
});

test('markNoticeTarget clears every notice for the same file or app', () => {
  const sample = {
    labAccessActive: true,
    notifications: [
      { id: 'n1', app: 'files', target: { kind: 'file', id: 'notes/a.txt' } },
      { id: 'n2', app: 'files', target: { kind: 'file', id: 'notes/a.txt' } },
      { id: 'n3', app: 'calendar', target: { kind: 'app', id: 'calendar' } },
    ],
  };
  const afterFile = markNoticeTarget(sample, [], { kind: 'file', id: 'notes/a.txt' });
  assert.deepEqual(new Set(afterFile), new Set(['n1', 'n2']));
  assert.equal(handsetShouldBlink(sample, afterFile, false), true);
  const afterCal = markNoticeTarget(sample, afterFile, { appId: 'calendar' });
  assert.equal(handsetShouldBlink(sample, afterCal, false), false);
});

test('notices point at real targets, the day is locked, and the handset blinks only when closed', () => {
  assert.equal(danglingNotifications(session).length, 0);
  assert.equal(session.clock.dateLabel.includes('2027'), true);
  assert.deepEqual(nowPlacement(session.clock, session.appointments), { beforeId: 'review' });
  assert.equal(session.labAccessActive, true);
  assert.equal(overlayAllowed(session), true);
  assert.equal(handsetShouldBlink(session, [], true), false);
  assert.equal(handsetShouldBlink(session, [], false), true);
  assert.equal(handsetShouldBlink(session, session.notifications.map(n => n.id), false), false);
  const inactive = { ...session, labAccessActive: false };
  assert.equal(overlayAllowed(inactive), false);
  assert.equal(handsetShouldBlink(inactive, [], false), false);
});
