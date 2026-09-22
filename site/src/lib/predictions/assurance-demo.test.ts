import assert from "node:assert/strict";
import test from "node:test";
import {
  assuranceOddsRatio,
  computeAssuranceUpdate,
  oddsToProbability,
  perAttemptCatastropheProbability
} from "./assurance-demo.ts";

test("assuranceOddsRatio with S_U=1 reduces to (1-kappa)+kappa/S_R", () => {
  const kappa = 0.9;
  const sR = 10;
  assert.equal(assuranceOddsRatio(kappa, sR, 1), (1 - kappa) + kappa / sR);
});

test("perfect S_R still leaves 1-kappa odds multiplier under S_U=1", () => {
  const ratio = assuranceOddsRatio(0.9, 1e9, 1);
  assert.ok(Math.abs(ratio - 0.1) < 1e-6);
});

test("computeAssuranceUpdate separates consequence layer", () => {
  const out = computeAssuranceUpdate({
    priorOdds: 1,
    kappa: 0.5,
    sR: 2,
    sU: 1,
    pDgivenF: 0.2,
    pDgivenNotF: 0.01
  });
  assert.equal(out.posteriorPF, oddsToProbability(out.posteriorOdds));
  assert.ok(out.posteriorPD > 0.01);
  assert.ok(out.posteriorPD < 0.2);
});

test("perAttemptCatastropheProbability is zero when m=0", () => {
  assert.equal(
    perAttemptCatastropheProbability({ m: 0, kappa: 0.9, fM: 0.1, fU: 0.5, o: 0.1, b: 0.3, c: 0.5 }),
    0
  );
});
