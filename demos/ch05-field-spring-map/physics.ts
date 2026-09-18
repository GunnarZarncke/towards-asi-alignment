import type { BridgeKey, WeightVector } from "./weights.js";
import { LIVE_BRIDGES, cosineSimilarity, springRestLength, springStiffness } from "./weights.js";
import {
  BRIDGE_LAYOUT_SCALE,
  PROJECT_ICON_SCALE,
  bridgeDependencyEdges,
  bridgePinPosition,
  graphDistance,
  type PinGeometry,
} from "./layout.js";

export type LayoutMode = "A" | "B" | "C";

export type SimNode = {
  id: string;
  kind: "project" | "bridge";
  label: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  pinned: boolean;
  radius: number;
  bridgeKey?: BridgeKey;
  projectId?: string;
  logoLocal?: string;
};

export type SimEdge = {
  source: string;
  target: string;
  weight: number;
  kind: "crux" | "bridge-dep" | "bridge-dep-static" | "similarity";
  color?: string;
  assembly?: boolean;
};

export type SimOptions = {
  mode: LayoutMode;
  pinGeometry: PinGeometry;
  pinBridges: boolean;
  dominantOnly: boolean;
  weightThreshold: number;
  useSquaredWeights: boolean;
};

export const DEFAULT_SIM_OPTIONS: SimOptions = {
  mode: "A",
  pinGeometry: "dependency",
  pinBridges: true,
  dominantOnly: false,
  weightThreshold: 0.05,
  useSquaredWeights: true,
};

function effectiveWeight(raw: number, useSquared: boolean): number {
  const w = Math.max(0, raw);
  return useSquared ? w * w : w;
}

function addBridgeDependencyEdges(edges: SimEdge[], forSimulation: boolean): void {
  for (const e of bridgeDependencyEdges()) {
    edges.push({
      source: `bridge:${e.from}`,
      target: `bridge:${e.to}`,
      weight: forSimulation ? 1 / (1 + graphDistance(e.from, e.to)) : 1,
      kind: forSimulation ? "bridge-dep" : "bridge-dep-static",
      color: e.color,
      assembly: e.assembly,
    });
  }
}

export function buildSimulation(
  projects: {
    id: string;
    title: string;
    weights: WeightVector;
    logoLocal?: string;
    scale?: string | null;
  }[],
  bridgeLabels: Record<BridgeKey, string>,
  options: SimOptions,
): { nodes: SimNode[]; edges: SimEdge[] } {
  const nodes: SimNode[] = [];
  const edges: SimEdge[] = [];
  const showBridges = options.mode !== "C";
  const showBridgeDeps =
    options.pinGeometry === "dependency" || options.mode === "B";

  if (showBridges) {
    for (const key of LIVE_BRIDGES) {
      const pos = bridgePinPosition(key, options.pinGeometry);
      nodes.push({
        id: `bridge:${key}`,
        kind: "bridge",
        label: `${key} ${bridgeLabels[key] ?? key}`,
        bridgeKey: key,
        x: pos.x + (Math.random() - 0.5) * 8,
        y: pos.y + (Math.random() - 0.5) * 8,
        vx: 0,
        vy: 0,
        pinned: options.mode === "A" || options.pinBridges,
        radius: 22,
      });
    }

    if (showBridgeDeps) {
      addBridgeDependencyEdges(edges, options.mode === "B" && !options.pinBridges);
    }
  }

  for (const p of projects) {
    const angle = Math.random() * Math.PI * 2;
    const r = BRIDGE_LAYOUT_SCALE * (70 + Math.random() * 110);
    const scaleRadius =
      (p.scale === "Large" ? 28 : p.scale === "Medium" ? 22 : p.scale === "Small" ? 16 : 20) *
      PROJECT_ICON_SCALE;
    nodes.push({
      id: `project:${p.id}`,
      kind: "project",
      label: p.title,
      projectId: p.id,
      logoLocal: p.logoLocal,
      x: Math.cos(angle) * r,
      y: Math.sin(angle) * r,
      vx: 0,
      vy: 0,
      pinned: false,
      radius: scaleRadius,
    });

    if (showBridges) {
      const entries = LIVE_BRIDGES.map((key) => ({
        key,
        w: effectiveWeight(p.weights[key], options.useSquaredWeights),
      })).filter((e) => e.w > options.weightThreshold);

      const springs =
        options.dominantOnly && entries.length
          ? entries.sort((a, b) => b.w - a.w).slice(0, 1)
          : entries;

      for (const { key, w } of springs) {
        edges.push({
          source: `project:${p.id}`,
          target: `bridge:${key}`,
          weight: w,
          kind: "crux",
        });
      }
    }
  }

  if (options.mode === "C") {
    const projNodes = projects.map((p) => ({
      id: p.id,
      weights: p.weights,
    }));
    for (let i = 0; i < projNodes.length; i++) {
      for (let j = i + 1; j < projNodes.length; j++) {
        const sim = cosineSimilarity(projNodes[i].weights, projNodes[j].weights);
        if (sim > options.weightThreshold) {
          edges.push({
            source: `project:${projNodes[i].id}`,
            target: `project:${projNodes[j].id}`,
            weight: sim,
            kind: "similarity",
          });
        }
      }
    }
  }

  return { nodes, edges };
}

export function simulateStep(
  nodes: SimNode[],
  edges: SimEdge[],
  options: SimOptions,
): void {
  const damping = 0.92;
  const repulsion = 520;
  const centerPull = 0.0005;
  const maxSpeed = 7;
  const bridgeDepRest = 100 * BRIDGE_LAYOUT_SCALE;
  const bridgeDepK = 0.012;

  for (const n of nodes) {
    n.vx *= damping;
    n.vy *= damping;
  }

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i];
      const b = nodes[j];
      let dx = b.x - a.x;
      let dy = b.y - a.y;
      let distSq = dx * dx + dy * dy;
      if (distSq < 1) distSq = 1;
      const dist = Math.sqrt(distSq);
      const minDist = a.radius + b.radius + 10;
      const force = repulsion / distSq;
      dx /= dist;
      dy /= dist;

      if (dist < minDist) {
        const push = (minDist - dist) * 0.22;
        if (!a.pinned) {
          a.vx -= dx * push;
          a.vy -= dy * push;
        }
        if (!b.pinned) {
          b.vx += dx * push;
          b.vy += dy * push;
        }
      }

      if (a.kind === "project" && b.kind === "project" && options.mode !== "C") {
        if (!a.pinned) {
          a.vx -= dx * force;
          a.vy -= dy * force;
        }
        if (!b.pinned) {
          b.vx += dx * force;
          b.vy += dy * force;
        }
      }
    }
  }

  const nodeById = new Map(nodes.map((n) => [n.id, n]));

  for (const edge of edges) {
    if (edge.kind === "bridge-dep-static") continue;

    const a = nodeById.get(edge.source);
    const b = nodeById.get(edge.target);
    if (!a || !b) continue;

    let dx = b.x - a.x;
    let dy = b.y - a.y;
    let dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 0.001) {
      dx = (Math.random() - 0.5) * 0.01;
      dy = (Math.random() - 0.5) * 0.01;
      dist = 0.01;
    }

    let rest: number;
    let k: number;
    if (edge.kind === "crux") {
      rest = springRestLength(edge.weight) + a.radius + b.radius;
      k = springStiffness(edge.weight);
    } else if (edge.kind === "bridge-dep") {
      rest = bridgeDepRest;
      k = bridgeDepK;
    } else {
      rest = 180 * (1 - edge.weight * 0.5);
      k = 0.008 + edge.weight * 0.02;
    }

    const delta = dist - rest;
    const fx = (k * delta * dx) / dist;
    const fy = (k * delta * dy) / dist;

    if (!a.pinned) {
      a.vx += fx;
      a.vy += fy;
    }
    if (!b.pinned) {
      b.vx -= fx;
      b.vy -= fy;
    }
  }

  for (const n of nodes) {
    if (n.pinned) {
      if (n.kind === "bridge") {
        const key = n.bridgeKey!;
        const pos = bridgePinPosition(key, options.pinGeometry);
        n.x = pos.x;
        n.y = pos.y;
      }
      n.vx = 0;
      n.vy = 0;
      continue;
    }
    n.vx -= n.x * centerPull;
    n.vy -= n.y * centerPull;

    const speed = Math.hypot(n.vx, n.vy);
    if (speed > maxSpeed) {
      const scale = maxSpeed / speed;
      n.vx *= scale;
      n.vy *= scale;
    }

    n.x += n.vx;
    n.y += n.vy;
  }
}

export function reheat(nodes: SimNode[]): void {
  for (const n of nodes) {
    if (n.pinned) continue;
    n.vx += (Math.random() - 0.5) * 12;
    n.vy += (Math.random() - 0.5) * 12;
  }
}
