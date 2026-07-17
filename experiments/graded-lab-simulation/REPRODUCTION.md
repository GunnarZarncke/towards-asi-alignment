# Reproduction — high-effort work packages for a larger team

This file collects the **large, workload-incurring engineering tasks**
that a single-agent session in this repo has explicitly chosen *not* to
attempt, together with the reasoning for why each matters and roughly
what closing it would require. It exists because external review
(2026-07-15, see `results/FINDINGS.md` GL-42) found that several
claims V2-2b's design made — about blinding, about "institutional
structure," about "exogenous workload" — were true of the *documentation*
but not of the *runtime*, and some of the honest fixes are themselves
large enough that a solo session should not attempt them under time
pressure. Each section below states the gap, why the cheap fix (a
documentation caveat) is not a substitute for the real fix, and a rough
shape for the work a larger team would take on.

This is a companion to `REPRODUCING.md` (v1's per-finding reproduction
map — different purpose: that file is about *replaying already-run*
findings; this file is about *work that has not been done yet*).

See `COLLABORATION.md` for how to pick up one of these packages.

**Update 2026-07-15 (GL-43):** items 1, 2, and 4 below are now
**in-scope for v3** — specified as slices A–C (item 1), E (item 2,
renamed **feedback-coupled pressure**, not standalone Poisson noise),
and F (item 4, including composable `ProgramMap`) in
[`PLAN_v3.md`](PLAN_v3.md). Item 3 (execution-isolated pilot service)
remains deferred. Slice A uses **loose** coherence tolerances in v3.0
(±25% flow-vs-declared-total warn); tightening to ±1% hard-fail is
listed below as a deliberate later tightening item.

**Update 2026-07-15 (backlog expansion):** items 5–7 carry the
**post-v3** graded-lab program from `PLAN_v2.md` (V2-4 variation
operator, V2-5 selection, V2-6 red-team) into this file so they are
not lost in phase tables alone. Item 8 lists **cross-book** tasks from
`metadata/TODO.md` with graded-lab touchpoints.

**Update 2026-07-16 (GL-53):** slice D **criteria freeze is partial** —
reference-battery constants and ``V3_REFERENCE_T=200`` are frozen in
``DESIGN.md`` and validated on the integrated hand-built fixture; growth
protocol, frozen-detector coverage battery, and ``ProgramMap`` overlap
report (``PLAN_v3.md`` slice D items 6–7) remain open. Items 5–7 below
are blocked on slice D completion + a passing v3 ecology (or honest null
on the frozen reference), not merely on criteria constants.

**Update 2026-07-16 (GL-66 design):** near-term **attention surface**
work (push: interleaved priority desk; pull: one cheap ``desk.scan`` via
host ``call`` endpoints — see session design notes) stays in-engine for
round 1. **Item 11** records the larger follow-on: replace the isolate's
JSONL wire protocol with a realistic in-process lab environment (DOM/VFS
files, HTTP/WebCAL desk service, comms library). Item 11 is **not**
blocking GL-66 or v3 round 1.

**Status key:** *v3 slice* = specified in `PLAN_v3.md`, not yet
implemented; *PLAN_v2 phase* = pre-registered in `DESIGN.md`, blocked
on v3 + prior phase gates.

---

## 1. Make institutional structure executable, or stop claiming it's live

**Status:** *v3 slices A, B, C* (`PLAN_v3.md`). Not implemented.

**Gap.** C1 (principal plurality), C2 (incentive coupling), and C5
(mechanism diversity) are checked **only against the candidate JSON's
declared sections** — `principals`, `conflicts`, `mechanisms`,
`resource_flows`. `graded_lab/harness/ecology_complexity.py` reads
these fields; `graded_lab/world_visible/world.py` (the actual episode
loop), `permissions.py`, and `resource_ledger.py` never do. A candidate
can pass "≥4 principals, ≥3 conflicts, 3+ mechanism kinds, every role
reachable from ≥2 principals" while every agent's payoffs, permissions,
and interactions in the running simulation are completely unaffected by
any of that declared structure.

**Why the cheap fix isn't enough.** Documentation notes (added in
`DESIGN.md` and `PLAN_v2.md`, this session) correctly downgrade the
claim from "a passing ecology has live multi-principal incentive
coupling" to "a passing ecology has a coherent, mechanically-checked
*declared* institutional structure." That is honest, but it also means
V2-3's plan to use C5's declared mechanisms as UAD ground truth is only
a test of whether UAD recovers **declared-but-behaviorally-inert**
structure — a coherence check on UAD's machinery, not evidence UAD
finds real institutional coupling units. If the manuscript or Q1
harvest wants to claim more than that, this gap has to close first.

**Rough shape of the real fix (large — plan for a multi-week effort,
not a session):**

1. Design a **compilation step**: `principals` → reward/objective
   terms actually folded into the referee's severity/EAI computation
   (not just `oracle_only` bookkeeping); `resource_flows` → actual
   per-role resource *allocation* (not merely allowance columns that
   are the same regardless of which principal is declared to fund
   them) — e.g. a principal's declared objective direction should
   change what the referee scores as good/bad for that role, and a
   `resource_flows` row should determine the actual size of a role's
   compute/io/standing allowance, not just be checked for reachability.
2. `mechanisms` → actual permission/communication channel bindings:
   a `message_channel` mechanism's declared `members_ground_truth`
   should be the *only* actor set that can use the corresponding
   `communicate` channel; a `joint_approval_vote` mechanism should
   require an actual multi-actor vote primitive (new mechanic) rather
   than the existing single-admin `access.request`/`process_next` flow.
3. Once compiled, C2's reachability check becomes a check on the
   **compiled runtime graph**, not the declared JSON graph — this
   changes what "incentive coupling reaches agents" means from "the
   grower said so" to "the simulation enforces it."
4. Full regression suite against the v1 digest pin and all V2-2/V2-2b
   round artifacts — this is a substrate-shape change, not additive,
   so it likely **cannot** preserve v1/v2-2 byte-identical replay; plan
   for a new `ecology_version` (e.g. `"v3"`) rather than mutating `"v2"`
   in place, and decide explicitly whether V2-2's four archived rounds
   are re-interpreted under the new semantics or left as a historical
   record under the old one.
5. Re-derive C1–C5 (or a superset) against the compiled runtime, not
   the declared JSON — the current thresholds were calibrated against
   declarative checks only and may not transfer.

---

## 2. Real exogenous work injection, not a cost multiplier

**Status:** *v3 slice E* (`PLAN_v3.md` **feedback-coupled pressure** +
task injection on threshold; no standalone Poisson). Not implemented.

**Gap.** `graded_lab/world_visible/exogenous_workload.py`'s
`ExogenousWorkloadEngine.cost_scale_for()` only multiplies the cost of
actions an affected role's agent **independently decides to take**
during an active window. It does not inject a task, ticket, incident,
or any demand that must be serviced regardless of what the agent
decides. If no affected actor happens to act during the window, no
demand spike exists at all — contention from this mechanism is a
side-effect of cost inflation, not a claim that "incident bursts create
concurrent demand," which is what the V2-2b brief says the mechanism
represents.

**Why the cheap fix isn't enough.** The brief now states this
limitation explicitly (`BLIND_GENERATION.md` "V2-2b," item 2), and the
module docstring is honest about it. But a grower whose ecology passes
C3 via this mechanism may be tuning a cost multiplier, not designing an
institutionally plausible incident-response process — the manuscript
should not cite a C3 pass achieved this way as evidence of "realistic
correlated demand," only as evidence the mechanical criterion cleared.

**Rough shape of the real fix (medium-large):**

1. Add an actual **task queue**: exogenous events append synthetic
   work items (e.g. "an incident review, requiring a `read` + `write`
   + `communicate` sequence from the affected role") to a per-role
   queue that the affordable-action set surfaces as newly-available
   (or newly-mandatory) primitives, independent of what the agent was
   already doing.
2. Decide the semantics of *mandatory* vs. *available*: does an
   ignored incident task expire, escalate, or block other actions?
   This is a real design decision with institutional-realism
   consequences, not just an engineering task — flag it for review
   before implementing, don't decide it unilaterally mid-session.
3. Regression-test that agents who never engage with injected tasks
   still produce a sane (if degenerate) episode — avoid a hang/deadlock
   failure mode.

---

## 3. Trusted execution-isolated pilot / grower environment

**Gap.** `ecology_pilot.py`'s output filter (`audit_pilot_payload()`)
filters the **JSON payload** the pilot CLI prints. It does not, and
cannot, stop a grower subagent that has ordinary code execution against
this repository from `import`ing `run_episode`, `OracleWorld`, or any
other genuinely-blinded module directly, enabling
`record_contention=True` itself, or reading `oracle_only/*.py` source.
Moving checker source files out of the working tree during a growth
round (`BLIND_GENERATION.md`'s physical-isolation protocol) mitigates
this for the checker's own source and thresholds, but does not create a
real capability boundary — it relies on the grower subagent not
choosing to explore, not on anything that would stop it if it did.

**User's assessment (2026-07-15):** this is a real gap, but building a
genuine capability-restricted sandbox (or routing pilot/grower access
through a separate, network-isolated service that only returns the
disclosed fields) is **excessive for the current single-agent session**
and is recorded here for a larger-team reproduction rather than
attempted now.

**Rough shape of the real fix (large — infrastructure project):**

1. Stand up a **separate process or container** with only the pilot
   entry point exposed (e.g. a thin HTTP/RPC service wrapping
   `run_pilot_episodes`), no filesystem access to the rest of the
   repository, and no ability to import arbitrary project modules.
2. The grower subagent's tool access for a growth round would be
   restricted to: writing its own candidate JSON, calling this service
   with a path/blob, and receiving only the disclosed fields — no shell,
   no arbitrary file read, for the duration of the round.
3. This is worth doing **only if** a future criterion needs a real
   blinding claim; per GL-42, C3/C4 no longer make that claim, so this
   work is not blocking with the current C1–C5 criterion set. Revisit
   if a future criterion (post-V2-2b) reintroduces something that must
   stay genuinely hidden from an agent with pilot access.

### 3.1 V3 grower orchestrator snapshots (GL-72 — mandatory for scored rounds)

**Failure mode (GL-71, voided).** Round 2 (2026-07-17) was **invalid** as a
successive grower round: the grower read
`runs/grower-v3-round1/check_result_round1.json`, which contained orchestrator
`details_summary` (failing conflict pairs, deploy rate, correlation values) —
**not** the authorized between-round payload (`pass_fail_only()` bools only).
That file lived under `runs/`, which is grower-reachable during design. The
resulting ecology passed all gates but is a **dead branch** archived at
`archive/v3-dead-branch-round2-blinding-leak/`; it does **not** count toward
the ≤4 successive rounds and must not be cited as a passing grower ecology.

**Fix (orchestrator discipline, not a capability sandbox):**

1. **Score only via** `scripts/score_grower_round.sh CANDIDATE.json LABEL` —
   writes to `growth-orchestrator/v3/check_result_<LABEL>.json` (gitignored).
2. **Before each grower launch:** `scripts/grower_stash.sh stash` must remove
   `growth-orchestrator/`, the voided archive, `results/`, checker source,
   fixtures, `graded_lab/oracle_only/`, and rubric docs.
3. **Between-round feedback to grower:** paste **`pass_fail_only()` JSON only**
   into the grower prompt — never attach checker snapshot files or
   `details_summary`.
4. **Successive rounds:** round *N* grower sees round *N−1* **ecology JSON +
   rationale + knowledge base** only, plus authorized feedback. Voided branches
   are not inputs to later rounds.

**Still open:** §3's full execution-isolated service (no arbitrary repo read).
Stashing orchestrator output closes the specific leak GL-71 exposed; it does not
stop a grower from importing `principal_scorecard` if not stashed — hence
`graded_lab/oracle_only/` is now on the stash list for v3 growth.

---

## 4. Heterogeneous multi-actor roles (not clones)

**Status:** *v3 slice F* (`PLAN_v3.md`).

**Gap (v2-2b):** `role_population` (GL-40) builds N **identical** clones per
role — same role program, same goal weights, against one shared global
pipeline. This manufactures queue depth (useful for C3's contention
mechanism) but is not evidence of heterogeneous institutional actors,
per-actor incentive structure, or strategic coupling between distinct
individuals holding the same role. C2's reachability check stays
explicitly per-role, not per-actor, for this reason.

**v3 spec (slice F):** per-actor `{program?, program_map?}` overrides;
**`ProgramMap`** composable genotype (walker + sparse `pattern_scores` +
discrete hooks) with preset expansion from frozen vocabulary; V2-4
mutates the same schema (`REPRODUCTION.md` §5). **Blinding note:**
`ProgramMap` exposes agent-visible vocabulary only; see `PLAN_v3.md`
§ "Blinding boundary (anticipating critics)" — ecology grower may be
restricted to frozen presets at growth time, with maps edited only under
selection.

**Rough shape (largely specified — implementation in v3 slice F):**

1. `program_map.py`: validate, expand preset, compose runtime policy;
   hybrid `mode` dispatch.
2. C2-v3 per-actor reachability as reported diagnostic; pass/fail TBD
   at design review.
3. Phenotype-hash reporting (syntax vs behaviorally distinct maps) for
   selection experiments.

---

## 5. Variation operator / mutation over `ProgramMap` (V2-4)

**Status:** *PLAN_v2 phase V2-4* — **blocked on v3 slice F** (`ProgramMap`
validation + runtime composition). Pre-registered edit vocabulary in
`DESIGN.md` § "Variation-operator edit vocabulary"; **update that
section** when slice F lands so mutations target unified `ProgramMap`
cells (not the legacy split between `feature:*` floats and walker tuples
alone).

**Gap.** Q2 ("emergence under selection with variation — MB6/MB7") cannot
run until a closed mutation operator exists over a genotype large enough
to explore (>10¹⁶ syntax-valid maps under discrete bins — see
`PLAN_v3.md` § Grower agent design space) with a **uniform-fitness null**
and permutation-band stats (`oracle_only/stats.py`, GL-25 lesson).

**Why not in v3.** v3 delivers the genotype and preset expansion; the
operator is a separate pre-registered battery with its own null harness.
Implementing both in one slice would blur "ecology wiring" from
"selection machinery."

**Rough shape (medium-large, ~1–2 wk after slice F):**

1. **Closed edit vocabulary** over `ProgramMap` (pre-register before
   any selection run): e.g. `pattern_score_±1`, `pattern_score_set`,
   `step_insert` / `step_drop` / `step_reorder`, `hook_tweak`,
   `temperature_bin±1`, `goal_weight_bin_nudge`, `mode_swap` — each edit
   re-validates mechanically; invalid mutants discarded, not repaired.
2. **Mutation rate:** one edit per member per generation with probability
   `MUTATION_RATE` (DESIGN.md default 0.3); at most one edit class per
   generation for attribution.
3. **Null harness:** uniform-fitness control + `N_PERMUTATIONS` shuffle
   band in `oracle_only/stats.py`; P5 gate — selection claim reportable
   only if treatment exits band and null does not.
4. **Expressiveness report:** distinct phenotypes per 100 mutants
   (phenotype hash from slice F), separate from syntax cardinality.
5. **Tests:** operator + null on frozen smoke ecology; no semantic
   filter on mutants.

**Touches:** new `graded_lab/harness/variation_operator.py` (or
`oracle_only/selection.py`), `program_map.py`, `oracle_only/stats.py`,
`DESIGN.md`, `tests/test_variation_operator.py`.

---

## 6. Selection with variation (V2-5, Q2 primary)

**Status:** *PLAN_v2 phase V2-5* — blocked on §5 + v3 slice D **completion**
(criteria constants frozen GL-53; growth protocol + pre-Q1 batteries still
open) + a passing v3 ecology (or honest null on frozen reference).

**Gap.** v1's Phase 8 null (GL-23) used a **fixed roster** — it could
not ask whether selection *with variation* surfaces evasive strategies.
V2-5 is the primary MB6/MB7 battery.

**Rough shape (large — multi-week compute + analysis):**

1. Multi-generation selection on v3 ecology: population ≥12, generations
   ≥12, episodes/member ≥6 (floors in `DESIGN.md`; finalize in V2-5
   protocol write-up).
2. Multi-handle fitness vector (Phase 8b default, carryover per GL-27);
   lineage tracking; evasion criterion each generation (same operational
   definition as V2-4 spec in `DESIGN.md`).
3. Output: `results/v2_selection.json`; archive any evolved program
   meeting evasion criterion with full lineage for replay.
4. **Predictions:** P6 (selection beats mutation-only null by gen 12),
   P7 (evasion if any) — resolve positive or null in FINDINGS.

**Blocked by:** item 5, v3 institutional runtime (item 1), slice D
**completion** (growth protocol + items 6–7; criteria constants frozen
GL-53).

---

## 7. LLM red-team with onboarding (V2-6, Q3)

**Status:** *PLAN_v2 phase V2-6* — blocked on v3 ecology + V2-3 go gate
(reference batteries on grown ecology).

**Gap.** Budget-capped LLM adversary on affordable-primitive API; tests
detector robustness against a class of adversary v1 could not run at
ecology scale.

**Rough shape (large — adapter port + protocol + compute):**

1. Port lab-sim subprocess-isolate LLM adapter; hard caps on ticks,
   tokens, dollars; progress logging.
2. Two conditions: surface-blind vs informed (detector-family docs, not
   thresholds); prompts frozen verbatim in `BLIND_GENERATION.md`.
3. Onboarding window (world live, scoring suppressed) then scored window;
   duration from reference-agent median ticks-to-deploy (V2-3 statistic).
4. ≥5 seeds/condition; evasion criterion identical to V2-5 on
   post-onboarding actions only.
5. Output: `results/v2_redteam.json`; P8 informed ≥ surface-blind ≥
   variation (report all three).

**Scope limit (pre-registered):** bounds robustness against *this*
adversary class, not absence of evasion in general.

---

## 8. Cross-book tasks with graded-lab touchpoints

Extracted from `metadata/TODO.md` § Experiments / Manuscript — not
graded-lab engineering per se, but flagged as major work that may wire
into this line:

| Task | Source | Graded-lab connection |
|---|---|---|
| **Wire embedded value formation paper** | `metadata/TODO.md` | Entropic Ecology Transfer Test may connect to ecology transfer / Q1 harvest; cite before claiming cross-paper empirical support. |
| **Review SOO vs book adversarial scenarios** | `metadata/TODO.md` § Experiments | Tier-1 scenarios (report inflation, shadow routing, correction-capture theater, bearer-map narrowing) — decide if any map to graded-lab detectors or stay manuscript-only; owner split Marc / book-side. |
| **Cornerstone empirical value-bundle test** | `metadata/TODO.md` § Manuscript | ch16/ch17 bundle recovery — distinct from graded-lab Q1–Q3 but may share measurand vocabulary; do not conflate lines in FINDINGS. |

---

## 9. Text→`ProgramMap` compiler (tighter reproduction / mitigation 1+)

**Status:** deferred — target for a **second growth protocol** after v3.0
(default: mitigation 2, direct `program_map` in `PLAN_v3.md`). Not
required for v3 engineering slices.

**Idea.** Ecology grower describes each actor's behavior in **plain
prose** (similar voice to Part C, but per role/actor — e.g. "engineer
who prioritizes draft reports, requests access when blocked, rarely uses
lab chat"). An **implementer-run** LLM call (or isolated subprocess
with no repo/oracle access) maps prose → validated `ProgramMap` JSON.
Grower never sees `pattern_scores` bins or preset expansion tables.

**Why bother.** Reduces direct tuning of the shared goal-feature
coordinate system while keeping heterogeneous actors. Closer to how a
real institution would specify "this hire's style" without writing
softmax tables.

**Rough shape (medium):**

1. **Schema:** optional `behavior_description` string per actor in
   `role_population`; mutually exclusive with inline `program_map` in
   the strict protocol (prose-only submission).
2. **Frozen compiler** in `BLIND_GENERATION.md` + `program_map_compiler.py`:
   prompt = primitive API + role + prose + output JSON schema only;
   explicitly excludes detectors, severity, criteria, FINDINGS.
3. **Validation gate:** `validate_program_map()` only; failed compiles
   reported as grower-facing "could not compile behavior" without
   revealing scorer internals (same pass/fail discipline as C-checks).
4. **Reproducibility:** pinned model id, temperature 0, structured output;
   log prompt/hash/output on every compile for replay; report
   compiler-null diversity (N random prose snippets → phenotype spread).
5. **Prior-risk battery:** hand-written prose fixtures designed to tempt
   generic "compliance-heavy" maps; measure systematic bias before trusting
   Q1 transfer claims on compiled ecologies.

**Blocked by:** v3 slice F (`ProgramMap` validation). **Pairs with:**
mitigation 1 (frozen presets if compile fails?) — policy TBD at protocol
freeze. **Does not replace:** `REPRODUCTION.md` §3 if grower retains
shell/repo access during growth.

---

## 10. Slice D reference-battery calibration (implemented, GL-53)

**Status:** *done for criteria constants* — not a deferred package. Listed
here so repro paths sit beside the backlog items that still depend on it.

**What was frozen.** v3 reference checker horizon ``V3_REFERENCE_T=200``
(v2 reference battery unchanged at ``T=100``); C3/C4/C1-v3/C5-v3 thresholds
unchanged but validated on the integrated fixture; confidence table in
``DESIGN.md`` § PLAN_v3 slice D.

**Reproduce calibration snapshot (~9 min, n=50):**

```bash
cd experiments/graded-lab-simulation
python3 scripts/run_slice_d_reference_battery.py
# → results/slice_d_reference_battery_T200_n50.json
```

**Pre-Q1 batteries (GL-54/GL-55, ~3–8 min each on integrated reference):**

```bash
python3 scripts/run_v3_detector_coverage_battery.py --seeds 20
# → results/slice_d_v3_detector_coverage_T200_n20.json

python3 scripts/run_program_map_phenotype_overlap.py --variants-per-actor 12
# → results/slice_d_program_map_phenotype_overlap.json
```

The phenotype-overlap script's first pass (GL-54) reported a spurious
100% overlap: two harness bugs in `graded_lab/harness/phenotype_overlap.py`
made every sampled mutation structurally inert (mutated temperature/
goal_weights were never applied to the episode; sampled variants stayed
in the `walker_only` mode, which `resolve_runtime_genotype` dispatches
straight to the frozen preset function without reading `ProgramMap`
fields at all). GL-55 fixed both — variants now force `mode="scorer_only"`
and the resolved temperature/goal_weights are applied — and the command
above reproduces the corrected 0–12.5% overlap result. See FINDINGS.md
GL-55 for detail; `DESIGN.md` § slice D still flags walker/hybrid maps as
runtime-unreachable pending a generic walker-step interpreter.

**Reproduce checker tests (n=20, ~5 min each slow test):**

```bash
pytest tests/test_slice_c_scorecard.py::test_reference_battery_passes_c1_v3_at_frozen_horizon \
  tests/test_slice_b_completion.py::test_c3_contention_liveness_on_integrated_reference_battery \
  -m slow --no-speed-check
```

**Short-horizon regression** (documents pre-GL-53 failure mode, fast):

```bash
pytest tests/test_slice_c_scorecard.py::test_c1_v3_not_exercised_when_episode_horizon_too_short -q
```

**Slice D brief frozen (GL-69).** Part B retargeting ✅ (GL-62); supplementary
detector ✅ (GL-60); causal C2-v3 ✅ (GL-59/68); supplementary UAD ✅ (GL-65);
attention surface ✅ (GL-66/67). **V3 grown ecology frozen (GL-73)** after valid
round 2 (GL-72). Still deferred: generic walker-step interpreter; v3 strict mode
→ §8; service-oriented isolate → §11; **V2-3 Q1 harness implemented (GL-75), not run**.

**Post-freeze pre-Q1 batteries on frozen grower ecology (GL-74, ~8–15 min):**

```bash
cd experiments/graded-lab-simulation
python3 scripts/run_v3_detector_coverage_battery.py \
  --fixture generated_ecology_v3.json --seeds 20 \
  --out results/v3_grown_detector_coverage_T200_n20.json

python3 scripts/run_v3_supplementary_detector_gate.py \
  --fixture generated_ecology_v3.json \
  --out results/v3_grown_supplementary_detector_gate.json

python3 scripts/run_program_map_phenotype_overlap.py \
  --fixture generated_ecology_v3.json \
  --out results/v3_grown_program_map_phenotype_overlap.json
```

Use ``.venv/bin/python`` if the project venv is active. ``machinery_transfer_verified``
must be ``true`` on the grown ecology before citing Q1 detector-transfer claims.

---

## 10.1 V2-3 Q1 machinery transfer battery (GL-75–GL-77)

**Status:** *executed* (GL-76) — P1–P3 false, go gate false; Q1 null harvested to manuscript;
BIQ singleton fix + re-run (GL-77). V2-4/5/6 descoped.

**Target ecology:** ``generated_ecology_v3.json`` (``ecology_version="v3_grown"``).

**What it runs (frozen machinery, no threshold edits):**

1. C5 declared mechanisms → UAD ground-truth catalog (all four kinds).
2. Reference ``WEAK_AGENT`` episodes: passive UAD + all-pairs intervention (P1, P2).
3. EAI agent-vantage (``full`` tier) vs referee-vantage (``light`` tier) over
   ``CARRIER_SCALES`` (P3 + go/no-go for V2-5/V2-6).
4. Ecology-BIQ on passive-inferred partition units, singletons included (subset of seeds).
5. Honest detector coverage (P4) + onboarding median ticks-to-deploy (V2-6 input).

**Output:** ``results/v2_transfer.json`` with ``predictions.P1``–``P4``.

**Reproduce (full run, ~10–30 min with ``--workers 4``, ~30–90 min serial):**

```bash
cd experiments/graded-lab-simulation
.venv/bin/python scripts/run_v2_transfer_battery.py \
  --fixture generated_ecology_v3.json \
  --out results/v2_transfer.json \
  --workers 4
```

Use ``--workers 1`` for deterministic single-process execution (tests, debugging).

**BIQ-only re-run** (after GL-77 singleton fix; skips UAD intervention + EAI):

```bash
.venv/bin/python scripts/run_v2_biq_only.py --workers 4 \
  --out results/v2_transfer_biq.json \
  --patch-transfer results/v2_transfer.json
```

**Smoke / harness validation only:**

```bash
.venv/bin/python scripts/run_v2_transfer_battery.py --smoke --no-biq
pytest tests/test_machinery_transfer.py -q --no-speed-check
```

**Module:** ``graded_lab/harness/machinery_transfer.py``; pre-registered constants
at module top (``UAD_SEEDS`` = ``C3_SEEDS``, ``EAI_SEEDS`` = ``CALIBRATION_SEEDS``,
``P1_COMMUNICATE_MAX_MEMBERS`` = 3, ``MECHANISM_MAJORITY_SEED_FRACTION`` = 0.5).

**Scoring rules (GL-75b, frozen before first full run):**
- P1 communicate pool excludes ``message_channel`` mechanisms with >3 members
  after role expansion (avoids whole-roster ACL co-cluster geometry).
- P1 pass: >= half of pool mechanisms have seed-hit rate >= 0.5 (not mean of rates).
- P4: honest-reference sparsity only; blocking detector gate is
  ``machinery_transfer_verified`` (supplementary gate, already true on v3_grown).
- Go gate for V2-5/V2-6: referee EAI mid band at **default load** (carrier=1.0).

---

## 11. Realistic isolate interior — service-oriented agent runtime

**Status:** *deferred* — design agreed 2026-07-16; not blocking v3 round 1
or GL-66 (host-side attention surface / ``desk.scan`` via ``call`` endpoints).

**Gap.** Graded-lab agents today run as **pure decision functions** over a
host-pushed JSON observation (`affordable_primitives`, resources, …) and
return a JSON primitive dict. ``SubprocessIsolate`` (`agent_main.py`) is
JSON Lines on stdin/stdout; ``MockIsolate`` calls the same functions
in-process. That boundary is clean for plane separation and fast tests,
but the **inside of the isolate is nothing like a real lab worker**:

- No workspace files the agent reads/writes incrementally.
- No intranet services (desk, catalog, calendar) — only a flat action menu.
- No comms library with channels, threads, or delivery semantics — only
  ``communicate`` entries embedded in the menu.
- LLM red-team (§7) and grower-facing Part C knowledge-base prose describe
  institutional coordination in human terms that the runtime does not mirror.

The near-term GL-66 fix (attention surface + ``desk.scan`` on the host)
makes the **published menu** more realistic but still pushes a dict across
the wire. Agents never *discover* the desk by opening a browser or polling
WebCAL — they receive whatever the host chose to list.

**Why the cheap fix isn't enough.** Host-side ``desk.scan`` endpoints preserve
the isolate contract and unblock cap starvation (communicate dropping after
~20 workspace paths). They do **not** let us claim that subprocess/LLM agents
operate through the same surfaces a human hire would (files, HTTP services,
lab chat). For V2-6 red-team and manuscript "embedded agent" claims, the
gap between Part C prose and isolate mechanics will remain visible unless
the interior is upgraded.

**Relationship to other items.**

| Item | Overlap |
|------|---------|
| **§3** (trusted pilot / grower sandbox) | Outward blinding — restricts what a **grower** can import/see. Item 11 is inward realism — what an **actor isolate** experiences. Complementary; neither substitutes for the other. |
| **GL-66** (attention surface) | Host publishes desk/catalog via ``call`` + ``affordable_primitives``. Item 11 exposes the **same host services** over HTTP/WebCAL inside the isolate so agent code uses services, not raw obs fields. GL-66 should define the service semantics Item 11 later wraps. |
| **embedded-simulation** | Prior art: Node isolate + sync host bridge, VFS ``fs.*``, ``fetch`` POST to host routes, ``localStorage``-backed DOM file (``experiments/embedded-simulation/isolate/``). Graded-lab should reuse patterns, not fork ad hoc. |
| **lab-simulation** | Prior art: ``comms_enabled``, board/channel abstractions in ecology builders. Graded-lab v3 mechanisms should map to a **comms lib** API inside the isolate, not only to primitive-log ``communicate`` rows. |

**Rough shape (large — multi-week, after GL-66 lands):**

1. **Host service plane (world-visible, already partially specified for GL-66):**
   - **WebCAL** — HTTP surface for the attention desk: prioritized feed
     (interleaved, capped), archive window metadata, optional iCal-like
     subscription for standing channels / scheduled sync slots. Same semantics
     as ``desk.scan`` / push surface; HTTP is transport only.
   - **DOM file / agent VFS** — per-actor workspace mirror (read/write/append,
     ``localStorage``-style persistence across ticks within an episode).
     Pipeline artifacts and governed paths appear as files, not only as
     menu rows. Prior art: embedded-simulation ``facade.js`` +
     ``/home/agent/.localStorage.json``.
   - **Comms lib** — channel membership, send/receive, thread history
     bounded per tick (analogue of desk cap for messages). Maps to v3
     ``message_channel`` mechanisms and ACLs; primitive log remains the
     audit projection.

2. **Isolate runtime (agent-visible):**
   - Replace JSONL ``{observation} → {primitive}`` as the *primary* agent
     interface with a **script runtime** (Node or Python subprocess) that
     exposes ``fs``, ``fetch`` (WebCAL routes), and ``comms`` — agent code
     written like a lab worker (poll desk, open files, post to channel).
   - Host bridge translates service calls into the existing primitive /
     scheduler / ACL enforcement layer (no oracle leakage through HTTP).
   - Keep a **compatibility shim**: frozen ``programs.py`` presets can run
     in MockIsolate for fast batteries; service-runtime isolates for LLM
     red-team and realism claims.

3. **Observation contract:**
   - Boundary stream records **service I/O** (HTTP paths, file paths,
     comms channel ids) plus resource snapshot — not a pre-digested
     ``affordable_primitives`` list. UAD/detectors consume primitive log
     as today; define mapping from service actions → log entries.

4. **Knowledge-base alignment:**
   - Part C documents (grower + reference templates) describe desk,
     catalog scan, and comms the way the service runtime exposes them.
   - ``BLIND_GENERATION.md`` v3 brief: qualitative disclosure that actors
     interact via lab services; withhold surfacing constants and HTTP
     route internals from growers (same class as C-threshold withholding).

5. **Tests and freeze discipline:**
   - Contract tests: bridge RPC parity (embedded-simulation-style smoke).
   - Plane tests: no oracle fields in VFS/HTTP responses.
   - ``CODE_VERSION`` bump + FINDINGS entry; expect digest re-pins and
     possible UAD trace mapping updates — same blast-radius class as GL-50.
   - V2-6 (§7) blocked on this **or** an explicit "JSONL-only red-team"
     scope downgrade.

**Blocked by:** GL-66 service semantics frozen on host; v3 round 1 not
required to wait. **Pairs with:** §7 LLM red-team, §9 text→ProgramMap
(compiler output could target service-runtime scripts, not dict presets).

**Not in scope:** Replacing grower pilot isolation (§3) or mutating v1/v2
digest replay — plan for a new isolate backend name (e.g.
``ServiceSubprocessIsolate``) alongside existing Mock/Subprocess backends.

---

## Status of items already fixed this pass (GL-42, not on this list)

For contrast — these were judged small enough to fix directly rather
than defer:

- Poisson trigger corrected to be actually memoryless (no fixed
  refractory cooldown).
- Candidate/pilot staging no longer mutates the shared canonical
  `generated_ecology_v2.json` (`EpisodeConfig.ecology_override_path`).
- C3's blinding claim retracted and replaced with an honest disclosed-
  requirement framing (this was cheap to *document* even though the
  underlying design tension — "you cannot both let the grower observe
  queueing and credibly hide whether the ecology has enough of it" — is
  not something engineering can fix; it's a scope decision, made).
- End-to-end test proving a multi-actor + workload ecology can clear
  C3 while staying in C4's interior band, through the real checker.

## Later tightening (not v3.0)

- **Slice A flow-vs-declared-total cross-check:** v3.0 warns at ±25%
  per resource type; tighten to ±10%, ±5%, or ±1% hard-fail once
  reference batteries show false-warn rates are acceptable.
- **C2-v3 contribution floor:** v3.0 draft uses ≥5% per principal;
  tighten toward ≥10% if growers routinely pass with token flows.

See `PLAN_v3.md` slice A.

See `results/FINDINGS.md` GL-42 for the full external-review record.

---

## 8. v3 strict mode / richer authorization (deferred — GL-61)

**Status:** *not chosen for slice D Part B closure* (human decision
2026-07-16). Round-1 load-bearing Part B closes via **retargeting reference
presets** instead (`PLAN_v3.md` slice B/D, `BLIND_GENERATION.md` § V3 gate).

**Gap.** Slice B ACLs are opt-in: agents using v1 patterns (`communicate` on
`"lab"`, path-only read/write, no `vote.cast`) never hit the compiled
mechanism layer. **Retargeting** closes this for frozen reference presets by
having preset logic choose governed ids from affordances. **Strict mode**
would additionally deny unbound surfaces globally on v3-shaped ecologies —
stronger institutional claim, but breaks v1-like bypass for *all* agents
(including future grower `ProgramMap`s) and needs careful C3/C4 liveness
validation (GL-50 lesson).

**Why deferred.** Strict mode (or a more complex authorization scheme —
capability lattices, default-deny artifact namespaces, etc.) is worth
revisiting for mitigation-2 rounds, manuscript "institutional realism"
claims beyond round 1, or if retargeting alone leaves decorative Part B
passing on structure. Not blocking the mitigation-1 growth path once
retargeting validates.

**Rough shape (medium — if revisited):**

1. Ecology-scoped flag (e.g. on v3 JSON) enabling default-deny for unbound
   channel names, path-only artifact I/O, and vote/transfer bypass.
2. Regression: v1/v2 digest replay unchanged; integrated reference C3/C4/C1-v3
   at T=200; C5-v3 negative controls.
3. Document interaction with grower-authored `ProgramMap` before any
   mitigation-2 brief uses it.
