# Session: Krym Phase 6 — Crux Props, formal contracts, field v2

**Date:** 2026-08-17  
**Thread:** Krym architecture revision (after Phase 5)

## Goal

Thread remaining bridges as `Prop` cruxes; pilot chapter formal contracts; field v2 preview (lifecycle + open interfaces); keep v1 live until author confirms cutover.

## Shipped

### 6a — Crux Props
- `formal/AlignmentProofSpine/BridgeCruxes.lean`: `MB1Crux`–`MB9Crux` (except MB2/MB4/MB8), `CoreBridgeCruxes`, `standardCoreBridgeCruxes`, `toBridgeAssumptions`.
- `Forgeability.lean`: `MB10Crux`, `mb10_crux_holds`.
- `Certification.lean`: `MB11Crux`, `mb11_crux_holds`, `certified_class_safety_from_core_cruxes`.
- `AlignmentConstruction.lean`: `ConstructionCrux` alias.

### 6b — Formal contracts
- `{formalcontract}` tcolorbox in `metadata/preamble.tex`.
- Pilot boxes: ch21, ch25, ch26, ch28, ch33, ch43.

#### 6b.0 audit (chapter ↔ Lean anchors)

| Bucket | Chapters |
|--------|----------|
| **With `\leanspine`** (22 ch, 52 anchors) | ch03, ch07, ch08, ch10, ch11, ch17, ch21, ch25–31, ch33, ch35, ch39, ch41–43, ch47–48 |
| **Touched this revision + contract** | ch21, ch25, ch26, ch28, ch33, ch43 |
| **Zero anchors** (26 ch) | ch01–02, ch04–06, ch09, ch12–16, ch18–20, ch22–24, ch34, ch36, ch37, ch40, ch44–46 |
| **ch01 decision** | Prose-only (no Lean symbols); construction Lean names on ch33 |

### 6c — Field v1/v2
- `reference/field-agendas/data/meta.yml`: MB8 retired from spineTranslation; `openSpineInterfaces` populated.
- `open-spine-interfaces.yml`, `bridges-v2.yml` (lifecycle roles).
- `site/scripts/sync-field-v2.mjs`, `site/src/data/field-v2.json`, `/field/v2/` preview page.
- `metadata/concepts/bodies/target-realization.md` + concept card.
- `formal/scripts/check_open_spine_interfaces.py`.

## Verification

- `lake build` — pass
- `check_open_spine_interfaces.py` — pass
- `check_axiom_budget.py --update` — pass (40 theorems)
- `npm run sync:field-agendas`, `sync:field-v2`, `sync:concepts` — pass

## Open / deferred

- **v2 cutover** to live `/field/` — manual author confirm (not done).
- Expand formal contracts to remaining `\leanspine` chapters (gap list above).
- Optional: wire `check_open_spine_interfaces.py` into `make check`.
- Chokepoint / disjunctive MB6b∨MB8 prose erasure (plan item; not this pass).

## Locked

- Live `/field/` stays v1 matrix (MB8 column already hidden).
- No new `MB*` for Target Realization.
