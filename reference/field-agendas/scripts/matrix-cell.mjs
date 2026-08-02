/**
 * Canonical coverage-matrix cell format shared by extract, sync, and site render.
 *
 * YAML cell: [] (empty) or list of { type: "C", ids: [1, 2] }.
 * Legacy markdown/HTML strings are parsed on import only.
 */

const LINK_RE = /\[([^\]]*)\]\(#ev-(\d+)\)/g;
const SUP_BLOCK_RE = /([A-Z])<sup>([\s\S]*?)<\/sup>/g;

/** At most this many catalog IDs share one type letter (affects line breaking in the site matrix). */
export const MAX_IDS_PER_GROUP = 3;

/** @typedef {{ type: string, ids: number[] }} MatrixCellGroup */

/**
 * Split groups so no type letter carries more than MAX_IDS_PER_GROUP ids.
 * @param {MatrixCellGroup[]} groups
 * @returns {MatrixCellGroup[]}
 */
export function chunkMatrixCellGroups(groups) {
  /** @type {MatrixCellGroup[]} */
  const out = [];
  for (const { type, ids } of groups) {
    for (let i = 0; i < ids.length; i += MAX_IDS_PER_GROUP) {
      out.push({ type, ids: ids.slice(i, i + MAX_IDS_PER_GROUP) });
    }
  }
  return out;
}

/**
 * Parse legacy cell text into canonical groups (one group per type run in source order).
 * @param {string} raw
 * @returns {MatrixCellGroup[]}
 */
export function parseMatrixCellRaw(raw) {
  if (!raw || raw === "—") return [];
  /** @type {MatrixCellGroup[]} */
  const groups = [];
  let remainder = raw;

  for (const block of raw.matchAll(SUP_BLOCK_RE)) {
    const type = block[1];
    /** @type {number[]} */
    const ids = [];
    for (const link of block[2].matchAll(LINK_RE)) {
      ids.push(Number(link[2]));
    }
    if (ids.length) groups.push({ type, ids });
    remainder = remainder.replace(block[0], "");
  }

  for (const link of remainder.matchAll(LINK_RE)) {
    const label = link[1];
    const id = Number(link[2]);
    const type = label.match(/^([A-Z])/)?.[1] ?? "?";
    groups.push({ type, ids: [id] });
  }

  return groups;
}

/**
 * @param {MatrixCellGroup[]} groups
 * @returns {MatrixCellGroup[]}
 */
function finalizeMatrixCellGroups(groups) {
  return chunkMatrixCellGroups(
    groups
      .map((group) => ({
        type: String(group.type ?? "?"),
        ids: (group.ids ?? []).map((id) => Number(id)).filter((id) => !Number.isNaN(id))
      }))
      .filter((g) => g.ids.length > 0)
  );
}

/**
 * @param {unknown} cell
 * @returns {MatrixCellGroup[]}
 */
export function normalizeMatrixCell(cell) {
  if (cell === null || cell === undefined || cell === "—" || cell === "") return [];
  if (typeof cell === "string") return finalizeMatrixCellGroups(parseMatrixCellRaw(cell));
  if (!Array.isArray(cell)) return [];
  return finalizeMatrixCellGroups(cell);
}

/**
 * Flatten groups to individual type+id pairs (render order preserved).
 * @param {MatrixCellGroup[]} groups
 * @returns {{ type: string, id: number }[]}
 */
export function flattenMatrixCell(groups) {
  /** @type {{ type: string, id: number }[]} */
  const flat = [];
  for (const { type, ids } of groups) {
    for (const id of ids) flat.push({ type, id });
  }
  return flat;
}

/**
 * Regenerate agent-readable matrix markdown (single HTML-sup format).
 * @param {MatrixCellGroup[]} groups
 * @returns {string}
 */
export function matrixCellToMarkdown(groups) {
  if (!groups.length) return "—";
  return groups
    .map(({ type, ids }) => {
      const links = ids.map((id) => `[${id}](#ev-${id})`).join(",");
      return `${type}<sup>${links}</sup>`;
    })
    .join(", ");
}

/**
 * Normalize all cells in a matrix object.
 * @param {{ columns: string[], rows: { agenda: string, slug?: string, cells: Record<string, unknown> }[] }} matrix
 */
export function normalizeMatrix(matrix) {
  return {
    columns: matrix.columns,
    rows: matrix.rows.map((row) => ({
      ...row,
      cells: Object.fromEntries(matrix.columns.map((col) => [col, normalizeMatrixCell(row.cells?.[col])]))
    }))
  };
}
