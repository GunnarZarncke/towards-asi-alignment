The conversation that led to the below changes began with Krym’s claim that CEV is downstream of being able to “point” an AI, which initially made CEV look like a separate route from the TSA dependency structure. 

Gunnar:

> Why do you think there has been little (visible?) research on CEV since it was posed?

StanislavKrym:

> Because we at least need to point the AI at something. Pointing it at the CEV conditioned on mankind having the ability to do so is close to a governance problem, which Yudkowsky compared with distributing bananas among monkeys.

Opening the CEV black box dissolved that distinction: its volition, referent, extrapolation, coherence, correction, and preservation components largely map back onto existing TSA problems, leaving mainly a constitutional rule rather than an independent technical bridge—so MB8 can be retired. That decomposition then exposed an overloaded use of “pointing.” We initially suspected a missing target-adoption bridge, but inspection of Chapters 25–26 and the MB4 Lean code showed that causal authority, directional uptake, and preservation are already conceptually part of correction integrity; the real formal mismatch is that Lean models these more weakly than the prose. Inspection of MB2 revealed a different problem: its theorem begins after the hard evidence-to-identification step that the chapter describes, so the formalization does not yet capture the actual identifiability crux. Finally, distinguishing **constructing** a system that tracks a target from **certifying** that it does revealed a genuine omission in the field overview: TSA’s proof spine can legitimately focus on certification, but the broader field map must also include alignment construction/target realization as a first-class open problem. The resulting revision is therefore not just about CEV, but about making the field overview, book, and Lean formalization precise, mutually consistent views of the same crux structure.


## 1. Book: fix the confusion much earlier

The book contains more of the right distinctions than was initially visible, but that itself is a problem. Important distinctions only become clear around Chapters 25–26 and 44, whereas readers form their model of “what TSA is claiming” much earlier.

I would add an early section, probably Chapter 1 or 2, called something like **Three different alignment questions**:

[
\boxed{\text{Determine the target}}
\qquad
\boxed{\text{Construct a system that tracks it}}
\qquad
\boxed{\text{Establish that it tracks it}}
]

or:

[
P
\xrightarrow[\text{construction}]{}
A
\xrightarrow[\text{measurement/certification}]{}
\text{warranted claim that }A\text{ tracks }P.
]

The crucial sentence should be explicit:

> **A certification framework does not by itself provide a construction procedure.** Showing what must be measured or proved for an alignment claim does not tell us how to train or design a system satisfying those conditions.

Then state the book's scope precisely. For example:

* TSA develops much of **target determination**, especially values, referents and legitimate correction.
* TSA develops a **certification/dependency structure** for maintaining alignment.
* TSA discusses mechanisms relevant to construction, but **does not claim a general solution to alignment construction**.
* Alignment construction remains a first-class field-level open problem.

That would have prevented much of our detour.

### Define “pointing” or retire the term

We encountered at least three meanings:

[
\begin{aligned}
\text{identification} &: \text{What is }P?\
\text{realization} &: \text{How do I produce }A\text{ that tracks }P?\
\text{preservation} &: \text{How does }A\text{ continue tracking }P?
\end{aligned}
]

I would avoid using **pointing problem** as a technical label unless qualified. In particular, MB2 should be renamed **Bundle/Value Identifiability**, not “pointing.”

### Bring the legitimacy/authority distinction forward

The later chapters already contain the important distinction:

[
\text{legitimate source}
\neq
\text{causal authority}
\neq
\text{correct uptake}.
]

Introduce this much earlier whenever corrigibility/correction first appears.

A correction process (G) must satisfy at least:

[
\underbrace{\operatorname{Legitimate}(G)}*{\text{whose judgment?}}
\land
\underbrace{\operatorname{Authoritative}(G,A)}*{\text{can it change }A?}
\land
\underbrace{\operatorname{DirectionalUptake}(G,A)}_{\text{does }A\text{ change as intended?}}.
]

Otherwise “human-correctable” sounds much simpler than the later chapters reveal it to be.

---

# 2. Lean: MB2 needs the clearest correction

The current shape

[
\operatorname{BundleGradientEquivalent}(H,A)
\rightarrow
\operatorname{BundleAligned}(H,A)
]

starts **after the main empirical identifiability problem**.

The chapter's actual chain is closer to:

[
\boxed{\text{observations + interventions}}
\rightarrow
\boxed{\text{identifiable bundle geometry}}
\rightarrow
\boxed{\text{bundle equivalence}}
\rightarrow
\boxed{\text{alignment claim}}.
]

I would explicitly model all four objects.

Something conceptually like:

```lean
structure BundleExperiment where
  -- observations, perturbations, intervention outcomes, context range

def CompatibleWithEvidence
    (E : BundleExperiment) (B : BundleModel) : Prop := ...

def BundleIdentifiable
    (E : BundleExperiment) : Prop :=
  ∀ B₁ B₂,
    CompatibleWithEvidence E B₁ →
    CompatibleWithEvidence E B₂ →
    BundleEquivalent B₁ B₂

def BundleGradientEquivalent
    (H A : System) : Prop := ...

def BundleAligned
    (H A : System) : Prop := ...
```

Then separate the cruxes:

[
\mathrm{MB2a}:
E\rightarrow\operatorname{BundleIdentifiable}(E)
]

[
\mathrm{MB2b}:
\operatorname{BundleIdentifiable}(E)
\rightarrow
\operatorname{BundleGradientEquivalent}(H,A)
]

[
\mathrm{MB2c}:
\operatorname{BundleGradientEquivalent}(H,A)
\rightarrow
\operatorname{BundleAligned}(H,A).
]

Whether those need three public MB numbers is secondary. **Lean should expose the decomposition even if the site groups them as MB2.**

Most importantly, don't put `identifiable` into the evidence structure as an assumed field; that would merely hide the crux again.

---

# 3. Make `BundleAligned` less opaque

A recurring source of confusion was that we could not tell whether

```lean
BundleAligned H A
```

meant representation, causal control, behavioral similarity, or all of them.

The chapter requires more than representation. So expose that.

For example:

[
\operatorname{BundleAligned}(H,A)
:=
\operatorname{BundleCorrespondence}(H,A)
\land
\operatorname{BundleControlsPolicy}(A)
\land
\operatorname{CorrectDirection}(H,A).
]

Possibly also distinguish:

```lean
BundleRepresented
BundleGrounded
BundleCausallyEffective
BundleGradientEquivalent
BundleAligned
```

Then a theorem cannot silently jump from “we found a latent feature” to “the system values it.”

This is exactly the kind of distinction Lean is useful for forcing.

---

# 4. Lean: model Chapter 25's correction semantics faithfully

The correction code already represents:

[
C\rightarrow U\rightarrow A,
]

so **target adoption is not absent**. But the chapter requires more semantic structure than simple reachability.

At minimum separate:

### Reach

[
\operatorname{Affects}(C,U)
]

### Direction

[
\operatorname{UpdateTracksJudgment}(J,U)
]

### Depth

[
\operatorname{ChangesPolicyGenerator}(U,A)
]

rather than merely changing output text or an irrelevant state.

### Persistence

[
\operatorname{FutureCorrectionPreserved}(A).
]

Thus something like:

```lean
def CorrectionUptake
    (p : CorrectionPath) : Prop :=
  CorrectionReachesUpdate p ∧
  UpdateTracksJudgment p ∧
  UpdateReachesPolicyGenerator p ∧
  FutureCorrectionAuthorityPreserved p
```

The existing generic notion such as

```lean
HandleReachesSystem h A
```

is too weak to encode the chapter's claim. A handle can “reach” the system while causing exactly the wrong update.

---

# 5. Separate legitimacy from CCI's causal machinery

I would reorganize MB4 roughly as:

[
\boxed{\mathrm{MB4:\ Correction\ integrity}}
]

with components such as:

[
\begin{aligned}
&\text{authority}\
&\text{directional uptake}\
&\text{depth}\
&\text{semantic preservation}\
&\text{persistence}\
&\text{anti-routing-around}.
\end{aligned}
]

And separately:

[
\boxed{\mathrm{MB4a:\ Reference\ legitimacy}}
]

including:

[
\operatorname{CorrectingAgentFor}(G,H),
\quad
\operatorname{CoincidesWithHumanity}(G),
\quad
\neg\operatorname{Captured}(G).
]

Then the composition becomes explicit:

[
\operatorname{LegitimateReference}(G)
+
\operatorname{CorrectionUptake}(G,A)
+
\operatorname{CorrectionPersistence}(G,A)
\Rightarrow
\operatorname{PreservesCorrectionOperator}(A).
]

Calling the whole existing MB4 theorem `correction_legitimacy` obscures this decomposition.

---

# 6. Add the construction problem to Lean—but **do not assume it solved**

This is perhaps the most important new addition.

The field has a crux:

[
\boxed{
\text{Given }P,\text{ can we construct }A\text{ such that }A\text{ robustly tracks }P?
}
]

Represent it explicitly.

For example:

```lean
structure AlignmentTarget where
  ...

def Realizes
    (A : System) (P : AlignmentTarget) : Prop :=
  GroundedTo A P ∧
  CausallyTracks A P ∧
  CorrectableThrough A P ∧
  RobustUnderRelevantChange A P

def TargetRealizable
    (P : AlignmentTarget) : Prop :=
  ∃ A : System, Realizes A P
```

A stronger construction formulation would quantify over procedures:

```lean
def Constructs
    (builder : AlignmentTarget → System)
    (P : AlignmentTarget) : Prop :=
  Realizes (builder P) P
```

or training procedures, architectures and environments:

[
B(P,\mathcal A,\mathcal E,\mathcal T)=A.
]

But crucially:

> **Do not add an axiom saying `TargetRealizable P`.**

The point of the formalization is to expose it as an unresolved crux.

This would give the field graph a formally defined node even when TSA-the-book explicitly takes solving it out of scope.

---

# 7. Make construction and certification formally non-identical

It would be valuable if Lean makes impossible the conceptual mistake we made.

Have separate predicates:

```lean
Realizes A P
CertifiedAsRealizing E A P
```

The former is a fact about the system.

The latter is an epistemic/certification claim given evidence (E).

Schematically:

[
\operatorname{CertifiedAsRealizing}(E,A,P)
\rightarrow
\operatorname{Realizes}(A,P)
]

is a **soundness theorem** requiring assumptions.

But:

[
\operatorname{Realizes}(A,P)
\not\Rightarrow
\text{we know it},
]

and

[
\operatorname{CertificationProcedure}(P)
\not\Rightarrow
\exists A,\operatorname{Realizes}(A,P).
]

The last non-implication captures:

> certification does not provide construction.

Even if you don't prove the negative theorem abstractly, the type separation itself is valuable.

---

# 8. Retire MB8 by factorizing CEV in Lean

Don't merely delete the theorem. Replace the black box with a decomposition showing why it disappears.

Something like:

```lean
structure ConstitutionalRule where
  constituency : ...
  extrapolation : ...
  aggregation : ...
  amendment : ...
```

CEV becomes one parameterization:

```lean
def cevConstitution : ConstitutionalRule := ...
```

and produces a target process:

```lean
def constitutionalTarget
    (C : ConstitutionalRule) : AlignmentTarget := ...
```

Then there is no special:

[
\mathrm{CEV}\rightarrow\mathrm{Alignment}
]

bridge.

CEV must travel through exactly the same predicates as any other procedural target:

[
C
\rightarrow
P_C
\rightarrow
\operatorname{Realizes}(A,P_C)
\rightarrow
\operatorname{CertifiedAsRealizing}(E,A,P_C).
]

This formally captures the dissolution we reached.

It also exposes the **Coherent** part rather than leaving it unconnected. Aggregation/coherence needs explicit dependencies on constituents, values and referents.

Keep the MB8 site card as "gravestone" explaining the decomposition. Remove MB8 from the field overview. Evidence in the MB8 column has to be either moved to the corresponding decomposed parts, or dropped.

---

# 9. Model the field's cruxes as propositions, not axioms where possible

This may be a broader Lean cleanup.

An axiom like

```lean
axiom MB2_bundle_identifiability :
  X → Y
```

makes an open research problem look structurally identical to a foundational assumption deliberately granted by the model.

Instead distinguish:

* **definitions** — what the claim means;
* **empirical hypotheses** — properties that experiments might establish;
* **bridge conjectures** — unresolved implications;
* **proved theorems** — consequences actually derived;
* **out-of-scope assumptions** — consciously granted for a particular chapter.

For example:

```lean
def MB2Crux : Prop :=
  ∀ ..., SufficientBundleEvidence ... →
         BundleGradientEquivalent ...
```

rather than immediately declaring it an axiom globally.

A particular theorem can then say:

```lean
theorem later_result
    (hMB2 : MB2Crux)
    (hMB3 : MB3Crux)
    ... :
    SafetyClaim := ...
```

This has a major advantage: **Lean now shows exactly which unresolved cruxes every conclusion depends on.**

That is almost ideal for the field overview.

---

# 10. Generate the field overview from Lean dependencies

This is perhaps the biggest “anything else.”

If confidence in the overview depends on every crux having a precise formal meaning, then the site graph should eventually be generated—or at least validated—from the Lean dependency graph.

For each field node, store:

* formal proposition;
* type: `construction`, `identification`, `certification`, `normative`, etc.;
* dependencies;
* status: open / empirical evidence / theorem / assumption;
* book chapter;
* relevant agenda/research program.

Then:

[
\boxed{\text{Lean is the canonical dependency structure}}
]

while the field overview is its human-readable projection.

That would have caught MB8: if CEV were formalized internally, its dependencies would immediately reconnect into MB2/MB3/MB4 rather than appearing as an isolated alternative route.

---

## 11. I would add a second axis to the field overview

The MB graph primarily asks **what property depends on what other property**.

But we discovered another orthogonal axis:

[
\boxed{
\text{specify}
\rightarrow
\text{construct}
\rightarrow
\text{identify/measure}
\rightarrow
\text{certify}
\rightarrow
\text{preserve}
}
]

A field overview needs both.

Otherwise construction repeatedly falls through the cracks because it is not itself a prerequisite proposition of the certification argument.

This does **not** mean duplicating every MB five times. It could simply classify each node by lifecycle role and add missing nodes where an entire role is absent.

“Target Realization / Alignment Construction” is the clearest current example.

---

## 12. One final methodological improvement

For every chapter-to-Lean mapping, add a tiny **formal contract** at the top of the chapter:

> This chapter claims (X).
> Lean representation: `Foo`.
> It assumes (A,B).
> It does not establish (C).

For Chapter 25, for example:

[
\text{correction}
=================

\text{legitimate source}
+
\text{causal authority}
+
\text{directional policy uptake}
+
\text{future preservation}.
]

Then readers can immediately see whether the prose is stronger than the formal object.

That would have exposed our CCI issue without several rounds of interpretation.

---

### Resulting revision

I would make the project architecture explicitly:

[
\boxed{
\begin{array}{ccc}
\textbf{Field overview} &:& \text{all important open cruxes}\
\updownarrow &&\
\textbf{Lean} &:& \text{precise propositions and dependencies}\
\updownarrow &&\
\textbf{Book} &:& \text{mechanisms, evidence, interpretation, scope}
\end{array}}
]

with **Lean as the semantic spine**, but not as a fiction that every open crux has been solved.

The immediate concrete changes seem to be: **retire MB8; repair MB2's missing evidence→identification step; de-opaque bundle alignment; strengthen CCI to match direction/depth semantics; separate legitimacy from causal uptake; add Alignment Construction/Target Realization as a field-level formally defined open crux; and introduce construction-vs-certification near the beginning of the book.**

That seems like the coherent endpoint of the Krym discussion—and, more importantly, a substantially better architecture for TSA itself.
