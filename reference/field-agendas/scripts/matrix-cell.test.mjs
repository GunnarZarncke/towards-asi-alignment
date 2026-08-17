import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  STANCE_CARON_BELOW,
  STANCE_CIRCUMFLEX,
  STANCE_DOT,
  buildStanceById,
  matrixCellToMarkdown,
  normalizeEvidenceStance,
  regroupMatrixCellByStance,
  stanceMark
} from "./matrix-cell.mjs";

const EXPECTED = {
  support1: STANCE_DOT + STANCE_CIRCUMFLEX,
  support2: STANCE_DOT + STANCE_CIRCUMFLEX + STANCE_CIRCUMFLEX,
  support3: STANCE_DOT + STANCE_CIRCUMFLEX.repeat(3),
  unclear: STANCE_DOT,
  challenge1: STANCE_DOT + STANCE_CARON_BELOW,
  challenge2: STANCE_DOT + STANCE_CARON_BELOW.repeat(2),
  challenge3: STANCE_DOT + STANCE_CARON_BELOW.repeat(3)
};

describe("stanceMark", () => {
  it("encodes all seven stance sequences", () => {
    assert.equal(stanceMark("support", 1), EXPECTED.support1);
    assert.equal(stanceMark("support", 2), EXPECTED.support2);
    assert.equal(stanceMark("support", 3), EXPECTED.support3);
    assert.equal(stanceMark("unclear"), EXPECTED.unclear);
    assert.equal(stanceMark("challenge", 1), EXPECTED.challenge1);
    assert.equal(stanceMark("challenge", 2), EXPECTED.challenge2);
    assert.equal(stanceMark("challenge", 3), EXPECTED.challenge3);
  });

  it("returns empty string for missing or unknown direction", () => {
    assert.equal(stanceMark(undefined), "");
    assert.equal(stanceMark(null), "");
    assert.equal(stanceMark(""), "");
    assert.equal(stanceMark("unknown"), "");
  });

  it("clamps weight to 1..3", () => {
    assert.equal(stanceMark("support", 0), EXPECTED.support1);
    assert.equal(stanceMark("challenge", 99), EXPECTED.challenge3);
  });
});

describe("normalizeEvidenceStance", () => {
  it("defaults weight to 1 for directional entries", () => {
    assert.deepEqual(normalizeEvidenceStance({ direction: "support" }), {
      direction: "support",
      weight: 1
    });
  });

  it("returns null for untagged legacy entries", () => {
    assert.equal(normalizeEvidenceStance({}), null);
    assert.equal(normalizeEvidenceStance({ direction: "bogus" }), null);
  });

  it("clears weight for unclear", () => {
    assert.deepEqual(normalizeEvidenceStance({ direction: "unclear", weight: 2 }), {
      direction: "unclear",
      weight: null
    });
  });
});

describe("regroupMatrixCellByStance", () => {
  const stanceById = buildStanceById([
    { id: 4, direction: "challenge", weight: 3 },
    { id: 5, direction: "support", weight: 2 },
    { id: 13, direction: "challenge", weight: 3 }
  ]);

  it("splits mixed directions for the same type letter", () => {
    const groups = [
      { type: "T", ids: [4, 5] },
      { type: "E", ids: [13] }
    ];
    const out = regroupMatrixCellByStance(groups, stanceById);
    assert.deepEqual(out, [
      { type: "T", ids: [4], direction: "challenge", weight: 3 },
      { type: "T", ids: [5], direction: "support", weight: 2 },
      { type: "E", ids: [13], direction: "challenge", weight: 3 }
    ]);
  });

  it("chunks to at most three ids per stance group", () => {
    const stance = buildStanceById([
      { id: 1, direction: "support", weight: 1 },
      { id: 2, direction: "support", weight: 1 },
      { id: 3, direction: "support", weight: 1 },
      { id: 4, direction: "support", weight: 1 }
    ]);
    const out = regroupMatrixCellByStance([{ type: "C", ids: [1, 2, 3, 4] }], stance);
    assert.deepEqual(out, [
      { type: "C", ids: [1, 2, 3], direction: "support", weight: 1 },
      { type: "C", ids: [4], direction: "support", weight: 1 }
    ]);
  });

  it("leaves direction null when stance map is absent", () => {
    const out = regroupMatrixCellByStance([{ type: "C", ids: [1] }], undefined);
    assert.deepEqual(out, [{ type: "C", ids: [1], direction: null, weight: null }]);
  });
});

describe("matrixCellToMarkdown", () => {
  it("prefixes stance marks when stance map is provided", () => {
    const stanceById = buildStanceById([
      { id: 4, direction: "challenge", weight: 3 },
      { id: 5, direction: "support", weight: 2 }
    ]);
    const md = matrixCellToMarkdown([{ type: "T", ids: [4, 5] }], stanceById);
    assert.equal(
      md,
      `${EXPECTED.challenge3}T<sup>[4](#ev-4)</sup>, ${EXPECTED.support2}T<sup>[5](#ev-5)</sup>`
    );
  });

  it("omits marks without stance map", () => {
    const md = matrixCellToMarkdown([{ type: "E", ids: [13] }]);
    assert.equal(md, "E<sup>[13](#ev-13)</sup>");
  });

  it("returns em dash for empty cells", () => {
    assert.equal(matrixCellToMarkdown([]), "—");
  });
});
