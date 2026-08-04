// Copy concept-card logo SVGs from drafts/illustrations/concept-logos/ to
// site/public/concept-logos/ for use on concept card pages and indexes.
import { cp, mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const SRC_DIR = path.join(repoRoot, "drafts", "illustrations", "concept-logos");
const OUT_DIR = path.join(siteRoot, "public", "concept-logos");
const MANIFEST_PATH = path.join(siteRoot, "src", "data", "concept-logos.json");

const checkMode = process.argv.includes("--check");

async function listSourceSvgs() {
  const names = await readdir(SRC_DIR);
  return names.filter((name) => name.endsWith(".svg")).sort();
}

async function writeManifest(slugs) {
  const payload = { slugs, updatedFrom: "drafts/illustrations/concept-logos" };
  await writeFile(MANIFEST_PATH, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function readManifest() {
  try {
    const text = await readFile(MANIFEST_PATH, "utf8");
    return JSON.parse(text);
  } catch {
    return { slugs: [] };
  }
}

async function sync() {
  const slugs = (await listSourceSvgs()).map((name) => name.replace(/\.svg$/, ""));
  await mkdir(OUT_DIR, { recursive: true });

  const existing = (await readdir(OUT_DIR)).filter((name) => name.endsWith(".svg"));
  const expected = new Set(slugs.map((slug) => `${slug}.svg`));

  for (const name of existing) {
    if (!expected.has(name)) {
      await rm(path.join(OUT_DIR, name));
    }
  }

  for (const slug of slugs) {
    await cp(path.join(SRC_DIR, `${slug}.svg`), path.join(OUT_DIR, `${slug}.svg`));
  }

  await writeManifest(slugs);
  console.log(`[sync-concept-logos] copied ${slugs.length} SVGs -> public/concept-logos/`);
}

async function check() {
  const slugs = (await listSourceSvgs()).map((name) => name.replace(/\.svg$/, ""));
  const manifest = await readManifest();
  const manifestSlugs = [...(manifest.slugs ?? [])].sort();
  const sorted = [...slugs].sort();

  if (JSON.stringify(manifestSlugs) !== JSON.stringify(sorted)) {
    console.error("[sync-concept-logos] manifest out of date; run npm run sync:concept-logos");
    process.exit(1);
  }

  for (const slug of slugs) {
    try {
      await readFile(path.join(OUT_DIR, `${slug}.svg`), "utf8");
    } catch {
      console.error(`[sync-concept-logos] missing public/concept-logos/${slug}.svg`);
      process.exit(1);
    }
  }

  console.log(`[sync-concept-logos] ok (${slugs.length} logos)`);
}

if (checkMode) {
  await check();
} else {
  await sync();
}
