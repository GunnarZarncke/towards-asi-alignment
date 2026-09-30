# 2026-09-30 — Wiki quotes: authbar split, site render, PDF

kind: correction
uptake: local

## Trigger
Follow-up on applied LW wiki quotes: authbars must not cover `\wikiq`; remove redundant wiki attribution; fix site rendering and broken cite links; regen PDF/site; end-of-session commit.
Prompts: paraphrase-only (telemetry prompt ids not copied this turn).

## Done
- content: Split authbars around all `\wikiq` blocks (23 chapters); trimmed lead-ins so attribution is lead-in + single `\autocite` in quote footer (`metadata/preamble.tex`).
- content: Fixed ch06 orphan `\end{authbar}` from split script; updated `scripts/split_authbars_around_wikiq.py` to skip stale `\end{authbar}` after quotes.
- housekeeping: `scripts/generate_global_nocite.py` — include `\wikiq` keys, skip `#1`/`bibkey` placeholders (fixes PDF `\nocite{#1,...}` fatal).
- housekeeping: Site `\wikiq` → `<blockquote class="wiki-quote">` with HTML cite links (`site/scripts/lib/tex-convert.mjs`); corporate-author bib parse fix (`site/scripts/lib/bib-index.mjs`); `.wiki-quote` CSS on book pages.
- housekeeping: Utility scripts `scripts/fix_wikiq_leadins.py`, `scripts/split_authbars_around_wikiq.py`.
- bookkeeping: PDF rebuilt — `make check`-level verify: `./build.sh` → `Built dist/pdf/towards-superintelligence-alignment.pdf`; `npm run sync:chapters` in `site/`.

## Decisions
- Quote footer is `\autocite` only (no repeated tag name or “LessWrong wiki,” prefix); lead-in names the concept, not the wiki host.
- `\wikiq` lives outside authbar environments so margin bars do not span quotes.

## Open / next
- Author read: whether field wiki quotes still feel like imported authority after de-duplication.
- Site book markdown under `site/src/content/book/` is sync output — run `cd site && npm run build` before deploy if full static site needed.

## Key paths
- `metadata/preamble.tex` (`\wikiq`)
- `site/scripts/lib/tex-convert.mjs`
- `scripts/split_authbars_around_wikiq.py`

## Commits
- `61dc240c4` Fix wiki quote layout and site rendering after LW wiki apply.
