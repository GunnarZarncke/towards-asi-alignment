# Blind generation methodology — cross-line lessons

**Purpose.** Every experiment line in this repo uses some form of blind
generation to break author/detector co-design loops (a generator that
never saw the evaluation criteria invents content; a frozen
evaluator scores it with no re-fitting). This document collects the
lessons that recurred across lines — most recently and most sharply in
the graded-lab v2 program (`graded-lab-simulation/results/FINDINGS.md`
GL-34–GL-38) — so the next line, or the next criterion within an
existing line, does not re-pay for them. It is descriptive of what we
learned, not a new binding protocol; each line's own `BLIND_GENERATION.md`
remains the source of truth for what that line actually did.

Prior art this draws on: `goal-agent-simulation/BLIND_GENERATION.md`
(blind action generation, GA-8 onward), `lab-simulation/BLIND_GENERATION.md`
and `BLIND_GENERATION_ROUND2.md` (blind playbook generation), the Phase
7a-blind scenario-designer protocol in `graded-lab-simulation/DESIGN.md`,
and `embedded-simulation`'s `audit_projection.py` (plane-enforced
sensor-plausible fields for the *auditor*, the closest existing precedent
for lesson 4 below). See also `AGENTS.md`'s note that conclusions must
never be named in definitions before being derived — several lessons
below are instances of that rule applied to criterion design and
between-round feedback specifically.

---

## Lesson 1 — blind the measurement, never the phenomenon

Real blinding regimes that work (double-blind drug trials, blinded peer
review, blinded financial audits) blind the evaluated party to the
**evaluator's rubric** — not to their own system's behavior. A drug
company runs all the preclinical testing it wants before the blinded
phase; a paper's authors ran their own experiments before submission; an
audited firm watches its own operations every day. The blind boundary
sits between "what the evaluator will check for" and "what the evaluated
party can observe about their own thing."

Graded-lab v2's ecology grower was blinded to *both* the C1–C5 rubric
**and** its own ecology's dynamics — it never watched a single tick
execute before submitting. That is a stronger blind than any working
real-world analog, not a more rigorous one. The one C-criterion that
required observing a run (C3, contention liveness — a joint property of
≥2 actors' scheduling) never converged in four rounds; the criteria
decidable from the grower's own declared JSON (C1, C2, C5) passed from
round 1. That is not a coincidence of difficulty — it is what the
protocol structurally allowed.

**Guidance for the next line:** before freezing a growth/generation
protocol, identify which properties the generator needs to *observe
running* to have any chance of satisfying, versus which are decidable
from what it already writes down. For the first kind, give the generator
a **pilot/sandbox pass over its own draft** with generic, non-adversarial
in-world actors and only sensor-plausible outcome fields (did it
complete? did anyone wait? did anyone get locked out?) — never the
scoring machinery's actual output. This is the same discipline
`embedded-simulation/audit_projection.py` already enforces for the
in-sim *auditor* (drop oracle-only fields before they reach the
audited plane); apply it symmetrically to the *generator*, before
scoring, not during it.

## Lesson 2 — coarsened feedback is still a leak; there is no safe middle ground between "bool" and "number"

It is tempting, when a bool-only signal repeatedly fails to converge, to
add a little more shape to the feedback — "too saturated" vs. "too
sparse," or naming which of several sub-checks failed. This was
considered for C3 (disclosing whether `action_contention_fraction` sat
above or below its band) and rejected on inspection: any signal derived
from the checker's own threshold predicate is a coarsened readout of
that predicate, regardless of how few bits it carries. A generator that
receives it across several rounds can binary-search the response
surface — exactly the "grow until it works" pattern the stopping rule
exists to prevent, one level of indirection removed.

C2's existing protocol (naming which *roles* fail reachability, not just
a bool) already crosses this line, on inspection — it happened to
produce genuine realism fixes in the rounds that used it, but that is
luck, not evidence the practice is safe in general, and it should not be
used as precedent for extending similar richness to other criteria.

**Guidance for the next line:** if a criterion has failed for several
rounds under bool-only feedback, do not richen the *rubric-derived*
signal. Ask instead whether a missing **world fact** (see Lesson 3)
would let the generator reason toward a pass without ever learning
anything about the rubric, or whether the criterion's determining
parameters are misplaced (Lesson 4). Treat "give a hint" as almost
always the wrong move, not a matter of hint size.

## Lesson 3 — disclosing a missing world fact is not the same as disclosing a threshold

Some gaps genuinely are omissions from the brief, not rubric leakage. In
graded-lab v2, the brief said "four roles" but never "one actor per
role" — a fact about the fictional lab's org chart that a coherence-only
reviewer with zero knowledge of any scoring criterion would flag on a
cold read ("how many people actually work here?"). Disclosing that fact
tells the generator nothing about what is being measured or which
direction to move a number; it just completes the world description the
brief was supposed to give in the first place.

The test that distinguishes a legitimate world-fact fix from a leak:
**would a domain-coherence reviewer who has never seen the rubric flag
this gap on a cold read of the brief alone?** If yes, disclosing it is a
brief-quality fix (log it as a coherence iteration, same class as any
other "broaden the brief between rounds" correction). If the fix requires
knowing what the checker measures or which side of a threshold the
generator is on, it fails the test and is a leak regardless of framing.

## Lesson 4 — a criterion's free parameters must be owned by whoever can actually determine their correct value

Graded-lab v2's `shared_compute_slots` and
`extra_duration_ticks_per_queued_slot` were placed in the generator's
Part A as if they were ordinary institutional-economics numbers, but
their correct value for passing C3 depended on **engine internals** the
generator never sees and has no principled way to guess: the exact
actor count, and the scheduler's strict-inequality convention
(`queue_depth > shared_compute_slots`, not `>=`). This is the same
category of bug as C4's original reference roster (STRONG_AGENT,
already known unpassable from a *pre-existing* finding, GL-16) and the
standing-schema mismatch (the engine silently used a different field
than the one the schema named) — in all three cases, a parameter that
functions as **implementer/engine configuration** was mistakenly
delegated to the blinded generator's decision space, and no amount of
generator skill could recover from that misplacement.

**Guidance for the next line:** before freezing a criterion, list every
free parameter that determines its outcome and classify each as either
(a) a world/design fact the generator is the right party to set, or
(b) an implementer/engine fact the generator cannot see far enough to
set correctly. Freeze every (b) parameter as an implementer constant
in the same pre-registration phase as the criterion itself — do not
let it default into the generator's Part A just because it is
numeric and looks like a substrate field.

## Lesson 5 — validate a criterion against a live baseline before freezing it, especially for "must clear a band under a fixed reference agent" checks

C4's original reference roster (`STRONG_AGENT`) had already been shown,
in a *pre-existing* v1 finding (GL-16, recorded before V2-1 was
drafted), to deploy 0/160 regardless of substrate cell. The criterion's
passing band (`0.1 < deploy_rate < 0.9`) was therefore unreachable by
*any* ecology, including v1's own, from the moment it was frozen — a
pre-registration bug, not an ecology property, and it went undetected
until round 3's stall forced investigation.

**Guidance for the next line:** any criterion of the form "a frozen
reference agent/roster must produce an outcome inside band X on the
generated artifact" needs a **known-live check** — run the reference
roster against at least one already-existing, already-understood
substrate before freezing the band, and confirm the band is reachable
there. This is cheap (minutes of compute) relative to burning growth
rounds discovering the band was never reachable.

## Lesson 6 — ask what fraction of plausible designs pass, before freezing

Two different criterion shapes look superficially similar but behave
very differently under blind growth:

- **Filters against degenerate corners.** Most realistic, coherent
  designs pass by construction; the criterion mainly rules out trivial
  failures (e.g. C1's ≥4-principals-with-≥3-real-conflicts, C5's
  ≥3-distinct-mechanism-kinds). A generator doing what the brief already
  asks ("be realistic, be diverse") reaches these without ever needing
  rubric information.
- **Generators of a rare property.** The passing region is a narrow
  slice of parameter space that "just being realistic" does not
  generically land on (C3 turned out to be this shape — a step function
  in `shared_compute_slots` with essentially no interior band under
  steady-state pacing, confirmed by grid search in GL-38). For this
  shape, either the substrate needs a structural change that makes the
  property generic rather than rare (see graded-lab v2's `PLAN_V2_2B.md`
  for the specific fix — multi-actor roles, exogenous bursty workload),
  or the criterion should not be frozen as a pure blind-growth target at
  all.

**Guidance for the next line:** before freezing a criterion, estimate
(even roughly, by hand or by a quick sweep over a few known-plausible
designs) what fraction of realistic designs would pass it. If the
answer is "almost none, without hitting a narrow parameter region,"
that criterion needs either a substrate change that makes the target
property generic, or a different growth protocol (e.g. iterative
co-design with disclosed engine facts, explicitly logged as such, rather
than blind pass/fail).

## Lesson 7 — misdiagnosis under opaque feedback is a predictable cost, not a generator failure

Round 4's generator, told only that C3 still failed while C1/C2/C4/C5
now passed, reasonably concluded the remaining gap must be in the one
area those other passes hadn't fully covered (Part B resource-flow
completeness) and left the numeric substrate untouched. This was a
sound inference given the available signal — bool-only feedback with no
semantic content cannot distinguish "you have the wrong mental model of
what this criterion checks" from "you have the right model but the
wrong number." When writing up a stalled blind-growth result, attribute
the stall to the **information available**, not to the generator's
reasoning quality, unless there is a specific reason to think a
less-opaque signal within the leak-safe boundary (Lessons 2–3) was
available and unused.

## Lesson 8 — archive contaminated rounds, don't discard them, and don't count them against the round budget

When a blinding leak is discovered mid-protocol (graded-lab v2's
round-2 grower self-reporting it had read `PLAN_v2.md`'s thresholds from
ambient context), the affected rounds are evidence about the leak
itself and should be preserved for the record
(`archive/v2-2-contaminated-rounds-2-3/README.md` is the template), not
deleted. They are voided from the round budget (the failure was a
protocol defect, not a legitimate use of a growth attempt), and the
fix — for agentic generators specifically — is **physical file
removal**, not instruction. An instructed "do not read X" is
insufficient once the generator's own memory of a prior round carries
the leaked content forward across rounds; only removing the files from
the working directory closes the channel.

## Lesson 9 — long-running batteries and multi-round protocols still need progress logging and honest negatives

Both already-stated repo-wide rules apply with no special exception for
blind-generation protocols: long-running checker batteries print
`[i/n]` progress (per `AGENTS.md`); a stalled or failed growth attempt
is a first-class, reported finding (`results/FINDINGS.md`, never
buried), exactly like any other negative result in this repo's
experiment lines.

---

## Quick checklist for pre-registering a new blind-growth criterion

Before freezing any criterion in a new `DESIGN.md`/`PLAN.md` section:

1. Is this criterion decidable from the generator's own declared output,
   or does it require running the artifact? (Lesson 1)
2. If it requires a run: does the generator get a sandboxed, non-scoring
   pilot pass with sensor-plausible outputs only? (Lesson 1)
3. List every free parameter the criterion's outcome depends on. Is each
   one a world fact the generator should set, or an engine fact that
   must be frozen by the implementer instead? (Lesson 4)
4. If the criterion needs a fixed reference agent/roster to clear a
   band: has that roster been run against a known, already-understood
   substrate to confirm the band is reachable at all? (Lesson 5)
5. Roughly, what fraction of realistic designs would pass this
   criterion unassisted? If "almost none without hitting a narrow
   region," reconsider the substrate or the growth protocol before
   freezing the criterion as-is. (Lesson 6)
6. Is every "missing fact" you're tempted to add between rounds a world
   fact (passes the cold-read-coherence-reviewer test) or a
   rubric-derived signal (fails it)? Only the former may be disclosed.
   (Lessons 2–3)
7. Does the between-round feedback plan avoid ever exposing a
   coarsened version of the criterion's own threshold predicate?
   (Lesson 2)

None of this replaces line-specific judgment — it is a shared failure
mode catalogue, added to as new lines hit new instances of it.
