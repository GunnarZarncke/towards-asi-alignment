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

function metaculusQuestionId(url) {
  const match = String(url ?? "").match(/metaculus\.com\/questions\/(\d+)/i);
  return match ? Number(match[1]) : undefined;
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
    .replace(/\\(?:ref|eqref)\{[^}]+\}/g, "")
    .replace(/\\emph\{([^}]*)\}/g, "$1")
    .replace(/\\textbf\{([^}]*)\}/g, "**$1**")
    .replace(/\\textit\{([^}]*)\}/g, "$1")
    .replace(/\\paragraph\{([^}]*)\}/g, "**$1**")
    .replace(/~/g, " ")
    .replace(/``/g, '"')
    .replace(/''/g, '"')
    .replace(/\\%/g, "%")
    .replace(/\\\$/g, "$")
    .replace(/\\,/g, " ")
    .replace(/\{,\}/g, ",")
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
    .replace(
      /\\begin\{description\}[\s\S]*?\\end\{description\}/g,
      (block) =>
        [...block.matchAll(/\\item\[([^\]]*)\]\s*([\s\S]*?)(?=\\item\[|$)/g)]
          .map((match) => `- **${stripLatexInline(match[1])}** ${stripLatexInline(match[2])}`)
          .join("\n") + "\n"
    );
}

function formatLatexParagraphs(text) {
  return convertBasicLatexLists(text)
    .split(/\n\s*\n|\n(?=[A-Z"(\[])/)
    .map((para) => stripLatexInline(para))
    .filter(Boolean)
    .join("\n\n");
}

function extractResolutionBlocks(resolutionInner) {
  const trimmed = resolutionInner.trim();
  if (!trimmed) return [];

  const blocks = [];
  const re = /\\textbf\{([^}]+)\}\s*([\s\S]*?)(?=\\textbf\{|$)/g;
  let match;
  while ((match = re.exec(trimmed)) !== null) {
    const label = stripLatexInline(match[1]).replace(/\.$/, "").trim();
    const body = formatLatexParagraphs(match[2]);
    if (label || body) blocks.push({ label, body });
  }

  if (!blocks.length) {
    const body = formatLatexParagraphs(trimmed);
    if (body) blocks.push({ label: "", body });
  }
  return blocks;
}

const RESOLUTION_THREE_WAY_INTRO =
  "These bars define when a qualifying attempt counts toward **YES**. A qualifying attempt that ran but missed them counts toward **NO** when no other qualifying attempt met them. Missing evals, missing publication, or unmet qualification requirements resolve **OTHER**.";

const RESOLUTION_YES_NO_INTRO =
  "These conditions define **YES**. Anything else, including missing evidence, resolves **NO**. This market has no OTHER.";

function isYesNoMarket(market) {
  const outcomes = market.outcomes ?? ["YES", "NO", "OTHER"];
  return outcomes.length === 2 && outcomes.includes("YES") && outcomes.includes("NO");
}

// Each market's fine print repeats the Common qualification rules verbatim so a question can be
// listed on its own. Markets 14, 19, and 20 state their own procedures and are exempt.
const COMMON_RULES_EXEMPT = new Set([14, 19, 20]);

function commonParagraph(tex, marker) {
  const start = tex.indexOf(marker);
  if (start === -1) throw new Error(`sync-predictions: Common qualification lacks "${marker}"`);
  const end = tex.indexOf("\n\n", start);
  return tex.slice(start, end === -1 ? undefined : end).trim();
}

function assertCommonRulesCopies(tex, sectionByNumber) {
  const boxStart = tex.indexOf("\\begin{predictionbox}[Common qualification]");
  const boxEnd = tex.indexOf("\\end{predictionresolution}", boxStart);
  const common = tex.slice(boxStart, boxEnd);
  const rules = commonParagraph(common, "\\textbf{Common rules.}");
  const serious = commonParagraph(common, "\\textbf{Adversarial budget: serious.}");
  const fallback = commonParagraph(common, "\\textbf{Adversarial budget: default.}");
  for (const [number, section] of sectionByNumber) {
    if (COMMON_RULES_EXEMPT.has(number)) continue;
    const body = section.body;
    const budgets = [serious, fallback].filter((text) => body.includes(text)).length;
    if (!body.includes(rules) || budgets !== 1) {
      throw new Error(
        `sync-predictions: Market ${number} fine print must repeat the Common rules verbatim and exactly one adversarial budget`
      );
    }
  }
}

function assertPlainCardText(label, text) {
  if (!text) return;
  if (/\\[a-zA-Z@]/.test(text) || /~/.test(text)) {
    throw new Error(`sync-predictions: leftover TeX in ${label}: ${text.slice(0, 180)}`);
  }
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

function extractContractEnv(sectionBody, envName) {
  const match = sectionBody.match(
    new RegExp(`\\\\begin\\{${envName}\\}([\\s\\S]*?)\\\\end\\{${envName}\\}`)
  );
  return match?.[1]?.trim() ?? "";
}

function extractPredictionBox(sectionBody) {
  const boxes = [
    ...sectionBody.matchAll(
      /\\begin\{predictionbox\}(?:\[([^\]]*)\])?([\s\S]*?)\\end\{predictionbox\}/g
    )
  ];
  if (!boxes.length) {
    return {
      title: "",
      question: "",
      questionLead: "",
      questionScope: "",
      background: "",
      resolutionBlocks: []
    };
  }
  const optionalTitle = boxes[0][1]?.trim() ?? "";
  const frontInner = boxes.map((b) => b[2]).join("\n\n");
  const questionMatch = frontInner.match(
    /\\textbf\{Question\.\}\s*([\s\S]*?)(?=\\textbf\{Choices\.\}|\\textbf\{Parameters\.\}|$)/
  );
  const questionRaw = questionMatch?.[1] ?? "";
  const { questionLead, questionScope } = splitQuestionBlock(questionRaw);

  const backgroundInner = extractContractEnv(sectionBody, "predictionbackground");
  const resolutionInner = extractContractEnv(sectionBody, "predictionresolution");
  const legacyInner = resolutionInner ? "" : frontInner;
  const resolutionBlocks = resolutionInner
    ? extractResolutionBlocks(resolutionInner)
    : extractResolutionBlocks(legacyInner);

  const extracted = {
    title: optionalTitle,
    question: stripLatexInline(questionRaw),
    questionLead,
    questionScope,
    background: formatLatexParagraphs(backgroundInner),
    resolutionBlocks
  };
  for (const [field, value] of Object.entries(extracted)) {
    if (field === "resolutionBlocks") {
      for (const block of value) {
        assertPlainCardText(`prediction box resolution ${block.label || "block"}`, block.body);
      }
      continue;
    }
    assertPlainCardText(`prediction box ${field}`, value);
  }
  return extracted;
}

function extractPriorTest(sectionBody) {
  const match = sectionBody.match(
    /Closest existing work(?: is)?[:\s]([\s\S]*?)(?=\\end\{authbar\})/
  );
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
  "resolved-no": "Resolved NO",
  "resolved-other": "Resolved OTHER"
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

function catalogShortTitle(market) {
  const raw = (market.shortTitle || market.shortQuestion || market.title || "").trim();
  if (!raw) return "";
  return raw.endsWith("?") ? raw : `${raw}?`;
}

function catalogLongTitle(market, extracted = {}) {
  return (
    market.longTitle ||
    market.marketQuestion ||
    extracted.questionLead ||
    extracted.question ||
    catalogShortTitle(market)
  );
}

function marketCardMarkdown(market, extracted, bridgeCardSlugs) {
  const shortTitle = catalogShortTitle(market);
  const longTitle = catalogLongTitle(market, extracted);
  const summary = longTitle || shortTitle || market.title || "";
  const appendixFull = `${APPENDIX_H_FULL}#${appendixAnchor(market.number)}`;
  const resolveByLabel = formatResolveBy(market.resolveBy);
  const bodyParts = [
    `**Resolve by:** ${resolveByLabel}.`,
    formatListingStatus(market),
    ""
  ];
  if (extracted.background) {
    bodyParts.push("## Background", "", extracted.background, "");
  }
  if (extracted.questionScope) {
    bodyParts.push("## Scope", "", extracted.questionScope, "");
  }
  if (extracted.resolutionBlocks?.length) {
    bodyParts.push("## Resolution criteria", "");
    const hasYesRequires = extracted.resolutionBlocks.some((block) =>
      block.label.toLowerCase().includes("yes requires")
    );
    if (hasYesRequires) {
      bodyParts.push(isYesNoMarket(market) ? RESOLUTION_YES_NO_INTRO : RESOLUTION_THREE_WAY_INTRO, "");
    }
    for (const block of extracted.resolutionBlocks) {
      if (block.label) {
        bodyParts.push(`### ${block.label}`, "");
      }
      if (block.body) {
        bodyParts.push(block.body, "");
      }
    }
  }
  const auditLine = formatAuditLine(market);
  if (auditLine) {
    bodyParts.push(auditLine, "");
  }
  if (market.notes) {
    bodyParts.push(market.notes.trim().replace(/\s+/g, " "), "");
  }
  if (extracted.priorTest) {
    assertPlainCardText(`market ${market.number} closest work`, extracted.priorTest);
    bodyParts.push("## Closest existing work", "", extracted.priorTest, "");
  }
  bodyParts.push(
    `[Read the full contract in Appendix H](${appendixFull}) (PDF canon).`,
    "",
    isYesNoMarket(market)
      ? "YES and NO are the two listing options: every condition holds, or not. Neither means the corresponding bridge is proved or discharged."
      : "YES, NO, and OTHER are the three listing options: at least one qualifying attempt met the bars, every qualifying attempt missed them, or no qualifying attempt existed. If several qualifying attempts exist and any met the bars, resolve YES. None of these means the corresponding bridge is proved or discharged.",
    ""
  );

  return [
    "---",
    `title: ${yamlString(`Market ${market.number}. ${shortTitle}`)}`,
    `type: "prediction"`,
    `status: "framework"`,
    `summary: ${yamlString(summary)}`,
    `predictionNumber: ${market.number}`,
    `predictionListingStatus: ${yamlString(market.marketStatus)}`,
    `predictionShortTitle: ${yamlString(shortTitle)}`,
    `primaryBridge: ${yamlString(market.primaryBridge)}`,
    "resolvesMB: false",
    ...(market.metaculusEmbedId != null ? [`metaculusEmbedId: ${market.metaculusEmbedId}`] : []),
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
    "**External factor.** This forecast is hosted on Metaculus, not among the AI alignment subproblem markets.",
    "",
    factor.note?.trim() ?? "",
    "",
    "## Role in the safety case",
    "",
    "This price forecasts whether binding legislation exists by a date. It may inform a separately modeled governance branch, complementing [Market 14](/cards/prediction/market-14/) (lab-internal binding criteria). It is **not** a direct estimate of override probability, and it is not a factor in a product bound on catastrophe.",
    "",
    "This is **not** one of the AI alignment subproblem markets. YES here does not discharge any MB*.",
    "",
    `[Open on Metaculus](${factor.url}) · [How these forecasts inform the safety case](${APPENDIX_H_FULL}#sec-appp-aggregation)`,
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

function overviewCardMarkdown(raw, markets, externalFactors, relatedForecasts, bridgeCardSlugs) {
  const list = markets.map((market) => {
    const cardPath = cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" });
    return `- [Market ${market.number}. ${catalogShortTitle(market)}](${cardPath})`;
  });
  const relatedList = [
    ...externalFactors.map((factor) => {
      const label = factor.shortQuestion || factor.title;
      return `- [${label}](${factor.url}) — ${(factor.note ?? "").replace(/\s+/g, " ").trim()} *(external)*`;
    }),
    ...relatedForecasts.map(
      (item) => `- [${item.title}](${item.url}) — ${(item.note ?? "").replace(/\s+/g, " ").trim()}`
    )
  ];

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
    "**Claim strength.** Each listing question is three-outcome: YES (at least one qualifying attempt met the bars), NO (every qualifying attempt missed them), or OTHER (no qualifying attempt existed). Missing evals or missed qualification is OTHER, not NO. Market 14 is the exception: YES or NO only, and anything short of YES, including missing evidence, is NO. None of these means a bridge is false.",
    "",
    `**Safety case.** A price is P(qualifying artifact exists by the deadline), not a safety-case probability. See [How these forecasts inform the safety case](${APPENDIX_H_FULL}#sec-appp-aggregation) and [False accept, coverage, and consequences](${APPENDIX_H_FULL}#sec-appp-assurance). YES means reconstructible public bars were met, not that a frontier deployment is certified.`,
    "",
    "## AI alignment subproblem markets",
    "",
    ...list,
    "",
    ...(relatedList.length
      ? [
          "## Related forecasts",
          "",
          "Live Metaculus questions, including the external pause factor. Not subproblem markets and not inputs to the safety-case model.",
          "",
          ...relatedList,
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
  "resolved-no",
  "resolved-other"
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
const missingSections = markets.filter((market) => !sectionByNumber.has(market.number));
if (missingSections.length) {
  throw new Error(
    `sync-predictions: YAML markets missing appendix sections: ${missingSections
      .map((m) => m.number)
      .join(", ")}`
  );
}
for (const market of markets) assertMarketAudit(market);
assertCommonRulesCopies(appendixTex, sectionByNumber);
const externalFactors = [...(raw.externalFactors ?? [])];
const relatedForecasts = [...(raw.relatedForecasts ?? [])];

await rm(predictionCardsDir, { recursive: true, force: true });
await mkdir(predictionCardsDir, { recursive: true });

let cardCount = 0;

await writeFile(
  path.join(predictionCardsDir, "overview.md"),
  overviewCardMarkdown(raw, markets, externalFactors, relatedForecasts, bridgeCardSlugs),
  "utf8"
);
cardCount += 1;

const enrichedMarkets = markets.map((market) => {
  const section = sectionByNumber.get(market.number);
  const box = section ? extractPredictionBox(section.body) : {};
  const priorTest = section ? extractPriorTest(section.body) : "";
  const longTitle = catalogLongTitle(market, box);
  if (
    longTitle &&
    box.questionLead &&
    normalizeQuestion(longTitle) !== normalizeQuestion(box.questionLead)
  ) {
    console.warn(
      `sync-predictions: market ${market.number} longTitle differs from appendix lead sentence`
    );
  }
  return {
    ...market,
    cardId: market.id,
    cardPath: cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" }),
    shortTitle: catalogShortTitle(market),
    longTitle,
    marketQuestion: longTitle,
    questionScope: box.questionScope || "",
    question: longTitle,
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
  embedId: factor.embedId ?? metaculusQuestionId(factor.url),
  cardId: factor.id,
  cardPath: cardPublicPath({ id: `predictions/${factor.id}`, type: "prediction" })
}));

const enrichedRelatedForecasts = relatedForecasts.map((item) => ({
  ...item,
  embedId: item.embedId ?? metaculusQuestionId(item.url)
}));

for (const factor of externalFactors) {
  const md = externalFactorCardMarkdown(factor);
  await writeFile(path.join(predictionCardsDir, `${factor.id}.md`), md, "utf8");
  cardCount += 1;
}

const aggregation = {
  title: raw.aggregation?.title ?? "How these forecasts inform the safety case",
  appendixAnchor: raw.aggregation?.appendixAnchor ?? "sec:appp-aggregation",
  blurb: collapseBlurb(raw.aggregation?.blurb),
  hubNote: collapseBlurb(raw.aggregation?.hubNote),
  assuranceAnchor: "sec:appp-assurance"
};
const graphPlaceholder = {
  title: raw.graphPlaceholder?.title ?? "Safety-case context, not a doom product",
  blurb: collapseBlurb(raw.graphPlaceholder?.blurb)
};

const payload = {
  purpose: raw.purpose?.trim() ?? "",
  overviewCardId: "predictions/overview",
  appendixBookId: "appP",
  markets: enrichedMarkets,
  externalFactors: enrichedExternalFactors,
  relatedForecasts: enrichedRelatedForecasts,
  resolution: raw.resolution ?? {},
  aggregation,
  graphPlaceholder
};

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

console.log(`sync-predictions: wrote ${cardCount} cards and predictions.json`);
