import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import conceptLogos from "../../src/data/concept-logos.json" with { type: "json" };

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const logoDir = path.join(siteRoot, "public/concept-logos");
const slugSet = new Set(conceptLogos.slugs);
const cache = new Map();

export function hasConceptLogo(slug) {
  return slugSet.has(slug);
}

export function loadConceptLogoSvg(slug) {
  if (!hasConceptLogo(slug)) return null;
  if (cache.has(slug)) return cache.get(slug);

  const file = path.join(logoDir, `${slug}.svg`);
  if (!existsSync(file)) return null;

  const svg = readFileSync(file, "utf8").replace(/<\?xml[^?]*\?>\s*/i, "").trim();
  cache.set(slug, svg);
  return svg;
}
