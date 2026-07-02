import { readFileSync, existsSync } from "node:fs";
import path from "node:path";

const PDF_URL = "https://github.com/GunnarZarncke/towards-asi-alignment/releases/latest";
const FIGURE_BASE = "https://raw.githubusercontent.com/GunnarZarncke/towards-asi-alignment/main";

const MATH_ENVS = new Set([
  "equation",
  "equation*",
  "align",
  "align*",
  "alignat",
  "alignat*",
  "gather",
  "gather*",
  "multline",
  "multline*",
  "split",
  "aligned",
  "alignedat",
  "gathered",
  "cases",
  "matrix",
  "pmatrix",
  "bmatrix",
  "vmatrix",
  "Bmatrix",
  "smallmatrix"
]);

const ENV_HANDLERS = {
  chapterthesis: (body) => `<div class="callout chapter-thesis"><strong>Chapter thesis.</strong> ${body.trim()}</div>\n\n`,
  quote: (body) => `> ${body.trim().replace(/\n+/g, "\n> ")}\n\n`,
  itemize: (body) => convertList(body, "ul"),
  enumerate: (body) => convertList(body, "ol"),
  description: (body) => convertDescription(body),
  figure: (body, ctx) => convertFigure(body, ctx),
  refsection: (body) => `${body}`,
  titlingpage: (body) => `<div class="title-page">${body.trim()}</div>\n\n`
};

const THEOREM_ENVS = new Set([
  "definition",
  "assumption",
  "lemma",
  "theorem",
  "corollary",
  "claim",
  "introclaim"
]);

export function stripComments(tex) {
  let out = "";
  let i = 0;
  let depth = 0;
  let inVerbatim = false;

  while (i < tex.length) {
    if (tex.startsWith("\\begin{verbatim}", i)) inVerbatim = true;
    if (tex.startsWith("\\end{verbatim}", i)) inVerbatim = false;

    const ch = tex[i];
    if (ch === "{" && !inVerbatim) depth += 1;
    if (ch === "}" && !inVerbatim && depth > 0) depth -= 1;

    if (ch === "%" && depth === 0 && !inVerbatim) {
      while (i < tex.length && tex[i] !== "\n") i += 1;
      continue;
    }

    out += ch;
    i += 1;
  }

  return out;
}

export function expandInputs(tex, repoRoot, stack = new Set()) {
  return tex.replace(/\\input\{([^}]+)\}/g, (_, rawPath) => {
    const rel = rawPath.endsWith(".tex") ? rawPath : `${rawPath}.tex`;
    const abs = path.join(repoRoot, rel);
    if (!existsSync(abs)) return `% missing input: ${rawPath}\n`;
    if (stack.has(abs)) return `% cyclic input: ${rawPath}\n`;
    stack.add(abs);
    const nested = stripComments(readFileSync(abs, "utf8"));
    return expandInputs(nested, repoRoot, stack);
  });
}

function convertList(body, tag) {
  const items = splitListItems(body);
  const lines = items.map((item) => `<li>${item.trim()}</li>`);
  return `<${tag}>\n${lines.join("\n")}\n</${tag}>\n\n`;
}

function convertDescription(body) {
  const items = [];
  const re = /\\item(?:\[[^\]]*\])?\s*([\s\S]*?)(?=\\item|$)/g;
  let match;
  while ((match = re.exec(body)) !== null) {
    const chunk = match[1].trim();
    const split = chunk.match(/^(.+?)\s*\n([\s\S]*)$/);
    if (split) {
      items.push(`<dt>${split[1].trim()}</dt><dd>${split[2].trim()}</dd>`);
    } else {
      items.push(`<dt>${chunk}</dt><dd></dd>`);
    }
  }
  return `<dl class="description-list">\n${items.join("\n")}\n</dl>\n\n`;
}

function splitListItems(body) {
  const items = [];
  let current = "";
  let depth = 0;
  for (let i = 0; i < body.length; i += 1) {
    const rest = body.slice(i);
    if (rest.startsWith("\\item")) {
      if (current.trim()) items.push(current.trim());
      current = "";
      i += 4;
      const optional = body.slice(i + 1).match(/^\[[^\]]*\]/);
      if (optional) i += optional[0].length;
      continue;
    }
    const ch = body[i];
    if (ch === "{") depth += 1;
    if (ch === "}" && depth > 0) depth -= 1;
    current += ch;
  }
  if (current.trim()) items.push(current.trim());
  return items;
}

function convertFigure(body, ctx) {
  const imgMatch = body.match(/\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}/);
  const captionMatch = body.match(/\\caption(?:\[[^\]]*\])?\{([\s\S]*?)\}/);
  const labelMatch = body.match(/\\label\{([^}]+)\}/);
  if (!imgMatch) return `${body.trim()}\n\n`;
  const src = `${FIGURE_BASE}/${imgMatch[1]}`;
  const caption = captionMatch ? captionMatch[1].trim() : "";
  const anchor = labelMatch ? `<span id="${labelMatch[1]}"></span>` : "";
  return `${anchor}<figure class="book-figure"><img src="${src}" alt="${caption}" /><figcaption>${caption}</figcaption></figure>\n\n`;
}

function readBalanced(tex, startIndex) {
  if (tex[startIndex] !== "{") return null;
  let depth = 0;
  for (let i = startIndex; i < tex.length; i += 1) {
    if (tex[i] === "{") depth += 1;
    if (tex[i] === "}") {
      depth -= 1;
      if (depth === 0) {
        return {
          content: tex.slice(startIndex + 1, i),
          end: i + 1
        };
      }
    }
  }
  return null;
}

function readOptional(tex, startIndex) {
  if (tex[startIndex] !== "[") return { content: "", end: startIndex };
  let depth = 0;
  for (let i = startIndex; i < tex.length; i += 1) {
    if (tex[i] === "[") depth += 1;
    if (tex[i] === "]") {
      depth -= 1;
      if (depth === 0) {
        return { content: tex.slice(startIndex + 1, i), end: i + 1 };
      }
    }
  }
  return { content: "", end: startIndex };
}

function readEnvironment(tex, startIndex) {
  const beginMatch = tex.slice(startIndex).match(/^\\begin\{([^}]+)\}/);
  if (!beginMatch) return null;
  const envName = beginMatch[1];
  let cursor = startIndex + beginMatch[0].length;
  let depth = 1;
  while (cursor < tex.length) {
    const nextBegin = tex.slice(cursor).match(/^\\begin\{([^}]+)\}/);
    const nextEnd = tex.slice(cursor).match(/^\\end\{([^}]+)\}/);
    if (nextBegin) {
      depth += 1;
      cursor += nextBegin[0].length;
      continue;
    }
    if (nextEnd) {
      depth -= 1;
      cursor += nextEnd[0].length;
      if (depth === 0) {
        const bodyStart = startIndex + beginMatch[0].length;
        const bodyEnd = cursor - nextEnd[0].length;
        return {
          name: envName,
          body: tex.slice(bodyStart, bodyEnd),
          end: cursor
        };
      }
      continue;
    }
    cursor += 1;
  }
  return null;
}

function convertInlineText(text, ctx) {
  return convertDocument(text, ctx).trim();
}

function relBookHref(pageId, anchor, fromPageId) {
  if (pageId === fromPageId) {
    return anchor ? `#${anchor}` : "./";
  }
  return `../${pageId}/${anchor ? `#${anchor}` : ""}`;
}

function relCardHref(cardSlug) {
  return `../../cards/${cardSlug}/`;
}

function relReferencesHref(key) {
  return `../../cards/references/${encodeURIComponent(key.toLowerCase())}/`;
}

function resolveRef(label, ctx, kind = "ref") {
  const entry = ctx.labelIndex.get(label);
  if (!entry) {
    ctx.errors.push(`Unresolved label: ${label}`);
    return `[missing: ${label}]`;
  }

  const cardSlug = ctx.cardIndex.get(label);
  const text = entry.title || label;

  if (cardSlug) {
    return `[${text}](${relCardHref(cardSlug)})`;
  }

  if (!entry.webPage) {
    return `[${text} (PDF)](${PDF_URL})`;
  }

  const anchor = label.startsWith("ch:") ? "" : label;
  return `[${text}](${relBookHref(entry.pageId, anchor, ctx.pageId)})`;
}

function formatCite(keys, ctx) {
  const parts = keys.split(",").map((k) => k.trim()).filter(Boolean);
  return parts.map((key) => {
    const entry = ctx.bibIndex.get(key);
    if (!entry) {
      ctx.errors.push(`Unresolved citation: ${key}`);
      return `[missing cite: ${key}]`;
    }
    const label = entry.shortLabel || key;
    return `[${label}](${relReferencesHref(key)})`;
  }).join(", ");
}

function convertCommand(name, tex, index, ctx) {
  const readArg = () => {
    const arg = readBalanced(tex, index);
    if (!arg) return null;
    index = arg.end;
    return arg.content;
  };

  switch (name) {
    case "chapter": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n# ${title}\n\n`, index };
    }
    case "chapter*": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n# ${title}\n\n`, index };
    }
    case "section": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n## ${title}\n\n`, index };
    }
    case "section*": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n## ${title}\n\n`, index };
    }
    case "subsection": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n### ${title}\n\n`, index };
    }
    case "subsection*": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n### ${title}\n\n`, index };
    }
    case "subsubsection": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n#### ${title}\n\n`, index };
    }
    case "paragraph": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n**${title}**\n\n`, index };
    }
    case "label": {
      const label = readArg() || "";
      return { output: `<span id="${label}"></span>`, index };
    }
    case "ref":
    case "eqref": {
      const label = readArg() || "";
      const link = resolveRef(label, ctx, name);
      return { output: link, index };
    }
    case "autocite":
    case "parencite":
    case "cite":
    case "textcite":
    case "footcite": {
      const keys = readArg() || "";
      return { output: formatCite(keys, ctx), index };
    }
    case "emph":
    case "textit": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: `*${inner}*`, index };
    }
    case "textbf": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: `**${inner}**`, index };
    }
    case "texttt":
    case "nolinkurl":
    case "url": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: `\`${inner}\``, index };
    }
    case "textsc": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: inner.toUpperCase(), index };
    }
    case "leanid": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: `\`${inner}\``, index };
    }
    case "leanspine": {
      const kind = convertInlineText(readArg() || "", ctx);
      const node = convertInlineText(readArg() || "", ctx);
      const gloss = convertInlineText(readArg() || "", ctx);
      return {
        output: `<p class="lean-spine"><em>Lean spine (${kind}):</em> <code>${node}</code> — ${gloss}</p>`,
        index
      };
    }
    case "epigraph": {
      const quote = convertInlineText(readArg() || "", ctx);
      const attribution = convertInlineText(readArg() || "", ctx);
      return {
        output: `<blockquote class="epigraph"><p>${quote}</p><footer>${attribution}</footer></blockquote>\n\n`,
        index
      };
    }
    case "includegraphics": {
      const opt = tex[index] === "[" ? readOptional(tex, index) : { end: index };
      index = opt.end;
      const file = readArg() || "";
      return {
        output: `<figure class="book-figure"><img src="${FIGURE_BASE}/${file}" alt="" /></figure>\n\n`,
        index
      };
    }
    case "footnote": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: `<sup class="footnote"><a href="#fn-${ctx.footnoteCount}">${++ctx.footnoteCount}</a></sup>`, index, footnote: inner };
    }
    case "printbibliography":
    case "addcontentsline":
    case "clearpage":
    case "newpage":
    case "thispagestyle":
    case "tableofcontents":
    case "listoffigures":
    case "listoftables":
    case "maketitle":
    case "renewcommand":
    case "newcommand":
    case "newcolumntype":
    case "providecommand":
    case "vspace":
    case "vfill":
    case "centering":
    case "par":
    case "smallskip":
    case "medskip":
    case "bigskip":
    case "noindent":
    case "hspace":
    case "today":
      return { output: "", index: skipCommand(name, tex, index) };
    case "caption":
    case "toprule":
    case "midrule":
    case "bottomrule":
    case "hline":
    case "endhead":
    case "endfoot":
    case "endfirsthead":
    case "endlastfoot":
      return { output: "", index: skipBracedOrOptional(tex, index) };
    default:
      if (name.startsWith("text")) {
        const arg = readArg();
        if (arg) {
          index = arg.end;
          return { output: convertInlineText(arg.content, ctx), index };
        }
      }
      return { output: "", index: skipCommand(name, tex, index) };
  }
}

function skipBracedOrOptional(tex, index) {
  if (tex[index] === "[") index = readOptional(tex, index).end;
  if (tex[index] === "{") index = readBalanced(tex, index).end;
  return index;
}

function skipCommand(name, tex, index) {
  while (index < tex.length && tex[index] === "*") index += 1;
  if (tex[index] === "[") index = readOptional(tex, index).end;
  while (index < tex.length && tex[index] === "{") {
    const arg = readBalanced(tex, index);
    if (!arg) break;
    index = arg.end;
  }
  return index;
}

function convertMath(body, display = true) {
  const trimmed = body.trim();
  if (display) return `\n$$\n${trimmed}\n$$\n\n`;
  return `$${trimmed}$`;
}

function convertTableEnv(body, ctx) {
  const rows = body
    .split(/\\\\/g)
    .map((row) => row.trim())
    .filter((row) => row && !/^\\(toprule|midrule|bottomrule|hline|caption|label|endhead|endfoot|endfirsthead|endlastfoot)/.test(row));

  const mdRows = rows.map((row) => {
    const cells = row
      .split("&")
      .map((cell) => convertInlineText(cell.replace(/\\newline/g, " ").trim(), ctx));
    return `| ${cells.join(" | ")} |`;
  });

  if (mdRows.length === 0) return "\n";
  const width = mdRows[0].split("|").length - 2;
  const sep = `| ${Array(width).fill("---").join(" | ")} |`;
  return `\n${mdRows[0]}\n${sep}\n${mdRows.slice(1).join("\n")}\n\n`;
}

function convertDocument(tex, ctx) {
  let out = "";
  let i = 0;
  const footnotes = [];

  while (i < tex.length) {
    if (tex.startsWith("\\begin{", i)) {
      const env = readEnvironment(tex, i);
      if (!env) break;
      i = env.end;

      if (MATH_ENVS.has(env.name)) {
        out += convertMath(env.body, !env.name.endsWith("*") || env.name.startsWith("align"));
        continue;
      }

      if (THEOREM_ENVS.has(env.name)) {
        const opt = env.body.match(/^\[[^\]]*\]\s*/);
        const body = opt ? env.body.slice(opt[0].length) : env.body;
        const title = env.name === "introclaim" ? "Claim" : env.name[0].toUpperCase() + env.name.slice(1);
        out += `<div class="env-box env-${env.name}"><strong>${title}.</strong> ${convertDocument(body, ctx).trim()}</div>\n\n`;
        continue;
      }

      if (env.name === "longtable" || env.name === "tabularx" || env.name === "tabular") {
        out += convertTableEnv(env.body, ctx);
        continue;
      }

      if (ENV_HANDLERS[env.name]) {
        out += ENV_HANDLERS[env.name](convertDocument(env.body, ctx), ctx);
        continue;
      }

      out += convertDocument(env.body, ctx);
      continue;
    }

    if (tex.startsWith("\\[", i)) {
      const end = tex.indexOf("\\]", i + 2);
      if (end === -1) break;
      out += convertMath(tex.slice(i + 2, end), true);
      i = end + 2;
      continue;
    }

    if (tex.startsWith("\\(", i)) {
      const end = tex.indexOf("\\)", i + 2);
      if (end === -1) break;
      out += convertMath(tex.slice(i + 2, end), false);
      i = end + 2;
      continue;
    }

    if (tex[i] === "$") {
      if (tex[i + 1] === "$") {
        const end = tex.indexOf("$$", i + 2);
        if (end === -1) break;
        out += convertMath(tex.slice(i + 2, end), true);
        i = end + 2;
        continue;
      }
      const end = tex.indexOf("$", i + 1);
      if (end === -1) break;
      out += convertMath(tex.slice(i + 1, end), false);
      i = end + 1;
      continue;
    }

    if (tex[i] === "\\") {
      const cmdMatch = tex.slice(i).match(/^\\([A-Za-z@]+)/);
      if (cmdMatch) {
        const cmd = cmdMatch[1];
        const start = i + cmdMatch[0].length;
        const result = convertCommand(cmd, tex, start, ctx);
        out += result.output;
        if (result.footnote) footnotes.push(result.footnote);
        i = result.index;
        continue;
      }
      out += tex[i];
      i += 1;
      continue;
    }

    if (tex[i] === "~") {
      out += " ";
      i += 1;
      continue;
    }

    if (tex[i] === "\n" && tex[i + 1] === "\n") {
      out += "\n\n";
      i += 2;
      continue;
    }

    out += tex[i];
    i += 1;
  }

  if (footnotes.length > 0) {
    out += `\n<div class="footnotes">\n`;
    footnotes.forEach((note, idx) => {
      out += `<p id="fn-${idx + 1}"><sup>${idx + 1}</sup> ${note}</p>\n`;
    });
    out += `</div>\n`;
  }

  return cleanupMarkdown(out);
}

function cleanupMarkdown(text) {
  return text
    .replace(/\n{3,}/g, "\n\n")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\\ldots/g, "…")
    .replace(/\\dots/g, "…")
    .replace(/---/g, "—")
    .replace(/``/g, "“")
    .replace(/''/g, "”")
    .replace(/\\&/g, "&")
    .replace(/\\%/g, "%")
    .replace(/\\_/g, "_")
    .replace(/\\#/g, "#")
    .replace(/\\textasciitilde\{\}/g, "~")
    .trim();
}

export function convertLatexDocument(tex, ctx) {
  const expanded = expandInputs(stripComments(tex), ctx.repoRoot);
  return convertDocument(expanded, ctx);
}

export function extractChapterMeta(tex) {
  const chapterMatch = tex.match(/\\chapter(?:\*?)?\{([^}]+)\}/);
  const labelMatch = tex.match(/\\label\{([^}]+)\}/);
  return {
    title: chapterMatch ? chapterMatch[1].replace(/\\[^ {}]+(?:\{[^}]*\})?/g, "").trim() : "Untitled",
    label: labelMatch ? labelMatch[1] : null
  };
}

export function collectLabels(tex, pageId, title, webPage, labelIndex) {
  const labelRe = /\\label\{([^}]+)\}/g;
  let match;
  while ((match = labelRe.exec(tex)) !== null) {
    labelIndex.set(match[1], { pageId, title, webPage, label: match[1] });
  }
}

export function collectReferences(tex, refs) {
  const refRe = /\\(?:ref|eqref)\{([^}]+)\}/g;
  let match;
  while ((match = refRe.exec(tex)) !== null) refs.add(match[1]);

  const rangeRe = /\\ref\{([^}]+)\}/g;
  while ((match = rangeRe.exec(tex)) !== null) refs.add(match[1]);

  const citeRe = /\\(?:autocite|parencite|cite|textcite|footcite)\{([^}]+)\}/g;
  while ((match = citeRe.exec(tex)) !== null) {
    for (const key of match[1].split(",")) refs.add(key.trim());
  }
}
