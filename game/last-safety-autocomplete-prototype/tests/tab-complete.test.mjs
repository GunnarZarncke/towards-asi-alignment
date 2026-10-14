import test from 'node:test';
import assert from 'node:assert/strict';

process.env.DEMO_MODE = '1';
const { newSession } = await import('../lib/game.mjs');
const { tabCompleteLines } = await import('../lib/text/tab-complete.mjs');

test('tabCompleteLines completes go targets and speech openings', async () => {
  const s = newSession();
  for (const line of ['go', 'go ']) {
    const rooms = await tabCompleteLines(s, line, 0);
    assert.ok(rooms.length > 0, `expected rooms for "${line}"`);
    assert.ok(rooms.every(l => /^go\s+\S/i.test(l)), `bad completion for "${line}": ${rooms[0]}`);
  }
  const prefixed = await tabCompleteLines(s, 'go cour', 0);
  assert.ok(prefixed.some(l => /courtyard/i.test(l)));

  const speech = await tabCompleteLines(s, '', 0);
  assert.ok(speech.some(l => /^Can\b/.test(l.trim()) || /^(Tell me about|Request)\b/.test(l)));
});
