#!/usr/bin/env node
/**
 * Export all Metaculus listing text for catalog markets 1–21 to Markdown (then pandoc → docx).
 * Run from repo root: node scripts/export_metaculus_questions.mjs
 */
import { readFile, writeFile, mkdir, access } from "node:fs/promises";
import { constants as fsConstants } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { stripComments } from "../site/scripts/lib/tex-convert.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..");
const require = createRequire(path.join(repoRoot, "site", "package.json"));
const yaml = require("js-yaml");
const sourcePath = path.join(repoRoot, "metadata", "predictions.yml");
const appendixPath = path.join(repoRoot, "appendices", "appP-bridge-predictions.tex");
const outMd = path.join(repoRoot, "drafts", "predictions", "metaculus-all-markets.md");
const outDocx = path.join(repoRoot, "drafts", "predictions", "metaculus-all-markets.docx");
const defaultClaimsRoot = path.join(repoRoot, "..", "ai-safety-claims");

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

/** Listing-template cutoff: ISO date + 23:59 UTC, plus Metaculus form datetime lines. */
function metaculusResolveByBlock(yamlMarket, texResolveByRaw) {
  let iso = yamlMarket?.resolveBy?.trim();
  if (!iso && texResolveByRaw) {
    const t = stripLatexInline(texResolveByRaw);
    const dmY = t.match(/(\d{1,2})\s+(\w+)\s+(\d{4})/);
    if (dmY) {
      const monthIdx = MONTHS.findIndex((m) => m.toLowerCase() === dmY[2].toLowerCase());
      if (monthIdx >= 0) {
        iso = `${dmY[3]}-${String(monthIdx + 1).padStart(2, "0")}-${String(dmY[1]).padStart(2, "0")}`;
      }
    }
  }
  const isoMatch = iso?.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!isoMatch) {
    const fallback = texResolveByRaw ? stripLatexInline(texResolveByRaw) : "(unknown cutoff)";
    return [fallback, ""];
  }
  const [, y, mo, d] = isoMatch;
  const human = `${Number(d)} ${MONTHS[Number(mo) - 1]} ${y}, 23:59 UTC`;
  const formTs = `${iso} 23:59:00`;
  return [
    `Question closes: ${iso}, 23:59 UTC (${human}).`,
    "Expected resolution: within 60 days after cutoff (registry snapshot tag).",
    "",
    "Metaculus form (UTC):",
    `- Open time: (set when listing)`,
    `- Closing time: ${formTs}`,
    `- Resolving time: ${formTs}`,
    `- CP reveal time: (optional)`,
    ""
  ];
}

const DEFAULT_REGISTRY_SITE = "https://ai-safety-claims.com/";

function claimsPageMarkdown(marketId, version, registrySite) {
  const root = String(registrySite || DEFAULT_REGISTRY_SITE).replace(/\/$/, "");
  return `[claims registry (contract v${version})](${root}/markets/${marketId}/v${version}/)`;
}

function expandClaimspage(tex, registrySite) {
  return tex.replace(/\\claimspage\{([^}]+)\}\{(\d+)\}/g, (_, market, version) =>
    claimsPageMarkdown(market, version, registrySite)
  );
}

function githubRepoPath(registryRepo) {
  return String(registryRepo || "https://github.com/aintelope/ai-safety-claims")
    .replace(/^https:\/\/github.com\//, "")
    .replace(/\/$/, "");
}

function addDaysIso(isoDate, days) {
  const m = isoDate?.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!m) return null;
  const dt = new Date(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])));
  dt.setUTCDate(dt.getUTCDate() + days);
  return dt.toISOString().slice(0, 10);
}

async function pathExists(filePath) {
  try {
    await access(filePath, fsConstants.R_OK);
    return true;
  } catch {
    return false;
  }
}

function claimsRootPath(catalog) {
  return catalog.claimsRepoPath || defaultClaimsRoot;
}

async function loadRegistryDoc(catalog) {
  const registryPath = path.join(claimsRootPath(catalog), "registry.yaml");
  if (!(await pathExists(registryPath))) return null;
  return yaml.load(await readFile(registryPath, "utf8"));
}

async function loadMetaculusListingRules(catalog) {
  const rulesPath = path.join(claimsRootPath(catalog), "shared-rules", "metaculus-listing-v1.yaml");
  if (!(await pathExists(rulesPath))) return null;
  return yaml.load(await readFile(rulesPath, "utf8"));
}

function fillListingTemplate(text, vars) {
  if (!text?.trim()) return "";
  let out = text.trim();
  for (const [key, value] of Object.entries(vars)) {
    out = out.replaceAll(`{${key}}`, value ?? "");
  }
  return out;
}

/** Listing-template snapshot / Zenodo / annulment bullets for registry markets. */
function registrySnapshotFinePrintMarkdown(yamlMarket, catalog) {
  const cutoff = yamlMarket?.resolveBy?.trim();
  if (!cutoff) return "";
  const id = yamlMarket.id;
  const v = yamlMarket.contractVersion;
  const snapshot = `snapshot-${cutoff}`;
  const repo = githubRepoPath(catalog.registryRepo);
  const annulBy = addDaysIso(cutoff, 90);
  const zenodoDoi = catalog.zenodoConceptDoi?.trim();
  const zenodoLine = zenodoDoi
    ? `If the tag is missing on GitHub, or was moved after creation, use the version titled \`${snapshot}\` of the Zenodo record [${zenodoDoi}](https://doi.org/${zenodoDoi.replace(/^https?:\/\/doi.org\//, "")}), which is deposited when the tag is created.`
    : `If the tag is missing on GitHub, or was moved after creation, use the version titled \`${snapshot}\` of the registry's Zenodo concept record (DOI listed in \`resolution-tags/${snapshot}.md\` on \`github.com/${repo}\` when deposited).`;
  return [
    `- Use git tag \`${snapshot}\` whenever it was created, if it exists by ${annulBy}, 23:59 UTC.`,
    `- ${zenodoLine}`,
    `- The question is annulled if, by ${annulBy}, 23:59 UTC, neither source has the file \`market-outcomes/${id}-v${v}.json\`, or the file is unreadable, names a different market or contract version, has \`contractStatus\` other than \`frozen\`, has \`resolutionSource\` other than \`true\`, or has an \`outcome\` value not among the options.`,
    `- OTHER means no qualifying attempt existed. It is not an annulment.`
  ].join("\n");
}

function registryFinePrintMarkdown(yamlMarket, catalog, listingRules, registryDoc) {
  if (!yamlMarket?.registryContractPublished || !yamlMarket.contractVersion) return "";
  if (!listingRules) return registrySnapshotFinePrintMarkdown(yamlMarket, catalog);

  const registrySite = String(catalog.registrySite || DEFAULT_REGISTRY_SITE).replace(/\/?$/, "/");
  const vars = {
    registrySite,
    marketId: yamlMarket.id,
    contractVersion: String(yamlMarket.contractVersion),
    host: registryDoc?.host ? String(registryDoc.host) : "(see registry.yaml at the snapshot tag)"
  };
  const prose = [
    fillListingTemplate(listingRules.registryHost, vars),
    fillListingTemplate(listingRules.companionSite, vars),
    fillListingTemplate(listingRules.qualificationNotHere, vars),
    fillListingTemplate(listingRules.hostTransfer, vars)
  ].filter(Boolean);
  if (registryDoc?.hostIndependent === false && listingRules.interimHost) {
    prose.push(fillListingTemplate(listingRules.interimHost, vars));
  }
  return [...prose, registrySnapshotFinePrintMarkdown(yamlMarket, catalog)].join("\n\n");
}

/** Listing-template resolution block for registry catalog markets (1–13, 15–18). */
function registryResolutionMarkdown(yamlMarket, catalog) {
  if (!yamlMarket?.registryContractPublished || !yamlMarket.contractVersion) return "";
  const registrySite = catalog.registrySite || DEFAULT_REGISTRY_SITE;
  const id = yamlMarket.id;
  const v = yamlMarket.contractVersion;
  const cutoff = yamlMarket.resolveBy;
  const snapshot = cutoff ? `snapshot-${cutoff}` : catalog.snapshotTag || "snapshot-0";
  const repo = githubRepoPath(catalog.registryRepo);
  const contractLink = claimsPageMarkdown(id, v, registrySite);
  return [
    `Frozen contract (numeric bars, qualification, freeze order): ${contractLink}.`,
    "",
    `This question resolves to the value of the \`outcome\` field in the file \`market-outcomes/${id}-v${v}.json\` at git tag \`${snapshot}\` of \`github.com/${repo}\`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.`,
    "",
    "YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version."
  ].join("\n");
}

function stripLatexInline(text) {
  return text
    .replace(/\\href\{([^}]+)\}\{([^}]+)\}/g, "[$2]($1)")
    .replace(/\\autocite\{[^}]+\}/g, "")
    .replace(/\\textcite\{[^}]+\}/g, "")
    .replace(/\\cite\{[^}]+\}/g, "")
    .replace(/\\(?:ref|eqref|autoref)\{[^}]+\}/g, "")
    .replace(/Chapter~\\ref\{[^}]+\}/g, "the relevant chapter")
    .replace(/Appendix~\\ref\{[^}]+\}/g, "Appendix H")
    .replace(/Section~\\ref\{[^}]+\}/g, "the relevant section")
    .replace(/Markets~(\d+(?:,~\d+| and~\d+)*)/g, (_, nums) =>
      nums.replace(/~/g, "").replace(/ and /g, ", ")
    )
    .replace(/Market~(\d+)/g, "Market $1")
    .replace(/\\emph\{([^}]*)\}/g, "$1")
    .replace(/\\textbf\{([^}]*)\}/g, "**$1**")
    .replace(/\\textit\{([^}]*)\}/g, "$1")
    .replace(/\\paragraph\{([^}]*)\}/g, "**$1**")
    .replace(/\\texttt\{([^}]*)\}/g, "$1")
    .replace(/\{(\[[^\]]+\])\}/g, "$1")
    .replace(/~/g, " ")
    .replace(/``/g, '"')
    .replace(/''/g, '"')
    .replace(/\\%/g, "%")
    .replace(/\\\$/g, "$")
    .replace(/\\,/g, " ")
    .replace(/\{,\}/g, ",")
    .replace(/---/g, "—")
    .replace(/\s+/g, " ")
    .trim();
}

function convertBasicLatexLists(text) {
  return text
    .replace(/\\begin\{itemize\}([\s\S]*?)\\end\{itemize\}/g, (_, items) => {
      const lines = [...items.matchAll(/\\item\s*([\s\S]*?)(?=\\item|$)/g)];
      return `${lines.map((match) => `- ${stripLatexInline(match[1])}`).join("\n")}\n`;
    })
    .replace(/\\begin\{enumerate\}([\s\S]*?)\\end\{enumerate\}/g, (_, items) => {
      const lines = [...items.matchAll(/\\item\s*([\s\S]*?)(?=\\item|$)/g)];
      return `${lines
        .map((match, index) => `${index + 1}. ${stripLatexInline(match[1])}`)
        .join("\n")}\n`;
    })
    .replace(/\\begin\{description\}([\s\S]*?)\\end\{description\}/g, (_, body) => {
      const items = [...body.matchAll(/\\item\[(\{[\s\S]*?\})\]\s*([\s\S]*?)(?=\\item\[|$)/g)];
      return `${items
        .map((match) => `- **${stripLatexInline(match[1])}**\n\n  ${stripLatexInline(match[2])}`)
        .join("\n\n")}\n`;
    });
}

function formatLatexBlock(text) {
  if (!text.trim()) return "";
  const withLists = convertBasicLatexLists(text);
  return withLists
    .split(/\n\s*\n/)
    .flatMap((chunk) => {
      if (chunk.trim().startsWith("- ") || chunk.trim().match(/^\d+\./)) {
        return [chunk.trim()];
      }
      return chunk
        .split(/\n(?=[A-Z"(\[`])/)
        .map((para) => stripLatexInline(para))
        .filter(Boolean);
    })
    .join("\n\n");
}

function extractContractEnv(sectionBody, envName) {
  const match = sectionBody.match(
    new RegExp(`\\\\begin\\{${envName}\\}([\\s\\S]*?)\\\\end\\{${envName}\\}`)
  );
  return match?.[1]?.trim() ?? "";
}

function extractMarketSections(tex) {
  const cleaned = stripComments(tex);
  const sections = new Map();
  const re =
    /\\subsection\{Market (\d+)\. ([^}]+)\}\s*\\label\{sec:appp-m(\d+)\}([\s\S]*?)(?=\\subsection\{Market |\\section\{)/g;
  let match;
  while ((match = re.exec(cleaned)) !== null) {
    sections.set(Number(match[1]), {
      number: Number(match[1]),
      title: match[2].trim(),
      body: match[4]
    });
  }
  return sections;
}

function extractBoxFields(boxInner) {
  const resolveBy = boxInner.match(/\\textbf\{Resolve by\.\}\s*([\s\S]*?)(?=\\textbf\{)/)?.[1];
  const question = boxInner.match(
    /\\textbf\{Question\.\}\s*([\s\S]*?)(?=\\textbf\{Choices\.\}|\\textbf\{Parameters\.\}|$)/
  )?.[1];
  const parameters = boxInner.match(
    /\\textbf\{Parameters\.\}\s*([\s\S]*?)(?=\\textbf\{Choices\.\}|$)/
  )?.[1];
  const choices = boxInner.match(/\\textbf\{Choices\.\}\s*([\s\S]*?)$/)?.[1];
  return {
    resolveBy: formatLatexBlock(resolveBy ?? ""),
    question: formatLatexBlock(question ?? ""),
    parameters: formatLatexBlock(parameters ?? ""),
    choices: formatLatexBlock(choices ?? "")
  };
}

function extractBoxTitle(sectionBody) {
  const match = sectionBody.match(/\\begin\{predictionbox\}\[([^\]]*)\]/);
  return match?.[1]?.trim() ?? "";
}

function extractBoxInner(sectionBody) {
  const match = sectionBody.match(
    /\\begin\{predictionbox\}(?:\[[^\]]*\])?([\s\S]*?)\\end\{predictionbox\}/
  );
  return match?.[1]?.trim() ?? "";
}

function metaculusShortTitleForExport(market, sectionBody) {
  const fromBox = extractBoxTitle(sectionBody);
  if (fromBox) return fromBox;
  return (market?.metaculusShortTitle || "").trim();
}

function marketMarkdown(number, title, yamlMarket, sectionBody, catalog, listingRules, registryDoc) {
  const registrySite = catalog.registrySite || DEFAULT_REGISTRY_SITE;
  const boxInner = extractBoxInner(sectionBody);
  const fields = extractBoxFields(boxInner);
  const background = formatLatexBlock(extractContractEnv(sectionBody, "predictionbackground"));
  const resolutionFromTex = formatLatexBlock(extractContractEnv(sectionBody, "predictionresolution"));
  const resolutionRegistry = registryResolutionMarkdown(yamlMarket, catalog);
  const resolution = resolutionRegistry
    ? resolutionRegistry
    : expandClaimspage(resolutionFromTex, registrySite);
  const fineprintFromTex = formatLatexBlock(extractContractEnv(sectionBody, "predictionfineprint"));
  const fineprintRegistry = resolutionRegistry
    ? registryFinePrintMarkdown(yamlMarket, catalog, listingRules, registryDoc)
    : "";
  const fineprint = fineprintFromTex || fineprintRegistry;
  const shortTitle = metaculusShortTitleForExport(yamlMarket, sectionBody);
  const longTitle = yamlMarket?.longTitle || fields.question;
  const choices =
    fields.choices ||
    (number === 20
      ? "YES and OTHER as defined in Appendix H reading rules."
      : "YES, NO, and OTHER as defined in Appendix H reading rules.");

  const lines = [
    `## Market ${number}. ${title}`,
    "",
    "### Short title (Metaculus)",
    "",
    shortTitle,
    "",
    "### Long title (Metaculus)",
    "",
    longTitle,
    ""
  ];

  if (fields.resolveBy || yamlMarket?.resolveBy) {
    lines.push("### Resolve by", "", ...metaculusResolveByBlock(yamlMarket, fields.resolveBy));
  }
  if (fields.parameters) {
    lines.push("### Parameters", "", fields.parameters, "");
  }
  lines.push("### Choices", "", choices, "");
  if (background) {
    lines.push("### Background information", "", background, "");
  }
  if (resolution) {
    lines.push("### Resolution criteria", "", resolution, "");
  }
  if (fineprint) {
    lines.push("### Fine print", "", fineprint, "");
  }
  lines.push("---", "");
  return lines.join("\n");
}

const raw = yaml.load(await readFile(sourcePath, "utf8"));
const appendixTex = await readFile(appendixPath, "utf8");
const sectionByNumber = extractMarketSections(appendixTex);
const yamlByNumber = new Map((raw.markets ?? []).map((m) => [m.number, m]));
const listingRules = await loadMetaculusListingRules(raw);
const registryDoc = await loadRegistryDoc(raw);

const parts = [
  "# Metaculus listing packet — AI alignment markets (Appendix H)",
  "",
  "Generated from `appendices/appP-bridge-predictions.tex`, `metadata/predictions.yml`, and",
  "`ai-safety-claims/shared-rules/metaculus-listing-v1.yaml`.",
  "",
  "Markets 1–13 and 15–18 resolve on the claims registry (git snapshot). **Fine print** for those markets",
  "covers host, repo, companion-site fallback, and annulment — not Common rules or adversarial budget",
  "(those live on [ai-safety-claims.com](https://ai-safety-claims.com/) and in the frozen contract files).",
  "Markets 19–21 keep appendix `predictionfineprint` until Phase 4.",
  "",
  "---",
  ""
];

for (const number of [...sectionByNumber.keys()].sort((a, b) => a - b)) {
  const section = sectionByNumber.get(number);
  parts.push(
    marketMarkdown(
      number,
      section.title,
      yamlByNumber.get(number),
      section.body,
      raw,
      listingRules,
      registryDoc
    )
  );
}

await mkdir(path.dirname(outMd), { recursive: true });
await writeFile(outMd, `${parts.join("\n")}\n`, "utf8");
console.log(`Wrote ${path.relative(repoRoot, outMd)}`);
