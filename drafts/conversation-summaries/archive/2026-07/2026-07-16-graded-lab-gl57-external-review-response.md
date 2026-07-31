# 2026-07-16 — Graded lab GL-57: external review response

## Trigger

User pasted a detailed external review of GL-53–GL-56 (slice D criteria
freeze, pre-Q1 batteries, C2-v3, growth brief) with five "load-bearing
concerns," a "shortcuts that will bite" table, an "unnecessarily complex"
critique, and five explicit asks. Asked: "what needs to be addressed, what
do you disagree with? Start with the obvious fixes."

## Done

1. **Growth gate closed for C1-v3/C5-v3.** Added `ecology_is_v3` field to
   `ComplexityReport`; `all_passed`/`pass_fail_only()` now require
   `c1_v3_measured_tension is True` and `c5_v3_mechanisms_exercised is
   True` for v3-shaped ecologies (set by `run_complexity_check`). A v3
   ecology that omits `reference_mechanism_exercise` now **fails**
   growth instead of silently skipping the criterion. `pass_fail_only()`
   exposes `C1_v3`/`C5_v3` bool bits to the grower. v1/v2 reports
   (`ecology_is_v3` default `False`) unaffected — verified with two new
   unit tests.
2. **Growth brief downgraded from "frozen" to DRAFT.** `BLIND_GENERATION.md`
   § V3 now says explicitly not to launch a round against this text;
   removed the mitigation-2 "optional if grower maps hit governed paths"
   escape hatch.
3. **Mitigation default reversed 2 → 1.** Round 1 now defaults to
   mitigation 1 (frozen presets, no grower `program_map`); mitigation 2
   deferred to a later V2-4/V2-5 selection experiment. Updated
   `BLIND_GENERATION.md`, `PLAN_v3.md` §§ Blinding boundary and slice D.
4. **C2-v3 claim narrowed.** `DESIGN.md` now states explicitly that
   C2-v3 is a compiled-graph *accounting* check, not a causal one — does
   not show principal identity changes behavior the way slice A's
   ablation gate does for flows.
5. **Detector-coverage `transfer_failure_risk` reframed as a blocking
   stop** for any Q1-facing growth claim, not a footnote — in `DESIGN.md`
   and `BLIND_GENERATION.md`.
6. Bumped `CODE_VERSION` to `graded-lab-0.31.0`; updated `README.md`,
   `PLAN_v3.md`, `REPRODUCTION.md`, `results/FINDINGS.md` (long GL-57
   entry recording agreements, partial agreements, and disagreements),
   and the conversation-summary index.
7. Ran full `--profile fast` suite: 284 passed (was 279 + 5 new tests),
   0 failed, 0 regressions.

## Decisions

- **Did not build** a causal ablation-style C2-v3 gate or load-bearing
  Part B this session — both are real engineering, agreed as valid
  asks, explicitly recorded as still-open rather than silently deferred.
- **Disagreed, in part,** with three review points, recorded in
  `FINDINGS.md` GL-57's "partially disagree" section:
  - Dropping the declarative C1/C5 layer entirely (kept as a distinct,
    cheap engineering sanity check; no longer gates v3 growth alone).
  - Narrowing the host-coupling/slots=1/T=200 stack without a second
    fixture to validate against (would repeat the GL-36 mistake in the
    opposite direction).
  - "Ceremony" framing of the disclosed-qualitative-bar posture — agreed
    it's a real open tension, flagged explicitly rather than resolved
    (resolving it means either fake blinding, which GL-42 already ruled
    out, or accepting the scope limit as final).

## Open / next

- Load-bearing Part B for default agents (the actual root fix; C5-v3
  stays "opt-in host choreography" until closed).
- Causal (ablation-style) C2-v3 gate on ≥2 fixtures.
- Generic walker-step interpreter.
- Supplementary detector fixtures — now blocking for Q1 claims, not
  optional.
- First v3 growth round: blocked until Part B closes; use the revised
  mitigation-1 brief when it does.

## Key paths

- `graded_lab/harness/ecology_complexity.py` (`ComplexityReport`,
  `all_passed`, `pass_fail_only`, `run_complexity_check`)
- `tests/test_ecology_complexity.py` (two new gating tests)
- `BLIND_GENERATION.md` § V3 (DRAFT status, mitigation reversal)
- `PLAN_v3.md` §§ Blinding boundary, slice D
- `results/FINDINGS.md` GL-57 (full review-response record)

## Commits

- `6fbc256` Close v3 growth-gate loopholes and add C2-v3 (GL-56/GL-57).

## Follow-up: expanded `ProgramMap` mitigation rationale

**Trigger.** User agreed with the three pushbacks and asked for a more
detailed explanation of the `ProgramMap` issue, its mitigations, and why
mitigation 1 should stay settled ("frozen") for round 1 even though the
rest of the brief is DRAFT pending Part B.

**Done.** Added a new subsection to `BLIND_GENERATION.md` § V3, "What the
`ProgramMap` issue actually is (expanded, GL-57)," covering:
- Why `ProgramMap`/slice F's design-space richness exists (V2-4/V2-5
  substrate), separate from whether growers should author into it during
  blinded growth.
- Three concrete reasons mitigation 2 is risky, not hypothetical: (1)
  shared `GOAL_FEATURES` coordinate system with the slice-C scorecard
  the grower is told qualitative bars about; (2) a second, agent-side
  lever to satisfy C5-v3 without load-bearing Part B ever landing for
  ordinary reference agents — the review's "escape hatch," now named
  precisely; (3) GL-55's finding that most of the nominal `ProgramMap`
  space is currently runtime-inert (only `scorer_only` mode is wired),
  so authoring into it in round 1 would be a second, independent honesty
  problem.
- Why the mitigation-1-for-round-1 choice is orthogonal to Part B's
  still-undecided implementation shape (retargeting reference presets
  vs. a global v3 strict mode) and can therefore be locked in now,
  unlike the brief's institutional-exercise wording, which genuinely
  must wait for that shape to be decided.
- What is not lost: design-space cardinality, V2-4 mutation, and V2-5
  selection are deferred, not dropped — `ProgramMap` diversity becomes
  its own later causal claim instead of a second unexamined degree of
  freedom inside the blinded institutional-growth round.

Cross-referenced from `PLAN_v3.md` § Blinding boundary with a short
pointer + summary rather than duplicating the full argument.

**Decisions.** Kept the full argument in `BLIND_GENERATION.md` (the
brief's home) and cross-referenced rather than duplicated in
`PLAN_v3.md`, per the repo convention of one canonical location per
topic. No `CODE_VERSION` bump (doc-only, no behavior change).

**Key paths.** `BLIND_GENERATION.md` § V3 (new subsection);
`PLAN_v3.md` § Blinding boundary (cross-reference).

## Follow-up 2: does settling mitigation 1 constrain later phases?

**Trigger.** User: didn't realize most of the `ProgramMap` space is
currently runtime-inert; asked whether freezing mitigation 1 limits
later phases.

**Answer (added to `BLIND_GENERATION.md` § V3 as "Reversibility"):** no,
in an engineering sense. Three things kept separate: (1) the mitigation
choice is brief text, not code — schema/checker logic is identical
either way, so a later mitigation-2 round needs zero engineering change;
(2) V2-4/V2-5 mutate `ProgramMap` on top of whatever institution round 1
freezes, independent of which mitigation produced round 1's presets; (3)
the generic walker-step interpreter build is independent of the
mitigation decision and unblocked either way. The one real, non-technical
cost: round 1's specific frozen ecology will pair a grower-designed
institution with implementer-frozen agents, never grower-designed
agents — getting that specific data point later needs its own,
separately-scoped mitigation-2 growth round (new brief, new run), not a
reinterpretation of round 1's artifact. Framed as an added-round cost to
budget for if ever wanted, not a block — and independently the right
sequencing anyway, since testing grower-authored heterogeneity before
the walker-step interpreter exists would mostly exercise a no-op schema.

No `CODE_VERSION` bump (doc-only).
