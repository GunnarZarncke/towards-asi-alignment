# 2026-11-02 — Self-audit instruments (§3.1, §3.8, §3.16)

kind: housekeeping
uptake: rule

## Trigger
Calibrate touch-rate and monthly review after October self-audit; build missing audit scripts; author scored November packet; end-of-session commit.
Prompts: paraphrase-only

## Done
- bookkeeping: `scripts/audit_authbar_series.py` — load-bearing authbar word share; stop below 2% when October volume gate met. Run: `.venv/bin/python scripts/audit_authbar_series.py --month 2026-10` → gz_touched_share 0.0521, exit 0. Output: `edit-attribution/authbar-series-2026-11-02.csv`.
- bookkeeping: `scripts/audit_parasite_budget.py` — weekly content vs bookkeeping from session logs; stop >40% for 3 ISO weeks. Run: `.venv/bin/python scripts/audit_parasite_budget.py` → exit 0 (W40–W43 ~21–30%; W45 partial 73%). Output: `parasite-budget-2026-11-02.csv`.
- bookkeeping: §3.16 `scripts/monthly_review_packet.py`, `scripts/score_monthly_review.py`, `monthly-review/README.md`, November packet and tops JSON. Excerpt order shuffled; four label lines per excerpt (author deletes all but one).
- bookkeeping: Author scored `monthly-review/2026-11.md`. `.venv/bin/python scripts/score_monthly_review.py drafts/project/self-audit/monthly-review/2026-11.md` → exit 1; top 3/4; miss E1 (`chapters/ch15-values-compressed-control.tex`, said RANDOM, true TOP_OLD).
- bookkeeping: `drafts/plans/tsa-on-itself.md` — §3.1/§3.8/§3.16 stops, checklist, monthly companion sync note (`sync:chapters` + `sync:chapter-cards` when manuscript changed).
- bookkeeping: Local companion sync after Ch. 1 ship gap: `cd site && npm run sync:chapters && npm run sync:chapter-cards && npm run sync:book` (gitignored book output).

## Decisions
- No live-tree error seeding; §3.16 packet only.
- `make check` (exit 0) does not verify gitignored chapter HTML; manuscript→site sync stays an explicit monthly step.

## Open / next
- **§3.16 stop:** human pass on `chapters/ch15-values-compressed-control.tex` before the next feature lane.
- **Ch. 7** vs Ch. 1 stopping rule (unchanged).
- After manuscript commits, log companion sync in the self-audit month when site-visible.

## Key paths
- `drafts/plans/tsa-on-itself.md`
- `scripts/audit_authbar_series.py`, `scripts/audit_parasite_budget.py`, `scripts/monthly_review_packet.py`, `scripts/score_monthly_review.py`
- `drafts/project/self-audit/monthly-review/2026-11.md`

## Commits
- `8181b24a97` — Add self-audit instruments: authbar share, parasite budget, monthly review.
