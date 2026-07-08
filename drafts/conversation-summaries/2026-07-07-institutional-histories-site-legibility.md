# 2026-07-07 — Institutional histories site legibility pass

## Trigger

Follow-up on Appendix M companion-site work: rewrite the overview hub and all eleven case-study cards for non-technical readers (generalists, philosophers, historians, funders, policy makers); link each card to the full appendix; document the appendix in README and other entry points; commit at session end.

## Done

- **Overview hub** (`sync-chapter-cards.mjs`): expanded `bodyExtra` for `appM` — concrete historical prose, no mechanism jargon (commit `564d73a`).
- **Eleven case cards** (`site/src/content/cards/institutional-*.md`): ~2× body length each; jargon unpacked; AI-governance payoff in plain language; footer linking to overview hub and `/full/` on every card.
- **Docs:** README (audience paths, PDF/site reading order, appendix count 8), `docs/MANUSCRIPT.md`, `CONTRIBUTING.md`, `AGENTS.md`, `site/README.md`, `RELEASE_NOTES.md` (unreleased section), `frontmatter/preface.tex`.
- Session log + commit (see Commits).

## Decisions

- Card frontmatter summaries/decision/evidence callouts left unchanged; expansion is in markdown body only so sidebar and index blurbs stay scannable.
- Footer uses relative links (`../chapters/appm/`, `../chapters/appm/full/`) so they resolve from any card URL depth.
- Lab-simulation LLM discovery work left unstaged (separate line of work).

## Open / next

- None for this site pass unless user wants card summaries also rewritten for length/tone.

## Key paths

- `site/src/content/cards/institutional-*.md`
- `site/scripts/sync-chapter-cards.mjs`
- `README.md`, `docs/MANUSCRIPT.md`, `frontmatter/preface.tex`

## Commits

- `564d73a` Rewrite Appendix M overview for non-technical readers.
- `7cf1030` Expand institutional history site cards for generalist readers.
