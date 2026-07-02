#!/usr/bin/env node
/** Download the latest release PDF asset into dist/pdf/ for site deployment. */
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "../..");
const PDF_NAME = "towards-superintelligence-alignment.pdf";
const outDir = path.join(repoRoot, "dist", "pdf");
const outPath = path.join(outDir, PDF_NAME);

const releaseApi =
  "https://api.github.com/repos/GunnarZarncke/towards-asi-alignment/releases/latest";

async function main() {
  const releaseRes = await fetch(releaseApi, {
    headers: { Accept: "application/vnd.github+json", "User-Agent": "towards-asi-alignment-site" }
  });
  if (!releaseRes.ok) {
    throw new Error(`Release lookup failed: ${releaseRes.status} ${releaseRes.statusText}`);
  }
  const release = await releaseRes.json();
  const asset = (release.assets ?? []).find((entry) => entry.name === PDF_NAME);
  if (!asset?.browser_download_url) {
    throw new Error(`No ${PDF_NAME} asset on release ${release.tag_name ?? "latest"}`);
  }

  const pdfRes = await fetch(asset.browser_download_url);
  if (!pdfRes.ok) {
    throw new Error(`PDF download failed: ${pdfRes.status} ${pdfRes.statusText}`);
  }

  await mkdir(outDir, { recursive: true });
  await writeFile(outPath, Buffer.from(await pdfRes.arrayBuffer()));
  console.log(`Downloaded ${PDF_NAME} from ${release.tag_name} to ${outPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
