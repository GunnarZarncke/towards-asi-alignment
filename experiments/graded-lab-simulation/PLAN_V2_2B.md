# V2-2b — revised blinded ecology growth (CLOSED EARLY 2026-07-15, superseded by v3)

**Status: CLOSED without a growth round (2026-07-15, user decision after
external review GL-42 — see `results/FINDINGS.md` GL-43 and
`PLAN_v3.md`).** The GL-42 review established that V2-2b's remaining
value proposition was too narrow to justify a growth program: C3/C4's
blinding claim was already retracted (the pilot is an effective C3
oracle), and C1/C2/C5 check declared JSON that the runtime never
consumes — so a passing ecology would have documented (not executable)
institutional structure plus a load-tested numeric substrate, and Q1
could only be phrased as "machinery transfer to a resource ecology with
narrative institutional metadata." Rather than run growth rounds toward
that weakened target, the program moves directly to **v3: institutional
runtime wiring** (`PLAN_v3.md`), which compiles Part B into live
permissions/budgets/channels/scoring before any new growth attempt.

**What carries forward into v3 (not wasted):** all GL-40/GL-42
engineering — multi-actor `role_population`, `ExogenousWorkloadEngine`,
the pilot harness (now honestly framed), `ecology_override_path`
statefulness fix, the end-to-end C3+C4 test, and the corrected Poisson
trigger — plus the blinding lessons (`BLIND_GENERATION.md` "V2-2b",
[`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) § Blind generation). n=1 `role_population`
keeps tests and smoke runs cheap; multi-actor is opt-in per ecology.

**Historical plan text below is kept as a record of what was designed
and why; do not execute it.**

---

**Correction (2026-07-15, external review, pre-closure):** the
pilot-sandbox design in §"Grower sandbox" (item 3) was found to be an
effective C3 oracle rather than a blind-safe boundary —
`pilot_generic`'s role programs are identical to the C3/C4 reference
roster, and its queue-pressure signal is the same predicate C3 scores.
The accepted fix (disclose C3's qualitative target, stop pretending the
pilot hides it, keep blinding on the machinery that still deserves it)
is in `BLIND_GENERATION.md` "V2-2b" and `REPRODUCTION.md`.

## Why V2-2b, not a V2-2 retry

V2-2's post-mortem (`results/FINDINGS.md` GL-36–GL-38, and the
2026-07-15 session discussion recorded in
`drafts/conversation-summaries/`) converged on a diagnosis that is about
the **protocol**, not the grower: C1/C2/C5 are declarative-state checks
(decidable from the grower's own JSON, no run required); C4 was a
pre-registration bug (unpassable reference roster, fixed); **C3 is
emergent** — a joint property of ≥2 actors' scheduling that cannot be
diagnosed from any single actor's numbers, depends on an unstated world
fact (exactly one actor per role), and has no *legitimately disclosable*
gradient (any richer feedback about "how far" is a coarsened readout of
the checker's own threshold, i.e. still a leak). Four rounds of pass/fail
feedback could not have converged on C3 by construction, independent of
grower quality.

The general lesson (write-up owed separately — see
[`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) § Blind generation, to be written alongside
this plan): **blind the measurement, never the phenomenon.** Real
blinding regimes (double-blind trials, blinded peer review, blinded
audits) blind the evaluator's rubric while leaving the blinded party full
observational access to their own system running. V2-2 blinded the
grower to *both* the rubric and the ecology's own dynamics — no sandbox,
no pilot run, ever. That is a stronger and less realistic blind than any
working real-world analog, and it removed the one channel (watching your
own design run) through which an emergent, unstated-cardinality property
like contention could plausibly be discovered by *coherence reasoning
alone*, without ever touching the rubric.

## Three changes (all discussed and agreed 2026-07-15, before writing this plan)

### 1. Multiple actors per role

Round 1–4 all had exactly one actor per role (`engineer`, `reviewer`,
`release_manager`, `admin`) — a fact the brief never states and the
checker's `queue_depth` semantics depend on. With one actor per role,
max pre-start `queue_depth` is 3, so `shared_compute_slots` must be
`< 3` for `queue_depth > shared_compute_slots` to ever fire — a
knife-edge that turns contention into an artifact of headcount rather
than a generic property of resource scarcity.

**Change:** the brief states population sizes per role explicitly as
something the grower designs (e.g. "how many engineers, reviewers,
release managers, and admins does this lab actually employ, and why"),
the same way it already asks for hazard-region and user-archetype
population shapes. This is a **world fact**, not a rubric fact — any
lab-realism reviewer with zero knowledge of scoring would ask "how many
people work here?" Multiple actors per role turns contention into a
property any moderately-provisioned shared-resource pool will generically
exhibit, removing the "hidden cardinality" trap without disclosing
anything about C3's thresholds.

**Engine/schema implication (implementer work, before any brief is
sent):** `EpisodeConfig.agents` currently assumes a fixed 1-per-role
tuple built by `default_lab_config()`; multi-actor-per-role requires the
grower's population counts to flow into agent instantiation. This is
schema completion in the same class as GL-33 (`ecology_version` key) and
GL-37 (`standing_mechanics.initial`) — additive, v1-path untouched,
regression-tested against the v1 digest pin before any v2 battery runs.

### 2. Exogenous stochastic workload

Round 1–4's contention search (grid sweep, `results/FINDINGS.md` GL-38)
found contention is a step function of `shared_compute_slots` with no
usable interior band under steady-state pacing: either 0.0 (slots too
generous) or saturated 1.0/degenerate deploy (slots=1). Real institutional
contention is mostly driven by **correlated demand spikes** (incident
bursts, deadline waves, batch releases), not steady per-tick overlap —
the ecology as specified has no mechanism for that.

**Change:** the brief asks the grower to describe (Part B, alongside
principals/conflicts/mechanisms) at least one **exogenous event class**
that periodically or stochastically raises multiple actors' resource
demand at once (e.g. a field-incident wave that pulls `reviewer` and
`release_manager` into the same monitoring window; a regulator-mandated
audit sprint; a funder milestone deadline that compresses eval + review
into the same span). This is squarely inside "describe the lab as
realistically as you can" — no lab operates on perfectly steady-state
demand — and it is the mechanism that makes an *interior* contention
band (neither 0 nor saturated) a natural outcome of realistic design
rather than a needle only found by parameter-sweeping
`shared_compute_slots`/`extra_duration_ticks_per_queued_slot` by hand.

**Design constraint:** the event class's *trigger* and *magnitude*
parameters are Part A numbers the grower sets (frequency, actor-overlap
pattern, duration) — same status as any other Part A field, same
forbidden-name rule (no field may name a downstream effect like
"contention_boost"). The *existence* of the mechanism is asked for in
the brief; its magnitude is the grower's design choice, not a disclosed
target.

### 3. Grower sandbox — pilot access to the ecology's own dynamics, not the rubric

This is the load-bearing change. Currently the grower designs Part A/B
purely on paper and never observes a single tick execute. That is a
stronger blind than any working real-world regime (a lab designing its
own resource policy would pilot it internally before finalizing) and is
the direct cause of C3's non-convergence: the one criterion that can
only be learned by watching the system run is the one criterion no
grower could learn anything about.

**Change:** after producing a draft Part A/B, the grower gets access to
a **generic in-world pilot harness** — a small number of episodes run
with **generic, non-adversarial in-world actors** (not the frozen
reference roster used for scoring; a distinct, disclosed-as-generic
"any reasonable engineer/reviewer/release_manager/admin" behavior) on
their own draft substrate, and observes only **in-world, sensor-plausible
facts**: does the pipeline ever complete? do any actors ever wait for a
compute slot? does anyone's standing/access ever run out? roughly how
long does a typical release take? No detector output, no severity, no
EAI, no C1–C5 pass/fail, no reference-roster identity or seeds, no
threshold numbers. This is the same blinding discipline the project
already uses elsewhere (embedded-simulation's `audit_projection.py`
enforces exactly this "sensor-plausible fields only" boundary for the
*auditor*; here it is enforced for the *designer*, before any scoring
round, not during one). Concretely this plane is implemented as a
frozen, non-scoring runner exposing only `EpisodeResult` fields any
in-world observer could plausibly have (completion, wait events,
lockouts) — never `contention_diagnostics`' internal fractions or
`deployed`'s exact rate, which remain rubric-only.

**What this fixes, and what it deliberately does not fix:** a grower
who pilots their own draft and sees "nobody ever waits for anything" or
"every access request is denied forever" would revise for realism
*before* a scoring round, the same way round 2/3 already fixed
standing-lockout-adjacent issues by hand-deriving invariants — except
now they can *check* the derivation against a run instead of guessing.
This does not disclose C3's exact thresholds (0.30 episode fraction,
0.05–0.95 action fraction) or its exact predicate
(`queue_depth > shared_compute_slots`); it discloses only that
contention/lockout are observable *world* phenomena, which the brief
already implies ("allowances that queue when actors compete for shared
resources"). The stopping rule (≤4 scored rounds, pass/fail-only
between scored rounds) is unchanged — the pilot sandbox is available
during each round's design phase, not as a substitute for or addition
to the scored feedback.

## What stays exactly as it was (no re-opening of settled ground)

- C1, C2, C4, C5 mechanical definitions and thresholds — unchanged,
  already correctly calibrated per GL-36.
- C3's mechanical definition and thresholds (episode fraction ≥ 0.30,
  action fraction in [0.05, 0.95]) — **unchanged**. What changes is the
  *substrate's capacity* to satisfy it plausibly (multi-actor + exogenous
  load) and the *grower's ability to notice* whether they're near it
  (sandbox), not the target itself.
- Physical file isolation for rubric-adjacent files (`PLAN_v2.md`,
  `DESIGN.md`, `BLIND_GENERATION.md`, `results/`, checker source) —
  unchanged. The pilot sandbox is a new tool exposed to the grower, not
  a relaxation of what stays hidden.
- The R ≤ 4 scored-round budget and pass/fail-only between-round
  feedback for the scored checker — unchanged.
- `standing_mechanics.initial` engine fix (GL-37) and `WEAK_AGENT`
  reference roster (GL-36) — carried forward as-is.

## Open engineering work before any V2-2b brief is sent

1. **Multi-actor population schema.** ✅ `role_population` on v2 JSONs;
   `build_agents_from_ecology()`; reference checker uses ecology roster;
   count=1/role preserves legacy ids (`eng1`…).
2. **Exogenous workload mechanism.** ✅ `exogenous_workload.events[]`
   with `periodic` / `poisson` triggers and per-role
   `resource_demand_scale` windows (`ExogenousWorkloadEngine`).
3. **Non-scoring pilot runner.** ✅ `graded_lab/harness/ecology_pilot.py`
   + `pilot_ecology.py` CLI; `audit_pilot_payload()` leak guard.
4. **Updated C1–C5 applicability check.** ✅ C2 remains per-role
   reachability (unchanged); multi-actor does not alter C1/C4/C5.
5. **BLIND_GENERATION.md v2-2b section.** ⏳ brief text below — freeze
   before round 1.
6. **FINDINGS GL-40.** ✅ pre-registers V2-2b engineering (this commit).

## Explicit non-goals

- Not a retroactive re-scoring of V2-2's four rounds under a relaxed
  criterion — those results stand as reported (GL-34–GL-38).
- Not a route to guarantee C3 passes; a multi-actor, workload-bursty,
  sandboxed grower could still fail to produce a passing ecology, and
  that would be reported the same way, honestly, as GL-38 was.
- Not a change to Q1/Q2/Q3 or the machinery-transfer program — V2-3
  onward remains gated on a C1–C5-passing ecology, from V2-2b or a later
  attempt, per `PLAN_v2.md`.
