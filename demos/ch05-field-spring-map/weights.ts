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

/** Multiplicative ± jitter on layout springs (breaks symmetric multi-bridge equilibria). */
export const WEIGHT_JITTER_AMPLITUDE = 0.05;

function hashString(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function mulberry32(seed: number): () => number {
  let state = seed;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Deterministic ±amplitude multiplicative noise per listing×bridge (zeros unchanged). */
export function jitterWeight(
  raw: number,
  projectId: string,
  bridge: BridgeKey,
  amplitude = WEIGHT_JITTER_AMPLITUDE,
): number {
  if (raw <= 0) return 0;
  const rand = mulberry32(hashString(`${projectId}\0${bridge}`))();
  return Math.min(1, raw * (1 + amplitude * (2 * rand - 1)));
}

export function jitterWeights(
  weights: WeightVector,
  projectId: string,
  amplitude = WEIGHT_JITTER_AMPLITUDE,
): WeightVector {
  const out = emptyWeights();
  for (const key of LIVE_BRIDGES) {
    out[key] = jitterWeight(weights[key], projectId, key, amplitude);
  }
  return out;
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

export type BridgeWeightOptions = {
  weightThreshold: number;
  useSquaredWeights: boolean;
  dominantOnly: boolean;
};

/** Bridge keys that receive a crux spring for this project (same rules as simulation). */
export function projectBridgeKeys(
  weights: WeightVector,
  opts: BridgeWeightOptions,
): BridgeKey[] {
  const entries = LIVE_BRIDGES.map((key) => ({
    key,
    w: opts.useSquaredWeights ? weights[key] * weights[key] : weights[key],
  })).filter((e) => e.w > opts.weightThreshold);

  const springs =
    opts.dominantOnly && entries.length
      ? entries.sort((a, b) => b.w - a.w).slice(0, 1)
      : entries;

  return springs.map((e) => e.key);
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
