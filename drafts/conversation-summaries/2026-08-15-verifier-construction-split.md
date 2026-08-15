# 2026-08-15 — Split feedback horizon gap into two papers

## Trigger
User chose Option 2 from the structure review: split the overloaded feedback-horizon-gap paper into two companions.

## Done
- Slimmed `papers/feedback-horizon-gap/` to the original mechanism paper (`K`, accumulation, RM overopt, Lean/code, mismatched clocks). Abstract and introduction unchanged. Discussion closes with evidence-channel reconstruction as future work (no forward reference to B).
- Created `papers/verifier-construction/` with its own claim: feedback architecture can be changed. Contains regimes, verifier construction, sixteen-row table, human-learning timing, AI–human asymmetries.
- B cites A for `K` and the accumulation identity (`zarncke2026feedbackhorizon`); A does not cite B.
- Indexed in `papers/README.md`. Built both PDFs (A: 8 pp; B: 18 pp).

## Decisions
- Paper B cites A for `K` and the accumulation identity; it restates only what B needs, without re-deriving the variance formulas.
- Construction is B’s body (not an appendix). Regimes are the design space; the table is the map.
- A does not mention construction in the abstract. Reconstruction of evidence channels is future work in A, not a forward reference to B.
- Shared examples (AlphaProof, Gao, A-Lab, clinical) may appear in both papers; that overlap is accepted for standalone readability.

## Open / next
- Table 1 in B still overruns the landscape page (pre-existing float warning).
- B’s construction section and discussion still share some closing sentences; a later pass could cut further.
- Optional: numeric citation style; prune unused keys from A’s `.bib`.

## Key paths
- `papers/feedback-horizon-gap/feedback-horizon-gap.tex`
- `papers/verifier-construction/verifier-construction.tex`
- `papers/README.md`

## Commits
- none (not requested)
