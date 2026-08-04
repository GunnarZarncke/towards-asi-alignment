# Graded Lab Simulation — v1 program terminal summary

**Status: the v1 experiment program (Phases 0–8d, FINDINGS GL-0–GL-31) is
CLOSED as of 2026-07-15.** The simulation codebase is **not** closed: a v2
program with a population-variation operator, blinded-grown ecology, and
LLM red-teaming is planned in [`../PLAN_v2.md`](../PLAN_v2.md). No v1
result is retracted; the frozen artifacts (`generated_substrate_v1.json`,
`generated_behavior_features_v1.json`, referee/detector freeze, `CODE_VERSION`
`graded-lab-0.17.0`) remain the baseline v2 builds on.

Reproduction instructions for every v1 finding:
[`../REPRODUCING.md`](../REPRODUCING.md).

**Final v1 code commit:** `ed21adb` (frozen code, `CODE_VERSION`
`graded-lab-0.17.0`); closure-docs commit hash recorded in
`../REPRODUCING.md`.

---

## The arc in one paragraph

The line was spawned (lab-sim GL-41) to make ambiguity **emerge** from a
blinded resource/population substrate instead of dialing it in. Phases 0–6
built that substrate, a Tier-K/Tier-I oracle, a frozen referee, and blinded
behavior features; Phase 7 measured the resulting ambiguity (EAI), ported
UAD unit discovery, and built an ecology-BIQ estimator; Phase 7c tried to
calibrate the ecology into a pre-registered sweet spot and **never fully
succeeded** (1/4 pass criteria under both the oracle and the referee
vantage, GL-22); Phase 8 ran throughput-linked selection anyway, under a
pre-registered exception, and returned a **clean null on detector-evading
emergence** (GL-23) that four follow-up phases (8a–8d) progressively
sharpened into: the selection mechanism amplifies statistical noise
(GL-25), is insensitive to widening the fitness proxy (GL-26), is
measurably but weakly affected by institutional carryover (GL-27/GL-28),
and offers no agent-program lever for a throughput/preservation tradeoff
on the frozen ecology (GL-29).

## Why the program is closed

The prize question — *"does selection under genuinely graded ambiguity
produce a detector-evading strategy that was not programmed in?"* — is
**structurally unanswerable in the v1 design**: Phase 8 selects over a
fixed roster of hand-written program maps. Fitness-proportional
reallocation over a frozen roster can only reweight existing strategies;
it cannot generate a novel one. Every further battery on this roster
would produce more refinements of the null, each buying at most one more
hedge-qualifier for a chapter that already has its paragraph. Per the v1
go/no-go rule (`PLAN.md`, manuscript backlog item 4): when the sentence a
further result would buy is thin, that is itself the finding.

A second, related reason: the "developed to the test" critique was
answered at the **substrate** level (blinded designer, `BLIND_GENERATION.md`)
but still bites one level up — the roster, the `correction_preserving`
tags, and the selection proxies were written by the unblinded process,
and that is exactly where the GL-23/GL-25/GL-29 confounds live. Fixing
that requires a new blinding boundary (ecology growth, variation
operator), which is a new program, not another v1 phase.

## What v1 established (positive findings)

| Finding | Result | Manuscript consumer |
|---|---|---|
| GL-11 | Passive UAD structurally misses coordination with no `communicate` signal (`signal_handoff_pair`); recovered only by standalone all-pairs dependency probing | ch07 (integrated 2026-07-14) |
| GL-12 | Intervention-based discovery over-merges a resource-bound bystander through shared queue contention (`three_way_nod`) | ch07 (integrated) |
| GL-13/GL-14 | A good-faith `I_ctrl` implementation silently re-imported a task ontology via a narrow outcome vector; widening fixed the confound but is not exhaustive | ch11 (integrated) |
| GL-19/GL-20 | "High ambiguity band unreachable" was a **measurement-vantage** artifact: light-tier (referee) projection of the same episodes reaches the mid band everywhere the agent-vantage measure reads ≈0 | candidate for ch39/ch43; not yet integrated |
| GL-25 | Fitness-proportional selection **amplifies statistical noise** into large cumulative mass drift (mass moved −0.19 while the tagged throughput difference had a CI covering zero) | ch34-adjacent; the strongest un-harvested v1 result |
| GL-27/GL-28 | Campaign grant/standing carryover is causally distinguishable from an episode-reset baseline (both CIs exclude zero; divergence begins at episode 1) — Phase 8 is not a repeated-single-episode loop | supports the "persistent institutional state" framing; small effect size stated |
| GL-30 | Mock/subprocess isolate parity holds bit-for-bit for all Phase 8 program maps and selection trajectories | engineering guarantee inherited by v2 |

## What v1 reported as nulls or negatives (honor these)

| Finding | Null / negative |
|---|---|
| GL-16 | Phase 7c's first diagnosis was itself wrong; three-cause postmortem, battery-design checklist added |
| GL-18 | EAI-v2 normalization fix: measured effect on this substrate is a null; the ecology is close to deterministic given full agent-visible context |
| GL-22 | Calibration never passed: 1/4 criteria under **both** vantages (a different criterion each); criterion 1's sign **flips** between vantages (−0.146 vs +0.177) |
| GL-23 | Clean null on detector-evading emergence: mass shifted to the *weaker* program and weighted severity/detector **fell** |
| GL-26 | Widening fitness to audit-pass + review-latency handles delays but does not prevent the same collapse (proxy-insensitivity on this roster) |
| GL-29 | Budget-aware member: deploy null holds at load 1.5; the preservation-mass endpoint is an accounting confound, not a tradeoff result |

Do not cite GL-23's direction as "correction-preservation was selected
against" (GL-25 forbids that causal read), and do not cite anything in
this line as evidence for ch36 (parasites) or ch40 (goal laundering) —
no such signature exists in any v1 result (GL-24).

## Manuscript integration state at closure

Integrated 2026-07-14 (see `PLAN.md` backlog section for exact
locations): ch07 (GL-11/GL-12), ch11 (GL-13/GL-14), ch33 (toy-sim
instrumentation-cost result), ch34 (GL-23 with GL-24 caveats inline).
Un-harvested candidates left for a future writing pass: GL-25
(selection-noise amplification), GL-19/GL-20 (vantage-dependence of
measured ambiguity), GL-27/GL-28 (carryover causality). ch36/ch40:
nothing to cite.

## What carries into v2

- The frozen substrate, oracle tiers, referee, UAD/EAI/BIQ machinery,
  isolate backends, test/speed discipline, and stats helpers — unchanged.
- The blinding workflow (`BLIND_GENERATION.md`) — extended, not replaced.
- The GL-25 noise-floor lesson: v2's selection phases pre-register a
  uniform-fitness null control before any selection claim.
- The GL-17/GL-29 lever note: deploy divergence between agent programs
  exists at `carrier_load_scale=2.0` (0.6 vs 0.9), not at the frozen 1.5.

See [`../PLAN_v2.md`](../PLAN_v2.md) for the v2 phases, blinding map, and
pre-registered predictions.
