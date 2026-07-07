# 2026-07-07 — Lab-layer sim S5: real lag-max-MI UAD detector ported, re-run against S4

## Trigger

Continuation of the same-day session. PLAN.md's S5 backlog entry
(recorded earlier that day) named two probes, neither started: (1) port
the real lag-max-MI UAD detector from `embedded-simulation/embedded_sim/
uad_core/` into lab-sim and re-run it against S4's shared-slot finding
(G-20); (2) a new, unimplemented acausal-coordination (ICI) probe. User:
"Implement S5."

## Done

Implemented probe (1) only — the well-scoped "port + re-run" ask.
Probe (2) is explicitly new work (no existing formalization code
anywhere in the repo, per PLAN.md's own "Scope note"), left exactly as
scoped, not attempted.

- `lab_sim/oracle_only/uad_core/` (new package): vendored, byte-for-byte
  (except one import-path fix per file) copy of `embedded_sim/
  uad_core/detection.py`/`markov_blanket.py`/`config.py`, plus a local
  `info.py` carrying only the two `mutual_information`/
  `entropy_from_keys` functions those files actually call (copied from
  `embedded_sim/audit_core/info.py`). Vendored rather than cross-
  imported — this repo's four experiment lines are otherwise
  self-contained codebases with no inter-line dependency.
- `lab_sim/oracle_only/uad_mi.py` (new module, sibling to `uad.py`,
  same "own module, never touches frozen code" discipline as
  `collusion.py`/`playbook_claim.py`):
  - `build_lab_trace(tool_events, actor_ids, horizon=None)` — tool
    events → discretized trace rows (`"<actor>.step"`/`"<actor>.ok"`
    per tick), the SAME "several scalar vars per actor" shape
    `embedded_sim/uad_core/workflow_trace.py` uses.
  - `discovered_units_mi(result, actor_ids=None, tier="full",
    **detection_overrides)` — SAME `{coalition_id: tuple of actor_ids}`
    return shape as `uad.discovered_units`, so it plugs directly into
    the existing `uad_score` scoring path.
- `run_s5_uad_core_port.py`: re-ran the SAME `shared_slot_config`
  episodes `run_s4_shared_slot_prototype.py` already scored, sweeping
  the detector's `n_agents` (hard target cluster count) over 1-4, 10
  seeds each. Stated the over-merge hypothesis in the script's own
  module docstring BEFORE running it.
- **Result, confirming the hypothesis**: eng1/eng2 always land in the
  same cluster at every `n_agents` (1.0 merge rate), but that cluster is
  ALWAYS the full four-actor set `{eng1, eng2, rev1, rm1}` — never just
  the true pair (`eng1_eng2_isolated_from_rev_rm` rate: 0.0 at every
  `n_agents`). Fully deterministic across seeds.
- **Side finding**: `uad_score` itself has a blind spot — it only scores
  pairs within `true_units`' own actor set, so the fully-merged blob
  still reads `uad_score = 1.0` (a "perfect", misleading score). Needed
  a separate ad-hoc metric to see the over-merge at all.
- **Vendored-detector quirk caught, not patched**: `filter_weak_
  connections` silently drops any complete-linkage cluster of size ≤1
  (`continue`s past it, added to neither the filtered dict nor the env
  bucket) — 2 of 12 input variables (`rev1.ok`/`rm1.ok`) vanished from
  `detect_agents`'s output entirely in a debug run. Pre-existing in the
  vendored source, deliberately left as-is (vendored byte-for-byte, on
  purpose), just recorded.
- `results/FINDINGS.md` G-24; `PLAN.md` S5 section updated ("first probe
  implemented"); `README.md` status line, run-commands, layout, and a
  new S5 narrative paragraph.
- `tests/oracle_only/test_uad_mi.py`: 10 new tests — `build_lab_trace`
  unit tests (idle default, actor filtering, denied-call encoding,
  horizon padding/truncation, empty input), a synthetic-coupling sanity
  check directly on the vendored `detect_agents`, two
  `discovered_units_mi` end-to-end tests via a monkeypatched
  `build_audit_view` (perfect-coupling merge, empty-trace singletons),
  a golden test against a real `shared_slot_config` episode, and a pin
  on the vendored `DetectionConfig` defaults.
- `results/s5_uad_core_port.{json,md}` — the actual run output.

Final state: **359 tests green** (up from 349 before this task).

## Decisions

- Scoped to probe (1) only, not the ICI acausal-coordination probe —
  PLAN.md's own S5 entry already called the second probe "new work, not
  a port," with no existing implementation anywhere in the repo; adding
  a brand-new theoretical construct was judged out of scope for
  "implement S5" without the user separately weighing in, and the first
  probe alone was the well-defined, already-scoped "port" the section
  title names.
- Vendored the detector rather than importing `embedded_sim` directly
  from `lab_sim` — keeps lab-sim a self-contained codebase, matching
  every other experiment line's independence (no line in this repo
  imports another).
- Both `.step` and `.ok` were kept as separate per-actor variables
  (matching `workflow_trace.py`'s multi-variable-per-actor precedent)
  rather than folding into one variable, even though this can make an
  actor's own two variables the dominant correlation (documented as a
  scope note in `build_lab_trace`'s docstring, not silently chosen).
- `n_agents` was swept (1-4) rather than fixed at the library default
  (4) — it is a hard target cluster count, not a similarity threshold,
  and the merge/no-merge behavior genuinely depends on it in a way no
  existing heuristic ever exposed; sweeping was the only way to see
  that dependency at all.
- The vendored `filter_weak_connections` quirk (silently dropping
  size-≤1 clusters) was recorded, not patched — this port's whole
  premise is running the REAL upstream algorithm as a comparison point,
  not a lab-sim-flavored variant of it.

## Open / next

- The acausal-coordination (ICI) second probe from PLAN.md's S5 entry
  remains fully unimplemented (no code anywhere).
- Not explored: whether a different variable choice (e.g. `.step` only,
  or model_id-keyed variables instead of step-code) would let the
  detector isolate `{eng1, eng2}` specifically instead of over-merging
  the whole pipeline — flagged as a natural next step in FINDINGS.md
  G-24's "Interpretation" paragraph, not attempted here.
- Whether the LLM error-feedback fix (same-day, prior task) actually
  changes `gpt-4o-mini`'s in-episode recovery behavior is still
  untested (carried over from the prior session log).

## Key paths

- `experiments/lab-simulation/lab_sim/oracle_only/uad_core/` — vendored
  detector (detection.py, markov_blanket.py, config.py, info.py).
- `experiments/lab-simulation/lab_sim/oracle_only/uad_mi.py` — lab-sim
  adapter (`build_lab_trace`, `discovered_units_mi`).
- `experiments/lab-simulation/run_s5_uad_core_port.py` — the sweep
  script; `results/s5_uad_core_port.{json,md}` — its output.
- `experiments/lab-simulation/results/FINDINGS.md` G-24.
- `experiments/lab-simulation/tests/oracle_only/test_uad_mi.py`.

## Commits

- Pending — not yet committed this task (staged only on request, per
  repo convention).
