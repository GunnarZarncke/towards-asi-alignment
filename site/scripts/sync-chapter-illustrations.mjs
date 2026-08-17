// Copy chapter-opening web JPEGs into site/public for same-origin serving and offline cache.
import { cp, mkdir, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const sourceDir = path.join(repoRoot, "figures", "illustrations", "web");
const destDir = path.join(siteRoot, "public", "figures", "illustrations", "web");

async function sync() {
  await mkdir(destDir, { recursive: true });
  const files = (await readdir(sourceDir)).filter((name) => name.endsWith(".jpg"));
  for (const name of files) {
    await cp(path.join(sourceDir, name), path.join(destDir, name));
  }
  console.log(`[sync-chapter-illustrations] copied ${files.length} JPEGs -> site/public/figures/illustrations/web/`);
}

sync().catch((err) => {
  console.error(err);
  process.exit(1);
});
