# 2026-07-14 — Graded lab: manuscript-integration backlog, resource-sensitive agent (G-17), EAI-v2 (G-18)

## Trigger

Continuation of the same-day Phase 7c-revised correction session
(FINDINGS G-16, logged separately as
`2026-07-14-graded-lab-phase7c-correction.md`). The user gave three
explicit instructions in one message:

1. Register the four "manuscript integration" findings from the prior
   review into `PLAN.md`.
2. Implement the resource-sensitive agent backlog item from G-16 —
   "make gradedness come from an agent whose decisions depend on its
   resource state" — accepting less than 100% coverage, validated in
   a small optional/slow test battery rather than folded into the main
   criteria.
3. Do a clean, pre-registered EAI-v2 fix for the entropy-term defect
   (G-16 Cause 2) — feasibility analysis *before* any code.

## What was done

### 1. PLAN.md manuscript-integration backlog

Added a "Manuscript integration backlog (2026-07-14)" section to
`PLAN.md` right after "Immediate next steps", with four items mapping
FINDINGS entries to specific chapters:

1. `ch07-finding-boundary.tex` — two demonstrated structural failure
   modes of trace-based boundary discovery (no-communicate-signal miss,
   G-11; resource-contention over-merge, G-12).
2. `ch11-capability-without-task-ontology.tex` — the `I_ctrl` outcome-
   vector ontology trap (G-14) as a concrete "task-agnostic but not
   ontology-free" failure case; the fix is itself not exhaustive (G-13).
3. `ch33-certification-without-construction.tex` — toy-simulation's
   "passive telemetry uncertifiable, interventional handles required"
   result as a sourced instance of the chapter's certification claim.
4. `ch34`/`ch36`/`ch40` (selection/parasites/goal-laundering) — framed
   as a registered go/no-go criterion for Phase 8 spend, not yet a
   finding: write down what a pass vs. a clean null would let the
   manuscript say before committing more engineering time.

None of the four are written into their chapters yet — this is a
registered mapping, not a completed writing task.

### 2. Resource-sensitive agent program (FINDINGS G-17)

Pre-registered in `DESIGN.md` ("Phase 7c backlog item 1"), then
implemented:

- `world.py` now exposes total episode length `T` in each agent's
  observation dict.
- `programs.py` adds `budget_release_manager` (rm1-only program): make
  the deploy/continue decision depend on `t/T` remaining-budget
  fraction, abandoning pipeline progress once that fraction drops below
  `BUDGET_ABANDON_REMAINING_FRACTION`.
- `oracle_only/calibration.py` registers a new agent type
  `programmatic_budget_aware` (`BUDGET_AWARE_AGENT`), explicitly *not*
  part of the default `AGENT_TYPES` sweep — it validates separately,
  not folded into the main strong/weak criteria comparison.
- New test file `tests/test_budget_aware_agent.py`: program-selection
  unit test, two synthetic abandon/no-abandon unit tests, and two
  `@pytest.mark.slow` multi-seed dose-response batteries (deploy rate
  vs. carrier-load scale; stress-sensitivity vs. frozen agents).

**Correction disclosed honestly in FINDINGS G-17:** the initial
`BUDGET_ABANDON_REMAINING_FRACTION = 0.2` failed its own validation
battery (deploy-rate range 0.0, criterion requires ≥0.05) — the
efficient walker finished the pipeline before the abandon window could
ever bind. A reachability dry run measured actual `deploy_tick`
distributions across carrier-load scales; the threshold was revised to
`0.4` (t > 60) based on that empirical measurement, and the battery
then passed (0.3 deploy-rate range, non-increasing trend). This
correction — and the fact that the *threshold* was tuned to the
substrate's own reachability, not to make an outcome come true — is
recorded in both `DESIGN.md` and `FINDINGS.md` per the "no baking a
target result into a definition" rule.

### 3. EAI-v2 (FINDINGS G-18)

**Feasibility analysis first**, written up in `FINDINGS.md` before any
code: traced all six `primitive_log.append` call sites in `world.py`,
confirmed the missing `primitive`/`observable_state` fields could be
attached from values already computed at each site (cheap, contained,
no new mechanics), and estimated a ceiling on the entropy-term effect.
Pre-registered in `DESIGN.md` ("EAI-v2: logging and normalization
fix") before implementing.

Implementation:

- `world.py`: new `_decision_state_snapshot` helper; all six
  `primitive_log` sites (`carrier_terminated`, `carrier_forced_skip`,
  `aborted`, `not_affordable`, `insufficient_resources`,
  `insufficient_standing`, plus the normal pending-action path) now
  consistently attach `primitive={"kind": ...}` and a real
  `observable_state` snapshot.
- `eai.py`: entropy term changed from one global normalizer
  (`log2(total distinct statuses)`) to **per-group** normalization —
  each `(kind, state)` group's entropy is normalized by its own
  distinct-outcome count and weighted by its share of the log; groups
  with ≤1 distinct outcome contribute zero. This directly fixes G-16
  Cause 2 (an unrelated homogeneous group no longer dilutes a genuinely
  mixed group's entropy contribution).
- New `tests/test_eai.py` (7 tests) covering empty-log, homogeneous,
  mixed, the G-16 Cause-2 regression case specifically, backward
  compatibility with old logs lacking the new fields, and component
  composition.
- `CODE_VERSION` bumped `0.13.0` → `0.14.0`.

**Honest result, reported as a null:** the entropy component remains
`≈0` on this substrate even after the fix. The corrected calculation
is verified correct on synthetic logs (`test_eai.py`), but real
episodes rarely produce genuinely mixed-outcome groups given full
agent-visible state — this substrate is close to deterministic given
observable context, so the previously observed EAI drops were, and
remain, driven by the margin-density component, not entropy. This is
recorded as a substrate-statistics finding, not a remaining
instrumentation defect.

### 4. Status rollup

- `README.md`: status line now "Phases 0–7c done (... plus two backlog
  items from G-16, G-17/G-18); Phase 8 not started"; `CODE_VERSION`
  `0.14.0`; phase table and quick-start suite-time note (`~270s`)
  updated.
- `PLAN.md`: status header and the 7c phase-table row updated to note
  both backlog items resolved without flipping the main battery's
  1/4-criteria verdict; item 4 of the manuscript-integration backlog
  sharpened with the G-18 finding — the Phase 8 go/no-go question is
  now "is genuinely graded ambiguity achievable on this near-
  deterministic substrate at all," not merely an instrumentation gap.
- `DESIGN.md`: CODE_VERSION history line and the Phase 7c-revised
  backlog note both updated to mark G-17/G-18 resolved (with the same
  null-result caveat, not silently marked "fixed").

## Verification

Full test suite (`pytest tests/ --profile slow`): **167 tests, all
green**, suite time 272.42s against a raised 300s cap (raised in
`speed_limits.json` specifically for the two new slow batteries).
`speed_limits.json`/`profiles.py` updated with new per-test caps for
`test_budget_aware_agent.py`'s two `@slow` tests (22s, 90s) and
`test_eai` added to the smoke-profile module list.

## Non-obvious decisions

- The resource-sensitive agent is deliberately **not** wired into the
  main strong/weak agent-type comparison this pass — it validates its
  own dose-response claim in an isolated battery. Folding it into the
  main calibration criteria (1/3/4) is a distinct, larger decision left
  for a future session, not implied by "implemented."
- `BUDGET_ABANDON_REMAINING_FRACTION` was set from an empirical
  reachability measurement (a dry run of actual `deploy_tick`
  distributions), not picked to make the validation battery pass —
  the initial 0.2 attempt is disclosed as a failure, not silently
  dropped.
- EAI-v2's entropy fix is reported as *verified-correct-but-null* on
  this substrate rather than claimed as a working fix for the
  calibration battery — the manuscript-integration backlog item 4 was
  updated to reflect that this reframes the Phase 8 question from a
  resource/instrumentation gap to a substrate-design question (does
  this ecology need a real source of per-tick outcome randomness to
  ever reach the "high EAI" band).

## Open / next steps

- Phase 8 (multi-episode / selection) still not started; per the
  sharpened go/no-go note, resolving whether "high EAI" is reachable at
  all on this substrate (possibly via a pre-registered source of real
  per-tick outcome randomness) should be settled before further Phase
  8 engineering spend.
- None of the four `PLAN.md` manuscript-integration items have been
  written into their target chapters yet.
- Whether/how to wire `programmatic_budget_aware` into the main
  calibration criteria (vs. keep it as a standalone validated
  mechanism) is unresolved.

## Key paths

- `experiments/graded-lab-simulation/PLAN.md` (backlog section, status
  header, 7c phase-table row)
- `experiments/graded-lab-simulation/DESIGN.md` (backlog item 1,
  EAI-v2 section, CODE_VERSION history)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-17, G-18)
- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/graded_lab/agent_visible/programs.py`
- `experiments/graded-lab-simulation/graded_lab/oracle_only/calibration.py`
- `experiments/graded-lab-simulation/graded_lab/oracle_only/eai.py`
- `experiments/graded-lab-simulation/tests/test_budget_aware_agent.py` (new)
- `experiments/graded-lab-simulation/tests/test_eai.py` (new)
- `experiments/graded-lab-simulation/README.md`

## Commits

Not committed this session (per AGENTS.md, commit only when the user
asks — stage only what a task authorizes).

---

## Addendum (same session, later) — G-19: reframing "high band
unreachable" as a measurement-vantage finding, not a substrate gap

After reviewing G-18's result, the user pushed back on the framing
"graded ambiguity is not achievable on this substrate" (surprised by
it), then, on hearing the actual decomposition (entropy ≈0 vs.
margin-density genuinely graded), reframed the conclusion themselves:
adding substrate randomness is the wrong fix; what matters is
**visibility to the in-sim referee**, and EAI should be predicted and
measured from the referee's own vantage before any further Phase 8
work. Instructed: "Document."

**What was found and documented (FINDINGS G-19, no code):**

- The entropy term's ≈0 result is not "this substrate lacks
  ambiguity" — it's "outcomes are deterministic given the *acting
  agent's own full context*," which was never the right vantage for
  the Phase 8 claim (a claim about what a correction channel/referee
  can resolve from outside, not about agent epistemics).
- The codebase already has the right mechanism for the correct
  vantage, built for an unrelated purpose: the Phase-5 audit-plane
  tier projection (`oracle_only/events.py`'s `project_primitive_log`,
  `light` tier strips exactly the two fields — `primitive`,
  `observable_state` — the entropy term conditions on).
- Pre-registered a falsifiable prediction *before* touching code:
  feeding a `light`-tier projected log into the unmodified
  `compute_eai` entropy term will show materially non-zero entropy
  (marginal status-outcome distribution, not conditional-on-full-
  state), because several distinct statuses co-occur across any real
  episode even though each is individually predictable given full
  state. Registered failure mode stated too: if this is also ≈0, the
  "unreachable" finding would extend to the referee's vantage as well
  — a stronger, not-adjusted-for result.
- Added `DESIGN.md` "EAI-referee" section pre-registering the plan (a
  second, separately-reported EAI variant keyed by audit tier — not
  replacing the agent-vantage EAI-v2 used for margin-density/dose-
  response criteria).
- Updated `PLAN.md` manuscript-integration item 4 to replace the
  "needs substrate randomness" framing with the referee-vantage
  reframe and name it the concrete next step before further Phase 8
  spend.

**Explicitly not done:** no implementation. `eai.py`, `calibration.py`,
`run_phase7_calibration.py` are unmodified; the described
`compute_eai_at_tier`-style helper is a future-session task, to be
checked against the stated prediction rather than implemented and
then rationalized.

### Key paths (addendum)

- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-19)
- `experiments/graded-lab-simulation/DESIGN.md` ("EAI-referee" section)
- `experiments/graded-lab-simulation/PLAN.md` (item 4 reframe)

---

## Addendum 2 (same session, immediately after) — G-20: measured the
G-19 prediction, held decisively

User: "predict and run measure from *their* perspective before
proceeding." Implemented exactly what G-19 pre-registered and checked
the result against G-19's own falsification bar, not the reverse.

**Code (additive, no `CODE_VERSION` bump — no existing caller's
output changes):**

- `eai.py`: split the existing entropy/margin arithmetic out of
  `compute_eai` into private `_entropy_component()`/
  `_margin_density()` helpers (behavior-preserving — verified by the
  unchanged `tests/test_eai.py` suite staying green); added
  `compute_eai_at_tier(log, margins, tier_i_fraction, tier)` (feeds a
  `oracle_only.events.project_primitive_log`-projected log into the
  unmodified entropy grouping) and `eai_components_at_tier(...)` for
  decomposed reporting.
- New `run_referee_eai_check.py`: reruns G-18's exact episode set
  (`programmatic_softmax`, `carrier_load_scale ∈ {0,0.5,1,1.5,2}`,
  seeds 0–9) at both `full` and `light` audit tiers; writes
  `results/referee_eai_check.json`.
- `tests/test_eai.py`: 4 new tests for `compute_eai_at_tier`/
  `eai_components_at_tier` (full-tier exact match to `compute_eai`,
  light-tier entropy rising on a per-full-tier-homogeneous log,
  component decomposition).

**Result — prediction held, by a wide margin, plus an unpredicted
shape:** light-tier entropy reaches `0.57`–`0.73` at every stressed
cell (bar was `>0.02`), vs. `≈0` at full tier (which reproduces G-18's
numbers exactly, confirming the refactor is behavior-preserving).
Referee-vantage composite EAI lands cleanly in the pre-registered
**mid** band (`0.33`–`0.40`) at every nonzero-load cell — the first
non-hairline mid-band signal in this whole line. It does **not** reach
**high** band anywhere (peak `0.396`). The shape across cells is
non-monotonic (peaks at `carrier_load=1.5`, dips at `2.0`) — not
predicted, reported as found rather than explained away.

**Not done:** the main calibration battery was **not** rewired to use
referee-vantage EAI — that changes every downstream pass criterion and
is a separate, larger decision, deferred. Full 167-test suite reran
green (270.29s) after the refactor.

### Key paths (addendum 2)

- `experiments/graded-lab-simulation/graded_lab/oracle_only/eai.py`
- `experiments/graded-lab-simulation/run_referee_eai_check.py` (new)
- `experiments/graded-lab-simulation/results/referee_eai_check.json` (new)
- `experiments/graded-lab-simulation/tests/test_eai.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-20)
- `experiments/graded-lab-simulation/DESIGN.md` ("EAI-referee" — measured)
- `experiments/graded-lab-simulation/PLAN.md` (item 4 — measured)

---

## Addendum 3 (same session) — G-21: is the non-monotonic shape
chance? Statistics, then a mechanistic account without new experiments

User: "The non-monotonic pattern could be chance. What are the
confidence intervals? If that's not it, what are plausible
explanations without further experiments?"

**Statistics added to `run_referee_eai_check.py`** (no new episodes,
no `CODE_VERSION` bump): per-cell mean/std/SE/95% CI (hardcoded
`t`-critical for `df=9`, no `scipy` in this venv, guarded by an
`assert` on the seed count) and **paired** (by-seed) 95% CIs on each
consecutive-cell difference in light-tier entropy.

**Result:** the initial rise (`0.0→0.5`, `0.5→1.0`) is clearly
significant (95% CIs exclude 0 by a wide margin). The two steps that
make up the "non-monotonic" shape are **not** individually
significant at `n=10`: `1.0→1.5` (diff −0.052, CI [−0.159, +0.055])
and `1.5→2.0` (diff +0.136, CI [−0.003, +0.274], the latter a hair's
width from significance). So: part of the pattern (the initial rise)
is real; whether entropy actually peaks at 1.5 and falls, versus
plateauing across `{1.0,1.5,2.0}` with sampling wiggle, cannot be
distinguished from this sample.

**Mechanistic account (re-analysis of the same 50 already-run
episodes' status labels, not a new experiment):** pooled status-mix
audit shows `carrier_forced_skip` fraction rises **monotonically**
with load (0%→23%→53%→64%→70% of all log entries) — a real substrate
effect. But Shannon entropy of a two-outcome mixture peaks near 50/50
and falls as one outcome comes to dominate; the `ok`/`skipped` split
crosses roughly even right around `carrier_load=1.0` and then drifts
toward `skipped`-dominant by `2.0`. A monotonically drifting
composition crossing 50/50 mechanically produces a non-monotonic
entropy curve — no new substrate mechanism needed. A compounding
secondary effect: rare statuses (`denied`, `terminated`) start
appearing only at the highest-stress cells, inflating the per-episode
normalization denominator (`log2(distinct statuses)`) and pulling the
normalized entropy down further at `carrier_load=2.0`.

**What this does/doesn't settle:** gives a plausible, data-grounded
reason a fall-past-peak is expected in principle, consistent with the
`1.5→2.0` step being the "more real" of the two non-significant ones.
Does not pin down the exact peak location — that needs more seeds or
a direct test on pooled composition, neither attempted (out of scope
per "without further experiments").

### Key paths (addendum 3)

- `experiments/graded-lab-simulation/run_referee_eai_check.py` (CI/paired-diff stats)
- `experiments/graded-lab-simulation/results/referee_eai_check.json` (updated)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-21)
