# 2026-10-20 — Last Safety grammar parse robustness

kind: correction
uptake: local

## Trigger
Review grammar parsing and tests; fix bugs (tests first), apply parser robustness, align spec to recent code, close test gaps; end of session and commit.

Prompts: paraphrase only (no prompt id in transcript)

## Done
- content: **Multi-clause rollback** — LLM sequences restore session on mid-line error; clause transcript uses `clause_text` (`lib/game.mjs`).
- content: **Completions** — Distinct empty-field opening phrases; Who local parse; Hi uses inferred room addressees; reply openings person-channel only (`public/grammar.js`).
- content: **LLM path** — `preparePlayerUtterance`, hint truncation, JSON parse fallback, exported sanitize helpers (`lib/llm.mjs`); server uses cleaned parse as hint (`server.mjs`).
- content: **Spec** — `spec/grammar.md`, `spec/testing.md` updated for Think on empty person channel, rollback, sanitize tests.
- content: **Tests** — `tests/parse-sequence.test.mjs`, `tests/llm/sanitize.test.mjs`, grammar/ranking extensions; bundles prior `tests/llm/parse-{story,probes}.test.mjs` and `test:llm` script.

## Decisions
- **Spec follows code** on Think chip (person + empty room), synonym opening chips, and Show “and ask about it” as single act.
- **One commit** with compound-parse + LLM fixtures from earlier same-day session (see `2026-10-20-last-safety-llm-parse-tests.md`).

## Open / next
- Run `npm run test:llm` before push when `OPENAI_API_KEY` set; probes may flake.
- Optional: composer UI for multi-clause preview while typing.

## Key paths
- `game/the-last-safety-review/lib/llm.mjs`, `lib/game.mjs`, `public/grammar.js`
- `game/the-last-safety-review/tests/llm/`, `tests/parse-sequence.test.mjs`

## Verification
- `cd game/the-last-safety-review && DEMO_MODE=1 npm test` — 155 pass, 1 skipped.

## Commits
- `5fdf7595c` — Last Safety: harden grammar parsing and LLM multi-clause handling.
