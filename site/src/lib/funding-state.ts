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

export function formatUsd(amount: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(amount);
}

export function fundingCardRef(id: string) {
  return id.startsWith("funding/") ? id : `funding/${id}`;
}
