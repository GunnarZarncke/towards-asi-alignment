export const SITE_NAME = "Towards Superintelligence Alignment";
export const DEFAULT_DESCRIPTION =
  "Companion site for the Towards Superintelligence Alignment project — guided paths, concept cards, Lean spine, and experiments.";
export const HOME_DESCRIPTION =
  "As AI gets more capable, can people still change what it does when it is wrong? The book Towards Superintelligence Alignment, plus a field map, experiments, and news.";
export const SITE_ORIGIN = "https://towards-alignment.com";
export const AUTHOR_NAME = "Gunnar Zarncke";
export const OG_IMAGE_PATH = "/og-image.png";
export const OG_IMAGE_URL = `${SITE_ORIGIN}${OG_IMAGE_PATH}`;
export const OG_IMAGE_ALT =
  "Towards Superintelligence Alignment — companion site for the research manuscript";
export const LLMS_TXT_PATH = "/llms.txt";
export const LLMS_TXT_URL = `${SITE_ORIGIN}${LLMS_TXT_PATH}`;
export const SEARCH_INDEX_JSON_PATH = "/search-index.json";
export const SEARCH_INDEX_JSON_URL = `${SITE_ORIGIN}${SEARCH_INDEX_JSON_PATH}`;
export const FEED_XML_PATH = "/feed.xml";
export const FEED_XML_URL = `${SITE_ORIGIN}${FEED_XML_PATH}`;
export const SEARCH_INDEX_DOC_PATH = "/search-index/";
export const SEARCH_INDEX_DOC_URL = `${SITE_ORIGIN}${SEARCH_INDEX_DOC_PATH}`;
/** Cloudflare Web Analytics beacon token (public; override with PUBLIC_CF_WEB_ANALYTICS_TOKEN). */
export const CF_WEB_ANALYTICS_TOKEN = "415dc5b7862f4b47a7f41047bbd6c81e";

/** Build an absolute URL on the deployed site (respects trailing-slash routes). */
export function absoluteSiteUrl(pathname: string, origin = SITE_ORIGIN): string {
  const normalized = pathname.startsWith("/") ? pathname : `/${pathname}`;
  return new URL(normalized, origin).href;
}

export function pageTitle(title?: string): string {
  if (!title || title === SITE_NAME) return SITE_NAME;
  return `${title} | ${SITE_NAME}`;
}

/** Keep meta descriptions within typical search/snippet limits. */
export function truncateDescription(text: string, maxLength = 160): string {
  const trimmed = text.replace(/\s+/g, " ").trim();
  if (trimmed.length <= maxLength) return trimmed;
  return `${trimmed.slice(0, maxLength - 1).trimEnd()}…`;
}
