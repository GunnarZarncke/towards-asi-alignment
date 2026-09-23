> **Status (2026-09-18):** reviewed; decisions locked in [`../plans/construct/embedded-v2.md`](../plans/construct/embedded-v2.md). This file is the source memo. 2.0 intro claim authorized; \(P\) ≠ \(D_{\mathrm{joint}}\); lifecycle is a cycle (Preserve = property); matrix stays evidential.

## Summary

The central proposed correction is to stop treating the alignment lifecycle, the bridge DAG, and the surrounding research/institutional field as three largely separate objects.

The current V2 architecture already contains the pieces of a more unified picture. The bridge DAG models load-bearing transitions such as boundary measurement, value identification, correction integrity, selection stability, successor safety, adversarial verification, and deployment safety. The V2 lifecycle adds the sequence

\[
\text{Specify}\rightarrow\text{Construct}\rightarrow\text{Identify}\rightarrow\text{Certify}\rightarrow\text{Preserve},
\]

and the Construction V2 plan adds a distinction between technical **Construction** and social/process-level **Constructibility**. The attractor papers further make selectors and environments endogenous rather than treating them as fixed external conditions.

Taken together, these suggest a stronger interpretation:

\[
\boxed{
\text{Alignment is a stability property of a coupled socio-technical construction and correction process.}
}
\]

The AI system, the human institutions constructing and evaluating it, the correction mechanisms, the deployment environment, and the selection pressures acting on all of them form one embedded dynamical system.

The bridges should therefore be understood as **cuts through this larger system**: each bridge compresses a complicated subgraph of causal processes into an interface claim. The key question for every bridge becomes:

> What environmental, institutional, epistemic, or organizational variables are being held fixed or projected away when the bridge antecedent is treated as sufficient for its consequent?

This changes how the lifecycle should be represented, how Construction V2 should treat field building, and eventually how the bridge formalizations should be typed.

## 1. The main conceptual correction: there are not two independent graphs

An initial interpretation was that there were two graphs:

\[
\text{technical bridge DAG}
\]

and

\[
\text{field/research production DAG}.
\]

The production DAG would describe how researchers, money, institutions, experiments, and coordination produce solutions to the bridge cruxes.

That graph exists, but it is not the important missing object. If it were independent of the bridge graph, there would be little reason to represent it in TSA. It would merely describe the sociology of producing alignment research.

The stronger point is that parts of the human and institutional system are themselves causally inside the alignment problem.

The relevant state is not just an AI system \(A_t\), but something closer to

\[
z_t=(x_t,h_t,k_t,\theta_t,e_t),
\]

where:

\[
x_t=\text{AI systems and technical artifacts},
\]

\[
h_t=\text{researchers, labs, auditors, funders, regulators and operators},
\]

\[
k_t=\text{knowledge, evaluations, models, specifications and safety cases},
\]

\[
\theta_t=\text{selection, certification and deployment rules},
\]

and

\[
e_t=\text{remaining technical, economic and institutional environment}.
\]

These components influence one another.

Labs and regulators determine which systems are trained, certified and deployed:

\[
h_t\rightarrow\theta_t\rightarrow x_{t+1}.
\]

But AI systems also affect the surrounding institutions:

\[
x_t\rightarrow h_{t+1},
\]

through economic incentives, research automation, organizational power, evaluator dependence, new capabilities, regulatory responses, and possibly strategic influence.

Likewise research artifacts change the field:

\[
k_t\rightarrow h_{t+1},
\]

while the field determines which artifacts are generated and selected:

\[
h_t\rightarrow k_{t+1}.
\]

The result is a coupled dynamical system, not a technical object surrounded by an external research process.

This interpretation follows naturally from the attractor work. *Alignment Under Selection* explicitly models population, selector and environment jointly, while deliberately leaving institutional selector capture and human correction-channel integrity outside its scope. *Constructing Alignment Attractors* then makes the crucial conceptual move that once the selector is endogenous, it is no longer an external field: it belongs inside the state being analyzed.  

Construction V2 already moves in the same direction by distinguishing technical construction from **constructibility**: whether people, labs and organizations are actually willing and able to construct the relevant system rather than merely maintaining an alignment-compatible narrative. 

The proposed extension is therefore not a foreign addition to V2. It is a closure of several ideas V2 already contains.

## 2. Extend the attractor concept to the research and deployment ecology

The current attractor framing asks whether an aligned region remains stable under transformation, competition, selection and endogenous selector dynamics.

The proposed extension is to include the research and institutional ecology in that attractor.

Instead of defining the desirable basin only over AI systems,

\[
x_t\in D_{\text{AI}},
\]

the more relevant object is a joint desirable region

\[
z_t\in D_{\text{joint}},
\]

where \(D_{\text{joint}}\) constrains both the AI systems and the socio-technical mechanisms maintaining them.

The field itself can then occupy good or bad attractors.

A representative bad attractor might operate as follows:

\[
\text{cheap evaluation becomes prestigious}
\]

\[
\downarrow
\]

\[
\text{funders select projects that improve it}
\]

\[
\downarrow
\]

\[
\text{labs hire specialists around that evaluation}
\]

\[
\downarrow
\]

\[
\text{regulators standardize it}
\]

\[
\downarrow
\]

\[
\text{models are optimized against it}
\]

\[
\downarrow
\]

\[
\text{the evaluation keeps returning reassuring results}
\]

\[
\downarrow
\]

\[
\text{the evaluation receives still more authority and investment}.
\]

No deception or corruption is required. Ordinary selection pressure can generate the loop.

This is structurally analogous to the “wrong vacuum” problem in the attractor paper: the system has become stable, but in the wrong basin.

The desired attractor should therefore include such properties as:

- epistemically independent evaluation;
- live correction channels;
- institutions capable of acting on negative evidence;
- incentives that reward discovery of failures rather than merely successful certification;
- enough methodological diversity that one evaluation ontology cannot silently become the entire safety ontology;
- sufficient ability to reconstruct or reject a system when certification fails;
- resilience against the AI system or capability race reshaping the institutions that are meant to govern it.

This makes “alignment attractor” substantially more than a property of model populations.

## 3. Reinterpret the bridges as cuts through the coupled system

The bridge DAG remains useful, but its meaning becomes clearer.

Suppose the real causal path is

\[
P\rightarrow M_1\rightarrow M_2\rightarrow M_3\rightarrow Q.
\]

A bridge compresses that subgraph to

\[
P\Rightarrow Q.
\]

That bridge is therefore an **interface contract across a causal cut**.

The problem appears when some contextual variable \(C\) enters the hidden subgraph:

\[
C\rightarrow M_2.
\]

Then

\[
P\Rightarrow Q
\]

is not automatically valid. It is valid only under some admissible class of contexts:

\[
\forall c\in\mathcal C_i,
\qquad
P_i(A,c)\Rightarrow Q_i(A,c).
\]

The current formalization often looks instead like

\[
P_i(A)\Rightarrow Q_i(A),
\]

which implicitly either fixes \(c\), assumes it irrelevant, or folds it into the opaque meaning of \(P_i\) and \(Q_i\).

This makes the question

> What environmental or institutional variables does this bridge silently hold fixed?

a systematic bridge-analysis method rather than an informal criticism.

Different bridge families cut different parts of the larger graph.

MB1, MB2, MB7 and MB9 are largely **epistemic cuts**:

\[
\text{world/system}
\rightarrow
\text{access and experiment}
\rightarrow
\text{evidence}
\rightarrow
\text{semantic claim}.
\]

MB4 and MB4a are **authority and correction cuts**:

\[
\text{human judgment}
\rightarrow
\text{institutional process}
\rightarrow
\text{control handles}
\rightarrow
\text{system update}.
\]

MB3, MB5 and MB10 are **temporal/inheritance cuts**:

\[
\text{current system}
\rightarrow
\text{transformation or successor process}
\rightarrow
\text{future system}.
\]

MB6 is the major **ecological cut**:

\[
\text{socio-technical interaction}
\rightarrow
\text{selection dynamics}
\rightarrow
\text{stable correction-preserving basin}.
\]

MB11 is the **deployment cut**:

\[
\text{evidence + governance judgment}
\rightarrow
\text{real-world deployment safety}.
\]

Once viewed this way, institutional variables are not an independent second graph. They frequently live inside the causal mechanisms being compressed by the bridge arrows.

## 4. Hidden variables in the current bridges

The bridge review suggests that several bridges silently rely on substantial environmental structure.

MB1 depends not only on the measured boundary but also on observability, sampling regime, instrumentation, access and non-stationarity. The Lean comment already acknowledges sampling, observability, estimator stability and non-stationarity as part of estimator soundness, but these are not explicit arguments of the bridge. 

MB2 depends on which interventions can be run, what data are available, who supplies the reference profile, and whether the experimental process can expose rival latent structures. The finite formalization already makes the chain explicitly depend on “observations (+ interventions).” 

MB3 depends on continuity of the bearer reference: who or what counts as the entity to which the values apply, and what institutional or social process legitimately updates that reference under ontology changes.

MB4 depends on the continued existence of a competent correction process with enough information, authority and control to alter the system.

MB4a is already considerably better than most bridges because the formalization explicitly contains a correcting agent, handles, control, reach, persistence and anti-capture.  The remaining hidden questions concern how that corrector is selected, replaced, funded, informed and protected from institutional capture.

MB5 treats successor safety largely as a relation between systems \(A\) and \(B\), while the actual safety of successor production also depends on which successors are generated and selected. A safe \(A\to B\) relation does not imply a safe successor ecology.

MB6 has the largest discrepancy. Its public wording explicitly concerns **socio-technical selection**, but formally it is represented by unary predicates such as

\[
\mathrm{PercolationEvidenceSys}(A)
\rightarrow
\mathrm{BasinStableSys}(A)
\rightarrow
\mathrm{CorrectionIntegrity}(A).
\]



Yet `Environment` elsewhere in Lean is explicitly described as institutions, markets and protocols that copy, deploy or fund systems.  The natural V2 extension is therefore to make those environmental variables first-class in MB6.

MB7a and MB7b depend on evaluator access, legal and organizational permissions, available interventions, time and compute budgets, tool quality, independence and methodological diversity.

MB7c depends not only on the hidden capability bound but also on whether detection leads to effective intervention before the system can exploit or bypass the oversight regime.

MB9 depends on who monitors domain drift, whether new phenomena become visible, and whether uncertainty escalation causes any operational response rather than merely appearing in an audit report.

MB10 already moves toward an explicit contextual model by giving the audit a measurement channel, fake-cost structure and capability-dependent verifiability condition.  The remaining institutional layer concerns who runs and controls that channel.

MB11 is perhaps the strongest reason to move toward context-relative formalization. The current form is essentially

\[
\mathrm{CertifiedSafetyCase}(A,\delta)
\land
\mathrm{WithinDeploymentRiskTolerance}(A,\delta)
\rightarrow
\mathrm{Safe}(A).
\]

The formalization correctly notes that the deployment tolerance is a governance input rather than a measurand.  But deployment safety itself is plausibly relational: the same system can be safe under one deployment environment and unsafe under another.

The V2 object should therefore move toward something like

\[
\mathrm{SafeIn}(C,A),
\]

where \(C\) contains the relevant deployment context.

## 5. The “lifecycle” should become a cycle

The current V2 field data describes

\[
\text{Specify}\rightarrow
\text{Construct}\rightarrow
\text{Identify}\rightarrow
\text{Certify}\rightarrow
\text{Preserve}
\]

as a lifecycle axis orthogonal to the bridge dependency graph. 

That is useful as a reader-facing ordering, but conceptually it is too linear.

Real alignment work is recurrent.

Certification may reveal a failure and trigger reconstruction:

\[
\text{Certify}
\rightarrow
\text{Construct}.
\]

Identification may reveal that the object being specified was wrong:

\[
\text{Identify}
\rightarrow
\text{Specify}.
\]

Environmental change may invalidate the specification:

\[
\text{Preserve/monitor}
\rightarrow
\text{Specify}.
\]

Deployment evidence may change the measurement regime:

\[
\text{Act}
\rightarrow
\text{Identify}.
\]

A more faithful architecture is therefore:

\[
\text{Specify}
\rightarrow
\text{Construct}
\rightarrow
\text{Identify}
\rightarrow
\text{Certify}
\rightarrow
\text{Act/Refuse}
\]

with feedback edges back to the earlier stages.

The especially important addition is **Act/Refuse**.

The Construction V2 plan already implicitly contains this node. Witness Exp. 4 demands a certification leaf that actually changed a decision. Family C treats a fail or refusal as a success of the method. Merely producing a green dashboard is explicitly not enough. 

The missing lifecycle stage is therefore the point where certification actually changes the world.

Under this interpretation, **Preserve is not really a stage at all**.

Preservation is a property of the entire repeated loop:

\[
z_t\in D
\land
z_t\rightarrow z_{t+1}
\Rightarrow
z_{t+1}\in D.
\]

This corresponds directly to the basin-stability style already present in the Lean development. `P35_basin_stability_induction` defines preservation under repeated transition. 

So the V2 lifecycle should be reconceived as an **alignment control cycle**, with preservation as its closed-loop stability condition.

## 6. Consequences for the Construction V2 plan

The existing Families A–D do not need to be discarded. They should be reinterpreted through the cycle.

### Family A: certification versus construction

The existing distinction remains correct, but it should be strengthened.

Certification is not merely different from construction. It is one of the feedback channels controlling future construction.

A new failure mode becomes important:

\[
\text{correct certification}
\not\Rightarrow
\text{correct reconstruction}.
\]

A safety case that correctly detects a problem but fails to alter the construction process is not closing the loop.

Likewise, “certification without construction” and “certification without decision leverage” become two distinct failure modes.

### Family B: concrete construction

Construction should no longer be interpreted as merely producing a state \(s\in D\).

The stronger target is that the intervention produces a state whose subsequent coupled dynamics remain in or return toward the desirable basin:

\[
I(z_t)\in D
\]

is weaker than

\[
T(I(z_t))\in D
\]

and weaker again than

\[
T^n(I(z_t))\in D
\quad
\text{for relevant }n.
\]

The construction intervention should explicitly state which parts of

\[
(Q,f,\theta,E)
\]

it changes, including institutional or human components where relevant.

This makes institutional interventions legitimate construction interventions rather than mere external support.

### Family C: technical process conditions

Family C should become explicitly cyclical.

Its existing requirements — frozen \(D/P\), named intervention \(I\), fail/refuse criteria, comparing construction and certification trees on the same episode — are already well suited to this.

The important modification is that “freeze the target” should mean **freeze the target within a construction/certification episode**, not “the target can never legitimately change.”

Otherwise the framework cannot simultaneously demand anti-post-hoc target selection and allow legitimate updating under new information.

A cycle can therefore use

\[
P_t
\]

as the frozen target for episode \(t\), while a separately specified legitimate process can produce

\[
P_{t+1}.
\]

That separates legitimate target revision from ex post rationalization.

### Family D: social process conditions

This is where the largest extension belongs.

The current plan already talks about career and prestige gradients as selectors on constructor stories, and distinguishes labs that are able but unwilling from those that are willing but unable. 

Family D should generalize this into a model of **constructor ecology**.

Relevant variables include:

- who becomes a researcher or evaluator;
- where researchers are placed;
- who funds which approaches;
- whether evaluators are institutionally independent from builders;
- whether negative results are rewarded or punished;
- whether different research traditions remain independently viable;
- whether correction roles have actual deployment authority;
- whether labs can replace external scrutiny with internal certification;
- whether capability gains reshape the institutions meant to govern them;
- whether the field converges onto an alignment-shaped but dynamically bad attractor.

This does not require a full sociological theory. The V2 goal can remain modest: identify the process conditions that must remain true for the technical alignment cycle to function.

## 7. Field building should be split into capacity building and structural field construction

The current “What This Map Misses” treatment of organizations such as Kairos correctly notes that talent discovery and placement can succeed while every technical measurement question remains unresolved. 

That remains true, but it does not exhaust the possible causal role of field building.

There are two importantly different cases.

### Capacity field building

Examples include:

- introductory courses;
- career outreach;
- general mentorship;
- workshops;
- community growth.

The main effect is approximately

\[
\text{field building}
\rightarrow
\text{more or better people}
\rightarrow
\text{higher probability of future research output}.
\]

This remains upstream of the bridge DAG.

It should not get a green MB cell merely because it increases research capacity.

### Structural field construction

Other interventions directly modify the socio-technical context in which bridges hold.

Examples include:

- establishing independent evaluator institutions;
- training and placing people into roles with actual stop authority;
- maintaining multiple technically independent research communities;
- creating funding structures that reward falsification and refusal;
- separating certifier and deployer roles;
- maintaining adversarial review capacity;
- giving safety researchers access rights that cannot be revoked when results become inconvenient.

These interventions change variables relevant to MB4a, MB6, MB7, MB10 and MB11.

They are not evidence that those bridges are discharged.

But they are interventions on the context that determines whether the bridges can hold.

This suggests an important representation change in the field map.

The map should distinguish:

\[
\mathrm{evidenceFor}(O,MB_i)
\]

from

\[
\mathrm{actsOnContextOf}(O,MB_i).
\]

A paper may provide evidence for MB7b.

An evaluator-training institution may act on the context of MB7b and MB10.

A general alignment course may affect neither directly and belong only in upstream capacity.

This preserves the evidential meaning of the matrix while avoiding the incorrect implication that field-building organizations are irrelevant to the alignment mechanism.

## 8. Formalization: introduce explicit alignment context

The present Lean model already contains many needed primitives.

`System` can represent agents, composites and institutions. `Environment` is explicitly defined as the selection environment containing institutions, markets and protocols that copy, deploy or fund systems. 

Correction already has explicit correctors, handles, control, reach, persistence and anti-capture. 

The issue is that these pieces are not consistently threaded through the bridge types.

A natural V2 extension is therefore to introduce an explicit context object, for example conceptually:

```lean
structure AlignmentContext where
  environment : Environment
  constructorEcology : System
  evaluator : System
  corrector : System
  deployer : System
```

and then

```lean
structure EmbeddedAlignmentState where
  subject : System
  context : AlignmentContext
```

The roles need not be distinct. Equality can represent a lab that builds, evaluates and deploys its own system. Separate independence predicates can then express when role separation is required.

Transitions can similarly become first-class:

```lean
structure AlignmentTransition where
  pre : EmbeddedAlignmentState
  post : EmbeddedAlignmentState
```

This is particularly useful for successor and preservation bridges.

The generic V2 bridge becomes:

\[
B_i:
\forall z,\;
P_i(z)\rightarrow Q_i(z),
\]

rather than

\[
P_i(A)\rightarrow Q_i(A).
\]

This does not imply that every bridge must immediately be rewritten. A staged migration is possible.

## 9. Which formalizations most need changing

MB6 should be the first candidate.

Current:

\[
\mathrm{PercolationEvidenceSys}(A)
\rightarrow
\mathrm{BasinStableSys}(A).
\]

More faithful:

\[
\mathrm{PercolationEvidence}(C,A)
\rightarrow
\mathrm{BasinStable}(C,A).
\]

Eventually basin stability should apply to the joint state:

\[
B(z_t)
\land
T(z_t,z_{t+1})
\rightarrow
B(z_{t+1}).
\]

This directly represents socio-technical basin stability instead of encoding it as a unary property of the AI.

MB11 is the second strong candidate.

Current:

\[
\mathrm{CertifiedSafetyCase}(A,\delta)
\land
\mathrm{WithinDeploymentRiskTolerance}(A,\delta)
\rightarrow
\mathrm{Safe}(A).
\]

Possible V2 shape:

\[
\mathrm{CertifiedSafetyCase}(C,A,\delta)
\land
\mathrm{WithinDeploymentRiskTolerance}(C,A,\delta)
\land
\mathrm{DeploymentConditions}(C,A)
\rightarrow
\mathrm{SafeIn}(C,A).
\]

That would make the deployment environment part of the safety claim rather than a silently fixed background condition.

MB4a already has much of the right structure. The next step is mainly to make the correcting institution itself dynamic rather than assuming properties such as `CoincidesWithHumanity` and `HandleControlPersists` without modeling how institutional selection affects them.

MB7 and MB10 should eventually type the evaluator or audit ecology more explicitly, because access, filtering and adversarial verifiability depend on who controls the evaluation process.

MB1, MB2 and MB9 can remain simpler for longer. Their immediate improvement would be to make their validity **context-relative** rather than globally unary.

## 10. Formalize the bridge cut itself

A particularly useful abstraction would be to formalize not merely individual bridges but the idea of a context-sensitive bridge interface.

Conceptually:

\[
\operatorname{BridgeCut}_i(\mathcal C_i,P_i,Q_i)
:=
\forall c\in\mathcal C_i,\;
P_i(c)\rightarrow Q_i(c).
\]

The bridge then states exactly which class of contexts it claims to survive.

The current bridge is approximately the special case where the context is fixed or suppressed.

This creates a precise research program:

> For each bridge, determine the smallest set of contextual variables that must cross the cut for the implication to remain valid.

That is a strong operationalization of the original question about silently fixed environmental variables.

The dynamic analogue is equally important:

\[
\operatorname{BridgePreserved}_i
\iff
\forall z_t,z_{t+1},
\;
B_i(z_t)
\land
T(z_t,z_{t+1})
\rightarrow
B_i(z_{t+1}).
\]

This connects the bridge formalizations directly to preservation and attractor stability.

## 11. The resulting V2 architecture

The revised conceptual structure is therefore not:

\[
\text{technical alignment}
+
\text{field building}
+
\text{deployment governance}.
\]

It is one embedded feedback system.

A useful schematic is:

\[
\text{Specify}
\rightarrow
\text{Construct}
\rightarrow
\text{Identify}
\rightarrow
\text{Certify}
\rightarrow
\text{Act/Refuse}
\]

with feedback from every downstream stage to earlier stages.

Researchers, labs, evaluators, institutions and AI systems are all parts of the state being transformed by that cycle.

The bridge DAG cuts across this cycle and labels the nontrivial interface claims required for evidence and control to propagate through it.

Construction changes the dynamics.

Certification observes and constrains them.

Action or refusal closes the causal loop.

Preservation means that the entire coupled process remains inside the desirable basin over repeated iterations.

Field building can either sit upstream as capacity production or, when it changes institutional independence, selection pressure, correction authority or evaluation structure, become a genuine construction intervention on the embedded alignment system.

The resulting V2 research question is therefore stronger than “How do we construct a system satisfying the alignment target?”

It becomes:

\[
\boxed{
\begin{gathered}
\text{Can we construct a coupled AI–human–institutional process}\\
\text{whose specification, measurement, correction, certification and}\\
\text{selection mechanisms remain valid as the process changes itself?}
\end{gathered}
}
\]

And the corresponding bridge question becomes:

\[
\boxed{
\text{Which bridge cuts remain valid once the constructor, evaluator, corrector,}
\atop
\text{deployer and their selection pressures are endogenous?}
}
\]

That is the main proposed extension to V2. It does not replace the existing bridge DAG or Construction plan. It supplies the embedded-system interpretation that connects them.