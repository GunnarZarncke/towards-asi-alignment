/** Root-relative site paths for book units (chapters, appendices, front matter). */

/** Appendices listed on the book page without a synced `/cards/appendix/…` hub. */
export const APPENDIX_DEDICATED_SITE_PATH = {
  appa: "/notation/",
  appe: "/glossary/",
  appg: "/lean/"
};

/**
 * Canonical on-site path for a book page id (`ch01`, `appD`, `frontmatter`, …).
 * @param {string} pageId
 */
export function bookUnitSitePath(pageId) {
  const id = String(pageId).toLowerCase();
  if (id === "frontmatter") return "/cards/frontmatter/";
  if (/^app/i.test(id)) {
    return APPENDIX_DEDICATED_SITE_PATH[id] ?? `/cards/appendix/${id}/`;
  }
  return `/cards/chapter/${id}/`;
}

/**
 * @param {string} pageId
 * @param {string} [anchor]
 */
export function bookUnitSiteHref(pageId, anchor = "") {
  const path = bookUnitSitePath(pageId);
  if (!anchor) return path;
  return path.endsWith("/") ? `${path}#${anchor}` : `${path}/#${anchor}`;
}

/** Book units whose synced body lives only at `/cards/…/full/` (overview hub on the parent URL). */
export const BOOK_OVERVIEW_ONLY_IDS = new Set(["appm"]);

export function bookOverviewOnlyId(pageId) {
  return BOOK_OVERVIEW_ONLY_IDS.has(String(pageId).toLowerCase());
}
