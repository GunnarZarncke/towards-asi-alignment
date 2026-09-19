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

function firstQuestionSentence(text) {
  const trimmed = stripLatexInline(text);
  const match = trimmed.match(/^[^?]+\?/);
  return match ? match[0].trim() : trimmed.slice(0, 220);
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
  if (!match) return { title: "", question: "", yesRequires: "", output: "" };
  const optionalTitle = match[1]?.trim() ?? "";
  const inner = match[2];
  const questionMatch = inner.match(
    /\\textbf\{Question\.\}\s*([\s\S]*?)(?=\\textbf\{YES requires\}|\\textbf\{Output\.\}|$)/
  );
  const yesMatch = inner.match(
    /\\textbf\{YES requires\}\s*([\s\S]*?)(?=\\textbf\{Output\.\}|$)/
  );
  const outputMatch = inner.match(/\\textbf\{Output\.\}\s*([\s\S]*?)$/);
  return {
    title: optionalTitle,
    question: stripLatexInline(questionMatch?.[1] ?? ""),
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
  for (const key of market.relatedBridges ?? []) {
    if (typeof key === "string" && !key.includes("-")) {
      const slug = bridgeCardSlugs[key];
      if (slug) related.add(slug);
    } else if (typeof key === "string") {
      related.add(key);
    }
  }
  const primarySlug = bridgeCardSlugs[market.primaryBridge];
  if (primarySlug) related.add(primarySlug);
  return [...related];
}

function appendixAnchor(number) {
  return `sec:appp-m${number}`;
}

function marketCardMarkdown(market, extracted, bridgeCardSlugs) {
  const summary = firstQuestionSentence(extracted.question || market.shortQuestion);
  const appendixFull = `/cards/appendix/appP/full/#${appendixAnchor(market.number)}`;
  const bodyParts = [
    `**Resolve by:** 31 December 2027.`,
    "",
    "## Question",
    "",
    extracted.question || market.shortQuestion,
    ""
  ];
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

function overviewCardMarkdown(raw, markets, bridgeCardSlugs) {
  const list = markets.map((market) => {
    const cardPath = cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" });
    return `- [Market ${market.number}. ${market.title}](${cardPath}) — ${market.shortQuestion}`;
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
    "**Claim strength.** YES means a public artifact met *these frozen bars* by 31 December 2027. NO lumps failed bars, no qualifying evaluation, inapplicable substrate, or unresolved residual judgment. NO does not mean a bridge is false.",
    "",
    "## The eighteen contracts",
    "",
    ...list,
    ""
  ].join("\n");
}

const raw = yaml.load(await readFile(sourcePath, "utf8"));
const appendixTex = await readFile(appendixPath, "utf8");
const sectionByNumber = extractMarketSections(appendixTex);
const bridgeCardSlugs = raw.bridgeCardSlugs ?? {};

const markets = [...raw.markets].sort((a, b) => a.number - b.number);

await rm(predictionCardsDir, { recursive: true, force: true });
await mkdir(predictionCardsDir, { recursive: true });

let cardCount = 0;

await writeFile(
  path.join(predictionCardsDir, "overview.md"),
  overviewCardMarkdown(raw, markets, bridgeCardSlugs),
  "utf8"
);
cardCount += 1;

const enrichedMarkets = markets.map((market) => {
  const section = sectionByNumber.get(market.number);
  const box = section ? extractPredictionBox(section.body) : {};
  const priorTest = section ? extractPriorTest(section.body) : "";
  return {
    ...market,
    cardId: market.id,
    cardPath: cardPublicPath({ id: `predictions/${market.id}`, type: "prediction" }),
    question: box.question || market.shortQuestion,
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

const payload = {
  purpose: raw.purpose?.trim() ?? "",
  resolveBy: raw.resolveBy ?? "2027-12-31",
  overviewCardId: "predictions/overview",
  appendixBookId: "appP",
  markets: enrichedMarkets,
  graphPlaceholder: {
    title: "Live prices (coming soon)",
    blurb:
      "When these contracts are listed on a public platform (Metaculus, Manifold, or both), aggregate prices will embed here. Until then, use the cards below and Appendix H for the frozen spec."
  }
};

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

console.log(`sync-predictions: wrote ${cardCount} cards and predictions.json`);
