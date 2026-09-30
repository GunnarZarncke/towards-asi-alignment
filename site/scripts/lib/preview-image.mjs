import { access, readdir } from "node:fs/promises";
import path from "node:path";

const PREVIEW_IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp"];

/** First site-root image path in markdown or HTML body text. */
export function firstImageSrcFromText(text) {
  if (!text) return undefined;
  const htmlMatch = text.match(/<img[^>]+src=["']([^"']+)["']/i);
  if (htmlMatch) return normalizePreviewPath(htmlMatch[1]);
  const mdMatch = text.match(/!\[[^\]]*\]\(([^)]+)\)/);
  if (mdMatch) return normalizePreviewPath(mdMatch[1].trim());
  return undefined;
}

function normalizePreviewPath(src) {
  if (!src || src.startsWith("data:") || src.startsWith("http://") || src.startsWith("https://")) {
    return undefined;
  }
  if (src.startsWith("/")) return src;
  return `/${src.replace(/^\/+/, "")}`;
}

async function fileExists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function memePreviewFromBodyPath(siteRoot, bodyPath) {
  if (!bodyPath) return undefined;
  const base = path.basename(bodyPath, path.extname(bodyPath));
  const memeDir = path.join(siteRoot, "public", "field-news", "memes");
  for (const ext of PREVIEW_IMAGE_EXTS) {
    const filePath = path.join(memeDir, `${base}${ext}`);
    if (await fileExists(filePath)) return `/field-news/memes/${base}${ext}`;
  }
  return undefined;
}

/** Chapter opening JPEG copied to public/figures/illustrations/web/ by sync-chapter-illustrations. */
export async function chapterIllustrationPreview(siteRoot, bookPageId) {
  if (!bookPageId) return undefined;
  const dir = path.join(siteRoot, "public", "figures", "illustrations", "web");
  try {
    const files = await readdir(dir);
    const match = files.find(
      (name) => name.startsWith(`${bookPageId}_`) && /\.jpe?g$/i.test(name)
    );
    if (match) return `/figures/illustrations/web/${match}`;
  } catch {
    // no illustration dir yet
  }
  return undefined;
}

/**
 * Resolve og:image / RSS preview path for a card.
 * Order: explicit previewImage → first in-body image → chapter illustration → field-news meme basename.
 */
export async function resolveCardPreviewImage({
  siteRoot,
  explicit,
  bodyPath,
  bodyText,
  bookPageId
}) {
  if (explicit) return explicit;

  const fromBody = firstImageSrcFromText(bodyText);
  if (fromBody) {
    const publicPath = path.join(siteRoot, "public", fromBody.replace(/^\/+/, ""));
    if (await fileExists(publicPath)) return fromBody;
  }

  const fromChapter = await chapterIllustrationPreview(siteRoot, bookPageId);
  if (fromChapter) return fromChapter;

  return memePreviewFromBodyPath(siteRoot, bodyPath);
}
