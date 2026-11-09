import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { pageviewProperties, servedFromCache, shouldRecordVisit } from "./page-visit.ts";

describe("shouldRecordVisit", () => {
  it("records a shown page, including one served from the offline cache", () => {
    assert.equal(shouldRecordVisit(""), true);
    assert.equal(shouldRecordVisit("?utm=letter"), true);
  });

  it("skips cache-fill URLs", () => {
    assert.equal(shouldRecordVisit("?cache=1"), false);
    assert.equal(shouldRecordVisit("?utm=letter&cache=1"), false);
  });
});

describe("servedFromCache", () => {
  it("still counts a service-worker hit when the document was not fetched", () => {
    assert.equal(servedFromCache({ workerStart: 12, transferSize: 0 }, false), true);
    const props = pageviewProperties({
      title: "Cached",
      restored: false,
      navigation: { workerStart: 12, transferSize: 0 }
    });
    assert.deepEqual(props, { title: "Cached", served_from_cache: true });
  });

  it("does not mark a service-worker pass-through that downloaded the document", () => {
    assert.equal(servedFromCache({ workerStart: 12, transferSize: 800 }, false), false);
  });

  it("counts a back-forward restore, which does not fetch or re-run the page", () => {
    assert.equal(servedFromCache(undefined, true), true);
  });
});
