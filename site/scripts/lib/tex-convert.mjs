import { readFileSync, existsSync, readdirSync } from "node:fs";
import path from "node:path";
import katex from "katex";

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
  chapterthesis: (body, ctx) =>
    `<div class="callout chapter-thesis"><strong>Chapter thesis.</strong> ${convertInlineText(body, ctx)}</div>\n\n`,
  quote: (body, ctx) => `> ${convertInlineText(body, ctx).replace(/\n+/g, "\n> ")}\n\n`,
  itemize: (body, ctx) => convertList(body, "ul", ctx),
  enumerate: (body, ctx) => convertList(body, "ol", ctx),
  description: (body, ctx) => convertDescription(body, ctx),
  figure: (body, ctx) => convertFigure(body, ctx),
  refsection: (body, ctx) => convertDocument(body, ctx),
  titlingpage: (body, ctx) => `<div class="title-page">${convertInlineText(body, ctx)}</div>\n\n`
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

function stripLeadingEnvOptions(body) {
  return body.replace(/^\[[^\]]*\]\s*/, "");
}

function formatMarkdownListItem(marker, content) {
  const lines = content.split("\n");
  const pad = " ".repeat(marker.length);
  const formatted = [`${marker}${lines[0] ?? ""}`];
  for (let i = 1; i < lines.length; i += 1) {
    const line = lines[i];
    formatted.push(line === "" ? "" : `${pad}${line}`);
  }
  return formatted.join("\n");
}

function convertList(body, tag, ctx) {
  const items = splitListItems(stripLeadingEnvOptions(body));
  const ordered = tag === "ol";
  const lines = items.map((item, index) => {
    const content = convertDocument(item, ctx).trim();
    const marker = ordered ? `${index + 1}. ` : "- ";
    return formatMarkdownListItem(marker, content);
  });
  return `${lines.join("\n\n")}\n\n`;
}

function convertDescription(body, ctx) {
  const items = [];
  const re = /\\item(?:\[[^\]]*\])?\s*([\s\S]*?)(?=\\item|$)/g;
  let match;
  while ((match = re.exec(stripLeadingEnvOptions(body))) !== null) {
    const chunk = match[1].trim();
    const split = chunk.match(/^(.+?)\s*\n([\s\S]*)$/);
    if (split) {
      items.push(
        `<dt>${convertInlineText(split[1].trim(), ctx)}</dt><dd>${convertInlineText(split[2].trim(), ctx)}</dd>`
      );
    } else {
      items.push(`<dt>${convertInlineText(chunk, ctx)}</dt><dd></dd>`);
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
      i += "\\item".length - 1;
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

// Chapter-opening illustrations live at figures/illustrations/chNN_<slug>.png.
// Their caption (the illustration title) links to an unlisted prompt page at
// /illustrations/{chapterId}/ that is not part of the cards collection and is
// therefore not listed or searchable — reachable only from this link.
const ILLUSTRATION_PATH_RE = /^figures\/illustrations\/(ch\d+)_/;

function relIllustrationHref(chapterId) {
  // The figure is rendered inside a book chapter served at /cards/chapters/{id}/.
  return `../../../illustrations/${chapterId.toLowerCase()}/`;
}

// The print-resolution PNG is what \includegraphics uses for the PDF; the
// site instead serves the downsized JPEG from figures/illustrations/web/
// (regenerate with scripts/generate_web_illustrations.py).
export function webIllustrationPath(sourcePath) {
  const match = sourcePath.match(/^figures\/illustrations\/(ch\d+_[^/]+)\.png$/);
  if (!match) return sourcePath;
  return `figures/illustrations/web/${match[1]}.jpg`;
}

/** Same-origin URL for chapter-opening illustrations (offline-cacheable). */
export function illustrationPublicSrc(sourcePath) {
  const webPath = webIllustrationPath(sourcePath);
  if (webPath === sourcePath) return null;
  return `/${webPath}`;
}

// Site-only alt text, richer than the title-only PDF caption: read once from
// the `alt` frontmatter field of site/src/content/illustrations/{chapterId}.md
// (the canonical source, condensed from each illustration's generation spec).
export function loadIllustrationAlts(repoRoot) {
  const dir = path.join(repoRoot, "site", "src", "content", "illustrations");
  const alts = new Map();
  if (!existsSync(dir)) return alts;
  for (const name of readdirSync(dir)) {
    if (!name.endsWith(".md")) continue;
    const text = readFileSync(path.join(dir, name), "utf8");
    const frontmatter = text.match(/^---\n([\s\S]*?)\n---/)?.[1] || "";
    const chapterId = frontmatter.match(/^chapterId:\s*"([^"]+)"/m)?.[1];
    const alt = frontmatter.match(/^alt:\s*"([^"]*)"/m)?.[1];
    if (chapterId && alt) alts.set(chapterId.toLowerCase(), alt);
  }
  return alts;
}

function convertFigure(body, ctx) {
  const imgMatch = body.match(/\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}/);
  const captionMatch = body.match(/\\caption(?:\[[^\]]*\])?\{([\s\S]*?)\}/);
  const labelMatch = body.match(/\\label\{([^}]+)\}/);
  if (!imgMatch) return `${body.trim()}\n\n`;
  const illustrationMatch = imgMatch[1].match(ILLUSTRATION_PATH_RE);
  const localSrc = illustrationMatch ? illustrationPublicSrc(imgMatch[1]) : null;
  const src = localSrc ?? `${FIGURE_BASE}/${imgMatch[1]}`;
  const caption = captionMatch ? captionMatch[1].trim() : "";
  const anchor = labelMatch ? `<span id="${labelMatch[1]}"></span>` : "";
  const alt = illustrationMatch ? ctx.illustrationAlts?.get(illustrationMatch[1].toLowerCase()) || caption : caption;
  const captionHtml = illustrationMatch
    ? `<a href="${relIllustrationHref(illustrationMatch[1])}">${caption}</a>`
    : caption;
  return `${anchor}<figure class="book-figure"><img src="${src}" alt="${alt}" /><figcaption>${captionHtml}</figcaption></figure>\n\n`;
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

function skipBeginOptional(tex, cursor) {
  if (tex[cursor] === "[") return readOptional(tex, cursor).end;
  return cursor;
}

const BEGIN_ENV_ARG_COUNT = {
  longtable: 1,
  tabular: 1,
  tabularx: 2,
  authbar: 1
};

function skipBeginArgs(tex, cursor, envName) {
  cursor = skipBeginOptional(tex, cursor);
  const argCount = BEGIN_ENV_ARG_COUNT[envName] ?? 0;
  for (let i = 0; i < argCount; i += 1) {
    if (tex[cursor] === "{") {
      const arg = readBalanced(tex, cursor);
      if (!arg) break;
      cursor = arg.end;
    }
  }
  return cursor;
}

function readBeginEnvArgs(tex, cursor, envName) {
  cursor = skipBeginOptional(tex, cursor);
  const args = [];
  const argCount = BEGIN_ENV_ARG_COUNT[envName] ?? 0;
  for (let i = 0; i < argCount; i += 1) {
    if (tex[cursor] === "{") {
      const arg = readBalanced(tex, cursor);
      if (!arg) break;
      args.push(arg.content.trim());
      cursor = arg.end;
    }
  }
  return { args, cursor };
}

const MULTILINE_MATH_ENVS = new Set([
  "align",
  "align*",
  "alignat",
  "alignat*",
  "gather",
  "gather*",
  "multline",
  "multline*",
  "split"
]);

function preprocessMathMacros(body) {
  return body
    .replace(/\\symboldef(?:\[[^\]]*\])?\{([^}]*)\}/g, "$1")
    .replace(/\\symbolref(?:\[[^\]]*\])?\{([^}]*)\}/g, "$1");
}

function stripMathLabels(body) {
  const labels = [];
  const stripped = body.replace(/\\label\{([^}]+)\}/g, (_, label) => {
    labels.push(label);
    return "";
  });
  return { body: stripped.trim(), labels };
}

function convertDisplayMath(body, envName = null) {
  const { body: labelStripped, labels } = stripMathLabels(body);
  const math = preprocessMathMacros(labelStripped);
  const anchors = labels.map((id) => `<span id="${id}"></span>`).join("");
  if (envName && MULTILINE_MATH_ENVS.has(envName)) {
    return `${anchors}\n$$\n\\begin{${envName}}\n${math}\n\\end{${envName}}\n$$\n\n`;
  }
  return `${anchors}\n$$\n${math}\n$$\n\n`;
}

function convertInlineMath(body) {
  const { body: labelStripped, labels } = stripMathLabels(body);
  const math = preprocessMathMacros(labelStripped);
  const anchors = labels.map((id) => `<span id="${id}"></span>`).join("");
  return `${anchors}$${math}$`;
}

function readEnvironment(tex, startIndex) {
  const beginMatch = tex.slice(startIndex).match(/^\\begin\{([^}]+)\}/);
  if (!beginMatch) return null;
  const envName = beginMatch[1];
  const afterBegin = startIndex + beginMatch[0].length;
  const { args, cursor } = readBeginEnvArgs(tex, afterBegin, envName);
  const bodyStart = cursor;
  let depth = 1;
  let cursorWalk = cursor;
  while (cursorWalk < tex.length) {
    const nextBegin = tex.slice(cursorWalk).match(/^\\begin\{([^}]+)\}/);
    const nextEnd = tex.slice(cursorWalk).match(/^\\end\{([^}]+)\}/);
    if (nextBegin) {
      depth += 1;
      cursorWalk = skipBeginArgs(tex, cursorWalk + nextBegin[0].length, nextBegin[1]);
      continue;
    }
    if (nextEnd) {
      depth -= 1;
      cursorWalk += nextEnd[0].length;
      if (depth === 0) {
        return {
          name: envName,
          args,
          body: tex.slice(bodyStart, cursorWalk - nextEnd[0].length),
          end: cursorWalk
        };
      }
      continue;
    }
    cursorWalk += 1;
  }
  return null;
}

function authKeysToMode(keys) {
  const parts = keys.split("+").map((part) => part.trim()).filter(Boolean);
  const hasAI = parts.includes("AI");
  if (!hasAI) return "none";
  if (hasAI && parts.length === 1) return "solid";
  return "dotted";
}

function formatAuthChip(keys) {
  const mode = authKeysToMode(keys);
  const label = keys.replace(/\+/g, "+");
  const readable = keys.replace(/\+/g, " ");
  return `<span class="auth-chip" data-auth="${label}" data-auth-mode="${mode}" aria-label="Authorship: ${readable}"><span class="auth-chip-label">${readable}</span></span>`;
}

function emitHeading(level, title, authKeys) {
  const chip = authKeys ? ` ${formatAuthChip(authKeys)}` : "";
  const hashes = "#".repeat(level);
  return `\n${hashes} ${title}${chip}\n\n`;
}

const HEADING_CMD_LEVEL = new Map([
  ["section", 2],
  ["section*", 2],
  ["subsection", 3],
  ["subsection*", 3],
  ["authbarsection", 2],
  ["authbarsubsection", 3]
]);

const AUTHBAR_SKIP_CMDS = new Set([
  "authbarneedspace",
  "authbarsubneedspace",
  "label",
  "needspace",
  "Needspace"
]);

/** Pre-scan: one auth key (or null) per section/subsection, in document order.
 *  Keys match `\begin{authbar}{…}` in LaTeX; see metadata/authorship-bars.tex and
 *  the Preface authorship note (PDF bars; site chips via Notes panel). */
export function scanAuthHeadingKeys(tex) {
  const keys = [];
  let pending = null;
  let i = 0;

  while (i < tex.length) {
    if (tex.startsWith("\\begin{authbar}", i)) {
      const env = readEnvironment(tex, i);
      if (!env) break;
      if (pending) {
        keys.push(env.args?.[0] || "AI");
        pending = null;
      }
      i = env.end;
      continue;
    }

    if (tex[i] === "\\") {
      const cmdMatch = tex.slice(i).match(/^\\([A-Za-z@]+)/);
      if (cmdMatch) {
        const name = cmdMatch[1];
        const cursor = i + cmdMatch[0].length;
        if (HEADING_CMD_LEVEL.has(name)) {
          if (pending) keys.push(null);
          const arg = readBalanced(tex, cursor);
          pending = { level: HEADING_CMD_LEVEL.get(name) };
          i = arg ? arg.end : cursor;
          continue;
        }
        if (AUTHBAR_SKIP_CMDS.has(name)) {
          i = skipCommand(name, tex, cursor);
          continue;
        }
      }
    }

    i += 1;
  }

  if (pending) keys.push(null);
  return keys;
}

function nextAuthHeadingKeys(ctx) {
  if (!ctx.authHeadingKeys || ctx.authHeadingIndex >= ctx.authHeadingKeys.length) return null;
  return ctx.authHeadingKeys[ctx.authHeadingIndex++];
}

function convertInlineText(text, ctx) {
  return convertDocument(text, ctx).trim();
}

function relBookHref(pageId, anchor, fromPageId) {
  const slug = pageId.toLowerCase();
  if (pageId === fromPageId) {
    return anchor ? `#${anchor}` : "./";
  }
  const segment = /^app/i.test(pageId)
    ? "appendix"
    : pageId === "frontmatter"
      ? "frontmatter"
      : "chapter";
  const fromSegment = /^app/i.test(fromPageId)
    ? "appendix"
    : fromPageId === "frontmatter"
      ? "frontmatter"
      : "chapter";
  if (segment === fromSegment) {
    if (segment === "frontmatter") return anchor ? `./#${anchor}` : "./";
    return `../${slug}/${anchor ? `#${anchor}` : ""}`;
  }
  if (segment === "frontmatter") return `../../frontmatter/${anchor ? `#${anchor}` : ""}`;
  return `../../${segment}/${slug}/${anchor ? `#${anchor}` : ""}`;
}

function relCardHref(cardSlug, cardType) {
  if (cardSlug.startsWith("chapters/")) {
    const chapterId = cardSlug.slice("chapters/".length).toLowerCase();
    const segment = /^app/i.test(chapterId)
      ? "appendix"
      : chapterId === "frontmatter"
        ? "frontmatter"
        : "chapter";
    if (segment === "frontmatter") return "../../frontmatter/";
    return `../../${segment}/${chapterId}/`;
  }
  if (cardSlug.startsWith("experiments/")) {
    return `../../experiment/${cardSlug.slice("experiments/".length).toLowerCase()}/`;
  }
  if (cardSlug.startsWith("references/")) {
    return `../../reference/${cardSlug.slice("references/".length).toLowerCase()}/`;
  }
  if (cardSlug.startsWith("field-agendas/")) {
    return `../../agenda/${cardSlug.slice("field-agendas/".length).toLowerCase()}/`;
  }
  const segment =
    cardType === "bridge"
      ? "bridge"
      : cardType === "glossary"
        ? "glossary"
        : cardType === "objection"
          ? "objection"
          : cardType === "artifact"
            ? "artifact"
            : cardType === "news"
              ? "news"
              : cardType === "release"
                ? "release"
                : "concept";
  const local = cardSlug.includes("/") ? cardSlug.split("/").pop() : cardSlug;
  return `../../${segment}/${String(local).toLowerCase()}/`;
}

function relReferencesHref(key) {
  return `../../references/${encodeURIComponent(key.toLowerCase())}/`;
}

function resolveRef(label, ctx, kind = "ref") {
  const entry = ctx.labelIndex.get(label);
  if (!entry) {
    ctx.errors.push(`Unresolved label: ${label}`);
    return `[missing: ${label}]`;
  }

  const card = ctx.cardIndex.get(label);
  const text = entry.title || label;

  if (card) {
    return `[${text}](${relCardHref(card.slug, card.type)})`;
  }

  if (!entry.webPage) {
    return text;
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
      return { output: emitHeading(2, title, nextAuthHeadingKeys(ctx)), index };
    }
    case "section*": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: emitHeading(2, title, nextAuthHeadingKeys(ctx)), index };
    }
    case "subsection": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: emitHeading(3, title, nextAuthHeadingKeys(ctx)), index };
    }
    case "subsection*": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: emitHeading(3, title, nextAuthHeadingKeys(ctx)), index };
    }
    case "subsubsection": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: `\n#### ${title}\n\n`, index };
    }
    case "authbarneedspace":
    case "authbarsubneedspace":
      return { output: "", index: skipCommand(name, tex, index) };
    case "authbarsection": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: emitHeading(2, title, nextAuthHeadingKeys(ctx)), index };
    }
    case "authbarsubsection": {
      const title = convertInlineText(readArg() || "", ctx);
      return { output: emitHeading(3, title, nextAuthHeadingKeys(ctx)), index };
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
    case "hyperref":
    case "gloss": {
      let label = "";
      if (tex[index] === "[") {
        const opt = readOptional(tex, index);
        label = opt.content;
        index = opt.end;
      }
      const textArg = readBalanced(tex, index);
      if (!textArg) return { output: "", index: skipCommand(name, tex, index) };
      index = textArg.end;
      const text = convertInlineText(textArg.content, ctx);
      if (!label) return { output: text, index };
      const card = ctx.cardIndex.get(label);
      if (card) {
        return { output: `[${text}](${relCardHref(card.slug, card.type)})`, index };
      }
      const entry = ctx.labelIndex.get(label);
      if (entry?.webPage) {
        const anchor = label.startsWith("ch:") || label.startsWith("gloss:") ? "" : label;
        return { output: `[${text}](${relBookHref(entry.pageId, anchor, ctx.pageId)})`, index };
      }
      return { output: text, index };
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
      return { output: `<em>${inner}</em>`, index };
    }
    case "textbf": {
      const inner = convertInlineText(readArg() || "", ctx);
      return { output: `<strong>${inner}</strong>`, index };
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
    case "symboldef":
    case "symbolref": {
      if (tex[index] === "[") {
        index = readOptional(tex, index).end;
      }
      const arg = readBalanced(tex, index);
      if (!arg) return { output: "", index };
      index = arg.end;
      return { output: `$${arg.content.trim()}$`, index };
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
    case "Huge":
    case "Large":
    case "bfseries":
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
  return display ? convertDisplayMath(body) : convertInlineMath(body);
}

function stripTableDecorations(body) {
  return body
    .replace(/\\endfirsthead[\s\S]*?\\endhead/g, "")
    .replace(/\\caption(?:\[[^\]]*\])?\{[\s\S]*?\}/g, "")
    .replace(/\\label\{[^}]+\}/g, "")
    .replace(/\\(toprule|midrule|bottomrule|hline|endfirsthead|endhead|endfoot|endlastfoot)\b/g, "")
    .replace(/\\addlinespace\b/g, "");
}

function cleanTableRow(row) {
  return row
    .replace(/^\\(?:noalign|smallskip|medskip|bigskip|vspace)\b[^\n]*/gm, "")
    .trim();
}

// Table cells are emitted as raw HTML (not markdown), because raw HTML blocks
// in the markdown pipeline are passed through unparsed: remark-math never sees
// `$...$` inside them, and markdown link syntax never turns into `<a>` tags.
// So table-cell inline content needs its own HTML-producing versions of ref
// links and math, instead of the markdown-syntax versions convertInlineText emits.
function renderTableCellMath(text) {
  const renderExpr = (expr, displayMode) => {
    try {
      return katex.renderToString(expr.trim(), { throwOnError: false, displayMode });
    } catch {
      return expr;
    }
  };
  return text
    .replace(/\$\$([\s\S]+?)\$\$/g, (_, expr) => renderExpr(expr, true))
    .replace(/\$([^$]+?)\$/g, (_, expr) => renderExpr(expr, false));
}

function tableCellLinksToHtml(text) {
  return text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, url) => `<a href="${url}">${label}</a>`);
}

function convertTableCell(cell, ctx) {
  const md = convertInlineText(cell.replace(/\\newline/g, " ").trim(), ctx);
  return tableCellLinksToHtml(renderTableCellMath(md));
}

function convertTableEnv(body, ctx) {
  const rows = stripTableDecorations(body)
    .split(/\\\\/g)
    .map(cleanTableRow)
    .filter((row) => row.includes("&"));

  if (rows.length === 0) return "\n";

  const htmlRows = rows.map((row, idx) => {
    const cells = row.split("&").map((cell) => convertTableCell(cell, ctx));
    const tag = idx === 0 ? "th" : "td";
    const cellHtml = cells.map((cell) => `<${tag}>${cell}</${tag}>`).join("");
    return `<tr>${cellHtml}</tr>`;
  });

  return `\n<div class="table-wrap"><table class="book-table">\n${htmlRows.join("\n")}\n</table></div>\n\n`;
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
        out += convertDisplayMath(env.body, env.name);
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

      if (env.name === "authbar") {
        out += convertDocument(env.body, ctx);
        continue;
      }

      if (ENV_HANDLERS[env.name]) {
        out += ENV_HANDLERS[env.name](env.body, ctx);
        continue;
      }

      out += convertDocument(env.body, ctx);
      continue;
    }

    if (tex.startsWith("\\[", i)) {
      const end = tex.indexOf("\\]", i + 2);
      if (end === -1) break;
      out += convertDisplayMath(tex.slice(i + 2, end));
      i = end + 2;
      continue;
    }

    if (tex.startsWith("\\(", i)) {
      const end = tex.indexOf("\\)", i + 2);
      if (end === -1) break;
      out += convertInlineMath(tex.slice(i + 2, end));
      i = end + 2;
      continue;
    }

    if (tex[i] === "$") {
      if (tex[i + 1] === "$") {
        const end = tex.indexOf("$$", i + 2);
        if (end === -1) break;
        out += convertDisplayMath(tex.slice(i + 2, end));
        i = end + 2;
        continue;
      }
      const end = tex.indexOf("$", i + 1);
      if (end === -1) break;
      out += convertInlineMath(tex.slice(i + 1, end));
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

    if (tex[i] === "{") {
      const group = readBalanced(tex, i);
      if (group) {
        out += convertDocument(group.content, ctx);
        i = group.end;
        continue;
      }
    }

    if (tex[i] === "}") {
      i += 1;
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
  ctx.authHeadingKeys = scanAuthHeadingKeys(expanded);
  ctx.authHeadingIndex = 0;
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
