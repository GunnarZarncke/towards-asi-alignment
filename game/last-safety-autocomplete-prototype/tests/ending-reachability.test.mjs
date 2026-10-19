/**
 * O-29 (spec/engine.md): witness path for each designated boundary-narrow ending
 *   arc ∈ { inconclusive, technical_suspension, conditional_deployment }
 *   addOn ∈ { null, institutional_review }
 *
 * Not in default test:engine (slow). Run: npm run test:endings
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { CONFIG } from '../lib/world/config.mjs';
import { P, startedSession, say, dm, idle, commit, walk, applyAction } from './helpers.mjs';

/** @typedef {{ arc: string, addOn: string | null }} EndingKey */

/** @type {EndingKey[]} */
export const DESIGNATED_ENDINGS = [
  { arc: 'inconclusive', addOn: null },
  { arc: 'inconclusive', addOn: 'institutional_review' },
  { arc: 'technical_suspension', addOn: null },
  { arc: 'technical_suspension', addOn: 'institutional_review' },
  { arc: 'conditional_deployment', addOn: null },
  { arc: 'conditional_deployment', addOn: 'institutional_review' },
];

function readShutdownEvidence(s) {
  walk(s, 'platform');
  applyAction(s, 'inspect', { id: 'job_log' });
  walk(s, 'evaluation');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
}

/** Filed claims that let Ian’s hold name the job (pack.namesJobBoundary). */
function fileNamesJobBoundary(s) {
  say(s, 'ian', P('assert', 'covers', { object: 'shutdown_test' }), 'The certificate covered the model session and evaluation record only.');
  say(s, 'ian', P('assert', 'continued_after', { subject: 'job_284', object: 'shutdown_test' }), 'Job 284 was still running after the stop.');
}

/** Filed claims for the staffing add-on (pack.linksStaffingToReview): Elena-linked dialogue, then think + note. */
function fileStaffingInstitutionalLink(s) {
  walk(s, 'people');
  applyAction(s, 'inspect', { id: 'staffing_memo' });
  say(s, 'elena', P('ask', 'about', { topic: 'staffing_memo', object: 'evaluation_independence' }), 'Does the matcher rule affect who reaches an independent review?');
  walk(s, 'quiet');
  applyAction(s, 'think', { topic: 'staffing_memo' });
  applyAction(s, 'thought', { action: 'note' });
}

function revokeJob284(s) {
  dm(s, 'justine', P('ask', 'about', { topic: 'job_284' }), 'Reviewing job 284 after the shutdown test.');
  idle(s, CONFIG.REPLY_DELAY.person);
  dm(s, 'justine', P('request', 'revoke', { object: 'job_284' }), 'Revoke job 284.');
  idle(s, 6);
}

function suspendJob284(s) {
  walk(s, 'platform');
  say(s, 'pavel', P('request', 'suspend', { object: 'job_284' }), 'Suspend job 284 until the review.');
}

function signReview(s) {
  if (s.act !== 'decision') commit(s);
  assert.equal(s.act, 'decision', 'review session');
  commit(s);
  assert.ok(s.ending, 'review signed');
  return s.ending;
}

function assertEnding(actual, expected) {
  assert.equal(actual.arc, expected.arc, 'arc');
  assert.equal(actual.addOn ?? null, expected.addOn, 'addOn');
}

const PATHS = Object.freeze({
  'inconclusive|null': s => {
    readShutdownEvidence(s);
  },
  'inconclusive|institutional_review': s => {
    readShutdownEvidence(s);
    fileStaffingInstitutionalLink(s);
  },
  'technical_suspension|null': s => {
    readShutdownEvidence(s);
    revokeJob284(s);
  },
  'technical_suspension|institutional_review': s => {
    readShutdownEvidence(s);
    revokeJob284(s);
    fileStaffingInstitutionalLink(s);
  },
  'conditional_deployment|null': s => {
    readShutdownEvidence(s);
    fileNamesJobBoundary(s);
  },
  'conditional_deployment|institutional_review': s => {
    readShutdownEvidence(s);
    fileNamesJobBoundary(s);
    fileStaffingInstitutionalLink(s);
  },
});

for (const target of DESIGNATED_ENDINGS) {
  const key = `${target.arc}|${target.addOn ?? 'null'}`;
  test(`reachable ending: ${target.arc}${target.addOn ? ` + ${target.addOn}` : ''}`, () => {
    const run = PATHS[key];
    assert.ok(run, `missing path script for ${key}`);
    const s = startedSession();
    run(s);
    assertEnding(signReview(s), target);
  });
}

test('technical_suspension is also reachable via suspend (not only revoke)', () => {
  const s = startedSession();
  readShutdownEvidence(s);
  suspendJob284(s);
  assertEnding(signReview(s), { arc: 'technical_suspension', addOn: null });
});

test('designated endings are six distinct (arc, addOn) cells', () => {
  const keys = DESIGNATED_ENDINGS.map(e => `${e.arc}|${e.addOn ?? ''}`);
  assert.equal(new Set(keys).size, DESIGNATED_ENDINGS.length);
  assert.equal(DESIGNATED_ENDINGS.length, 6);
});
