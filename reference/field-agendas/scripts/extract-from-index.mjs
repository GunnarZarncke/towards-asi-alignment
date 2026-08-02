// One-time (and repeatable) extractor: field-agenda-index.md → structured YAML under data/.
// Usage: node reference/field-agendas/scripts/extract-from-index.mjs
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "../../../site");
const yaml = (await import(pathToFileURL(path.join(siteRoot, "node_modules/js-yaml/index.js")).href)).default;
const root = path.resolve(scriptDir, "..");
const { normalizeMatrixCell } = await import("./matrix-cell.mjs");
const dataDir = path.join(root, "data");
const agendasDir = path.join(dataDir, "agendas");

/** Short matrix row labels → agenda slug (when title differs). */
const MATRIX_AGENDA_SLUG = {
  MIRI: "miri",
  Redwood: "redwood-research",
  CHAI: "chai-russell",
  Christiano: "christiano-lineage",
  ARC: "arc-alignment-research-center",
  GSAI: "davidad-guaranteed-safe-ai-gsai",
  "Anthropic (lab)": "anthropic-lab",
  "Google DeepMind": "google-deepmind-safety",
  Apollo: "apollo-research",
  METR: "metr",
  Resolution: "resolution",
  "AE Studio": "ae-studio",
  Orthogonal: "orthogonal",
  Wentworth: "wentworth-natural-abstractions",
  "Kosoy / IB & LTA": "kosoy-infra-bayesianism-lta",
  "Kosoy / PreDCA": "kosoy-predca",
  CIRIS: "ciris",
  GovAI: "govai",
  "UK AISI / CAISI": "uk-aisi-caisi-gov-eval-institutes",
  "Pause cluster": "pause-standards-advocacy-cluster",
  CLR: "clr-cooperation-conflict",
  "Truthful AI": "truthful-ai-evans",
  "Goodfire / MI": "goodfire-mechanistic-interpretability-cluster",
  "AI Futures": "ai-futures-forecasting-cluster",
  "FAR.AI": "farai",
  Conjecture: "conjecture-cognitive-emulation",
  TSA: "this-project-towards-superintelligence-alignment-tsa"
};

function matrixSlugFor(agendaLabel, roster) {
  if (MATRIX_AGENDA_SLUG[agendaLabel]) return MATRIX_AGENDA_SLUG[agendaLabel];
  const hit = roster.find((r) => r.title === agendaLabel);
  return hit?.slug ?? slugify(agendaLabel);
}

function slugify(title) {
  return title
    .toLowerCase()
    .replace(/\*\*/g, "")
    .replace(/[^\w\s/-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/\//g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function parseLinks(line) {
  const links = [];
  const re = /\[([^\]]+)\]\(([^)]+)\)/g;
  let m;
  while ((m = re.exec(line)) !== null) {
    links.push({ label: m[1], url: m[2] });
  }
  return links;
}

function parseAgendaSection(text) {
  const agendas = [];
  const section = text.match(/## Agendas\n([\s\S]*?)\n---\n\n## Coverage vs book treatment/)?.[1];
  if (!section) throw new Error("Agendas section not found");

  const blocks = section.split(/\n### /).slice(1);
  for (const block of blocks) {
    const lines = block.split("\n");
    const title = lines[0].trim();
    const slug = slugify(title);
    const fields = {};
    for (const line of lines.slice(1)) {
      const m = line.match(/^- \*\*([^:]+):\*\* (.+)$/);
      if (!m) continue;
      const key = m[1].trim();
      const value = m[2].trim();
      if (key === "Links") {
        fields.links = parseLinks(value);
      } else if (key === "Book bridges") {
        fields.bookBridges = value === "—" ? [] : value.split(/,\s*/);
      } else if (key === "Manuscript hooks") {
        fields.manuscriptHooks = value.split(/;\s*/);
      } else {
        const camel = key
          .replace(/\s+/g, " ")
          .replace(/[^a-zA-Z0-9 ]/g, "")
          .split(" ")
          .map((w, i) => (i === 0 ? w.toLowerCase() : w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()))
          .join("");
        fields[camel] = value;
      }
    }
    agendas.push({ slug, title, ...fields });
  }
  return agendas;
}

function parseEvidenceCatalog(text) {
  const section = text.match(/### Coverage evidence catalog[^\n]*\n\n([\s\S]*?)\n\n\*\*Maintenance:\*\*/)?.[1];
  if (!section) throw new Error("Evidence catalog not found");
  const entries = [];
  const rows = section.split("\n").slice(2); // skip header rows
  for (const row of rows) {
    if (!row.startsWith("|")) continue;
    const cells = row
      .split("|")
      .slice(1, -1)
      .map((c) => c.trim());
    if (cells.length < 6 || cells[0].startsWith("---")) continue;
    const idMatch = cells[0].match(/id="ev-(\d+)"/) ?? cells[0].match(/^(\d+)$/);
    const id = idMatch ? Number(idMatch[1]) : Number(cells[0].replace(/<[^>]+>/g, ""));
    if (!id) continue;
    const bridgeCell = cells[2];
    const bridges = bridgeCell.split(/,\s*/).map((b) => b.trim());
    const sourceLinks = parseLinks(cells[5]);
    entries.push({
      id,
      agenda: cells[1],
      bridges,
      type: cells[3],
      evidence: cells[4],
      sources: sourceLinks
    });
  }
  return entries;
}

function parseMatrix(text) {
  const section = text.match(/## Coverage matrix \(agenda × bridge\)\n\n([\s\S]*?)\n\n### Coverage evidence catalog/)?.[1];
  if (!section) throw new Error("Matrix section not found");
  const lines = section.split("\n");
  const headerIdx = lines.findIndex((l) => l.startsWith("| Agenda |"));
  if (headerIdx < 0) throw new Error("Matrix header not found");
  const headerLine = lines[headerIdx];
  const columns = headerLine
    .split("|")
    .slice(2, -1)
    .map((c) => c.trim());

  const rows = [];
  for (const line of lines.slice(headerIdx + 2)) {
    if (!line.startsWith("|")) break;
    if (line.startsWith("|---")) continue;
    const cells = line
      .split("|")
      .slice(1, -1)
      .map((c) => c.trim());
    if (cells.length < 2) continue;
    const agenda = cells[0].replace(/\*\*/g, "").trim();
    const cellMap = {};
    for (let i = 0; i < columns.length; i++) {
      cellMap[columns[i]] = normalizeMatrixCell(cells[i + 1] ?? "—");
    }
    rows.push({ agenda, cells: cellMap });
  }
  return { columns, rows };
}

function parseClustering(text) {
  const section = text.match(/## Map → agenda clustering[^\n]*\n\n([\s\S]*?)\n\n---\n\n## Maintenance/)?.[1];
  if (!section) throw new Error("Clustering section not found");
  const rows = [];
  for (const line of section.split("\n").slice(2)) {
    if (!line.startsWith("|")) continue;
    const cells = line
      .split("|")
      .slice(1, -1)
      .map((c) => c.trim());
    if (cells.length < 2 || cells[0].startsWith("---")) continue;
    const rollsUpLinks = parseLinks(cells[1]);
    const anchor = rollsUpLinks.find((l) => l.url.startsWith("#"))?.url.slice(1);
    rows.push({
      listings: cells[0],
      listingLinks: parseLinks(cells[0]),
      rollsUpTo: cells[1],
      rollsUpLinks,
      rollsUpSlug: anchor ?? null
    });
  }
  return rows;
}

function parseMeta(text) {
  const statusLine = text.match(/^\*\*Status:\*\* (.+)$/m)?.[1] ?? "";
  const inclusion = text.match(/## Inclusion test\n\n([\s\S]*?)\n\n---/)?.[1]?.trim() ?? "";
  const spineTranslation = text.match(/### How to read matrix cells[^\n]*\n\n([\s\S]*?)\n\n\*\*Do not infer/)?.[1]?.trim() ?? "";
  const doNotInfer = text.match(/\*\*Do not infer from cells alone:\*\* ([^\n]+)/)?.[1] ?? "";
  const kosoyDiagnostic = text.match(/\*\*Kosoy diagnostic:\*\* ([^\n]+)/)?.[1] ?? "";
  const openInterfaces = text.match(/\*\*Open spine interfaces\*\*[^\n]*\n\n([^\n]+)/)?.[1] ?? "";
  const typeLetters = text.match(/\*\*Type letters\*\*[^\n]*\n\n([\s\S]*?)\n\n\| Agenda \|/)?.[1] ?? "";
  const coverageIntro = text.match(/## Coverage vs book treatment[^\n]*\n\n([\s\S]*?)\n\n### How to read matrix/)?.[1]?.trim() ?? "";
  const matrixIntro = text.match(/## Coverage matrix \(agenda × bridge\)\n\n([\s\S]*?)\n\nEach cell lists/)?.[1]?.trim() ?? "";
  const matrixLegend = text.match(/Each cell lists \*\*typed evidence tags\*\*[^\n]*\n\n([\s\S]*?)\n\n\*\*Type letters\*\*/)?.[1]?.trim() ?? "";
  const excludedNote = text.match(/\*\*Excluded from matrix rows\*\*[^\n]*\n\n([^\n]+)/)?.[1] ?? "";
  return {
    status: statusLine,
    inclusionTest: inclusion,
    coverageIntro,
    spineTranslation,
    doNotInfer,
    kosoyDiagnostic,
    openSpineInterfaces: openInterfaces,
    typeLettersTable: typeLetters,
    matrixIntro,
    matrixLegend,
    excludedFromMatrix: excludedNote
  };
}

async function main() {
  const indexPath = path.join(root, "field-agenda-index.md");
  const text = await readFile(indexPath, "utf8");

  const meta = parseMeta(text);
  const agendas = parseAgendaSection(text);
  const evidence = parseEvidenceCatalog(text);
  const matrix = parseMatrix(text);
  const clustering = parseClustering(text);

  await mkdir(agendasDir, { recursive: true });

  const roster = agendas.map((a, i) => ({
    slug: a.slug,
    title: a.title,
    order: i + 1,
    inMatrix: matrix.rows.some((r) => matrixSlugFor(r.agenda, agendas) === a.slug)
  }));

  const matrixWithSlugs = {
    columns: matrix.columns,
    rows: matrix.rows.map((row) => ({
      ...row,
      slug: matrixSlugFor(row.agenda, agendas)
    }))
  };

  await writeFile(path.join(dataDir, "meta.yml"), yaml.dump(meta), "utf8");
  await writeFile(path.join(dataDir, "roster.yml"), yaml.dump({ agendas: roster }), "utf8");
  await writeFile(path.join(dataDir, "evidence.yml"), yaml.dump({ evidence }), "utf8");
  await writeFile(path.join(dataDir, "matrix.yml"), yaml.dump(matrixWithSlugs), "utf8");
  await writeFile(path.join(dataDir, "clustering.yml"), yaml.dump({ clustering }), "utf8");

  for (const agenda of agendas) {
    const { slug, title, ...rest } = agenda;
    await writeFile(path.join(agendasDir, `${slug}.yml`), yaml.dump({ slug, title, ...rest }), "utf8");
  }

  console.log(
    `extract-from-index: ${agendas.length} agendas, ${evidence.length} evidence entries, ${matrix.rows.length} matrix rows, ${clustering.length} clustering rows`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
