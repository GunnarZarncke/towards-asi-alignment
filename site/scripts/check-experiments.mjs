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
const errors = [];

const lineIds = new Set(data.lines.map((line) => line.id));
const columnIds = new Set(data.coverageColumns.map((col) => col.id));

for (const line of data.lines) {
  if (typeof line.order !== "number") {
    errors.push(`line ${line.id}: missing numeric order`);
  }
}

for (const entry of data.howToRead) {
  if (!lineIds.has(entry.lineId)) {
    errors.push(`howToRead references unknown lineId: ${entry.lineId}`);
  }
}

for (const ledger of data.ledgers) {
  if (!lineIds.has(ledger.lineId)) {
    errors.push(`ledger references unknown lineId: ${ledger.lineId}`);
  }
}

for (const feature of data.coverageFeatures) {
  for (const [cellLineId] of Object.entries(feature.cells ?? {})) {
    if (!columnIds.has(cellLineId)) {
      errors.push(`coverage feature ${feature.id}: cell key ${cellLineId} is not a coverage column`);
    }
  }
  for (const col of data.coverageColumns) {
    if (!(col.id in (feature.cells ?? {}))) {
      errors.push(`coverage feature ${feature.id}: missing cell for column ${col.id}`);
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
