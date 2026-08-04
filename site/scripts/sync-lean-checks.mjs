// Generates lean-check pages data from metadata/lean-checks/index.yml
// → site/src/data/lean-checks.json
//
// Usage: node scripts/sync-lean-checks.mjs [--check]
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { repoPaths, loadYaml, loadBody, normalizeMarkdownMath } from "./lib/concepts-yaml.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const { repoRoot, metadataDir } = repoPaths(siteRoot);
const CHECKS_DIR = path.join(repoRoot, "metadata", "lean-checks");
const CHECKS_BODIES = path.join(CHECKS_DIR, "bodies");

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
  const { checks } = await loadYaml(path.join(CHECKS_DIR, "index.yml"));
  const enriched = [];

  for (const row of checks) {
    let bodyHtml = "";
    if (row.body) {
      const { body } = await loadBody(CHECKS_BODIES, row.body);
      bodyHtml = normalizeMarkdownMath(body);
    }
    enriched.push({
      slug: row.slug,
      question: row.question,
      summary: row.summary ?? "",
      fieldTerms: row.fieldTerms ?? [],
      steppingStones: row.steppingStones ?? [],
      leanForward: row.leanForward ?? [],
      leanSeparations: row.leanSeparations ?? [],
      leanNotChecked: row.leanNotChecked ?? [],
      bridges: row.bridges ?? [],
      body: bodyHtml
    });
  }

  const outPath = path.join(siteRoot, "src", "data", "lean-checks.json");
  const mismatches = [];
  await writeJson(outPath, { checks: enriched }, check, mismatches);

  if (check && mismatches.length > 0) {
    console.error(`sync-lean-checks --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-lean-checks: wrote ${checks.length} check(s) (${check ? "check mode, all up to date" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
