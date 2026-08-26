/** Relative links from `/lean/graph/{slug}/` pages (work with any Astro base). */

const SUB_SPINE_GRAPHS = {
  S1: "boundary-measurement",
  S2: "value-transport",
  S3: "correction-successors",
  S4: "selection-limits"
};

export function nodeHrefFromGraphPage(nodeId, { cardSlug = null } = {}) {
  const sub = SUB_SPINE_GRAPHS[nodeId];
  if (sub) return `../../graph/${sub}/`;
  if (cardSlug) return `../../cards/bridge/${cardSlug.toLowerCase()}/`;
  return `../../node/${encodeURIComponent(nodeId)}/`;
}

export function buildGraphHrefMap(nodes) {
  return Object.fromEntries(
    nodes.map((node) => [node.id, nodeHrefFromGraphPage(node.id, node)])
  );
}
