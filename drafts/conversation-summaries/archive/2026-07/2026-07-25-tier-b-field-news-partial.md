# 2026-07-25 — Tier B field news (partial)

## Trigger
Implement selected Tier B items with user-specified surface split: CLTR and Claude Code cluster (site only); METR embedded red-team (ch42 only); Meta/Summer Yue OpenClaw (both).

## Done
- **Site:** three new roster entries in `metadata/field-news.yml` + bodies (`cltr-scheming-wild-mar-2026`, `meta-openclaw-feb-2026`, `claude-code-production-feb-2026`); sync now generates 9 cards.
- **Bibliography:** `cltr2026scheminginthewild`, `metr2026anthropicredteam`, `meta2026openclawincident`, `claudecode2026productioncluster` + summaries (427/427 check passed).
- **Manuscript:** ch42 adversarial-measurement bullet (`metr2026anthropicredteam`); ch26 OpenClaw compaction/STOP failure (`meta2026openclawincident`).
- **`.gitignore`:** three new generated card paths.

## Decisions
- METR embedded red-team is manuscript-only (Frontier Risk Report already has Tier A site card).
- Claude Code cluster is one aggregated `anecdote` card with representative GitHub issue links—not per-issue cards.
- OpenClaw cite uses trade-press URL with note that primary account was social media.

## Open / next
- Remaining Tier B items (MonitoringBench, GPT-Red, Meta Sev-1, GRP-Obliteration, policy cluster) not requested.
- Run `npm run sync` in `site/` before deploy to refresh search index.

## Key paths
- `metadata/field-news.yml`
- `chapters/ch42-safety-case.tex`, `chapters/ch26-correction-channel-integrity.tex`

## Commits
- (none)
