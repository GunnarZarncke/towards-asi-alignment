import { access, copyFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const PDF_NAME = "towards-superintelligence-alignment.pdf";
const src = path.join(repoRoot, "dist", "pdf", PDF_NAME);
const dest = path.join(siteRoot, "public", PDF_NAME);

async function exists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  if (!(await exists(src))) {
    const onMainDeploy =
      process.env.GITHUB_EVENT_NAME === "push" &&
      process.env.GITHUB_REF === "refs/heads/main";
    if (onMainDeploy) {
      console.error(`Missing ${src} — build the book PDF before deploying the site.`);
      process.exit(1);
    }
    console.warn(`PDF not found at ${src}; run ./build.sh from the repo root. Site PDF links will 404.`);
    return;
  }

  await mkdir(path.dirname(dest), { recursive: true });
  await copyFile(src, dest);
  console.log(`Copied ${PDF_NAME} to site/public/ for deployment.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
