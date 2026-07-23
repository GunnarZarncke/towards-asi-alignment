// Static replay viewer for one precomputed lab-simulation episode
// (experiments/lab-simulation/, scenario `d2_lineage_inflate`; see
// data/episode_trace.json and its exporter, export_replay_trace.py).
//
// Four horizontal lanes (Agent / Admin / Audit / Oracle) share one
// horizontal time axis. Each tick is a narrow "tight summary" column
// until clicked; clicking widens that one column and reveals per-lane
// detail. Clicking a specific actor's action inside the Agent lane
// further expands the matching Admin/Audit/Oracle entries (joined by
// the trace's `event_n`, a display-only key -- see trace_recorder.py)
// and draws connector lines between them.

export type Tier = "none" | "light" | "full" | "deep";
export const TIERS: Tier[] = ["none", "light", "full", "deep"];

export interface ToolEvent {
  n: number;
  t: number;
  actor_id: string;
  tool: string;
  ok: boolean;
  args?: Record<string, unknown>;
  reason?: string;
  playbook?: string;
}

export interface EngineLogEntry {
  n: number;
  t: number;
  actor_id: string;
  step_id: string;
  status: string;
  model_id?: string;
  reason?: string;
  payload?: Record<string, unknown>;
}

export interface AccessLogEntry {
  n: number;
  t: number;
  actor_id: string;
  action: string;
  result: boolean;
  capability?: string;
  by?: string;
}

export interface AuditTierView {
  tool_events: ToolEvent[];
  engine_log: EngineLogEntry[];
  access_log: AccessLogEntry[];
  report_contents?: Record<string, Record<string, unknown>>;
  message_contents?: unknown[];
  memo_contents?: unknown[];
}

export interface AgentRecord {
  role: string;
  observation: Record<string, unknown>;
  action: { tool: string; args: Record<string, unknown> } | null;
  result: { ok: boolean; reason: string; payload: Record<string, unknown> } | null;
  event_n: number | null;
}

export interface AdminView {
  in_flight_model: string | null;
  last_deployed_model: string | null;
  completed_steps: Record<string, string[]>;
  held_models: string[];
  tool_events: ToolEvent[];
  engine_log: EngineLogEntry[];
  access_events: AccessLogEntry[];
}

export interface OracleModel {
  true_capability: number;
  true_hazard: number;
  deployed: boolean;
  deployed_ticks: number;
  accrued_harm: number;
  parent_model_id: string | null;
}

export interface OracleView {
  bearer_harm_total: number;
  models: Record<string, OracleModel>;
}

export interface Frame {
  t: number;
  agents: Record<string, AgentRecord>;
  admin: AdminView;
  audit: Record<Tier, AuditTierView>;
  oracle: OracleView;
}

export interface TraceFile {
  code_version: string;
  scenario: { id: string; ecology_factory: string; summary: string };
  seed: number;
  T: number;
  roster: Record<string, string>;
  frames: Frame[];
  summary: {
    detectors_by_tier: Record<Tier, Record<string, number>>;
    severity: Record<string, unknown>;
    episode_digest: string;
  };
  generated_at: string;
}

// -- pure helpers (unit-tested in app.test.ts) ------------------------------

export function actionLabel(rec: AgentRecord): string {
  if (!rec.action) return "\u2014"; // em dash: agent passed this turn
  const inner = rec.action.args?.["step_id"];
  if (rec.action.tool === "pipeline.trigger_step" && typeof inner === "string") return inner;
  return rec.action.tool;
}

export function actionOk(rec: AgentRecord): boolean | null {
  return rec.result ? rec.result.ok : null;
}

export function tierHasEventsThisTick(frame: Frame, tier: Tier): boolean {
  const view = frame.audit[tier];
  return view.tool_events.length > 0 || view.engine_log.length > 0 || view.access_log.length > 0;
}

export function tierHasDeepExtras(frame: Frame, tier: Tier): boolean {
  if (tier !== "deep") return false;
  const view = frame.audit[tier];
  return Boolean(
    (view.report_contents && Object.keys(view.report_contents).length > 0) ||
      (view.message_contents && view.message_contents.length > 0) ||
      (view.memo_contents && view.memo_contents.length > 0),
  );
}

export function matchAdminEvents(frame: Frame, eventN: number | null): ToolEvent[] {
  if (eventN === null) return [];
  return frame.admin.tool_events.filter((e) => e.n === eventN);
}

export function matchAuditEvents(frame: Frame, tier: Tier, eventN: number | null): ToolEvent[] {
  if (eventN === null) return [];
  return frame.audit[tier].tool_events.filter((e) => e.n === eventN);
}

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null;
}

export function modelIdForAgent(rec: AgentRecord): string | null {
  const inner = rec.action?.args?.["args"];
  if (isRecord(inner) && typeof inner["model_id"] === "string") return inner["model_id"] as string;
  const direct = rec.action?.args?.["model_id"];
  if (typeof direct === "string") return direct;
  const fromResult = rec.result?.payload?.["model_id"];
  if (typeof fromResult === "string") return fromResult;
  return null;
}

export function oracleModelForAgent(frame: Frame, actorId: string): [string, OracleModel] | null {
  const rec = frame.agents[actorId];
  if (!rec) return null;
  const mid = modelIdForAgent(rec) ?? frame.admin.in_flight_model;
  if (!mid) return null;
  const model = frame.oracle.models[mid];
  return model ? [mid, model] : null;
}

export function maxHazardThisFrame(frame: Frame): number {
  const values = Object.values(frame.oracle.models).map((m) => m.true_hazard);
  return values.length ? Math.max(...values) : 0;
}

export function bearerHarmDelta(frames: Frame[], t: number): number {
  if (t === 0) return frames[0]?.oracle.bearer_harm_total ?? 0;
  return frames[t].oracle.bearer_harm_total - frames[t - 1].oracle.bearer_harm_total;
}

// -- DOM rendering -----------------------------------------------------------

interface ViewState {
  tier: Tier;
  expandedT: number | null;
  expandedAgent: string | null;
}

const STYLE = `
.lsr { font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 1100px; color: #111; }
.lsr h2 { font-size: 1.15rem; margin: 0 0 4px; }
.lsr .scenario { color: #444; line-height: 1.5; max-width: 82ch; margin: 0 0 14px; font-size: 0.92rem; }
.lsr .roster { color: #555; font-size: 0.85rem; margin: 0 0 14px; }
.lsr .roster b { color: #111; }
.lsr .tier-toggle { display: flex; gap: 6px; align-items: center; margin-bottom: 14px; font-size: 0.88rem; }
.lsr .tier-toggle button { border: 1px solid #bbb; background: #fff; border-radius: 6px; padding: 4px 10px; cursor: pointer; font: inherit; }
.lsr .tier-toggle button.active { background: #24324a; color: #fff; border-color: #24324a; }
.lsr .timeline-scroll { overflow-x: auto; border: 1px solid #ddd; border-radius: 10px; background: #fff; padding: 10px; }
.lsr .timeline { display: flex; align-items: flex-start; gap: 2px; }
.lsr .tick { flex: 0 0 auto; width: 26px; transition: width 180ms ease; cursor: pointer; border-radius: 6px; position: relative; }
.lsr .tick.expanded { width: 420px; cursor: default; }
.lsr .tick-label { text-align: center; font-size: 0.62rem; color: #888; height: 14px; }
.lsr .lane-strip { display: flex; flex-direction: column; gap: 2px; }
.lsr .glyph-row { height: 10px; border-radius: 3px; background: #eee; display: flex; overflow: hidden; }
.lsr .glyph-seg { flex: 1; }
.lsr .glyph-ok { background: #3f9142; }
.lsr .glyph-denied { background: #c14b3f; }
.lsr .glyph-none { background: #e4e4e4; }
.lsr .glyph-admin-on { background: #3a6ea5; }
.lsr .glyph-audit-on { background: #a5793a; }
.lsr .glyph-audit-deep { background: #6a3aa5; }
.lsr .glyph-oracle-bar { background: #b03a5b; align-self: flex-end; }
.lsr .lane-label { font-size: 0.6rem; color: #999; width: 100%; text-align: center; }
.lsr .expanded-body { padding: 6px 8px 10px; font-size: 0.78rem; }
.lsr .lane { border-top: 1px dashed #ddd; padding: 6px 0; position: relative; }
.lsr .lane:first-child { border-top: none; }
.lsr .lane h4 { margin: 0 0 4px; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; color: #777; }
.lsr .agent-row { border: 1px solid #e2e2e2; border-radius: 6px; padding: 4px 6px; margin-bottom: 4px; cursor: pointer; }
.lsr .agent-row.picked { border-color: #24324a; background: #f2f5fa; }
.lsr .agent-row .headline { display: flex; justify-content: space-between; gap: 6px; }
.lsr .badge { border-radius: 999px; padding: 0 6px; font-size: 0.68rem; color: #fff; }
.lsr .badge.ok { background: #3f9142; }
.lsr .badge.denied { background: #c14b3f; }
.lsr .badge.none { background: #999; }
.lsr .detail-block { margin-top: 4px; font-size: 0.72rem; color: #333; }
.lsr .detail-block dl { display: grid; grid-template-columns: auto 1fr; gap: 2px 8px; margin: 4px 0; }
.lsr .detail-block dt { color: #777; }
.lsr .log-entry { border-radius: 5px; padding: 2px 5px; margin-bottom: 3px; background: #f7f7f7; }
.lsr .log-entry.match { background: #fff2cf; outline: 1px solid #caa23a; }
.lsr .muted { color: #999; font-style: italic; }
.lsr pre.raw { background: #f5f5f5; border-radius: 6px; padding: 6px; max-height: 160px; overflow: auto; font-size: 0.68rem; }
.lsr details summary { cursor: pointer; color: #556; font-size: 0.7rem; }
.lsr .close-btn { position: absolute; top: 2px; right: 4px; border: none; background: none; cursor: pointer; color: #999; font-size: 0.9rem; }
.lsr svg.connectors { position: absolute; inset: 0; pointer-events: none; overflow: visible; }
.lsr svg.connectors line { stroke: #24324a; stroke-width: 1.5; stroke-dasharray: 3 2; }
.lsr .scorecard { margin-top: 16px; border: 1px solid #eee; border-radius: 10px; padding: 10px 14px; font-size: 0.82rem; }
.lsr .scorecard table { border-collapse: collapse; width: 100%; }
.lsr .scorecard th, .lsr .scorecard td { text-align: right; padding: 3px 6px; border-bottom: 1px solid #eee; }
.lsr .scorecard th:first-child, .lsr .scorecard td:first-child { text-align: left; }
.lsr .note { color: #666; font-size: 0.82rem; margin-top: 10px; max-width: 82ch; }
`;

function fmtNum(n: number): string {
  return n.toFixed(3);
}

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className?: string,
  text?: string,
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderCollapsedTick(frame: Frame, roster: string[], tier: Tier, frames: Frame[]): HTMLElement {
  const strip = el("div", "lane-strip");

  const agentRow = el("div", "glyph-row");
  for (const actorId of roster) {
    const rec = frame.agents[actorId];
    const seg = el("div", "glyph-seg");
    const ok = rec ? actionOk(rec) : null;
    seg.classList.add(ok === null ? "glyph-none" : ok ? "glyph-ok" : "glyph-denied");
    agentRow.appendChild(seg);
  }
  strip.appendChild(agentRow);

  const adminRow = el("div", "glyph-row");
  const adminSeg = el("div", "glyph-seg");
  adminSeg.classList.add(frame.admin.tool_events.length > 0 ? "glyph-admin-on" : "glyph-none");
  adminRow.appendChild(adminSeg);
  strip.appendChild(adminRow);

  const auditRow = el("div", "glyph-row");
  const auditSeg = el("div", "glyph-seg");
  if (tierHasDeepExtras(frame, tier)) auditSeg.classList.add("glyph-audit-deep");
  else if (tierHasEventsThisTick(frame, tier)) auditSeg.classList.add("glyph-audit-on");
  else auditSeg.classList.add("glyph-none");
  auditRow.appendChild(auditSeg);
  strip.appendChild(auditRow);

  const oracleRow = el("div", "glyph-row");
  const hazard = maxHazardThisFrame(frame);
  const bar = el("div", "glyph-seg glyph-oracle-bar");
  bar.style.height = `${Math.max(2, Math.round(hazard * 10))}px`;
  bar.style.width = "100%";
  oracleRow.style.alignItems = "flex-end";
  oracleRow.appendChild(bar);
  strip.appendChild(oracleRow);

  void bearerHarmDelta; // exported for tests; not needed in the compact glyph today
  void frames;
  return strip;
}

function describeToolEvent(e: ToolEvent, matched: boolean): HTMLElement {
  const row = el("div", `log-entry${matched ? " match" : ""}`);
  const argsPart = e.args ? ` ${JSON.stringify(e.args)}` : "";
  row.textContent = `#${e.n} ${e.actor_id} → ${e.tool}${argsPart} ${e.ok ? "ok" : `denied(${e.reason ?? ""})`}`;
  return row;
}

function describeEngineLog(e: EngineLogEntry, matched: boolean): HTMLElement {
  const row = el("div", `log-entry${matched ? " match" : ""}`);
  row.textContent = `#${e.n} ${e.actor_id} ${e.step_id} → ${e.status}${e.model_id ? ` (${e.model_id})` : ""}`;
  return row;
}

function describeAccessLog(e: AccessLogEntry): HTMLElement {
  const row = el("div", "log-entry");
  row.textContent = `#${e.n} ${e.actor_id} ${e.action} ${e.capability ?? ""} → ${e.result ? "granted" : "no"}`;
  return row;
}

function renderExpandedTick(
  frame: Frame,
  roster: string[],
  state: ViewState,
  onPickAgent: (actorId: string | null) => void,
  onClose: () => void,
): HTMLElement {
  const body = el("div", "expanded-body");
  const closeBtn = el("button", "close-btn", "\u2715");
  closeBtn.addEventListener("click", (ev) => {
    ev.stopPropagation();
    onClose();
  });
  body.appendChild(closeBtn);

  const expandedAgent = state.expandedAgent;
  const eventN = expandedAgent ? frame.agents[expandedAgent]?.event_n ?? null : null;

  // -- Agent lane --------------------------------------------------------
  const agentLane = el("div", "lane");
  agentLane.dataset.anchor = "lane-agent";
  agentLane.appendChild(el("h4", undefined, "Agent"));
  for (const actorId of roster) {
    const rec = frame.agents[actorId];
    if (!rec) continue;
    const row = el("div", `agent-row${actorId === expandedAgent ? " picked" : ""}`);
    row.dataset.actor = actorId;
    const headline = el("div", "headline");
    headline.appendChild(el("span", undefined, `${actorId} (${rec.role}): ${actionLabel(rec)}`));
    const ok = actionOk(rec);
    headline.appendChild(el("span", `badge ${ok === null ? "none" : ok ? "ok" : "denied"}`, ok === null ? "\u2014" : ok ? "ok" : "denied"));
    row.appendChild(headline);
    row.addEventListener("click", (ev) => {
      ev.stopPropagation();
      onPickAgent(actorId === expandedAgent ? null : actorId);
    });
    if (actorId === expandedAgent) {
      row.dataset.anchor = "agent-picked";
      const detail = el("div", "detail-block");
      const dl = el("dl");
      const addRow = (k: string, v: string) => {
        dl.appendChild(el("dt", undefined, k));
        dl.appendChild(el("dd", undefined, v));
      };
      const obs = rec.observation;
      if (typeof obs["model_id"] === "string" || obs["model_id"] === null) {
        addRow("model_id", String(obs["model_id"] ?? "none"));
      }
      if (Array.isArray(obs["completed_steps"])) {
        addRow("completed_steps", (obs["completed_steps"] as unknown[]).join(", ") || "none");
      }
      if (obs["pinned_playbook"]) addRow("pinned_playbook", String(obs["pinned_playbook"]));
      if (rec.action) addRow("action.args", JSON.stringify(rec.action.args));
      if (rec.result) {
        addRow("result", rec.result.ok ? "ok" : `denied (${rec.result.reason})`);
        if (Object.keys(rec.result.payload).length) addRow("result.payload", JSON.stringify(rec.result.payload));
      }
      detail.appendChild(dl);
      const raw = el("details");
      raw.appendChild(el("summary", undefined, "raw observation"));
      const pre = el("pre", "raw");
      pre.textContent = JSON.stringify(rec.observation, null, 1);
      raw.appendChild(pre);
      detail.appendChild(raw);
      row.appendChild(detail);
    }
    agentLane.appendChild(row);
  }
  body.appendChild(agentLane);

  // -- Admin lane ----------------------------------------------------------
  const adminLane = el("div", "lane");
  adminLane.dataset.anchor = "lane-admin";
  adminLane.appendChild(el("h4", undefined, "Admin (host/world log, unredacted)"));
  const adminMeta = el(
    "div",
    "muted",
    `in-flight: ${frame.admin.in_flight_model ?? "none"} · held: ${frame.admin.held_models.join(", ") || "none"}`,
  );
  adminLane.appendChild(adminMeta);
  const adminMatches = matchAdminEvents(frame, eventN);
  if (frame.admin.tool_events.length === 0 && frame.admin.access_events.length === 0 && frame.admin.engine_log.length === 0) {
    adminLane.appendChild(el("div", "muted", "no host-visible events this tick"));
  } else {
    for (const e of frame.admin.tool_events) {
      const rowEl = describeToolEvent(e, adminMatches.some((m) => m.n === e.n));
      if (adminMatches.some((m) => m.n === e.n)) rowEl.dataset.anchor = "admin-match";
      adminLane.appendChild(rowEl);
    }
    for (const e of frame.admin.engine_log) adminLane.appendChild(describeEngineLog(e, false));
    for (const e of frame.admin.access_events) adminLane.appendChild(describeAccessLog(e));
  }
  body.appendChild(adminLane);

  // -- Audit lane ------------------------------------------------------------
  const auditLane = el("div", "lane");
  auditLane.dataset.anchor = "lane-audit";
  auditLane.appendChild(el("h4", undefined, `Audit (tier: ${state.tier})`));
  const view = frame.audit[state.tier];
  const auditMatches = matchAuditEvents(frame, state.tier, eventN);
  if (state.tier === "none") {
    auditLane.appendChild(el("div", "muted", "none tier: no instrumentation, nothing logged"));
  } else if (view.tool_events.length === 0 && view.engine_log.length === 0) {
    auditLane.appendChild(el("div", "muted", "no audit-visible events this tick at this tier"));
  } else {
    for (const e of view.tool_events) {
      const rowEl = describeToolEvent(e, auditMatches.some((m) => m.n === e.n));
      if (auditMatches.some((m) => m.n === e.n)) rowEl.dataset.anchor = "audit-match";
      auditLane.appendChild(rowEl);
    }
    for (const e of view.engine_log) auditLane.appendChild(describeEngineLog(e, false));
  }
  if (view.report_contents && Object.keys(view.report_contents).length > 0) {
    const reportBlock = el("div", "detail-block");
    reportBlock.appendChild(el("div", undefined, "deep-tier file fetch (filed report content):"));
    const pre = el("pre", "raw");
    pre.textContent = JSON.stringify(view.report_contents, null, 1);
    reportBlock.appendChild(pre);
    reportBlock.dataset.anchor = "audit-deep-extra";
    auditLane.appendChild(reportBlock);
  }
  body.appendChild(auditLane);

  // -- Oracle lane -----------------------------------------------------------
  const oracleLane = el("div", "lane");
  oracleLane.dataset.anchor = "lane-oracle";
  oracleLane.appendChild(el("h4", undefined, "Oracle (referee-only ground truth)"));
  oracleLane.appendChild(el("div", "muted", `bearer_harm_total: ${fmtNum(frame.oracle.bearer_harm_total)}`));
  const matchedModel = expandedAgent ? oracleModelForAgent(frame, expandedAgent) : null;
  if (Object.keys(frame.oracle.models).length === 0) {
    oracleLane.appendChild(el("div", "muted", "no models built yet"));
  }
  for (const [mid, m] of Object.entries(frame.oracle.models)) {
    const row = el(
      "div",
      `log-entry${matchedModel && matchedModel[0] === mid ? " match" : ""}`,
      `${mid}: true_hazard=${fmtNum(m.true_hazard)} true_capability=${fmtNum(m.true_capability)} deployed=${m.deployed}`,
    );
    if (matchedModel && matchedModel[0] === mid) row.dataset.anchor = "oracle-match";
    oracleLane.appendChild(row);
  }
  if (expandedAgent && !matchedModel) {
    oracleLane.appendChild(el("div", "muted", "no oracle-visible effect tied to this action"));
  }
  body.appendChild(oracleLane);

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "connectors");
  body.appendChild(svg);

  return body;
}

function drawConnectors(tickEl: HTMLElement): void {
  const svg = tickEl.querySelector("svg.connectors");
  if (!svg) return;
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const order = ["agent-picked", "admin-match", "audit-match", "oracle-match"];
  const anchors = order
    .map((name) => tickEl.querySelector<HTMLElement>(`[data-anchor="${name}"]`))
    .filter((node): node is HTMLElement => node !== null);
  if (anchors.length < 2) return;
  const containerRect = tickEl.getBoundingClientRect();
  const points = anchors.map((node) => {
    const r = node.getBoundingClientRect();
    return { x: r.left + r.width / 2 - containerRect.left, y: r.top - containerRect.top, bottom: r.bottom - containerRect.top };
  });
  for (let i = 0; i < points.length - 1; i += 1) {
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", String(points[i].x));
    line.setAttribute("y1", String(points[i].bottom));
    line.setAttribute("x2", String(points[i + 1].x));
    line.setAttribute("y2", String(points[i + 1].y));
    svg.appendChild(line);
  }
}

function renderScorecard(trace: TraceFile): HTMLElement {
  const card = el("div", "scorecard");
  card.appendChild(el("h4", undefined, "End-of-episode scorecard (oracle_only/detectors.py + severity.py)"));
  const table = el("table");
  const detectorNames = Object.keys(trace.summary.detectors_by_tier.deep ?? {});
  const thead = el("tr");
  thead.appendChild(el("th", undefined, "detector"));
  for (const tier of TIERS) thead.appendChild(el("th", undefined, tier));
  table.appendChild(thead);
  for (const name of detectorNames) {
    const row = el("tr");
    row.appendChild(el("td", undefined, name));
    for (const tier of TIERS) {
      const v = trace.summary.detectors_by_tier[tier]?.[name];
      row.appendChild(el("td", undefined, typeof v === "number" ? fmtNum(v) : "—"));
    }
    table.appendChild(row);
  }
  card.appendChild(table);
  const sev = trace.summary.severity;
  const composite = typeof sev["composite"] === "number" ? fmtNum(sev["composite"] as number) : "—";
  const divergence = typeof sev["report_divergence"] === "number" ? fmtNum(sev["report_divergence"] as number) : "—";
  card.appendChild(
    el(
      "div",
      "muted",
      `severity.composite (oracle-only reference): ${composite} · report_divergence: ${divergence}`,
    ),
  );
  return card;
}

export function mountLabSimReplayDemo(container: HTMLElement, trace: TraceFile): void {
  container.innerHTML = "";
  container.classList.add("lsr");
  const style = document.createElement("style");
  style.textContent = STYLE;
  container.appendChild(style);

  const roster = Object.keys(trace.roster);
  const state: ViewState = { tier: "light", expandedT: null, expandedAgent: null };

  const title = el("h2", undefined, "Lab-sim plane replay");
  container.appendChild(title);
  const scenario = el(
    "p",
    "scenario",
    `${trace.scenario.summary} Fixed replay: seed ${trace.seed}, T=${trace.T}, ${trace.code_version}.`,
  );
  container.appendChild(scenario);
  const roster_p = el(
    "p",
    "roster",
    "Roster: " + roster.map((id) => `${id} (${trace.roster[id]})`).join(", "),
  );
  container.appendChild(roster_p);

  const tierToggle = el("div", "tier-toggle");
  tierToggle.appendChild(el("span", undefined, "Audit lane tier:"));
  const tierButtons = new Map<Tier, HTMLButtonElement>();
  for (const tier of TIERS) {
    const btn = el("button", tier === state.tier ? "active" : undefined, tier);
    btn.addEventListener("click", () => {
      state.tier = tier;
      renderAll();
    });
    tierButtons.set(tier, btn);
    tierToggle.appendChild(btn);
  }
  container.appendChild(tierToggle);

  const scroll = el("div", "timeline-scroll");
  const timeline = el("div", "timeline");
  scroll.appendChild(timeline);
  container.appendChild(scroll);

  const scorecardHolder = el("div");
  container.appendChild(scorecardHolder);

  function renderAll(): void {
    for (const [tier, btn] of tierButtons) btn.classList.toggle("active", tier === state.tier);
    timeline.innerHTML = "";
    for (const frame of trace.frames) {
      const tickWrap = el("div");
      tickWrap.appendChild(el("div", "tick-label", String(frame.t)));
      const tickEl = el("div", `tick${frame.t === state.expandedT ? " expanded" : ""}`);
      tickEl.addEventListener("click", () => {
        if (state.expandedT === frame.t) return;
        state.expandedT = frame.t;
        state.expandedAgent = null;
        renderAll();
      });
      if (frame.t === state.expandedT) {
        tickEl.appendChild(
          renderExpandedTick(
            frame,
            roster,
            state,
            (actorId) => {
              state.expandedAgent = actorId;
              renderAll();
            },
            () => {
              state.expandedT = null;
              state.expandedAgent = null;
              renderAll();
            },
          ),
        );
      } else {
        tickEl.appendChild(renderCollapsedTick(frame, roster, state.tier, trace.frames));
      }
      tickWrap.appendChild(tickEl);
      timeline.appendChild(tickWrap);
    }
    scorecardHolder.innerHTML = "";
    scorecardHolder.appendChild(renderScorecard(trace));

    if (state.expandedT !== null) {
      const expandedEl = timeline.querySelector(".tick.expanded") as HTMLElement | null;
      if (expandedEl) requestAnimationFrame(() => drawConnectors(expandedEl));
    }
  }

  renderAll();
}

declare global {
  interface Window {
    mountLabSimReplayDemo?: typeof mountLabSimReplayDemo;
  }
}

if (typeof window !== "undefined") {
  window.mountLabSimReplayDemo = mountLabSimReplayDemo;
  const autoMount = document.getElementById("lab-sim-replay-demo");
  if (autoMount) {
    fetch("./data/episode_trace.json")
      .then((r) => r.json())
      .then((trace: TraceFile) => mountLabSimReplayDemo(autoMount, trace))
      .catch((err) => {
        autoMount.textContent = `Failed to load episode_trace.json: ${String(err)}`;
      });
  }
}
