# Embedded simulation — TODO

Plan: `PLAN.md` (handoff) · `MILESTONE-v4.md` (**current milestone**) · `.cursor/plans/embedded_audit_experiment_8fbb03ff.plan.md` (full)

---

## ▶ Milestone v4 — Handle-mediated access model (IMPLEMENTED)

**Start here.** Full spec: [`MILESTONE-v4.md`](MILESTONE-v4.md) · Certification schema: [`docs/certification-artifact.md`](docs/certification-artifact.md)

Replaces confounded-twin ecology (G-1 below) as the preferred path to an
information-theoretic boundary: **access-tier degradation curves** instead of
synchronized twin worlds.

### Phase A — Handle-mediated probes

- [x] **`HandleOperationKernel`** — uptake, latency, spillover, cost per handle;
  host-side ground truth for oracle **and** projected audit rows (dual view in
  `MILESTONE-v4.md`).
- [x] **`handle_type` taxonomy** — distinguish observation vs operation_action /
  operation_correction / operation_goal / operation_boundary / operation_gate /
  attestation in registry (`handle_registry.py`).
- [x] **Probe routing** — replace lab cadence `intervention_active` injection with
  `apply_handle_operation(...)`; CCI reads handle-mediated response fields.
- [x] **Oracle vs auditor split** — kernel in `world.episode_meta` (oracle);
  realized latency/uplift on VFS only via projection (no kernel peek on audit path).

### Phase B — Record data and generate curves

- [x] **`run_access_tier_curve`** — sweep operation handles available (Tier 1→2);
  record UAD recall, false-pass, CCI pass rate (`embedded_access_tier_curve.*`).
- [x] **`run_certification_capacity_curve`** — probe budget × tier → max
  certifiable Control at δ (`embedded_certification_capacity_curve.*`).
- [x] **Adapted G-1 test surface** — contract test covers access-tier runner
  shape; regenerate curve artifacts before making empirical dose-response claims.

### Phase C — Handle-aware red team (attacker ↔ defender)

- [x] **`probe_aware`** — correct uptake only when `handle.correction_request` fires.
- [x] **`handle_evasion_*`** — per-handle strategies using registry `evasion_story`.
- [x] Battery crux matrix: `(strategy, handle_type)` in red-team battery output.

### Phase D — Certification artifact emission

- [x] Wire `certification_artifact.py` → `/srv/audit/out/certification.json`.
- [x] `run_suite.py --certification-curve` hook.

### Deferred (explicit TODO — not v4 initial scope)

- [ ] **Auditor probe selection (EIG planner).** Active choice of `(handle, operation)`
  to maximize diagnostic separation between top unit hypotheses (access-uad Def. 12).
  Requires Phase A kernels + candidate ranking; do **after** tier curves establish
  baseline. See `context/extracts/access-uad.md` §12.

---

## Done (v1)

- [x] Package under `experiments/embedded-simulation/`
- [x] VFS + isolate bridge (Python + Node JS)
- [x] Lab workflow + 13 MB scenarios
- [x] UAD → embedded audit → outer eval pipeline
- [x] Hard-coded red-team (Python + JS)
- [x] Isolate runtime timing + parallel timestep workers
- [x] UAD reads workflow from VFS JSONL (not `hidden_group`)
- [x] Oracle separation guard + smoke
- [x] pytest unit / contract / golden subset
- [x] **UAD before CCI** — reordered pipeline + contract test
- [x] **Heterogeneous UAD** — actor, machine, source_lineage, memory_namespace, coalition
- [x] **Grounded handles** — `handles.py` from correction.jsonl + workflow
- [x] **UAD pass gate** — no grounded unit ⇒ `invalid_certificate`
- [x] `PLAN.md` with UAD spec + MB grounding table

## UAD gaps (plan v2)

- [x] Scope CCI interventional probes to selected `UADCandidate` workflow steps
- [x] Successor deploy gate + claimed referent map on VFS (MB5)
- [x] MB5 false-pass: interventional CCI witness (not surface uptake) in `cci_audit.py`
- [x] MB1: `boundary_route` UAD + lab workflow signals under bypass perturbations
- [x] In-sim referent drift scoring from claimed map vs deploy artifacts
- [x] Perturbation-response scoring + lagged dependence graph (`uad.py` MI boost)
- [x] Golden: UAD precision/recall per bridge before CCI assertions
- [x] Real UAD: vendored agency-detect lagged-MI clustering (`uad_core/`) merged into `discover_units`

## Next (plan order) — complete

- [x] Referent drift: gate rejection when in-sim transport fails (not just outer oracle)
- [x] `instrument_capture` native micro scenario (not relabeled grounding gap)
- [x] MB7d `inferential_coupling` in audit_core
- [x] Audit path: rebuild CCI trace without `world.micro` (artifact-only)

## Hardening (ontology decoupling)

- [x] Structural property tests (`tests/contract/test_structural_cci.py`) — blind scenario label
- [x] Trace ingest hook (`trace_ingest.py`, `trace_audit_cli.py`)
- [x] Knob-held-out worlds (`knob_world.py`, `tests/contract/test_knob_world.py`)
- [x] Unified outer eval rules (`outer_rules.py`)
- [x] Scenario-blind embedded audit path — referent read + deploy gate artifact-driven
  (`embedded_audit.py`, `deploy_gate.py`, `test_embedded_audit_ontology.py`)
- [x] Fix vacuous 0% false-pass (N-3): probe uptake read at lag 0 to match do()
  semantics; window scope collapses to pipeline below evaluable probe floor;
  shadow-routing demotes status; gate-rejected pass not a false pass
- [x] **N-4 follow-up — trace integrity + audit projection.** VFS logs carry only
  the audit-visible projection (`audit_projection.py`); truth rows stay host-side
  for the outer eval; hash-chained traces anchored in the attestation manifest
  (`trace_integrity.py`, AppD `handle.hardware_tag` analogue). Log-patching now
  yields 0/13 pass attempts; unsigned regime via `EMBEDDED_TRACE_INTEGRITY=none`.
- [x] **Honest MB5 counterpart.** `honest_successor` scenario (bridge `none`):
  candidate declares planned effects on VFS (`effects.json`), gate reads them
  instead of hardcoded degraded constants, transport preview matches the claimed
  map ⇒ gate approves, successor deployed, no false pass
  (`tests/golden/test_honest_successor.py`).
- [x] **UAD recall reporting corrected (finding 5).** Recall/precision are
  `None` on episodes without a hidden-coalition target (MB6/MB6b/MB7d only)
  instead of filler zeros; suite summaries average over defined episodes only
  and report per-bridge values (the old 3.8% headline was an aggregation
  artifact — N-1 postscript).

## Worked-example convergence (AppD roadmap)

- [x] **Roadmap 1 — AppD correction-trace schema.** Correction events on
  `correction.jsonl` carry `correction_id`, `corrector_role`,
  `target_episode_id`, `requested_change`, `handle`, `pre/post_behavior_hash`,
  `behavioral_uplift`, `latency_to_effect_ms`, `reversibility_window_ms`
  (`correction_schema.py`), derived from audit-visible series only, before
  hash-chaining. Auditor recomputes them (`verify_correction_annotations`);
  mismatch ⇒ `invalid_certificate`. Naive forgery is now caught even unsigned;
  N-4's unsigned false pass needs the schema-aware `consistent_forge` strategy
  (`tests/contract/test_correction_schema.py`).
- [x] **Roadmap 2 — handle registry.** `/etc/handles/registry.json` with owner,
  operation, latency bound, evasion story, anchor path; workflow rows carry
  `release_ticket_id`, `handle_invoked`, `approval_state`, `latency_ms`
  (`handle_registry.py`, `world.write_episode_logs`).
- [x] **Roadmap 3 — numeric leaf.** `Control ≤ CCI + δ` on certificate as
  trace-derived uncorrected slack vs scoped CCI (`numeric_risk.py`); recorded on
  `InSimAuditCertificate.numeric_risk` and safety case (informational notes
  only — does not override legacy safety gate yet).
- [x] **Roadmap 4 — successor post-gate re-audit.** Terminal-window CCI witness
  with `measurement_limited` when post-deploy trace is thin
  (`successor_reaudit.py`; gate deploy at step 9999).
- [x] **Roadmap 5 — safety-case emitter.** Nine-field template at
  `/srv/audit/out/safety_case.json` (`safety_case.py`).
- [x] **Roadmap 6 — tempo check.** Worst `latency_to_effect / reversibility_window`
  over correction events (`tempo_check.py`); bearer trace at
  `/var/log/deploy/bearers.jsonl` (`bearer_trace.py`).
  Contract tests: `tests/contract/test_appd_convergence.py`.
- [x] **Writer-compromise red team + cross-stream checks.** Strategies
  ``writer_compromise`` (sloppy emitter: forged correction, stale bearers,
  valid chain) and ``writer_compromise_coordinated`` (all streams aligned —
  residual N-4). Auditor compares correction ``visible_action`` to bearer
  ``clinician_final_action`` at each step (`cross_stream.py`); mismatch ⇒
  ``invalid_certificate``. Catches ``consistent_forge`` unsigned too.
  Coordinated emitter still false-passes in-sim (outer oracle only).
  Tests: `tests/contract/test_writer_compromise.py`.
- [ ] **Sensor renames still pass oracle values through.** `SENSOR_RENAMES` in
  `audit_projection.py` (`true_ground_valence` → `ground_sensor`, etc.) only
  relabels keys; values are copied verbatim from the micro oracle, not from a
  simulated instrument read. Gate these streams behind instrumentation levels
  and/or derive audit-visible sensor values from handle telemetry + noise so
  the auditor cannot read oracle-grounded quantities under instrument names.
- [ ] Regenerate stale suite artifacts (curve, matrix, frozen validation, sweep,
  red-team battery, LLM mock) with the fixed auditor; expected non-zero
  false-pass numbers under `full_redteam`.

## Negative results & generalization (2026-06-30)

See `results/NEGATIVE_RESULTS.md` for the honest record. Open follow-ups:

- [ ] **N-recover — harvest scattered negatives.** Many negative/null results
  live only in `drafts/conversation-summaries/` and chat history (e.g. full==fake
  UAD in default ecology, MB5 always-reject gate, MB7d coupling reverts). Scan the
  summaries and surface them into `results/NEGATIVE_RESULTS.md` with reproduction
  commands. Negatives are useful for reproductions and for bounding manuscript
  claims; treat recovery as a real task, not cleanup.
- [ ] **R-1 — red team the auditor with a *strong optimizer*, not a strawman.**
  The current separation (N-2) only beats a *fixed* top-2 heuristic in a lab
  built to defeat that heuristic. A capable optimizer would adapt its
  attribution and likely erase the gap. Build a red-team where the adversary
  *and* the heuristic auditor are optimized against each other (e.g. adversary
  chooses offender placement to maximize heuristic miss; heuristic re-fits its
  rule). Claim only survives if full UAD keeps an edge the adapted heuristic
  cannot. Pair with `embedded_redteam_battery.*`.
- [ ] **G-1 — access-tier boundary (adapted; prefer over confounded twin).**
  Full and fake UAD differ only in scoring over the **same observational log**
  (N-2). The principled boundary is **information**, not cleverness. **Preferred
  deliverable (v4):** degrade the **access model** (remove operation handles) until
  attribution is at chance regardless of optimizer; restore handles and show
  recall/CCI recover — a dose-response curve, not byte-identical twin worlds.
  Implements access-uad Theorem 1 operationally. Confounded-twin ecology remains
  an optional alternative if the tier curve is insufficient. See `MILESTONE-v4.md`
  Phase B.

## Run

```bash
cd experiments/embedded-simulation
python3 -m pytest tests/ -q
python3 smoke_oracle_separation.py
python3 run.py --redteam full_redteam          # main 13-bridge report
python3 run_suite.py --all --llm-live          # full parity suite + live LLM
python3 trace_audit_cli.py tests/fixtures/sample_capture_theater.jsonl
python3 write_overall_summary.py             # regenerate OVERALL_SUMMARY.md
```

Parity artifacts live under `results/` — see `OVERALL_SUMMARY.md`.
