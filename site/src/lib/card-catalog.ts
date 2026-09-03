import { ALL_GEM_SLUGS } from "./gems";

export type CatalogCard = {
  id: string;
  data: {
    title: string;
    summary: string;
    type: string;
    status: string;
    bookPageId?: string;
    experimentLineId?: string;
    experimentOverview?: boolean;
    releasedAt?: string;
  };
};

export type CatalogEntry = {
  id: string;
  title: string;
  summary: string;
  type: string;
  status: string;
};

const toEntry = (card: CatalogCard): CatalogEntry => ({
  id: card.id,
  title: card.data.title,
  summary: card.data.summary,
  type: card.data.type,
  status: card.data.status
});

const chapterRank = (card: CatalogCard) => Number(card.data.bookPageId?.replace("ch", "") || 0);

const appendixRank = (card: CatalogCard) => {
  if (card.data.type === "frontmatter") return 0;
  return 1 + (card.data.bookPageId || "").charCodeAt(3);
};

export function highlightEntries(cards: CatalogCard[]): CatalogEntry[] {
  const byId = new Map(cards.map((card) => [card.id, card]));
  return ALL_GEM_SLUGS.map((slug) => byId.get(slug))
    .filter((card): card is CatalogCard => Boolean(card))
    .map(toEntry);
}

export function cardCatalogSections(
  cards: CatalogCard[],
  fieldProjectionGems: string[],
  experimentsData: { lines: { id: string; order: number }[] }
): { title: string; id: string; cards: CatalogEntry[] }[] {
  const byType = (type: string) =>
    cards
      .filter((card) => card.data.type === type)
      .sort((a, b) => a.data.title.localeCompare(b.data.title))
      .map(toEntry);

  const chapters = cards
    .filter((card) => card.data.type === "chapter")
    .sort((a, b) => chapterRank(a) - chapterRank(b))
    .map(toEntry);

  const appendices = cards
    .filter((card) => ["appendix", "frontmatter"].includes(card.data.type))
    .sort((a, b) => appendixRank(a) - appendixRank(b))
    .map(toEntry);

  const concepts = byType("concept").filter((card) => !fieldProjectionGems.includes(card.id));
  const referenceIndexCard = cards.find((card) => card.id === "reference-index");
  const referenceCards = cards
    .filter((card) => card.data.type === "reference")
    .sort((a, b) => a.data.title.localeCompare(b.data.title))
    .map(toEntry);
  const referencesSection = [
    ...(referenceIndexCard ? [toEntry(referenceIndexCard)] : []),
    ...referenceCards
  ];
  const experimentOrder = new Map(experimentsData.lines.map((line) => [line.id, line.order]));
  const experiments = cards
    .filter((card) => card.data.type === "experiment")
    .sort((a, b) => {
      const aOverview = a.data.experimentOverview === true;
      const bOverview = b.data.experimentOverview === true;
      if (aOverview !== bOverview) return aOverview ? -1 : 1;
      const orderA = experimentOrder.get(a.data.experimentLineId ?? "") ?? 999;
      const orderB = experimentOrder.get(b.data.experimentLineId ?? "") ?? 999;
      if (orderA !== orderB) return orderA - orderB;
      return a.data.title.localeCompare(b.data.title);
    })
    .map(toEntry);
  const fieldProjections = cards
    .filter((card) => fieldProjectionGems.includes(card.id))
    .sort((a, b) => fieldProjectionGems.indexOf(a.id) - fieldProjectionGems.indexOf(b.id))
    .map(toEntry);
  const releaseVersions = cards
    .filter((card) => card.data.type === "release" && card.id !== "releases-updates")
    .sort((a, b) => (b.data.releasedAt ?? "").localeCompare(a.data.releasedAt ?? ""))
    .map(toEntry);

  return [
    { title: "Chapters", id: "chapters", cards: chapters },
    { title: "Glossary", id: "glossary", cards: byType("glossary") },
    { title: "Concepts", id: "concepts", cards: concepts },
    { title: "Bridges", id: "bridges", cards: byType("bridge") },
    { title: "Field projections", id: "field-projections", cards: fieldProjections },
    { title: "Field agendas", id: "field-agendas", cards: byType("agenda") },
    { title: "Funding opportunities", id: "funding", cards: byType("funding") },
    { title: "Experiments", id: "experiments", cards: experiments },
    { title: "Objections & caveats", id: "objections", cards: byType("objection") },
    { title: "Artifacts", id: "artifacts", cards: byType("artifact") },
    { title: "Appendices & front matter", id: "appendices", cards: appendices },
    { title: "Releases & updates", id: "releases", cards: releaseVersions },
    { title: "Reference cards", id: "references", cards: referencesSection }
  ];
}
