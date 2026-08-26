import type { CollectionEntry } from "astro:content";
import { badgeStatusHref, badgeTypeHref } from "./badges";
import {
  bookHref,
  cardHref,
  chapterCardFor,
  essayHref,
  resolveCard
} from "./site-urls";
import type { ReadingPathStep } from "./reading-paths";
import demosIndex from "../data/demos.json";
import experimentsIndex from "../data/experiments.json";
import bookIndex from "../data/book.json";

export type StepBadge = {
  label: string;
  variant?: string;
  href?: string;
};

export type ResolvedReadingPathStep = {
  href: string;
  title: string;
  summary: string;
  kind: ReadingPathStep["kind"];
  ref: string;
  bookChapterId?: string;
  cardSlug?: string;
  badges: StepBadge[];
  newTab?: boolean;
};

export type ReadingPathStepContext = {
  base: string;
  cards: CollectionEntry<"cards">[];
  withBase: (route: string) => string;
};

const bookTitleFor = (chapterId: string) => {
  const chapter = bookIndex.chapters.find((entry) => entry.id === chapterId);
  if (chapter) return chapter.title;
  if (chapterId === "frontmatter") return "Executive Overview";
  return chapterId;
};

export function resolveReadingPathStep(
  step: ReadingPathStep,
  context: ReadingPathStepContext
): ResolvedReadingPathStep | null {
  const { base, cards, withBase } = context;
  const cardById = new Map(cards.map((card) => [card.id, card]));

  switch (step.kind) {
    case "card": {
      const card = resolveCard(cards, step.ref) ?? cardById.get(step.ref);
      if (!card) return null;
      return {
        kind: step.kind,
        ref: step.ref,
        href: card.data.type === "essay" ? essayHref(base, card.id) : cardHref(base, card.id),
        cardSlug: card.id,
        title: card.data.title,
        summary: step.note ?? card.data.summary,
        badges: [
          { label: card.data.type, href: badgeTypeHref(base, card.data.type) },
          {
            label: card.data.status,
            variant: card.data.status,
            href: badgeStatusHref(base, card.data.status)
          }
        ]
      };
    }
    case "demo": {
      const demo = demosIndex.demos.find((entry) => entry.id === step.ref);
      if (!demo) return null;
      const badges: StepBadge[] = [
        { label: "demo", variant: "framework", href: withBase("/demos/") }
      ];
      if (demo.chapterId) {
        badges.push({ label: demo.chapterId, variant: "framework" });
      }
      badges.push({ label: demo.kind.replace(/-/g, " ") });
      return {
        kind: step.kind,
        ref: step.ref,
        href: withBase(demo.sitePath),
        title: demo.title,
        summary: step.note ?? demo.summary,
        badges,
        newTab: true
      };
    }
    case "experiment": {
      const line = experimentsIndex.lines.find((entry) => entry.id === step.ref);
      if (!line) return null;
      return {
        kind: step.kind,
        ref: step.ref,
        href: cardHref(base, `experiments/${line.id}`),
        title: line.title,
        summary: step.note ?? line.role.trim(),
        badges: [
          { label: "experiment", variant: "open", href: withBase("/experiments/") },
          { label: "sanity check", variant: "open" },
          { label: `line ${line.order}`, variant: "framework" }
        ]
      };
    }
    case "book": {
      const chapterCard = chapterCardFor(cards, step.ref);
      const title = chapterCard?.data.title ?? bookTitleFor(step.ref);
      const summary =
        step.note ??
        chapterCard?.data.summary ??
        "Read on the site.";
      const bookType = chapterCard?.data.type ?? (step.ref === "frontmatter" ? "frontmatter" : "chapter");
      const bookStatus = chapterCard?.data.status ?? "reviewed";
      return {
        kind: step.kind,
        ref: step.ref,
        bookChapterId: step.ref.toLowerCase(),
        href: bookHref(base, step.ref),
        title,
        summary,
        badges: [
          { label: bookType, href: badgeTypeHref(base, bookType) },
          {
            label: bookStatus,
            variant: bookStatus,
            href: badgeStatusHref(base, bookStatus)
          },
          { label: step.ref, variant: "framework" }
        ]
      };
    }
    case "lean": {
      const leanRoutes: Record<string, { title: string; summary: string }> = {
        overview: {
          title: "Lean dependency spine",
          summary: "Machine-checked conditional skeleton — proofs, bridges, counterexamples."
        },
        "graph/overview": {
          title: "Overview dependency graph",
          summary: "Visual map of what the formal spine checks."
        }
      };
      const entry = leanRoutes[step.ref];
      if (!entry) return null;
      return {
        kind: step.kind,
        ref: step.ref,
        href: withBase(`/lean/${step.ref === "overview" ? "" : `${step.ref}/`}`),
        title: entry.title,
        summary: step.note ?? entry.summary,
        badges: [
          { label: "lean", variant: "framework", href: withBase("/lean/") },
          { label: step.ref.replace("/", " · "), variant: "plausible" }
        ]
      };
    }
    default:
      return null;
  }
}
