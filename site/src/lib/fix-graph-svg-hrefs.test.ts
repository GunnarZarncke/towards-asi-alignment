import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { nodeHrefFromGraphPage } from "../../scripts/lib/graph-node-hrefs.mjs";
import { fixGraphSvgHrefs, siteRootGraphHref } from "./fix-graph-svg-hrefs.ts";

describe("nodeHrefFromGraphPage", () => {
  it("emits site-root paths for subgraphs, bridges, and nodes", () => {
    assert.equal(nodeHrefFromGraphPage("S2"), "/lean/graph/value-transport/");
    assert.equal(
      nodeHrefFromGraphPage("MB6a", { cardSlug: "mb6-selection-and-basin-stability" }),
      "/cards/bridge/mb6-selection-and-basin-stability/"
    );
    assert.equal(nodeHrefFromGraphPage("P30T"), "/lean/node/P30T/");
  });
});

describe("siteRootGraphHref", () => {
  it("rewrites old graph-page-relative hrefs", () => {
    assert.equal(siteRootGraphHref("../../graph/value-transport/"), "/lean/graph/value-transport/");
    assert.equal(
      siteRootGraphHref("../../cards/bridge/mb6-selection-and-basin-stability/"),
      "/cards/bridge/mb6-selection-and-basin-stability/"
    );
    assert.equal(siteRootGraphHref("../../node/P30T/"), "/lean/node/P30T/");
  });

  it("leaves site-root and absolute URLs alone", () => {
    assert.equal(siteRootGraphHref("/lean/graph/value-transport/"), "/lean/graph/value-transport/");
    assert.equal(siteRootGraphHref("https://example.com/x"), "https://example.com/x");
  });
});

describe("fixGraphSvgHrefs", () => {
  it("rewrites relative xlink hrefs from /lean/spine/", () => {
    const svg = '<a xlink:href="../../graph/value-transport/" class="lean-graph-node"></a>';
    assert.equal(
      fixGraphSvgHrefs(svg, "/"),
      '<a xlink:href="/lean/graph/value-transport/" class="lean-graph-node"></a>'
    );
  });

  it("prefixes Astro base on site-root hrefs", () => {
    const svg = '<a xlink:href="/cards/bridge/mb6-selection-and-basin-stability/"></a>';
    assert.equal(
      fixGraphSvgHrefs(svg, "/site/"),
      '<a xlink:href="/site/cards/bridge/mb6-selection-and-basin-stability/"></a>'
    );
  });
});
