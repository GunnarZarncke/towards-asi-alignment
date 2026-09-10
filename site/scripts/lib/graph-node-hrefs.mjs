/** Site-root hrefs (leading `/`) so inlined SVGs resolve on any page. */

import { cardPublicPath } from "./card-urls.mjs";

const SUB_SPINE_GRAPHS = {
  S1: "boundary-measurement",
  S2: "value-transport",
  S3: "correction-successors",
  S4: "selection-limits"
};

export function nodeHrefFromGraphPage(nodeId, { cardSlug = null } = {}) {
  const sub = SUB_SPINE_GRAPHS[nodeId];
  if (sub) return `/lean/graph/${sub}/`;
  if (cardSlug) return cardPublicPath({ id: cardSlug, type: "bridge" });
  return `/lean/node/${encodeURIComponent(nodeId)}/`;
}

export function buildGraphHrefMap(nodes) {
  return Object.fromEntries(
    nodes.map((node) => [node.id, nodeHrefFromGraphPage(node.id, node)])
  );
}
