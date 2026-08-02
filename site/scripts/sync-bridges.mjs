// Generates the mb1..mb11 + bridge-assumptions site cards from metadata/bridges.yml.
// Cross-checks bridges.yml's fieldCrux/owningAgenda/bookMove against the appB
// longtable (appendices/appB-bridge-crosswalk.tex) as a validation source only —
// bridges.yml stays authoritative for what gets written to the site cards.
//
// Usage: node scripts/sync-bridges.mjs [--check]
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { repoPaths, loadYaml, loadBody, renderCard, writeCard } from "./lib/concepts-yaml.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const { repoRoot, metadataDir, bodiesDir, cardsDir } = repoPaths(siteRoot);

function publicFieldsFor(row) {
  return {
    title: row.title,
    type: "bridge",
    status: row.status ?? "bridge",
    summary: row.summary,
    decision: row.decision,
    evidence: row.evidence,
    bookChapters: row.bookChapters,
    bookLabels: row.bookLabels
  };
}

// Parse `\textbf{Bridge (home)}` / crux / agenda / move rows from the appB
// longtable. This is a best-effort validation parser: it looks for MBn markers
// in the first column and grabs the next three `&`-separated cells.
async function parseAppB() {
  const text = await readFile(path.join(repoRoot, "appendices", "appB-bridge-crosswalk.tex"), "utf8");
  const rows = new Map(); // MBn -> { fieldCrux, owningAgenda, bookMove }
  const lines = text.split("\n");
  let current = null;
  for (const line of lines) {
    const idMatches = [...line.matchAll(/MB(\d+[a-z]?)/g)].map((m) => `MB${m[1].replace(/[a-z]$/, "")}`);
    const cells = line
      .split("&")
      .map((c) => c.replace(/\\\\\s*$/, "").replace(/\\label\{[^}]*\}/g, "").replace(/\s+/g, " ").trim());
    if (idMatches.length > 0 && cells.length >= 4) {
      for (const id of new Set(idMatches)) {
        rows.set(id, { fieldCrux: cells[1], owningAgenda: cells[2], bookMove: cells[3] });
      }
      current = idMatches;
    }
  }
  return rows;
}

async function main() {
  const check = process.argv.includes("--check");
  const { bridges, index } = await loadYaml(path.join(metadataDir, "bridges.yml"));
  const appBRows = await parseAppB();

  const warnings = [];
  for (const row of bridges) {
    if (!appBRows.has(row.id)) {
      warnings.push(`${row.id}: not found in appB longtable (check appendices/appB-bridge-crosswalk.tex row markers)`);
    }
  }
  if (warnings.length > 0) {
    console.warn("sync-bridges: appB cross-check warnings (yaml.bridges stays authoritative):");
    for (const w of warnings) console.warn(`  ${w}`);
  }

  const mismatches = [];
  for (const row of [...bridges, index]) {
    const { fm: bodyFm, body } = await loadBody(bodiesDir, row.body);
    const contents = renderCard(publicFieldsFor(row), bodyFm, body);
    const result = await writeCard(cardsDir, row.slug, contents, { check });
    if (!result.matches) mismatches.push(result.filePath);
  }

  if (check && mismatches.length > 0) {
    console.error(`sync-bridges --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-bridges: wrote ${bridges.length + 1} cards (${check ? "check mode, all up to date" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
