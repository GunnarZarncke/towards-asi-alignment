/**
 * Stance mark icons: stacked + / − glyphs (no Unicode combining characters).
 * Seven icons — support/challenge weights 1–3, plus unclear (±).
 */

/** @typedef {"support" | "challenge" | "unclear"} StanceDirection */

export const STANCE_ICON_IDS = [
  "stance-support-1",
  "stance-support-2",
  "stance-support-3",
  "stance-challenge-1",
  "stance-challenge-2",
  "stance-challenge-3",
  "stance-unclear"
];

const VIEW = "0 0 12 14";

function svgWrap(body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${VIEW}" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">${body}</svg>`;
}

function plusAt(cx, cy, half = 2.2) {
  return `<line x1="${cx - half}" y1="${cy}" x2="${cx + half}" y2="${cy}"/><line x1="${cx}" y1="${cy - half}" x2="${cx}" y2="${cy + half}"/>`;
}

function minusAt(cx, cy, half = 2.2) {
  return `<line x1="${cx - half}" y1="${cy}" x2="${cx + half}" y2="${cy}"/>`;
}

/** @param {number} count @param {"plus" | "minus"} kind */
function stacked(count, kind) {
  const cx = 6;
  const ys = count === 1 ? [7] : count === 2 ? [4.5, 9.5] : [3, 7, 11];
  const draw = kind === "plus" ? plusAt : minusAt;
  return ys.map((y) => draw(cx, y)).join("");
}

/** @type {Record<string, string>} */
export const STANCE_ICON_SVG = {
  "stance-support-1": svgWrap(stacked(1, "plus")),
  "stance-support-2": svgWrap(stacked(2, "plus")),
  "stance-support-3": svgWrap(stacked(3, "plus")),
  "stance-challenge-1": svgWrap(stacked(1, "minus")),
  "stance-challenge-2": svgWrap(stacked(2, "minus")),
  "stance-challenge-3": svgWrap(stacked(3, "minus")),
  "stance-unclear": svgWrap(`${plusAt(6, 4.2, 1.9)}${minusAt(6, 9.8, 1.9)}`)
};

/**
 * @param {string | null | undefined} direction
 * @param {number | null | undefined} [weight]
 * @returns {string}
 */
export function stanceIconId(direction, weight = 1) {
  if (direction === "support") {
    const w = Math.min(3, Math.max(1, Number(weight) || 1));
    return `stance-support-${w}`;
  }
  if (direction === "challenge") {
    const w = Math.min(3, Math.max(1, Number(weight) || 1));
    return `stance-challenge-${w}`;
  }
  if (direction === "unclear") return "stance-unclear";
  return "";
}

/** Plain-text mark for generated markdown (sync index, catalog export). */
export function stanceMarkText(direction, weight = 1) {
  const id = stanceIconId(direction, weight);
  if (!id) return "";
  if (id === "stance-unclear") return "±";
  if (id.startsWith("stance-support-")) return "+".repeat(Number(id.slice(-1)));
  if (id.startsWith("stance-challenge-")) return "−".repeat(Number(id.slice(-1)));
  return "";
}
