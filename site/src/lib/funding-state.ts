export type FundingState = "open" | "unfunded" | "partial" | "funded";
export type DoneState = "not_started" | "partial" | "done";

export const FUNDING_STATE_LABEL: Record<FundingState, string> = {
  open: "Open",
  unfunded: "Unfunded",
  partial: "Partially funded",
  funded: "Funded"
};

export const DONE_STATE_LABEL: Record<DoneState, string> = {
  not_started: "Not started",
  partial: "Partially done",
  done: "Done"
};

/** Public funding display: two significant figures (no budget-line false precision). */
export function roundFundingAmount(amount: number, significantDigits = 2): number {
  if (!Number.isFinite(amount) || amount === 0) return amount;
  const sign = Math.sign(amount);
  const abs = Math.abs(amount);
  const power = Math.floor(Math.log10(abs));
  const scale = 10 ** (power - significantDigits + 1);
  return sign * Math.round(abs / scale) * scale;
}

export function formatUsd(amount: number) {
  const rounded = roundFundingAmount(amount);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(rounded);
}

export function formatFte(fte?: number, fteMax?: number): string | null {
  if (fte == null) return null;
  if (fteMax != null && fteMax !== fte) {
    return `${fte}–${fteMax} people`;
  }
  return fte === 1 ? "1 person" : `${fte} people`;
}

export function fundingCardRef(id: string) {
  return id.startsWith("funding/") ? id : `funding/${id}`;
}
