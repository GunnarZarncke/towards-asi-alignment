# 2026-08-01 — AFFINE field openness

## Trigger
User asked to check AFFINE seminar learning outcomes against the project, then to implement a plan: reopen outer-alignment peers, Meta (substitution hazards) in App. F, anthropics vs acausal split, CCC→CCI, predictor-loop genesis with Lean TODO, NAH WWCTV, terminology duals, and archive AFFINE into `context/`.

## Done
- Archived AFFINE curriculum: `context/affine-seminar-learning-outcomes.md`; indexed in `context/lw-references.md`.
- App. B: field-agendas overview + outer-alignment peers table (CEV/CBV paired, QACI, PreDCA, KANSI, tool AI, conditioning predictors); anthropics≠acausal note on MB7d; intervention-map rows; softened takeaway.
- App. F: new §Preparadigmatic research hazards (substitution hazards careful framing + Meta checklist).
- App. E glossary: field dual terms section.
- Targeted chapters: ch02 (predictor genesis), ch04 (CEV+CBV), ch07 (NUS), ch10 (outer/inner + predictor loop + anthropic capture), ch14 (CCC→CCI), ch17 (NAH WWCTV), ch25 (EU/coherence), ch27 (tool-AI peers), ch35 (acausal≠anthropic), ch44 (predictor-loop + robustness-to-scale row).
- Bib keys + summaries: CBV, PreDCA, QACI, KANSI, Predict-O-Matic, oracle AI, conditioning, NUS, selection vs control, natural latents, P2B, anthropics paper, AFFINE seminar.
- Lean TODO: `metadata/TODO.md` chapter↔Lean gap + `formal/README.md` open note for `PredictorLoop.lean`.
- `python3 scripts/check_bibliography_summaries.py` passed (456/456).

## Decisions
- Meta lives in App. F only (no new chapter).
- Predictor-loop: strong subsumption in prose; Lean formalization deferred as explicit TODO.
- Substitution hazards: preparadigmatic Meta hypothesis, not org indictment; distinct from NUS and Goodhart.
- NAH: WWCTV only; what-follows bullets without promoting NAH to spine.

## Follow-up (same day, user edits + agent pass)
- User removed App. B field-agendas/outer-peers section (show not tell); removed MB7d anthropic sentence and most acausal–anthropic distinctions; removed glossary field-dual section.
- Agent: App. F split Meta *problem substitution* vs object-level *substitution hazards*; MIRI-only preparadigmatic sentence; CCC `\autocite{affine2026seminar}`; NAH moved next to shard theory in ch17; broken `sec:outer-alignment-peers` refs fixed; terminology toward field names (perils of predictors, NUS, selection vs control note in ch34).

## Open / next
- Implement `Field/Finite/PredictorLoop.lean` when prioritized.
- Optional: deeper outer/inner consistency sweep beyond ch10/ch44.
- Optional: Obliqueness remains minimal (no dedicated section, as planned).

## Key paths
- `context/affine-seminar-learning-outcomes.md`
- `appendices/appB-bridge-crosswalk.tex` §`sec:field-agendas-outer-peers`
- `appendices/appF-research-program.tex` §`sec:preparadigmatic-hazards`
- `chapters/ch10-strategic-opacity.tex` (predictor-loop genesis)

## Commits
- `147e1aba` — Integrate AFFINE field coverage: outer-alignment peers, Meta hazards, and predictor-loop genesis.
