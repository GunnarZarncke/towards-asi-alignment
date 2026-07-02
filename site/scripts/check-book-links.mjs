#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");

const result = spawnSync("node", ["scripts/sync-chapters.mjs"], {
  cwd: siteRoot,
  stdio: "inherit"
});

process.exit(result.status ?? 1);
