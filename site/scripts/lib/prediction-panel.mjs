/** Hub panel summaries: markdown with site-root /cards/… links. */

/** Turn `Chapter [Title](url)` into `[Chapter Title](url)` (card converter artifact). */
export function fixPrefixedRefLinks(markdown) {
  let out = String(markdown ?? "");
  for (const prefix of ["Chapter", "Appendix", "Section"]) {
    out = out.replace(
      new RegExp(`\\b${prefix} (\\[[^\\]]+\\]\\([^)]+\\))`, "g"),
      (_, link) => {
        const label = link.match(/\[([^\]]+)\]/)?.[1] ?? "";
        const url = link.match(/\(([^)]+)\)/)?.[1] ?? "";
        return `[${prefix} ${label}](${url})`;
      }
    );
  }
  return out;
}

/** Card-relative `../../chapter/…` → site-root `/cards/chapter/…`. */
export function rewriteCardRelativeLinks(markdown) {
  return String(markdown ?? "").replace(
    /\]\((?:\.\.\/)+(chapter|appendix|frontmatter|concept|bridge|experiment|reference|agenda|funding|glossary|objection|artifact|news|release)\/([^)]+)\)/gi,
    (_, kind, rest) => `](/cards/${kind.toLowerCase()}/${rest})`
  );
}

function takeMarkdownSentences(md, maxSentences) {
  if (!md.trim() || maxSentences < 1) return "";
  const out = [];
  let buf = "";
  let inLabel = 0;
  let inUrl = 0;
  for (let i = 0; i < md.length; i += 1) {
    const c = md[i];
    const prev = md[i - 1];
    if (c === "[" && inUrl === 0) inLabel += 1;
    else if (c === "]" && inLabel > 0 && prev !== "\\") inLabel -= 1;
    else if (c === "(" && inLabel === 0 && prev === "]") inUrl += 1;
    else if (c === ")" && inUrl > 0) inUrl -= 1;

    buf += c;
    if (inLabel === 0 && inUrl === 0 && /[.!?]/.test(c)) {
      const tail = md.slice(i + 1);
      if (!tail.length || /^\s/.test(tail)) {
        out.push(buf.trim());
        buf = "";
        if (out.length >= maxSentences) break;
      }
    }
  }
  if (buf.trim() && out.length < maxSentences) out.push(buf.trim());
  return out.join(" ");
}

function plainForDedup(markdown) {
  return String(markdown ?? "")
    .replace(/<em>([^<]*)<\/em>/gi, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

/**
 * @param {object} market
 * @param {string} propertyMarkdown — from appendix Property authbar (markdown)
 * @param {(text: string) => string} normalizeListing — optional, for dedup vs Metaculus text
 */
export function panelSummaryMarkdown(market, propertyMarkdown, normalizeListing = (t) => t) {
  const override = (market.panelSummary ?? "").trim();
  if (override) {
    return rewriteCardRelativeLinks(fixPrefixedRefLinks(override)).trim();
  }
  const listingNorm = plainForDedup(
    normalizeListing(market.metaculusShortTitle || market.longTitle || "")
  );
  let md = takeMarkdownSentences(propertyMarkdown.trim(), 2);
  if (listingNorm.length > 24 && plainForDedup(md).includes(listingNorm.slice(0, 48))) {
    md = takeMarkdownSentences(propertyMarkdown.trim(), 1);
  }
  md = fixPrefixedRefLinks(md);
  md = rewriteCardRelativeLinks(md);
  if (md.length > 420) {
    md = `${md.slice(0, 417).replace(/\s+\S*$/, "")}…`;
  }
  return md.trim();
}
