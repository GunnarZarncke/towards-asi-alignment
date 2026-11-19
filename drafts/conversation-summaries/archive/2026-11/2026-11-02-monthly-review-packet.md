# 2026-11-02 — Monthly section-vintage packet

kind: new-work
uptake: rule

## Trigger
After dropping live-tree seeding, build the monthly review as a mixed packet: priority sections from an Opus medium pass over TODOs and heuristics, plus random manuscript and site sections, plus older git text. Score whether priority excerpts are current or old. Random excerpts stay informational.
Prompts: paraphrase-only

## Done
- bookkeeping: `scripts/monthly_review_packet.py` and `scripts/score_monthly_review.py`. Labels `TOP`, `TOP_OLD`, `RANDOM`, `RANDOM_OLD` sit on their own line. The key is a sibling JSON. Incomplete priority marks exit 2 and do not print vintages. A wrong priority vintage exits 1.
- bookkeeping: First packet `drafts/project/self-audit/monthly-review/2026-11.md` (807 words on the first build, 835 after the prose cleaner; six excerpts; four priority, of both vintages; one random current and one random old). Priority files ranked by [Opus medium](e0076af0-7e9f-415a-b5c9-5a2055e75f27) from the handoff, TODOs, and the 2026-11-02 blind-status lines, without opening chapter bodies. Picks: `2026-11.tops.json`.
- bookkeeping: Scorer checked on a throwaway copy: all-correct exits 0; one flipped priority mark exits 1. The review file in the repo still has its labels.
- bookkeeping: §3.1 stop in `drafts/plans/tsa-on-itself.md` set to a GZ-touched share under 2% on the load-bearing chapters, armed only when manuscript and tracked line totals are at least the October 2026 csv. §3.16 written into the plan, the monthly schedule, and the non-goals (no planted defects in the tree).

## Decisions
- No live-tree seeding. The packet is the whole instrument.
- The scored task is vintage (working tree vs earlier git), not comprehension and not a prose-quality screen.
- Old and current of one path are never both in the packet. A packet that cannot show both vintages among the priority excerpts is not generated.

## Open / next
- Superseded by author score and `2026-11-02-self-audit-instruments.md` (stop on ch15).

## Key paths
- `drafts/plans/tsa-on-itself.md` §3.1, §3.16
- `drafts/project/self-audit/monthly-review/README.md`
- `drafts/project/self-audit/monthly-review/2026-11.md`

## Commits
- See `2026-11-02-self-audit-instruments.md`.
