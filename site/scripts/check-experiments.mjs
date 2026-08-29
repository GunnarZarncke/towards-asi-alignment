import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const sourcePath = path.join(repoRoot, "metadata", "experiments.yml");

const source = await readFile(sourcePath, "utf8");
const data = yaml.load(source);
const witnessTestsPath = path.join(repoRoot, "metadata", "experiments-witness-tests.yml");
const witnessTests = yaml.load(await readFile(witnessTestsPath, "utf8"));
data.lines = [...data.lines, ...(witnessTests.lines ?? [])];
const errors = [];

const KINDS = new Set(["sim", "external", "witness"]);
const lineIds = new Set(data.lines.map((line) => line.id));
const columnIds = new Set(data.coverageColumns.map((col) => col.id));
const requiredColumnIds = new Set(
  data.coverageColumns.filter((col) => !col.optional).map((col) => col.id)
);

if (!data.purpose) {
  errors.push("missing purpose (overall experiments hub copy)");
}
if (!data.kinds || !KINDS.has("sim") || !data.kinds.sim) {
  errors.push("missing kinds.sim/external/witness");
}
for (const id of KINDS) {
  if (!data.kinds?.[id]?.title) {
    errors.push(`kinds.${id}: missing title`);
  }
  if (!data.kinds?.[id]?.cardId) {
    errors.push(`kinds.${id}: missing cardId`);
  }
  if (!data.kinds?.[id]?.overview) {
    errors.push(`kinds.${id}: missing overview`);
  }
}

for (const line of data.lines) {
  if (typeof line.order !== "number") {
    errors.push(`line ${line.id}: missing numeric order`);
  }
  const kind = line.kind ?? "sim";
  if (!KINDS.has(kind)) {
    errors.push(`line ${line.id}: kind ${kind} is not sim|external|witness`);
  }
  if (!line.repoUrl && !line.location && !line.readmePath && !line.planPath) {
    errors.push(`line ${line.id}: missing source (repoUrl, location, readmePath, or planPath)`);
  }
  if (!line.findingsPath && !line.findingsUrl && !(line.headlineFindings ?? []).length) {
    errors.push(`line ${line.id}: missing results (findingsPath, findingsUrl, or headlineFindings)`);
  }
  if (!line.summary) {
    errors.push(`line ${line.id}: missing public summary`);
  }
  if (kind === "witness") {
    for (const field of ["witnesses", "host", "setup", "analysis", "numbers", "outcome"]) {
      if (!line[field]?.trim()) {
        errors.push(`line ${line.id}: missing ${field}`);
      }
    }
  }
}

const kindCardIds = new Set(Object.values(data.kinds ?? {}).map((k) => k.cardId).filter(Boolean));

for (const entry of data.howToRead) {
  if (!lineIds.has(entry.lineId) && !kindCardIds.has(entry.lineId)) {
    errors.push(`howToRead references unknown lineId: ${entry.lineId}`);
  }
}

for (const ledger of data.ledgers) {
  if (!lineIds.has(ledger.lineId) && !columnIds.has(ledger.lineId)) {
    errors.push(`ledger references unknown lineId: ${ledger.lineId}`);
  }
}

for (const feature of data.coverageFeatures) {
  for (const [cellLineId] of Object.entries(feature.cells ?? {})) {
    if (!columnIds.has(cellLineId)) {
      errors.push(`coverage feature ${feature.id}: cell key ${cellLineId} is not a coverage column`);
    }
  }
  for (const col of requiredColumnIds) {
    if (!(col in (feature.cells ?? {}))) {
      errors.push(`coverage feature ${feature.id}: missing cell for column ${col}`);
    }
  }
}

if (errors.length > 0) {
  console.error("experiments.yml validation failed:");
  for (const error of errors) {
    console.error(`  - ${error}`);
  }
  process.exit(1);
}

console.log("metadata/experiments.yml OK");
