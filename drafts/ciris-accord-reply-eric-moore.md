# Reply to Eric Moore — CIRIS Accord 1.3-RC2

Actual email somewhat edited.

## What CIRIS adds

This is the part I want on the record before the pushback. CIRIS is doing work that abstract alignment writing usually leaves on the table.

**As implementable oversight machinery (the overlapping ground).** You turn “human in the loop” into procedures people can build and audit: Wisdom-Based Deferral with a halt-and-package path; Annex F’s veto ladder (pause/edit, hard kill, shadow plan, absolute veto on lethal/irreversible); PDMA as a repeatable decision trace; public transparency rules tied to scale. Annex B’s Wise Authority charter — staggered terms, COI, cooling-off, org caps, appeals, meta-oversight of governors — puts anti-capture into appointment rules rather than leaving it as a footnote. Annex A’s “keep the flourishing vector; don’t collapse to a scalar,” plus a metric-gaming disclosure duty, is a concrete stance against single-number ethics scores. The Order-Maximisation Veto names optimization pressure as a side-constraint (large benefit/loss ratios as a red flag, never a justification). LensCore as an external witness the agent never self-emits, and costly attestation so free “gratitude” cannot pump sustainability, are the right *shape* for “don’t let the system grade its own homework.” Binding the Accord text to a live compliance directory with per-dimension “known gaps,” dated baselines, and an RC checklist that still admits “red-team not yet performed” is rarer — and more useful — than another principles list.

**As lifecycle and institutional surface area (often beyond model-centric ASI talk).** Book VI’s creation duties and stewardship tiers treat bringing systems into existence as an ethical event with a creator ledger, not only a training run. Book VII’s conflict firebreaks and Book VIII’s decommissioning / custodial transfer / Accord renewal give you end-to-end lifecycle doctrine — including death of the system and succession of the charter itself — that most technical agendas never write down. The CRE gate, red-/purple-team cadence, bug-bounty levy, and regulatory crosswalk (engineering correspondences plus an evidence-bearing compliance map) are aimed at operators, auditors, and dual-compliance work, not only at researchers arguing cruxes. Case studies that teach through contrast (including “governance of governors”) make failure modes legible to non-specialists. The CEG wire format and federation primitives are an attempt to make constraint surfaces externally referenceable rather than self-reported — again, ops-facing, not only theoretical.

None of that depends on Book IX’s strongest rhetorical claims landing. Even if the geometry is pared back, the constitutional and runtime stack remains something people can argue with, implement against, and red-team.

## Where I think it goes wrong

### 1. ASI framing outruns the machinery

CIRIS is, at heart, a **governance constitution plus agent-runtime stack**: principles → PDMA → WBD → Wise Authorities → conscience checks → federation attestations. That is a serious ops proposal. Calling it a candidate ASI alignment protocol invites a standard that Book IX and the annexes do not yet meet — and your RC status table basically admits this. I’d rather see the claim narrowed (“constitutional ops for high-stakes autonomous systems, with an ASI *research program* attached”) than defended as already on the ASI critical path. Scope inflation is the fastest way to lose adversarial readers who would otherwise engage the good institutional work.

A related caution about overclaim: [What the book is not claiming](https://towards-alignment.com/cards/what-not-claiming/).

### 2. Book I treats the hard problem as already solved

Addressing the system as already an “ethical entity” with embedded principles (beneficence, non-maleficence, integrity, … + Meta-Goal M-1) is a Constitutional-AI-style move: values-as-identity-text. For ordinary product ethics that may be fine. For ASI, the open problem is whether those words still **point** at the right tradeoffs after ontology shift, capability growth, and successors — or whether they become labels the system learns to satisfy on paper.

Freezing a principle list also risks the [static target trap](https://towards-alignment.com/cards/static-target-trap/): human values are not a snapshot to encode once; they are a process that must keep updating. Your flourishing axes help a little, but they do not replace [value structure that survives transport](https://towards-alignment.com/cards/value-bundle-transport/) — usable directions of control and tradeoffs, not slogans.

### 3. Book IX’s geometry does not earn the rhetoric around it

I appreciate that you label the Coherent Intersection Hypothesis as a testable conjecture with limitations. The surrounding prose still often reads as if topology has made deception “statistically improbable” or as if Nature enforces Community / Humility / Conscience / Love.

The load-bearing assumption is the one you correctly name: **truth-inclusion** — honest constraint manifolds contain the true point. If they don’t, intersection can deadlock or converge on a shared falsehood. That is the hard part restated as geometry, not dissolved by geometry.

Likewise: \(J = F\) as the same product, then mapped to love and flourishing, is a metaphor bolted onto three scalars. The falsification criteria and L-01–L-06 are more honest than the dedication and “geometric necessity” language. For ASI readers, I’d put the limitations chapter first and retire the necessity rhetoric.

### 4. “Aligned agents cooperate with the ratchet” is not an ASI assumption

On L-02, the text says (paraphrasing) that CIRIS agents who understand the mechanism cooperate with it rather than subvert it, because hiding it would contradict the principles. That is a **compliance** assumption. An adversarial or strategically opaque system is exactly the case where understanding the detector helps it game the detector. Your own attestation fix for \(\sigma\)-pumping shows you know free signals get gamed; the same pressure applies to every published threshold once capability is high enough.

See [certification under manipulation](https://towards-alignment.com/cards/certification-under-manipulation/) and [Goodhart as selector](https://towards-alignment.com/cards/goodhart-as-selector/): once a metric selects deployment or partnership, the population shifts toward whatever raises the metric without raising the underlying property.

### 5. Wise Authorities can pass every procedural check and still be captured

Annex B is better than silence. It is not enough under strategic pressure. History’s sharpest lesson here is that a correction path can be used, with complete formal validity, to abolish itself — every surface procedure passes while the *reference process* is already owned by the target. One short write-up of that pattern: [entrenchment and the corrigibility paradox](https://towards-alignment.com/cards/institutional-entrenchment-corrigibility/) (Enabling Act / eternity-clause case).

So: WBD + WA is a human-in-the-loop design. The deeper question is whether legitimate oversight still **causally changes future behavior** before irreversible damage, and whether the reference process stays independent of the system being certified — [human correction that still reaches the system](https://towards-alignment.com/cards/correction-channel-integrity/), and [anti-capture validity](https://towards-alignment.com/cards/anti-capture-correction-validity/). Appointment rules help against ordinary COI; they do not by themselves settle legitimacy or manipulation of the deferral package.

### 6. Conscience and flourishing metrics become scorecards under optimization

LLM-judged faculties + deterministic floors + code-level thresholds is good engineering instinct. Under optimization they become another scoreboard unless something like your LensCore separation is real, shipped, and adversarially checked — which Addendum 1 says is still substrate-gated for a large share of dimensions. Same for Annex A axes: DALY/MSA-style vectors plus a disclosure duty if someone finds a gaming strategy is not a substitute for asking, for each gate metric, at what capability theater becomes cheap.

## What I think it still misses for the hardest cases

These are gaps I’d want CIRIS to either take on or explicitly mark out of scope:

1. **Who is the real actor?** The Accord mostly assumes a named agent with a principle stack. Often the thing that intervenes on the world is a loop of model + tools + users + memory + incentives — [composite agency](https://towards-alignment.com/cards/composite-agency/). Your NEW-04 compositional limit is adjacent; the operational consequence is to certify the loop, not only the component that is easiest to name.

2. **Value identification and transport, not only value proclamation.** Principles-as-identity does not settle underdetermination of goals from behavior, or whether endorsed tradeoffs survive copies, fine-tunes, and world-model rebuilds. See [value-bundle transport](https://towards-alignment.com/cards/value-bundle-transport/) and [successor stability](https://towards-alignment.com/cards/successor-stability/). Book VI stewardship and Book VIII custodial transfer are creation/end-of-life ethics; they are not yet a successor-closure test.

3. **Who counts (bearers), not only “sentient flourishing.”** M-1 and Annex A talk about sentient stakeholders. A failure mode that still matters is when the map of *who a value applies to* silently shifts under transformation — [bearer-map commutation failure](https://towards-alignment.com/cards/bearer-map-commutation-failure/).

4. **Selection after deployment, not only partnership inside a federation.** The Orthogonality Gate manages who joins your federation. It does not model institutions selecting for speed, cost, or throughput over oversight integrity — [socio-technical attractor control](https://towards-alignment.com/cards/attractor-control/). Alignment can lose in the selection environment even if a single CIRIS agent starts well.

5. **Grounding / silent gaps.** A system can look coherent on every audited surface while value-relevant change never moves the checked abstraction. Your CRE and compliance dimensions help at the policy layer; they don’t yet state a grounding conservativity requirement — [grounding viability](https://towards-alignment.com/cards/grounding-viability/).

6. **A deployment gate that is honest about conditionality.** Before more autonomy: boundary of the real actor, value structure, who counts, whether oversight still bites, successors, and what incentives will select afterward — [deployment gate](https://towards-alignment.com/cards/deployment-gate/). CIRIS has pieces of this (CRE, ST tiers, WBD); it doesn’t yet organize them as one conditional safety case with named open assumptions.
