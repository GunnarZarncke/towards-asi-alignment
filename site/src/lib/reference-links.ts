export type ReferenceLink = {
  label: string;
  url: string;
};

type BibEntry = {
  doi?: string;
  url?: string;
};

export function doiHref(doi: string) {
  const normalized = doi.replace(/^https?:\/\/doi.org\//i, "").trim();
  return `https://doi.org/${normalized}`;
}

/** Resolve DOI/URL links for a reference card from frontmatter and bibliography JSON. */
export function referenceLinksFor(
  external: ReferenceLink[],
  bibEntry?: BibEntry | null
): ReferenceLink[] {
  if (external.length > 0) return external;

  const links: ReferenceLink[] = [];
  if (bibEntry?.doi) {
    links.push({ label: "DOI", url: doiHref(bibEntry.doi) });
  }
  if (bibEntry?.url) {
    links.push({ label: "URL", url: bibEntry.url });
  }
  return links;
}

export function formatExternalLinksYaml(links: ReferenceLink[]) {
  if (links.length === 0) return "external: []";
  return [
    "external:",
    ...links.map(
      (link) =>
        `  - label: ${JSON.stringify(link.label)}\n    url: ${JSON.stringify(link.url)}`
    )
  ].join("\n");
}
