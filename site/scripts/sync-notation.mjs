// Generates src/data/notation.json from metadata/notation.md (the "Appendix
// index" tables also consumed by scripts/generate_notation_appendix.py) for the
// site /notation/ page. No per-symbol cards — see the content sync plumbing plan.
// metadata/notation.md stays the single hand-maintained source (heavily
// cross-referenced by metadata/symbol-census/ and metadata/preamble.tex); this
// script only mirrors its tables into JSON, it never writes notation.md.
//
// Usage: node scripts/sync-notation.mjs [--check]
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { repoPaths } from "./lib/concepts-yaml.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const { metadataDir } = repoPaths(siteRoot);

const APPENDIX_MARKER = "## Appendix index";

function parseTableRow(line) {
  if (!line.startsWith("|")) return null;
  const cells = line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((c) => c.trim());
  if (cells.length === 0 || cells[0].toLowerCase() === "symbol") return null;
  if (cells.every((c) => /^[-:]+$/.test(c))) return null;
  return cells;
}

// Chapter id extracted from the "home" column (e.g. "⟳ ch34" -> "ch34"); the
// site page turns this into a href via bookHref(base, chapterId), matching the
// convention used for src/data/book.json elsewhere.
function chapterHome(home) {
  const clean = home.startsWith("⟳") ? home.slice(1).trim() : home;
  const match = clean.match(/^ch\d+b?/);
  return match ? match[0] : null;
}

function parseNotationMd(text) {
  if (!text.includes(APPENDIX_MARKER)) {
    throw new Error(`Missing "${APPENDIX_MARKER}" in metadata/notation.md`);
  }
  const appendix = text.split(APPENDIX_MARKER)[1];
  const sections = [];
  let currentTitle = null;
  let currentEntries = [];
  for (const line of appendix.split("\n")) {
    if (line.startsWith("### ")) {
      if (currentTitle && currentEntries.length > 0) sections.push({ title: currentTitle, entries: currentEntries });
      currentTitle = line.slice(4).trim();
      currentEntries = [];
      continue;
    }
    const cells = parseTableRow(line);
    if (!cells || currentTitle === null) continue;
    if (cells.length < 3) throw new Error(`Expected Symbol | Definition | Home, got: ${line}`);
    const [symbol, definition, home] = cells;
    currentEntries.push({ symbol, definition, home, chapterId: chapterHome(home) });
  }
  if (currentTitle && currentEntries.length > 0) sections.push({ title: currentTitle, entries: currentEntries });
  if (sections.length === 0) throw new Error("No notation tables found under Appendix index");
  return sections;
}

async function main() {
  const check = process.argv.includes("--check");
  const text = await readFile(path.join(metadataDir, "notation.md"), "utf8");
  const sections = parseNotationMd(text);

  const outPath = path.join(siteRoot, "src", "data", "notation.json");
  const json = JSON.stringify(sections, null, 2) + "\n";
  if (check) {
    let existing = "";
    try {
      existing = await readFile(outPath, "utf8");
    } catch {}
    if (existing !== json) {
      console.error(`sync-notation --check: ${outPath} out of date`);
      process.exit(1);
    }
    console.log("sync-notation: check mode, up to date.");
    return;
  }
  await writeFile(outPath, json, "utf8");
  const count = sections.reduce((n, s) => n + s.entries.length, 0);
  console.log(`sync-notation: wrote ${sections.length} sections, ${count} symbols.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
