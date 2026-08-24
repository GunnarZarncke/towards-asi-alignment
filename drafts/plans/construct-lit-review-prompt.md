# Literature review prompt (self-contained)

**How to use:** Copy from `BEGIN PROMPT` through `END PROMPT` (or attach this whole file) to an agent that has web/search access. The agent does not need any other project files.

---

BEGIN PROMPT

You are an independent literature reviewer. You do not have, and should not assume, any private manuscript, codebase, or in-house terminology. Use public sources. Prefer primary papers, handbooks, and documented historical cases over blogs and vendor pages. When you use a secondary source, say so.

## Question

Advanced AI systems will be trained, copied, selected, governed, and constrained by people, firms, laws, markets, and software. Some literatures claim we already know how to **build** pieces of that surrounding system: institutions, contracts, voting rules, cryptographic ledgers, hardware enclaves, formal verifiers.

Review those literatures and answer:

**Which parts of a socio-technical control system can already be constructed, under what conditions, and what is known not to work?**

“Constructed” means: we can actually put the piece in place so that a **pre-specified** desired property is more likely to hold, and we can tell whether we failed.

This is **not** a review of “how to align AGI” in general, and **not** a review of how to *evaluate* or *certify* a system after it exists. Evaluation/certification (tests, audits, safety cases, licenses that check a list) is in scope only when it is being confused with construction, or when the certification regime itself is the thing being built (e.g. an insurance market, an independent regulator).

## Definitions (use these; do not replace them with slogans)

**Desired region D.** A property or set of states specified **before** the intervention. Examples: “cooperation is the unique ESS in this game,” “the uncertified product cannot be sold without insurance,” “only this measured binary can run,” “this social-choice rule is the Nash outcome.” If someone defines D as “whatever our intervention made stable,” that is not construction; it is tautology.

**Intervention I.** A change to payoffs, copying/transformation rules, who gets selected, the environment, the contract language, the voting rule, the hardware, or the legal mandate.

**Construction** of a *part* of the system: I is applied, D was fixed first, and there is a check (theorem, experiment, or historical outcome) that the part now does what it was specified to do—or a clear fail.

**Not construction:**

- Making it more expensive to *forge a log, a vote record, or a certificate* while the underlying behavior is unconstrained.
- A report, dashboard, or white paper that people can ignore.
- A research agenda that *names* a builder (“train with principles,” “write a world model”) without a demonstrated system or a theorem of implementation.
- “Code is law,” “decentralization,” “alignment by design,” or “crypto will enforce it.”
- Turning up selection pressure (stronger scoring, more competition) when the scorer cannot tell desired states from undesired lookalikes.

**Constructibility** (process, not a gadget): conditions under which people or organizations will *actually* build the part rather than keep the label. Genesis routes, dual mandates, career incentives, and “we had to ship” belong here.

**Claim strength** (tag every finding):

| Tag | Meaning |
|-----|---------|
| **proved** | Theorem with stated assumptions |
| **standard** | Textbook result, widely replicated in that field |
| **historical** | Documented institutional case |
| **empirical** | Systematic data (many DAOs, CPR meta-analysis, etc.) |
| **agenda** | Proposed architecture, not shown |
| **marketing** | Vendor or advocacy claim |

If a source is **agenda** or **marketing**, say what would count as a fail.

## Parts vocabulary (classify each source as acting on one or more)

Use ordinary names, then optionally the short code:

| Part | Code | Meaning |
|------|------|---------|
| Transformation / copying | Q | How variants are generated (mutation, fine-tune, fork, reconstruction) |
| Payoffs / fitness | f | What success is, including sanctions and transfers |
| Selector | θ | Who is copied, funded, licensed, insured, elected |
| Environment | E | Physical/legal/technical setting |
| Records | R | Logs, chain state, attestations, proofs about traces |
| Social layer | S | Human override: courts, hard forks, boards, “we ignore the code” |
| Handle | H | A stop, delay, veto, recall, pause, threshold consent that actually binds |
| Independent corrector | C | A body that can constrain the promoter without sharing its mandate |
| Inheritance lever | L | A constraint that still binds copies, successors, or modified versions |
| Verifier-for-stated-spec | V | Proof or monitor that a *stated* spec holds in a *stated* model |

A cryptographic ledger that faithfully executes Solidity is **R** (and maybe **H** on on-chain assets). It is not automatically **D** for “fair governance” or “aligned AI.”

## Starting points (verify; do not treat as complete or as your conclusions)

These are leads. Check primaries. Contradict them if the sources do.

**Institutions**

- Elinor Ostrom, *Governing the Commons* (1990): design principles for common-pool resources; not a universal recipe.
- Dual-mandate regulators: U.S. Atomic Energy Commission vs later NRC split; “nuclear village”; Arthur Andersen/Enron and PCAOB.
- Selection by insurance and licensing: Lloyd’s Register; aviation airworthiness + insurance; pharmaceutical licensure.
- Constraint inheritance and its failure: GNU GPL; SaaS bypassing “distribution”; **tivoization** (cryptographic signing so users cannot run modified code while the license text is satisfied); GPLv3 installation-information patch.
- Reform decay: Glass–Steagall repeal to 2008; ritual drills with a permanent zero failure rate vs exercises that can fail.
- Capability outrunning correction: Marian army reforms and the late Roman Republic (new private military power; old civilian checks idle).
- *De jure* reform vs *de facto* power: Acemoglu & Robinson, “Persistence of Power, Elites, and Institutions,” *AER* 2008.
- AI-governance uses of these analogies: Anderljung et al. on frontier licensing; dual-mandate warnings for IAEA-like AI bodies (e.g. Law 2023; Zaidi on Baruch/nuclear precedents).

**Mechanism design**

- Hurwicz: incentive compatibility.
- Gibbard revelation principle: incentive-compatible direct mechanisms; truth-telling need not be the *unique* equilibrium.
- Gibbard–Satterthwaite: strategy-proof social choice is extremely restrictive.
- Maskin (1999 / 1977): Nash implementation requires monotonicity; with ≥3 agents, monotonicity + no veto is sufficient; proofs are often constructive but mechanisms can be huge.
- Incomplete contracts: Grossman & Hart 1986; Hart & Moore 1988, 1999.
- Hadfield-Menell & Hadfield, “Incomplete Contracting and AI Alignment,” AIES 2019: misspecification as incomplete contracting; gaps filled by external law/norms, not a complete reward.
- Huang, Tharas, Marro, et al., “Mechanism Design Is Not Enough,” arXiv:2605.08426 (2026): *incontractible cells* and a welfare gap no mechanism in that language closes; verify the theorem, do not cite from memory.
- Sandholm, evolutionary implementation (static Nash ≠ dynamic convergence).
- Efficiency / budget / incentive tradeoffs: Myerson–Satterthwaite, Green–Laffont; do not propose “run VCG for alignment” without them.
- Cooperative AI: Dafoe et al. 2020/2021; Chassang, “Interactive Alignment,” arXiv:2607.25019.

**Crypto, DAOs, hardware**

- The DAO (2016): reentrancy; intended member-controlled treasury vs actual Solidity machine; Ethereum hard fork vs Ethereum Classic; U.S. SEC DAO Report.
- Vitalik Buterin, “DAOs are not corporations” (2022): https://vitalik.eth.limo/general/2022/09/20/daos.html
- Empirical DAO work: Sharma et al., arXiv:2410.13095; Ostrom-to-DAO papers in *Frontiers in Blockchain* (commons DAO design 2023; digital commons 2025; RARI/Arbitrum/Optimism governance comparison 2026).
- Token-voting failure modes: plutocracy, low turnout, whale capture; patches such as Optimism Token House / Citizens’ House.
- TEEs and attestable evaluation: e.g. arXiv:2506.23706; also known SGX/TDX/SEV side channels, availability, and vendor root-of-trust.
- Formal verification of *stated* specs in *stated* models: seL4, CompCert, Common Criteria, DO-178C — report what is actually proved.

**Spec-relative AI builders (agendas unless you find a deployed theorem)**

- Dalrymple, Skalse, et al., “Towards Guaranteed Safe AI,” arXiv:2405.06624; ARIA Safeguarded AI programme notes.
- Constitutional AI / RLAIF (Bai et al. 2022): a *claimed* training procedure, not a proof that the constitution is realized.
- Redwood-style AI control: safety despite subversion — usually evaluation/oversight, not construction of the optimizer’s target. Classify carefully.

## Search coverage (hit all six)

1. **Institutional design and political economy** — Ostrom and CPR meta-analyses; Buchanan constitutional political economy; Hirschman exit/voice; capture (Stigler, Carpenter); principal–agent; procurement and insurance as selectors; licensing of dangerous technologies.
2. **Mechanism design and implementation** — as above, plus Bayesian and robust/Wilson mechanisms, renegotiation, collusion.
3. **Blockchains and DAOs** — The DAO; Maker, Moloch, Aragon, Optimism, Arbitrum, Snapshot, Governor Bravo; quadratic/conviction voting; futarchy (Hanson); MACI; Kleros; legal wrappers (e.g. Wyoming DAO LLC).
4. **Cryptography and hardware as handles** — threshold signatures, timelocks, circuit breakers; remote attestation; ZK proofs of statements about traces; secure boot / tivoization as *anti*-correction; what TEEs do not prove.
5. **Builders that claim to produce a system from a spec** — guaranteed-safe / world-model+spec+verifier; runtime monitors; debate and amplification (construction vs evaluation).
6. **Amendments to existing institutions for frontier AI** — concrete proposals (with evidence or failed trials) for courts, procurement, insurance, standards, and compute access. No wish lists without a citation.

## How to classify each source

Pick one primary bucket:

1. Constructs a named part (say which part from the table).
2. Constructs only cheaper-to-detect forgery of records (R), not the target property.
3. Constructibility / genesis condition (when people will build it).
4. Negative or impossibility.
5. Analogy, slogan, or toolkit that restates the difficulty.

Then fill: acts on Q / f / θ / E / R / S / H / C / L / V; claim-strength tag; assumptions that would make the result idle for AI (speed, copyability, opacity, incomplete language, endogenous selector, irreversible failure).

## Deliverable

Write a standalone markdown report with these sections. No dependence on any other document.

1. **Executive summary.** Bullet list: parts that can already be built; one line each; claim-strength tag; the condition that must hold.
2. **Negatives.** What cannot be constructed by (a) written contracts, (b) coin voting, (c) TEEs/ledgers, (d) waiting for a catastrophe, (e) intensifying an indiscriminate selector.
3. **Master table.** Columns: Source (cite) | Part | Acts on | Strength | Idle for AI if… | Bucket (1–5).
4. **Institutions cluster.** Genesis routes; dual mandate; inheritance/tivoization; decay vs refresh; insurance/licensing gates. For each: flagship case, what was built, what broke.
5. **Mechanism-design cluster.** Which theorems are load-bearing for *building* a game or contract; which are idle because message spaces, completeness, or unique-equilibrium assumptions fail for AI. Quote assumptions, not just names.
6. **DAO/crypto cluster.** The DAO (2016) plus **three** later DAOs you actually look up. For each: intended D; actual machine; whether a social-layer override happened; whether Ostrom-style monitoring and graduated sanctions held.
7. **Hardware/proof cluster.** What attestation and machine-checked proof construct; vendor trust; side channels; tivoization as constructed *loss* of a user handle.
8. **Amendment cluster.** For each of: courts, licensing, insurance, public procurement, technical standards, compute/cloud access — one real proposal or failed proposal with a citation, and whether it builds a handle or only a record.
9. **Open questions** (maximum 10) that this review cannot close.
10. **Sources** used, with URLs or DOIs. Mark unread items you only saw cited.

## Rules

- Do not invent a new alignment framework or a list of new technical primitives.
- Do not conclude that aligned superintelligence has been or can be built from these pieces.
- Do not treat “the community forked the chain” as on-chain construction of D; classify it as social layer S.
- Do not treat a claimed builder (RLAIF, GSAI, a DAO constitution) as success unless you have a check that D, specified first, held—or an explicit fail.
- If two fields use the same English word (selection, contract, verification, governance), say that they are different objects.
- Prefer fewer, load-bearing sources over a long bibliography of near-duplicates.

END PROMPT
