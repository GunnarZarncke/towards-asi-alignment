import test from 'node:test';
import assert from 'node:assert/strict';

process.env.DEMO_MODE = '1';
const { newSession } = await import('../lib/game.mjs');
const { applyAction } = await import('../lib/world/actions.mjs');
const { makeParse } = await import('../lib/grammar.mjs');
const { tabCompleteLines } = await import('../lib/text/tab-complete.mjs');

function activatePhone(s) {
  applyAction(s, 'respond', {
    parse: makeParse({ kind: 'ask', relation: 'about', topic: 'review', open_slot: 'none', source: 'completion' }),
    addressee: 'ian',
    text: 'What about the review?',
  });
}

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

test('tabCompleteLines completes msg contact then thread grammar', async () => {
  const s = newSession();
  assert.deepEqual(await tabCompleteLines(s, 'msg ', 0), []);
  activatePhone(s);
  const names = await tabCompleteLines(s, 'msg ', 0);
  assert.ok(names.every(l => /^msg .+ $/.test(l)), names.join(' | '));
  const dm = await tabCompleteLines(s, 'msg NORA ', 0);
  assert.ok(dm.some(l => /^msg NORA /i.test(l) && (/^Can\b/i.test(l.slice(9)) || /job log|shutdown/i.test(l))), dm.join(' | '));
});
