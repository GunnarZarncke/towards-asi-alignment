import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, cleanParse } from '../lib/game.mjs';
import { demoParse } from '../lib/llm.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import { makeParse } from '../lib/grammar.mjs';

test('demo parser always returns a single clause', () => {
  const p = demoParse('Does Ian know about the review and show Ian the job log', ['ian', 'review']);
  assert.ok(!p.clauses);
});

test('respond sequences LLM clauses, not completion', () => {
  const s = newSession();
  const hi = cleanParse(demoParse('Hi', s.vocab), s);
  const ask = cleanParse(demoParse('Can Ian know about the review?', s.vocab), s);
  applyAction(s, 'respond', {
    parse: { ...hi, source: 'llm', clauses: [{ ...hi, clause_text: 'Hi', source: 'llm' }, { ...ask, clause_text: 'Can Ian know about the review?', source: 'llm' }] },
    addressee: 'ian',
    text: 'Hi. Can Ian know about the review?',
  });
  const playerLines = s.conversations.filter(x => x.role === 'player');
  assert.equal(playerLines.length, 2);
});

test('completion with embedded clauses still runs once', () => {
  const s = newSession();
  const p = cleanParse(makeParse({ kind: 'social', relation: 'open', open_slot: 'none', source: 'completion' }), s);
  const extra = cleanParse(demoParse('Can Ian know about the review?', s.vocab), s);
  applyAction(s, 'respond', {
    parse: { ...p, clauses: [p, extra] },
    addressee: 'ian',
    text: 'Hi',
  });
  assert.equal(s.conversations.filter(x => x.role === 'player').length, 1);
});

test('multi-clause sequence rolls back when a later clause errors', () => {
  const s = newSession();
  const fuelBefore = s.fuelSpent;
  const convBefore = s.conversations.length;
  const hi = cleanParse(makeParse({ kind: 'social', relation: 'open', open_slot: 'none', source: 'llm' }), s);
  const think = cleanParse(makeParse({ kind: 'think', relation: 'about', topic: 'review', open_slot: 'none', source: 'llm' }), s);
  const r = applyAction(s, 'respond', {
    parse: { ...hi, source: 'llm', clauses: [{ ...hi, clause_text: 'Hi', source: 'llm' }, { ...think, clause_text: 'Think about the review', source: 'llm' }] },
    addressee: 'ian',
    text: 'Hi. Think about the review',
  });
  assert.ok(r.error);
  assert.equal(s.fuelSpent, fuelBefore);
  assert.equal(s.conversations.length, convBefore);
});

test('multi-clause player lines omit internal signatures when clause_text is missing', () => {
  const s = newSession();
  const hi = cleanParse(makeParse({ kind: 'social', relation: 'open', open_slot: 'none', source: 'llm' }), s);
  const ask = cleanParse(demoParse('Can Ian know about the review?', s.vocab), s);
  applyAction(s, 'respond', {
    parse: {
      ...hi,
      source: 'llm',
      clauses: [
        { ...hi, clause_text: 'Hi', source: 'llm' },
        { ...ask, clause_text: 'Can Ian know about the review?', source: 'llm' },
      ],
    },
    addressee: 'ian',
    text: 'Hi. Can Ian know about the review?',
  });
  const playerLines = s.conversations.filter(x => x.role === 'player').map(x => x.text);
  assert.equal(playerLines.length, 2);
  assert.ok(!playerLines.some(t => t.includes('|')));
});
