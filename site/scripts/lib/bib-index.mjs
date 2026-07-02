import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";

const KEY_RE = /@\w+\{([^,\s]+),/g;
const FIELD_RE = /^\s*([a-zA-Z_]+)\s*=\s*(\{[\s\S]*?\}|"[\s\S]*?"|\d+)\s*,?\s*$/gm;

function stripBraces(value) {
  let v = value.trim();
  if (v.startsWith("{") && v.endsWith("}")) v = v.slice(1, -1);
  if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1);
  return v.replace(/\s+/g, " ").trim();
}

function firstAuthorLast(author) {
  if (!author) return "Unknown";
  const first = author.split(/\s+and\s+/i)[0];
  const comma = first.match(/^([^,]+),/);
  if (comma) return comma[1].trim();
  const parts = first.trim().split(/\s+/);
  return parts[parts.length - 1];
}

function parseEntry(text) {
  const fields = {};
  let match;
  FIELD_RE.lastIndex = 0;
  while ((match = FIELD_RE.exec(text)) !== null) {
    fields[match[1].toLowerCase()] = stripBraces(match[2]);
  }
  return fields;
}

function resolvePublicationUrl(fields) {
  if (fields.url && /^https?:\/\//i.test(fields.url)) return fields.url;
  if (fields.howpublished && /^https?:\/\//i.test(fields.howpublished)) return fields.howpublished;
  const eprintType = (fields.eprinttype || fields.archiveprefix || "").toLowerCase();
  if (fields.eprint && eprintType.includes("arxiv")) {
    return `https://arxiv.org/abs/${fields.eprint}`;
  }
  return "";
}

export function buildBibIndex(repoRoot) {
  const refsDir = path.join(repoRoot, "references");
  const index = new Map();

  for (const file of readdirSync(refsDir)) {
    if (!file.endsWith(".bib")) continue;
    const text = readFileSync(path.join(refsDir, file), "utf8");
    const chunks = text.split(/(?=@\w+\{)/g).filter(Boolean);
    for (const chunk of chunks) {
      const keyMatch = chunk.match(/^@\w+\{([^,\s]+),/);
      if (!keyMatch) continue;
      const key = keyMatch[1];
      const fields = parseEntry(chunk);
      const author = firstAuthorLast(fields.author);
      const year = fields.year || fields.date?.slice(0, 4) || "n.d.";
      index.set(key, {
        key,
        author,
        year,
        title: fields.title || key,
        doi: fields.doi || "",
        url: resolvePublicationUrl(fields),
        shortLabel: `${author}, ${year}`,
        crossref: fields.crossref || ""
      });
    }
  }

  return index;
}

/** Map alias bib keys (crossref entries) to their canonical target. */
export function buildBibAliasMap(bibIndex) {
  const aliases = new Map();
  for (const [key, entry] of bibIndex) {
    if (entry.crossref) aliases.set(key, entry.crossref);
  }
  return aliases;
}

export function canonicalCiteKey(key, aliasMap) {
  let current = key;
  const seen = new Set();
  while (aliasMap.has(current) && !seen.has(current)) {
    seen.add(current);
    current = aliasMap.get(current);
  }
  return current;
}

function mergeCitedInUnits(keyToUnits, aliasMap) {
  for (const [alias, canonical] of aliasMap) {
    const aliasUnits = keyToUnits.get(alias);
    if (!aliasUnits?.length) continue;
    if (!keyToUnits.has(canonical)) keyToUnits.set(canonical, []);
    const canonList = keyToUnits.get(canonical);
    for (const unit of aliasUnits) {
      if (!canonList.some((entry) => entry.id === unit.id)) canonList.push(unit);
    }
    keyToUnits.delete(alias);
  }
}

export function buildReferencesJson(repoRoot, citationIndex) {
  const rawBib = buildBibIndex(repoRoot);
  const aliasMap = buildBibAliasMap(rawBib);
  const summaries = buildSummaryIndex(repoRoot);

  if (citationIndex?.keyToUnits) {
    mergeCitedInUnits(citationIndex.keyToUnits, aliasMap);
  }

  const entries = [...rawBib.values()]
    .filter((entry) => !entry.crossref)
    .sort((a, b) => a.shortLabel.localeCompare(b.shortLabel))
    .map((entry) => {
      const { crossref: _drop, ...rest } = entry;
      return {
        ...rest,
        summary: summaries.get(entry.key) || summaries.get(entry.key.toLowerCase()) || "",
        citedIn: citationIndex?.keyToUnits.get(entry.key)?.map((unit) => unit.id) || []
      };
    });

  return { entries, aliasMap };
}

export function buildSummaryIndex(repoRoot) {
  const file = path.join(repoRoot, "references", "bibliography-summaries.tex");
  const text = readFileSync(file, "utf8");
  const summaries = new Map();
  const re = /\\bibsummary\{([^}]+)\}\{([^}]*)\}/g;
  let match;
  while ((match = re.exec(text)) !== null) {
    summaries.set(match[1], match[2]);
  }
  return summaries;
}

/** @deprecated Use buildReferencesJson(...).entries */
export function buildReferencesList(repoRoot, citationIndex) {
  return buildReferencesJson(repoRoot, citationIndex).entries;
}

/** Body inside refsection when present; otherwise the full document. */
export function extractBibliographyScope(tex) {
  const match = tex.match(/\\begin\{refsection\}([\s\S]*?)\\end\{refsection\}/);
  return match ? match[1] : tex;
}

/** Cite keys in first-appearance order within a tex fragment. */
export function collectCiteKeysOrdered(tex) {
  const keys = [];
  const seen = new Set();
  const citeRe = /\\(?:autocite|parencite|cite|textcite|footcite)\{([^}]+)\}/g;
  let match;
  while ((match = citeRe.exec(tex)) !== null) {
    for (const raw of match[1].split(",")) {
      const key = raw.trim();
      if (!key || seen.has(key)) continue;
      seen.add(key);
      keys.push(key);
    }
  }
  return keys;
}

function chapterIdFromFile(file) {
  return file.match(/^(ch\d+)-/)?.[1] || null;
}

function appendixIdFromFile(file) {
  const match = file.match(/^app([A-Za-z])-/);
  return match ? `app${match[1]}` : null;
}

function extractChapterTitle(tex) {
  const match = tex.match(/\\chapter(?:\*)?\{([^}]+)\}/);
  if (!match) return "";
  return match[1].replace(/\\[^ {}]+(?:\{[^}]*\})?/g, "").replace(/\s+/g, " ").trim();
}

/**
 * Scan manuscript tex sources and build per-unit bibliographies (refsection-scoped
 * for chapters) plus inverse key → citing units index.
 */
export function buildManuscriptCitationIndex(repoRoot, { readText, stripComments, expandInputs, bookChapters = [] }) {
  const chapterTitleById = new Map(bookChapters.map((ch) => [ch.id, ch.title]));
  const units = [];
  const keyToUnits = new Map();

  function addUnit(unit) {
    units.push(unit);
    for (const key of unit.keys) {
      if (!keyToUnits.has(key)) keyToUnits.set(key, []);
      const list = keyToUnits.get(key);
      if (!list.some((entry) => entry.id === unit.id)) list.push({ id: unit.id, title: unit.title, kind: unit.kind });
    }
  }

  const chaptersDir = path.join(repoRoot, "chapters");
  for (const file of readdirSync(chaptersDir).sort()) {
    if (!file.endsWith(".tex")) continue;
    const id = chapterIdFromFile(file);
    if (!id) continue;
    const raw = readText(path.join(chaptersDir, file));
    const tex = expandInputs(stripComments(raw), repoRoot);
    const scope = extractBibliographyScope(tex);
    const keys = collectCiteKeysOrdered(scope);
    addUnit({
      id,
      title: chapterTitleById.get(id) || extractChapterTitle(tex) || id,
      kind: "chapter",
      keys
    });
  }

  const appendicesDir = path.join(repoRoot, "appendices");
  for (const file of readdirSync(appendicesDir).sort()) {
    if (!file.endsWith(".tex")) continue;
    const id = appendixIdFromFile(file);
    if (!id) continue;
    const raw = readText(path.join(appendicesDir, file));
    const tex = expandInputs(stripComments(raw), repoRoot);
    const scope = extractBibliographyScope(tex);
    const keys = collectCiteKeysOrdered(scope);
    if (keys.length === 0) continue;
    addUnit({
      id,
      title: extractChapterTitle(tex) || id,
      kind: "appendix",
      keys
    });
  }

  return { units, keyToUnits };
}

export function canonicalizeCitationIndex(citationIndex, aliasMap) {
  const { units } = citationIndex;
  const keyToUnits = new Map();

  for (const unit of units) {
    const seen = new Set();
    unit.keys = unit.keys
      .map((key) => canonicalCiteKey(key, aliasMap))
      .filter((key) => {
        if (!key || seen.has(key)) return false;
        seen.add(key);
        return true;
      });

    for (const key of unit.keys) {
      if (!keyToUnits.has(key)) keyToUnits.set(key, []);
      const list = keyToUnits.get(key);
      if (!list.some((entry) => entry.id === unit.id)) {
        list.push({ id: unit.id, title: unit.title, kind: unit.kind });
      }
    }
  }

  citationIndex.keyToUnits = keyToUnits;
  return citationIndex;
}

export function buildReferencesBibliography(units) {
  const chapters = units
    .filter((unit) => unit.kind === "chapter" && unit.keys.length > 0)
    .map(({ id, title, keys }) => ({ id, title, keys }));
  const other = units
    .filter((unit) => unit.kind !== "chapter" && unit.keys.length > 0)
    .map(({ id, title, kind, keys }) => ({ id, title, kind, keys }));
  return { chapters, other };
}

export function collectCiteKeys(tex, cites) {
  const citeRe = /\\(?:autocite|parencite|cite|textcite|footcite)\{([^}]+)\}/g;
  let match;
  while ((match = citeRe.exec(tex)) !== null) {
    for (const key of match[1].split(",")) cites.add(key.trim());
  }
}

export function collectLabelRefs(tex, labels) {
  const refRe = /\\(?:ref|eqref)\{([^}]+)\}/g;
  let match;
  while ((match = refRe.exec(tex)) !== null) labels.add(match[1]);
}
