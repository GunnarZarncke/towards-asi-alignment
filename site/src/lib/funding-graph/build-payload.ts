import type { CollectionEntry } from "astro:content";
import { cardHrefForCard } from "../site-urls";

export type FundingGraphNode = {
  id: string;
  label: string;
  href: string;
  fundingState?: string;
  doneState?: string;
};

export type FundingGraphEdge = {
  source: string;
  target: string;
};

export type FundingGraphPayload = {
  nodes: FundingGraphNode[];
  edges: FundingGraphEdge[];
};

const SHORT_LABEL: Record<string, string> = {
  "unsupervised-agent-discovery": "UAD",
  "tsa-writing": "TSA",
  "practical-uad": "Practical UAD",
  "alignment-observability-platform": "Observability",
  "alignment-attractor-hub": "Attractor hub",
  "corrigibility-measurement": "Corrigibility",
  "multi-principal-testbed": "Multi-principal testbed",
  "competitive-lab-selection": "Competitive labs",
  "alignment-crux-map": "Crux Map"
};

export function fundingNodeLabel(slug: string) {
  return SHORT_LABEL[slug] ?? slug;
}

type CardEntry = CollectionEntry<"cards">;

export function buildFundingGraphPayload(
  base: string,
  fundingCards: CardEntry[]
): FundingGraphPayload {
  const slug = (id: string) => id.replace(/^funding\//, "");

  const nodes: FundingGraphNode[] = fundingCards.map((card) => {
    const id = slug(card.id);
    return {
      id,
      label: fundingNodeLabel(id),
      href: cardHrefForCard(base, card),
      fundingState: card.data.fundingState,
      doneState: card.data.doneState
    };
  });

  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges: FundingGraphEdge[] = [];

  for (const card of fundingCards) {
    const target = slug(card.id);
    for (const depId of card.data.dependsOn) {
      const source = depId.replace(/^funding\//, "");
      if (nodeIds.has(source) && nodeIds.has(target)) {
        edges.push({ source, target });
      }
    }
  }

  return { nodes, edges };
}
