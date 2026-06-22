# 2026-06-22 — Fix plans for the full-book review + chapter-ending style pass

## Trigger
Follow-up to the full-book review (`review/full-book-continuity-review-2026-06-22.md`). User asked for a set of **sub-plans** to fix the issues (mostly plan-only, not execute), with specific carve-outs: (1) per-duplication strategy for re-derived formulas using a fixed strategy menu; (2) same for redundant taxonomies/objects; (3) make TODOs for frontmatter gaps + ch05 + ch40; (4) list which opening promises are payable in the ending today + add a reconciliation TODO; (5) a resolution for each formula inconsistency; (6) appendix content suggestions; (7) one fix per per-part pointer; (8) **fix style directly** to the most-common usage; (9) flag anything not planned for. User owns WWCTV, the ch33 draft, the deferred synthesis chapters (intentionally incomplete), and the continuity defects (later).

## Done
- Wrote `review/fix-plans-2026-06-22.md` — the consolidated sub-plans:
  - §A per-formula re-derivation strategy (8 spine objects, each: home + per-chapter elide/reminder/ref/add-context/rewrite); principle = prefer one-line "reminder + ref" over barren pointers.
  - §B redundant taxonomies/argument-blocks/worked-examples (11 items) + intra-chapter duplication.
  - §C a concrete resolution for all 16 formula inconsistencies (with chosen canonical symbols: `B→K`, `G_B`=ch19 4-tuple, CCI penalty set with Goodhart out, `U_H`+5-tuple `V_t`, parasite=ch10 form, `κ`=cooperativity only / artifact conductivity=`χ`, ΔL log-evidence convention, etc.).
  - §D opening-promise payability table (claims 1–4 already backed; claim 5/basin needs ch33; safety-case + synthesis are the only structural gaps → premise IS deliverable).
  - §E appendix recommendations (write appA notation + appF glossary now; B–E/G track their chapters; fold appH).
  - §F one fix per per-part pointer.
  - §G style (what was executed + capitalization held for a decision).
  - §H gaps not in any user bullet (unused box envs; build verification; duplicate labels; ledgers; Lean alignment; part-openers; notation.md/INSTRUCTIONS sync; demos/figures).
- **Executed style fix (chapter endings):** normalized chapter-ending headings to `\section{Summary}` (de-facto majority) in 8 single-ending chapters: ch02, ch04, ch06, ch09 (also removed the `\section*` star), ch24, ch25, ch30, ch31. Heading text only; `\label`s left intact (no ref breakage).
- **Executed style fix (Title Case, book-wide):** user approved Title Case + bulk pass. Ran 9 parallel subagents with one identical rubric to Title-Case every `\section`/`\subsection`/`\subsubsection` heading in all 44 chapters, skipping `Summary` and `What Would Change This View` (author-owned) and `[STUB]` lines. ~630 headings converted. Reconciled one cross-agent inconsistency: lowercased mid-title prepositions `across`/`around`/`inside`/`near`/`plus` (ch09 ×6, ch10, ch16 ×2, ch18, ch19, ch20, ch28). **Verified:** `make check` passes; `./build.sh` compiles the PDF (exit 0).
  - Open style decisions left as-is pending a house-style call: hyphenated-compound casing (`Lock-In`/`Lock-in`, `Non-Manipulation`/`Non-manipulation`, `CEV-like`/`CEV-Like`, `Market-Like`).
- **Updated `metadata/TODO.md`** (Manuscript cross-cutting): expanded ch05; added ch40 flesh-out, Frontmatter gaps, Opening-promise reconciliation, Notation reconciliation; updated the §10 structure item to reflect the heading normalization + remaining dual-ending chapters.

## Decisions
- Style "fix directly" interpreted as: do the mechanical, high-confidence, low-volume normalizations now (chapter endings); **hold section-title capitalization** for an explicit decision because the majority (Title Case, ~30 vs ~14) would require ~150 subjective per-title edits — asked the user rather than churn lines in the wrong direction.
- Dual-ending chapters (ch12, ch42) and ch23's front-summary were **excluded** from the style pass and routed to §B12 (content merge, not a rename).
- §C sequencing: resolve inconsistencies (especially both-inconsistent-and-duplicated objects) **before** deduplication, so canonical forms aren't propagated wrong.
- TODO.md edits are tracking-file changes (the "make TODOs" instruction), not manuscript fixes — consistent with "don't execute the fixes yet."

## Open / next (for the user / next session)
- Optional house-style call on hyphenated-compound casing (see Done).
- User-owned: stronger WWCTV sections; ch33 draft; deferred synthesis (ch39/ch43/ch44 + appendices) pending premise/Lean confirmation; continuity defects.
- Recommended next execution (per `review/fix-plans-2026-06-22.md` order): §C inconsistencies → §A/§B deduplication → continuity defects, re-running `./build.sh` + `make check` after the §C edits.

## Key paths
- `review/fix-plans-2026-06-22.md` — the deliverable.
- `review/full-book-continuity-review-2026-06-22.md` + `review/_pass/part-0N.md` — source issue list.
- `metadata/TODO.md` — new cross-cutting TODOs.
- Edited chapters: ch02, ch04, ch06, ch09, ch24, ch25, ch30, ch31 (ending heading only).

## Commits
- None (no commit requested).
