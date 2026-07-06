import { describe, expect, it } from "vitest";
import { runLhvExperiment } from "./app";

describe("LHV learnability toy", () => {
  const result = runLhvExperiment();

  it("recovers the planted hub count", () => {
    expect(result.recoveredHubDim).toBe(result.config.hubDim);
  });

  it("keeps the recovered hub probe close to the oracle probe", () => {
    const final = result.probes[result.probes.length - 1];
    expect(final.lhvAuc).toBeGreaterThan(0.7);
    expect(final.oracleAuc - final.lhvAuc).toBeLessThan(0.08);
  });

  it("implies nonzero value information from held-out prediction", () => {
    expect(result.infoLowerBoundBits).toBeGreaterThan(0.05);
  });
});
