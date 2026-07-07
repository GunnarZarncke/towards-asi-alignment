import LabSimLeakProof.Keys
import LabSimLeakProof.JsonTree
import LabSimLeakProof.Tiers
import LabSimLeakProof.Projections
import LabSimLeakProof.Leakage
import LabSimLeakProof.Reachability
import LabSimLeakProof.Theorems
import LabSimLeakProof.SpineBridge

/-!
# LabSimLeakProof

Lean translation of lab-simulation's three-plane information policy:

* **Oracle** — referee ground truth (`ORACLE_ONLY_FIELDS` in Python).
* **Audit** — tier-projected logs + deep fetches (`events.py`, `detectors.py`).
* **Simulation** — per-agent observations and tool results (`world.py`, `tools.py`).

Main results:

* **Projection certificates** — `buildAuditView_no_oracle_leak`,
  `buildSimObservation_no_oracle_secret_leak`, `buildSimObservation_no_audit_surface_leak`.
* **Reachability analysis** — `Reachability.lean` models every Python transfer
  function and exchange medium; `reachability_certificate` proves no alternate
  path carries forbidden keys.
* **Combined** — `certified_episode_no_unintended_leak` / `episode_leakage_exact`.

Runtime assurance remains `tests/harness/test_planes.py` plus import/isolation
tests; this layer makes the information policy explicit and machine-checkable.
-/
