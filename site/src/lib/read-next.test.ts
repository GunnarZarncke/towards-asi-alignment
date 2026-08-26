import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  buildGraphSuccessors,
  latestBookChapterVisit,
  latestReadingPathVisit,
  parseBookChapterFromPath,
  parseReadingPathFromPath,
  resolveReadNext,
  type ReadNextConfig
} from "./read-next-core.ts";
import type { VisitEntry } from "./visit-history.ts";

const sampleConfig: ReadNextConfig = {
  manuscriptOrder: ["ch01", "ch02", "ch03"],
  chapterTitles: {
    ch01: "Chapter One",
    ch02: "Chapter Two",
    ch03: "Chapter Three"
  },
  chapterHrefs: {
    ch01: "/cards/chapter/ch01/",
    ch02: "/cards/chapter/ch02/",
    ch03: "/cards/chapter/ch03/"
  },
  graphSuccessors: {
    ch01: ["ch03"],
    ch02: ["ch03"]
  },
  paths: [
    {
      id: "researcher-applied",
      title: "Researcher — Applied",
      href: "/paths/researcher-applied/",
      steps: [
        {
          kind: "book",
          ref: "ch01",
          bookChapterId: "ch01",
          href: "/cards/chapter/ch01/",
          title: "Chapter One"
        },
        {
          kind: "demo",
          ref: "demo-a",
          href: "/demos/a/",
          title: "Demo A"
        },
        {
          kind: "book",
          ref: "ch02",
          bookChapterId: "ch02",
          href: "/cards/chapter/ch02/",
          title: "Chapter Two"
        }
      ]
    }
  ]
};

describe("parseBookChapterFromPath", () => {
  it("parses chapter card URLs", () => {
    assert.equal(parseBookChapterFromPath("/cards/chapter/ch04/"), "ch04");
    assert.equal(parseBookChapterFromPath("/cards/chapters/ch04/full/"), "ch04");
    assert.equal(parseBookChapterFromPath("/cards/appendix/appb/"), "appb");
    assert.equal(parseBookChapterFromPath("/cards/frontmatter/"), "frontmatter");
  });
});

describe("parseReadingPathFromPath", () => {
  it("parses role paths but not the chapter graph", () => {
    assert.equal(parseReadingPathFromPath("/paths/researcher-applied/"), "researcher-applied");
    assert.equal(parseReadingPathFromPath("/paths/chapter-reading-graph/"), null);
  });
});

describe("latestBookChapterVisit", () => {
  it("finds the most recent chapter stop", () => {
    const history: VisitEntry[] = [
      { path: "/paths/", title: "Guided Tour", type: "paths", t: 3 },
      { path: "/cards/chapter/ch02/", title: "Ch 2", type: "cards", t: 2 },
      { path: "/cards/chapter/ch01/", title: "Ch 1", type: "book", t: 1 }
    ];
    assert.equal(latestBookChapterVisit(history)?.chapterId, "ch02");
  });
});

describe("latestReadingPathVisit", () => {
  it("finds the most recent role path", () => {
    const history: VisitEntry[] = [
      { path: "/cards/chapter/ch02/", title: "Ch 2", type: "cards", t: 3 },
      { path: "/paths/researcher-applied/", title: "Applied", type: "paths", t: 2 },
      { path: "/paths/generalist/", title: "Generalist", type: "paths", t: 1 }
    ];
    assert.equal(latestReadingPathVisit(history), "researcher-applied");
  });
});

describe("resolveReadNext", () => {
  it("continues within the active path when the chapter matches", () => {
    const history: VisitEntry[] = [
      { path: "/cards/chapter/ch01/", title: "Ch 1", type: "cards", t: 2 },
      { path: "/paths/researcher-applied/", title: "Applied", type: "paths", t: 1 }
    ];
    const next = resolveReadNext(sampleConfig, history);
    assert.equal(next?.title, "Demo A");
    assert.equal(next?.source, "path");
  });

  it("prefers the page path over visit history", () => {
    const history: VisitEntry[] = [
      { path: "/cards/chapter/ch01/", title: "Ch 1", type: "cards", t: 2 },
      { path: "/paths/generalist/", title: "Generalist", type: "paths", t: 1 }
    ];
    const next = resolveReadNext(sampleConfig, history, { preferredPathId: "researcher-applied" });
    assert.equal(next?.title, "Demo A");
  });

  it("falls back to graph successors", () => {
    const history: VisitEntry[] = [{ path: "/cards/chapter/ch02/", title: "Ch 2", type: "cards", t: 1 }];
    const next = resolveReadNext(sampleConfig, history);
    assert.equal(next?.title, "Chapter Three");
    assert.equal(next?.source, "graph");
  });

  it("falls back to manuscript order when the graph has no edge", () => {
    const history: VisitEntry[] = [{ path: "/cards/chapter/ch03/", title: "Ch 3", type: "cards", t: 1 }];
    assert.equal(resolveReadNext(sampleConfig, history), null);
  });
});

describe("buildGraphSuccessors", () => {
  it("sorts dependents by manuscript order", () => {
    const order = ["ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch08", "ch09"];
    const edges = [
      { from: "unit:ch01", to: "unit:ch09" },
      { from: "unit:ch01", to: "unit:ch07" }
    ];
    const successors = buildGraphSuccessors(order, edges);
    assert.deepEqual(successors.ch01, ["ch07", "ch09"]);
  });
});
