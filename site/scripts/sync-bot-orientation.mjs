// Copies repo-root bot-orientation files into site/public/ for deployment.
// Also builds llms-full.txt (llms.txt + reviewing-for-agents) per llmstxt.org.
//
// Usage: node scripts/sync-bot-orientation.mjs [--check]
import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const publicDir = path.join(siteRoot, "public");

const checkMode = process.argv.includes("--check");

function sha256(text) {
  return createHash("sha256").update(text, "utf8").digest("hex");
}

async function readRepoFile(name) {
  return readFile(path.join(repoRoot, name), "utf8");
}

async function readPublicFile(name) {
  return readFile(path.join(publicDir, name), "utf8");
}

function buildLlmsFull(llms, reviewing) {
  const body = reviewing.replace(/^# Reviewing For Agents\s*\n+/, "");
  return `${llms.trim()}\n\n---\n\n# Reviewing For Agents\n\n${body.trim()}\n`;
}

async function writeOrCheck(name, content) {
  const dest = path.join(publicDir, name);
  if (checkMode) {
    let existing;
    try {
      existing = await readPublicFile(name);
    } catch {
      console.error(`sync-bot-orientation: missing ${dest} (run without --check)`);
      process.exit(1);
    }
    if (sha256(existing) !== sha256(content)) {
      console.error(`sync-bot-orientation: ${name} is out of date (run npm run sync:bot-orientation)`);
      process.exit(1);
    }
    return;
  }
  await writeFile(dest, content, "utf8");
}

async function main() {
  const llms = await readRepoFile("llms.txt");
  const reviewing = await readRepoFile("REVIEWING_FOR_AGENTS.md");
  const llmsFull = buildLlmsFull(llms, reviewing);

  await writeOrCheck("llms.txt", llms.endsWith("\n") ? llms : `${llms}\n`);
  await writeOrCheck(
    "reviewing-for-agents.md",
    reviewing.endsWith("\n") ? reviewing : `${reviewing}\n`
  );
  await writeOrCheck("llms-full.txt", llmsFull);

  if (!checkMode) {
    console.log(
      "sync-bot-orientation: wrote llms.txt, reviewing-for-agents.md, llms-full.txt to public/"
    );
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
