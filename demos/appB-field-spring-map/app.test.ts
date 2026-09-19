import { describe, expect, it } from "vitest";
import { buildSimulation, simulateStep } from "./physics.js";
import { computeCircleBridgeOrder } from "./layout.js";
import {
  RESEARCH_CATEGORIES,
  categoryParts,
  cosineSimilarity,
  emptyWeights,
  evidenceContribution,
  isResearchListing,
  jitterWeight,
  saturate,
  springRestLength,
  springStiffness,
  WEIGHT_JITTER_AMPLITUDE,
  type BridgeKey,
  type WeightVector,
} from "./weights.js";

describe("weight model", () => {
  it("aggregates Redwood-style evidence (MB7 high, MB2 zero)", () => {
    const mb7 =
      evidenceContribution("C", "support", 2) +
      evidenceContribution("E", "challenge", 3);
    const mb4 = evidenceContribution("C", "support", 2);
    expect(saturate(mb7)).toBe(1);
    expect(saturate(mb4)).toBe(1);
    expect(saturate(0)).toBe(0);
  });

  it("varies stiffness more than rest length as weight increases", () => {
    const restLo = springRestLength(0.1);
    const restHi = springRestLength(0.9);
    const kLo = springStiffness(0.1);
    const kHi = springStiffness(0.9);
    expect(restHi / restLo).toBeGreaterThan(0.7);
    expect(kHi / kLo).toBeGreaterThan(4);
  });

  it("returns zero cosine for orthogonal vectors", () => {
    const a = emptyWeights();
    const b = emptyWeights();
    a.MB7 = 1;
    b.MB4 = 1;
    expect(cosineSimilarity(a, b)).toBe(0);
  });

  it("applies deterministic ±5% jitter per listing and bridge", () => {
    const w = 0.8;
    const a = jitterWeight(w, "rec-test", "MB7");
    const b = jitterWeight(w, "rec-test", "MB7");
    const c = jitterWeight(w, "rec-test", "MB4");
    expect(a).toBe(b);
    expect(a).toBeGreaterThanOrEqual(w * (1 - WEIGHT_JITTER_AMPLITUDE));
    expect(a).toBeLessThanOrEqual(w * (1 + WEIGHT_JITTER_AMPLITUDE));
    expect(c).not.toBe(a);
    expect(jitterWeight(0, "rec-test", "MB7")).toBe(0);
  });

  it("treats comma-separated AISafety.com categories as a set", () => {
    expect(isResearchListing("Governance, Advocacy, Conceptual research")).toBe(true);
    expect(isResearchListing("Newsletter")).toBe(false);
    expect(categoryParts("Capabilities research, Empirical research")).toEqual([
      "Capabilities research",
      "Empirical research",
    ]);
    expect(RESEARCH_CATEGORIES.has("Governance, Advocacy, Conceptual research")).toBe(false);
  });
});

describe("circle bridge order", () => {
  const opts = {
    weightThreshold: 0.05,
    useSquaredWeights: false,
    dominantOnly: false,
  };

  function ringStep(order: BridgeKey[], a: BridgeKey, b: BridgeKey): number {
    const n = order.length;
    const ia = order.indexOf(a);
    const ib = order.indexOf(b);
    const d = Math.abs(ia - ib);
    return Math.min(d, n - d);
  }

  it("places bridges with shared projects adjacent on the ring", () => {
    const w1 = emptyWeights();
    w1.MB1 = 1;
    w1.MB2 = 1;
    const w2 = emptyWeights();
    w2.MB2 = 1;
    w2.MB3 = 1;
    const order = computeCircleBridgeOrder([{ weights: w1 }, { weights: w2 }], opts);
    expect(ringStep(order, "MB1", "MB2")).toBe(1);
    expect(ringStep(order, "MB2", "MB3")).toBe(1);
  });
});

describe("simulation", () => {
  const bridges = {
    MB1: "Embedded Agency",
    MB2: "Value Learning",
    MB3: "Value Referent",
    MB4: "Corrigibility",
    MB4a: "Audit Independence",
    MB5: "Tiling",
    MB6: "Goodhart Selection",
    MB7: "Inner Alignment",
    MB7d: "Acausal Coordination",
    MB9: "Grounding Drift",
    MB10: "Successor Gaming",
    MB11: "Deployment Safety",
  };

  it("creates bridge nodes in mode A", () => {
    const w: WeightVector = emptyWeights();
    w.MB7 = 1;
    const sim = buildSimulation([{ id: "p1", title: "Test Org", weights: w }], bridges, {
      mode: "A",
      pinGeometry: "circle",
      pinBridges: true,
      dominantOnly: false,
      weightThreshold: 0.05,
      useSquaredWeights: true,
    });
    expect(sim.nodes.some((n) => n.kind === "bridge")).toBe(true);
    expect(sim.edges.some((e) => e.kind === "crux")).toBe(true);
  });

  it("uses similarity edges only in mode C", () => {
    const a = emptyWeights();
    a.MB7 = 0.8;
    const b = emptyWeights();
    b.MB7 = 0.7;
    const sim = buildSimulation(
      [
        { id: "p1", title: "A", weights: a },
        { id: "p2", title: "B", weights: b },
      ],
      bridges,
      {
        mode: "C",
        pinGeometry: "circle",
        pinBridges: true,
        dominantOnly: false,
        weightThreshold: 0.05,
        useSquaredWeights: true,
      },
    );
    expect(sim.nodes.every((n) => n.kind === "project")).toBe(true);
    expect(sim.edges.some((e) => e.kind === "similarity")).toBe(true);
  });

  it("steps without NaN positions", () => {
    const w = emptyWeights();
    w.MB4 = 0.5;
    const sim = buildSimulation([{ id: "x", title: "X", weights: w }], bridges, {
      mode: "A",
      pinGeometry: "circle",
      pinBridges: true,
      dominantOnly: false,
      weightThreshold: 0.05,
      useSquaredWeights: true,
    });
    for (let i = 0; i < 50; i++) {
      simulateStep(sim.nodes, sim.edges, {
        mode: "A",
        pinGeometry: "circle",
        pinBridges: true,
        dominantOnly: false,
        weightThreshold: 0.05,
        useSquaredWeights: true,
      });
    }
    for (const n of sim.nodes) {
      expect(Number.isFinite(n.x)).toBe(true);
      expect(Number.isFinite(n.y)).toBe(true);
    }
  });
});
