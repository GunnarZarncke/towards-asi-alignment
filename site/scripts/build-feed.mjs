// Builds public/feed.xml — combined RSS 2.0 feed for release cards and field news.
// Run after sync:field-news and sync:releases (included in npm run sync).
//
// Usage: node scripts/build-feed.mjs [--check]
import { readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const cardsDir = path.join(siteRoot, "src", "content", "cards");
const fieldNewsPath = path.join(siteRoot, "src", "data", "field-news.json");
const outPath = path.join(siteRoot, "public", "feed.xml");

const SITE_ORIGIN = "https://towards-alignment.com";
const FEED_TITLE = "Towards Superintelligence Alignment — updates & field news";
const FEED_DESCRIPTION =
  "Manuscript releases and external AI safety incidents mapped to the companion site.";
const MAX_ITEMS = 50;

function cardHref(cardId) {
  const routePath = cardId.split("/").map((part) => encodeURIComponent(part.toLowerCase())).join("/");
  return `${SITE_ORIGIN}/cards/${routePath}/`;
}

function parseFrontmatter(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  return match ? yaml.load(match[1]) || {} : {};
}

function normalizeDate(value) {
  if (!value) return null;
  const iso = String(value).slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(iso) ? iso : null;
}

function pubDateRfc822(isoDate) {
  return new Date(`${isoDate}T12:00:00.000Z`).toUTCString();
}

function escapeXml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

async function loadReleaseItems() {
  let entries;
  try {
    entries = await readdir(cardsDir, { withFileTypes: true });
  } catch {
    return [];
  }

  const items = [];
  for (const entry of entries) {
    if (!entry.isFile() || !/^release-v/.test(entry.name)) continue;
    const text = await readFile(path.join(cardsDir, entry.name), "utf8");
    const fm = parseFrontmatter(text);
    const slug = entry.name.replace(/\.md$/, "");
    const date = normalizeDate(fm.releasedAt);
    if (!date || !fm.title) continue;
    items.push({
      kind: "release",
      date,
      slug,
      title: `[Release] ${fm.title}`,
      summary: fm.summary ?? "",
      url: cardHref(slug)
    });
  }
  return items;
}

async function loadNewsItems() {
  let raw;
  try {
    raw = await readFile(fieldNewsPath, "utf8");
  } catch {
    return [];
  }
  const rows = JSON.parse(raw);
  return rows
    .map((row) => {
      const date = normalizeDate(row.date);
      if (!date || !row.title) return null;
      return {
        kind: "news",
        date,
        slug: row.slug,
        title: `[News] ${row.title}`,
        summary: row.hook ?? row.summary ?? "",
        url: cardHref(row.slug)
      };
    })
    .filter(Boolean);
}

function renderFeed(items) {
  const sorted = [...items].sort((a, b) => {
    const byDate = b.date.localeCompare(a.date);
    if (byDate !== 0) return byDate;
    return a.kind.localeCompare(b.kind);
  });
  const capped = sorted.slice(0, MAX_ITEMS);
  const lastBuildDate = capped[0] ? pubDateRfc822(capped[0].date) : pubDateRfc822(new Date().toISOString().slice(0, 10));

  const itemXml = capped
    .map(
      (item) => `    <item>
      <title>${escapeXml(item.title)}</title>
      <link>${escapeXml(item.url)}</link>
      <guid isPermaLink="true">${escapeXml(item.url)}</guid>
      <pubDate>${pubDateRfc822(item.date)}</pubDate>
      <description>${escapeXml(item.summary)}</description>
      <category>${escapeXml(item.kind)}</category>
    </item>`
    )
    .join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>${escapeXml(FEED_TITLE)}</title>
    <link>${SITE_ORIGIN}/</link>
    <description>${escapeXml(FEED_DESCRIPTION)}</description>
    <language>en</language>
    <lastBuildDate>${lastBuildDate}</lastBuildDate>
    <generator>towards-asi-alignment-site/build-feed.mjs</generator>
${itemXml}
  </channel>
</rss>
`;
}

async function main() {
  const check = process.argv.includes("--check");
  const items = [...(await loadReleaseItems()), ...(await loadNewsItems())];
  const xml = renderFeed(items);

  if (check) {
    let existing = "";
    try {
      existing = await readFile(outPath, "utf8");
    } catch {}
    if (existing !== xml) {
      console.error("build-feed --check: public/feed.xml out of date");
      process.exit(1);
    }
    console.log(`build-feed: check mode, ${items.length} source items up to date.`);
    return;
  }

  await writeFile(outPath, xml, "utf8");
  console.log(`build-feed: wrote ${Math.min(items.length, MAX_ITEMS)} items to public/feed.xml (${items.length} source items).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
