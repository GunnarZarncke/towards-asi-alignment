// Generates site cards for every metadata/concepts.yml roster entry (internal
// kinds: concept, glossary, standalone-claim, institutional, objection), plus
// src/data/part-gems.json and src/data/standalone-claims.json.
//
// Source of truth: metadata/concepts.yml (roster) + metadata/concepts/bodies/*.md
// (body text + attached-element frontmatter: formulas, leanNodes, evidenceNotes,
// demos, related, external, bookSections). This script never edits either.
//
// Usage: node scripts/sync-concepts.mjs [--check]
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { repoPaths, loadYaml, loadBody, renderCard, writeCard } from "./lib/concepts-yaml.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const { repoRoot, metadataDir, bodiesDir, cardsDir } = repoPaths(siteRoot);

const KIND_TO_TYPE = {
  concept: "concept",
  glossary: "glossary",
  "standalone-claim": "concept",
  institutional: "concept",
  objection: "objection"
};

function publicFieldsFor(row) {
  return {
    title: row.title ?? row.term,
    type: KIND_TO_TYPE[row.kind] ?? "concept",
    status: row.status,
    summary: row.summary,
    decision: row.decision,
    evidence: row.evidence,
    bookPageId: row.bookPageId,
    part: row.featured ? row.part : undefined,
    formalDensity: row.formalDensity,
    bookChapters: row.bookChapters,
    bookLabels: row.bookLabels,
    claimId: row.claimId
  };
}

// metadata/claims-ledger.md stays the audit ground truth (never generated);
// this only warns if a concept points at a claim ID the ledger doesn't have.
async function loadLedgerClaimIds(repoRoot) {
  const text = await readFile(path.join(repoRoot, "metadata", "claims-ledger.md"), "utf8");
  return new Set([...text.matchAll(/^## Claim ID: (C-\d+[a-z]?)$/gm)].map((m) => m[1]));
}

async function main() {
  const check = process.argv.includes("--check");
  const { concepts, legacyGems } = await loadYaml(path.join(metadataDir, "concepts.yml"));
  const ledgerClaimIds = await loadLedgerClaimIds(repoRoot);

  const mismatches = [];
  const partGems = {};
  const standaloneClaims = [];
  const glossary = [];
  const missingClaims = [];
  const bodyHeadingWarnings = [];

  for (const row of concepts) {
    if (row.claimId && !ledgerClaimIds.has(row.claimId)) missingClaims.push(`${row.slug} -> ${row.claimId}`);
    const { fm: bodyFm, body } = await loadBody(bodiesDir, row.body);
    const h1Line = body.split("\n").find((line) => /^#\s+[^#]/.test(line.trim()));
    if (h1Line) {
      bodyHeadingWarnings.push(
        `${row.slug}: remove leading h1 (${h1Line.trim()}) — card page already renders title as h1`
      );
    }
    const contents = renderCard(publicFieldsFor(row), bodyFm, body);
    const result = await writeCard(cardsDir, row.slug, contents, { check });
    if (!result.matches) mismatches.push(result.filePath);

    if (row.featured && row.part) {
      partGems[row.part] = partGems[row.part] || [];
      partGems[row.part].push(row.slug);
    }
    if (row.kind === "standalone-claim") {
      standaloneClaims.push({ slug: row.slug, title: row.title, blurb: row.summary });
    }
    if (row.kind === "glossary") {
      glossary.push({ term: row.term, definition: row.summary, slug: row.slug });
    }
    for (const entry of row.glossaryTerms ?? []) {
      glossary.push({ term: entry.term, definition: entry.definition, slug: row.slug });
    }
  }
  glossary.sort((a, b) => a.term.localeCompare(b.term));

  for (const gem of legacyGems ?? []) {
    partGems[gem.part] = partGems[gem.part] || [];
    partGems[gem.part].push(gem.slug);
  }
  for (const part of Object.keys(partGems)) partGems[part].sort();

  const dataDir = path.join(siteRoot, "src", "data");
  const partGemsPath = path.join(dataDir, "part-gems.json");
  const partGemsJson = JSON.stringify(partGems, null, 2) + "\n";
  if (check) {
    const { readFile } = await import("node:fs/promises");
    let existing = "";
    try {
      existing = await readFile(partGemsPath, "utf8");
    } catch {}
    if (existing !== partGemsJson) mismatches.push(partGemsPath);
  } else {
    await writeFile(partGemsPath, partGemsJson, "utf8");
  }

  const standaloneClaimsPath = path.join(dataDir, "standalone-claims.json");
  const standaloneClaimsJson =
    JSON.stringify(
      {
        title: "Standalone claims",
        summary: "Extractable notes from the manuscript — each is citable without the full book argument.",
        claims: standaloneClaims
      },
      null,
      2
    ) + "\n";
  if (check) {
    const { readFile } = await import("node:fs/promises");
    let existing = "";
    try {
      existing = await readFile(standaloneClaimsPath, "utf8");
    } catch {}
    if (existing !== standaloneClaimsJson) mismatches.push(standaloneClaimsPath);
  } else {
    await writeFile(standaloneClaimsPath, standaloneClaimsJson, "utf8");
  }

  const glossaryPath = path.join(dataDir, "glossary.json");
  const glossaryJson = JSON.stringify(glossary, null, 2) + "\n";
  if (check) {
    const { readFile } = await import("node:fs/promises");
    let existing = "";
    try {
      existing = await readFile(glossaryPath, "utf8");
    } catch {}
    if (existing !== glossaryJson) mismatches.push(glossaryPath);
  } else {
    await writeFile(glossaryPath, glossaryJson, "utf8");
  }

  if (missingClaims.length > 0) {
    console.warn(`sync-concepts: ${missingClaims.length} claimId(s) not found in metadata/claims-ledger.md:`);
    for (const entry of missingClaims) console.warn(`  ${entry}`);
  }

  if (bodyHeadingWarnings.length > 0) {
    console.warn(`sync-concepts: ${bodyHeadingWarnings.length} body h1 heading(s) to remove from metadata/concepts/bodies/:`);
    for (const entry of bodyHeadingWarnings) console.warn(`  ${entry}`);
  }

  if (check && mismatches.length > 0) {
    console.error(`sync-concepts --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-concepts: wrote ${concepts.length} cards (${check ? "check mode, all up to date" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
