/** Resolve Lean declaration names to GitHub source and optional spine graph node pages. */

const REPO_BLOB_BASE = "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main";

export interface LeanDeclEntry {
  kind: string;
  file: string;
  githubUrl: string;
  graphNodeId?: string;
}

export interface LeanDeclLinks {
  githubUrl: string;
  graphNodeHref: string | null;
  file: string;
  found: boolean;
}

export function normalizeModulePath(module: string): string {
  const trimmed = module.replace(/^AlignmentProofSpine\//, "");
  return `formal/AlignmentProofSpine/${trimmed}`;
}

export function resolveLeanDeclLinks(
  declName: string,
  moduleFallback: string,
  declIndex: Record<string, LeanDeclEntry>,
  baseUrl: string
): LeanDeclLinks {
  const withBase = (path: string) => {
    const normalized = path.replace(/^\/+/, "");
    return baseUrl.endsWith("/") ? `${baseUrl}${normalized}` : `${baseUrl}/${normalized}`;
  };
  const entry = declIndex[declName];

  if (entry) {
    return {
      githubUrl: entry.githubUrl,
      graphNodeHref: entry.graphNodeId
        ? withBase(`/lean/node/${encodeURIComponent(entry.graphNodeId)}/`)
        : null,
      file: entry.file,
      found: true
    };
  }

  const file = normalizeModulePath(moduleFallback);
  return {
    githubUrl: `${REPO_BLOB_BASE}/${file}`,
    graphNodeHref: null,
    file,
    found: false
  };
}
