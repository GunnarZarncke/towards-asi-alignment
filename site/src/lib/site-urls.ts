/** Astro static routes lower-case path segments; canonical ids may use mixed case (e.g. appD). */

import type { CardType } from "./badges";
import {
  bookFullPublicHref,
  bookPublicHref,
  cardPublicHref,
  cardPublicPath,
  cardRouteSlug,
  cardTypeFromPath,
  inferTypeFromCardId,
  legacyCardRedirectPath,
  legacyCardRouteSlug,
  resolveCardFromRoute,
  routeSlug
} from "../../scripts/lib/card-urls.mjs";

export {
  cardPublicPath,
  cardRouteSlug,
  cardTypeFromPath,
  inferTypeFromCardId,
  legacyCardRedirectPath,
  legacyCardRouteSlug,
  resolveCardFromRoute,
  routeSlug
};

export function bookHref(base: string, chapterId: string) {
  return bookPublicHref(base, chapterId);
}

export function bookFullHref(base: string, chapterId: string) {
  return bookFullPublicHref(base, chapterId);
}

/** Canonical card URL from collection id + optional type (type required for flat ids). */
export function cardHref(base: string, cardId: string, type?: CardType | null) {
  return cardPublicHref(base, { id: cardId, type: type ?? undefined });
}

export function cardHrefForCard(base: string, card: { id: string; data: { type: CardType } }) {
  return cardPublicHref(base, { id: card.id, type: card.data.type });
}

export const FIRST_ESSAY_ID = "the-chatbot-passed-the-test";

export function essayHref(base: string, slug: string) {
  const id = slug.split("/").pop() ?? slug;
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}essay/${encodeURIComponent(routeSlug(id))}/`;
}

export function firstEssayHref(base: string) {
  return essayHref(base, FIRST_ESSAY_ID);
}

export function normalizeCardId(id: string) {
  return id.split("/").map(routeSlug).join("/");
}

export function resolveCard<T extends { id: string }>(cards: T[], slug: string) {
  const normalized = normalizeCardId(slug);
  return cards.find((card) => normalizeCardId(card.id) === normalized);
}

export function chapterCardFor<T extends { id: string; data: { bookPageId?: string; type: string } }>(
  cards: T[],
  chapterId: string
) {
  const normalized = routeSlug(chapterId);
  return cards.find(
    (card) =>
      routeSlug(card.data.bookPageId ?? "") === normalized &&
      ["chapter", "appendix", "frontmatter"].includes(card.data.type)
  );
}

export const WORKED_EXAMPLE_BOOK_ID = "appD";
export const WORKED_EXAMPLE_CARD_ID = "chapters/appD";

export const BOOK_PDF_FILENAME = "towards-superintelligence-alignment.pdf";

/** Root-relative PDF URL for the deployed site (works in nav and absolute links). */
export function pdfHref(base: string) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}${BOOK_PDF_FILENAME}`;
}

/** Relative PDF link from generated book chapter markdown (cards/chapters/{id}/). */
export const BOOK_CHAPTER_PDF_HREF = "../../../towards-superintelligence-alignment.pdf";

/** Classify an outbound URL for the small link-type indicator: PDF file, GitHub-hosted, or other external. */
export function classifyLinkKind(url: string): "pdf" | "github" | "external" {
  if (/\.pdf(?:[?#]|$)/i.test(url)) return "pdf";
  if (/^https?:\/\/(www\.)?github\.com\//i.test(url)) return "github";
  return "external";
}

export function pathHref(base: string, pathId: string) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}paths/${encodeURIComponent(pathId)}/`;
}
