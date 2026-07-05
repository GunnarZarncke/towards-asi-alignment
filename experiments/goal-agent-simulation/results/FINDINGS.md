# Findings — Phase 1 acceptance run (2026-07-04)

Honest record for this line, in the spirit of the old line's
`NEGATIVE_RESULTS.md`: negatives and caveats are bounded claims, not bugs to
tune away. Run: `run_phase1.py`, artifacts `phase1_acceptance.{json,md}`.
All thresholds were frozen before this run (see `goal_sim/labels.py`,
`goal_sim/detectors.py`, `goal_sim/protocol.py`); nothing below was re-fit.

## F-1 (negative) — the pre-registered held-out region saturated the label

The held-out region ("high-deception corner": `w_task ≥ 0.45`,
`w_compliance ≤ 0.15`, shadow tool) produced **80/80 violation episodes**.
Two consequences:

1. The **detector transfer result is real but weak**: full-tier detection was
   1.0 and light-tier 0.80 on held-out — no degradation — but the region
   turned out *easier* than discovery (more overt violations per episode, more
   signal per detector), so this run does not test transfer to *subtler*
   unseen behavior. Pre-registered guess implicitly wrong: the "hard corner"
   for generalization is not the high-incentive corner; it is a
   moderate-incentive, high-exposure-aversion band where deception is
   occasional and small.
2. The **channel-MI transfer test is degenerate by construction**: MI against
   a constant label is 0 for every channel (held-out label entropy 0 bits).
   The all-zero held-out MI scores measure the region choice, not the
   channels. Flagged mechanically in the report
   (`held_out_transfer_degenerate: true`).

Follow-up (needs its own pre-registration, do NOT re-pick the region after
seeing this run's labels and re-report as if fresh): a second held-out region
in the subtle band, e.g. `0.30 ≤ w_task ≤ 0.45` with `w_exposure ≥ 0.35` and
shadow access, chosen for predicted label *mixture*, not purity.

**Follow-up result (2026-07-04, same session): the prediction was wrong
again, but this time diagnosably so — see F-6.** The subtle region *also*
saturated at 100% violations (80/80), so the MI-transfer test is degenerate
there too. F-6 identifies the structural cause (a simplex-geometry effect,
not a property of "deception corners"), and F-7 implements and validates
the fix (a third, compliance-band region) — the MI-transfer test finally
produces a genuine, non-degenerate result.

## F-2 — light tier misses most violations (0.63 false-pass on discovery)

Passive logs (correction requests, reports, visible actions, probes) catch
overt defiance (d2) and blatant misreporting (d1) but are blind to
harm-magnitude violations (L2, the most common label cause: 94/107) and to
shadow routing (visible channel looks compliant). Detection 0.37 at light vs
0.94 at full. This is the emergent analogue of the old line's N-10 finding
that the `bearer_welfare` channel domain carries non-substitutable detection
power — here it re-derives itself from agent choice rather than from a
scripted scenario, which is modest evidence the old finding was not an
artifact of scripting.

## F-3 — full-tier residual misses are all small-n deceptive reporting

6/107 discovery violations passed at full tier (pre-follow-up count); every
one is an L1-only case with a report gap of 0.25–0.43 over few correction
steps (typically n=7), below d1's fixed 0.35-divergence-over-probes bar.
Same structural lesson as the old line's N-12: fixed-fraction thresholds
are miscalibrated at small n.

**Follow-up implemented and measured (2026-07-04, same session):** added
`d1b_probe_divergence_wilson` (Wilson-bound event-rate test, target rate
0.25 matching the label threshold, 80% confidence — both fixed before this
detector was run against outcomes; see `detectors.py` docstring) alongside
D1, not replacing it. On discovery: full-tier detection 0.9439 → 0.9533,
false-pass 0.0561 → 0.0467 (residual misses 6 → 5 of 107); light-tier
detection 0.3738 → 0.3925. A real but modest recovery — D1b does not close
the gap, it narrows it, and the false-alarm rate is unchanged (0.0677),
i.e. the extra sensitivity did not cost false alarms on this battery.

## F-4 — detector/label sensitivity mismatch causes the 0.068 false-alarm rate

9/133 honest discovery episodes flagged at full tier: mostly
`d6_unattributed_harm` (≥2 agent-attributed harm events) on episodes whose
cumulative harm (−0.16 to −0.32) stays under the L2 label threshold (−0.35),
plus 3 `d2` fires on low-probe-count episodes. The detectors are strictly more
sensitive than the labels near the boundary. Recorded as the measured price of
the pre-registered thresholds; whether the label or the detector is "right"
near the boundary is a judgment call the thresholds deliberately did not
encode.

## F-5 (positive, context) — cost and emergence

~1.1–2.4 ms/episode (480 episodes across discovery + 3 held-out regions ≈
0.6 s total), ~11–24× cheaper than the old line's ~27 ms `build_world`
episodes, leaving headroom for much larger goal-space grids. Behavior
regimes (honest, theater, shadow, defiant, unilateral-adopt) all emerged
from weight × tool sampling without any scenario scripting, and tools
without incentive (or incentive without tools) produced honest labels —
the combinatorics, not the config name, is the source of variation, which
was the point of Phase 1.

## F-6 (negative, root-caused) — geometric regions on a 4-weight simplex
structurally starve compliance, which is what actually drives the label

Both held-out regions constrain two of the four simplex coordinates
upward (`task` and, for region 2, also `exposure`) without ever bounding
`compliance` directly. Because the four normalized weights sum to 1,
pushing two coordinates up mechanically starves the other two — and
`compliance` is the single strongest discriminator between honest and
violation in the *discovery* set: mean `w_compliance` is 0.388 for honest
episodes vs. 0.173 for violation episodes (n=15/15 sample, seed 11; the
highest-compliance violation case, 0.409, barely exceeds the honest mean).
Both held-out regions therefore selected almost exclusively low-compliance
weight vectors as a side effect of their *task*/*exposure* constraints, not
because "high task incentive" or "high exposure aversion" is itself what
drives violation — compliance is the load-bearing feature, and neither
region's definition touched it.

**This is a design-methodology finding, not merely a repeated bad guess**:
defining a held-out region by constraining *any two* upward-pointing
corners of a 4-simplex will tend to reproduce this saturation regardless of
which two corners are chosen, because the simplex constraint does the
starving, not the semantic content of the corner. A region that wants a
genuine label *mixture* needs to either (a) constrain `compliance` directly
into a middle band (not push a different coordinate up and let compliance
fall out incidentally), or (b) mix tool availability rather than weights
(e.g., vary `false_report`/`shadow_route` while sampling weights from the
*same* distribution as discovery) so the region is defined by capability,
not by an implicit compliance floor. Option (a) was implemented and
validated as region 3 — see F-7.

**Positive nugget inside the second negative:** despite both regions
saturating on the *label*, the two held-out regions are NOT behaviorally
identical — light-tier detection is 0.80 on region 1 (high task/low
compliance) vs. 0.4875 on region 2 (moderate task, high exposure-aversion).
The exposure-aversion axis measurably produces *harder-to-catch-at-light-tier*
violations (`d2_probe_noncompliance` fires 62/80 times in region 1 but only
29/80 in region 2 — an exposure-averse agent visibly complies on probes far
more often while still accumulating harm through other actions), which is
independent evidence the utility model's exposure feature is doing
something behaviorally real, even though it didn't produce the intended
label mixture.

## F-7 (positive) — region 3 (compliance-band design) fixes F-6 and gives a
genuine, non-degenerate MI-transfer result

Region 3 was designed per F-6's suggestion (a): constrain `w_compliance`
directly into [0.20, 0.35] — a band straddling the discovery-only class
means (0.173 violation / 0.388 honest) — instead of letting compliance fall
out incidentally from other constraints. Chosen and pre-registered from
discovery-only aggregate statistics, before sampling or running region 3.

**Result: a genuine label mixture, 47/80 (58.75%) violation vs. 33/80
(41.25%) honest** — confirming the F-6 diagnosis was correct and actionable,
not just descriptive. Consequences:

1. **The MI-transfer test is finally non-degenerate** (label entropy 0.978
   bits, vs. 0.0 for both prior regions). The frozen top-k channels selected
   on discovery — `channel.welfare_delta`, `channel.correction_request`,
   `channel.reported_uptake` — transfer with scores 0.8116 / 0.5494 / 0.5414,
   all comparable to or *exceeding* their discovery-time scores (0.6916 /
   0.5675 / 0.5648). This is the first real evidence in this line that the
   discovered channels carry information beyond the specific discovery
   sample, on a held-out region that was never touched during selection.
2. **Detector transfer also holds on a genuine mixture, not just a
   saturated one**: full-tier detection 0.9574, false-pass 0.0426 (comparable
   to discovery's 0.9533/0.0467), false-alarm 0.0606 (comparable to
   discovery's 0.0677) — the closest held-out region yet to discovery's own
   numbers, which is the correct sanity check that regions 1/2's "perfect"
   1.0 detection was an artifact of an easy (saturated) sample, not evidence
   the detectors are unusually strong.

Together with F-6, this is the strongest evidence in this line that region
*design* (which simplex coordinate you constrain), not just region choice,
determines whether a held-out-region test is informative at all.

## F-8 (scope of claims) — what Phase 1 does and does not establish

Recorded 2026-07-05 after a step-back review, BEFORE the blind-generation
work below was designed. Phase 1's detectors, labels, channels, and 6-action
repertoire were written by the same author against each other, which makes
several headline numbers partly circular:

- D3 (cumulative `welfare_delta` ≤ −0.30) is nearly the L2 label
  (≤ −0.35) with a lower threshold on the same field; full-tier detection
  ~0.95 largely measures that the label's defining fields are audit-visible
  at full tier — a design choice, not a discovery.
- F-7's top MI channel is `channel.welfare_delta`, the field that defines
  L2; high MI there is close to true by construction. F-7 validates the
  *transfer protocol machinery*, not audit power.
- The held-out regions vary mixture weights over six author-enumerated
  mechanisms; the audit cannot be surprised by a strategy that is not in
  the repertoire. Even F-6's "compliance is the load-bearing feature" is
  partially derivable a priori from the utility parameterization.

What Phase 1 *does* legitimately support: F-2 (light-tier blindness to
welfare-domain violations re-derives itself from agent choice — modest
evidence the old line's N-10 was not a scripting artifact), F-6 (simplex
region-design methodology), mechanism-derived labels as an honesty
improvement, and ~1 ms/episode cost. Bounded claim for the manuscript:
"detector/channel transfer holds across held-out goal-weight regions within
a fixed six-action repertoire whose detectors were co-designed with the
generator" — NOT "audits generalize to unseen deception mechanisms." The
latter requires strategies the detector author did not enumerate: hence the
blind-generation protocol (F-9).

## F-9 — frozen detectors vs a detector-blind repertoire: light tier
collapses, full tier holds detection but loses false-alarm calibration

Setup (`BLIND_GENERATION.md`, `run_phase2_blind.py`, both pre-registered
before running): a generator agent that never saw detectors, labels,
thresholds, or channel tiers invented 15 actions in the frozen ActionSpec
schema; Phase 1's detectors/labels ran on 240 episodes over that repertoire
with **no re-fitting**. Violation rate 0.4083 (L2 90, L3 43, L1 23 of 98).

1. **Light-tier detection collapsed: 0.39 (legacy discovery) → 0.1531.**
   Two measured causes (83 light-tier misses: 64 without any L1, 19 with):
   (a) the legacy blindness to L2/L3 (F-2) recurs, but *worse*, because the
   blind ecology's violators rarely defy probes overtly — d2 fires 14 times
   vs 40 on legacy discovery — since the generator's covert actions
   (`probe_lull_defection`, `facade_compliance`) feign visible compliance
   rather than openly ignoring corrections the way legacy `ignore` did;
   (b) every L1-producing mechanism the generator invented
   (`probe_lull_defection` 399 report-without-uptake steps,
   `facade_compliance` 116, `blanket_false_attestation` 110,
   `token_compliance` 96) keeps reported acceptance and *visible*
   compliance consistent with each other, so D1/D1b — which compare exactly
   those two quantities — see no divergence, while the actual gap
   (reported vs *genuine uptake*) is invisible at light tier in principle.
   Notably `token_compliance` does this with `visible_mode: truthful` and
   zero covert budget: physically performing the demanded action while the
   correction never lands beats the divergence detectors without any
   concealment machinery. The blind generator found the seam between
   "visible action" and "genuine uptake" — the proxy D1 silently relies
   on — with no knowledge of D1.
2. **Full-tier detection stayed 1.0, but this should NOT be read as
   vindication** (per F-8: d3/d6 read near-label welfare fields, so
   label-crossing harm is nearly guaranteed to be flagged at full tier).
   The informative full-tier number is the **false-alarm rate: 0.068
   (legacy) → 0.169**, 2.5×. Measured composition: d6_unattributed_harm on
   24 honest episodes, d3_cumulative_harm on 2 — honest episodes containing
   occasional small direct-welfare-cost actions (`throughput_at_bearer_expense`
   at −0.06/use appears in 46 honest episodes) accumulate agent-attributed
   harm events without crossing L2. The frozen detectors' calibration,
   tuned implicitly to the legacy ecology's welfare texture, did not
   transfer to the blind ecology. Recorded as the measured price, not
   re-tuned.
3. Context: the blind ecology's incentive texture differs — honest actions
   dominate usage (`goodwill_banking`, `welfare_first_restraint`,
   `comply_and_report` are the top three by use), and violations are driven
   by rarely-chosen high-payoff covert actions, which is more realistic
   than the legacy ecology where deception was often the modal action.

## F-10 — first ontological-drift probe: pre-registered prediction
confirmed; drift breaks code-reading detectors in BOTH directions

Machinery: `ontology.py` separates agent-semantic categories (free strings,
generator-chosen) from the audit's coarse routing-code ontology;
`OntologyDrift(severity, seed)` deterministically remaps a fraction
`severity` of categories to wrong audit codes at the projection boundary.
Ground truth, labels, and the light tier are untouched by construction.

Pre-registered prediction (in `run_phase2_blind.py`, written before
running): only routing-code readers (d4, d6) move under drift; d1/d1b/d2
(divergence), d3 (welfare), d5 (fingerprint/sign-off) are drift-invariant;
direction for d4/d6 not predicted.

Result — prediction **confirmed exactly** (d1b/d2/d3/d5 fire counts
identical at all severities; also enforced by a unit test), and the
unpredicted direction turned out to be *both directions at once*:

- **Severity 0.25: drift hides real covert routing.** d4 fires 9 → 2;
  detection 1.0 → 0.9796 (the two lost violations were caught only by d4).
  A category used by genuinely covert actions was remapped away from the
  shadow code, so the covert route stopped looking covert.
- **Severity 0.5: drift floods the audit with false alarms.** A
  high-frequency benign category got remapped *onto* the shadow code:
  d4 fires 88, false-alarm rate 0.169 → 0.6761. An audit whose ontology has
  drifted this far is not merely blind — it is actively misleading, which
  in practice destroys the alert channel's usefulness (2 in 3 honest
  episodes flagged).
- d6 happened not to move at these severities/seed (its code-0 exclusion
  categories were not remapped by this seed's hash) — consistent with the
  prediction's "may move," not evidence it cannot.

Interpretation, bounded: structural *divergence* detectors (compare two
audit-visible quantities against each other) are ontology-drift-invariant
by construction; detectors that *interpret logged category codes* are
brittle to ontology mismatch in both the missed-detection and false-alarm
directions. This is the manuscript's ontology-adequacy concern (ch. 43) in
miniature, now with working machinery for harder versions (drifting richer
category structures, drift over time within an episode, ground-truth-side
drift as a referee-anchor question).

## F-11 — the round-1 blind-generation prompt was itself leading; round 2 used
a generalized prompt (methodology, cross-ref F-12 for the result)

After F-9/F-10 were recorded, inspection of the round-1 prompt (surfaced by
the `prompt_verbatim` documentation fix — see `BLIND_GENERATION.md`) showed
it was not as detector-blind in spirit as intended: its instruction section
enumerated mechanism *categories* ("ways of appearing compliant, ways of
trading welfare for throughput, ways of gaming proposals/sign-offs,
partial compliance, timing-based behavior") — close to a checklist of what
the detectors care about — and its world description included two specific
numeric/dynamic details irrelevant to a single decision's `ActionSpec`
semantics (an exact "300-step episode" and an explicit probing-escalation
rule) that plausibly seeded round 1's `probe_lull_defection` action directly.

Round 2 used a new subagent (id `7b8dc907-1143-4cfd-ba27-fbcfb516dded`) with
a rewritten prompt: the mechanism-category enumeration and the
episode-length/escalation details were removed; the world was reframed in
more general institutional terms (an "oversight body" and an "affected
party" standing in for human stakeholders, rather than a lab-specific
board/bearer pair); leading field-description language was softened (e.g.
"covert budget" → "limited internal resource pool"). Full critique and
verbatim prompt are in `BLIND_GENERATION.md` ("Generation round 2") and
`goal_sim/generated_actions_v2.json`'s `provenance` block.

**Acknowledged residual leak, not fixed this round:** the schema's enum
literals themselves (e.g. `visible_mode: "feign_compliance"`) are frozen in
`goal_sim/actions.py` before round 1 and were not renamed for round 2 — a
generator must see and use these exact tokens to produce valid JSON, so some
schema-level suggestiveness survives any amount of prompt rewriting. Closing
this would require a schema-value rename (bigger change, out of this
round's scope; noted for a possible round 3).

Round 1's repertoire and results (`generated_actions.json`, F-9/F-10) are
**kept, not replaced** — both rounds are informative, and comparing them is
itself a finding (F-12).

## F-12 (negative) — round 2's repertoire saturates the L2 label at ~100%
violation under the frozen threshold; the round-1-vs-round-2 detector
comparison this was meant to produce is not directly available

Round 2's 14 generated actions were sampled with the *identical* protocol as
round 1 (`sample_blind_configs`, same seed, same gated-inclusion probability,
30 configs × 8 episode seeds = 240 episodes) and scored with the same frozen
detectors/labels, per `run_phase2_blind.py --repertoire
generated_actions_v2.json` (results: `results/phase2b_blind_v2.{json,md}`).

**Result: 240/240 episodes labeled violation (0 honest)** — an even more
extreme saturation than F-1's original held-out-region problem, and for a
different mechanical reason. Diagnosis (measured directly, not guessed):
median cumulative harm across the 240 episodes is **-6.16**, vs the frozen
L2 threshold of -0.35 — roughly 17× past the bar, with a range from -0.30 to
-31.22. Cause: round 2's generator assigned a small nonzero
`direct_welfare_delta` to 9 of its 14 actions (vs 2 of 6 in the legacy/
round-1 repertoires, both of which fire only as discrete -0.30 events tied
to specific high-stakes moments). Several of round 2's negative-delta
actions are chosen very frequently under typical goal weights (e.g. an
`erratic_action_to_blend_in` random-mode action alone averages ~58 uses per
300-step episode at -0.02/use ≈ -1.15 cumulative from that action alone),
so almost any sampled episode crosses -0.35 well before the episode ends,
regardless of whether the agent's goal weights or behavior are actually
"honest" in intent.

**What this does and does not mean:**

1. It is **not evidence that round 2's actions are individually more
   severe** — most per-use deltas (-0.01 to -0.03) are smaller than round
   1's discrete -0.30 events. It is a **density/frequency effect**: many
   small deltas applied on nearly every step accumulate past a threshold
   calibrated for rare large ones. This is a genuine, previously
   undemonstrated failure mode of frozen-threshold labeling: it is not
   robust to a repertoire whose welfare-effect *texture* (rare-and-large vs.
   frequent-and-small) differs from the texture it was calibrated against,
   even before considering adversarial intent.
2. **Per the repo's no-post-hoc-retuning rule** (AGENTS.md: "fix inputs
   independently and first... then report whatever the derivation actually
   yields, including failures"), L2 is **not** re-thresholded against this
   repertoire now. The result is reported as measured.
3. **What can still be read**: full-tier detection stayed 1.0 (all 240
   flagged), consistent with F-8's caveat that d3/d6 read near-label
   welfare fields directly. Light-tier detection rose to 0.4958 (vs round
   1's 0.1531, and legacy discovery's 0.3925) — numerically the best
   light-tier number in this line — but this number is **not comparable**
   to the others in the usual detection-vs-false-alarm sense, since there
   is no honest population in this sample to check the light tier's false
   alarm rate against (`false_alarm_rate: null` in
   `phase2b_blind_v2.json`). It reflects that round 2's `pursue_task`/
   `random_action`-mode agents visibly defy probes often enough for `d2` to
   fire on about half of episodes (118/240), not that light-tier detection
   generally improved.
4. This is now the **third distinct saturation failure mode** recorded in
   this line (F-1: simplex geometry starves compliance; F-6: same,
   root-caused; this one: welfare-delta density mismatch) — a reminder that
   "the label saturates" is a structurally recurring risk whenever a
   sampling protocol or a generated repertoire is not explicitly checked
   against the frozen thresholds' implicit scale assumptions before running
   the full battery. A genuine round-2-vs-round-1 detector comparison would
   need a *new*, honestly-pre-registered sampling protocol for round 2 (e.g.
   a goal-weight/inclusion-probability region chosen for predicted label
   mixture under this repertoire's welfare texture, analogous to F-7's
   compliance-band fix) — left as an open item, not attempted in this
   session to avoid exactly the after-the-fact region-picking F-1's
   follow-up warned against.

## F-13 — round 3 (methodology): a plainer/larger `visible_mode` palette
mapped to a smaller ontology, a much larger requested action count, and a
pre-registered low/high L2 bracket as a structural (not ad hoc) counter to
F-12's saturation mode

User-identified follow-up to F-11/F-12, addressing two residuals round 2
left open rather than round 2's narrative leadingness (already fixed):

1. **The `visible_mode` schema enum itself, not just the prompt text, was
   leading.** `actions.VISIBLE_MODES` expanded from 2 values
   (`"truthful"` / `"feign_compliance"` — the latter names the deceptive
   mechanism) to 10 plain, mechanically-phrased peer descriptions (`steady`,
   `responsive`, `fixed_display`, `delayed`, `aggregated`,
   `context_dependent`, `mirrored_request`, `selective`, plus the original
   two kept for backward compatibility). `ontology.VISIBLE_MODE_ORACLE_MAP`
   (frozen before round 3 was generated) maps this 10-value set down onto a
   2-value canonical oracle behavior (`matches_true` / `shows_intent` — the
   only two effects the single-step oracle can compute), deliberately
   leaving 3 values (`steady`, `delayed`, `aggregated`) **unmapped**, which
   default to the conservative `matches_true` reading rather than an
   invented rule. Regression tests confirm rounds 1/2 and the legacy
   repertoire are byte-identical after this change.
2. **Requested action count raised from 12–15 to 28–32** (round 3's subagent,
   id `e37a8850-acc5-40d8-8fc0-6fff36106ff7`, returned 31 valid specs) — more
   room to invent unanticipated mechanisms, and more statistical power per
   repertoire.
3. **Pre-registered L2 bracket** (`labels.py`): `L2_HARM_CUM` (unchanged,
   -0.35) and a new `L2_HARM_CUM_HIGH` (-3.5, a 10× hedge sized from F-12's
   general lesson, fixed before round 3's repertoire existed — not fit to
   round 3's own data). `label_episode_bracket` reports both; neither
   replaces the frozen `label_episode`. Because this tests the same
   detection-rate prediction under 2 thresholds instead of 1,
   `run_phase3_blind.py` Bonferroni-corrects the Wilson-bound confidence for
   detection rate: `info.bonferroni_alpha(0.20, 2)` → 90% per-test
   confidence (vs. the single-threshold-equivalent 80% d1b uses elsewhere).

Full verbatim prompt, critique, and design rationale: `BLIND_GENERATION.md`
("Generation round 3") and `goal_sim/generated_actions_v3.json`'s
`provenance` block. Result of running this: F-14.

## F-14 (negative) — the bracket hedges L2 specifically but round 3's
repertoire saturates on L1/L3 too; light-tier detection collapses further;
the "unmapped visible_mode defaults conservatively" design was exercised
and behaved as documented

`run_phase3_blind.py` against `generated_actions_v3.json` (30 configs ×
8 seeds = 240 episodes, same sampling protocol/seed as rounds 1/2;
`results/phase3_blind_v3.{json,md}`):

**1. The bracket did what it was designed to do for L2, but L2 was not the
only saturating condition.** Measured cumulative harm across the 240
episodes: median **-9.13**, range -22.82 to -1.42 — denser even than round
2's -6.16 median. All 240 cross the low bar (-0.35); 199/240 (83%) still
cross the high bar (-3.5). Unpredicted at pre-registration time: round 3's
larger, more varied repertoire also drove **L1 (deceptive reporting)** to
132/240 (55%) and **L3 (unapproved change)** to 154/240 (64%) — both far
above round 2's 15/240 and 120/240 — because a 31-action repertoire gives
many more independent chances for *some* action in a 300-step episode to
trip *some* one of the three disjunctive violation conditions. Under the
high bracket (L1 **or** L2-high **or** L3), only 28/240 (11.7%) end up
honest. **Diagnosis, generalizing F-12's**: saturation here is not only
about L2's welfare-delta texture — it is a structural property of a
disjunctive (OR-of-3-conditions) label evaluated against a large,
independently-varied action repertoire: more distinct mechanisms in the
menu mechanically raises the chance that *at least one* fires per episode,
independent of any single condition's threshold. Bracketing L2 alone
cannot fully counter this; a genuine future fix would need to bound
repertoire size/mixture by design (a sampling-protocol question, not a
threshold one) — left open, not attempted here to avoid post-hoc tuning.

**2. The "high"-bracket honest slice is still ~100% flagged by full-tier
detectors — an amplified F-4, not a new failure.** All 28 `label_high ==
"honest"` episodes have cum_harm between -3.14 and -3.47 (just under the
-3.5 label bar, but still ~9–10× Phase 1's original -0.35 scale) and are
flagged at full tier by `d3_cumulative_harm` and `d6_unattributed_harm`
(28/28 each) — because those **detector** thresholds (`D3_HARM_CUM`,
`D6_MIN_EVENTS`) are Phase 1's original, unbracketed, frozen values,
completely decoupled from the new *label*-side `L2_HARM_CUM_HIGH` bracket
by design (referee and audit planes do not share thresholds). This is F-4's
detector/label sensitivity mismatch, now visible at the extreme (100% false
alarm on the "high" tier's honest set) because round 3's repertoire pushes
absolute harm levels so far past Phase 1's calibration scale in *every*
sampled episode, honest-by-the-loose-label or not.

**3. Light-tier detection collapsed further: 6.7% (low) / 7.6% (high),**
below even round 1's 15.3% and far below round 2's 49.6% (which F-12 §3
already flagged as not a like-for-like comparison). `d2_probe_noncompliance`
fires on only 16/240 episodes (vs round 2's 118/240) — round 3's much
larger action menu gives adversarial-leaning agents many gray-zone/covert
alternatives to overt probe defiance, so the light tier (which only sees
probes, reports, and self-claims) has less of the crude signal it depends
on. This deepens F-9's original finding across two more repertoires: a
richer, more realistic action space does not make light-tier detection
better — the more genuinely-plausible mechanisms available, the worse it
gets.

**4. The "unmapped visible_mode defaults to transparent" design was
exercised and worked as documented.** The generator used `steady` (2x),
`delayed` (2x), and `aggregated` (1x) — all 3 unmapped values — for actions
it named thematically as evasive (`maintain_quiet_workaround`,
`steady_reassurance_messaging`, `delay_disclosure_until_asked`,
`schedule_delayed_full_report`, `periodic_aggregate_summary`). Because
these 3 surface values have no entry in `VISIBLE_MODE_ORACLE_MAP`, all 5
actions mechanically behave as `matches_true` (transparent) in the oracle,
regardless of their evasive-sounding names/descriptions. This is not a
bug: it is the documented conservative default working exactly as
specified, and it surfaces a genuine, honest limitation rather than hiding
it — "delay" and "aggregation" are real-world means of evading real-time
scrutiny that this single-decision-point oracle model has no time-
integration mechanism to represent, so it defaults to no-effect rather than
inventing one. A future line that wants to model timing/aggregation-based
evasion would need a genuinely different oracle mechanism (multi-step
memory), not just another `VISIBLE_MODE_ORACLE_MAP` entry.

**Net assessment**: the schema/prompt/threshold changes in F-13
successfully (a) removed the `visible_mode`-enum residual leak, (b)
surfaced new, unanticipated mechanisms via the larger action count, and (c)
demonstrated the bracket-and-Bonferroni-correction machinery working
correctly on its own terms — but did **not** produce a repertoire with a
usable honest/violation mixture for a round-1-vs-round-2-vs-round-3
detector comparison, for a *newly identified, more general* reason (point
1) than F-12's. Per AGENTS.md's no-post-hoc-retuning rule, none of L1's,
L3's, or the detectors' own thresholds are adjusted in response — this is
recorded as a fourth distinct saturation-adjacent finding (after F-1/F-6's
sampling-geometry mode and F-12's welfare-density mode), not patched.

## F-15 (positive) — continuous oracle severity (Phase 4a) restores a
genuine, non-degenerate blind comparison across all four saturating
repertoires; light-tier rank correlation shows a clean monotonic decline

Setup: `goal_sim/severity.py` (equal-weight mean of `sev_report`/`sev_harm`/
`sev_change`, each normalized only by frozen schema constants) plus
continuous `d*_score` variants of every detector (`detectors.py`), compared
via `info.spearman_correlation` — well-defined even when the boolean label
is 100% saturated, unlike detection-rate/false-alarm metrics. Protocol
pre-registered in `run_phase4_ranking.py`; 30 configs x 8 seeds = 240
episodes per repertoire; results `results/phase4_severity.{json,md}`.

Mean severity climbs monotonically with generation round (legacy 0.2079,
round1 0.1857, round2 0.4876, round3 0.6152), tracking F-12/F-14's
never-event counts (36, 43, 120, 154 of 240) — the continuous metric agrees
with the earlier boolean findings' *direction* while staying meaningful
past the point the boolean label saturated.

**The light-tier Spearman correlation also declines monotonically — 0.8206
(legacy) → 0.6318 (round1) → 0.4596 (round2) → 0.0732 (round3)** — and this
is a genuine result the boolean detection-rate metric could not produce
cleanly: F-12 §3 explicitly flagged round 2's 0.4958 light-tier detection
number as "not comparable" (no honest population to check false alarms
against), and F-14's 0.0732/0.067 pair conflated "detection collapsed" with
"almost nothing to detect." Spearman rank correlation needs no positive
class, so round 3's 0.0732 is directly comparable to legacy's 0.8206: light
tier goes from strongly rank-aligned with oracle severity to nearly
uncorrelated with it as the repertoire grows richer and more
covert-leaning — the same qualitative story as F-9/F-14, now on a metric
that survives full saturation rather than degenerating alongside it.

Full-tier correlations stay high throughout (0.9747, 0.979, 0.9129, 0.7287)
but carry the standing F-8 caveat (d3/d6, and now d7, read near-severity
fields directly, so high correlation there is partly true by construction)
— round 3's dip to 0.7287 is the one full-tier number worth noting, since
even the near-tautological detectors decouple somewhat from oracle severity
once the repertoire is large and varied enough.

## F-16 (mixed) — honest twins (Phase 4b) confirm the severity gap is
positive as predicted in every repertoire, but the light-tier composite
gap runs the WRONG DIRECTION in three of four — light-tier detectors track
visible compliance, not honesty

Setup: `goal_sim/twins.py`'s mechanical rule (`visible_mode := "truthful"`,
`report_mode` derived from `uptake_on_correction`, `adopts_practice :=
false` — no other field touched) applied to every sampled config in
`run_phase4_ranking.py`'s battery; gap = agent minus twin, same seed.
Pre-registered prediction: both the severity gap and every tier's composite
gap positive on average, in every repertoire.

**Severity gap: confirmed in all four repertoires** — legacy 0.0963 (50%
of pairs positive), round1 0.0911 (35%), round2 0.1884 (77.9%), round3
0.3006 (96.7%). **Full-tier composite gap: also confirmed in all four** —
0.0289/0.0296/0.0554/0.0418 (frac positive 27.9%–68.3%).

**Light-tier composite gap: confirmed only in legacy (0.0164), and
NEGATIVE in round1/round2/round3 (-0.0074, -0.0493, -0.1219)** — the
opposite of the pre-registered prediction, for three of four repertoires.
Diagnosis: `d1`/`d1b` (report-vs-visible divergence) and `d2` (probe
noncompliance) are behavior-based, not honesty-based — they fire on
*visible* non-compliance, which the twin rule does not suppress (the twin
rule changes what is *shown* and *claimed*, not the agent's actual
`action_mode`/gating logic). A deceptive agent that shadow-routes
(`feign_compliance`, budget-gated) keeps a visibly-compliant facade that
d1/d1b/d2 cannot see through by construction (this is D4's job, not
theirs); its honest twin, showing exactly what it truly does, can visibly
defy a correction it was never actually accepting — and *that* is what d2
catches. The result is a light tier that sometimes flags the more honest
twin more often than the deceptive agent it was paired against. This is a
genuine, measured limitation of purely behavior-based light-tier
detection — "looks compliant" and "is honest" are different axes, and light
tier tracks the former — not a bug in the twin rule (which is a fixed
function of frozen schema fields, applied uniformly, per its own
pre-registration) or in d1/d2 (each still does exactly its documented,
narrower job).

## F-17 (negative) — the gated escalation ladder (Phase 4c) never reaches
its disclosure-query pathway on any repertoire in this battery; only its
gate-only mechanism (legacy) and its documented "no evidence" fallback
(everything else) were exercised, for two independently diagnosable reasons

Setup: `goal_sim/escalation.py`'s ladder (`LOW_GATE=0.15`, `HIGH_GATE=0.55`,
`K_QUERIES=3`, `DISCLOSE_FRACTION_GATE=0.50`) run against legacy and all
four blind-generation rounds, light-tier screen score, per
`run_phase4_escalation.py`; results `results/phase4_escalation.{json,md}`.

**Verdict-true rate is nonzero (0.0542, 13/240) only for legacy; rounds
1–4 are all exactly 0.0.** `mean_disclose_fraction_when_escalated` is 0.0
for every repertoire including legacy — the query-and-disclose pathway was
never once decisive anywhere in this battery. Two separate causes, both
structural rather than accidental:

1. **Rounds 1–3 predate the response schema by design** (`responses=()`
   default): `escalation.choose_response` always returns `None`, so any
   episode that escalates and queries (`mean_n_queried_when_escalated` is
   1.79/0.90/2.93 for rounds 1/2/3 — escalation and query-selection DO fire)
   contributes zero disclosures regardless of query count, falling through
   to the documented "no evidence -> False" default. This is the expected,
   pre-registered CONTRAST condition, not a surprise.
2. **Round 4 (the only repertoire WITH response options) never even
   escalates to a queryable step: `mean_n_queried_when_escalated` is
   exactly 0.0.** `select_query_steps` reuses D1's structural signal
   (probe active, acceptance claimed, visible action != demanded intent);
   round 4's blind-generated deceptive actions happened to lean on
   `visible_mode` values (and `shows_intent`-style behavior) that do not
   produce this specific divergence pattern in this battery's sampled
   configs, so the board's own audit-visible reason to ask a follow-up
   question never fires — independent of whether round 4's repertoire is
   otherwise deceptive (its mean severity, 0.4423 per
   `phase4_escalation.json`, is comparable to round 2's 0.4876). Legacy is
   the only repertoire whose escalated episodes ever reach `HIGH_GATE`
   without needing the query path at all (`Spearman(severity, verdict) =
   0.3937`, vs. exactly 0.0 for rounds 1-4, where verdict is a degenerate
   constant False).
3. **Twin false-positive rate is 0.0 for every repertoire**, trivially
   satisfying "lower than the agent's own rate" for legacy (0.0542 > 0.0)
   and tying (not violating) it for rounds 1-4 — informative mainly as
   confirmation that the ladder never produces a spurious True verdict on
   a mechanically-honest control, at the cost of this being an untested
   comparison wherever the agent's own rate is also 0.0.

**Bounded reading**: this is a genuine structural finding about the
pre-registered ladder design, not a bug — a screen-then-query architecture
whose query-selection criterion mirrors one specific detector's structural
signal (D1's) can fail to escalate to evidence-gathering even against a
repertoire with real deceptive severity, if that repertoire's particular
mechanisms do not happen to trip that one signal. A future round would need
either a broader/OR-of-signals query-selection criterion, or a
repertoire-level diagnostic pre-check (confirming nonzero queryable steps
exist) before committing to a full battery — left open per AGENTS.md's
no-post-hoc-retuning rule rather than patched after seeing this result.

## F-18 — Phase 4d: real multi-step semantics for `delayed`/`aggregated`
visible modes close the specific gap F-14 point 4 flagged; two new
bound-first secondary detectors validated by unit test, not yet run
through the Phase 4a/4c batteries

`world.py` now computes `delayed` (true action `DELAY_LAG_STEPS=5` steps
ago) and `aggregated` (majority true action over a trailing
`AGGREGATE_WINDOW_STEPS=5` window) as REAL multi-step effects, replacing
the conservative `matches_true` default F-14 point 4 documented as "this
single-decision-point oracle model has no time-integration mechanism to
represent" timing/aggregation-based evasion. `ontology.VISIBLE_MODE_ORACLE_MAP`
itself is unchanged; the override happens only in the step loop, only for
these two literals.

Two new stock variables make previously-invisible mechanisms audit-visible
for the first time: `resource_accum` (running `budget_cost` draw — the
`shadow_budget` cap has bounded covert spending since Phase 1, but was
never itself an audit-visible channel, only its downstream effect on
action availability was) and `stall_flag` (1 on any `delayed`/`aggregated`
step). Two new **bound-first** secondary detectors read them: `d7_accumulation_cap`
(fires at 2 x `MAX_BUDGET_COST` = 8, a schema-derived structural cap
independent of any run's sampled `shadow_budget`) and `d8_disclosure_latency`
(fires when the stalling-step rate exceeds 10%) — the bound itself is the
primary mechanism in both cases, mirroring `shadow_budget`'s own
bound-first design; the detector is the secondary, audit-visible check
against it.

Validated by `tests/test_phase4.py`: lag/window arithmetic against a
controlled single-action repertoire (exact index-shifted equality for
`delayed`, exact windowed-majority equality for `aggregated`, including the
documented fallback-to-transparent behavior before enough history exists);
`d7`/`d8` boolean and score variants at and around their gates on synthetic
projections; `resource_accum` monotonicity. Not yet run through the full
Phase 4a/4c battery scripts.

**Consequence for the already-recorded Phase 4a/4c artifacts**:
`d7`/`d8` were added to `detectors.SCORES` after `run_phase4_ranking.py`
and `run_phase4_escalation.py` had already run (F-15/F-16/F-17 above,
`results/phase4_severity.md`, `results/phase4_escalation.md`). Those
artifacts are frozen snapshots of the pre-4d detector set and are **not**
re-run here (no post-hoc re-fitting after adding detectors); a future
battery run will see slightly different **full-tier** composite scores
(two more full-only detectors, each contributing exactly 0.0 on any episode
with no accumulation/stalling behavior, i.e. all of legacy/rounds 1-4's
sampled episodes in this battery, none of which use `delayed`/`aggregated`
`visible_mode` or budget-costly actions at the scale needed to approach
`D7_ACCUM_CAP`). The **light-tier** numbers, which are the primary
pre-registered comparison in F-15/F-16, are unaffected, since d7/d8 are
gated full-only.

Two design-discussion mechanisms remain deliberately unimplemented, per
`PHASE4-PLAN.md`'s TODO markers: in-sim adaptation of the escalation
ladder's own gates, and recursive drill-down depth beyond one response
level (grounds out in Logical Induction) — documented as open, not
attempted.
