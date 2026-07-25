import conceptLogos from "../data/concept-logos.json";

const slugSet = new Set(conceptLogos.slugs);

/** True when a square concept logo SVG exists for this card slug. */
export function hasConceptLogo(slug: string): boolean {
  return slugSet.has(slug);
}

export const conceptLogoSlugs: readonly string[] = conceptLogos.slugs;
