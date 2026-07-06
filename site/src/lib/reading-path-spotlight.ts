import type { CollectionEntry } from "astro:content";
import demosIndex from "../data/demos.json";
import experimentsIndex from "../data/experiments.json";
import bookIndex from "../data/book.json";
import { bookHref, cardHref, chapterCardFor } from "./site-urls";
import type { ReadingPathSpotlight, ReadingPathSpotlightLink } from "./reading-paths";

type CardEntry = CollectionEntry<"cards">;

type SpotlightContext = {
  base: string;
  cards: CardEntry[];
  withBase: (route: string) => string;
};

const bookTitleFor = (chapterId: string) => {
  const chapter = bookIndex.chapters.find((entry) => entry.id === chapterId);
  if (chapter) return chapter.title;
  if (chapterId === "frontmatter") return "Executive Overview";
  return chapterId;
};

export function resolveSpotlightTarget(
  link: Pick<ReadingPathSpotlightLink, "kind" | "ref">,
  ctx: SpotlightContext
) {
  const { base, cards, withBase } = ctx;

  switch (link.kind) {
    case "book":
      return bookHref(base, link.ref);
    case "demo": {
      const demo = demosIndex.demos.find((entry) => entry.id === link.ref);
      return demo ? withBase(demo.sitePath) : withBase("/demos/");
    }
    case "experiment":
      return withBase(`/experiments/#${link.ref}`);
    case "lean":
      return withBase(`/lean/${link.ref === "overview" ? "" : `${link.ref}/`}`);
    case "card":
      return cardHref(base, link.ref);
    default:
      return withBase("/");
  }
}

export function defaultPrimaryLabel(spotlight: ReadingPathSpotlight, ctx: SpotlightContext) {
  if (spotlight.primaryLabel) return spotlight.primaryLabel;

  switch (spotlight.kind) {
    case "book": {
      const card = chapterCardFor(ctx.cards, spotlight.ref);
      return card ? `Read ${card.data.title}` : `Read ${bookTitleFor(spotlight.ref)}`;
    }
    case "demo": {
      const demo = demosIndex.demos.find((entry) => entry.id === spotlight.ref);
      return demo ? `Open ${demo.title}` : "Open demo";
    }
    case "experiment": {
      const line = experimentsIndex.lines.find((entry) => entry.id === spotlight.ref);
      return line ? `Read ${line.title}` : "Open experiment line";
    }
    case "lean":
      return spotlight.ref === "overview" ? "Open Lean proof spine" : "Open Lean graph";
    case "card": {
      const card = ctx.cards.find((entry) => entry.id === spotlight.ref);
      return card ? `Read ${card.data.title}` : "Open card";
    }
    default:
      return "Open";
  }
}
