// appB-field-spring-map/weights.ts
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
var BRIDGE_SHORT_LABELS = {
  MB1: "Boundary",
  MB2: "Value",
  MB3: "Ref.",
  MB4: "Corrig.",
  MB4a: "Indep.",
  MB5: "Tiling",
  MB6: "Goodhard",
  MB7: "Inner",
  MB7d: "Acausal",
  MB9: "Ground.",
  MB10: "Gaming",
  MB11: "Safety"
};
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
var WEIGHT_JITTER_AMPLITUDE = 0.05;
function hashString(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}
function mulberry32(seed) {
  let state = seed;
  return () => {
    state = state + 1831565813 >>> 0;
    let t = state;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function jitterWeight(raw, projectId, bridge, amplitude = WEIGHT_JITTER_AMPLITUDE) {
  if (raw <= 0) return 0;
  const rand = mulberry32(hashString(`${projectId}\0${bridge}`))();
  return Math.min(1, raw * (1 + amplitude * (2 * rand - 1)));
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
function projectBridgeKeys(weights, opts) {
  const entries = LIVE_BRIDGES.map((key) => ({
    key,
    w: opts.useSquaredWeights ? weights[key] * weights[key] : weights[key]
  })).filter((e) => e.w > opts.weightThreshold);
  const springs = opts.dominantOnly && entries.length ? entries.sort((a, b) => b.w - a.w).slice(0, 1) : entries;
  return springs.map((e) => e.key);
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

// appB-field-spring-map/layout.ts
var DEPENDENCY_ANCHOR_SCALE = 2.3;
var CIRCLE_ANCHOR_SCALE = 1;
function bridgeAnchorScale(geometry) {
  return geometry === "dependency" ? DEPENDENCY_ANCHOR_SCALE : CIRCLE_ANCHOR_SCALE;
}
var PROJECT_ICON_SCALE = 0.7;
var bridgeLayout = null;
var circleBridgeOrder = null;
function pairKey(a, b) {
  return a < b ? `${a}|${b}` : `${b}|${a}`;
}
function pairAffinity(map, a, b) {
  if (a === b) return 0;
  return map.get(pairKey(a, b)) ?? 0;
}
function ringCooccurrenceScore(order, map) {
  let score = 0;
  for (let i = 0; i < order.length; i++) {
    const j = (i + 1) % order.length;
    score += pairAffinity(map, order[i], order[j]);
  }
  return score;
}
function computeCircleBridgeOrder(projects, opts) {
  const cooccurrence = /* @__PURE__ */ new Map();
  for (const project of projects) {
    const bridges = projectBridgeKeys(project.weights, opts);
    for (let i = 0; i < bridges.length; i++) {
      for (let j = i + 1; j < bridges.length; j++) {
        const pk = pairKey(bridges[i], bridges[j]);
        cooccurrence.set(pk, (cooccurrence.get(pk) ?? 0) + 1);
      }
    }
  }
  const n = LIVE_BRIDGES.length;
  const affinity = (i, j) => pairAffinity(cooccurrence, LIVE_BRIDGES[i], LIVE_BRIDGES[j]);
  let hasCooccurrence = false;
  for (const v of cooccurrence.values()) {
    if (v > 0) {
      hasCooccurrence = true;
      break;
    }
  }
  if (!hasCooccurrence) return [...LIVE_BRIDGES];
  const full = (1 << n) - 1;
  const negInf = -1e9;
  const dp = Array.from({ length: 1 << n }, () => Array(n).fill(negInf));
  const parent = Array.from({ length: 1 << n }, () => new Int16Array(n).fill(-1));
  dp[1][0] = 0;
  for (let mask2 = 1; mask2 <= full; mask2++) {
    if (!(mask2 & 1)) continue;
    for (let j = 0; j < n; j++) {
      if (!(mask2 & 1 << j)) continue;
      const base = dp[mask2][j];
      if (base <= negInf / 2) continue;
      for (let k = 0; k < n; k++) {
        if (mask2 & 1 << k) continue;
        const nextMask = mask2 | 1 << k;
        const next = base + affinity(j, k);
        if (next > dp[nextMask][k]) {
          dp[nextMask][k] = next;
          parent[nextMask][k] = j;
        }
      }
    }
  }
  let bestScore = negInf;
  let bestEnd = 0;
  for (let j = 1; j < n; j++) {
    const score = dp[full][j] + affinity(j, 0);
    if (score > bestScore) {
      bestScore = score;
      bestEnd = j;
    }
  }
  const idxPath = [];
  let mask = full;
  let cur = bestEnd;
  while (cur >= 0) {
    idxPath.push(cur);
    const prev = parent[mask][cur];
    mask ^= 1 << cur;
    cur = prev;
  }
  idxPath.reverse();
  let bestOrder = idxPath.map((i) => LIVE_BRIDGES[i]);
  bestScore = ringCooccurrenceScore(bestOrder, cooccurrence);
  for (let rot = 0; rot < bestOrder.length; rot++) {
    for (const candidate of [
      [...bestOrder.slice(rot), ...bestOrder.slice(0, rot)],
      [...bestOrder.slice(rot), ...bestOrder.slice(0, rot)].reverse()
    ]) {
      const score = ringCooccurrenceScore(candidate, cooccurrence);
      if (score > bestScore) {
        bestScore = score;
        bestOrder = candidate;
      }
    }
  }
  return bestOrder;
}
function setCircleBridgeOrder(order) {
  circleBridgeOrder = order;
}
function bridgeCirclePosition(key, radius, cx = 0, cy = 0) {
  const order = circleBridgeOrder ?? LIVE_BRIDGES;
  const idx = order.indexOf(key);
  const slot = idx >= 0 ? idx : LIVE_BRIDGES.indexOf(key);
  const angle = slot / order.length * Math.PI * 2 - Math.PI / 2;
  return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
}
function setBridgeLayout(layout) {
  bridgeLayout = layout;
}
function bridgePinPosition(key, geometry, radius = 320) {
  const scale = bridgeAnchorScale(geometry);
  if (geometry === "dependency") {
    const pos = bridgeLayout?.positions[key];
    if (pos) {
      return {
        x: pos.x * scale,
        y: pos.y * scale
      };
    }
  }
  return bridgeCirclePosition(key, radius * scale);
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

// appB-field-spring-map/physics.ts
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
  const layoutScale = bridgeAnchorScale(options.pinGeometry);
  const projectSpawnScale = options.mode === "A" ? layoutScale : 1;
  if (showBridges && options.pinGeometry === "circle") {
    setCircleBridgeOrder(computeCircleBridgeOrder(projects, options));
  } else {
    setCircleBridgeOrder(null);
  }
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
        radius: 34
      });
    }
    if (showBridgeDeps) {
      addBridgeDependencyEdges(edges, options.mode === "B" && !options.pinBridges);
    }
  }
  for (const p of projects) {
    const angle = Math.random() * Math.PI * 2;
    const r = projectSpawnScale * (70 + Math.random() * 110);
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
      const keys = projectBridgeKeys(p.weights, options);
      for (const key of keys) {
        const raw = jitterWeight(p.weights[key], p.id, key);
        edges.push({
          source: `project:${p.id}`,
          target: `bridge:${key}`,
          weight: effectiveWeight(raw, options.useSquaredWeights),
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
  const bridgeDepRest = 100 * bridgeAnchorScale(options.pinGeometry);
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

// appB-field-spring-map/app.ts
var DEFAULT_VIEW_SCALE = 1 / DEPENDENCY_ANCHOR_SCALE;
var COMPACT_LAYOUT_MQ = "(max-width: 900px)";
var MOUSE_POINTER_MQ = "(hover: hover) and (pointer: fine)";
var BRIDGE_POP_SCALE = 2;
var SIM_OPTIONS = {
  mode: "A",
  pinGeometry: "dependency",
  pinBridges: true,
  dominantOnly: false,
  weightThreshold: 0.05,
  useSquaredWeights: true
};
function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function companionHref(snapshot, sitePath) {
  if (!sitePath) return "";
  const path = window.location.pathname;
  const embedded = path.match(/^(.*)\/chapter-demos\//);
  if (embedded) return `${embedded[1]}${sitePath}`;
  const base = String(snapshot.meta.companionSite ?? "https://towards-alignment.com");
  return `${base.replace(/\/$/, "")}${sitePath}`;
}
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
function filterListings(listings, category) {
  return listings.filter((l) => {
    if (l.status !== "Active") return false;
    if (!isResearchListing(l.category) && !PINNED_LISTING_IDS.has(l.id)) return false;
    if (category !== "all" && !categoryParts(l.category).includes(category)) return false;
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
  let pinGeometry = SIM_OPTIONS.pinGeometry;
  let selectedId = null;
  let hoveredId = null;
  let transform = { x: 0, y: 0, scale: DEFAULT_VIEW_SCALE };
  const ui = document.createElement("div");
  ui.className = "fsm-root";
  const evidenceCatalogHref = companionHref(
    snapshot,
    "/field/coverage/#coverage-evidence-catalog"
  );
  ui.innerHTML = `
    <header class="fsm-header">
      <h1>Interactive Field Crux Map</h1>
      <p class="fsm-caption"><a href="https://aisafety.com/map" target="_blank" rel="noopener">AISafety.com</a> listings placed by bridge-crux affinity. Weights reflect field <a href="${escapeHtml(evidenceCatalogHref)}">listed evidence</a> or heuristics.</p>
    </header>
    <div class="fsm-controls">
      <label>Category <select data-category><option value="all">All research</option></select></label>
      <button type="button" data-toggle-geometry>Layout: dependency</button>
    </div>
    <div class="fsm-main">
      <div class="fsm-canvas-wrap"><canvas data-canvas></canvas></div>
      <aside class="fsm-panel" data-panel><p class="muted">Hover a node.</p></aside>
    </div>
    <div class="fsm-overlay" data-overlay hidden>
      <div class="fsm-overlay-backdrop" data-overlay-close></div>
      <div class="fsm-overlay-pane">
        <button type="button" class="fsm-overlay-close" data-overlay-close aria-label="Close">\xD7</button>
        <div data-overlay-content></div>
      </div>
    </div>
    <footer class="fsm-footer">Data: <a href="https://aisafety.com/map" target="_blank" rel="noopener">AISafety.com</a> (CC-BY-4.0)</footer>
  `;
  root.appendChild(ui);
  const style = document.createElement("style");
  style.textContent = `
    .fsm-root { font-family: system-ui,sans-serif; color:#1a2433; max-width:1200px; margin:0 auto; padding:16px; }
    .fsm-header h1 { margin:0 0 6px; font-size:1.35rem; }
    .fsm-caption { margin:0 0 12px; color:#555; font-size:0.92rem; line-height:1.45; }
    .fsm-caption a { color:#2f4f6f; }
    .fsm-controls { display:flex; flex-wrap:wrap; gap:10px 14px; align-items:center; margin-bottom:12px; font-size:0.85rem; }
    .fsm-controls label { display:flex; align-items:center; gap:4px; }
    .fsm-controls select, .fsm-controls button { font:inherit; }
    .fsm-controls button { padding:4px 10px; border:1px solid #c8d4e0; border-radius:4px; background:#fff; cursor:pointer; }
    .fsm-controls button:hover { background:#f0f4f8; }
    .fsm-main { display:grid; grid-template-columns:1fr 280px; gap:12px; min-height:520px; }
    @media (max-width:900px) { .fsm-main { grid-template-columns:1fr; } .fsm-panel { display:none; } }
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
    .fsm-panel .bridge-summary { margin:0 0 10px; line-height:1.45; color:#333; }
    .weight-row { display:grid; grid-template-columns:1fr 1fr auto; gap:6px; align-items:center; margin:4px 0; font-size:0.78rem; }
    .weight-bar { height:8px; background:#e8edf2; border-radius:4px; overflow:hidden; }
    .weight-fill { height:100%; border-radius:4px; }
    .fsm-panel .ev-list { margin:8px 0 0; padding-left:18px; font-size:0.78rem; color:#444; }
    .fsm-footer { margin-top:10px; font-size:0.8rem; color:#666; }
    .fsm-overlay { position:fixed; inset:0; z-index:100; display:flex; align-items:flex-end; justify-content:center; }
    .fsm-overlay[hidden] { display:none; }
    .fsm-overlay-backdrop { position:absolute; inset:0; background:rgba(0,0,0,0.45); }
    .fsm-overlay-pane { position:relative; background:#fff; border-radius:12px 12px 0 0; max-height:75vh; overflow-y:auto; padding:16px 16px 24px; width:100%; max-width:640px; font-size:0.88rem; box-shadow:0 -4px 24px rgba(0,0,0,0.15); }
    .fsm-overlay-close { position:absolute; top:8px; right:10px; border:none; background:transparent; font-size:1.5rem; line-height:1; cursor:pointer; color:#555; padding:4px 8px; z-index:1; }
    .fsm-overlay-pane h2 { margin:0 0 6px; font-size:1rem; padding-right:28px; }
  `;
  document.head.appendChild(style);
  const catSelect = ui.querySelector("[data-category]");
  const catNames = /* @__PURE__ */ new Set();
  for (const l of snapshot.listings) {
    for (const part of categoryParts(l.category)) {
      if (RESEARCH_CATEGORIES.has(part)) catNames.add(part);
    }
  }
  for (const c of [...catNames].sort()) {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    catSelect.appendChild(opt);
  }
  const canvas = ui.querySelector("[data-canvas]");
  const panel = ui.querySelector("[data-panel]");
  const overlay = ui.querySelector("[data-overlay]");
  const overlayContent = ui.querySelector("[data-overlay-content]");
  const ctx = canvas.getContext("2d");
  const tooltip = document.createElement("div");
  tooltip.className = "fsm-tooltip";
  tooltip.hidden = true;
  canvas.parentElement.appendChild(tooltip);
  let dragging = null;
  let pointerDown = null;
  let listingCount = 0;
  let suppressMouseUntil = 0;
  const geometryBtn = ui.querySelector("[data-toggle-geometry]");
  function compactLayout() {
    return window.matchMedia(COMPACT_LAYOUT_MQ).matches;
  }
  function touchInteraction() {
    return compactLayout() && !window.matchMedia(MOUSE_POINTER_MQ).matches;
  }
  function sidePanelVisible() {
    return !compactLayout();
  }
  function focusNodeId() {
    return touchInteraction() ? selectedId : hoveredId;
  }
  function simOptions() {
    return { ...SIM_OPTIONS, pinGeometry };
  }
  function updateGeometryLabel() {
    geometryBtn.textContent = pinGeometry === "dependency" ? "Layout: dependency" : "Layout: circle";
  }
  function rebuild() {
    const category = ui.querySelector("[data-category]").value;
    const filtered = filterListings(snapshot.listings, category);
    const projects = filtered.map((l) => ({
      id: l.id,
      title: l.title,
      weights: listingWeights(l),
      logoLocal: l.logoLocal,
      scale: l.scale
    }));
    const sim = buildSimulation(projects, snapshot.bridges, simOptions());
    nodes = sim.nodes;
    edges = sim.edges;
    ensureLogoImages(filtered, logos);
    listingCount = filtered.length;
    resetPanel();
    selectedId = null;
    hoveredId = null;
    closeOverlay();
  }
  function resetPanel() {
    const hint = touchInteraction() ? "Tap a node" : "Hover a node";
    panel.innerHTML = `<p class="muted">${listingCount} listings \xB7 ${hint}</p>`;
  }
  function closeOverlay() {
    overlay.hidden = true;
    overlayContent.innerHTML = "";
  }
  function openOverlay(node) {
    overlayContent.innerHTML = panelHtml(node);
    overlay.hidden = false;
  }
  function nodeUrl(node) {
    if (node.kind === "bridge" && node.bridgeKey) {
      const card = snapshot.bridgeCards?.[node.bridgeKey];
      return card?.cardPath ? companionHref(snapshot, card.cardPath) : null;
    }
    const listing = snapshot.listings.find((l) => l.id === node.projectId);
    return listing?.link ?? null;
  }
  function navigateToNode(node) {
    const href = nodeUrl(node);
    if (href) window.open(href, "_blank", "noopener");
  }
  function strokeEdge(e, a, b, nodeById, highlight) {
    if (e.kind === "bridge-dep" || e.kind === "bridge-dep-static") {
      if (highlight === "bright") {
        ctx.strokeStyle = e.assembly ? "rgba(51,51,51,0.95)" : "rgba(204,51,51,0.95)";
        ctx.lineWidth = e.assembly ? 5.6 : 4.4;
      } else if (highlight === "dim") {
        ctx.strokeStyle = "rgba(204,51,51,0.08)";
        ctx.lineWidth = 1.5;
      } else if (e.kind === "bridge-dep-static") {
        ctx.strokeStyle = e.assembly ? "rgba(51,51,51,0.55)" : "rgba(204,51,51,0.6)";
        ctx.lineWidth = e.assembly ? 4 : 3;
      } else {
        ctx.strokeStyle = "rgba(204,51,51,0.35)";
        ctx.lineWidth = 2.4;
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
  function nodeHitRadius(n) {
    const focus = focusNodeId();
    const pop = n.kind === "bridge" && focus === n.id ? BRIDGE_POP_SCALE : 1;
    return n.radius * pop + 6;
  }
  function pick(sx, sy) {
    const [wx, wy] = screenToWorld(sx, sy);
    let best = null;
    let bestD = Infinity;
    for (const n of nodes) {
      const d = Math.hypot(n.x - wx, n.y - wy);
      if (d < nodeHitRadius(n) && d < bestD) {
        bestD = d;
        best = n;
      }
    }
    return best;
  }
  function panelHtml(node) {
    if (node.kind === "bridge" && node.bridgeKey) {
      const card = snapshot.bridgeCards?.[node.bridgeKey];
      const label = snapshot.bridges[node.bridgeKey] ?? node.bridgeKey;
      const title = card?.title ?? `${node.bridgeKey} \u2014 ${label}`;
      const summary = card?.summary ?? "";
      const href = card?.cardPath ? companionHref(snapshot, card.cardPath) : "";
      const linkHtml = href ? `<p><a href="${escapeHtml(href)}" target="_blank" rel="noopener">Bridge concept card</a></p>` : "";
      return `
        <h2>${escapeHtml(title)}</h2>
        ${summary ? `<p class="bridge-summary">${escapeHtml(summary)}</p>` : `<p>${escapeHtml(label)}</p>`}
        ${linkHtml}`;
    }
    const listing = snapshot.listings.find((l) => l.id === node.projectId);
    if (!listing) return "";
    const dom = dominantBridge(listingWeights(listing));
    const logoHtml = listing.logoLocal ? `<img class="panel-logo" src="./data/${listing.logoLocal}" alt="" />` : "";
    return `
      ${logoHtml}
      <h2>${escapeHtml(listing.title)}</h2>
      <p class="meta">${escapeHtml(listing.category)} \xB7 ${escapeHtml(listing.status)}</p>
      <p>${escapeHtml(listing.description)}</p>
      ${listing.link ? `<p><a href="${escapeHtml(listing.link)}" target="_blank" rel="noopener">Website</a></p>` : ""}
      ${renderProvenance(listing)}
      ${dom ? `<p><strong>Dominant:</strong> ${dom}</p>` : ""}
      <div>${renderWeightBars(listing, snapshot.bridges)}</div>`;
  }
  function renderPanel(node) {
    panel.innerHTML = panelHtml(node);
  }
  function drawBridgeNode(ctx2, n, active) {
    const col = n.bridgeKey ? BRIDGE_COLORS[n.bridgeKey] : "#888";
    const scale = active ? BRIDGE_POP_SCALE : 1;
    const r = n.radius;
    const label = n.bridgeKey ? BRIDGE_SHORT_LABELS[n.bridgeKey] : "";
    ctx2.save();
    ctx2.translate(n.x, n.y);
    ctx2.scale(scale, scale);
    ctx2.fillStyle = col;
    ctx2.strokeStyle = active ? "#111" : "#fff";
    ctx2.lineWidth = active ? 2.5 : 1.5;
    ctx2.beginPath();
    ctx2.moveTo(0, -r);
    ctx2.lineTo(r, 0);
    ctx2.lineTo(0, r);
    ctx2.lineTo(-r, 0);
    ctx2.closePath();
    ctx2.fill();
    ctx2.stroke();
    ctx2.fillStyle = "#fff";
    ctx2.font = `bold ${Math.max(8, Math.round(10 / scale))}px system-ui`;
    ctx2.textAlign = "center";
    ctx2.textBaseline = "middle";
    ctx2.fillText(label, 0, 0);
    ctx2.restore();
  }
  function handleMobileTap(node) {
    if (!node) {
      selectedId = null;
      closeOverlay();
      return;
    }
    if (selectedId === node.id) {
      openOverlay(node);
    } else {
      selectedId = node.id;
      closeOverlay();
    }
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
    const focusId = focusNodeId();
    const focusNode = focusId ? nodeById.get(focusId) : void 0;
    const edgeHighlight = (e) => {
      if (!focusNode) return "normal";
      if (focusNode.kind === "project") {
        if (e.kind !== "crux") return "normal";
        return e.source === focusId ? "bright" : "dim";
      }
      if (focusNode.kind === "bridge") {
        if (e.kind === "crux") {
          return e.target === focusId ? "bright" : "dim";
        }
        if (e.kind === "bridge-dep" || e.kind === "bridge-dep-static") {
          return e.source === focusId || e.target === focusId ? "bright" : "dim";
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
      if (n.kind === "bridge") continue;
      drawProjectNode(ctx, n, focusId === n.id, logos);
    }
    for (const n of nodes) {
      if (n.kind !== "bridge") continue;
      drawBridgeNode(ctx, n, focusId === n.id);
    }
    ctx.restore();
  }
  let raf = 0;
  function loop() {
    for (let i = 0; i < 2; i++) simulateStep(nodes, edges, simOptions());
    drawFrame();
    raf = requestAnimationFrame(loop);
  }
  ui.querySelector("[data-category]")?.addEventListener("change", rebuild);
  geometryBtn.addEventListener("click", () => {
    pinGeometry = pinGeometry === "dependency" ? "circle" : "dependency";
    transform = { x: 0, y: 0, scale: DEFAULT_VIEW_SCALE };
    updateGeometryLabel();
    rebuild();
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
  }
  function updateDesktopHover(clientX, clientY, offsetX, offsetY) {
    if (dragging || touchInteraction()) return;
    const node = pick(offsetX, offsetY);
    if (node?.kind === "project" || node?.kind === "bridge") {
      hoveredId = node.id;
      if (sidePanelVisible()) renderPanel(node);
      if (node.kind === "bridge" && node.bridgeKey) {
        const card = snapshot.bridgeCards?.[node.bridgeKey];
        tooltip.textContent = card?.title ?? snapshot.bridges[node.bridgeKey] ?? node.label;
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
    hoveredId = null;
    if (sidePanelVisible()) resetPanel();
    hideTooltip();
    canvas.style.cursor = "grab";
  }
  canvas.addEventListener("mousemove", (e) => {
    updateDesktopHover(e.clientX, e.clientY, e.offsetX, e.offsetY);
  });
  canvas.addEventListener("mouseleave", () => {
    if (touchInteraction()) return;
    hoveredId = null;
    if (sidePanelVisible()) resetPanel();
    hideTooltip();
    canvas.style.cursor = "grab";
  });
  canvas.addEventListener("mousedown", (e) => {
    pointerDown = { x: e.clientX, y: e.clientY, ox: e.offsetX, oy: e.offsetY };
    dragging = { lastX: e.clientX, lastY: e.clientY };
    hideTooltip();
  });
  window.addEventListener("mousemove", (e) => {
    if (!dragging) return;
    transform.x += (e.clientX - dragging.lastX) / transform.scale;
    transform.y += (e.clientY - dragging.lastY) / transform.scale;
    dragging.lastX = e.clientX;
    dragging.lastY = e.clientY;
  });
  window.addEventListener("mouseup", (e) => {
    if (pointerDown && !touchInteraction() && Date.now() >= suppressMouseUntil) {
      const moved = Math.hypot(e.clientX - pointerDown.x, e.clientY - pointerDown.y);
      if (moved < 6) {
        const node = pick(pointerDown.ox, pointerDown.oy);
        if (node) {
          if (sidePanelVisible()) navigateToNode(node);
          else openOverlay(node);
        } else if (compactLayout()) {
          closeOverlay();
        }
      }
    }
    dragging = null;
    pointerDown = null;
  });
  canvas.addEventListener(
    "touchstart",
    (e) => {
      if (e.touches.length !== 1) return;
      const t = e.touches[0];
      const rect = canvas.getBoundingClientRect();
      pointerDown = {
        x: t.clientX,
        y: t.clientY,
        ox: t.clientX - rect.left,
        oy: t.clientY - rect.top
      };
      dragging = { lastX: t.clientX, lastY: t.clientY };
    },
    { passive: true }
  );
  canvas.addEventListener(
    "touchmove",
    (e) => {
      if (!dragging || e.touches.length !== 1) return;
      const t = e.touches[0];
      transform.x += (t.clientX - dragging.lastX) / transform.scale;
      transform.y += (t.clientY - dragging.lastY) / transform.scale;
      dragging.lastX = t.clientX;
      dragging.lastY = t.clientY;
    },
    { passive: true }
  );
  canvas.addEventListener("touchend", (e) => {
    if (!pointerDown) return;
    const t = e.changedTouches[0];
    const moved = Math.hypot(t.clientX - pointerDown.x, t.clientY - pointerDown.y);
    if (moved < 10 && touchInteraction()) {
      handleMobileTap(pick(pointerDown.ox, pointerDown.oy));
      suppressMouseUntil = Date.now() + 400;
    }
    dragging = null;
    pointerDown = null;
  });
  for (const el of ui.querySelectorAll("[data-overlay-close]")) {
    el.addEventListener("click", () => {
      closeOverlay();
    });
  }
  updateGeometryLabel();
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
