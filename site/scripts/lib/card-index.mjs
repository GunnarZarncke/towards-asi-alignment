import { readFileSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

function walkMdFiles(dir) {
  const files = [];
  for (const entry of readdirSync(dir)) {
    const abs = path.join(dir, entry);
    if (statSync(abs).isDirectory()) {
      files.push(...walkMdFiles(abs));
      continue;
    }
    if (entry.endsWith(".md")) files.push(abs);
  }
  return files;
}

function parseSimpleYamlList(block, key) {
  const inline = block.match(new RegExp(`^${key}:\\s*\\[(.+?)\\]`, "m"));
  if (inline) {
    return inline[1]
      .split(",")
      .map((item) => item.trim().replace(/^"|"$/g, ""))
      .filter(Boolean);
  }
  const re = new RegExp(`^${key}:\\s*\\n((?:  - .+\\n)+)`, "m");
  const match = block.match(re);
  if (!match) return [];
  return [...match[1].matchAll(/^\s*-\s+(.+)$/gm)].map((m) => m[1].replace(/^"|"$/g, ""));
}

function parseFormulas(block) {
  const formulas = [];
  const re = /^\s*-\s+id:\s+"(.+)"[\s\S]*?(?=^\s*-\s+id:|^\s*\w|$)/gm;
  let match;
  while ((match = re.exec(block)) !== null) {
    const chunk = match[0];
    const id = chunk.match(/id:\s+"(.+?)"/)?.[1];
    if (id) formulas.push(id);
  }
  return formulas;
}

function cardType(fm) {
  const match = fm.match(/^type:\s+"?([^"\n]+)"?\s*$/m);
  return match?.[1] || "";
}

export function buildCardIndex(cardsDir) {
  /** @type {Map<string, { slug: string, type: string }>} */
  const labelToCard = new Map();
  const files = walkMdFiles(cardsDir).sort((a, b) => {
    const aChapter = a.includes("/chapters/") ? 0 : 1;
    const bChapter = b.includes("/chapters/") ? 0 : 1;
    return aChapter - bChapter;
  });

  for (const abs of files) {
    const slug = path.relative(cardsDir, abs).replace(/\\/g, "/").replace(/\.md$/, "");
    const text = readFileSync(abs, "utf8");
    const fmMatch = text.match(/^---\n([\s\S]*?)\n---/);
    if (!fmMatch) continue;
    const fm = fmMatch[1];
    const type = cardType(fm);
    const isChapterCard = type === "chapter" || type === "appendix" || type === "frontmatter";
    const entry = { slug, type };

    for (const label of parseSimpleYamlList(fm, "bookLabels")) {
      if (!isChapterCard && label.startsWith("ch:") && labelToCard.has(label)) continue;
      labelToCard.set(label, entry);
    }
    if (fm.includes("formulas:")) {
      for (const id of parseFormulas(fm)) labelToCard.set(id, entry);
    }
  }
  return labelToCard;
}

export function validateCardLabels(cardsDir, labelIndex) {
  const errors = [];
  for (const abs of walkMdFiles(cardsDir)) {
    if (abs.includes("/chapters/")) continue;
    const text = readFileSync(abs, "utf8");
    const fmMatch = text.match(/^---\n([\s\S]*?)\n---/);
    if (!fmMatch) continue;
    const fm = fmMatch[1];
    for (const label of parseSimpleYamlList(fm, "bookLabels")) {
      if (!labelIndex.has(label)) {
        errors.push(`Card ${path.basename(abs)} references unknown bookLabel: ${label}`);
      }
    }
  }
  return errors;
}
