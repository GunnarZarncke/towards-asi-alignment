import {
  buildStanceById,
  normalizeEvidenceStance,
  regroupMatrixCellByStance,
  stanceAriaLabel,
  stanceDirectionLabel,
  stanceIconId,
  stanceMarkText
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

export {
  buildStanceById,
  stanceIconId,
  stanceMarkText,
  stanceAriaLabel,
  stanceDirectionLabel,
  regroupMatrixCellByStance
};

function iconSrc(iconBase: string, iconId: string): string {
  const prefix = iconBase.replace(/\/?$/, "/");
  return `${prefix}icons/stance/${iconId}.svg`;
}

/** Render a stance mark as an inline SVG icon (monochrome, no Unicode combining marks). */
export function renderStanceMarkHtml(
  direction: string | null,
  weight: number | null = 1,
  iconBase = ""
): string {
  if (!direction) return "";
  const id = stanceIconId(direction, weight ?? 1);
  if (!id) return "";
  const aria = stanceAriaLabel(direction, weight ?? 1);
  const src = iconSrc(iconBase, id);
  return `<img class="stance-mark" src="${src}" alt="" aria-label="${aria}" width="12" height="14" decoding="async" />`;
}

export function flattenMatrixCell(groups: MatrixCellGroup[]): MatrixEvidenceTag[] {
  const flat: MatrixEvidenceTag[] = [];
  for (const { type, ids } of groups) {
    for (const id of ids) flat.push({ type, id });
  }
  return flat;
}

/** Render normalized cell groups for the Field hub matrix (one type letter per group, ≤3 ids in superscript). */
export function renderMatrixCellHtml(
  groups: MatrixCellGroup[] | undefined,
  fieldPrefix: string,
  stanceById?: Map<number, EvidenceStance>,
  iconBase = ""
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
      const markHtml = direction ? renderStanceMarkHtml(direction, weight, iconBase) : "";
      return `<span class="matrix-ev">${markHtml}<span class="matrix-ev-type">${type}</span><sup class="matrix-ev-id">${idLinks}</sup></span>`;
    });

  return parts.length ? parts.join(", ") : null;
}
