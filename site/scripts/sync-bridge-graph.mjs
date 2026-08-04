import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bridgeCardSlug } from "./lib/bridge-card-slug.mjs";
import { parseDot } from "./lib/dot-parse.mjs";
import { renderDotToSvg } from "./lib/render-graphviz.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const DOT_SOURCE = path.join(repoRoot, "reference/field-agendas/graphs/mb-bridge-dependencies.dot");
const OUT_DIR = path.join(siteRoot, "public/field-graphs");
const OUT_JSON = path.join(siteRoot, "src/data/bridge-graph.json");
const OUT_SVG = path.join(OUT_DIR, "bridge-dependencies.svg");
const OUT_DOT = path.join(OUT_DIR, "bridge-dependencies.dot");

/** Relative from `/field/` pages to bridge cards. */
function buildFieldHrefMap(nodes) {
  const hrefMap = {};
  for (const node of nodes) {
    const slug = bridgeCardSlug(node.id);
    if (slug) hrefMap[node.id] = `../cards/${slug}/`;
  }
  return hrefMap;
}

function buildPayload(parsed) {
  const nodes = parsed.nodes.map((node) => ({
    ...node,
    cardSlug: bridgeCardSlug(node.id)
  }));
  return {
    sourceDot: "reference/field-agendas/graphs/mb-bridge-dependencies.dot",
    title: parsed.title || "Bridge crux dependencies",
    nodes,
    edges: parsed.edges,
    svgFile: "field-graphs/bridge-dependencies.svg",
    dotFile: "field-graphs/bridge-dependencies.dot",
    clickableNodes: nodes.filter((n) => n.cardSlug).length
  };
}

async function main() {
  const check = process.argv.includes("--check");
  const dot = await readFile(DOT_SOURCE, "utf8");
  const parsed = parseDot(dot);
  const payload = buildPayload(parsed);
  const stableJson = JSON.stringify(payload, null, 2) + "\n";
  const json = JSON.stringify({ ...payload, generatedAt: new Date().toISOString() }, null, 2) + "\n";

  if (check) {
    const mismatches = [];
    try {
      const existing = JSON.parse(await readFile(OUT_JSON, "utf8"));
      const { generatedAt: _ignored, ...existingPayload } = existing;
      const existingStable = JSON.stringify(existingPayload, null, 2) + "\n";
      if (existingStable !== stableJson) mismatches.push(OUT_JSON);
    } catch {
      mismatches.push(OUT_JSON);
    }
    try {
      await readFile(OUT_SVG, "utf8");
      await readFile(OUT_DOT, "utf8");
    } catch {
      mismatches.push(OUT_SVG);
    }
    if (mismatches.length > 0) {
      console.error(`sync-bridge-graph --check: ${mismatches.length} file(s) out of date:`);
      for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
      process.exit(1);
    }
    console.log("sync-bridge-graph: check mode, all up to date.");
    return;
  }

  await mkdir(OUT_DIR, { recursive: true });
  const hrefMap = buildFieldHrefMap(payload.nodes);
  const svg = await renderDotToSvg(dot, hrefMap);
  await writeFile(OUT_SVG, svg, "utf8");
  await writeFile(OUT_DOT, dot, "utf8");
  await mkdir(path.dirname(OUT_JSON), { recursive: true });
  await writeFile(OUT_JSON, json, "utf8");

  console.log(
    `sync-bridge-graph: wrote bridge dependency graph (${payload.clickableNodes} clickable nodes).`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
