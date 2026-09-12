# 2026-09-11 — Agency-detect maintained-blanket import

## Trigger
User asked to check sibling `agency-detect` for new papers, add them to `context/`, and check whether any chapter should take them into account.

## Done
- Compared `../agency-detect/docs/papers/` to `metadata/source-canon.md`. Only new paper since the 2026-06-25 UAD import: **Discovering Maintained Agent Boundaries** (`maintained-blanket`, sibling commit `028069e`). Other listed papers already had `context/` PDFs + extracts; `applications-uad-loops` still has no built PDF.
- Copied `context/maintained-blanket.pdf`; extracted `context/extracts/maintained-blanket.md` (10 pages).
- Indexed in `metadata/source-canon.md`, `scripts/import_source_map_refs.py` (`zarncke2026maintained`), `references/internal-project-sources.bib`, `references/bibliography-summaries.tex`.
- Source-map one-liners: `docs/MANUSCRIPT.md`, `docs/EXPERIMENTS.md` §0, `REVIEWING_FOR_AGENTS.md`.
- Did **not** rewrite chapters (citation policy: internal UAD papers stay in context; book prose derives the claim). Did **not** run `import_source_map_refs.py` to completion against live `.bib` files — a trial run rewrote unrelated entries (dropped DOIs, added sibling aliases); reverted those files and added the new key by hand.

## Decisions
- Key `zarncke2026maintained` matches the sibling `refs.bib`.
- Chapter impact is real but surgical: the book already uses ε-blanket separation and says “maintains a boundary” in prose; it does not yet have the paper’s second axis (observable damage + post-damage mean reversion) or the identifiability result (passive traces cannot distinguish active repair from passive relaxation).
- **Correction (same session):** do not add self-repair to the operational-agent definition. Boundary persistence can be accidental, operator-supplied, or selected-for; AI need not try to repair “its” cut. “Maintain” wording on agent boundaries (ch01/ch06/ch08) is the real manuscript issue. Lean `AgentCandidate` is leakage-only; do not bake repair into `BoundaryCondition`.
- Do not add App N AD-3 from the paper’s toy table: that experiment is not in `agency-detect/docs/FINDINGS.md`.

## Open / next
- Optional manuscript pass (ask before writing): retarget ch01/ch06/ch08 “maintains a boundary” sentences so persistence ≠ self-repair; optional ch07 paragraph on *who pays* for damage-reversion (physics / operator / institution / selected policy). Do not add a fifth agency clause. Do not `\autocite{zarncke2026maintained}`.
- Lean: no change. Optional later empirical predicate (reversion + restorer locus), not a requirement for `AgentCandidate`.
- Related unindexed sketch: `drafts/entropic-agency-experiment.md` (transfer into a degrading ecology).

## Key paths
- `context/extracts/maintained-blanket.md`
- `../agency-detect/docs/papers/maintained-blanket/maintained-blanket.tex`
- `chapters/ch06-agent-without-anthropomorphism.tex` (operational agent def.)
- `chapters/ch07-finding-boundary.tex` (ε-blanket + handles)
- `chapters/ch08-grow-split-merge.tex` (snapshot vs identity over time — different sense of “maintain”)
- `drafts/entropic-agency-experiment.md`
