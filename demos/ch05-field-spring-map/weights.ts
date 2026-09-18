/** Live matrix bridge keys (MB8 gravestone excluded). */
export const LIVE_BRIDGES = [
  "MB1",
  "MB2",
  "MB3",
  "MB4",
  "MB4a",
  "MB5",
  "MB6",
  "MB7",
  "MB7d",
  "MB9",
  "MB10",
  "MB11",
] as const;

export type BridgeKey = (typeof LIVE_BRIDGES)[number];
export type WeightVector = Record<BridgeKey, number>;

/** Always shown in the default research-only filter (companion site / hub listings). */
export const PINNED_LISTING_IDS = new Set(["rec1QpsZCIfnfTF1y"]);

export const RESEARCH_CATEGORIES = new Set([
  "Conceptual research",
  "Empirical research",
  "Capabilities research",
  "Strategy",
  "Governance",
  "Forecasting",
]);

export function categoryParts(category: string): string[] {
  return category
    .split(",")
    .map((p) => p.trim())
    .filter(Boolean);
}

export function isResearchListing(category: string): boolean {
  return categoryParts(category).some((p) => RESEARCH_CATEGORIES.has(p));
}

export const TYPE_MULT: Record<string, number> = {
  T: 1.0,
  D: 1.0,
  E: 0.8,
  S: 0.8,
  P: 0.8,
  C: 0.5,
  O: 0.3,
};

export function directionMult(direction?: string | null): number {
  if (!direction) return 0.5;
  if (direction === "support" || direction === "challenge") return 1.0;
  if (direction === "unclear") return 0.4;
  return 0.5;
}

export function evidenceContribution(
  type: string,
  direction?: string | null,
  weight = 1,
): number {
  const typeMult = TYPE_MULT[type] ?? 0.3;
  return weight * typeMult * directionMult(direction);
}

export function saturate(sum: number): number {
  return Math.min(1, sum);
}

export function emptyWeights(): WeightVector {
  return Object.fromEntries(LIVE_BRIDGES.map((b) => [b, 0])) as WeightVector;
}

/** Gap beyond touching circles. Weight barely changes length; affinity is stiffness. */
export function springRestLength(w: number, l0 = 38, shrink = 0.18): number {
  const clamped = Math.min(1, Math.max(0, w));
  return l0 * (1 - shrink * clamped);
}

export function springStiffness(w: number, k0 = 0.01, kScale = 0.28): number {
  const clamped = Math.min(1, Math.max(0, w));
  return k0 + kScale * clamped * clamped;
}

export function cosineSimilarity(a: WeightVector, b: WeightVector): number {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (const key of LIVE_BRIDGES) {
    const x = a[key];
    const y = b[key];
    dot += x * y;
    na += x * x;
    nb += y * y;
  }
  if (na === 0 || nb === 0) return 0;
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}

export function dominantBridge(weights: WeightVector): BridgeKey | null {
  let best: BridgeKey | null = null;
  let bestVal = 0;
  for (const key of LIVE_BRIDGES) {
    if (weights[key] > bestVal) {
      bestVal = weights[key];
      best = key;
    }
  }
  return bestVal > 0 ? best : null;
}
