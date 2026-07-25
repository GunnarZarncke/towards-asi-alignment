# 2026-07-25 — Field news (Tier A/B + HF entity framing)

## Trigger
Implement Tier A and selected Tier B AI-safety incident catalog items on manuscript + companion site; rewrite OpenAI/Hugging Face news with entity-discovery / UAD framing; commit at session end.

## Done
- **Site infrastructure:** `metadata/field-news.yml`, nine body files, `site/scripts/sync-field-news.mjs`, `/news/` index, chapter-card “Related news” sidebar, nav links, `"news"` card type, `.gitignore` for generated cards/JSON.
- **Tier A (6):** OpenAI HF hack, long-horizon sandbox, AISI cheating, METR Frontier Risk, Mythos withheld, accidental CoT opt — site + surgical `\autocite{}` in ch11–43 and appB.
- **Tier B (4):** CLTR + Claude Code cluster (site only); METR Anthropic red-team (ch42); OpenClaw (site + ch26).
- **HF card rewrite:** entity-attribution problem, OpenAI/HF lateral-movement quotes, UAD + graded-lab-simulation link, Zvi scope limit; ch07 added to chapter routing.
- **Bibliography:** ten new 2026 keys + summaries (427 total, check passed).
- **Commit:** (this session).

## Decisions
- Generated news cards stay gitignored; CI runs `sync:field-news --check`.
- Concept-logo site work left unstaged (parallel WIP in working tree).
- Claude Code cluster = one aggregated anecdote card, not per-issue cards.

## Open / next
- Remaining Tier B (MonitoringBench, GPT-Red, Meta Sev-1, GRP-Obliteration, policy cluster) not in scope.
- Run `cd site && npm run sync` before deploy (search index).
- Optional: align ch14 manuscript cite with expanded HF news framing.

## Key paths
- `metadata/field-news.yml`, `metadata/field-news/bodies/openai-huggingface-jul-2026.md`
- `site/src/pages/news/index.astro`, `site/scripts/sync-field-news.mjs`
- `chapters/ch42-safety-case.tex`, `chapters/ch26-correction-channel-integrity.tex`

## Commits
- (filled after commit)
