// Generates the release-vX-Y-Z.md cards and the releases-updates hub card from
// RELEASE_NOTES.md (the canonical long-form changelog). No hand-edited release
// cards — add a new `## vX.Y.Z — YYYY-MM-DD — Title` section to RELEASE_NOTES.md
// and re-run this script.
//
// Usage: node scripts/sync-releases.mjs [--check]
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readFile } from "node:fs/promises";
import { repoPaths, writeCard } from "./lib/concepts-yaml.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const { repoRoot, cardsDir } = repoPaths(siteRoot);

const REPO_BLOB_URL = "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/RELEASE_NOTES.md";
const REPO_TAGS_URL = "https://github.com/GunnarZarncke/towards-asi-alignment/releases";
const HUB_SLUG = "releases-updates";

// Mirrors GitHub's markdown heading-anchor algorithm closely enough for the
// plain ASCII headings used in RELEASE_NOTES.md: lowercase, drop punctuation
// outside [a-z0-9 -], then turn every remaining space into a hyphen.
function githubAnchor(heading) {
  return heading
    .toLowerCase()
    .replace(/[^a-z0-9 -]/g, "")
    .replace(/ /g, "-");
}

function yamlScalar(value) {
  return JSON.stringify(value);
}

function versionSlug(version) {
  return `release-v${version.replace(/\./g, "-")}`;
}

function parseReleaseNotes(text) {
  const firstHeadingIndex = text.search(/\n## v/);
  const preamble = text.slice(0, firstHeadingIndex);
  const preambleBody = preamble
    .replace(/^# Release Notes\s*\n/, "")
    .replace(/^\*[^*]+\*\s*\n/, "")
    .replace(/\n---\s*$/, "")
    .trim();

  const sectionRe = /\n## (v(\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2}) — ([^\n]+))\n([\s\S]*?)(?=\n## v|\n?$)/g;
  const releases = [];
  let match;
  while ((match = sectionRe.exec(text)) !== null) {
    const [, heading, version, releasedAt, titleSuffix, rawBody] = match;
    const body = rawBody.replace(/\n---\s*$/, "").trim();
    releases.push({ heading, version, releasedAt, titleSuffix: titleSuffix.trim(), body });
  }
  return { preambleBody, releases };
}

function firstParagraph(body) {
  const paragraphs = body.split(/\n\s*\n/);
  // Skip a leading "Commit: ... · Tag: ..." metadata line if present; the
  // descriptive summary is the next paragraph.
  const para = paragraphs.find((p) => !/^(Commit|Tag):/.test(p.trim())) ?? paragraphs[0] ?? "";
  return para.replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
}

function publicFieldsForRelease(release, versionTag) {
  return {
    title: `${versionTag} — ${release.titleSuffix}`,
    type: "release",
    status: "reviewed",
    releasedAt: release.releasedAt,
    version: release.version,
    summary: firstParagraph(release.body),
    decision: `Use ${versionTag} (or later) when citing or linking this section of the manuscript externally.`
  };
}

function renderReleaseCard(release, relatedSlugs) {
  const versionTag = `v${release.version}`;
  const fields = publicFieldsForRelease(release, versionTag);
  const anchor = githubAnchor(release.heading);
  const lines = ["---"];
  for (const key of ["title", "type", "status", "releasedAt", "version", "summary", "decision"]) {
    lines.push(`${key}: ${yamlScalar(fields[key])}`);
  }
  lines.push(`related: [${relatedSlugs.map(yamlScalar).join(", ")}]`);
  lines.push("external:");
  lines.push(`  - label: "Full release notes"`);
  lines.push(`    url: ${yamlScalar(`${REPO_BLOB_URL}#${anchor}`)}`);
  lines.push(`  - label: ${yamlScalar(`Tag ${versionTag}`)}`);
  lines.push(`    url: ${yamlScalar(`${REPO_TAGS_URL}/tag/${versionTag}`)}`);
  lines.push("---", "");
  lines.push(`Released **${release.releasedAt}**.`, "");
  lines.push(release.body);
  return lines.join("\n") + "\n";
}

function renderHubCard(preambleBody, versionSlugs) {
  const fields = {
    title: "Releases & updates",
    type: "release",
    status: "reviewed",
    summary:
      "Versioned milestones for the manuscript and companion site — newest first. Each release card compresses what changed; the full changelog lives in RELEASE_NOTES.md.",
    decision:
      "When citing or linking the book externally, prefer a tagged release so chapter numbers and appendix letters stay stable."
  };
  const lines = ["---"];
  for (const key of ["title", "type", "status", "summary", "decision"]) {
    lines.push(`${key}: ${yamlScalar(fields[key])}`);
  }
  lines.push(`related: [${versionSlugs.map(yamlScalar).join(", ")}]`);
  lines.push("external:");
  lines.push(`  - label: "Full release notes (GitHub)"`);
  lines.push(`    url: ${yamlScalar(REPO_BLOB_URL)}`);
  lines.push(`  - label: "GitHub releases / tags"`);
  lines.push(`    url: ${yamlScalar(REPO_TAGS_URL)}`);
  lines.push("---", "");
  lines.push(
    "This companion site tracks **manuscript releases** as short cards so readers can see what changed without opening the PDF changelog.",
    "",
    "**How versions work**",
    ""
  );
  lines.push(preambleBody, "");
  lines.push(
    `Browse the [Updates page](/updates/) for the newest release first, or open a version card below. The canonical long-form changelog remains [\`RELEASE_NOTES.md\`](${REPO_BLOB_URL}) in the repository.`
  );
  return lines.join("\n") + "\n";
}

async function main() {
  const check = process.argv.includes("--check");
  const text = await readFile(path.join(repoRoot, "RELEASE_NOTES.md"), "utf8");
  const { preambleBody, releases } = parseReleaseNotes(text);
  releases.sort((a, b) => b.releasedAt.localeCompare(a.releasedAt));

  const versionSlugs = releases.map((r) => versionSlug(r.version));
  const mismatches = [];

  for (let i = 0; i < releases.length; i++) {
    const slug = versionSlugs[i];
    const related = [HUB_SLUG, ...versionSlugs.filter((s) => s !== slug)];
    const contents = renderReleaseCard(releases[i], related);
    const result = await writeCard(cardsDir, slug, contents, { check });
    if (!result.matches) mismatches.push(result.filePath);
  }

  const hubContents = renderHubCard(preambleBody, versionSlugs);
  const hubResult = await writeCard(cardsDir, HUB_SLUG, hubContents, { check });
  if (!hubResult.matches) mismatches.push(hubResult.filePath);

  if (check && mismatches.length > 0) {
    console.error(`sync-releases --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-releases: wrote ${releases.length} version cards + hub (${check ? "check mode, all up to date" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
