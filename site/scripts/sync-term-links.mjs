// Builds reverse index from reference/field-agendas/data/term-links.yml
// → site/src/data/term-links-reverse.json
//
// Usage: node scripts/sync-term-links.mjs [--check]
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const TERM_LINKS_PATH = path.join(repoRoot, "reference", "field-agendas", "data", "term-links.yml");
const OUT_PATH = path.join(siteRoot, "src", "data", "term-links-reverse.json");

function normalizeUrl(url) {
  if (url.startsWith("http")) return url;
  const pathPart = url.startsWith("/") ? url : `/${url}`;
  return pathPart.endsWith("/") ? pathPart : `${pathPart}/`;
}

async function main() {
  const check = process.argv.includes("--check");
  const { terms = [] } = yaml.load(await readFile(TERM_LINKS_PATH, "utf8")) || {};
  const reverse = {};

  for (const entry of terms) {
    const url = normalizeUrl(entry.url);
    if (!reverse[url]) {
      reverse[url] = { phrases: [], agendas: [], fields: new Set() };
    }
    reverse[url].phrases.push(entry.phrase);
    if (entry.agendas) {
      for (const agenda of entry.agendas) reverse[url].agendas.push(agenda);
    }
    if (entry.fields) reverse[url].fields.add(entry.fields);
  }

  const payload = Object.fromEntries(
    Object.entries(reverse)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([url, data]) => [
        url,
        {
          phrases: [...new Set(data.phrases)].sort((a, b) => b.length - a.length),
          agendas: [...new Set(data.agendas)].sort(),
          fields: [...data.fields].sort()
        }
      ])
  );

  const json = JSON.stringify(payload, null, 2) + "\n";
  if (check) {
    let existing = "";
    try {
      existing = await readFile(OUT_PATH, "utf8");
    } catch {}
    if (existing !== json) {
      console.error(`sync-term-links --check: ${OUT_PATH} out of date`);
      process.exit(1);
    }
    console.log(`sync-term-links: check mode, ${Object.keys(payload).length} destinations up to date.`);
    return;
  }

  await writeFile(OUT_PATH, json, "utf8");
  console.log(`sync-term-links: wrote ${Object.keys(payload).length} reverse entries.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
