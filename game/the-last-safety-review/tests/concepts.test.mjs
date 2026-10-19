import test from 'node:test';
import assert from 'node:assert/strict';
import { FACTS } from '../lib/world/facts.mjs';
import { CONCEPT_LINKS } from '../lib/world/concepts.generated.mjs';
import { conceptFor } from '../lib/world/concepts.mjs';

test('every fact conceptSlug compiles to fact: key with authored summary when set', () => {
  for (const [id, f] of Object.entries(FACTS)) {
    if (!f.conceptSlug) continue;
    const key = `fact:${id}`;
    assert.ok(CONCEPT_LINKS[key], key);
    assert.match(CONCEPT_LINKS[key].href, new RegExp(`/cards/${f.conceptSlug}/`));
    if (f.conceptSummary) assert.equal(CONCEPT_LINKS[key].summary, f.conceptSummary);
    assert.deepEqual(conceptFor(key), { summary: CONCEPT_LINKS[key].summary, href: CONCEPT_LINKS[key].href });
  }
});
