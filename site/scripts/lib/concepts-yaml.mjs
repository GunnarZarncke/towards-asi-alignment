// Shared loader/writer for the metadata/concepts.yml, metadata/bridges.yml, and
// metadata/projections.yml roster files. Roster entries are internal (kind, id,
// fieldCrux, ...); generated site cards only ever get the public content.config.ts
// fields (title, type, status, summary, ...).
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import yaml from "js-yaml";

export function repoPaths(siteRoot) {
  const repoRoot = path.resolve(siteRoot, "..");
  return {
    repoRoot,
    metadataDir: path.join(repoRoot, "metadata"),
    bodiesDir: path.join(repoRoot, "metadata", "concepts", "bodies"),
    cardsDir: path.join(siteRoot, "src", "content", "cards")
  };
}

export async function loadYaml(filePath) {
  const text = await readFile(filePath, "utf8");
  return yaml.load(text) || {};
}

export async function loadBody(bodiesDir, relPath) {
  const text = await readFile(path.join(bodiesDir, path.basename(relPath)), "utf8");
  const m = text.match(/^---\n([\s\S]*?)\n---\n?\n?([\s\S]*)$/);
  if (!m) return { fm: {}, body: text.trim() };
  return { fm: yaml.load(m[1]) || {}, body: m[1] === undefined ? text : m[2].trim() };
}

function yamlScalar(value) {
  return JSON.stringify(value);
}

function yamlBlockList(key, items) {
  if (!items || items.length === 0) return null;
  return [`${key}:`, ...items.map((item) => `  - ${yamlScalar(item)}`)].join("\n");
}

function yamlObjectList(key, items) {
  if (!items || items.length === 0) return null;
  const lines = [`${key}:`];
  for (const item of items) {
    const entries = Object.entries(item);
    entries.forEach(([k, v], i) => {
      const prefix = i === 0 ? "  - " : "    ";
      lines.push(`${prefix}${k}: ${yamlScalar(v)}`);
    });
  }
  return lines.join("\n");
}

/** LaTeX-style `\(...\)` / `\[...\]` delimiters are stripped by CommonMark before remark-math runs. */
export function normalizeMarkdownMath(text) {
  if (!text) return text;
  let out = text.replace(/\\\[([\s\S]*?)\\\]/g, (_, inner) => `$$\n${inner.trim()}\n$$`);
  out = out.replace(/\\\(([\s\S]*?)\\\)/g, (_, inner) => `$${inner.trim()}$`);
  return out;
}

/**
 * Build the frontmatter + body text for a generated card from a merged roster
 * row (public fields only) and a parsed body file ({ fm, body }).
 */
export function renderCard(publicFields, bodyFmFields, bodyText) {
  const lines = ["---"];
  const simpleKeys = [
    "title", "type", "status", "summary", "decision", "evidence", "bookPageId",
    "overviewOnly", "bibKey", "experimentLineId", "releasedAt", "eventDate", "version",
    "part", "formalDensity", "claimId"
  ];
  for (const key of simpleKeys) {
    if (publicFields[key] === undefined || publicFields[key] === null) continue;
    lines.push(`${key}: ${yamlScalar(publicFields[key])}`);
  }
  for (const key of ["bookChapters", "bookLabels", "citedIn", "citeKeys"]) {
    const rendered = yamlBlockList(key, publicFields[key] ?? bodyFmFields[key]);
    if (rendered) lines.push(rendered);
  }
  for (const key of ["bookSections", "formulas", "leanNodes", "evidenceNotes", "demos", "external"]) {
    const val = bodyFmFields[key];
    if (!val || val.length === 0) continue;
    lines.push(renderNestedList(key, val));
  }
  const related = bodyFmFields.related;
  const relatedRendered = yamlBlockList("related", related);
  if (relatedRendered) lines.push(relatedRendered);

  lines.push("---", "");
  const bodyParts = [];
  if (publicFields.overviewOnly) {
    // overview-only chapter/appendix cards omit the summary paragraph (handled by callers).
  }
  if (bodyText) bodyParts.push(normalizeMarkdownMath(bodyText.trim()));
  return lines.join("\n") + "\n" + bodyParts.join("\n\n") + "\n";
}

function renderNestedList(key, items) {
  const lines = [`${key}:`];
  for (const item of items) {
    const entries = Object.entries(item);
    entries.forEach(([k, v], i) => {
      const prefix = i === 0 ? "  - " : "    ";
      if (Array.isArray(v)) {
        lines.push(`${prefix}${k}:`);
        for (const sub of v) lines.push(`      - ${yamlScalar(sub)}`);
      } else {
        lines.push(`${prefix}${k}: ${yamlScalar(v)}`);
      }
    });
  }
  return lines.join("\n");
}

export async function writeCard(cardsDir, slug, contents, { check = false, dir = "" } = {}) {
  const outDir = dir ? path.join(cardsDir, dir) : cardsDir;
  await mkdir(outDir, { recursive: true });
  const filePath = path.join(outDir, `${slug}.md`);
  if (check) {
    let existing = "";
    try {
      existing = await readFile(filePath, "utf8");
    } catch {
      // file does not exist yet
    }
    return { filePath, matches: existing === contents, existing, contents };
  }
  await writeFile(filePath, contents, "utf8");
  return { filePath, matches: true };
}
