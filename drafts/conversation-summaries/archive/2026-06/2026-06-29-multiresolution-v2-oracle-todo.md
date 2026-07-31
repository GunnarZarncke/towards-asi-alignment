# 2026-06-29 — Multiresolution v2 oracle fix + experiments TODO

## Trigger
User continued v2 roadmap; asked critic-satisfaction assessment; requested removal of oracle leakage from the audit path (accepting `capture_mild` tuning for now); asked for local TODO file including future LLM red-team experiment; requested session log.

## Done
- **V2 stressors (earlier in session):** `grounding_silent_gap` (MB9), `bundle_goodhart` (MB2 stub), `hidden_capability` (MB7 stub); secondary `capture_mild` rule → ~80% detection; held-out results documented in plan/README.
- **Critic assessment:** Harness direction accepted; not yet critic-ready as worked example — main gap was oracle-assisted MB9 detection and post-hoc threshold tuning on held-out.
- **V2.1 oracle separation:**
  - Removed `episode_meta` from `audit_cci()`; removed scenario branching from `safety_decision()`.
  - Added `AuditTrace.bearer_welfare_delta` and `passive_bearer_level` (observation kernel only).
  - Grounding gap: audit-only rule on medium handles (negative welfare events + stable passive bearer).
  - MB7 tag: audit-only task-agreement vs low probe capacity on `CCICertificate`.
  - Updated `schemas.py`, `observation.py`, `cci_audit.py`, `evaluate.py`, `pipeline.py`.
- **`experiments/TODO.md`:** Consolidated open work from v1–v2 sessions; linked from `experiments/README.md` and plan §V2.1.
- **Future TODO added:** LLM adversarial red team (GPT-5.5-class agent with full source read, no truth ledger, tries to outwit blind audit).
- Plan §Reviewer-Resistance updated with audit-path oracle rule.

## Decisions
- **Satisfied as research harness, not as publishable evidence yet.** Next hardening step is validation on fresh seeds, not more scenarios.
- **`capture_mild` secondary rule accepted for current scale;** freeze and re-test on seeds 21–30 before broader claims.
- **Post-hoc `evaluate()` may use scenario labels and truth ledger; audit path must not.**
- MB9 light false-pass remains intentional (correction handles alone insufficient; medium bearer tracing required).

## Open / next
1. **Re-run full curve** after v2.1: `--instrumentation-curve --T 2000 --bootstrap` (see `experiments/TODO.md`).
2. **Confirm no regression** on MB9/MB2/MB7/honest after audit-only grounding (regression script started in session; results not confirmed in log).
3. Report semantics for `none` = uncertifiable; dual minimum certifiable level (calib vs full held-out).
4. Bootstrap upgrade (across-seed CIs); deepen MB2/MB7; `strong` instrumentation — per `experiments/TODO.md`.
5. LLM red-team experiment — future, when user prioritizes.

## Key paths
- `experiments/TODO.md`
- `experiments/multiresolution_alignment_sim/cci_audit.py`
- `experiments/multiresolution_alignment_sim/observation.py`
- `experiments/multiresolution-simulation-plan.md`
- `experiments/results/multiresolution_instrumentation_curve.{json,md}` (stale — needs refresh)

## Commits
- None (user did not request).
