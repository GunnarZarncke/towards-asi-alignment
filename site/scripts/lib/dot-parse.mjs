/** Minimal Graphviz .dot parser for lean_proof_graphs/*.dot */

function unquote(value) {
  if (!value) return "";
  const trimmed = value.trim();
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
    return trimmed.slice(1, -1).replace(/\\n/g, "\n").replace(/\\"/g, '"');
  }
  return trimmed;
}

function parseAttrs(raw) {
  const attrs = {};
  const re = /(\w+)\s*=\s*("(?:\\.|[^"\\])*"|[^,\]]+)/g;
  let match;
  while ((match = re.exec(raw)) !== null) {
    attrs[match[1]] = unquote(match[2]);
  }
  return attrs;
}

export function parseDot(text) {
  const nodes = new Map();
  const edges = [];

  const nodeRe = /^\s*(?:"([^"]+)"|([A-Za-z_][\w]*))\s*\[([^\]]+)\]\s*;?\s*$/gm;
  let match;
  while ((match = nodeRe.exec(text)) !== null) {
    const id = match[1] || match[2];
    if (id === "graph" || id === "node" || id === "edge") continue;
    const attrs = parseAttrs(match[3]);
    nodes.set(id, {
      id,
      label: attrs.label || id,
      shape: attrs.shape || "box",
      fillcolor: attrs.fillcolor || "",
      style: attrs.style || "",
      penwidth: attrs.penwidth || ""
    });
  }

  const edgeRe =
    /^\s*(?:"([^"]+)"|([A-Za-z_][\w]*))\s*->\s*(?:"([^"]+)"|([A-Za-z_][\w]*))(?:\s*\[([^\]]+)\])?\s*;?\s*$/gm;
  while ((match = edgeRe.exec(text)) !== null) {
    const from = match[1] || match[2];
    const to = match[3] || match[4];
    const attrs = parseAttrs(match[5] || "");
    edges.push({
      from,
      to,
      label: attrs.label || "",
      dashed: (attrs.style || "").includes("dashed"),
      color: attrs.color || ""
    });
    if (!nodes.has(from)) nodes.set(from, { id: from, label: from });
    if (!nodes.has(to)) nodes.set(to, { id: to, label: to });
  }

  const graphMatch = text.match(/label\s*=\s*"([^"]*(?:\\.[^"]*)*)"/);
  const title = graphMatch ? unquote(`"${graphMatch[1]}"`) : "";

  return {
    title,
    nodes: [...nodes.values()],
    edges
  };
}
