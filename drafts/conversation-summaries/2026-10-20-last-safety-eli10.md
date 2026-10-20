# 2026-10-20 — Last Safety ELI10

kind: new-work
uptake: status

## Trigger
Add an ELI10 control that simplifies the last NPC reply or the current document; prepared text for documents and standard engine sentences; LLM for model-phrased replies. Then make it a phone setting, off by default.

Prompts: (paraphrase-only — no prompt id in transcript)

## Done
- content: `POST /api/eli10`, `lib/eli10.mjs`, prepared `content/eli10/` (facts + document sidecars), `explainLikeTen` in `lib/llm.mjs` (720 output tokens).
- content: Room HUD panel + phone file viewer button; session `eli10Enabled` synced via Settings (`applyPhoneSettings`); API 403 when off.
- content: NPC conversation rows store `template` for prepared vs LLM detection; tests in `tests/eli10.test.mjs`.
- content: Contract and `spec/terminal.md` updated.
- bookkeeping: Session log; HANDOFF/INDEX.

## Decisions
- ELI10 is opt-in like concept links (Lab Access Settings), not always-visible HUD chrome.
- Server gates `/api/eli10` on `eli10Enabled`; resolver itself unchanged for unit tests.

## Open / next
- Hand-polish `content/eli10/documents/*.md` (auto stubs except shutdown report).
- Optional: replay save events for `eli10Enabled` in import tests.

## Key paths
- `game/the-last-safety-review/lib/eli10.mjs`
- `game/the-last-safety-review/content/eli10/`
- `game/the-last-safety-review/public/terminal/project.mjs` (setting row)

## Commits
- `96188a63e` Add optional ELI10 simplifications to Last Safety Review.

## Verification
- `cd game/the-last-safety-review && npm test` → `ℹ pass 161` `ℹ fail 0` (2026-10-20).
