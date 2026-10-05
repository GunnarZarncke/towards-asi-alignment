# Claim-extract lane: fix Chapter 42 first

Status: open. Scope: repair `chapters/ch42-safety-case.tex` against the claim extract; other chapters wait until this is done.

Instrument: `metadata/claim-extracts/ch42.jsonl` (one record per load-bearing sentence: formal line, qualifier, Lean referents, flags; schema and stop rule in `metadata/claim-extracts/README.md`). Check with `python3 scripts/check_claim_extract.py`. Records are cited as `ch42.NNN`.

Stop rule: an item is closed when the chapter or plan was changed and the affected records re-checked, or the author wrote "keep as is" here. Closed items are deleted from this file with a session-log note. Items still open after the Ch. 42 pass move to `metadata/TODO.md`.

## Principles

1. **Prose claims no more than the spine at the same name.** If the chapter states something the Lean spine does not carry, the sentence names the bridge or assumption that carries it. Where the chapter and Lean diverge and the divergence is not repaired, say so in the chapter.
2. **The case is the four-spine join.** The eight predicates (`BoundaryAligned`, `GroundingViable`, `BundleTransport`, `BearerTransport`, `CorrectionIntegrity`, `SuccessorStable`, `CorrectionSupportingBasinSys`, `AdversariallyRobust`) are exports of the four spines in `context/lean_proof_graphs/00-overview.dot`: boundary and measurement; value and transport; correction and successors; selection and limits. The chapter walks those spines and the edges between them. `LayeredAlignedDef` is only the conjunctive join after the edges: one missing export blocks the case. Do not define "layer" as an object, and do not keep a layer table. Which bridge an export depends on is an edge tag on the figure below, read as what must be validated for that export to mean what it says. The assembled theorem today consumes only `MB6a`, `MB6b`, `MB7a`, `MB7b`, `MB7c`, `MB9`; boundary, bundle, bearer and successor enter as `DirectLayerEvidence`. That split is historical. The 2.0 assembly joins the four spine exports instead (below).
3. **Parameter convention, stated once at the assembly.** Full form `SafeFor(A, D, T, δ)`. Explicit arguments: `A` (system), `δ` (accepted slack). Context parameters, fixed once per case and suppressed in notation: `P` (alignment target), `D` (deployment class), `T` (threat model). Short forms (`Safe(A)`, `AdversariallyRobust(A)`, and the eight export predicates) are read as `· (A | P, D, T)`. Earlier chapters keep the informal short form. A book-wide scheme is 2.0 work (below); Ch. 42 only anticipates it.
4. **Verifiability gating is stated, not enforced (G0).** The assembled theorem assumes each audit channel (`MB6b`, `MB7b`, `MB7c`) is not steerable at the system's capability (`Chokepoint.AdversariallyVerifiableUpTo`, `SteerableAt`). The chapter says so, names the defeater ledger (`Defeaters.lean`, `MB7bcd_defeater_signal`), and says that a case that cannot show it must restrict, redesign or refuse. The existing `VerifiabilityGatedBridge` instances ignore their gate hypothesis and must not be cited as enforcement.
5. **Sufficiency of the join is carried by `MB11`.** The chapter says the exports are assembled from earlier chapters, not derived from a completeness argument, and that `MB11` (certified safety case + tolerance ⇒ `Safe`) is where sufficiency of that join is assumed. Deriving or bounding completeness is 2.0 work.
6. **One name per object.** Root: `SafeFor` is the full form, `Safe` the short form, the package of `eq:safety-case-root-ch42` is what the case establishes, `MB11` is the step between them. `Certified(A)` is reserved for the certificate bundle; the package is "certified safety case". "Leaf" means a required export of the join, or the support for that export, not an observed fact. "Graph", not "tree". One decision vocabulary. Do not introduce "layer" as a name for the exports.
7. **Unhedged universals are hedged, argued, or cited.** Qualifiers stay as words in the text; no numeric mapping.
8. **Process.** Chapter edits are surgical and limited to the items below. Do not type counts into docs. No recency markers. After edits: shift or repair affected extract records, run the checker, run `./build.sh` and `make check`, write the session log.

Defaults until the author decides otherwise: normative sentences ("must/should") stay in the same record schema with `rule` naming the obligation form; the checker is not part of `make check`.

## Figure

The figure is in Plain-Language Model (`fig:ch42-safety-case-join`). Canonical source [`figures/ch42-safety-case-join.dot`](../../../figures/ch42-safety-case-join.dot); render with `dot -Tpdf`. Caption carries the title and the arrow key.

- The Lean graphs (`context/lean_proof_graphs/01`–`04`, and `context/lean_proof_dependency_graph.dot`) are theorem ids. Appendix I keeps them. `00-overview.dot` is the right compression but the wrong labels for a reader who has not met `P02` and `MB7a`, and its `P02` node still says seven layers and omits grounding. The chapter points at that overview only after the label matches the join. It does not reprint it.
- The field bridge graph (`reference/field-agendas/graphs/mb-bridge-dependencies-v2.dot`) is one node per bridge, in field nouns (Inner Alignment, Tiling, Goodhart), including `MB8`, `MB10`, `MB4`, `MB4a`, and `MB7d`. Its black edges into `MB11` restate the flat layer join. That picture stays on the field overview. This chapter assembles proofs and bridges, and its nouns are the earlier chapters' deliveries.

**Reading.** Height is assembly: more independent deliveries above, the package then `SafeFor` below. A solid arrow means this is an input, and the spine discharges it. A dashed red arrow means this is an input, and a named bridge warrants it. Every `MB*` tag sits on a dashed red arrow; there are no solid bridge arrows. Arrows into the package are conjunctive assembly, not sequence; their style follows the warrant. `MB11` + tolerance is the only arrow out of the package, and it is a bridge.

There is no cycle. Selection takes successor and risk from correction (solid, downward). `MB6` does not feed back into that box: it warrants two *join* conjuncts, `CorrectionIntegrity` and the supporting basin. Those are not inputs to Chapters 25–31. The earlier same-row drawing treated `CorrectionIntegrity` as if it lived in the correction box, which made a false loop. `MB7` is the same kind of arrow: adversarial robustness is a join conjunct, not an input to the correction chapters, so it goes to the package, not back into the correction box.

Four boxes. Inside each box, the delivery this chapter uses, with the chapter that introduced it:

1. **Boundary and measurement.** Ch. 7 (the boundary), Ch. 9 (the composite), Ch. 11 (capability). Grounding, introduced in Ch. 3, is named in this box: the overview puts `GroundingViable` on Spine I, and the bridge tag is `MB9`.
2. **Value and transport.** Ch. 16 (the value bundle), Ch. 18 (bearer maps), Ch. 23 (whether the goal survived transport).
3. **Correction and successors.** Ch. 25 and Ch. 26 (correction as a causal channel, CCI), Ch. 30 and Ch. 31 (successors and conserved properties). The numeric leaf, control within CCI slack, sits on this box.
4. **Selection.** Ch. 34 (the environment selects for correction or against it).

Edges, in those words, taken from the overview. Do not invent edges.

- Boundary → value: the measured system has to be the real one before bundle geometry is readable.
- Boundary → correction: handles and control reach.
- Value → correction and successors: transport and bearer maps.
- Correction → selection: successor and risk exports (one way; Selection sits below).
- Bridge-warranted edges, dashed red, one tag each, not a node per split letter. Into the package, not back into a prior box: boundary and grounding (`MB1`, `MB9`); bundle and bearer (`MB2`, `MB3`); successor (`MB5`); adversarial robustness (`MB7`; Ch. 27 and Ch. 39 prior, Ch. 43 later); basin and correction integrity (`MB6`). Package to `SafeFor`: `MB11` + tolerance. Solid into the package: the numeric leaf.
- All four boxes → the safety-case package. The join is conjunctive: one missing export blocks it. Style of each join arrow follows the warrant (solid or dashed), not a third kind of arrow.

Bridge ids are edge tags. No `P`-numbers on this figure. No `MB4`, `MB4a`, `MB8`, `MB10`, or `MB7d`. Ch. 41 (multiscale decomposition) is a method used inside the checks, not a fifth box. The formal section refers to this figure, names the eight export predicates as the contents of the join, and does not repeat them in a table.

When the overview's cross-spine edges change, this figure changes. It is not generated from Lean and not copied from the field graph.

## Changes to Chapter 42

P1 prose pass closed 2026-10-05. Closed items deleted here. See session log `2026-10-05-ch42-p1-pass.md`.

Remaining after this pass: confirm `lean.status = proved` entries with `#print axioms` or `formal/axiom-ledger.json` before citing them as proved. 2.0 work stays below.

Not changed (intentionally informal): `Open` leaf kind; observable / i.i.d.-robust predicates have no Lean term; the extract marks them `none`. "Refusal condition" is now an instance of refuse.

## Work for 2.0 (do not do in this pass)

Recorded in `drafts/plans/construct/construct.md` (checklist) and `drafts/plans/spine/spine.md` (2.0 bullet):

- Book-wide parameterization scheme: one scheme for the arguments of `Safe`, `RiskGap`, the eight export predicates, bridges and construction objects, stated once where it matters, with the context-parameter convention of principle 3. Today `P` is explicit for `Realizes`/`TargetRealizable`/`CertifiedAsRealizing` but implicit for `Safe`; `κ` is explicit in `AdversariallyVerifiableUpTo` but not in the bridges that rely on it; `D`, `T`, setting are not arguments (stub: `DeclaredSetting`, `SafeIn` in `Evidence.lean`). No `AlignmentContext` n-tuple.
- G2: restate `MB6b`/`MB7b`/`MB7c` with `AdversariallyVerifiableUpTo chan (capability A)` as a true antecedent; thread it through `BridgeLayerInputs`; update `SpineModel`, axiom ledger, `check_spine_model.py`.
- Completeness of the joined exports: derive or bound, or state as an explicit crux.
- Assembly follows the four spines. The join takes their exports; the 8-way conjunction stays only as a view used by the blocking lemma. Drop `DirectLayerEvidence` and `BridgeDerivedLayerEvidence`. A bridge is an edge on a spine, not a member of a flat record that the theorem happens to consume. Before any chapter cites `00-overview.dot`, correct its `P02` label so it names the eight exports, including grounding.

Spine items to consider in a separate Lean session (small, not 2.0): connect `FiniteProvenDef` to the join or demote `P40` to a documented generic lemma; resolve `SatisfiesInvariants := LayeredAlignedDef` (root conjuncts 2 and 3 coincide; drop or give it ch48 content).

## After the pass

1. Repair or delete extract records for edited sentences; re-run the checker.
2. `./build.sh`, `make check`.
3. Session log in `drafts/conversation-summaries/`; delete closed items here.
4. Extract the next chapter (Ch. 25 proposed) and compare flag histograms.
