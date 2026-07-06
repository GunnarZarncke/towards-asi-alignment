/** Astro static routes lower-case path segments; canonical ids may use mixed case (e.g. appD). */

export function routeSlug(segment: string) {
  return segment.toLowerCase();
}

export function bookHref(base: string, chapterId: string) {
  return cardHref(base, `chapters/${chapterId}`);
}

export function cardHref(base: string, cardId: string) {
  const path = cardId.split("/").map((part) => encodeURIComponent(routeSlug(part))).join("/");
  return `${base}${`cards/${path}/`.replace(/^\/+/, "")}`;
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

/** Relative PDF link from generated book chapter markdown (book/chNN/). */
export const BOOK_CHAPTER_PDF_HREF = "../../towards-superintelligence-alignment.pdf";

export function pathHref(base: string, pathId: string) {
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}paths/${encodeURIComponent(pathId)}/`;
}
