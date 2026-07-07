# 2026-07-07 — Institutional genesis, memory, and decay appendix

## Trigger

User wanted to apply the book's alignment framework to historical instances of institutional alignment: how correction mechanisms are founded, stabilize, and fail, to surface genesis routes and new failure modes for AI governance. Discussion (in-chat, no repo changes) covered: candidate historical cases (aviation, pharma, finance, constitutional government, Rome vs. Venice, nuclear, insurance/audit); a memory-decay framing tied to the book's human value-update operator \(U_H\) and its time constant; who-audits-the-auditors (resolved as re-grounding in a different incentive basin or a mutually-auditing cycle, not a vertical tower); non-catastrophic genesis routes (insurance, chronic threat, dispute resolution, GPL/copyleft); and dual-mandate genesis as the most consequential failure mode for present-day AI regulation. User then asked, in order: (1) look up references for the cases into a new bib file, (2) write the new appendix sections using those references, (3) adapt existing chapters/appendices to cross-reference it.

## Done

- Created `references/institutional-histories.bib` (24 new entries: Vaughan/Challenger, Mazuzan & Walker/AEC-NRC, Kingston/Lloyd's, Kelty and Weber/free software, FSF GPLv3, Preuss/Art. 79(3), Evans/Enabling Act, Reason/aviation safety culture, Carpenter/FDA history, Herkert et al./737 MAX, FCIC report, White/rating agencies, Kroszner & Strahan/bank deregulation, Coffee/gatekeepers, Keaveney and Gruen/Rome, Lane and Finlay/Venice, TeBrake/Dutch water boards, Russell/IETF, Woodward/canonization).
- Added all 24 `\bibsummary` lines to `references/bibliography-summaries.tex` in correct alphabetical order; `scripts/check_bibliography_summaries.py` passes (399/399).
- Wrote `appendices/appM-institutional-histories.tex` ("Institutional Genesis, Memory, and Decay: Historical Case Studies"), mechanism-led sections in life-cycle order: genesis from money at risk (Lloyd's) → catastrophe ratchet (FDA, aviation) → chronic self-refreshing threat (Dutch water boards, IETF) → evidence before authority (NTSB/ASRS) → selection gating (airworthiness + insurance, INPO) → constraint inheritance across successors (GPL, with the tivoization/v3-fork and distribution-ontology-drift failures) → memory refresh through succession (Venice's *promissione*, the \(U_H\)-time-constant argument, *advocatus diaboli*, the ritual-vs-refresh discriminator) → entrenchment and the corrigibility paradox (Weimar Enabling Act → Art. 79(3) Ewigkeitsklausel) → failure: reform decay (Glass-Steagall → 2008) → failure: dual-mandate genesis (AEC→NRC, Arthur Andersen→PCAOB, with the present-day AI-governance map: lab self-evaluation, safety institutes inside promotion ministries, standards delegation, negotiated evaluator access, sovereign-AI conflicts) → failure: capability jump outruns correction latency (Marian reforms, Caesar) → summary table + three open research questions (CCI decay/refresh model, enforcement-lever inventory for constraint inheritance, entrenchment-coordinate/guardian-regress).
- Wired the appendix into `book.tex` (`\addbibresource` + `\input`, placed directly after Appendix C — landed as Appendix D at build time).
- Added cross-reference pointers (surgical, few sentences each): Appendix C intro pointer + expanded "How Weaker Correction Systems Become Stronger" section (reform decay / dual-mandate warnings); Chapter 27 institutional-correction section; Chapter 31 conserved-properties (GPL constraint-inheritance pointer); Chapter 34 selection-environment (dual-mandate genesis inserted at the existing repair-term equation \(R(a_t)-s_t\)); Chapter 37 attractor theory (ritual-vs-refresh test inserted into the compliance-attractor subsection).
- Bumped `APPENDIX_COUNT` from 12 to 13 in `scripts/check_structure.py`.
- Full `./build.sh` succeeds (1290 pages, zero undefined citations/references after adding the missing `\addbibresource` line). `make check` passes: structure, citations (202/399 keys cited), bibliography summaries (399/399) all green. `ReadLints` clean on all edited files.
- Committed all of the above (see Commits).

## Decisions

- New appendix placed as file `appM-institutional-histories.tex` but positioned via `\input` order right after `appC`, so it renders as Appendix D; existing appendix files D–L are not currently wired into `book.tex` at all (pre-existing, unrelated orphan state — left untouched, out of scope for this session).
- Appendix labels in this repo are already decoupled from filename letters (e.g. `appC-institutional-translation.tex` has `\label{appj-institutional-translation}`), so the new file's `\label{appm-institutional-histories}` does not need to match its position; this avoided any renumbering/relabeling risk to existing cross-references.
- Used only real, checkable historical/academic sources for the new bib entries (no invented DOIs/URLs where uncertain) — some entries omit a `doi` field where none was known with confidence.
- Kept the "who audits the auditors" resolution as re-grounding-in-a-different-incentive-basin or a mutually-auditing cycle (not a vertical tower), matching the existing \(D_{\mathrm{inst}}\) institutional-diversity term in ch27 rather than introducing new formal machinery.
- Cross-reference edits into existing chapters were deliberately minimal (1–3 sentences each) per AGENTS.md's surgical-changes rule; no adjacent prose was rewritten.

## Open / next

- Three research questions are flagged as open in the appendix's closing section but not developed further: a formal CCI decay/refresh time-dependence, an enforcement-lever inventory for AI successor constraint inheritance, and the entrenchment-coordinate/guardian-regress question. Any of these could become a fuller technical treatment (possibly back in Chapter 26/31) if the project wants to formalize them.
- Site sync (`site/src/content/book/`) was not updated for the new appendix — appC/appD/appF currently have site pages but appM does not yet. Out of scope unless requested.
- appD–appL orphan-appendix wiring gap (files exist, not `\input` in `book.tex`) noticed but left alone; flagging here in case it's an oversight worth a separate session.

## Key paths

- `appendices/appM-institutional-histories.tex` — the new appendix.
- `references/institutional-histories.bib`, `references/bibliography-summaries.tex` — new sources.
- `appendices/appC-institutional-translation.tex`, `chapters/ch27-correction-channels-adversarial-pressure.tex`, `chapters/ch31-conserved-properties.tex`, `chapters/ch34-selection-environment.tex`, `chapters/ch37-alignment-attractor.tex` — cross-reference edits.
- `book.tex`, `scripts/check_structure.py` — wiring and structure-count update.

## Commits

- `fceeb79` Add Appendix D: institutional genesis, memory, and decay case studies.
