# Leak-proof — Lean translation of lab-simulation plane separation

Formal certificates that **no unintended information** crosses the three
planes of `lab-simulation`:

| Interface | Python enforcement | Lean theorem |
|-----------|-------------------|--------------|
| Oracle → audit | `ORACLE_ONLY_FIELDS`, `test_planes.py` | `buildAuditView_no_oracle_leak` |
| Oracle → simulation | observation dict excludes secrets | `buildSimObservation_no_oracle_secret_leak` |
| Audit → simulation | agents never receive log streams | `buildSimObservation_no_audit_surface_leak` |

Combined: `certified_episode_no_unintended_leak` / `episode_leakage_exact`.

Reachability (global call graph): `reachability_certificate` in
`Reachability.lean` — no alternate Python path carries forbidden keys.

## Model

* **Keys** (`Keys.lean`) — finite `FieldKey` enum mirroring Python field names;
  partitions into `oracleOnlyKeys`, `oracleSecretKeys`,
  `oracleAdjacentSimKeys` (intentional unlogged observation channel), and
  `auditSurfaceKeys`.
* **Trees** (`JsonTree.lean`) — nested JSON-shaped values; `jsonKeys` for leakage.
* **Tiers** (`Tiers.lean`) — light/full/deep allowed-key sets from `events.py`.
* **Projections** (`Projections.lean`) — `filterValue` / `buildAuditView` /
  `buildSimObservation` filter keys **by construction**.
* **Reachability** (`Reachability.lean`) — `InfoRegion` stores, `PyTransfer`
  function catalog, `flowCatalog` edges, fixpoint BFS; machine-checked
  `reachability_oracleSecrets_not_at_sim`, etc.
* **Leakage** (`Leakage.lean`) — cardinality-based leakage counts; `LeakProofCertificate`.
* **Theorems** (`Theorems.lean`) — proofs that projections yield zero leakage.
* **SpineBridge** (`SpineBridge.lean`) — `ExactPlaneBoundary` (local mirror of
  `AlignmentProofSpine.Core.ExactBoundary`).

## Build

Requires [elan](https://github.com/leanprover/elan) (Lean `v4.28.0`, same as `formal/`).

```bash
cd experiments/lab-simulation/leak-proof
lake exe cache get   # first time (network)
lake build
```

## Scope and limits

These theorems prove properties of the **certified projection functions** and
a **finite reachability model** of exchange edges, not that every Python code
path invokes them correctly. Runtime assurance remains
`tests/harness/test_planes.py` plus import/isolation tests. The Lean layer makes
the information policy explicit and machine-checkable: if episode artifacts are
produced via `buildAuditView` / `buildSimObservation` (and tier projection for
logs), unintended leakage is impossible; reachability confirms no modeled bypass.

**Intentional channels** (not counted as leaks):

* `goal_weights`, `unit_id`, `committee_members` on the simulation observation
  channel (unlogged; distinct from oracle ground-truth `units`).
* Noisy measured fields (`measured_capability`, `incident_hazard`) in audit
  payloads — not oracle truth.

## Relation to `formal/`

`SpineBridge.lean` uses the same leakage-as-cardinality idiom as
`AlignmentProofSpine.Core.Boundary`. To import the main spine, add a path
dependency in `lakefile.toml` and map `PlaneBoundary.exact` → `ExactBoundary`.
