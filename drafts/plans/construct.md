# Construct — TSA 2.0 construction and constructibility

Status: **planning** (2026-08-24). **v1 manuscript still gated** on Witness Expectation 4 **with deployment leverage** on the system under test. W-9–W-11 (FAA/GPL/Debian) are institutional analogues only; they do not open this gate. This file is the Construct lane checklist. Voice / Witness / Field / Spine stay as they are.

**Trigger for opening the plan:** Ngo’s impact-counterfactual / “differentially advancing alignment” failure mode is not a missing spine invariant. It is a **constructibility** gap: TSA currently tests the optimizer’s policy and the selector on labs/artifacts, not whether people will *build* the certified class rather than narrate it.

## Goal

Make **Construction** an explicit TSA 2.0 object, without smuggling it into v1 as a sixth intro claim or as denser definitions.

Two objects, kept separate:

| Object | Question | v1 home | 2.0 home |
|--------|----------|---------|----------|
| **Construction** (technical) | Given frozen target \(P\) / region \(D\), can we *build* a system (or change \(Q,f,\theta,E\)) that realizes it? | Open Q2 in the introduction; Lean `ConstructionCrux`; site specify/construct cards; spin-out papers | Concrete construction chapters *when* a part has a fail/refuse, not a recipe catalog |
| **Constructibility** (process) | Under what circumstances will people, labs, and orgs be *willing and able* to construct the relevant system, rather than keep the alignment brand? | Implied by ch37 conductivity and ch40 institutional laundering; not operationalized on the *researcher* | Social + technical process-condition chapters, tied to existing formulations |

**Operational success for the plan (not for ASI alignment):**

1. A 2.0 chapter map exists, each node pointing at a v1 chapter, Lean object, paper, or explicit “not yet.”
2. Constructibility has a named test that can **fail** (including: the lab’s impact story is not evidence).
3. Concrete construction remains behind the existing reviewer bar: a Witness-style **fail/refuse**, not more vocabulary.

## Non-goals

- Do not add Construction to the **v1** PDF/site chapter list until Witness Exp. 4.
- Do not add a sixth intro claim in v1. A 2.0 claim (if any) is a later author decision.
- Do not absorb Ngo’s motivated counterfactuals into goal laundering, \(\mathrm{Fit}_E\), or ch25 “correction is counterfactual” (homograph).
- Do not treat ch37 artifact conductivity as construction success. Conductivity into AGI-company decision loops is a **constructibility risk**.
- Do not claim `ConstructionCrux` is discharged by `claimsExplicitBuilder` (already a Lean counterexample).

## Relation to v1 (do not rewrite the book’s Q2 hedge)

Introduction (`sec:three-alignment-questions`): the book develops Q1 (what to track) and a structure for Q3 (how to tell); Q2 (how to build) stays open. ch33 is **certification without construction** on purpose.

2.0 does not retract that. It answers a different pair:

- When is certification **not enough**, so construction must be attempted?
- When is an attempted construction **not the thing named**, because the constructors’ stories, selectors, or symmetries were never broken?

## Existing surfaces (reuse)

| Surface | What it already is |
|---------|-------------------|
| Intro Q2 + ch33 | Certification class vs construction recipe |
| Lean `AlignmentConstruction.lean` | `AlignmentTarget`, `Realizes`, `ConstructionCrux` (open ∃), `CertifiedAsRealizing`, `ConstructionBet` catalog ≠ crux |
| Site | `/cards/alignment-lifecycle/`, specify/construct instance cards (CEV, CAI, GSAI, institutional) |
| Papers | *Alignment Under Selection*; *Constructing Alignment Attractors* (explicit symmetry breaking; \(D\) frozen independently of \(I\)) |
| ch34–ch38 | Selection, parasites, attractor, conductive artifacts |
| ch37 \(\mathcal{S}_{\mathrm{align}}\) | \(A_t\) changes decisions; \(E_t\) constrains claims; \(G_t\) connects to deployment; \(C_t\) cross-role correction; \(L_t\) challengeable |
| ch40 institutional laundering | \(G_{\mathrm{sem}}\) stable, operational goal shifted; “not ordinary hypocrisy” (system-side) |
| Witness Exp. 4 | Real stop = certification leaf that changed a decision |
| Field | Target Realization is an open interface, not an `MB*` column |

## The Ngo residue (why constructibility is not optional)

From [Pragmatism and Pessimization](https://www.lesswrong.com/posts/yaz8nx4ogZmiqHzt7/what-just-happened-pragmatism-and-pessimization): many futures make it cheap to argue that *this* work is impactful on the margin; incentives pick the convenient world; inside AGI companies that becomes stories about worlds where the alignment-branded intervention never happened; “differentially advancing alignment” is hard to demarcate from overhang / buying time.

v1 nearby objects (ch09 distributed deception, ch34 compliance overhang, ch37 false attractors, ch40 composite laundering) cover **orgs that keep safety language**. They do **not** model:

- TSA tests the **optimizer’s policy**, not the researcher’s story about their own intervention.
- Selectors act on **labs and artifacts**; they do not model **which counterfactual a person attends to**.
- Residual: TSA used as a *brand* (“this scaling run preserves CCI on the margin because of overhang”) with no artifact that fails that sentence.

That is constructibility: willing/able to construct the certified class vs willing/able to produce an alignment-shaped justification.

## Tie to ch37 (mandatory)

ch37 success is an **ecosystem basin**: knowledge conducts into decisions. Construction 2.0 treats that as **necessary and not sufficient**.

| ch37 criterion | Construction reading | Constructibility failure if… |
|----------------|----------------------|------------------------------|
| \(A_t\) changes decisions | Artifacts can be construction interventions \(I\) (change \(Q,f,\theta,E\)) or mere certificates | Decisions change toward capability under an alignment label |
| \(E_t\) constrains claims | Frozen \(D\) / \(P\) set **before** \(I\); disconfirming worlds pre-registered | Evidence is selected among impact-counterfactuals |
| \(G_t\) connects to deployment | Uptake of a **stop** or of a **symmetry-breaking rule**, not of a narrative | Governance uptake of passable evals (compliance attractor) |
| \(C_t\) cross-role correction | Constructors can be corrected by people who do not share the lab’s career gradient | Coalition glued by the word “alignment” (conflationary alliance) |
| \(L_t\) challengeable | Outsiders can reject “without us it would have been worse” without joining the ontology | Legibility of the *story*, not of the control geometry |

ch37 WWCTV already names: false attractors can propagate safety-theater as efficiently as real constraints. 2.0’s job is to make that a **constructor-side** test, not only a field-conductivity test.

Split already proposed for foundational work (`drafts/ngo-ontology-and-TSA.md`), reused here:

- \(Q_{\mathrm{science}}\): what confusion dissolves / what worlds would make this *not* construction?
- \(Q_{\mathrm{action}}\): what decision changes once the relevant bridge is measurable?

Lab uptake (\(Q_{\mathrm{action}}\) only) is not constructibility success.

## Proposed 2.0 chapter families

Numbers are placeholders. Do not create `.tex` files until a family is unblocked. Prefer **new Part XI** (or a construction companion volume) over stuffing ch33–ch38.

### Family A — Restate the cut (short; can draft from existing prose)

1. **Certification is not construction** — v1 ch33 + intro Q2; Lean `CertifiedAsRealizing` vs `ConstructionCrux`.
2. **When certification is not enough** — singleton/fast-takeoff, wrong vacuum (attractor paper), no independent types for ecological checking (ch34 census vs ecology).

**Deferred manuscript object (not Family A–D):** hybrid harm-path grammar (flow + jumps + \(T^{n}\)) from [`drafts/adverse-process-generator/`](../adverse-process-generator/). v1 weaves operational closure into ch05/ch12/ch30/ch33/ch36/ch42/ch44/ch46 without publishing the nine axes. Candidate **2.0 appendix** (coverage audit, same role as Turchin’s table in ch05—not a second ontology) or a **2.0 chapter** next to successor/certification if Witness/Construct unblocks construction-conditioned bounds. Sources: `generator.md`, `measures-coverage.md`, `design-bounds.md`.

### Family B — Concrete construction (gated: Witness fail/refuse *on that part*)

Only open a chapter when the corresponding part has a named \(I\), frozen \(D\)/\(P\), and a host that can fail the construction criterion.

| Candidate part | v1 / Lean / paper hook | Unblock when |
|----------------|------------------------|--------------|
| Spec-relative builder (GSAI-shaped) | `gsaiConstructionBet`; ch42 safety-case | Spec coverage fail on a real omitted phenomenon |
| Principles-as-feedback (CAI-shaped) | `caiConstructionBet`; `fin_claimed_builder_without_realization` | Catalog builder claimed, realization fails on frozen constitution |
| Institutional / procurement class | `institutionalConstructionBet`; App C; ch38 clauses | A procurement rule that *stopped* a deployment, or refused |
| Attractor symmetry breaking | Constructing Alignment Attractors; ch34–ch38 | Named \(I\) moved geometry toward frozen \(D\), or fail/refuse (TODO H5 construction vs certification stop) |
| Successor / tiling construction | ch30–ch33; MB5 | Inheritance test that a built successor *fails* |

Until unblocked, keep these as **site cards + paper + Lean bets**, which is the current state.

### Family C — Technical process conditions (can outline now; empirical later)

Conditions on the *construction process*, not on the finished ASI:

- \(D\) / \(P\) frozen independently of \(I\) (anti-baked-conclusion; `INSTRUCTIONS.md` / AGENTS.md).
- Named intervention \(I\) (payoffs, kernels, selectors, reconstructive biases) — paper’s construction class.
- Fail/refuse is a success of the *method*; green dashboard without a stop is not.
- Construction vs certification trees on the **same episode** (TODO: H5 two trees).
- Distinguishing optimizer-policy counterfactuals (ch16/ch25/ch39) from **intervention-impact** counterfactuals.

### Family D — Social process conditions (the Ngo-shaped gap; outline now)

When people/labs/orgs will actually construct rather than pessimize:

- Impact-counterfactual flexibility as a **constructor** failure mode (not system goal-laundering).
- Demarcation: work that may count as constructing \(P\) vs “prevent overhangs” / “buy time” / “without us, worse.”
- Career and prestige gradients as selectors on *stories* (ch37 reputation attractor applied to constructors).
- Composite willingness: ch09 \(C_{\mathrm{lab}}\) may be able to construct and unwilling, or willing and unable.
- Reverse-gap pointers (do not add spine terms): conflationary alliances; fake thinking; Long Self-Correction (competence-to-wield ≠ channel integrity).

**Best example (residual risk):** if TSA is used as a brand inside a lab, v1 has no artifact that fails “this capability work differentially advances alignment.” Family D’s first operational ask is that sentence-shaped **refuse**.

## Phasing

| Phase | When | Work |
|-------|------|------|
| **P0** | Now (this file) | Objects split; 2.0 map; ch37 ties; Ngo residue named; manuscript still out |
| **P1** | After author OK | One Family D note (App B reverse column or field-hub “constructor-side”) — still not v1 chapters |
| **P2** | Witness Exp. 4 | Revisit manuscript: Family A paragraphs in ch33/intro only if they do not claim Q2 solved |
| **P3** | Per-part fail/refuse | Open Family B chapters one at a time; H3/H4 wrong-vacuum / enforcement-collapse only after bar |
| **P4** | TSA 2.0 | Part XI (or companion): Families A–D; decide whether a seventh claim exists; **rerun** the 48-chapter formulation-groundedness (G) pass on the 2.0 map before treating new covering formalisms as settled ([`review/chapter-formulation-groundedness.md`](../../review/chapter-formulation-groundedness.md)) |

**Gates (unchanged from TODO):** Witness real stop → *concrete construction* manuscript revisit. Family D outlining does **not** wait on that gate; Family D *claiming that we can construct* does.

## External lit review — usable list (2026-08-25)

Raw result: [`drafts/ontology-reviews-2021-2026/construct-lit-review-result.md`](../ontology-reviews-2021-2026/construct-lit-review-result.md) (wrong folder; treat as FINDINGS draft). Prompt: [`construct-lit-review-prompt.md`](construct-lit-review-prompt.md). Internal seed: [`construct-external-lit.md`](construct-external-lit.md).

**Verdict:** usable as an XI/XII briefing after stripping Perplexity `turnNsearch` cite junk. Argument matches the construction filter. **Not** a new spine primitive. Do not ingest into v1 chapters.

**Load-bearing line from the review (keep):** construction is strong when \(D\) is coupled to a controllable, distinguishable boundary. If desired and undesired states look the same at that boundary, contracts, coin votes, TEEs, zk proofs, stronger selectors, and verified compilers cannot create the missing distinction.

**Prompt compliance (why keep the file):** claim-strength tags; buckets; “idle for AI if…”; DAO split \(R \neq \theta \neq H \neq S \neq D\); hard fork classified as social layer; contract/verification homographs; amendment table asks handle vs record; GSAI = agenda, CAI = empirical on a proxy, AI Control = testbed \(\theta/H\).

**Disagreement with App M (keep both):** the review puts Glass–Steagall→2008 and Marian/Republic in bucket 5 (analogy, not builder theorems). App M may still use them as genesis/slack *stories*. XI should not load them as construction proofs.

### Already in v1 / papers (do not re-cite as new)

AEC→NRC, Enron/PCAOB, Acemoglu–Robinson 2008, FAA/FDA/Lloyd’s, GPL/tivoization, Maskin 1999, Huang et al. 2026, Grossman–Hart 1986, Ostrom 1990, Anderljung et al. 2023, Dalrymple et al. GSAI 2024, Bai et al. Constitutional AI, Greenblatt/control (field; TSA also has alignment-faking). The review’s *distinction* (deployment filter ≠ constructed target) is the usable bit of the control paper.

### Keep for XI — new or under-cited, with reasoning

| Source | Reasoning |
|--------|-----------|
| Cox, Arnold & Villamayor-Tomás 2010 (*Ecology & Society*) | Empirical check of Ostrom principles (91 studies). TSA cites Ostrom 1990, not this meta-analysis. Constructibility: principles are conditions, not a recipe; copyable millisecond AI may fail the monitoring/boundary conditions. |
| Sandholm 2005 (*RESTUD*, negative externalities / evolutionary implementation) | Stronger than Sandholm 2002 already in the constructing-attractors bib. Shows construction = change payoff *geometry* so dynamics converge, not “more selection pressure.” |
| Myerson–Satterthwaite 1983; Gibbard 1973 | Prompted; not in constructing bib. Blocks “just VCG” / unrestricted strategy-proof voting. |
| Bergemann, Koh & Morris 2026 (arXiv:2609.01595) | Mechanism design for acting AI with unknown \((A,u)\). Verification order + honesty/obedience is the field implementation of ch10/11/14 concealment and eval→permission IC. Peer scoring is a Crémer–McLean benchmark (unbounded free rewards), not a protocol. XI: constructs announced \(f\) on contractible certificates; does not construct \(D\). |
| Klein et al. seL4 (SOSP 2009); CompCert | Best exhibits of verifier-for-*stated*-spec. TSA named the class; these pay the hedge (spec may not be \(D\); hardware/boot assumptions). |
| Foreshadow (Van Bulck et al. 2018) + AMD/Intel 2025–26 TEE advisories | Concrete “TEE relocates trust” (vendor root, side channel, firmware). |
| NIST multi-party threshold crypto; OpenZeppelin TimelockController; Maker Emergency Shutdown | Operational handles \(H\). Timelock idle if damage horizon \(< \tau_{\mathrm{detect}}+\tau_{\mathrm{decide}}+\tau_{\mathrm{intervene}}\). |
| Optimism Token House / Citizens’ House (2023); Arbitrum AIP-1 → AIP-1.1 | Construction of a selector/veto vs fail-and-patch when de facto treasury control diverged from DAO competence. |
| SEC *DAO Report* (2017) | Primary for 2016: intended \(D\) ≠ Solidity machine; recovery was \(S\). |
| Trout 2024 arXiv:2409.06673; Stetler 2025 arXiv:2504.02127 | Insurance as *agenda* gate; fail if tail unpriceable or coverage not mandatory. |
| OMB M-25-22 (2025); BIS advanced-compute / IaaS license rules (2025–26) | Strongest AI-specific *historical* \(\theta/H\) rows (procurement, chip/cloud choke). Idle if copies/compute substitute. |
| EU AI Liability Directive (proposed 2022, withdrawn 2025) | Failed amendment: not a handle. |

### Abstract-only in the review — do not treat as paid

Hart–Moore 1999; Bergemann–Morris 2005 (robust MD — promising if verified); Sharma et al. 2024 (DAO sample; was in the seed); Pahari et al. 2026 (48 DAOs, concentration). Verify primary before XI cite.

### Prompt gaps (optional later pass)

Hadfield-Menell & Hadfield 2019, Chassang Interactive Alignment, Dafoe Cooperative AI, futarchy, Kleros, MACI, Dutch water boards, Japan nuclear village. Not blocking; the review chose load-bearing cases.

### Do not ingest

Perplexity citation tokens; a new TSA primitive; GSAI/CAI as `ConstructionCrux` discharge; conductivity as construction.

## Checklist

- [x] Lane plan file exists; TODO work-map node points here
- [ ] Author decision: 2.0 as Part XI vs XI+XII vs companion volume vs keep papers-only until P3
- [x] External construction lit review received — [`construct-lit-review-result.md`](../ontology-reviews-2021-2026/construct-lit-review-result.md); usable list in this file
- [ ] Cite-clean FINDINGS + optional move out of `ontology-reviews-2021-2026/`; ingest **keep** rows to constructing-paper / XI bib only when drafting
- [ ] P1: reverse-crosswalk row for impact-counterfactual cherry-picking ≠ laundering ≠ \(\mathrm{Fit}_E\) ≠ ch25 counterfactuals
- [ ] Map Family B candidates → current site cards (CEV/CAI/GSAI/institutional) without implying crux discharge
- [ ] Specify H5 “two trees” protocol (construction vs certification stop, same episode) as Witness *addendum*, not Expectation 7 revival
- [ ] ch37: one 2.0 paragraph (when drafting) that conductivity ≠ construction; false attractor = constructibility failure
- [ ] ch40: one 2.0 sentence that humans also launder *motives* via unused counterfactuals; v1 detector does not cover that
- [ ] Do not open chapter `.tex` files in this lane until P2/P3
- [ ] **Rerun formulation-groundedness (G)** on the 2.0 chapter map (same process as the 2026-08 v1 pass: one read-only reader per chapter, F1–F5, do not raise G by inventing early tuples). Method and v1 snapshot: [`review/chapter-formulation-groundedness.md`](../../review/chapter-formulation-groundedness.md). Do not reuse v1 scores after 2.0 drafting.

## Related

- [`metadata/TODO.md`](../../metadata/TODO.md) — Construct row + parked manuscript rule
- [`witness.md`](witness.md) — Exp. 4 gate; evaluation ≠ changing \((Q,f,\theta,E)\)
- [`drafts/plans/construct-external-lit.md`](construct-external-lit.md) — internal seed
- [`drafts/plans/construct-lit-review-prompt.md`](construct-lit-review-prompt.md) — attachable external-agent prompt
- [`drafts/ontology-reviews-2021-2026/construct-lit-review-result.md`](../ontology-reviews-2021-2026/construct-lit-review-result.md) — external-agent FINDINGS (cite-clean later)
- [`papers/constructing-alignment-attractors/`](../../papers/constructing-alignment-attractors/)
- [`formal/AlignmentProofSpine/AlignmentConstruction.lean`](../../formal/AlignmentProofSpine/AlignmentConstruction.lean)
- [`review/chapter-formulation-groundedness.md`](../../review/chapter-formulation-groundedness.md) — v1 E/G snapshot; **rerun G at 2.0**
- Session: Ngo paragraph review (2026-08-24, this conversation)
