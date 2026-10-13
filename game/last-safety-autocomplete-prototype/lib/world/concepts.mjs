import { CONCEPT_LINKS } from './concepts.generated.mjs';

/** Scene trigger key → { summary, href } or null. Ending triggers share the decision card. */
export function conceptFor(key) {
  const hit = CONCEPT_LINKS[key] || (String(key).startsWith('ending:') ? CONCEPT_LINKS['act:decision'] : null);
  return hit ? { summary: hit.summary, href: hit.href } : null;
}
