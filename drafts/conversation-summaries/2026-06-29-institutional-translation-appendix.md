# 2026-06-29 — Institutional translation appendix (full session)

## Trigger

User asked to map the book's alignment concepts to human institutional analogues as a translation aid for policy makers, regulators, funders, and social scientists—not load-bearing argument. Work evolved from draft crosswalk → full LaTeX appendix → navigation wiring → editorial passes → partial bibliography pass.

## Done

- **Draft seed:** `drafts/institutional-alignment-crosswalk.md` (not in PDF).
- **Appendix:** `appendices/appJ-institutional-translation.tex` — translation guide with compact table up front, terminology discipline inline, trimmed back-projection section, forward/back projection, `refsection`, and chapter-style `\section*{Appendix References}` at end.
- **Book wiring (prior commit):** `book.tex`, `scripts/check_structure.py`, `README.md`, navigation cross-links in frontmatter and ch02/ch05/ch25b/ch27/ch35b, `appBridge-crosswalk.tex`.
- **Bibliography pass (partial):** 16 entries added to `references/governance-institutions.bib` (capture, certification, antitrust, beneficial ownership, EIA/NEPA, VW defeat-device, NIST/EU AI Act/ISO 42001, Fuller rule-of-law); inline `\autocite{}` throughout appendix; `metadata/global-nocite.tex` regenerated.
- **Removed from appendix body:** Terms to Decompose (integrated inline), Open Source Gaps (→ `metadata/TODO.md`), standalone Institutional Source Literature section (→ chapter-style Appendix References block at end).

## Decisions

- Appendix is **translation guide only**, not core argument.
- Institutional analogies are **baselines and mechanisms**, not proof institutions solve alignment.
- Broad policy words must decompose to correctors, handles, timing, bearers, or selection levers.
- Literature orientation belongs in **Appendix References** (chapter pattern), not a mid-appendix review section.

## Open / next

- [ ] Deeper sector-specific empirics in appendix cites (consent-decree effectiveness, coordinated-effects empirics, incident-reporting comparisons) — see partial note in `metadata/TODO.md`.
- [ ] Appendix renumbering / filename↔letter sync (pre-existing global issue).

## Key paths

- `appendices/appJ-institutional-translation.tex`
- `references/governance-institutions.bib`
- `metadata/TODO.md`
- `drafts/institutional-alignment-crosswalk.md`

## Verification

- `make check` passed after bibliography and references-block edits.
- `./build.sh` passed after bibliography pass (1189 pages).

## Commits

- `1f57fbc` Add institutional translation appendix for policy-adjacent readers.
- (this session) bibliography pass + Appendix References restructuring.
