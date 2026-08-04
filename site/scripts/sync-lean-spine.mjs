import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseDot } from "./lib/dot-parse.mjs";
import { buildGraphHrefMap } from "./lib/graph-node-hrefs.mjs";
import { attachSpineSources } from "./lib/spine-source-index.mjs";
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

const MODULES = [
  { file: "AlignmentProofSpine/Core.lean", title: "Core carriers and bridges", chapters: "foundations" },
  { file: "AlignmentProofSpine/Boundaries.lean", title: "Boundaries and measurement", chapters: "6–7, 10, 36" },
  { file: "AlignmentProofSpine/Capability.lean", title: "Capability and BIQ", chapters: "11–14, 33, 36" },
  { file: "AlignmentProofSpine/Bundles.lean", title: "Value bundles and transport", chapters: "15–23, 30" },
  { file: "AlignmentProofSpine/Correction.lean", title: "Correction channels", chapters: "25–29, 41–43" },
  { file: "AlignmentProofSpine/Successors.lean", title: "Successors and continuity", chapters: "28–31" },
  { file: "AlignmentProofSpine/Certification.lean", title: "Basins, layers, certification", chapters: "1–5, 35, 39, 44" },
  { file: "AlignmentProofSpine/Adversarial.lean", title: "Adversarial measurement", chapters: "32–37" },
  { file: "AlignmentProofSpine/Forgeability.lean", title: "Successor forgeability (MB10)", chapters: "8, 31, 43, 48" },
  { file: "AlignmentProofSpine/Field.lean", title: "Field-agenda crosswalk", chapters: "Appendix B crosswalk" }
];

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

function bridgeCardSlug(nodeId) {
  if (nodeId.startsWith("MB4a")) return "mb4a-measured-path-legitimacy";
  if (nodeId.startsWith("MB7d")) return "mb7d-acausal-coordination";
  const mb = nodeId.match(/^MB(\d+)/);
  if (!mb) return null;
  const names = {
    1: "mb1-boundary-estimator-soundness",
    2: "mb2-bundle-identifiability",
    3: "mb3-bearer-import",
    4: "mb4-correction-legitimacy",
    5: "mb5-successor-ontology-shift",
    6: "mb6-selection-and-basin-stability",
    7: "mb7-hidden-capability-and-access",
    8: "mb8-cev-process-convergence",
    9: "mb9-grounding-certificate",
    10: "mb10-successor-forgeability",
    11: "mb11-deployment-safety"
  };
  const key = nodeId.startsWith("MB6") ? 6 : nodeId.startsWith("MB7") ? 7 : Number(mb[1]);
  return names[key] || null;
}

function normalizeGraphNode(node, cardIndex) {
  const baseId = node.id.replace(/_IN$/, "");
  const cardSlug = cardIndex.get(baseId) || cardIndex.get(node.id) || bridgeCardSlug(baseId);
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
  const [graphs, playgrounds, ledger, cardIndex] = await Promise.all([
    loadGraphs(),
    loadPlaygrounds(),
    loadLedgerNodes(),
    loadCardNodeIndex()
  ]);

  for (const graph of Object.values(graphs)) {
    graph.nodes = graph.nodes.map((node) => normalizeGraphNode(node, cardIndex));
  }

  await renderGraphSvgs(graphs);

  const nodes = buildNodeRegistry(graphs, ledger, playgrounds, cardIndex);
  attachSpineSources(nodes, graphs, FORMAL_ROOT, NODE_ALIAS_PATH);

  const payload = {
    generatedAt: new Date().toISOString(),
    liveBase: "https://live.lean-lang.org/",
    sections: [
      {
        id: "field",
        title: "Field agenda projections",
        summary: "External alignment agendas projected into the book's invariants on a shared finite domain.",
        graphSlugs: ["field-subsumptions"]
      },
      {
        id: "bridges",
        title: "Bridge assumptions",
        summary: "MB1–MB10 connect measured systems to book predicates. Bridges are never hidden inside definitions.",
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
    modules: MODULES,
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
