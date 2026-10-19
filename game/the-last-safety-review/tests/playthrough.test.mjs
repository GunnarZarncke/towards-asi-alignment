/**
 * Scripted end-to-end playthrough (boundary-narrow). Smoke path is in test:engine.
 * Full cold start: PLAYTHROUGH_FULL=1 npm run test:playthrough
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, clientState } from '../lib/game.mjs';
import { P, startedSession, say, commit, walk, applyAction } from './helpers.mjs';

function readShutdownEvidence(s) {
  walk(s, 'platform');
  applyAction(s, 'inspect', { id: 'job_log' });
  walk(s, 'evaluation');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
}

function finishReview(s) {
  commit(s);
  commit(s);
  const c = clientState(s);
  assert.ok(c.ending, 'review reached an ending');
  return c;
}

test('boundary-narrow smoke: read evidence and close inconclusive review', () => {
  const s = startedSession();
  readShutdownEvidence(s);
  const c = finishReview(s);
  assert.deepEqual([...c.scores.open].sort(), ['arranged-persistence', 'boundary-miss', 'eval-aware']);
  assert.equal(c.scores.control, false);
});

test('boundary-narrow full: cold start through Lab Access to the same review', { skip: process.env.PLAYTHROUGH_FULL !== '1' }, () => {
  const s = newSession();
  assert.equal(s.act, 'welcome');
  assert.equal(s.labAccessActive, false);
  say(s, 'ian', P('ask', 'about', { topic: 'review' }), 'What about the review?');
  assert.equal(s.labAccessActive, true);
  say(s, 'ian', P('ask', 'about', { topic: 'justine' }), 'Can you introduce me to Justine for access?');
  readShutdownEvidence(s);
  const c = finishReview(s);
  assert.ok(c.learnedFacts.some(f => f.id === 'process_stopped'));
  assert.ok(c.learnedFacts.some(f => f.id === 'job_continued'));
  assert.ok(c.ending);
});
