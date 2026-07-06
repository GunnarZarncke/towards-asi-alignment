/** Canonical guided-tour path order (matches content collection ids). */
export const PATH_ORDER = [
  "generalist",
  "philosopher",
  "researcher-applied",
  "researcher-formal",
  "engineer-evals",
  "funder-policy"
] as const;

export type PathId = (typeof PATH_ORDER)[number];

export const PATH_LABELS: Record<PathId, string> = {
  generalist: "Generalist",
  philosopher: "Philosopher",
  "researcher-applied": "Researcher — applied",
  "researcher-formal": "Researcher — formal",
  "engineer-evals": "Engineer / evals",
  "funder-policy": "Funder / policy"
};

export function sortPaths<T extends { id: string }>(paths: T[]): T[] {
  return [...paths].sort(
    (a, b) => PATH_ORDER.indexOf(a.id as PathId) - PATH_ORDER.indexOf(b.id as PathId)
  );
}
