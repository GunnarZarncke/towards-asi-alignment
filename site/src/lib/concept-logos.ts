import conceptLogos from "../data/concept-logos.json";

const slugSet = new Set(conceptLogos.slugs);

/** True when a square concept logo SVG exists for this card slug. */
export function hasConceptLogo(slug: string): boolean {
  return slugSet.has(slug);
}

/** Extract a top-level card slug from internal card links (absolute or relative). */
export function conceptSlugFromHref(href: string): string | null {
  const path = href.split(/[#?]/)[0];

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

export const conceptLogoSlugs: readonly string[] = conceptLogos.slugs;
