import {
  buildStanceById,
  normalizeEvidenceStance,
  regroupMatrixCellByStance,
  stanceAriaLabel,
  stanceDirectionLabel,
  stanceMark
} from "../../../reference/field-agendas/scripts/matrix-cell.mjs";

export type MatrixCellGroup = {
  type: string;
  ids: number[];
};

export type MatrixEvidenceTag = {
  type: string;
  id: number;
};

export type EvidenceStance = NonNullable<ReturnType<typeof normalizeEvidenceStance>>;

export type StancedMatrixCellGroup = MatrixCellGroup & {
  direction: string | null;
  weight: number | null;
};

export { buildStanceById, stanceMark, stanceAriaLabel, stanceDirectionLabel, regroupMatrixCellByStance };

export function flattenMatrixCell(groups: MatrixCellGroup[]): MatrixEvidenceTag[] {
  const flat: MatrixEvidenceTag[] = [];
  for (const { type, ids } of groups) {
    for (const id of ids) flat.push({ type, id });
  }
  return flat;
}

function stanceMarkHtml(direction: string | null, weight: number | null): string {
  if (!direction) return "";
  const mark = stanceMark(direction, weight ?? 1);
  const aria = stanceAriaLabel(direction, weight ?? 1);
  const classes = [
    "matrix-ev-stance",
    direction === "support" ? "matrix-ev-stance-support" : "",
    direction === "challenge" ? "matrix-ev-stance-challenge" : "",
    weight === 3 ? "matrix-ev-stance-weight-3" : ""
  ]
    .filter(Boolean)
    .join(" ");
  return `<span class="${classes}" aria-label="${aria}">${mark}</span>`;
}

/** Render normalized cell groups for the Field hub matrix (one type letter per group, ≤3 ids in superscript). */
export function renderMatrixCellHtml(
  groups: MatrixCellGroup[] | undefined,
  fieldPrefix: string,
  stanceById?: Map<number, EvidenceStance>
): string | null {
  if (!groups?.length) return null;

  const stanced: StancedMatrixCellGroup[] = stanceById?.size
    ? regroupMatrixCellByStance(groups, stanceById)
    : groups.map(({ type, ids }) => ({ type, ids, direction: null, weight: null }));

  const parts = stanced
    .filter(({ ids }) => ids.length > 0)
    .map(({ type, ids, direction, weight }) => {
      const idLinks = ids
        .map((id) => {
          const href = `${fieldPrefix}#ev-${id}`;
          return `<a href="${href}" class="matrix-ev-id-link">${id}</a>`;
        })
        .join(",");
      const markHtml = stanceMarkHtml(direction, weight);
      return `<span class="matrix-ev">${markHtml}<span class="matrix-ev-type">${type}</span><sup class="matrix-ev-id">${idLinks}</sup></span>`;
    });

  return parts.length ? parts.join(", ") : null;
}
