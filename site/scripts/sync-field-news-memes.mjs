// Copy field-news meme images from scripts/meme_workflow/output into site/public/.
// Dest basename must match metadata/field-news/bodies/YYYY-MM-slug.{jpg,png}.
import { cp, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

/** @type {{ src: string; dest: string }[]} */
const MEMES = [
  {
    src: "scripts/meme_workflow/output/openai-training-safety-case.jpg",
    dest: "field-news/memes/2026-09-openai-training-safety-case.jpg"
  },
  {
    src: "scripts/meme_workflow/output/huang-release-rule.jpg",
    dest: "field-news/memes/2026-09-huang-klein-zvi.jpg"
  },
  {
    src: "scripts/meme_workflow/output/math-misalignment.png",
    dest: "field-news/memes/2026-09-math-misalignment.png"
  },
  {
    src: "scripts/meme_workflow/output/ban-asi-act.jpg",
    dest: "field-news/memes/2026-09-ban-asi-act.jpg"
  },
  {
    src: "scripts/meme_workflow/output/openai-rsi-standards.jpg",
    dest: "field-news/memes/2026-09-openai-rsi-standards.jpg"
  },
  {
    src: "scripts/meme_workflow/output/anthropic-pace-measurements.jpg",
    dest: "field-news/memes/2026-09-anthropic-pace-measurements.jpg"
  },
  {
    src: "scripts/meme_workflow/output/embedded-evaluators.jpg",
    dest: "field-news/memes/2026-09-embedded-evaluators.jpg"
  },
  {
    src: "scripts/meme_workflow/output/openai-dns-chatbot.jpg",
    dest: "field-news/memes/2026-09-openai-dns-chatbot.jpg"
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
