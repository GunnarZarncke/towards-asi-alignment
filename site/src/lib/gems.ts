import partGems from "../data/part-gems.json";
import fieldProjectionGems from "../data/field-projection-gems.json";

export const GEM_LABEL = "gem" as const;

export const GEM_META = {
  title: "Gem",
  description:
    "Highlighted companion cards — one anchor per book part plus field-projection formula cards in the bridge crosswalk."
};

/** All card slugs that carry the gem badge (part highlights + field projections). */
export const ALL_GEM_SLUGS = [
  ...new Set([...Object.values(partGems).flat(), ...fieldProjectionGems])
];

const gemSlugSet = new Set(ALL_GEM_SLUGS);

export function isGemSlug(slug: string): boolean {
  return gemSlugSet.has(slug);
}

export function badgeGemHref(base: string) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}badges/gem/`;
}

export { partGems, fieldProjectionGems };
