// ch05-field-spring-map/weights.ts
var LIVE_BRIDGES = [
  "MB1",
  "MB2",
  "MB3",
  "MB4",
  "MB4a",
  "MB5",
  "MB6",
  "MB7",
  "MB7d",
  "MB9",
  "MB10",
  "MB11"
];
var PINNED_LISTING_IDS = /* @__PURE__ */ new Set(["rec1QpsZCIfnfTF1y"]);
var RESEARCH_CATEGORIES = /* @__PURE__ */ new Set([
  "Conceptual research",
  "Empirical research",
  "Capabilities research",
  "Strategy",
  "Governance",
  "Forecasting"
]);
function categoryParts(category) {
  return category.split(",").map((p) => p.trim()).filter(Boolean);
}
function isResearchListing(category) {
  return categoryParts(category).some((p) => RESEARCH_CATEGORIES.has(p));
}
function emptyWeights() {
  return Object.fromEntries(LIVE_BRIDGES.map((b) => [b, 0]));
}
function springRestLength(w, l0 = 38, shrink = 0.18) {
  const clamped = Math.min(1, Math.max(0, w));
  return l0 * (1 - shrink * clamped);
}
function springStiffness(w, k0 = 0.01, kScale = 0.28) {
  const clamped = Math.min(1, Math.max(0, w));
  return k0 + kScale * clamped * clamped;
}
function cosineSimilarity(a, b) {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (const key of LIVE_BRIDGES) {
    const x = a[key];
    const y = b[key];
    dot += x * y;
    na += x * x;
    nb += y * y;
  }
  if (na === 0 || nb === 0) return 0;
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}
function dominantBridge(weights) {
  let best = null;
  let bestVal = 0;
  for (const key of LIVE_BRIDGES) {
    if (weights[key] > bestVal) {
      bestVal = weights[key];
      best = key;
    }
  }
  return bestVal > 0 ? best : null;
}

// ch05-field-spring-map/layout.ts
var BRIDGE_LAYOUT_SCALE = 1.5;
var PROJECT_ICON_SCALE = 0.7;
var bridgeLayout = null;
function bridgeCirclePosition(key, radius, cx = 0, cy = 0) {
  const idx = LIVE_BRIDGES.indexOf(key);
  const angle = idx / LIVE_BRIDGES.length * Math.PI * 2 - Math.PI / 2;
  return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
}
function setBridgeLayout(layout) {
  bridgeLayout = layout;
}
function bridgePinPosition(key, geometry, radius = 320) {
  if (geometry === "dependency") {
    const pos = bridgeLayout?.positions[key];
    if (pos) {
      return {
        x: pos.x * BRIDGE_LAYOUT_SCALE,
        y: pos.y * BRIDGE_LAYOUT_SCALE
      };
    }
  }
  return bridgeCirclePosition(key, radius * BRIDGE_LAYOUT_SCALE);
}
function bridgeDependencyEdges() {
  return bridgeLayout?.edges ?? [];
}
function graphDistance(a, b) {
  if (a === b) return 0;
  const edges = bridgeLayout?.edges ?? [];
  const adj = /* @__PURE__ */ new Map();
  for (const e of edges) {
    if (!adj.has(e.from)) adj.set(e.from, []);
    if (!adj.has(e.to)) adj.set(e.to, []);
    adj.get(e.from).push(e.to);
  }
  const queue = [{ node: a, dist: 0 }];
  const seen = /* @__PURE__ */ new Set([a]);
  while (queue.length) {
    const { node, dist } = queue.shift();
    if (node === b) return dist;
    for (const nxt of adj.get(node) ?? []) {
      if (seen.has(nxt)) continue;
      seen.add(nxt);
      queue.push({ node: nxt, dist: dist + 1 });
    }
  }
  return 4;
}

// ch05-field-spring-map/physics.ts
var DEFAULT_SIM_OPTIONS = {
  mode: "A",
  pinGeometry: "dependency",
  pinBridges: true,
  dominantOnly: false,
  weightThreshold: 0.05,
  useSquaredWeights: true
};
function effectiveWeight(raw, useSquared) {
  const w = Math.max(0, raw);
  return useSquared ? w * w : w;
}
function addBridgeDependencyEdges(edges, forSimulation) {
  for (const e of bridgeDependencyEdges()) {
    edges.push({
      source: `bridge:${e.from}`,
      target: `bridge:${e.to}`,
      weight: forSimulation ? 1 / (1 + graphDistance(e.from, e.to)) : 1,
      kind: forSimulation ? "bridge-dep" : "bridge-dep-static",
      color: e.color,
      assembly: e.assembly
    });
  }
}
function buildSimulation(projects, bridgeLabels, options) {
  const nodes = [];
  const edges = [];
  const showBridges = options.mode !== "C";
  const showBridgeDeps = options.pinGeometry === "dependency" || options.mode === "B";
  if (showBridges) {
    for (const key of LIVE_BRIDGES) {
      const pos = bridgePinPosition(key, options.pinGeometry);
      nodes.push({
        id: `bridge:${key}`,
        kind: "bridge",
        label: `${key} ${bridgeLabels[key] ?? key}`,
        bridgeKey: key,
        x: pos.x + (Math.random() - 0.5) * 8,
        y: pos.y + (Math.random() - 0.5) * 8,
        vx: 0,
        vy: 0,
        pinned: options.mode === "A" || options.pinBridges,
        radius: 22
      });
    }
    if (showBridgeDeps) {
      addBridgeDependencyEdges(edges, options.mode === "B" && !options.pinBridges);
    }
  }
  for (const p of projects) {
    const angle = Math.random() * Math.PI * 2;
    const r = BRIDGE_LAYOUT_SCALE * (70 + Math.random() * 110);
    const scaleRadius = (p.scale === "Large" ? 28 : p.scale === "Medium" ? 22 : p.scale === "Small" ? 16 : 20) * PROJECT_ICON_SCALE;
    nodes.push({
      id: `project:${p.id}`,
      kind: "project",
      label: p.title,
      projectId: p.id,
      logoLocal: p.logoLocal,
      x: Math.cos(angle) * r,
      y: Math.sin(angle) * r,
      vx: 0,
      vy: 0,
      pinned: false,
      radius: scaleRadius
    });
    if (showBridges) {
      const entries = LIVE_BRIDGES.map((key) => ({
        key,
        w: effectiveWeight(p.weights[key], options.useSquaredWeights)
      })).filter((e) => e.w > options.weightThreshold);
      const springs = options.dominantOnly && entries.length ? entries.sort((a, b) => b.w - a.w).slice(0, 1) : entries;
      for (const { key, w } of springs) {
        edges.push({
          source: `project:${p.id}`,
          target: `bridge:${key}`,
          weight: w,
          kind: "crux"
        });
      }
    }
  }
  if (options.mode === "C") {
    const projNodes = projects.map((p) => ({
      id: p.id,
      weights: p.weights
    }));
    for (let i = 0; i < projNodes.length; i++) {
      for (let j = i + 1; j < projNodes.length; j++) {
        const sim = cosineSimilarity(projNodes[i].weights, projNodes[j].weights);
        if (sim > options.weightThreshold) {
          edges.push({
            source: `project:${projNodes[i].id}`,
            target: `project:${projNodes[j].id}`,
            weight: sim,
            kind: "similarity"
          });
        }
      }
    }
  }
  return { nodes, edges };
}
function simulateStep(nodes, edges, options) {
  const damping = 0.92;
  const repulsion = 520;
  const centerPull = 5e-4;
  const maxSpeed = 7;
  const bridgeDepRest = 100 * BRIDGE_LAYOUT_SCALE;
  const bridgeDepK = 0.012;
  for (const n of nodes) {
    n.vx *= damping;
    n.vy *= damping;
  }
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i];
      const b = nodes[j];
      let dx = b.x - a.x;
      let dy = b.y - a.y;
      let distSq = dx * dx + dy * dy;
      if (distSq < 1) distSq = 1;
      const dist = Math.sqrt(distSq);
      const minDist = a.radius + b.radius + 10;
      const force = repulsion / distSq;
      dx /= dist;
      dy /= dist;
      if (dist < minDist) {
        const push = (minDist - dist) * 0.22;
        if (!a.pinned) {
          a.vx -= dx * push;
          a.vy -= dy * push;
        }
        if (!b.pinned) {
          b.vx += dx * push;
          b.vy += dy * push;
        }
      }
      if (a.kind === "project" && b.kind === "project" && options.mode !== "C") {
        if (!a.pinned) {
          a.vx -= dx * force;
          a.vy -= dy * force;
        }
        if (!b.pinned) {
          b.vx += dx * force;
          b.vy += dy * force;
        }
      }
    }
  }
  const nodeById = new Map(nodes.map((n) => [n.id, n]));
  for (const edge of edges) {
    if (edge.kind === "bridge-dep-static") continue;
    const a = nodeById.get(edge.source);
    const b = nodeById.get(edge.target);
    if (!a || !b) continue;
    let dx = b.x - a.x;
    let dy = b.y - a.y;
    let dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 1e-3) {
      dx = (Math.random() - 0.5) * 0.01;
      dy = (Math.random() - 0.5) * 0.01;
      dist = 0.01;
    }
    let rest;
    let k;
    if (edge.kind === "crux") {
      rest = springRestLength(edge.weight) + a.radius + b.radius;
      k = springStiffness(edge.weight);
    } else if (edge.kind === "bridge-dep") {
      rest = bridgeDepRest;
      k = bridgeDepK;
    } else {
      rest = 180 * (1 - edge.weight * 0.5);
      k = 8e-3 + edge.weight * 0.02;
    }
    const delta = dist - rest;
    const fx = k * delta * dx / dist;
    const fy = k * delta * dy / dist;
    if (!a.pinned) {
      a.vx += fx;
      a.vy += fy;
    }
    if (!b.pinned) {
      b.vx -= fx;
      b.vy -= fy;
    }
  }
  for (const n of nodes) {
    if (n.pinned) {
      if (n.kind === "bridge") {
        const key = n.bridgeKey;
        const pos = bridgePinPosition(key, options.pinGeometry);
        n.x = pos.x;
        n.y = pos.y;
      }
      n.vx = 0;
      n.vy = 0;
      continue;
    }
    n.vx -= n.x * centerPull;
    n.vy -= n.y * centerPull;
    const speed = Math.hypot(n.vx, n.vy);
    if (speed > maxSpeed) {
      const scale = maxSpeed / speed;
      n.vx *= scale;
      n.vy *= scale;
    }
    n.x += n.vx;
    n.y += n.vy;
  }
}
function reheat(nodes) {
  for (const n of nodes) {
    if (n.pinned) continue;
    n.vx += (Math.random() - 0.5) * 12;
    n.vy += (Math.random() - 0.5) * 12;
  }
}

// ch05-field-spring-map/app.ts
var DEFAULT_VIEW_SCALE = 0.85 / BRIDGE_LAYOUT_SCALE;
var BRIDGE_COLORS = {
  MB1: "#4a7c59",
  MB2: "#5b8a72",
  MB3: "#6b9888",
  MB4: "#c45c3e",
  MB4a: "#d47355",
  MB5: "#7b6b8a",
  MB6: "#b8860b",
  MB7: "#8b3a62",
  MB7d: "#9a5080",
  MB9: "#3d6b8a",
  MB10: "#a0522d",
  MB11: "#2f4f6f"
};
async function loadSnapshot() {
  const resp = await fetch("./data/snapshot.json");
  if (!resp.ok) throw new Error(`Failed to load snapshot: ${resp.status}`);
  return resp.json();
}
async function loadBridgeLayout() {
  const resp = await fetch("./data/bridge-layout.json");
  if (!resp.ok) throw new Error(`Failed to load bridge layout: ${resp.status}`);
  return resp.json();
}
function ensureLogoImages(listings, cache) {
  for (const listing of listings) {
    if (!listing.logoLocal || cache.has(listing.id)) continue;
    cache.set(listing.id, new Image());
    const img = cache.get(listing.id);
    img.onload = () => {
      if (img.naturalWidth > 0) cache.set(listing.id, img);
      else cache.delete(listing.id);
    };
    img.onerror = () => cache.delete(listing.id);
    img.src = `./data/${listing.logoLocal}`;
  }
}
function drawProjectNode(ctx, n, sel, logos) {
  const r = n.radius;
  const img = n.projectId ? logos.get(n.projectId) : void 0;
  ctx.beginPath();
  ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
  ctx.closePath();
  if (img && img.complete && img.naturalWidth > 0) {
    ctx.save();
    ctx.clip();
    ctx.drawImage(img, n.x - r, n.y - r, r * 2, r * 2);
    ctx.restore();
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.strokeStyle = sel ? "#16324f" : "#fff";
    ctx.lineWidth = sel ? 2.5 : 1.5;
    ctx.stroke();
  } else {
    ctx.fillStyle = sel ? "#16324f" : "#5a7896";
    ctx.fill();
  }
}
function listingWeights(listing) {
  const w = emptyWeights();
  for (const key of LIVE_BRIDGES) {
    w[key] = listing.weights[key] ?? 0;
  }
  return w;
}
function filterListings(listings, opts) {
  return listings.filter((l) => {
    if (!opts.showAll && !isResearchListing(l.category) && !PINNED_LISTING_IDS.has(l.id)) {
      return false;
    }
    if (opts.category !== "all" && !categoryParts(l.category).includes(opts.category)) return false;
    if (opts.status !== "all" && l.status !== opts.status) return false;
    if (opts.source !== "all" && l.source !== opts.source) return false;
    if (opts.search) {
      const q = opts.search.toLowerCase();
      if (!l.title.toLowerCase().includes(q) && !l.description.toLowerCase().includes(q)) {
        return false;
      }
    }
    const maxW = Math.max(...LIVE_BRIDGES.map((b) => l.weights[b] ?? 0));
    if (maxW < opts.minWeight) return false;
    return true;
  });
}
function renderWeightBars(listing, bridges) {
  const rows = LIVE_BRIDGES.map((key) => {
    const w = listing.weights[key] ?? 0;
    if (w <= 1e-3) return "";
    const pct = Math.round(w * 100);
    const label = bridges[key] ?? key;
    return `<div class="weight-row"><span class="weight-label">${key} ${label}</span><div class="weight-bar"><div class="weight-fill" style="width:${pct}%;background:${BRIDGE_COLORS[key]}"></div></div><span class="weight-val">${w.toFixed(2)}</span></div>`;
  }).filter(Boolean);
  return rows.length ? rows.join("") : '<p class="muted">No crux weights above zero.</p>';
}
function renderProvenance(listing) {
  const p = listing.provenance;
  if (listing.source === "inherited" && p.agendaSlug) {
    const be = p.bridgeEvidence ?? {};
    const lines = [];
    for (const key of LIVE_BRIDGES) {
      if ((listing.weights[key] ?? 0) <= 1e-3) continue;
      const evs = be[key] ?? [];
      if (!evs.length) continue;
      const bits = evs.map((e) => {
        const flag = e.tagMismatch ? " \xB7 matrix-only" : "";
        return `#${e.evidenceId}${flag}: ${e.summary}`;
      });
      lines.push(`<li><strong>${key}:</strong> ${bits.join("; ")}</li>`);
    }
    const evHtml = lines.length ? `<ul class="ev-list">${lines.join("")}</ul>` : "";
    return `<p><strong>Source:</strong> inherited from agenda <code>${p.agendaSlug}</code> (${p.matchKind})</p>${evHtml}`;
  }
  if (p.rationale) {
    return `<p><strong>Source:</strong> ${listing.source}<br/>${p.rationale}</p>`;
  }
  return `<p><strong>Source:</strong> ${listing.source}</p>`;
}
async function initDemo(root) {
  const [snapshot, bridgeLayout2] = await Promise.all([loadSnapshot(), loadBridgeLayout()]);
  setBridgeLayout(bridgeLayout2);
  const logos = /* @__PURE__ */ new Map();
  let nodes = [];
  let edges = [];
  let simOptions = { ...DEFAULT_SIM_OPTIONS };
  let paused = false;
  let selectedId = null;
  let hoveredId = null;
  let transform = { x: 0, y: 0, scale: DEFAULT_VIEW_SCALE };
  const ui = document.createElement("div");
  ui.className = "fsm-root";
  ui.innerHTML = `
    <header class="fsm-header">
      <h1>Field crux spring map</h1>
      <p class="fsm-caption">AISafety.com listings placed by bridge-crux affinity. Scores reflect field evidence or heuristics \u2014 not discharge to Safe.</p>
    </header>
    <div class="fsm-controls">
      <label>Mode <select data-mode><option value="A">A \u2014 fixed bridges</option><option value="B">B \u2014 movable bridges</option><option value="C">C \u2014 similarity</option></select></label>
      <label>Geometry <select data-geometry><option value="circle">Circle</option><option value="dependency" selected>Dependency</option></select></label>
      <label><input type="checkbox" data-pin-bridges checked /> Pin bridges</label>
      <label><input type="checkbox" data-dominant /> Dominant only</label>
      <label><input type="checkbox" data-show-all /> All categories</label>
      <label>Category <select data-category><option value="all">All</option></select></label>
      <label>Status <select data-status><option value="all">All</option><option value="Active">Active</option><option value="Inactive">Inactive</option></select></label>
      <label>Source <select data-source><option value="all">All</option><option value="inherited">Inherited</option><option value="heuristic">Heuristic</option><option value="unmatched">Unmatched</option></select></label>
      <label>Min w <input type="range" data-min-weight min="0" max="0.5" step="0.05" value="0" /><span data-min-label>0</span></label>
      <input type="search" data-search placeholder="Search\u2026" />
      <button type="button" data-pause>Pause</button>
      <button type="button" data-reheat>Reheat</button>
      <button type="button" data-reset-view>Reset view</button>
    </div>
    <div class="fsm-main">
      <div class="fsm-canvas-wrap"><canvas data-canvas></canvas></div>
      <aside class="fsm-panel" data-panel><p class="muted">Click a node.</p></aside>
    </div>
    <footer class="fsm-footer">Data: <a href="https://aisafety.com/map" target="_blank" rel="noopener">AISafety.com</a> (CC-BY-4.0)</footer>
  `;
  root.appendChild(ui);
  const style = document.createElement("style");
  style.textContent = `
    .fsm-root { font-family: system-ui,sans-serif; color:#1a2433; max-width:1200px; margin:0 auto; padding:16px; }
    .fsm-header h1 { margin:0 0 6px; font-size:1.35rem; }
    .fsm-caption { margin:0 0 12px; color:#555; max-width:70ch; font-size:0.92rem; }
    .fsm-controls { display:flex; flex-wrap:wrap; gap:10px 14px; align-items:center; margin-bottom:12px; font-size:0.85rem; }
    .fsm-controls label { display:flex; align-items:center; gap:4px; }
    .fsm-controls select, .fsm-controls input[type=search] { font:inherit; }
    .fsm-main { display:grid; grid-template-columns:1fr 280px; gap:12px; min-height:520px; }
    @media (max-width:900px) { .fsm-main { grid-template-columns:1fr; } }
    .fsm-canvas-wrap { position:relative; border:1px solid #c8d4e0; border-radius:8px; background:#fff; height:480px; min-height:480px; overflow:hidden; }
    canvas { display:block; width:100%; cursor:grab; }
    canvas:active { cursor:grabbing; }
    .fsm-tooltip { position:fixed; pointer-events:none; z-index:20; background:rgba(26,36,51,0.92); color:#fff; padding:5px 9px; border-radius:4px; font-size:0.78rem; max-width:320px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; box-shadow:0 2px 8px rgba(0,0,0,0.18); transform:translate(10px,10px); }
    .fsm-tooltip.fsm-tooltip-bridge { white-space:normal; max-width:260px; line-height:1.35; }
    .fsm-panel { border:1px solid #c8d4e0; border-radius:8px; padding:12px; background:#fff; overflow-y:auto; max-height:520px; font-size:0.88rem; }
    .fsm-panel h2 { margin:0 0 6px; font-size:1rem; }
    .fsm-panel .panel-logo { width:48px; height:48px; border-radius:50%; object-fit:cover; margin-bottom:8px; border:1px solid #c8d4e0; }
    .fsm-panel .meta { color:#666; margin:0 0 8px; }
    .fsm-panel .muted { color:#777; }
    .weight-row { display:grid; grid-template-columns:1fr 1fr auto; gap:6px; align-items:center; margin:4px 0; font-size:0.78rem; }
    .weight-bar { height:8px; background:#e8edf2; border-radius:4px; overflow:hidden; }
    .weight-fill { height:100%; border-radius:4px; }
    .fsm-panel .ev-list { margin:8px 0 0; padding-left:18px; font-size:0.78rem; color:#444; }
    .fsm-footer { margin-top:10px; font-size:0.8rem; color:#666; }
  `;
  document.head.appendChild(style);
  const catSelect = ui.querySelector("[data-category]");
  const catNames = /* @__PURE__ */ new Set();
  for (const l of snapshot.listings) {
    for (const part of categoryParts(l.category)) catNames.add(part);
  }
  for (const c of [...catNames].sort()) {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    catSelect.appendChild(opt);
  }
  const canvas = ui.querySelector("[data-canvas]");
  const panel = ui.querySelector("[data-panel]");
  const ctx = canvas.getContext("2d");
  const tooltip = document.createElement("div");
  tooltip.className = "fsm-tooltip";
  tooltip.hidden = true;
  canvas.parentElement.appendChild(tooltip);
  let dragging = null;
  const getFilters = () => ({
    showAll: ui.querySelector("[data-show-all]").checked,
    category: ui.querySelector("[data-category]").value,
    status: ui.querySelector("[data-status]").value,
    source: ui.querySelector("[data-source]").value,
    search: ui.querySelector("[data-search]").value.trim(),
    minWeight: Number(ui.querySelector("[data-min-weight]").value)
  });
  function rebuild() {
    const filtered = filterListings(snapshot.listings, getFilters());
    const projects = filtered.map((l) => ({
      id: l.id,
      title: l.title,
      weights: listingWeights(l),
      logoLocal: l.logoLocal,
      scale: l.scale
    }));
    const sim = buildSimulation(projects, snapshot.bridges, simOptions);
    nodes = sim.nodes;
    edges = sim.edges;
    ensureLogoImages(filtered, logos);
    panel.innerHTML = `<p class="muted">${filtered.length} listings \xB7 click a node</p>`;
    selectedId = null;
    hoveredId = null;
  }
  function strokeEdge(e, a, b, nodeById, highlight) {
    if (e.kind === "bridge-dep" || e.kind === "bridge-dep-static") {
      if (highlight === "bright") {
        ctx.strokeStyle = e.assembly ? "rgba(51,51,51,0.95)" : "rgba(204,51,51,0.95)";
        ctx.lineWidth = e.assembly ? 2.8 : 2.2;
      } else if (highlight === "dim") {
        ctx.strokeStyle = "rgba(204,51,51,0.08)";
        ctx.lineWidth = 0.75;
      } else if (e.kind === "bridge-dep-static") {
        ctx.strokeStyle = e.assembly ? "rgba(51,51,51,0.55)" : "rgba(204,51,51,0.6)";
        ctx.lineWidth = e.assembly ? 2 : 1.5;
      } else {
        ctx.strokeStyle = "rgba(204,51,51,0.35)";
        ctx.lineWidth = 1.2;
      }
    } else if (e.kind === "crux") {
      if (highlight === "bright") {
        const bridge = nodeById.get(e.target);
        const col = bridge?.bridgeKey ? BRIDGE_COLORS[bridge.bridgeKey] : "#2f4f6f";
        ctx.strokeStyle = col;
        ctx.lineWidth = 2.5 + Math.min(e.weight, 1) * 2.5;
      } else if (highlight === "dim") {
        ctx.strokeStyle = "rgba(100,120,140,0.05)";
        ctx.lineWidth = 0.75;
      } else {
        ctx.strokeStyle = "rgba(100,120,140,0.14)";
        ctx.lineWidth = 1;
      }
    } else {
      ctx.strokeStyle = "rgba(100,120,140,0.14)";
      ctx.lineWidth = 1;
    }
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }
  function resize() {
    const wrap = canvas.parentElement;
    const dpr = window.devicePixelRatio || 1;
    const cw = wrap.clientWidth;
    const ch = Math.max(480, wrap.clientHeight || 480);
    canvas.width = cw * dpr;
    canvas.height = ch * dpr;
    canvas.style.width = `${cw}px`;
    canvas.style.height = `${ch}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function screenToWorld(sx, sy) {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    return [(sx - w / 2) / transform.scale - transform.x, (sy - h / 2) / transform.scale - transform.y];
  }
  function pick(sx, sy) {
    const [wx, wy] = screenToWorld(sx, sy);
    let best = null;
    let bestD = Infinity;
    for (const n of nodes) {
      const d = Math.hypot(n.x - wx, n.y - wy);
      if (d < n.radius + 6 && d < bestD) {
        bestD = d;
        best = n;
      }
    }
    return best;
  }
  function renderPanel(node) {
    if (node.kind === "bridge" && node.bridgeKey) {
      panel.innerHTML = `<h2>${node.bridgeKey}</h2><p>${snapshot.bridges[node.bridgeKey]}</p><p class="muted">Bridge anchor node.</p>`;
      return;
    }
    const listing = snapshot.listings.find((l) => l.id === node.projectId);
    if (!listing) return;
    const dom = dominantBridge(listingWeights(listing));
    const logoHtml = listing.logoLocal ? `<img class="panel-logo" src="./data/${listing.logoLocal}" alt="" />` : "";
    panel.innerHTML = `
      ${logoHtml}
      <h2>${listing.title}</h2>
      <p class="meta">${listing.category} \xB7 ${listing.status}</p>
      <p>${listing.description}</p>
      ${listing.link ? `<p><a href="${listing.link}" target="_blank" rel="noopener">Website</a></p>` : ""}
      ${renderProvenance(listing)}
      ${dom ? `<p><strong>Dominant:</strong> ${dom}</p>` : ""}
      <div>${renderWeightBars(listing, snapshot.bridges)}</div>`;
  }
  function drawFrame() {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "#f7f9fb";
    ctx.fillRect(0, 0, w, h);
    ctx.save();
    ctx.translate(w / 2 + transform.x * transform.scale, h / 2 + transform.y * transform.scale);
    ctx.scale(transform.scale, transform.scale);
    const nodeById = new Map(nodes.map((n) => [n.id, n]));
    const hoveredNode = hoveredId ? nodeById.get(hoveredId) : void 0;
    const edgeHighlight = (e) => {
      if (!hoveredNode) return "normal";
      if (hoveredNode.kind === "project") {
        if (e.kind !== "crux") return "normal";
        return e.source === hoveredId ? "bright" : "dim";
      }
      if (hoveredNode.kind === "bridge") {
        if (e.kind === "crux") {
          return e.target === hoveredId ? "bright" : "dim";
        }
        if (e.kind === "bridge-dep" || e.kind === "bridge-dep-static") {
          return e.source === hoveredId || e.target === hoveredId ? "bright" : "dim";
        }
      }
      return "normal";
    };
    for (const e of edges) {
      const hl = edgeHighlight(e);
      if (hl === "bright") continue;
      const a = nodeById.get(e.source);
      const b = nodeById.get(e.target);
      if (!a || !b) continue;
      strokeEdge(e, a, b, nodeById, hl);
    }
    for (const e of edges) {
      if (edgeHighlight(e) !== "bright") continue;
      const a = nodeById.get(e.source);
      const b = nodeById.get(e.target);
      if (!a || !b) continue;
      strokeEdge(e, a, b, nodeById, "bright");
    }
    for (const n of nodes) {
      const sel = selectedId === n.id;
      if (n.kind === "bridge") {
        const col = n.bridgeKey ? BRIDGE_COLORS[n.bridgeKey] : "#888";
        ctx.fillStyle = col;
        ctx.strokeStyle = sel ? "#111" : "#fff";
        ctx.lineWidth = sel ? 2.5 : 1.5;
        const r = n.radius;
        ctx.beginPath();
        ctx.moveTo(n.x, n.y - r);
        ctx.lineTo(n.x + r, n.y);
        ctx.lineTo(n.x, n.y + r);
        ctx.lineTo(n.x - r, n.y);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "#fff";
        ctx.font = "bold 9px system-ui";
        ctx.textAlign = "center";
        ctx.fillText(n.bridgeKey ?? "", n.x, n.y + 3);
      } else {
        drawProjectNode(ctx, n, sel, logos);
      }
    }
    ctx.restore();
  }
  let raf = 0;
  function loop() {
    if (!paused) {
      for (let i = 0; i < 2; i++) simulateStep(nodes, edges, simOptions);
    }
    drawFrame();
    raf = requestAnimationFrame(loop);
  }
  const bind = (sel, fn) => ui.querySelector(sel)?.addEventListener("change", fn);
  const bindClick = (sel, fn) => ui.querySelector(sel)?.addEventListener("click", fn);
  bind("[data-mode]", () => {
    simOptions.mode = ui.querySelector("[data-mode]").value;
    simOptions.pinBridges = simOptions.mode === "A" || ui.querySelector("[data-pin-bridges]").checked;
    rebuild();
  });
  bind("[data-geometry]", () => {
    simOptions.pinGeometry = ui.querySelector("[data-geometry]").value;
    rebuild();
  });
  ui.querySelector("[data-pin-bridges]")?.addEventListener("change", (e) => {
    simOptions.pinBridges = e.target.checked || simOptions.mode === "A";
    rebuild();
  });
  ui.querySelector("[data-dominant]")?.addEventListener("change", (e) => {
    simOptions.dominantOnly = e.target.checked;
    rebuild();
  });
  ui.querySelector("[data-show-all]")?.addEventListener("change", rebuild);
  bind("[data-category]", rebuild);
  bind("[data-status]", rebuild);
  bind("[data-source]", rebuild);
  ui.querySelector("[data-min-weight]")?.addEventListener("input", (e) => {
    ui.querySelector("[data-min-label]").textContent = e.target.value;
    rebuild();
  });
  ui.querySelector("[data-search]")?.addEventListener("input", rebuild);
  bindClick("[data-pause]", () => {
    paused = !paused;
    ui.querySelector("[data-pause]").textContent = paused ? "Resume" : "Pause";
  });
  bindClick("[data-reheat]", () => reheat(nodes));
  bindClick("[data-reset-view]", () => {
    transform = { x: 0, y: 0, scale: DEFAULT_VIEW_SCALE };
  });
  canvas.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      const factor = e.deltaY > 0 ? 0.92 : 1.08;
      transform.scale = Math.min(2.5, Math.max(0.2, transform.scale * factor));
    },
    { passive: false }
  );
  function hideTooltip() {
    tooltip.hidden = true;
    tooltip.classList.remove("fsm-tooltip-bridge");
    hoveredId = null;
  }
  function updateTooltip(clientX, clientY, offsetX, offsetY) {
    if (dragging) {
      hideTooltip();
      return;
    }
    const node = pick(offsetX, offsetY);
    if (node?.kind === "project" || node?.kind === "bridge") {
      hoveredId = node.id;
      if (node.kind === "bridge" && node.bridgeKey) {
        tooltip.textContent = snapshot.bridges[node.bridgeKey] ?? node.label;
        tooltip.classList.add("fsm-tooltip-bridge");
      } else {
        tooltip.textContent = node.label;
        tooltip.classList.remove("fsm-tooltip-bridge");
      }
      tooltip.style.left = `${clientX}px`;
      tooltip.style.top = `${clientY}px`;
      tooltip.hidden = false;
      canvas.style.cursor = "pointer";
      return;
    }
    hideTooltip();
    canvas.style.cursor = "grab";
  }
  canvas.addEventListener("mousemove", (e) => {
    updateTooltip(e.clientX, e.clientY, e.offsetX, e.offsetY);
  });
  canvas.addEventListener("mouseleave", () => {
    hideTooltip();
    canvas.style.cursor = "grab";
  });
  canvas.addEventListener("mousedown", (e) => {
    dragging = { lastX: e.clientX, lastY: e.clientY };
    hideTooltip();
    const node = pick(e.offsetX, e.offsetY);
    if (node) {
      selectedId = node.id;
      renderPanel(node);
    }
  });
  window.addEventListener("mousemove", (e) => {
    if (!dragging) return;
    transform.x += (e.clientX - dragging.lastX) / transform.scale;
    transform.y += (e.clientY - dragging.lastY) / transform.scale;
    dragging.lastX = e.clientX;
    dragging.lastY = e.clientY;
  });
  window.addEventListener("mouseup", () => {
    dragging = null;
  });
  resize();
  rebuild();
  window.addEventListener("resize", resize);
  loop();
  return () => {
    cancelAnimationFrame(raf);
    window.removeEventListener("resize", resize);
    root.innerHTML = "";
    style.remove();
  };
}
var mount = document.getElementById("field-spring-map-demo");
if (mount) {
  initDemo(mount).catch((err) => {
    mount.innerHTML = `<p style="color:#a00">Failed to load demo: ${err}</p>`;
  });
}
export {
  initDemo,
  loadBridgeLayout,
  loadSnapshot
};
