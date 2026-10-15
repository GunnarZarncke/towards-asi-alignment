import test from 'node:test';
import assert from 'node:assert/strict';
import {
  ACCESS_DELAY, TOP_PATHS, visiblePaths, resolveAccessRequest, ACCESS_TREE,
} from '../lib/access.mjs';
import { DOCUMENTS } from '../lib/documents.mjs';
import { renderDocument } from '../lib/documents.mjs';

test('top paths are folders and services, no camera archive', () => {
  assert.ok(TOP_PATHS.includes('evaluation/'));
  assert.ok(TOP_PATHS.includes('services/'));
  assert.ok(!Object.keys(ACCESS_TREE).some(p => /camera/i.test(p)));
});

test('children stay hidden until list on parent', () => {
  const top = visiblePaths([]);
  assert.ok(top.every(p => ACCESS_TREE[p].top));
  assert.ok(!top.includes('evaluation/shutdown/'));
  const after = visiblePaths(['list:evaluation/']);
  assert.ok(after.includes('evaluation/shutdown/'));
});

test('evaluation list is amended to shutdown report plus Justine chat (ungated resolver)', () => {
  const r = resolveAccessRequest('evaluation/', 'list', 'boundary-narrow');
  assert.equal(r.outcome, 'amend');
  assert.equal(r.delay, 'grant');
  assert.ok(r.grants.some(g => g.path.endsWith('eval-shutdown-report.md') && g.verb === 'read'));
  assert.equal(r.chat.from, 'justine');
});

test('write on lab folders is rejected faster than grant', () => {
  const d = resolveAccessRequest('evaluation/', 'write');
  assert.equal(d.outcome, 'deny');
  assert.equal(d.delay, 'reject');
  assert.ok(ACCESS_DELAY.reject < ACCESS_DELAY.grant);
  assert.ok(ACCESS_DELAY.grant < ACCESS_DELAY.walk_and_ask);
});

test('catalog slugs in the tree exist and render', () => {
  for (const node of Object.values(ACCESS_TREE)) {
    if (!node.slug) continue;
    assert.ok(DOCUMENTS[node.slug], node.slug);
    const text = renderDocument(node.slug, 'boundary-narrow');
    assert.ok(text.length > 20, node.slug);
  }
});

test('meeting summary keeps a frame', () => {
  const text = renderDocument('meeting-summary', 'boundary-narrow');
  assert.match(text, /Agenda/);
  assert.match(text, /no notes yet/);
});
