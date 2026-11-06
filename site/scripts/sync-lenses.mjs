// Generates lens cards from site/scripts/lib/lenses-data.mjs.
import { mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { LENSES, OVERVIEW_ID } from "./lib/lenses-data.mjs";
import { repoBlobBase } from "./lib/repo-pin.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const cardsDir = path.join(siteRoot, "src/content/cards/lenses");

function overviewBasename() {
  const slug = OVERVIEW_ID.replace(/^lenses\//, "");
  if (!slug) throw new Error(`sync-lenses: invalid OVERVIEW_ID ${JSON.stringify(OVERVIEW_ID)}`);
  return `${slug}.md`;
}

function assertUniqueSlugs() {
  const seen = new Map();
  for (const row of LENSES) {
    if (seen.has(row.slug)) {
      throw new Error(`sync-lenses: duplicate slug ${JSON.stringify(row.slug)}`);
    }
    seen.set(row.slug, row.nodeId);
  }
}

function validateLensRow(row) {
  const id = row.slug ?? row.nodeId ?? "?";
  for (const key of ["slug", "title", "role", "summary", "nodeId"]) {
    if (typeof row[key] !== "string" || !row[key].trim()) {
      throw new Error(`sync-lenses: lens ${JSON.stringify(id)} missing ${key}`);
    }
  }
  if (typeof row.body !== "string") {
    throw new Error(`sync-lenses: lens ${JSON.stringify(id)} missing body`);
  }
  if (Boolean(row.quote) !== Boolean(row.quoteSource)) {
    throw new Error(`sync-lenses: lens ${JSON.stringify(id)} needs both quote and quoteSource`);
  }
  if (row.lwTag) {
    if (typeof row.lwTag.label !== "string" || typeof row.lwTag.url !== "string") {
      throw new Error(`sync-lenses: lens ${JSON.stringify(id)} lwTag needs label and url`);
    }
  }
  for (const [i, link] of (row.external ?? []).entries()) {
    if (typeof link?.label !== "string" || typeof link?.url !== "string") {
      throw new Error(`sync-lenses: lens ${JSON.stringify(id)} external[${i}] needs label and url`);
    }
  }
}

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
  const base = repoBlobBase();
  const summary =
    "An effort to map and compare different alignment proposals, making different mathematical approaches and terminology comparable. What happens if you try to identify the objects and objectives of the different proposals, group them and derive relations between approaches, and then render the result as a graph?";
  const body =
    "Different alignment proposals often seem hard to compare, but in the end try to achieve the same objective via different mathematical approaches and different terminology. But are these all comparable? Are some specializations of others? Or are some genuinely different? Many alignment approaches talk about states of the world and compare the value, utility, or reward of that state. Others try to prevent or prove impossible undesirable states. Others look at the system overall and establish properties or require empirical evidence. In this work, each alignment approach is mapped to an object and an assessment, then pairs of criteria are made comparable by finding a shared model where both can be determined and compared. Sometimes this leads to a one-to-one mapping between the two approaches. Sometimes, one approach is a specialization of the other. Sometimes, you can show that one criterion chooses differently from the other. Overall, there are four larger classes of alignment approaches: Scores, i.e., numeric utility or reward, relations and capacities, guarantees, and warrants, i.e., evidence. The map below shows the relations that were determined so far, using the toy worlds to make objectives pairwise comparable. Click to open the matching card or relation proof. Green combines two criteria through a named interface, in one correction-first reading. Red and orange are incompatibility inside a named situation class, with a boundary where both criteria can hold. Dotted red means one criterion cannot represent what the other needs, and enlarging it helps; dashed red means the two criteria choose differently from the same options; solid red means rigidity, where one criterion accepts only changes that do not matter to it. Orange is a shared resource that is zero-sum because the total is fixed.";
  return [
    "---",
    `title: "Lenses and frameworks"`,
    `type: "lens"`,
    `status: "framework"`,
    `summary: ${JSON.stringify(summary)}`,
    yamlList("related", [
      "field-coverage",
      "bridge-assumptions",
      "alignment-target",
      "correction-channel-integrity",
      "field-map-starting-points"
    ]),
    "external:",
    `  - label: "Frames relations note"`,
    `    url: ${JSON.stringify(`${base}/drafts/alignment-frames-relations.md`)}`,
    `  - label: "Lean FrameRelations"`,
    `    url: ${JSON.stringify(`${base}/formal/AlignmentProofSpine/FrameRelations.lean`)}`,
    "---",
    "",
    body,
    ""
  ].join("\n");
}

async function writeIfNeeded(filePath, contents, check) {
  let existing = null;
  try {
    existing = await readFile(filePath, "utf8");
  } catch (err) {
    if (err?.code !== "ENOENT") throw err;
  }
  if (existing === contents) return { matches: true, filePath };
  if (check) return { matches: false, filePath };
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, contents, "utf8");
  return { matches: true, filePath, wrote: true };
}

async function removeStaleLensCards(expectedNames, check) {
  let entries;
  try {
    entries = await readdir(cardsDir);
  } catch (err) {
    if (err?.code === "ENOENT") return [];
    throw err;
  }
  const stale = entries.filter((name) => name.endsWith(".md") && !expectedNames.has(name));
  if (!stale.length) return [];
  if (check) return stale.map((name) => path.join(cardsDir, name));
  for (const name of stale) {
    await rm(path.join(cardsDir, name));
  }
  return stale;
}

async function main() {
  const check = process.argv.includes("--check");
  assertUniqueSlugs();
  for (const row of LENSES) validateLensRow(row);

  const mismatches = [];
  let wrote = 0;
  const expectedNames = new Set([overviewBasename(), ...LENSES.map((row) => `${row.slug}.md`)]);

  const stalePaths = await removeStaleLensCards(expectedNames, check);
  mismatches.push(...stalePaths);

  const overviewPath = path.join(cardsDir, overviewBasename());
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

  const removed = stalePaths.length;
  const removedNote = removed ? `, ${removed} stale removed` : "";
  console.log(
    `sync-lenses: ${LENSES.length + 1} lens cards (${wrote} written${removedNote}). Overview id ${OVERVIEW_ID}.`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
