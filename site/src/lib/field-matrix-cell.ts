/** Canonical matrix cell tag from field-agendas.json (source-normalized). */
export type MatrixCellGroup = {
  type: string;
  ids: number[];
};

export type MatrixEvidenceTag = {
  type: string;
  id: number;
};

export function flattenMatrixCell(groups: MatrixCellGroup[]): MatrixEvidenceTag[] {
  const flat: MatrixEvidenceTag[] = [];
  for (const { type, ids } of groups) {
    for (const id of ids) flat.push({ type, id });
  }
  return flat;
}

/** Render normalized cell groups for the Field hub matrix (one type letter per group, ≤3 ids in superscript). */
export function renderMatrixCellHtml(groups: MatrixCellGroup[] | undefined, fieldPrefix: string): string | null {
  if (!groups?.length) return null;

  const parts = groups
    .filter(({ ids }) => ids.length > 0)
    .map(({ type, ids }) => {
      const idLinks = ids
        .map((id) => {
          const href = `${fieldPrefix}#ev-${id}`;
          return `<a href="${href}" class="matrix-ev-id-link">${id}</a>`;
        })
        .join(",");
      return `<span class="matrix-ev"><span class="matrix-ev-type">${type}</span><sup class="matrix-ev-id">${idLinks}</sup></span>`;
    });

  return parts.length ? parts.join(", ") : null;
}
