import { mkdir, readdir, readFile, writeFile, rm } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { stripComments } from "./lib/tex-convert.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

const PART_TITLES = {
  part01: "The Alignment Problem Reframed",
  part02: "Agents, Boundaries, and Real Optimizers",
  part03: "Capability Growth and Competence",
  part04: "Value Bundles",
  part05: "Goal Inference and Transport",
  part06: "Correction Channels",
  part07: "Successors and Continuity",
  part08: "Attractor Basins and Selection",
  part09: "Safety Cases and Adversaries",
  part10: "Civilizational Limits"
};

function yamlString(value) {
  return JSON.stringify(value);
}

function extractChapterThesis(tex) {
  const match = stripComments(tex).match(/\\begin\{chapterthesis\}([\s\S]*?)\\end\{chapterthesis\}/);
  if (!match) return "";
  return match[1]
    .replace(/\\emph\{([^}]*)\}/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function extractChapterLabel(tex) {
  return stripComments(tex).match(/\\label\{(ch:[^}]+)\}/)?.[1] || null;
}

function extractAppendixLabel(tex) {
  return stripComments(tex).match(/\\label\{([^}]+)\}/)?.[1] || null;
}

async function listConceptCards(cardsDir) {
  const entries = await readdir(cardsDir, { withFileTypes: true });
  const related = new Map();

  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
    const text = await readFile(path.join(cardsDir, entry.name), "utf8");
    const fm = text.match(/^---\n([\s\S]*?)\n---/)?.[1] || "";
    const slug = entry.name.replace(/\.md$/, "");
    const chapters = [];
    const inline = fm.match(/^bookChapters:\s*\[(.+?)\]/m);
    if (inline) {
      chapters.push(...inline[1].split(",").map((item) => item.trim().replace(/^"|"$/g, "")));
    } else {
      const block = fm.match(/^bookChapters:\s*\n((?:\s+-\s+.+\n)+)/m);
      if (block) {
        for (const line of block[1].matchAll(/^\s+-\s+"?([^"\n]+)"?\s*$/gm)) {
          chapters.push(line[1]);
        }
      }
    }
    for (const chapterId of chapters) {
      if (!related.has(chapterId)) related.set(chapterId, []);
      related.get(chapterId).push(slug);
    }
  }

  for (const [key, slugs] of related) {
    related.set(key, [...new Set(slugs)].sort());
  }
  return related;
}

function cardFrontmatter(data) {
  const lines = [
    "---",
    `title: ${yamlString(data.title)}`,
    `type: ${yamlString(data.type)}`,
    `status: ${yamlString(data.status)}`,
    `summary: ${yamlString(data.summary)}`,
    `bookPageId: ${yamlString(data.bookPageId)}`,
    `bookChapters: [${yamlString(data.bookPageId)}]`,
    `bookLabels: [${yamlString(data.bookLabel)}]`
  ];

  if (data.part) lines.push(`part: ${yamlString(data.part)}`);
  if (data.formalDensity) lines.push(`formalDensity: ${yamlString(data.formalDensity)}`);
  if (data.overviewOnly) lines.push("overviewOnly: true");
  if (data.related.length > 0) {
    lines.push("related:");
    for (const slug of data.related) lines.push(`  - ${slug}`);
  }

  lines.push("---", "");
  return lines.join("\n");
}

function cardBody(data) {
  const lines = [];
  if (!data.overviewOnly) {
    lines.push(data.summary);
  }
  if (data.bodyExtra) {
    if (lines.length > 0) lines.push("");
    lines.push(data.bodyExtra);
  }
  if (data.partTitle) {
    lines.push("", `Part: ${data.partTitle}`);
  }
  return lines.join("\n");
}

async function main() {
  const book = JSON.parse(await readFile(path.join(siteRoot, "src", "data", "book.json"), "utf8"));
  const cardsDir = path.join(siteRoot, "src", "content", "cards");
  const outDir = path.join(cardsDir, "chapters");
  const relatedByChapter = await listConceptCards(cardsDir);

  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });

  let count = 0;

  for (const chapter of book.chapters) {
    const file = (await readdir(path.join(repoRoot, "chapters"))).find((name) => name.startsWith(`${chapter.id}-`));
    if (!file) continue;
    const tex = await readFile(path.join(repoRoot, "chapters", file), "utf8");
    const thesis = extractChapterThesis(tex);
    const bookLabel = extractChapterLabel(tex);
    if (!bookLabel) continue;

    const md = [
      cardFrontmatter({
        title: chapter.title,
        type: "chapter",
        status: chapter.status,
        summary: thesis || chapter.title,
        bookPageId: chapter.id,
        bookLabel,
        part: chapter.part?.id,
        partTitle: chapter.part ? PART_TITLES[chapter.part.id] : undefined,
        formalDensity: chapter.formalDensity,
        related: relatedByChapter.get(chapter.id) || []
      }),
      cardBody({
        title: chapter.title,
        type: "chapter",
        summary: thesis || chapter.title,
        bookPageId: chapter.id,
        partTitle: chapter.part ? PART_TITLES[chapter.part.id] : undefined
      })
    ].join("\n");

    await writeFile(path.join(outDir, `${chapter.id}.md`), md, "utf8");
    count += 1;
  }

  const appendixSpecs = [
    {
      id: "appB",
      file: "appendices/appB-bridge-crosswalk.tex",
      type: "appendix",
      title: "Bridges and the Field: A Crosswalk",
      related: [
        "bridge-assumptions",
        "mb1-boundary-estimator-soundness",
        "mb2-bundle-identifiability",
        "mb3-bearer-import",
        "mb4-correction-legitimacy",
        "mb5-successor-ontology-shift",
        "mb6-selection-and-basin-stability",
        "mb7-hidden-capability-and-access",
        "mb8-cev-process-convergence",
        "mb9-grounding-certificate",
        "mb10-successor-forgeability",
        "evidence-and-uncertainty",
        "what-not-claiming"
      ],
      bodyExtra:
        "This appendix maps each formal bridge (MB1–MB10) to the alignment field's canonical open problems and names where the book shares an agenda versus where it adds structure. Use the crosswalk table for the field mapping; bridge cards, concept cards, and book chapters are in the sidebar."
    },
    { id: "appC", file: "appendices/appC-institutional-translation.tex", type: "appendix", title: "Human Institutions as Alignment Translation Guide" },
    {
      id: "appM",
      file: "appendices/appM-institutional-histories.tex",
      type: "appendix",
      title: "Institutional Genesis, Memory, and Decay: Historical Case Studies",
      overviewOnly: true,
      related: [
        "institutional-genesis-money-at-risk",
        "institutional-genesis-catastrophe-ratchet",
        "institutional-genesis-chronic-threat",
        "institutional-evidence-before-authority",
        "institutional-selection-gating",
        "institutional-constraint-inheritance",
        "institutional-memory-refresh",
        "institutional-entrenchment-corrigibility",
        "institutional-reform-decay",
        "institutional-dual-mandate-genesis",
        "institutional-capability-latency-gap"
      ],
      bodyExtra:
        "Appendix C maps the book's technical vocabulary onto institutional language. This appendix asks a different question: how did any of those institutional correction mechanisms come to exist, what kept them working once they existed, and what specifically broke when they failed?\n\nEleven historical cases, one per mechanism, are read in life-cycle order: genesis (from money at risk, from catastrophe, or from chronic threat), stabilization (evidence before authority, selection gating, constraint inheritance across successors, memory refresh through succession), hardening (entrenchment), and failure (reform decay, dual-mandate genesis, capability-jump latency).\n\nThe central disanalogy runs through the whole appendix: the catastrophe-ratchet genesis route, which produced most of the strongest human correction regimes, requires a catastrophe survivable enough that the polity persists to reform. If an AI failure at the relevant capability level is unbounded or irreversible, that route is unavailable exactly when it is needed most — which is why the money-at-risk and chronic-threat genesis routes, and the memory-refresh and entrenchment mechanisms that do not depend on remembering a specific disaster, matter more for AI governance than for institutional history generally.\n\nUse the case study cards below for the mechanism-by-mechanism treatment. For the complete historical narrative and bibliography, [read the full appendix on site](full/) or [download the PDF](../../../towards-superintelligence-alignment.pdf)."
    },
    { id: "appD", file: "appendices/appD-worked-example.tex", type: "appendix", title: "Worked Example" },
    { id: "appF", file: "appendices/appF-research-program.tex", type: "appendix", title: "Research Program" }
  ];

  for (const spec of appendixSpecs) {
    const tex = await readFile(path.join(repoRoot, spec.file), "utf8");
    const thesis = extractChapterThesis(tex);
    const titleMatch = tex.match(/\\chapter\{([^}]+)\}/);
    const title = titleMatch ? titleMatch[1].replace(/\\[^ {}]+(?:\{[^}]*\})?/g, "").trim() : spec.title;
    const bookLabel = extractAppendixLabel(tex) || spec.id;

    const md = [
      cardFrontmatter({
        title,
        type: spec.type,
        status: "reviewed",
        summary: thesis || title,
        bookPageId: spec.id,
        bookLabel,
        overviewOnly: spec.overviewOnly,
        related: spec.related ?? relatedByChapter.get(spec.id) ?? []
      }),
      cardBody({
        title,
        type: spec.type,
        summary: thesis || title,
        bookPageId: spec.id,
        overviewOnly: spec.overviewOnly,
        bodyExtra: spec.bodyExtra
      })
    ].join("\n");

    await writeFile(path.join(outDir, `${spec.id}.md`), md, "utf8");
    count += 1;
  }

  const frontmatterTex = await readFile(path.join(repoRoot, "frontmatter", "introduction.tex"), "utf8");
  const introBrief = stripComments(frontmatterTex).match(/\\section\*\{In Brief\}([\s\S]*?)\\section\*\{/)?.[1]
    ?.replace(/\\emph\{([^}]*)\}/g, "$1")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 320);

  const frontmatterMd = [
    cardFrontmatter({
      title: "Front Matter",
      type: "frontmatter",
      status: "reviewed",
      summary: introBrief || "Preface, introduction, roadmap, and executive overview.",
      bookPageId: "frontmatter",
      bookLabel: "frontmatter",
      related: []
    }),
    cardBody({
      title: "Front Matter",
      type: "frontmatter",
      summary: introBrief || "Preface, introduction, roadmap, and executive overview.",
      bookPageId: "frontmatter"
    })
  ].join("\n");

  await writeFile(path.join(outDir, "frontmatter.md"), frontmatterMd, "utf8");
  count += 1;

  console.log(`Wrote ${count} chapter cards to src/content/cards/chapters/`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
