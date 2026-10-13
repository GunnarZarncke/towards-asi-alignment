import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { ROOMS, EDGES, doorsOn, reachable, passageError } from '../lib/floorplan.mjs';
import { LAYOUTS, layoutFor } from '../public/render/layouts.mjs';

const OPP = { back: 'front', front: 'back', left: 'right', right: 'left' };

function overlap(a, b) {
  return Math.abs(a.at - b.at) < (a.w + b.w) / 2 - 1e-6;
}

test('rooms tile the 22 × 17 m envelope and the drawing names each one', () => {
  const area = Object.values(ROOMS).reduce((sum, room) => sum + room.w * room.d, 0);
  assert.ok(Math.abs(area - 22 * 17) < 1e-6, area);
  const svg = readFileSync(new URL('../public/floorplan.svg', import.meta.url), 'utf8');
  const ids = [...svg.matchAll(/data-room="([^"]+)"/g)].map(m => m[1]).sort();
  assert.deepEqual(ids, Object.keys(ROOMS).sort());
});

test('every door sits on both rooms, on opposite sides, and inside the wall', () => {
  assert.equal(EDGES.length, 16);
  for (const edge of EDGES) {
    const a = doorsOn(edge.a).find(d => d.to === edge.b);
    const b = doorsOn(edge.b).find(d => d.to === edge.a);
    assert.ok(a && b, `${edge.a}–${edge.b}`);
    assert.equal(b.wall, OPP[a.wall], `${edge.a}–${edge.b}`);
    assert.equal(a.required, edge.required);
    for (const [id, door] of [[edge.a, a], [edge.b, b]]) {
      const room = ROOMS[id];
      const span = door.wall === 'left' || door.wall === 'right' ? room.d : room.w;
      assert.ok(Math.abs(door.at) + door.w / 2 <= span / 2 + 1e-6, `${id} ${door.wall} ${door.to}`);
    }
  }
  for (const id of Object.keys(ROOMS)) {
    const byWall = new Map();
    for (const door of doorsOn(id)) {
      const list = byWall.get(door.wall) || [];
      list.push(door);
      byWall.set(door.wall, list);
    }
    for (const list of byWall.values()) {
      for (let i = 0; i < list.length; i++)
        for (let j = i + 1; j < list.length; j++)
          assert.equal(overlap(list[i], list[j]), false, `${id} ${list[i].to}/${list[j].to}`);
    }
  }
});

test('clearance 2 walks the staffed rooms and leaves the secure pair shut', () => {
  const at0 = [...reachable(0)].sort();
  assert.deepEqual(at0, ['commons', 'review']);
  const at2 = reachable(2);
  assert.equal(at2.has('platform'), true);
  assert.equal(at2.has('people'), true);
  assert.equal(at2.has('evaluation'), true);
  assert.equal(at2.has('test'), false);
  assert.equal(at2.has('security'), false);
  assert.equal(reachable(3).size, Object.keys(ROOMS).length);
  assert.equal(passageError('platform', 'people', 2), 'No door from here.');
  assert.equal(passageError('platform', 'tech', 2), null);
  assert.equal(passageError('tech', 'test', 2), 'That door needs a higher clearance.');
  assert.equal(passageError('tech', 'nowhere', 2), 'Unknown room.');
});

test('room art uses the plan neighbors, and generated rooms use its metres', () => {
  for (const id of Object.keys(ROOMS)) {
    const layout = layoutFor(id);
    const spec = doorsOn(id);
    assert.deepEqual(layout.doors.map(d => d.to).sort(), spec.map(d => d.to).sort(), id);
    const [W, D] = layout.size;
    for (const door of layout.doors) {
      const span = door.wall === 'left' || door.wall === 'right' ? D : W;
      assert.ok(Math.abs(door.at) + door.w / 2 <= span / 2 + 1e-6, `${id} ${door.to}`);
    }
    for (const wall of ['back', 'left', 'front', 'right']) {
      const doors = layout.doors.filter(d => d.wall === wall);
      const windows = (layout.windows || []).filter(w => w.wall === wall);
      for (const door of doors) for (const win of windows) assert.equal(overlap(door, win), false, `${id} ${wall}`);
    }
    if (!LAYOUTS[id]) {
      const room = ROOMS[id];
      assert.deepEqual(layout.size, [room.w, room.d]);
      for (const door of layout.doors) {
        const match = spec.find(d => d.to === door.to);
        assert.equal(door.wall, match.wall);
        assert.ok(Math.abs(door.at - match.at) < 1e-6);
      }
    }
  }
});
