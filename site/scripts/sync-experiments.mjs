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
  if (line.findingsPath) {
    links.push({ label: "Findings", url: repoUrl(line.findingsPath) });
  } else if (line.findingsUrl) {
    links.push({ label: "Findings", url: line.findingsUrl });
  }
  if (line.repoUrl && !line.readmePath) {
    links.push({ label: "Repository", url: line.repoUrl });
  }

  return {
    ...line,
    links,
    locationUrl: line.repoUrl ?? repoUrl(line.location?.replace(/^\.\.\//, "")),
    readmeUrl: repoUrl(line.readmePath),
    findingsUrlResolved: line.findingsUrl ?? repoUrl(line.findingsPath)
  };
}

function experimentCardMarkdown(line, howToReadEntry) {
  const summary = firstSentence(line.role);
  const findings = line.headlineFindings ?? [];
  const bodyParts = [line.role.trim()];

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

const lines = [...raw.lines]
  .sort((a, b) => a.order - b.order)
  .map(enrichLine);

const howToReadByLineId = new Map(raw.howToRead.map((entry) => [entry.lineId, entry]));

const howToRead = raw.howToRead.map((entry) => {
  const line = lines.find((item) => item.id === entry.lineId);
  return {
    ...entry,
    lineTitle: line?.title ?? entry.lineId
  };
});

const ledgers = raw.ledgers.map((ledger) => ({
  ...ledger,
  url: ledger.path ? repoUrl(ledger.path) : ledger.url ?? null
}));

const payload = {
  claimStrength: raw.claimStrength.trim(),
  negativeResultsFirst: raw.negativeResultsFirst,
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
