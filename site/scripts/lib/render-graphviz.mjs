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

let vizPromise;

async function getViz() {
  if (!vizPromise) vizPromise = instance();
  return vizPromise;
}

export async function renderDotToSvg(dotSource, hrefMap = {}) {
  const viz = await getViz();
  const raw = viz.renderString(dotSource, { format: "svg", engine: "dot" });
  return injectNodeLinks(raw, hrefMap);
}
