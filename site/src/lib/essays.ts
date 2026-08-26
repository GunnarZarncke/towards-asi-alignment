import type { CollectionEntry } from "astro:content";

export type EssayCard = CollectionEntry<"cards">;

export function isEssayCard(card: CollectionEntry<"cards">): boolean {
  return card.data.type === "essay";
}

export function spineAndCloser(cards: CollectionEntry<"cards">[]): EssayCard[] {
  return cards
    .filter(
      (card) =>
        card.data.type === "essay" &&
        (card.data.essayRole === "spine" || card.data.essayRole === "closer")
    )
    .sort((a, b) => (a.data.essayOrder ?? 99) - (b.data.essayOrder ?? 99));
}

export function branchEssays(cards: CollectionEntry<"cards">[]): EssayCard[] {
  return cards
    .filter((card) => card.data.type === "essay" && card.data.essayRole === "branch")
    .sort((a, b) => a.data.title.localeCompare(b.data.title));
}

export function totalSpineMinutes(cards: CollectionEntry<"cards">[]): number {
  return spineAndCloser(cards).reduce((sum, card) => sum + (card.data.minutes ?? 0), 0);
}

export function findEssay(cards: CollectionEntry<"cards">[], slug: string): EssayCard | undefined {
  const normalized = slug.replace(/^essays\//, "").toLowerCase();
  return cards.find(
    (card) => card.data.type === "essay" && card.id.toLowerCase() === normalized
  );
}

/** First prose paragraphs of an essay body, skipping figures, asides, and branch chips. */
export function essayTeaserMarkdown(body: string, maxParagraphs = 2): string {
  const blocks = body.split(/\n\n+/);
  const paras: string[] = [];
  for (const block of blocks) {
    const trimmed = block.trim();
    if (!trimmed) continue;
    if (
      trimmed.startsWith("<figure") ||
      trimmed.startsWith("<aside") ||
      trimmed.startsWith("<a class=\"essay-branch")
    ) {
      continue;
    }
    paras.push(trimmed);
    if (paras.length >= maxParagraphs) break;
  }
  return paras.join("\n\n");
}
