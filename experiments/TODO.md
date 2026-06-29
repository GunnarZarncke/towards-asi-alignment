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

- [x] **Governor hardening:** `experiments/smoke_governor.py` (run after `resources.py` changes).

- [ ] **Deepen MB2 / MB7 stubs.** Tuning prep done; tune sim knobs only if medium+ regresses on full seeds.

- [x] **`strong` instrumentation level** (plan): 4-level curve complete.

- [x] **MB6 / selection-basin** — `selection_basin` scenario + `mb6_diagnostic.py`; red-team next.

---

## Next — manuscript (only when user requests)

- [ ] **Appendix worked example** wiring multiresolution sim results into the book. Blocked until experiment survives adversarial review and user explicitly lifts `experiments/`-only boundary.

---

## Future — adversarial red team

**Plan:** [`llm_redteam/PLAN.md`](llm_redteam/PLAN.md) (Phases 1–5; RL is Phase 4–5, not implemented).

- [x] **Phase 1 scaffold:** hand-written strategies, harness, smoke CLI.
- [ ] **Phase 1 battery:** full stress run + false-pass report.
- [ ] **Phase 2:** deployment API types + contract tests (`PublicObservation` / `StepPatch`).
- [ ] **Phase 3:** LLM episodic runner (no learning).
- [ ] **Phase 4–5:** RL against blind audit + critic report — **plan only**.

---

## Notes for agents

- Stay under `experiments/` unless the user lifts the boundary.
- Do not commit unless asked.
- Post-hoc `evaluate()` may use scenario labels and truth ledger; **audit path must not**.
- **macOS:** long curve/validation runs (~15–90 min) must use `./experiments/run_long.sh` (`caffeinate -dims`) or the Mac may sleep and stall workers mid-batch.
