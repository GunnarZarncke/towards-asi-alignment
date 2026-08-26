import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  cardTypeFromPath,
  continueTarget,
  latestByKind,
  latestByType,
  normalizePath,
  prependVisit,
  visitTypeForPath
} from "./visit-history.ts";

describe("visitTypeForPath", () => {
  it("maps prefixes to nav types", () => {
    assert.equal(visitTypeForPath("/cards/concept/foo/"), "cards");
    assert.equal(visitTypeForPath("/glossary/"), "cards");
    assert.equal(visitTypeForPath("/references/"), "book");
    assert.equal(visitTypeForPath("/chapter-demos/x/"), "demos");
    assert.equal(visitTypeForPath("/faq/"), "start");
    assert.equal(visitTypeForPath("/essay/the-chatbot-passed-the-test/"), "essay");
    assert.equal(visitTypeForPath("/"), null);
  });
});

describe("cardTypeFromPath", () => {
  it("reads card content type from typed slugs", () => {
    assert.equal(cardTypeFromPath("/cards/chapter/ch07/"), "chapter");
    assert.equal(cardTypeFromPath("/cards/bridge/mb1-boundary-estimator-soundness/"), "bridge");
    assert.equal(cardTypeFromPath("/cards/concept/boundary-discovery/"), "concept");
    assert.equal(cardTypeFromPath("/cards/frontmatter/"), "frontmatter");
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

describe("latestByKind", () => {
  it("returns one row per card kind and skips nav landings", () => {
    const history = [
      { path: "/", title: "Home", type: null, t: 5 },
      { path: "/cards/chapter/ch07/", title: "Finding the Boundary", type: "cards" as const, t: 4 },
      { path: "/cards/concept/boundary-discovery/", title: "Finding the Boundary", type: "cards" as const, t: 3 },
      { path: "/book/", title: "Book", type: "book" as const, t: 2 },
      { path: "/cards/chapter/ch01/", title: "Ch 1", type: "cards" as const, t: 1 }
    ];
    const rows = latestByKind(history, "/");
    assert.deepEqual(
      rows.map((row) => [row.kind, row.entry.path]),
      [
        ["chapter", "/cards/chapter/ch07/"],
        ["concept", "/cards/concept/boundary-discovery/"]
      ]
    );
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
