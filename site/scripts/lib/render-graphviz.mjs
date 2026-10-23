import { instance } from "@viz-js/viz";

function decodeEntities(value) {
  return value
    .replace(/&#45;/g, "-")
    .replace(/&#58;/g, ":")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

/**
 * Wrap Graphviz node groups in SVG link elements.
 * Node ids come from the `<title>` inside each `<g class="node">`.
 */
export function injectNodeLinks(svg, hrefMap) {
  return svg.replace(
    /<g id="(node\d+)" class="node">\s*<title>([^<]+)<\/title>([\s\S]*?)<\/g>/g,
    (match, gid, rawId, body) => {
      const nodeId = decodeEntities(rawId.trim());
      const href = hrefMap[nodeId];
      if (!href) return match;
      return `<a xlink:href="${href}" class="lean-graph-node"><g id="${gid}" class="node"><title>${rawId}</title>${body}</g></a>`;
    }
  );
}

function edgeTitleKey(rawTitle) {
  const decoded = decodeEntities(rawTitle.trim());
  return decoded.replace(/--/g, "->");
}

/**
 * Wrap Graphviz edge groups so labels (and strokes) can link out.
 * Titles look like `src->tgt` or `src--tgt` (undirected).
 */
export function injectEdgeLinks(svg, hrefMap) {
  if (!hrefMap || Object.keys(hrefMap).length === 0) return svg;
  return svg.replace(
    /<g id="(edge\d+)" class="edge">\s*<title>([^<]+)<\/title>([\s\S]*?)<\/g>/g,
    (match, gid, rawTitle, body) => {
      const key = edgeTitleKey(rawTitle);
      const href = hrefMap[key] || hrefMap[rawTitle.trim()];
      if (!href) return match;
      return `<a xlink:href="${href}" class="lean-graph-edge" target="_blank" rel="noopener noreferrer"><g id="${gid}" class="edge"><title>${rawTitle}</title>${body}</g></a>`;
    }
  );
}

let vizPromise;

async function getViz() {
  if (!vizPromise) vizPromise = instance();
  return vizPromise;
}

export async function renderDotToSvg(dotSource, hrefMap = {}, edgeHrefMap = {}) {
  const viz = await getViz();
  const raw = viz.renderString(dotSource, { format: "svg", engine: "dot" });
  return injectEdgeLinks(injectNodeLinks(raw, hrefMap), edgeHrefMap);
}
