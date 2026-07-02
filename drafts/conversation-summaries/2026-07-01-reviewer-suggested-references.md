# 2026-07-01 — Reviewer-suggested references

## Trigger
User supplied reviewer-suggested reference clusters (viability theory, ecological resilience, planetary boundaries, safe-set/reachability control, human-values alignment papers, corrigibility). Task: assess fit, add bib + cites where they strengthen existing material, add TODOs where they open new angles.

## Done
- Added 20 BibTeX keys across `references/dynamical-systems.bib`, `references/external-alignment.bib`, `references/philosophy.bib`.
- Added matching `\bibsummary{...}` lines in `references/bibliography-summaries.tex` (376/376 keys).
- Surgical in-body cites and chapter reference blocks:
  - **ch03** — viability kernel / safe operating space; grounding viability; drift/regime shifts; set invariance + HJ reachability.
  - **ch04** — Kasirzadeh preferentialist critique.
  - **ch28** — Nayebi lexicographic corrigibility (hedged vs dynamical basin view).
  - **ch33** — invariant sets, reachability, shielding, safe MARL in basin guarantees.
- **metadata/TODO.md** — follow-up items for Edelman *Full-Stack Alignment* and Heitzig & Potham human-power maximization (bib present, not cited in prose).
- `make check` passes.

## Decisions
- **Corrigibility URL correction:** user link `2508.00159` is Heitzig & Potham human-power maximization, not corrigibility. Cited **Nayebi 2025** (`2507.20964`, `nayebi2025core`) for formal corrigibility instead.
- **Edelman 2025 / Heitzig 2025 human power:** added to bibliography for discoverability but deferred in-prose integration — they open institutional/thick-value and power-max vs correction-channel angles better handled as a dedicated pass.
- **Kasirzadeh:** Springer article (doi `10.1007/s11098-024-02249-w`); bib year 2025 matching *Philosophical Studies* volume 182.

## Open / next
- Prose pass on Edelman full-stack co-alignment vs value-bundle transport (ch04/ch48/appC).
- Compare Heitzig human-power objective to correction-channel integrity framing (ch25–28).
- Optional: rebuild PDF (`./build.sh`) if user wants links rendered for new cites.

## Key paths
- `references/dynamical-systems.bib`, `references/external-alignment.bib`, `references/philosophy.bib`
- `chapters/ch03-dynamical-guarantee.tex`, `ch04-fixed-values-wrong-target.tex`, `ch28-extrapolative-correction.tex`, `ch33-certification-without-construction.tex`
- `metadata/TODO.md` (reviewer-suggested references section)

## Commits
None (user did not request commit).
