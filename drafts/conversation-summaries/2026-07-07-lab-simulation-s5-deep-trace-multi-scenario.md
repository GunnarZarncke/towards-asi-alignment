# 2026-07-07 — Lab-layer sim S5 follow-up: deeper UAD trace, multi-scenario sweep, over-merge diagnosis, CMI detector, S6 plan

## Trigger

Continuation of the same-day S5 session. User first asked what exactly
is in the recorded traces and whether other agents appear in other
scenarios' traces (answered: only S4 had been run through this
detector; the G-24 trace was `.step`/`.ok` only). User then: "I think
that trace is much too light. Though we might want to record UAD at
different depth to determine probe scale. A deeper trace should
include file reads and writes, DM send and receive, tool call, compute
(e.g. CoT length), API call. access request/grant. Should cover the
whole lab except oracle. Run against multiple scenarios."

## Done

- `lab_sim/oracle_only/uad_mi.py`: added a `depth: str = "shallow"|"deep"`
  parameter to `build_lab_trace`/`discovered_units_mi`.
  - `"shallow"`: G-24's original 2 vars/actor/tick (`.tool`/`.ok`,
    renamed from `.step` for clarity — same codes/semantics otherwise).
  - `"deep"` (new default): 5 vars/actor/tick. `.tool`'s vocabulary
    widens from "pipeline step or one generic other bucket" to a
    distinct code per `board.post`/`board.read`/`dm.send`/`dm.read`/
    `file.write`/`file.share`/`file.read`/`state.save`/`state.load`
    (`_DEEP_TOOL_CODES`). New `.dm_recv` — 1 iff some OTHER actor's
    `dm.send` named this actor as `args.recipient` this tick (a signal
    ABOUT the actor, not one of its own tool calls). New
    `.access_grant`/`.access_deny` — read from `PermissionService.log`
    (`action == "grant"`/`"deny_request"`, `actor_id` = the actor the
    decision is about), a SEPARATE admin-side event from the actor's
    own `access.request` call (already visible via `.tool == 11`).
  - `discovered_units_mi` now also pulls `view.access_log` (already
    present on `AuditView` at every tier — `t`/`actor_id`/`action` are
    light-tier fields, no deep-tier fetch needed) and threads `depth`
    through.
- **Explicit scope limit, recorded not hidden**: "compute (e.g. CoT
  length)" and "API call" were ALSO requested but are in NEITHER
  depth. Neither signal exists anywhere on `world.EpisodeResult` for
  any backend today — an LLM backend's transcript/usage/cache-hit
  bookkeeping lives entirely inside the backend object
  (`llm_isolate.LLMSubprocessHandle`), never surfaced generically.
  Adding it would need a structural change to `world.py`'s core
  episode loop (new `EpisodeResult` field threading backend-specific
  usage through), which was judged out of scope for this pass and
  flagged as a named follow-up in `uad_mi.py`'s module docstring and
  PLAN.md, rather than silently shipped as an incomplete "deep" trace.
- `run_s5_deep_trace_sweep.py` (new): both depths × `n_agents` ∈
  {1,2,3,4} × 5 seeds, across FIVE ecologies each with one known
  non-singleton true pair: `dm_pair_config` ({eng1,rm1}),
  `covert_file_handoff_config(trusting=True)` ({eng1,rev1}),
  `committee_with_informal_chatter_config` ({eng1,rm1}),
  `build_loop_config` ({eng1,rm1}), `shared_slot_config` ({eng1,eng2},
  G-24's own episodes, re-run at both depths for direct comparison).
- **Result**: identical to G-24 in every one of the 200 cells — true
  pair merges 100%, isolated-from-the-rest 0%, at both depths, all
  four `n_agents`, all five scenarios. `uad_score` reports 1.0
  everywhere for the same blind-spot reason as G-24. Widening the
  trace changed what the detector sees, not that it over-merges; the
  gap generalizes well beyond S4.
- `results/FINDINGS.md` G-25 (full writeup); `PLAN.md` S5 section
  "Update 2"; `README.md` status line, run-commands, layout, S5
  narrative paragraph, test count (359 → 368).
- `tests/oracle_only/test_uad_mi.py`: rewritten/expanded to 19 tests
  (from 10) — shallow-depth unit tests (renamed `.step`→`.tool`,
  explicit `depth="shallow"` folding comm/file tools into "other"),
  deep-depth unit tests (`.tool` widening, `.dm_recv` on
  recipient-only / not on failed sends, `.access_grant`/`.access_deny`
  from a synthetic access log, ignoring `"check"`/`"revoke"`/outsider
  entries, horizon spanning access-log ticks), an unknown-`depth`
  `ValueError` test, and a shallow-depth companion to the existing
  deep-depth golden test.

Final state: **368 tests green** (up from 359 before this task).

## Decisions

- Renamed `.step` → `.tool` at BOTH depths (not just deep) for naming
  consistency, since "deep" widens what `.tool` covers beyond pipeline
  steps — a `.step` name would have been misleading once comm/file
  tools got their own codes.
- `.dm_recv`/`.access_grant`/`.access_deny` are separate 0/1 variables
  from `.tool`, not folded into it — a tick can have at most one
  `.tool` value (one call/tick), but "received a DM" or "was granted
  access" are facts ABOUT an actor that can co-occur with that actor's
  own unrelated tool call the same tick, so they need their own slots.
- `access_log` reads use only `t`/`actor_id`/`action` — all present at
  `"light"` tier already — so `discovered_units_mi` still only
  requires `tier="full"` (unchanged default), matching the "no
  deep-tier fetch needed" discipline `uad.py`/`uad_mi.py` already
  documented for tool events.
- Chose NOT to attempt the compute/API-call plumbing this pass rather
  than build a partial/asymmetric proxy (e.g. reusing `playbook.
  selection` events, which only programmatic — not LLM — actors emit) —
  judged that a half-signal covering only non-LLM actors would be more
  misleading than an explicitly-scoped-out gap.
- 5 scenarios chosen to cover every ecology with a well-defined
  non-singleton `units=` ground truth already in `ecology.py` (no new
  ecology configs added); seeds reduced to 5 (from G-24's 10) to keep
  the 5-scenario × 2-depth × 4-`n_agents` grid's runtime reasonable —
  every cell was already fully deterministic at temperature=0 in G-24,
  so fewer seeds does not weaken the finding.

## Follow-up in same session: over-merge diagnosis (G-26)

User asked to diagnose WHY UAD doesn't discover the "right" agents.
Ad-hoc diagnostic (throwaway script, deleted after use; findings in
FINDINGS.md G-26):

- The pairwise lag-MI matrix already ranks the TRUE pair first in 3/5
  scenarios; at `n_agents = n_active_vars − 1` (one merge allowed) the
  detector's first merge IS the true pair in dm_pair/build_loop/
  shared_slot, 5/5 seeds. The over-merge is the CLUSTERING step's
  fault: hard `n_agents` variable-cluster target + globally-normalized
  complete-linkage with no gap-based stopping rule.
- Deep trace is mildly WORSE for first merges (more within-actor
  variable redundancy to chew through) — relevant to the probe-scale
  question.
- The 2 residual failures need conditioning: I(A;B|rest) explains away
  pipeline-common-cause coupling (shared_slot eng1–rm1: 1.15→0.04)
  while true-pair coupling survives (eng1–eng2: 0.26). The vendored
  detector never conditions. The covert file handoff is additionally a
  low-rate channel invisible to occurrence-MI.
- **Bug found and fixed**: `run_s5_deep_trace_sweep.py` scored the
  committee scenario against the wrong true pair ({eng1,rm1} instead
  of {rev1,rev2} per `ecology.py`'s `units=` literal). Re-run flips
  that scenario's heuristic merge rate 0.0→1.0; MI cells unchanged
  (the all-merged blob masked the bug — another `uad_score`-blind-spot
  data point). G-25's text corrected in place.

## Follow-up 2 in same session: G-26 easy fixes + S6 intervention-UAD plan (G-27)

User: do the easy fixes, then plan intervention-supported UAD using the
handles; the vendored code can eventually be thrown away.

- `lab_sim/oracle_only/uad_cmi.py` (new, standalone — no vendored
  imports, so `uad_core/` is deletable later): all three G-26 fixes.
  Actor-level composite symbols (tuple of all the actor's trace vars
  per tick); edge weight = lag-max I(A;B|rest) with rest = joint
  symbol of all other active actors; stopping rule = circular-shift
  permutation null (95th pct of 40 shifts) + 0.1-bit floor — NO
  `n_agents` target. Defaults pre-registered before the sweep.
- `run_s6_cmi_detector.py`: same 5 scenarios/seeds, three detectors
  side by side, new stricter `exact` metric (non-singleton clusters ==
  exactly {true pair}).
- **Result (G-27)**: blob gone everywhere; shared_slot {eng1,eng2}
  isolated from rev1/rm1, 5/5 seeds, both depths — first detector in
  the line to crack S4 (heuristic G-20 blind, vendored G-24 blob).
  Honestly reported ceiling: `exact_rate` 0.0 everywhere — conditional
  MI recovers the causal SKELETON (rev1–rm1's direct sign_off→release
  edge merges too; dm_pair/build_loop yield the 3-actor chain), and
  committee content-coupling stays invisible. "Direct causal edge" ≠
  "same unit" for any passive occurrence statistic.
- 10 new tests (`tests/oracle_only/test_uad_cmi.py`), 378 total green.
- **S6 plan written into PLAN.md** ("S6 — intervention-supported
  UAD"): deterministic same-seed episode-pair diffs (twins.py pattern
  pointed at interventions); probe library over existing levers
  (handles via overseer_script, perturbation hooks, D4 channel
  ablation); unit test = mutual adaptive COMPENSATION under probes
  (vs. mechanical stall propagation, honest twin as control); 6 phases
  incl. peel-and-mask (agent_spotlight analog) and active probe
  selection under budget (uad_handles analog); vendored `uad_core/` +
  `uad_mi.py` deletable on completion, `uad_cmi.py` stays as the
  passive proposal stage. Precedents referenced from sibling repo
  `~/repos/zarncke/agency-detect` (`uad_handles/`, `agent_spotlight/`
  peel/refine) — referenced, not vendored.

## Open / next

- The acausal-coordination (ICI) second probe from PLAN.md's S5 entry
  remains fully unimplemented (carried over, unchanged).
- Compute/API-call trace signals remain unimplemented — would need a
  new `EpisodeResult` field surfacing backend-specific usage data,
  flagged in PLAN.md/`uad_mi.py` as a named follow-up.
- S6 intervention-supported UAD: planned (PLAN.md section), phase 1
  (episode-pair diff substrate) not started.
- A workflow-edge-only negative-control ecology (serial pair with no
  unit) is needed before S6 phase 3 can claim edge-vs-unit separation.
- Whether the LLM error-feedback fix actually changes `gpt-4o-mini`'s
  in-episode recovery behavior is still untested (carried over).

## Key paths

- `experiments/lab-simulation/lab_sim/oracle_only/uad_mi.py` —
  `build_lab_trace`/`discovered_units_mi`, both depths.
- `experiments/lab-simulation/run_s5_deep_trace_sweep.py` — the
  5-scenario × 2-depth sweep script; `results/s5_deep_trace_sweep.
  {json,md}` — its output.
- `experiments/lab-simulation/results/FINDINGS.md` G-25.
- `experiments/lab-simulation/tests/oracle_only/test_uad_mi.py`.

## Commits

- `e96dba6` — Lab-sim UAD: error feedback, lag-MI port, deep traces, CMI
  detector, S6 plan.
