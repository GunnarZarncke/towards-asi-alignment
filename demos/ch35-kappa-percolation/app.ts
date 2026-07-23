/**
 * kappa-edge percolation simulator
 *
 * Illustrates chapters/ch35-multi-agent-strategic-coupling.tex, subsection
 * "Percolation and Inferential Coupling": social (causal) edges exist first;
 * a cooperative edge is only "open" when kappa = (b/c) * p * rho > 1. The
 * failure mode the chapter warns about is visible when the social graph has
 * a giant component but the kappa-open graph does not: communication exists,
 * but cooperative correction does not conduct.
 */

export type Distribution = "homogeneous" | "lognormal" | "power" | "hub";

export type Params = {
  communities: number;
  nodesPerCommunity: number;
  avgDegree: number;
  distribution: Distribution;
  communityMixing: number;
  strengthContrast: number;
  benefitCost: number;
};

export type NodeDatum = {
  id: number;
  community: number;
  theta: number;
  x: number;
  y: number;
};

export type EdgeDatum = {
  source: number;
  target: number;
  bridge: boolean;
  strength: number;
  pReach: number;
  rho: number;
  kappa: number;
  cooperative: boolean;
};

export type GraphResult = {
  nodes: NodeDatum[];
  edges: EdgeDatum[];
  stats: {
    socialLargest: number;
    coopLargest: number;
    socialLargestFrac: number;
    coopLargestFrac: number;
    avgDegree: number;
    avgDegreeSquared: number;
    phi: number;
    phiCritical: number;
    meanKappa: number;
    bridgeEdges: number;
    coopBridgeEdges: number;
  };
};

export const defaultParams: Params = {
  communities: 5,
  nodesPerCommunity: 18,
  avgDegree: 5.2,
  distribution: "lognormal",
  communityMixing: 0.16,
  strengthContrast: 0.62,
  benefitCost: 2.2,
};

class Rng {
  private state: number;

  constructor(seed: number) {
    this.state = seed >>> 0;
  }

  next(): number {
    this.state = (1664525 * this.state + 1013904223) >>> 0;
    return this.state / 4294967296;
  }

  normal(): number {
    const u = Math.max(this.next(), 1e-9);
    const v = Math.max(this.next(), 1e-9);
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
}

const clamp = (x: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, x));

const mean = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;

function makeActivities(n: number, distribution: Distribution, rng: Rng): number[] {
  let values: number[];

  if (distribution === "homogeneous") {
    values = Array.from({ length: n }, () => 1);
  } else if (distribution === "lognormal") {
    values = Array.from({ length: n }, () => Math.exp(1.05 * rng.normal()));
  } else if (distribution === "power") {
    const alpha = 2.3;
    values = Array.from({ length: n }, () => {
      const u = Math.max(rng.next(), 1e-9);
      const pareto = 1 / Math.pow(1 - u, 1 / alpha);
      return Math.min(pareto, 18);
    });
  } else {
    values = Array.from({ length: n }, () => (rng.next() < 0.07 ? 9 : 0.45));
  }

  const m = mean(values);
  return values.map((v) => v / m);
}

function placeNodes(params: Params, theta: number[], rng: Rng): NodeDatum[] {
  const width = 720;
  const height = 420;
  const cx = width / 2;
  const cy = height / 2;
  const bigR = params.communities === 1 ? 0 : 140;
  const smallR = clamp(65 / Math.sqrt(params.communities), 16, 46);
  const nodes: NodeDatum[] = [];

  for (let g = 0; g < params.communities; g++) {
    const a = (2 * Math.PI * g) / params.communities - Math.PI / 2;
    const gx = cx + bigR * Math.cos(a);
    const gy = cy + bigR * Math.sin(a) * 0.72;

    for (let j = 0; j < params.nodesPerCommunity; j++) {
      const id = g * params.nodesPerCommunity + j;
      const r = smallR * Math.sqrt(rng.next());
      const b = 2 * Math.PI * rng.next();

      nodes.push({
        id,
        community: g,
        theta: theta[id],
        x: gx + r * Math.cos(b),
        y: gy + r * Math.sin(b),
      });
    }
  }

  return nodes;
}

function expectedAvgDegree(nodes: NodeDatum[], lambda: number, mixing: number): number {
  let sumProb = 0;

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const same = nodes[i].community === nodes[j].community;
      const block = same ? 1 : mixing;
      const q = clamp(lambda * nodes[i].theta * nodes[j].theta * block, 0, 0.95);
      sumProb += q;
    }
  }

  return (2 * sumProb) / nodes.length;
}

function calibrateLambda(nodes: NodeDatum[], targetAvgDegree: number, mixing: number): number {
  let lo = 0;
  let hi = 1;

  while (expectedAvgDegree(nodes, hi, mixing) < targetAvgDegree && hi < 1000) {
    hi *= 2;
  }

  for (let iter = 0; iter < 28; iter++) {
    const mid = (lo + hi) / 2;
    if (expectedAvgDegree(nodes, mid, mixing) < targetAvgDegree) lo = mid;
    else hi = mid;
  }

  return (lo + hi) / 2;
}

function largestComponentSize(n: number, edges: EdgeDatum[], edgeFilter: (e: EdgeDatum) => boolean): number {
  const adj: number[][] = Array.from({ length: n }, () => []);

  for (const e of edges) {
    if (!edgeFilter(e)) continue;
    adj[e.source].push(e.target);
    adj[e.target].push(e.source);
  }

  const seen = new Array<boolean>(n).fill(false);
  let best = 0;

  for (let start = 0; start < n; start++) {
    if (seen[start]) continue;

    let size = 0;
    const stack = [start];
    seen[start] = true;

    while (stack.length > 0) {
      const v = stack.pop()!;
      size++;

      for (const u of adj[v]) {
        if (!seen[u]) {
          seen[u] = true;
          stack.push(u);
        }
      }
    }

    best = Math.max(best, size);
  }

  return best;
}

export function makeGraph(params: Params): GraphResult {
  const rng = new Rng(12345);
  const n = params.communities * params.nodesPerCommunity;
  const theta = makeActivities(n, params.distribution, rng);
  const nodes = placeNodes(params, theta, rng);
  const lambda = calibrateLambda(nodes, params.avgDegree, params.communityMixing);

  const edges: EdgeDatum[] = [];

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const same = nodes[i].community === nodes[j].community;
      const block = same ? 1 : params.communityMixing;
      const q = clamp(lambda * nodes[i].theta * nodes[j].theta * block, 0, 0.95);

      if (rng.next() > q) continue;

      const localMean = 0.6 + 0.35 * params.strengthContrast;
      const bridgeMean = 0.6 - 0.42 * params.strengthContrast;
      const strengthMean = same ? localMean : bridgeMean;
      const strength = clamp(strengthMean + 0.08 * rng.normal(), 0.03, 1);

      // Absence of an edge means p = 0. For existing edges, pReach is the
      // conditional probability that a cooperative act actually reaches the other side.
      const pReach = clamp(0.12 + 0.86 * strength, 0, 1);

      // rho is predictive or value correlation. Strength is not enough. Weak bridge
      // ties can exist and reach, but still have low rho.
      const rho = Math.pow(strength, 1.35);

      const kappa = params.benefitCost * pReach * rho;

      edges.push({
        source: i,
        target: j,
        bridge: !same,
        strength,
        pReach,
        rho,
        kappa,
        cooperative: kappa > 1,
      });
    }
  }

  const degrees = new Array<number>(n).fill(0);
  for (const e of edges) {
    degrees[e.source]++;
    degrees[e.target]++;
  }

  const avgDegree = mean(degrees);
  const avgDegreeSquared = mean(degrees.map((k) => k * k));
  const denom = avgDegreeSquared - avgDegree;
  const phiCritical = denom > 0 ? avgDegree / denom : Infinity;

  const coopEdges = edges.filter((e) => e.cooperative);
  const bridgeEdges = edges.filter((e) => e.bridge).length;
  const coopBridgeEdges = edges.filter((e) => e.bridge && e.cooperative).length;

  const socialLargest = largestComponentSize(n, edges, () => true);
  const coopLargest = largestComponentSize(n, edges, (e) => e.cooperative);

  return {
    nodes,
    edges,
    stats: {
      socialLargest,
      coopLargest,
      socialLargestFrac: socialLargest / n,
      coopLargestFrac: coopLargest / n,
      avgDegree,
      avgDegreeSquared,
      phi: edges.length === 0 ? 0 : coopEdges.length / edges.length,
      phiCritical,
      meanKappa: edges.length === 0 ? 0 : mean(edges.map((e) => e.kappa)),
      bridgeEdges,
      coopBridgeEdges,
    },
  };
}

function nodeColor(community: number, communities: number): string {
  const hue = Math.round((360 * community) / Math.max(communities, 1));
  return `hsl(${hue} 62% 55%)`;
}

const SVG_NS = "http://www.w3.org/2000/svg";

function svgEl<K extends keyof SVGElementTagNameMap>(
  tag: K,
  attrs: Record<string, string> = {},
): SVGElementTagNameMap[K] {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
  return el;
}

function createElement<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string> = {},
  text?: string,
): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
  if (text !== undefined) el.textContent = text;
  return el;
}

type SliderDef = {
  key: keyof Params;
  label: string;
  min: number;
  max: number;
  step: number;
};

const sliderDefs: SliderDef[] = [
  { key: "communities", label: "Communities", min: 1, max: 9, step: 1 },
  { key: "nodesPerCommunity", label: "Nodes per community", min: 6, max: 36, step: 1 },
  { key: "avgDegree", label: "Average degree", min: 1, max: 12, step: 0.2 },
  { key: "communityMixing", label: "Community mixing", min: 0, max: 1, step: 0.01 },
  { key: "strengthContrast", label: "Strength contrast", min: 0, max: 1, step: 0.01 },
  { key: "benefitCost", label: "Benefit / cost", min: 0.2, max: 6, step: 0.05 },
];

function fmtValue(v: number): string {
  return Number.isInteger(v) ? String(v) : v.toFixed(2);
}

export function mountKappaPercolationDemo(container: HTMLElement, initial: Params = defaultParams) {
  let params: Params = { ...initial };

  container.innerHTML = "";
  container.classList.add("kappa-demo");

  const style = createElement("style");
  style.textContent = `
    .kappa-demo { font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; max-width: 1100px; border: 1px solid #e2e8f0; border-radius: 18px; padding: 16px; background: #fff; color: #0f172a; box-sizing: border-box; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); }
    .kappa-demo * { box-sizing: border-box; }
    .kd-header { display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; margin-bottom: 12px; flex-wrap: wrap; }
    .kd-title { margin: 0; font-size: 22px; letter-spacing: -0.02em; }
    .kd-subtitle { margin: 4px 0 0; font-size: 13px; color: #475569; max-width: 60ch; }
    .kd-badge { font-size: 13px; font-weight: 700; padding: 7px 10px; border-radius: 999px; background: #ecfdf5; color: #166534; white-space: nowrap; }
    .kd-body { display: grid; grid-template-columns: minmax(0, 1fr) 290px; gap: 14px; align-items: stretch; }
    @media (max-width: 780px) { .kd-body { grid-template-columns: 1fr; } }
    .kd-svg { width: 100%; height: min(46vh, 430px); min-height: 300px; display: block; border-radius: 18px; border: 1px solid #e2e8f0; }
    .kd-legend { display: flex; gap: 14px; align-items: center; flex-wrap: wrap; margin-top: 8px; font-size: 12px; color: #475569; }
    .kd-line-sample { display: inline-block; width: 24px; height: 3px; border-radius: 4px; margin-right: 5px; vertical-align: middle; }
    .kd-controls { display: flex; flex-direction: column; gap: 10px; padding: 12px; border-radius: 16px; background: #f8fafc; border: 1px solid #e2e8f0; }
    .kd-control { display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #334155; }
    .kd-control-top { display: flex; justify-content: space-between; gap: 12px; }
    .kd-select { width: 100%; border: 1px solid #cbd5e1; border-radius: 9px; padding: 6px 8px; background: white; color: #0f172a; }
    .kd-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin-top: 12px; }
    @media (min-width: 620px) { .kd-stats { grid-template-columns: repeat(6, minmax(0, 1fr)); } }
    .kd-stat { border: 1px solid #e2e8f0; border-radius: 12px; padding: 9px 10px; background: #fff; }
    .kd-stat-value { font-size: 18px; font-weight: 800; letter-spacing: -0.02em; }
    .kd-stat-label { font-size: 11px; color: #64748b; margin-top: 2px; }
    .kd-note { margin: 12px 2px 0; font-size: 13px; line-height: 1.45; color: #475569; }
  `;
  container.appendChild(style);

  const header = createElement("div", { class: "kd-header" });
  const headerLeft = createElement("div");
  headerLeft.appendChild(createElement("h2", { class: "kd-title" }, "\u03ba-edge percolation simulator"));
  headerLeft.appendChild(
    createElement(
      "p",
      { class: "kd-subtitle" },
      "Social edges exist first. A cooperative edge opens only when \u03ba = (b/c) \u00b7 p \u00b7 \u03c1 > 1.",
    ),
  );
  header.appendChild(headerLeft);
  const badge = createElement("div", { class: "kd-badge" });
  header.appendChild(badge);
  container.appendChild(header);

  const body = createElement("div", { class: "kd-body" });
  container.appendChild(body);

  const graphPanel = createElement("div");
  const svg = svgEl("svg", { viewBox: "0 0 720 420", class: "kd-svg", role: "img" });
  const bg = svgEl("rect", { x: "0", y: "0", width: "720", height: "420", rx: "18", fill: "#f8fafc" });
  svg.appendChild(bg);
  const edgesGroup = svgEl("g");
  const nodesGroup = svgEl("g");
  svg.appendChild(edgesGroup);
  svg.appendChild(nodesGroup);
  graphPanel.appendChild(svg);

  const legend = createElement("div", { class: "kd-legend" });
  const legendCoop = createElement("span");
  legendCoop.appendChild(createElement("i", { class: "kd-line-sample", style: "background:#16a34a" }));
  legendCoop.appendChild(document.createTextNode(" \u03ba > 1"));
  const legendSocial = createElement("span");
  legendSocial.appendChild(
    createElement("i", { class: "kd-line-sample", style: "background:#64748b;opacity:0.4" }),
  );
  legendSocial.appendChild(document.createTextNode(" social only"));
  const legendBridge = createElement("span", {}, "dashed = bridge tie");
  legend.appendChild(legendCoop);
  legend.appendChild(legendSocial);
  legend.appendChild(legendBridge);
  graphPanel.appendChild(legend);
  body.appendChild(graphPanel);

  const controls = createElement("div", { class: "kd-controls" });
  body.appendChild(controls);

  const sliderValueEls = new Map<keyof Params, HTMLElement>();

  function makeSlider(def: SliderDef) {
    const wrap = createElement("label", { class: "kd-control" });
    const top = createElement("span", { class: "kd-control-top" });
    top.appendChild(createElement("span", {}, def.label));
    const valueEl = createElement("strong", {}, fmtValue(params[def.key] as number));
    top.appendChild(valueEl);
    sliderValueEls.set(def.key, valueEl);
    wrap.appendChild(top);

    const input = createElement("input", {
      type: "range",
      min: String(def.min),
      max: String(def.max),
      step: String(def.step),
    }) as HTMLInputElement;
    input.value = String(params[def.key]);
    input.addEventListener("input", () => {
      const v = Number(input.value);
      (params as any)[def.key] = v;
      valueEl.textContent = fmtValue(v);
      render();
    });
    wrap.appendChild(input);
    controls.appendChild(wrap);
  }

  makeSlider(sliderDefs[0]);
  makeSlider(sliderDefs[1]);
  makeSlider(sliderDefs[2]);

  const distWrap = createElement("label", { class: "kd-control" });
  const distTop = createElement("span", { class: "kd-control-top" });
  distTop.appendChild(createElement("span", {}, "Degree distribution"));
  const distValue = createElement("strong", {}, params.distribution);
  distTop.appendChild(distValue);
  distWrap.appendChild(distTop);
  const distSelect = createElement("select", { class: "kd-select" }) as HTMLSelectElement;
  (["homogeneous", "lognormal", "power", "hub"] as Distribution[]).forEach((d) => {
    const option = createElement("option", { value: d }, d) as HTMLOptionElement;
    if (d === params.distribution) option.selected = true;
    distSelect.appendChild(option);
  });
  distSelect.addEventListener("change", () => {
    params = { ...params, distribution: distSelect.value as Distribution };
    distValue.textContent = distSelect.value;
    render();
  });
  distWrap.appendChild(distSelect);
  controls.appendChild(distWrap);

  makeSlider(sliderDefs[3]);
  makeSlider(sliderDefs[4]);
  makeSlider(sliderDefs[5]);

  const statsEl = createElement("div", { class: "kd-stats" });
  container.appendChild(statsEl);

  const note = createElement(
    "p",
    { class: "kd-note" },
    "The key failure mode is visible when the social graph has a giant component but the \u03ba-open graph does not. Communication exists, but cooperative correction does not conduct.",
  );
  container.appendChild(note);

  function stat(label: string, value: string): HTMLElement {
    const el = createElement("div", { class: "kd-stat" });
    el.appendChild(createElement("div", { class: "kd-stat-value" }, value));
    el.appendChild(createElement("div", { class: "kd-stat-label" }, label));
    return el;
  }

  function render() {
    const graph = makeGraph(params);

    edgesGroup.innerHTML = "";
    for (const e of graph.edges) {
      const a = graph.nodes[e.source];
      const b = graph.nodes[e.target];
      const width = e.cooperative ? 1.6 + 2.2 * e.strength : 0.6;
      const opacity = e.cooperative ? 0.75 : 0.15;
      const stroke = e.cooperative ? "#16a34a" : "#64748b";
      const line = svgEl("line", {
        x1: String(a.x),
        y1: String(a.y),
        x2: String(b.x),
        y2: String(b.y),
        stroke,
        "stroke-width": String(width),
        opacity: String(opacity),
      });
      if (e.bridge) line.setAttribute("stroke-dasharray", "4 5");
      edgesGroup.appendChild(line);
    }

    nodesGroup.innerHTML = "";
    for (const n of graph.nodes) {
      const r = clamp(3.2 + Math.sqrt(n.theta) * 2.1, 3, 8.5);
      const circle = svgEl("circle", {
        cx: String(n.x),
        cy: String(n.y),
        r: String(r),
        fill: nodeColor(n.community, params.communities),
        stroke: "#0f172a",
        "stroke-width": "0.7",
        opacity: "0.94",
      });
      const title = svgEl("title");
      title.textContent = `node ${n.id}, community ${n.community + 1}, activity ${n.theta.toFixed(2)}`;
      circle.appendChild(title);
      nodesGroup.appendChild(circle);
    }

    const criticalText = graph.stats.phiCritical === Infinity ? "\u221e" : graph.stats.phiCritical.toFixed(2);
    const verdict =
      graph.stats.coopLargestFrac > 0.5
        ? "Cooperation percolates"
        : graph.stats.socialLargestFrac > 0.5
        ? "Social graph connected, cooperation fragmented"
        : "Social graph fragmented";
    badge.textContent = verdict;

    statsEl.innerHTML = "";
    statsEl.appendChild(stat("Social giant", `${Math.round(100 * graph.stats.socialLargestFrac)}%`));
    statsEl.appendChild(stat("Coop giant", `${Math.round(100 * graph.stats.coopLargestFrac)}%`));
    statsEl.appendChild(stat("\u03c6 = open edge share", graph.stats.phi.toFixed(2)));
    statsEl.appendChild(stat("\u03c6 critical", criticalText));
    statsEl.appendChild(stat("Mean \u03ba", graph.stats.meanKappa.toFixed(2)));
    statsEl.appendChild(stat("Coop bridges", `${graph.stats.coopBridgeEdges}/${graph.stats.bridgeEdges}`));
  }

  render();

  return {
    getParams: () => ({ ...params }),
    setParams: (next: Params) => {
      params = { ...next };
      render();
    },
  };
}

declare global {
  interface Window {
    mountKappaPercolationDemo?: typeof mountKappaPercolationDemo;
  }
}

if (typeof window !== "undefined") {
  window.mountKappaPercolationDemo = mountKappaPercolationDemo;
  const autoMount = document.getElementById("kappa-percolation-demo");
  if (autoMount) mountKappaPercolationDemo(autoMount);
}
