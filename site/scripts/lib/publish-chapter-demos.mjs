import { spawn } from "node:child_process";
import { cp, mkdir, readdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "../..");
const repoRoot = path.resolve(siteRoot, "..");
const demosRoot = path.join(repoRoot, "demos");
const demosSrc = demosRoot;
const demosPublic = path.join(siteRoot, "public", "chapter-demos");

const STATIC_COPY = new Set([".html", ".js", ".css", ".json", ".svg", ".png", ".webp", ".ico"]);
const SKIP_DIRS = new Set(["tests", "__pycache__", "node_modules"]);

function runBuildDemos() {
  return new Promise((resolve, reject) => {
    const child = spawn("node", ["build-demos.mjs"], {
      cwd: demosRoot,
      stdio: "inherit"
    });
    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`build-demos.mjs exited with ${code}`));
    });
  });
}

async function hasBackend(demoDir) {
  try {
    await stat(path.join(demoDir, "backend.json"));
    await stat(path.join(demoDir, "app.py"));
    return true;
  } catch {
    return false;
  }
}

async function hasStaticFrontend(demoDir) {
  const entries = await readdir(demoDir);
  return entries.some((name) => name.endsWith(".js") && !name.endsWith(".test.js"));
}

async function isHybridBackend(demoDir) {
  try {
    const cfg = JSON.parse(await readFile(path.join(demoDir, "backend.json"), "utf8"));
    return cfg.hybrid === true || (await hasStaticFrontend(demoDir));
  } catch {
    return false;
  }
}

async function copyStaticDemo(demoId, demoDir) {
  const outDir = path.join(demosPublic, demoId);
  await mkdir(outDir, { recursive: true });
  const entries = await readdir(demoDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      continue;
    }
    const ext = path.extname(entry.name).toLowerCase();
    if (!STATIC_COPY.has(ext)) continue;
    if (entry.name.endsWith(".test.js")) continue;
    await cp(path.join(demoDir, entry.name), path.join(outDir, entry.name));
  }
}

async function writeBackendFallback(demoId, title, backendPort) {
  const outDir = path.join(demosPublic, demoId);
  await mkdir(outDir, { recursive: true });
  const html = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${title}</title>
    <style>
      body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }
      code { font-size: 0.92em; }
    </style>
  </head>
  <body>
    <h1>${title}</h1>
    <p>This demo uses a Python backend (port ${backendPort}). With <code>./serve-site.sh</code> running, open the same URL again — the site proxies to the backend automatically.</p>
    <p>For demos only: <code>./serve-demos.sh</code> then open <code>http://127.0.0.1:${backendPort}/</code>.</p>
  </body>
</html>
`;
  await writeFile(path.join(outDir, "index.html"), html, "utf8");
}

export async function publishChapterDemos() {
  await runBuildDemos();
  await rm(demosPublic, { recursive: true, force: true });
  await mkdir(demosPublic, { recursive: true });

  const folders = (await readdir(demosSrc, { withFileTypes: true }))
    .filter((e) => e.isDirectory() && e.name.startsWith("ch"))
    .map((e) => e.name)
    .sort();

  for (const demoId of folders) {
    const demoDir = path.join(demosSrc, demoId);
    try {
      await stat(path.join(demoDir, "index.html"));
    } catch {
      continue;
    }

    if (await hasBackend(demoDir)) {
      if (await isHybridBackend(demoDir)) {
        await copyStaticDemo(demoId, demoDir);
      } else {
        const backend = JSON.parse(await readFile(path.join(demoDir, "backend.json"), "utf8"));
        const indexHtml = await readFile(path.join(demoDir, "index.html"), "utf8");
        const title = indexHtml.match(/<title>([^<]+)<\/title>/i)?.[1] || demoId;
        await writeBackendFallback(demoId, title, backend.port || 8766);
      }
    } else {
      await copyStaticDemo(demoId, demoDir);
    }
  }

  return demosPublic;
}
