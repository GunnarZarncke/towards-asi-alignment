import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { publishChapterDemos } from "./lib/publish-chapter-demos.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const DEMOS_DIR = path.join(repoRoot, "demos");
const BOOK_PATH = path.join(siteRoot, "src", "data", "book.json");
const CARDS_DIR = path.join(siteRoot, "src", "content", "cards");
const OUT_PATH = path.join(siteRoot, "src", "data", "demos.json");

const DEFAULT_STATIC_PORT = 8765;

function parseChapterId(folderName) {
  const match = folderName.match(/^ch(\d+)/);
  return match ? `ch${match[1].padStart(2, "0")}` : null;
}

function titleFromHtml(html) {
  return html.match(/<title>([^<]+)<\/title>/i)?.[1]?.trim() || null;
}

function summaryFromReadme(text) {
  const lines = text.split("\n");
  let started = false;
  const parts = [];
  for (const line of lines) {
    if (line.startsWith("#")) {
      started = true;
      continue;
    }
    if (!started) continue;
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("```")) continue;
    if (trimmed.startsWith("From ") || trimmed.startsWith("Run ") || trimmed.startsWith("Board:")) continue;
    parts.push(trimmed.replace(/\*\*/g, ""));
    if (parts.join(" ").length > 40) break;
  }
  return parts.join(" ").replace(/\s+/g, " ").trim();
}

function summaryFromIndexHtml(html) {
  const lead = html.match(/class="lead"[^>]*>([\s\S]*?)<\//i)?.[1];
  if (!lead) return "";
  return lead.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
}

async function loadBookChapters() {
  try {
    const book = JSON.parse(await readFile(BOOK_PATH, "utf8"));
    return new Map(book.chapters.map((ch) => [ch.id, ch.title]));
  } catch {
    return new Map();
  }
}

async function loadCardLinks() {
  const byDemo = new Map();
  const entries = await readdir(CARDS_DIR, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
    const text = await readFile(path.join(CARDS_DIR, entry.name), "utf8");
    const slug = entry.name.replace(/\.md$/, "");
    const title = text.match(/^title:\s*"?([^"\n]+)"?/m)?.[1] || slug;
    for (const match of text.matchAll(/demoId:\s*"([^"]+)"/g)) {
      if (!byDemo.has(match[1])) byDemo.set(match[1], []);
      byDemo.get(match[1]).push({ slug, title });
    }
  }
  return byDemo;
}

async function loadDemoFolder(name) {
  const dir = path.join(DEMOS_DIR, name);
  const indexPath = path.join(dir, "index.html");
  const readmePath = path.join(dir, "README.md");
  const backendPath = path.join(dir, "backend.json");

  const indexHtml = await readFile(indexPath, "utf8");
  let readme = "";
  try {
    readme = await readFile(readmePath, "utf8");
  } catch {
    /* optional */
  }

  let backend = null;
  try {
    backend = JSON.parse(await readFile(backendPath, "utf8"));
  } catch {
    /* static demo */
  }

  const hasPython = backend !== null;
  const hasTypeScript = (await readdir(dir)).some((f) => f.endsWith(".ts") && !f.endsWith(".test.ts"));
  const port = backend?.port || DEFAULT_STATIC_PORT;
  const chapterId = parseChapterId(name);
  const sitePath = `/chapter-demos/${name}/`;
  const standalonePath = hasPython ? "/" : `/${name}/`;
  const standaloneUrl = hasPython
    ? `http://127.0.0.1:${port}/`
    : `http://127.0.0.1:${DEFAULT_STATIC_PORT}/${name}/`;

  return {
    id: name,
    title: titleFromHtml(indexHtml) || name,
    summary: summaryFromReadme(readme) || summaryFromIndexHtml(indexHtml) || "",
    chapterId,
    chapterNumber: chapterId ? Number(chapterId.replace("ch", "")) : null,
    kind: hasPython ? "python-backend" : hasTypeScript ? "static-typescript" : "static-html",
    port,
    sitePath,
    standalonePath,
    standaloneUrl,
    requiresBackend: hasPython,
    githubPath: `demos/${name}`,
    hasReadme: readme.length > 0,
    hasTests: (await readdir(dir, { withFileTypes: true }).catch(() => [])).some(
      (e) => e.isDirectory() && e.name === "tests"
    )
  };
}

async function main() {
  await publishChapterDemos();

  const [chapters, cardLinks] = await Promise.all([loadBookChapters(), loadCardLinks()]);
  const folders = (await readdir(DEMOS_DIR, { withFileTypes: true }))
    .filter((e) => e.isDirectory() && e.name.startsWith("ch"))
    .map((e) => e.name)
    .sort((a, b) => a.localeCompare(b));

  const demos = [];
  for (const folder of folders) {
    const demo = await loadDemoFolder(folder);
    demo.chapterTitle = demo.chapterId ? chapters.get(demo.chapterId) || null : null;
    demo.cards = cardLinks.get(demo.id) || [];
    demos.push(demo);
  }

  demos.sort((a, b) => (a.chapterNumber || 999) - (b.chapterNumber || 999));

  const payload = {
    generatedAt: new Date().toISOString(),
    standaloneCommand: "cd demos && python3 serve.py",
    standalonePort: DEFAULT_STATIC_PORT,
    demos
  };

  await writeFile(OUT_PATH, JSON.stringify(payload, null, 2) + "\n", "utf8");
  console.log(`Wrote ${demos.length} chapter demos to src/data/demos.json`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
