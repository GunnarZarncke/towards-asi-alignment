// Copy field-news meme images from scripts/meme_workflow/output into site/public/.
import { cp, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

/** @type {{ src: string; dest: string }[]} */
const MEMES = [
  {
    src: "scripts/meme_workflow/output/huang-release-rule.jpg",
    dest: "field-news/memes/field-news-huang-klein-zvi-sep-2026.jpg"
  },
  {
    src: "scripts/meme_workflow/output/math-misalignment.png",
    dest: "field-news/memes/field-news-math-misalignment-sep-2026.png"
  },
  {
    src: "scripts/meme_workflow/output/ban-asi-act.jpg",
    dest: "field-news/memes/field-news-ban-asi-act-sep-2026.jpg"
  },
  {
    src: "scripts/meme_workflow/output/openai-rsi-standards.jpg",
    dest: "field-news/memes/field-news-openai-rsi-standards-sep-2026.jpg"
  },
  {
    src: "scripts/meme_workflow/output/anthropic-pace-measurements.jpg",
    dest: "field-news/memes/field-news-anthropic-pace-measurements-sep-2026.jpg"
  }
];

async function sync() {
  for (const { src, dest } of MEMES) {
    const from = path.join(repoRoot, src);
    const to = path.join(siteRoot, "public", dest);
    await mkdir(path.dirname(to), { recursive: true });
    await cp(from, to);
  }
  console.log(`[sync-field-news-memes] copied ${MEMES.length} image(s) -> site/public/field-news/memes/`);
}

sync().catch((err) => {
  console.error(err);
  process.exit(1);
});
