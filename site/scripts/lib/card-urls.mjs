/** Canonical card URL paths: /cards/{type-segment}/{local-slug}/ */

/** @typedef {import('../../src/lib/badges.ts').CardType} CardType */

/** @type {Record<string, string>} */
export const TYPE_URL_SEGMENT = {
  concept: "concept",
  bridge: "bridge",
  objection: "objection",
  artifact: "artifact",
  glossary: "glossary",
  chapter: "chapter",
  appendix: "appendix",
  frontmatter: "frontmatter",
  reference: "reference",
  experiment: "experiment",
  release: "release",
  news: "news",
  agenda: "agenda",
  funding: "funding"
};

/**
 * @param {string} id
 * @param {string | null | undefined} type
 * @returns {string | null}
 */
export function inferTypeFromCardId(id, type) {
  if (type && type !== "essay") return type;
  if (id.startsWith("chapters/")) {
    const local = id.slice("chapters/".length);
    if (local === "frontmatter") return "frontmatter";
    if (/^app/i.test(local)) return "appendix";
    return "chapter";
  }
  if (id.startsWith("references/")) return "reference";
  if (id.startsWith("experiments/")) return "experiment";
  if (id.startsWith("field-agendas/")) return "agenda";
  if (id.startsWith("funding/")) return "funding";
  return type ?? null;
}

/**
 * Local slug under the type segment (no type prefix).
 * @param {string} id
 * @param {string} type
 */
export function cardLocalSlug(id, type) {
  if (type === "chapter" || type === "appendix") {
    return id.replace(/^chapters\//i, "");
  }
  if (type === "frontmatter") return "";
  if (type === "reference") return id.replace(/^references\//, "");
  if (type === "experiment") return id.replace(/^experiments\//, "");
  if (type === "agenda") return id.replace(/^field-agendas\//, "");
  if (type === "funding") return id.replace(/^funding\//, "");
  if (id.includes("/")) return id.split("/").pop() ?? id;
  return id;
}

/**
 * Route slug segments under /cards/ (no leading or trailing slash).
 * @param {{ id: string, type?: string | null }} card
 */
export function cardRouteSlug(card) {
  const type = inferTypeFromCardId(card.id, card.type);
  if (!type || type === "essay") return null;
  const segment = TYPE_URL_SEGMENT[type];
  if (!segment) return null;
  const local = cardLocalSlug(card.id, type);
  if (type === "frontmatter") return segment;
  return `${segment}/${routeSlug(local)}`;
}

/** @param {string} segment */
export function routeSlug(segment) {
  return segment.toLowerCase();
}

/**
 * Legacy path under /cards/ before type-prefix migration.
 * @param {string} id
 */
export function legacyCardRouteSlug(id) {
  return id
    .split("/")
    .map((part) => routeSlug(part))
    .join("/");
}

/**
 * Root-relative href under /cards/ (or /essay/ for essays).
 * @param {{ id: string, type?: string | null }} card
 */
export function cardPublicPath(card) {
  if (card.type === "essay" || inferTypeFromCardId(card.id, card.type) === "essay") {
    const local = cardLocalSlug(card.id, "essay");
    return `/essay/${routeSlug(local)}/`;
  }
  const slug = cardRouteSlug(card);
  if (!slug) return `/cards/${legacyCardRouteSlug(card.id)}/`;
  return `/cards/${slug}/`;
}

/**
 * @param {string} base
 * @param {{ id: string, type?: string | null }} card
 */
export function cardPublicHref(base, card) {
  const path = cardPublicPath(card);
  const normalized = base.endsWith("/") ? base.slice(0, -1) : base;
  if (path.startsWith("/")) return `${normalized}${path}`;
  return `${normalized}/${path}`;
}

/**
 * @param {string} base
 * @param {string} chapterId
 */
export function bookPublicHref(base, chapterId) {
  const type = inferTypeFromCardId(`chapters/${chapterId}`, null);
  return cardPublicHref(base, { id: `chapters/${chapterId}`, type });
}

/**
 * @param {string} base
 * @param {string} chapterId
 */
export function bookFullPublicHref(base, chapterId) {
  const href = bookPublicHref(base, chapterId);
  return href.endsWith("/") ? `${href}full/` : `${href}/full/`;
}

/**
 * Parse card content type from a normalized site path (for visit history).
 * @param {string} pathname
 * @returns {string | null}
 */
export function cardTypeFromPath(pathname) {
  const path = pathname.endsWith("/") ? pathname : `${pathname}/`;
  const match = path.match(/^\/cards\/([^/]+)(?:\/([^/]+))?\/?$/);
  if (!match) return null;
  const [, first, second] = match;
  if (first === "frontmatter") return "frontmatter";
  if (!second) return null;
  const segment = first.toLowerCase();
  for (const [type, urlSegment] of Object.entries(TYPE_URL_SEGMENT)) {
    if (urlSegment === segment) return type;
  }
  return null;
}

/**
 * Legacy /cards/... path → new path, or null if already canonical / unknown.
 * @param {string} slugParam - catch-all slug without /cards/ prefix
 */
export function legacyCardRedirectPath(slugParam) {
  if (!slugParam) return null;
  const parts = slugParam.split("/").filter(Boolean);
  let showFull = false;
  if (parts[parts.length - 1] === "full") {
    showFull = true;
    parts.pop();
  }

  const joined = parts.join("/");
  if (!joined) return null;

  // Already type-prefixed?
  const first = parts[0]?.toLowerCase();
  if (first && Object.values(TYPE_URL_SEGMENT).includes(first) && parts.length >= 1) {
    if (first === "frontmatter" && parts.length === 1) return null;
    if (parts.length >= 2) return null;
  }

  // Old chapters/*
  if (first === "chapters" && parts[1]) {
    const local = parts[1];
    let type = "chapter";
    if (local.toLowerCase() === "frontmatter") type = "frontmatter";
    else if (/^app/i.test(local)) type = "appendix";
    const card = { id: `chapters/${local}`, type };
    const target = cardPublicPath(card).replace(/\/$/, "");
    return showFull ? `${target}/full/` : `${target}/`;
  }

  // Old field-agendas/*
  if (first === "field-agendas" && parts[1]) {
    const target = cardPublicPath({ id: `field-agendas/${parts[1]}`, type: "agenda" }).replace(/\/$/, "");
    return showFull ? `${target}/full/` : `${target}/`;
  }

  // Old experiments/*
  if (first === "experiments" && parts[1]) {
    const target = cardPublicPath({ id: `experiments/${parts[1]}`, type: "experiment" }).replace(/\/$/, "");
    return showFull ? `${target}/full/` : `${target}/`;
  }

  // Old references/*
  if (first === "references" && parts[1]) {
    const target = cardPublicPath({ id: `references/${parts[1]}`, type: "reference" }).replace(/\/$/, "");
    return showFull ? `${target}/full/` : `${target}/`;
  }

  // Flat legacy slug — cannot redirect without card type lookup
  return null;
}

/**
 * @param {Array<{ id: string, data?: { type?: string }, type?: string }>} cards
 * @param {string} slugParam
 */
export function resolveCardFromRoute(cards, slugParam) {
  if (!slugParam) return null;
  const parts = slugParam.split("/").filter(Boolean);
  let showFull = false;
  if (parts[parts.length - 1] === "full") {
    showFull = true;
    parts.pop();
  }
  const routeKey = parts.join("/");

  for (const card of cards) {
    const type = card.data?.type ?? card.type;
    const slug = cardRouteSlug({ id: card.id, type });
    if (slug === routeKey) {
      return { card, showFull };
    }
  }

  // Legacy id exact match (pre-migration bookmarks)
  const normalized = routeKey.split("/").map(routeSlug).join("/");
  const legacy = cards.find((card) => legacyCardRouteSlug(card.id) === normalized);
  if (legacy) return { card: legacy, showFull };

  return null;
}

/**
 * Build redirect map for astro.config (legacy → canonical).
 * @param {Array<{ id: string, data?: { type?: string }, type?: string }>} cards
 */
export function buildCardRedirects(cards) {
  /** @type {Record<string, string>} */
  const redirects = {};

  for (const card of cards) {
    const type = card.data?.type ?? card.type;
    if (type === "essay") {
      const legacy = `/cards/${legacyCardRouteSlug(card.id)}/`;
      const target = cardPublicPath({ id: card.id, type: "essay" });
      if (legacy !== target) redirects[legacy] = target;
      continue;
    }

    const canonical = cardPublicPath({ id: card.id, type });
    const legacy = `/cards/${legacyCardRouteSlug(card.id)}/`;
    if (legacy !== canonical) redirects[legacy] = canonical;

    if (card.data?.overviewOnly || card.overviewOnly) {
      const legacyFull = `${legacy}full/`;
      const canonicalFull = canonical.endsWith("/") ? `${canonical}full/` : `${canonical}/full/`;
      if (legacyFull !== canonicalFull) redirects[legacyFull] = canonicalFull;
    }
  }

  // releases-updates → /updates/ stays in page redirect
  return redirects;
}
