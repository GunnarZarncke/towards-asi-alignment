# 2026-06-18 — Deep research citation inserts

## Trigger
User asked for surgical reference inserts in drafted chapters and TODO blocks for stub chapters, from deep-research report / source-canon bibliography candidates.

## Done
- Added 16 BibTeX entries: `external-alignment.bib` (biehl2020, scholkopf2021, strouse2016, kolchinsky2017, baker2009, ramachandran2007, casper2023, komanduru2019, deblanc2011, everitt2016, manheim2018, wang2013); `neuroscience-values.bib` (panksepp1998); `philosophy.bib` (olson2023); `governance-institutions.bib` (unesco2021, seoul2024, iaisr2025).
- Drafted chapters: prose + Chapter References updates in ch03, ch04, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch40.
- Stub chapters ch05, ch14–ch44 (except ch40): `% TODO(deep-research)` blocks in Chapter References with primary cite keys.
- ch13: deferred TODO note (content in ch12).
- `./build.sh` succeeds after biber pass.

## Open / next
- Wire TODO stubs when each chapter is drafted.
- Part III renumbering still pending.

## Key paths
- `references/external-alignment.bib`, `references/governance-institutions.bib`
- `chapters/ch03`–`ch12`, `ch40`; stub `ch05`, `ch14`–`ch44`
