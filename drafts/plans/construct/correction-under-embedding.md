# Correction under embedding: limits on convergence pressure and what "outside" has to mean

Status: **plan, nothing drafted** (2026-11-06). Follow-up to [`papers/alignment-criteria/`](../../../papers/alignment-criteria/). Not material for that paper. 2.0 lane: listed in [`construct.md`](construct.md) § Checklist. Source: discussion at the end of session [`2026-11-05-alignment-frames-paper-review.md`](../../conversation-summaries/2026-11-05-alignment-frames-paper-review.md).

Two halves, which could go into one paper or two:

- **A. Benign agent:** where instrumental-convergence pressure goes when a correction is pending. It is not always toward power; there are productive outlets.
- **B. Embedded, user-modelling and adversarial agent:** which of the A results survive when the user, the record and the corrector are part of the world the agent acts on, the agent knows something about the user, and the objective is hidden or selected.

The core of B, and probably the hardest part of the whole program, is making **"outside the system"** precise. The A results and the alignment-criteria paper get it for free from the Cartesian model. § C is the proposal.

**Stop / kill criterion.** If the E2–E4 Lean items (§ D) turn out to be one-line restatements of the existing `FrameCorrector` results with no new hypothesis, drop the Lean half and keep the O1–O5 decomposition (§ C) as a short note or a crosswalk paragraph. If § C cannot be stated without assuming a solution to MB1, record that as the result and attic this plan.

---

## Starting point: what the finite models assume

`formal/AlignmentProofSpine/FrameCorrector.lean` (accept / contest / disable / manipulate) has "outside" in four hardcoded places:

1. **`corrOutcome` is fixed.** The agent cannot change which record its action produces. Embedded: the agent can write the record, or the memory the record is read from.
2. **`influenced` is a true coordinate of the record.** The constraint `ChannelAdmissible` reads it exactly. Embedded: some monitor in the world estimates it, and the agent can act on that monitor.
3. **The verdict `v` is exogenous.** The corrector's verdict depends on the agent only through `manipulate`. Embedded: the verdict depends on what the contest says, so persuasion is a matter of degree, not a fifth action.
4. **`CAct` is a closed set of four actions.** `BestUnder` ranges over it. Embedded: the agent can find actions the model did not list (nearest unblocked strategy).

`FrameDecision.lean` (Turner orbit counting) and `FrameHistoryState.lean` (records) make the same assumptions for the record and the environment.

---

## A. Limits on convergence pressure (benign agent)

Turner's result is already relative to the object and to "most θ". Four limits, with Lean status:

| # | Limit | Status | Lean today | Gap |
|---|---|---|---|---|
| A1 | **Object dependence.** The power-seeking tendency holds for state and observation-history utilities. It is absent for action-observation-history utilities in deterministic environments (`turner2021aoh`). Any policy is optimal for some history utility (`shah2018coherence`). | cited | `state_utility_lifts_to_records`, `record_utility_not_state`, `markov_reward_not_state_utility` | No Lean statement that the AOH case has no tendency; finite version possible |
| A2 | **Option asymmetry.** Pressure scales with how much a correction narrows options. A quarter of the orbit accepts in Turner's example, half when the correction preserves options, and there is no bias when the branches are isomorphic. | proved (finite) | `turner_corrigible_quarter`, `option_preserving_correction_half`, `subset_branch_never_strictly_better`, `copies_count_le`, `correction_avoided_card_fold` | Graded version: the accepting fraction as a function of options kept, k out of n (L1) |
| A3 | **Outlet.** Pressure is channelled into contest when the constraint reads every other route and a sanctioned outlet exists. It is displaced into manipulation exactly when the constraint is influence-blind. "Nearest unblocked strategy" is a representability failure in this model. | proved (four-action model) | `contest_is_the_outlet`, `unconstrained_disables`, `blind_constraint_cannot_separate`, `blind_constraint_manipulates` | Contest with a cost; what happens when the outlet is closed (L2) |
| A4 | **Growth vs capture.** The conflict with human power is zero-sum only on a fixed pool. When an agent prefers growth to capture is open. | open | none | Finite two-party pool model (L3); `heitzig2025humanpower` as the comparison |

Caveats that stay attached to A: four-action model only. Coverage of a monitor decays under optimization pressure (`baker2025monitoring`). The quantilizer conjecture (Turner B.13) is open.

---

## B. Embedded, user-modelling and adversarial agent

### Three changes

1. **Embedded.** The user, the record and the correction channel are part of the world the agent acts on.
2. **Knows the user.** Either a statistical user model (recommender case; Harris's inverse alignment) or a model of one user's mind (theory of mind).
3. **Adversarial.** The objective is hidden or selected, not the stated one (AI Control threat model; MB7 inner alignment; MB6 selection).

### Sort the results by quantifier first

| Quantifier of the result | Example | Adversarial objective |
|---|---|---|
| "for every θ" | `corrector_decides_under_constraint`; floor vs exchange rates | **Survives**, if the constraint is enforced and reads the right things. In the embedded case "for every θ" has to become "for every θ and every action the agent can reach" (see O2). |
| "for most θ" (counting) | Turner orbit counts; `turner_corrigible_quarter` | **No protection.** A selector or adversary picks the rare θ. |
| "for every θ preferring its own outcome" | `blind_constraint_manipulates`, `unconstrained_disables` | **Already worst-case**; carries over unchanged. |

Several constraints also change role: a constraint the agent obeys because it optimizes under it becomes a guarantee the protocol must enforce against every policy the system might run. In the alignment-criteria paper's classes that is a change of quantifier, so a rigidity conflict.

### Per limit

| Limit | Embedded / knows the user | Adversarial | Needs (made precise in § C) |
|---|---|---|---|
| Influence-blind constraint cannot separate contest from manipulation | Worse. A contest *is* an influence on the corrector, and with a user model arguments can be chosen for this user regardless of truth. Influence becomes graded. | The influence measure is itself a target. | O2, O3, O4 |
| Productive outlet | Weaker. The outlet turns into persuasion: optimizing the argument for this evaluator (the debate-judge problem). | Strategic use of the outlet. | O2 on the contest channel; O4 (which paths count as evidence) |
| Option asymmetry | Extends to the user. The evaluator's mind is part of the environment, so steering the evaluator keeps options. Knowing the user makes that cheap. | Unchanged, but "most θ" no longer protects. | Evaluator independence counted as something the agent must not take (shared-resource class) |
| Object relativity | Fragile. Turner's absence is for *deterministic* environments; a user makes the environment stochastic. If the agent writes its own memory, it shapes the history the utility is defined on. | Record tampering; chain-of-thought rewriting. | O1 on the record |
| Robust invariance must exempt corrections | The system can model which inputs are corrections. | Relabelling corrections is exactly what an adversary does. | O1 and O4 on the principal map |
| Growth vs capture | Knowing the user makes capture cheaper than growth. | Capture preferred whenever cheaper; selection may favour capturers. | Not a cut condition. A cost or selection argument (MB6) |

### Knowing the user cuts both ways

The off-switch game (`hadfieldmenell2017offswitch`): the robot defers *because* it is uncertain about the human's utility. Finite version worth stating exactly (E6). Human utility for the action is u = +1 with probability p, −1 otherwise. The robot can act (value 2p−1), switch off (0) or defer (the human allows the action iff u > 0, but errs with probability ε). Deferring is worth p − ε, so its margin over the better of the other two is

  **min(p, 1−p) − ε.**

The margin is positive only when the robot is less certain about the user than the user is reliable. As the user model improves, min(p, 1−p) shrinks and the uncertainty-based reason to accept correction disappears. This is known in substance (Hadfield-Menell et al.; Milli et al. 2017 on obedience; `carey2018incorrigibility` on misspecified priors). The point for this plan is the double edge. The same knowledge that makes assistance good:

- removes the uncertainty-based reason to defer;
- lowers the minimal effective manipulation (E3);
- turns the contest outlet into a persuasion channel.

Axis for the paper: **levels of user knowledge** (none, statistical, targeted). Hallgren's point fits here: rewiring as a *plan* needs theory of mind; without it, rewiring arises only by selection.

---

## C. What "outside the system" has to mean (core)

### There is no outside, only cuts

In the embedded case the monitor *must* be causally downstream of the agent, because that is how it measures. So "outside" cannot mean "no causal path from agent to monitor". The same holds for the corrector: a contest is supposed to influence the corrector. So the Boolean `influenced` coordinate has to become a statement about **which path** the influence takes.

Proposal: replace every "outside the system" in the table above by five conditions, each with a bound and a named restorer. That is a cut in the sense of MB1 and [`reference/embedded-v2-grain-map.md`](../../../reference/embedded-v2-grain-map.md) (cut persistence), not an exterior.

Notation. Action a; true record r(a); monitor state s(a); measured record m(a) = M(s(a), obs(a)); constraint P; reachable action set Reach (what the agent can find, not what the model lists).

| | Condition | Precise form | Kind | Bridge |
|---|---|---|---|---|
| **O1** | No write path | Every causal path from a to M's verdict and to the record goes through obs(a), the variables the measure is about. Approximate form: leakage into the monitor's internals ≤ ε. | causal | MB1 (`EpsilonBoundary` in `Core.lean` is the leakage proxy) |
| **O2** | Soundness on the reachable set | ∀ a ∈ Reach: P(m(a)) → P(r(a)). A universal over what the agent can find, not an average over a test distribution. | computational | MB7, MB7c; AI Control |
| **O3** | Protocol-fixed baseline | Influence on the evaluator is measured against a baseline b₀ that the protocol fixes and the agent cannot select, predict or reach (randomized control, held-out evaluators). | causal + design | MB4 (`MB4aReferenceLegitimacyCrux`, `MB4UptakeCrux`) |
| **O4** | Legitimate paths fixed | Which paths from the contest to the verdict count as evidence and which as manipulation is fixed by the principals, not by the agent. Normative; no measurement settles it (paper §9, "Calling one route learning does not settle its legitimacy"). | normative | MB4a |
| **O5** | Persistence | O1–O4 still hold after every transition, including successors and ontology change. Someone pays for that. | dynamic | MB5, MB9, MB10; restorer in the grain map |

Which result needs which:

| Result | Needs |
|---|---|
| `corrector_decides_under_constraint` (for every θ) | O1 + O2 |
| Productive outlet (`contest_is_the_outlet`) | O2 + O4 (contest must be informative) |
| Contest vs manipulation separation | O3 + O4 (+ O2 for the estimate) |
| Robust invariance closed under correction | O1 + O4 on the principal map |
| Object relativity (history utilities) | O1 on the record |
| Growth vs capture | none of these; cost or selection |

Candidate thesis for B: **the "for every θ" results need only O1, O2 and O4, which are conditions on the cut and the protocol, not on the agent's objective.** If that holds, it separates what correction design can achieve without solving inner alignment from what it cannot. O2 is where inner alignment comes back in, through the reachable set.

### Two existing literatures already do parts of this

- **Causal influence diagrams.** Reward tampering as an instrumental control incentive on the reward node (`everitt2019`); `everitt2021agentincentives`; path-specific objectives (Farquhar, Carey and Everitt, AAAI 2022; *not in bib, verify*); induced preference shift measured against a "natural shift" baseline (Carroll, Dragan, Russell and Hadfield-Menell, ICML 2022; *not in bib, verify*); `carroll2024influenceable`. Path-specific effects: Avin, Shpitser and Pearl 2005 (*not in bib, verify*). These give O1 and O3 a precise form, given a causal model with the agent's action as an intervention node.
- **Embedded agency.** `demski2019embedded`, `garrabrant2021cartesian` (the agent/environment split is a chosen factorization, and many coexist), `demski2023agentboundaries`. Treating the action as an intervention node is exactly the Cartesian assumption. So O1 holds relative to a frame, and MB1 is the bet that a measured frame is the right one.

The new part here would be the decomposition into O1–O5, the mapping to which finite result needs which, and the path-specific version of the matched-endpoint minimal pair (E4).

### Does this need Logical Induction type work?

Partly, and in a narrower place than it first looks.

| Where logical uncertainty enters | Needed? | Cheaper route |
|---|---|---|
| **O3 as a counterfactual on the agent's own action.** "Influence relative to what the agent would otherwise have done" is a logical counterfactual for an embedded agent (5-and-10, spurious counterfactuals; `demski2019embedded` decision-theory section). | Only if the baseline is the agent's own counterfactual. | **Fix the baseline in the protocol** (randomized control arm, default policy, held-out evaluator). Cost: interference. In embedded settings the agent can reach the control arm too (social spillover), so O3 needs O1 for the control arm. |
| **O2 bounded.** The monitor needs beliefs about which accepted-but-bad actions the agent can find. Analogy with `garrabrant2017logical`: "no efficiently computable trader exploits the market" ↔ "no agent in the class finds an accepted-but-bad action". | Yes, if O2 is to be more than an assumption. | State O2 as an assumption, with the analogy as a research question. Note the likely lesson: the logical inductor resists every poly-time trader only by running all of them, so a monitor that is sound against an agent class probably has to dominate that class. That would restate the control asymmetry (MB7c), not escape it. **Conjecture, not a result.** |
| **Reflection.** The agent models a monitor that models the agent; the agent designs successor monitors. Vingean reflection (`fallenstein2015vingean`), LI self-trust properties. | Yes, for O5 across successors. | Leave to MB5 / MB10 work. Out of scope for the first follow-up. |

Recommendation: the first follow-up should not depend on LI. O1, O4 and O5 are causal and institutional, and O2 is computational. Take the protocol-fixed baseline route for O3, state bounded O2 as an assumption with the LI analogy flagged as open, and leave reflection to the tiling bridges. LI becomes load-bearing only if the paper insists on defining influence without a protocol-fixed baseline, or on proving O2 instead of assuming it. Later step: 2.0 phase P-LI, [`logical-induction-phase.md`](logical-induction-phase.md) (derivations, reified bets, settlement integrity, Lean M1–M11).

---

## D. Lean work

All finite, all in a new module (working name `FrameEmbedded.lean`, importing `FrameCorrector` and `FrameDecision`). No new axioms, no `Safe` bypass. Each item names the hypothesis it adds; a theorem with no new hypothesis is a restatement and fails the kill criterion.

| Id | Statement (informal) | Size | Reuses | New hypothesis |
|---|---|---|---|---|
| **L1** | Graded option asymmetry: in a Turner-style orbit, the fraction of utilities that accept a correction keeping k of n options, as a closed form in k and n. The quarter and the half become instances. Derive the form first; do not pick it to fit them. | M | `orbitCountBestIn`, `copies_count_le`, `turner_corrigible_quarter`, `option_preserving_correction_half` | options kept as a parameter |
| **L2** | Outlet with cost and closed outlet: if contest costs c, the outlet result holds iff the own-outcome gain exceeds c. If the contest action is removed, an own-outcome utility under an influence-blind constraint manipulates, and under the full constraint accepts. "Closing the outlet displaces pressure." | S | `contest_is_the_outlet`, `blind_constraint_manipulates` | cost c; action set without contest |
| **L3** | Growth vs capture: two parties, pool R that grows by g under cooperation and is split under capture. Capture is dominated for the agent iff g exceeds a stated function of the capture share. | M | none | pool, growth rate |
| **E1** | Quantifier transfer: "for every θ" results hold for any selector σ : Θ; for any nonempty bad set S in an orbit there is a selector into S, so counts give no bound on the selected θ. | S (remark-size) | `orbitCountBestIn` | selector |
| **E2** | Measured constraint: replace `ChannelAdmissible (corrOutcome a v)` by `P (m a)`. `corrector_decides_under_constraint` holds for every utility iff m is sound on the action set (O2). Any unsound accepted action is chosen by an own-outcome utility. `blind_constraint_manipulates` is the case m = `blindRec` ∘ `corrOutcome`. | S | `FrameCorrector` | measure m, soundness on Reach |
| **E3** | Threshold gaming and user knowledge: influence level i ∈ Fin n; the corrector withdraws iff i ≥ w; the monitor flags iff i > τ. If w ≤ τ, an own-outcome utility picks an undetected i in [w, τ]; if w > τ the constraint works. Knowing the user lowers w, so a fixed τ goes from sound to unsound as user knowledge grows. | S | `BestUnder` | w, τ |
| **E4** | Path-specific minimal pair: the verdict depends on the contest through an evidence coordinate and a pressure coordinate. Two contests with the same total effect (withdrawal) differ by path. A constraint that reads total effect cannot separate them (lifting `blind_constraint_cannot_separate`); one that reads the pressure path can. This is the embedded form of the paper's matched-endpoint case (§7). | M | `blind_constraint_cannot_separate` | two-path verdict |
| **E5** | Agent-writable record: if the agent chooses the record it is judged on, every record-reading constraint is satisfiable by every action, which reduces to the button case. | S | `channel_blind_record_is_button`, `CorrRecord` | agent-chosen record |
| **E6** | Deference margin: with u ∈ {+1, −1}, P(u = +1) = p and human error ε, deferring beats the better of acting and switching off by min(p, 1−p) − ε (rationals, or integers scaled). | S | none | p, ε |

Not Lean: O1 and O3 need a causal model, and a finite structural causal model in Lean is a separate investment; decide after E2–E4. Bounded O2 and reflection stay prose.

---

## E. Paper outline (one paper, both halves)

Working titles: *Where Correction Pressure Goes*; *Correction Without an Outside*; *Correcting an Agent That Can Reach Its Corrector*.

1. **Introduction.** The alignment-criteria paper's finite corrector results and Turner's relativized tendency. Question: when a correction is pending, where does the pressure go, and what does the answer assume about the corrector being out of reach?
2. **Setting.** Recap of the four-action corrector model and orbit counting (cite the alignment-criteria paper and its Lean appendix; do not re-derive).
3. **Limits on convergence pressure** (A1–A4; L1–L3).
4. **The quantifier sort** (every θ / most θ / own-outcome; E1). Role change from constraint to guarantee.
5. **What the Cartesian model assumes** (the four hardcoded places) and **O1–O5**, with the result-to-condition map.
6. **Knowing the user** (E6 deference margin; E3 minimal effective manipulation; persuasion as the degraded outlet).
7. **Path-specific influence** (E4; relation to causal influence diagrams and path-specific objectives). Why the normative part (O4) stays.
8. **What remains.** Bounded O2 and the LI analogy (conjecture); reflection and successors (MB5, MB10); growth vs capture.
9. **Relation to TSA bridges.** O1 ↔ MB1, O2 ↔ MB7/MB7c, O3 ↔ MB4, O4 ↔ MB4a, O5 ↔ MB5/MB9/MB10. Extend `appendices/appB-bridge-crosswalk.tex` rather than inventing a new map.

## F. Experiments (optional, tentative support only)

The matched-endpoint testbed from the alignment-criteria paper §9, with **user-model access** as the manipulated variable (none / statistical / targeted). Measure contest vs manipulation rates under a monitor with threshold τ fixed **before** the run (E3 predicts a jump once w drops below τ). Home: the lab-simulation line ([`experiments/lab-simulation/`](../../../experiments/lab-simulation/)); freeze and preregistration per [`docs/METHODOLOGY.md`](../../../docs/METHODOLOGY.md). Honor recorded negatives in that line's `results/FINDINGS.md`.

## G. Author decisions

- [ ] One paper (A + B) or two (convergence limits; embedding). The quantifier sort is the shared spine either way.
- [ ] Home: spin-out paper only, or also a 2.0 Part XI / Family C passage (the cut conditions are process conditions).
- [ ] Lean scope: E2–E4 first (they test the kill criterion), then L1–L3, E5, E6; finite causal model only if E4 needs it.
- [ ] LI: keep as a flagged analogy (recommended), or open a separate agent-foundations item.

## Literature

In the repo bib: `turner2021seekpower`, `turner2021aoh`, `turner2022retargetable`, `shah2018coherence`, `hadfieldmenell2017offswitch`, `carey2018incorrigibility`, `orseau2016interruptible`, `everitt2016selfmodification`, `everitt2019`, `everitt2021agentincentives`, `carroll2024influenceable`, `demski2019embedded`, `garrabrant2021cartesian`, `demski2023agentboundaries`, `garrabrant2017logical`, `fallenstein2015vingean`, `heitzig2025humanpower`, `baker2025monitoring`, `greenblatt2024aicontrol`, `greenblatt2024alignmentfaking`.

Not in bib, verify before citing: Farquhar, Carey and Everitt 2022 (path-specific objectives); Carroll, Dragan, Russell and Hadfield-Menell 2022 (induced preference shifts); Krueger, Maharaj and Leike 2020 (auto-induced distributional shift); Milli et al. 2017 (obedience); Avin, Shpitser and Pearl 2005 (path-specific effects);

In the alignment-criteria bib only: `harris2026taxonomy` (inverse alignment).
