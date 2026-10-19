import test from 'node:test';
import assert from 'node:assert/strict';
import { isOpenAsk, responseCandidates, openAskHintMove } from '../lib/world/npcs.mjs';
import { clientState } from '../lib/game.mjs';
import { P, startedSession, walk, applyAction, say } from './helpers.mjs';

test('isOpenAsk: grounded ask is not open', () => {
  assert.equal(isOpenAsk(P('ask', 'about', { topic: 'review' })), false);
  assert.equal(isOpenAsk(P('ask', 'has_access', { subject: 'nora', object: 'camera_system' })), false);
});

test('isOpenAsk: ungrounded ask and ask_why', () => {
  assert.equal(isOpenAsk(P('ask', 'about')), true);
  assert.equal(isOpenAsk(P('ask', 'open', { open_content: 'what to do next' })), true);
  assert.equal(isOpenAsk(P('ask_why', 'about')), true);
  assert.equal(isOpenAsk(P('social', 'open')), false);
});

test('open ask prefers goal question when when-pred holds', () => {
  const s = startedSession();
  walk(s, 'evaluation');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
  walk(s, 'platform');
  const hint = openAskHintMove(s, 'pavel', P('ask', 'about'));
  assert.equal(hint?.type, 'ask');
  assert.equal(hint?.hintOnly, true);
  assert.equal(hint?.goal, 'pavel.two_objects');
  assert.equal(hint?.about, 'task_queue');
});

test('open ask response does not set pendingQuestion', () => {
  const s = startedSession();
  walk(s, 'evaluation');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
  walk(s, 'platform');
  say(s, 'pavel', P('ask', 'about'), 'What should I look at?');
  assert.equal(s.npcs.pavel.pendingQuestion, null);
  assert.equal(clientState(s).pendingQuestion, null);
});

test('open ask with no hint falls back to refer or work', () => {
  const s = startedSession();
  walk(s, 'model');
  const moves = responseCandidates(s, 'jun', P('ask', 'about'));
  assert.ok(['refer', 'work', 'hint_ask', 'ask', 'share'].includes(moves[0]?.type));
  assert.notEqual(moves[0]?.type, 'catchall');
});
