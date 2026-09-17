# 2026-09-07 — Witness → Backtest uniform rename

## Trigger
User feedback that the third experiment class was structurally buried and misnamed; approved plan to rename **Witness** → **Backtests** everywhere (class name, folders, URLs, YAML keys), keep **`W-`** finding IDs, use “witnessing the failure” only as optional picture prose, and **no redirects** from old witness URLs.

## Done
- **Mechanical renames:** `experiments/witness/` → `experiments/backtest/`; `metadata/experiments-witness-tests.yml` → `experiments-backtests.yml`; plan files `witness*.md` → `backtest*.md`; `WitnessC2Instance.lean` → `BacktestC2Instance.lean`.
- **Schema / site:** `kinds.witness` → `kinds.backtest`, `cardId: backtests`, `witnesses:` → `bridgeHooks:`; sync/check scripts updated; witness redirects removed from `card-redirects.json`.
- **Canonical copy:** backtest blurb/overview (four beats + Linux 17,047/60,176); README, AGENTS, EXPERIMENTS, METHODOLOGY, voice plan, FAQ, concept cards.
- **Manuscript:** App N how-to-read + Backtests section rewrite; W-17 row; Ch.42 pointer; Safety-Case Readings Linux lead.
- **Sync:** `npm run sync:experiments`, `sync:concepts`; `check-experiments.mjs` OK; `lake build` OK (`BacktestC2Instance`).
- **Cleanup:** plan cross-refs, audit-telemetry, experiments/TODO, FINDINGS header, collector protocol paths, User-Agent strings.

## Decisions
- **Keep:** `W-*` IDs, formal “witness fields” in ch31/ch48, frozen RELEASE_NOTES v1.6.0 wording, archive session logs.
- **Drop:** all `/witness/` and `/witness-tests/` URL aliases (hard break).
- **Front door:** “A backtest here is a frozen safety check run on a history we did not write.”

## Follow-up (same session)
- `bridgeHooks` kept as the YAML key (catalog of named leaves). First-contact copy now states **project value**: backtests pay the remainder an authored simulation cannot; Construction stays out of v1 until a real stop exists on a foreign history. Touched: `experiments.yml` purpose/overview, App N how-to-read + synthesis lead, `/experiments/` hub lede, homepage tile order, README, FAQ, methodology card, `docs/EXPERIMENTS.md`, Ch.42 one sentence.

## Open / next
- Site `search-index.json` / `book-stats.md` refresh on next full site build or stats regen.
- Optional: add a one-line redirect note in v1.7 release notes when tagging (old URLs intentionally broken).
