---
leanNodes:
  - nodeId: MB3_bearer_import
    kind: bridge
    summary: Bundle transport plus a preserved bearer map across systems is assumed to license bearer transport — a translated substrate still applies values to the right entities.
    module: AlignmentProofSpine/Core.lean
  - nodeId: ConservativeExclusion
    kind: definition
    summary: One-sided non-bearer certificate soundness (admission sub-obligation); not part of MB3Crux / BridgeAssumptions. Success licenses exclusion; failure abstains; soundness ≠ completeness.
    module: AlignmentProofSpine/Bundles.lean
  - nodeId: BearerAdmissionMisclassified
    kind: defeater
    summary: Named U-17 signal for unsound or incomplete bearer admission / exclusion under unfamiliar substrates; distinct from BearerMapSpoofed (transport).
    module: AlignmentProofSpine/Defeaters.lean
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
  - pointing-problem
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Field adjacent work (bearer admission)
    url: https://towards-alignment.com/field/v2/#adjacent-work
---

In the field, value learning usually folds "who the values apply to" into reward or preference learning and moves on. That leaves a quiet failure mode: the words for a value can survive a merge, upload, or substrate change while the entities those values protect are dropped, relabeled, or quietly redefined. Surface semantics look fine; moral application has shifted. That is the [bearer-map commutation](/cards/bearer-map-commutation-failure/) worry, adjacent to the identification sense of the [pointing problem](/cards/pointing-problem/), not the same crux as [MB2](/cards/mb2-bundle-identifiability/).

This project's precise bet is **MB3**, with two conceptually distinct obligations:

1. **Bearer admission (inference).** When a system encounters a process unlike the examples on which its value concepts were learned — a digital mind, a simulated agent, a hybrid tool-memory loop — what evidence should make that process count as a bearer of bundle $k$ at all? Conservative one-sided exclusion certificates (`ConservativeExclusion` in Lean) may certify "definitely not relevant for $k$" and must abstain otherwise; they do not complete classification. Consciousness, sentience, and valence theories enter as candidate evidence providers, not as the definition of MB3.
2. **Bearer transport (persistence).** Given an already-recognized bearer map, a preserved map under substrate translation is assumed to make [value-bundle transport](/cards/value-bundle-transport/) more than a coincidence of wording.

The live Lean bridge (`MB3Crux` / `MB3_bearer_import`) types the **transport** half. Admission is an open sub-obligation (ledgers: U-17), not a new `MB*` column and not part of `BridgeAssumptions`. Neighborhood field notes: [adjacent work](/field/v2/#adjacent-work).

**Where agendas agree:** thin coverage (CEV "whom"; some PreDCA population talk; nonperson-predicate and AI-welfare work as admission neighborhood). **Where they diverge:** the field usually folds referent into identification-pointing; this project types referent transport separately and keeps admission inside MB3 rather than inventing MB3a.

Diagnostic evidence shows why passive signals are not enough for *transport*: a system can drop or relabel a bearer while every human-facing channel stays flat. Only handle-level tracing catches the mismap. Admission failures are a different signal (`BearerAdmissionMisclassified`): treating abstention as exclusion, or an unsound non-bearer certificate, under unfamiliar substrates.
