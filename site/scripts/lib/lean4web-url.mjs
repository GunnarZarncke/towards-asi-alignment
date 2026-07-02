import LZString from "lz-string";

export const LEAN4WEB_BASE = "https://live.lean-lang.org/";

/** Practical share-link ceiling (conservative; IE-era total URL ~2048). */
export const CONSERVATIVE_MAX_URL_LENGTH = 1800;

/** Upper bound before sync warns even when a shorter fallback exists. */
export const DEFAULT_MAX_URL_LENGTH = 8000;

const RAW_GITHUB_BASE =
  "https://raw.githubusercontent.com/GunnarZarncke/towards-asi-alignment/main/";

/** Matches lean4web: compressToBase64, strip trailing = padding. */
export function lean4WebCodez(code, base = LEAN4WEB_BASE) {
  const compressed = LZString.compressToBase64(code).replace(/=+$/, "");
  return `${base}#codez=${compressed}`;
}

export function lean4WebPlain(code, base = LEAN4WEB_BASE) {
  return `${base}#code=${encodeURIComponent(code)}`;
}

export function lean4WebImportUrl(rawFileUrl, base = LEAN4WEB_BASE) {
  return `${base}#url=${encodeURIComponent(rawFileUrl)}`;
}

export function playgroundRawUrl(playgroundFile) {
  const rel = playgroundFile.replace(/^formal\//, "");
  return `${RAW_GITHUB_BASE}${rel}`;
}

/**
 * Pick the shortest lean4web link that fits under maxUrlLength.
 * Prefers inline codez; falls back to #url= GitHub raw when codez is too long.
 */
export function buildLean4WebUrl(code, options = {}) {
  const {
    base = LEAN4WEB_BASE,
    playgroundFile = null,
    maxUrlLength = DEFAULT_MAX_URL_LENGTH,
    conservativeMax = CONSERVATIVE_MAX_URL_LENGTH
  } = options;

  const codeLength = code.length;
  const codezUrl = lean4WebCodez(code, base);
  const plainUrl = lean4WebPlain(code, base);

  const candidates = [
    { encoding: "codez", url: codezUrl, length: codezUrl.length },
    { encoding: "code", url: plainUrl, length: plainUrl.length }
  ];

  if (playgroundFile) {
    const importUrl = lean4WebImportUrl(playgroundRawUrl(playgroundFile), base);
    candidates.push({ encoding: "url", url: importUrl, length: importUrl.length });
  }

  candidates.sort((a, b) => a.length - b.length || (a.encoding === "codez" ? -1 : 1));

  const codez = candidates.find((c) => c.encoding === "codez");
  const importCandidate = candidates.find((c) => c.encoding === "url");

  let chosen;
  if (codez && codez.length <= maxUrlLength) {
    chosen = codez;
  } else if (importCandidate && importCandidate.length <= maxUrlLength) {
    chosen = importCandidate;
  } else {
    const withinLimit = candidates.filter((c) => c.length <= maxUrlLength);
    chosen = withinLimit[0] ?? candidates[0];
  }
  const codezPayload = codezUrl.split("#codez=")[1];
  const roundtrip = LZString.decompressFromBase64(codezPayload);

  const warnings = [];
  if (roundtrip !== code) {
    warnings.push("codez round-trip decompression mismatch");
  }
  if (chosen.length > conservativeMax) {
    warnings.push(
      `URL length ${chosen.length} exceeds conservative share limit ${conservativeMax}`
    );
  }
  if (chosen.length > maxUrlLength) {
    warnings.push(`URL length ${chosen.length} exceeds max ${maxUrlLength}; no fallback available`);
  }

  return {
    url: chosen.url,
    encoding: chosen.encoding,
    codeLength,
    urlLength: chosen.length,
    withinLimit: chosen.length <= maxUrlLength,
    withinConservativeLimit: chosen.length <= conservativeMax,
    warnings
  };
}

/** Back-compat: return the best URL string. */
export function lean4WebUrl(code, base = LEAN4WEB_BASE) {
  return buildLean4WebUrl(code, { base }).url;
}
