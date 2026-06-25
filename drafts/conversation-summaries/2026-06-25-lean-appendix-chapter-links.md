# 2026-06-25 — Lean appendix chapter links

## Trigger
User asked that definitions in the Lean proof appendix, such as CCI, Risk, and Control, link to their chapter definitions, then asked to also link high-priority, medium-priority, and bridge references while skipping lower-priority toy counterexamples.

## Done
- Added chapter anchors for `Control`, `RiskGap`, `Risk`, and `SelfControlGap` in:
  - `chapters/ch11-capability-without-task-ontology.tex`
  - `chapters/ch30-self-modeling-self-opacity.tex`
  - `chapters/ch31-certification-without-construction.tex`
- Updated `appendices/appI-lean-proof-spine.tex` so definition blocks link to book homes for boundary/blanket quantities, access and handle identifiability, CCI, successor safety, layered alignment, tripwire certification, MDL gain, distance/drift basics, percolation, and selected high/medium theorem nodes.
- Added `Book bridge:` lines to MB1-MB8, pointing each bridge assumption to the chapters that carry its empirical/philosophical load.
- Kept lower-priority toy counterexamples mostly unlinked as requested.
- Updated `metadata/notation.md` with entries for `Control`, `RiskGap`/`Risk`, and `SelfControlGap`.
- Follow-up cleanup: renamed ch31's local CCI subsection to "Correction-Channel Certification", removed the local-looking `CCI(A,\mathcal{E},\mathcal{M})` form, and made ch31/ch32 explicitly use canonical ch25 CCI.
- Follow-up cleanup 2: removed ch31's ad-hoc correction trace and MI-based correction guarantee; ch31 now certifies the ch24 handle-controlled channel and ch25 canonical CCI threshold.
- Ran `./build.sh`; PDF build succeeded. Remaining warnings are pre-existing unresolved citations, not new cross-reference failures.

## Decisions
- Avoided introducing additional chapter equations unless an anchor was needed for a real appendix definition (`Control`, `Risk`, `SelfControlGap`).
- Used section-level references for broad concepts such as access-model soundness, layered certification, hidden-BIQ robustness, and basin/percolation bridges.
- Did not link lower-priority toy counterexamples P15/P17/P18/P22b/P25/P26/P31/P41-P44.
- Ch31 defines only `RiskGap`/`Risk`; CCI remains canonical in ch25.

## Open / next
- Optional: add a dedicated aliasing subsection/equation in ch39b if host-capacity aliasing should have a more precise anchor than `ch:verifiability-ontology`.
- Optional: add a named `LayeredAligned`-style displayed conjunction in ch31 if the Lean predicate should match the chapter more literally.

## Key paths
- `appendices/appI-lean-proof-spine.tex`
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch30-self-modeling-self-opacity.tex`
- `chapters/ch31-certification-without-construction.tex`
- `metadata/notation.md`

## Commits
- (none)
