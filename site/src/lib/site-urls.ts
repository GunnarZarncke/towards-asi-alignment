/** Astro static routes lower-case path segments; canonical ids may use mixed case (e.g. appD). */

export function routeSlug(segment: string) {
  return segment.toLowerCase();
}

export function bookHref(base: string, chapterId: string) {
  return `${base}${`book/${routeSlug(chapterId)}/`.replace(/^\/+/, "")}`;
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
  return cards.find(
    (card) =>
      card.data.bookPageId === chapterId &&
      ["chapter", "appendix", "frontmatter"].includes(card.data.type)
  );
}

export const WORKED_EXAMPLE_BOOK_ID = "appD";
export const WORKED_EXAMPLE_CARD_ID = "chapters/appD";
