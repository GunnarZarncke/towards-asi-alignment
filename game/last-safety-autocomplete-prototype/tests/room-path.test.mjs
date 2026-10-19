import test from 'node:test';
import assert from 'node:assert/strict';
import { roomPath, STAFF_ENTRY, transitStep } from '../lib/world/room-path.mjs';
import { initNpcs } from '../lib/world/npcs.mjs';

test('staff enter through commons on the way to distant desks', () => {
  const p = roomPath(STAFF_ENTRY, 'security');
  assert.ok(p);
  assert.equal(p[0], 'commons');
  assert.equal(p.at(-1), 'security');
  assert.deepEqual(roomPath('commons', 'collab'), ['commons', 'collab']);
});

test('transitStep walks one edge per call from absent to desk', () => {
  const npcs = initNpcs();
  const n = npcs.daniel;
  let r = transitStep(n, 'collab', 'body');
  assert.equal(r.room, 'commons');
  n.room = 'commons';
  n.presence = 'body';
  r = transitStep(n, 'collab', 'body');
  assert.equal(r.room, 'collab');
  n.room = 'collab';
  r = transitStep(n, 'collab', 'body');
  assert.equal(r.room, 'collab');
  assert.equal(n.transit, null);
});
