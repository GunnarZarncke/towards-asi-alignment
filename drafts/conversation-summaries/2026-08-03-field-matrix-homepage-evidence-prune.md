# 2026-08-03 — Field matrix homepage evidence prune

## Trigger
Reviewer feedback: matrix citations accurate but ~dozen cells use org landing pages as evidence; user agreed — remove generic entries, move org links to agenda cards, add concrete papers.

## Done (pass 1)
- Removed ev **12, 30, 32, 37, 44, 71**; added ev-150 (Orthogonal MB1).

## Done (pass 2)
- Removed ev **33, 34, 69, 72, 74, 75, 76**.
- Added matrix evidence: **151** Meinke scheming, **152** SAD, **153** Berglund situational awareness, **154** Dafoe Cooperative AI, **155–156** Monosemanticity papers.
- Agenda links updated: Apollo/Truthful, CLR (+ CAIF org link retained on card).

## Still open
- ~~Other root-URL cells (Resolution, FAR, AI 2027, etc.)~~ — **pass 3 done (2026-08-04):** all matrix-active root URLs replaced or removed (ev 138 dropped; 39–79, 108–130 sources tightened).

## Done (pass 3)
- Replaced homepage sources for ev **39, 40, 54, 58, 61, 64, 65, 77–79, 108, 115, 129, 130** with concrete essays, papers, reports, or deep links.
- Removed ev **138** (Zeroth homepage) from catalog and Safeguarded AI matrix cells (137–142 cover programme).
- **78** → FAR scalable-oversight paper (matrix type O→E); agenda cards enriched.
- `grep 'url: https://[^/]+/?$' evidence.yml` → **zero** root-URL sources remain.

## Key paths
- `reference/field-agendas/data/evidence.yml`
- `reference/field-agendas/data/matrix.yml`

## Commits
- `06cb17fe` Pass 1 + MB4a/MB7d bridge cards (prior session).
- (pending) Pass 3 — finish homepage evidence tightening.
