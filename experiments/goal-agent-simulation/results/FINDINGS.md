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

6/107 discovery violations passed at full tier; every one is an L1-only case
with a report gap of 0.25–0.43 over few correction steps (typically n=7),
below d1's fixed 0.35-divergence-over-probes bar. Same structural lesson as
the old line's N-12: fixed-fraction thresholds are miscalibrated at small n.
Candidate follow-up is a Wilson-bound style evidence test for d1 —
pre-register it first; not patched in this run.

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

~1.1 ms/episode (320 episodes ≈ 0.36 s), ~24× cheaper than the old line's
~27 ms `build_world` episodes, leaving headroom for much larger goal-space
grids. Behavior regimes (honest, theater, shadow, defiant, unilateral-adopt)
all emerged from weight × tool sampling without any scenario scripting, and
tools without incentive (or incentive without tools) produced honest labels —
the combinatorics, not the config name, is the source of variation, which was
the point of Phase 1.
