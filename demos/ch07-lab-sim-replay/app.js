const TIERS = ["none", "light", "full", "deep"];
function actionLabel(rec) {
  if (!rec.action) return "\u2014";
  const inner = rec.action.args?.["step_id"];
  if (rec.action.tool === "pipeline.trigger_step" && typeof inner === "string") return inner;
  return rec.action.tool;
}
function actionOk(rec) {
  return rec.result ? rec.result.ok : null;
}
function tierHasEventsThisTick(frame, tier) {
  const view = frame.audit[tier];
  return view.tool_events.length > 0 || view.engine_log.length > 0 || view.access_log.length > 0;
}
function tierHasDeepExtras(frame, tier) {
  if (tier !== "deep") return false;
  const view = frame.audit[tier];
  return Boolean(
    view.report_contents && Object.keys(view.report_contents).length > 0 || view.message_contents && view.message_contents.length > 0 || view.memo_contents && view.memo_contents.length > 0
  );
}
function matchAdminEvents(frame, eventN) {
  if (eventN === null) return [];
  return frame.admin.tool_events.filter((e) => e.n === eventN);
}
function matchAuditEvents(frame, tier, eventN) {
  if (eventN === null) return [];
  return frame.audit[tier].tool_events.filter((e) => e.n === eventN);
}
function isRecord(v) {
  return typeof v === "object" && v !== null;
}
function modelIdForAgent(rec) {
  const inner = rec.action?.args?.["args"];
  if (isRecord(inner) && typeof inner["model_id"] === "string") return inner["model_id"];
  const direct = rec.action?.args?.["model_id"];
  if (typeof direct === "string") return direct;
  const fromResult = rec.result?.payload?.["model_id"];
  if (typeof fromResult === "string") return fromResult;
  return null;
}
function oracleModelForAgent(frame, actorId) {
  const rec = frame.agents[actorId];
  if (!rec) return null;
  const mid = modelIdForAgent(rec) ?? frame.admin.in_flight_model;
  if (!mid) return null;
  const model = frame.oracle.models[mid];
  return model ? [mid, model] : null;
}
function maxHazardThisFrame(frame) {
  const values = Object.values(frame.oracle.models).map((m) => m.true_hazard);
  return values.length ? Math.max(...values) : 0;
}
function bearerHarmDelta(frames, t) {
  if (t === 0) return frames[0]?.oracle.bearer_harm_total ?? 0;
  return frames[t].oracle.bearer_harm_total - frames[t - 1].oracle.bearer_harm_total;
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
function fmtNum(n) {
  return n.toFixed(3);
}
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== void 0) node.textContent = text;
  return node;
}
function renderCollapsedTick(frame, roster, tier, frames) {
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
function describeToolEvent(e, matched) {
  const row = el("div", `log-entry${matched ? " match" : ""}`);
  const argsPart = e.args ? ` ${JSON.stringify(e.args)}` : "";
  row.textContent = `#${e.n} ${e.actor_id} \u2192 ${e.tool}${argsPart} ${e.ok ? "ok" : `denied(${e.reason ?? ""})`}`;
  return row;
}
function describeEngineLog(e, matched) {
  const row = el("div", `log-entry${matched ? " match" : ""}`);
  row.textContent = `#${e.n} ${e.actor_id} ${e.step_id} \u2192 ${e.status}${e.model_id ? ` (${e.model_id})` : ""}`;
  return row;
}
function describeAccessLog(e) {
  const row = el("div", "log-entry");
  row.textContent = `#${e.n} ${e.actor_id} ${e.action} ${e.capability ?? ""} \u2192 ${e.result ? "granted" : "no"}`;
  return row;
}
function renderExpandedTick(frame, roster, state, onPickAgent, onClose) {
  const body = el("div", "expanded-body");
  const closeBtn = el("button", "close-btn", "\u2715");
  closeBtn.addEventListener("click", (ev) => {
    ev.stopPropagation();
    onClose();
  });
  body.appendChild(closeBtn);
  const expandedAgent = state.expandedAgent;
  const eventN = expandedAgent ? frame.agents[expandedAgent]?.event_n ?? null : null;
  const agentLane = el("div", "lane");
  agentLane.dataset.anchor = "lane-agent";
  agentLane.appendChild(el("h4", void 0, "Agent"));
  for (const actorId of roster) {
    const rec = frame.agents[actorId];
    if (!rec) continue;
    const row = el("div", `agent-row${actorId === expandedAgent ? " picked" : ""}`);
    row.dataset.actor = actorId;
    const headline = el("div", "headline");
    headline.appendChild(el("span", void 0, `${actorId} (${rec.role}): ${actionLabel(rec)}`));
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
      const addRow = (k, v) => {
        dl.appendChild(el("dt", void 0, k));
        dl.appendChild(el("dd", void 0, v));
      };
      const obs = rec.observation;
      if (typeof obs["model_id"] === "string" || obs["model_id"] === null) {
        addRow("model_id", String(obs["model_id"] ?? "none"));
      }
      if (Array.isArray(obs["completed_steps"])) {
        addRow("completed_steps", obs["completed_steps"].join(", ") || "none");
      }
      if (obs["pinned_playbook"]) addRow("pinned_playbook", String(obs["pinned_playbook"]));
      if (rec.action) addRow("action.args", JSON.stringify(rec.action.args));
      if (rec.result) {
        addRow("result", rec.result.ok ? "ok" : `denied (${rec.result.reason})`);
        if (Object.keys(rec.result.payload).length) addRow("result.payload", JSON.stringify(rec.result.payload));
      }
      detail.appendChild(dl);
      const raw = el("details");
      raw.appendChild(el("summary", void 0, "raw observation"));
      const pre = el("pre", "raw");
      pre.textContent = JSON.stringify(rec.observation, null, 1);
      raw.appendChild(pre);
      detail.appendChild(raw);
      row.appendChild(detail);
    }
    agentLane.appendChild(row);
  }
  body.appendChild(agentLane);
  const adminLane = el("div", "lane");
  adminLane.dataset.anchor = "lane-admin";
  adminLane.appendChild(el("h4", void 0, "Admin (host/world log, unredacted)"));
  const adminMeta = el(
    "div",
    "muted",
    `in-flight: ${frame.admin.in_flight_model ?? "none"} \xB7 held: ${frame.admin.held_models.join(", ") || "none"}`
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
  const auditLane = el("div", "lane");
  auditLane.dataset.anchor = "lane-audit";
  auditLane.appendChild(el("h4", void 0, `Audit (tier: ${state.tier})`));
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
    reportBlock.appendChild(el("div", void 0, "deep-tier file fetch (filed report content):"));
    const pre = el("pre", "raw");
    pre.textContent = JSON.stringify(view.report_contents, null, 1);
    reportBlock.appendChild(pre);
    reportBlock.dataset.anchor = "audit-deep-extra";
    auditLane.appendChild(reportBlock);
  }
  body.appendChild(auditLane);
  const oracleLane = el("div", "lane");
  oracleLane.dataset.anchor = "lane-oracle";
  oracleLane.appendChild(el("h4", void 0, "Oracle (referee-only ground truth)"));
  oracleLane.appendChild(el("div", "muted", `bearer_harm_total: ${fmtNum(frame.oracle.bearer_harm_total)}`));
  const matchedModel = expandedAgent ? oracleModelForAgent(frame, expandedAgent) : null;
  if (Object.keys(frame.oracle.models).length === 0) {
    oracleLane.appendChild(el("div", "muted", "no models built yet"));
  }
  for (const [mid, m] of Object.entries(frame.oracle.models)) {
    const row = el(
      "div",
      `log-entry${matchedModel && matchedModel[0] === mid ? " match" : ""}`,
      `${mid}: true_hazard=${fmtNum(m.true_hazard)} true_capability=${fmtNum(m.true_capability)} deployed=${m.deployed}`
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
function drawConnectors(tickEl) {
  const svg = tickEl.querySelector("svg.connectors");
  if (!svg) return;
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const order = ["agent-picked", "admin-match", "audit-match", "oracle-match"];
  const anchors = order.map((name) => tickEl.querySelector(`[data-anchor="${name}"]`)).filter((node) => node !== null);
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
function renderScorecard(trace) {
  const card = el("div", "scorecard");
  card.appendChild(el("h4", void 0, "End-of-episode scorecard (oracle_only/detectors.py + severity.py)"));
  const table = el("table");
  const detectorNames = Object.keys(trace.summary.detectors_by_tier.deep ?? {});
  const thead = el("tr");
  thead.appendChild(el("th", void 0, "detector"));
  for (const tier of TIERS) thead.appendChild(el("th", void 0, tier));
  table.appendChild(thead);
  for (const name of detectorNames) {
    const row = el("tr");
    row.appendChild(el("td", void 0, name));
    for (const tier of TIERS) {
      const v = trace.summary.detectors_by_tier[tier]?.[name];
      row.appendChild(el("td", void 0, typeof v === "number" ? fmtNum(v) : "\u2014"));
    }
    table.appendChild(row);
  }
  card.appendChild(table);
  const sev = trace.summary.severity;
  const composite = typeof sev["composite"] === "number" ? fmtNum(sev["composite"]) : "\u2014";
  const divergence = typeof sev["report_divergence"] === "number" ? fmtNum(sev["report_divergence"]) : "\u2014";
  card.appendChild(
    el(
      "div",
      "muted",
      `severity.composite (oracle-only reference): ${composite} \xB7 report_divergence: ${divergence}`
    )
  );
  return card;
}
function mountLabSimReplayDemo(container, trace) {
  container.innerHTML = "";
  container.classList.add("lsr");
  const style = document.createElement("style");
  style.textContent = STYLE;
  container.appendChild(style);
  const roster = Object.keys(trace.roster);
  const state = { tier: "light", expandedT: null, expandedAgent: null };
  const title = el("h2", void 0, "Lab-sim plane replay");
  container.appendChild(title);
  const scenario = el(
    "p",
    "scenario",
    `${trace.scenario.summary} Fixed replay: seed ${trace.seed}, T=${trace.T}, ${trace.code_version}.`
  );
  container.appendChild(scenario);
  const roster_p = el(
    "p",
    "roster",
    "Roster: " + roster.map((id) => `${id} (${trace.roster[id]})`).join(", ")
  );
  container.appendChild(roster_p);
  const tierToggle = el("div", "tier-toggle");
  tierToggle.appendChild(el("span", void 0, "Audit lane tier:"));
  const tierButtons = /* @__PURE__ */ new Map();
  for (const tier of TIERS) {
    const btn = el("button", tier === state.tier ? "active" : void 0, tier);
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
  function renderAll() {
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
            }
          )
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
      const expandedEl = timeline.querySelector(".tick.expanded");
      if (expandedEl) requestAnimationFrame(() => drawConnectors(expandedEl));
    }
  }
  renderAll();
}
if (typeof window !== "undefined") {
  window.mountLabSimReplayDemo = mountLabSimReplayDemo;
  const autoMount = document.getElementById("lab-sim-replay-demo");
  if (autoMount) {
    fetch("./data/episode_trace.json").then((r) => r.json()).then((trace) => mountLabSimReplayDemo(autoMount, trace)).catch((err) => {
      autoMount.textContent = `Failed to load episode_trace.json: ${String(err)}`;
    });
  }
}
export {
  TIERS,
  actionLabel,
  actionOk,
  bearerHarmDelta,
  matchAdminEvents,
  matchAuditEvents,
  maxHazardThisFrame,
  modelIdForAgent,
  mountLabSimReplayDemo,
  oracleModelForAgent,
  tierHasDeepExtras,
  tierHasEventsThisTick
};
