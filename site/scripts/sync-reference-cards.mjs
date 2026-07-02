import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  buildBibIndex,
  buildBibAliasMap,
  buildManuscriptCitationIndex,
  buildReferencesBibliography,
  buildReferencesJson,
  canonicalizeCitationIndex
} from "./lib/bib-index.mjs";
import { expandInputs, stripComments } from "./lib/tex-convert.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const OUT_DIR = path.join(siteRoot, "src", "content", "cards", "references");
const DATA_DIR = path.join(siteRoot, "src", "data");
const INDEX_CARD = path.join(siteRoot, "src", "content", "cards", "reference-index.md");

function yamlString(value) {
  return JSON.stringify(value);
}

function readText(absPath) {
  return readFileSync(absPath, "utf8");
}

function externalLinks(entry) {
  const links = [];
  if (entry.doi) {
    links.push({ label: "DOI", url: `https://doi.org/${entry.doi.replace(/^https?:\/\/doi.org\//i, "")}` });
  }
  if (entry.url) {
    links.push({ label: "URL", url: entry.url });
  }
  return links;
}

function formatExternalLinksYaml(links) {
  if (links.length === 0) return "external: []";
  return [
    "external:",
    ...links.map(
      (link) =>
        `  - label: ${JSON.stringify(link.label)}\n    url: ${JSON.stringify(link.url)}`
    )
  ].join("\n");
}

function referenceCardMarkdown(entry) {
  const citedIn = entry.citedIn || [];
  const bookChapters = citedIn.filter((id) => /^ch\d+$/i.test(id));
  const fm = [
    "---",
    `title: ${yamlString(`${entry.shortLabel} — ${entry.title}`)}`,
    `type: "reference"`,
    `status: "reviewed"`,
    `summary: ${yamlString(entry.summary || entry.title)}`,
    `bibKey: ${yamlString(entry.key)}`,
    `citedIn: [${citedIn.map((id) => yamlString(id)).join(", ")}]`,
    `bookChapters: [${bookChapters.map((id) => yamlString(id)).join(", ")}]`,
    "related: []",
    formatExternalLinksYaml(externalLinks(entry)),
    "---",
    "",
    entry.summary || entry.title,
    ""
  ].join("\n");
  return fm;
}

async function main() {
  const book = JSON.parse(await readFile(path.join(DATA_DIR, "book.json"), "utf8"));
  const { units, keyToUnits } = buildManuscriptCitationIndex(repoRoot, {
    readText,
    stripComments,
    expandInputs,
    bookChapters: book.chapters
  });
  const rawBib = buildBibIndex(repoRoot);
  const aliasMap = buildBibAliasMap(rawBib);
  const citationIndex = canonicalizeCitationIndex({ units, keyToUnits }, aliasMap);

  const { entries: references } = buildReferencesJson(repoRoot, citationIndex);
  const bibliography = buildReferencesBibliography(units);

  const errors = [];
  for (const unit of units) {
    for (const key of unit.keys) {
      if (!references.some((entry) => entry.key === key)) {
        errors.push(`Unresolved citation key ${key} in ${unit.id}`);
      }
    }
  }

  if (errors.length > 0) {
    console.error("Reference sync failed:");
    for (const err of errors) console.error(`  - ${err}`);
    process.exit(1);
  }

  await mkdir(DATA_DIR, { recursive: true });
  await writeFile(
    path.join(DATA_DIR, "references.json"),
    JSON.stringify(references, null, 2) + "\n",
    "utf8"
  );
  await writeFile(
    path.join(DATA_DIR, "references-bibliography.json"),
    JSON.stringify(bibliography, null, 2) + "\n",
    "utf8"
  );

  await rm(OUT_DIR, { recursive: true, force: true });
  await mkdir(OUT_DIR, { recursive: true });

  for (const entry of references) {
    await writeFile(path.join(OUT_DIR, `${entry.key.toLowerCase()}.md`), referenceCardMarkdown(entry), "utf8");
  }

  const indexMd = [
    "---",
    `title: ${yamlString("Reference cards")}`,
    `type: "artifact"`,
    `status: "reviewed"`,
    `summary: ${yamlString(`Alphabetical index of ${references.length} bibliography entries as site cards — each links to citing chapters and appendices.`)}`,
    "related: []",
    "---",
    "",
    "Browse every manuscript bibliography entry as its own card. Use the alphabetical sections below, or open the chapter-grouped bibliography from the top menu.",
    ""
  ].join("\n");
  await writeFile(INDEX_CARD, indexMd, "utf8");

  console.log(`Wrote references.json (${references.length} entries)`);
  console.log(`Wrote references-bibliography.json (${bibliography.chapters.length} chapters, ${bibliography.other.length} other units)`);
  console.log(`Wrote ${references.length} reference cards to src/content/cards/references/`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
