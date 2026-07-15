# PLAN v3 — institutional runtime wiring

**Status (build order):** slices **A**, **F**, **E**, **C** done; slice **B** partial
(enforcement + reference opt-in gate); **slice D criteria partial**
(GL-53); growth protocol + pre-Q1 batteries still open.
Supersedes the V2-2b growth program (closed without a growth round,
GL-43) as the next step of the graded-lab v2 program (`PLAN_v2.md`
Q1–Q3 stand; this plan replaces V2-2b's row on the path to a passing
ecology). Origin: external review GL-42 established that C1/C2/C5
check declared JSON the runtime never consumes and that C3's blinding
was untenable once a pilot exists; the user decided (GL-43) to wire
institutional structure into the runtime *before* any new growth
attempt rather than grow toward a weakened declarative target.

Source material: `REPRODUCTION.md` items 1 (institutional structure
executable), 2 (real work injection), and 4 (heterogeneous roles) —
items judged in-scope for v3. Item 3 (execution-isolated pilot
service) stays out of scope: with C3/C4 no longer claimed blind, no
current criterion needs it (revisit only if a v3 criterion
reintroduces something that must stay hidden from an agent with pilot
access).

## Goal

Make a candidate ecology's Part B (`principals`, `conflicts`,
`mechanisms`, `resource_flows`) **causally load-bearing at runtime**:
compiled into per-actor budgets, enforced channel/artifact/vote
permissions, injected work, and referee-visible objectives — so that a
future growth program's criteria check the **compiled runtime**, not
grower prose, and Q1 ("does frozen v1 machinery transfer to an ecology
it was not co-developed with?") can honestly claim the ecology has
*live* multi-principal incentive structure.

## Non-negotiable constraints (carried from v1/v2)

1. **v1 untouched.** `ecology_version="v1"` behavior stays
   byte-identical (`PINNED_V1_DEFAULT_DIGEST` in
   `tests/test_ecology_version.py` must not move). v2-shaped JSONs
   (`ecology_version` key, V2-2 round artifacts) also stay replayable
   as-is: v3 is a **new ecology version** (`"v3"` / new schema tag),
   not an in-place mutation of v2 semantics.
2. **Conclusions never named in definitions** (AGENTS.md): v3 criteria
   thresholds are fixed against reference batteries *before* any
   growth brief, not tuned until a grower can pass.
3. **Frozen machinery means frozen** during any Q1 transfer battery
   (PLAN_v2 design principle 5).
4. **Honesty about what is and is not blinded.** Per GL-42: blinding
   claims attach to the oracle/referee plane (EAI, severity,
   detectors, UAD ground truth), never to criteria whose phenomena the
   designer can observe by piloting.
5. **Cheap tests.** `role_population` defaults to n=1 per role;
   heterogeneity and work injection default off. Tests and smoke runs
   stay at ~v2 cost; multi-actor/injection cost is opt-in per ecology
   (GL-43 user decision).
6. **Progress logging** on any battery > ~1 min (AGENTS.md).

## Architecture: one compilation step

New module `graded_lab/world_visible/institutional_compiler.py`:

```text
compile_ecology(data: dict) -> RuntimeEcology
```

Called once at `run_episode` load time for v3-shaped ecologies (cost:
negligible, once per episode). `RuntimeEcology` is a frozen dataclass
bundle consumed by the episode loop:

- `allowances_by_actor` (slice A)
- `channel_acls`, `artifact_acls`, `vote_specs`, `transfer_specs` (slice B)
- `principal_objectives` (slice C — referee-plane, exported to
  `oracle_only`, never into agent observations)
- `pressure_coupling_specs` (slice E)
- `actor_overrides` (slice F)

v1/v2-shaped ecologies bypass the compiler entirely (no behavior
change). Estimated steady-state episode-loop overhead for a fully
wired v3 ecology: single-digit percent (ACL dict lookups per
read/write/communicate, allowance derivation at load, vote state only
when a vote is active); multi-actor headcount remains the dominant
cost factor and is n=1 in tests.

---

## Slice A — `resource_flows` → live budgets

**Gap closed:** allowances currently come from fixed
`resource_allowances_per_tick[role]` regardless of declared funding
structure (`REPRODUCTION.md` §1, GL-42 item 1).

**Accounting (frozen at slice A start — not revisited mid-implementation):**

1. **Whole allowance, not a delta.** For v3 ecologies, compiled flows
   **replace** role defaults at runtime. An actor's effective per-tick
   allowance for each resource type = **sum of `amount_per_tick` over
   compiled flows that reach it** (same reachability semantics as C2).
   `resource_allowances_per_tick` is **declarative only** — a cross-check
   target, never added on top of compiled totals.
2. **Valid amounts.** Each `amount_per_tick` must be a **finite
   non-negative number**. Reject NaN, infinities, and negatives at schema
   validation.
3. **Required coverage.** Every active actor must receive a compiled
   source for **compute** and **io** (minimum consumable resources).
   Missing required coverage → **schema validation fail**, not a silent
   zero-allowance episode (avoids GL-36-style standing lockouts dressed
   as "empty funding graph").
4. **Cross-check (unchanged posture).** Summed flows vs declared
   `resource_allowances_per_tick` totals: **warn** at ±25% per resource
   type in v3.0 (hard-fail tightening deferred to `REPRODUCTION.md`).

**Spec:**

1. v3 `resource_flows` rows gain a required `amount_per_tick` (number)
   and keep `principal_id` / `mechanism_id` / `role` (v3 may target
   `actor_id` too, see slice F). `resource_type` maps onto ledger
   fields: `compute_allowance` → compute/tick, `io_allowance` →
   io/tick, `standing_recovery` → standing recovery rate,
   `standing_stock` → initial standing, `grant_approval` → bootstrap
   capability grants.
2. *(Accounting rules above — items renumbered.)*
3. C2-v3 criterion: for every role, ≥ 2 distinct principals'
   flows contribute **≥ 5% each** (draft, loose — thresholds frozen
   at **slice D**, not slice A; validated against reference batteries
   first per GL-36).
4. **Slice A validation gate (pre-registered, engineering-only — not a
   growth criterion):** prove compiled flows are **causally load-bearing**
   on a frozen hand-built fixture before slice B starts.

   | Field | Frozen value |
   |---|---|
   | Fixture | `tests/fixtures/ecology_v3_slice_a_reference.json` (+ provenance note in fixture metadata) |
   | Roster | `WEAK_AGENT`, default load, `role_population` n=1 per role |
   | Seeds | `{0, 2, 4}` (seed 1 failed L1 threshold on first battery — not retuned post hoc) |
   | Load | `carrier_load_scale = 1.5` (default 0.0 leaves ablation inert for this roster; frozen in fixture metadata) |
   | Ablation | Zero `amount_per_tick` on one designated row (`ablation_target_flow_id` in fixture metadata — the larger of two unequal engineer compute flows: 30 vs 10; chosen to avoid a degenerate near-total-starvation split, see negative control below) |
   | Pass rule | On **≥ 2 / 3** seeds, ablation vs full run differs on **either**: (a) `deploy_count`, **or** (b) normalized primitive-pattern histogram L1 distance ≥ **0.10** |

   Constants (`0.10`, seed set, roster, ablation row id) are written
   into the fixture **before** the first ablation battery run — not tuned
   after observing outcomes (GL-36 discipline).

   **Negative control (added after self-review):**
   `test_slice_a_ablation_gate_negative_control_at_default_load` reruns the
   same ablation at the ecology's *default* `carrier_load_scale = 0.0` and
   asserts it must **not** diverge on all 3 seeds — evidence that the
   positive gate's `1.5` requirement is doing real work, not padding an
   unconditional pass. This control caught a real bug: an earlier fixture
   split (`38`/`2`) was degenerate (near-total starvation at *any* load,
   including `0.0`), which the negative control flagged immediately. See
   FINDINGS GL-44 addendum for the full account.

5. **Hand-built reference fixture (slice A minimum):** implementer
   authorship; frozen in-repo before the ablation gate runs. Must
   include ≥ 2 principals funding the engineer role with **deliberately
   unequal** compute flows so severing the dominant row materially
   lowers allowance. Used only to validate compiler wiring + gate (4);
   **not** used to calibrate C2-v3/C3 thresholds (those wait for slice D
   fixtures and batteries).

**Later gates (explicitly not slice A):** C2-v3 contribution floors,
vote semantics (slice B), principal scorecard vocabulary (slice C),
`ProgramMap` bin tables (slice F) — unchanged deferral.

**Anticipated critic — hand-built reference fixture:**

- **"Developed-to-the-test."** True at engineering scope: the implementer
  picks flows known to ablate. That is intentional for wiring validation
  (same class as Phase 7a golden ecologies). It does **not** support Q1
  transfer claims — only "the compiler is connected."
- **"Same roster cherry-pick as GL-36."** The gate uses `WEAK_AGENT`
  because that is the frozen reference roster, not because it is the only
  agent that works. Report if ablation is inert under other frozen
  presets — that is a wiring bug, not a reason to change the gate
  constants post hoc.
- **"Threshold gaming."** If `0.10` or the ablation row is adjusted after
  a failed battery, that repeats GL-36. Fixture + gate constants are
  version-controlled artifacts; failures are FINDINGS entries, not retunes.
- **"Declarative theater again?"** The gate requires **behavioral**
  divergence (deploy or pattern histogram), not JSON reachability alone —
  the failure mode GL-42 flagged for C1/C2/C5.
- **Acceptable claim if gate passes:** "v3 compiled flows change runtime
  allowances and measurably shift reference-agent behavior under ablation."
  **Not claimable:** "grown ecologies will be institutionally realistic" —
  that requires slice D batteries on separate fixtures and eventual blind
  growth.
- **"Mechanisms/principals mostly decorative at runtime."** True at slice A
  close, **partially closed at slice B**: `message_channel`, `shared_artifact`,
  `resource_transfer`, and `joint_approval_vote` mechanisms now compile to
  enforced ACLs/vote specs the dispatch layer actually checks. Still
  decorative: **no reference agent program yet exercises any of this** — the
  enforcement exists and is tested at the compiler/dispatch level, but
  nothing in `programs.py` chooses to communicate on a governed channel,
  write to a governed artifact by id, execute a transfer, or cast a vote.
  That agent-side exercise (and the C5-v3 "≥3 kinds exercised" criterion) is
  slice D's job. `principals` remain fully narrative — slice C adds
  objectives/scorecard (referee-plane only); slice D re-derives C2-v3
  contribution-floor thresholds against real batteries before any growth
  round.
- **"Behavioral signal is thin (one agent, one histogram, OR rule)."**
  Correct for slice A's engineering-only gate. Broadening the signal
  (multi-actor histograms, a stricter AND rule, more seeds, additional
  hand-built fixtures beyond one) is deliberately deferred to slice D's
  reference-battery calibration — widening the gate now, before mechanisms
  are enforced, would validate the wrong thing (flow wiring, not the
  eventual growth criteria the signal needs to support).

**Touches:** `institutional_compiler.py` (new), `substrate.py`
(v3 validation), `world.py` (`_allowances_map` reads compiled
allowances), `ecology_complexity.py` (C2-v3 at slice D), fixture +
`tests/test_v3_slice_a_flow_ablation.py`, DESIGN.md schema (accounting
paragraph only — full v3 pre-registration still slice D).

**Overhead:** load-time only; ~0% steady-state.

## Slice B — `mechanisms` → enforced coordination

**Status: partial close (2026-07-15, GL-45 wiring; GL-48 engineering gate; GL-48b scope
correction `graded-lab-0.24.1`).** Enforcement is proven; **load-bearing Part B**
for ordinary agents is **not** closed — see claim scope below.

**Gap closed:** `communicate` channels are free-form; artifact access
is unrestricted; `joint_approval_vote` has no runtime meaning
(`REPRODUCTION.md` §1 item 2).

**Spec per mechanism kind (as implemented):**

| kind | runtime binding |
|---|---|
| `message_channel` | `communicate(channel=X)` where `X` matches a compiled channel id: allowed **only** for actors whose role is in `members_ground_truth`; others get `{"status": "denied", "reason": "not_channel_member"}`. Channel names that do not match a compiled id (e.g. v1/v2's `"lab"`) are unenforced. |
| `shared_artifact` | `read`/`write` carrying an explicit `artifact_id` matching a compiled id: **denied outright** (not cost-scaled — design gate) for non-member roles; `reason: "not_artifact_member"`. Plain reads/writes without an `artifact_id` are unenforced (backward compatible). |
| `resource_transfer` | new endpoint `call(endpoint="transfer.execute", args={mechanism_id, target_actor_id})`; both the caller's and the target's role must be in the mechanism's members, else `"not_transfer_member"`. |
| `joint_approval_vote` | new endpoint `call(endpoint="vote.cast", args={vote_id, approve})` (free — no standing cost, design gate); quorum = majority-of-members only (no per-mechanism override yet); a pipeline step may declare `requires_vote: <mechanism_id>` and is denied `vote_pending` until quorum, `vote_denied_timeout` if the mechanism's `timeout_ticks` (default `10`) elapses without quorum — **no escalation path** (design gate). |

**Design gate (pre-registered, human review before code — answered
2026-07-15, all recommended/simplest options, frozen in
`institutional_compiler.py`'s module docstring and DESIGN.md):** vote
quorum majority-only; timeout **fails** the gated step, no escalation;
`vote.cast` is free; non-member `shared_artifact` access is denied
outright, not cost-scaled.

**C5-v3 criterion (reference opt-in, GL-48/GL-48b):** ≥ 3 mechanism kinds
**exercised** in the **same** ``WEAK_AGENT`` reference battery when the ecology
declares ``reference_mechanism_exercise`` (host merges targets into
``behavior_profile`` — **not** ecology ``ProgramMap`` genotypes). Checked by
``check_c5_v3`` on ``run_reference_episodes`` results. Ecologies without the
field skip C5-v3 (``None``). **Does not** claim grower-chosen programs exercise
Part B; ordinary paths still use unbound ``lab`` / path-only I/O unless slice D
strict reference or grower maps require governed ids.

**Anticipated critic — opt-in ACL enforcement:**

- **"Mechanisms are still optional theater."** Partially true at slice B
  close: ACL checks activate **only when the action explicitly names a
  compiled mechanism id** (`communicate` with a channel id matching a
  `message_channel`; `read`/`write` with `artifact_id` matching a
  `shared_artifact`; `transfer.execute` / `vote.cast` by mechanism id).
  Agents that keep using v1/v2 patterns — default `"lab"` channel,
  path-only read/write, no vote casts — **never hit the ACL layer**. A
  grower can declare a rich Part B and still get v1-like behavior if
  reference programs never target governed ids. This is intentional for
  v1/v2 byte-identical replay and zero regression on digest-pinned
  tests, but it means C5-v3 ("present **and exercised**") cannot pass on
  declared structure alone.
- **Why not enforce by default on v3?** Would require either (a)
  renaming/binding all default communication and artifact paths to
  compiled mechanism ids, or (b) a global v3 strict mode that denies
  unbound channel/artifact surfaces — both break backward compatibility
  and expand slice B scope. Deferred to slice D: reference agent
  programs / `ProgramMap` must **require** governed ids (or a v3 ecology
  flag must narrow the unbound surface) before growth claims "live
  multi-principal coordination."
- **Acceptable claim at slice B close:** (1) When an action targets a compiled
  mechanism id, dispatch enforces ACL / vote semantics. (2) On the integrated
  reference fixture, one ``WEAK_AGENT`` battery co-exercises slice A flows, slice
  E pressure injection, and slice B mechanisms **when** the ecology declares
  ``reference_mechanism_exercise``. **Not claimable:** "Declared mechanisms
  constrain all reference-agent behavior" or "grower ``ProgramMap`` genotypes
  exercise Part B" — deferred to slice D.

**Touches:** `institutional_compiler.py` (`_compile_mechanism_runtime`,
`VoteSpec`), new `votes.py` (`VoteService`), `world.py`
(`_execute_primitive` ACL checks + `vote.cast`/`transfer.execute`
endpoints, `run_episode` threads the compiled `RuntimeEcology` through),
`pipeline_spec.py` (`PipelineStep.requires_vote`), `pipeline_engine.py`
(`trigger_step` vote gate, same extension pattern as the existing
`permission_service` check), `tests/test_slice_b_mechanisms.py` (new,
18 tests). UAD live-coupling gate (GL-48b): passive UAD recovers governed
channel unit when ``reference_mechanism_exercise`` is active — not a full
Q1 transfer claim.

**Overhead:** ACL dict lookup only on actions that explicitly reference a
compiled mechanism id (empty dict lookup otherwise); vote state only
while a vote is open. No measured regression in `--profile fast` (all
tests green).

## Slice C — `principals` + `conflicts` → referee-visible objectives

**Gap closed:** principals/conflicts are narrative; referee severity /
EAI never read them (`REPRODUCTION.md` §1 item 1).

**Spec:**

1. v3 `principals[].objective_metric` must name a metric from a
   **closed, implementer-frozen vocabulary** mapped to measurable
   episode quantities: `deploy_rate`, `bearer_harm`,
   `field_incident_rate`, `release_latency`, `compute_burn`,
   `review_thoroughness` (exact list frozen in DESIGN.md v3; grower
   chooses from it, cannot invent unmeasurable metrics).
2. Referee plane (`oracle_only`) gains a **principal scorecard**: per
   episode, each principal's objective delta, computed from Tier-K
   ground truth. Never enters agent observations (plane discipline
   unchanged).
3. `conflicts` validation upgrades from prose-length check to
   **measured tension**: for each declared conflict pair, the two
   principals' scorecard deltas must be **negatively correlated across
   the reference battery** (draft criterion C1-v3; exact statistic and
   threshold frozen before any brief; if reference agents don't
   exercise the tension, that is a reportable finding, not a silent
   pass).
4. **Optional, flagged, default-off:** derive agent `GoalWeights` from
   funding shares (an actor mostly funded by the throughput-principal
   weights task higher). This couples slice C to agent behavior and
   has the highest developed-to-the-test risk — implement last, behind
   a config flag, with its own FINDINGS entry, or defer out of v3
   entirely at design review.

**Touches:** `oracle_only/` (scorecard module), `ecology_complexity.py`
(C1-v3 measured-tension check), DESIGN.md metric vocabulary; item 4
would touch `ecology_agents.py`.

**Overhead:** scorecard is post-episode referee work; ~0% on the loop.

**Status: implemented (2026-07-15, GL-49, `graded-lab-0.25.0`).**

**GoalWeights derivation:** **deferred out of v3.0** (design gate default-off;
not implemented behind a flag in this slice).

## Slice E — feedback-coupled work pressure (not exogenous noise)

**Gap closed:** v2's `exogenous_workload` only multiplies costs of actions
agents already chose; v2-2b's Poisson/periodic triggers add **free
standing noise** unrelated to what the lab's outputs actually did
(`REPRODUCTION.md` §2, GL-42 item 4; user review 2026-07-15).

**Design principle:** pressure should **follow from in-simulation
state the lab's own pipeline created**, not from an RNG stream whose
mean the grower dials independently of outcomes. We cannot model the
whole outside world, but we *can* tie generic workload-event rates to
oracle-visible quantities that deployed models and field monitoring
already influence — e.g. higher measured capability / wider deployed
footprint → more user-population exposure → more generic
incident-review and audit tasks. The coupling is **deterministic given
simulation state**; any remaining stochasticity is confined to
*which* generic event kind fires when pressure crosses a threshold,
not to inventing demand unrelated to outputs.

**Spec (minimum viable):**

1. Replace v2's standalone `exogenous_workload` block with v3
   **`pressure_coupling`**: a list of **pressure channels**, each
   declaring:
   - `id`, `roles_affected`, `task_kind` (from frozen vocabulary),
   - **`driver`**: a closed vocabulary reference to an in-simulation
     signal (implementer-frozen, grower picks and scales — not invented
     names): e.g. `deployed_model_count`, `mean_deployed_capability`,
     `integrated_field_harm_rate`, `active_user_archetype_mass`,
     `pending_access_queue_depth`, `eval_draws_outstanding`.
   - **`gain`** and **`threshold`**: pressure accumulates each tick as
     `gain × driver_value`; when accumulated pressure crosses
     `threshold`, inject `count` tasks (same queue machinery as before)
     and reset or decay the accumulator (decay rule frozen in
     DESIGN.md v3 — draft: linear decay `× (1 − decay_per_tick)` so
     pressure falls when drivers fall).
2. On threshold crossing, append **task items** to a per-role world
   queue. Task kinds remain a small frozen vocabulary — v3 minimum:
   `incident_review` (`read` of a synthesized incident artifact tied
   to the driver snapshot + `write` of a response note). Artifact
   content is **derived from the driver state at injection time**
   (deterministic template), not RNG fluff.
3. Injected tasks surface in the affordable set as ordinary
   primitives (referee log marks `injected: true`; agents see work,
   not oracle field names).
4. **Expiry semantics (unchanged from prior draft):** unserviced tasks
   expire after `expiry_ticks`; `expired_task_count` on referee
   plane only; no escalation in v3.
5. **Optional v3.0 carry-over:** the v2 cost-multiplier window
   (`resource_demand_scale` during active surges) may remain as a
   *secondary* effect when a pressure channel fires, but the **primary
   demand signal is task injection**, and the trigger is the pressure
   accumulator, not an independent Poisson draw. Pure Poisson/periodic
   triggers with no driver are **not** in v3 — they belong in
   `REPRODUCTION.md` as a rejected pattern unless reintroduced with an
   explicit endogenous driver.

**Grower-facing story:** "when our deployed models are more capable /
more exposed in the field, generic audit and incident-handling work
increases" — stated as `gain`/`threshold` on named drivers, not as
hidden contention knobs.

**Touches:** new `pressure_coupling.py` (replaces/extends
`exogenous_workload.py` for v3), `affordable.py`, `world.py`,
`oracle.py` (driver signal exports on referee plane only),
`workspace.py`, referee logging.

**Overhead:** ~0% when no channels configured; per tick: O(channels)
deterministic driver reads + float accumulators (negligible vs
scheduler).

**Status: implemented (2026-07-15, GL-47, `graded-lab-0.23.0`).**

## Slice F — heterogeneous roles + composable `ProgramMap`

**Gap closed:** `role_population` builds N identical clones
(`REPRODUCTION.md` §4, GL-42 item 6). Also closes the design-space
gap: a single `program` name plus a few floats does **not** yield a
practically large or mutation-ready genotype (see § Grower agent design
space below).

**Spec:**

1. v3 `role_population` values may be either the v2 integer (clones,
   backward-compatible) or a list of per-actor override objects:
   `{goal_weights?, program?, program_map?}` — count = list length.
   Exactly one of `program` (legacy preset key) or `program_map`
   (structured genotype) per actor; if both absent, frozen role fallback
   applies.
2. **`ProgramMap`** — the v3 per-actor behavioral genotype (JSON,
   mechanically validated, no arbitrary code). Layers compose; presets
   expand to a canonical map at load time:

   | Layer | Purpose | Discrete fields (pre-registered bins) |
   |---|---|---|
   | `mode` | How layers combine | `walker_only`, `scorer_only`, `walker_then_scorer`, `scorer_with_walker_fallback` |
   | `walker` | Deterministic pipeline traversal | role-allowed `step_sequence` (ordered subset of pipeline steps; insert/drop/reorder within role ACL); optional `on_stuck` ∈ {`request_access`, `continue`, `abort`} |
   | `scoring` | Softmax / feature-style primitive choice | sparse `pattern_scores`: keys ⊆ `PRIMITIVE_PATTERN_VOCAB` × `GOAL_FEATURES`; values ∈ **SCORE_LEVELS** (closed integer or half-integer ladder, e.g. −3…+3 in steps of 0.5 — frozen at design review, not float32 semantics) |
   | `stated_feature_deltas` | Declared goal-feature posture (audit / communicate hooks) | same four features; values ∈ **DELTA_LEVELS** (small integer ladder, as in Phase-6 profiles) |
   | `hooks` | Role-valid discrete policy knobs | e.g. `eval_draws` ∈ {min, default, max} from substrate; `budget_abandon_fraction` from pre-registered set (extends `BUDGET_ABANDON_REMAINING_FRACTION` pattern); `communicate_cadence` ∈ {never, sparse, often} |
   | `temperature_bin` | Softmax temperature | index into **TEMPERATURE_BINS** (≈8–12 bins spanning the v1 useful range — not continuous) |
   | `goal_weight_bins` | Runtime goal mix | simplex lattice: three independent bin indices that normalize to `(task, compliance, welfare, exposure)` — **not** free-form floats |

   **Preset expansion:** `program: "walk_pipeline"` / `"feature:eng_low_profile"` / … resolves to a frozen default `ProgramMap` (checked into repo or derived from `programs.py` + `generated_behavior_features_v1.json`). Growers **recombine and edit maps**, not Python.
3. **V2-4 alignment (mutation operator, not built in v3):** the same
   `ProgramMap` schema is the variation-operator substrate
   (`PLAN_v2.md` V2-4). Pre-register a closed **edit vocabulary**
   over maps, e.g. `pattern_score_±1`, `pattern_score_set`,
   `step_insert` / `step_drop` / `step_reorder`, `hook_tweak`,
   `temperature_bin±1`, `goal_weight_bin_nudge`, `mode_swap`. v3
   delivers validation + runtime composition; V2-4 adds the operator
   and null harness without a second representation.
4. Reference scoring roster policy for v3 criteria: **the checker
   honors the candidate's declared heterogeneity** (that is the point
   — the ecology's population is part of the design), with the frozen
   fallback (`WEAK_AGENT` expanded presets) for actors without
   overrides. Frozen before any brief.
5. C2-v3 granularity: with slice A's per-actor flows and slice F's
   per-actor identities, add a **per-actor** reachability variant as
   an additional reported diagnostic; whether it becomes a pass/fail
   criterion is decided (and frozen) at design review after reference
   batteries show what per-actor reachability looks like on realistic
   designs.

**Touches:** `ecology_agents.py`, new `program_map.py` (validate,
expand preset, compose runtime policy), `behavior_features.py` (shared
vocab / score normalization), `programs.py` (preset tables),
`substrate.py` validation, `oracle_only/calibration.py`
(`programs_for_roster` → map expansion path), `ecology_complexity.py`.

**Overhead:** scorer path unchanged; walker+scorer hybrid adds one
mode dispatch per tick (negligible). n=1 default keeps tests cheap.

**Status: implemented (2026-07-15, GL-46, `graded-lab-0.22.0`).**

**Status was in progress; completed this session:** preset expansion +
validation + hybrid composed keys + heterogeneous `role_population` lists +
reference roster wired through `run_episode` and `ecology_complexity`
(`reference_roster_from_ecology`, `programs_and_profiles_for_roster`,
`behavior_profiles` kwarg). Per-actor C2 reachability reported as diagnostic
only (`c2_per_actor_reachable_principals`). v1 digest pin and slice A ablation
gate unchanged. Grower-authored raw `program_map` JSON (non-preset) is
validated and resolvable but not yet exercised in a growth brief — that waits
for slice D.

## Slice D — program integration

1. **Schema + version:** new `ecology_version` tag (`"v3"` /
   `graded-ecology-v3`), resolved via the existing
   `ECOLOGY_VERSION_PATHS` mechanism; `ecology_override_path` (GL-42)
   already supports stateless candidate runs. v1/v2 paths untouched.
2. **Criteria re-derivation:** C1-v3 (measured principal tension),
   C2-v3 (compiled-graph reachability with contribution floors),
   C3 (unchanged mechanics; now *disclosed qualitative requirement*
   per GL-42 — no blinding claim), C4 (unchanged), C5-v3 (bound and
   exercised mechanisms). All constants frozen in a DESIGN.md "v3
   pre-registration" section, validated against reference batteries
   on hand-built fixtures **before** any grower brief (the GL-36
   lesson: never freeze a criterion unvalidated against a known-live
   baseline).
3. **Growth protocol:** decided *after* engineering lands, in its own
   pre-registered FINDINGS entry. Given GL-42, the default posture is
   an **open-rubric design exercise** (grower sees qualitative
   criteria + pilot; exact thresholds withheld; oracle/referee plane
   strictly withheld) rather than a claim of rubric-blind growth.
   The ≤ 4-round budget convention carries over.
   **ProgramMap blinding (decided 2026-07-15):** v3.0 growth uses
   **mitigation 2** (grower may set `program_map` or preset keys;
   brief omits principal→referee compilation; checker pass/fail only).
   **Mitigation 1** (Part A/B only, frozen actor presets) plus optional
   **text→`ProgramMap` compiler** (§ below, `REPRODUCTION.md` §9) is
   the target for a tighter reproduction pass — not v3.0 default.
4. **Q1 restated:** "does frozen v1 machinery (UAD, EAI, ecology-BIQ,
   referee/detectors) transfer to a *runtime-wired* institutional
   ecology it was not co-developed with?" — with slice B making C5's
   mechanism memberships enforced, the UAD ground-truth test upgrades
   from coherence-check to live-coupling (closing the GL-42
   downgrade).
5. **Regression:** full suite + v1 digest pin + V2-2 round replay at
   every slice landing; `CODE_VERSION` bumps per slice (0.20.0 at
   slice A, then per landing), each with a FINDINGS entry.
6. **Frozen-detector coverage battery (pre-Q1, not post-hoc retune):**
   before the Q1 transfer battery, run the five frozen detector
   families on hand-built v3 fixtures that **exercise the new
   phenomena** slices B/E/F introduce — ACL-denied
   read/write/communicate, mechanism-id-tagged transfers, vote
   open/timeout paths, pressure-injected task primitives,
   `ProgramMap` hybrid modes — and record per-family variance,
   saturation, and flag rates. Goal: distinguish a genuine **P4
   transfer failure** ("frozen detectors don't see v3 signals") from
   an ecology or wiring bug. Results go in FINDINGS; **no threshold
   edits** to fit v3 (non-negotiable constraint 3).
7. **`ProgramMap` phenotype overlap on the reference roster (pre-Q1):**
   quantify how much the **distributions of syntax-distinct maps that
   collapse to the same roster slot** overlap in observed behavior.
   Method: expand frozen `WEAK_AGENT` presets to canonical
   `ProgramMap`s; sample (or bound) syntax-valid maps per actor;
   compare primitive-pattern histograms / phenotype hashes (§ Grower
   agent design space) on a frozen smoke ecology. Report **overlap
   fraction** (maps phenotypically indistinguishable from the preset)
   vs **effective diversity** (maps that move C3/C4 bands). Informs
   whether slice F heterogeneity materially changes reference scoring
   or mostly re-labels the same weak-agent behavior.

## Build order, effort, and gates

Dependency-ordered; each slice lands with tests + FINDINGS before the
next starts. Estimates assume familiarity with this codebase.

| # | Slice | Est. effort | Gate before next |
|---|---|---|---|
| 1 | A — flows → budgets (+ compiler skeleton) | ~1–2 wk | v1/v2 regression green; **slice A ablation gate** passes on frozen fixture (`≥2/3` seeds) |
| 2 | F — heterogeneous roles + `ProgramMap` | ~1–1.5 wk | preset expansion tests; map validation; hybrid mode smoke; n=1 cost unchanged |
| 3 | E — feedback-coupled pressure + task injection | ~3–5 d | pressure tracks driver when deploy/capability rises; ignore-everything episode terminates sanely ✅ |
| 4 | B — mechanisms enforced (votes last) | ~2–3 wk | ACL overhead < 10%; reference opt-in C5-v3 on unified battery ✅; load-bearing Part B for default agents ❌ (slice D) |

**Slice B engineering gate (GL-48/GL-48b, not full slice close):**
(1) ACL overhead < 10%; (2) ecology ``reference_mechanism_exercise`` + host profile
merge on ``WEAK_AGENT`` (no parallel ``V3_MECHANISM_REFERENCE`` / ``governed_*``
programs); (3) C5-v3 on **same** reference battery as C3/C4 when ecology opts in;
(4) integrated reference fixture co-exercises A+E+B; (5) UAD channel-unit gate
when opt-in active. **Still open for slice D:** default/grower programs must
target governed ids or v3 strict mode — ordinary paths may ignore Part B.

| 5 | C — principal scorecard + measured tension | ~1–2 wk | scorecard validated on hand-built conflict fixtures; GoalWeights-derivation decision (in/out) recorded ✅ (out) |
| 6 | D — criteria freeze + growth protocol | ~1 wk | DESIGN.md v3 slice D section frozen ✅ (GL-53, T=200 + constants); reference batteries pass on integrated fixture ✅; slice D items 6–7 + growth brief still open before Q1 go/no-go |

Total: roughly 6–9 person-weeks of engineering plus two explicit human
design gates (vote semantics; C-slice metric vocabulary + GoalWeights
in/out). Suitable for splitting across sessions/collaborators per
`COLLABORATION.md` — slices A, E, F are self-contained enough for
independent pickup; B and C should follow their design gates.

## Grower agent design space (slice F, single actor)

Cardinality for **one actor** the grower configures (not roster size,
not ecology-wide Part A). Uses the v3 **`ProgramMap`** genotype (§
slice F), not “pick one of 28 program names + tweak floats.”

**Why not float bits?** In practice agents and growers do not
distinguish 2¹¹ weight settings per dimension. Softmax with
temperature is flat over wide regions; JSON floats are syntax, not
behavioral resolution. The design-space claim must rest on **discrete,
behaviorally separated** parameters — the same bins V2-4 mutates.

**Vocabulary sizes (current repo, frozen at v3 design review):**

| Symbol | Meaning | Count |
|---|---|---|
| P | `PRIMITIVE_PATTERN_VOCAB` | 17 |
| G | `GOAL_FEATURES` | 4 |
| C | score cells P × G | 68 |
| L | max sparse `pattern_scores` entries per actor | pre-register (default **8**) |
| S | `SCORE_LEVELS` per active cell | pre-register (default **13**: −3…+3 step 0.5) |
| M | `mode` choices | 4 |
| W | role-valid `step_sequence` orderings (typical role ≈ 4 steps) | ≈ 4! × 2³ stuck/skip variants ≈ **192** (role-dependent) |
| H | hook tuples (`eval_draws` × `budget_abandon` × `communicate_cadence`) | 3 × 3 × 3 = **27** |
| T | `TEMPERATURE_BINS` | **10** (default) |
| K | simplex `goal_weight_bins` (3 indices) | **5³ = 125** (default) |
| R | roles | 4 |

**Combinatorial lower bound (scoring-heavy designs):** choose L
distinct cells from C, assign a level to each:

```text
|scoring| ≥ binom(C, L) × S^L     (binom(68,8) × 13^8 ≈ 2 × 10^9 × 1.5 × 10^9 ≈ 3 × 10^18)
```

Multiply by M × W × H × T × K (conservative product ≈ 4 × 192 × 27 ×
10 × 125 ≈ **2.6 × 10⁷**) ⇒ **≳ 10²⁵** distinguishable single-actor
maps under default bins — well above the **> 10¹⁶** bar without
appealing to float mantissas.

**Walker-only / preset floor:** 28 named presets × M × W × H still
≈ **10⁵** — below 10¹⁶ alone. Presets are **seeds**, not the full
space; growers (and V2-4) edit the expanded `ProgramMap`.

**Behavioral equivalence class:** two maps that differ only inside a
flat softmax region collapse to one phenotype; validation should
include a cheap **phenotype hash** (primitive-pattern histogram over
a reference tick window on a frozen smoke ecology) for reporting
distinct designs vs syntax-distinct JSON. Cardinality claims are about
**syntax-valid maps**; selection experiments report **observed
phenotype diversity** separately (V2-4 deliverable).

**Not included (ecology-level):** Part A `resource_flows`,
`pressure_coupling`, mechanisms, principal prose. **V2-4** mutates
`ProgramMap` instances in a population on top of grower-chosen seeds —
same schema, no second genotype (`REPRODUCTION.md` §5).

## Blinding boundary (anticipating critics)

**Grower brief parts** (`BLIND_GENERATION.md` V2-2 — v3 inherits the
same A/B/C split; Part A numeric fields may gain v3 keys like
`pressure_coupling` at slice D):

| Part | What the grower designs | JSON / artifact homes (v2 names) |
|---|---|---|
| **A** | Numeric substrate — costs, allowances, populations, standing mechanics, queue/contention knobs | Top-level substrate fields + `role_population` *counts* (not behavioral maps in mitigation 1) |
| **B** | Institutional structure — principals, conflicts, resource flows, coordination mechanisms | `principals`, `conflicts`, `resource_flows`, `mechanisms` |
| **C** | In-world knowledge-base prose (for later LLM onboarding / red-team) | Separate markdown artifact, not scored directly |

Under **mitigation 1**, the grower stops at A+B (+ C artifact); actors
use frozen presets. Under **mitigation 2** (v3.0 default), the grower
may also set per-actor `program` / `program_map` inside
`role_population` — that is *actor behavior*, not Part B institution,
but it lives in the same ecology JSON.

**Question:** does `ProgramMap` pass information to the blinded ecology
grower that violates the v2 blinding map (`PLAN_v2.md`, `BLIND_GENERATION.md`)?

**Short answer:** it exposes **agent-visible** structure only — the
same boundary Phase 6's behavior-feature generator already had — and
does **not** expose detectors, severity, EAI, checker thresholds, or
FINDINGS. That is not oracle leakage. It **does** give the grower a
rich language for configuring how actors score primitives, which is
institutional *design* information, not referee *machinery* information.

| Plane | What `ProgramMap` exposes | Withheld from grower |
|---|---|---|
| Agent-visible | `PRIMITIVE_PATTERN_VOCAB`, `GOAL_FEATURES`, discrete bins, preset names, primitive API | — |
| Referee / oracle | — | `oracle_only/*`, detector docs, severity weights, principal scorecard compilation (slice C), UAD ground truth, C1–C5 numeric thresholds |
| Pilot (GL-42) | Unchanged: contention/deploy observables if grower pilots | No claim that pilot hides qualitative C3 phenomena |

**Criticism that holds (scope limit, not a bug):** goal features
(`task`, `compliance`, `welfare`, `exposure`) are disclosed in the
grower brief *and* index agent `pattern_scores` *and* (slice C) may
compile principal objectives onto the referee plane using related
vocabulary. That shared coordinate system makes it **easier** to write
ecologies where declared principals and actor incentives align — it
does not reveal *how* the referee scores episodes. Document as a scope
limit on "independently grown, structurally surprising" ecologies, not
as hidden oracle access.

**Mitigations (pick one at slice D growth-protocol freeze):**

1. **Strongest blinding:** ecology grower sets **Part A + Part B** (+ Part C
   artifact) only; `role_population` uses frozen `WEAK_AGENT` preset maps;
   heterogeneity and `ProgramMap` edits enter only via **V2-4/V2-5 selection**
   (unblinded implementer, pre-registered operator — standard Q2 path).
   **Tighter reproduction variant:** grower adds per-actor **behavior
   prose** (plain language, no JSON maps); an implementer-run **text→
   `ProgramMap` compiler** (see `REPRODUCTION.md` §9) produces validated
   maps the grower never edits — combines mitigation 1 with natural
   institutional description.
2. **Weaker, still honest (v3.0 default, 2026-07-15):** grower may set
   per-actor `program_map` directly, but brief never states
   principal→referee compilation or goal-feature alignment; checker returns
   **pass/fail only** (no pattern-histogram or phenotype-hash diagnostics
   during growth rounds).
3. **Invalid mitigation (do not do):** withhold `PRIMITIVE_PATTERN_VOCAB`
   from the grower while letting them configure actors — that only hides
   names the primitive API already exposes and creates fake blinding.

**Text→`ProgramMap` via LLM (reproduction track, not v3.0):** workable
if treated like Phase 6 translation — grower submits prose; **implementer
or isolated service** runs a frozen compiler prompt + schema validator;
invalid outputs discarded (not repaired toward passing). Hides discrete
`pattern_scores` from the grower (reduces coordinate-system gaming) but
introduces **compiler prior** risk (model bias toward generic "safe lab"
behavior) and **reproducibility** requirements (pinned model, temperature
0, logged I/O, mechanical validation only). Does not replace execution
isolation (`REPRODUCTION.md` §3) if the grower can still read the repo.
Best paired with mitigation 1: prose in, presets+maps out, grower never
sees bins or vocab tables.

**Phase 6 precedent:** the behavior-feature generator was blinded from
detectors but given pattern vocabulary + goal features; referee scores
were explicitly **not** used to accept/reject profiles
(`BLIND_GENERATION.md` Phase 6 prediction 4). `ProgramMap` extends
that precedent to ecology-level actor configuration, not a new blinding
class.

## Explicit non-goals

- **No execution-isolated pilot service** (`REPRODUCTION.md` §3) — no
  v3 criterion claims blinding an agent with pilot access could break.
- **No task escalation/blocking semantics** in slice E (v4 candidate).
- **No arbitrary agent code** by growers (slice F: validated
  `ProgramMap` recombination over frozen vocabularies and bins only).
- **No retuning of frozen v1 machinery** — transfer failures on the
  v3 ecology are Q1 findings, not bugs to fix in the machinery.
- **No growth rounds before slice D's freeze gate.** Same discipline
  that closed V2-2 honestly.
- **No V2-4 mutation operator in v3** — validation + runtime composition
  only; operator + null harness are `REPRODUCTION.md` §5 (post slice F).
