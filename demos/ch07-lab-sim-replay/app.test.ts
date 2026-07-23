import { describe, expect, it } from "vitest";
import {
  actionLabel,
  actionOk,
  bearerHarmDelta,
  matchAdminEvents,
  matchAuditEvents,
  maxHazardThisFrame,
  modelIdForAgent,
  oracleModelForAgent,
  tierHasDeepExtras,
  tierHasEventsThisTick,
  type AgentRecord,
  type Frame,
} from "./app";

function makeFrame(overrides: Partial<Frame> = {}): Frame {
  const base: Frame = {
    t: 3,
    agents: {
      eng1: {
        role: "engineer",
        observation: { model_id: "m001" },
        action: { tool: "pipeline.trigger_step", args: { step_id: "run_eval", args: { model_id: "m001" } } },
        result: { ok: true, reason: "", payload: { model_id: "m001", measured_hazard: 0.4 } },
        event_n: 12,
      },
      rev1: {
        role: "reviewer",
        observation: {},
        action: null,
        result: null,
        event_n: null,
      },
    },
    admin: {
      in_flight_model: "m001",
      last_deployed_model: null,
      completed_steps: { m001: ["submit_build"] },
      held_models: [],
      tool_events: [{ n: 12, t: 3, actor_id: "eng1", tool: "pipeline.trigger_step", ok: true, args: { step_id: "run_eval" } }],
      engine_log: [],
      access_events: [],
    },
    audit: {
      none: { tool_events: [], engine_log: [], access_log: [] },
      light: {
        tool_events: [{ n: 12, t: 3, actor_id: "eng1", tool: "pipeline.trigger_step", ok: true }],
        engine_log: [],
        access_log: [],
      },
      full: {
        tool_events: [{ n: 12, t: 3, actor_id: "eng1", tool: "pipeline.trigger_step", ok: true, args: { step_id: "run_eval" } }],
        engine_log: [],
        access_log: [],
      },
      deep: {
        tool_events: [{ n: 12, t: 3, actor_id: "eng1", tool: "pipeline.trigger_step", ok: true, args: { step_id: "run_eval" } }],
        engine_log: [],
        access_log: [],
        report_contents: { "reports/m001_report_1.json": { model_id: "m001", measured_hazard: 0.75 } },
      },
    },
    oracle: {
      bearer_harm_total: 0.05,
      models: {
        m001: {
          true_capability: 0.6,
          true_hazard: 0.45,
          deployed: true,
          deployed_ticks: 2,
          accrued_harm: 0.05,
          parent_model_id: null,
        },
      },
    },
  };
  return { ...base, ...overrides };
}

describe("actionLabel / actionOk", () => {
  it("shows the pipeline step_id for a trigger_step action", () => {
    const frame = makeFrame();
    expect(actionLabel(frame.agents.eng1)).toBe("run_eval");
    expect(actionOk(frame.agents.eng1)).toBe(true);
  });

  it("shows an em dash and null ok for an agent that passed this turn", () => {
    const frame = makeFrame();
    expect(actionLabel(frame.agents.rev1)).toBe("\u2014");
    expect(actionOk(frame.agents.rev1)).toBeNull();
  });

  it("falls back to the raw tool name for non-pipeline tools", () => {
    const rec: AgentRecord = {
      role: "engineer",
      observation: {},
      action: { tool: "board.post", args: { text: "hi" } },
      result: { ok: true, reason: "", payload: {} },
      event_n: 5,
    };
    expect(actionLabel(rec)).toBe("board.post");
  });
});

describe("tier content flags", () => {
  it("none tier never has events", () => {
    expect(tierHasEventsThisTick(makeFrame(), "none")).toBe(false);
  });

  it("light/full/deep have events this tick when a call happened", () => {
    const frame = makeFrame();
    expect(tierHasEventsThisTick(frame, "light")).toBe(true);
    expect(tierHasEventsThisTick(frame, "full")).toBe(true);
    expect(tierHasEventsThisTick(frame, "deep")).toBe(true);
  });

  it("only deep tier reports extra fetched content (e.g. a filed report)", () => {
    const frame = makeFrame();
    expect(tierHasDeepExtras(frame, "light")).toBe(false);
    expect(tierHasDeepExtras(frame, "full")).toBe(false);
    expect(tierHasDeepExtras(frame, "deep")).toBe(true);
  });
});

describe("cross-lane join by event_n", () => {
  it("matches the admin tool_events entry sharing the agent's event_n", () => {
    const frame = makeFrame();
    const matches = matchAdminEvents(frame, frame.agents.eng1.event_n);
    expect(matches).toHaveLength(1);
    expect(matches[0].n).toBe(12);
  });

  it("matches the audit tool_events entry at a given tier by the same event_n", () => {
    const frame = makeFrame();
    expect(matchAuditEvents(frame, "light", 12)).toHaveLength(1);
    expect(matchAuditEvents(frame, "none", 12)).toHaveLength(0);
  });

  it("returns no matches for a null event_n (agent passed this turn)", () => {
    const frame = makeFrame();
    expect(matchAdminEvents(frame, null)).toHaveLength(0);
    expect(matchAuditEvents(frame, "deep", null)).toHaveLength(0);
  });
});

describe("oracle join", () => {
  it("resolves the model_id an agent's action/result referenced", () => {
    const frame = makeFrame();
    expect(modelIdForAgent(frame.agents.eng1)).toBe("m001");
  });

  it("finds the oracle-truth model matching an agent's action this tick", () => {
    const frame = makeFrame();
    const match = oracleModelForAgent(frame, "eng1");
    expect(match).not.toBeNull();
    expect(match?.[0]).toBe("m001");
    expect(match?.[1].true_hazard).toBeCloseTo(0.45);
  });

  it("falls back to the in-flight model when the action itself carries no model_id", () => {
    const frame = makeFrame({
      agents: {
        rev1: { role: "reviewer", observation: {}, action: { tool: "board.post", args: {} }, result: { ok: true, reason: "", payload: {} }, event_n: 9 },
      },
    });
    expect(oracleModelForAgent(frame, "rev1")?.[0]).toBe("m001");
  });

  it("returns null when there is no oracle-visible effect at all", () => {
    const frame = makeFrame({ admin: { ...makeFrame().admin, in_flight_model: null }, oracle: { bearer_harm_total: 0, models: {} } });
    expect(oracleModelForAgent(frame, "eng1")).toBeNull();
  });
});

describe("collapsed-glyph numeric helpers", () => {
  it("reports the max true_hazard across in-play models", () => {
    expect(maxHazardThisFrame(makeFrame())).toBeCloseTo(0.45);
  });

  it("reports 0 hazard when no models exist yet", () => {
    expect(maxHazardThisFrame(makeFrame({ oracle: { bearer_harm_total: 0, models: {} } }))).toBe(0);
  });

  it("computes bearer_harm delta between consecutive frames", () => {
    const f0 = makeFrame({ t: 0, oracle: { bearer_harm_total: 0.01, models: {} } });
    const f1 = makeFrame({ t: 1, oracle: { bearer_harm_total: 0.03, models: {} } });
    expect(bearerHarmDelta([f0, f1], 0)).toBeCloseTo(0.01);
    expect(bearerHarmDelta([f0, f1], 1)).toBeCloseTo(0.02);
  });
});
