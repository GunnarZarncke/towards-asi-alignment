# 2026-08-15 — ch34 selection spin-out integration

## Trigger
Implement the ch34 selection spin-out integration plan: adversarial selection/coevolution, `N_proxy`, hierarchy, fast/slow regime map, spin-out paper symbol sync, ch27 reward tampering—without citing spin-out papers in the book.

## Done
- [`drafts/ch34-fast-slow-selection-regime-map.md`](../../drafts/ch34-fast-slow-selection-regime-map.md) — slow/fast/shared `\vec{\Pi}` regime note.
- [`papers/feedback-horizon-gap/feedback-horizon-gap.tex`](../../papers/feedback-horizon-gap/feedback-horizon-gap.tex): `K` → `N_{\mathrm{proxy}}` (`\Nproxy` macro); PDF rebuilt.
- [`papers/verifier-construction/`](../../papers/verifier-construction/): synced `N_{\mathrm{proxy}}` across all `.tex` fragments; PDF rebuilt.
- [`chapters/ch34-selection-environment.tex`](../../chapters/ch34-selection-environment.tex): ecology paragraph (selection turn); `N_proxy` subsection; coupled-selector ¶; adversarial selection + coevolution; selection-stable hierarchy; selection-alignment opening tweak.
- [`chapters/ch27-correction-channels-adversarial-pressure.tex`](../../chapters/ch27-correction-channels-adversarial-pressure.tex): reward tampering bullet (`everitt2019`).
- [`references/manuscript-citations.bib`](../../references/manuscript-citations.bib) + [`references/bibliography-summaries.tex`](../../references/bibliography-summaries.tex): geritz, everitt2019, hardt, perdomo, courret, gao2022overoptimization, coevolution refs, wilke, etc.
- [`metadata/notation.md`](../../metadata/notation.md): `N_proxy`, `InvFit`, homograph row.
- `./build.sh` succeeded; symbol dependency graph regenerated.
- **Symbolref recipe (ch34):** `\symboldef[M_sel]`, `\symboldef[AdvVerif]` in preservation envelope; `\symbolref[CCI]`, `\symbolref[M_sel]`, `\symbolref[AdvVerif]`, `\symbolref[InvFit]`, `\symbolref[RiskGap]`, `\symbolref[Control]`, `\symbolref[K_X]` at load-bearing sites; `M_sel` / `AdvVerif` rows in `notation.md`. Graph regen: raw **`ch26→ch34` (CCI, 7 sites)**, **`ch11→ch34` (Control/K_X, 4)**; reduced graph keeps **`ch33→ch34` (RiskGap)** and drops bridged `ch26→ch34` (path via `ch26→ch33→ch34`).
- **Prose pass:** hierarchy → alignment-condition flow; Adversarial Selection limitations paired with operational responses (rare-type test, two-sided regeneration target, AdvVerif + `M_{\mathrm{sel}}`).

## Decisions
- Symbol: **`N_{\mathrm{proxy}}`** (not `K` / `H`) for proxy-throughput count; English *feedback-horizon exposure* in prose.
- Invasion fitness: dual-regime `\mathrm{InvFit}_E(a\mid D)`; fast regime collapses to pre-deploy cert/`AdvVerif`.
- No spin-out paper cites in manuscript.

## Open / next
- `make check` still fails on pre-existing missing bib keys in `global-nocite` vs `manuscript-citations.bib` (unrelated to this session).
- Optional: `metadata/concepts.yml` glossary rows for `N_proxy` / invasion resistance.
- User review of regime-map draft before further ecology prose expansion.
- Optional: Adversarial Coevolution section could get the same limitation→response treatment as Adversarial Selection.

## Verification
- `python3 scripts/check_bibliography_summaries.py` — pass.
- `./build.sh` — pass.
- `python3 scripts/build_chapter_symbol_dependency.py --mode combined` — pass.
