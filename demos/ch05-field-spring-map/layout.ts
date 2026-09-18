import type { BridgeKey } from "./weights.js";
import { LIVE_BRIDGES } from "./weights.js";

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

/** Uniform scale on bridge anchor geometry (dependency coords + circle radius). */
export const BRIDGE_LAYOUT_SCALE = 1.5;

/** Logo / project node radius multiplier (crowded map). */
export const PROJECT_ICON_SCALE = 0.7;

let bridgeLayout: BridgeLayout | null = null;

/** Fallback circle positions when bridge-layout.json is not loaded. */
export function bridgeCirclePosition(
  key: BridgeKey,
  radius: number,
  cx = 0,
  cy = 0,
): { x: number; y: number } {
  const idx = LIVE_BRIDGES.indexOf(key);
  const angle = (idx / LIVE_BRIDGES.length) * Math.PI * 2 - Math.PI / 2;
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
  if (geometry === "dependency") {
    const pos = bridgeLayout?.positions[key];
    if (pos) {
      return {
        x: pos.x * BRIDGE_LAYOUT_SCALE,
        y: pos.y * BRIDGE_LAYOUT_SCALE,
      };
    }
  }
  return bridgeCirclePosition(key, radius * BRIDGE_LAYOUT_SCALE);
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
