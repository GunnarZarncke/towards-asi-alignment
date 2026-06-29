# 2026-06-29 — Institutional translation appendix (full session)

## Trigger

User asked to map the book's alignment concepts to human institutional analogues as a translation aid for policy makers, regulators, funders, and social scientists—not load-bearing argument. Work evolved from a structured draft crosswalk into a full LaTeX appendix, then navigation wiring, PDF build, and several editorial passes on structure and terminology.

## Done

- **Draft seed:** `drafts/institutional-alignment-crosswalk.md` (not in PDF; source for appendix expansion).
- **Appendix:** `appendices/appJ-institutional-translation.tex` — full prose translation guide (boundaries, capability, bundles, bearers, goal transport, correction/CCI, false consent, successors, attractors, conductive artifacts, adversarial measurement, inferential coupling, grounding conservativity, interface/amendment matrix, weaker→stronger correction, back/forward projection).
- **Book wiring:** `\input` in `book.tex` after `appBridge-crosswalk.tex`; `scripts/check_structure.py` `APPENDIX_COUNT = 11`; `README.md` updated (11 appendices, reading paths).
- **Citation:** `yudkowsky2017inadequate` (*Inadequate Equilibria*) on institutional-failure sentence in appendix opening.
- **Navigation links** to Appendix J (`appj-institutional-translation`):
  - `frontmatter/preface.tex` (audience + appendices list)
  - `frontmatter/executive-overview.tex` (Navigation)
  - `frontmatter/introduction.tex` (institutional claim + How to Read)
  - `appendices/appBridge-crosswalk.tex` (companion pointer)
  - `chapters/ch02-artificial-civilization.tex`, `ch05-assumptions-scope-failure-coverage.tex`, `ch25b-correction-channels-adversarial-pressure.tex` (`sec:institutional-correction`), `ch27-manipulation-false-consent.tex`, `ch35b-conductive-artifacts-pivotal-processes.tex` (funders + regulators)
  - Appendix J opening back-links to Ch. 2, 25b, 35b, Preface
- **PDF:** `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh` succeeded mid-session (`dist/pdf/towards-superintelligence-alignment.pdf`). Later editorial edits not rebuilt in this session.
- **Structure edits (appendix):**
  - Moved **Compact Translation Table** to immediately after *How to Read the Institutional Analogy* (before baselines).
  - Trimmed **What AI Alignment Can Learn from Institutions** to three under-weighted lessons only (corrector bandwidth; opacity that protects dissent; patchwork jurisdiction as selection). Removed redundant bullets already covered by CCI / civilizational loop chapters.
  - Removed **Terms to Decompose** section; added **Terminology discipline** paragraph under *How to Read* and decomposed loaded policy words inline (oversight, accountability, ethics, transparency, governance, trust, rule of law; legitimation vs vague “legitimacy”; checkbox/fake/proxy compliance variants).
  - Removed **Open Source Gaps** section from appendix body; consolidated into expanded **Institutional translation appendix bibliography pass** in `metadata/TODO.md`.

## Decisions

- Appendix is **translation guide only**, not part of the core argument or a new chapter.
- Audience: policy-adjacent, institutional, funder-facing readers; technical detail points back to chapters and bridge crosswalk.
- Institutional analogies are **baselines and mechanisms**, not proof that institutions solve alignment.
- Grounding conservativity remains the **weakest** institutional analogue.
- Value bundles / bearer maps stay subordinate to **legitimation process**, not democratic replacement.
- Broad policy vocabulary must name a mechanism (corrector, handle, timing, bearer, selection lever)—no standalone decompose table at end.
- Source/bibliography gaps belong in `metadata/TODO.md`, not in appendix prose.

## Open / next

- [ ] **Bibliography pass** — `metadata/TODO.md` item *Institutional translation appendix bibliography pass* (antitrust, EIA/disclosure, consent decrees/capture, AI policy instruments, legitimation literature). Keep institutional-implement claims narrow until done.
- [ ] **Rebuild PDF** after latest appendix edits if a fresh artifact is needed.
- [ ] **Appendix renumbering / filename↔letter sync** — pre-existing global issue (`metadata/TODO.md`); appJ inserted by filename after bridge crosswalk, not by letter.
- No git commit this session (user did not request).

## Key paths

- `appendices/appJ-institutional-translation.tex` — main deliverable
- `drafts/institutional-alignment-crosswalk.md` — seed draft
- `appendices/appBridge-crosswalk.tex` — companion appendix
- `book.tex`, `README.md`, `metadata/TODO.md`, `scripts/check_structure.py`
- Navigation touchpoints: `frontmatter/preface.tex`, `frontmatter/introduction.tex`, `frontmatter/executive-overview.tex`, `chapters/ch02`, `ch05`, `ch25b`, `ch27`, `ch35b`
- `references/manuscript-citations.bib` — Yudkowsky entry

## Verification

- `make check` passed after all edits (structure + citations).
- Full `./build.sh` passed once mid-session; not re-run after final terminology/source-gaps edits.

## Commits

- None.
