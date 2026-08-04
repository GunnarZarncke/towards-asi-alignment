import { access, copyFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { BOOK_PDF_FILENAME, fetchBookPdf } from "./lib/fetch-book-pdf-core.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const src = path.join(repoRoot, "dist", "pdf", BOOK_PDF_FILENAME);
const dest = path.join(siteRoot, "public", BOOK_PDF_FILENAME);

async function exists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function ensureSourcePdf() {
  if (await exists(src)) return "local";

  const allowFetch =
    process.env.SITE_FETCH_PDF !== "0" &&
    (process.env.CI === "true" || process.env.SITE_FETCH_PDF === "1");

  if (!allowFetch) return null;

  try {
    const { releaseTag } = await fetchBookPdf(src);
    console.log(`Fetched ${BOOK_PDF_FILENAME} from release ${releaseTag} into dist/pdf/.`);
    return "release";
  } catch (err) {
    console.warn(`Could not fetch ${BOOK_PDF_FILENAME}: ${err.message}`);
    return null;
  }
}

async function main() {
  const source = await ensureSourcePdf();
  if (!source) {
    const onMainDeploy =
      process.env.GITHUB_EVENT_NAME === "push" &&
      process.env.GITHUB_REF === "refs/heads/main";
    if (onMainDeploy) {
      console.error(
        `Missing ${src} — build the book PDF locally or publish a GitHub Release with ${BOOK_PDF_FILENAME}.`
      );
      process.exit(1);
    }
    console.warn(
      `PDF not found at ${src}; run ./build.sh from the repo root or set SITE_FETCH_PDF=1. Site PDF links will 404.`
    );
    return;
  }

  await mkdir(path.dirname(dest), { recursive: true });
  await copyFile(src, dest);
  console.log(`Copied ${BOOK_PDF_FILENAME} to site/public/ for deployment (${source}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
