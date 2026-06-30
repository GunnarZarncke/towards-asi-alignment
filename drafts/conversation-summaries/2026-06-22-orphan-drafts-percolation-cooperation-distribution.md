# 2026-06-22 — Distribute two orphaned drafts (Percolation of Cooperation; Cooperation, Privacy, Opacity)

## Trigger
User supplied two early standalone drafts that are no longer in the lineup ("Percolation of Cooperation" and "Cooperation, Privacy, and Opacity") and asked whether their content adds anything around ch48, to suggest additions before editing, then approved distributing the genuinely-new pieces.

## Done
- Analyzed both drafts against existing chapters. Found ~two-thirds already covered: `kappa_ij = b p rho / c` in ch13/ch48/ch46/ch48; percolation threshold + `S(phi)` in ch13/ch48; CCI chain + penalties in ch46; parasite persistence in ch46; privacy islands in ch13/ch46; value-bundle relation in ch16/ch45/ch46.
- ch48 (`ch48-multi-agent-strategic-coupling.tex`): in `sec:cooperation-privacy-opacity` added the `gamma_ij` (recipient value) vs `kappa_ij` (relational cooperativity) distinction + the "predator has gamma>0" point. In `sec:percolation-inferential-coupling` added value-sensitive cooperation `rho^V`/`kappa^V`/`phi_V`, correction percolation `phi_C`, edge-level goal laundering `D_ij`, and the thesis "alignment must percolate before capability does." Added `D_ij` line to Counterexample and two bullets + thesis to Summary. Cross-refs to ch13/ch16/ch18/ch46/ch46/ch48. (Only `\ref`, no `\autocite` — ch48 has no refsection.)
- ch46 (`ch46-parasites-correction-system.tex`): new subsections `sec:selective-opacity-legitimacy-ch46` (selective opacity ratio `O_sel`, legitimacy sign `Lambda(e)` turning the kappa-test into a 2x2, role-sensitive disclosure table) and `sec:parasitic-disclosure-ch46` (privacy laundering; asymmetric model advantage).
- ch46 (`ch46-correction-channel-integrity.tex`): new section `sec:directional-transparency-ch46` (three directional legibility channels; manipulation exposure `M_exposure = I(M^H_AI; U_H)`; surveillance-alignment failure mode) + a matching entry in the Failure Modes catalog.
- Build: `./build.sh` exits 0, 952 pages. No new lint errors. Only pre-existing duplicate-label warnings (`sec:self-modeling-transparency`, `sec:example-helpful-assistant`) remain — unrelated to this work.

## Decisions
- Did NOT resurrect either draft as a chapter. ch48 line 14 already declares both removed chapters folded in as subsections; the drafts are sources, not new parts.
- Distributed rather than dumping into ch48: ch48 kept to the strategic-coupling-relevant slice; privacy/opacity diagnostics went to ch46 (which already owns `kappa_ij` for privacy); directional transparency + manipulation exposure went to ch46 (which already owns the correction chain and `U_H`).
- Avoided re-deriving `kappa_ij` / the percolation threshold a third time; cross-referenced ch13/ch48 instead.
- Used `-ch46/-ch48/-ch46` label suffixes to avoid new duplicate labels.
- Dropped already-covered material (CCI, parasite persistence, percolation threshold, value-bundle relation).

## Open / next
- ch48 is still a stub overall (Worked Example, Counterexample, What-Would-Change, References are `[STUB]`/TODO). The new formal content is in place but the narrative scaffolding and `refsection`/`\printbibliography` + cites (wang2013percolation, zarncke2025attractor, hamilton1964genetical) are not yet wired.
- Pre-existing duplicate labels still unaddressed.
- Remaining stub chapters: ch48 (partial), ch46, ch47, ch48.
- Not committed (user has not asked).

## Key paths
- `chapters/ch35-multi-agent-strategic-coupling.tex`, `chapters/ch36-parasites-correction-system.tex`, `chapters/ch26-correction-channel-integrity.tex`
- `chapters/ch13-coordination-bottleneck.tex`, `chapters/ch37-alignment-attractor.tex` (existing homes of kappa/percolation)

## Commits
- none (no commit requested)
