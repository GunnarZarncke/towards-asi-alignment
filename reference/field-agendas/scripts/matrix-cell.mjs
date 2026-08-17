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

export const STANCE_DOT = "\u00B7";
export const STANCE_CIRCUMFLEX = "\u0302";
export const STANCE_CARON_BELOW = "\u032C";

export const STANCE_DIRECTIONS = new Set(["support", "challenge", "unclear"]);

/** @typedef {{ type: string, ids: number[] }} MatrixCellGroup */
/** @typedef {{ direction: string, weight: number | null }} EvidenceStance */
/** @typedef {{ type: string, ids: number[], direction: string | null, weight: number | null }} StancedMatrixCellGroup */

/**
 * @param {string | null | undefined} direction
 * @param {number | null | undefined} [weight]
 * @returns {string}
 */
export function stanceMark(direction, weight = 1) {
  if (direction === "support") {
    const w = Math.min(3, Math.max(1, Number(weight) || 1));
    return STANCE_DOT + STANCE_CIRCUMFLEX.repeat(w);
  }
  if (direction === "challenge") {
    const w = Math.min(3, Math.max(1, Number(weight) || 1));
    return STANCE_DOT + STANCE_CARON_BELOW.repeat(w);
  }
  if (direction === "unclear") return STANCE_DOT;
  return "";
}

/**
 * @param {string | null | undefined} direction
 * @param {number | null | undefined} [weight]
 * @returns {string}
 */
export function stanceAriaLabel(direction, weight = 1) {
  if (direction === "support") return `advances, weight ${weight ?? 1}`;
  if (direction === "challenge") return `complicates, weight ${weight ?? 1}`;
  if (direction === "unclear") return "direction unclear";
  return "";
}

/**
 * @param {{ direction?: string, weight?: number } | null | undefined} entry
 * @returns {EvidenceStance | null}
 */
export function normalizeEvidenceStance(entry) {
  const direction = entry?.direction;
  if (!direction || !STANCE_DIRECTIONS.has(direction)) return null;
  if (direction === "unclear") return { direction: "unclear", weight: null };
  const weight = Math.min(3, Math.max(1, Number(entry?.weight ?? 1) || 1));
  return { direction, weight };
}

/**
 * @param {{ id: number, direction?: string, weight?: number }[]} evidence
 * @returns {Map<number, EvidenceStance>}
 */
export function buildStanceById(evidence) {
  /** @type {Map<number, EvidenceStance>} */
  const map = new Map();
  for (const entry of evidence ?? []) {
    const stance = normalizeEvidenceStance(entry);
    if (stance) map.set(entry.id, stance);
  }
  return map;
}

/**
 * @param {string | null | undefined} direction
 * @returns {string}
 */
export function stanceDirectionLabel(direction) {
  if (direction === "support") return "Advances";
  if (direction === "challenge") return "Complicates";
  if (direction === "unclear") return "Unclear";
  return "—";
}

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
 * Regroup flattened tags by type + stance, preserving order; chunk to MAX_IDS_PER_GROUP.
 * @param {MatrixCellGroup[]} groups
 * @param {Map<number, EvidenceStance> | undefined} stanceById
 * @returns {StancedMatrixCellGroup[]}
 */
export function regroupMatrixCellByStance(groups, stanceById) {
  /** @type {StancedMatrixCellGroup[]} */
  const out = [];
  for (const { type, ids } of groups) {
    for (const id of ids) {
      const stance = stanceById?.get(id) ?? null;
      const direction = stance?.direction ?? null;
      const weight = direction === "unclear" || !direction ? null : (stance?.weight ?? 1);
      const last = out[out.length - 1];
      const canMerge =
        last &&
        last.type === type &&
        last.direction === direction &&
        last.weight === weight &&
        last.ids.length < MAX_IDS_PER_GROUP;
      if (canMerge) last.ids.push(id);
      else out.push({ type, ids: [id], direction, weight });
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
 * @param {Map<number, EvidenceStance> | undefined} [stanceById]
 * @returns {string}
 */
export function matrixCellToMarkdown(groups, stanceById) {
  if (!groups.length) return "—";
  const stanced = stanceById?.size
    ? regroupMatrixCellByStance(groups, stanceById)
    : groups.map(({ type, ids }) => ({ type, ids, direction: null, weight: null }));
  return stanced
    .map(({ type, ids, direction, weight }) => {
      const mark = direction ? stanceMark(direction, weight ?? 1) : "";
      const links = ids.map((id) => `[${id}](#ev-${id})`).join(",");
      return `${mark}${type}<sup>${links}</sup>`;
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
