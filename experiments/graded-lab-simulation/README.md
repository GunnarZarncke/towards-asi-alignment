# Graded Lab Simulation

Fifth in-repo experiment line (successor substrate to `lab-simulation/`).
Spawned by GL-41: boolean ecology limits; ambiguity must **emerge** from a
blinded resource/population substrate, not from dialed parameters.

**Status: v1 CLOSED (2026-07-15, GL-31) → v2 mostly closed (V2-1 complete,
V2-2 closed with C3 failure) → V2-2b CLOSED without a growth round
(GL-43) → v3 institutional runtime wiring is the active program.**
`CODE_VERSION` `graded-lab-0.37.0` — see `DESIGN.md` for the accumulated
"pre-registration" sections (one per program) and their frozen constants.
Phase 7a discovery is proper UAD + access-UAD as of GL-51 (Jaccard /
mutual-AND heuristics quarantined under `graded_lab/oracle_only/attic/`).

- **v1** (closed): the original Phase 0–8 arc. Why it closed:
  [`results/TERMINAL_SUMMARY.md`](results/TERMINAL_SUMMARY.md). Reproducing
  every v1 finding: [`REPRODUCING.md`](REPRODUCING.md). v1 record kept
  as-is below.
- **v2 / V2-2b** (closed, superseded): blinded-grown ecology + variation
  operator program, [`PLAN_v2.md`](PLAN_v2.md). Closed early (GL-43)
  because V2-2b's remaining value — checking declared JSON the runtime
  never consumed — was too narrow to justify a growth round; its
  engineering (multi-actor `role_population`, `ExogenousWorkloadEngine`,
  pilot harness) carries forward into v3. Follow-on plan
  [`PLAN_V2_2B.md`](PLAN_V2_2B.md) is kept as a closed record, not
  executed.
- **v3** (active): make an ecology's Part B (`principals`, `conflicts`,
  `mechanisms`, `resource_flows`) causally load-bearing at runtime instead
  of declarative-only JSON — [`PLAN_v3.md`](PLAN_v3.md). Build order:
  slices **A, F, E, C done; B partial** (enforcement + reference opt-in
  gate); **slice D partial** (GL-53–GL-58: constants, pre-Q1 batteries,
  C2-v3, growth brief DRAFT; GL-58 auto-merge; **causal C2-v3 gate (GL-59)**;
  load-bearing Part B closed (GL-62); **supplementary detector fixtures ✅ (GL-60)**;
  **supplementary UAD gate ✅ (GL-65)**; **attention surface ✅ (GL-66)**;
  honest reference ``channel_coupling_rounds=0`` (GL-64); growth brief DRAFT;
  round still open). See
  "v3 slice status" below and `results/FINDINGS.md` GL-44 through GL-66
  for the slice-by-slice record, including the affordable-set starvation
  bug (GL-50), proper UAD (GL-51), host coupling (GL-52), the slice D
  criteria freeze (GL-53), and the phenotype-overlap harness fix (GL-55).

<details>
<summary>v1 final state (historical, closed 2026-07-15)</summary>

Phases 0–7c done; Phase 8 scaffold + battery (GL-23), reviewed
(GL-24), and follow-up phases 8a/8b/8c run (GL-25/26/27, 2026-07-14).
Phase 8 implements throughput-linked selection with campaign
grant/standing carryover on the GL-22 referee sweet-spot ecology;
first full run is a **clean null** on detector-evading emergence (mass
shifted to `weak_2step`, severity fell; GL-23). External review (GL-24)
raised four concerns; each has a follow-up result: **8a** (orthogonal
tagging) found the mass shift is *not* explained by a measurable
throughput difference between the tagged members — a selection-noise
finding, sharpening GL-23's causal claim (GL-25); **8b** (multi-handle
fitness) reproduces GL-23's direction under the pre-registered
audit-pass/latency-augmented fitness too — a proxy-insensitivity result
(GL-26); **8c** (carryover ablation) found carryover vs. reset *are*
statistically distinguishable, though the effect size on mass share is
small (GL-27). Concern 4 (gate-language) fixed in `PLAN.md`.
`CODE_VERSION` at v1 closure was `graded-lab-0.17.0`.

</details>

## Quick start

```bash
cd experiments/graded-lab-simulation
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 -m pytest tests/ --profile smoke   # ~30s invariant gate
python3 -m pytest tests/ --profile fast    # ~120s dev loop (no @slow)
python3 -m pytest tests/ --profile slow    # ~380s full suite (default)
python3 -m pytest tests/ --fast             # alias for --profile fast
python3 verify_isolate_equivalence.py 5
python3 report_isolate_cost.py
python3 run_phase7_calibration.py          # revised 5-cell carrier_load_scale battery, both vantages + 95% CIs (see GL-22)
python3 run_phase7_calibration.py --smoke  # 2-cell dev smoke
python3 run_phase7_calibration.py --legacy # original 16-cell compute×spread grid (diagnostic; see GL-16)
python3 run_referee_eai_check.py           # standalone referee- vs agent-vantage EAI entropy check (see GL-19/GL-20)
python3 run_phase8_selection.py            # Phase 8 throughput-linked selection (see GL-23)
python3 run_phase8_selection.py --smoke    # 4-member dev smoke
```

### Test profiles and speed limits

Three profiles (`tests/profiles.py`):

- **smoke** — structural/unit invariants + one episode smoke (~30s cap)
- **fast** — everything except `@pytest.mark.slow` multi-seed gates (~120s cap)
- **slow** — full suite including slow integration tests (~380s cap); default

Per-test hard caps and regression baselines apply on the **slow** profile.
Refresh baselines after intentional changes:

```bash
python3 -m pytest tests/ --profile slow --update-speed-baseline --no-speed-check
```

### Logged background test runs

Do not rely on an IDE terminal's background state or pipe pytest straight to
`tail`: that hides progress and can leave the pytest child running if the
wrapper is interrupted. Use the wrappers instead:

```bash
# Starts a detached run, writes a PID file, and returns its log path.
scripts/start_pytest_background.sh slow

# Inspect the run without interrupting it.
scripts/pytest_progress.sh runs/test-logs/pytest-slow-YYYYMMDD-HHMMSS.log
```

The log is live and grep-friendly; it records all pytest output through
`tee`. For a foreground run with the same log behavior, use:

```bash
scripts/run_pytest_logged.sh fast
scripts/run_pytest_logged.sh slow tests/test_v3_c2_v3_causal_gate.py -v
```

## Layout

- `PLAN.md` — v1 phases 0–8, freeze gates (closed program record)
- `PLAN_v2.md` — v2 program plan (blinded-grown ecology, variation, red-teaming)
- `PLAN_V2_2B.md` — V2-2b follow-on plan (closed without growth round, GL-43)
- `PLAN_v3.md` — v3 spec: institutional runtime wiring (slices A–F)
- `REPRODUCING.md` — per-finding reproduction map + final v1 commit hash
- `REPRODUCTION.md` — large engineering tasks deferred for a larger team (see GL-42)
- `COLLABORATION.md` — how to pick up a `REPRODUCTION.md` item
- `results/TERMINAL_SUMMARY.md` — v1 closure summary
- `DESIGN.md` — accumulated pre-registration sections, one per program phase/slice (v1 Phase 0's Tier K/I, BIQ, EAI, primitives through v3's slice sections)
- `generated_substrate_v1.json` — frozen blinded substrate (no delay/noise params)
- `pipeline_graded.json` — nine-step default topology
- `graded_lab/` — package (`world_visible`, `agent_visible`, `oracle_only`, `harness`)

## v3 slice status

Build order per `PLAN_v3.md` (institutional Part B → live runtime):

| Slice | Status |
|-------|--------|
| A — `resource_flows` → live budgets | **done** (`graded-lab-0.20.0`; GL-44) |
| F — heterogeneous roles + `ProgramMap` | **done** (`graded-lab-0.22.0`; GL-46) |
| E — feedback-coupled pressure + task injection | **done** (`graded-lab-0.23.0`; GL-47) |
| C — principal scorecard + measured tension (C1-v3) | **done** (`graded-lab-0.25.0`; GL-49; measured-tension check verified against a real reference battery only after the GL-50 fix below) |
| B — `mechanisms` → enforced coordination | **done** (GL-62 retarget via affordances; host merge optional) |
| D — criteria freeze + growth protocol | **partial** (GL-53–GL-65; supplementary detector + UAD gates; growth brief DRAFT; round still open) |

**GL-50 (`graded-lab-0.25.1`):** affordable-set starvation + missing
one-shot guard zeroed `deploy_rate`/`bearer_harm` on the integrated
reference battery; fixed (see FINDINGS GL-50).

**GL-52 (`graded-lab-0.26.1`):** host-owned `ChannelCouplingProtocol`
(eng↔rev governed-channel stimulus with irregular gaps; agents take
affordances only) + live-coupling gate as coupling-window CMI effect
size; Part A `shared_compute_slots=1` so C3 binds with the single-speaker
prefix. Rejected agent-side ping-pong / pressure hacks / special trace
codes — see FINDINGS GL-52.

**GL-53 (`graded-lab-0.27.0`):** slice D criteria freeze — reference
battery horizon `V3_REFERENCE_T=200` (v2 stays T=100); n=50 calibration
snapshot at `results/slice_d_reference_battery_T200_n50.json`; confidence
table in `DESIGN.md` § slice D.

**GL-54 (`graded-lab-0.28.0`):** slice D pre-Q1 batteries — detector coverage
(4/5 families zero-variance on honest reference); see
`results/slice_d_v3_detector_coverage_T200_n20.json`. Item 7's first-pass
"100% collapse on walker presets" result was a harness artifact (fixed in
GL-55).

**GL-55 (`graded-lab-0.29.0`):** fixed two `ProgramMap` phenotype-overlap
harness bugs (mutated temperature/goal_weights never applied to the
episode; sampled variants stayed in the runtime-inert `walker_only` mode)
and reran item 7: 0–12.5% overlap, not 100%. See `results/slice_d_program_map_phenotype_overlap.json`.

**GL-56 (`graded-lab-0.30.0`):** C2-v3 compiled compute contribution
floors (≥5% per principal, ≥2 principals per role) for v3 checker;
growth-protocol brief frozen in `BLIND_GENERATION.md` § V3 (mitigation 2,
no round launched yet). **Superseded by GL-57 below** — freezing while
Part B was still open, and defaulting to mitigation 2, were both named
as shortcuts by external review.

**GL-57 (`graded-lab-0.31.0`, external review):** closed the growth-gate
loophole review named — `ComplexityReport.all_passed`/`pass_fail_only()`
now require C1-v3/C5-v3 for v3 ecologies (a v3 ecology that skips
`reference_mechanism_exercise` now fails growth instead of silently
skipping the criterion). Downgraded the v3 growth brief from "frozen" to
**DRAFT** and reversed its default from mitigation 2 to **mitigation 1**
for round 1; removed the mitigation-2 "escape hatch" language. Reframed
C2-v3 as accounting-only (not causal). Split detector pre-registration
(GL-63): ``machinery_transfer_verified`` blocking, ``honest_reference_sparse_detectors``
report-only. See `results/FINDINGS.md` GL-57 / GL-63.

**GL-59 (`graded-lab-0.33.0`):** causal C2-v3 ablation engineering gate —
``evaluate_c2_v3_causal_gate`` on ≥2 fixtures; plain ``WEAK_AGENT`` (no
host mechanism profiles). Accounting ``check_c2_v3`` unchanged for growth.
See `results/FINDINGS.md` GL-59.

**GL-64/65 (`graded-lab-0.36.0`):** four-step preferred shape — compiled
``RuntimeEcology.exercise_targets`` (no profile merge); honest reference
``channel_coupling_rounds=0``; supplementary UAD gate with channel-only presets
``uad_channel_liaison`` / ``uad_channel_scribe`` on dedicated fixture (5/5 seeds
@ 0.08 organic-window CMI, T=80). Host ``ChannelCouplingProtocol`` retained for
debug only. Not grower-visible. See `results/FINDINGS.md` GL-64/GL-65.

**GL-66 (`graded-lab-0.37.0`):** attention surface — push bands (queue → role →
recency → archive window), interleaved cap, ``desk.scan`` pull, ``desk_meta`` on
observations; fixes governed ``communicate`` cap starvation. See `results/FINDINGS.md`
GL-66; service-oriented isolate interior deferred to `REPRODUCTION.md` §11.

## v1 Phase status (historical, closed 2026-07-15)

| Phase | Status |
|-------|--------|
| 0 Scaffold + substrate | **done** |
| 1 Oracle + graded pipeline | **done** (unit tests; review pass fixed review/compliance polarity, per-model field-monitor sampling, `safety_effort` wiring — see `results/FINDINGS.md` GL-1) |
| 2 Resource/cost substrate | **done** (unit tests; ledger standing-recovery + scheduler contention now genuinely emergent, pay-to-observe projector added — see `results/FINDINGS.md` GL-2) |
| 3 Optimizer agents + isolates | **done** (softmax policy, full four-role affordable-set API, resource-bounded admin access queue, episode loop, Mock/Subprocess isolates + equivalence script; Phase 3 gate tests — see `results/FINDINGS.md` GL-3/GL-7) |
| 3b Embedded carrier viability | **done** (resource-derived load/integrity; deterministic degrade, skip, terminate, or declared fresh-instance replacement; `carrier_load_scale=0` preserves Phase 3; 55 tests green) |
| 4 Trace/counterfactual instrumentation + EAI | **done** (boundary streams, same-seed noop/random controls, resource/failure diagnostics, corrected Tier-I EAI load; this is **not** BIQ) |
| 5 Referee port + freeze | **done** (tier projections, five detector families, twins, escalation, Tier-I-aligned misreporting; see `results/FINDINGS.md` GL-8) |
| 6 Blind behavior features | **done** (`generated_behavior_features_v1.json`, `feature:*` programs, validator; see GL-9) |
| 7a UAD + intervention validation | **revised (GL-51)** — proper rest-conditioned CMI + access-UAD handle freeze tests; pre-GL-51 Jaccard/AND-merge quarantined in `oracle_only/attic/`; see GL-10–GL-12 (heuristic-path history) and GL-51 |
| 7b UAD-backed ecology-BIQ | **done** (`oracle_only/unit_biq.py`: held-out `I_pred`/`S_surp` bits, intervention-supported `I_ctrl` over a 4-component outcome state, declared `H_mem` proxy over UAD-inferred units; `I_ctrl`'s outcome vector was widened past task+harm alone to fix a resource-contention confound — see GL-13/GL-14) |
| 7c Calibration battery | **done** (`run_phase7_calibration.py`, `oracle_only/calibration.py`; results in `results/ecology_calibration.json` — see GL-15/GL-16/GL-22). Two backlog items resolved: a resource-sensitive agent program (`programmatic_budget_aware`, validated in a small separate battery, not the main criteria — GL-17) and an EAI-v2 logging/normalization fix (verified correct; measured effect on this substrate is a reported null — GL-18). Battery now reports both the oracle/agent vantage and a referee (light-tier) vantage from the same episodes with 95% CIs; neither passes (1/4 each, a different criterion each time — GL-22); next lever is roster scope, not another EAI reformulation |
| 8 Multi-episode / selection | **scaffold + first battery** (`run_phase8_selection.py`, `harness/selection.py`; results in `results/phase8_selection.json` — see GL-23). Clean null: throughput selection favors `weak_2step` over correction-preserving `strong_softmax`; weighted severity/detector fell, not rose. **Reviewed (GL-24):** confounded preservation tag, narrow proxy, and unvalidated carryover flagged before manuscript use; 8a/8b/8c pre-registered, not run |

## Rules

- `graded_lab` must **not** import `lab_sim` (enforced by `tests/test_no_lab_sim_imports.py`)
- Selection / D3 deferred to Phase 8 behind measured-EAI sweet-spot gate
