# Claim-extract lane

Status: open. **Pilot closed 2026-10-05** (Ch. 42, commit `5b474be47`). **Rollout:** same instrument for every manuscript chapter.

Instrument: one `metadata/claim-extracts/chNN.jsonl` per chapter (one record per load-bearing sentence: formal line, qualifier, Lean referents, flags; schema and stop rule in `metadata/claim-extracts/README.md`). Check with `python3 scripts/check_claim_extract.py`. Records are cited as `chNN.NNN`.

Stop rule: an item is closed when the chapter or plan was changed and the affected records re-checked, or the author wrote "keep as is" here. Closed items are deleted from this file with a session-log note.

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

## Pilot: Chapter 42 (closed)

P1 prose pass closed 2026-10-05. Session logs: `2026-10-02-claim-extract-pilot.md` through `2026-10-05-ch42-p1-pass.md`.

Remaining on Ch. 42 only: confirm `lean.status = proved` entries with `#print axioms` or `formal/axiom-ledger.json` before citing them as proved.

Not changed (intentionally informal): `Open` leaf kind; observable / i.i.d.-robust predicates have no Lean term; the extract marks them `none`. "Refusal condition" is now an instance of refuse.

Principles §1–§8 and the join figure below are the **template** for spine-heavy chapters; most chapters will not need a chapter-local assembly figure.

## Rollout to all chapters

Goal: every manuscript chapter has a checked extract. Load-bearing prose is aligned with the Lean spine at the same name when a name exists; where it does not, the extract still makes the warrant explicit (`lean: none` is allowed and flagged). Divergences are flagged rather than hidden.

Scope: `metadata/book.yml` chapters `ch01`–`ch48` (main text). Appendices after the main run, starting with load-bearing ones (App I, App P). One JSONL per chapter; full chapter body including Summary, excluding `\printbibliography` / references-only sections unless a sentence there is load-bearing.

Per chapter (repeat until all `chNN.jsonl` exist and checker-clean):

1. Extract load-bearing sentences (same schema as Ch. 42).
2. `python3 scripts/check_claim_extract.py metadata/claim-extracts/chNN.jsonl` → 0 errors.
3. Prose pass only where flags require repair (surgical; principles §1–§8 where they apply). Informal chapters still get the unhedged-universal / hidden-premise pass; they do not need a chapter-local assembly figure.
4. Session log; compare flag histogram to prior chapters; retire unused flags from the vocabulary when nothing needs them.

Do not treat `formal_density` in `metadata/book.yml` as the queue. High density is one input. The stale examples (Ch. 33, 43, 48 as “high”) do not match the YAML.

### Two value lenses (same schema)

Score a chapter on both; the queue below is their combination, not density rank.

1. **Spine names.** Prose uses Lean predicates or bridges at the same name (join exports, CCI, boundary, bundle, successor, verifiability). Payoff: principle §1 (prose claims no more than the spine). Typical: 7, 16, 25–27, 30–31, 43.
2. **Informal warrant.** Low-formula argument that still changes a decision: thesis, scope, folklore, selection, consent, lethality, artifacts. Payoff: auto-formalize “therefore” chains; `lean: none` is a result, not a skip. Reader/funder appreciation is part of the score, not a side effect. Typical: 1, 4, 5, 28–29, 34, 36–38, 44–45.

Low density alone is not a reason to go early (Ch. 2, 47). Synthesis chapters (Ch. 48) wait until source extracts exist. Reorder when a chapter edit makes another urgent.

### Combined queue

Ch. 42 is done (`ch42.jsonl`). Ch. 1 extract is done; its prose items are open (below). **Next is Ch. 5.** Do not start a pass until the author asks.

- [~] **Ch. 1** — extract `ch01.jsonl` checker-clean; surgical prose applied 2026-10-16; author-decision items in § Ch. 1 still open.
- [ ] **Ch. 5** — assumptions and failure coverage as an informal ledger.
- [ ] **Ch. 25** — correction channel; join delivery; recent `Pers` / `Auth_k` edits.
- [ ] **Ch. 7** — boundary; `BoundaryAligned` / `MB1`; join box 1.
- [ ] **Ch. 26** — CCI; `CorrectionIntegrity`; numeric leaf.
- [ ] **Ch. 44** — lethality stress test; field-reader heat; mostly informal warrants.
- [ ] **Ch. 16** — value-bundle model; `BundleTransport` / `MB2`.
- [ ] **Ch. 34** — selection; join box 4; `MB6`; socio-technical prose.
- [ ] **Ch. 43** — verifiability / representability; G0 gate; `AdversariallyVerifiableUpTo`.
- [ ] **Ch. 31** — conserved properties; `SuccessorStable`; `MB5` / `MB10`.
- [ ] **Ch. 29** — manipulation, domestication, false consent; policy-adjacent universals.
- [ ] **Ch. 30** — successor creation as the inheritance test (extract with 31 in mind).
- [ ] **Ch. 38** — conductive artifacts and pivotal processes; funder/decision prose.
- [ ] **Ch. 23** — whether the goal survived transport.
- [ ] **Ch. 11** — capability without task ontology; join box 1.
- [ ] **Ch. 27** — correction under adversarial pressure; feeds `AdversariallyRobust`.
- [ ] **Ch. 4** — fixed values as the wrong target; philosophical load-bearing.
- [ ] **Ch. 3** — dynamical guarantee; grounding / `MB9`.
- [ ] **Ch. 37** — alignment attractor; metaphor vs claim.
- [ ] **Ch. 36** — parasites in the correction system.
- [ ] **Ch. 28** — beyond following instruction; RLHF-era folklore.
- [ ] **Ch. 18** — bearers; `BearerTransport` / `MB3`.
- [ ] **Ch. 9** — composite agent; who the real optimizer is.
- [ ] **Ch. 32** — better self-modeling can be worse.
- [ ] **Ch. 45** — value-update envelope; Part 10 thesis.
- [ ] **Ch. 33** — certification without construction; `Certified` vs safety-case naming.
- [ ] **Ch. 10** — strategic opacity; high density, not a join export.
- [ ] **Ch. 8** — grow, split, merge; forgeability neighborhood.
- [ ] **Ch. 24** — words survive, meaning does not.
- [ ] **Ch. 21** — from rewards to values.
- [ ] **Ch. 22** — compression test for intention.
- [ ] **Ch. 20** — measuring and stress-testing bundle geometry.
- [ ] **Ch. 19** — tradeoffs and bundle geometry.
- [ ] **Ch. 17** — when low dimensionality helps.
- [ ] **Ch. 15** — values as compressed control signals.
- [ ] **Ch. 12** — capability growth as boundary expansion.
- [ ] **Ch. 14** — when intelligence deepens misalignment.
- [ ] **Ch. 13** — coordination bottleneck.
- [ ] **Ch. 6** — agent without anthropomorphism.
- [ ] **Ch. 35** — multi-agent inferential coupling.
- [ ] **Ch. 40** — detecting goal laundering.
- [ ] **Ch. 41** — checking a system at every level (method inside checks, not a fifth join box).
- [ ] **Ch. 39** — passive observation is not enough.
- [ ] **Ch. 46** — end of unconscious value drift.
- [ ] **Ch. 47** — who still counts; after bearers (18/24).
- [ ] **Ch. 2** — artificial civilization; framing, few decision-changing chains.
- [ ] **Ch. 48** — closing synthesis; last among main text so it does not replay unextracted claims.
- [ ] **Appendices** (App I, App P, …) after `ch48`.

Infrastructure (do early in rollout, not per chapter):

- [x] `scripts/check_claim_extract.py` resolves any `chNN.jsonl` to the unique `chapters/chNN-*.tex`.
- [ ] Line drift: chapter edits shift `lines` and fail every later record although the quotes still exist (Ch. 42 after the FLI and Market commits; relocated 2026-10-16). Decide between a `--relocate` mode in the checker and re-running the extractor's span fill after each chapter edit.
- [ ] Optional: wire the checker into `make check` once a threshold of chapters is clean (author decides threshold).
- [ ] Optional: extraction prompt/spec document if manual extract quality drifts across agents.

Done for the lane: all scoped chapters have checker-clean JSONL; cross-chapter flag histogram reviewed; remaining open items are 2.0 spine work or author "keep as is" on flagged records.

## Ch. 1 (extract done; surgical applied; author decisions open)

Extract: `metadata/claim-extracts/ch01.jsonl`. Surgical phrase-level items applied 2026-10-16 (session `2026-10-16-ch01-claim-extract.md`); records re-checked. Remaining items close when the chapter is edited and the cited records are re-checked, or the author writes "keep as is" here.

**Finding.** The chapter states its selection criterion in several forms, and they still disagree: best predicts (`ch01.024`), helps predict (`ch01.029`), loop persistence (`ch01.034`), prose cost comparison (`ch01.044`; the displayed inequality was removed), argmax without the boundary residual (`ch01.087`), and Ch. 7's `J(C) = R − αP + λΩ`, which keeps the boundary residual that Ch. 1 drops. Related open flags: one object or several (`ch01.036`, `ch01.058`, `ch01.066`), several names for the object (`ch01.081`).

Author decisions (argument, not phrasing):

- [ ] `ch01.036`, `ch01.058` — the boundary-error definition presumes a unique risk system; the chapter allows several. Pick a reading ("not among", coverage).
- [ ] `ch01.037` — the four forms mix two axes (extent: narrow, wide; resolution: timescale, abstraction) and miss "misplaced". This is the chapter's stated contribution.
- [ ] `ch01.073` — "moving equivalence class": tolerance-preservation is not transitive. Equivalence under exact preservation, or a chain of admissible transitions?
- [ ] `ch01.087` vs `ch01.003` — which is the key claim, the ordering or the selection rule?
- [ ] `ch01.090` — the second falsifier asks for a proof of non-localizability; consider an empirical version.

Spine (Lean gaps, record only; not chapter work):

- `ch01.003`, `ch01.008`, `ch01.014` — the object slot is the `System` argument, fixed outside the spine. No relation links the evaluated system to the risk-determining one, and no map links `System` to the `Boundary` record that `MB1` speaks about. A case can be valid for A and yield `Safe A` through `MB11` while the risk sits in a larger A'.
- `ch01.061` — `BoundaryAligned` is not risk-indexed; Ch. 1 implies one boundary per risk inside one case (principle 3 fixes `T` per case).
- `ch01.084` — `MB1` has no `AdversariallyVerifiableUpTo` antecedent although the chapter names boundary camouflage; candidate for the G2 list.
- `ch01.041` — "alignment is a property of a trajectory"; the join predicates take a `System`.

Lean support worth one clause in the chapter: `ch01.068` (`P09`, `P36`, "passive observation is weak"), `ch01.085` (finding the optimizer is necessary, not sufficient: one conjunct of `LayeredAlignedDef`). Confirm with `#print axioms` first.

## Work for 2.0 (do not do in this pass)

Recorded in `drafts/plans/construct/construct.md` (checklist) and `drafts/plans/spine/spine.md` (2.0 bullet):

- Book-wide parameterization scheme: one scheme for the arguments of `Safe`, `RiskGap`, the eight export predicates, bridges and construction objects, stated once where it matters, with the context-parameter convention of principle 3. Today `P` is explicit for `Realizes`/`TargetRealizable`/`CertifiedAsRealizing` but implicit for `Safe`; `κ` is explicit in `AdversariallyVerifiableUpTo` but not in the bridges that rely on it; `D`, `T`, setting are not arguments (stub: `DeclaredSetting`, `SafeIn` in `Evidence.lean`). No `AlignmentContext` n-tuple.
- G2: restate `MB6b`/`MB7b`/`MB7c` with `AdversariallyVerifiableUpTo chan (capability A)` as a true antecedent; thread it through `BridgeLayerInputs`; update `SpineModel`, axiom ledger, `check_spine_model.py`.
- Completeness of the joined exports: derive or bound, or state as an explicit crux.
- Assembly follows the four spines. The join takes their exports; the 8-way conjunction stays only as a view used by the blocking lemma. Drop `DirectLayerEvidence` and `BridgeDerivedLayerEvidence`. A bridge is an edge on a spine, not a member of a flat record that the theorem happens to consume. Before any chapter cites `00-overview.dot`, correct its `P02` label so it names the eight exports, including grounding.

Spine items to consider in a separate Lean session (small, not 2.0): connect `FiniteProvenDef` to the join or demote `P40` to a documented generic lemma; resolve `SatisfiesInvariants := LayeredAlignedDef` (root conjuncts 2 and 3 coincide; drop or give it ch48 content).

## After each chapter pass

1. Repair or delete extract records for edited sentences; re-run the checker.
2. `./build.sh`, `make check` when the chapter prose changed.
3. Session log in `drafts/conversation-summaries/`; delete closed items here.
4. Queue the next chapter from **Rollout** above.
