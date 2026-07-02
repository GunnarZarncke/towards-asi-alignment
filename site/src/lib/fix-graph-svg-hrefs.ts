/** Adjust Graphviz SVG link targets when embedded off the graph route. */
export function fixGraphSvgHrefs(svg: string, mode: "graph-page" | "lean-index") {
  if (mode === "graph-page") return svg;
  return svg
    .replace(/xlink:href="\.\.\/\.\.\/graph\//g, 'xlink:href="graph/')
    .replace(/xlink:href="\.\.\/\.\.\/node\//g, 'xlink:href="node/')
    .replace(/xlink:href="\.\.\/\.\.\/cards\//g, 'xlink:href="../cards/');
}
