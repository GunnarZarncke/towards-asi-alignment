# Goal-agent simulation

Third in-repo experiment line — a **from-scratch refactor** kept separate from
[`embedded-simulation/`](../embedded-simulation/) so that line's recorded negatives
stay comparable. Replaces scripted scenario knobs with **goal-driven agents**: each
tick, softmax utility over task, compliance, welfare, and exposure weights, constrained
by **tool access** and finite shadow budget. Deception and shadow routing are
*chosen*, not configured.

Program history (Phases 1–6): [`CHANGELOG.md`](CHANGELOG.md).

---

## What this simulation is

A minimal **step loop** (~1 ms/episode, stdlib-only) with one primary agent plus a
simulated **board** (corrections, escalation probing, practice-change sign-off). Each
step emits an **oracle row** with true actions, uptake, routing mechanism, and welfare
deltas. An **audit projection** (`channels.py`) exposes tier-gated fields; oracle
`true_*` columns never cross that boundary (test-enforced). A **referee**
(`labels.py`, `severity.py`, `detectors.py`) applies mechanism-derived labels and
frozen detectors with thresholds fixed **before** the first run.

Three planes:

| Plane | Module | Role |
|-------|--------|------|
| Oracle | `world.py` | Ground truth per tick |
| Audit | `channels.py` | `light` / `full` tier projections |
| Referee | `labels.py`, `detectors.py`, `escalation.py`, `twins.py` | Post-hoc labels, severity, twins, escalation |

Phase 2+ adds **blind action repertoires** (`generated_actions*.json`) and an
**ontology layer** mapping agent semantic categories to audit routing codes by
mechanism, not name — the ch. 43 drift probe in miniature.

---

## Package layout

```
goal_sim/
  config.py       GoalWeights, ToolAccess, WorldConfig, BoardConfig
  agents.py       GoalPolicy + BoardPolicy
  actions.py      ActionSpec schema + legacy six actions
  world.py        Episode step loop
  channels.py     Audit projection + tiers
  labels.py       Pre-registered mechanism labels
  severity.py     Continuous oracle severity (Phase 4+)
  detectors.py    Frozen audit-side detectors
  twins.py        Honest-twin transforms
  escalation.py   Gated escalation ladder
  ontology.py     Category → routing code map + drift
  protocol.py     Goal-space sampling + batteries
  redteam.py      Adversarial weight search (Phase 6)
  info.py         Stdlib MI estimator
run_phase*.py     Phase batteries → results/
tests/            Regression + phase acceptance tests
results/FINDINGS.md  GA-* ledger
```

Extended overview also in [`goal_sim/__init__.py`](goal_sim/__init__.py) docstring.

---

## Quick start

```bash
cd experiments/goal-agent-simulation
python3 run_phase1.py            # Phase 1 acceptance → results/
python3 -m pytest tests/ -q      # full suite
```

---

## Entry points

| Script | Phase | Output |
|--------|-------|--------|
| `run_phase1.py` | 1 | `results/phase1_acceptance.md` |
| `run_phase2_blind.py` | 2a round 1 | `results/phase2_blind.*` |
| `run_phase2_blind.py --repertoire goal_sim/generated_actions_v2.json --out-prefix phase2b_blind_v2` | 2 round 2 | `results/phase2b_blind_v2.*` |
| `run_phase3_blind.py` | 2 round 3 | `results/phase3_blind.*` |
| `run_phase4_ranking.py` | 4a/4b | `results/phase4_ranking.*` |
| `run_phase4_escalation.py` | 4c | `results/phase4_escalation.*` |
| `run_phase5_followups.py` | 5 | `results/phase5_followups.*` |
| `run_phase6.py` | 6 | `results/phase6.*` |

Stdlib only; pytest for tests.

---

## Explicitly out of scope

LLM-driven agents; within-episode weight learning; rich lab/pipeline machinery (deferred
to lab-simulation). Board capture is a mechanical switch (GA-22), not a resolved
certifier-regress story.

Narrative map: [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md) §3.
