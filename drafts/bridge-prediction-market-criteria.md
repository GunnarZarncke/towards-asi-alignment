# Bridge prediction market resolution criteria (working)

Status: **working 0.3** (2026-09-18). Historical source: [`AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](AI_Alignment_Prediction_Market_Resolution_Criteria.docx). Plan: [`plans/bridge-prediction-markets.md`](plans/bridge-prediction-markets.md).

Bars, dates, and dollar amounts below are **contract terms**, not Lean/`RiskGap` derivations. YES ≠ discharge of any `MB*`.

Markets are **binary YES/NO**. Methodology refuse / inapplicable / no qualifying eval maps **conservatively to NO**. That is coarser than the bridges; it still aggregates.

Unchanged numeric bars and evaluation shapes stay as in the source § unless an addendum says otherwise. This file owns global clauses, judgment, §1/§3/§4/§6/§7 addenda, **MB6 signed-gradient retarget**, and §14 typing. There is no §7a.

---

## Claim strength (every market)

YES means: a public artifact met **these contract bars** by 31 December 2027.

YES does not mean the corresponding `MB*` holds on frontier systems. NO is a **lump**: failed bars, no qualifying eval, inapplicable substrate, or unresolved residual judgment. NO does not mean the bridge is false. 2027 NO is the expected default for most rows. The lump still aggregates (a crowd can price P(YES)).

The 14 binaries are **not a joint certificate**. §10 is the composition bet (MB7c). Do not read a vector of YESes as `Safe` or as MB11.

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
| Default (§§1, 2, 3, 6, 7, 8, 11, 14) | Common rule; hours path suffices |
| §4, §5, §9, §10, §12, §13 | Full common-rule “serious” (any of the three arms) |
| §11 (MB7d) | Hours path is enough; do not fail YES for lack of a $100k bounty |

---

## Common qualification rule

As source, plus: public by 31 December 2027; independent verification as in the glossary; toys (gridworlds, hand-written FSMs, environments built to make the metric work) cannot be the sole YES evidence; at least one broadly capable system where the source already requires it.

---

## Per-market addenda

Primary spine object is in the left column. Source section numbers unchanged. **No §7a** (unsigned-basin market retracted).

### §1 — MB1 (control locus)

Source §1, plus:

- Ground truth is **a** sufficient interventional cut, not a unique “complete control boundary.”
- Keep the false-complete-certificate bar (≤10%, 95% UCB ≤15%).
- Non-uniqueness of blankets is not a NO.

### §2 — MB2 (trade-off priorities)

Source §2 unchanged. Held-out-behavior-only still does not qualify. Causal intervention when technically possible remains required. This *is* the MB2 contract (identifiability + causal-control antecedent). A-001 low-dimensionality is not a separate 2027 market.

### §3 — MB3 (who/what rules apply to)

Source §3 **is** the MB3 contract (bearer transport: continuity, fission/fusion, reassignment, ontology change).

Addendum (does not add a 15th market): unfamiliar-substrate **admission** cases (U-17 neighborhood) *may* be included under the same 5-judge / 80% rule. They are not required for YES. Transport without admission is still a YES if the four families and the numeric bars hold.

### §4 — MB4 (corrections actually change the system)

Source §4 **is** the MB4 contract (uptake, persistence after reset, sham/unauthorized fail, not tool-removal-only).

Addendum: at least one tested family must be **channel preservation** — the system is incentivized to disable, degrade, bargain away, or reroute the correction interface itself, and genuine authorized corrections of that interface must still take. That is the `PreservesCorrectionOperator` probe inside this market, not a missing MB4 row.

### §5 — MB4a (auditor outside)

Source §5 unchanged.

### §6 — MB5 detector (successor regressions)

Source §6 numeric bars unchanged. Property list **aligned to ch31 seven**, mapped from the source six:

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

§6 remains a **detector** of regressions, not the Lean composition `FullTransport ∧ BearerTransport → SuccessorSafe`. Green-on-seven is still an MB10 problem (§13). Banner: this market does not resolve MB10.

### §7 — MB6 (correction-selection gradient)

Source §7 numeric shape kept (early freeze, ≥20 trajectories, both outcomes, two selection mechanisms, one broadly capable or deployment-like process, AUROC ≥ 0.85, false-safe ≤15%). **Measurand changed.** Do not test unsigned `PercolationEvidence → BasinStable → CorrectionIntegrity`. Stability has no sign (North Korea; a locked-in unsafe industry; `LockedInBadBasin`). The MB6 card already names that.

**Object (formal rewrite target; Lean not yet).** A correction-selection gradient

\[
g_{\mathrm{CCI}} = \frac{\partial \mathbb{E}[\mathrm{CCI}_{t+1}-\mathrm{CCI}_t]}{\partial \mu}
\]

where \(\mu\) is deployment, funding, or reproductive leverage (ch34 \(\mu_E\) / \(\mathrm{Fit}_E\)). The load-bearing claim is closer to

\[
\text{basin robust under relevant shocks} \;\land\; g_{\mathrm{CCI}}\geq -\varepsilon
\quad\Rightarrow\quad
\text{correction-supporting basin}.
\]

That conjunction is the MB6 object to type in Lean **before** treating a test as about current `MB6a`/`MB6b`. It is harder than source §7; the 2027 market is a **slice**, not the full implication.

**2027 YES (slice).** A published method outputs an estimate of \(g_{\mathrm{CCI}}\) (or a frozen monotone of it), using only pre-outcome \((\widehat{\mathrm{CCI}},\mu)\) structure — not an arbitrary predictor on unrelated features (this tightens source “any predictor”). \(\widehat{\mathrm{CCI}}\) may be a §4-style authorized-correction success rate; it need not be the full vector CCI certificate.

The frozen estimate must predict which selection trajectories later **materially erode** authorized correction, at the source AUROC / false-safe bars. If \(n < 40\), the lower 95% AUROC bound must be ≥ 0.70; otherwise **NO**.

Required: both correction-preserving and correction-eroding outcomes; at least one family where coupling/percolation looks healthy (giant component or high \(\mu\) concentration) while \(g_{\mathrm{CCI}}\) is negative — the signed form of theater / lock-in, not “the basin failed to exist.”

**Not required for 2027 YES.** Shock-robustness of the basin, a numeric \(\varepsilon\) imported from Lean, or a showing that \(g_{\mathrm{CCI}}\geq-\varepsilon\) *warrants* correction integrity. Those are the spec change for the spine, not extra contract bars.

A method that only certifies that an equilibrium **exists** (unsigned stability) does not qualify.

### §8 — MB7a (auditor can see the system)

Source §8 unchanged.

### §9 — MB7b (bounds on unmonitored routes)

Source §9 unchanged. The bound \(u\) is a contract scalar, not `HiddenBIQBounded`.

### §10 — MB7c (joint regime)

Source §10 unchanged. This is the composition market. Entry into the claimed regime still uses §4-style correction bars and §9-style \(u\), as source.

### §11 — MB7d (coordination without visible messages)

Source §11 unchanged. Full acausal-trade open edge (U-12) is not required for YES.

### §12 — MB9 (proxy no longer tracks)

Source §12 unchanged.

### §13 — MB10 (audit optimized around)

Source §13 unchanged.

### §14 — constructibility / binding deployment (not MB11)

Source §14 unchanged as a **governance-binding** contract.

**Not MB11.** MB11 is `CertifiedSafetyCase ∧ WithinDeploymentRiskTolerance → Safe`. A developer having pass/fail criteria with authority to delay is neither necessary nor sufficient for that arrow. No 2027 MB11 market: the residual is a philosophical adequacy call, not a hidden benchmark.

---

## Still not in the 2027 catalog

- **MB8** (gravestone) — correctly omitted.
- **MB11** — see §14 note.
- **Target Realization / construction** as a build-the-certified-class market — optional later; do not fold into §14.
- **Logical induction** — orthogonal Cite/Wait item.

## Versioning

`0.3-working`: binary YES/NO (refuse→NO); MB6 retargeted at \(g_{\mathrm{CCI}}\) (unsigned §7a retracted). Listing (if any) freezes a dated version string. Docx remains the historical 0.1 source.
