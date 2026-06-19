import { build } from "esbuild";
import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const demosDir = join(import.meta.dirname, "demos");

function entrypoints() {
  const entries = [];
  for (const name of readdirSync(demosDir)) {
    const demoDir = join(demosDir, name);
    if (!statSync(demoDir).isDirectory()) continue;

    const tsFiles = readdirSync(demoDir).filter(
      (file) => file.endsWith(".ts") && !file.endsWith(".test.ts"),
    );
    if (tsFiles.length === 0) continue;

    const preferred = tsFiles.includes("app.ts") ? "app.ts" : tsFiles.sort()[0];
    const infile = join(demoDir, preferred);
    const outfile = infile.replace(/\.ts$/, ".js");
    entries.push({ infile, outfile, label: name });
  }
  return entries;
}

const entries = entrypoints();
if (entries.length === 0) {
  console.log("No demo TypeScript entrypoints found.");
  process.exit(0);
}

for (const { infile, outfile, label } of entries) {
  await build({
    entryPoints: [infile],
    outfile,
    format: "esm",
    target: "es2020",
    logLevel: "info",
  });
  console.log(`Built ${label}`);
}
