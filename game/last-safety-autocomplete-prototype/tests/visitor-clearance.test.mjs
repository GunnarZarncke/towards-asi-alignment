import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, go } from '../lib/game.mjs';
import { passageError, START_CLEARANCE, HUB_CLEARANCE, VISITOR_CLEARANCE } from '../lib/floorplan.mjs';
import { P, say, applyAction, walk } from './helpers.mjs';

test('doors follow Lab Access and Justine introduction', () => {
  const s = newSession();
  assert.equal(s.clearance, START_CLEARANCE);
  assert.equal(passageError('commons', 'collab', s.clearance), 'That door needs a higher clearance.');
  say(s, 'ian', P('ask', 'about', { topic: 'review' }));
  assert.equal(s.clearance, HUB_CLEARANCE);
  say(s, 'ian', P('ask', 'about', { topic: 'justine' }));
  assert.equal(s.clearance, VISITOR_CLEARANCE);
  assert.equal(walk(s, 'platform').room, 'platform');
});
