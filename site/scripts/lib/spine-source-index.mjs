import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const DECL_START =
  /^(theorem|def|noncomputable\s+def|axiom|abbrev|structure|class|instance|inductive|namespace)\s+([A-Za-z0-9_]+)/;

const TOP_LEVEL_BREAK =
  /^(theorem|def|noncomputable\s+def|axiom|abbrev|structure|class|instance|inductive|namespace|end|\/-!)/;

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function walkLeanFiles(dir, root, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      walkLeanFiles(full, root, out);
    } else if (name.endsWith(".lean")) {
      out.push(relative(root, full).replace(/\\/g, "/"));
    }
  }
  return out;
}

function extractDeclSnippet(source, declName) {
  const lines = source.split("\n");
  const startRe = new RegExp(
    `^(theorem|def|noncomputable def|axiom|abbrev|structure|class|instance|inductive)\\s+${escapeRegExp(declName)}\\b`
  );
  const start = lines.findIndex((line) => startRe.test(line));
  if (start < 0) return null;

  let end = start + 1;
  while (end < lines.length) {
    const line = lines[end];
    if (/^end AlignmentProofSpine/.test(line)) break;
    if (end > start && TOP_LEVEL_BREAK.test(line)) break;
    end += 1;
  }
  return lines.slice(start, end).join("\n").trimEnd();
}

function declNamesFromGraphLabel(label) {
  return label
    .split("\n")
    .slice(1)
    .flatMap((line) => line.match(/\b[a-z][a-z0-9_]*(?:_[a-z0-9_]+)+\b/g) ?? [])
    .filter((name) => name.length > 4);
}

function resolveDeclNames(nodeId, label, aliases, declIndex) {
  const alias = aliases[nodeId];
  if (alias?.decls) return alias.decls;
  if (alias?.kind === "subgraph" || alias?.kind === "label-only" || alias?.kind === "module") {
    return [];
  }

  const fromLabel = declNamesFromGraphLabel(label);
  const foundFromLabel = fromLabel.filter((name) => declIndex.has(name));
  if (foundFromLabel.length > 0) return foundFromLabel;

  const direct = declIndex.get(nodeId);
  if (direct) return [nodeId];

  const underscored = [...declIndex.keys()].filter((name) =>
    name.startsWith(`${nodeId}_`)
  );
  if (underscored.length === 1) return [underscored[0]];
  if (underscored.length > 1) {
    const exact = underscored.find((name) => name === `${nodeId}_${nodeId.slice(1).toLowerCase()}`);
    return [exact || underscored[0]];
  }

  const pMatch = nodeId.match(/^(P\d+[A-Za-z]?)/);
  if (pMatch) {
    const prefix = pMatch[1];
    const matches = [...declIndex.keys()].filter((name) => name.startsWith(`${prefix}_`));
    if (matches.length === 1) return [matches[0]];
  }

  const mbMatch = nodeId.match(/^(MB\d+[a-z]?)/i);
  if (mbMatch) {
    const key = mbMatch[1];
    const axiom = [...declIndex.keys()].find(
      (name) => name.toLowerCase().startsWith(`${key.toLowerCase()}_`) && declIndex.get(name)?.kind === "axiom"
    );
    if (axiom) return [axiom];
  }

  return [];
}

export function buildSpineSourceIndex(formalRoot, aliasPath) {
  const aliases = JSON.parse(readFileSync(aliasPath, "utf8"));
  delete aliases._comment;

  const files = walkLeanFiles(formalRoot, formalRoot);
  const fileCache = new Map();
  const declIndex = new Map();

  for (const file of files) {
    const source = readFileSync(join(formalRoot, file), "utf8");
    fileCache.set(file, source);
    const lines = source.split("\n");
    for (let i = 0; i < lines.length; i++) {
      const match = lines[i].match(DECL_START);
      if (!match) continue;
      const kind = match[1].replace(/\s+/g, " ");
      const name = match[2];
      if (!declIndex.has(name)) {
        declIndex.set(name, { file, kind, startLine: i + 1 });
      }
    }
  }

  function snippetForDecl(declName) {
    const meta = declIndex.get(declName);
    if (!meta) return null;
    const source = fileCache.get(meta.file);
    const code = extractDeclSnippet(source, declName);
    if (!code) return null;
    return {
      name: declName,
      kind: meta.kind,
      file: `formal/AlignmentProofSpine/${meta.file}`,
      code
    };
  }

  function resolveNodeSource(nodeId, label = "") {
    const alias = aliases[nodeId];
    if (alias?.kind === "subgraph") {
      return { kind: "subgraph", slug: alias.slug };
    }
    if (alias?.kind === "label-only") {
      return { kind: "label-only" };
    }
    if (alias?.kind === "module") {
      const file = `formal/AlignmentProofSpine/${alias.file}`;
      const source = readFileSync(join(formalRoot, alias.file), "utf8");
      const header = source.split("\n").slice(0, 40).join("\n");
      return { kind: "module", file, code: header.trimEnd() };
    }

    const declNames = resolveDeclNames(nodeId, label, aliases, declIndex);
    const snippets = declNames.map(snippetForDecl).filter(Boolean);
    if (snippets.length === 0) return null;

    return {
      kind: "decls",
      file: snippets[0].file,
      decls: snippets.map((s) => s.name),
      code: snippets.map((s) => s.code).join("\n\n")
    };
  }

  return { resolveNodeSource, declIndex, repoDeclIndex: buildRepoDeclIndex(declIndex) };
}

const REPO_BLOB_BASE = "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main";

/** Serializable decl → GitHub URL map for site cards and check pages. */
export function buildRepoDeclIndex(declIndex) {
  const out = {};
  for (const [name, meta] of declIndex) {
    const file = `formal/AlignmentProofSpine/${meta.file}`;
    out[name] = {
      kind: meta.kind,
      file,
      githubUrl: meta.startLine ? `${REPO_BLOB_BASE}/${file}#L${meta.startLine}` : `${REPO_BLOB_BASE}/${file}`
    };
  }
  return out;
}

export function enrichDeclIndexWithGraphNodes(declIndexJson, nodes) {
  for (const node of Object.values(nodes)) {
    const decls = node.spineSource?.decls;
    if (!decls) continue;
    for (const declName of decls) {
      if (declIndexJson[declName]) {
        declIndexJson[declName].graphNodeId = node.id;
      }
    }
  }
  return declIndexJson;
}

export function attachSpineSources(nodes, graphs, formalRoot, aliasPath) {
  const { resolveNodeSource, declIndex, repoDeclIndex } = buildSpineSourceIndex(formalRoot, aliasPath);
  const labelById = new Map();
  for (const graph of Object.values(graphs)) {
    for (const node of graph.nodes) {
      if (!labelById.has(node.id)) labelById.set(node.id, node.label || node.id);
    }
  }

  for (const [id, node] of Object.entries(nodes)) {
    const spineSource = resolveNodeSource(id, labelById.get(id) || node.label || id);
    if (spineSource) node.spineSource = spineSource;
  }

  enrichDeclIndexWithGraphNodes(repoDeclIndex, nodes);
  return repoDeclIndex;
}
