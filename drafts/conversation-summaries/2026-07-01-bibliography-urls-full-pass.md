# 2026-07-01 — Bibliography URLs full pass

## Trigger
User approved the doi/url convention from a ~10% pilot and asked to apply it to all references; later requested DOI/URL in the PDF bibliography appendix; end-of-session commit.

## Done
- Enriched all seven `references/*.bib` files: bare `doi`, canonical `url`, arXiv fields where applicable; migrated `\url{...}` out of `howpublished`.
- Added `scripts/enrich_bibliography_urls.py` (Crossref + publisher landing heuristics) and `scripts/fix_bib_urls_final.py` (manual fixes + internal cleanup).
- Added `scripts/apply_bib_patches.py` for curated subagent/manual patches.
- Removed Crossref title-search pollution on internal `zarncke*` techreports; only `zarncke2025attractor` and `zarncke2025uad` retain public doi/url.
- Fixed wrong DOIs/URLs: `yeung2017hypernudge`, `gsn2021standard`, `euaiact2024`, `HenrichGilWhite2001`, `gruber2022curiosity`, `nakano2021`, `salgepolani2014`, `Dennett1991`, `Singer2011`, `schwartz2012refining`, etc.
- **PDF bibliography:** `book.tex` loads `hyperref` after `biblatex` with `doi/url/eprint=true`; `metadata/preamble.tex` appends DOI/eprint/URL at `\finentry` (global bibliography + chapter reference lists).
- `make check` and `biber book` pass; zero `doi.org` entries in `url` fields.

## Decisions
- Internal AE Studio sources without public pages stay without doi/url (19 entries).
- `dennett1981true` (Oxford incollection) left without link — no stable canonical page.
- Enrichment script skips Crossref search for `internal-project-sources.bib` keys except public allowlist (`zarncke2025attractor`, `zarncke2025uad`).

## Open / next
- Metadata mismatches flagged in pilot still need author review: `bonneaud2022coevolutionary`, `iadecola2023vascular`, `ramstead2022bayesian`.
- `gruber2022curiosity` citation key still says 2022 but entry now matches 2016 Neuron paper (title-aligned).
- Untracked in working tree (not this commit): `site/`, `serve-site.sh`, `.github/workflows/site.yml`, `metadata/TODO.md` site section, astro session log.

## Key paths
- `references/*.bib`, `references/README.md`
- `book.tex`, `metadata/preamble.tex`
- `scripts/enrich_bibliography_urls.py`, `scripts/fix_bib_urls_final.py`, `scripts/apply_bib_patches.py`

## Commits
- (filled after commit)
