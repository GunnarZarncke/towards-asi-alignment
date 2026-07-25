import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const sourcePath = path.join(repoRoot, "metadata", "experiments.yml");
const outputDir = path.join(siteRoot, "src", "data");
const outputPath = path.join(outputDir, "experiments.json");
const experimentCardsDir = path.join(siteRoot, "src", "content", "cards", "experiments");

const REPO = "https://github.com/GunnarZarncke/towards-asi-alignment";
const SITE_ORIGIN = "https://towards-alignment.com";

function yamlString(value) {
  return JSON.stringify(value);
}

function repoUrl(relativePath) {
  if (!relativePath) return null;
  return `${REPO}/blob/main/${relativePath.replace(/^\/+/, "")}`;
}

function firstSentence(text) {
  const trimmed = text.trim().replace(/\s+/g, " ");
  const match = trimmed.match(/^[^.!?]+[.!?]/);
  return match ? match[0].trim() : trimmed.slice(0, 220);
}

function formatExternalLinksYaml(links) {
  if (links.length === 0) return "external: []";
  return [
    "external:",
    ...links.map(
      (link) =>
        `  - label: ${yamlString(link.label)}\n    url: ${yamlString(link.url)}`
    )
  ].join("\n");
}

// Site findings are auto-extracted from **Key finding:** paragraphs in the
// line's own findings ledger (FINDINGS.md / NEGATIVE_RESULTS.md), so the full
// terse/bug-fix history stays on GitHub and only curated, readable summaries
// reach the site. Tag one entry per site bullet (usually the last entry in a
// related sequence) with a paragraph starting "**Key finding:** ...". Lines
// with no tagged paragraphs fall back to their `headlineFindings:` array in
// metadata/experiments.yml (manual, for lines not yet retrofitted).
async function extractKeyFindings(findingsPath) {
  if (!findingsPath) return [];
  let text;
  try {
    text = await readFile(path.join(repoRoot, findingsPath), "utf8");
  } catch {
    return [];
  }
  const matches = [...text.matchAll(/^[\t ]*\*\*Key finding:\*\*\s*([^\n]+(?:\n(?!\n)[^\n]+)*)/gm)];
  return matches.map((m) => m[1].replace(/\s+/g, " ").trim());
}

function experimentCardPath(lineId) {
  return `/cards/experiments/${lineId}/`;
}

function experimentCardUrl(lineId) {
  return `${SITE_ORIGIN}${experimentCardPath(lineId)}`;
}

function findingsSitePath(lineId) {
  return `/experiments/findings/${lineId}/`;
}

function findingsSiteUrl(lineId) {
  return `${SITE_ORIGIN}${findingsSitePath(lineId)}`;
}

// Site shows curated key findings; GitHub holds the full terse ledger.
function enrichLine(line) {
  const links = [];
  if (line.readmePath) {
    links.push({ label: "README", url: repoUrl(line.readmePath) });
  }
  if (line.designPath) {
    links.push({ label: "Design", url: repoUrl(line.designPath) });
  }
  if (line.planPath) {
    links.push({ label: "Plan", url: repoUrl(line.planPath) });
  }
  if (line.findingsPath || line.findingsUrl) {
    links.push({ label: "Key findings", url: findingsSiteUrl(line.id) });
    if (line.findingsPath) {
      links.push({ label: "Full ledger (GitHub)", url: repoUrl(line.findingsPath) });
    } else if (line.findingsUrl) {
      links.push({ label: "Full ledger (GitHub)", url: line.findingsUrl });
    }
  }
  if (line.leakProofPath) {
    links.push({ label: "Lean leak-proof", url: repoUrl(line.leakProofPath) });
  }
  if (line.repoUrl && !line.readmePath) {
    links.push({ label: "Repository", url: line.repoUrl });
  }

  return {
    ...line,
    links,
    cardPath: experimentCardPath(line.id),
    cardUrl: experimentCardUrl(line.id),
    findingsSitePath: findingsSitePath(line.id),
    findingsSiteUrl: findingsSiteUrl(line.id),
    locationUrl: line.repoUrl ?? repoUrl(line.location?.replace(/^\.\.\//, "")),
    readmeUrl: repoUrl(line.readmePath),
    findingsUrlResolved: line.findingsUrl ?? repoUrl(line.findingsPath)
  };
}

function bodyWithoutDuplicateSummary(role, summary) {
  const trimmedRole = role.trim();
  if (trimmedRole.startsWith(summary)) {
    const rest = trimmedRole.slice(summary.length).trim();
    return rest.length > 0 ? rest : trimmedRole;
  }
  return trimmedRole;
}

function experimentCardMarkdown(line, howToReadEntry) {
  const summary = firstSentence(line.role);
  const findings = line.headlineFindings ?? [];
  const bodyParts = [bodyWithoutDuplicateSummary(line.role, summary)];

  if (findings.length > 0) {
    bodyParts.push("", "## Headline findings", "", ...findings.map((item) => `- ${item}`));
  }

  if (howToReadEntry?.text) {
    bodyParts.push("", "## How to read", "", howToReadEntry.text.trim());
  }

  bodyParts.push("");

  return [
    "---",
    `title: ${yamlString(line.title)}`,
    `type: "experiment"`,
    `status: "open"`,
    `summary: ${yamlString(summary)}`,
    `experimentLineId: ${yamlString(line.id)}`,
    "related: []",
    formatExternalLinksYaml(line.links),
    "---",
    "",
    ...bodyParts
  ].join("\n");
}

const source = await readFile(sourcePath, "utf8");
const raw = yaml.load(source);

const lines = await Promise.all(
  [...raw.lines]
    .sort((a, b) => a.order - b.order)
    .map(async (line) => {
      const enriched = enrichLine(line);
      const keyFindings = await extractKeyFindings(line.findingsPath);
      return {
        ...enriched,
        headlineFindings: keyFindings.length > 0 ? keyFindings : enriched.headlineFindings
      };
    })
);

const howToReadByLineId = new Map(raw.howToRead.map((entry) => [entry.lineId, entry]));

const howToRead = raw.howToRead.map((entry) => {
  const line = lines.find((item) => item.id === entry.lineId);
  return {
    ...entry,
    lineTitle: line?.title ?? entry.lineId
  };
});

// Negative-results ledgers: curated key findings on-site, full record on GitHub.
const ledgers = raw.ledgers.map((ledger) => ({
  ...ledger,
  findingsSitePath: findingsSitePath(ledger.lineId),
  findingsSiteUrl: findingsSiteUrl(ledger.lineId),
  repoUrl: ledger.path ? repoUrl(ledger.path) : ledger.url ?? null
}));

const payload = {
  claimStrength: raw.claimStrength.trim(),
  negativeResultsFirst: raw.negativeResultsFirst,
  negativeResultsCardPath: "/cards/negative-results/",
  negativeResultsCardUrl: `${SITE_ORIGIN}/cards/negative-results/`,
  canonicalDocPath: raw.canonicalDoc,
  canonicalDocUrl: repoUrl(raw.canonicalDoc),
  openTasksUrl: repoUrl(raw.openTasksPath),
  ledgers,
  lines,
  howToRead,
  coverageColumns: raw.coverageColumns,
  coverageFeatures: raw.coverageFeatures
};

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, JSON.stringify(payload, null, 2) + "\n");

await rm(experimentCardsDir, { recursive: true, force: true });
await mkdir(experimentCardsDir, { recursive: true });

for (const line of lines) {
  const cardPath = path.join(experimentCardsDir, `${line.id}.md`);
  await writeFile(
    cardPath,
    experimentCardMarkdown(line, howToReadByLineId.get(line.id)),
    "utf8"
  );
}

console.log(`Wrote ${path.relative(siteRoot, outputPath)} from metadata/experiments.yml`);
console.log(`Wrote ${lines.length} experiment cards to src/content/cards/experiments/`);
