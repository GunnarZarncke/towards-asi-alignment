# 2026-07-19 — Bibliography hallucination audit

## Trigger
User flagged four confabulated or inconsistent bibliography entries that survived into v1.0.0 (`dalrymple2024gsai`, `orseau2016interruptible`, `variationalagent2025`, `kuhn2025humanism`).

## Done
- **`dalrymple2024gsai`**: Replaced hallucinated "Garrabrant–Stiennon Alignment Intelligence (GSAI)" title and GovAI URL with arXiv:2405.06624 (*Towards Guaranteed Safe AI*); updated `\bibsummary` and `scripts/apply_bib_patches.py`.
- **`orseau2016interruptible`**: Removed fabricated arXiv DOI; changed to `@inproceedings` with UAI 2016 metadata (DOI `10.5555/3020948.3021006`, ML Anthology URL).
- **`variationalagent2025`**: Removed uncited entry (Anonymous/OpenReview mashup of unrelated IJCAI 2025 paper 538) from `dynamical-systems.bib`, summaries, and `fix_bib_urls_final.py`.
- **`kuhn2025humanism`**: Corrected title to *Humanism: An Obituary* and URL to human-readable Substack slug; synced philosopher reading path link.
- `python3 scripts/check_bibliography_summaries.py` passes (413 keys).

## Decisions
- Deleted `variationalagent2025` rather than repairing it: zero manuscript/Lean cites; metadata was a title/author/venue mashup with no project role.
- Kept citation key `dalrymple2024gsai` unchanged so chapter/Lean cites need no edits.

## Open / next
- Full bibliography audit beyond these four keys (user noted 230k AI-drafted words in three weeks).
- Rebuild PDF if bibliography display in references section should reflect fixes in a release artifact.

## Key paths
- `references/manuscript-citations.bib` (`dalrymple2024gsai`, `orseau2016interruptible`)
- `references/philosophy.bib` (`kuhn2025humanism`)
- `references/bibliography-summaries.tex`
- `scripts/apply_bib_patches.py`

## Commits
- (none — user did not request commit)
