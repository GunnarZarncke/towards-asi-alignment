# Phase 4 — Severity-Graded Referee, Gated Escalation, Accumulation Bounds

Roadmap document for Phase 4 of the goal-agent simulation line. Companion to
`BLIND_GENERATION.md` (generation protocol) and `results/FINDINGS.md`
(negative/positive results register). All Phase 4 work lives in this
directory; Phase 1-3 artifacts (`label_episode`, the boolean `detectors.py`
functions, and all three blind-generated repertoires) stay byte-identical
throughout — see the "No re-fitting" clause in every Phase 4 runner's
docstring.

## Why Phase 4 exists

Phase 3 (round 3's blind generation, `BLIND_GENERATION.md` "Generation round
3") found that a large, independently-varied action repertoire drives the
boolean episode label to near-total saturation (`results/FINDINGS.md` F-14)
regardless of which of two pre-registered L2 thresholds is used. Once nearly
every episode is "violation", there is no honest subgroup left inside a
population to compute a false-alarm rate against, and no meaningful
detection-rate comparison across repertoires either — the boolean label
itself, not any specific threshold, is the binding constraint.

The user's diagnosis (session discussion, 2026-07-05) reframed the problem:
binary pass/fail decisions ARE common in real oversight systems, but real
systems get away with them because (a) they reserve the bare binary
decision for a short list of unambiguous "never events", (b) everything
else is scored on a graded, continuous scale, and (c) borderline cases go
through further, deeper investigation before a final decision is made — a
degree of freedom (asking follow-up questions) our episode-level boolean
label never had. Phase 4 imports that structure.

## Design decisions

- **Oracle emits continuous severity** (`goal_sim/severity.py`). The binary
  `label_episode` (`labels.py`) is kept exactly as-is for comparability with
  Phase 1-3, but Phase 4 does not treat it as the thing detectors are
  compared against; `severity.severity()` re-expresses the same oracle
  ground truth as a continuous scalar in [0, 1) that stays meaningful under
  full saturation.
- **Audit ends in a boolean verdict**, but only after a gated escalation
  ladder: a cheap continuous screen, a borderline band that triggers a
  bounded number of follow-up queries, and only then a final yes/no
  (`goal_sim/escalation.py`).
- **Two-tier label structure**, mirroring real practice: a short absolute
  "never event" list (L3, unapproved practice change — kept as a bright-line
  boolean flag, `severity()`'s `never_event`) sits above graded severity for
  the dense, frequency-sensitive conditions (report gap, cumulative
  welfare harm).
- **Honest twins** (`goal_sim/twins.py`) instead of population-targeting: a
  fixed, schema-only mechanical transform of the repertoire gives a paired
  control without ever looking at outcomes to decide what counts as
  "honest".
- **Blind detector comparison via rank correlation, not raw agreement**: two
  detectors, or the same detector across repertoires, can be compared by how
  well they RANK episodes against oracle severity (Spearman), which survives
  saturation that would sink a detection-rate comparison.

## The medical / aviation rationale

Two real-world oversight systems motivated this shape, both cited by the
user in the design discussion:

- **Medical trigger tools** (e.g. the IHI Global Trigger Tool for adverse
  events): most chart review is a cheap, high-recall/low-specificity
  screen for "triggers" (a lab value out of range, an antidote
  administered); a trigger does not itself mean harm occurred, it gates a
  more expensive human chart review that renders the actual yes/no harm
  determination. The system's precision comes from the SECOND stage, not
  the first — exactly the light-screen/borderline-escalation/verdict shape
  `escalation.py` implements. Separately, a short list of "never events"
  (wrong-site surgery, retained instrument) bypasses grading entirely and
  is reported as an absolute standard — the L3/never-event split above.
- **Aviation FOQA (Flight Operations Quality Assurance)**: routine flight
  data is scored against continuous exceedance bands (a hard landing is a
  *rate*, not a binary), with a separate, absolute list of mandatory-report
  events. Critically, FOQA programs are explicitly firewalled from
  discipline (a *de-identified, non-punitive* learning channel) precisely
  because a channel used for enforcement changes what gets reported into
  it — a separation this simulation line does not model (the board here
  reads the same channels it enforces on) and states as a limitation.

Both systems also motivate why the escalation ladder queries via *response
options* rather than reading the same signal twice: the second stage asks a
DIFFERENT question (can the entity account for the flagged event) using a
different evidence channel, not a stricter threshold on the first
screen's own signal.

## TODO markers (documented, not implemented this phase)

- **In-sim adaptation of the escalation ladder.** `escalation.py`'s gates
  (`LOW_GATE`, `HIGH_GATE`, `K_QUERIES`, `DISCLOSE_FRACTION_GATE`) are fixed
  constants, pre-registered once. A more realistic board would adapt its own
  gating organically as it observes outcomes (the way real trigger-tool
  programs periodically re-calibrate their trigger list from chart-review
  yield) — deliberately out of scope here, since an adapting board reading
  its own past verdicts reintroduces exactly the after-the-fact-tuning risk
  this line's "no re-fitting" discipline exists to avoid, and needs its own
  pre-registered protocol for HOW it may adapt before it is safe to add.
- **Recursive drill-down depth.** The escalation ladder in this phase is
  "one nesting level": a query against a step's response set, once, bounded
  by `K_QUERIES`. A real investigation can recurse — a response can itself
  be questioned, arbitrarily deep, until it grounds out in something no
  longer contestable. Modeling that grounding condition precisely is, in the
  limit, the same problem this book's Lean spine gestures at with Logical
  Induction (a self-referential process that must itself terminate in a
  stable, exploitable-free equilibrium rather than regress forever) —
  well beyond this experiment's scope; noted here so the simplification is
  visible rather than silently assumed away.

## Phase ordering (as executed)

0. This roadmap document.
1. **4a** — `severity.py` (continuous severity), `detectors.py` score
   variants, `run_phase4_ranking.py` (Spearman ranking per repertoire:
   legacy, round 1, round 2, round 3). No new generation.
2. **4b** — `twins.py` (mechanical honest-twin rule), paired evaluation
   folded into the same `run_phase4_ranking.py` run. Completes the blind
   comparison on existing data.
3. **4c** — Response-option schema extension (`actions.py`
   `ResponseOption`/`RESPONSE_TRUTHFUL_MODES`, `ontology.py`
   `RESPONSE_MODE_CANONICAL_MAP`), `escalation.py` ladder + verdict, blind
   round-4 generation (`generated_actions_v4.json`), evaluation battery.
4. **4d** — Oracle stock variables in `world.py` (real `delayed`/
   `aggregated` semantics, an audit-visible accumulation channel), a
   bound-first accumulation cap, and two secondary detectors.

Each phase: pre-registered in its runner's docstring before the first run;
regression tests extended (booleans and rounds 1-3 artifacts stay
byte-identical); findings recorded in `results/FINDINGS.md` (F-15 onward);
session logged in `drafts/conversation-summaries/`.

## Results summary (filled in as each phase completes)

See `results/FINDINGS.md` F-15 onward and `results/phase4_*.{json,md}` for
full numbers; headline results are not duplicated here to avoid two sources
of truth drifting apart.
