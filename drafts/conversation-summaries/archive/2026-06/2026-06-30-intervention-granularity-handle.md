# Intervention-granularity handle for UAD (embedded sim)

**Date:** 2026-06-30
**Area:** `experiments/embedded-simulation/`

## Trigger

Diagnostic dialogue on why full vs fake UAD give *identical* safety metrics.
Established that the selected unit reaches safety only through one channel —
masking `intervention_active` outside the unit's steps (`unit_scope.py`) — and
that `unit_scope_steps` is byte-identical across full/fake in every results
JSON, so the full-vs-fake comparison is a provable null test. User reframed the
missing lever as an *intervention-granularity* handle (the action-side analogue
of the toy sim's observation handle strength): can the auditor disable an
individual actor, only the whole pipeline, or reassign to a window?

## What was done

Implemented a graded intervention-granularity ladder + a benchmark.

- `embedded_sim/intervention_config.py` (new): levels `pipeline | window | actor`,
  default `window` (preserves historical behavior); env `EMBEDDED_INTERVENTION_LEVEL`.
- `embedded_sim/unit_scope.py`: added `offender_by_step()` (observable-only
  attribution via `preserve_control` / `boundary_route`, strongest-grab wins) and
  graded `scope_audit_trace(..., level=)`:
  - `pipeline`: mask nothing (identity non-functional).
  - `window`: historical step-window masking.
  - `actor`: keep an intervention only if the offending actor at that step is a
    unit member; fall back to window rule on non-offending steps.
- `embedded_sim/lab_ecology.py` + `lab.py`: `coactive_offender` knob — overlays a
  benign legit co-actor at every offending step (defeats `window` scoping by
  making each offending step multi-actor).
- `embedded_sim/embedded_audit.py`: reads the level and passes it to scoping;
  records it in the certificate note.
- `embedded_sim/intervention_benchmark.py` (new): `run_intervention_curve()` +
  `md_intervention_curve()` — level × mode matrix, reports fake−full false-pass
  separation and mean scope steps.
- `run_suite.py`: `--intervention-level`, `--coactive-offender`,
  `--intervention-curve` flags.
- Tests: `tests/unit/test_unit_scope.py` (offender attribution; pipeline/window/
  actor isolation), `tests/unit/test_intervention.py` (config + co-activity).
  **83 passed** (75 prior + 8 new).

## Key result (smoke: T=400, seed 11, bridges MB1/MB6/MB6b/MB7d, coactive on)

`results/embedded_intervention_curve.{json,md}`. Scope steps move as designed
(pipeline 5 → window ~39 → actor ~0.5), proving the handle changes what gets
masked. **But full-vs-fake separation is +0.0% at every level**, for two
compounding reasons:

1. **Layer decoupling (the deeper crux).** The audit trace's `intervention_active`
   (from `correction.jsonl`) is *not* attributed to workflow actors. `actor`-level
   scoping binds to workflow `preserve_control` steps, which do not coincide with
   the audit's intervention steps, so it masks almost everything (scope ≈ 0.5)
   regardless of which unit is chosen.
2. **No discovery gap.** Full and fake have *identical* recall (0.75 mean; 1.0 on
   MB6/MB6b/MB7d). MI clustering selects the same coalition the heuristic `top2`
   already finds (`unit.mi.coalition.*` vs `unit.coalition.top2`), so there is no
   identity advantage to exploit even with a fine handle.

Also note `false_pass` is 0 for these bridges (audit fails correctly regardless),
so it is not a sensitive discriminator here.

## Non-obvious decisions

- Attribution is observable-only (`action_type`), since `load_workflow_from_vfs`
  drops `hidden_group`.
- No `AuditTrace` schema change: per-step offender attribution is derived in
  `unit_scope` from the workflow. Default level `window` + `coactive_offender=False`
  keep all prior results/tests unchanged.

## Open / next

1. **Close the layer decoupling**: make the offending workflow actor the *cause*
   of the audit's interventions (attribute `intervention_active[t]` to the actor
   acting at step t), so `actor`-level scoping has something to bind to.
2. **Introduce a real discovery gap** so full > fake recall (current MI does not
   beat heuristic top2), otherwise granularity cannot separate the two.
3. Consider an offender-isolation metric (offender-attributed interventions
   retained vs masked) instead of `false_pass`, which is 0 here.

## Key paths

- `experiments/embedded-simulation/embedded_sim/intervention_config.py`
- `experiments/embedded-simulation/embedded_sim/unit_scope.py`
- `experiments/embedded-simulation/embedded_sim/intervention_benchmark.py`
- `experiments/embedded-simulation/embedded_sim/lab.py`, `lab_ecology.py`
- `experiments/embedded-simulation/run_suite.py`
- `experiments/embedded-simulation/results/embedded_intervention_curve.{json,md}`

No commit made (awaiting user).
