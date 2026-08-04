// Generates the subsumption-* ("Field projection —") site cards from
// metadata/projections.yml, plus src/data/field-projections.json and
// field-projection-gems.json (replacing the old field-subsumptions*.json).
// Slugs stay stable (subsumption-*) because they are posted externally; only
// the display title changes.
//
// Usage: node scripts/sync-projections.mjs [--check]
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { repoPaths, loadYaml, loadBody, renderCard, writeCard } from "./lib/concepts-yaml.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const { repoRoot, metadataDir, bodiesDir, cardsDir } = repoPaths(siteRoot);

function publicFieldsFor(row) {
  return {
    title: row.title,
    type: "concept",
    status: row.status ?? "established",
    summary: row.summary,
    decision: row.decision,
    bookChapters: row.bookChapters,
    bookLabels: row.bookLabels,
    graphNodeId: row.graphNodeId
  };
}

async function writeJson(filePath, data, check, mismatches) {
  const json = JSON.stringify(data, null, 2) + "\n";
  if (check) {
    let existing = "";
    try {
      existing = await readFile(filePath, "utf8");
    } catch {}
    if (existing !== json) mismatches.push(filePath);
  } else {
    await writeFile(filePath, json, "utf8");
  }
}

async function main() {
  const check = process.argv.includes("--check");
  const { projections } = await loadYaml(path.join(metadataDir, "projections.yml"));
  const ordered = [...projections].sort((a, b) => (a.order ?? 99) - (b.order ?? 99));

  const mismatches = [];
  for (const row of projections) {
    const { fm: bodyFm, body } = await loadBody(bodiesDir, row.body);
    const contents = renderCard(publicFieldsFor(row), bodyFm, body);
    const result = await writeCard(cardsDir, row.slug, contents, { check });
    if (!result.matches) mismatches.push(result.filePath);
  }

  const dataDir = path.join(siteRoot, "src", "data");
  await writeJson(
    path.join(dataDir, "field-projections.json"),
    ordered.map((row) => ({
      id: row.id,
      card: row.slug,
      agenda: row.agenda,
      headline: row.headline,
      chapters: row.bookChapters,
      leanStatus: row.leanStatus ?? null
    })),
    check,
    mismatches
  );
  await writeJson(
    path.join(dataDir, "field-projection-gems.json"),
    ordered.map((row) => row.slug),
    check,
    mismatches
  );

  if (check && mismatches.length > 0) {
    console.error(`sync-projections --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-projections: wrote ${projections.length} cards (${check ? "check mode, all up to date" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
