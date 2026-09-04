import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bridgeCardSlug } from "./lib/bridge-card-slug.mjs";
import { cardPublicPath } from "./lib/card-urls.mjs";
import { parseDot } from "./lib/dot-parse.mjs";
import { renderDotToSvg } from "./lib/render-graphviz.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const OUT_DIR = path.join(siteRoot, "public/field-graphs");

/** v1 frozen at field cutover; live hub at /field/v2/ (/field/ redirects). */
const GRAPHS = [
  {
    version: "v1",
    sourceDot: "reference/field-agendas/graphs/mb-bridge-dependencies-v1.dot",
    svgFile: "field-graphs/bridge-dependencies-v1.svg",
    dotFile: "field-graphs/bridge-dependencies-v1.dot",
    jsonFile: "src/data/bridge-graph-v1.json"
  },
  {
    version: "v2",
    sourceDot: "reference/field-agendas/graphs/mb-bridge-dependencies-v2.dot",
    svgFile: "field-graphs/bridge-dependencies-v2.svg",
    dotFile: "field-graphs/bridge-dependencies-v2.dot",
    jsonFile: "src/data/bridge-graph-v2.json",
    legacyJsonFile: "src/data/bridge-graph.json"
  }
];

function buildFieldHrefMap(nodes) {
  const hrefMap = {};
  for (const node of nodes) {
    const slug = bridgeCardSlug(node.id);
    if (slug) hrefMap[node.id] = cardPublicPath({ id: slug, type: "bridge" });
  }
  return hrefMap;
}

function buildPayload(parsed, graph) {
  const nodes = parsed.nodes.map((node) => ({
    ...node,
    cardSlug: bridgeCardSlug(node.id)
  }));
  return {
    version: graph.version,
    sourceDot: graph.sourceDot,
    title: parsed.title || "Bridge crux dependencies",
    nodes,
    edges: parsed.edges,
    svgFile: graph.svgFile,
    dotFile: graph.dotFile,
    clickableNodes: nodes.filter((n) => n.cardSlug).length
  };
}

async function syncGraph(graph, check) {
  const dotPath = path.join(repoRoot, graph.sourceDot);
  const dot = await readFile(dotPath, "utf8");
  const parsed = parseDot(dot);
  const payload = buildPayload(parsed, graph);
  const stableJson = JSON.stringify(payload, null, 2) + "\n";
  const json = JSON.stringify({ ...payload, generatedAt: new Date().toISOString() }, null, 2) + "\n";
  const outJson = path.join(siteRoot, graph.jsonFile);
  const outSvg = path.join(OUT_DIR, path.basename(graph.svgFile));
  const outDot = path.join(OUT_DIR, path.basename(graph.dotFile));

  if (check) {
    const mismatches = [];
    try {
      const existing = JSON.parse(await readFile(outJson, "utf8"));
      const { generatedAt: _ignored, ...existingPayload } = existing;
      const existingStable = JSON.stringify(existingPayload, null, 2) + "\n";
      if (existingStable !== stableJson) mismatches.push(outJson);
    } catch {
      mismatches.push(outJson);
    }
    try {
      await readFile(outSvg, "utf8");
      await readFile(outDot, "utf8");
    } catch {
      mismatches.push(outSvg);
    }
    if (graph.legacyJsonFile) {
      const legacyJson = path.join(siteRoot, graph.legacyJsonFile);
      try {
        const existing = JSON.parse(await readFile(legacyJson, "utf8"));
        const { generatedAt: _ignored, ...existingPayload } = existing;
        const existingStable = JSON.stringify(existingPayload, null, 2) + "\n";
        if (existingStable !== stableJson) mismatches.push(legacyJson);
      } catch {
        mismatches.push(legacyJson);
      }
    }
    return mismatches;
  }

  await mkdir(OUT_DIR, { recursive: true });
  const hrefMap = buildFieldHrefMap(payload.nodes);
  const svg = await renderDotToSvg(dot, hrefMap);
  await writeFile(outSvg, svg, "utf8");
  await writeFile(outDot, dot, "utf8");
  await mkdir(path.dirname(outJson), { recursive: true });
  await writeFile(outJson, json, "utf8");
  if (graph.legacyJsonFile) {
    await writeFile(path.join(siteRoot, graph.legacyJsonFile), json, "utf8");
  }

  return payload.clickableNodes;
}

async function main() {
  const check = process.argv.includes("--check");
  const allMismatches = [];
  let totalClickable = 0;

  for (const graph of GRAPHS) {
    const result = await syncGraph(graph, check);
    if (check) {
      allMismatches.push(...result);
    } else {
      totalClickable += result;
    }
  }

  if (check) {
    if (allMismatches.length > 0) {
      console.error(`sync-bridge-graph --check: ${allMismatches.length} file(s) out of date:`);
      for (const f of allMismatches) console.error(`  ${path.relative(repoRoot, f)}`);
      process.exit(1);
    }
    console.log("sync-bridge-graph: check mode, all up to date.");
    return;
  }

  console.log(
    `sync-bridge-graph: wrote v1 + v2 bridge dependency graphs (${totalClickable} clickable nodes on v2).`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
