import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import { cardPublicPath } from "./lib/card-urls.mjs";

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

function repoTreeUrl(relativePath) {
  if (!relativePath) return null;
  return `${REPO}/tree/main/${relativePath.replace(/^\/+|\/$/g, "")}`;
}

function githubUrlForExperimentPath(relativePath) {
  const clean = relativePath.replace(/[.,;:)\]'"]+$/, "").replace(/\/+$/, "");
  const lastSegment = clean.split("/").pop() ?? "";
  const looksLikeFile = /\.\w+$/.test(lastSegment);
  return looksLikeFile ? repoUrl(clean) : repoTreeUrl(clean);
}

function linkLabelForExperimentPath(relativePath) {
  const clean = relativePath.replace(/[.,;:)\]'"]+$/, "");
  const parts = clean.split("/");
  return parts[parts.length - 1] || clean;
}

/** Turn bare `experiments/...` paths in card copy into GitHub links at sync time. */
function linkifyExperimentPaths(text) {
  if (!text?.trim()) return text;

  let out = text.replace(
    /(?<!\[)`(experiments\/[^`\n]+)`(?!\()/g,
    (_, path) => `[${linkLabelForExperimentPath(path)}](${githubUrlForExperimentPath(path)})`
  );

  out = out.replace(
    /`?python3 (experiments\/[\w./-]+(?:\.\w+)?)`?/g,
    (_, path) => `[${linkLabelForExperimentPath(path)}](${githubUrlForExperimentPath(path)})`
  );

  out = out.replace(
    /(?<![\[`(:/\w-])(experiments\/[\w./-]+(?:\.\w+)?)/g,
    (match, path, offset, whole) => {
      const before = whole.slice(0, offset);
      const openLink = before.lastIndexOf("](");
      const closeLink = before.lastIndexOf(")");
      if (openLink > closeLink) return match;
      if (/https?:\/\/[^\s]*$/.test(before)) return match;

      const trailing = match.slice(path.length);
      const punct = trailing.match(/^[.,;:]+/)?.[0] ?? "";
      return `[${linkLabelForExperimentPath(path)}](${githubUrlForExperimentPath(path)})${punct}`;
    }
  );

  return out;
}

const LINKIFY_LINE_FIELDS = [
  "summary",
  "role",
  "witnesses",
  "host",
  "setup",
  "analysis",
  "numbers",
  "outcome"
];

function linkifyLineFields(line) {
  const out = { ...line };
  for (const field of LINKIFY_LINE_FIELDS) {
    if (typeof out[field] === "string") {
      out[field] = linkifyExperimentPaths(out[field]);
    }
  }
  if (Array.isArray(out.headlineFindings)) {
    out.headlineFindings = out.headlineFindings.map((entry) => linkifyExperimentPaths(entry));
  }
  return out;
}

function sourceUrlForLine(line) {
  if (line.repoUrl) return line.repoUrl;
  const location = line.location?.replace(/^\.\.\//, "") ?? "";
  if (/\.(py|json|lean|md)$/i.test(location)) return repoUrl(location);
  if (location.startsWith("experiments/") && location.endsWith(".md")) {
    return repoUrl(location);
  }
  if (location.startsWith("experiments/")) {
    return repoTreeUrl(location);
  }
  if (line.readmePath) return repoUrl(line.readmePath);
  if (line.planPath) return repoUrl(line.planPath);
  return null;
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
  return cardPublicPath({ id: `experiments/${lineId}`, type: "experiment" });
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
// Source and results are first-class fields for the card chrome; `links` are extras.
function enrichLine(line) {
  const kind = line.kind ?? "sim";
  const sourceUrl = sourceUrlForLine(line);
  const findingsUrlResolved = line.findingsUrl ?? repoUrl(line.findingsPath);
  const links = [];
  if (line.designPath) {
    links.push({ label: "Design", url: repoUrl(line.designPath) });
  }
  if (line.planPath && sourceUrl !== repoUrl(line.planPath)) {
    links.push({ label: "Plan", url: repoUrl(line.planPath) });
  }
  if (line.readmePath && sourceUrl !== repoUrl(line.readmePath) && sourceUrl !== line.repoUrl) {
    links.push({ label: "README", url: repoUrl(line.readmePath) });
  }
  if (line.leakProofPath) {
    links.push({ label: "Lean leak-proof", url: repoUrl(line.leakProofPath) });
  }

  return {
    ...line,
    kind,
    summary: line.summary?.trim() ?? line.summary,
    links,
    cardPath: experimentCardPath(line.id),
    cardUrl: experimentCardUrl(line.id),
    sourceUrl,
    findingsSitePath: findingsSitePath(line.id),
    findingsSiteUrl: findingsSiteUrl(line.id),
    locationUrl: sourceUrl,
    readmeUrl: repoUrl(line.readmePath),
    findingsUrlResolved
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

function relatedForKind(kind) {
  const overviewId =
    kind === "external" ? "experiments/external-tests" : kind === "witness" ? "experiments/witness-tests" : "experiments/simulations";
  const related = [overviewId, "experiment-methodology", "negative-results"];
  if (kind === "external") related.push("et-external-transfer");
  return related;
}

function formatRelatedYaml(ids) {
  return ["related:", ...ids.map((id) => `  - ${yamlString(id)}`)].join("\n");
}

function labeledSection(label, text) {
  if (!text?.trim()) return [];
  return ["", `**${label}.**`, "", text.trim()];
}

function experimentCardMarkdown(line, howToReadEntry) {
  const summary = (line.summary ?? firstSentence(line.role)).trim().replace(/\s+/g, " ");
  const bodyParts = [
    bodyWithoutDuplicateSummary(line.role, summary),
    ...labeledSection("Witnesses", line.witnesses),
    ...labeledSection("Host", line.host),
    ...labeledSection("Setup", line.setup),
    ...labeledSection("Analysis", line.analysis)
  ];

  const firstFinding = (line.headlineFindings ?? [])[0]?.trim();
  if (firstFinding) {
    const findingText = `${firstFinding} [Full results](${findingsSitePath(line.id)})`;
    bodyParts.push(...labeledSection("Finding", findingText));
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
    `experimentKind: ${yamlString(line.kind)}`,
    formatRelatedYaml(relatedForKind(line.kind)),
    formatExternalLinksYaml(line.links),
    "---",
    "",
    ...bodyParts
  ].join("\n");
}

function overviewCardMarkdown(kindId, kind, lines) {
  const related =
    kindId === "external"
      ? ["experiment-methodology", "negative-results", "et-external-transfer"]
      : ["experiment-methodology", "negative-results"];
  const list = lines.map((line) => {
    const blurb = (line.summary ?? firstSentence(line.role)).trim().replace(/\s+/g, " ");
    return `- [${line.title}](${line.cardPath}) — ${blurb}`;
  });
  const extraLinks = [
    { label: "Experiments hub", url: `${SITE_ORIGIN}/experiments/` },
    { label: "Narrative on GitHub", url: repoUrl("docs/EXPERIMENTS.md") }
  ];
  return [
    "---",
    `title: ${yamlString(kind.title)}`,
    `type: "experiment"`,
    `status: "framework"`,
    `summary: ${yamlString(kind.blurb.trim().replace(/\s+/g, " "))}`,
    "experimentOverview: true",
    `experimentKind: ${yamlString(kindId)}`,
    formatRelatedYaml(related),
    formatExternalLinksYaml(extraLinks),
    "---",
    "",
    linkifyExperimentPaths(kind.overview.trim()),
    "",
    "## Experiments in this class",
    "",
    ...list,
    ""
  ].join("\n");
}

const source = await readFile(sourcePath, "utf8");
const raw = yaml.load(source);
const witnessTestsPath = path.join(repoRoot, "metadata", "experiments-witness-tests.yml");
const witnessTests = yaml.load(await readFile(witnessTestsPath, "utf8"));
raw.lines = [...raw.lines, ...(witnessTests.lines ?? [])];

const lines = await Promise.all(
  [...raw.lines]
    .sort((a, b) => a.order - b.order)
    .map(async (line) => {
      const enriched = linkifyLineFields(enrichLine(line));
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
  const kindTitle = Object.values(raw.kinds).find((k) => k.cardId === entry.lineId)?.title;
  return {
    ...entry,
    text: entry.text ? linkifyExperimentPaths(entry.text) : entry.text,
    lineTitle: line?.title ?? kindTitle ?? entry.lineId
  };
});

// Negative-results ledgers: curated key findings on-site, full record on GitHub.
const ledgers = await Promise.all(
  raw.ledgers.map(async (ledger) => ({
    ...ledger,
    overviewCardId: ledger.overviewCardId ?? ledger.lineId,
    headlineFindings: ledger.path ? await extractKeyFindings(ledger.path) : [],
    findingsSitePath: findingsSitePath(ledger.lineId),
    findingsSiteUrl: findingsSiteUrl(ledger.lineId),
    repoUrl: ledger.path ? repoUrl(ledger.path) : ledger.url ?? null
  }))
);

const KIND_ORDER = ["sim", "external", "witness"];

const kinds = Object.fromEntries(
  KIND_ORDER.map((kindId) => {
    const kind = raw.kinds[kindId];
    const cardId = kind.cardId;
    return [
      kindId,
      {
        ...kind,
        cardId,
        cardPath: experimentCardPath(cardId),
        cardUrl: experimentCardUrl(cardId)
      }
    ];
  })
);

const payload = {
  claimStrength: raw.claimStrength.trim(),
  purpose: raw.purpose.trim(),
  negativeResultsFirst: raw.negativeResultsFirst,
  kinds,
  negativeResultsCardPath: cardPublicPath({ id: "negative-results", type: "concept" }),
  negativeResultsCardUrl: `${SITE_ORIGIN}${cardPublicPath({ id: "negative-results", type: "concept" })}`,
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

for (const kindId of KIND_ORDER) {
  const kind = kinds[kindId];
  const classLines = lines.filter((line) => line.kind === kindId);
  const cardPath = path.join(experimentCardsDir, `${kind.cardId}.md`);
  await writeFile(cardPath, overviewCardMarkdown(kindId, kind, classLines), "utf8");
}

console.log(`Wrote ${path.relative(siteRoot, outputPath)} from metadata/experiments.yml`);
console.log(
  `Wrote ${lines.length} line cards and ${KIND_ORDER.length} overview cards to src/content/cards/experiments/`
);
