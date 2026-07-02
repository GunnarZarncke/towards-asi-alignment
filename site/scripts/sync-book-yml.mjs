import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const bookPath = path.join(repoRoot, "metadata", "book.yml");
const outputDir = path.join(siteRoot, "src", "data");
const outputPath = path.join(outputDir, "book.json");

const partRanges = [
  ["part01", 1, 5, "The Alignment Problem Reframed"],
  ["part02", 6, 10, "Agents, Boundaries, and Real Optimizers"],
  ["part03", 11, 14, "Capability Growth and Competence"],
  ["part04", 15, 20, "Value Bundles"],
  ["part05", 21, 24, "Goal Inference and Transport"],
  ["part06", 25, 29, "Correction Channels"],
  ["part07", 30, 33, "Successors and Continuity"],
  ["part08", 34, 38, "Attractor Basins and Selection"],
  ["part09", 39, 44, "Safety Cases and Adversaries"],
  ["part10", 45, 48, "Civilizational Limits"]
];

function chapterNumber(id) {
  return Number(id.replace("ch", ""));
}

function partForChapter(number) {
  const found = partRanges.find(([, start, end]) => number >= start && number <= end);
  if (!found) return null;
  const [id, start, end, title] = found;
  return { id, start, end, title };
}

function cleanValue(raw) {
  const value = raw.trim();
  if (value.startsWith("[") && value.endsWith("]")) {
    return value.slice(1, -1).split(",").map((item) => item.trim()).filter(Boolean);
  }
  if (value.startsWith("\"") && value.endsWith("\"")) {
    return value.slice(1, -1);
  }
  return value;
}

function readBookSubset(source) {
  const book = {
    title: "",
    subtitle: "",
    author: "",
    milestone: "",
    chapters: {},
    parts: {}
  };
  let section = null;
  let currentId = null;

  for (const line of source.split(/\r?\n/)) {
    const top = line.match(/^([a-z_]+):\s*(.+)$/);
    if (top && !["chapters", "parts"].includes(top[1])) {
      book[top[1]] = cleanValue(top[2]);
      continue;
    }

    if (line === "chapters:") {
      section = "chapters";
      currentId = null;
      continue;
    }
    if (line === "parts:") {
      section = "parts";
      currentId = null;
      continue;
    }

    const item = line.match(/^  (ch\d+|part\d+):\s*$/);
    if (item) {
      currentId = item[1];
      if (section === "chapters") book.chapters[currentId] = {};
      if (section === "parts") book.parts[currentId] = {};
      continue;
    }

    const field = line.match(/^    ([a-z_]+):\s*(.+)$/);
    if (section && currentId && field) {
      const [, key, raw] = field;
      if (section === "chapters" && ["title", "status", "formal_density", "reviewer_needed"].includes(key)) {
        book.chapters[currentId][key] = cleanValue(raw);
      }
      if (section === "parts" && key === "summary") {
        book.parts[currentId][key] = cleanValue(raw);
      }
    }
  }

  return book;
}

const source = await readFile(bookPath, "utf8");
const book = readBookSubset(source);

const chapters = Object.entries(book.chapters).map(([id, chapter]) => {
  const number = chapterNumber(id);
  return {
    id,
    number,
    title: chapter.title,
    status: chapter.status,
    formalDensity: chapter.formal_density,
    reviewerNeeded: chapter.reviewer_needed ?? [],
    part: partForChapter(number)
  };
});

const parts = partRanges.map(([id, start, end, title]) => ({
  id,
  title,
  range: `${start}-${end}`,
  summary: book.parts?.[id]?.summary ?? "",
  chapters: chapters.filter((chapter) => chapter.part?.id === id)
}));

await mkdir(outputDir, { recursive: true });
await writeFile(
  outputPath,
  JSON.stringify({
    title: book.title,
    subtitle: book.subtitle,
    author: book.author,
    milestone: book.milestone,
    chapters,
    parts
  }, null, 2) + "\n"
);

console.log(`Wrote ${path.relative(siteRoot, outputPath)} from metadata/book.yml`);
