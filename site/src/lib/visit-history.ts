import { cardTypeFromPath } from "../../scripts/lib/card-urls.mjs";

export const VISIT_HISTORY_KEY = "tsa-visit-history-v1";
export const VISIT_HISTORY_MAX = 100;

export type VisitType =
  | "book"
  | "cards"
  | "field"
  | "paths"
  | "experiments"
  | "lean"
  | "demos"
  | "news"
  | "about"
  | "start"
  | "essay";

export type VisitEntry = {
  path: string;
  title: string;
  type: VisitType | null;
  t: number;
};

const TYPE_LABELS: Record<VisitType, string> = {
  book: "Book",
  cards: "Cards",
  field: "Field",
  paths: "Guided Tour",
  experiments: "Experiments",
  lean: "Lean",
  demos: "Demos",
  news: "News",
  about: "About",
  start: "Start Here",
  essay: "Essays"
};

const CARD_KIND_LABELS: Record<string, string> = {
  concept: "Concept",
  bridge: "Bridge",
  objection: "Objection",
  artifact: "Artifact",
  glossary: "Glossary",
  chapter: "Chapter",
  appendix: "Appendix",
  frontmatter: "Front matter",
  reference: "Reference",
  experiment: "Experiment",
  release: "Release",
  news: "News",
  agenda: "Field agenda"
};

const NAV_LANDING_PATHS = new Set([
  "/book/",
  "/cards/",
  "/field/",
  "/paths/",
  "/experiments/",
  "/lean/",
  "/demos/",
  "/news/",
  "/about/",
  "/start/",
  "/essay/",
  "/glossary/",
  "/references/",
  "/notation/"
]);

const SKIP_PREFIXES = ["/offline", "/search-index", "/impressum", "/feed.xml"];

export function typeLabel(type: VisitType): string {
  return TYPE_LABELS[type];
}

export function kindLabel(kind: string): string {
  return CARD_KIND_LABELS[kind] ?? TYPE_LABELS[kind as VisitType] ?? kind;
}

export function normalizePath(pathname: string): string {
  const trimmed = pathname.split("?")[0].split("#")[0] || "/";
  if (trimmed === "/") return "/";
  return trimmed.endsWith("/") ? trimmed : `${trimmed}/`;
}

export { cardTypeFromPath };

export function visitTypeForPath(pathname: string): VisitType | null {
  const path = normalizePath(pathname);
  const first = path.replace(/^\//, "").split("/")[0] ?? "";
  if (first === "book" || first === "references" || first === "notation") return "book";
  if (first === "cards" || first === "glossary" || first === "badges") return "cards";
  if (first === "field") return "field";
  if (first === "paths") return "paths";
  if (first === "experiments") return "experiments";
  if (first === "lean") return "lean";
  if (first === "demos" || first === "chapter-demos") return "demos";
  if (first === "news" || first === "updates") return "news";
  if (first === "about") return "about";
  if (first === "start" || first === "faq") return "start";
  if (first === "essay") return "essay";
  return null;
}

export function visitKindForEntry(entry: VisitEntry): string | null {
  return cardTypeFromPath(entry.path) ?? entry.type;
}

export function shouldSkipPath(pathname: string): boolean {
  const path = normalizePath(pathname);
  return SKIP_PREFIXES.some((prefix) => path === prefix || path.startsWith(`${prefix}/`));
}

export function stripSiteTitle(title: string, siteName: string): string {
  const suffix = ` | ${siteName}`;
  return title.endsWith(suffix) ? title.slice(0, -suffix.length) : title;
}

export function parseVisitHistory(raw: string | null): VisitEntry[] {
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter((item): item is VisitEntry => {
        if (!item || typeof item !== "object") return false;
        const row = item as VisitEntry;
        return typeof row.path === "string" && typeof row.title === "string" && typeof row.t === "number";
      })
      .slice(0, VISIT_HISTORY_MAX);
  } catch {
    return [];
  }
}

export function prependVisit(history: VisitEntry[], entry: VisitEntry): VisitEntry[] {
  const next = history[0]?.path === entry.path ? history : [entry, ...history];
  return next.slice(0, VISIT_HISTORY_MAX);
}

/** Last page that is not the current path (so `/` does not continue to itself). */
export function continueTarget(history: VisitEntry[], currentPath: string): VisitEntry | null {
  const current = normalizePath(currentPath);
  return history.find((entry) => normalizePath(entry.path) !== current) ?? null;
}

export function latestByType(history: VisitEntry[], currentPath: string): { type: VisitType; entry: VisitEntry }[] {
  const current = normalizePath(currentPath);
  const seen = new Set<VisitType>();
  const out: { type: VisitType; entry: VisitEntry }[] = [];
  for (const entry of history) {
    if (!entry.type) continue;
    if (normalizePath(entry.path) === current) continue;
    if (seen.has(entry.type)) continue;
    seen.add(entry.type);
    out.push({ type: entry.type, entry });
  }
  return out;
}

/** One recent visit per card kind (chapter, concept, bridge, …) or nav area. */
export function latestByKind(history: VisitEntry[], currentPath: string): { kind: string; entry: VisitEntry }[] {
  const current = normalizePath(currentPath);
  const seen = new Set<string>();
  const out: { kind: string; entry: VisitEntry }[] = [];
  for (const entry of history) {
    const path = normalizePath(entry.path);
    if (path === current) continue;
    if (NAV_LANDING_PATHS.has(path)) continue;
    const kind = visitKindForEntry(entry);
    if (!kind) continue;
    if (seen.has(kind)) continue;
    seen.add(kind);
    out.push({ kind, entry });
  }
  return out;
}
