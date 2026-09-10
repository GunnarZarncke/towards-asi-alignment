/** Make inlined Graphviz node links resolve from any page, with Astro `base`. */

function withBase(base: string, path: string) {
  const prefix = base.endsWith("/") ? base : `${base}/`;
  return `${prefix}${path.replace(/^\/+/, "")}`;
}

/** Map sync-era relative hrefs (written for `/lean/graph/{slug}/`) to site-root paths. */
export function siteRootGraphHref(href: string) {
  if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith("//")) return href;
  if (href.startsWith("../../graph/")) return `/lean/${href.slice("../../".length)}`;
  if (href.startsWith("../../node/")) return `/lean/${href.slice("../../".length)}`;
  if (href.startsWith("../../cards/")) return href.slice("../..".length);
  return href;
}

export function fixGraphSvgHrefs(svg: string, base = "/") {
  return svg.replace(/xlink:href="([^"]+)"/g, (_, href: string) => {
    const rooted = siteRootGraphHref(href);
    const next = rooted.startsWith("/") ? withBase(base, rooted) : rooted;
    return `xlink:href="${next}"`;
  });
}
