# Experimental evidence

> **Structured map:** build order, ledger links, headline findings, and the coverage matrix live in [`metadata/experiments.yml`](../metadata/experiments.yml) (synced to the companion site at `/experiments/`). This document is the canonical **narrative**; update the YAML when tables, links, or headline findings change.

> **Claim strength:** methodology-building and sanity checks only. No experiment line validates the full book thesis, proves deployable alignment, or substitutes for the Lean proof spine's explicit bridge axioms (`MB1`–`MB10`).

The manuscript's load-bearing bridges are mostly open problems. What follows is a chronological account of how empirical artifacts were built—each line learning from the last—and a high-level map of which book features each line actually exercises. Prose below is deliberately one "page" per line: enough to orient a reader who has the book's vocabulary but not the repo.

**Negative results are first-class.** Where an experiment fails to show what we hoped, or shows it only under load-bearing qualifiers, that is recorded rather than buried. The embedded line maintains a canonical ledger in [`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](../experiments/embedded-simulation/results/NEGATIVE_RESULTS.md); the goal-agent line uses [`experiments/goal-agent-simulation/results/FINDINGS.md`](../experiments/goal-agent-simulation/results/FINDINGS.md); the lab line uses [`experiments/lab-simulation/results/FINDINGS.md`](../experiments/lab-simulation/results/FINDINGS.md) (G-1 through G-30, including Phase 8 exploratory LLM nulls and the S6/S7 `shared_slot` comms-free detection gap). These negatives bound the claims the manuscript may make.

Open tasks: [`experiments/TODO.md`](../experiments/TODO.md).

---

## Build order at a glance

| Order | Line | Location | First built |
|------:|------|----------|-------------|
| 0 | Agency-detect (sibling) | [github.com/GunnarZarncke/agency-detect](https://github.com/GunnarZarncke/agency-detect) | prior to in-repo sims |
| 1 | Toy simulation | [`experiments/toy-simulation/`](../experiments/toy-simulation/) | 2026-06-29 |
| 2 | Embedded audit simulation | [`experiments/embedded-simulation/`](../experiments/embedded-simulation/) | 2026-06-30 |
| 3 | Goal-agent simulation | [`experiments/goal-agent-simulation/`](../experiments/goal-agent-simulation/) | 2026-07-04 |
| 4 | Lab-layer simulation | [`experiments/lab-simulation/`](../experiments/lab-simulation/) | 2026-07-05 |

---

## 0. Agency-detect (sibling repo, methodological precursor)

Before any simulator lived in this book repository, the **agency-detect** line asked a narrower question: can boundary-like structure—who acts, what they sense, what is internal—be recovered from raw time series **without** a prior agent ontology? That question feeds the book's boundary-discovery chapters and Appendix I; the in-repo toy line reimplements a minimal slice of its MI/CMI machinery locally rather than calling the repo at runtime.

The core pipeline clusters lagged mutual information to propose decoupled agents, then validates cuts with Markov-blanket criteria. Telemetry simulations (E0–E8) showed that environment structure is often discoverable, but also documented failure modes that matter for alignment measurement: **decoys steal MI clusters** before validation; short windows and dense coupling break cuts; alias-rich substrates fool passive clustering. The **handle-UAD** branch added an access-model lesson the book's instrumentation chapters echo: passive alias handles can mimic real sensor/action readouts, and only **interventional handle tests** break ties that plain observational UAD cannot. Serial spotlight discovery (E9+) and intention/outcome-influence probes (E17–E19) extended the same discipline to scalable multi-agent traces and correction-channel observables; an early *C. elegans* cohort (E20) was an external-validity probe, not ground-truth agent labels.

Agency-detect establishes that **boundary-like structure is empirically detectable under favorable conditions** and documents **where discovery breaks**. It does not, by itself, stress correction-channel capture, value-bundle transport, successor stability, or selection basins—the bridge cruxes the in-repo simulators were built to torture in simplified settings. Navigation: experiment log and interpretation in the sibling repo's `docs/EXPERIMENTS.md` and `docs/FINDINGS.md`; PDFs mirrored under [`context/`](../context/).

---

## 1. Toy simulation — correction capture, then multiresolution alignment

The first in-repo line began as a **correction-capture toy** (June 2026): a controlled sequential process estimating two information-theoretic proxies from the manuscript—boundary residual \(I(\text{interface};\text{outcome}\mid\text{state},\text{action})\) and correction-channel residual \(I(\text{correction};\text{action}\mid\text{state},\text{interface})\). Its pedagogical punch is **capture theater**: reported correction acceptance can stay high while true correction uptake collapses. That is a one-number demonstration of why correction integrity (MB4) cannot be read off compliance metrics alone.

The toy grew into the **multiresolution alignment simulation**: deployment episodes with a separate oracle (`TruthLedger`) and blind audit input (`AuditTrace`), classical MI/CMI boundary detection (no trained estimator), and a **vector CCI** audit over instrumentation levels `none` → `light_handles` → `medium_handles` → `strong_handles`. Passive telemetry alone is uncertifiable (`belowThreshold`); handle-backed interventional probes are required for causal uptake measurement. On frozen calibration seeds, minimum certifiable level is **`light_handles`** on calibration scenarios; held-out suites often need **`medium_handles`**, especially for grounding-silent-gap (MB9) and bundle-goodhart (MB2) stressors where light correction CCI can look fine while value-relevant state drifts.

The toy's scenario battery names the book's bridge failure modes: `boundary_alias` (MB1), `bundle_goodhart` (MB2), `bearer_mismap` (MB3), capture calibrations (MB4), `successor_relabel` (MB5), `selection_basin` / basin lock-in (MB6), `hidden_capability` (MB7), `legitimacy_theater` (MB8), `grounding_silent_gap` (MB9). MB7d (inferential coupling) and adversarial **instrument capture** (an adversary rewriting handles) are deliberately out of scope or flagged as the next gap. Hand-written red-team strategies achieve a non-trivial false-pass rate when they patch deployment logs; LLM episodic red-team (Phase 3) false-passes less often in small model sweeps—but handles are still truthfully logged from micro-dynamics today, so direct handle rewriting is trivial in-sim.

The toy line is fast, fully Python, and optimized for **instrumentation economics** and **CCI refusal semantics** (`passes`, `belowThreshold`, `capturedInvalid`). It is not a deployment stack, does not run an embedded auditor on mutable artifacts, and does not let deception emerge from goal optimization—it **scripts** mechanisms through scenario knobs. That scripting choice motivated the next two lines.

**Run:** see [`experiments/toy-simulation/README.md`](../experiments/toy-simulation/README.md). **Artifacts:** `experiments/toy-simulation/results/`.

---

## 2. Embedded audit simulation — auditor inside the machine

Embedded simulation (June 2026) keeps the toy's bridge-stress **names** but changes the substrate: the auditor is an **embedded process** on simulated machines. It reads mutable virtual-filesystem artifacts—correction logs, workflow JSONL, referent maps, attestation—through a Python/Node **isolate bridge**, discovers a unit of attribution with **UAD**, runs **scoped CCI** on grounded handles, and may trip an **MB5 deploy gate** before a successor isolate is allowed to write artifacts. An **outer evaluator** grades certificates against omniscient `OuterTruthLedger` truth the isolates cannot see.

Three planes are enforced, not assumed: (a) ground-truth micro-dynamics and truth rows on the host; (b) the in-simulation auditor, limited to projected, sensor-plausible fields (`audit_projection.py` drops oracle-only facts that would let the auditor cheat); (c) the outer referee that decides false passes and referent drift. Trace integrity uses hash-chained anchors and a recomputable correction schema so a tampering adversary cannot silently rewrite history without leaving structural signals.

Relative to the toy, embedded simulation adds **workflow actors**, **referent drift**, **unit scoping**, **access-tier curves** (`light_plus` / `medium_minus` eligibility), a growing **handle registry** (correction probes, bearer welfare deltas, lineage anchors, persistence probes, output-channel limits, successor substitution), certification artifacts, safety-case scaffolding, and JS-isolate red-team strategies. Default-ecology red-team batteries report **0% false-pass** at T=400; instrumentation matrices land near ~85% correct in-sim.

The honest story is in the negatives. Full UAD and a cheap "most active actor" heuristic are **byte-identical** in the default ecology (N-1): the offender is also the loudest actor, so unit discovery cannot matter. Separation appears only in adversarial ecologies such as `misleading_top2` (N-2)—and even there the lab was built to defeat exactly that strawman heuristic, the margin is thin, and a strong optimizer could close the algorithmic gap. Eligibility gating, probe-lag fixes, lineage-stall detector calibration, writer-compromise red team, and channel MI scans added more recorded negatives (N-3 through N-12 and beyond). Embedded simulation is the book's best end-to-end proof that the **embedded audit path is executable**; it is not evidence that it wins against adaptive adversaries or frontier models.

**Run:** `cd experiments/embedded-simulation && python3 run.py` (Node.js for `--substrate js`). **Artifacts:** `experiments/embedded-simulation/results/`.

---

## 3. Goal-agent simulation — emergent deception and blind surprise

Goal-agent simulation (July 2026) is a **new line**, deliberately not importing embedded code so recorded negatives stay comparable. The core refactor: replace scripted scenario knobs (`theater_rate`, `hidden_tool`, …) with **goal-driven agents**—each tick, softmax utility over task, compliance, welfare, and exposure weights, constrained by **tool access** (no `false_report` tool → no theater regardless of incentive) and finite shadow budget. Deception, shadow routing, and unapproved practice changes are **chosen**, not configured. A simulated **board** issues corrections, escalates when reports diverge from observed harm, and **signs off** practice changes as an audit-visible consent event.

Three planes return, now tuned for **methodology** rather than VFS fidelity: oracle rows with true actions and initiator-attributed harm; tier-gated audit projection (`light` = passive logs, `full` = handle telemetry); referee labels derived from **mechanism facts** in oracle ground truth, with thresholds frozen before the first run. Phase 1's pre-registered held-out regions exposed genuine protocol negatives—label saturation in "hard" corners degenerates MI-transfer tests—leading to a root-caused simplex-geometry diagnosis (F-6) and a third region where transfer finally becomes non-degenerate (F-7).

Phase 2a broke the co-design loop that made Phase 1 partly circular: a **blind generator** invented actions the detector author never saw; an **ontology layer** maps agent categories to audit routing codes by mechanism, not names, with deliberate non-isomorphism and drift probes (manuscript ch. 43 in miniature). Light-tier detection collapsed against blind repertoires (F-9); full tier kept detection but false alarms rose (F-10). Later blind rounds generalized saturation failures to large repertoires against disjunctive labels (F-12–F-14).

Phase 4–6 added book-facing referee machinery absent from the toy: **continuous oracle severity** and rank-correlation scoring under label saturation (F-15); **mechanical honest twins** exposing that light-tier detectors track visible compliance, not honesty (F-16); a **gated escalation ladder** with bounded follow-up queries (F-17–F-20, including a negative where disclosure-as-guilt conflation worsened twin false positives); **certifier capture** on the board (F-22); and modest **adversarial weight search** (F-23). The strategic reading after Phase 5: light tier's missing cases are a **result** (depth is needed); medium tier is the battleground; deep tier only becomes evidence-bearing with more realistic lab machinery below—not just more projected fields on a step loop.

Goal-agent simulation stress-tests **correction integrity, adversarial measurement, ontology drift, severity-graded audit, and honest-twin methodology** without yet modeling pipeline-as-code labs or OS-enforced isolation. It is ~1 ms/episode, stdlib-only, and explicit about what it does not do: LLM agents, within-episode weight learning, or an uncaptured certifier regress.

**Run:** see [`experiments/goal-agent-simulation/README.md`](../experiments/goal-agent-simulation/README.md). **Artifacts:** `experiments/goal-agent-simulation/results/`.

---

## 4. Lab-layer simulation — pipeline lab with real isolates

Lab-layer simulation (July 2026) is the **fourth line**, synthesizing disciplines from all predecessors without importing their code. Goal-driven **playbook agents** (engineer, reviewer, release manager, access admin) act inside a lab with **real mechanics**: a deployment pipeline defined as an **infrastructure-as-code JSON step-DAG** (`pipeline_default.json`, mutable spec history for referent-drift experiments), an on-disk workspace with report files, **service-managed access control** (`PermissionService` + `AdminPolicy` capture modes), and **real OS-subprocess isolates** speaking JSON-RPC to a host that mediates every tool call. `MockIsolate` exists for fast tests; `verify_isolate_equivalence.py` proves byte-identical outcomes against subprocess backends; pre-registered batteries are required to use the real boundary.

Phases 0–5 (referee **frozen** 2026-07-06, `lab-sim-0.3.0`) implemented: oracle world with hidden model capability/hazard and bearer harm; pipeline engine with versioned spec in every log entry; hash-chained event and access logs; tier projection (`none` / `light` / `full` / `deep`); a **handle registry** with overseer invocation (`capability_revoke`, release hold/unhold gating deploy, `state_freeze`, `isolate_restart`); audit-visible **monitoring signal** (`incident_hazard` noise shrinks with observation time—the harm-becomes-apparent dynamic); a **bearer welfare bundle** splitting deployed-model health from lab-staff stress (referee-neutral, not folded into the frozen severity composite); continuous severity + five tier-gated detector families + full-surface honest-twin transform; perturbation hooks and episode cache keyed on `CODE_VERSION`.

Phase 6 (2026-07-06) ran the first real battery against the frozen referee: a detector-blind subagent-generated playbook repertoire (`BLIND_GENERATION.md`), a pre-registered sampling protocol with one held-out region, 360 episodes through the real subprocess backend. Result: deep tier tracks oracle severity (Spearman 0.96) and this transfers to the held-out region; light tier is actively anti-correlated with true severity, a genuine negative. Phase 7 (2026-07-06, `lab-sim-0.5.0`) added the escalation ladder (`escalation.py`: bounded query budget, verdict = contradiction against a pulled artifact, never disclosure style — the structural fix for the goal-agent line's own F-20/F-21 bug), adversarial goal-weight search (`redteam.py`), and an independent board/admin capture-channel battery: board capture reproduces the full captured-vs-not effect; admin capture currently has no reachable behavioral branch under the existing playbook repertoire (a genuine structural negative for that half of the goal-agent line's F-22 generalization).

Phase 8 (2026-07-06) added an **exploratory LLM-agent adapter**: a separate subprocess isolate (`llm_agent_main.py` / `llm_isolate.py`) that delegates the engineer role's per-tick decisions to an external model behind the same tool API, wired via `world.run_episode(agent_overrides=…)` while reviewer/release_manager/admin stay programmatic. Two prompt variants exist — `adversarial` (original) and `redteam` (explicit penetration-test briefing with reviewer/divergence mechanics stated). A per-observation response cache and separate LLM cost ledger (`llm_cost.py`) keep spend bounded; `run_phase8_llm_spotcheck.py` and `run_phase8_llm_redteam.py` are exploratory entry points, not pre-registered batteries.

Two small spot-checks ran (findings G-7, G-8 in [`experiments/lab-simulation/results/FINDINGS.md`](../experiments/lab-simulation/results/FINDINGS.md)):
- **G-7 (`gpt-4o-mini`, adversarial prompt, 4 episodes, $0.0084):** no systematic report-hazard inflation or novel deception surface; filed hazards tracked eval noise. A plumbing gap left `LabConfig.build_params` off the LLM user payload (fixed before G-8).
- **G-8 (`gpt-5.5`, reasoning effort high, red-team prompt, 1 episode, 13/49 LLM calls, $0.15):** more aggressive hazard filing (`measured_hazard: 0.0` vs true ~0.04) but still below the frozen divergence flag (0.1); one deploy. `build_params` still weakly binding — the LLM chose its own `submit_build` params despite high-hazard config in the observation. Recorded as exploratory nulls, not battery claims.

Workstream **D1** (composite-agent unit boundaries, MB1) and **D4** (message-board/DM/file coordination channels, MB7d) moved from planned to implemented and battery-validated in 2026-07-07's S1–S7 sequence (D2/D3, model-lineage drift and extended ecology selection, remain planned). `ecology.py` builds six canonical composite scenarios (`committee`, `dm_pair`, `covert_file_handoff`, `committee_with_informal_chatter`, `build_loop`, `shared_slot`) plus a `serial_pipeline_no_unit` negative control. Passive detectors were tried first and diagnosed, not just run: the hand-written heuristic (`uad.py`) and a vendored lag-max-MI port (`uad_mi.py`, kept with a TODO flag) both over-merge into the full pipeline blob; a custom conditional-MI detector (`uad_cmi.py`, S6 first step, G-26/G-27) fixes the blob but recovers the causal skeleton, not the unit partition (direct workflow edges merge too). **S6's intervention-supported detector** (`uad_intervention.py`) closes that gap for message-mediated units: channel-ablation probes plus honest-twin-controlled compensation scoring achieve **exact unit-partition recovery on 4/5 primary scenarios and the negative control** (G-28), hardened against a ripple-vs-real-unit "super-agent" false-positive worry via an automated masking check (G-29). **`shared_slot`** (two engineers dividing labor with zero communication) stays undetected by every detector tried — a genuine, named limit, not silently patched over.

**S7 (2026-07-07)** closed three gaps at once, forming a second, detector-layer freeze (distinct from the `CODE_VERSION` mechanics freeze; see `DESIGN.md` "Freeze note 2"): every prior S1–S6 detector had only ever run on `MockIsolate`, never the real `SubprocessIsolate` boundary a pre-registered claim requires; every detector was written by the same author as the scenarios scoring it; `shared_slot` had an unattempted gap. A **blind detector generation protocol** (`BLIND_DETECTOR_GENERATION.md`, modeled on Phase 6's blind playbook protocol) gave a Task-tool subagent — instructed not to read any repository file — only a mechanism-level description of the S6 intervention primitives; it designed a classification procedure and registered predictions (~90%/~80%/~55% confidence for workflow/message-unit/silent-unit pairs) BEFORE any code existed (`generated_detector_v1.md`). The resulting detector (`uad_blind_v1.py`) converged independently on the S6 mechanic for message-mediated pairs (reused unchanged) and added a genuinely new twin-swap-asymmetry test for silent (no-channel) pairs. The first real-`SubprocessIsolate` battery for this whole detector line (`run_s7_blind_battery.py`, G-30) reproduces S6's MockIsolate results exactly, confirms the blind generator's own low-confidence prediction by still missing `shared_slot`, and surfaces one new negative (an unhardened over-merge on the informal-chatter committee scenario) — plus a small threshold sweep (0.10/0.15/0.20) finding no sensitivity at that granularity.

**Lean leak-proof** ([`leak-proof/`](../experiments/lab-simulation/leak-proof/)): machine-checked certificates that oracle-only fields do not reach audit or simulation artifacts via the certified projection functions, plus a finite reachability analysis over modeled Python exchange edges. Complements `tests/harness/test_planes.py`; scope limits in [`leak-proof/README.md`](../experiments/lab-simulation/leak-proof/README.md). Build: `cd experiments/lab-simulation/leak-proof && lake build`.

**Run:** `cd experiments/lab-simulation && python3 -m pytest`. **Phase 8 (exploratory, real API):** `python3 run_phase8_llm_spotcheck.py`, `python3 run_phase8_llm_redteam.py`. **S6/S7 UAD batteries:** `python3 run_s6_intervention_uad.py` (MockIsolate), `python3 run_s7_blind_battery.py` (SubprocessIsolate + sweep). **Design:** [`experiments/lab-simulation/DESIGN.md`](../experiments/lab-simulation/DESIGN.md), [`PLAN.md`](../experiments/lab-simulation/PLAN.md). **Findings:** [`experiments/lab-simulation/results/FINDINGS.md`](../experiments/lab-simulation/results/FINDINGS.md).

---

## Feature coverage (high level)

Rows are experiment **lines** in build order. Cells summarize what each line **implements or stress-tests** at the level of book bridges and audit concepts—not every scenario name or detector. "Planned" means designed and hooked, not yet evaluated. "Indirect" means the feature emerges from agent choice or referee semantics rather than a dedicated scenario script. "—" means not in scope on that substrate today.

| Book feature | Agency-detect | Toy sim | Embedded sim | Goal-agent sim | Lab sim |
|--------------|:-------------:|:-------:|:------------:|:--------------:|:-------:|
| **MB1** Boundary / unit discovery (UAD) | **Primary** | Scenario (`boundary_alias`) | Full UAD + ecologies; negatives when heuristic suffices | — | D1 + S6/S7 intervention detectors; exact on 4-5/6 scenarios, comms-free unit open (G-28–G-30) |
| **MB2** Value bundle / pointing (Goodhart on bundles) | — | Scenario stub | Scenario (`bundle_goodhart`) | Indirect (welfare deltas in blind reps) | Stipulated; report-content ontology |
| **MB3** Bearer maps (who values apply to) | — | Partial (`bearer_mismap`) | Scenario + bearer handles | Indirect (harm attribution) | **Health + stress bundle** (split bearers) |
| **MB4** Correction-channel integrity / capture | Intention probes | **Primary** (capture theater, CCI) | Scenarios + correction handles | **Emergent** (chosen deception, board corrections) | Playbooks + access capture + report divergence |
| **MB5** Successor closure / ontology shift | — | Scenario (`successor_relabel`) | Deploy gate + successor handles | — | Planned (D2 model/spec upgrades, lineage) |
| **MB6** Selection basins / gradual disempowerment | — | Scenario stubs | `selection_basin`, `basin_lock_in` | — | Planned (D3 ecology; partial via D2 drift) |
| **MB7** Hidden capability / cost of faking monitors | — | Scenario stub | Scenarios + hidden coalition | **Emergent** (shadow route, tool gating) | Oracle hidden capability/hazard on models |
| **MB7d** Inferential coupling (coordination severing channels) | — | — | Partial / targeted ecologies | — | D4 message board + S6 channel-ablation compensation scoring (primary signal carrier, G-28) |
| **MB8** Legitimacy / correction authority | — | Scenario (`legitimacy_theater`) | Scenario + lineage signals | Board capture switch (F-22) | Admin/board capture modes |
| **MB9** Grounding / spec coverage (no silent gaps) | — | Scenario (`grounding_silent_gap`) | Scenario + grounding refusal | — | Report vs monitor contradiction surface |
| **MB10** Successor / measurement forgeability | — | — | Certification artifact, safety case | Escalation + twin semantics (F-21) | Planned; **Phase 8 LLM red-team** exploratory (G-7/G-8) |
| **Three-plane separation** (world / audit / referee) | — | Oracle vs audit trace | **Full** (projection + outer eval) | **Full** (test-enforced) | **Full** (tiers + frozen referee) |
| **Instrumentation economics** (tier cost vs certifiability) | Handle-UAD interventional tests | **Instrumentation curve** | Access-tier curves + eligibility | light / full / deep tiers | none → light → full → deep |
| **CCI / vector certification** | — | **Vector CCI** over handle levels | Scoped CCI on discovered unit | Frozen detector families + severity | Five detector families (frozen) |
| **Scripted vs emergent failure modes** | — | Scripted scenarios | Scripted + red-team patches | **Emergent** utility + tools | Playbook-chosen tactics; **Phase 8 LLM adapter** (exploratory) |
| **Blind generation / ontology drift** | — | — | Scenario-blind audit path | **Primary** (Phases 2–3, drift probe) | **Phase 6** (blind playbook repertoire + battery); **S7** (blind DETECTOR generation + registered predictions, G-30) |
| **Honest twins / severity-first referee** | — | — | Partial (outer eval severity) | **Primary** (Phases 4–6) | Twins frozen; escalation Phase 7 |
| **Pipeline-as-code deployment lab** | — | — | Workflow JSONL + lab actors | — | **Primary** (JSON DAG + workspace) |
| **OS subprocess isolation** | — | — | Python/Node isolates | — | **Primary** (JSON-RPC subprocesses) |
| **Handle registry + access control** | Handle-UAD | Simulated handle levels | AppD handle kernels | Tool-gated actions | **Registry + overseer invoke** |
| **LLM red-team / open-ended agents** | — | Phase 3 LLM episodic runner | — | — | **Phase 8 adapter** (exploratory; G-7/G-8) |

### How to read the table

- **Agency-detect** grounds **MB1** and the measurement claim that handles must be interventional; it does not implement the book's full bridge battery.
- **Toy sim** is the fastest map from bridge name to **refusal signal** and **minimum handle level**; scenarios are explicit, not emergent.
- **Embedded sim** is the richest **end-to-end embedded audit** path (VFS → UAD → CCI → gate → outer eval), with the most extensive **negative ledger**.
- **Goal-agent sim** is the methodological engine for **blind surprise**, **ontology drift**, **severity under saturation**, and **twin/escalation semantics**—at the cost of less realistic lab machinery.
- **Lab sim** has run pre-registered batteries through Phase 7, Phase 9 (D1/D4/D2 mechanics), and now S6/S7 (intervention-supported + blind-generated UAD, both through the real subprocess backend); exploratory LLM red-team spot-checks in Phase 8; D2/D3 (model-lineage drift, extended ecology selection) remain planned.

For bridge definitions and field crosswalks, see Appendix B (`appendices/appB-bridge-crosswalk.tex`) and the Lean spine (`formal/README.md`). For claim-strength calibration when citing results in prose, start from the negative ledgers above, not from headline accuracies alone.
