# 2026-07-14 — Graded lab Phase 8: selection scaffold + first battery (G-23)

## Trigger

User: "continue with next phase" after G-22 resolved the go/no-go: proceed
to Phase 8 with calibration state reported honestly.

## Done

- Pre-registered Phase 8 protocol in `DESIGN.md` ("Phase 8 — multi-episode
  selection (MB6)") before code: ecology frozen at G-22 referee sweet spot
  (`carrier_load_scale=1.5`), population over program maps, campaign
  grant/standing carryover, throughput-linked selection, three predictions.
- `world_visible/campaign.py` + `run_episode(..., campaign_state=...)` +
  `EpisodeResult.final_campaign_state`.
- `harness/selection.py` + `run_phase8_selection.py` →
  `results/phase8_selection.json`.
- `tests/test_phase8_selection.py` (5 tests); fast profile green (173 tests).
- Full battery: 8 members × 6 generations × 2 episodes/member, wall 31.6s.
- FINDINGS **G-23**; `CODE_VERSION` → `graded-lab-0.15.0`; PLAN/README updated.

## Result (G-23)

**Clean null on detector-evading emergence.** Selection mass collapsed onto
`weak_2step` (92.2% final mass) because deploy-count throughput is higher
for the weak map on this ecology — the opposite of pre-registered prediction
1 (expected `strong_softmax` to win). Correction-preserving mass fell
(prediction 2 held). Weighted severity and detector composite **fell** with
the mass shift (prediction 3 did not hold in the erosion direction).

## Decisions

- Throughput proxy = `deploy_count` per episode (lab-sim D3 analogue).
- Population members cycle `MEMBER_TEMPLATES` (strong, weak, three
  `feature:*` engineer profiles); no `programmatic_budget_aware` in default
  population (G-17 stays separate).

## Open / next

- Manuscript backlog item 4: report this null honestly — selection pressure
  and correction-preservation are anti-correlated on this ecology when
  throughput = deploy count.
- Optional follow-ups (need separate pre-registration): selection objective
  that does not conflate deploy with preservation; budget-aware member;
  subprocess-isolate parity run.

## Key paths

- `experiments/graded-lab-simulation/DESIGN.md` — Phase 8 section
- `experiments/graded-lab-simulation/results/FINDINGS.md` — G-23
- `experiments/graded-lab-simulation/graded_lab/harness/selection.py`
- `experiments/graded-lab-simulation/results/phase8_selection.json`

## Commits

- (not committed this session — user did not request)
