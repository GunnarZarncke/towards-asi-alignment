import type { CollectionEntry } from "astro:content";
import bookIndex from "../data/book.json";
import chapterGraph from "../data/chapter-reading-graph.json";
import { bookHref, pathHref } from "./site-urls";
import { getReadingPaths, type ReadingPathRecord } from "./reading-paths";
import { resolveReadingPathStep, type ReadingPathStepContext } from "./reading-path-steps";
import {
  buildGraphSuccessors,
  type ReadNextConfig,
  type ReadNextPathConfig
} from "./read-next-core";

export function buildReadNextConfig(
  context: ReadingPathStepContext,
  paths: ReadingPathRecord[] = getReadingPaths()
): ReadNextConfig {
  const { base, cards } = context;
  const manuscriptOrder = bookIndex.chapters.map((chapter) => chapter.id.toLowerCase());
  const chapterTitles: Record<string, string> = {};
  const chapterHrefs: Record<string, string> = {};

  for (const chapter of bookIndex.chapters) {
    const id = chapter.id.toLowerCase();
    chapterTitles[id] = chapter.title;
    chapterHrefs[id] = bookHref(base, chapter.id);
  }

  for (const card of cards) {
    if (!["chapter", "appendix", "frontmatter"].includes(card.data.type)) continue;
    const id = (card.data.bookPageId ?? card.id.replace(/^chapters\//i, "")).toLowerCase();
    chapterTitles[id] = card.data.title;
    chapterHrefs[id] = bookHref(base, id);
  }

  const pathConfigs: ReadNextPathConfig[] = paths.map((path) => ({
    id: path.id,
    title: path.title,
    href: pathHref(base, path.id),
    steps: path.steps
      .map((step) => resolveReadingPathStep(step, context))
      .filter((step): step is NonNullable<typeof step> => step !== null)
      .map((step) => ({
        kind: step.kind,
        ref: step.ref,
        href: step.href,
        title: step.title,
        bookChapterId: step.bookChapterId
      }))
  }));

  return {
    manuscriptOrder,
    chapterTitles,
    chapterHrefs,
    graphSuccessors: buildGraphSuccessors(manuscriptOrder, chapterGraph.graphEdges),
    paths: pathConfigs
  };
}

export type { ReadNextConfig, ReadNextResult } from "./read-next-core";
