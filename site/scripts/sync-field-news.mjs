// Generates field-news-* site cards from metadata/field-news.yml and
// src/data/field-news.json (chapter → related news lookup).
//
// Usage: node scripts/sync-field-news.mjs [--check]
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadYaml, loadBody, renderCard, writeCard } from "./lib/concepts-yaml.mjs";
import {
  buildChapterRefs,
  formatReadMoreMarkdown,
  loadChapterTitles,
  stripReadMoreFooter
} from "./lib/chapter-links.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const metadataDir = path.join(repoRoot, "metadata");
const bodiesDir = path.join(metadataDir, "field-news", "bodies");
const cardsDir = path.join(siteRoot, "src", "content", "cards");

function publicFieldsFor(row) {
  const fields = {
    title: row.title,
    type: "news",
    status: row.status ?? "established",
    summary: row.summary,
    decision: row.decision,
    bookChapters: row.bookChapters,
    releasedAt: row.date
  };
  if (row.eventDate && row.eventDate !== row.date) {
    fields.eventDate = row.eventDate;
  }
  return fields;
}

function yamlDateString(value) {
  if (value instanceof Date) {
    return value.toISOString().slice(0, 10);
  }
  return String(value);
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
  const { fieldNews } = await loadYaml(path.join(metadataDir, "field-news.yml"));
  const ordered = [...fieldNews].sort((a, b) => (a.order ?? 99) - (b.order ?? 99));

  const chapterTitles = await loadChapterTitles(siteRoot);
  const mismatches = [];
  for (const row of fieldNews) {
    const { fm: bodyFm, body: rawBody } = await loadBody(bodiesDir, row.body);
    const stripped = stripReadMoreFooter(rawBody);
    const readMore = formatReadMoreMarkdown(row.bookChapters, chapterTitles);
    const body = readMore ? `${stripped}\n\n${readMore}` : stripped;
    const hookLine = row.hook ? `${row.hook}\n\n` : "";
    const contents = renderCard(publicFieldsFor(row), bodyFm, hookLine + body);
    const result = await writeCard(cardsDir, row.slug, contents, { check });
    if (!result.matches) mismatches.push(result.filePath);
  }

  const dataDir = path.join(siteRoot, "src", "data");
  await writeJson(
    path.join(dataDir, "field-news.json"),
    ordered.map((row) => ({
      slug: row.slug,
      card: row.slug,
      date: yamlDateString(row.date),
      eventDate: yamlDateString(row.eventDate ?? row.date),
      kind: row.kind,
      title: row.title,
      hook: row.hook,
      chapters: row.bookChapters,
      chapterRefs: buildChapterRefs(row.bookChapters, chapterTitles),
      bridges: row.bridges ?? []
    })),
    check,
    mismatches
  );

  if (check && mismatches.length > 0) {
    console.error(`sync-field-news --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-field-news: wrote ${fieldNews.length} cards (${check ? "check mode, all up to date" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
