import test from 'node:test';
import assert from 'node:assert/strict';
import {
  PACK_ORDER,
  renderDocument,
  renderDocumentSource,
  includeAfterPack,
  getDocumentByDocId,
} from '../lib/documents.mjs';

test('pack order matches incident table length', () => {
  assert.equal(PACK_ORDER.length, 5);
  assert.equal(PACK_ORDER[0], 'boundary-narrow');
});

test('includeAfterPack is strict later-than', () => {
  assert.equal(includeAfterPack('boundary-narrow', 'boundary-narrow'), false);
  assert.equal(includeAfterPack('boundary-narrow', 'named-path'), true);
  assert.equal(includeAfterPack('false-positive', 'eval-conditioned'), false);
});

test('SEC-ARCH-04 boundary-narrow omits job-outlives-process include', () => {
  const text = renderDocument('sec-arch-04', 'boundary-narrow');
  assert.match(text, /SEC-ARCH-04/);
  assert.doesNotMatch(text, /Stopping a model process does not, by itself, guarantee/);
  assert.match(text, /Lab Access binding/);
});

test('SEC-ARCH-04 named-path adds boundary-narrow includes only', () => {
  const text = renderDocument('sec-arch-04', 'named-path');
  assert.match(text, /Stopping a model process does not/);
  assert.doesNotMatch(text, /not, by itself, evidence about the others/);
});

test('SEC-ARCH-04 goodhart adds named-path includes', () => {
  const text = renderDocument('sec-arch-04', 'goodhart');
  assert.match(text, /not, by itself, evidence about the others/);
});

test('infer spans survive in first pack', () => {
  const text = renderDocument('sec-arch-04', 'boundary-narrow');
  assert.match(text, /NORA Operations may submit work to the laboratory's execution service/);
  assert.doesNotMatch(text, /<!--\s*infer/);
});

test('authoring block and exec-never do not appear in served text', () => {
  const text = renderDocument('sec-arch-04', 'false-positive');
  assert.doesNotMatch(text, /Lean must/);
  assert.doesNotMatch(text, /exec-never/);
});

test('catalog lookup by doc id', () => {
  const d = getDocumentByDocId('SEC-ARCH-04');
  assert.equal(d?.slug, 'sec-arch-04');
  assert.equal(d?.leanKnowledge, false);
});

test('renderDocumentSource handles inline include fragments', () => {
  const src = 'v1.0<!-- include after-boundary-narrow -->.5<!-- /include --> end';
  assert.equal(renderDocumentSource(src, 'boundary-narrow'), 'v1.0 end');
  assert.equal(renderDocumentSource(src, 'named-path'), 'v1.0.5 end');
});
