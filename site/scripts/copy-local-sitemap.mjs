import { cp, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const distDir = path.join(siteRoot, "dist");
const publicDir = path.join(siteRoot, "public");

await mkdir(publicDir, { recursive: true });
await Promise.all(
  ["sitemap-index.xml", "sitemap-0.xml"].map((file) =>
    cp(path.join(distDir, file), path.join(publicDir, file))
  )
);
console.log("Copied generated sitemaps to public/ for local development.");
