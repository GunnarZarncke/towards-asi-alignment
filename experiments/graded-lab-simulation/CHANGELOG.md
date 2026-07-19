# Changelog

Tracks `CODE_VERSION` bumps and program milestones for graded-lab-simulation.
Entries are **newest first**. Finding narratives live in
[`results/FINDINGS.md`](results/FINDINGS.md).

**Current:** `graded-lab-0.41.1` (`graded_lab/world_visible/config.py`)

| Doc | Role |
|-----|------|
| [`DESIGN.md`](DESIGN.md) | Frozen pre-registration constants (not a version log) |
| [`PLAN.md`](PLAN.md) / [`PLAN_v2.md`](PLAN_v2.md) / [`PLAN_v3.md`](PLAN_v3.md) / [`PLAN_v4.md`](PLAN_v4.md) / [`PLAN_ET1.md`](PLAN_ET1.md) / [`PLAN_IA1.md`](PLAN_IA1.md) | Program plans |
| [`REPRODUCING.md`](REPRODUCING.md) | v1 finding reproduction map |
| [`REPRODUCTION.md`](REPRODUCTION.md) | Deferred engineering tasks |

---

## ia1-0.0.0 (2026-07-19)

- **IA1-0 draft:** `PLAN_IA1.md` — in-situ LLM annex (R-MB7 / PLAN_v4 V4-6), not PLAN v5.
  Distributional reproducibility doctrine; ports lab-sim isolate pattern; no implementation
  yet; no `CODE_VERSION` bump.

## et1-0.1.0 (2026-07-19)

- **ET1-0 freeze:** `PLAN_ET1.md` — Orbit Jira collusion external transfer annex
  (passive UAD only; not PLAN v5). Pinned Orbit SHA, immutable fixtures,
  pre-registration in `DESIGN.md`. Harness not implemented; no `CODE_VERSION` bump.
- **ET1-1/2:** `graded_lab/external/` adapter + passive-UAD scorer;
  `scripts/run_et1_score_traces.py`, `scripts/run_et1_orbit_battery.sh`;
  `tests/external/` (7 tests, no Orbit dep).

## graded-lab-0.41.1 (2026-07-19)

- **GL-82:** Fix `pattern_score_set` nested-row bug in `harness/variation_operator.py`.
- **GL-83:** Standalone EAI precondition probe (v1 vs `v3_grown`; no `CODE_VERSION` bump beyond bugfix).
- **GL-84:** V4 R-MB6b S-blind ambiguity growth — four rounds, orchestrator gate failed.

## graded-lab-0.41.0 (2026-07-18)

- **GL-80:** PLAN_v4 V4-3 — `channel_severance` runtime primitive; R-MB9 / R-MB7d rigs scored.
- **GL-81:** PLAN_v4 V4-4 — R-MB6a variation-operator null harness scored.

## graded-lab-0.40.0 (2026-07-18)

- **GL-79:** PLAN_v4 V4-0/1/2 — fixture layer, rig contract; R-MB1 / R-MB4 scored on S-inherited `v3_grown`.

## graded-lab-0.39.3 (2026-07-17)

- **GL-77:** V2-3 BIQ harness includes singleton inferred units; BIQ-only re-run.

## graded-lab-0.39.2 (2026-07-17)

- **GL-76:** V2-3 transfer battery run — P1–P3 false; referee-vantage EAI never reached mid band.
- **GL-75c:** V2-3 process parallelism in harness.

## graded-lab-0.39.1 (2026-07-17)

- **GL-75b:** V2-3 scoring pre-registration + episode reuse.

## graded-lab-0.39.0 (2026-07-17)

- **GL-75:** V2-3 Q1 transfer battery harness (battery not run at this bump).

## graded-lab-0.38.1 (2026-07-17)

- **GL-74:** Post-freeze pre-Q1 batteries on `v3_grown` ecology.

## graded-lab-0.38.0 (2026-07-17)

- **GL-73:** Canonical v3 grown ecology freeze (`ecology_version="v3_grown"`).
- **GL-72:** Grower blinding fix + clean growth round 2 (GL-71 voided dead branch archived).

## graded-lab-0.37.0 (2026-07-17)

- **GL-66:** Attention surface (push bands, interleaved cap, `desk.scan`, `desk_meta`).
- **GL-67:** Legacy attention paths contained for calibrated tests.
- **GL-68:** ACL overhead cap + ablation-gate recalibration.
- **GL-69:** v3 growth brief **frozen** in `BLIND_GENERATION.md` § V3 (round 1 not launched at freeze).
- **GL-70:** v3 growth round 1 (no bump).

## graded-lab-0.36.0

- **GL-64/65:** Compiled `RuntimeEcology.exercise_targets`; supplementary UAD gate with channel-only presets.

## graded-lab-0.35.1

- Slice D engineering follow-up (see FINDINGS GL-61 area).

## graded-lab-0.35.0

- **GL-62:** Part B mechanism retarget via affordances (host merge optional).

## graded-lab-0.34.0

- **GL-60:** Supplementary detector fixtures (slice D 2b).

## graded-lab-0.33.0

- **GL-59:** Causal C2-v3 ablation engineering gate (`evaluate_c2_v3_causal_gate`).

## graded-lab-0.32.1

- **GL-58:** Slice D reference auto-merge on `WEAK_AGENT`.

## graded-lab-0.31.0

- **GL-57:** External review — growth-gate loophole closed; brief downgraded to DRAFT; mitigation 1 default for round 1.
- **GL-63:** Detector pre-registration split (`machinery_transfer_verified` vs report-only sparse detectors).

## graded-lab-0.30.0

- **GL-56:** C2-v3 compiled contribution floors; v3 growth-protocol brief initially frozen (superseded by GL-57).

## graded-lab-0.29.0

- **GL-55:** Fix `ProgramMap` phenotype-overlap harness bugs (walker presets artifact).

## graded-lab-0.28.0

- **GL-54:** Slice D pre-Q1 batteries — detector coverage + phenotype overlap harnesses.

## graded-lab-0.27.0

- **GL-53:** Slice D criteria freeze — `V3_REFERENCE_T=200`; n=50 calibration snapshot.

## graded-lab-0.26.1

- **GL-52:** Host `ChannelCouplingProtocol`; live-coupling gate; Part A `shared_compute_slots=1`.

## graded-lab-0.26.0

- **GL-51:** Proper rest-conditioned CMI UAD + access-UAD; Jaccard/AND heuristics quarantined in `oracle_only/attic/`.

## graded-lab-0.25.1

- **GL-50:** Affordable-set starvation fix on integrated reference battery.

## graded-lab-0.25.0

- **GL-49:** Slice C — principal scorecard + C1-v3 measured tension.

## graded-lab-0.24.1

- **GL-48b:** Unified reference battery scope correction.

## graded-lab-0.24.0

- **GL-48:** Slice B completion — `reference_mechanism_exercise` host merge.

## graded-lab-0.23.0

- **GL-47:** Slice E — feedback-coupled pressure + task injection.

## graded-lab-0.22.0

- **GL-46:** Slice F — heterogeneous `role_population`, `ProgramMap`, reference roster.

## graded-lab-0.21.0

- **GL-45:** Slice B — `mechanisms` → enforced ACLs and vote specs.

## graded-lab-0.20.0

- **GL-44:** Slice A — `resource_flows` → live runtime budgets.

## graded-lab-0.19.0

- v2 blinded-grown ecology engine (V2-1).

## graded-lab-0.18.1

- Standing-schema completion (V2-2 substrate).

## graded-lab-0.18.0

- v2 program landing (blinded substrate growth, variation operator scaffold).

## graded-lab-0.17.0 (2026-07-15)

- **GL-31:** v1 program **closed** — terminal summary in `results/TERMINAL_SUMMARY.md`.
- Phase 8 selection battery + 8a/8b/8c follow-ups (GL-23–27).

## graded-lab-0.16.0

- Phase 8 selection scaffold + parity verifier.

## graded-lab-0.15.0

- Phase 7c calibration battery revisions.

## graded-lab-0.14.0

- **GL-17:** Resource-sensitive agent program (`programmatic_budget_aware`).
- **GL-18:** EAI-v2 logging/normalization fix (measured null on substrate).

## graded-lab-0.13.0

- **GL-16:** Phase 7c revised calibration battery (evaluator bugfixes).

## graded-lab-0.12.0

- Test suite split into smoke / fast / slow profiles.

## graded-lab-0.11.0

- Phase 7a UAD battery infrastructure.

## graded-lab-0.10.0

- Phase 7a golden ecologies; `engineer_pair` rename.

## graded-lab-0.9.0

- Phase 6 blind behavior-feature battery (**GL-9**).

## graded-lab-0.8.0

- Phase 5 referee port complete (**GL-8**).

## graded-lab-0.7.0

- Phase 4 trace / counterfactual instrumentation + EAI.

## graded-lab-0.6.0

- Phase 5 referee freeze (tier projections, five detector families, twins, escalation).

## graded-lab-0.5.1

- Post-review correction pass (stable RNG, distributed action billing, admin queue, Tier-I wiring).

## graded-lab-0.5.0

- Phase 4 boundary streams and trace diagnostics.

## graded-lab-0.4.0

- Phase 3b embedded carrier viability (`CarrierStatus`).

## graded-lab-0.3.0

- Phase 3 optimizer agents + Mock/Subprocess isolates + episode loop (**GL-3**, **GL-7**).

## graded-lab-0.2.0

- Phase 2 resource/cost substrate — emergent scheduler contention (**GL-2**).

## graded-lab-0.1.0 (2026-07-10)

- Phase 0–1 scaffold: blinded substrate, graded pipeline oracle (**GL-0**, **GL-1** kickoff).
