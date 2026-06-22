# 2026-06-23 — Ledger cross-check + preamble/label build fixes

## Trigger
Three follow-on cleanup requests after the full-book review/fix-plans work: (1) remove unused box environments, (2) fix duplicate LaTeX labels, (3) cross-check and update the Claims / Assumptions / Uncertainty ledgers against actual chapter content.

## Done
- **Unused box environments** — removed `decisionbox`, `failurebox`, `assumptionbox`, `formalbox`, `examplebox` from `metadata/preamble.tex` (verified zero `\begin{...}` uses book-wide). Kept `chapterthesis` + `\usepackage{tcolorbox}`. Build passes.
- **Duplicate labels** — the two TODO-tracked labels (`sec:self-modeling-transparency`, `sec:example-helpful-assistant`) were already unique in source (each clash carries a `-chNN` suffix); build shows no `multiply defined` warnings. The real remaining duplicate identifier was hyperref `page.i`: memoir's `titlingpage` runs `\setcounter{page}{1}` at both ends, so the title page and dedication both became roman `i`. Switched `frontmatter/titlepage.tex` to `titlingpage*` (no counter reset). Rebuild: 0 same-identifier warnings, 0 multiply-defined. Marked both items `[x]` in `metadata/TODO.md`.
- **Ledger cross-check** — extracted all 44 `chapterthesis` blocks, the 5 Introduction `introclaim`s, and ch05's background/correction-capacity assumptions, then rewrote the three ledgers:
  - `metadata/claims-ledger.md`: C-001–C-011 (composite optimizer; correctable value process; the 5 named intro claims = boundary/value-bundle/correction/successor/basin; intelligence-deepens-misalignment; goal transport/laundering; adversarial measurement; civilizational value-change limit) + C-044 tracking that the intro claims are **not yet discharged** (ch44/ch39 stubs). Added status vocabulary calibrated to the Lean spine.
  - `metadata/assumptions-ledger.md`: A-001–A-007, each with a `Bears on:` link to the claim(s) it supports. Added correction-capacity, observability, certifiability-of-deployment, intention-inferability, successor-channel-enumerability assumptions.
  - `metadata/uncertainty-ledger.md`: restructured to a table U-01–U-15 (was 8 bare questions), each linked to the chapter(s) treating it and the claim/assumption it threatens; folded in `open-problems.md` items.
  - `tables/assumptions-table.tex`: synced to A-001–A-007 (note: this file is **not** `\input` in `book.tex`).
- **Notation reference** — rewrote `metadata/notation.md` from a 10-row stub into a full canonical symbol table grouped by spine area (boundary/state, capability, bundles, bearers, intention/transport, correction, successors, multi-agent, conventions). Recorded the fix-plans §C reconciliation decisions: capability `B→K`; `B` reserved for value bundle; `G_B` = ch19 4-tuple with partials `g_B`/`H_B`; `Φ` = bearer map (ch17 feature matrix → `F`); `ΔL` log-evidence convention; CCI penalty set `L,M,R,O` (Goodhart out); `U_H` + 5-tuple `V_t`; parasite host capacity `C_X`; `κ` = cooperativity only, artifact conductivity = `χ`; residual surprise `S_X`; `η_g`/`η_c`. Rows not yet propagated into chapters are marked **⟳ propagating**.

- **ch10 forward-reference framing** — ch10 (strategic opacity, Part II) front-ran value bundles, goal laundering, parasites, self-modeling, and CCI with **no** forward `\ref`s. Per the user's decision ("operational gloss + forward-ref in a previewing frame; keep the opacity content; do it consistently"), added six surgical previewing frames — keeping all opacity material — that gloss each not-yet-defined object and forward-ref its canonical home: goal laundering → ch37 (`ch:goal-laundering`, incl. the four-layer taxonomy); value bundles/bearer maps/geometry → ch16/18/19 + inference → ch20; parasite persistence → ch34; self-modeling vs transparency → ch30; CCI → ch25; correction channel → ch24/25. Build clean, no undefined refs.

## Decisions
- Fixed stale chapter references throughout the ledgers (old "ch45" conclusion → ch44; the 44-chapter `book.yml` map is canonical).
- Did **not** invent new content/claims — every ledger entry traces to an existing `chapterthesis`, `introclaim`, or ch05 statement. Claim strengths kept honest (`framework`/`plausible`/`limit`), never "proven," per `AGENTS.md` Lean-spine calibration.
- Left `References:` as placeholders (BibLaTeX wiring is per-chapter, deferred).
- `notation.md` records the §C **canonical target** (not current manuscript state), since it is the documented canonical reference and TODO lists it as the place to record canonical forms; rows pending propagation are flagged.
- **Flagged, not resolved:** fix-plans §C4 vs §C16 disagree on whether `C_corr` is the raw capacity or the penalised value. `notation.md` sidesteps with unambiguous `C_raw` (capacity) / `CCI` (integrity) and retires `C_corr` pending the author's decision.

## Open / next
- Wire BibLaTeX keys into the ledger `References:` placeholders as chapters are finalized.
- C-044 / U-14 stay open until ch44 (conclusion) and ch39 (safety case) are written — highest completeness gap.
- U-12 (coalition/coupling detection) weak until ch33 multi-agent stub is drafted.

## Key paths
- `metadata/claims-ledger.md`, `metadata/assumptions-ledger.md`, `metadata/uncertainty-ledger.md`, `tables/assumptions-table.tex`
- `metadata/preamble.tex`, `frontmatter/titlepage.tex`, `metadata/TODO.md`

## Commits
- `8ee4956` — Propagate canonical notation, refresh ledgers, and tighten continuity bridges.
