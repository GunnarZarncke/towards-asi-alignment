/** Card type and status badge metadata — aligned with `site/src/content.config.ts`. */

export const CARD_TYPES = [
  "concept",
  "bridge",
  "objection",
  "artifact",
  "glossary",
  "chapter",
  "appendix",
  "frontmatter",
  "reference",
  "experiment",
  "release",
  "news",
  "agenda"
] as const;

export type CardType = (typeof CARD_TYPES)[number];

export const CARD_STATUSES = [
  "established",
  "plausible",
  "framework",
  "bridge",
  "open",
  "negative",
  "reviewed",
  "gravestone"
] as const;

export type CardStatus = (typeof CARD_STATUSES)[number];

export const TYPE_META: Record<
  CardType,
  { title: string; description: string }
> = {
  concept: {
    title: "Concept",
    description:
      "Core ideas, definitions, and operational paraphrases from the manuscript — the vocabulary layer of the framework."
  },
  bridge: {
    title: "Bridge",
    description:
      "Load-bearing assumptions (A-001–A-014 / MB1–MB9) that connect this project's conditional structure to field cruxes."
  },
  objection: {
    title: "Objection",
    description:
      "Hostile readings, failure modes, and counterarguments this project treats as first-class rather than footnotes."
  },
  artifact: {
    title: "Artifact",
    description:
      "Operational templates, audit questions, gates, and checklists intended for eval builders and safety engineers."
  },
  glossary: {
    title: "Glossary",
    description: "Term definitions and notation anchors from Appendix E and the notation index."
  },
  chapter: {
    title: "Chapter",
    description: "Companion card for a numbered book chapter — summary, gems, and cross-links."
  },
  appendix: {
    title: "Appendix",
    description: "Companion card for a built appendix (A–G) — crosswalk, worked example, Lean spine, etc."
  },
  frontmatter: {
    title: "Frontmatter",
    description: "Executive overview, introduction, preface, and other entry-point material."
  },
  reference: {
    title: "Reference",
    description: "Bibliography entry card with publication links and where the source is cited."
  },
  experiment: {
    title: "Experiment",
    description:
      "In-repo or sibling sanity-check line — methodology-building evidence with explicit negative results."
  },
  release: {
    title: "Release",
    description:
      "Manuscript and companion-site release notes — versioned milestones, newest first on the Updates page."
  },
  news: {
    title: "News",
    description:
      "External AI safety incidents and evaluation results — mapped to book chapters; companion-site orientation, not PDF canon."
  },
  agenda: {
    title: "Field agenda",
    description:
      "Coherent AI safety research or advocacy program — introduction, links, map clustering, and bridge coverage on the Field hub."
  }
};

export const STATUS_META: Record<
  CardStatus,
  { title: string; description: string }
> = {
  established: {
    title: "Established",
    description:
      "Widely accepted background or a result this project treats as settled enough to build on without re-deriving."
  },
  plausible: {
    title: "Plausible",
    description:
      "Reasonably supported claim or mechanism — not yet load-bearing proof, but stronger than pure speculation."
  },
  framework: {
    title: "Framework",
    description:
      "Organizing structure, definition, or decomposition — correctness depends on bridges and empirical follow-through."
  },
  bridge: {
    title: "Bridge (status)",
    description:
      "Card status marking bridge-shaped content — distinct from card type 'bridge' (assumption objects)."
  },
  open: {
    title: "Open",
    description:
      "Unresolved research problem or falsifier — this project names it explicitly rather than smuggling it in as done."
  },
  negative: {
    title: "Negative",
    description:
      "Documented failure, bound, or counterexample — including experiment results that limit what may be claimed."
  },
  reviewed: {
    title: "Reviewed",
    description:
      "Manuscript unit that has passed a structured review pass — not a claim that every argument is final."
  },
  gravestone: {
    title: "Gravestone",
    description:
      "Retired object kept for history and leftover formal uses — not on the live certification or matrix path."
  }
};

export function badgeTypeHref(base: string, type: CardType) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}badges/type/${type}/`;
}

export function badgeStatusHref(base: string, status: CardStatus) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}badges/status/${status}/`;
}

export function badgesIndexHref(base: string) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}badges/`;
}
