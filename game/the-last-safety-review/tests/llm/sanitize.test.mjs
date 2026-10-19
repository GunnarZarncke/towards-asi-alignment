import test from 'node:test';
import assert from 'node:assert/strict';
import { sanitizeParseResponse, preparePlayerUtterance, parseModelParseOutput } from '../../lib/llm.mjs';
import { MAX_CLAUSES } from '../../lib/parse-sequence.mjs';
import { CONFIG } from '../../lib/world/config.mjs';

test('sanitizeParseResponse drops entity ids outside vocabulary', () => {
  const out = sanitizeParseResponse({
    clauses: [{
      kind: 'ask',
      relation: 'about',
      subject: 'hidden_job',
      object: 'ian',
      recipient: null,
      evidence: null,
      topic: null,
      open_slot: 'none',
      unfinished: '',
      open_content: '',
      confidence: 0.9,
      clause_text: 'test',
      source: 'llm',
    }],
  }, ['ian']);
  assert.equal(out.subject, null);
  assert.equal(out.object, 'ian');
});

test('sanitizeParseResponse caps clause count and unwraps a single clause', () => {
  const clauses = Array.from({ length: MAX_CLAUSES + 2 }, (_, i) => ({
    kind: 'ask',
    relation: 'about',
    subject: 'ian',
    object: null,
    recipient: null,
    evidence: null,
    topic: null,
    open_slot: 'none',
    unfinished: '',
    open_content: String(i),
    confidence: 1,
    clause_text: `c${i}`,
    source: 'llm',
  }));
  const multi = sanitizeParseResponse({ clauses }, ['ian']);
  assert.ok(multi.clauses);
  assert.equal(multi.clauses.length, MAX_CLAUSES);
  const one = sanitizeParseResponse({ clauses: [clauses[0]] }, ['ian']);
  assert.ok(!one.clauses);
  assert.equal(one.kind, 'ask');
});

test('sanitizeParseResponse maps unknown kind to unintelligible', () => {
  const out = sanitizeParseResponse({
    clauses: [{
      kind: 'teleport',
      relation: 'about',
      subject: null,
      object: null,
      recipient: null,
      evidence: null,
      topic: null,
      open_slot: 'none',
      unfinished: '',
      open_content: '',
      confidence: 1,
      clause_text: '',
      source: 'llm',
    }],
  }, []);
  assert.equal(out.kind, 'unintelligible');
});

test('parseModelParseOutput returns null on invalid JSON', () => {
  assert.equal(parseModelParseOutput('{not json', ['ian']), null);
});

test('preparePlayerUtterance strips disallowed characters and caps length', () => {
  const raw = 'Hello<script>world ' + 'x'.repeat(CONFIG.SENTENCE_CAP + 40);
  const out = preparePlayerUtterance(raw);
  assert.ok(!out.includes('<'));
  assert.ok(out.length <= CONFIG.SENTENCE_CAP);
});
