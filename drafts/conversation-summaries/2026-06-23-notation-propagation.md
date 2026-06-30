# 2026-06-23 — Notation propagation into chapters (fix-plans §C)

## Trigger
"Propagate new notation into chapters" — apply the `metadata/notation.md` / fix-plans §C canonical forms to the manuscript. User decisions for this pass:
- **CCI capacity symbol:** retire `C_corr`; use `C_raw` (capacity) / `CCI` (integrity).
- **Sequencing:** *stage* — do the well-specified renames now; hold `B→K` (C5) for its own focused pass.

## Method
Recon-first: grepped the actual current symbol forms before editing (the book turned out to be **already largely migrated** — `U_H`, `S_X`, `G_B`(ch19) were dominant; the work was mostly mopping up stragglers + real overloads). Disambiguated by reading each context to avoid corrupting look-alike symbols.

## Done (build verified, no undefined refs / errors)
- **C1** — Introduction `ΔL` had the sign backwards; flipped to ch46 convention `ΔL = L_intentional − L_mechanistic − λ DL`.
- **C15** — ch02: 3 raw `I(…)` mutual-information → `\MI(…)`.
- **C2** — ch16: gradient/Hessian pair renamed to partials `g_B` / `H_B`; interaction curvature `T_{ij}` retired → `(H_B)_{ij}` (3×); added "these compose into `G_B` (ch19)" forward note. ch17: gradient field `G_B`→`g_B` + same forward note. **`G_B` kept** as the canonical ch19 4-tuple (and the ch16 transport-distance use).
- **C8** — ch17 feature matrix `Φ∈ℝ^{N×n}` → `F` (6 sites; bearer-map `Φ` left untouched). ch18 bundle-dim `ℝ^m`/`[0,1]^m` → `ℝ^k`/`[0,1]^k`.
- **C10** — ch46 host capacity `C_H` → `C_X` (8×, incl. `C_X^{eff}`); added one-line bridge deriving ch46's persistence inequality as a refinement of ch10's `eq:parasite-persistence-ch10`.
- **C11** — ch48 artifact conductivity `κ_ij(a)` → `χ_ij(a)` (6×); cooperativity `κ_ij` (ch13 ref) and the disclosure `κ_ij^{disclosure}` left as cooperativity.
- **C7** — value-update operator `U^H_t`/`U_t`/bare `U` → `U_H` across ch02, ch03, ch04, ch15, ch46, ch46, ch45, ch46; variants `U^A_t→U_A`, `U^{H+A}_t→U_{H+A}`, `\tilde U^H_t→\tilde U_H`, `U^{org}→U_{org}`. Value-state tuple `𝒱_t` → roman `V_t` (ch46 27×; ch04 4×). Time-indexed comparisons written `U_{H,t}`/`U_{H,t+1}`.
- **C6** — `η` overload split: growth `η = g/ΔB` → `η_g` (ch11, 9 sites incl. capability profile + decision table); coordination `η(N)` → `η_c` (ch11 + ch13). Collective gain/loss in ch11 `B_coord`/`𝒞_friction` → `G_coord`/`Ω_coord` (matching ch13's canonical pair). Residual surprise was already `S_X` book-wide (the `\mathcal S` hits were `\mathcal S_certified`, a set).

## Decisions / flags (in `metadata/notation.md` "Propagation status")
- **Did NOT merge `\mathcal U` (ch46/ch48) into `U_H`.** `U_H` is the human *value*-update operator; ch46/ch48 `\mathcal U` updates the *system's* `(Θ_t,Z_t)` under correction — a distinct object. Left as-is; author to decide whether to unify.
- **`C_H` vs `C^H_t`:** the `V_t` tuple lists `C_H` (capacity); ch02/04/36 use the time-indexed correction variable `C^H_t` inside MI. Left as-is; convention to confirm (same `t`-index question as `U_H`).
- **ch19 `\mathcal V`** = a value-representation *set* `{(B_i,Φ_i,χ_i)}`, not the value-state tuple — left calligraphic on purpose.
- **C12 (pivotal-process `𝓑_race→𝓑_certified`) deferred:** authoring an open-problem statement, not a symbol rename; would also touch the (deferred) C5 capability symbol.
- **C5 (`B→K`) not started** — its own focused pass (capability `B` overloaded vs value-bundle `B`).
- **C4/C16 (`C_corr`→`C_raw`/`CCI`) not propagated** — resolved in principle but outside this staged list; ch02 still shows `C_corr` (only its raw `I(` was fixed). Now unblocked as a follow-up.

## Addendum — broken / mis-pointed cross-ref fixes
- **ch12 L20** (real reader-facing mis-pointer): prose describes ch11's capability functional but `\ref`'d `ch:finding-boundary` (ch7) → fixed to `ch:capability-without-task-ontology` (ch11).
- **ch48↔ch48 pivotal process:** no reader-facing `\ref` exists — only the source comment (ch48-open-issues L117) falsely implied ch48 already formalizes `𝓑_race→𝓑_certified`. Corrected the comment to mark it pending (do not cite ch48 until C12 adds it). Formalization itself stays deferred (C12).
- **Scan:** no chapter `\ref`s its own `ch:` label (self-ref bug check, all 44 files); `ch:goal-transport` refs (ch18, ch46, ch46, etc.) all resolve correctly to ch46; build shows zero undefined/multiply-defined/unresolved-reference warnings.
- ch46→ch46 hand-off and ch48→ch45 bridge were already fixed in the earlier session.

## Addendum — one-directional bridge prose (review §6.10)
Small forward/back cross-ref sentences added (build clean):
- **ch45** §"The Problem of Scale" → ch09: scale question framed as the composite agent (`ch:composite-agent`).
- **ch46** §"Cross-Scale Measurement" → ch45: forward-ref to the full decomposition (`ch:multiscale-decomposition`).
- **ch48** §"The Problem" → ch46 (four layers = transport stack `ch:transport-types`) and → ch10 (detector extends the laundering signature `ch:strategic-opacity`).
- **ch46** §"False Attractors" → ch48: forward-ref (`ch:alignment-attractor`) — completes the previously one-way ch48→ch46 link.

## Addendum — remaining notation propagation (2026-06-23)
- **C4/C16:** `C_corr` → `C_raw` (bare weakest-link capacity) / `CCI` (capacity − penalties) book-wide in chapters; **kept** ch05 `$C_{\text{corr}}^{\text{society}}$` as the distinct societal scalar. ch46 canonical: ontology penalty `Ω` → `O`; ch14 fixed conflated single equation → separate `C_raw` + `CCI`.
- **C5:** capability `B` → `K` in Part III (ch11–13): `K_X`, `K_H`, `K_{\mathrm{ref}}` (was `B_Y`, avoids clash with ch46 parasite `K_Y`), collective `K_{\mathrm{coll}}`, etc.; prose `$B$` → `$K$` in ch11. ch14 `mathcal{S}` → `S_X` in competence functional.
- **metadata/notation.md** + **TODO.md** updated; build clean.

## Open / next
- **C12** pivotal-process `𝓑_race→𝓑_certified` formalization (ch48 content, not rename).
- Sync `appendices/appA-notation.tex` and `INSTRUCTIONS.md` §18 with `metadata/notation.md`.
- **Lean spine** review per `metadata/TODO.md` (`U_H` vs `U_S`, `C_raw`/`CCI`, `K`; no Lean edits this session).
- Confirm `C_H` vs `C^H_t` convention; WWCTV labels on remaining 8 chapters; fix-plans §A/B deferred items.

## Key paths
- `metadata/notation.md`, `metadata/TODO.md`, ledgers, `review/fix-plans-2026-06-22.md` §C
- chapters ch02–ch46 (Part III–VII notation + bridges); `chapters/ch43-verifiability-and-ontology-adequacy.tex`

## Commits
- `54ad1ea` — Propagate canonical notation, refresh ledgers, and tighten continuity bridges.
