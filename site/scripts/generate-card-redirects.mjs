#!/usr/bin/env node
/** Generate site/src/data/card-redirects.json for astro.config.mjs */
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import { buildCardRedirects } from "./lib/card-urls.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const cardsDir = path.join(siteRoot, "src", "content", "cards");
const outPath = path.join(siteRoot, "src", "data", "card-redirects.json");

function parseFrontmatter(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  return match ? yaml.load(match[1]) || {} : {};
}

async function loadCardsInDir(dir, prefix = "") {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return [];
  }
  const cards = [];
  for (const entry of entries) {
    const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) {
      cards.push(...(await loadCardsInDir(path.join(dir, entry.name), rel.replace(/\/$/, ""))));
      continue;
    }
    if (!entry.name.endsWith(".md")) continue;
    const id = prefix ? `${prefix}/${entry.name.replace(/\.md$/, "")}` : entry.name.replace(/\.md$/, "");
    const text = await readFile(path.join(dir, entry.name), "utf8");
    const fm = parseFrontmatter(text);
    cards.push({ id, data: fm, type: fm.type, overviewOnly: fm.overviewOnly });
  }
  return cards;
}

async function main() {
  const cards = await loadCardsInDir(cardsDir);
  const redirects = buildCardRedirects(cards);
  await mkdir(path.dirname(outPath), { recursive: true });
  await writeFile(outPath, `${JSON.stringify(redirects, null, 2)}\n`, "utf8");
  console.log(`Wrote ${Object.keys(redirects).length} card redirects → ${outPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
