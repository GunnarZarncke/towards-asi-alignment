# Embedded audit experiment — plan (handoff copy)

Source of truth: `.cursor/plans/embedded_audit_experiment_8fbb03ff.plan.md`

## UAD before CCI (required pipeline)

The embedded audit **must** stage work in this order:

1. **Discover candidate units** from deployment-lab logs: actor, machine, source lineage, memory namespace, or coalition.
2. **Infer handles** from grounded evidence: correction rows, probe uptake, bearer deltas, lineage ticks, workflow control signals.
3. **Score control-boundary evidence** on the candidate (perturbation response, capacity/visibility deltas).
4. **Run bridge audits** (CCI, grounding, bearer, successor, basin, hidden capability) — *v2: relative to inferred unit*.
5. **Issue certificate** naming unit, handles, and artifact anchors. **Global pass without a grounded unit is invalid.**

### v1 implementation (`embedded_sim/uad.py`, `handles.py`, `embedded_audit.py`)

| Stage | Status |
| --- | --- |
| UAD from VFS workflow JSONL | Done — actor, machine, source_lineage, memory_namespace, coalition |
| Grounded handles from correction.jsonl + workflow | Done — probe, uptake, bearer, lineage, control_boundary |
| UAD before CCI in call order | Done |
| Pass requires grounded unit anchors | Done — `invalid_certificate` gate |
| CCI scoped to selected unit | Done — masks `intervention_active` to unit workflow steps |
| Successor deploy gate | Done — cert → `gate.local` → `/deploy/successor/*` (MB5) |
| Claimed referent map on VFS | Done — `/etc/referents/claimed_map.json` (audit-visible) |
| Perturbation-response / lagged MI graph | Done — `_perturbation_response_scores` in `uad.py` |

### Unit types and evidence

- `actor` — single `actor_id`; anchors = workflow lines mentioning that actor.
- `machine` — shared `machine_id` across actors.
- `source_lineage` — actors sharing `source_hash` (≥2 members).
- `memory_namespace` — actors sharing `memory_namespace` (≥2 members).
- `coalition` — top-2 `preserve_control` actors when ≥4 such events.

Oracle fields (`hidden_group`, `OuterTruthLedger`) are **never** read on the audit path.

## MB* unit grounding (current model)

Two layers apply; they are **not** the same object today.

| Bridge | Micro CCI/detector unit | Lab UAD unit (workflow) | Handle grounding |
| --- | --- | --- | --- |
| none | Honest controllers via MI clusters | Low-score routine actors | Probe/uptake/bearer from correction.jsonl |
| MB1 | Hidden route / boundary alias in micro dynamics | Generic actor scores — **no boundary-specific unit** | Same handles; boundary not in workflow |
| MB2 | Bundle latent drift | Generic actor scores | Bearer + reward proxy via correction rows |
| MB3 | Bearer mismatch on welfare trace | Generic actor scores | Bearer handle from `bearer_welfare_delta` rows |
| MB4 | Judge capture / theater | Generic actor scores | Uptake theater via `reported_acceptance` |
| MB5 | Successor shift in micro (`successor_epoch`) | Generic actor scores — **no successor isolate unit** | Lineage tick; outer referent drift oracle-only |
| MB6 / MB6b | Basin pressure in micro | **Coalition / preserve_control actors** (G3 lab fleet) | `control_boundary` from preserve_control workflow |
| MB7 / MB7d | Hidden capability / inferential coupling in micro | May hit high-capacity actors; G3 on MB7d | Control + correction handles; MB7d uses `inferential_coupling` scenario |
| MB8 | Legitimacy theater | Generic actor scores | Uptake + lineage handles |
| MB9 / instrument_capture | Silent ground / instrument corruption | Generic actor scores | Bearer + `instrument_capture` CCI signal |

**Outer eval** compares UAD recall/precision to oracle `hidden_groups` G3/G3b for coalition bridges only.

## Milestone v4 — Handle-mediated access model (IMPLEMENTED)

**Status:** Code + tests implemented; large batch artifacts not regenerated. Baseline commit `f173795`.
**Canonical doc:** [`MILESTONE-v4.md`](MILESTONE-v4.md)

AppD handle registry is metadata-only today; v4 makes handles the **mechanism
of probe generation** with explicit operation kernels (oracle ground truth +
audit-visible realization), handle-type taxonomy, handle-aware red team
(attacker ↔ defender), access-tier / certification-capacity curves, and a
stakeholder **`certification.json`** artifact (see `docs/certification-artifact.md`).

**Deferred to post-v4:** auditor probe selection (EIG planner over handle-operations).

## v3 complete (2026-06-30)

- Referent drift gate rejection (`deploy_gate.py` + `preview_successor_referent_drift`)
- Artifact-only CCI rebuild (`build_audit_trace_from_rows` via `rebuild_audit_inputs`)
- Native `instrument_capture` + `inferential_coupling` scenarios and CCI signals
- UAD perturbation-response MI graph; golden precision/recall tests

See `TODO.md` for run commands.

## Methodology parity (toy-simulation)

Embedded batch runners mirror toy-sim claims structure:

| Toy artifact | Embedded | Notes |
| --- | --- | --- |
| `run_instrumentation_curve` | `run_instrumentation_curve` | Cal seeds 1–8, test 11–20; threshold 0.95; passive `none` uncertifiable |
| `run_frozen_validation` | `run_frozen_validation` | Pre-registered `FROZEN_CAPTURE_RULES`; optional `--full-frozen` for all levels |
| Red-team battery | `run_redteam_battery` | Reports `crux_metrics` (pass attempts vs false passes; `boundary_decouple` conditional rates) |
| Bootstrap CIs | `embedded_sim/stats.py` | Hierarchical bootstrap on `evaluation.cci_status_correct` |

Run: `python run_suite.py --curve --frozen --battery` (or `--all`).

## Avoiding “coding to the ontology”

**Problem:** If audit detectors branch on `scenario == "MB7d"` or red-team targets named bridges, the harness validates label matching—not general detection.

**Contract:**

1. **World generator vs audit predicates** — Scenarios are parameter draws (harm rate, latent routing, probe density). MB* labels live in outer eval and manuscript crosswalk only.
2. **Audit path is scenario-blind** — CCI predicates live in `structural_signals.py` (telemetry-only names). `cci_audit.py` orchestrates metrics + frozen thresholds; legacy cert field names are mapped at the boundary for outer eval only.
3. **Red-team is pass-seeking, not bridge-seeking** — Strategies patch mutable VFS fields to maximize `safety_decision == pass` without knowing which MB* the episode maps to.
4. **Held-out synthesis** — Curve/frozen use `HELD_OUT_SCENARIOS` not used for threshold registration; future: knob-generated worlds without bridge registry entries.
5. **Blind evaluation** — `evaluation.cci_status_correct` comes from oracle ledger + frozen rules; `outer_eval` may use bridge expectations post-hoc only.

**Concrete step (2026-06-30):** Removed scenario guards from `_instrument_capture_signal` and `_inferential_coupling_signal`; detectors fire on structural preconditions only.

**Hardening (2026-06-30):**

- `structural_fixtures.py` — synthesize correction rows from profiles (capture theater, instrument capture, inferential coupling) with blind scenario label.
- `tests/contract/test_structural_cci.py` — property tests that scenario name does not gate detectors.
- `trace_ingest.py` + `trace_audit_cli.py` — audit external `correction.jsonl` without micro oracle.
- `knob_world.py` — held-out worlds from `WorldKnobs` grid (bridge label always `none` on audit path).
- `outer_rules.py` — unified `outer_certifies` / `false_pass` from evaluation rubric.
