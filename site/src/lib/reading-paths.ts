import yaml from "js-yaml";
import { PATH_ORDER, sortPaths } from "./path-order";

export type ReadingPathStep = {
  kind: "card" | "demo" | "experiment" | "book" | "lean";
  ref: string;
  note?: string;
};

export type ReadingPathSpotlightLink = {
  kind: ReadingPathStep["kind"];
  ref: string;
  label: string;
};

export type ReadingPathSpotlight = {
  eyebrow: string;
  title: string;
  blurb: string;
  kind: ReadingPathStep["kind"];
  ref: string;
  primaryLabel?: string;
  secondary?: ReadingPathSpotlightLink;
};

/** Optional site page linked from the path card on /paths/ (not a reading step). */
export type ReadingPathCompanionLink = {
  href: string;
  label: string;
};

export type ReadingPathRecord = {
  id: string;
  title: string;
  audience: string;
  summary: string;
  steps: ReadingPathStep[];
  featuredSpotlight?: ReadingPathSpotlight;
  companionLink?: ReadingPathCompanionLink;
  body: string;
};

const rawModules = import.meta.glob("../content/reading-paths/*.md", {
  query: "?raw",
  import: "default",
  eager: true
}) as Record<string, string>;

function pathIdFromKey(key: string) {
  return key.replace(/^.*\//, "").replace(/\.md$/, "");
}

function parsePathFile(raw: string, id: string): ReadingPathRecord {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) {
    throw new Error(`Missing frontmatter in reading path ${id}`);
  }
  const data = yaml.load(match[1]) as Omit<ReadingPathRecord, "id" | "body">;
  return { id, ...data, body: match[2].trimEnd() };
}

/** Canonical reading-path list from src/content/reading-paths/*.md. */
export function getReadingPaths(): ReadingPathRecord[] {
  return sortPaths(
    Object.entries(rawModules).map(([key, raw]) => parsePathFile(raw, pathIdFromKey(key)))
  );
}

export function getReadingPath(id: string): ReadingPathRecord | undefined {
  return getReadingPaths().find((entry) => entry.id === id);
}

export function readingPathIds(): string[] {
  const ids = getReadingPaths().map((entry) => entry.id);
  return ids.length > 0 ? ids : [...PATH_ORDER];
}
