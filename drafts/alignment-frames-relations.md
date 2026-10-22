# How Alignment Frames Combine

This note classifies relations among the frames in [alignment-frames-by-object-and-measure.md](alignment-frames-by-object-and-measure.md). It does not add frames. A graph with one edge style per relation is [alignment-frames-relations.dot](alignment-frames-relations.dot) ([SVG](alignment-frames-relations.svg)).

The words below are used in one sense each.

- **Specializes.** Every instance of the source is an instance of the target once a named restriction holds. The source is the narrower frame.
- **Projects.** A many-to-one map sends the source onto the target and discards structure. The target cannot recover the source.
- **Encodes.** Objects of the source can be represented as objects of the target under stated assumptions. The induced claim may match. The original objects remain distinct, and the encoding can fail to be observable or hard to fake.
- **Isomorphism.** A representation theorem gives an inverse, up to a named equivalence such as an additive constant or an affine transformation.
- **Summand.** The source decomposes as a direct sum, and each summand is a frame with an inverse on that component.
- **Limit.** The target is what the source becomes at a named boundary of a parameter.
- **Strengthens.** Same object and same acceptance shape, with a stronger quantifier.
- **Composes.** The two claims can be true together because they have different roles: target, constraint, guarantee, or warrant. Composition is not implication.
- **Incompatible.** In a named class of situations, the two acceptance relations cannot hold together. Outside that class they may still compose.

No pair of frames in this inventory is a dual in the sense that one theory is the dual of the other. The two near-misses are recorded at the end.

## Summands inside route value

On a fixed directed graph, an additive value of a path is the sum of a value \(r\) on its edges. Two facts from Hallgren's unpublished draft v0.7, under the reachability assumption stated there, separate this family.

If every state is reachable from a fixed start, path worth depends only on the final state exactly when \(r\) is an exact potential: each edge scores the utility of its target minus the utility of its source. On a reachable graph, every such \(r\) arises from some state utility \(U\), but \(U\) is determined only up to an additive constant, so the state-labeled object is not interchangeable with the route-labeled one. **State utility** therefore **specializes** additive route value: it pins worth to states and induces an exact potential on edges. It is not a different scale on the same object, and it is not an isomorphism of frames with exact potential despite the shared policy ranking on reachable endpoints.

The complementary summand is the cycle component. Every state utility scores every round trip at zero. A walk, a conversation, or a revision that returns to the same state and is still worth taking lives only in the cycle component. Endpoint-only acceptance and a nonzero round-trip value are incompatible acceptance relations on the same edges.

In an unending process scored by the long-run average of \(r\), adding an exact potential does not change the average. The long-run average projects additive route value onto its cycle summand and drops the state-utility summand. A pure state utility then supplies no steering signal for that criterion. Discounted potential-based shaping, \(F(s,a,s')=\gamma\Phi(s')-\Phi(s)\), is a different relation: under the assumptions in Ng, Harada, and Russell (1999), it leaves the optimal policy unchanged and does not leave the edge values or the finite-horizon returns unchanged. Policy equivalence is not an isomorphism of the value frame.

## Encodings

A finite history can be written into an enlarged state, and a state utility on that enlargement can reproduce a history preference. Route labels can likewise be copied into the state. Temporal constraints can be rewritten as reachability or invariance on a product with an automaton. These are encodings. They are isomorphisms of the induced claim relative to the chosen product, and they are not isomorphisms of the original state space.

The cost sits in the conditions the spinout draft already names: the added coordinates have to be observable, stable under a change of ontology, and costly to fake. An encoding that hides the route bit in an unmeasured coordinate is compatible with the mathematics and useless as an audit.

An open procedure such as coherent extrapolated volition can be encoded as a state utility by scoring only the procedure's output. That encoding drops the commitment to leave the output unset. It is available. It is a different frame.

## Projections and limits

A distribution over outcomes projects to a state or history value by a choice functional. Expectation is one such projection. A tail functional such as CVaR is another. In the convention where the level selects the lower tail of return, one end of the level approaches the mean and the other approaches the worst case. The two projections agree on degenerate distributions and come apart as soon as the distribution has a tail. Expectation does not imply a tail bound.

A vector of criteria projects to a scalar once weights are chosen. The weighted scalar specializes the vector problem only after those weights are fixed. A lexicographic order also specializes the vector problem, by imposing a strict priority rather than by projecting. The Pareto front is a solution concept for the vector, not a scalar frame. Fixed finite weights do not represent a lexicographic priority: a large enough gain on a lower coordinate can cross any finite exchange rate.

A quantilizer approaches unconstrained maximization as the retained quantile approaches the top of the base distribution. The limit depends on the base. If the base already contains judge-shaping acts, the limit still contains them.

Act-level approval specializes route or act evaluation to one proposed act and one overseer's stated judgment. It does not project onto, and does not specialize, a future correction relation. A predictor fitted to past approval is a method for estimating that local score.

The correction relation projects onto classical corrigibility by retaining one handle, shutdown or modification, and one class of operators. Shutdown is a one-bit projection. The inverse does not exist: a system can accept shutdown and still capture the process that decides whether shutdown is requested.

Learned reward is not an inverse of observed behavior. Many rewards can rationalize the same choices. Inference is a method that selects an element of whatever target class was hypothesized: state rewards, route rewards, or approval scores. Partial identification blocks an isomorphism between behavior and the target.

## What composes

Composition is legal when the frames occupy different roles and the interfaces in the spinout draft are stated.

A non-compensatory constraint defines an admissible set. Inside it, a cycle-sensitive route value can rank learning above rewiring even though the endpoints match. A human-power aggregate or a welfare score can then choose among admissible routes. A task scalar comes after those constraints. Non-obstruction is a pointwise floor on one human's attainable-utility landscape. Attainable-utility preservation is a soft penalty on movement of a related landscape. They compose with each other as floor and penalty. Neither one is the correction relation.

Viability composes with a supplied set. If the set is the set of states in which the correction relation still clears its thresholds, viability is the persistence claim for that relation. Selection stability composes in the same way when the selector is part of the dynamics being closed. A safety case composes as a warrant: proofs, monitors, and control protocols are leaves. A model-relative proof certifies the property written in the specification. A control protocol supplies evidence under an intentional-subversion assumption. Neither leaf chooses the correction relation.

Human power composes as a positive direction inside the admissible region. It can also be used as a rival top-level target that treats correction as instrumental. Those are different compositions. The graph draws only the first.

## What is incompatible

These conflicts are acceptance conflicts in a stated class. They are not claims that the formalisms cannot appear in one document.

Endpoint-only state utility and a nonzero value for a round trip cannot both be the value of the same edges. The first forces every round trip to zero.

A state utility that scores every change of itself by its current values rejects any change that would make it choose an outcome it currently ranks lower, whether the change comes from learning or from rewiring. Changes that leave its chosen outcome as good by its own lights are not resisted. A correction relation that endorses some changes of the value-bearing process requires the opposite verdict on those changes. The conflict is lifted if the utility is redefined over a larger object that already includes the endorsed update. That redefinition is an encoding into a different frame, not a reconciliation inside fixed state utility.

A non-compensatory ban and an unrestricted weighted scalar are incompatible when a finite task gain can buy the banned act. An exact-penalty theorem can restore equivalence for a particular program. The equivalence is not free.

Pointwise non-obstruction over a goal set rejects a policy that spends one of those goals to raise another. A scalar objective that permits that trade is incompatible with the pointwise floor on that set.

Agent empowerment and a human-power aggregate are incompatible in situations where the agent's action-to-sensor channel grows by narrowing the humans' attainable goals. They are compatible in situations where both channels widen. The red edge in the graph is restricted to the first class.

Robust invariance quantifies over a class of disturbances. A correction is an external input too. If correction inputs belong to that class and a legitimate correction aims at a state outside the invariant set, the correction cannot take effect. Counting a correction as a disturbance is the same as requiring the set to be closed under that correction. Existential viability is not in this conflict, because "some control stays in the set" leaves the corrector free to steer elsewhere. The coherent form separates adversarial inputs, against which the set is invariant, from correction inputs, which must stay effective. That split only helps if the system cannot decide which inputs count as corrections.

A special case is a set in which every state is captured. There, robust invariance is lock-in: the stability that makes the set look safe also keeps correction from ever being live. Robust invariance does not distinguish such a set from a good one, which is why stability needs a sign before it counts as a guarantee.

## Quantifiers, and the duals that are not here

Existential viability says some admissible control stays in the set. Robust invariance says the chosen control stays in the set under every disturbance in a named class. The second strengthens the quantifier. It is not a dual theory of the first, and the first does not imply the second.

In temporal logic, the De Morgan dual of "always \(\varphi\)" is "eventually not \(\varphi\)." Liveness, "eventually \(\psi\)," is a companion requirement for a correction handle that must be usable in time. It is not that dual.

A constrained optimization program has a Lagrangian dual. Under constraint qualifications, penalties and multipliers can represent the constrained program. That is a conversion of one optimization problem. It does not make a rights constraint and a scalar reward into dual frames. Where the qualification fails, the penalty form and the hard constraint come apart, which is the incompatibility already stated.

## How to read the graph

[alignment-frames-relations.dot](alignment-frames-relations.dot) uses eight edge kinds.

| Edge | DOT | Meaning |
| --- | --- | --- |
| Specializes | solid arrow, special case → general frame | The source is the target plus a named restriction. |
| Projects | dashed arrow | A many-to-one map. The target does not determine the source. |
| Encodes | dotted arrow | A representation under stated assumptions, without identity of the original objects. |
| Isomorphic summand | bold arrow, both directions | A direct-sum component with an inverse on that component. |
| Limit | dashed orange arrow | The target is a parameter boundary of the source. |
| Strengthens | purple arrow | Same shape, stronger quantifier. |
| Composes | green arrow | Different roles, conjoined only with the stated interface. |
| Incompatible | red, no direction | The named acceptance relations exclude each other in the named class. |

Green arrows are the correction-centered composition from the spinout draft: constraints, then route residue and human power inside the region, then viability of that supplied set, then a safety case whose leaves include proof and control. A power-centered composition would draw different green arrows. The red edges are not a claim that those nodes cannot be discussed together.

Variant **b** adds a **Certification geometry** cluster (coordinate floor gate, correction certificate, scalar risk-gap leaf, deployment preserve tuple) and TSA-facing edges; see [alignment-frames-relations-b.dot](alignment-frames-relations-b.dot) ([SVG](alignment-frames-relations-b.svg)). The default graph above is unchanged.

Variant **c** keeps only nodes incident to **compose**, **isomorphic summand**, or **incompatible** edges (union of the default graph and **b**); see [alignment-frames-relations-c.dot](alignment-frames-relations-c.dot) ([SVG](alignment-frames-relations-c.svg)).

## Interface types on graph nodes

The compact graphs label nodes by name only. A **full** relations diagram—one that could support a commuting diagram checked against explicit maps—should attach at least a **compact interface type** to each node:

\[
\texttt{Interface} = (\text{role},\ \text{object-kind},\ \text{assessment-kind}).
\]

**Role** is one of **Target**, **Constraint**, **Guarantee**, or **Protocol** (warrant and assurance live under Protocol), as in the inventory's four mandatory labels ([alignment-frames-by-object-and-measure.md](alignment-frames-by-object-and-measure.md), typed record). **Object-kind** and **assessment-kind** are short names for the inventory's **object** and **assessment** fields, not a replacement for the full eight-tuple `(boundary, principals, object, assessment, temporal rule, quantifiers, solution concept, warrant)`.

When a node is used in more than one role in different compositions, the table gives the **primary** role for that interface type. Green **compose** edges then mean conjoining claims whose roles differ; specialize, project, encode, summand, limit, and strengthen edges are **typed morphisms** between interfaces (many-to-one, restriction, representation, …). A formal check would state a map on objects and assessments and verify that the target acceptance is preserved or that the named failure mode is explicit (projection loses information; encoding may be unobservable).

Controlled vocabulary for the last two columns (extend only with a named entry in the inventory):

| object-kind | Typical assessment-kind |
| --- | --- |
| `state` | scalar order, threshold membership |
| `history` | preference / value on trajectories |
| `route` | additive path score |
| `route-exact` | exact potential on edges |
| `route-cycle` | cycle / round-trip residue |
| `lottery` | expectation, tail functional |
| `criteria-vector` | Pareto, weighted scalar, lex order |
| `single-act` | local approval score |
| `quantile-base` | quantilizer retention |
| `human-AU-landscape` | on–off floor, option penalty |
| `human-power-channel` | aggregate capacity order |
| `agent-power-channel` | empowerment / channel capacity |
| `corrigibility-handles` | named intervention acceptance |
| `correction-relation` | relation + channel profile |
| `open-procedure` | unset output; legitimacy or scored halt |
| `deontic-admissibility` | forbid / obligation on acts or coordinates |
| `dynamics+set` | ∃ viability kernel |
| `dynamics+set` | ∀ controlled invariance |
| `selection-population` | invasion resistance / signed basin |
| `formal-model+spec` | proof relative to model |
| `deployment-under-threat` | control / monitor protocol |
| `deployment-claim` | safety argument + residual risk |
| `coordinate-vector` | componentwise floor (θ) |
| `correction-certificate` | vector CCI vs θ_corr |
| `scalar-risk-gap` | control ≤ CCI + δ |
| `deployment-vector` | preservation tuple membership |

### Node registry (DOT id → compact type)

Nodes in **variant b** only are marked †. **Variant c** is the subset of rows that appear in [alignment-frames-relations-c.dot](alignment-frames-relations-c.dot); all other rows belong to the default graph **a** ([alignment-frames-relations.dot](alignment-frames-relations.dot)).

| DOT id | Graph label (short) | `(role, object-kind, assessment-kind)` | Notes |
| --- | --- | --- | --- |
| `route` | Additive route value | `(Target, route, additive path score)` | Parent of exact ⊕ cycle summands |
| `exact` | Exact potential | `(Target, route-exact, exact potential on edges)` | Specializes `route`; endpoint-only acceptance |
| `cycle` | Cycle component | `(Target, route-cycle, round-trip / residue score)` | Summand; composes inside admissible region |
| `state` | State utility | `(Target, state, scalar order on states)` | Induces exact potential on reachable graphs |
| `hist` | History value | `(Target, history, trajectory preference)` | Encodes into augmented `state` |
| `dist` | Distribution over outcomes | `(Target, lottery, expectation or risk functional)` | Projects to `state` under chosen functional |
| `criteria_vector` | Criteria vector (Pareto · task costs/stakeholders) | `(Target, criteria-vector, multi-objective order)` | Not flat-composable with `cci_cert` without order |
| `weighted_scalar` | Weighted scalar (fixed weights on criteria) | `(Target, criteria-vector, fixed-weight scalar maximize)` | Weights on task/cost/stakeholder coordinates |
| `lex` | Lexicographic priority (on criteria vector) | `(Target, criteria-vector, lexicographic priority)` | Specializes `criteria_vector` |
| `quant` | Quantilizer (retained quantile of base) | `(Target, quantile-base, quantile retention on base)` | Limit toward max under stated base |
| `approval` | Act approval score (Protocol · one edge) | `(Protocol, single-act, local approval score)` | Specializes one edge of `route`; partial monitor for CCI |
| `au_penalty` | Human AU landscape · soft penalty (AUP) | `(Constraint, human-AU-landscape, soft penalty on movement)` | Same landscape family as `au_floor` |
| `au_floor` | Human AU landscape · on–off floor (non-obs.) | `(Constraint, human-AU-landscape, on–off pointwise floor)` | Counterfactual goals fixed in the claim |
| `human_power` | Human-power aggregate | `(Target, human-power-channel, aggregate capacity order)` | Composes as positive direction, not rival top-level here |
| `ai_power` | Agent empowerment | `(Target, agent-power-channel, empowerment functional)` | Red edge class: channels diverge |
| `corrig` | Corrigibility | `(Constraint, corrigibility-handles, shutdown/mod acceptance)` | Specializes `correction` |
| `correction` | Correction relation (handles + channel profile) | `(Target, correction-relation, relation + channel profile)` | TSA relational target; scored by `cci_cert` when certified |
| `cev` | Open procedure (CEV) | `(Target, open-procedure, deliberative / unset output)` | Encoding to `state` drops revisability |
| `deontic` | Non-compensatory constraint (forbid traded violations) | `(Constraint, deontic-admissibility, forbid compensatory trade)` | Defines admissible region; coordinate floors → `cci_cert` |
| `coord_floor` † | Coordinate floor gate (componentwise θ) | `(Constraint, coordinate-vector, componentwise θ floor)` | Specializes vector gate pattern |
| `cci_cert` † | Correction certificate (CCI vs θ_corr · not task vector) | `(Constraint, correction-certificate, vector CCI vs θ_corr)` | Assessment **on** `correction-relation`; not task `criteria_vector` |
| `risk_leaf` † | Scalar risk-gap leaf (control ≤ CCI + δ) | `(Protocol, scalar-risk-gap, control ≤ CCI + δ)` | Arithmetic warrant leaf after vector gate |
| `preserve_tuple` † | Deployment preserve tuple (coordinates for K) | `(Constraint, deployment-vector, tuple / coordinate preservation)` | Supplies deployment coordinates to viability / selection |
| `viable` | Existential viability (∃ control in supplied K) | `(Guarantee, dynamics+set, ∃ control in supplied set K)` | K often “correction still clears thresholds” |
| `robust` | Robust invariance (∀ disturbance in class) | `(Guarantee, dynamics+set, ∀ disturbance in class)` | Strengthens quantifier over `viable` |
| `selection` | Selection stability | `(Guarantee, selection-population, invasion resistance / signed basin)` | Selector inside closed dynamics |
| `proof` | Model-relative proof | `(Protocol, formal-model+spec, proof relative to model)` | Leaf evidence; does not pick target |
| `control` | Control protocol | `(Protocol, deployment-under-threat, monitor / control satisfaction)` | Subversion model explicit in claim |
| `safecase` | Safety case | `(Protocol, deployment-claim, structured argument + residual risk)` | Warrant wrapper; conjuncts leaves |

### Toward a checkable commuting diagram

The edge legend above is already a **kind** of morphism (specialize, project, encode, …). A machine-checkable layer would add, for each edge `source → target`, a named map `f` on `(object, assessment)` and optionally on `(boundary, quantifiers)`, plus a proof obligation: e.g. **specialize** = inclusion of acceptance predicates; **project** = existence of a surjective forgetful map with no section; **encode** = representation with stated observability assumptions; **summand** = direct-sum decomposition with named inverse on that component; **compose** = product of claims in distinct roles with interfaces from the spinout draft ([alignment-frames-spinout-paper.md](alignment-frames-spinout-paper.md)). Squares commute only up to the equivalence named on summand and encoding edges (additive constant on state utility, affine ambiguity on route vs state, etc.). The compact graph deliberately omits these labels; this registry is the hook for a fuller DOT or Lean layer that does not change the inventory's frame entries.

## Formal layer (Lean)

Module: [`formal/AlignmentProofSpine/FrameRelations.lean`](../formal/AlignmentProofSpine/FrameRelations.lean) (orthogonal to `MB*` certification spine).

**Criterion.** An edge should be **derivable** when it is forced by typed structure, not when it is a narrative choice among compatible frames.

| Mechanism | What Lean defines | What variant **c** gets |
| --- | --- | --- |
| **Summand** | `summandPair` on `FrameNode` (inventory nodes for `route` / `exact` / `cycle`). Mathematical witness: `exact_potential_cycle_sum_zero` on a 3-cycle edge score (supports the `state`–`cycle` red edge). Full Helmholtz decomposition on general digraphs is not in this file yet. | The four bold summand edges only. |
| **Incompatible** | `incompatWitnesses` registry; every entry is backed by an `Incompatibility` instance in `FrameIncompatibility.lean` (`registry_matches_proofs`). | All red edges in **c**; a new red edge needs a new instance. |
| **Compose** | `ComposeSlot`: one constructor per **semantic** compose rule (landscape chain, admissible region, certificate geometry, guarantee stack, warrant leaves). `CorrectionCentered.compose` is `true` iff some slot matches. `roleCompose_necessary_slot` shows each slot passes the role gate. | Exactly the green edges in **c** — **not** the full role-compatible compose-closure. |

**Check.** `variantCEdges` lists every edge in variant **c**; `derivedEdgeKind` classifies pairs; `variantC_all_derived` (`native_decide`) shows the list agrees with the classifier.

**Why not a full commuting diagram yet**

1. **Compose is underdetermined by `(role, object-kind, assessment-kind)` alone.** Many pairs pass `RoleCompose` but are not in **c** (e.g. a power-centered reading would swap green arrows). Those readings should be alternate `ComposeSlot` families or parameters, not extra DOT ink without a Lean name.

2. **Specialize / project / encode** (graphs **a** / **b**) need **maps on carriers**, not just interface tags: e.g. `StateUtility → RouteValue` is a functor with a named ambiguity (additive constant; route bits in state). That is the **`FrameMorphisms`** registry (`MorphismSpec`, `mapId`); commuting squares on acceptance predicates are still mostly informal.

3. **Incompatible** reds are proved per conflict kind; see *Incompatibilities (Lean)* below.

4. **Summand** edges are **isomorphisms of assessment on a shared route carrier**; proving the direct-sum theorem for all finite graphs belongs in Mathlib-style graph cohomology, not in the inventory typing.

**Next steps (if this becomes load-bearing).** Generate DOT from `variantCEdges`; link `cci_cert` to `Correction.CCICertificate`; prove or import general `route = exact ⊕ cycle` on `Digraph`; add `limit` / `strengthen` to `MorphismSpec` or a sibling registry.

### Compose paths and slots (Lean)

Module: [`FrameComposePaths.lean`](../formal/AlignmentProofSpine/FrameComposePaths.lean). Each **`ComposeSlot`** belongs to exactly one **`ComposePathId`**; paths meet at hub nodes `correction`, `cci_cert`, `viable`, `safecase`.

| Path id | Intended track | Allowed edges `(src → tgt)` |
| --- | --- | --- |
| `landscapeHumanTarget` | Soft AUP → non-obstruction → human power → correction | `au_penalty→au_floor→human_power→correction` |
| `admissibleRegion` | Deontic admissible set | `deontic→correction` |
| `routeResidueInRegion` | Cycle residue inside region | `cycle→correction` |
| `certificateOnRelation` | Floors + relation scored + **K** | `deontic→cci_cert`, `correction→cci_cert`, `correction→viable`, `cci_cert→viable` |
| `certificateEvidence` | Warrant leaves on coordinates | `proof|control|approval → cci_cert` |
| `guaranteeSuppliedSet` | Deployment tuple supplies **K** | `preserve_tuple→viable` |
| `selectionEcology` | Selector in closed dynamics | `preserve_tuple→selection`, `viable→selection` |
| `warrantBundle` | Safety-case conjuncts | `proof|control|cci_cert|correction → safecase` |

Checks: `all_slots_on_paths`, `paths_partition_slots`, `slots_have_unique_path`.

### Carriers and maps (graphs **a** / **b**)

Module: [`FrameMorphisms.lean`](../formal/AlignmentProofSpine/FrameMorphisms.lean). Nodes: **`FrameNodeExt`**. Each specialize / project / encode edge is a **`MorphismSpec`**: `srcCarrier`, `tgtCarrier`, stable **`mapId`**, optional **`EquivalenceNote`**.

| DOT edge | Kind | Carriers (src → tgt) | `mapId` | Commutes up to |
| --- | --- | --- | --- | --- |
| `exact → route` | specialize | exact summand → edge reward | `subspace.inclusion.exactPotential` | — |
| `approval → route` | specialize | single act + judge → edge reward | `restrict.oneEdgeOneJudge` | — |
| `weighted_scalar → criteria_vector` | specialize | criteria vector → criteria vector | `scalarize.fixedWeights` | weights fixed |
| `lex → criteria_vector` | specialize | lex priority → criteria vector | `prioritize.lexOrder` | strict priority |
| `corrig → correction` | specialize | handles → correction relation | `restrict.oneHandleNamedOperators` | named operators |
| `state → route` | specialize | bare state → edge reward | `induceGradient.exactPotential` | **additive constant on U** |
| `dist → state` | project | lottery → bare state | `expectationFunctional` | **no section** |
| `criteria_vector → weighted_scalar` | project | criteria vector → criteria vector | `forget.chosenWeights` | **no section** |
| `correction → corrig` | project | correction relation → handles | `forget.shutdownBit` | **no section** |
| `route → cycle` | project | edge reward → cycle summand | `longRunAverage.retainCycleSummand` | — |
| `hist → state` | encode | path → augmented state (history) | `appendHistoryToState` | **observability** |
| `route → state` | encode | edge reward → augmented state (route bits) | `embedRouteBitsInState` | **observability** |
| `cev → state` | encode | open procedure → scored output state | `scoreProcedureByOutputOnly` | **drops revisability** |
| `cci_cert → coord_floor` (**b**) | specialize | CCI vector → coordinate floors | `restrict.cciCoordinateFloors` | — |
| `correction → cci_cert` (**b**) | project | correction relation → CCI vector | `auditProfileUnderFixedProtocol` | fixed protocol |
| `preserve_tuple → cci_cert` (**b**) | project | deployment tuple → CCI sub-vector | `project.deploymentSubVector` | — |
| `cci_cert → risk_leaf` (**b**) | project | CCI vector (passed) → scalar gap | `scalarRiskGapAfterVectorGate` | — |

Informal domain/codomain strings live in `mapSignatures` (same module). Checks: `graphA_morphisms_typed`, `graphB_morphisms_typed`.

### Incompatibilities (Lean)

Module: [`FrameIncompatibility.lean`](../formal/AlignmentProofSpine/FrameIncompatibility.lean). A red edge is an `Incompatibility C` on a shared carrier `C`:

- `H`: a situation class stated in the carrier's vocabulary, not as "the frames disagree";
- `A₁`, `A₂`: what the two frames accept on `C`;
- `disjoint`: inside `H`, never both;
- `liveInH`: some situation in `H` is accepted by at least one frame, so the conflict bites;
- `boundary`: some situation outside `H` is accepted by both, so the edge is conditional on `H`.

Per-frame non-vacuity inside `H` was dropped from the template: a fixed-utility evaluator rejects *every* update in its conflict class, and that is the conflict, not a degenerate case.

| Red edge | Kind | Carrier | `H` | Boundary witness |
| --- | --- | --- | --- | --- |
| state–cycle | algebraic | edge reward with a walk | nonempty closed walk | open walk: a gradient may have nonzero path sum |
| deontic–weighted_scalar | floor vs trade-off | menu of (floor, gain) via `deonticToOpt` | a banned act's gain exceeds its floor loss at the exchange rate | gain too small: scalar picks the permitted act |
| au_floor–weighted_scalar | floor vs trade-off | same via `nonobsToOpt` (on minus off value of one goal) | as above | as above |
| cci_cert–weighted_scalar | floor vs trade-off | same via `cciToOpt` (CCI minus threshold) | as above | as above |
| criteria_vector–cci_cert | via projection | same, after `forget.chosenWeights` | as above | as above |
| state–correction | evaluator vs update | menu with (U, U') values, endorsed flag | update makes the agent pick an outcome U ranks strictly lower | update that keeps a U-optimal choice: both accept |
| ai_power–human_power | shared resource | option counts before/after | total options do not grow | pool grows: both gain |
| robust–correction | quantifier conflict | dynamics with adversarial and correction inputs, `K`, correction target | correction inputs are in the robustness class and the target lies outside `K` | corrections exempt from the robustness class: both hold |

General results beyond the instances:

- `gradient_closed_walk_zero`: on any vertex type, a reward induced by a state utility sums to zero on every closed walk.
- `no_finite_weights_represent_floor`: for every strictly positive finite weighting there is a menu with an admissible option on which every scalar-optimal choice violates the floor. This one theorem carries four red edges once the ban, the non-obstruction floor, and the CCI threshold are mapped to floor coordinates.
- `pareto_does_not_entail_floor`: Pareto optimality alone is a **non-entailment**, not a disjointness (a Pareto-optimal choice can violate the floor while an admissible one exists). The criteria_vector–cci_cert edge is red only after scalarization, which is why it is typed `viaProjection`.

Two edges are weaker than their labels suggested:

- **state–correction** previously read "fixed U resists every change of U". Only updates that lower the chosen outcome by U's own ranking are rejected; the DOT labels now say so.
- **robust–correction** first read "if every invariant state is captured". That version only constrains the choice of `K`, so the frames themselves never clash. The edge is now the quantifier conflict above. `robust_with_correction_iff_closed` shows that counting a correction as a disturbance is the same as requiring `K` to be closed under it, and `robust_correction_target_meets_K` shows such a correction can only aim at targets that meet `K`. The captured-set version is kept in [`FrameLockIn.lean`](../formal/AlignmentProofSpine/FrameLockIn.lean) as an illustration: `robust_invariance_sign_blind` exhibits a good set and a captured set that robust invariance cannot tell apart.

Checks: `registry_matches_proofs` (each registry entry has a proof), and `#print axioms` on every instance shows only `propext`, `Quot.sound`, `Classical.choice` (no `sorry`, no `native_decide`, no `MB*`).

**How far this gets you.** Paths + slots make **c** compose edges a **partitioned hypergraph** (parallel tracks, shared hubs). Morphisms make **a**/**b** edges **typed forgetful/representation maps** with named failure modes — enough to state commuting squares (“after projecting weights, optimizing scalar vs vector agrees when …”) once you instantiate acceptance predicates on carriers. Still missing: actual `def mapId` functions, `limit`/`strengthen` registry, and proofs that composition of morphisms matches slot order at hubs.
