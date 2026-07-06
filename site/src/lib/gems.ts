import partGems from "../data/part-gems.json";
import fieldSubsumptionGems from "../data/field-subsumption-gems.json";

export const GEM_LABEL = "gem" as const;

export const GEM_META = {
  title: "Gem",
  description:
    "Highlighted companion cards — one anchor per book part plus field-subsumption formula cards in the bridge crosswalk."
};

/** All card slugs that carry the gem badge (part highlights + field subsumptions). */
export const ALL_GEM_SLUGS = [
  ...new Set([...Object.values(partGems).flat(), ...fieldSubsumptionGems])
];

const gemSlugSet = new Set(ALL_GEM_SLUGS);

export function isGemSlug(slug: string): boolean {
  return gemSlugSet.has(slug);
}

export function badgeGemHref(base: string) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}badges/gem/`;
}

export { partGems, fieldSubsumptionGems };
