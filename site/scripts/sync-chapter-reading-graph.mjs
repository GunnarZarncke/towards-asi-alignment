import { execSync } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cardPublicPath, inferTypeFromCardId } from "./lib/card-urls.mjs";
import { parseDot } from "./lib/dot-parse.mjs";
import { renderDotToSvg } from "./lib/render-graphviz.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const DOT_SOURCE = path.join(repoRoot, "metadata/concept-graph/chapter-reading-dependency.dot");
const MD_SOURCE = path.join(repoRoot, "metadata/concept-graph/chapter-reading-dependency.md");
const OUT_DIR = path.join(siteRoot, "public/path-graphs");
const OUT_JSON = path.join(siteRoot, "src/data/chapter-reading-graph.json");
const OUT_SVG = path.join(OUT_DIR, "chapter-reading-dependency.svg");
const OUT_DOT = path.join(OUT_DIR, "chapter-reading-dependency.dot");

function buildChapterHrefMap(dot) {
  const hrefMap = {};
  for (const match of dot.matchAll(/"unit:(ch\d+)"/g)) {
    const chapterId = match[1];
    hrefMap[`unit:${chapterId}`] = cardPublicPath({
      id: `chapters/${chapterId}`,
      type: inferTypeFromCardId(`chapters/${chapterId}`, "chapter")
    });
  }
  return hrefMap;
}

function layerCount(md) {
  const m = md.match(/\*\*Summary:\*\* (\d+) chapters in graph, (\d+) directed edges/);
  return {
    chapters: m ? Number(m[1]) : null,
    edges: m ? Number(m[2]) : null
  };
}

function buildPayload(parsed, stats) {
  const nodes = parsed.nodes.map((node) => {
    const chapterMatch = node.id.match(/^unit:(ch\d+)$/i);
    return {
      ...node,
      chapterId: chapterMatch ? chapterMatch[1].toLowerCase() : null
    };
  });
  return {
    sourceDot: "metadata/concept-graph/chapter-reading-dependency.dot",
    title: parsed.title || "Chapter reading prerequisites",
    chapterCount: stats.chapters,
    edgeCount: stats.edges,
    nodes,
    graphEdges: parsed.edges,
    svgFile: "path-graphs/chapter-reading-dependency.svg",
    dotFile: "path-graphs/chapter-reading-dependency.dot",
    clickableNodes: nodes.filter((n) => n.chapterId).length
  };
}

async function regenerateDot() {
  execSync("python3 scripts/build_chapter_symbol_dependency.py --mode combined", {
    cwd: repoRoot,
    stdio: "inherit"
  });
}

async function main() {
  const check = process.argv.includes("--check");

  if (!check) {
    await regenerateDot();
  }

  const dot = await readFile(DOT_SOURCE, "utf8");
  const md = await readFile(MD_SOURCE, "utf8").catch(() => "");
  const parsed = parseDot(dot);
  const payload = buildPayload(parsed, layerCount(md));
  const stableJson = JSON.stringify(payload, null, 2) + "\n";
  const json =
    JSON.stringify({ ...payload, generatedAt: new Date().toISOString() }, null, 2) + "\n";

  if (check) {
    const mismatches = [];
    try {
      const existing = JSON.parse(await readFile(OUT_JSON, "utf8"));
      const { generatedAt: _ignored, ...existingPayload } = existing;
      if (JSON.stringify(existingPayload, null, 2) + "\n" !== stableJson) {
        mismatches.push(OUT_JSON);
      }
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
      console.error(`sync-chapter-reading-graph --check: ${mismatches.length} file(s) out of date:`);
      for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
      process.exit(1);
    }
    console.log("sync-chapter-reading-graph: check mode, all up to date.");
    return;
  }

  await mkdir(OUT_DIR, { recursive: true });
  const hrefMap = buildChapterHrefMap(dot);
  const svg = await renderDotToSvg(dot, hrefMap);
  await writeFile(OUT_SVG, svg, "utf8");
  await writeFile(OUT_DOT, dot, "utf8");
  await mkdir(path.dirname(OUT_JSON), { recursive: true });
  await writeFile(OUT_JSON, json, "utf8");

  console.log(
    `sync-chapter-reading-graph: wrote reading DAG (${payload.clickableNodes} clickable chapters, ${payload.edgeCount} edges).`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
