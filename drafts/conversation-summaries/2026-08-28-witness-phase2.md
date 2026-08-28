# 2026-08-28 — Witness Phase 2

## Trigger
User asked to continue Phase 2, then pushed back that catalogs lacked parent-plan fields, then: **Do the richer sources.**

## Done
- Downloaded Zenodo `bfc_bic.csv` + Perceval `linux-commits-2023-11-12.json.gz` (563 MB), SNAP `wiki-RfA.txt.gz`, wiki-socks clone, linux-6.1.y shallow.
- Joined `Reviewed-by` onto BIC SHAs: **17047/60176**.
- Pinned C-005 episode: cpufreq merge → revert → same-title re-entry (kernel.org patches).
- Pinned C-006 episode: `-stable` `f8a07021679a` vs upstream `42c5ca1f0a28` (`event_sched_out` arity).
- SNAP+MediaWiki API: 2012 passed RfAs with oppose (\(n=21\)).
- BetacommandBot BRFA→flag/block. wiki-socks stats.
- Protocols `h2-v1.2.0` / `h3-v1.1.0`. Checkers pass. Raw data gitignored.

## Decisions
- C-004a fail is `Reviewed-by`×BIC, not merge-count.
- C-005 fail is one revert/re-entry triple, not a lore NAK census.
- C-006 fail is hunk identity, not a seven-tag \(\kappa\).
- H3 causal RfA stays refuse (no control). C-006 bots is fail.
- Exp. 3 still refuse (`Reviewed-by` / SPI).
- Did not fetch 3.3 GB tarball, KernelCI, or lore mboxes.

## Open / next
- Phase 3: H4 leaderboards + WVS/Moral Machine/RLHF.
- Optional: KernelCI on BIC SHAs; lore NAK; zero-oppose RfA control.

## Key paths
- `drafts/plans/witness-phase2.md`
- `experiments/witness/fixtures/h2-linux-v1.json`
- `experiments/witness/fixtures/h3-wikipedia-v1.json`
- `experiments/witness/data/README.md`

## Commits
- none
