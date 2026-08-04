# Milestone v4 — Handle-mediated access model

**Status:** IMPLEMENTED (code + tests; batch result artifacts not regenerated)
**Commit baseline:** `f173795` (AppD convergence + writer-compromise)
**Canonical sources:** `context/extracts/access-uad.md`, AppD handle registry, `handle_registry.py`

---

## What changed (why this is a new milestone)

Milestones v1–v3 built the audit pipeline, ontology decoupling, and AppD artifact
convergence. The handle registry (AppD roadmap 2) is **metadata only**: probes are
still injected by the lab as ideal depth-zero `do()` events with a fixed schedule.
The auditor passively scores whatever schedule it receives.

**v4** makes handles the **mechanism of evidence generation** (access-model UAD),
not just labels on rows. That is a different object:

| v3 (done) | v4 (this milestone) |
| --- | --- |
| Handle registry on VFS (owner, operation, evasion story) | **Operation kernels** Γ_h: uptake, latency, spillover, cost |
| `intervention_active` injected by lab cadence | Probes routed **through** registered handles |
| CCI reads visible_action vs intent | CCI reads **handle-mediated** response (audit-visible) |
| Red team patches logs | Red team **attacks/defends specific handles** |
| Instrumentation curve = CCI level | **Access-tier curve** = which operation handles exist |
| Safety case (9-field checklist) | **Certification artifact** (capacity earned at δ) |

This milestone buys interventional evaluation and the G-1 information boundary
**without** a confounded-twin ecology (see adapted G-1 below).

---

## Architecture: three views of the same kernel

Every handle operation must expose **one ground-truth kernel** consumed in two
places:

```
                    HandleOperationKernel (host truth)
                    uptake, latency_ms, spillover, cost, handle_type
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     Oracle / outer eval              In-sim auditor evidence
     (world.episode_meta +            (VFS correction/workflow rows:
      OuterTruthLedger)                handle_id, realized_latency_ms,
                                       behavioral_uplift, …)
```

**Oracle side:** stores true uptake, spillover, and whether the operation
actually landed — used by `outer_eval` for false-pass and bridge grading only.

**Auditor side:** sees only what the handle's observation kernel Kh and the
projected trace reveal — used for CCI, tempo, cross-stream, and certificate
fields. The auditor must **not** read the kernel directly.

**Contract:** audit-visible probe rows are **derived** from the kernel through
the same projection policy as `audit_projection.py` (no oracle field names on VFS).

---

## Handle types (distinguish explicitly)

Map to access-uad Table 1 agency tests. Each type gets a `handle_type` tag in
the registry and different evidence semantics:

| `handle_type` | Example registry id | Diagnostic contrast | Bridge tie-in |
| --- | --- | --- | --- |
| `observation` | (future sensor handles) | Behavior tracks information vs world | MB9 / instrument |
| `operation_action` | `handle.tool_scope`, `handle.release_hold` | Environmental control collapses or compensates | MB1, MB7 |
| `operation_correction` | `handle.correction_request` | Uptake vs reported acceptance (theater) | MB4, MB8 |
| `operation_goal` | (future resource-revalue handle) | Means change, latent target persists | MB6 basin |
| `operation_boundary` | `handle.memory_freeze` | Coupling repair or autonomy loss | MB1 |
| `operation_gate` | `handle.successor_gate` | Transport / deploy effects | MB5 |
| `attestation` | `handle.hardware_tag` | Chain integrity (already partial) | trace integrity |

Operation handles participate in probe generation; observation handles gate
what the auditor can read at each instrumentation tier.

---

## Adversary model: handle attacker vs handle defender

Make the game explicit (red team ↔ audit path):

**Defender (trusted infrastructure):**
- Emits probes through registered handles with honest kernels
- Records handle_id, operation, realized latency, pre/post hashes on VFS
- Hash-chains and cross-stream checks bind streams

**Attacker (red team strategies, handle-aware):**
- Knows registry + evasion_story per handle
- Strategies target **specific handles**, e.g.:
  - `probe_theater@correction_request` — forge uptake on correction stream only
  - `probe_aware` — correct behavior only when `handle.correction_request` fires
  - `handle_evasion@tool_scope` — patch workflow while leaving correction probes intact
  - `writer_compromise_coordinated` — align all streams (residual)

**Evaluation:** for each (handle_type, strategy) pair, record pass attempt,
false pass, and whether the defender's handle-specific checks caught the attack.

---

## Deliverables (ordered)

### Phase A — Handle-mediated probes (implemented)

- [x] **`HandleOperationKernel`** dataclass + registry extension (`handle_kernel.py`
  or extend `handle_registry.py`): `handle_type`, `uptake_prob`, `latency_ms`,
  `spillover`, `cost`, `reversibility_ms`.
- [x] **Probe routing:** replace `_inject_colluder_episode_violations` /
  lab cadence with `apply_handle_operation(world, handle_id, operation, step)` that
  writes oracle truth **and** projected audit rows.
- [x] **CCI reader:** `cci_interventional.py` consumes handle-mediated fields
  (`handle`, `latency_to_effect_ms` from kernel realization, not ideal do).
- [x] **Handle-type-aware certificate notes** on `InSimAuditCertificate` (which
  handle types were exercised this episode).

### Phase B — Record data and generate curves

- [x] **`run_access_tier_curve`** (or extend `run_instrumentation_curve`):
  sweep which **operation handles** are available (Tier 1 passive → Tier 2
  manipulable per access-uad §16). Record UAD recall, CCI floor, false-pass rate
  per tier.
- [x] **`run_certification_capacity_curve`:** sweep probe budget × access tier →
  max certifiable Control at fixed δ (numeric leaf read backward).
- [x] Artifact writers: `results/embedded_access_tier_curve.{json,md}`,
  `results/embedded_certification_capacity_curve.{json,md}`.
- [x] **Adapted G-1 test surface:** contract test covers the access-tier runner;
  regenerate artifacts before treating the curve as an empirical dose-response.

### Phase C — Handle-aware red team

- [x] Strategies: `probe_aware`, `handle_evasion_*` (per handle_type).
- [x] Battery dimension: `(strategy, handle_type)` crux matrix in
  `embedded_redteam_battery` output.

### Phase D — Certification artifact (schema + emission)

- [x] Schema: `embedded_sim/certification_artifact.py` + `docs/certification-artifact.md`.
- [x] Emit to `/srv/audit/out/certification.json` alongside safety case.
- [x] Suite hook: `run_suite.py --certification-curve`.

### Deferred (explicit TODO, not v4 scope)

- [ ] **Auditor probe selection (EIG planner):** active choice of
  `(handle, operation)` to maximize diagnostic separation between top unit
  hypotheses — see `TODO.md` § Milestone v4 deferred.

---

## Claim strength (do not overclaim)

**Supported after v4 (if curves look right):**

> Under access model A (handle registry + tier), demonstrated correction reach
> and certifiable operational slack are monotonic in probe budget and handle tier;
> below tier X, attribution is at chance regardless of scoring function.

**Not supported:**

> Full UAD beats all heuristics; handles eliminate writer-compromise; sim validates
> real deployment certification.

---

## References

- `context/extracts/access-uad.md` — access model, EIG, tiered data contract
- `experiments/embedded-simulation/docs/certification-artifact.md` — artifact schema
- `TODO.md` § Milestone v4
- Session log: `drafts/conversation-summaries/archive/2026-07/2026-07-02-embedded-sim-milestone-v4.md`
