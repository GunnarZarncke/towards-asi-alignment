import { describe, expect, it } from "vitest";
import { buildSimulation, simulateStep } from "./physics.js";
import {
  RESEARCH_CATEGORIES,
  categoryParts,
  cosineSimilarity,
  emptyWeights,
  evidenceContribution,
  isResearchListing,
  saturate,
  springRestLength,
  springStiffness,
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
