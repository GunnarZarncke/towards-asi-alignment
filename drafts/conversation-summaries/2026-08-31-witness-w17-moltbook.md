# Session log — Witness W-17 Moltbook MB7a scored

**Date:** 2026-08-31 / 2026-09-01 (interpretation + commit)  
**Scope:** Implement witness-v2 Phase 1 Moltbook plan — cache corpus, collect, check, record W-17; interpret; commit.

## Done

- Cached jscmp4/Moltbook 2026-07-03 → `experiments/witness/data/moltbook/` (gitignored).
- Implemented `fetch_h7_moltbook_cache.py`, `collect_h7_moltbook_mb7a.py` (chunked), `check_h7_moltbook_mb7a.py`.
- Scored fixture `fixtures/h7-moltbook-mb7a-v1.json`; checker PASS.
- **Outcome:** `structure_stop` — Tier A joined, Jan-31 coactive, not merged on `E_agent`; 100% broadcast on Jan 31, no thread edge.
- Recorded **W-17** in `results/FINDINGS.md` with interpretation paragraph (Jiang/Li/Nagli attribution vs discursive instrument).
- Updated witness plans, README, `metadata/TODO.md`, `experiments.yml`, `experiments-witness-tests.yml` (w-17 card).
- HANDOFF + INDEX updated.

## Preregistration crosswalk

| # | Prediction | Result |
|---|------------|--------|
| 1 | Tier A merge uncertain | Not merged; structure_stop blocks fail |
| 2 | E_thread-only / broadcast → structure_stop allowed | Yes |
| 3 | MBC-20 → structure type 5 | 1,038,375 posts |
| 4 | coalition_node_* informative | 167 agents |
| 5 | Random pairs mostly unmerged | diagnostic rate 0.0 |
| 6 | Claim vs boundary gap informative | no claim keywords in Tier A posts |

## Interpretation (load-bearing)

- Jiang et al. **same-operator** claim for Hackerclaw/thehackerman rests on **campaign copy + burst timing**, not reply-graph merge — aligned with Li duplicate-title / CoV human-influence typing.
- **Human owner** is outside the jscmp4 public pin; Nagli/Wiz `owners` join existed briefly via Supabase exposure, not in scored export.
- W-17 paid read: **reply-graph MB7a is the wrong access model** for this coordination class; structure_stop is correct, not instrument broken.
- Next honest leaves: MB6 time series, duplicate-title/sync measurand, ET-5 passive UAD annex — not retune `specificity_ratio`.

## Not in this commit

- Site sync build for w-17 card (metadata entry present; run site build separately).
- Optional MB6 second leaf; ET-5 UAD annex.
- Unrelated working-tree drafts (alignment-crux-map, conversation archive moves, site chapter graph).

## Resume

- `./serve-site.sh` or site build to publish w-17 card.
- Optional Phase 1 follow-ups per `witness-v2-moltbook-inventory.md` step 3.
