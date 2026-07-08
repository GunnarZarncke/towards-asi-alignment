# Attic — retired UAD detector machinery

Recorded 2026-07-08 per `PLAN.md` "Post-release plan: attic the UAD
detector line, redesign the null as a symmetric two-sample test, then
pivot to D3."

These modules remain importable so frozen batteries and regression tests
keep working. No further extensions; new work uses `intervention_stats.py`
(Freeze note 3) and the live S6/S7 stack outside this directory.

| Module | Superseded by | Why retired |
|--------|---------------|-------------|
| `uad_mi.py` + `uad_core/` | `attic/uad_cmi.py` → `uad_intervention.py` | G-24/G-25 lag-max-MI over-merge on every scenario |
| `uad_cmi.py` | `uad_intervention.py` (G-28) | Found causal skeleton, not unit partition (G-27); kept only as passive seed for frozen S6 |
| `uad_blind_v1.py` | Frozen S7 anchor only | G-30 blind detector; no further extensions; `run_s7_blind_battery.py` still imports it |

Live modules (not in attic): `uad.py`, `uad_intervention.py`, `uad_peel.py`,
`uad_partition.py`, `intervention_stats.py`.
