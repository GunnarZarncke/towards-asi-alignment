/** Download the latest release PDF asset into dist/pdf/ for site deployment. */
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

export const BOOK_PDF_FILENAME = "towards-superintelligence-alignment.pdf";

const releaseApi =
  "https://api.github.com/repos/GunnarZarncke/towards-asi-alignment/releases/latest";

export async function fetchBookPdf(outPath) {
  const releaseRes = await fetch(releaseApi, {
    headers: { Accept: "application/vnd.github+json", "User-Agent": "towards-asi-alignment-site" }
  });
  if (!releaseRes.ok) {
    throw new Error(`Release lookup failed: ${releaseRes.status} ${releaseRes.statusText}`);
  }
  const release = await releaseRes.json();
  const asset = (release.assets ?? []).find((entry) => entry.name === BOOK_PDF_FILENAME);
  if (!asset?.browser_download_url) {
    throw new Error(`No ${BOOK_PDF_FILENAME} asset on release ${release.tag_name ?? "latest"}`);
  }

  const pdfRes = await fetch(asset.browser_download_url);
  if (!pdfRes.ok) {
    throw new Error(`PDF download failed: ${pdfRes.status} ${pdfRes.statusText}`);
  }

  await mkdir(path.dirname(outPath), { recursive: true });
  await writeFile(outPath, Buffer.from(await pdfRes.arrayBuffer()));
  return { releaseTag: release.tag_name ?? "latest", outPath };
}
