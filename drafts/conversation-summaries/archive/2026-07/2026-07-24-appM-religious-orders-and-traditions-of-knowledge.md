# 2026-07-24 — Appendix M: religious orders and traditions-of-knowledge citation

## Trigger

Reviewer feedback on Appendix M (Institutional Genesis, Memory, and Decay): why are religious orders stable, is this a special case of an existing case study or an overlooked gap, and should the appendix cite Samo Burja's LessWrong post "On the Loss and Preservation of Knowledge" (or its sources)?

## Done

- Read Appendix M (`appendices/appM-institutional-histories.tex`) in full and the uploaded Burja post to assess fit before writing anything.
- Researched and verified (web search, not memory) two separate evidence strands before drafting:
  - Religious-order stability: Rost, Inauen, Osterloh & Frey (2010), *Journal of Management History* — quantitative study of every Benedictine abbey in Bavaria/Baden-Württemberg/German-speaking Switzerland, ~500-year average lifespan, ~26.5% dissolved from internal problems; Cluny/Cîteaux reform cycles; Jesuit suppression (1773, *Dominus ac Redemptor*) and restoration (1814, *Sollicitudo omnium ecclesiarum*).
  - General traditions-of-knowledge phenomenon: Polanyi's tacit knowledge, Collins's TEA-laser replication study (labs failed to replicate from published specs alone), with Burja's post cited as the source of the living/dead/lost-tradition and "counterfeit understanding" vocabulary rather than as evidentiary support (it is an unrefereed, still-unpublished draft manuscript).
- Presented findings via `AskQuestion` before editing (placement options, citation scope, apply-now vs. draft-only); user chose: fold into Section M.7 (Memory Refresh Through Succession), ground the general point on Polanyi/Collins with Burja as the naming source, apply now.
- Edited `appendices/appM-institutional-histories.tex`:
  - Added a paragraph on religious orders as the same memory-refresh mechanism under non-hereditary succession (recruitment/novitiate as selection gate, Rule as portable constraint, Cluny/Cîteaux as endogenous reform), explicitly hedged with the Rost et al. finding and the Jesuit suppression as a caution against over-claiming.
  - Added a separate paragraph on the general tacit-knowledge / traditions-of-knowledge point (Polanyi, Collins), naming Burja as the framing/vocabulary source only.
  - Added "religious orders" to the Memory Refresh row of the mechanism-summary table (§M.11).
  - Extended the Appendix References closing paragraph to cite the four new sources.
- Added four bib entries to `references/institutional-histories.bib`: `rost2010benedictine`, `collins1974teaset`, `polanyi1966tacit`, `burja2018knowledge`, each with a `note` field.
- Added matching `\bibsummary{}` lines (alphabetically placed) to `references/bibliography-summaries.tex`.
- Ran `make check`: structure check, citation check (220 keys cited), and bibliography-summary check (417/417) all passed.

## Decisions

- Burja's post is cited as the source of useful vocabulary, not as historical evidence — the appendix's factual claims about knowledge transmission rest on Polanyi/Collins (peer-reviewed/established), consistent with this repo's prior bibliography-hallucination-audit concerns.
- Religious orders were treated as a compound case (memory refresh + constraint inheritance + selection gating), not a new mechanism, and folded into the existing M.7 section rather than given a dedicated section, per the appendix's "organized by mechanism, not by case" rule.
- Deliberately did not add a dedicated citation for the Jesuit suppression/restoration dates (1773/1814) inside the new paragraph — flagged to the user as an open item rather than silently leaving it uncited or inventing a source.

## Open / next

- User has not yet decided whether to add a dedicated source for the Jesuit suppression/restoration sentence or trim the specific dates from that sentence.
- The repo has many other unrelated uncommitted changes (site work, ET-2 experiment files, other drafts) predating this session; per AGENTS.md scope rules, only the three files this task touched were staged and committed.

## Key paths

- `appendices/appM-institutional-histories.tex` (Section M.7, §M.11 summary table, Appendix References)
- `references/institutional-histories.bib`
- `references/bibliography-summaries.tex`

## Commits

- (recorded after this log is written — see repo history for the exact hash)
