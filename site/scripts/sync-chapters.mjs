import { mkdir, readdir, readFile, writeFile, rm } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  collectLabels,
  convertLatexDocument,
  expandInputs,
  extractChapterMeta,
  loadIllustrationAlts,
  stripComments
} from "./lib/tex-convert.mjs";
import { buildReferencesJson, collectCiteKeys, collectLabelRefs, buildBibIndex, buildBibAliasMap, canonicalCiteKey } from "./lib/bib-index.mjs";
import { buildCardIndex, validateCardLabels } from "./lib/card-index.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const FRONTMATTER_FILES = [
  "frontmatter/titlepage.tex",
  "frontmatter/dedication.tex",
  "frontmatter/acknowledgements.tex",
  "frontmatter/preface.tex",
  "frontmatter/introduction.tex",
  "frontmatter/current-status.tex",
  "frontmatter/executive-overview.tex"
];

const APPENDIX_FILES = [
  { id: "appB", file: "appendices/appB-bridge-crosswalk.tex", order: 100 },
  { id: "appC", file: "appendices/appC-institutional-translation.tex", order: 101 },
  { id: "appM", file: "appendices/appM-institutional-histories.tex", order: 102 },
  { id: "appD", file: "appendices/appD-worked-example.tex", order: 103 },
  { id: "appF", file: "appendices/appF-research-program.tex", order: 104 },
  { id: "appN", file: "appendices/appN-experimental-evidence.tex", order: 105 }
];

const PART_RANGES = [
  ["part01", 1, 5],
  ["part02", 6, 10],
  ["part03", 11, 14],
  ["part04", 15, 20],
  ["part05", 21, 24],
  ["part06", 25, 29],
  ["part07", 30, 33],
  ["part08", 34, 38],
  ["part09", 39, 44],
  ["part10", 45, 48]
];

function partForChapter(number) {
  const found = PART_RANGES.find(([, start, end]) => number >= start && number <= end);
  return found ? found[0] : undefined;
}

function chapterNumberFromFile(file) {
  const match = file.match(/^ch(\d+)-/);
  return match ? Number(match[1]) : 0;
}

function chapterIdFromFile(file) {
  return file.match(/^(ch\d+)-/)?.[1] || file.replace(/\.tex$/, "");
}

async function readTex(relPath) {
  return readFile(path.join(repoRoot, relPath), "utf8");
}

function buildLabelIndex(sources, webPageIds, repoRoot) {
  const labelIndex = new Map();
  for (const source of sources) {
    const tex = expandInputs(stripComments(source.tex), repoRoot);
    collectLabels(tex, source.id, source.title, webPageIds.has(source.id), labelIndex);
  }
  return labelIndex;
}

function yamlEscape(value) {
  return JSON.stringify(value);
}

function frontmatterBlock(data) {
  return [
    "---",
    `id: ${data.id}`,
    `title: ${yamlEscape(data.title)}`,
    `kind: ${data.kind}`,
    data.part ? `part: ${data.part}` : null,
    `order: ${data.order}`,
    `sourceFile: ${yamlEscape(data.sourceFile)}`,
    "---",
    "",
    ""
  ].filter((line) => line !== null).join("\n");
}

async function main() {
  const errors = [];
  const chapterFiles = (await readdir(path.join(repoRoot, "chapters")))
    .filter((f) => f.startsWith("ch") && f.endsWith(".tex"))
    .sort();

  const webSources = [];
  const indexSources = [];

  for (const file of chapterFiles) {
    const tex = await readTex(path.join("chapters", file));
    const id = chapterIdFromFile(file);
    const number = chapterNumberFromFile(file);
    const meta = extractChapterMeta(tex);
    const source = {
      id,
      title: meta.title,
      kind: "chapter",
      part: partForChapter(number),
      order: number,
      sourceFile: `chapters/${file}`,
      tex
    };
    webSources.push(source);
    indexSources.push(source);
  }

  const frontmatterTex = [];
  for (const rel of FRONTMATTER_FILES) {
    frontmatterTex.push(await readTex(rel));
  }
  webSources.push({
    id: "frontmatter",
    title: "Front Matter",
    kind: "frontmatter",
    order: 0,
    sourceFile: FRONTMATTER_FILES.join(", "),
    tex: frontmatterTex.join("\n\n")
  });
  indexSources.push({
    id: "frontmatter",
    title: "Front Matter",
    tex: frontmatterTex.join("\n\n")
  });

  for (const appendix of APPENDIX_FILES) {
    const tex = await readTex(appendix.file);
    const meta = extractChapterMeta(tex);
    const source = {
      id: appendix.id,
      title: meta.title,
      kind: "appendix",
      order: appendix.order,
      sourceFile: appendix.file,
      tex
    };
    webSources.push(source);
    indexSources.push(source);
  }

  const labelScanPaths = [
    ...chapterFiles.map((f) => path.join("chapters", f)),
    ...APPENDIX_FILES.map((a) => a.file),
    ...FRONTMATTER_FILES,
    "appendices/appA-notation.tex",
    "appendices/appE-glossary.tex",
    "appendices/appG-lean-proof-spine.tex",
    "appendices/appH-boundary-worked-example.tex",
    "appendices/appI-value-bundle-inference.tex",
    "appendices/appJ-correction-channel-audit.tex",
    "appendices/appK-safety-case-template.tex",
    "appendices/appN-experimental-evidence.tex"
  ];

  for (const rel of labelScanPaths) {
    if (indexSources.some((s) => s.sourceFile === rel || s.sourceFile?.includes(rel))) continue;
    try {
      const tex = await readTex(rel);
      const meta = extractChapterMeta(tex);
      indexSources.push({
        id: path.basename(rel, ".tex"),
        title: meta.title,
        tex,
        webPage: false
      });
    } catch {
      // optional appendix files may not exist in all snapshots
    }
  }

  const webPageIds = new Set(webSources.map((s) => s.id));
  const labelIndex = buildLabelIndex(indexSources, webPageIds, repoRoot);
  const bibIndex = new Map(buildReferencesJson(repoRoot).entries.map((entry) => [entry.key, entry]));
  const aliasMap = buildBibAliasMap(buildBibIndex(repoRoot));
  const cardIndex = buildCardIndex(path.join(siteRoot, "src", "content", "cards"));
  const illustrationAlts = loadIllustrationAlts(repoRoot);

  const outDir = path.join(siteRoot, "src", "content", "book");
  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });

  for (const source of webSources) {
    const ctx = {
      repoRoot,
      pageId: source.id,
      labelIndex,
      bibIndex,
      cardIndex,
      illustrationAlts,
      errors,
      footnoteCount: 0
    };
    const body = convertLatexDocument(source.tex, ctx);
    const md = `${frontmatterBlock(source)}${body}\n`;
    await writeFile(path.join(outDir, `${source.id}.md`), md, "utf8");
  }

  await mkdir(path.join(siteRoot, "src", "data"), { recursive: true });

  const allTex = [];
  for (const source of webSources) {
    allTex.push(expandInputs(stripComments(source.tex), repoRoot));
  }
  for (const rel of labelScanPaths) {
    try {
      allTex.push(expandInputs(stripComments(await readTex(rel)), repoRoot));
    } catch {
      // ignore
    }
  }

  const citeKeys = new Set();
  const labelRefs = new Set();
  for (const tex of allTex) {
    collectCiteKeys(tex, citeKeys);
    collectLabelRefs(tex, labelRefs);
  }

  for (const key of citeKeys) {
    const canonical = canonicalCiteKey(key, aliasMap);
    if (!bibIndex.has(canonical)) errors.push(`Unresolved citation key: ${key}`);
  }
  for (const label of labelRefs) {
    if (!labelIndex.has(label)) errors.push(`Unresolved label reference: ${label}`);
  }
  errors.push(...validateCardLabels(path.join(siteRoot, "src", "content", "cards"), labelIndex));

  if (errors.length > 0) {
    console.error("Chapter sync failed:");
    for (const err of errors) console.error(`  - ${err}`);
    process.exit(1);
  }

  console.log(`Wrote ${webSources.length} book pages to src/content/book/`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
