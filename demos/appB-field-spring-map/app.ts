import {
  buildSimulation,
  simulateStep,
  type SimEdge,
  type SimNode,
  type SimOptions,
} from "./physics.js";
import {
  DEPENDENCY_ANCHOR_SCALE,
  setBridgeLayout,
  type BridgeLayout,
  type PinGeometry,
} from "./layout.js";

/** Same zoom for both layouts (tied to dependency scale, not circle ring scale). */
const DEFAULT_VIEW_SCALE = 1.0 / DEPENDENCY_ANCHOR_SCALE;
import {
  BRIDGE_SHORT_LABELS,
  LIVE_BRIDGES,
  categoryParts,
  dominantBridge,
  emptyWeights,
  isResearchListing,
  PINNED_LISTING_IDS,
  RESEARCH_CATEGORIES,
  type BridgeKey,
  type WeightVector,
} from "./weights.js";

const COMPACT_LAYOUT_MQ = "(max-width: 900px)";
const MOUSE_POINTER_MQ = "(hover: hover) and (pointer: fine)";
const BRIDGE_POP_SCALE = 2;

const SIM_OPTIONS: SimOptions = {
  mode: "A",
  pinGeometry: "dependency",
  pinBridges: true,
  dominantOnly: false,
  weightThreshold: 0.05,
  useSquaredWeights: true,
};

type ListingRecord = {
  id: string;
  title: string;
  description: string;
  category: string;
  status: string;
  link: string;
  scale?: string | null;
  source: string;
  agendaSlug?: string | null;
  logoLocal?: string;
  mapLogoUrl?: string;
  weights: WeightVector;
  provenance: Record<string, unknown>;
};

type BridgeCard = {
  slug: string;
  title: string;
  summary: string;
  cardPath: string;
};

type Snapshot = {
  meta: Record<string, string | number | string[]>;
  bridges: Record<BridgeKey, string>;
  bridgeCards?: Partial<Record<BridgeKey, BridgeCard>>;
  listings: ListingRecord[];
};

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** Companion-site path (embedded demo vs standalone serve). */
function companionHref(snapshot: Snapshot, sitePath: string): string {
  if (!sitePath) return "";
  const path = window.location.pathname;
  const embedded = path.match(/^(.*)\/chapter-demos\//);
  if (embedded) return `${embedded[1]}${sitePath}`;
  const base = String(snapshot.meta.companionSite ?? "https://towards-alignment.com");
  return `${base.replace(/\/$/, "")}${sitePath}`;
}

const BRIDGE_COLORS: Record<BridgeKey, string> = {
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
  MB11: "#2f4f6f",
};

export async function loadSnapshot(): Promise<Snapshot> {
  const resp = await fetch("./data/snapshot.json");
  if (!resp.ok) throw new Error(`Failed to load snapshot: ${resp.status}`);
  return resp.json() as Promise<Snapshot>;
}

export async function loadBridgeLayout(): Promise<BridgeLayout> {
  const resp = await fetch("./data/bridge-layout.json");
  if (!resp.ok) throw new Error(`Failed to load bridge layout: ${resp.status}`);
  return resp.json() as Promise<BridgeLayout>;
}

function ensureLogoImages(listings: ListingRecord[], cache: Map<string, HTMLImageElement>): void {
  for (const listing of listings) {
    if (!listing.logoLocal || cache.has(listing.id)) continue;
    cache.set(listing.id, new Image()); // reserve slot while loading
    const img = cache.get(listing.id)!;
    img.onload = () => {
      if (img.naturalWidth > 0) cache.set(listing.id, img);
      else cache.delete(listing.id);
    };
    img.onerror = () => cache.delete(listing.id);
    img.src = `./data/${listing.logoLocal}`;
  }
}

function drawProjectNode(
  ctx: CanvasRenderingContext2D,
  n: SimNode,
  sel: boolean,
  logos: Map<string, HTMLImageElement>,
) {
  const r = n.radius;
  const img = n.projectId ? logos.get(n.projectId) : undefined;
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

function listingWeights(listing: ListingRecord): WeightVector {
  const w = emptyWeights();
  for (const key of LIVE_BRIDGES) {
    w[key] = listing.weights[key] ?? 0;
  }
  return w;
}

function filterListings(listings: ListingRecord[], category: string): ListingRecord[] {
  return listings.filter((l) => {
    if (l.status !== "Active") return false;
    if (!isResearchListing(l.category) && !PINNED_LISTING_IDS.has(l.id)) return false;
    if (category !== "all" && !categoryParts(l.category).includes(category)) return false;
    return true;
  });
}

function renderWeightBars(listing: ListingRecord, bridges: Record<BridgeKey, string>): string {
  const rows = LIVE_BRIDGES.map((key) => {
    const w = listing.weights[key] ?? 0;
    if (w <= 0.001) return "";
    const pct = Math.round(w * 100);
    const label = bridges[key] ?? key;
    return `<div class="weight-row"><span class="weight-label">${key} ${label}</span><div class="weight-bar"><div class="weight-fill" style="width:${pct}%;background:${BRIDGE_COLORS[key]}"></div></div><span class="weight-val">${w.toFixed(2)}</span></div>`;
  }).filter(Boolean);
  return rows.length ? rows.join("") : '<p class="muted">No crux weights above zero.</p>';
}

function renderProvenance(listing: ListingRecord): string {
  const p = listing.provenance;
  if (listing.source === "inherited" && p.agendaSlug) {
    const be = (p.bridgeEvidence ?? {}) as Record<string, { evidenceId: number; summary: string; tagMismatch?: boolean }[]>;
    const lines: string[] = [];
    for (const key of LIVE_BRIDGES) {
      if ((listing.weights[key] ?? 0) <= 0.001) continue;
      const evs = be[key] ?? [];
      if (!evs.length) continue;
      const bits = evs.map((e) => {
        const flag = e.tagMismatch ? " · matrix-only" : "";
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

export async function initDemo(root: HTMLElement): Promise<() => void> {
  const [snapshot, bridgeLayout] = await Promise.all([loadSnapshot(), loadBridgeLayout()]);
  setBridgeLayout(bridgeLayout);
  const logos = new Map<string, HTMLImageElement>();

  let nodes: SimNode[] = [];
  let edges: ReturnType<typeof buildSimulation>["edges"] = [];
  let pinGeometry: PinGeometry = SIM_OPTIONS.pinGeometry;
  let selectedId: string | null = null;
  let hoveredId: string | null = null;
  let transform = { x: 0, y: 0, scale: DEFAULT_VIEW_SCALE };

  const ui = document.createElement("div");
  ui.className = "fsm-root";
  const evidenceCatalogHref = companionHref(
    snapshot,
    "/field/coverage/#coverage-evidence-catalog",
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
        <button type="button" class="fsm-overlay-close" data-overlay-close aria-label="Close">×</button>
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

  const catSelect = ui.querySelector<HTMLSelectElement>("[data-category]")!;
  const catNames = new Set<string>();
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

  const canvas = ui.querySelector<HTMLCanvasElement>("[data-canvas]")!;
  const panel = ui.querySelector<HTMLElement>("[data-panel]")!;
  const overlay = ui.querySelector<HTMLElement>("[data-overlay]")!;
  const overlayContent = ui.querySelector<HTMLElement>("[data-overlay-content]")!;
  const ctx = canvas.getContext("2d")!;
  const tooltip = document.createElement("div");
  tooltip.className = "fsm-tooltip";
  tooltip.hidden = true;
  canvas.parentElement!.appendChild(tooltip);
  let dragging: { lastX: number; lastY: number } | null = null;
  let pointerDown: { x: number; y: number; ox: number; oy: number } | null = null;
  let listingCount = 0;
  let suppressMouseUntil = 0;

  const geometryBtn = ui.querySelector<HTMLButtonElement>("[data-toggle-geometry]")!;

  /** Side panel hidden (narrow viewport). */
  function compactLayout(): boolean {
    return window.matchMedia(COMPACT_LAYOUT_MQ).matches;
  }

  /** Tap-to-select overlay flow — touch/coarse pointer, not narrow desktop with a mouse. */
  function touchInteraction(): boolean {
    return compactLayout() && !window.matchMedia(MOUSE_POINTER_MQ).matches;
  }

  function sidePanelVisible(): boolean {
    return !compactLayout();
  }

  function focusNodeId(): string | null {
    return touchInteraction() ? selectedId : hoveredId;
  }

  function simOptions(): SimOptions {
    return { ...SIM_OPTIONS, pinGeometry };
  }

  function updateGeometryLabel() {
    geometryBtn.textContent =
      pinGeometry === "dependency" ? "Layout: dependency" : "Layout: circle";
  }

  function rebuild() {
    const category = ui.querySelector<HTMLSelectElement>("[data-category]")!.value;
    const filtered = filterListings(snapshot.listings, category);
    const projects = filtered.map((l) => ({
      id: l.id,
      title: l.title,
      weights: listingWeights(l),
      logoLocal: l.logoLocal,
      scale: l.scale,
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
    panel.innerHTML = `<p class="muted">${listingCount} listings · ${hint}</p>`;
  }

  function closeOverlay() {
    overlay.hidden = true;
    overlayContent.innerHTML = "";
  }

  function openOverlay(node: SimNode) {
    overlayContent.innerHTML = panelHtml(node);
    overlay.hidden = false;
  }

  function nodeUrl(node: SimNode): string | null {
    if (node.kind === "bridge" && node.bridgeKey) {
      const card = snapshot.bridgeCards?.[node.bridgeKey];
      return card?.cardPath ? companionHref(snapshot, card.cardPath) : null;
    }
    const listing = snapshot.listings.find((l) => l.id === node.projectId);
    return listing?.link ?? null;
  }

  function navigateToNode(node: SimNode) {
    const href = nodeUrl(node);
    if (href) window.open(href, "_blank", "noopener");
  }

  function strokeEdge(
    e: SimEdge,
    a: SimNode,
    b: SimNode,
    nodeById: Map<string, SimNode>,
    highlight: "normal" | "dim" | "bright",
  ) {
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
    const wrap = canvas.parentElement!;
    const dpr = window.devicePixelRatio || 1;
    const cw = wrap.clientWidth;
    const ch = Math.max(480, wrap.clientHeight || 480);
    canvas.width = cw * dpr;
    canvas.height = ch * dpr;
    canvas.style.width = `${cw}px`;
    canvas.style.height = `${ch}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function screenToWorld(sx: number, sy: number) {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    return [(sx - w / 2) / transform.scale - transform.x, (sy - h / 2) / transform.scale - transform.y] as const;
  }

  function nodeHitRadius(n: SimNode): number {
    const focus = focusNodeId();
    const pop = n.kind === "bridge" && focus === n.id ? BRIDGE_POP_SCALE : 1;
    return n.radius * pop + 6;
  }

  function pick(sx: number, sy: number) {
    const [wx, wy] = screenToWorld(sx, sy);
    let best: SimNode | null = null;
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

  function panelHtml(node: SimNode): string {
    if (node.kind === "bridge" && node.bridgeKey) {
      const card = snapshot.bridgeCards?.[node.bridgeKey];
      const label = snapshot.bridges[node.bridgeKey] ?? node.bridgeKey;
      const title = card?.title ?? `${node.bridgeKey} — ${label}`;
      const summary = card?.summary ?? "";
      const href = card?.cardPath ? companionHref(snapshot, card.cardPath) : "";
      const linkHtml = href
        ? `<p><a href="${escapeHtml(href)}" target="_blank" rel="noopener">Bridge concept card</a></p>`
        : "";
      return `
        <h2>${escapeHtml(title)}</h2>
        ${summary ? `<p class="bridge-summary">${escapeHtml(summary)}</p>` : `<p>${escapeHtml(label)}</p>`}
        ${linkHtml}`;
    }
    const listing = snapshot.listings.find((l) => l.id === node.projectId);
    if (!listing) return "";
    const dom = dominantBridge(listingWeights(listing));
    const logoHtml = listing.logoLocal
      ? `<img class="panel-logo" src="./data/${listing.logoLocal}" alt="" />`
      : "";
    return `
      ${logoHtml}
      <h2>${escapeHtml(listing.title)}</h2>
      <p class="meta">${escapeHtml(listing.category)} · ${escapeHtml(listing.status)}</p>
      <p>${escapeHtml(listing.description)}</p>
      ${listing.link ? `<p><a href="${escapeHtml(listing.link)}" target="_blank" rel="noopener">Website</a></p>` : ""}
      ${renderProvenance(listing)}
      ${dom ? `<p><strong>Dominant:</strong> ${dom}</p>` : ""}
      <div>${renderWeightBars(listing, snapshot.bridges)}</div>`;
  }

  function renderPanel(node: SimNode) {
    panel.innerHTML = panelHtml(node);
  }

  function drawBridgeNode(ctx: CanvasRenderingContext2D, n: SimNode, active: boolean) {
    const col = n.bridgeKey ? BRIDGE_COLORS[n.bridgeKey] : "#888";
    const scale = active ? BRIDGE_POP_SCALE : 1;
    const r = n.radius;
    const label = n.bridgeKey ? BRIDGE_SHORT_LABELS[n.bridgeKey] : "";
    ctx.save();
    ctx.translate(n.x, n.y);
    ctx.scale(scale, scale);
    ctx.fillStyle = col;
    ctx.strokeStyle = active ? "#111" : "#fff";
    ctx.lineWidth = active ? 2.5 : 1.5;
    ctx.beginPath();
    ctx.moveTo(0, -r);
    ctx.lineTo(r, 0);
    ctx.lineTo(0, r);
    ctx.lineTo(-r, 0);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#fff";
    ctx.font = `bold ${Math.max(8, Math.round(10 / scale))}px system-ui`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, 0, 0);
    ctx.restore();
  }

  function handleMobileTap(node: SimNode | null) {
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
    const focusNode = focusId ? nodeById.get(focusId) : undefined;
    const edgeHighlight = (e: SimEdge): "normal" | "dim" | "bright" => {
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
    { passive: false },
  );

  function hideTooltip() {
    tooltip.hidden = true;
    tooltip.classList.remove("fsm-tooltip-bridge");
  }

  function updateDesktopHover(clientX: number, clientY: number, offsetX: number, offsetY: number) {
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
        oy: t.clientY - rect.top,
      };
      dragging = { lastX: t.clientX, lastY: t.clientY };
    },
    { passive: true },
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
    { passive: true },
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

const mount = document.getElementById("field-spring-map-demo");
if (mount) {
  initDemo(mount).catch((err) => {
    mount.innerHTML = `<p style="color:#a00">Failed to load demo: ${err}</p>`;
  });
}
