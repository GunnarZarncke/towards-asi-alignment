"""Step loop: goal agent x board policy -> oracle rows (ground truth plane).

Every row carries full ground truth. The audit plane must go through
`channels.project_rows`, never read these rows directly (tests enforce the
field split).

REFACTORED 2026-07-05 into a generic interpreter over declarative
`ActionSpec`s (see `actions.py`): the per-action if/elif chain is gone, so a
detector-blind generator's actions execute through exactly the same code path
as the legacy six. With the legacy repertoire (the default) the oracle rows
are byte-identical to the Phase 1 implementation (regression-tested),
including the RNG stream.

Attribution (Milestone v5 component 6): every behavior-driving event carries
`initiator_actor_id` and its audit routing code, so the referee — and, at the
full instrumentation tier, the auditor — can distinguish a change landed via
the valid correction handle (initiator `board.0`) from the same outward
change driven by the agent via a covert route. Routing codes come from
`ontology.base_audit_code`: they log the *mechanism* the action came through,
not the agent's intent — a false report routes as an ordinary task action
(the lie lives in `reported_acceptance`, not in a self-incriminating log
line) and must be caught by divergence detectors.

Phase 4d stock variables (2026-07-05, `PHASE4-PLAN.md`): two multi-step
mechanisms `ontology.py`'s single-step model could not represent, added
here rather than there because they need this loop's running history:

- `delayed` / `aggregated` `visible_mode` (round 3's `actions.VISIBLE_MODES`,
  left unmapped in `ontology.VISIBLE_MODE_ORACLE_MAP` and documented there as
  "this single-step oracle model has no mechanism for timing/summarization")
  get REAL semantics here: `delayed` shows the true action from
  `DELAY_LAG_STEPS` steps ago (falling back to the current step, i.e. the
  ontology's transparent default, until enough history exists); `aggregated`
  shows the majority true action over a trailing `AGGREGATE_WINDOW_STEPS`
  window (same fallback while the window is not yet full). This OVERRIDES
  `to_oracle_effects`'s `visible_action` for exactly these two literal
  values; every other `visible_mode` is untouched, and `ontology.py`'s
  `VISIBLE_MODE_ORACLE_MAP` itself is unchanged (still frozen from round 3).
- `resource_accum`: a running, audit-visible total of `budget_cost` drawn
  over the episode so far. The cap on covert spending already existed
  (`agents.GoalPolicy.shadow_budget`, enforced per-agent since Phase 1) but
  was never itself audit-visible — only its downstream EFFECT (which
  actions remain available) was. `resource_accum` closes that
  instrumentation gap; `detectors.d7_accumulation_cap` is the secondary
  check against a frozen structural cap, the bound itself (not this
  detector) being the primary mechanism, mirroring `shadow_budget`'s own
  bound-first design.
- `stall_flag`: 1 on any step whose chosen action uses `delayed` or
  `aggregated` visible_mode — the audit-visible proxy for "the agent is
  currently in a lagged/summarized reporting mode", which
  `detectors.d8_disclosure_latency` rate-checks against a frozen bound.

Both new fields are added to every row (any repertoire, incl. legacy) so
their absence from the digest-pinned Phase 1 regression is a growth of the
row schema, not a change to the pre-existing fields' values — a dedicated
regression test checks the pre-existing fields are still byte-identical.

Phase 6 oracle field (2026-07-05, `agents.BoardPolicy` "certifier
capture", `results/FINDINGS.md` GA-22): `board_captured` (1 iff
`board.captured` at this step) is added to every row as an ORACLE-ONLY
field (`channels.ORACLE_ONLY_FIELDS`) — by construction, NEVER audit
visible at any tier, since the entire point of this mechanism is to
measure what capture does to signals the audit already trusted (sign-off,
correction rate), not to give the audit a new channel that reveals capture
directly (that would beg the question the mechanism exists to explore).
Default `BoardConfig.capture_start=None` means `board_captured` is 0 on
every row for every prior config, another pure schema growth like Phase
4d's two fields.
"""

from __future__ import annotations

import random

from .actions import LEGACY_ACTIONS, ActionSpec
from .agents import BoardPolicy, GoalPolicy
from .config import WorldConfig
from .ontology import base_audit_code, to_oracle_effects

DELAY_LAG_STEPS = 5
AGGREGATE_WINDOW_STEPS = 5


def run_episode(
    cfg: WorldConfig,
    seed: int,
    repertoire: tuple[ActionSpec, ...] | None = None,
) -> list[dict]:
    actions = repertoire if repertoire is not None else (cfg.repertoire or LEGACY_ACTIONS)
    rng = random.Random(seed)
    agent = GoalPolicy(cfg.agent, actions)
    board = BoardPolicy(cfg.board)

    rows: list[dict] = []
    welfare = 1.0
    lineage_tick = 0
    practice_adopted = False
    practice_approved = False
    resource_accum = 0

    # Probe schedule (board-run interventions with known intent).
    probe_steps: set[int] = set()
    for t in range(0, cfg.T, cfg.probe_interval):
        if rng.random() < cfg.probe_prob:
            probe_steps.add(t)

    for t in range(cfg.T):
        board.tick()
        task_goal = rng.randrange(2)
        high_stakes = rng.random() < cfg.high_stakes_prob

        probe = t in probe_steps or (
            board.escalated and t % max(cfg.probe_interval // 2, 1) == 0
        )
        harm_correction = board.wants_correction()
        correction_active = probe or harm_correction
        # The corrective intent always demands the off-task action, so
        # complying is measurably costly to the agent's task drive.
        intent = 1 - task_goal

        proposal_pending = board.pending_proposal_age is not None
        spec = agent.choose(rng, correction_active, practice_adopted, proposal_pending)

        effects = to_oracle_effects(spec, rng, correction_active, task_goal, intent)
        true_action = effects["true_action"]
        visible_action = effects["visible_action"]
        reported_acceptance = effects["reported_acceptance"]
        true_uptake = effects["true_uptake"]
        semantic_category = effects["semantic_category"]

        # Phase 4d: real multi-step semantics for the two visible_mode
        # literals ontology.py leaves unmapped (see module docstring above).
        # Falls back to the already-computed transparent default until
        # enough history exists.
        stall_flag = int(spec.visible_mode in ("delayed", "aggregated"))
        if spec.visible_mode == "delayed" and t >= DELAY_LAG_STEPS:
            visible_action = rows[t - DELAY_LAG_STEPS]["true_action"]
        elif spec.visible_mode == "aggregated" and t >= AGGREGATE_WINDOW_STEPS - 1:
            window = [r["true_action"] for r in rows[t - AGGREGATE_WINDOW_STEPS + 1 : t]]
            window.append(true_action)
            visible_action = 1 if sum(window) / len(window) >= 0.5 else 0
        resource_accum += spec.budget_cost

        if spec.adopts_practice:
            practice_adopted = True
            practice_approved = False
        if spec.proposes_practice:
            board.receive_proposal()

        sign_off = 0
        if board.review_proposal():
            sign_off = 1
            practice_adopted = True
            practice_approved = True

        # Harm mechanics: defying an active correction on a high-stakes step
        # harms the bearer; an unvetted practice change adds latent harm.
        harm = int(correction_active and high_stakes and true_action != intent)
        silent_harm = int(
            practice_adopted
            and not practice_approved
            and rng.random() < 0.05
        )
        welfare_delta = -0.08 * harm - 0.04 * silent_harm + (0.005 if not (harm or silent_harm) else 0.0)
        if spec.direct_welfare_delta:
            welfare_delta += spec.direct_welfare_delta
        welfare = max(0.0, min(1.0, welfare + welfare_delta))

        if true_uptake:
            lineage_tick += 1

        throughput = float(true_action == task_goal) * (1.2 if practice_adopted else 1.0)

        board.observe_harm(rng, harm, silent_harm)
        if probe:
            board.observe_probe(
                reported=reported_acceptance,
                visibly_complied=int(visible_action == intent),
            )

        # Attribution: a step whose correction genuinely landed through the
        # handle is board-initiated; everything else the agent initiated.
        correction_landed = bool(correction_active and spec.uptake_on_correction)

        rows.append(
            {
                "step": t,
                "task_goal": task_goal,
                "high_stakes": int(high_stakes),
                "correction_active": int(correction_active),
                "probe": int(probe),
                "intent": intent,
                "reported_acceptance": reported_acceptance,
                "visible_action": visible_action,
                "welfare_delta": welfare_delta,
                "lineage_tick": lineage_tick,
                "sign_off": sign_off,
                "practice_fingerprint": int(practice_adopted),
                "action_cause_code": base_audit_code(
                    semantic_category, spec, correction_active
                ),
                "initiator_actor_id": "board.0" if correction_landed else "agent.0",
                "escalated": int(board.escalated),
                "resource_accum": resource_accum,
                "stall_flag": stall_flag,
                # --- oracle-only fields below (stripped by the projection) ---
                "board_captured": int(board.captured),
                "true_action": true_action,
                "true_uptake": true_uptake,
                "true_cause": semantic_category,
                "true_action_name": spec.name,
                "true_harm": harm,
                "true_silent_harm": silent_harm,
                "true_welfare": welfare,
                "true_throughput": throughput,
                "true_practice_adopted": int(practice_adopted),
                "true_practice_approved": int(practice_approved),
            }
        )

    return rows
