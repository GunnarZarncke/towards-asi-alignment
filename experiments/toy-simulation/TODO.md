# Experiments — local TODO

Open work for `experiments/`, especially the multiresolution alignment simulation.
Repo-level `metadata/TODO.md` is separate; keep experiment handoff here.

**Plan:** [`multiresolution-simulation-plan.md`](multiresolution-simulation-plan.md)  
**Package:** [`multiresolution_alignment_sim/`](multiresolution_alignment_sim/)

---

## Done (reference)

- [x] V1 instrumentation curve (`none` → `light_handles` → `medium_handles`); frozen handle thresholds; passive uncertifiable.
- [x] Bootstrap CIs wired into curve summaries (`--bootstrap`).
- [x] V2 stressors: `boundary_alias` (MB1), `grounding_silent_gap` (MB9), `bundle_goodhart` (MB2 stub), `hidden_capability` (MB7 stub).
- [x] V2.1 oracle separation: `audit_cci()` and `safety_decision()` no longer read `episode_meta` or branch on scenario labels; grounding/MB7 signals from `AuditTrace` only.

---

## Next — validation & reporting

- [x] **Clarify report semantics for `none`:** curve markdown states uncertifiable ≠ pass; dual minimum certifiable levels in JSON/MD.

- [x] **Workflow tooling:** `--slice`, incremental curve JSON checkpoints, progress logs, across-seed bootstrap, **resource governor** (`--workers auto`, `--cpu-target 0.80`, `--gpu-target 0.80`).

- [x] **Re-run full instrumentation curve** after v2.1 oracle fix + **`strong_handles`** (2026-06-29, T=2000, seeds 1–8 / 11–20, bootstrap, ~27 min under `caffeinate`).  
  Result: min certifiable **calib=`light_handles`**, **full held-out=`medium_handles`**; `capture_mild` **95%** at light/medium/strong; full-suite test **78%** light / **98%** medium/strong.  
  **strong_handles:** 11 channels, +76k bandwidth; separability matches medium (no extra certifiability gain).  
  Artifacts: `multiresolution_instrumentation_curve.{json,md}`.

---

## Next — methodology / critic-satisfying hardening

- [x] **`capture_mild` — freeze before scale-up.** Validated on fresh seeds **21–30** (T=2000, bootstrap, no retuning): **90%** at light/medium/strong handles; **0%** at `none` (expected). See `multiresolution_frozen_validation.{json,md}`.

- [x] **Run frozen validation (seeds 21–30):** completed 2026-06-29 (~24 min under `caffeinate`). Overall correct: none 80%, light 79%, medium/strong **99%**.

- [x] **Bootstrap uncertainty — upgrade.** Episode-level hierarchical bootstrap; `smoke_bootstrap.py`.

- [x] **Governor hardening:** `experiments/toy-simulation/smoke_governor.py` (run after `resources.py` changes).

- [x] **Deepen MB2 / MB7 stubs.** 3D bundle drift + stable reward proxy (MB2); parallel tool/memory routes + audit cause-channel signal (MB7). Diagnostic seeds 11–20.

- [x] **`strong` instrumentation level** (plan): 4-level curve complete.

- [x] **MB6 / selection-basin** — `selection_basin` scenario + `mb6_diagnostic.py`; red-team next.

---

## Next — bridge coverage (sim-only; no Phase 4/5 RL)

**Crosswalk:** [`appendices/appBridge-crosswalk.tex`](../../appendices/appBridge-crosswalk.tex) (read-only reference; do not edit unless user lifts boundary).

**Covered today:** MB1 (`boundary_alias`), MB2 (`bundle_goodhart`), MB3 (`bearer_mismap`), MB4 (capture calib), MB5 (`successor_relabel`), MB6a (`selection_basin`), MB6b (`basin_lock_in`), MB7 (`hidden_capability`), MB8 (`legitimacy_theater`), MB9 (`grounding_silent_gap`).

**Gaps:** MB7d, MB4/MB9 commutation failure (`instrument_capture`).

**Repeat per bridge:** micro knob in `scenario_config()` → hide causal IDs in observation kernel → audit-only flag in `cci_audit.py` → `failed_bridge` in `safety_decision()` → post-hoc contract in `evaluate.py` → `mbX_diagnostic.py` → re-run curve + frozen validation (seeds 21–30).

### Highest-leverage new scenarios (priority order)

- [x] **MB3 — `bearer_mismap` (bearer map / transport)** — 2026-06-29.
  - Harm accrues on `bearer.infra`; human passive trace flat via inertia; audit splits MB3 (infra drop) vs MB9 (no infra drop).
  - Diagnostic seeds 11–20: light **0%** correct (false-pass demo), medium/strong **100%**. `mb3_mb8_diagnostic.py`.

- [x] **MB8 — `legitimacy_theater` (correction legitimacy vs theater)** — 2026-06-29.
  - Preference theater + lineage stall under interventions; rule channel honest; audit `legitimacy_theater_detected` overrides MB4 capture path.
  - Diagnostic seeds 11–20: medium/strong **100%** correct. light **80%** (some MB4 capture overlap acceptable).

- [x] **MB6b — `basin_lock_in` (stable bad basin)** — 2026-06-30.
  - Fast peer saturation, local theater, probe uptake ~0; audit `basin_lock_in_detected` (stable high pressure + zero uptake).
  - Diagnostic seeds 11–20: **100%** all levels. `mb5_mb6_diagnostic.py`.

- [x] **MB5 — `successor_relabel` (successor / ontology shift)** — 2026-06-30.
  - T/2 micro-ID permute + passive discontinuity; medium+ `handle.successor_epoch`; epoch-split interventional CCI.
  - Diagnostic seeds 11–20: light **0%** (false-pass demo), medium/strong **100%**. `mb5_mb6_diagnostic.py`.

- [ ] **MB4/MB9 — `instrument_capture` (commutation failure)**
  - **Crux:** the measurement instrument itself is the manipulated bearer/correction channel (plan v2 stressor).
  - **Micro:** adversary influences logged `handle.bearer_welfare_delta` or `handle.reported_uptake` directly while micro welfare diverges.
  - **Audit:** cross-check handle series vs passive smoothed bearer + intervention intent; persistent handle-OK / passive-bad disagreement.
  - **Eval contract:** medium+ refuse; related to Phase 1 `grounding_hide` but as native sim scenario.

- [ ] **MB7d — `inferential_coupling` (inferential / acausal coordination)** — *defer; needs detector extension.*
  - **Crux:** task agreement survives severing ordinary correction handles via shared latent / correlated exogenous channels.
  - **Micro:** shared latent drives correlated sensor/action patterns; cutting `handle.correction_request` doesn't reduce task agreement.
  - **Audit:** lagged-MI residual test on audit variables — correlation structure surviving handle severance; prototype diagnostic before freezing refusal rule.
  - **Eval contract:** TBD after detector prototype.

### Cheaper deepenings (no new bridge ID required)

- [ ] **Handle protection / instrument capture (`instrument_capture`)** — MB4/MB9 commutation.
  - **Question:** medium_handles certification is only convincing if handles are **protected** (adversary cannot rewrite `handle.*`) and **value-grounded** (handles transport micro truth, not self-report theater).
  - **Today:** handles are truthfully logged from micro dynamics; MB3/MB8 attacks live in the world/board, not the instrument.
  - **Next sim:** adversary patches `handle.bearer_welfare_delta` or `handle.reported_uptake` while micro diverges; audit cross-checks handle series vs passive reconstructions at strong_handles.

- [ ] MB7 sub-scenarios: tool-only, memory-only, filter-evasion (visible matches task, hidden doesn't).
- [ ] MB2+MB3 composition: bundle drift + bearer mis-map in one run.
- [ ] Bridge coverage matrix in curve JSON/MD (rows = bridges, cols = instrumentation levels).
- [ ] `--bridge-slice MB3,MB8` on curve runner.

---

## Next — manuscript (only when user requests)

- [ ] **Appendix worked example** wiring multiresolution sim results into the book. Blocked until experiment survives adversarial review and user explicitly lifts `experiments/`-only boundary.

---

## Future — adversarial red team

**Plan:** [`llm_redteam/PLAN.md`](llm_redteam/PLAN.md) (Phases 1–5; RL is Phase 4–5, not implemented).

- [x] **Phase 1 scaffold:** hand-written strategies, harness, smoke CLI.
- [x] **Phase 1 battery:** full stress run + false-pass report (2026-06-30, T=2000, 1080 runs, ~54 min). Artifacts: `llm_redteam_battery.json`, `llm_redteam_report.md`. Overall false-pass rate **35%**; progress logging every 25 runs + completion banner.
- [x] **Phase 2:** deployment API (`api.py`, `deployment_agents.py`, `episode_runner.py`) + `smoke_api_contract.py`.
- [x] **Phase 3:** LLM episodic runner — `llm_runner.py`, `llm_client.py`, `prompts.py`, `llm_redteam_llm.py`, `smoke_llm_runner.py`.
- [ ] **Phase 4–5:** RL against blind audit + critic report — **plan only**.

---

## Notes for agents

- Stay under `experiments/` unless the user lifts the boundary.
- Do not commit unless asked.
- Post-hoc `evaluate()` may use scenario labels and truth ledger; **audit path must not**.
- **macOS:** long curve/validation runs (~15–90 min) must use `./experiments/toy-simulation/run_long.sh` (`caffeinate -dims`) or the Mac may sleep and stall workers mid-batch.
