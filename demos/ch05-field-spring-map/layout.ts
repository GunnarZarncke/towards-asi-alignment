import type { BridgeKey, BridgeWeightOptions, WeightVector } from "./weights.js";
import { LIVE_BRIDGES, projectBridgeKeys } from "./weights.js";

export type PinGeometry = "circle" | "dependency";

export type BridgeLayoutEdge = {
  from: BridgeKey;
  to: BridgeKey;
  color: string;
  assembly: boolean;
};

export type BridgeLayout = {
  source: string;
  positions: Partial<Record<BridgeKey, { x: number; y: number }>>;
  edges: BridgeLayoutEdge[];
};

/** Scale on bridge-layout.json coords (dependency geometry). */
export const DEPENDENCY_ANCHOR_SCALE = 2.3;

/** Scale on circle ring radius (circle geometry). */
export const CIRCLE_ANCHOR_SCALE = 1.0;

export function bridgeAnchorScale(geometry: PinGeometry): number {
  return geometry === "dependency" ? DEPENDENCY_ANCHOR_SCALE : CIRCLE_ANCHOR_SCALE;
}

/** Logo / project node radius multiplier (crowded map). */
export const PROJECT_ICON_SCALE = 0.7;

let bridgeLayout: BridgeLayout | null = null;
let circleBridgeOrder: BridgeKey[] | null = null;

function pairKey(a: BridgeKey, b: BridgeKey): string {
  return a < b ? `${a}|${b}` : `${b}|${a}`;
}

function pairAffinity(map: Map<string, number>, a: BridgeKey, b: BridgeKey): number {
  if (a === b) return 0;
  return map.get(pairKey(a, b)) ?? 0;
}

function ringCooccurrenceScore(order: BridgeKey[], map: Map<string, number>): number {
  let score = 0;
  for (let i = 0; i < order.length; i++) {
    const j = (i + 1) % order.length;
    score += pairAffinity(map, order[i], order[j]);
  }
  return score;
}

/** Max-weight Hamiltonian cycle on bridge co-occurrence (exact DP; n = |LIVE_BRIDGES| is small). */
export function computeCircleBridgeOrder(
  projects: { weights: WeightVector }[],
  opts: BridgeWeightOptions,
): BridgeKey[] {
  const cooccurrence = new Map<string, number>();

  for (const project of projects) {
    const bridges = projectBridgeKeys(project.weights, opts);
    for (let i = 0; i < bridges.length; i++) {
      for (let j = i + 1; j < bridges.length; j++) {
        const pk = pairKey(bridges[i], bridges[j]);
        cooccurrence.set(pk, (cooccurrence.get(pk) ?? 0) + 1);
      }
    }
  }

  const n = LIVE_BRIDGES.length;
  const affinity = (i: number, j: number): number =>
    pairAffinity(cooccurrence, LIVE_BRIDGES[i], LIVE_BRIDGES[j]);

  let hasCooccurrence = false;
  for (const v of cooccurrence.values()) {
    if (v > 0) {
      hasCooccurrence = true;
      break;
    }
  }
  if (!hasCooccurrence) return [...LIVE_BRIDGES];

  const full = (1 << n) - 1;
  const negInf = -1e9;
  const dp: number[][] = Array.from({ length: 1 << n }, () => Array(n).fill(negInf));
  const parent: Int16Array[] = Array.from({ length: 1 << n }, () => new Int16Array(n).fill(-1));

  dp[1][0] = 0;

  for (let mask = 1; mask <= full; mask++) {
    if (!(mask & 1)) continue;
    for (let j = 0; j < n; j++) {
      if (!(mask & (1 << j))) continue;
      const base = dp[mask][j];
      if (base <= negInf / 2) continue;
      for (let k = 0; k < n; k++) {
        if (mask & (1 << k)) continue;
        const nextMask = mask | (1 << k);
        const next = base + affinity(j, k);
        if (next > dp[nextMask][k]) {
          dp[nextMask][k] = next;
          parent[nextMask][k] = j;
        }
      }
    }
  }

  let bestScore = negInf;
  let bestEnd = 0;
  for (let j = 1; j < n; j++) {
    const score = dp[full][j] + affinity(j, 0);
    if (score > bestScore) {
      bestScore = score;
      bestEnd = j;
    }
  }

  const idxPath: number[] = [];
  let mask = full;
  let cur = bestEnd;
  while (cur >= 0) {
    idxPath.push(cur);
    const prev = parent[mask][cur];
    mask ^= 1 << cur;
    cur = prev;
  }
  idxPath.reverse();

  let bestOrder = idxPath.map((i) => LIVE_BRIDGES[i]);
  bestScore = ringCooccurrenceScore(bestOrder, cooccurrence);

  for (let rot = 0; rot < bestOrder.length; rot++) {
    for (const candidate of [
      [...bestOrder.slice(rot), ...bestOrder.slice(0, rot)],
      [...bestOrder.slice(rot), ...bestOrder.slice(0, rot)].reverse(),
    ]) {
      const score = ringCooccurrenceScore(candidate, cooccurrence);
      if (score > bestScore) {
        bestScore = score;
        bestOrder = candidate;
      }
    }
  }

  return bestOrder;
}

export function setCircleBridgeOrder(order: BridgeKey[] | null): void {
  circleBridgeOrder = order;
}

/** Fallback circle positions when bridge-layout.json is not loaded. */
export function bridgeCirclePosition(
  key: BridgeKey,
  radius: number,
  cx = 0,
  cy = 0,
): { x: number; y: number } {
  const order = circleBridgeOrder ?? LIVE_BRIDGES;
  const idx = order.indexOf(key);
  const slot = idx >= 0 ? idx : LIVE_BRIDGES.indexOf(key);
  const angle = (slot / order.length) * Math.PI * 2 - Math.PI / 2;
  return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
}

export function setBridgeLayout(layout: BridgeLayout | null): void {
  bridgeLayout = layout;
}

export function getBridgeLayout(): BridgeLayout | null {
  return bridgeLayout;
}

export function bridgePinPosition(
  key: BridgeKey,
  geometry: PinGeometry,
  radius = 320,
): { x: number; y: number } {
  const scale = bridgeAnchorScale(geometry);
  if (geometry === "dependency") {
    const pos = bridgeLayout?.positions[key];
    if (pos) {
      return {
        x: pos.x * scale,
        y: pos.y * scale,
      };
    }
  }
  return bridgeCirclePosition(key, radius * scale);
}

export function bridgeDependencyEdges(): BridgeLayoutEdge[] {
  return bridgeLayout?.edges ?? [];
}

export function graphDistance(a: BridgeKey, b: BridgeKey): number {
  if (a === b) return 0;
  const edges = bridgeLayout?.edges ?? [];
  const adj = new Map<BridgeKey, BridgeKey[]>();
  for (const e of edges) {
    if (!adj.has(e.from)) adj.set(e.from, []);
    if (!adj.has(e.to)) adj.set(e.to, []);
    adj.get(e.from)!.push(e.to);
  }
  const queue: { node: BridgeKey; dist: number }[] = [{ node: a, dist: 0 }];
  const seen = new Set<BridgeKey>([a]);
  while (queue.length) {
    const { node, dist } = queue.shift()!;
    if (node === b) return dist;
    for (const nxt of adj.get(node) ?? []) {
      if (seen.has(nxt)) continue;
      seen.add(nxt);
      queue.push({ node: nxt, dist: dist + 1 });
    }
  }
  return 4;
}
