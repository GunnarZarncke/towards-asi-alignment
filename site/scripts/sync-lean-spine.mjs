import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseDot } from "./lib/dot-parse.mjs";
import { buildGraphHrefMap } from "./lib/graph-node-hrefs.mjs";
import { attachSpineSources } from "./lib/spine-source-index.mjs";
import { bridgeCardSlug } from "./lib/bridge-card-slug.mjs";
import { renderDotToSvg } from "./lib/render-graphviz.mjs";
import {
  buildLean4WebUrl,
  CONSERVATIVE_MAX_URL_LENGTH,
  DEFAULT_MAX_URL_LENGTH
} from "./lib/lean4web-url.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const GRAPH_DIR = path.join(repoRoot, "context", "lean_proof_graphs");
const PLAYGROUND_DIR = path.join(repoRoot, "formal", "playgrounds");
const LEDGER_PATH = path.join(repoRoot, "formal", "axiom-ledger.json");
const CARDS_DIR = path.join(siteRoot, "src", "content", "cards");
const OUT_PATH = path.join(siteRoot, "src", "data", "lean-spine.json");
const GRAPH_SVG_DIR = path.join(siteRoot, "public", "lean-graphs");
const FORMAL_ROOT = path.join(repoRoot, "formal", "AlignmentProofSpine");
const NODE_ALIAS_PATH = path.join(repoRoot, "context", "lean_graph_node_aliases.json");

const GRAPH_ORDER = [
  { id: "00-overview", slug: "overview", title: "Overview: four spines into certified-class safety" },
  { id: "01-boundary-measurement", slug: "boundary-measurement", title: "Spine I: Boundary and measurement" },
  { id: "02-value-transport", slug: "value-transport", title: "Spine II: Value and transport" },
  { id: "03-correction-successors", slug: "correction-successors", title: "Spine III: Correction and successors" },
  { id: "04-selection-limits", slug: "selection-limits", title: "Spine IV: Selection and limits" },
  { id: "05-field-subsumptions", slug: "field-subsumptions", title: "Field-agenda crosswalk" }
];

const SPINE_ROOT_FILE = path.join(repoRoot, "formal", "AlignmentProofSpine.lean");

// Hand-written titles/chapter ranges for modules that predate the derived
// list. Every other module gets its title from its own docstring heading
// and its chapter column from the module table in AlignmentProofSpine.lean.
const MODULE_OVERRIDES = new Map([
  ["Core", { title: "Core carriers and bridges", chapters: "foundations" }],
  ["Boundaries", { title: "Boundaries and measurement", chapters: "6–7, 10, 36" }],
  ["Capability", { title: "Capability and BIQ", chapters: "11–14, 33, 36" }],
  ["Bundles", { title: "Value bundles and transport", chapters: "15–23, 30" }],
  ["Correction", { title: "Correction channels", chapters: "25–29, 41–43" }],
  ["Successors", { title: "Successors and continuity", chapters: "28–31" }],
  ["Certification", { title: "Basins, layers, certification", chapters: "1–5, 35, 39, 44" }],
  ["Adversarial", { title: "Adversarial measurement", chapters: "32–37" }],
  ["Forgeability", { title: "Successor forgeability (MB10)", chapters: "8, 31, 43, 48" }],
  ["Field", { title: "Field-agenda crosswalk", chapters: "Appendix B crosswalk" }]
]);

function stripMarkdown(text) {
  return text.replace(/[`*]/g, "").replace(/\s+/g, " ").trim();
}

function titleFromDocstring(text, fallback) {
  // First paragraph after the `# AlignmentProofSpine.X` heading of the module
  // docstring, cut at the first sentence and capped at a word boundary.
  const doc = text.match(/\/-!\s*\n#\s*AlignmentProofSpine[^\n]*\n\s*\n([\s\S]*?)\n\s*\n/);
  if (!doc) return fallback;
  let title = stripMarkdown(doc[1].replace(/-\n\s*/g, "-"));
  const sentenceEnd = title.search(/[.:;](\s|$)/);
  if (sentenceEnd > 0) title = title.slice(0, sentenceEnd);
  if (title.length > 90) title = `${title.slice(0, 90).replace(/\s+\S*$/, "")}…`;
  // Drop a parenthetical the cut left unclosed.
  const open = title.lastIndexOf("(");
  if (open > 0 && title.indexOf(")", open) < 0) title = title.slice(0, open).trim();
  return title || fallback;
}

/**
 * Derive the module list from formal/AlignmentProofSpine.lean: the top-level
 * `import AlignmentProofSpine.X` lines (source order), followed by any module
 * rows of its docstring table that are not direct imports (e.g. `Field`,
 * `Field/Finite/*`). Chapters come from the table's book-chapters column,
 * titles from MODULE_OVERRIDES or the module's own docstring. Output shape is
 * unchanged: `{ file, title, chapters }`.
 */
async function loadModules() {
  const rootText = await readFile(SPINE_ROOT_FILE, "utf8");
  const ordered = [];
  const chaptersByModule = new Map();
  for (const line of rootText.split("\n")) {
    const imp = line.match(/^import AlignmentProofSpine\.([A-Za-z0-9_.]+)\s*$/);
    if (imp) {
      ordered.push(imp[1]);
      continue;
    }
    // `| \`Module\` | nodes | chapters |` rows of the docstring table.
    const row = line.match(/^\|\s*`([^`]+)`\s*\|(.*)\|\s*([^|]*?)\s*\|\s*$/);
    if (!row) continue;
    const key = row[1].replace(/\//g, ".");
    const chapters = stripMarkdown(row[3]).replace(/^\((.*)\)$/, "$1");
    if (chapters) chaptersByModule.set(key, chapters);
    if (!ordered.includes(key)) ordered.push(key);
  }

  const modules = [];
  for (const mod of ordered) {
    const file = `AlignmentProofSpine/${mod.replace(/\./g, "/")}.lean`;
    let text;
    try {
      text = await readFile(path.join(repoRoot, "formal", file), "utf8");
    } catch {
      console.warn(`[lean-spine] module ${mod} listed in AlignmentProofSpine.lean but ${file} not found`);
      continue;
    }
    const override = MODULE_OVERRIDES.get(mod);
    const title = override?.title ?? titleFromDocstring(text, mod);
    const chapters = override?.chapters ?? chaptersByModule.get(mod) ?? "";
    modules.push({ file, title, chapters });
  }
  return modules;
}

function nodeKind(id) {
  if (/^MB\d/.test(id)) return "bridge";
  if (id.startsWith("P") && /^\d/.test(id.slice(1))) return "proof";
  if (id.startsWith("S")) return "convention";
  return "other";
}

function nodeIdFromPlaygroundFilename(name) {
  const match = name.match(/^([A-Za-z]+\d+[A-Za-z]?)-/);
  return match ? match[1] : null;
}

function extractPlaygroundGloss(text) {
  const match = text.match(/^\/-!\s*\n([\s\S]*?)\n\s*-\/\//);
  return match ? match[1].replace(/\s+/g, " ").trim() : "";
}

async function loadCardNodeIndex() {
  const index = new Map();
  const entries = await readdir(CARDS_DIR, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
    const text = await readFile(path.join(CARDS_DIR, entry.name), "utf8");
    const slug = entry.name.replace(/\.md$/, "");
    const blocks = text.matchAll(/nodeId:\s*"([^"]+)"/g);
    for (const block of blocks) {
      if (!index.has(block[1])) index.set(block[1], slug);
    }
  }
  return index;
}

const PROJECTION_CARD_SLUG = {
  CIRL: "subsumption-cirl",
  SHUT: "subsumption-shutdown",
  INT: "subsumption-interruptibility",
  CORR: "subsumption-corrigibility",
  ELK: "subsumption-elk",
  DEB: "subsumption-debate",
  IMPACT: "subsumption-low-impact",
  QUANT: "subsumption-quantilization",
  EMBED: "subsumption-embedded-agency",
  BASIN: "subsumption-selection-basin",
  GROUND: "subsumption-grounding-drift",
  DEPLOY: "subsumption-deployment-gate",
  BIQ: "subsumption-hidden-biq"
};

function projectionCardSlug(nodeId) {
  return PROJECTION_CARD_SLUG[nodeId] ?? null;
}

function normalizeGraphNode(node, cardIndex) {
  const baseId = node.id.replace(/_IN$/, "");
  const cardSlug =
    cardIndex.get(baseId) ||
    cardIndex.get(node.id) ||
    projectionCardSlug(baseId) ||
    bridgeCardSlug(baseId);
  return {
    ...node,
    kind: nodeKind(baseId),
    cardSlug
  };
}

async function loadGraphs() {
  const graphs = {};
  for (const spec of GRAPH_ORDER) {
    const dotPath = path.join(GRAPH_DIR, `${spec.id}.dot`);
    const dot = await readFile(dotPath, "utf8");
    const parsed = parseDot(dot);
    graphs[spec.slug] = {
      id: spec.slug,
      dotId: spec.id,
      title: spec.title || parsed.title,
      nodes: parsed.nodes,
      edges: parsed.edges
    };
  }
  return graphs;
}

async function loadPlaygrounds() {
  const playgrounds = [];
  let entries;
  try {
    entries = await readdir(PLAYGROUND_DIR);
  } catch {
    return playgrounds;
  }

  for (const name of entries.filter((n) => n.endsWith(".lean"))) {
    const code = await readFile(path.join(PLAYGROUND_DIR, name), "utf8");
    const nodeId = nodeIdFromPlaygroundFilename(name);
    const file = `formal/playgrounds/${name}`;
    const live = buildLean4WebUrl(code, { playgroundFile: file });
    for (const warning of live.warnings) {
      console.warn(`[lean-spine] ${name}: ${warning}`);
    }
    if (!live.withinLimit) {
      throw new Error(
        `[lean-spine] ${name}: live URL length ${live.urlLength} exceeds ${DEFAULT_MAX_URL_LENGTH}`
      );
    }
    if (!live.withinConservativeLimit) {
      console.warn(
        `[lean-spine] ${name}: using ${live.encoding} encoding (${live.urlLength} chars); ` +
          `consider shortening snippet (conservative limit ${CONSERVATIVE_MAX_URL_LENGTH})`
      );
    }
    playgrounds.push({
      id: name.replace(/\.lean$/, ""),
      nodeId,
      file,
      title: extractPlaygroundGloss(code) || name,
      code,
      liveUrl: live.url,
      liveEncoding: live.encoding,
      codeLength: live.codeLength,
      liveUrlLength: live.urlLength
    });
  }
  return playgrounds.sort((a, b) => a.id.localeCompare(b.id));
}

async function loadLedgerNodes() {
  const ledger = JSON.parse(await readFile(LEDGER_PATH, "utf8"));
  return ledger.theorems.map((row) => ({
    theorem: row.name,
    shortName: row.name.replace(/^AlignmentProofSpine\./, ""),
    gloss: row.gloss,
    axioms: row.axioms
  }));
}

function buildNodeRegistry(graphs, ledger, playgrounds, cardIndex) {
  const nodes = new Map();

  for (const graph of Object.values(graphs)) {
    for (const node of graph.nodes) {
      if (!nodes.has(node.id)) {
        nodes.set(node.id, normalizeGraphNode(node, cardIndex));
      }
    }
  }

  for (const row of ledger) {
    const pMatch = row.shortName.match(/^(P\d+[A-Za-z]?)/);
    const mbMatch = row.shortName.match(/^(MB\d+[a-z]?)/);
    const id = pMatch?.[1] || mbMatch?.[1]?.toUpperCase() || null;
    if (!id) continue;
    const existing = nodes.get(id) || { id, label: id, kind: nodeKind(id) };
    nodes.set(id, {
      ...existing,
      theorem: row.theorem,
      gloss: row.gloss || existing.gloss,
      axioms: row.axioms,
      cardSlug: existing.cardSlug || cardIndex.get(id) || bridgeCardSlug(id)
    });
  }

  for (const pg of playgrounds) {
    if (!pg.nodeId) continue;
    const existing = nodes.get(pg.nodeId) || { id: pg.nodeId, label: pg.nodeId, kind: nodeKind(pg.nodeId) };
    nodes.set(pg.nodeId, {
      ...existing,
      playgroundId: pg.id,
      liveUrl: pg.liveUrl
    });
  }

  return Object.fromEntries([...nodes.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

async function renderGraphSvgs(graphs) {
  await mkdir(GRAPH_SVG_DIR, { recursive: true });
  for (const spec of GRAPH_ORDER) {
    const graph = graphs[spec.slug];
    if (!graph) continue;
    const dotPath = path.join(GRAPH_DIR, `${spec.id}.dot`);
    const dot = await readFile(dotPath, "utf8");
    const hrefMap = buildGraphHrefMap(graph.nodes);
    const svg = await renderDotToSvg(dot, hrefMap);
    await writeFile(path.join(GRAPH_SVG_DIR, `${spec.slug}.svg`), svg, "utf8");
    await writeFile(path.join(GRAPH_SVG_DIR, `${spec.slug}.dot`), dot, "utf8");
    graph.svgFile = `lean-graphs/${spec.slug}.svg`;
    graph.dotFile = `lean-graphs/${spec.slug}.dot`;
    graph.clickableNodes = Object.keys(hrefMap).length;
  }
}

async function main() {
  const [graphs, playgrounds, ledger, cardIndex, modules] = await Promise.all([
    loadGraphs(),
    loadPlaygrounds(),
    loadLedgerNodes(),
    loadCardNodeIndex(),
    loadModules()
  ]);

  for (const graph of Object.values(graphs)) {
    graph.nodes = graph.nodes.map((node) => normalizeGraphNode(node, cardIndex));
  }

  await renderGraphSvgs(graphs);

  const nodes = buildNodeRegistry(graphs, ledger, playgrounds, cardIndex);
  const declIndex = attachSpineSources(nodes, graphs, FORMAL_ROOT, NODE_ALIAS_PATH);

  const payload = {
    generatedAt: new Date().toISOString(),
    liveBase: "https://live.lean-lang.org/",
    declIndex,
    sections: [
      {
        id: "field",
        title: "Field agenda projections",
        summary: "External alignment agendas projected into this project's invariants on a shared finite domain.",
        graphSlugs: ["field-subsumptions"]
      },
      {
        id: "bridges",
        title: "Bridge assumptions",
        summary: "MB1–MB10 connect measured systems to project predicates. Bridges are never hidden inside definitions.",
        graphSlugs: []
      },
      {
        id: "spine",
        title: "Complete Lean proof spine",
        summary: "Proved nodes, counterexamples, and how the four sub-spines compose into certified-class safety.",
        graphSlugs: ["overview", "boundary-measurement", "value-transport", "correction-successors", "selection-limits"]
      }
    ],
    graphs,
    graphOrder: GRAPH_ORDER.map((g) => g.slug),
    modules,
    nodes,
    playgrounds,
    ledger
  };

  await mkdir(path.dirname(OUT_PATH), { recursive: true });
  await writeFile(OUT_PATH, JSON.stringify(payload, null, 2) + "\n", "utf8");
  console.log(
    `Wrote lean spine index (${Object.keys(graphs).length} graphs, ${playgrounds.length} playgrounds, ` +
      `${GRAPH_ORDER.length} Graphviz SVGs) to src/data/lean-spine.json`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
