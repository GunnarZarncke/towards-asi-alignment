import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  buildStanceById,
  matrixCellToMarkdown,
  normalizeEvidenceStance,
  regroupMatrixCellByStance,
  stanceIconId,
  stanceMarkText
} from "./matrix-cell.mjs";

const EXPECTED = {
  support1: "+",
  support2: "++",
  support3: "+++",
  unclear: "±",
  challenge1: "−",
  challenge2: "−−",
  challenge3: "−−−"
};

describe("stanceMarkText", () => {
  it("encodes all seven stance marks", () => {
    assert.equal(stanceMarkText("support", 1), EXPECTED.support1);
    assert.equal(stanceMarkText("support", 2), EXPECTED.support2);
    assert.equal(stanceMarkText("support", 3), EXPECTED.support3);
    assert.equal(stanceMarkText("unclear"), EXPECTED.unclear);
    assert.equal(stanceMarkText("challenge", 1), EXPECTED.challenge1);
    assert.equal(stanceMarkText("challenge", 2), EXPECTED.challenge2);
    assert.equal(stanceMarkText("challenge", 3), EXPECTED.challenge3);
  });

  it("returns empty string for missing or unknown direction", () => {
    assert.equal(stanceMarkText(undefined), "");
    assert.equal(stanceMarkText(null), "");
    assert.equal(stanceMarkText(""), "");
    assert.equal(stanceMarkText("unknown"), "");
  });

  it("clamps weight to 1..3", () => {
    assert.equal(stanceMarkText("support", 0), EXPECTED.support1);
    assert.equal(stanceMarkText("challenge", 99), EXPECTED.challenge3);
  });
});

describe("stanceIconId", () => {
  it("maps direction and weight to icon ids", () => {
    assert.equal(stanceIconId("support", 2), "stance-support-2");
    assert.equal(stanceIconId("challenge", 1), "stance-challenge-1");
    assert.equal(stanceIconId("unclear"), "stance-unclear");
    assert.equal(stanceIconId(null), "");
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
