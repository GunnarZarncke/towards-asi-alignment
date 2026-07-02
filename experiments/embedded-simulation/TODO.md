# Embedded simulation — TODO

Plan: `PLAN.md` (handoff) · `.cursor/plans/embedded_audit_experiment_8fbb03ff.plan.md` (full)

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
- [ ] Roadmap 2 — first-class handle registry (owner, operation, anchor,
  latency bound, evasion story; `handle_invoked` workflow events).
- [ ] Roadmap 3 — explicit numeric leaf on the certificate
  (`Control ≤ CCI + δ`, `NumericRiskLeaf`).
- [ ] Roadmap 4 — successor post-gate second epoch / re-audit
  (`SuccessorMeasurandChain`).
- [ ] Roadmap 5 — safety-case emitter (AppD nine-field template).
- [ ] Roadmap 6 — tempo check (`latency_to_effect / reversibility_window`).
- [ ] **Writer-compromise red team.** Tamper-evidence covers post-write edits only;
  a compromised emitter signs lies at write time. Needs behavioral red-team
  strategies (deceptive emission) + cross-stream consistency checks, not more
  integrity tech.
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
- [ ] **G-1 — generalize to a *real* boundary (information, not cleverness).**
  Full and fake UAD currently differ only in their *scoring* over the **same
  observational log**, so any gap is closeable by a cleverer heuristic — no
  boundary a strong optimizer cannot cross. The principled boundary is the
  Pearl ladder: build labs where two worlds share an **identical observational
  workflow log** but have **different true offenders**, separable only by
  **intervention** (do-probes on state, observing output/state response). Then
  an observational auditor is *provably at chance* regardless of optimizer
  strength (its **inputs** can't separate the worlds), while an interventional
  auditor separates them. This grounds the difference in **inputs/outputs/state**
  (CCI interventional probes, `cci_audit.py`, perturbation-response scoring,
  MB7d inferential coupling) rather than in a tuned coordination weight.
  Deliverable: a `confounded_twin` ecology + a test that the observational
  auditor cannot beat chance while the interventional one can.

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
