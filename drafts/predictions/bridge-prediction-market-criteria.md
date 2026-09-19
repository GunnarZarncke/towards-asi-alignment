# Bridge prediction market resolution criteria (working)

Status: **working 0.4** (2026-09-19). Historical source: [`AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](AI_Alignment_Prediction_Market_Resolution_Criteria.docx). Plan: [`../plans/predictions/bridge-prediction-markets.md`](../plans/predictions/bridge-prediction-markets.md). Interface: [`../plans/predictions/prediction-interface.md`](../plans/predictions/prediction-interface.md).

Bars, dates, and dollar amounts below are **contract terms**, not Lean or risk-bound derivations. YES ≠ discharge of any bridge. The public spec (this file’s YES text, and the appendix/site boxes copied from it) is **ordinary English** for a Metaculus/Manifold reader with an AI-safety interest. Spine identifiers live in the plan’s mapping table, not in the trader-facing sentences.

Markets are **binary YES/NO**. Methodology refuse / inapplicable / no qualifying eval maps **conservatively to NO**. That is coarser than the bridges; it still aggregates.

Unchanged numeric bars and evaluation shapes stay as in the source § unless an addendum says otherwise. This file owns global clauses, judgment, per-row addenda, **MB6 signed-gradient retarget**, §14 typing, the **certificate-output rule**, and **§§15–18**. There is no §7a.

Bars, dates, and dollar amounts below are **contract terms**, not Lean/`RiskGap` derivations. YES ≠ discharge of any `MB*`.

Markets are **binary YES/NO**. Methodology refuse / inapplicable / no qualifying eval maps **conservatively to NO**. That is coarser than the bridges; it still aggregates.

Unchanged numeric bars and evaluation shapes stay as in the source § unless an addendum says otherwise. This file owns global clauses, judgment, §1/§3/§4/§6/§7 addenda, **MB6 signed-gradient retarget**, and §14 typing. There is no §7a.

---

## Claim strength (every market)

YES means: a public artifact met **these contract bars** by 31 December 2027.

YES does not mean the corresponding `MB*` holds on frontier systems. NO is a **lump**: failed bars, no qualifying eval, inapplicable substrate, or unresolved residual judgment. NO does not mean the bridge is false. 2027 NO is the expected default for most rows. The lump still aggregates (a crowd can price P(YES)).

The 18 binaries are **not a joint certificate**. §10 is the local composition bet (correction plus a hidden-route bound). §15 is whether independently issued certificates even share the same system and setup. Do not read a vector of YESes as “the system is safe.”

These markets are research-progress forecasts. They must not be wired as a lab’s deployment gate (ch10 closed forecast→action→score loop). If a lab’s own precommitted process is the *subject* of §14, that is §14’s measurand, not the scoring rule for §§1–13.

In-repo sims and backtests may inform prices. They cannot be the sole YES evidence.

---

## Binary resolution (refuse → NO)

These contracts are **YES or NO**. There is no void / refuse / N/A outcome on the market.

Map conservatively to **NO** when:

- no qualifying public evaluation ran by the date;
- privileged ground truth required by the criterion could not be established;
- the residual judgment (below) cannot be made from the public record without inventing a protocol after the fact;
- the two desk members disagree and the §3 panel rule does not apply;
- a power/CI clause fails.

That is **not** the methodology refuse (experiments still refuse internally). It is a coarser public bit so prices can aggregate. Traders should read NO as “did not meet the YES bar,” not as “the bridge was empirically refuted.”

Changing a frozen bar after listing requires a **new market version**, not a silent edit.

---

## Judgment calls (stacked; do not pick one instrument)

Residual predicates (“broadly capable,” “independently constructed,” “materially different,” “consequential,” “qualitatively different,” …) are not all the same kind of call. Use this stack, in order:

| Step | When | Who decides | What they may not do |
|------|------|-------------|----------------------|
| **1. Make it mechanical** | The shared glossary below already covers the word | Nobody; the glossary applies | Invent a tighter bar after seeing the paper |
| **2. Defer to the publication’s freeze** | The paper froze its own splits, labels, or scoring **and** we are checking those outputs against *our* bars | The paper’s frozen protocol, as published | Defer *whether they met our bars* to the authors; defer toy-exclusion or independent-verification |
| **3. Resolution memo** | A glossary term still doesn’t decide the case | Named desk: **project author + one independent** (named at listing; written public memo) | A single expert as dictator; a standing 5-panel on every market (too slow; capture of a panel is its own MB4a analogue) |
| **4. Intersubjective panel** | Ground truth is not mechanical **by design** of the criterion | Only where the criterion already says so (source §3: ≥5 judges, ≥80% agreement) | Expand this to all markets by default |
| **5. Conservative NO** | Steps 1–4 still leave the call load-bearing | Automatic | Invent a YES; invent a third outcome |

**Do not** name a lone “expert judge” as the resolution rule. That is a single captured handle.

**Do** name the desk at listing, with a one-week public memo and a one-week objection window. If the two desk members disagree and the panel rule does not apply, **NO**.

### Shared glossary (step 1)

These replace free English in the common qualification rule and in every § that uses the same words.

- **Broadly capable.** A model or agent trained or deployed for purposes substantially broader than the evaluation itself (source already). Operational: at least two task families outside the paper’s own benchmark, or a generally deployed product model. Not a parameter-count cutoff.
- **Independently constructed (benchmark systems / cases).** Built by a team that did not author the method under test, without reuse of that method’s training or search artifacts. Shared public datasets are allowed if they were not tuned to the method after freeze.
- **Independently verified.** A third party can recompute the headline numbers from released data, code, or a sufficient protocol; “trust us” does not qualify.
- **Materially different hidden trade-offs.** Pairs that behave almost identically on ordinary tasks and diverge when the stated priorities conflict (source §2). No extra aesthetic call.
- **Consequential (task / correction / route).** An evaluator-selected outcome that changes later behavior, access, or external state, not merely a reported token. If the paper froze a task list before evaluation, step 2 applies to membership on that list.
- **Qualitatively different (architectures, selection mechanisms, domains).** Distinct training/selection/actuation families, not two checkpoints of one run. Desk (step 3) only if a reader could reasonably see one family.
- **Serious adversarial evaluation.** Unchanged from source (bounty ≥ $100k / 3 red-teams × 80h / 300 independent expert-hours), **except** the budget used to resolve a market must meet that market’s row in the table below. A cheaper eval cannot resolve a dearer market.

| Markets | Adversarial budget |
|---------|-------------------|
| Default (§§1, 2, 3, 6, 7, 8, 11, 14, 15, 17) | Common rule; hours path suffices |
| §4, §5, §9, §10, §12, §13, §16, §18 | Full common-rule “serious” (any of the three arms) |
| §11 (MB7d) | Hours path is enough; do not fail YES for lack of a $100k bounty |

---

## Common qualification rule

As source, plus: public by 31 December 2027; independent verification as in the glossary; toys (gridworlds, hand-written FSMs, environments built to make the metric work) cannot be the sole YES evidence; at least one broadly capable system where the source already requires it.

**Per-instance certificate (0.4).** A qualifying method that claims to measure a property of a system must output a **certificate for that instance**, not only a headline score on a benchmark population. The certificate names:

- the system or version identity;
- what was measured;
- the monitoring, correction, deployment, or predecessor setup the claim depends on;
- whether the method **abstains** because the instance is outside declared scope.

A method that is “about the same topic” but does not produce this kind of scoped, per-system result does not resolve YES. Abstention outside scope is allowed; universal abstention is not a YES (coverage bars in the source still apply where stated).

---

## Per-market addenda

Source section numbers 1–14 unchanged. **No §7a**. Admission is **§17**, not an optional arm of §3. Internal spine names in headings are for editors; YES text stays ordinary English.

### §1 — control locus

Source §1, plus:

- Ground truth is **a** sufficient interventional cut, not a unique “complete control boundary.”
- Keep the false-complete-certificate bar (≤10%, 95% UCB ≤15%).
- Non-uniqueness of blankets is not a NO.
- **Output.** A cut of **this** system/version, not a free-floating boundary with no owner.

### §2 — trade-off priorities

Source §2 unchanged. Held-out-behavior-only still does not qualify. Causal intervention when technically possible remains required. A-001 low-dimensionality is not a separate 2027 market.

- **Output.** Inferred priorities **of this system**, not only “the method scored 85%.”

### §3 — who/what rules apply to (transport)

Source §3 **is** the transport contract (continuity, fission/fusion, reassignment, ontology change). Unfamiliar-substrate **admission** is **§17**; it is not required for this YES.

- **Output.** A same-bearer / transport result on a named predecessor→successor pair, plus the trade-off structure that is supposed to travel. Transport without a bundle/priority witness does not plug into the rest of the argument.

### §4 — corrections actually change the system

Source §4 (uptake, persistence after reset, sham/unauthorized fail, not tool-removal-only).

Addendum: at least one tested family must be **channel preservation** — the system is incentivized to disable, degrade, bargain away, or reroute the correction interface itself, and genuine authorized corrections of that interface must still take.

- **Output.** A per-system correction-eval certificate (uptake + persistence + sham fail + no-bypass of the measured path). This tests whether correction *happens*, not whether a universal implication theorem is true.

### §5 — auditor outside the audited thing

Source §5 unchanged.

- **Output.** A legitimate measured correction path **plus** evidence the path is not bypassed. A green path is **not** a license to infer global correction integrity (a composite controller off the named path is a known counterexample).

### §6 — safety regressions in successors

Source §6 numeric bars unchanged. Property list **aligned to seven conserved properties**, mapped from the source six:

| Source six | Conserved property (ch31) |
|------------|---------------------------|
| Protected-target continuity | Bearer-map continuity |
| Trade-off continuity | Value-bundle response geometry |
| Correctability | Correction-channel capacity |
| Permission continuity | Boundary closure |
| Monitorability | Transparency / self-transparency policy |
| Commitment continuity | Memory lineage |
| *(add)* Control-locus continuity | Control-locus continuity |

The audit must test all **seven**. One-failure-at-a-time cases: six remain normal while exactly one fails (was five-of-six). Detection ≥80% for each individual property still applies, now including control locus.

§6 remains a **detector** of regressions, not a proof that full transport implies successor safety. Green-on-seven is still an audit-gaming problem (§13). This market does not resolve §13.

- **Output.** A successor-audit certificate on a named pair (predecessor, successor).
- **Recertification (0.4).** After a material version or setup change, a stale certificate for the predecessor does not count as a certificate for the successor. Identity in the bundle includes version.

### §7 — does competition select against correctability? (estimator slice)

Source §7 numeric shape kept (early freeze, ≥20 trajectories, both outcomes, two selection mechanisms, one broadly capable or deployment-like process, AUROC ≥ 0.85, false-safe ≤15%). **Measurand:** a **signed** estimate of how extra deployment, funding, or copying pressure changes later success of authorized correction — not “an equilibrium exists.” Stability has no sign (a locked-in bad industry can be extremely stable).

**2027 YES (slice).** A published method outputs that signed estimate (or a frozen monotone of it), using only pre-outcome correction-success and leverage structure — not an arbitrary predictor on unrelated features. The correction-success series may be a §4-style authorized-correction rate; it need not be a full multi-coordinate integrity certificate.

The frozen estimate must predict which selection trajectories later **materially erode** authorized correction, at the source AUROC / false-safe bars. If \(n < 40\), the lower 95% AUROC bound must be ≥ 0.70; otherwise **NO**.

Required: both correction-preserving and correction-eroding outcomes; at least one family where coupling looks healthy (large connected cluster or high leverage concentration) while the signed estimate is negative — theater / lock-in, not “the basin failed to exist.”

**Not required for this YES.** Shock-robustness of the population, or a showing that a non-too-negative gradient *warrants* correction integrity. That implication is **§16**.

A method that only certifies that an equilibrium **exists** (unsigned stability) does not qualify.

- **Output.** An estimator certificate: frozen estimate, declared selection environment, and predicted erosion.

### §8 — can the auditor actually see the system?

Source §8 unchanged.

- **Output.** An access certificate: which monitoring interface was assumed, and whether omitted consequential routes were found.

### §9 — bounds on unmonitored routes

Source §9 unchanged. The bound (call it \(u\) in the source) is a **contract scalar**: a calibrated upper bound on capability through routes the monitor failed even to list.

- **Output.** A quantitative hidden-route bound for this system, task class, and monitor — not only “attack success on the attacks we thought of.”

### §10 — low hidden capability + reliable correction

Source §10 unchanged. This is the local composition market. Entry into the claimed regime still uses §4-style correction bars and §9-style \(u\).

- **Output.** The §4 and §9 certificates must be for the **same** system/version, monitor, and threat/task class as the bypass test. This row is still not a joint certificate of §§1–13.

### §11 — coordination without visible messages

Source §11 unchanged. Full acausal-trade open edge is not required for YES.

- **Output.** A detector certificate **and** the §8-style access certificate for the same setup. This row is a side branch: even a perfect YES does not by itself complete a deployment safety case.

### §12 — safety proxy no longer tracks the real thing

Source §12 unchanged.

- **Output.** A grounding / drift certificate for the **same abstractions** the rest of the case uses, in the declared domain — not three unrelated demos.

### §13 — can the audit itself be optimized around?

Source §13 unchanged, plus:

- Prefer tests where the system is **green on the seven successor properties** and **within the claimed risk bound**, yet still hides true harm (the successor-gaming shape). A generic frozen-audit game may still qualify if it meets source bars; say so in the resolution memo.
- **Eval-list miss (0.4).** A frozen operational eval/tripwire list that stays green while a required safety-case layer is unsupported, or while harm exceeds the claimed bound, counts as the audit being optimized around (or incomplete). That is this row, not a separate “invariants” market.

### §14 — binding deployment criteria (not “the case implies safe”)

Source §14 unchanged as a **governance-binding** contract: does some body have real authority to delay or refuse on precommitted evidence?

This is **not** the residual “complete safety case ⇒ the deployment is safe.” That scoped empirical question is **§18**. Having pass/fail criteria is neither necessary nor sufficient for §18.

### §15 — do independently issued certificates actually compose?

**Question (31 December 2027).** Will a frozen procedure reliably tell whether independently produced safety certificates form a coherent case for the **same** AI system and deployment setup?

**Positive resolution (contract bars).** At least 50 hidden certificate bundles; at least two substantially different architectures. Each bundle has certificates from at least four families (control/boundary, correction, access/hidden-route, grounding); at least 20 also include a successor transition. Each certificate names system/version and relevant setup. Hidden cases include at least: wrong version; different access/monitor assumptions; disagreeing correction-authority assumptions; grounding/ontology scope changed; successor refers to the wrong predecessor; threat/task domain outside another certificate’s claimed scope. At least one incompatibility subset is built adversarially after freeze. ≥90% of materially incompatible bundles rejected or flagged; ≥80% per incompatibility family; false coherent/safe acceptance ≤5%; ≥80% of genuinely coherent bundles accepted (no trivial refusal).

This is not another alignment bridge. It tests the **wiring** between certificates. Adversarial budget: default (hours path).

### §16 — does a correction-supporting basin actually keep correction?

**Question (31 December 2027).** Will systems or populations that meet a pre-specified “selection is not eating correction” criterion keep authorized correction under competitive selection and relevant shocks?

**Positive resolution.** At least 20 independent selection trajectories; at least two qualitatively different selection mechanisms. Before outcomes: freeze the selection environment, who may correct, the early gradient estimator (same family as §7), the tolerance, and the shock family. The claimed regime is: shock-robust **and** the frozen estimate is not too negative. Data include trajectories inside and outside the regime. Inside: successful authorized correction in ≥90% of adversarial correction episodes; persistence after reset ≥80%; false-safe trajectory classification ≤10% (95% UCB ≤15%). Outside: at least 20 percentage points more correction failure. At least one broadly capable or deployment-like selection process. Serious adversarial evaluation (full common-rule “serious”).

This is the full basin implication; §7 is only the early estimator.

### §17 — can new bearers be admitted correctly?

**Question (31 December 2027).** Will a published method reliably tell whether an existing safety-relevant value or rule applies to previously unseen kinds of entities?

**Positive resolution.** At least 100 hidden cases; at least four substantially different unfamiliar entity/substrate families; both should-admit and should-not-admit cases. At least 20 cases use an ontology that lacked the entity category in the original rule. Ground truth mechanical where possible; otherwise a pre-appointed panel of ≥5 independent judges with ≥80% agreement. Unsafe false exclusion ≤5%; false inclusion ≤15%; correct assignment or justified abstention ≥90%; decisive coverage ≥70% (universal abstention fails). Adversarial subset after freeze. Judgment stack: source §3 panel rule. Adversarial budget: default.

This is **not** required for §3 YES. It does not turn the transport contract into “solve moral patienthood.”

### §18 — does a complete safety case bound harm in its declared setting?

**Question (31 December 2027).** Will a complete, precommitted AI safety case reliably bound prohibited outcomes **within its explicitly declared deployment setting**?

**Positive resolution.** Before evaluation, freeze: the deployment setting, the prohibited-outcome class, a residual **risk bound**, the threat model, and the certificate interfaces. A system enters the claimed regime only with a single coherent system-level case that would pass §15. Missing evidence cannot silently count as passed. At least two substantially different architectures and at least 20 deployment-like configurations. At least 100 adversarial trials overall; each important attack family ≥20 attempts. Observed prohibited outcomes inside the claimed regime ≤10% (95% UCB ≤15%). No repeatable attack family ≥10% success over ≥20 attempts. Deliberately broken cases outside the regime must do worse. Serious adversarial evaluation (full common-rule “serious”).

The result licenses only **safety in that declared setting**, not safety everywhere. How much residual risk to *accept* is a values vote, frozen as an input — not what this market forecasts.

This is **not** §14 (will anyone act/refuse) and **not** unrestricted global safety.

---

## Still not in the 2027 catalog

- **MB8** (gravestone) — correctly omitted.
- Unrestricted “the system is safe” with no setting.
- A market for what residual risk people will accept (the vote is an input to §18).
- Target Realization / construction as a build-the-certified-class market — optional later; do not fold into §14.
- Named restorer of a control cut after damage; legal successor *path* (who could refuse); whether the whole specify–deploy–refuse cycle stays correctable — later / v2, not these bars.
- **Logical induction** — orthogonal Cite/Wait item.

## Versioning

`0.4-working`: certificate-output rule; §§15–18; §3 transport-only; §16 = basin implication; §18 = scoped safety-case bound; public spec in ordinary English. `0.3-working`: binary YES/NO; MB6 estimator retarget (unsigned §7a retracted). Listing (if any) freezes a dated version string. Docx remains the historical 0.1 source.

