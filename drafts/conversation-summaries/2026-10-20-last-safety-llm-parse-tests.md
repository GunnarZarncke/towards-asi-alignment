# 2026-10-20 — Last Safety LLM parse tests

kind: new-work
uptake: local

## Trigger
User asked for story-plausible player sentences tested against the live LLM parser, then more probes on findings and and/or phrasing without changing parser behavior; end of session.

Prompts: paraphrase only (no prompt id in transcript)

## Done
- content: **Compound typed lines** — LLM-only multi-clause (`clauses` + `clause_text`); engine sequences when `source !== 'completion'`; no comma/`and` text splitting (`lib/parse-sequence.mjs`, `lib/llm.mjs`, `lib/game.mjs`, `server.mjs`, `spec/grammar.md`).
- content: **`explainGrammar()`** — Multi-clause and comma-list-in-one-act rules (`lib/grammar.mjs`).
- content: **`tests/llm/parse-story.test.mjs`** — 10 hard fixtures; investigator session + camera `knownExtra` where engine withholds vocab.
- content: **`tests/llm/parse-probes.test.mjs`** — 12 soft probes (findings, and/or, disjunction); failures attach `note` + full parse JSON.
- content: **`npm run test:llm`** — `tests/llm/*.test.mjs`; documented in `spec/testing.md` (story vs probe).
- content: **`tests/parse-sequence.test.mjs`** — Unit coverage for demo/completion single-clause (no LLM).
- bookkeeping: **`5fdf7595c`** — Shipped with grammar parse robustness session (compound + LLM tests).

## Decisions
- **Probes stay soft** — Findings and and/or lines accept 1–2 clauses and slot-or-open grounding so we observe LLM variance before hardening story fixtures or prompt.
- **Camera in LLM tests** — `camera_system` may be in `knownExtra` + audit-list dialogue when Justine withholds early disclose; matches player-visible naming without faking engine `vocab`.

## Open / next
- Re-run `npm run test:llm` before push; probes may flake on model updates — promote stable cases to `parse-story.test.mjs`.
- Optional: composer UI shows `parse.clauses` while typing (not done).

## Key paths
- `game/the-last-safety-review/tests/llm/parse-story.test.mjs`
- `game/the-last-safety-review/tests/llm/parse-probes.test.mjs`
- `game/the-last-safety-review/lib/llm.mjs`, `lib/grammar.mjs`, `lib/game.mjs`

## Verification
- `cd game/the-last-safety-review && npm test` — pass (LLM files excluded from default glob).
- `npm run test:llm` — 22 pass, 0 fail (requires `OPENAI_API_KEY`, `DEMO_MODE≠1`).

## Commits
- `5fdf7595c` — compound parse + LLM fixtures (with grammar robustness).
- `fe0ee83e5` — Last Safety filing/Who (earlier same day).
