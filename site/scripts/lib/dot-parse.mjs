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

  const nodeRe = /^\s*([A-Za-z_][\w]*)\s*\[([^\]]+)\]\s*;?\s*$/gm;
  let match;
  while ((match = nodeRe.exec(text)) !== null) {
    const id = match[1];
    if (id === "graph" || id === "node" || id === "edge") continue;
    const attrs = parseAttrs(match[2]);
    nodes.set(id, {
      id,
      label: attrs.label || id,
      shape: attrs.shape || "box",
      fillcolor: attrs.fillcolor || "",
      style: attrs.style || "",
      penwidth: attrs.penwidth || ""
    });
  }

  const edgeRe = /^\s*([A-Za-z_][\w]*)\s*->\s*([A-Za-z_][\w]*)(?:\s*\[([^\]]+)\])?\s*;?\s*$/gm;
  while ((match = edgeRe.exec(text)) !== null) {
    const attrs = parseAttrs(match[3] || "");
    edges.push({
      from: match[1],
      to: match[2],
      label: attrs.label || "",
      dashed: (attrs.style || "").includes("dashed"),
      color: attrs.color || ""
    });
    if (!nodes.has(match[1])) nodes.set(match[1], { id: match[1], label: match[1] });
    if (!nodes.has(match[2])) nodes.set(match[2], { id: match[2], label: match[2] });
  }

  const graphMatch = text.match(/label\s*=\s*"([^"]*(?:\\.[^"]*)*)"/);
  const title = graphMatch ? unquote(`"${graphMatch[1]}"`) : "";

  return {
    title,
    nodes: [...nodes.values()],
    edges
  };
}
