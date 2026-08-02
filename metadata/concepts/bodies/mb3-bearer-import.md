---
leanNodes:
  - nodeId: MB3_bearer_import
    kind: bridge
    summary: Bundle transport plus a preserved bearer map across systems is assumed to license bearer transport — a translated substrate still applies values to the right entities.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: embedded-simulation diagnostic (T-5)
    scenario: bearer_mismap
    finding: negative
    summary: Light-handle instrumentation false-passes 100% of diagnostic seeds where harm is routed to the wrong bearer while the human-facing passive trace stays flat; medium/strong handles catch all of them.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
related:
  - bearer-persistence
  - bearer-map-commutation-failure
  - value-bundle-transport
  - mb2-bundle-identifiability
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

In the field, value learning usually folds "who the values apply to" into reward or preference learning and moves on. That leaves a quiet failure mode: the words for a value can survive a merge, upload, or substrate change while the entities those values protect are dropped, relabeled, or quietly redefined. Surface semantics look fine; moral application has shifted. That is the [bearer-map commutation](/cards/bearer-map-commutation-failure/) worry, adjacent to the same pointing problem as [MB2](/cards/mb2-bundle-identifiability/).

The book's precise bet is **MB3**: a preserved [bearer map](/cards/bearer-persistence/) under a substrate translation is assumed to make [value-bundle transport](/cards/value-bundle-transport/) more than a coincidence of wording. Most agendas do not name this as a separate crux; the book treats it as first-class and measurable.

**Where agendas agree:** thin coverage (CEV "whom"; some PreDCA population talk). **Where they diverge:** the field usually folds referent into pointing; the book types referent transport separately.

Diagnostic evidence shows why passive signals are not enough: a system can drop or relabel a bearer while every human-facing channel stays flat. Only handle-level tracing catches the mismap.
