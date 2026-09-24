import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import { stripComments } from "./lib/tex-convert.mjs";
import { bookFullPublicHref, cardPublicPath } from "./lib/card-urls.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const sourcePath = path.join(repoRoot, "metadata", "predictions.yml");
const appendixPath = path.join(repoRoot, "appendices", "appP-bridge-predictions.tex");
const outputDir = path.join(siteRoot, "src", "data");
const outputPath = path.join(outputDir, "predictions.json");
const predictionCardsDir = path.join(siteRoot, "src", "content", "cards", "predictions");

const REPO = "https://github.com/GunnarZarncke/towards-asi-alignment";
const APPENDIX_H_FULL = bookFullPublicHref("", "appP");
const FUNDING_CARD = "/cards/funding/prediction-evaluation-program/";

function yamlString(value) {
  return JSON.stringify(value ?? "");
}

function formatRelatedYaml(related) {
  if (!related?.length) return "related: []";
  return `related:\n${related.map((id) => `  - ${yamlString(id)}`).join("\n")}`;
}

function formatExternalYaml(links) {
  if (!links?.length) return "external: []";
  return [
    "external:",
    ...links.map(
      (link) => `  - label: ${yamlString(link.label)}\n    url: ${yamlString(link.url)}`
    )
  ].join("\n");
}

function stripLatexInline(text) {
  return text
    .replace(/\\autocite\{[^}]+\}/g, "")
    .replace(/\\textcite\{[^}]+\}/g, "")
    .replace(/\\cite\{[^}]+\}/g, "")
    .replace(/\\emph\{([^}]*)\}/g, "$1")
    .replace(/\\textbf\{([^}]*)\}/g, "**$1**")
    .replace(/\\textit\{([^}]*)\}/g, "$1")
    .replace(/\\paragraph\{([^}]*)\}/g, "**$1**")
    .replace(/~ /g, " ")
    .replace(/(\d)~([A-Za-z])/g, "$1 $2")
    .replace(/``/g, '"')
    .replace(/''/g, '"')
    .replace(/\\%/g, "%")
    .replace(/\\\$/g, "$")
    .replace(/\\, /g, " ")
    .replace(/\{,\}/g, ",")
    .replace(/\s+/g, " ")
    .trim();
}

function splitQuestionBlock(text) {
  const trimmed = stripLatexInline(text);
  const leadMatch = trimmed.match(/^[^?]+\?/);
  if (!leadMatch) {
    return { questionLead: trimmed.slice(0, 220), questionScope: "" };
  }
  const questionLead = leadMatch[0].trim();
  const questionScope = trimmed.slice(leadMatch[0].length).trim();
  return { questionLead, questionScope };
}

function normalizeQuestion(text) {
  return stripLatexInline(text)
    .replace(/---/g, "-")
    .replace(/—/g, "-")
    .replace(/\s+/g, " ")
    .trim();
}

function extractMarketSections(tex) {
  const cleaned = stripComments(tex);
  const sections = new Map();
  const re =
    /\\subsection\{Market (\d+)\. ([^}]+)\}\s*\\label\{sec:appp-m(\d+)\}([\s\S]*?)(?=\\subsection\{Market |\\section\{)/g;
  let match;
  while ((match = re.exec(cleaned)) !== null) {
    const number = Number(match[1]);
    sections.set(number, {
      number,
      title: match[2].trim(),
      label: `sec:appp-m${match[3]}`,
      body: match[4]
    });
  }
  return sections;
}

function extractPredictionBox(sectionBody) {
  const match = sectionBody.match(
    /\\begin\{predictionbox\}(?:\[([^\]]*)\])?([\s\S]*?)\\end\{predictionbox\}/
  );
  if (!match) {
    return {
      title: "",
      question: "",
      questionLead: "",
      questionScope: "",
      yesRequires: "",
      output: ""
    };
  }
  const optionalTitle = match[1]?.trim() ?? "";
  const inner = match[2];
  const questionMatch = inner.match(
    /\\textbf\{Question\.\}\s*([\s\S]*?)(?=\\textbf\{YES requires\}|\\textbf\{Output\.\}|$)/
  );
  const yesMatch = inner.match(
    /\\textbf\{YES requires\}\s*([\s\S]*?)(?=\\textbf\{Output\.\}|$)/
  );
  const outputMatch = inner.match(/\\textbf\{Output\.\}\s*([\s\S]*?)$/);
  const questionRaw = questionMatch?.[1] ?? "";
  const { questionLead, questionScope } = splitQuestionBlock(questionRaw);
  return {
    title: optionalTitle,
    question: stripLatexInline(questionRaw),
    questionLead,
    questionScope,
    yesRequires: stripLatexInline(yesMatch?.[1] ?? ""),
    output: stripLatexInline(outputMatch?.[1] ?? "")
  };
}

function extractPriorTest(sectionBody) {
  const match = sectionBody.match(/As of 19~September 2026:([\s\S]*?)(?=\\end\{authbar\})/);
  if (!match) return "";
  return stripLatexInline(match[1]);
}

function relatedForMarket(market, bridgeCardSlugs) {
  const related = new Set(["chapters/appP"]);
  const addKey = (key) => {
    if (!key) return;
    const slug = bridgeCardSlugs[key];
    if (slug) related.add(slug);
    else console.warn(`predictions.yml: unknown bridgeCardSlugs key "${key}" (market ${market.number})`);
  };
  addKey(market.primaryBridge);
  for (const key of market.relatedBridges ?? []) addKey(key);
  return [...related];
}

function appendixAnchor(number) {
  return `sec:appp-m${number}`;
}

function formatResolveBy(isoDate) {
  if (!isoDate) return "31 December 2027";
  const [year, month, day] = isoDate.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC"
  });
}

function formatResolverLine(market) {
  if (market.resolverStatus === "confirmed" && market.resolvers?.length) {
    return `**Resolver:** ${market.resolvers.join(", ")} (confirmed).`;
  }
  if (market.resolverStatus === "ideal" && market.resolvers?.length) {
    return `**Resolver (proposed):** ${market.resolvers.join(", ")}.`;
  }
  return "**Resolver:** not yet named.";
}

const OUTPUT_CLASS_LABEL = {
  "diagnostic-certificate": "Diagnostic certificate",
  "quantitative-bound": "Quantitative bound",
  "conditional-rate": "Conditional rate",
  "structural-validation": "Structural validation",
  governance: "Governance evidence"
};

const EVIDENCE_TIER_LABEL = {
  A: "Tier A (method exists)",
  B: "Tier B (quantitatively validated)",
  C: "Tier C (adversarially validated)"
};

const LISTING_STATUS_LABEL = {
  draft: "Draft contract",
  "funding-gated": "Funding-gated",
  "ready-to-list": "Ready to list",
  listed: "Listed",
  "resolved-yes": "Resolved YES",
  "resolved-no": "Resolved NO"
};

function formatListingStatus(market) {
  const label = LISTING_STATUS_LABEL[market.marketStatus] ?? market.marketStatus;
  if (!label) return "";
  if (market.marketStatus === "funding-gated") {
    return `**Listing status.** ${label}. A credible YES route requires an unfunded independent evaluation or challenge. This is not evidence that the technical claim is false. [Fund the evaluation program](${FUNDING_CARD}).`;
  }
  if (market.marketStatus === "draft") {
    return `**Listing status.** ${label}. The contract exists, but listing questions or scientific prerequisites remain open. It is not live on a prediction platform.`;
  }
  return `**Listing status.** ${label}.`;
}

function formatAuditLine(market) {
  const output = OUTPUT_CLASS_LABEL[market.outputClass] ?? market.outputClass;
  const tier = EVIDENCE_TIER_LABEL[market.evidenceTier] ?? market.evidenceTier;
  if (!output || !tier) return "";
  const adapter = market.adapterVersion ?? 1;
  const unit = market.sampleUnit ? ` Sample unit: ${market.sampleUnit.replace(/-/g, " ")}.` : "";
  return `**Evidence class.** ${output}. YES predicts ${tier}. Adapter v${adapter}.${unit}`;
}

function marketCardMarkdown(market, extracted, bridgeCardSlugs) {
  const marketQuestion =
    market.marketQuestion || extracted.questionLead || extracted.question || market.shortQuestion;
  const summary = marketQuestion || market.shortQuestion || market.title || "";
  const appendixFull = `${APPENDIX_H_FULL}#${appendixAnchor(market.number)}`;
  const resolveByLabel = formatResolveBy(market.resolveBy);
  const bodyParts = [
    `**Resolve by:** ${resolveByLabel}.`,
    formatResolverLine(market),
    formatListingStatus(market),
    "",
    "## Question",
    "",
    marketQuestion,
    ""
  ];
  if (extracted.questionScope) {
    bodyParts.push("## Scope", "", extracted.questionScope, "");
  }
  if (extracted.yesRequires) {
    bodyParts.push("## YES requires", "", extracted.yesRequires, "");
  }
  if (extracted.output) {
    bodyParts.push("## Output", "", extracted.output, "");
  }
  const auditLine = formatAuditLine(market);
  if (auditLine) {
    bodyParts.push(auditLine, "");
  }
  if (market.notes) {
    bodyParts.push(market.notes.trim().replace(/\s+/g, " "), "");
  }
  if (extracted.priorTest) {
    bodyParts.push("## Closest work (19 September 2026)", "", extracted.priorTest, "");
  }
  bodyParts.push(
    `[Read the full contract in Appendix H](${appendixFull}) (PDF canon).`,
    "",
    "YES means these public bars were met; it does **not** mean the corresponding bridge is proved or discharged.",
    ""
  );

  return [
    "---",
    `title: ${yamlString(`Market ${market.number}. ${market.title}`)}`,
    `type: "prediction"`,
    `status: "framework"`,
    `summary: ${yamlString(summary)}`,
    `predictionNumber: ${market.number}`,
    `predictionListingStatus: ${yamlString(market.marketStatus)}`,
    `primaryBridge: ${yamlString(market.primaryBridge)}`,
    "resolvesMB: false",
    formatRelatedYaml(relatedForMarket(market, bridgeCardSlugs)),
    formatExternalYaml([
      { label: "Full contract (Appendix H)", url: appendixFull },
      {
        label: "Criteria draft (GitHub)",
        url: `${REPO}/blob/main/drafts/predictions/bridge-prediction-market-criteria.md`
      },
      {
        label: "Prediction-evaluation funding",
        url: FUNDING_CARD
      }
    ]),
    "---",
    "",
    ...bodyParts
  ].join("\n");
}

function externalFactorCardMarkdown(factor) {
  const cardPath = cardPublicPath({ id: `predictions/${factor.id}`, type: "prediction" });
  const bodyParts = [
    "**External factor.** This forecast is hosted on Metaculus, not in the eighteen bridge contracts.",
    "",
    factor.note?.trim() ?? "",
    "",
    "## Role in assurance",
    "",
    "This price forecasts whether binding legislation exists by a date. It may inform a separately modeled governance branch, complementing [Market 14](/cards/prediction/market-14/) (lab-internal binding criteria). It is **not** a direct estimate of override probability, and it is not a factor in a product bound on catastrophe.",
    "",
    "This is **not** one of the eighteen markets. YES here does not discharge any MB*.",
    "",
    `[Open on Metaculus](${factor.url}) · [How these forecasts inform assurance](${APPENDIX_H_FULL}#sec-appp-aggregation)`,
    ""
  ];

  return [
    "---",
    `title: ${yamlString(factor.title)}`,
    `type: "prediction"`,
    `status: "open"`,
    `summary: ${yamlString(factor.shortQuestion)}`,
    "predictionExternal: true",
    `predictionRole: ${yamlString(factor.role)}`,
    `metaculusEmbedId: ${factor.embedId}`,
    formatRelatedYaml(["chapters/appP", "predictions/market-14"]),
    formatExternalYaml([{ label: "Metaculus (live market)", url: factor.url }]),
    "---",
    "",
    ...bodyParts
  ].join("\n");
}

function overviewCardMarkdown(raw, markets, externalFactors, relatedForecasts, underspecifiedExamples, bridgeCardSlugs) {
  const list = markets.map((market) => {
    const cardPath = cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" });
    return `- [Market ${market.number}. ${market.title}](${cardPath}) — ${market.shortQuestion}`;
  });
  const externalList = externalFactors.map((factor) => {
    const cardPath = cardPublicPath({ id: `predictions/${factor.id}`, type: "prediction" });
    return `- [${factor.title}](${cardPath}) — ${factor.shortQuestion} *(external)*`;
  });
  const relatedList = relatedForecasts.map(
    (item) => `- [${item.title}](${item.url}) — ${(item.note ?? "").replace(/\s+/g, " ").trim()}`
  );
  const underspecifiedList = underspecifiedExamples.map(
    (item) => `- [${item.title}](${item.url}) — ${(item.note ?? "").replace(/\s+/g, " ").trim()}`
  );

  return [
    "---",
    `title: ${yamlString(raw.overview.title)}`,
    `type: "prediction"`,
    `status: "framework"`,
    `summary: ${yamlString(raw.overview.summary.trim().replace(/\s+/g, " "))}`,
    "predictionOverview: true",
    formatRelatedYaml([
      "chapters/appP",
      "mb1-boundary-estimator-soundness",
      "mb4-correction-legitimacy",
      "mb6-selection-and-basin-stability",
      "evidence-and-uncertainty"
    ]),
    formatExternalYaml([
      { label: "Appendix H (full on site)", url: APPENDIX_H_FULL },
      { label: "Bridge crosswalk (Appendix B)", url: "/cards/appendix/appB/" },
      {
        label: "Working criteria (GitHub)",
        url: `${REPO}/blob/main/drafts/predictions/bridge-prediction-market-criteria.md`
      }
    ]),
    "---",
    "",
    raw.purpose.trim(),
    "",
    "**Claim strength.** YES means a public artifact met the appendix thresholds by each market's resolve-by date. NO lumps failed bars, no qualifying evaluation, inapplicable substrate, or unresolved residual judgment. NO does not mean a bridge is false.",
    "",
    `**Assurance.** A price is P(qualifying artifact exists by the deadline), not a safety-case probability. See [How these forecasts inform assurance](${APPENDIX_H_FULL}#sec-appp-aggregation) and [Assurance failure, coverage, and consequences](${APPENDIX_H_FULL}#sec-appp-assurance). YES means reconstructible public bars were met, not that a frontier deployment is certified.`,
    "",
    "## The eighteen markets",
    "",
    ...list,
    "",
    ...(externalList.length
      ? ["## External factors (not bridge markets)", "", ...externalList, ""]
      : []),
    ...(relatedList.length
      ? [
          "## Related forecasts",
          "",
          "Nearby Metaculus questions. They are not the pause factor above, not bridge markets, and not inputs to the assurance model.",
          "",
          ...relatedList,
          ""
        ]
      : []),
    ...(underspecifiedList.length
      ? [
          "## An underspecified question",
          "",
          "Listed as a contract shape this catalog refuses. Not a forecast input.",
          "",
          ...underspecifiedList,
          ""
        ]
      : [])
  ].join("\n");
}

const REQUIRED_OUTPUT_CLASSES = new Set([
  "diagnostic-certificate",
  "quantitative-bound",
  "conditional-rate",
  "structural-validation",
  "governance"
]);
const REQUIRED_TIERS = new Set(["A", "B", "C"]);
const REQUIRED_LISTING_STATUSES = new Set([
  "draft",
  "funding-gated",
  "ready-to-list",
  "listed",
  "resolved-yes",
  "resolved-no"
]);
const REQUIRED_REASON_CODES = new Set([
  "substantive-bar-failed",
  "no-qualifying-artifact",
  "reporting-insufficient",
  "adversarial-validation-absent",
  "evidence-incompatible",
  "unresolved-judgment"
]);

function assertMarketAudit(market) {
  const problems = [];
  if (!REQUIRED_OUTPUT_CLASSES.has(market.outputClass)) {
    problems.push(`missing/invalid outputClass (${market.outputClass ?? "—"})`);
  }
  if (!REQUIRED_TIERS.has(market.evidenceTier)) {
    problems.push(`missing/invalid evidenceTier (${market.evidenceTier ?? "—"})`);
  }
  if (!REQUIRED_LISTING_STATUSES.has(market.marketStatus)) {
    problems.push(`missing/invalid marketStatus (${market.marketStatus ?? "—"})`);
  }
  if (!market.sampleUnit) problems.push("missing sampleUnit");
  if (!market.bars?.scientific?.length) problems.push("missing scientific bars");
  if (problems.length) {
    console.warn(`sync-predictions: market ${market.number} audit: ${problems.join("; ")}`);
  }
}

function collapseBlurb(value) {
  return (value ?? "").replace(/\s+/g, " ").trim();
}

const raw = yaml.load(await readFile(sourcePath, "utf8"));
const appendixTex = await readFile(appendixPath, "utf8");
const sectionByNumber = extractMarketSections(appendixTex);
const bridgeCardSlugs = raw.bridgeCardSlugs ?? {};

const markets = [...raw.markets].sort((a, b) => a.number - b.number);
const configuredListingStatuses = new Set(Object.keys(raw.resolution?.listingStatuses ?? {}));
const configuredReasonCodes = new Set(raw.resolution?.reasonCodes ?? []);
for (const status of REQUIRED_LISTING_STATUSES) {
  if (!configuredListingStatuses.has(status)) {
    throw new Error(`predictions.yml: missing listing-status definition "${status}"`);
  }
}
for (const reason of REQUIRED_REASON_CODES) {
  if (!configuredReasonCodes.has(reason)) {
    throw new Error(`predictions.yml: missing resolution reason code "${reason}"`);
  }
}
if (markets.length !== 18) {
  console.warn(`sync-predictions: expected 18 catalog markets, found ${markets.length}`);
}
if (sectionByNumber.size !== markets.length) {
  console.warn(
    `sync-predictions: appendix market sections (${sectionByNumber.size}) != YAML markets (${markets.length})`
  );
}
for (const market of markets) assertMarketAudit(market);
const externalFactors = [...(raw.externalFactors ?? [])];
const relatedForecasts = [...(raw.relatedForecasts ?? [])];
const underspecifiedExamples = [...(raw.underspecifiedExamples ?? [])];

await rm(predictionCardsDir, { recursive: true, force: true });
await mkdir(predictionCardsDir, { recursive: true });

let cardCount = 0;

await writeFile(
  path.join(predictionCardsDir, "overview.md"),
  overviewCardMarkdown(raw, markets, externalFactors, relatedForecasts, underspecifiedExamples, bridgeCardSlugs),
  "utf8"
);
cardCount += 1;

const enrichedMarkets = markets.map((market) => {
  const section = sectionByNumber.get(market.number);
  const box = section ? extractPredictionBox(section.body) : {};
  const priorTest = section ? extractPriorTest(section.body) : "";
  const marketQuestion =
    market.marketQuestion || box.questionLead || box.question || market.shortQuestion;
  if (
    market.marketQuestion &&
    box.questionLead &&
    normalizeQuestion(market.marketQuestion) !== normalizeQuestion(box.questionLead)
  ) {
    console.warn(
      `sync-predictions: market ${market.number} marketQuestion differs from appendix lead sentence`
    );
  }
  return {
    ...market,
    cardId: market.id,
    cardPath: cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" }),
    marketQuestion,
    questionScope: box.questionScope || "",
    question: marketQuestion,
    priorTest
  };
});

for (const market of markets) {
  const section = sectionByNumber.get(market.number);
  const box = section ? extractPredictionBox(section.body) : {};
  const priorTest = section ? extractPriorTest(section.body) : "";
  const md = marketCardMarkdown(
    market,
    { ...box, priorTest },
    bridgeCardSlugs
  );
  await writeFile(path.join(predictionCardsDir, `${market.id}.md`), md, "utf8");
  cardCount += 1;
}

const enrichedExternalFactors = externalFactors.map((factor) => ({
  ...factor,
  cardId: factor.id,
  cardPath: cardPublicPath({ id: `predictions/${factor.id}`, type: "prediction" })
}));

for (const factor of externalFactors) {
  const md = externalFactorCardMarkdown(factor);
  await writeFile(path.join(predictionCardsDir, `${factor.id}.md`), md, "utf8");
  cardCount += 1;
}

const aggregation = {
  title: raw.aggregation?.title ?? "How these forecasts inform assurance",
  appendixAnchor: raw.aggregation?.appendixAnchor ?? "sec:appp-aggregation",
  blurb: collapseBlurb(raw.aggregation?.blurb),
  hubNote: collapseBlurb(raw.aggregation?.hubNote),
  assuranceAnchor: "sec:appp-assurance"
};
const graphPlaceholder = {
  title: raw.graphPlaceholder?.title ?? "Assurance context, not a doom product",
  blurb: collapseBlurb(raw.graphPlaceholder?.blurb)
};

const payload = {
  purpose: raw.purpose?.trim() ?? "",
  overviewCardId: "predictions/overview",
  appendixBookId: "appP",
  markets: enrichedMarkets,
  externalFactors: enrichedExternalFactors,
  relatedForecasts,
  underspecifiedExamples,
  resolution: raw.resolution ?? {},
  aggregation,
  graphPlaceholder
};

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

console.log(`sync-predictions: wrote ${cardCount} cards and predictions.json`);
