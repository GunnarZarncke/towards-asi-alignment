# 2026-11-04 — Control phrases read backward

kind: correction
uptake: local

## Trigger
The Chapter 25 sentences on button-press, missed alerts, and a mission frame were hard to read. The institutional translation belongs in Appendix C, in the usual direction: book term, then institutional name. No reverse section.
Prompts: paraphrase-only (no resolvable prompt id).

## Done
- content: Chapter 25, `sec:human-fallibility-conventions`, shortened. Alert-fatigue rules are deliberation, authority, and a late correction, in ordinary words.
- content: Appendix C correction section names the institutional forms: person in the loop, stop switch, mission limit, named responsible person, watch limit and alert budget, practice with the system off, review after the event. Latency row of the CCI table includes watch limits. Manipulation section includes a tired supervisor the system gains from. The reverse section was removed.
- bookkeeping: Bib entries and summaries for the new keys. `check_bibliography_summaries.py` passed (573 summaries for 573 bib keys). Deleted `drafts/institutional-control-translation.md`.

## Decisions
- Same direction as the rest of Appendix C. No phrase-first table.
- ISO/IEC 42105 is cited as a final draft under publication, not as a finished standard.

## Open / next
- Author pass on the new appendix section and the shortened chapter paragraphs.

## Key paths
- `chapters/ch25-correction-causal-channel.tex` (`sec:human-fallibility-conventions`)
- `appendices/appC-institutional-translation.tex` (`sec:institutional-correction-and-cci`)

## Commits
- Map weapons and oversight control language onto the correction channel (`git log -1 --oneline` on main after session close).
