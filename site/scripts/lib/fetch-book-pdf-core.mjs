/** Download the latest release PDF asset into dist/pdf/ for site deployment. */
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

export const BOOK_PDF_FILENAME = "towards-superintelligence-alignment.pdf";

const REPO = "GunnarZarncke/towards-asi-alignment";
const directDownloadUrl = `https://github.com/${REPO}/releases/latest/download/${BOOK_PDF_FILENAME}`;
const releaseApi = `https://api.github.com/repos/${REPO}/releases/latest`;

function githubHeaders() {
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": "towards-asi-alignment-site",
    "X-GitHub-Api-Version": "2022-11-28"
  };
  const token = process.env.GITHUB_TOKEN;
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

function releaseTagFromUrl(url) {
  const match = String(url).match(/\/releases\/download\/([^/]+)\//);
  return match?.[1] ?? "latest";
}

async function sleep(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithRetry(url, options, { attempts = 3 } = {}) {
  let lastError;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const res = await fetch(url, options);
    if (res.ok) return res;

    const retryable = res.status === 403 || res.status === 429;
    lastError = new Error(`HTTP ${res.status} ${res.statusText}`);
    if (!retryable || attempt === attempts) {
      throw lastError;
    }

    const retryAfter = Number(res.headers.get("retry-after"));
    const delayMs = Number.isFinite(retryAfter) && retryAfter > 0 ? retryAfter * 1000 : attempt * 2000;
    await sleep(delayMs);
  }
  throw lastError;
}

async function downloadDirect(outPath) {
  const pdfRes = await fetchWithRetry(directDownloadUrl, {
    headers: githubHeaders(),
    redirect: "follow"
  });
  await mkdir(path.dirname(outPath), { recursive: true });
  await writeFile(outPath, Buffer.from(await pdfRes.arrayBuffer()));
  return { releaseTag: releaseTagFromUrl(pdfRes.url), outPath };
}

async function downloadViaReleaseApi(outPath) {
  const releaseRes = await fetchWithRetry(releaseApi, { headers: githubHeaders() });
  const release = await releaseRes.json();
  const asset = (release.assets ?? []).find((entry) => entry.name === BOOK_PDF_FILENAME);
  if (!asset?.browser_download_url) {
    throw new Error(`No ${BOOK_PDF_FILENAME} asset on release ${release.tag_name ?? "latest"}`);
  }

  const pdfRes = await fetchWithRetry(asset.browser_download_url, { headers: githubHeaders() });
  await mkdir(path.dirname(outPath), { recursive: true });
  await writeFile(outPath, Buffer.from(await pdfRes.arrayBuffer()));
  return { releaseTag: release.tag_name ?? "latest", outPath };
}

export async function fetchBookPdf(outPath) {
  try {
    return await downloadDirect(outPath);
  } catch (directErr) {
    try {
      return await downloadViaReleaseApi(outPath);
    } catch (apiErr) {
      throw new Error(
        `Direct download failed (${directErr.message}); release API failed (${apiErr.message})`
      );
    }
  }
}
