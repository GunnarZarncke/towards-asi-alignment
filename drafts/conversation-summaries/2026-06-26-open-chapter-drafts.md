# 2026-06-26 — Open chapter drafts

## Trigger

The user asked to implement the open-chapter drafting plan: build a synthesis brief, draft the remaining incomplete main chapters, revise against the Lean proof spine, update bookkeeping, and verify.

## Done

- Added a synthesis brief: `drafts/chapter-notes/open-chapters-synthesis-brief-2026-06-26.md`.
- Drafted Chapter 5 from partial scope stub into a fuller scope contract with the correction-capacity precondition, an "alignment after capture" failure mode, Turchin coverage audit, and updated references.
- Drafted Chapter 33 into a complete multi-agent strategic-coupling bridge: effective-agent count, privacy islands, \(\kappa\), \(\mathrm{ICI}_{ij}\), \(\tilde{\kappa}\), correction percolation, acausal detector limits, worked examples, and coalition-collapse failure mode.
- Drafted Chapter 39 as a conditional safety-case assembly chapter tied to `P30`, `P40`, `MB1`--`MB8`, verifiability labels, refusal conditions, and a worked deployment example.
- Drafted Chapter 43 as the bearer/merger philosophical-limit chapter, including upload/merger treatment, \(\beta_{\mathrm{self}}\), bearer-map transformation, `P44`/`P45` limitation framing, worked example, and failure mode.
- Drafted Chapter 44 as the final synthesis, explicitly revisiting the five Introduction claims, progress artifacts, Practical Hope regime, proof-spine conditional shape, and remaining open gaps.
- Promoted `ch05`, `ch33`, `ch39`, `ch43`, and `ch44` from `stub` to `draft` in `metadata/book.yml`; regenerated `tables/chapter-map.tex`.
- Updated `frontmatter/current-status.tex`, `metadata/TODO.md`, `metadata/claims-ledger.md`, and `metadata/uncertainty-ledger.md` to reflect draft completion and remaining research gaps.
- Added `turchin2020classification` to `references/manuscript-citations.bib`.
- Follow-up: marked chapters with explicit logged reader/reviewer/user feedback as `reviewed` in `metadata/book.yml` and regenerated `tables/chapter-map.tex`.

## Decisions

- Kept `ch39` as a conditional safety-case chapter rather than moving `ch39b`; `ch39` uses verifiability labels operationally and lets `ch39b` remain the deeper critique.
- Treated `ch33` giant-component and detector claims as conjectural/empirical, with Lean support limited to `P32` threshold arithmetic and `P33` no-open-edge graph fact.
- Treated `ch43` and `ch44` as philosophical-limit synthesis: technical invariants preserve conditions for legitimate value change but do not decide legitimacy.
- Did not expand `ch39b`, `ch40`, appG, or other appendices beyond the plan scope.

## Open / next

- `appendices/appG-safety-case-template.tex` remains a stub and should be written from the new `ch39`.
- `ch39b` still owns the cost-of-faking formalization and perturbation-recognition crux.
- `ch40` remains thin and still needs per-lethality expansion plus reflective-correction/delegated-verification open-crux work.
- Historical review files under `review/` still describe the old stubs; they were not rewritten.
- Frontmatter stubs and other appendix stubs remain outside this pass.

## Key paths

- `drafts/chapter-notes/open-chapters-synthesis-brief-2026-06-26.md`
- `chapters/ch05-assumptions-scope-failure-coverage.tex`
- `chapters/ch33-multi-agent-strategic-coupling.tex`
- `chapters/ch39-safety-case.tex`
- `chapters/ch43-bearers-of-value.tex`
- `chapters/ch44-towards-alignment.tex`
- `metadata/book.yml`
- `metadata/TODO.md`
- `metadata/claims-ledger.md`
- `metadata/uncertainty-ledger.md`
- `references/manuscript-citations.bib`

## Verification

- `cd formal && lake build`
- `make check`
- `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`
- `make check` after bibliography addition
- Follow-up metadata check: `make check`
- `ReadLints` on edited chapter/frontmatter files: no linter errors

## Commits

- None.

