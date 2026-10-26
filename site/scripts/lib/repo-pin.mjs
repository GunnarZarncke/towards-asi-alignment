/** GitHub blob base pinned to the commit being built, so line anchors keep
 * pointing at the code they were computed from. Outputs that use it are
 * generated at build time (gitignored), so the SHA never churns tracked files.
 * Links to an unpushed commit resolve once it is pushed. */

import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = "https://github.com/GunnarZarncke/towards-asi-alignment";
const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");

let cached = null;

function git(args) {
  return execFileSync("git", args, { cwd: repoRoot, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
}

/** `https://github.com/…/blob/<sha>`; falls back to `main` without git. */
export function repoBlobBase() {
  if (cached) return cached;
  let ref = process.env.GITHUB_SHA || "";
  try {
    if (!ref) ref = git(["rev-parse", "HEAD"]);
    if (git(["status", "--porcelain", "--", "formal/AlignmentProofSpine"])) {
      console.warn("repo-pin: formal/AlignmentProofSpine has uncommitted changes; Lean line anchors follow the working tree, not the pinned commit. Re-sync after committing.");
    }
  } catch {
    console.warn("repo-pin: git unavailable; Lean links use blob/main");
  }
  cached = `${REPO}/blob/${ref || "main"}`;
  return cached;
}
