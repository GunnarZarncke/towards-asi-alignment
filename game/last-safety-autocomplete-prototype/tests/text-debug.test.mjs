import test from 'node:test';
import assert from 'node:assert/strict';
import { kbSnapshot, kbDelta } from '../lib/text/kb-debug.mjs';

test('kbDelta reports new learned facts and entities', () => {
  const before = kbSnapshot({
    learnedFacts: [{ id: 'a', text: 'A', provenance: 'recorded_before', from: null, refs: [] }],
    entities: { a: {}, x: {} },
    examined: [],
    heard: [],
    introduced: [],
  });
  const after = kbSnapshot({
    learnedFacts: [
      { id: 'a', text: 'A', provenance: 'recorded_before', from: null, refs: [] },
      { id: 'b', text: 'B happened', provenance: 'staff_action', from: 'ian', refs: ['x'] },
    ],
    entities: { a: {}, x: {}, y: {} },
    examined: ['screen1'],
    heard: [{ id: 'b', from: 'ian' }],
    introduced: ['ian'],
  });
  const lines = kbDelta(before, after);
  assert.ok(lines.some(l => l.includes('+ fact b:')));
  assert.ok(lines.some(l => l.includes('staff_action')));
  assert.ok(lines.some(l => l.includes('+ entity visible: y')));
  assert.ok(lines.some(l => l.includes('+ examined screen: screen1')));
});
