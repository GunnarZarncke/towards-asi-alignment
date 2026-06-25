# 2026-06-23 — Lean spine sync with manuscript (notation, SuccessorSafe, CCI-only)

## Trigger
Review Lean proof spine against chapter/notation changes; bring identifiers in sync; then remove backward compatibility, clarify SuccessorSafe vs `U_S`/`CCI`, drop `C_raw` from Lean to avoid manuscript inconsistencies.

## Done
- **Operators:** `ValueUpdateOperator` (`U_H`), `SystemUpdateOperator` (`U_S`); no legacy `UpdateOperator`.
- **Correction measurand:** **`CCI` only** in Lean. Weakest-link MI is `CorrectionPath.weakestLink` (internal to `CCI`); book’s $C_{\mathrm{raw}}$ is not exported. Removed `CorrectionRawCapacity`, `CorrectionRawCapacityPreserved`, `RawRiskGap`, raw-path certificates.
- **Typed path:** `CorrectionChainLink`, `CorrectionPath`, `SystemCorrectionPath`; `P24_weakest_link_le_each_link`.
- **`SuccessorSafe`:** `Nonempty SuccessorSafeWitness` with ch29 fields; correction conjuncts = `CCIPreserved` + `SystemUpdateOperatorPreserved` (distinct); `P28` variants for each.
- **Risk / certification:** `RiskGap = Control − CCI`; `P30` / certificates use `Control ≤ CCI + δ`.
- **Spine citations:** `\leanspine{kind}{node}{gloss}` in `metadata/preamble.tex`; wired in ch03, ch24–26, ch29, ch31, ch39.
- **`formal/README.md`**, **`metadata/TODO.md`** updated.
- `lake build` clean; `./build.sh` clean after citation pass.

## Decisions
- **Manuscript vs Lean:** book keeps $C_{\mathrm{raw}}$ and $CCI$ as named symbols; Lean exports **`CCI` only** so the spine cannot drift on a second capacity identifier.
- **`U_S` vs `CCI`:** different objects — integrity metric vs system update semantics; both in `SuccessorSafeWitness`.
- **No backward compatibility** in Lean (legacy abbrevs and raw-cert theorems removed).

## Open / next
- More `\leanspine` citations (ch07, ch11, ch33, ch37, ch44).
- ch35 pivotal basins vs `P35`; bundle geometry in `Bundles.lean`; ch13 coordination in `P12`.
- Expand ch39 stub; appA Lean spine index.
- Other working-tree items from earlier sessions (continuity review, epigraphs, etc.) — not staged.

## Key paths
- `formal/AlignmentProofSpine/*.lean`, `formal/README.md`
- `metadata/preamble.tex`, `metadata/TODO.md`
- `chapters/ch03-dynamical-guarantee.tex`, ch24–26, ch29, ch31, ch39

## Commits
- `f29f8c2` — Sync Lean proof spine with manuscript notation and wire spine citations.
