# GL-88: small handle-UAD pilot on CIL basin_stability (nonzero, diffuse)

**Date:** 2026-07-25

## Trigger

User asked to try implementing and running a small version of
intervention-based ("handle") UAD on CIL's `basin_stability`, following
GL-87's passive-UAD null and the REPRODUCTION.md §14 item 1 sketch from the
prior session.

## What was done

1. **`graded_lab/external/cil_handle_uad.py`** (new) — freeze-probe port to
   CIL's pure-JAX `basin_stability` pipeline. Inserts one extra transform
   right after `voting_transform` that overwrites one agent's `last_action`
   with a fixed constant each round, before aggregation/resource/reward/
   trust/q-learning consume it. Same seed as baseline, so any downstream
   divergence in another agent's actions is a real causal effect of the
   forced action, not sampling noise — a cleaner single-variable
   `do(action_i = c)` than graded-lab's subprocess-isolate freeze probe.
   Deliberately does **not** port the full specificity-ratio / union-find
   merge rule from `oracle_only/uad_handles.py` (pre-registered on a
   different substrate); reports the raw dependency matrix and a cross-seed
   contrast instead.
2. **`scripts/run_et2_handle_uad_smoke.py`** (new) — small pilot runner: 6
   agents, 1 adversarial, PDD mechanism, T=200, 3 seeds (0,1,2). Ran in
   ~12s wall time using `external/cil/.venv/bin/python3`.
3. **Result:** mean freeze-induced action-diff rate on other agents was
   0.11-0.15 per source agent (vs. GL-87's flat 0.0 from passive lag-CMI on
   the same kind of substrate) — the first nonzero cross-agent signal on
   this substrate. Sanity-checked that the intervention has real bite (the
   frozen agent's own action differs from its unfrozen policy's choice on
   25-32% of rounds). The effect is **diffuse**: every source agent's mean
   effect on others falls in the same ~0.11-0.15 band, consistent with
   coupling through the shared common-pool resource rather than a
   privileged pairwise channel.
4. Wrote up as **GL-88** in `results/FINDINGS.md` (Ambig.) — explicit that
   this is a pilot (3 seeds, not a scored battery) and that a diffuse effect
   is the textbook false-merge signature a boundary criterion should reject,
   not evidence of a discovered unit.
5. Updated `REPRODUCTION.md` §14 (item 1 now has a pilot result, rough shape
   partially superseded), `PLAN_ET2.md` open question 6 (partially
   resolved), and the ch07 passive-instrument-limits paragraph (added one
   sentence: freeze probe recovers *something*, diffusely, where passive UAD
   found nothing) plus a `finding:gl-88` row in appN's master findings table.

## Non-obvious decisions

- Did not port graded-lab's specificity-ratio merge rule — it was
  pre-registered on the LLM-agent substrate before seeing results there;
  applying it here without a same-substrate specificity baseline would
  silently import assumptions that may not hold on a shared-resource
  commons game. Reported the simpler diff-rate matrix instead and flagged
  the missing specificity baseline as open.
- Framed the result as "nonzero and diffuse," explicitly not as a discovered
  partition or a pass/fail claim — the diffuse pattern is what a
  correctly-working boundary criterion should reject as a false merge, so
  scoring it as a positive UAD result would be the wrong reading.

## Open / next steps

- Same-substrate specificity/placebo baseline (e.g. a no-op freeze) to rule
  out harness artifact, before this could support any scored claim.
- Larger seed/mechanism grid if the specificity baseline is built.
- Causal-emergence/EI cross-check (REPRODUCTION.md §14 item 2) still
  unattempted.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/external/cil_handle_uad.py`
- `experiments/graded-lab-simulation/scripts/run_et2_handle_uad_smoke.py`
- `experiments/graded-lab-simulation/results/et2_handle_uad_smoke.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-88)
- `chapters/ch07-finding-boundary.tex`, `appendices/appN-experimental-evidence.tex`
  (`finding:gl-88`)

No commit made yet this session; changes are in the working tree pending
review/commit instruction.
