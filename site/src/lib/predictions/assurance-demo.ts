export type AssuranceInputs = {
  priorOdds: number;
  kappa: number;
  sR: number;
  sU: number;
  pDgivenF: number;
  pDgivenNotF: number;
};

export type PerAttemptInputs = {
  m: number;
  kappa: number;
  fM: number;
  fU: number;
  o: number;
  b: number;
  c: number;
};

export type AssuranceOutputs = {
  oddsRatio: number;
  posteriorOdds: number;
  posteriorPF: number;
  posteriorPD: number;
};

export function assuranceOddsRatio(kappa: number, sR: number, sU: number): number {
  const safeSR = Math.max(sR, 1e-9);
  const safeSU = Math.max(sU, 1e-9);
  return kappa / safeSR + (1 - kappa) / safeSU;
}

export function oddsToProbability(odds: number): number {
  if (!Number.isFinite(odds) || odds < 0) return 0;
  return odds / (1 + odds);
}

export function computeAssuranceUpdate(input: AssuranceInputs): AssuranceOutputs {
  const oddsRatio = assuranceOddsRatio(input.kappa, input.sR, input.sU);
  const posteriorOdds = Math.max(input.priorOdds, 0) * oddsRatio;
  const posteriorPF = oddsToProbability(posteriorOdds);
  const posteriorPD =
    input.pDgivenF * posteriorPF + input.pDgivenNotF * (1 - posteriorPF);
  return { oddsRatio, posteriorOdds, posteriorPF, posteriorPD };
}

export function perAttemptCatastropheProbability(input: PerAttemptInputs): number {
  const represented = input.kappa * (input.fM + (1 - input.fM) * input.o);
  const unrepresented = (1 - input.kappa) * (input.fU + (1 - input.fU) * input.o);
  return input.m * (represented + unrepresented) * input.b * input.c;
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

export function formatPercent(value: number, digits = 2): string {
  if (!Number.isFinite(value)) return "—";
  return `${(value * 100).toFixed(digits)}%`;
}

export function formatRatio(value: number, digits = 2): string {
  if (!Number.isFinite(value)) return "—";
  return value.toFixed(digits);
}
