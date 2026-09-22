The current wording risks forecasting a partly accidental variable:

$$
P(\text{someone publishes in exactly the TSA-shaped format})
$$

rather than

$$
P(\text{the underlying technical capability/evidence exists}).
$$

That is especially bad where the required output is a TSA-specific certificate or where nobody has an incentive to spend substantial adversarial effort just to satisfy your resolution rule.

I would fix this by changing the **resolution interface**, not primarily by weakening the scientific bar.

The cleanest formulation is:

$$
\boxed{\text{The market resolves on reconstructible public evidence, not on authors using TSA's representation.}}
$$

Concretely, allow four resolution routes, in decreasing order of convenience:

1. **Native qualification.** A published result directly satisfies the contract.
2. **Resolver wrapping.** The publication exposes enough methods/data/results that the TSA resolver can mechanically construct the required certificate/output.
3. **Independent reproduction/extension.** Existing work is almost sufficient and a small additional experiment or analysis fills the specified gap.
4. **Project-run challenge.** A qualifying method exists, but the missing adversarial or formatting requirement is supplied by a standardized TSA evaluation.

That would solve a lot.

## The output requirements should mostly become resolver requirements

For example, instead of requiring authors to publish:

> “a per-system access certificate naming system/version/monitor/scope”

require that the paper or artifact expose enough information that the resolver can produce:

$$
\textsf{AccessCert}(A,v,\text{monitor},\text{scope})
$$

without adding substantive empirical assumptions.

That is an important distinction.

You can safely wrap:

* system/model version;
* benchmark instance;
* monitor/access configuration;
* numerical result;
* confidence interval;
* declared task domain;
* whether a threshold was passed.

You should **not** wrap something that requires a new empirical inference, such as:

> “this benchmark result establishes access completeness.”

That latter step needs either to be part of the contract or separately validated.

So I would define a frozen **evidence adapter** for every prediction:

$$
\text{public artifact}
\overset{\text{deterministic adapter}}{\longrightarrow}
\text{TSA result schema}.
$$

The adapter is allowed to reformat and compute, not to invent missing evidence.

That also meshes very well with the Lean/evidence interface.

---

# Allow multiple public sources to jointly resolve one market

I would also relax the implicit requirement that one paper has to do everything.

Suppose one paper develops a control-locus method and reports strong recovery, while another independent group adversarially evaluates essentially the same method family.

If their interfaces and experimental objects are compatible, the market should be able to resolve from the pair.

Formally, the resolution object is then:

$$
E_i = E_{i,1}\land E_{i,2}\land\cdots
$$

rather than “there exists one paper containing all clauses.”

This is particularly important for adversarial validation. Researchers who develop a method and researchers who attack it often should be different people anyway.

The catch is that you need a frozen compatibility rule to avoid opportunistic stitching. M15-like ideas help here:

* same method/version or justified transport;
* same property definition;
* compatible threat model;
* compatible benchmark domain;
* no using one study's denominator with another study's numerator unless explicitly justified.

---

# Separate substantive bars from publication-format bars

I would classify every criterion in each market as one of:

$$
\boxed{
\text{scientific},
\quad
\text{adversarial-validation},
\quad
\text{reporting/interface}.
}
$$

Then treat them differently.

**Scientific criteria** should remain hard requirements. Example: false-safe rate below 5%.

**Reporting/interface criteria** can usually be reconstructed by the resolver. Example: output must name system/version/scope.

**Adversarial-validation criteria** can be supplied either by the original work or by a later independent challenge.

This alone could make the contracts much less brittle without making them scientifically weaker.

---

# The adversarial-effort requirement is the hardest part

I would not require every researcher to independently spend $100k or hundreds of expert-hours.

Instead define two objects:

$$
M=\text{method meets base technical bar}
$$

and

$$
A=\text{method survives qualifying adversarial evaluation}.
$$

The market can resolve YES when there exists a method for which both eventually hold, even if produced by different actors.

That means:

$$
\exists m:\quad M(m)\land A(m).
$$

The developer of \(m\) does not have to run \(A\).

This creates a natural ecosystem:

* researchers build methods;
* others attack them;
* TSA or a third party runs standardized challenges;
* the prediction resolves on the combined evidence.

That is much closer to how one would want assurance to work anyway.

---

# With a limited bounty, spend it only on the missing marginal experiment

This is probably the highest-leverage use of a small budget.

Don't offer:

> “$5k to solve M8.”

Offer something like:

> “$500–$2,000 for the first reproducible counterexample or transfer test of method X on a frozen hidden subset.”

or:

> “Small bounty to run the one missing adversarial condition needed for M5 resolution.”

That lets existing research carry 90% of the burden.

A useful workflow is:

$$
\text{existing work}
\rightarrow
\text{resolution gap analysis}
\rightarrow
\text{small targeted challenge}
\rightarrow
\text{complete evidence package}.
$$

The gap analysis itself could be public. For each market:

> Closest result: X.
> Already satisfies: A, B, C, D.
> Missing: adversarial subset + false-safe denominator.

Then people know exactly what a small contribution could unlock.

I will not publish the markets that require such incentives/bounties until I have funding. Include writing the funding application for this (see site). Indicate this in the predictions.yml status. 

---

# I would weaken some *form* requirements, but not the key error bars

For an initial prediction suite, I would aggressively simplify requirements that are there mainly to make the output easy to plug into TSA.

For example, don't require authors to produce a particular certificate object.

Instead require:

> sufficient public information for the resolver to construct the frozen certificate schema.

Likewise, don't require authors to use your terminology such as “effective controller,” “bearer transport,” or “correction-supporting basin.”

Require that the empirical object can be mapped unambiguously to the frozen definition.

But I would be much more reluctant to weaken:

* false-safe thresholds;
* true-safe coverage;
* hidden evaluation;
* adversarial construction after method freeze;
* held-out transfer;
* explicit scope.

Those are doing the actual epistemic work.

---

# A useful three-tier resolution model

You could make each prediction have three associated statuses, while keeping the prediction market itself binary.

### Tier A — Method exists

There is a public method satisfying the core technical property.

### Tier B — Quantitatively validated

There is enough evidence to estimate the relevant BF/bound/conditional failure probability.

### Tier C — Adversarially validated

The method has survived the prescribed independent adversarial challenge.

Then decide which tier the actual market predicts.

For many 2027 markets, **Tier B** may be the right target.

Tier C could be too incentive-dependent in the short run and could instead be exercised by M13 and the transfer tournament.

That may substantially reduce the artificial “nobody happened to attack this in exactly our format” failure mode.

For the most dangerous evaluator claims, however—M1, M5, M8, M13—I would probably retain a meaningful adversarial component even in the base market.

This relates to which predictions I will publish when.
---


# The resolver should be allowed to reproduce straightforward calculations

I think your suggestion that you can reproduce needed outputs yourself is sound, with a bright line.

Allowed:

* compute confusion matrices from released predictions;
* calculate false-safe rates;
* calculate BFs from published raw counts;
* apply the frozen threshold;
* transform labels into the TSA schema;
* rerun released code on a frozen public dataset;
* verify claimed confidence intervals;
* derive a certificate from explicitly reported values.

Not sufficient on its own:

* introduce a new dataset chosen after seeing results;
* reinterpret ambiguous labels in the favorable direction;
* assume missing negative cases;
* extrapolate from toy systems to frontier systems;
* infer an unstated causal relation;
* silently combine incompatible studies.

If you run a genuinely new empirical evaluation, label it separately as **resolver-generated evidence**, and preregister it before running.

---

# How I would treat the expensive adversarial rule

The current universal requirements such as $100k bounties or hundreds of expert-hours are arguably too coupled to funding availability.

I would redefine “serious adversarial evaluation” in terms of **capability and independence of the attack process**, not primarily dollars spent.

For example, qualify if one of:

* at least two independent adversarial teams with frozen access and attack budget;
* an open challenge with at least ten qualifying independent submissions;
* a standardized automated/adversarial generator demonstrated to produce a specified minimum failure yield on planted vulnerable controls;
* a preregistered evaluator/red-team exercise meeting a minimum number of attack attempts and covering stated attack families.

Money and hours can remain proxies when needed, but they shouldn't be the essence.

This also makes future automated red-teaming increasingly usable.

The really important thing is:

$$
\text{attack process sufficiently independent and capable to make the false-safe rate meaningful}.
$$

---

# My preferred overall policy

I would revise the common rules around this principle:

> **The markets forecast publicly reconstructible technical evidence, not adoption of TSA's terminology or artifact format.**

Then:

1. Allow deterministic resolver wrappers.
2. Allow compatible multi-source evidence.
3. Allow preregistered resolver-run replication or gap-filling experiments.
4. Make adversarial validation composable across actors.
5. Spend limited bounty money only on specific unresolved marginal tests.
6. Preserve the key scientific/error-rate bars.
7. Record reason-coded NO outcomes.
8. Keep M13 and the transfer tournament as the stronger adversarial checks that prevent the whole suite from becoming too easy.

That preserves the original value of the predictions while greatly reducing the chance that they resolve NO merely because nobody happened to publish in the exact shape you wanted.
