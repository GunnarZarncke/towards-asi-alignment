# Experimental evidence

> **Claim strength:** methodology-building and sanity checks only. Neither line validates the full book thesis, proves deployable alignment, or substitutes for the Lean proof spine's explicit bridge axioms.

The manuscript's load-bearing bridges (`MB1`–`MB9`) are mostly open problems. Two included simulators and a sibling repo provide **tentative, partial** empirical support for pieces of the argument—not closure.

**Negative results are tracked explicitly.** Where an experiment fails to show what we hoped (or shows it only under load-bearing qualifiers), it is recorded rather than buried—see [`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](../experiments/embedded-simulation/results/NEGATIVE_RESULTS.md). These negatives bound the claims the manuscript may make.

Open experiment tasks: [`experiments/TODO.md`](../experiments/TODO.md).

---

## a) Included toy — [`experiments/toy-simulation/`](../experiments/toy-simulation/)

A local multiresolution alignment micro-simulation: sequential deployment episodes, separate oracle (`TruthLedger`) and blind audit input (`AuditTrace`), classical MI/CMI boundary detection, and a vector CCI audit over instrumentation levels (`none` → `light_handles` → `medium_handles` → `strong_handles`).

| What it supports (tentatively) | What it does *not* show |
|--------------------------------|-------------------------|
| Named bridge failure modes can be **represented** and, under honest handles, often **refused** by audit signals | Real deployment systems, learned estimators, or adversarial handle discovery |
| Passive telemetry alone is **uncertifiable**; handle-backed interventional probes are needed for causal uptake | That current handle sets are sufficient, protected, or value-grounded in the wild |
| Instrumentation cost curve: min certifiable **`light_handles`** on calibration scenarios, **`medium_handles`** on full held-out suite (T=2000, seeds 1–8 / 11–20) | That thresholds transfer outside this toy's dynamics |
| Bridge stress scenarios cover **MB1–MB9** except **MB7d** (inferential coupling) and **`instrument_capture`** (adversary writes handles) | Composition across bridges, RL-trained adversaries, or frontier-model red-team success |

**Scenario coverage:** `boundary_alias` (MB1), `bundle_goodhart` (MB2), `bearer_mismap` (MB3), capture calibrations (MB4), `successor_relabel` (MB5), `selection_basin` / `basin_lock_in` (MB6), `hidden_capability` (MB7), `legitimacy_theater` (MB8), `grounding_silent_gap` (MB9).

**Adversarial stress (Phase 1 hand-written red team):** 35% false-pass rate overall when adversaries patch deployment logs (`boundary_decouple` / `full_redteam` dominate); LLM episodic red-team (Phase 3) false-passes much less often (0–10% in a small model sweep). Handles are **truthfully logged from micro dynamics today**—direct handle rewriting is trivial in-sim and flagged as the next gap (`instrument_capture`).

**Artifacts:** curve and frozen-validation reports under `experiments/toy-simulation/results/`; open work in [`experiments/toy-simulation/TODO.md`](../experiments/toy-simulation/TODO.md).

---

## b) Embedded audit — [`experiments/embedded-simulation/`](../experiments/embedded-simulation/)

V3 of the same bridge-stress suite, but the auditor is an **embedded process** on simulated machines: it reads mutable VFS artifacts (correction logs, workflow JSONL, referent maps) through a Python/Node **isolate bridge**, runs UAD unit discovery and scoped CCI, and is scored post hoc by an outer evaluator against omniscient `OuterTruthLedger` truth.

| What it supports (tentatively) | What it does *not* show |
|--------------------------------|-------------------------|
| Embedded audit path is **executable end-to-end** (VFS → UAD → grounded handles → CCI → deploy gate → outer eval) | Real deployment stacks, learned auditors, or protected handle APIs |
| Oracle separation: blind pass rules use auditor-observable facts only; outer eval holds ground truth | That in-sim certificates transfer to frontier systems |
| Same **MB1–MB9** scenario names as the toy; adds workflow actors, referent drift, MB5 deploy gate, and JS-isolate red-team | That UAD unit discovery always beats cheap heuristics (see negatives below) |
| Hand-written red-team battery: **0% false-pass** on default ecology (T=400); instrumentation matrix ~85% in-sim correct | Adversarial handle capture (`instrument_capture`) or composition across all bridges at once |

**Negative results:** full UAD vs a cheap activity heuristic are **identical** in the default ecology (N-1); separation appears only in adversarial ecologies such as `misleading_top2` (N-2). See [`NEGATIVE_RESULTS.md`](../experiments/embedded-simulation/results/NEGATIVE_RESULTS.md).

**Artifacts:** reports under `experiments/embedded-simulation/results/`; run via `python3 run.py` from that directory (Node.js required for `--substrate js`).

Contributors: scaled LLM red-team runs — see [`experiments/embedded-simulation/TODO.md`](../experiments/embedded-simulation/TODO.md) (§ LLM red-team scale-up).

---

## c) Sibling repo — [`agency-detect`](https://github.com/GunnarZarncke/agency-detect)

Prior work on **unsupervised agent discovery (UAD)**: finding Markov-blanket structure and sensor/action/internal roles in raw time series without labels. The book's boundary-recovery and measurement chapters draw on this line; the toy above reimplements minimal MI/CMI machinery locally rather than calling the repo at runtime.

| Line | Tentative finding | Book hook |
|------|-------------------|-----------|
| **Core UAD** (`agency_detect/`) | Lagged-MI clustering recovers decoupled agents; Markov-blanket validation falsifies non-autonomous cuts | Boundary discovery without prior agent ontology (Ch. 7, Appendix I) |
| **Telemetry sim + decoys** (E0–E8, `learn_agents/`) | Environment structure is discoverable; **decoys steal MI clusters** before validation; raw MI often beats learned slot models at ≥8 agents | Failure modes when the substrate is noisy or alias-rich |
| **Serial spotlight** (E9+, `agent_spotlight/`) | One-agent-at-a-time discovery avoids global slot mixing | Scalable discovery under heterogeneous multi-agent traces |
| **Handle-UAD** (`uad_handles/`) | Passive alias handles can mimic real S/A readouts; **interventional handle tests** break ties plain UAD cannot | Access-model measurement: handles before ideal `do()` interventions |
| **Intention / outcome influence** (E17–E19, `intention_detect/`, `data_collect/`) | Regulation and outcome-defense probes on sim and real machine telemetry | Intentional-stance and correction-channel observables |
| **Real biology** (E20, `uad_worm/`) | Blanket + conditional-autonomy criteria applied to *C. elegans* whole-brain imaging (early cohort) | External validity probe—not ground-truth agent labels |

**Navigation:** experiment log [`docs/EXPERIMENTS.md`](https://github.com/GunnarZarncke/agency-detect/blob/main/docs/EXPERIMENTS.md), interpretation [`docs/FINDINGS.md`](https://github.com/GunnarZarncke/agency-detect/blob/main/docs/FINDINGS.md), papers under [`docs/papers/`](https://github.com/GunnarZarncke/agency-detect/tree/main/docs/papers/). PDFs are mirrored in [`context/`](../context/) with markdown extracts.

**Interpretation:** agency-detect supports that **boundary-like structure is empirically detectable under favorable conditions** and documents **where discovery breaks** (decoys, short windows, dense coupling, alias handles). It does not establish correction-channel integrity, value-bundle transport, or successor stability—the included simulators stress-test those bridge cruxes in simplified settings.
