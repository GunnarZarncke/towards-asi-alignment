# 2026-08-17 — Reward as evidence, Byrnes as construction alternative

## Trigger
Does ch21 discuss Turner’s reward-function-design posts? User then asked to discuss Turner (reward is not the optimization target; why still use reward), keep shards out of scope via the model-internals limit, treat Byrnes as an alternative construction approach, and include Pihlakas’s concave/homeostatic agenda.

## Done
- New ch21 §`sec:reward-not-optimization-target`: Turner’s reinforcement-schedule critique; reward as evidence channel for `(B,W,Φ)`; shards out of scope (ch05 whitebox + App B opacity default); Byrnes as construction rival; Pihlakas concave training + BioBlue drift.
- ch15 Byrnes section now names the construction-vs-inference fork; WWCTV bullet if brain-like circuits succeed without recoverable outer geometry.
- ch17 shard paragraph points to the internals exclusion and ch21’s inference-target cut.
- App B intervention map: shard internals stay out of the inference target; new row for Byrnes / Pihlakas.
- Bib: `turner2022rewardnotopt`, `pihlakas2025concaveagenda`, `pihlakas2025bioblue` + summaries. `check_bibliography_summaries.py` passed.

## Decisions
- Shards stay a ch17 borderline sibling, not a ch21 inference object, because they are model internals (ch05 / App B).
- Byrnes is discussed as a rival *construction* program (ch15 primary, ch21 fork), not as internals survey.
- Pihlakas is a sibling outer-training prescription plus empirical evidence that flat scalar aggregation is fragile; not adopted as the book’s target.

## Open / next
- Optional: cite Turner’s RFD manifesto (`oxvnREntu82tffkYW`) as a footnote if the “field of reward function design” name should appear.
- PDF rebuild not run this session.

## Key paths
- `chapters/ch21-reward-to-bundle-inference.tex` (`sec:reward-not-optimization-target`)
- `chapters/ch15-values-compressed-control.tex` (`sec:structured-social-drive-proposal-ch15`)
- `appendices/appB-bridge-crosswalk.tex` (`sec:intervention-coverage-map`)
