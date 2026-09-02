// Generates site/src/data/product-comparison.json from reference/field-agendas/data/product-comparison.yml
//
// Usage: node scripts/sync-product-comparison.mjs [--check]
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const dataRoot = path.join(repoRoot, "reference", "field-agendas", "data");
const outPath = path.join(siteRoot, "src", "data", "product-comparison.json");
const SYNC_CMD = "cd site && npm run sync:product-comparison";

const TSA_SLUG = "this-project-towards-superintelligence-alignment-tsa";
const BOTTOM_FEATURE_IDS = ["ships-usable-product", "living-communal-canon"];

async function loadYaml(name) {
  return yaml.load(await readFile(path.join(dataRoot, name), "utf8"));
}

function normalizeMark(mark) {
  const m = String(mark ?? "dash").toLowerCase();
  if (m === "yes" || m === "some" || m === "dash") return m;
  if (m === "—" || m === "-") return "dash";
  throw new Error(`Invalid mark "${mark}" — use yes, some, or dash`);
}

function displayMark(mark) {
  if (mark === "yes") return "Yes";
  if (mark === "some") return "Some";
  return "No";
}

function orderFeatures(features) {
  const list = [...features];
  const bottom = list.filter((f) => BOTTOM_FEATURE_IDS.includes(f.id));
  const top = list.filter((f) => !BOTTOM_FEATURE_IDS.includes(f.id));
  return [...top, ...bottom];
}

function orderColumns(columns, rosterBySlug) {
  return [...columns].sort((a, b) => {
    if (a.slug === TSA_SLUG) return -1;
    if (b.slug === TSA_SLUG) return 1;
    const oa = rosterBySlug[a.slug]?.order ?? 999;
    const ob = rosterBySlug[b.slug]?.order ?? 999;
    return oa - ob;
  });
}

async function main() {
  const check = process.argv.includes("--check");
  const doc = await loadYaml("product-comparison.yml");
  const { agendas: roster } = await loadYaml("roster.yml");
  const agendaFiles = await import("node:fs/promises").then((fs) =>
    fs.readdir(path.join(dataRoot, "agendas"))
  );
  const agendaBySlug = {};
  for (const file of agendaFiles.filter((f) => f.endsWith(".yml"))) {
    const raw = yaml.load(await readFile(path.join(dataRoot, "agendas", file), "utf8"));
    agendaBySlug[raw.slug] = raw;
  }

  const rosterBySlug = Object.fromEntries(roster.map((r) => [r.slug, r]));

  const columns = [];
  for (const [slug, col] of Object.entries(doc.columns ?? {})) {
    const rosterRow = rosterBySlug[slug];
    const agenda = agendaBySlug[slug];
    if (!rosterRow) {
      throw new Error(`product-comparison column "${slug}" not in roster.yml`);
    }
    columns.push({
      slug,
      title: rosterRow.title ?? agenda?.title ?? slug,
      shortName: col.shortName ?? rosterRow.title?.split(/[\s(/]/)[0] ?? slug,
      bestFor: col.bestFor ?? "",
      skipIf: col.skipIf ?? "",
      inMatrix: rosterRow.inMatrix ?? false,
      generateCard: agenda?.generateCard !== false,
      matrixLink: agenda?.matrixLink ?? null,
      defaultVisible: col.defaultVisible ?? rosterRow.inMatrix ?? false,
      isTsa: slug === TSA_SLUG
    });
  }

  const orderedColumns = orderColumns(columns, rosterBySlug);
  const orderedFeatures = orderFeatures(doc.features ?? []);
  const featureIds = orderedFeatures.map((f) => f.id);

  const cellsRaw = doc.cells ?? {};
  const cells = [];
  for (const col of orderedColumns) {
    const row = cellsRaw[col.slug];
    if (!row) {
      throw new Error(`product-comparison.yml missing cells.${col.slug}`);
    }
    for (const featureId of featureIds) {
      const cell = row[featureId];
      if (!cell) {
        throw new Error(`product-comparison.yml missing cells.${col.slug}.${featureId}`);
      }
      const mark = normalizeMark(cell.mark);
      cells.push({
        feature: featureId,
        column: col.slug,
        mark,
        display: displayMark(mark),
        because: cell.because ?? ""
      });
    }
  }

  const payload = {
    _generated: `<!-- GENERATED FILE — do not edit. Source: reference/field-agendas/data/product-comparison.yml. Regenerate: ${SYNC_CMD} -->`,
    intro: doc.intro ?? "",
    caption: doc.caption ?? "",
    features: orderedFeatures,
    columns: orderedColumns,
    cells
  };

  const contents = JSON.stringify(payload, null, 2) + "\n";
  if (check) {
    let existing = "";
    try {
      existing = await readFile(outPath, "utf8");
    } catch {}
    if (existing !== contents) {
      console.error(`sync-product-comparison --check: out of date: ${path.relative(repoRoot, outPath)}`);
      process.exit(1);
    }
    console.log("sync-product-comparison: check ok.");
    return;
  }

  await mkdir(path.dirname(outPath), { recursive: true });
  await writeFile(outPath, contents, "utf8");
  console.log(`sync-product-comparison: ${orderedColumns.length} columns, ${cells.length} cells.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
