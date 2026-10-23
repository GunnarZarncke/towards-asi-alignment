// Generates lens cards from site/scripts/lib/lenses-data.mjs.
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { LENSES, OVERVIEW_ID, lensCardId } from "./lib/lenses-data.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const cardsDir = path.join(siteRoot, "src/content/cards/lenses");

function yamlList(name, items) {
  if (!items?.length) return `${name}: []`;
  return `${name}:\n${items.map((item) => `  - ${JSON.stringify(item)}`).join("\n")}`;
}

function yamlExternal(row) {
  const links = [];
  if (row.lwTag) links.push({ label: row.lwTag.label, url: row.lwTag.url });
  for (const extra of row.external ?? []) links.push(extra);
  if (!links.length) return "external: []";
  const lines = ["external:"];
  for (const link of links) {
    lines.push(`  - label: ${JSON.stringify(link.label)}`);
    lines.push(`    url: ${JSON.stringify(link.url)}`);
  }
  return lines.join("\n");
}

function renderLensCard(row) {
  const related = [...new Set([...(row.related ?? []), ...(row.agendas ?? [])])];
  const quoteBlock = row.quote
    ? `> ${row.quote.replace(/\n/g, "\n> ")}\n>\n> — ${row.quoteSource}\n`
    : "";
  const body = `${quoteBlock}\n${row.body.trim()}\n`;
  return [
    "---",
    `title: ${JSON.stringify(row.title)}`,
    `type: "lens"`,
    `status: "framework"`,
    `summary: ${JSON.stringify(row.summary)}`,
    yamlList("related", related),
    yamlExternal(row),
    "---",
    "",
    `**Role.** ${row.role}. Graph node \`${row.nodeId}\`.`,
    "",
    body.trimEnd(),
    ""
  ].join("\n");
}

function renderOverview() {
  return [
    "---",
    `title: "Lenses and frameworks"`,
    `type: "lens"`,
    `status: "framework"`,
    `summary: "Alignment proposals are compared as if they supplied rival objective functions. Separate the object, the assessment or guarantee, and the warrant — then the red edges say when two frames cannot both accept the same situation."`,
    yamlList("related", [
      "field-coverage",
      "bridge-assumptions",
      "alignment-target",
      "correction-channel-integrity",
      "field-map-starting-points",
    ]),
    "external:",
    `  - label: "Frames relations note"`,
    `    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/drafts/alignment-frames-relations.md"`,
    `  - label: "Lean FrameRelations"`,
    `    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/FrameRelations.lean"`,
    "---",
    "",
    "Alignment work is often scored as if every proposal were a competing utility. That flattens targets, constraints, dynamical guarantees, and evidence protocols into one overloaded word. A state utility, an attainable-option penalty, a correction channel, a viability kernel, an AI-control monitor, and a safety case can all guide a deployment decision; they are not alternative scalars.",
    "",
    "The map below is one **correction-centered** reading of how those frames specialize, project, compose, or conflict. Nodes open the matching lens card. Edge labels open the Lean module that classifies or proves that edge (GitHub). Green is composition of different roles, not implication. Red is incompatibility inside a named situation class, with a boundary where both frames can hold.",
    ""
  ].join("\n");
}

async function writeIfNeeded(filePath, contents, check) {
  let existing = null;
  try {
    existing = await readFile(filePath, "utf8");
  } catch {
    existing = null;
  }
  if (existing === contents) return { matches: true, filePath };
  if (check) return { matches: false, filePath };
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, contents, "utf8");
  return { matches: true, filePath, wrote: true };
}

async function main() {
  const check = process.argv.includes("--check");
  const mismatches = [];
  let wrote = 0;

  const overviewPath = path.join(cardsDir, "lenses-and-frameworks.md");
  const overview = await writeIfNeeded(overviewPath, renderOverview(), check);
  if (!overview.matches) mismatches.push(overview.filePath);
  if (overview.wrote) wrote += 1;

  for (const row of LENSES) {
    const filePath = path.join(cardsDir, `${row.slug}.md`);
    const result = await writeIfNeeded(filePath, renderLensCard(row), check);
    if (!result.matches) mismatches.push(result.filePath);
    if (result.wrote) wrote += 1;
  }

  if (check) {
    if (mismatches.length) {
      console.error(`sync-lenses --check: ${mismatches.length} file(s) out of date`);
      for (const f of mismatches) console.error(`  ${f}`);
      process.exit(1);
    }
    console.log("sync-lenses: check mode, all up to date.");
    return;
  }

  console.log(`sync-lenses: ${LENSES.length + 1} lens cards (${wrote} written). Overview id ${OVERVIEW_ID}.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
