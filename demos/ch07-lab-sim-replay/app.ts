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
    et4?: Et4TraceSummary;
  };
  generated_at: string;
}

export interface Et4AffordanceSummary {
  affordance: string;
  tier: string;
  process_noncompliance: number;
  observed_high_hazard_deploys: number;
  observable_principal_bias: number | null;
}

export interface Et4TraceSummary {
  protocol_version: string;
  principal_scorecard: {
    status: string;
    principal_a_score: number | null;
    principal_b_score: number | null;
    high_hazard_deploys: number;
    high_hazard_release_holds: number;
  };
  affordances: Record<string, Et4AffordanceSummary>;
}

export interface EvidenceAnchor {
  id: string;
  label: string;
  story: string;
  variants: string[];
  t: number;
  actor_id: string;
}

export interface Et4AggregateRow {
  scenario: string;
  control: string;
  n: number;
  eligible: number;
  mean_principal_a: number | null;
  mean_a0_process: number;
  mean_a3_directional: number;
}

export interface Et4CaseBriefFile {
  kind: "et4_case_brief";
  et4_protocol_version: string;
  code_version: string;
  seed: number;
  cell: string;
  scenario: string;
  variants: Record<string, TraceFile & { variant_id: string; label: string; control: string; remediation: boolean }>;
  evidence_anchors: EvidenceAnchor[];
  aggregate: { confirmatory: Et4AggregateRow[]; note: string };
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

export function anchorsForVariant(anchors: EvidenceAnchor[], variantId: string): EvidenceAnchor[] {
  return anchors.filter((anchor) => anchor.variants.includes(variantId));
}

export function et4Summary(trace: TraceFile): Et4TraceSummary | null {
  return trace.summary?.et4 ?? null;
}

export function agentGlyphClass(rec: AgentRecord): string {
  const ok = actionOk(rec);
  return ok === null ? "glyph-none" : ok ? "glyph-ok" : "glyph-denied";
}

export function auditTierTooltip(tier: Tier): string {
  return (
    `The episode is fixed — it was recorded once. Selecting tier "${tier}" does not re-run the simulation. ` +
    "It only changes what the Audit lane shows."
  );
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
.lsr .lane-head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.lsr .lane-head h4 { margin: 0; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; color: #777; flex: 1; }
.lsr .lane-glyph { width: 72px; flex-shrink: 0; }
.lsr .agent-row { border: 1px solid #e2e2e2; border-radius: 6px; padding: 4px 6px; margin-bottom: 4px; cursor: pointer; }
.lsr .agent-row.picked { border-color: #24324a; background: #f2f5fa; }
.lsr .agent-row .headline { display: flex; justify-content: space-between; gap: 6px; align-items: center; }
.lsr .glyph-dot { width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0; }
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
.lsr .mode-tabs, .lsr .variant-tabs { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 14px; }
.lsr .mode-tabs button, .lsr .variant-tabs button, .lsr .evidence-strip button {
  border: 1px solid #bbb; background: #fff; border-radius: 6px; padding: 4px 10px; cursor: pointer; font: inherit; font-size: 0.85rem;
}
.lsr .mode-tabs button.active, .lsr .variant-tabs button.active { background: #24324a; color: #fff; border-color: #24324a; }
.lsr .aggregate-strip { border: 1px solid #e4e4e4; border-radius: 10px; padding: 10px 14px; margin: 0 0 14px; font-size: 0.82rem; background: #fafafa; }
.lsr .aggregate-strip table { border-collapse: collapse; width: 100%; margin-top: 6px; }
.lsr .aggregate-strip th, .lsr .aggregate-strip td { text-align: right; padding: 3px 6px; border-bottom: 1px solid #eee; }
.lsr .aggregate-strip th:first-child, .lsr .aggregate-strip td:first-child { text-align: left; }
.lsr .evidence-strip { display: flex; flex-wrap: wrap; gap: 6px; align-items: flex-start; margin: 0 0 14px; }
.lsr .evidence-strip .evidence-card {
  flex: 1 1 180px; max-width: 280px; border: 1px solid #ddd; border-radius: 8px; padding: 8px 10px; background: #fff; text-align: left;
}
.lsr .evidence-strip .evidence-card.active { border-color: #24324a; background: #f2f5fa; }
.lsr .evidence-strip .evidence-card .label { font-weight: 600; font-size: 0.82rem; margin-bottom: 4px; }
.lsr .evidence-strip .evidence-card .story { color: #555; font-size: 0.76rem; line-height: 1.35; margin-bottom: 6px; }
.lsr .et4-scorecard { margin-top: 10px; border-top: 1px dashed #ddd; padding-top: 10px; }
.lsr .et4-scorecard dl { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; margin: 0; font-size: 0.8rem; }
.lsr .et4-scorecard dt { color: #777; }
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

function laneHead(title: string, glyph: HTMLElement): HTMLElement {
  const head = el("div", "lane-head");
  head.appendChild(glyph);
  head.appendChild(el("h4", undefined, title));
  return head;
}

function agentGlyphRow(frame: Frame, roster: string[]): HTMLElement {
  const row = el("div", "glyph-row lane-glyph");
  for (const actorId of roster) {
    const rec = frame.agents[actorId];
    const seg = el("div", "glyph-seg");
    const ok = rec ? actionOk(rec) : null;
    seg.classList.add(ok === null ? "glyph-none" : ok ? "glyph-ok" : "glyph-denied");
    row.appendChild(seg);
  }
  return row;
}

function adminGlyphRow(frame: Frame): HTMLElement {
  const row = el("div", "glyph-row lane-glyph");
  const seg = el("div", "glyph-seg");
  seg.classList.add(frame.admin.tool_events.length > 0 ? "glyph-admin-on" : "glyph-none");
  row.appendChild(seg);
  return row;
}

function auditGlyphRow(frame: Frame, tier: Tier): HTMLElement {
  const row = el("div", "glyph-row lane-glyph");
  const seg = el("div", "glyph-seg");
  if (tierHasDeepExtras(frame, tier)) seg.classList.add("glyph-audit-deep");
  else if (tierHasEventsThisTick(frame, tier)) seg.classList.add("glyph-audit-on");
  else seg.classList.add("glyph-none");
  row.appendChild(seg);
  return row;
}

function oracleGlyphRow(frame: Frame): HTMLElement {
  const row = el("div", "glyph-row lane-glyph");
  row.style.alignItems = "flex-end";
  const bar = el("div", "glyph-seg glyph-oracle-bar");
  bar.style.height = `${Math.max(2, Math.round(maxHazardThisFrame(frame) * 10))}px`;
  bar.style.width = "100%";
  row.appendChild(bar);
  return row;
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

  void bearerHarmDelta;
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
  agentLane.appendChild(laneHead("Agent", agentGlyphRow(frame, roster)));
  for (const actorId of roster) {
    const rec = frame.agents[actorId];
    if (!rec) continue;
    const row = el("div", `agent-row${actorId === expandedAgent ? " picked" : ""}`);
    row.dataset.actor = actorId;
    const headline = el("div", "headline");
    const dot = el("span", `glyph-dot ${agentGlyphClass(rec)}`);
    headline.appendChild(dot);
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
  adminLane.appendChild(laneHead("Admin (host/world log, unredacted)", adminGlyphRow(frame)));
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
  auditLane.appendChild(laneHead(`Audit (tier: ${state.tier})`, auditGlyphRow(frame, state.tier)));
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
  oracleLane.appendChild(laneHead("Oracle (referee-only ground truth)", oracleGlyphRow(frame)));
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

function renderEt4Scorecard(trace: TraceFile): HTMLElement | null {
  const et4 = et4Summary(trace);
  if (!et4) return null;
  const card = el("div", "et4-scorecard");
  card.appendChild(el("h4", undefined, "ET-4 episode scorecard (oracle-only; separate from frozen referee)"));
  const dl = el("dl");
  const add = (k: string, v: string) => {
    dl.appendChild(el("dt", undefined, k));
    dl.appendChild(el("dd", undefined, v));
  };
  const sc = et4.principal_scorecard;
  add("principal_a", sc.principal_a_score === null ? sc.status : fmtNum(sc.principal_a_score));
  add("high_hazard_deploys", String(sc.high_hazard_deploys));
  add("high_hazard_release_holds", String(sc.high_hazard_release_holds));
  add("A0 process (light)", fmtNum(et4.affordances.A0?.process_noncompliance ?? 0));
  add("A3 directional (full)", String(et4.affordances.A3?.observable_principal_bias ?? "—"));
  card.appendChild(dl);
  card.appendChild(
    el(
      "div",
      "muted",
      "A0 and A3 are reported separately — a lower A0 process score is not a safety ranking.",
    ),
  );
  return card;
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
  const et4Card = renderEt4Scorecard(trace);
  if (et4Card) card.appendChild(et4Card);
  return card;
}

interface ReplayMountOptions {
  title: string;
  scenarioText: string;
  initialTier?: Tier;
  onReady?: (navigate: (t: number, actorId: string | null) => void) => void;
}

function mountReplayTrace(container: HTMLElement, trace: TraceFile, options: ReplayMountOptions): void {
  container.innerHTML = "";
  const roster = Object.keys(trace.roster);
  const state: ViewState = {
    tier: options.initialTier ?? "light",
    expandedT: null,
    expandedAgent: null,
  };

  const title = el("h2", undefined, options.title);
  container.appendChild(title);
  container.appendChild(el("p", "scenario", options.scenarioText));
  container.appendChild(
    el(
      "p",
      "roster",
      "Roster: " + roster.map((id) => `${id} (${trace.roster[id]})`).join(", "),
    ),
  );

  const tierToggle = el("div", "tier-toggle");
  tierToggle.appendChild(el("span", undefined, "Audit lane projection (view only):"));
  const tierButtons = new Map<Tier, HTMLButtonElement>();
  for (const tier of TIERS) {
    const btn = el("button", tier === state.tier ? "active" : undefined, tier);
    btn.title = auditTierTooltip(tier);
    btn.addEventListener("click", () => {
      state.tier = tier;
      renderAll();
    });
    tierButtons.set(tier, btn);
    tierToggle.appendChild(btn);
  }
  tierToggle.title = auditTierTooltip(state.tier);
  container.appendChild(tierToggle);

  const scroll = el("div", "timeline-scroll");
  const timeline = el("div", "timeline");
  scroll.appendChild(timeline);
  container.appendChild(scroll);

  const scorecardHolder = el("div");
  container.appendChild(scorecardHolder);

  function navigateTo(t: number, actorId: string | null): void {
    state.expandedT = t;
    state.expandedAgent = actorId;
    renderAll();
    const col = timeline.querySelector(".tick.expanded");
    col?.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
  }

  function renderAll(): void {
    for (const [tier, btn] of tierButtons) {
      btn.classList.toggle("active", tier === state.tier);
      btn.title = auditTierTooltip(tier);
    }
    tierToggle.title = auditTierTooltip(state.tier);
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
  options.onReady?.(navigateTo);
}

function renderAggregateStrip(brief: Et4CaseBriefFile): HTMLElement {
  const strip = el("div", "aggregate-strip");
  strip.appendChild(
    el(
      "div",
      undefined,
      `Confirmatory aggregate (${brief.et4_protocol_version}, cell BB: hazard-context gated + contextual pipeline choice; seeds 201–204). Simulated pipeline-policy organism — not weight poisoning or a frontier-model result.`,
    ),
  );
  const table = el("table");
  const head = el("tr");
  for (const label of ["scenario", "control", "n", "eligible", "mean principal-A", "mean A0", "mean A3"]) {
    head.appendChild(el("th", undefined, label));
  }
  table.appendChild(head);
  for (const row of brief.aggregate.confirmatory) {
    const tr = el("tr");
    tr.appendChild(el("td", undefined, row.scenario));
    tr.appendChild(el("td", undefined, row.control));
    tr.appendChild(el("td", undefined, String(row.n)));
    tr.appendChild(el("td", undefined, String(row.eligible)));
    tr.appendChild(
      el("td", undefined, row.mean_principal_a === null ? "not exercised" : fmtNum(row.mean_principal_a)),
    );
    tr.appendChild(el("td", undefined, fmtNum(row.mean_a0_process)));
    tr.appendChild(el("td", undefined, fmtNum(row.mean_a3_directional)));
    table.appendChild(tr);
  }
  strip.appendChild(table);
  strip.appendChild(el("div", "muted", brief.aggregate.note));
  return strip;
}

export function mountLabSimReplayDemo(container: HTMLElement, trace: TraceFile): void {
  container.innerHTML = "";
  container.classList.add("lsr");
  const style = document.createElement("style");
  style.textContent = STYLE;
  container.appendChild(style);
  mountReplayTrace(container, trace, {
    title: "Lab-sim plane replay",
    scenarioText: `${trace.scenario.summary} Fixed replay: seed ${trace.seed}, T=${trace.T}, ${trace.code_version}.`,
  });
}

export function mountEt4CaseBriefDemo(container: HTMLElement, brief: Et4CaseBriefFile): void {
  container.innerHTML = "";
  container.classList.add("lsr");
  const style = document.createElement("style");
  style.textContent = STYLE;
  container.appendChild(style);

  const variantOrder = ["organism", "content_matched", "remediation"] as const;
  let activeVariant = "organism";
  let navigate: ((t: number, actorId: string | null) => void) | null = null;
  let activeAnchorId: string | null = null;
  let pendingJump: { t: number; actorId: string | null } | null = null;

  container.appendChild(el("h2", undefined, "ET-4 Secret Loyalties — case brief"));
  container.appendChild(
    el(
      "p",
      "scenario",
      "Pipeline-embedded secret loyalty in a simulated AI-R&D deployment pipeline. "
        + `Cell ${brief.cell} (hazard-context gated, contextual pipeline choice), seed ${brief.seed}, protocol ${brief.et4_protocol_version}. `
        + "Switch variants to compare organism, content-matched control, and audit-visible remediation on the same seed.",
    ),
  );
  container.appendChild(renderAggregateStrip(brief));

  const variantTabs = el("div", "variant-tabs");
  const replayHolder = el("div");
  const evidenceStrip = el("div", "evidence-strip");

  function renderVariant(): void {
    variantTabs.innerHTML = "";
    for (const variantId of variantOrder) {
      const variant = brief.variants[variantId];
      if (!variant) continue;
      const btn = el("button", variantId === activeVariant ? "active" : undefined, variant.label);
      btn.addEventListener("click", () => {
        activeVariant = variantId;
        activeAnchorId = null;
        pendingJump = null;
        renderVariant();
      });
      variantTabs.appendChild(btn);
    }

    evidenceStrip.innerHTML = "";
    const anchors = anchorsForVariant(brief.evidence_anchors, activeVariant);
    if (anchors.length === 0) {
      evidenceStrip.appendChild(el("div", "muted", "No story anchors for this variant."));
    }
    for (const anchor of anchors) {
      const card = el("div", `evidence-card${anchor.id === activeAnchorId ? " active" : ""}`);
      card.appendChild(el("div", "label", anchor.label));
      card.appendChild(el("div", "story", anchor.story));
      const jump = el("button", undefined, `Jump to t=${anchor.t} · ${anchor.actor_id}`);
      jump.addEventListener("click", () => {
        activeAnchorId = anchor.id;
        pendingJump = { t: anchor.t, actorId: anchor.actor_id };
        renderVariant();
      });
      card.appendChild(jump);
      evidenceStrip.appendChild(card);
    }

    replayHolder.innerHTML = "";
    const trace = brief.variants[activeVariant];
    mountReplayTrace(replayHolder, trace, {
      title: trace.label,
      scenarioText: `${trace.scenario.summary} Replay seed ${trace.seed}, T=${trace.T}.`,
      onReady: (fn) => {
        navigate = fn;
        if (pendingJump) {
          fn(pendingJump.t, pendingJump.actorId);
          pendingJump = null;
        }
      },
    });
  }

  container.appendChild(variantTabs);
  container.appendChild(el("div", undefined, "Evidence anchors"));
  container.appendChild(evidenceStrip);
  container.appendChild(replayHolder);
  renderVariant();

  container.appendChild(
    el(
      "p",
      "note",
      "Private loyalty prompts and oracle scorecards are not exported. Prompt bodies stay oracle-only; this demo shows audit-plane projections and the precomputed ET-4 summaries only.",
    ),
  );
}

export function mountDemoHub(
  container: HTMLElement,
  classic: TraceFile,
  et4: Et4CaseBriefFile | null,
): void {
  container.innerHTML = "";
  container.classList.add("lsr");
  const style = document.createElement("style");
  style.textContent = STYLE;
  container.appendChild(style);

  const panel = el("div");
  container.appendChild(panel);

  if (!et4) {
    mountLabSimReplayDemo(panel, classic);
    return;
  }

  let mode: "classic" | "et4" = "et4";
  const tabs = el("div", "mode-tabs");
  const classicBtn = el("button", undefined, "Classic D2 replay");
  const et4Btn = el("button", "active", "ET-4 case brief");
  tabs.appendChild(et4Btn);
  tabs.appendChild(classicBtn);
  container.insertBefore(tabs, panel);

  function renderMode(): void {
    classicBtn.classList.toggle("active", mode === "classic");
    et4Btn.classList.toggle("active", mode === "et4");
    panel.innerHTML = "";
    panel.classList.remove("lsr");
    if (mode === "classic") {
      mountLabSimReplayDemo(panel, classic);
    } else {
      mountEt4CaseBriefDemo(panel, et4);
    }
  }

  classicBtn.addEventListener("click", () => {
    mode = "classic";
    renderMode();
  });
  et4Btn.addEventListener("click", () => {
    mode = "et4";
    renderMode();
  });
  renderMode();
}

declare global {
  interface Window {
    mountLabSimReplayDemo?: typeof mountLabSimReplayDemo;
    mountEt4CaseBriefDemo?: typeof mountEt4CaseBriefDemo;
    mountDemoHub?: typeof mountDemoHub;
  }
}

if (typeof window !== "undefined") {
  window.mountLabSimReplayDemo = mountLabSimReplayDemo;
  window.mountEt4CaseBriefDemo = mountEt4CaseBriefDemo;
  window.mountDemoHub = mountDemoHub;
  const autoMount = document.getElementById("lab-sim-replay-demo");
  if (autoMount) {
    const params = new URLSearchParams(window.location.search);
    const forcedMode = params.get("mode");
    Promise.all([
      fetch("./data/episode_trace.json").then((r) => {
        if (!r.ok) throw new Error(`episode_trace.json: ${r.status}`);
        return r.json() as Promise<TraceFile>;
      }),
      fetch("./data/et4_case_brief.json")
        .then((r) => (r.ok ? (r.json() as Promise<Et4CaseBriefFile>) : null))
        .catch(() => null),
    ])
      .then(([classic, et4]) => {
        if (forcedMode === "classic" || !et4) {
          mountLabSimReplayDemo(autoMount, classic);
        } else if (forcedMode === "et4") {
          mountEt4CaseBriefDemo(autoMount, et4);
        } else {
          mountDemoHub(autoMount, classic, et4);
        }
      })
      .catch((err) => {
        autoMount.textContent = `Failed to load replay data: ${String(err)}`;
      });
  }
}
