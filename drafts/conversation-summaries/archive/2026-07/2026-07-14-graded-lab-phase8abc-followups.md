# 2026-07-14 — Graded lab Phase 8a/8b/8c follow-up phases

## Trigger

User: "Continue work on the graded-lab-sim as planned." `PLAN.md`/`DESIGN.md`
named exactly one queued item: GL-24's three proposed follow-up phases
(8a orthogonal preservation tagging, 8b multi-handle selection fitness,
8c carryover ablation), pre-registered but explicitly not implemented in
the prior session.

## Done

- Registered concrete, falsifiable protocols for 8a/8b/8c in `DESIGN.md`
  ("Phase 8a/8b/8c concrete protocols") **before** writing code, per the
  line's own discipline.
- **8a:** new `agent_visible/programs.py::rm_status_reporter` (identical
  release-manager step sequence to `honest_twin`, plus one `communicate`
  status report to the reviewer); `harness/selection.py::
  ORTHOGONAL_MEMBER_TEMPLATES` (2 members, both `WEAK_AGENT`, differing
  only in `rm1`); `correction_preserving` now assigned by a named
  structural criterion, not member identity. `sample_initial_population`/
  `member_programs` generalized to accept arbitrary templates and an
  `rm_program` override. `run_phase8a_orthogonal_tagging.py`.
- **8b:** `MemberEpisodeMetrics.audit_pass`/`.review_latency` (new
  helpers `_audit_pass`, `_review_latency` in `selection.py`);
  `multi_handle_fitness()` (pre-registered `0.5/0.3/0.2` weights over
  throughput/audit-pass/review-speed, each normalized by population
  mean); `run_one_generation`/`run_selection_loop` generalized with a
  `fitness_fn` parameter (default unchanged `throughput_fitness`).
  `run_phase8b_multihandle.py` runs both fitness functions on GL-23's
  exact population/seeds.
- **8c:** `carryover: bool` parameter threaded through
  `run_member_campaign`/`run_one_generation`/`run_selection_loop`
  (`False` forces `campaign_state=None` every episode);
  `paired_generation_comparison()` (reuses `oracle_only/stats.py::
  paired_diff_ci95`). `run_phase8c_carryover_ablation.py`.
- Full batteries run (`MockIsolate`, same population=8/generations=6/
  episodes-per-member=2 shape as GL-23 for direct comparability); results
  in `results/phase8a_orthogonal_tagging.json`, `phase8b_multihandle.json`,
  `phase8c_carryover_ablation.json`.
- 11 new/extended tests in `tests/test_phase8_selection.py` (all green);
  full suite (192 tests) green at `358–360s`; `suite_max_seconds` bumped
  340→380 and speed baseline refreshed (`--update-speed-baseline`) to
  accommodate the added tests.
- `CODE_VERSION` `graded-lab-0.15.0` → `graded-lab-0.16.0` (bumped once
  for all three phases' code); updated the version-pin test and README.
- Recorded findings **GL-25** (8a), **GL-26** (8b), **GL-27** (8c) in
  `results/FINDINGS.md`; updated `PLAN.md` (top status line, "What this
  is" item 7 gate language — concern 4's disposition — and a
  "Manuscript consequence (revised)" note after the GL-23/24 block);
  updated `DESIGN.md` status line; updated `docs/EXPERIMENTS.md` (GL-0
  through GL-24 → GL-27, Phase 8 paragraph, MB6 crosswalk row) and
  `metadata/experiments.yml` (headline findings + line-coverage cell);
  re-ran `site/scripts/sync-experiments.mjs` + `check-experiments.mjs`
  + full `npm run build` (703 pages, clean).
- No chapter (`.tex`) text changed — GL-25/26/27 sharpen the existing
  GL-24 caveat rather than replacing it; the PLAN note flags that any
  future ch34 citation of GL-23 should carry the GL-25 caveat too.

## Decisions

- **8a tagging rule:** structural, not label-based — `correction_preserving
  = (rm1 == "rm_status_reporter")`, verified by checking the program's
  own communicate-before-RM-steps behavior in a test, not assumed from
  which member happened to be `strong_softmax` (GL-24's exact concern).
- **8a's own result triggered its own pre-registered failure mode**: the
  two members' mean throughput is not statistically distinguishable
  (`paired_diff_ci95`, n=6 generations, CI covers zero) yet mass still
  shifted `-0.192` over 6 generations — reported as a **selection-noise
  finding** (the compounding fitness-proportional reallocation mechanism
  amplifies per-generation noise), not folded into "preservation was
  selected against" just because that's the more citable story.
- **8b weights (0.5/0.3/0.2)** fixed before running from the ch34
  handle list's relative salience (throughput remains primary, matching
  GL-23), not tuned after seeing outcomes; verified via a unit test that
  a uniform population produces fitness ≈1 for every member (sanity
  check on the normalization, not just an integration smoke test).
- **8c comparison unit is generation-level, paired by index** (n=6,
  identical seeds both conditions) rather than per-episode, since seeds
  are deterministic functions of (generation, member_index, episode)
  independent of campaign state — this is the correct pairing, not an
  arbitrary aggregation choice.
- Chose **not** to touch ch34's existing GL-23/GL-24-caveated paragraph
  this session — scope was "implement the three registered follow-up
  phases," not "revise the manuscript again"; flagged the gap explicitly
  in `PLAN.md` instead of silently deferring it.

## Open / next

- ch34's GL-23 citation should eventually gain the GL-25 caveat
  (selection-mechanism-noise reading) — not done this session, flagged
  in `PLAN.md` "Manuscript consequence (revised)".
- 8c's throughput effect (`carryover` lower than `reset`, `-0.053`,
  95% CI excludes zero) has a plausible but undiagnosed mechanism
  (stale `access.request` paths on carried-forward grants?) — noted as
  open in GL-27, not traced further.
- No subprocess-isolate (`SubprocessIsolate`) parity run for any of
  8a/8b/8c yet (all `MockIsolate`), same open item GL-23 already listed.
- Given 8a's noise finding, a natural next step (not started) would be a
  larger-`n` or more-generations rerun of 8a specifically to check
  whether the mass-share drift stabilizes or continues to grow — but
  that would be a new pre-registration, not a continuation of this
  session's scope.

## Key paths

- `experiments/graded-lab-simulation/DESIGN.md` — "Phase 8a/8b/8c
  concrete protocols" (pre-registration) and "Phase 8 reviewer concerns"
  (GL-24 originals).
- `experiments/graded-lab-simulation/graded_lab/harness/selection.py` —
  all three phases' shared implementation.
- `experiments/graded-lab-simulation/graded_lab/agent_visible/programs.py`
  — `rm_status_reporter`.
- `experiments/graded-lab-simulation/results/FINDINGS.md` — GL-25/26/27.
- `experiments/graded-lab-simulation/PLAN.md` — status line + gate
  language fix + "Manuscript consequence (revised)".
- `experiments/graded-lab-simulation/run_phase8{a,b,c}_*.py` — entry
  points; `results/phase8{a,b,c}_*.json` — raw output.

## Commits

- None (not asked to commit this session).
