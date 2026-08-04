import { describe, expect, it } from "vitest";
import { defaultParams, makeGraph, type Params } from "./app";

describe("kappa-edge percolation toy", () => {
  it("is deterministic for a fixed parameter set", () => {
    const a = makeGraph(defaultParams);
    const b = makeGraph(defaultParams);
    expect(a.stats).toEqual(b.stats);
  });

  it("keeps the cooperative giant component no larger than the social one", () => {
    const graph = makeGraph(defaultParams);
    expect(graph.stats.coopLargest).toBeLessThanOrEqual(graph.stats.socialLargest);
  });

  it("shows social connectivity without cooperative percolation when benefit/cost is low", () => {
    const params: Params = { ...defaultParams, benefitCost: 0.3 };
    const graph = makeGraph(params);
    expect(graph.stats.socialLargestFrac).toBeGreaterThan(0.5);
    expect(graph.stats.coopLargestFrac).toBeLessThan(graph.stats.socialLargestFrac);
  });

  it("percolates cooperation when benefit/cost is high", () => {
    const params: Params = { ...defaultParams, benefitCost: 6, communityMixing: 0.9 };
    const graph = makeGraph(params);
    expect(graph.stats.coopLargestFrac).toBeGreaterThan(0.5);
  });
});
