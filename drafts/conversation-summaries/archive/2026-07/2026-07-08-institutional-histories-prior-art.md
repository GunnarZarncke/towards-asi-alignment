# 2026-07-08 — Institutional histories prior-art integration

## Trigger
User asked whether institutional-design comparisons in Appendices C and M are novel, requested a literature survey (academic and blog), then asked to integrate prior-art references with wording that credits existing work—especially dual-mandate genesis, Roman Republic analogies, GPL/succession, and corrigibility/entrenchment—and to commit at session end.

## Done
- Researched prior art: Anderljung et al. 2023 (frontier licensing/insurance), Zaidi & Dafoe 2021 (Baruch/nuclear governance), Law & Ho 2023 (dual mandate), Miller 2025 (Roman/ASI precedents), Henderson & Lemley 2025 (AI licensing enforceability), Abiri 2025 (AI constitutions).
- Added six bib entries to `references/institutional-histories.bib` and matching `\bibsummary` lines.
- Updated `appendices/appM-institutional-histories.tex`: originality caveat in Purpose and Method; section-level credit for selection gating, GPL/successor inheritance, entrenchment/corrigibility, dual-mandate genesis, Roman capability-latency; expanded Appendix References paragraph.
- Updated `appendices/appC-institutional-translation.tex`: credit in attractor-control and weaker-to-stronger sections; expanded Appendix References paragraph.
- Rewrote the awkward "second caveat concerns originality" paragraph into three shorter sentences aligned with the section's caveat cadence.
- Verified `make check` and full `./build.sh` (1283 pages) green.

## Decisions
- Use `\textcite` for in-prose author attribution where the book names who already made the argument; keep `\autocite` in closing reference paragraphs.
- Credit prior art explicitly but state what this book adds: life-cycle mechanism frame, genesis-route typology, decay-and-refresh CCI reading, GPL as successor-inheritance case study, entrenchment-coordinate vs corrigibility paradox (distinct from Abiri's authorship-legitimacy question), capability-correction slack vs Miller's power-seeking reading of Roman material.
- Stage only this session's appendix/bibliography/log files for commit; leave unrelated lab-simulation and book.tex working-tree changes unstaged.

## Open / next
- Optional: add Henderson/Miller/Law citations to site Appendix M overview cards if funders read the hub before the PDF.
- Unrelated dirty tree: lab-simulation D2/LLM stress tests, `book.tex`, `metadata/toc-inline-sections.tex`, etc.—not part of this commit.

## Key paths
- `appendices/appM-institutional-histories.tex` — main prior-art integration
- `appendices/appC-institutional-translation.tex` — attractor/dual-mandate cross-refs
- `references/institutional-histories.bib` — six new keys

## Commits
- `65932af` Credit prior AI-governance literature in institutional appendices.
