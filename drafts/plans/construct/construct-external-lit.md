# External construction knowledge + literature-review prompt

Status: **seed** (2026-08-24). Companion to [`construct.md`](construct.md). v1 App C/M already map institutions onto TSA vocabulary; this file asks what those literatures (and crypto / mechanism design) actually **construct**, for TSA 2.0 Parts XI–XII.

**Do not treat this seed as the review.** External FINDINGS: [`../ontology-reviews-2021-2026/construct-lit-review-result.md`](../ontology-reviews-2021-2026/construct-lit-review-result.md). Keep-list + reasoning: [`construct.md`](construct.md) § External lit review.

---

## Filter (use on every source)

An intervention \(I\) is construction for a frozen target \(D\) / \(P\) only if it (i) breaks a stated harmful symmetry or implements a named social-choice / constraint object, (ii) the post-\(I\) process can be checked against attractor or realization conditions for **that same** \(D\), (iii) \(D\) is not defined as “whatever \(I\) stabilized.”

**Not construction:** raising the fake-cost of a *record*; conductivity of a report; catalog `claimsExplicitBuilder`; “code is law” slogans; intensifying a selector that cannot tell \(D\) from \(A\).

---

## Seed: what is already reliably known *outside* the TSA chapters

In-repo homes: App C (`appendices/appC-institutional-translation.tex`), App M (`appendices/appM-institutional-histories.tex`), constructing-attractors paper + bib, Lean `institutionalConstructionBet` / `gsaiConstructionBet`.

### 1. Institutional design (App C/M; amend, do not replace)

These construct **correction and selection infrastructure**, not an aligned superintelligence. That is still a part of the overall system.

| Constructible part | What is known | Limit |
|--------------------|----------------|-------|
| **Genesis of a corrector** | Three routes that do not require alignment theory first: money already at risk (Lloyd’s Register, audit, cyber-insurance); survivable catastrophe ratchet (FDA, aviation); chronic threat that refreshes attention (Dutch water boards). | Catastrophe route is idle if failure is irreversible at scale (App M explicit). |
| **Selection gating** | Joint insurance + licensing + procurement can make the uncertified path more expensive than the certified one (airworthiness; pharma licensure; INPO). | Needs a checkable signal whose fake-cost exceeds honest compliance. |
| **Structural split at founding** | Dual-mandate bodies (AEC; Andersen/Enron; “nuclear village”) are captured *at genesis*. Historical remedy is split + independent funding + statutory evidence access, not a second audit layer. | Lab self-eval, AISI-in-growth-ministry, industry-populated standards, negotiated eval access already instantiate this. |
| **Constraint inheritance** | Copyleft (GPL) can inherit a handle across successors *when* a distributed lever exists. | GPLv2 “distribution” ontology failed under SaaS; **tivoization** used cryptographic signing to keep the *text* while killing the *run-modified-code* handle. GPLv3 patched installation information — ontology shift of the trigger, not a proof that copyright transfers to weights. |
| **Memory / decay** | Constraints decay on roughly a working-generation timescale unless independently re-derived (Glass-Steagall). Ritual drills with zero observed failure ≠ refresh. | TSA CCI is still a point certificate; App M proposes a decay term (open). |
| **Entrenchment** | Eternity clauses / mutually incentive-diverse auditors, not a tower of same-basin auditors. | Guardian regress unsolved for AI CCI as the entrenched object. |
| **Capability–correction slack** | New causal-reach class (Marian legions) can make an existing sophisticated correction architecture idle. Retrofit needs the actor the channel would constrain. | Construct the channel *before* the class exists. |
| **Interface vs amendment (App C §Interface or Amendment)** | Use existing institutions for legitimation, contestability, enforcement, public meaning. Amend where they lack speed, adversarial measurement, composite-agent maps, or new bearers. | Mapping is analogy, low confidence (App C epistemic status). |

**Already in TSA papers, not chapters:** Ostrom nested rules change \(f,\theta\) in commons-like games; Acemoglu–Robinson *de facto* power can neutralize *de jure* reform (selector endogeneity at social scale).

### 2. Mechanism design and implementation theory

Reliable as **possibility/impossibility for announced games**, not as ASI construction.

| Result | Claim strength | Construction purchase |
|--------|----------------|------------------------|
| Hurwicz incentive compatibility; Gibbard revelation principle | Standard | Search among direct mechanisms is enough *for IC*; IC ≠ unique equilibrium. |
| Gibbard–Satterthwaite | Standard | Strategy-proof social choice over ≥3 alternatives is dictatorial (under usual conditions). Dominant-strategy construction of rich social choice is mostly negative. |
| Maskin monotonicity necessary for Nash implementation; monotonicity + no-veto, \(n\ge 3\), **constructive** mechanism | Proved (Maskin 1999 / 1977) | Some social-choice rules *can* be implemented as game forms. The constructed mechanisms are often huge / unnatural message spaces. |
| Incomplete contracts (Grossman–Hart–Moore) | Standard | Language cannot distinguish all payoff-relevant states. |
| Hadfield-Menell & Hadfield 2019 | Agenda | Alignment as incomplete contracting; gaps filled by **external** law/norms, not a complete reward. Construction of the *cognitive* process that appeals to those institutions is the open bet. |
| Huang et al. 2026 arXiv:2605.08426 | Cited in TSA paper; verify on review | **Incontractible cells** → strictly positive welfare gap no mechanism *in that language* closes; other-regarding weight can close it but is exploitable without certification. |
| Sandholm evolutionary implementation | Standard in that literature | Static Nash implementation ≠ convergence under adjustment dynamics. |
| Myerson–Satterthwaite, Green–Laffont, etc. | Standard | Budget-balance / efficiency / IC tradeoffs; do not ignore when proposing “just run a VCG for alignment.” |
| Bergemann, Koh, Morris 2026 arXiv:2609.01595 | Mechanism design with unknown alignment and capability; one-sided verification order; honesty+obedience (double deviation); sandbagging as IC of eval→permission maps; capability–bias covariance; peer scoring as a possibility result under unbounded free rewards | Construction of *announced* permission/reward maps on contractible reports. Residual: incontractible cells, no free transfers, static one-shot. v1 uses this as the implementation of ch10/11/14 incentive constraints, not as a construction of \(D\). Peer implementation is a benchmark, not a protocol, because rewards are unbounded and free. |

**Purchase for XI:** written mechanisms construct announced \(f\) on **contractible** coordinates. Residual defection moves to incontractible cells (already a named failure mode). Filling cells requires either a richer language, a change of \(f\) *inside* the agent, or a change of \(\theta\) — not a longer contract.

### 3. Cryptographically secured / blockchain / DAO systems

Reliable negatives and a narrow positive.

**Positive (narrow):** Consensus + signatures can make *stated* state transitions of a *stated* machine costly to fake after the fact. Multi-sig, time-locks, and pause/guardian keys can construct **handles** (halts, delays, threshold consent) on assets the chain actually controls. TEEs / remote attestation can bind “this measured code ran on this hardware” (e.g. attestable audits, arXiv:2506.23706). ZK proofs can raise fake-cost of *statements about traces* without revealing the traces.

**That is not \(D\).** TSA constructing paper already: proofs and commitments constrain traces; they do not keep CCI uncaptured or force predicates to track \(D\) after ontology shift. Hardware attestation adds a **vendor/root-of-trust** and side-channel / availability assumptions.

**DAO / “The DAO” (2016) — canonical construction failure:**

- The intended governance object (member-controlled treasury) was not identical to the Solidity machine (reentrancy / checks-effects-interactions). Spec ≠ code is incomplete contracting on a formal substrate.
- Warnings existed; dual-mandate-ish construction (builders reviewing their own high-value contract under time pressure).
- Recovery was a **social-layer hard fork**, not an on-chain correction channel. “Code is law” was explicitly broken. Ethereum Classic is the vacuum that kept the unforked history.
- SEC “DAO Report” treated the offering as securities — legal layer reasserted.

**Empirical DAO governance (2023–2026 literature, seed not verified end-to-end):** token voting → plutocracy, low turnout, whale capture; “decentralized” orgs independently converge on **legal wrapper + security council + token house** (RARI / Arbitrum / Optimism-style three-body). That is re-importing App C institutions, not replacing them. Ostrom-to-DAO mappings repeatedly find missing cheap monitoring of the *intended* referent, graduated sanctions that don’t bind, and nested enterprises that collapse into core teams. Buterin 2022: DAOs that must be *sovereign* (stablecoins, courts, purpose-locked treasuries) need political-science construction, not corporate boards; coin voting is the wrong \(f\) when the target is not shareholder profit.

**Tivoization again:** cryptography as construction of *anti-correction* (signed boot) while semantic freedom is preserved — App M’s GPL case is the TSA-relevant exhibit.

### 4. Spec-relative / GSAI-shaped construction (field, not TSA theorem)

Dalrymple et al. 2024 *Towards Guaranteed Safe AI*; ARIA Safeguarded AI. Three-part builder: world model, safety specification, verifier/proof. TSA already catalogs this as `gsaiConstructionBet` with `claimsExplicitBuilder = true` and `openWorldCoverage = true`. **Known:** the architecture. **Not known:** a world model that is complete enough for the spec (TSA MB9 / omitted-phenomena cousin). Construction of *verifiers for stated specs in stated models* is a real engineering industry (avionics, crypto protocols, seL4). Construction of the *spec of human-correctable value update* is not.

### 5. Parts of the overall system these literatures *can* already construct

Say this in XI without overclaim:

1. **Handles on money, licenses, and compute access** — if a counterparty’s capital is exposed and a signal is checkable (insurance, procurement gates).
2. **Independent corrector bodies** — if promotional and safety mandates are split at founding.
3. **On-chain or TEE-backed records and delays** — for properties that are literally the encoded machine.
4. **Nash-implementable social-choice rules** that satisfy Maskin monotonicity (in the model).
5. **Commons rules** that match Ostrom’s design principles in slow, monitored, local CPRs.

Do **not** say they construct: bundle geometry, bearer maps, uncaptured CCI under strategic opacity, successor closure for weight copies, or lab constructibility (Ngo).

---

## Seed bibliography (do not rediscover; do extend)

**Already in repo / papers bib:** Ostrom 1990; Maskin 1999; Grossman–Hart 1986; Hart–Moore 1988/1999; Hadfield-Menell & Hadfield 2019; Huang et al. 2026; Sandholm 2002; Acemoglu–Robinson 2008; Anderljung et al. 2023; Law 2023 dual mandate; Zaidi 2021; Dalrymple et al. GSAI 2024 (field card); constructing-attractors intervention table.

**Must add on review (seed URLs):**

- Buterin, *DAOs are not corporations* (2022): https://vitalik.eth.limo/general/2022/09/20/daos.html
- The DAO 2016 + Ethereum hard fork / social layer (The Block anniversary; DF3NDR DAO chapter)
- Frontiers blockchain: Ostrom–DAO (2023 commons DAO design; 2025 digital commons; 2026 RARI/Arbitrum/Optimism three-body)
- Sharma et al. 2024 *Future of Algorithmic Organization* arXiv:2410.13095 (100 DAOs, Gini/participation)
- Attestable audits / TEEs arXiv:2506.23706
- Maskin implementation handbook chapter; Nobel lecture (constructive Nash implementation)
- Gibbard–Satterthwaite (strategy-proofness)
- Optimism bicameral (Token House / Citizens’ House) as plutocracy patch
- seL4 / Common Criteria / DO-178C as *verifier construction for stated specs* (not value specs)

---

## Prompt for a literature review

**Self-contained (for an external agent):** copy or attach [`construct-lit-review-prompt.md`](construct-lit-review-prompt.md). It does not mention this repo, TSA, Lean, or in-house terms.

Internal seed above is for authors in this repo only; the external prompt re-states the filter in ordinary language.

---

## Related

- [`construct.md`](construct.md) — XI/XII plan
- App C / App M as v1 institutional surfaces
- Session log: this file’s creation
