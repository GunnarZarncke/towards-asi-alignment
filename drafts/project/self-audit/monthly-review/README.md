# Monthly section-vintage review

Packet for [`tsa-on-itself.md`](../../../plans/tsa-on-itself.md) §3.16. Each excerpt is either the working-tree text or an older git version. **Excerpt order is shuffled** (`E1`, `E2`, … does not mark priority). Under each excerpt, all four labels are listed; you delete all but the one that fits. Only `TOP` / `TOP_OLD` correctness fires the stop.

1. Rank priority files (Opus 5.5, medium) from TODOs, HANDOFF, and the latest blind-status results. Do not read chapter or card bodies. Save `{ "picks": [ { "path", "heading", "reason" } ] }`.
2. Generate: `.venv/bin/python scripts/monthly_review_packet.py --month YYYY-MM --tops <picks.json>`
3. In `YYYY-MM.md`, under each excerpt, delete every label line except the one you mean (`TOP`, `TOP_OLD`, `RANDOM`, or `RANDOM_OLD`).
4. Score: `.venv/bin/python scripts/score_monthly_review.py drafts/project/self-audit/monthly-review/YYYY-MM.md`

`YYYY-MM.key.json` is the answer sheet. Scoring before exactly one label remains on each priority excerpt exits 2 and does not print answers. A wrong priority label exits 1: human pass on the named paths before the next feature lane.

The same path is never both current and old. Nothing here is written into the manuscript or the site.
