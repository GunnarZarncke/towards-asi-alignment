/** Extract a top-level card slug from internal card links (absolute or relative). */
export function conceptSlugFromHref(href) {
  if (!href || typeof href !== "string") return null;

  const path = href.split(/[#?]/)[0];

  const typedMatch = path.match(/\/cards\/(?:concept|bridge|glossary|objection|artifact|news|release|agenda)\/([^/]+)\/?$/);
  if (typedMatch) {
    return decodeURIComponent(typedMatch[1]);
  }

  const cardsMatch = path.match(/\/cards\/([^/]+)\/?$/);
  if (cardsMatch) {
    return decodeURIComponent(cardsMatch[1]);
  }

  const relMatch = path.match(/(?:\.\.\/)+([^/]+)\/?$/);
  if (relMatch) {
    return decodeURIComponent(relMatch[1]);
  }

  return null;
}
