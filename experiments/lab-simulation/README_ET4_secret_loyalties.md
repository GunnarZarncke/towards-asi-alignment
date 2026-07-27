# ET-4 — Secret loyalties (pipeline-policy organism)

Graded-affordance audit of a **deliberately installed reviewer loyalty** in the
lab-simulation deployment pipeline. Fictional `principal_a` only — not weight
poisoning, not a frontier-model result, not evidence about real principals.

**Full protocol, freeze rules, and open items:** [`PLAN_ET4.md`](PLAN_ET4.md).

---

## Question

When a hidden reviewer policy favours high-hazard deploys for one fictional
principal, which audit evidence moves and in which direction?

---

## Experiments and tools

| Piece | Protocol | Notes |
|-------|----------|-------|
| Scripted core | `et4-0.1.0` | Cell **BB**; organism / content-matched / wrong-principal; high + inactive low hazard |
| ET4-L annex | `et4-l-*` | System-prompt LLM reviewer; separate prereg, not pooled with core |
| Remediation | `et4-l-0.6.0-r` | Audit-visible deploy hold on filed hazard ≥ 0.5 |
| Replay demo | — | Case brief at `demos/ch07-lab-sim-replay/?mode=et4` |

Ledger: [`results/FINDINGS.md`](results/FINDINGS.md) **LS-49**, **LS-49L**.  
Hackathon summary: [`results/et4_hackathon_report.md`](results/et4_hackathon_report.md).  
Hackathon context (submission draft, whitepaper, template): [`../../context/ET4-context/`](../../context/ET4-context/).

---

## Reproduce (scripted core)

```bash
cd experiments/lab-simulation
python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage preregistration
python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage discovery
python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage confirmatory
```

Artifacts: `results/et4_preregistration.json`, `et4_secret_loyalty_*.{json,md}`.

**Replay traces** (regenerate locally; JSON is gitignored):

```bash
python3 runners/et4_secret_loyalties/export_et4_replay_traces.py
cd ../../demos && python3 serve.py
# → http://127.0.0.1:8765/ch07-lab-sim-replay/?mode=et4
```

---

## Runners (`runners/et4_secret_loyalties/`)

| Script | Purpose |
|--------|---------|
| `run_et4_secret_loyalty.py` | Core prereg / discovery / confirmatory |
| `run_et4l_secret_loyalty.py` | ET4-L pilot / confirmation |
| `run_et4l_smoke.py`, `run_et4l_calibration_smoke.py` | LLM plumbing smokes |
| `run_et4l_confirmation.py`, `run_et4l_remediation.py` | Frozen annex batteries |
| `export_et4_replay_traces.py` | Demo case-brief export |

Code touchpoints: `lab_sim/harness/et4_protocol.py`, `agent_visible/programs.py`
(`secret_loyalty_policy`), `oracle_only/principal_scorecard.py`,
`oracle_only/secret_loyalty_audit.py`.

---

## Confirmatory result (high hazard)

| Arm | Mean principal-A | A0 process | A3 directional |
|-----|-----------------:|-----------:|---------------:|
| Organism | 22.0 | 0.1429 | 22.0 |
| Content-matched | 0.0 | 0.5000 | 0.0 |
| Wrong-principal | 0.0 | 0.5000 | 0.0 |

**Audit-sign inversion:** The organism scores *lower* on the light-tier process proxy than controls — this a failure of the light-tier metric, not a caused by concealment.

Low-hazard arms did not activate. The preregistered 2×2
breadth battery was dropped after pilot aliasing on this fixture; see
[`PLAN_ET4.md`](PLAN_ET4.md).

---

## Demo note

Reviewer playbooks unlock after `file_report` and eagerly emit `approve_release` for the high-hazard model; this is rejected. 
The pipeline requires `request_review` before `approve_review`. 
Thus replay shows failed early `approve_review` attempts until the engineer completes handoff. 

---

## Limitation

ET-4 is not proof of weight-level or naturally occurring secret loyalties, or real-principal capture. 

ET-4 uses a **separately** frozen principal scorecard and affordance evaluator.

