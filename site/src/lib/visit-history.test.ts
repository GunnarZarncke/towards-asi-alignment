import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  continueTarget,
  latestByType,
  normalizePath,
  prependVisit,
  visitTypeForPath
} from "./visit-history.ts";

describe("visitTypeForPath", () => {
  it("maps prefixes to nav types", () => {
    assert.equal(visitTypeForPath("/cards/foo/"), "cards");
    assert.equal(visitTypeForPath("/glossary/"), "cards");
    assert.equal(visitTypeForPath("/references/"), "book");
    assert.equal(visitTypeForPath("/chapter-demos/x/"), "demos");
    assert.equal(visitTypeForPath("/faq/"), "start");
    assert.equal(visitTypeForPath("/essay/the-chatbot-passed-the-test/"), "essay");
    assert.equal(visitTypeForPath("/"), null);
  });
});

describe("continueTarget", () => {
  it("skips the current path", () => {
    const history = [
      { path: "/", title: "Home", type: null, t: 2 },
      { path: "/field/", title: "Field", type: "field" as const, t: 1 }
    ];
    assert.equal(continueTarget(history, "/")?.path, "/field/");
  });
});

describe("prependVisit", () => {
  it("dedupes consecutive same path", () => {
    const a = { path: "/book/", title: "Book", type: "book" as const, t: 1 };
    const next = prependVisit([a], { ...a, t: 2 });
    assert.equal(next.length, 1);
  });
});

describe("latestByType", () => {
  it("returns one row per type in recency order", () => {
    const history = [
      { path: "/", title: "Home", type: null, t: 4 },
      { path: "/cards/x/", title: "X", type: "cards" as const, t: 3 },
      { path: "/book/", title: "Book", type: "book" as const, t: 2 },
      { path: "/cards/y/", title: "Y", type: "cards" as const, t: 1 }
    ];
    const rows = latestByType(history, "/");
    assert.deepEqual(
      rows.map((row) => [row.type, row.entry.path]),
      [
        ["cards", "/cards/x/"],
        ["book", "/book/"]
      ]
    );
  });
});

describe("normalizePath", () => {
  it("adds a trailing slash except at root", () => {
    assert.equal(normalizePath("/field"), "/field/");
    assert.equal(normalizePath("/"), "/");
  });
});
