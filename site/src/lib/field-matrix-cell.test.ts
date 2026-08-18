import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { buildStanceById, renderMatrixCellHtml } from "./field-matrix-cell.ts";

describe("renderMatrixCellHtml", () => {
  it("renders type tags without stance marks by default", () => {
    const html = renderMatrixCellHtml([{ type: "E", ids: [13] }], "/field/");
    assert.match(html ?? "", /<span class="matrix-ev-type">E<\/span>/);
    assert.doesNotMatch(html ?? "", /stance-mark/);
  });

  it("renders stance icon and aria labels when stance map is provided", () => {
    const stanceById = buildStanceById([{ id: 13, direction: "challenge", weight: 3 }]);
    const html = renderMatrixCellHtml(
      [{ type: "E", ids: [13] }],
      "/field/v2/",
      stanceById,
      "/"
    );
    assert.match(html ?? "", /class="stance-mark"/);
    assert.match(html ?? "", /icons\/stance\/stance-challenge-3\.svg/);
    assert.match(html ?? "", /aria-label="complicates, weight 3"/);
    assert.match(html ?? "", /href="\/field\/v2\/#ev-13"/);
  });

  it("splits mixed stances in one cell into separate tag groups", () => {
    const stanceById = buildStanceById([
      { id: 4, direction: "challenge", weight: 3 },
      { id: 5, direction: "support", weight: 2 }
    ]);
    const html = renderMatrixCellHtml(
      [{ type: "T", ids: [4, 5] }],
      "/field/v2/",
      stanceById,
      "/"
    );
    assert.match(html ?? "", /stance-challenge-3\.svg.*matrix-ev-type">T/s);
    assert.match(html ?? "", /stance-support-2\.svg.*matrix-ev-type">T/s);
    assert.match(html ?? "", /#ev-4/);
    assert.match(html ?? "", /#ev-5/);
  });

  it("respects max three ids per rendered group", () => {
    const stanceById = buildStanceById([
      { id: 1, direction: "support", weight: 1 },
      { id: 2, direction: "support", weight: 1 },
      { id: 3, direction: "support", weight: 1 },
      { id: 4, direction: "support", weight: 1 }
    ]);
    const html = renderMatrixCellHtml(
      [{ type: "C", ids: [1, 2, 3, 4] }],
      "/field/v2/",
      stanceById,
      "/"
    );
    assert.equal((html?.match(/matrix-ev-type">C/g) ?? []).length, 2);
    assert.match(html ?? "", /#ev-1.*#ev-2.*#ev-3/s);
    assert.match(html ?? "", /#ev-4/);
  });

  it("returns null for empty cells", () => {
    assert.equal(renderMatrixCellHtml([], "/field/"), null);
    assert.equal(renderMatrixCellHtml(undefined, "/field/"), null);
  });
});
