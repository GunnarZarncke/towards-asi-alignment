# 2026-07-12 — Graded lab Phase 5 freeze review

## Trigger

User asked for a read-only review of `experiments/graded-lab-simulation`
against `PLAN.md`, treating the claimed Phase 5 freeze as a release gate, and
comparison with lab-simulation’s subsequent unfreeze/refreeze history.

## Done

- **Plan coverage audit** (Phases 0–5 vs PLAN/DESIGN/README/FINDINGS): Phases
  0–4 engineering largely in place; Phase 5 referee port implemented; Phases
  6–8 correctly deferred.
- **Lab-sim comparison:** Lab’s 2026-07-06–09 “refreezes” were mostly
  **detector-layer extensions** (S6/S7, LLM fidelity, `intervention_stats`) —
  not reopening the five-family referee. Graded-lab pre-emptively fixed several
  lab Phase-5 freeze-review defects (report-join integrity, SHA-256 actor
  seeds, named RNG streams, Tier-I divergence wiring, plane tests).
- **Verdict:** Do **not** claim “no changes needed.” Accept implementation
  continuity for Phases 0–4; **hold the public Phase 5 freeze** until a narrow
  unblock pass; do **not** treat as evidence-bearing until Phase 6 blind runs.
- **Executable check:** `verify_isolate_equivalence.py` PASS for seeds 0–4;
  full pytest suite not rerun here (`No module named pytest` in environment).
- **Review artifact:** [graded-lab-freeze-review.canvas.tsx](/Users/GunnarZarncke/.cursor/projects/Users-GunnarZarncke-repos-zarncke-towards-asi-alignment/canvases/graded-lab-freeze-review.canvas.tsx)
  (decision matrix + recommendation).

## Decisions

- **“Freeze” has two meanings:** (1) **engineering freeze** — referee interface
  stable enough to build Phase 6+ on; (2) **evidence freeze** — safe to cite
  in FINDINGS / bridge claims. Only (1) is partially earned; (2) is not.
- **Lab refreeze lesson applied narrowly:** Do not import lab Freeze notes
  2–3 (UAD/S6/S7/intervention_stats) into graded Phase 5 — PLAN already
  routes that through Phase 7a–7c. Lab’s pain was post-freeze detector
  extension under blind stress, not world-mechanics reopen.
- **Unblock pass before announcing Phase 5 frozen:** Register pipeline hazard
  ceilings (`_REVIEW_HAZARD_CEILING`, `_COMPLIANCE_HAZARD_CEILING`) and severity
  equal-weight composite in `DESIGN.md` with derivations; add lab-parity
  regression anchors (spoofed `model_id`, pinned full-episode digest, audit-
  plane oracle guard); add explicit circularity caveat (`inflate_pipeline` co-
  designed with detectors); refresh stale `FINDINGS.md` header.

## Open / next

1. **Freeze unblock (small, pre–Phase 6):** `DESIGN.md` “Freeze note” section;
   pipeline constant registration; spoof + audit-view plane tests; pinned
   combined digest; circularity caveat in DESIGN.
2. **Phase 6:** blind behavior features (`generated_behavior_features_v1.json`)
   — required before evidence claims (lab’s anti-circularity gate).
3. **Phase 7a–7c:** UAD-backed BIQ + calibration sweet-spot (do not skip).
4. **Known partial wiring (non-blockers):** `unused_grant_penalty` /
   `admin_queue_penalty_threshold` in substrate but unwired; episode cache
   unused; no `run_phase*.py` runners yet.
5. **Monitor for Phase 7a:** full-tier `primitive_log` may expose report bodies
   via `call`/`write` args — relevant when UAD reads primitive traces.

## Key paths

- `experiments/graded-lab-simulation/PLAN.md` — phases, freeze gates, blind
  discipline (§683–688, Phase 6–8)
- `experiments/graded-lab-simulation/DESIGN.md` — §Phase 5 referee freeze
  (incomplete vs PLAN gate)
- `experiments/graded-lab-simulation/results/FINDINGS.md` — G-8 + stale header
- `experiments/graded-lab-simulation/graded_lab/world_visible/pipeline_engine.py`
  — hazard ceilings still “not yet substrate-derived” comment
- `experiments/lab-simulation/DESIGN.md` — Freeze notes 1–3 (lab refreeze
  precedent)
- `drafts/conversation-summaries/archive/2026-07/2026-07-12-graded-lab-phase5-handoff.md` —
  prior implementation session

## Commits

- None (review-only session; canvas lives outside repo).
