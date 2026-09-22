import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const sourcePath = path.join(repoRoot, "metadata", "assurance-model.yml");
const evidencePath = path.join(repoRoot, "formal", "AlignmentProofSpine", "Evidence.lean");
const outputPath = path.join(siteRoot, "src", "data", "assurance-model.json");

function leanIdentifiers(text) {
  const ids = new Set();
  for (const match of text.matchAll(/\b([A-Z][A-Za-z0-9_]*)\b/g)) {
    ids.add(match[1]);
  }
  return ids;
}

const raw = yaml.load(await readFile(sourcePath, "utf8"));
const evidenceText = await readFile(evidencePath, "utf8");
const leanIds = leanIdentifiers(evidenceText);

const drift = [];
for (const node of raw.nodes ?? []) {
  for (const key of ["leanCert", "leanPredicate"]) {
    const id = node[key];
    if (id && !leanIds.has(id)) {
      drift.push(`${node.id}: unknown Lean identifier ${id} (${key})`);
    }
  }
}

if (drift.length) {
  for (const line of drift) console.warn(`sync-assurance-model: ${line}`);
} else {
  console.log("sync-assurance-model: Lean identifier check passed");
}

const payload = {
  version: raw.version,
  unitOfAnalysis: raw.unitOfAnalysis?.trim() ?? "",
  events: raw.events ?? {},
  parameters: raw.parameters ?? {},
  relationTypes: raw.relationTypes ?? {},
  nodes: raw.nodes ?? [],
  relations: raw.relations ?? [],
  dependenceWarnings: raw.dependenceWarnings ?? [],
  phase3Markets: raw.phase3Markets ?? [],
  presets: raw.presets ?? { sR: [], kappaRanges: [] }
};

await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
console.log(`sync-assurance-model: wrote assurance-model.json (${payload.nodes.length} nodes)`);
