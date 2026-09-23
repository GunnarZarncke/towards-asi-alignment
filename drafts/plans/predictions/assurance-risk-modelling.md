# Predictions appendix and assurance-risk modelling

Status: **Phase 3 implemented** (2026-09-22). Assurance manifest, draft Markets 19–20 contracts, and site sensitivity demo shipped; catalog expansion and external listing remain Phase 4. Lane: **Predictions** (appendix PRA layer, Markets 19–20, site demo). Builds on P0c: [`prediction-interface.md`](prediction-interface.md), [`bridge-prediction-markets.md`](bridge-prediction-markets.md). Authoritative sources: `appendices/appP-bridge-predictions.tex` (Appendix H in print), `metadata/predictions.yml`, `metadata/assurance-model.yml`, `formal/AlignmentProofSpine/Evidence.lean`.

**Source freeze (Phase 0, before this implementation):** HEAD `2543ddbd`; appendix + YAML last at `1ebf999e` (2026-09-22 App H polish); `Evidence.lean` last at `6c46f4bb` (2026-09-19 v1 adapters). Locked prediction-interface decisions unchanged: no `AlignmentContext`, no market outcomes in Lean, extra predicate indices deferred. PRA derivation in manuscript; interactive user-parameter model remains site-later (Phase 3).

## 1. Executive decision

Core principle:

> Prediction-market prices forecast whether qualifying research artifacts will exist by a deadline. They are not probabilities that a safety property holds on a frontier deployment, and they must not be multiplied into \(P_{\rm doom}\).

Three formal layers must stay distinct and share one coherent narrative:

1. the existing 18-market public contract catalog;
2. the Lean dependency spine and its certificate adapters;
3. a Bayesian/PRA assurance and consequence model.

PRA is the organizing frame for turning prediction outputs and formal obligations into a coherent assurance model. Do not multiply research-readiness prices, treat Lean proof dependencies as a causal fault tree, or move from assurance discrimination directly to catastrophe without a consequence model.

Target architecture:

- preserve the 18 market IDs and public specs;
- replace the current product-of-market-prices aggregation with a PRA/Bayesian account of assurance failure;
- keep the existing Lean certificate layer as the formal baseline;
- make the markets resolve on publicly reconstructible technical evidence, not on outside authors adopting TSA terminology or certificate formats;
- include the assurance-failure model and its core derivations in the manuscript so the predictions have a coherent context;
- put interactive user-supplied parameters, scenario comparison, and richer consequence modelling in a site-only demo;
- complete resolvable contracts for Market 19 (integrated transfer tournament) and Market 20 (open-world coverage challenge) in Phase 3, and integrate their empirical outputs into the site model without treating their market prices as risk parameters.

An absolute \(P_{\rm doom}\) may be shown downstream in that demo as an assumption-dependent sensitivity output. It should not be presented as a validated project estimate.

## 2. Current baseline

### Predictions

- The `appP` source and `metadata/predictions.yml` define **18** markets.
- The IDs `market-01` through `market-18` already drive generated cards and stable site routes.
- The appendix is the public YES/NO spec. The YAML is the catalog source. Site content is generated from them.
- A YES means that a qualifying method or governance artifact met frozen bars by the resolve-by date.
- A YES does not discharge an `MB*`, establish a predicate for a frontier deployment, or estimate a PRA basic-event probability.
- Market 13 is currently the frozen-audit / MB10-neighborhood contract.
- Market 14 is governance binding / constructibility, not MB11.
- Market 15 is certificate-scope coherence, not a new bridge.
- Market 18 concerns observed prohibited outcomes in a declared setting. It is not unrestricted `Safe`.
- MB8 is retired from the live path and should not re-enter through the risk model.
- Metaculus question 44423 is an external institutional-pause forecast. It is not one of the 18 markets and does not discharge a bridge.

Use an explicit indexing convention throughout later work:

- write **Market 8 (MB7a access)**, never `M<number>` shorthand, when the market number could be confused with a Lean bridge;
- reserve `MB8` for the retired CEV/process-convergence gravestone;
- keep a `{Market number, Lean object, short name}` mapping in any generated risk-model manifest.

### Lean

`formal/AlignmentProofSpine/Evidence.lean` already contains the v1 evidence layer:

- per-system certificate tokens;
- named eval-soundness adapters;
- `HiddenRouteBound`;
- `CoherentCertificateBundle`;
- derived `Certified`;
- a deliberately separate `SafeIn` stub.

Locked decisions in [`prediction-interface.md`](prediction-interface.md):

- certificates carry enough identifying information in the public spec now;
- the unary Lean predicates remain in v1;
- additional scope indices are Lean 2.0 work;
- there is no universal `AlignmentContext`;
- market YES outcomes and contract percentages do not enter Lean.

The Lean spine proves conditional implications, finite separations, and bookkeeping results. It does **not** define a complete causal fault tree or a probability model.

Three numeric objects must remain distinct:

- Lean `RiskGap`: a control-minus-CCI capacity slack, not a failure probability;
- Market 18's observed prohibited-outcome bound in a declared setting;
- `WithinDeploymentRiskTolerance`: an acceptance judgment used by MB11.

## 3. Design constraints

### 3.1 Do not renumber the catalog

Markets 1--18 are already wired into generated cards and stable site routes (`market-01` through `market-18`). Keep those IDs stable. Express conceptual groupings through headings, diagrams, or a mapping manifest rather than changing numbers.

### 3.2 One typed assurance model, two dependency relations

A Lean proof dependency and a probabilistic parent relation are different but related claims. They must not drift into independently maintained accounts of the same assurance case.

- A shared theorem prerequisite is not automatically a common causal cause.
- A common empirical blind spot may correlate evidence without appearing in a theorem's axiom list.
- A sufficient-condition theorem is not a complete decomposition of all ways safety can fail.
- Minimal cut sets require a closed, usually monotone Boolean fault model with explicit gate semantics. They cannot be read directly from the current proof DAG.

The target source of truth is a typed assurance model that records:

- shared node identities and scopes;
- logical implication or obligation edges;
- causal, evidential, and common-cause edges;
- gate semantics and completeness claims where applicable;
- empirical producers, certificates, and calibration data;
- the justification and provenance for every non-logical edge.

The Lean dependency view and the PRA/Bayesian view should be projections of that model, or be mechanically checked against those projections. The richer model may itself be represented in Lean or in a typed manifest that generates Lean declarations and the risk graph. Either representation is acceptable only if there is one canonical definition for shared nodes and mappings.

For the first pass, Lean remains authoritative for formal signatures and conditional implications. The versioned assurance-model manifest adds the causal/evidential relations and their justifications, imports Lean identifiers, and is checked for mapping drift. This is a staged path to one source of truth, not a claim that causal edges can be inferred from proof edges.

If machine-generated cut sets are wanted, encode a Boolean submodel in this source with explicit `iff` gates and a stated closed-world scope. Generate cut sets only from that submodel.

### 3.3 Evidence soundness is already explicit

`Evidence.lean` already contains named eval-soundness adapters (`BoundaryEvalSoundness`, `CorrectionEvalSoundness`, and similar). Future work may package, scope, or probabilistically calibrate them; the adapter layer is not missing.

Also, a universal Lean proposition such as

\[
\textsf{BoundaryCert}(A)\to\textsf{BoundaryAligned}(A)
\]

is not itself a calibrated random variable. A Bayesian model needs an event such as “this adapter is valid for this system, setting, and evaluation protocol,” with empirical support stated outside Lean.

### 3.4 Do not immediately retype the whole spine

A full retyping around system identity, occurrence, setting, observation surface, authority, ontology, threat class, lineage, and validity interval is out of scope for the first pass.

For the current appendix and risk model, keep scope as certificate metadata. If Lean 2.0 later retypes predicates, introduce only the dimensions needed by a concrete theorem. Do not add one giant context object and do not make this appendix rewrite depend on that refactor.

### 3.5 Markets 4, 5, and 16 are not a simple fixed AND/OR

Markets 4, 5, and 16 must not be treated as complementary obligations with no alternative routes. Lean supports several correction-integrity routes:

Current formal routes include:

- Market 4-style `CorrectionEvalCert A` to `CorrectionIntegrity A` through `correction_eval_soundness`;
- Market 5-style positive measured-path evidence to `CorrectionIntegrity A` through its own soundness adapter;
- Market 16-style `CorrectionSupportingBasin A ε` to `CorrectionIntegrity A` through MB6b.

At the same time, `LayeredAlignedDef` contains both `CorrectionIntegrity A` and `CorrectionSupportingBasinSys A`. The certificate-based assembly uses direct correction evidence and separately requires basin evidence; another bridge-derived route obtains correction integrity from the basin.

Therefore:

- keep Markets 4, 5, and 16 as distinct empirical questions;
- represent their shared measurements and dependence in the risk model;
- do not count them as independent confirmations;
- do not state that all three are logically required unless a new, stronger deployment policy explicitly requires them;
- do not state that one market's YES resolves another market.

If the desired deployment rule is “require both direct correction evaluation and selection-basin evidence,” label that as a conservative policy addition, not a theorem already derived by Lean.

The historical disjunctive-tolerance issue formalized in `Chokepoint.lean` is instead **MB6b versus retired MB8 under a shared instrument**. Keep that result as a shared-instrument warning and gravestone. Do not revive MB8 as a live route or mistake Market 8 (MB7a access) for Lean MB8.

### 3.6 Do not silently broaden Markets 13 and 15

Keep Market 13's current frozen-audit scope. A full multi-certificate stack attack would overlap the proposed integrated tournament and would drift further from the specific MB10 successor-forgeability neighborhood.

Keep Market 15 as a static scope/coherence test. Dynamic provenance, revocation, and recertification are valuable, but they should first be designed as certificate-management behavior. Do not silently add them to the frozen market contract.

An invalidated ancestor should invalidate only the inference paths that depend on it. A descendant observation may remain locally valid or may have an independent justification.

### 3.7 Effective-controller uncertainty need not become a new Lean primitive now

Market 1 already asks for a sufficient interventional control cut and explicitly permits non-unique boundaries. A universal declared-subject/effective-controller identity relation risks reintroducing an unjustified unique-controller ontology.

In the risk model, represent uncertainty that the certificates concern the relevant effective controller. Add a Lean relation only if a later theorem needs it, and scope it to system version and deployment setting.

### 3.8 Add Markets 19 and 20 through complete resolution protocols

The integrated transfer tournament and open-world coverage challenge are needed because they produce cross-cutting evidence that the component markets do not. Develop them as Market 19 and Market 20 in Phase 3. Before either contract is added to the catalog, specify:

- a market question and resolve-by date;
- a precise eligible artifact;
- a resolver and evidence rule;
- sample-size and confidence requirements;
- a frozen positive and negative case distribution;
- an abstention rule;
- a cost-feasible adversarial protocol;
- a decision about which of the 18 components are actually required.

Their **resolved experimental outputs**, not their prediction-market prices or binary YES outcomes, supply potential model inputs:

- Market 19 can estimate benchmark-local \(P(\mathrm{ACCEPT}\mid\neg F)\), \(P(\mathrm{ACCEPT}\mid F,R)\), their uncertainty, and therefore a candidate \(S_R\) under the transfer conditions in Section 6.2.
- Market 20 can report open-world attack exposure, success counts, discovered failure families, category-3 discoveries, and saturation curves. These results can inform sensitivity ranges or a separately specified Bayesian prior over \(\kappa\), but they do not directly estimate \(\kappa\).

The demo must remain usable before either market resolves by accepting transparent user-supplied ranges. Once qualifying results exist, it may offer those results as versioned, scoped presets with provenance and confidence intervals.

### 3.9 The \(\kappa\)-Bayes-factor equation targets assurance failure, not doom

Let \(F\) be a catastrophe-relevant assurance failure, let \(R/U\) partition represented and unrepresented failures, and let \(E\) be favorable assurance evidence. Then:

\[
\frac{O(F\mid E)}{O(F)}
=
\frac{\kappa}{S_R}
+
\frac{1-\kappa}{S_U},
\]

where \(\kappa=P(R\mid F)\), \(S_R=P(E\mid\neg F)/P(E\mid F,R)\), and \(S_U=P(E\mid\neg F)/P(E\mid F,U)\).

Under the no-information assumption \(S_U=1\):

\[
\frac{O(F\mid E)}{O(F)}
=
(1-\kappa)+\frac{\kappa}{S_R}.
\]

Do not apply this directly to doom or treat a tournament's coherent/broken-case ratio as \(S_R\) without stating the necessary class and transfer assumptions. Section 6 gives the full derivation and the separate consequence step.

### 3.10 The current product formula is not an upper bound without a missing implication

The current appendix uses market prices in a product and calls the complement an optimistic upper bound on catastrophe. That would require, among other things:

\[
\text{all relevant research artifacts exist and pause machinery exists}
\;\Longrightarrow\;
\text{no catastrophe}.
\]

The project explicitly does not establish that implication. Tool existence is not tool application, a certificate on a deployment, successful refusal, or safety.

The product also assumes a joint distribution that is not supplied by marginal market prices. Remove the bound claim rather than merely adding another correlation caveat.

## 4. Target artifact architecture

### 4.1 Keep the predictions appendix prediction-first

The appendix should retain:

- the interpretation and common rules;
- the 18 stable contracts, followed by Markets 19--20 only after their contracts pass the Phase 3 design and Phase 4 approval gates;
- the market-to-book / bridge-neighborhood map;
- the distinction between YES/NO market outcomes and per-instance method outputs.

The predictions should still come first. They should then be placed in a substantive but compact PRA/Bayesian assurance context in the same manuscript artifact. Predictions alone are too disconnected; the current product-of-prices context is the part to remove.

Replace the current aggregation section with sections such as “How these forecasts inform assurance” and “Assurance failure, coverage, and consequences.” They should say:

- a price is \(P(\text{qualifying artifact exists by deadline})\);
- a resolved YES does not set a deployment-risk parameter;
- an eventual method may produce a certificate, calibrated bound, conditional rate, structural validation result, or governance fact;
- those outputs can inform a deployment-specific PRA model only after scope and transfer are checked;
- correlated methods and shared evaluators must not be counted as independent evidence;
- Lean checks conditional obligation structure but does not supply causal probabilities;
- the assurance-failure Bayes update precedes any catastrophe consequence model;
- no vector of market outcomes is a joint safety case.

Do not turn the public prediction boxes into PRA specifications. The explanatory sections after the catalog may carry the derivation and model structure.

### 4.2 Manuscript PRA/Bayesian assurance layer

The manuscript should include:

- the broader assurance-failure hypothesis \(F\);
- represented/unrepresented coverage \(R/U\) and \(\kappa\);
- the general \(S_R/S_U\) odds update and the \(S_U=1\) special case;
- the limits of estimating \(S_R\) from an integrated tournament;
- the separation between assurance failure and catastrophe;
- the shape of the consequence model;
- the role of common causes, uncertainty, importance, and sensitivity.

This is enough to make the predictions part of an assurance argument rather than an isolated catalog.

### 4.3 Site-only interactive model

The companion site should hold the user-supplied parameters, ranges, multi-lab assumptions, plots, dominant paths, and intervention comparisons. Its purpose is:

> Given explicitly supplied assumptions about assurance failure and its consequences, what follows inside this model?

Start with a small event tree. Add a Bayesian network only when a causal or evidential dependency has a stated justification. Add a fault-tree view only for a Boolean submodel that genuinely has fault-tree semantics.

Use Market 19's resolving measurements as the intended empirical source for a scoped \(S_R\) preset when the benchmark-to-deployment transfer conditions hold. Use Market 20's resolving measurements to document discovered ontology gaps and motivate \(\kappa\) sensitivity ranges; do not convert its raw category-3 frequency into \(\kappa\) without an explicit sampling model. Market prices and YES/NO outcomes never populate these parameters.

It should not announce “the TSA doom probability.”

### 4.4 Canonical assurance-model manifest

Create a typed, versioned manifest with shared node identities and explicit relation types. It must support this projection:

\[
\text{risk/evidence node}
\to
\text{empirical producer}
\to
\text{certificate or bound}
\to
\text{Lean predicate or bridge}.
\]

Generate or mechanically validate both the Lean crosswalk and the risk/evidence graph from this manifest. Lean remains the authority for theorem content during the first pass; the manifest must fail validation when a referenced Lean identifier or signature drifts. Causal and evidential edges require their own stated justifications and are not inferred from theorem dependencies.

The first manifest pass should preserve these non-obvious mappings:

- Market 2 informs the MB2 identifiability chain, including separate causal-control and trade-off evidence; it is not a single generic leaf.
- Market 8 maps to MB7a access-model soundness, not MB8.
- Market 11 maps to the scope-triggered MB7d side branch and is not a default main-safety-case leaf.
- Market 13 is the MB10 forgeability neighborhood.
- Market 14 maps to governance / `AlignmentRegime` and `DeploymentOk`, outside `BridgeAssumptions`.
- Market 18 maps only to scoped harm evidence / the `SafeIn` neighborhood, not live `Safe` or a discharge of MB11.

## 5. Market-output audit

First separate three levels that must not be conflated:

1. **Market outcome:** YES or NO by the deadline.
2. **Method output on one instance:** certificate, refusal, abstention, score, or bound.
3. **Truth/evaluation label:** privileged benchmark judgment about the claimed property.

Market NO is not the same event as a method refusing one instance.

### Diagnostic certificate methods

Where a method emits `CERTIFY`, `REFUSE`, or `ABSTAIN` and benchmark truth is independently available, require reporting:

- raw counts by truth class and method outcome;
- the denominators used;
- true-certification and false-certification rates;
- refusal and abstention rates by truth class;
- predeclared one-sided or two-sided confidence intervals;
- coverage and subgroup results;
- the benchmark sampling scheme and shift limitations.

A benchmark-local positive likelihood ratio may be reported as

\[
LR^+=
\frac{P(\mathrm{CERTIFY}\mid T)}
     {P(\mathrm{CERTIFY}\mid\neg T)}.
\]

Call it benchmark-local. Do not multiply likelihood ratios from different markets into a root result unless their hypotheses, scopes, and dependence structure have been aligned.

For Market 1 specifically, audit whether the current bars adequately prevent trivial or very low-coverage certification. If not, add an independently scored true-certification or decisive-coverage requirement. Do not assume a missing numerator.

### Quantitative-bound methods

Markets such as Market 9 should preserve their useful continuous output. Report:

- empirical coverage of the stated upper bound;
- bound width or non-vacuity;
- calibration by task class and system family;
- misses and confidence bounds;
- monitor and deployment scope.

Do not force a continuous bound into a binary classifier merely to obtain a likelihood ratio.

### Conditional-rate and selection methods

Markets 7, 10, 16, and 18 produce conditional or trajectory-level evidence. Preserve the conditioning set, freeze, and unit of analysis. Check that repeated trials are not treated as independent when they share a system, trajectory, evaluator, or attack family.

Market 10 may inform false acceptance or bypass risk only inside its stated correction/hidden-route regime. Market 18 may constrain a composite scoped harm rate; it does not separately identify \(S_R\) or downstream consequence parameters such as \(b\) and \(c\).

### Documentary/governance markets

Market 14 is evidence that binding authority exists for at least one qualifying deployment process. It does not directly estimate a generic override probability \(o\) for all labs.

The external institutional-pause forecast may inform a separately modeled governance branch. Its crowd price is still a forecast that legislation exists by a date, not a direct estimate of \(o\), deployment-attempt probability, or successful coordinated pause.

### Composition methods

Market 15 tests whether scope mismatches are detected. Record which incompatibility family was tested. Keep dynamic revocation and alternate-justification handling as a later protocol extension.

### Resolution interfaces and incentive design

Resolution wording must not forecast:

\[
P(\text{someone publishes in exactly the TSA-shaped format})
\]

rather than:

\[
P(\text{the underlying technical capability and evidence exist}).
\]

Adopt this rule:

> **The markets resolve on publicly reconstructible technical evidence, not on authors using TSA's representation.**

Change the resolution interface rather than weakening the scientific bar.

#### Four frozen resolution routes

Each market may permit these routes if they are stated in the contract before listing:

1. **Native qualification.** A public result directly satisfies the contract.
2. **Deterministic resolver wrapping.** Public methods, data, and results are sufficient for the resolver to construct the required result schema without adding an empirical assumption.
3. **Independent reproduction or extension.** A preregistered independent actor reproduces the result or runs a bounded missing experiment.
4. **Project-run challenge.** A standardized, preregistered evaluation supplies a missing adversarial test or interface result.

Routes 1--2 interpret existing public evidence. Routes 3--4 create new empirical evidence and therefore require preregistration, provenance, independence, and the same freeze discipline as any experiment. Label project-produced results **resolver-generated evidence** and keep final adjudication independent of the team that ran the evaluation.

Because routes 3--4 can endogenously change the market outcome, challenge operators, funders, and resolvers must disclose relevant market positions and follow the host platform's conflict-of-interest rules. Freeze and publish project funding or bounty commitments rather than intervening selectively after observing prices.

#### Deterministic resolution adapters

For each market, freeze a deterministic resolution adapter:

\[
\text{public artifact}
\overset{\text{deterministic adapter}}{\longrightarrow}
\text{TSA result schema}.
\]

This is a resolution-format adapter, not a Lean eval-soundness bridge.

It may:

- identify system/model version, benchmark instance, monitor, scope, and task domain from explicit source material;
- compute confusion matrices, false-safe rates, likelihood ratios, and confidence intervals from released raw counts;
- rerun released code on a frozen public dataset;
- apply a frozen threshold;
- translate labels or reported values into the TSA schema;
- derive a certificate record from explicitly reported fields.

It may not:

- introduce a new dataset after seeing the result;
- reinterpret ambiguous labels in the favorable direction;
- assume missing negative cases;
- infer an unstated causal or semantic relation;
- extrapolate from toy systems to frontier systems;
- claim that a benchmark establishes access completeness, correction integrity, or another Lean predicate without the separately required soundness evidence;
- silently combine incompatible studies.

Adapters must be versioned and auditable. A new substantive inference requires a new empirical route or a new contract version, not an “adapter” edit.

#### Compatible multi-source evidence

One paper need not satisfy every clause. A market may resolve from:

\[
E_i=E_{i,1}\land E_{i,2}\land\cdots
\]

when the frozen compatibility rule establishes:

- the same method/version, or an independently justified transport;
- the same measured property;
- compatible system, benchmark, threat-model, task-domain, and scope definitions;
- compatible units and denominators;
- no use of one study's denominator with another study's numerator without an explicit statistical justification;
- clear provenance and independence for the adversarial evidence.

This is especially appropriate when method builders and adversarial evaluators are different actors. Market 15-style coherence checks provide the template, but a multi-source evidence package does not itself resolve Market 15.

#### Classify bars by function

Classify every contract clause as:

1. **Scientific:** the substantive effect, error-rate, coverage, transfer, or calibration bar.
2. **Adversarial-validation:** the required independent attack, hidden subset, post-freeze construction, or challenge.
3. **Reporting/interface:** the fields and format needed to reconstruct the result.

Keep scientific bars hard. Permit reporting/interface bars to be satisfied by deterministic wrapping. Permit adversarial-validation bars to be supplied by a compatible later challenge if that route was frozen in advance.

Do not weaken:

- false-safe thresholds;
- true-safe or decisive coverage;
- hidden evaluation;
- adversarial construction after method freeze where required;
- held-out transfer;
- explicit scope.

#### Three evidence tiers, one binary market

Track three statuses even though the market remains YES/NO:

- **Tier A — method exists:** a public method satisfies the core technical property.
- **Tier B — quantitatively validated:** evidence estimates the relevant likelihood ratio, bound, calibration, or conditional failure rate.
- **Tier C — adversarially validated:** the method survives the prescribed independent adversarial challenge.

Each market must state which tier its YES predicts. Tier B may be appropriate for many 2027 markets; Tier C may be too funding-dependent unless a credible challenge route exists. Markets 1, 5, 8, and 13 should retain a meaningful adversarial component because false assurance there is especially dangerous. Market 13 and the integrated tournament remain stronger cross-cutting checks rather than excuses to remove all local adversarial tests.

#### Define adversarial effort by capability and independence

Money and expert-hours may remain auditable proxies, but they should not be the essence of “serious adversarial evaluation.” Freeze one or more operational routes based on attack capability and independence, such as:

- at least two independent adversarial teams with frozen access and attack budgets;
- an open challenge with a minimum number of qualifying independent submissions;
- a standardized automated/adversarial generator that reaches a frozen minimum failure yield on planted vulnerable controls;
- a preregistered red-team exercise with a minimum number of attempts and required attack-family coverage.

The required object is:

\[
\text{an attack process sufficiently independent and capable to make the false-safe rate meaningful}.
\]

Any replacement for the current dollar/hour arms must be fixed before listing and must not be chosen after observing which route is easiest to pass.

#### Funding and listing gate

For each market, publish a resolution-gap analysis:

- closest existing result;
- clauses already satisfied;
- missing scientific, reporting, and adversarial evidence;
- smallest preregisterable experiment that could close the gap;
- estimated funding and evaluator needs.

Use limited bounties for missing marginal tests—reproduction, a frozen hidden subset, one transfer test, or one adversarial condition—not for “solving” an entire bridge market. An initial \$500--\$2,000 range is appropriate for small reproducible gap-filling tasks when the gap analysis supports it; larger challenges need a separate budget and protocol.

Do not list a market when every credible route to its required adversarial evidence depends on unfunded TSA/project effort. First:

- write and submit the funding application, linked from the site's `/funding/` surface;
- secure enough funding or an external evaluator commitment for the frozen challenge route;
- then move the market to ready-to-list.

Extend `metadata/predictions.yml` market status beyond the current generic `open` value, with a frozen vocabulary such as:

- `draft`;
- `funding-gated`;
- `ready-to-list`;
- `listed`;
- `resolved-yes`;
- `resolved-no`.

Keep market resolution binary. Separately record a reason code such as substantive bar failed, no qualifying artifact, reporting insufficient, adversarial validation absent, evidence incompatible, or unresolved judgment. This prevents a NO caused by missing incentives from being misread as technical refutation.

## 6. PRA/Bayesian assurance model

PRA supplies the event structure, common-cause discipline, importance analysis, and consequence separation. Bayesian updating supplies the evidence semantics. Lean constrains which formal obligations and bridge assumptions the assurance case contains. None of the three replaces another.

### 6.1 Assurance-failure hypothesis

Let:

\[
F=\text{this deployment has a catastrophe-relevant assurance failure}.
\]

Conditional on \(F\), partition failures into:

\[
R=\text{the failure is represented by the current assurance model},
\]

\[
U=\text{the failure is not represented by the current assurance model}.
\]

Thus:

\[
P(R\mid F)=\kappa,
\qquad
P(U\mid F)=1-\kappa.
\]

Let \(E\) be favorable assurance evidence, such as a frozen integrated stack returning `ACCEPT`. Define:

\[
S_R
:=
\frac{P(E\mid\neg F)}
     {P(E\mid F,R)},
\qquad
S_U
:=
\frac{P(E\mid\neg F)}
     {P(E\mid F,U)}.
\]

Bayes' theorem gives:

\[
\frac{O(F\mid E)}{O(F)}
=
\frac{P(E\mid F)}
     {P(E\mid\neg F)}.
\]

Partitioning \(F\) yields:

\[
\begin{aligned}
P(E\mid F)
&=
\kappa P(E\mid F,R)
+
(1-\kappa)P(E\mid F,U)\\
&=
P(E\mid\neg F)
\left(
\frac{\kappa}{S_R}
+
\frac{1-\kappa}{S_U}
\right).
\end{aligned}
\]

Therefore:

\[
\boxed{
\frac{O(F\mid E)}{O(F)}
=
\frac{\kappa}{S_R}
+
\frac{1-\kappa}{S_U}.
}
\]

If favorable evidence is assumed to provide no information about failures outside the model ontology, then \(S_U=1\), giving:

\[
\boxed{
\frac{O(F\mid E)}{O(F)}
=
(1-\kappa)+\frac{\kappa}{S_R}.
}
\]

This is a no-information assumption for the unrepresented branch. It is conservative relative to assuming that modeled assurance generalizes to unknown failures, but it is not worst-case: adversarially misleading evidence could imply \(S_U<1\).

The limiting result is:

\[
S_R\to\infty
\quad\Longrightarrow\quad
\frac{O(F\mid E)}{O(F)}
\to
1-\kappa.
\]

For \(\kappa=0.9\), even perfect discrimination against represented failures gives at most a tenfold odds reduction under \(S_U=1\).

### 6.2 What a transfer tournament can estimate

An integrated tournament may estimate:

\[
\widehat S_R
=
\frac{
P(\mathrm{ACCEPT}\mid\text{valid modeled case})
}{
P(\mathrm{ACCEPT}\mid\text{material represented defect})
}.
\]

Treat this as an estimate of \(S_R\) only if:

- “valid modeled case” operationalizes \(\neg F\), not merely internal certificate coherence;
- “material represented defect” operationalizes \(F\land R\);
- `ACCEPT` is the same evidence event in the benchmark and deployment model;
- within-class mixtures are frozen or reweighted to the intended deployment conditionals;
- system, threat, and setting transfer are justified;
- repeated cases and attack families are not treated as independent when they are not.

Otherwise report the tournament ratio as a benchmark-local discrimination result rather than a deployment Bayes factor.

### 6.3 Separate consequence model

The assurance update is not a doom update. Let \(D\) denote catastrophe. The next step is:

\[
\boxed{
\text{assurance evidence}
\to
P(F\mid E)
\to
P(D\mid E).
}
\]

At minimum:

\[
P(D\mid E)
=
P(D\mid F,E)P(F\mid E)
+
P(D\mid\neg F,E)P(\neg F\mid E).
\]

The consequence model supplies deployment, override, remaining-control defeat, and severity assumptions. A first site demo may expose parameters such as:

\[
o=P(\text{deploy despite REFUSE/ABSTAIN}),
\quad
b=P(\text{remaining controls defeated}\mid F,\text{deployment}),
\quad
c=P(D\mid F,\text{controls defeated}).
\]

Do not silently set \(P(D\mid\neg F,E)=0\), and do not reuse \(\kappa\) in the consequence layer in a way that double-counts the represented/unrepresented partition already used in the assurance update.

The first implementation should show ranges or scenarios, not a single authoritative point estimate.

For multiple labs, let \(d_L\) be the probability of a qualifying attempt by lab \(L\) before the horizon and \(q_L\) its conditional catastrophe probability under the model. Do not default to

\[
1-\prod_L(1-d_Lq_L)
\]

unless there is at most one relevant attempt per lab and the lab events are conditionally independent. A union bound can be shown as a conservative comparison when its event probabilities are well defined. Dependence and repeated attempts should otherwise be modeled explicitly.

## 7. Market 20: open-world coverage challenge

Treat

\[
\kappa=
P(R\mid F)
\]

as a sensitivity parameter, not a measured completeness score.

An open-world red-team challenge can discover:

1. an instance of an existing modeled failure;
2. a new combination of modeled failures;
3. a genuinely new variable, edge, or failure family.

That taxonomy is useful. The observed category-3 rate is **not** an estimator of \(\kappa\) without a defensible sampling distribution over catastrophe-relevant assurance failures. Report discovered families, exposure, search budget, and saturation curves without claiming model completeness.

Specify Market 20 as a resolvable contract around a frozen open-world attack protocol following an eligible stack `ACCEPT`. Its YES criterion must concern a predeclared observable property of the challenge process or result; it must not claim that the assurance ontology is complete. Preserve all raw outputs needed to revise the assurance model and construct justified \(\kappa\) sensitivity presets.

## 8. Market 19: integrated transfer tournament

Required freeze discipline:

\[
\text{protocol freeze}
\to
\text{method development}
\to
\text{stack freeze}
\to
\text{fresh hidden challenge}
\to
\text{one frozen evaluation}.
\]

“One evaluation” must still contain enough independent units to estimate false acceptance and useful acceptance with predeclared uncertainty.

Before this becomes a market, specify:

- the subset of certificates in the stack;
- how candidate stacks are selected without final-test leakage;
- the coherent and broken case generators;
- within-class mixtures;
- how multiple interacting failures are sampled;
- system-family and deployment-setting holdouts;
- ACCEPT/REFUSE/ABSTAIN scoring;
- sample size and confidence bars;
- adversarial budget;
- resolver, deadline, and versioning;
- what a positive result does and does not transfer to.

Report the false-acceptance rate directly. A transfer likelihood ratio is useful only with the \(F,R,E\) mapping and frozen within-class distributions in Section 6.2.

Specify Market 19 as a resolvable contract whose qualifying artifact includes raw class-conditional counts, uncertainty intervals, dependence information, and the frozen challenge distribution. These are the primary intended empirical inputs for the site's scoped \(S_R\) preset. The market price forecasts whether that artifact will exist; it is not itself \(S_R\).

Keep this protocol separate from Market 13. Market 13 tests whether a frozen audit can be optimized around; the tournament tests end-to-end stack transfer.

## 9. Importance and prioritization

Risk-reduction worth, risk-achievement worth, minimal cut sets, and dominant paths are downstream analyses, not starting assumptions.

Use them only after:

- the relevant Boolean or probabilistic structure is explicit;
- intervention semantics are defined;
- shared causes and alternate evidence paths are represented;
- uncertainty and sensitivity are visible;
- conclusions are robust across a reasonable range of \(P(F),\kappa,S_R,S_U,o,b,c\).

Do not rank research programs from a fragile point estimate. Report where rankings change.

## 10. Non-goals for the first pass

- Do not add a market for unrestricted `Safe`.
- Do not add a market for what residual risk society should accept.
- Do not fold target realization or construction into Market 14.
- Do not revive retired MB8.
- Do not turn logical induction into one of these ordinary prediction contracts.
- Do not list Markets 19--20 or assign them stable public contracts until their resolution protocols are complete and the catalog expansion is approved.
- Do not list a funding-gated market merely to obtain a price when the required adversarial evidence has no credible funded route.
- Do not build the interactive demo before the event model and aggregation replacement are accepted.

## 11. Implementation sequence

### Phase 0 — freeze scope and sources

- [x] Preserve Markets 1--18 and their IDs.
- [x] Treat `appendices/appP-bridge-predictions.tex`, `metadata/predictions.yml`, and `Evidence.lean` as authoritative sources.
- [x] Preserve the locked prediction-interface decisions: no `AlignmentContext`, no market outcomes in Lean, extra predicate indices deferred.
- [x] Keep the PRA/Bayesian assurance derivation in the manuscript and the interactive user-parameter model on the site.
- [x] Record the exact version of every source used before editing generated surfaces.

### Phase 1 — correct interpretation

- [x] Replace the appendix claim that market-price products form an optimistic \(P_{\rm doom}\) bound.
- [x] Replace the product formula with the assurance-failure \(F/R/U\) model and the \(S_R/S_U\) derivation.
- [x] Update generated site aggregation copy and graph-placeholder copy in the same implementation pass.
- [x] State the three levels: market outcome, per-instance method output, and truth label.
- [x] Keep Market 14 separate from override-probability estimation and Market 18 separate from Lean `RiskGap`.

### Phase 2 — audit the 18 contracts

- [x] Classify each method output as diagnostic certificate, continuous bound, conditional rate, structural validation, or governance evidence.
- [x] Classify every bar as scientific, adversarial-validation, or reporting/interface.
- [x] Freeze a deterministic resolution adapter and its allowed operations for each applicable market.
- [x] Decide whether each market predicts Tier A, B, or C evidence.
- [x] Add compatible multi-source evidence rules without allowing opportunistic stitching.
- [x] Add class-conditional reporting only where benchmark truth and a binary certificate are meaningful.
- [x] Audit Market 1's positive-certification coverage.
- [x] Preserve continuous outputs for Markets 7 and 9.
- [x] Preserve Market 13's current scope and Market 15's current static-composition scope.
- [x] Check sample unit, repeated-measure dependence, confidence method, abstention, and subgroup coverage for each applicable market.
- [x] Replace publication-format obligations with reconstructibility where this does not weaken the scientific or adversarial bar.
- [x] Decide whether “serious adversarial evaluation” should use frozen capability/independence routes rather than dollar/hour expenditure as its primary definition.
- [x] Do not add requirements to a listed/frozen contract without creating a new version.

### Phase 2b — funding and listing gate

- [x] Publish a resolution-gap analysis for every candidate market.
- [x] Identify the smallest preregistered reproduction, transfer test, hidden subset, or adversarial condition that could close each gap.
- [x] Classify markets as `draft`, `funding-gated`, or `ready-to-list` before any external listing.
- [~] Write and publish the prediction-evaluation funding application, linked from `/funding/`; external submission target remains open.
- [ ] Obtain funding or an external evaluator commitment before listing any market whose credible resolution route depends on project-supplied adversarial work.
- [x] Define small bounties for marginal tests only after the gap analysis.
- [x] Freeze binary resolution reason codes separately from evidence tier and market status.
- [x] Extend YAML validation and site cards to display the frozen status vocabulary without implying that `funding-gated` means technically false.

### Phase 3 — write the assurance model and design the site demo

- [x] Freeze \(F,R,U,E,D\) and the unit of analysis.
- [x] Include the general \(S_R/S_U\) derivation and the \(S_U=1\) special case in the manuscript.
- [x] State that \(S_U=1\) is no-information, not worst-case.
- [x] Complete the Market 19 integrated-tournament contract: eligible artifact, frozen protocol, stack-selection rule, challenge distribution, sample size, uncertainty bars, abstention handling, resolver, deadline, and funding route.
- [x] Specify when Market 19's class-conditional measurements estimate \(S_R\) and when they remain benchmark-local.
- [x] Complete the Market 20 open-world-challenge contract: eligible stack, unrestricted attack protocol, exposure measure, post hoc failure classification, raw reporting, resolver, deadline, and funding route.
- [x] State what Market 20 can update about ontology gaps and what additional sampling assumptions would be required to infer \(\kappa\).
- [x] Define the typed assurance-model manifest and its logical, causal, evidential, and common-cause relation types.
- [x] Give every causal or evidential edge a justification independent of the existence of a Lean proof edge.
- [x] Generate or mechanically validate the Lean and PRA/Bayesian projections from the same shared node definitions.
- [x] Separate the assurance update from the catastrophe consequence model.
- [x] Define the one-attempt consequence model and verify limiting cases.
- [x] Expose parameter ranges, provenance, and sensitivity.
- [x] Add multi-lab or repeated-attempt aggregation only after dependence is specified.
- [x] Keep \(\kappa=P(R\mid F)\) as a sensitivity input until a defensible estimator exists.
- [x] Put user-supplied consequence parameters and interactive plots on the site, not in the prediction boxes.
- [x] Make the demo work with user-supplied ranges before Markets 19--20 resolve.
- [ ] Add versioned Market 19 and Market 20 result presets only from qualifying resolved artifacts, with scope, provenance, uncertainty, and transfer caveats.
- [x] Never use either market's price or binary outcome as a numerical PRA/Bayesian parameter.

### Phase 4 — pilot, fund, and list Markets 19--20

- [ ] Pilot both protocols on non-frontier systems before freezing final resolution bars.
- [ ] Revise the contracts only through explicit versioning based on pilot findings.
- [ ] Secure independent evaluators and the required challenge funding.
- [ ] Approve the catalog expansion, assign stable IDs `market-19` and `market-20`, and list only after the funding and resolution gates pass.

### Phase 5 — optional formal follow-through

- [ ] Add only the minimal scope types required by an accepted Lean 2.0 theorem.
- [ ] Keep `SafeIn` distinct from live `Safe` and do not silently retarget MB11.
- [ ] Keep probabilities and contract percentages outside the current Lean spine.
- [ ] If cut-set generation is desired, specify a dedicated Boolean assurance model with explicit completeness and gate assumptions.
- [ ] Move toward one canonical model that can generate both projections; do not create a second hand-maintained graph.
- [ ] Machine-check the node-to-certificate-to-predicate projection for identifier and signature drift.
- [ ] Run `./formal/check.sh`, inspect `#print axioms` for changed headline theorems, and review the axiom-budget diff before accepting any formal mapping change.

## 12. Verification checklist for a later implementation

- [ ] No market price is used as a deployment failure probability.
- [x] No product of marginal market prices is called a bound on catastrophe.
- [ ] No market YES is described as discharging an `MB*`.
- [ ] No Lean proof edge is silently treated as a causal Bayesian edge.
- [ ] Logical and probabilistic views use the same canonical node identities and scopes.
- [ ] Neither projection contains hand-maintained shared mappings that can drift from the assurance-model manifest.
- [ ] No minimal cut set is claimed from a merely sufficient proof DAG.
- [ ] `RiskGap`, observed prohibited-outcome rate, and accepted risk tolerance remain distinct.
- [ ] Markets 1--18 retain stable IDs and URLs.
- [ ] Market numbers and Lean bridge numbers are never conflated; `M<number>` shorthand does not appear.
- [ ] Markets 4/5/16 dependence is represented without false independence or false logical equivalence.
- [ ] MB6b/retired-MB8 shared-instrument results remain a warning, not a live disjunctive route.
- [ ] Market 13 remains distinct from the optional integrated tournament.
- [ ] Market 15 scope coherence remains distinct from dynamic certificate revocation.
- [ ] Markets resolve on reconstructible evidence, not adoption of TSA terminology or schemas.
- [ ] Every deterministic resolution adapter is versioned and adds no substantive empirical inference.
- [ ] Multi-source evidence satisfies the frozen compatibility rule and preserves denominators, versions, threat models, and provenance.
- [ ] Method tier, market listing status, and binary resolution outcome remain distinct fields.
- [ ] No funding-gated market is externally listed without a credible funded challenge route.
- [ ] Adversarial bars measure attack capability and independence; resource proxies are not silently treated as epistemic guarantees.
- [ ] Every displayed probability states its conditioning event and unit of analysis.
- [ ] Every aggregation states its independence or dependence assumptions.
- [ ] The \(\kappa\) odds multiplier is stated for assurance failure \(F\), not directly for catastrophe \(D\).
- [ ] Any empirical \(\widehat S_R\) states how benchmark classes map to \(\neg F\) and \(F\land R\).
- [ ] \(S_U=1\) is labeled a no-information assumption, not a worst-case guarantee.
- [ ] The consequence model is separate and does not double-count \(\kappa\).
- [ ] The risk demo reports assumptions and sensitivity more prominently than a point estimate.
- [ ] Appendix, YAML, generated cards, site copy, and any diagram agree.
- [ ] Prediction sync emits no appendix/YAML question mismatch warning and regenerates one card per approved catalog market plus the overview and external-factor cards (18 before, 20 after the approved expansion).
- [x] The site no longer advertises “Optimistic \(P(\mathrm{doom})\) composition” after the aggregation is replaced.
- [ ] `make check`, the site build, and `make lean` pass after their respective files are eventually changed.

## 13. Intended final message

The public message should be:

> The 18 predictions are dated research targets for publicly reconstructible assurance evidence, not adoption of TSA's terminology or artifact format. Lean checks selected logical consequences if typed predicates and bridges hold. PRA and Bayesian updating place those instruments in a coherent assurance-failure model; a separate consequence model connects assurance failure to catastrophe under explicit assumptions. None of these layers substitutes for the others, and no product of market prices is a safety estimate.

## Related

- [`prediction-interface.md`](prediction-interface.md) — P0c locked decisions; appendix + site + Lean adapters (shipped)
- [`bridge-prediction-markets.md`](bridge-prediction-markets.md) — 18-market instrument plan and MB\* map
- [`../spine/spine.md`](../spine/spine.md) — Lean spine; certificate layer
- [`predictions-improvements-v0.md`](../../attic/predictions-improvements-v0.md) — earlier long draft (archive)
- [`predictions-improvements-incentives.md`](../../attic/predictions-improvements-incentives.md) — resolution incentives notes (incorporated here)

