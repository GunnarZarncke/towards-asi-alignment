import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseDot } from "./lib/dot-parse.mjs";
import { renderDotToSvg } from "./lib/render-graphviz.mjs";
import { lensByNodeId, lensPublicPath, leanHrefForEdge } from "./lib/lenses-data.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const SOURCE_DOT = "drafts/alignment-frames-relations.dot";
const OUT_DIR = path.join(siteRoot, "public/field-graphs");
const SVG_NAME = "alignment-frames-relations.svg";
const DOT_NAME = "alignment-frames-relations.dot";

function nodeHrefMap(nodes) {
  const hrefMap = {};
  for (const node of nodes) {
    const lens = lensByNodeId(node.id);
    if (lens) hrefMap[node.id] = lensPublicPath(lens.slug);
  }
  return hrefMap;
}

function edgeHrefMap(edges) {
  const hrefMap = {};
  for (const edge of edges) {
    if ((edge.style || "").includes("invis")) continue;
    const href = leanHrefForEdge(edge);
    if (!href) continue;
    hrefMap[`${edge.from}->${edge.to}`] = href;
    hrefMap[`${edge.from}--${edge.to}`] = href;
  }
  return hrefMap;
}

async function main() {
  const check = process.argv.includes("--check");
  const dotPath = path.join(repoRoot, SOURCE_DOT);
  const dot = await readFile(dotPath, "utf8");
  const parsed = parseDot(dot);
  const hrefMap = nodeHrefMap(parsed.nodes);
  const edges = parsed.edges;
  const svg = await renderDotToSvg(dot, hrefMap, edgeHrefMap(edges));
  const outSvg = path.join(OUT_DIR, SVG_NAME);
  const outDot = path.join(OUT_DIR, DOT_NAME);

  if (check) {
    try {
      const existing = await readFile(outSvg, "utf8");
      if (existing !== svg) {
        console.error("sync-lens-graph --check: SVG out of date");
        process.exit(1);
      }
      await readFile(outDot, "utf8");
    } catch {
      console.error("sync-lens-graph --check: missing public graph files");
      process.exit(1);
    }
    console.log("sync-lens-graph: check mode, all up to date.");
    return;
  }

  await mkdir(OUT_DIR, { recursive: true });
  await writeFile(outSvg, svg, "utf8");
  await writeFile(outDot, dot, "utf8");
  const clickable = Object.keys(hrefMap).length;
  console.log(`sync-lens-graph: wrote ${SVG_NAME} (${clickable} clickable nodes).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
