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
const experimentLedgersDir = path.join(siteRoot, "src", "content", "experiment-ledgers");

const REPO = "https://github.com/GunnarZarncke/towards-asi-alignment";
const SITE_ORIGIN = "https://towards-alignment.com";

function yamlString(value) {
  return JSON.stringify(value);
}

function repoUrl(relativePath) {
  if (!relativePath) return null;
  return `${REPO}/blob/main/${relativePath.replace(/^\/+/, "")}`;
}

function ledgerSitePath(lineId) {
  return `/experiments/ledgers/${lineId}/`;
}

function ledgerSiteUrl(lineId) {
  return `${SITE_ORIGIN}${ledgerSitePath(lineId)}`;
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

function enrichLine(line, ledgerLineIds) {
  const links = [];
  const ledgerOnSite = ledgerLineIds.has(line.id);
  if (line.readmePath) {
    links.push({ label: "README", url: repoUrl(line.readmePath) });
  }
  if (line.designPath) {
    links.push({ label: "Design", url: repoUrl(line.designPath) });
  }
  if (line.planPath) {
    links.push({ label: "Plan", url: repoUrl(line.planPath) });
  }
  if (ledgerOnSite) {
    links.push({ label: "Findings (site)", url: ledgerSiteUrl(line.id) });
    if (line.findingsPath) {
      links.push({ label: "Findings (GitHub)", url: repoUrl(line.findingsPath) });
    }
  } else if (line.findingsPath) {
    links.push({ label: "Findings", url: repoUrl(line.findingsPath) });
  } else if (line.findingsUrl) {
    links.push({ label: "Findings", url: line.findingsUrl });
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
    locationUrl: line.repoUrl ?? repoUrl(line.location?.replace(/^\.\.\//, "")),
    readmeUrl: repoUrl(line.readmePath),
    findingsUrlResolved: ledgerOnSite
      ? ledgerSiteUrl(line.id)
      : line.findingsUrl ?? repoUrl(line.findingsPath)
  };
}

async function syncLedgerPages(ledgers) {
  await rm(experimentLedgersDir, { recursive: true, force: true });
  await mkdir(experimentLedgersDir, { recursive: true });
  const publicLedgersDir = path.join(siteRoot, "public", "experiment-ledgers");
  await rm(publicLedgersDir, { recursive: true, force: true });
  await mkdir(publicLedgersDir, { recursive: true });

  for (const ledger of ledgers) {
    if (!ledger.path) continue;
    const sourceMd = path.join(repoRoot, ledger.path);
    const body = await readFile(sourceMd, "utf8");
    const trimmed = body.trim();
    const contents = [
      "---",
      `title: ${yamlString(ledger.label)}`,
      `lineId: ${yamlString(ledger.lineId)}`,
      `sourcePath: ${yamlString(ledger.path)}`,
      "---",
      "",
      trimmed,
      ""
    ].join("\n");
    await writeFile(path.join(experimentLedgersDir, `${ledger.lineId}.md`), contents, "utf8");
    await writeFile(path.join(publicLedgersDir, `${ledger.lineId}.md`), `${trimmed}\n`, "utf8");
  }
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

const ledgerLineIds = new Set(raw.ledgers.map((ledger) => ledger.lineId));

const lines = [...raw.lines]
  .sort((a, b) => a.order - b.order)
  .map((line) => enrichLine(line, ledgerLineIds));

const howToReadByLineId = new Map(raw.howToRead.map((entry) => [entry.lineId, entry]));

const howToRead = raw.howToRead.map((entry) => {
  const line = lines.find((item) => item.id === entry.lineId);
  return {
    ...entry,
    lineTitle: line?.title ?? entry.lineId
  };
});

await syncLedgerPages(raw.ledgers);

const ledgers = raw.ledgers.map((ledger) => ({
  ...ledger,
  sitePath: ledgerSitePath(ledger.lineId),
  siteUrl: ledgerSiteUrl(ledger.lineId),
  repoUrl: ledger.path ? repoUrl(ledger.path) : ledger.url ?? null,
  url: ledgerSiteUrl(ledger.lineId)
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
console.log(`Wrote ${raw.ledgers.length} experiment ledgers to src/content/experiment-ledgers/`);
