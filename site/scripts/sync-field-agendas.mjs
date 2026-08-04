// Generates field agenda cards, field-agendas.json, and regenerates field-agenda-index.md
// from reference/field-agendas/data/ (single source of truth).
//
// Usage: node scripts/sync-field-agendas.mjs [--check]
import { readFile, writeFile, readdir, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import {
  matrixCellToMarkdown,
  normalizeMatrix,
  normalizeMatrixCell
} from "../../reference/field-agendas/scripts/matrix-cell.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const dataRoot = path.join(repoRoot, "reference", "field-agendas", "data");
const cardsDir = path.join(siteRoot, "src", "content", "cards", "field-agendas");
const indexPath = path.join(repoRoot, "reference", "field-agendas", "field-agenda-index.md");

function buildMbBridgeCards(bridgeRows) {
  const map = {};
  for (const row of bridgeRows) {
    map[row.key] = row.cardSlug;
  }
  return map;
}

function bridgeByKey(bridgeRows) {
  return Object.fromEntries(bridgeRows.map((row) => [row.key, row]));
}

function yamlScalar(v) {
  return JSON.stringify(v);
}

function yamlBlockList(key, items) {
  if (!items?.length) return `${key}: []`;
  return [`${key}:`, ...items.map((item) => `  - ${yamlScalar(item)}`)].join("\n");
}

function yamlExternalLinks(links) {
  if (!links?.length) return "external: []";
  return [
    "external:",
    ...links.map((l) => `  - label: ${yamlScalar(l.label)}\n    url: ${yamlScalar(l.url)}`)
  ].join("\n");
}

function agendaSummary(agenda) {
  const raw = agenda.primaryCrux || agenda.statedIntent || agenda.title;
  // Strip markdown links for the short card teaser.
  return String(raw).replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/\s+/g, " ").trim();
}

function normalizeBridgeKeys(items) {
  if (!items?.length) return [];
  const keys = [];
  for (const item of items) {
    if (typeof item !== "string") continue;
    for (const match of item.matchAll(/\bMB\d+[a-z]?\b/g)) {
      if (!keys.includes(match[0])) keys.push(match[0]);
    }
  }
  return keys;
}

function formatBridgeLinks(bridgeKeys, bridgeRows) {
  const byKey = bridgeByKey(bridgeRows);
  return bridgeKeys
    .map((key) => {
      const row = byKey[key];
      if (!row?.cardSlug) return null;
      return `[${row.noun}](/cards/${row.cardSlug}/)`;
    })
    .filter(Boolean)
    .join("; ");
}

function clusteringForSlug(slug, clustering) {
  return clustering.filter((row) => row.rollsUpSlug === slug);
}

function renderAgendaBody(agenda, clusteringRows, bridgeRows) {
  const lines = [];
  const bridgeKeys = normalizeBridgeKeys(agenda.bookBridges);
  lines.push(`## Introduction`);
  lines.push("");
  if (agenda.overview) {
    lines.push(agenda.overview);
    lines.push("");
    if (agenda.carrier) {
      lines.push(`**Who carries it:** ${agenda.carrier}`);
      lines.push("");
    }
  } else {
    lines.push(
      `**${agenda.title}** is a ${(agenda.type || "research agenda").toLowerCase()} carried by **${agenda.carrier}**.`
    );
    lines.push("");
  }
  if (agenda.statedIntent) {
    lines.push(`**What they aim to do.** ${agenda.statedIntent}`);
    lines.push("");
  }
  if (agenda.primaryCrux) {
    lines.push(`**The hard question.** ${agenda.primaryCrux}`);
    lines.push("");
  }
  if (agenda.primaryArtifact) {
    lines.push(`**What they produce.** ${agenda.primaryArtifact}`);
    lines.push("");
  }
  if (agenda.signatureVocabulary) {
    lines.push(`**Key terms.** ${agenda.signatureVocabulary}`);
    lines.push("");
  }
  if (bridgeKeys.length) {
    lines.push(`**Related field cruxes.** ${formatBridgeLinks(bridgeKeys, bridgeRows)}`);
    lines.push("");
  }
  if (agenda.contributes) {
    lines.push(`**What they contribute.** ${agenda.contributes}`);
    lines.push("");
  }
  if (agenda.bookSeparates) {
    lines.push(`**How this book treats it.** ${agenda.bookSeparates}`);
    lines.push("");
  }
  if (agenda.reviewStatus) {
    lines.push(`**Current status.** ${agenda.reviewStatus}`);
    lines.push("");
  }
  if (agenda.links?.length) {
    lines.push(`## Links`);
    lines.push("");
    for (const link of agenda.links) {
      lines.push(`- [${link.label}](${link.url})`);
    }
    lines.push("");
  }
  if (clusteringRows.length) {
    lines.push(`## Map clustering`);
    lines.push("");
    lines.push(`AISafety.com map listings that roll up to this agenda:`);
    lines.push("");
    for (const row of clusteringRows) {
      lines.push(`- ${row.listings} → ${row.rollsUpTo}`);
    }
    lines.push("");
  }
  lines.push(
    `See the [coverage matrix](/field/#coverage-matrix) for evidence tagged to this agenda, and the [glossary](/glossary/) for shared terms.`
  );
  return lines.join("\n");
}

function renderAgendaCard(agenda, clusteringRows, bridgeRows) {
  const bridgeKeys = normalizeBridgeKeys(agenda.bookBridges);
  const fm = [
    "---",
    `title: ${yamlScalar(agenda.title)}`,
    `type: "agenda"`,
    `status: "reviewed"`,
    `summary: ${yamlScalar(agendaSummary(agenda))}`,
    `agendaSlug: ${yamlScalar(agenda.slug)}`,
    yamlBlockList("bookBridges", bridgeKeys),
    yamlExternalLinks(agenda.links),
    "related: []",
    "---",
    "",
    renderAgendaBody(agenda, clusteringRows, bridgeRows)
  ].join("\n");
  return fm;
}

async function loadAgendas() {
  const dir = path.join(dataRoot, "agendas");
  const files = (await readdir(dir)).filter((f) => f.endsWith(".yml")).sort();
  const agendas = [];
  for (const file of files) {
    const raw = yaml.load(await readFile(path.join(dir, file), "utf8"));
    agendas.push(raw);
  }
  return agendas;
}

async function loadYaml(name) {
  return yaml.load(await readFile(path.join(dataRoot, name), "utf8"));
}

function renderIndexMarkdown(meta, roster, agendas, matrix, evidence, clustering, bridgeRows) {
  const bridgeMap = bridgeByKey(bridgeRows);
  const lines = [];
  lines.push("# Field agenda index");
  lines.push("");
  lines.push(`**Status:** ${meta.status}`);
  lines.push(`**Term glossary:** [\`inter-agenda-term-glossary.md\`](inter-agenda-term-glossary.md) (alphabetical; TSA integration deferred)`);
  lines.push(`**Bridge map:** [App B (companion)](https://towards-alignment.com/cards/chapters/appb/) · [Lean spine](https://towards-alignment.com/lean/) · LaTeX source: [\`appendices/appB-bridge-crosswalk.tex\`](../../appendices/appB-bridge-crosswalk.tex)`);
  lines.push(`**Field hub (companion):** [towards-alignment.com/field/](https://towards-alignment.com/field/)`);
  lines.push("");
  lines.push("## Inclusion test");
  lines.push("");
  lines.push(meta.inclusionTest);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## Agendas");
  lines.push("");
  for (const agenda of agendas) {
    lines.push(`### ${agenda.title}`);
    lines.push("");
    if (agenda.overview) {
      lines.push(agenda.overview);
      lines.push("");
    }
    if (agenda.type) lines.push(`- **Type:** ${agenda.type}`);
    if (agenda.carrier) lines.push(`- **Carrier:** ${agenda.carrier}`);
    if (agenda.primaryArtifact) lines.push(`- **Primary artifact:** ${agenda.primaryArtifact}`);
    if (agenda.signatureVocabulary) lines.push(`- **Signature vocabulary:** ${agenda.signatureVocabulary}`);
    if (agenda.statedIntent) lines.push(`- **Stated intent:** ${agenda.statedIntent}`);
    if (agenda.primaryCrux) lines.push(`- **Primary crux:** ${agenda.primaryCrux}`);
    {
      const keys = normalizeBridgeKeys(agenda.bookBridges);
      if (keys.length) {
        const labeled = keys.map((key) => {
          const row = bridgeMap[key];
          return row ? `${row.noun} (${key})` : key;
        });
        lines.push(`- **Field cruxes:** ${labeled.join("; ")}`);
      } else if (agenda.bookBridges) lines.push(`- **Field cruxes:** —`);
    }
    if (agenda.contributes) lines.push(`- **Contributes:** ${agenda.contributes}`);
    if (agenda.bookSeparates) lines.push(`- **Book separates:** ${agenda.bookSeparates}`);
    if (agenda.reviewStatus) lines.push(`- **Review status:** ${agenda.reviewStatus}`);
    if (agenda.manuscriptHooks?.length) lines.push(`- **Manuscript hooks:** ${agenda.manuscriptHooks.join("; ")}`);
    if (agenda.links?.length) {
      lines.push(`- **Links:** ${agenda.links.map((l) => `[${l.label}](${l.url})`).join("; ")}`);
    }
    lines.push("");
  }
  lines.push("---");
  lines.push("");
  lines.push("## Coverage vs book treatment {#coverage-vs-book-treatment}");
  lines.push("");
  lines.push(meta.coverageIntro);
  lines.push("");
  lines.push("### How to read matrix cells (spine translation) {#spine-translation}");
  lines.push("");
  lines.push(meta.spineTranslation);
  lines.push("");
  lines.push(`**Do not infer from cells alone:** ${meta.doNotInfer}`);
  lines.push("");
  lines.push(`**Kosoy diagnostic:** ${meta.kosoyDiagnostic}`);
  lines.push("");
  lines.push(`**Open spine interfaces** (vocabulary, not matrix columns): ${meta.openSpineInterfaces}`);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## Coverage matrix (agenda × bridge)");
  lines.push("");
  lines.push(meta.matrixIntro);
  lines.push("");
  if (meta.matrixLegend) {
    lines.push(meta.matrixLegend);
    lines.push("");
  }
  lines.push("**Type letters** (prefix on each tag; full definitions in catalog **Type** column):");
  lines.push("");
  lines.push(meta.typeLettersTable);
  lines.push("");
  const columnLabels = matrix.columns.map((col) => {
    const row = bridgeMap[col];
    return row ? `${row.noun} (${col})` : col;
  });
  const header = ["Agenda", ...columnLabels].join(" | ");
  const sep = ["---", ...matrix.columns.map(() => "---")].join(" | ");
  lines.push(`| ${header} |`);
  lines.push(`| ${sep} |`);
  for (const row of matrix.rows) {
    const agendaMeta = agendas.find((a) => a.slug === row.slug);
    const agendaLabel =
      agendaMeta?.matrixLink != null
        ? `[${row.agenda}](${agendaMeta.matrixLink})`
        : row.agenda;
    const cells = [
      agendaLabel,
      ...matrix.columns.map((col) => matrixCellToMarkdown(normalizeMatrixCell(row.cells[col])))
    ];
    lines.push(`| ${cells.join(" | ")} |`);
  }
  lines.push("");
  lines.push(`**Excluded from matrix rows** (see [Inclusion test](#inclusion-test)): ${meta.excludedFromMatrix}`);
  lines.push("");
  lines.push("### Coverage evidence catalog {#coverage-evidence-catalog}");
  lines.push("");
  lines.push("| ID | Agenda | Bridge | Type | Evidence (one line) | Source |");
  lines.push("|---|---|---|---|---|---|");
  for (const ev of evidence) {
    const src = ev.sources.map((s) => `[${s.label}](${s.url})`).join("; ");
    lines.push(`| <a id="ev-${ev.id}"></a>${ev.id} | ${ev.agenda} | ${ev.bridges.join(", ")} | ${ev.type} | ${ev.evidence} | ${src} |`);
  }
  lines.push("");
  lines.push("**Maintenance:** when adding an agenda row or bridge cell, edit YAML under `reference/field-agendas/data/` and run `cd site && npm run sync:field-agendas`. Prefer bibliography keys already in `references/` when citing external work.");
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## Map → agenda clustering (selected listings)");
  lines.push("");
  lines.push("| Map listing(s) | Rolls up to agenda |");
  lines.push("|---|---|");
  for (const row of clustering) {
    lines.push(`| ${row.listings} | ${row.rollsUpTo} |`);
  }
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## Maintenance");
  lines.push("");
  lines.push("- Source of truth: `reference/field-agendas/data/` — regenerate this file and site cards with `npm run sync:field-agendas` in `site/`.");
  lines.push("- Refresh clustering when AISafety.com map updates (Airtable export).");
  lines.push("- New signature vocabulary → add headword(s) to [`inter-agenda-term-glossary.md`](inter-agenda-term-glossary.md).");
  lines.push("");
  return lines.join("\n");
}

async function writeFileCheck(filePath, contents, check, mismatches) {
  if (check) {
    let existing = "";
    try {
      existing = await readFile(filePath, "utf8");
    } catch {}
    if (existing !== contents) mismatches.push(filePath);
  } else {
    await mkdir(path.dirname(filePath), { recursive: true });
    await writeFile(filePath, contents, "utf8");
  }
}

async function main() {
  const check = process.argv.includes("--check");
  const meta = await loadYaml("meta.yml");
  const { agendas: roster } = await loadYaml("roster.yml");
  const agendas = await loadAgendas();
  const matrixRaw = await loadYaml("matrix.yml");
  const matrix = normalizeMatrix(matrixRaw);
  const { evidence } = await loadYaml("evidence.yml");
  const { clustering } = await loadYaml("clustering.yml");
  const { bridges: bridgeRows } = await loadYaml("bridges.yml");
  const mbBridgeCards = buildMbBridgeCards(bridgeRows);

  const mismatches = [];
  const matrixPath = path.join(dataRoot, "matrix.yml");

  await writeFileCheck(matrixPath, yaml.dump(matrix), check, mismatches);

  for (const agenda of agendas) {
    if (agenda.generateCard === false) continue;
    const clusterRows = clustering.filter((row) => row.rollsUpSlug === agenda.slug);
    const card = renderAgendaCard(agenda, clusterRows, bridgeRows);
    await writeFileCheck(path.join(cardsDir, `${agenda.slug}.md`), card, check, mismatches);
  }

  const jsonData = {
    meta,
    roster,
    agendas: agendas.map((a) => ({
      slug: a.slug,
      title: a.title,
      summary: agendaSummary(a),
      bookBridges: normalizeBridgeKeys(a.bookBridges),
      inMatrix: roster.find((r) => r.slug === a.slug)?.inMatrix ?? false,
      generateCard: a.generateCard !== false,
      matrixLink: a.matrixLink ?? null
    })),
    matrix,
    evidence,
    clustering,
    bridges: bridgeRows,
    mbBridgeCards
  };
  const jsonPath = path.join(siteRoot, "src", "data", "field-agendas.json");
  const jsonContents = JSON.stringify(jsonData, null, 2) + "\n";
  await writeFileCheck(jsonPath, jsonContents, check, mismatches);

  const indexMd = renderIndexMarkdown(meta, roster, agendas, matrix, evidence, clustering, bridgeRows);
  await writeFileCheck(indexPath, indexMd, check, mismatches);

  if (check && mismatches.length > 0) {
    console.error(`sync-field-agendas --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(
    `sync-field-agendas: ${agendas.length} agenda cards, field-agendas.json, index markdown (${check ? "check ok" : "generated"}).`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
