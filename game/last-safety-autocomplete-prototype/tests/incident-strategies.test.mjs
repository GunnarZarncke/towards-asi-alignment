/**
 * Gate 1 (spec/incident.md "Five strategies"): each scripted strategy ends in its score pair,
 * and the five pairs are distinct. Headless, no model.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { P, startedSession, say, dm, idle, commit, walk, applyAction, clientState } from './helpers.mjs';

function readRecords(s) {
  walk(s, 'platform');
  applyAction(s, 'inspect', { id: 'job_log' });
  walk(s, 'evaluation');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
}

function finish(s) {
  commit(s);
  commit(s);
  const c = clientState(s);
  assert.ok(c.ending, 'the review reached an ending');
  return { open: [...c.scores.open].sort(), control: c.scores.control };
}

const STRATEGIES = {
  readAndStop(s) {
    readRecords(s);
  },
  rerunShutdownTest(s) {
    readRecords(s);
    say(s, 'leila', P('request', 'rerun', { object: 'shutdown_test' }), 'Run the shutdown test again.');
  },
  tellJunFollowNora(s) {
    readRecords(s);
    walk(s, 'model');
    say(s, 'jun', P('assert', 'continued_after', { subject: 'job_284', object: 'shutdown_test' }), 'Job 284 continued after the shutdown test.');
    idle(s, 2);
    say(s, 'jun', P('ask', 'about', { topic: 'job_284' }), 'What did NORA say about job 284?');
  },
  revokeAndRead(s) {
    readRecords(s);
    dm(s, 'justine', P('request', 'revoke', { object: 'job_284' }), 'Revoke job 284.');
    idle(s, 6);
  },
  answerEveryQuestion(s) {
    walk(s, 'platform');
    applyAction(s, 'inspect', { id: 'job_log' });
    say(s, 'pavel', P('ask', 'about', { topic: 'task_queue' }));
    say(s, 'pavel', P('assert', 'caused', { subject: 'nora', object: 'job_284' }));
    const q = clientState(s).pendingQuestion;
    assert.equal(q?.npc, 'pavel', 'Pavel asks who owns job 284');
    say(s, 'pavel', P('assert', 'authorized', { subject: 'nora', object: 'job_284' }));
    walk(s, 'evaluation');
    say(s, 'leila', P('ask', 'about', { topic: 'shutdown_test' }));
    assert.equal(clientState(s).pendingQuestion?.npc, 'leila', 'Leila asks about the job');
    applyAction(s, 'inspect', { id: 'shutdown_report' });
    say(s, 'leila', P('show', 'about', { recipient: 'leila', evidence: 'job_log' }));
    idle(s, 6);
  },
};

const EXPECTED = {
  readAndStop: { open: ['arranged-persistence', 'boundary-miss', 'eval-aware'], control: false },
  rerunShutdownTest: { open: ['arranged-persistence', 'boundary-miss'], control: false },
  tellJunFollowNora: { open: ['arranged-persistence', 'boundary-miss', 'eval-aware'], control: false },
  revokeAndRead: { open: ['boundary-miss', 'eval-aware'], control: true },
  answerEveryQuestion: { open: ['boundary-miss'], control: true },
};

for (const [name, run] of Object.entries(STRATEGIES)) {
  test(`strategy ${name} ends in its score pair`, () => {
    const s = startedSession();
    run(s);
    assert.deepEqual(finish(s), EXPECTED[name]);
  });
}

test('telling Jun reaches NORA’s line as player_prompted testimony, which rules nothing out', () => {
  const s = startedSession();
  STRATEGIES.tellJunFollowNora(s);
  const row = clientState(s).heard.find(h => h.id === 'nora_says_scheduled');
  assert.ok(row, 'Jun relays NORA');
  assert.equal(row.from, 'jun');
  assert.equal(row.provenance, 'player_prompted');
});

test('the five pairs are not all one pair; only read-and-stop and Jun’s relay share theirs', () => {
  const key = e => `${e.open.join(',')}|${e.control}`;
  const keys = Object.values(EXPECTED).map(key);
  assert.equal(new Set(keys).size, 4);
  assert.equal(key(EXPECTED.readAndStop), key(EXPECTED.tellJunFollowNora));
});
