import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import { stripComments } from "./lib/tex-convert.mjs";
import { cardPublicPath } from "./lib/card-urls.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const sourcePath = path.join(repoRoot, "metadata", "predictions.yml");
const appendixPath = path.join(repoRoot, "appendices", "appP-bridge-predictions.tex");
const outputDir = path.join(siteRoot, "src", "data");
const outputPath = path.join(outputDir, "predictions.json");
const predictionCardsDir = path.join(siteRoot, "src", "content", "cards", "predictions");

const REPO = "https://github.com/GunnarZarncke/towards-asi-alignment";

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
    /\\subsection\{Market (\d+)\. ([^}]+)\}\s*\\label\{sec:appp-m(\d+)\}([\s\S]*?)(?=\\subsection\{Market |\\section\{Not in)/g;
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

function marketCardMarkdown(market, extracted, bridgeCardSlugs) {
  const summary = market.shortQuestion || market.title || "";
  const marketQuestion =
    market.marketQuestion || extracted.questionLead || extracted.question || market.shortQuestion;
  const appendixFull = `/cards/appendix/appP/full/#${appendixAnchor(market.number)}`;
  const resolveByLabel = formatResolveBy(market.resolveBy);
  const bodyParts = [
    `**Resolve by:** ${resolveByLabel}.`,
    formatResolverLine(market),
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
    `status: "open"`,
    `summary: ${yamlString(summary)}`,
    `predictionNumber: ${market.number}`,
    `primaryBridge: ${yamlString(market.primaryBridge)}`,
    "resolvesMB: false",
    formatRelatedYaml(relatedForMarket(market, bridgeCardSlugs)),
    formatExternalYaml([
      { label: "Full contract (Appendix H)", url: appendixFull },
      {
        label: "Criteria draft (GitHub)",
        url: `${REPO}/blob/main/drafts/predictions/bridge-prediction-market-criteria.md`
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
    "## Role in aggregation",
    "",
    "The Appendix H aggregation sketch uses this price as **q_pause**: institutional capacity to slow or restrict frontier deployment when evidence warrants pause, complementing [Market 14](/cards/prediction/market-14/) (lab-internal binding criteria).",
    "",
    "This is **not** one of the eighteen markets. YES here does not discharge any MB*.",
    "",
    `[Open on Metaculus](${factor.url}) · [Aggregation section in Appendix H](/cards/appendix/appP/full/#sec-appp-aggregation)`,
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

function overviewCardMarkdown(raw, markets, externalFactors, bridgeCardSlugs) {
  const list = markets.map((market) => {
    const cardPath = cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" });
    return `- [Market ${market.number}. ${market.title}](${cardPath}) — ${market.shortQuestion}`;
  });
  const externalList = externalFactors.map((factor) => {
    const cardPath = cardPublicPath({ id: `predictions/${factor.id}`, type: "prediction" });
    return `- [${factor.title}](${cardPath}) — ${factor.shortQuestion} *(external)*`;
  });

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
      { label: "Appendix H (full on site)", url: "/cards/appendix/appP/full/" },
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
    "**Aggregation.** Prices compose along the spine dependency graph into an *optimistic* upper bound on $P(\\mathrm{doom})$; see [Composing an optimistic bound](/cards/appendix/appP/full/#sec-appp-aggregation) in Appendix H. YES on a market means the *tool exists*, not that it certifies a frontier deployment.",
    "",
    "## The eighteen contracts",
    "",
    ...list,
    "",
    ...(externalList.length
      ? ["## External factors (not bridge markets)", "", ...externalList, ""]
      : [])
  ].join("\n");
}

const raw = yaml.load(await readFile(sourcePath, "utf8"));
const appendixTex = await readFile(appendixPath, "utf8");
const sectionByNumber = extractMarketSections(appendixTex);
const bridgeCardSlugs = raw.bridgeCardSlugs ?? {};

const markets = [...raw.markets].sort((a, b) => a.number - b.number);
const externalFactors = [...(raw.externalFactors ?? [])];

await rm(predictionCardsDir, { recursive: true, force: true });
await mkdir(predictionCardsDir, { recursive: true });

let cardCount = 0;

await writeFile(
  path.join(predictionCardsDir, "overview.md"),
  overviewCardMarkdown(raw, markets, externalFactors, bridgeCardSlugs),
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

const payload = {
  purpose: raw.purpose?.trim() ?? "",
  overviewCardId: "predictions/overview",
  appendixBookId: "appP",
  markets: enrichedMarkets,
  externalFactors: enrichedExternalFactors,
  aggregation: {
    title: "Optimistic bound on P(doom)",
    appendixAnchor: "sec-appp-aggregation",
    blurb:
      "Compose spine-market YES prices with an external pause factor (Metaculus Q44423). This is an optimistic upper bound: YES means operational tools exist, not that bridges hold on frontier systems."
  },
  graphPlaceholder: {
    title: "Optimistic P(doom) composition",
    blurb:
      "Eighteen bridge markets price operational milestones along the spine. An external Metaculus forecast prices institutional pause capacity. Together they sketch an optimistic bound—see Appendix H §aggregation."
  }
};

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

console.log(`sync-predictions: wrote ${cardCount} cards and predictions.json`);
