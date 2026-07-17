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
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

Most value-learning agendas fold "who the values apply to" into reward learning and move on. The book treats bearer maps — who or what counts as the target of a value — as a first-class, separately measurable object, because bundle content can survive a transition while its bearer map silently does not.

MB3 is the assumption that a preserved bearer map, checked under a substrate translation, is enough to call the transport more than a coincidence of surface semantics. It is one of the bridges the book adds rather than inherits, since most agendas do not name this as a separate crux at all.

The diagnostic evidence shows why the bridge needs real instrumentation to hold: a system can drop or relabel a bearer while every passive, human-facing signal stays flat. Only handle-level tracing catches the mismap.
