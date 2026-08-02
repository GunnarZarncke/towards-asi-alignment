// Builds public/search-index.json: a documented, client-fetchable index over concept
// cards (glossary/gem/bridge/projection/objection/institutional/standalone/
// release), chapter + appendix cards, experiment cards, and notation symbols.
// Reference cards (site/src/content/cards/references/, ~380 bibliography
// entries) are intentionally excluded — see the content sync plumbing plan.
//
// Output is a versioned JSON object with metadata plus an `entries` array.
// SiteSearch and /search-index/ consume the same file.
// Usage: node scripts/build-search-index.mjs [--check]
import { readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const cardsDir = path.join(siteRoot, "src", "content", "cards");

// Mirrors src/lib/site-urls.ts (cardHref/bookHref); root-relative since the
// index is a static asset fetched at runtime, and the site has no base path.
function cardHref(cardId) {
  const routePath = cardId.split("/").map((part) => encodeURIComponent(part.toLowerCase())).join("/");
  return `/cards/${routePath}/`;
}

function bookHref(chapterId) {
  return cardHref(`chapters/${chapterId}`);
}

function parseFrontmatter(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  return match ? yaml.load(match[1]) || {} : {};
}

async function loadCards(dir) {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return [];
  }
  const cards = [];
  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
    const text = await readFile(path.join(dir, entry.name), "utf8");
    cards.push({ id: entry.name.replace(/\.md$/, ""), fm: parseFrontmatter(text) });
  }
  return cards;
}

async function buildEntries() {
  const entries = [];

  const rootCards = await loadCards(cardsDir);
  for (const { id, fm } of rootCards) {
    entries.push({
      title: fm.title,
      type: fm.type,
      summary: fm.summary ?? "",
      url: cardHref(id)
    });
  }

  const chapterCards = await loadCards(path.join(cardsDir, "chapters"));
  for (const { id, fm } of chapterCards) {
    entries.push({
      title: fm.title,
      type: fm.type,
      summary: fm.summary ?? "",
      url: cardHref(`chapters/${id}`)
    });
  }

  const experimentCards = await loadCards(path.join(cardsDir, "experiments"));
  for (const { id, fm } of experimentCards) {
    entries.push({
      title: fm.title,
      type: fm.type,
      summary: fm.summary ?? "",
      url: cardHref(`experiments/${id}`)
    });
  }

  const fieldAgendaCards = await loadCards(path.join(cardsDir, "field-agendas"));
  for (const { id, fm } of fieldAgendaCards) {
    entries.push({
      title: fm.title,
      type: fm.type,
      summary: fm.summary ?? "",
      url: cardHref(`field-agendas/${id}`)
    });
  }

  entries.push({
    title: "Field — AI safety and alignment",
    type: "field",
    summary: "Public map of major agendas, bridge coverage matrix, and field overviews (AISafety.com map, interventions index, surveys).",
    url: "/field/"
  });

  const notation = JSON.parse(await readFile(path.join(siteRoot, "src", "data", "notation.json"), "utf8"));
  for (const section of notation) {
    for (const entry of section.entries) {
      entries.push({
        title: entry.symbol,
        type: "notation",
        summary: entry.definition,
        url: entry.chapterId ? bookHref(entry.chapterId) : "/notation/"
      });
    }
  }

  entries.sort((a, b) => a.title.localeCompare(b.title));
  return entries;
}

async function main() {
  const check = process.argv.includes("--check");
  const entries = await buildEntries();
  const outPath = path.join(siteRoot, "public", "search-index.json");
  const payload = {
    version: 1,
    generatedAt: new Date().toISOString(),
    site: "https://towards-alignment.com",
    documentation: "https://towards-alignment.com/search-index/",
    description:
      "Flat index of concept cards, chapter and appendix cards, experiment cards, and notation symbols. Header search uses the same data with client-side substring matching.",
    entryCount: entries.length,
    entries
  };
  const json = JSON.stringify(payload, null, 2) + "\n";

  if (check) {
    let existing = "";
    try {
      existing = await readFile(outPath, "utf8");
    } catch {}
    if (existing !== json) {
      console.error(`build-search-index --check: ${outPath} out of date`);
      process.exit(1);
    }
    console.log(`build-search-index: check mode, ${entries.length} entries up to date.`);
    return;
  }

  await writeFile(outPath, json, "utf8");
  console.log(`build-search-index: wrote ${entries.length} entries to public/search-index.json.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
