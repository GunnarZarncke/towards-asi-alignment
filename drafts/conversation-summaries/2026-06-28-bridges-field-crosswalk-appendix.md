# 2026-06-28 — Bridges ↔ field-cruxes crosswalk appendix

## Trigger
External reviewer feedback argued the book's bridges (`MB1`–`MB9`) are "ad-hoc names" that merely re-import the field's standing open problems and dissolve none. User accepted the critique's core and asked to (a) relate bridges to existing field cruxes via a crosswalk rather than ad-hoc names, (b) execute it as an **early appendix**, and (c) mention it in key sections including README and AGENTS.md.

## Done
- New appendix `appendices/appBridge-crosswalk.tex` ("Bridges and the Field: A Crosswalk", label `appbridge-crosswalk`):
  - `longtable` mapping each bridge (with A-ID + home chapter) → canonical field crux → owning agenda → book's move.
  - Per-bridge notes with `\autocite`s to the canonical field works (IRL non-identifiability, ELK, CIRL, off-switch anti-naturality, tiling, ontology identification, deceptive alignment, debate/amplification, AI Control, davidad GSAI, decision-theory/acausal).
  - Sections on what the book *shares* (dissolves none), the bridges with *no clean field analog* (`MB3` bearer maps, `MB6a/b` socio-technical selection, `MB7d` inferential coupling), and the *differentiator* (fixed dependency order + adversarial verifiability A-009 as the single chokepoint; falsifiable per appH / ch39b / ch40).
- Inserted `\input{appendices/appBridge-crosswalk}` in `book.tex` directly after `appA-notation` → renders as **Appendix B**.
- Mentions added: `README.md` (thesis section + status count 9→10 + repo map), `AGENTS.md` (Chapter work — Lean spine, new step 5), `REVIEWING_FOR_AGENTS.md` (Existing-Work Subsumptions intro + gem map), `INSTRUCTIONS.md` (two index tables made letter-agnostic + new crosswalk row), `formal/README.md` (bridges paragraph + spine appendix ref), `metadata/assumptions-ledger.md` (§IV).
- `scripts/check_structure.py`: `APPENDIX_COUNT` 9→10.
- `tables/assumptions-table.tex` (orphan, not `\input`): made its two appendix-letter literals letter-agnostic.
- Build green: `./build.sh` (1155 pp, exit 0), no undefined refs/citations; `make check` passes (structure + 132 cited keys).

## Decisions
- **Crosswalk, not rename.** Kept neutral `MB*` labels: field cruxes are not 1:1 with bridges (one crux spans several; `MB7` fans into a–d), and neutral labels avoid importing another agenda's ontology. Appendix supplies the translation. Rationale stated in the appendix intro.
- **Early placement = Appendix B** (after Notation). Per established repo precedent (`2026-06-25-remove-appendix-e-...`): filenames stay stable, appendix *letters* drift, `\ref` is label-based → no manuscript breakage. Confirmed the PDF has **zero** hardcoded appendix-letter literals (all `\ref`); only the unused `tables/assumptions-table.tex` fragment had letters.
- Made live-doc appendix references (INSTRUCTIONS, formal/README) **letter-agnostic** (by name) so future letter drift won't rot them. Did **not** edit dated historical logs / `review/*` plan snapshots that mention old letters.
- New appendix filename uses non-letter prefix `appBridge-` to avoid colliding with existing `appB-worked-example` and to signal it does not own a fixed letter.

## Open / next
- Letters after A now shift by one in the PDF (assumptions index, glossary, research program, Lean spine, etc.). Live canonical docs were updated/neutralized; older conversation-summary and `review/*.md` snapshots still quote pre-shift letters (intentionally left as historical record).
- Optional: extend the crosswalk if/when bib gains keys for obfuscated arguments (Barnes–Christiano), weak-to-strong (Burns), constitutional AI (Bai), shard theory — currently described in prose without `\cite` where no key exists.
- Optional: cross-link the crosswalk from ch40 (lethality stress test) and ch44 (closing synthesis) bodies.

## Key paths
- `appendices/appBridge-crosswalk.tex`, `book.tex`
- `metadata/assumptions-ledger.md` §IV (bridge ↔ A-ID map), `appendices/appH-research-program.tex` (validate/falsify), `appendices/appI-lean-proof-spine.tex` (formal MB statements)
- `REVIEWING_FOR_AGENTS.md` (Existing-Work Subsumptions), `formal/AlignmentProofSpine/Core.lean` (MB axioms)

## Commits
- (none this session)
