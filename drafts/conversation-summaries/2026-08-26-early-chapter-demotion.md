# 2026-08-26 — Early-chapter preview demotion

**Status: closed** (v1). Durable method and scores: [`review/chapter-formulation-groundedness.md`](../../review/chapter-formulation-groundedness.md). 2.0 rerun is a Construct-lane checklist item, not this plan.

## Trigger
User asked to implement the plan: demote premature tuples and covering-inventory equations in ch02, ch03, ch04, and ch08 so first readers meet theses in prose; follow through on notation, site cards, `\symboldef`/`\symbolref`, and dependency graphs.

## Follow-on (same day): equation/section forward refs
User: demotion sites still lacked pointers to the later formulas. Added `\eqref` / `\ref{sec:…}` at those homes without `\symbolref` of later-home tokens.

- **ch02:** boundary leakage `eq:epsilon-boundary-ch07`; selection `eq:fitness-ch34`--`eq:selection-divergence-ch34`; expansion/capacity ratios; control-info `eq:ctrl-info-obs`--`eq:ctrl-info-int`; grounding `eq:conservative-abstraction-ch03`--`eq:abstraction-gap-exploitation-ch03`; attractor `sec:attractor-feedback-system-ch37`; safety-case root; agency `sec:colder-definition`--`sec:degrees-of-agency`; CCI; self-control gap; stronger-claims eq list.
- **ch03:** eight-layer roadmap now names the later eq/section; schema points at `eq:desired-guarantee-ch28` and `eq:safety-case-root-ch42`.
- **ch04:** bundle compression, bearer sufficient-statistics, response geometry, process pieces, guarantee (`sec:what-is-dynamical-guarantee` + `eq:desired-guarantee-ch28`).
- **ch08:** transport/recertification `eq:import-preserving-successor-transport-ch30`; remaining preview displays (leakage, CCI MI, transparency) now name later homes; dropped local \(\Phi_t\).

`make check` passed. Undefined `\ref` still needs a PDF/aux pass to confirm.

## Follow-on (same day): remaining preview sites
User asked to treat remaining chapters as suggested.

- **ch10:** Dropped `eq:opacity-preview-ch10`, `eq:self-control-outruns-correction`, `eq:self-control-matched`. Prose + `eq:self-control-gap` / audit-bridge.
- **ch01:** Leakage displays `\eqref{eq:epsilon-boundary-ch07}`; \(\Delta L\) → `eq:intentional-gain-simple`.
- **ch06:** Formal-summary leakage and goal-compression point at ch07/ch22 eqs.
- **ch09:** Composite residual + `A_prelim` / successor displays name ch07/ch26/ch30 eqs.
- **ch08 leftovers:** Dropped unlabeled leakage, \(d(G)\), correction MI, transparency MI, schema \(\ell\); kept labeled growth/split/merge math.
- **ch14 leftovers:** Dropped \(B_t\)/\(\Phi_t\) covering eqs, \(L\downarrow\ldots\) display, duplicate `eq:value-update-process`; kept `eq:bundle-preservation` and misalignment-growth theses.

No later-home `\symbolref` in these chapters.

## Done
- **ch04:** Kept \(U_H\) at `eq:human-value-update-ch04` with `\symboldef[U_H]`. Dropped the 5-tuple \(V_t=(B,W,\Phi,U_H,C^H)\) and \(\mathcal{S}_{\text{human-correctable}}\) displays; demoted bundle/bearer/\(G_B\) preview equations to prose plus forward chapter refs.
- **ch03:** Kept viability, basins, grounding-viability equations. Replaced \(C_A\) competence formula with prose + ch11/ch12 pointers (no \(K_X\) math). Roadmapped the eight layers; dropped \(Z_t\) alignment-structure schema.
- **ch08:** Removed \(\Xi\), transport-loss, and continuity-condition displays; recertification and replication in prose pointing at ch31. Left growth/split/merge math.
- **ch02:** Dropped 6-tuple \(X_t\), \(\Pi\), MI/power/\(D_t\) formulas; kept three-object and tool-picture lists; agency list → ch06; eval questions → ch42; \(U_H\) via ch04 eqref.
- **Follow-through:** `notation.md` (\(V_t\), \(U_H\), \(C_H\) home ch29); site recertification card + ch08 illustration prompt; informal edge `ch08 → ch31`.
- **Graphs:** `extract_symbol_formula_graph.py` + `build_chapter_symbol_dependency.py --all-modes`. Symbol DAG now 25 chapters (ch04 provides \(U_H\)). Combined reading DAG: Part I still layer 1; no reverse edge from early `\symbolref` of later-home symbols. Existing `ch08 → ch11 | I_pred` heuristic remains.
- `make check` passed.

## Decisions
- Forward pointers use `\ref{ch:…}` / `\eqref{eq:…}` / `\ref{sec:…}` in prose; no `\symbolref` of \(K_X\)/\(\chi_X\)/CCI in ch02–ch04/ch08 (would invert the reading DAG).
- Did not add \(\Xi\) to ch31; did not unify later \(V_t\) projections.
- ch08 seven-property *subsections* kept as preview depth; unlabeled covering displays later dropped in the same-day follow-on.

## Open / next
- **DAG vs `\eqref`:** Part I (ch01–ch05) may `\eqref` only Part I equations; later homes use `\ref{ch:…}` / `\ref{sec:…}`. Enforced by `check_structure.py`. Combined reading DAG still keeps Part I early because forward symbol uses are excluded.
- Optional PDF compile to confirm `\symboldef[U_H]` inside `eq:human-value-update-ch04` typesets.
- Later `V_t` arities (ch26/ch45/ch46/ch47) still differ; out of this pass.

## Key paths
- `chapters/ch02-artificial-civilization.tex`, `ch03-dynamical-guarantee.tex`, `ch04-fixed-values-wrong-target.tex`, `ch08-grow-split-merge.tex`
- `metadata/concept-graph/chapter-reading-dependency.md`, `chapter-informal-edges.yml`

## Commits
- `b0572027` — Demote early preview formulas and refresh CIRIS field evidence.
- `ec149d92` — Demote remaining preview formulas and point at later equation homes.
- `64643e11` — Keep Part I free of later-home equation numbers.
