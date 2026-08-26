import { PATH_ORDER } from "./path-order.ts";
import { normalizePath, type VisitEntry } from "./visit-history.ts";

export type ReadNextPathStep = {
  kind: string;
  ref: string;
  href: string;
  title: string;
  bookChapterId?: string;
};

export type ReadNextPathConfig = {
  id: string;
  title: string;
  href: string;
  steps: ReadNextPathStep[];
};

export type ReadNextConfig = {
  manuscriptOrder: string[];
  chapterTitles: Record<string, string>;
  chapterHrefs: Record<string, string>;
  graphSuccessors: Record<string, string[]>;
  paths: ReadNextPathConfig[];
};

export type ReadNextResult = {
  href: string;
  title: string;
  kind: string;
  source: "path" | "graph" | "manuscript";
  pathTitle?: string;
  afterChapterId: string;
  afterChapterTitle: string;
};

const PATH_SLUGS = new Set<string>(PATH_ORDER);

function routeSlug(segment: string): string {
  return segment.toLowerCase();
}

/** Strip `/full/` and parse a book-unit id from chapter card URLs. */
export function parseBookChapterFromPath(pathname: string): string | null {
  const path = normalizePath(pathname).replace(/\/full\/$/, "/");
  const chapterMatch = path.match(/^\/cards\/(?:chapter|chapters)\/([^/]+)\/$/);
  if (chapterMatch) return routeSlug(chapterMatch[1]);
  const appendixMatch = path.match(/^\/cards\/appendix\/([^/]+)\/$/);
  if (appendixMatch) return routeSlug(appendixMatch[1]);
  if (path === "/cards/frontmatter/") return "frontmatter";
  const bookMatch = path.match(/^\/book\/([^/]+)\/$/);
  if (bookMatch) return routeSlug(bookMatch[1]);
  return null;
}

export function parseReadingPathFromPath(pathname: string): string | null {
  const match = normalizePath(pathname).match(/^\/paths\/([^/]+)\/$/);
  if (!match) return null;
  const slug = match[1];
  if (slug === "chapter-reading-graph") return null;
  return PATH_SLUGS.has(slug) ? slug : null;
}

export function latestBookChapterVisit(
  history: VisitEntry[]
): { chapterId: string; entry: VisitEntry } | null {
  for (const entry of history) {
    const chapterId = parseBookChapterFromPath(entry.path);
    if (chapterId) return { chapterId, entry };
  }
  return null;
}

export function latestReadingPathVisit(history: VisitEntry[]): string | null {
  for (const entry of history) {
    const pathId = parseReadingPathFromPath(entry.path);
    if (pathId) return pathId;
  }
  return null;
}

function normalizeChapterId(id: string): string {
  return routeSlug(id);
}

function findBookStepIndex(steps: ReadNextPathStep[], chapterId: string): number {
  const target = normalizeChapterId(chapterId);
  return steps.findIndex(
    (step) => step.kind === "book" && normalizeChapterId(step.bookChapterId ?? step.ref) === target
  );
}

function manuscriptIndex(order: string[], chapterId: string): number {
  return order.indexOf(normalizeChapterId(chapterId));
}

function sortByManuscript(order: string[], ids: string[]): string[] {
  return [...ids].sort(
    (a, b) => manuscriptIndex(order, a) - manuscriptIndex(order, b) || a.localeCompare(b)
  );
}

export type GraphEdge = {
  from: string;
  to: string;
};

export function buildGraphSuccessors(
  manuscriptOrder: string[],
  edges: GraphEdge[]
): Record<string, string[]> {
  const successors: Record<string, string[]> = {};
  for (const edge of edges) {
    const from = edge.from.replace(/^unit:/i, "").toLowerCase();
    const to = edge.to.replace(/^unit:/i, "").toLowerCase();
    if (!successors[from]) successors[from] = [];
    successors[from].push(to);
  }
  for (const [from, targets] of Object.entries(successors)) {
    successors[from] = sortByManuscript(manuscriptOrder, targets);
  }
  return successors;
}

export function resolveReadNext(
  config: ReadNextConfig,
  history: VisitEntry[],
  options?: { preferredPathId?: string }
): ReadNextResult | null {
  const latest = latestBookChapterVisit(history);
  if (!latest) return null;

  const chapterId = normalizeChapterId(latest.chapterId);
  const afterChapterTitle = config.chapterTitles[chapterId] ?? latest.entry.title ?? chapterId;

  const pathId = options?.preferredPathId ?? latestReadingPathVisit(history);
  if (pathId) {
    const path = config.paths.find((entry) => entry.id === pathId);
    if (path) {
      const index = findBookStepIndex(path.steps, chapterId);
      if (index >= 0 && index + 1 < path.steps.length) {
        const next = path.steps[index + 1];
        return {
          href: next.href,
          title: next.title,
          kind: next.kind,
          source: "path",
          pathTitle: path.title,
          afterChapterId: chapterId,
          afterChapterTitle
        };
      }
    }
  }

  const successors = config.graphSuccessors[chapterId] ?? [];
  if (successors.length > 0) {
    const nextId = successors[0];
    return {
      href: config.chapterHrefs[nextId],
      title: config.chapterTitles[nextId] ?? nextId,
      kind: "book",
      source: "graph",
      afterChapterId: chapterId,
      afterChapterTitle
    };
  }

  const index = manuscriptIndex(config.manuscriptOrder, chapterId);
  if (index >= 0 && index + 1 < config.manuscriptOrder.length) {
    const nextId = config.manuscriptOrder[index + 1];
    return {
      href: config.chapterHrefs[nextId],
      title: config.chapterTitles[nextId] ?? nextId,
      kind: "book",
      source: "manuscript",
      afterChapterId: chapterId,
      afterChapterTitle
    };
  }

  return null;
}

export function readNextSourceLabel(result: ReadNextResult): string {
  if (result.source === "path" && result.pathTitle) {
    return `${result.pathTitle} path`;
  }
  if (result.source === "graph") {
    return "chapter graph";
  }
  return "book order";
}
