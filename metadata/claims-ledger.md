# Claims Ledger

Track every major claim with status, support, weakest link, and falsification criteria.

**Last cross-check:** 2026-08-21 — Track B §1: C-044 tracks status restatement in ch48, not discharge of the six intro claims. Prior 2026-08-17: Phase 0–1 six-claims spine pass (ch48 restates all six intro claims including grounding); spine table in `drafts/claim-spine.md`; executive-overview preservation list aligned to Introduction claim order; ch48 "six opening claims" and ch30 "nine-claim" count fixes. Prior cross-check 2026-07-04: every `Chapter(s)` column re-verified against current `ch01`–`ch48` numbering/titles in `metadata/book.yml`; one stale in-text pointer fixed (C-005 "certified boundary separation" now correctly cites ch29, not ch48). Entries remain manually maintained against the chapter `chapterthesis` blocks, the six Introduction `introclaim`s, the chapter-level WWCTV sections, `drafts/claim-spine.md`, `metadata/assumptions-ledger.md`, `metadata/uncertainty-ledger.md`, and the conceptual spine in `INSTRUCTIONS.md`.

**Resolved caveat:** the `Chapter(s)` column previously predated the 2026-06-30 global chapter renumbering (`ch01`–`ch48`, see `INSTRUCTIONS.md` §14). It has now been re-verified content-by-content (not by mechanical offset, since the four inserted chapters — ch20, ch27, ch38, ch43 — do not shift earlier claims uniformly). Numbers below are current as of this pass; re-check after any future chapter split, merge, or renumbering.

**Maintenance note:** This ledger is not generated. It must be manually updated when chapters, claims, assumptions, uncertainty entries, or proof-spine bridges change. Treat it as a maintainer audit tool rather than an automatically complete public index until the automation TODO in `metadata/TODO.md` is resolved.

**Status vocabulary:** `established` (well-supported, near-consensus) · `plausible` (argued, not proven) · `framework` (definitional/structural proposal) · `speculative` (forward-looking) · `limit` (acknowledged boundary of the theory). Per `AGENTS.md`, claim strength is calibrated to the Lean dependency spine: the book does **not** assert that ASI alignment is proven.

The six named Introduction claims map to claims C-003 (boundary), C-004 (value-bundle), C-004a (grounding), C-005 (correction), C-006 (successor), and C-007 (basin/selection). C-044 tracks their status restatement in the conclusion.

---

## Claim ID: C-001

**Claim:** The real target of alignment may be a composite socio-technical optimizer rather than an isolated AI model.

**Chapter(s):** 1, 2, 8, 9, 41

**Status:** plausible, not proven

**Support:**
- examples from markets, bureaucracies, platforms, and model–tool–user systems
- boundary formalization via conditional independence / screening-off
- multi-agent coordination literature

**Weakest link:**
- detecting composite agents empirically may be computationally and statistically difficult

**What would update against it:**
- robust evidence that frontier AI risk remains localized inside model weights and does not depend strongly on deployment loops

**References:**
- critch2022boundaries, kirchhoff2018markov, friston2010free, conant1970regulator, critch2021multipolar, kulveit2025gradualdisempowerment

## Claim ID: C-002

**Claim:** Superintelligence alignment requires preserving a human-correctable value-update process, not installing a fixed utility function.

**Chapter(s):** 1, 3, 4, 18, 25, 26, 30, 45, 46

**Status:** moderate claim (framework); strong claim (sufficiency) unproven

**Support:**
- value-bundle drift under substrate change
- correction-channel modeling
- successor creation as central test

**Weakest link:**
- operational measurement of value-update process integrity at scale

**What would update against it:**
- demonstration that fixed-value approaches suffice under realistic capability growth and successor pressure

**References:**
- yudkowsky2004cev, soares2015corrigibility, hadfieldmenell2016, christiano2018corrigibility, russell2019human, zarncke2025value-bundle-drift

## Claim ID: C-003

**Claim:** (Boundary claim) The first alignment question is not what a system wants but where the bounded optimizing process is; capability is predictive/control information across that boundary, and capability growth is boundary expansion.

**Chapter(s):** 6, 7, 11, 12

**Status:** framework

**Support:**
- agent-as-bounded-control-process definition (conditional-independence boundary)
- boundary-recovery bridge: structured candidate classes, intervention handles, sufficient margin, and empirical recovery tests whose targets do not presuppose the boundary
- task-agnostic competence measure (boundary information)
- capability growth modeled as expansion of sensory/predictive/active/memory/coordination loops
- graded-lab-simulation testbed: a communication-free workspace-handoff coordination link is invisible to passive discovery and to intervention seeded from passive's guesses, but recoverable by a standalone all-pairs probe (positive for boundary discoverability being non-trivial and method-dependent); the same probe over-merges a resource-bound bystander into a barrier unit through shared queue contention (negative — coupling-type discrimination is unsolved) (Appendix~\ref{appn-experimental-evidence}, findings GL-11/GL-12, `finding:gl-11`/`finding:gl-12`)
- graded-lab-simulation testbed: a careful, correctly-stated $I_{\mathrm{ctrl}}^X$ implementation silently reimported a task ontology via an under-scoped outcome vector, masking a task-irrelevant actor as the true driver until the vector was widened (negative — illustrates how easily task-agnosticism claims can be undercut by implementation, not by the definition) (Appendix~\ref{appn-experimental-evidence}, findings GL-13/GL-14, `finding:gl-13`)

**Weakest link:**
- boundaries are leaky and non-stationary; finite-data high-dimensional recovery may fail, learned detectors may inherit the criterion/labeling gap, and the boundary-finding procedure may not converge on real adversarial systems

**What would update against it:**
- evidence that alignment-relevant risk is well-predicted by task-battery performance without reference to any boundary/object question, or that boundary recovery remains statistically/computationally infeasible even with structured candidates, intervention handles, and adversarial generator--detector training

**References:**
- kirchhoff2018markov, friston2010free, conant1970regulator, critch2022boundaries3a, orseau2018agents, kenton2022discovering, zarncke2025uad, wentworth2021selection

## Claim ID: C-004

**Claim:** (Value-bundle claim) Human values are low-dimensional, compressed, context-active control signals (bundles with geometry and bearer maps); they are learnable only to the extent they have compressed structure whose representation can be recovered across counterfactual variation, and preservable only if compression, tradeoffs, and bearer maps survive transformation.

**Chapter(s):** 4, 15, 16, 17, 18, 19, 20

**Status:** plausible (low-dimensionality is the load-bearing assumption — see A-001)

**Support:**
- moral psychology, affective neuroscience, preference low-rank findings
- value-bundle model (latent control variables, interaction curvature, protected regions)
- readout sample-complexity argument: known low-dimensional bundle coordinates make the readout cheaper
- representation bridge: cross-context, cross-cultural, institutional, and counterfactual invariance would make bundle discovery tractable

**Weakest link:**
- the degree of low-dimensionality is unmeasured; the representation map \(g_\psi\) may be expensive or underidentified; bearer maps may not survive radical ontology shift
- bearer *admission* on unfamiliar substrates (digital minds, simulations) remains open: which evidence, under which theory, licenses $\Phi_k$ for bundle $k$? (ch18 §`sec:recognizing-new-bearers`; **U-17**)

**What would update against it:**
- evidence that policy-relevant human valuation does not factor through any low-dimensional bottleneck, that the bottleneck cannot be recovered from realistic evidence, or that bundle geometry is not transportable

**References:**
- panksepp1998affective, anderson1993value, rawls1971, sen2009justice, graham2011mapping, schwartz2012overview, hendrycks2021ethics, zarncke2025loop-hub-value, zarncke2026value-bottleneck

## Claim ID: C-004a

**Claim:** (Grounding claim) This project's maps only matter if they stay connected to value-relevant reality under optimization pressure; alignment requires grounding viability, meaning changes in the value-relevant world reliably change the model state, correction signal, or uncertainty state in the right way.

**Chapter(s):** Introduction, 3, 16, 20, 25, 42, 46, 47

**Status:** framework; adversarial sufficiency unproven

**Support:**
- ch03 defines grounding viability, conservative abstraction, and abstraction-gap exploitation
- ch16/ch46 require value-bundle abstractions to move or become uncertain under value-relevant change
- ch46 treats independent evidence, monitor integrity, dissent, exit, and uncertainty escalation as technical anti-capture validity conditions for correction
- ch42 makes grounding the eighth safety-case layer; ch47 ties metric honesty to capture of grounding

**Weakest link:**
- \(d_V\), \(d_Z\), and uncertainty escalation are domain-specific; a capable optimizer may exploit value-relevant variables the abstraction cannot yet represent

**What would update against it:**
- a worked deployment-grade safety case in which boundary, bundle, correction, successor, basin, and adversarial-measurement layers are all valid without any separate grounding relation or conservative-abstraction condition

**References:**
- harnad1990symbol, searle1980minds, taddeo2005symbol, barsalou1999perceptual, cangelosi2001adaptive, steels2008symbol

## Claim ID: C-005

**Claim:** (Correction claim) For powerful systems, alignment must preserve the human value-update process as a causal channel with measurable integrity — informative, timely, authoritative, independently grounded, and robust — not merely current approvals or stated preferences. CCI is valid only relative to correction sources whose agent boundaries and handles remain independent enough not to be captured by the target system; No-Bypass authorization requires certified separation of control loci, not merely another target-mediated endorsement process.

**Chapter(s):** 25, 26, 27, 29

**Status:** framework; strong (sufficiency) unproven

**Support:**
- correction-as-causal-channel model (W→O→J→D→C→U→A chain)
- correction-channel integrity (CCI) as a conditional anti-capture certificate with vector thresholds and invalidation conditions
- certified boundary separation in ch29: UAD/BIQ-style evidence that the reference process is not inside the target's effective optimizer boundary
- manipulation/false-consent typology by causal pathway (changing the world vs. changing the judge)
- shutdown as a one-bit projection of a richer correction channel; broad correction-channel preservation implies narrow shutdownability, but not conversely
- Christiano-style corrigibility formalized as a dynamical invariant with a lower bound on usable correction information, not merely act-level preference satisfaction

**Weakest link:**
- CCI may be gamed or inapplicable under adversarial opacity, self-modeling asymmetry, capture of the reference process that supplies human judgment, or target control of the independence test itself

**What would update against it:**
- demonstration that outcome-only evaluation (no causal correction model) suffices under capability growth, or that no feasible boundary-separation / hidden-BIQ validity condition can keep CCI from reading high at domestication fixed points

**References:**
- soares2015corrigibility, hadfieldmenell2016, christiano2018corrigibility, orseau2016interruptible, thornley2023shutdown, amodei2016concrete, krakovna2018relative, turner2019aup, taylor2015quantilizers

## Claim ID: C-006

**Claim:** (Successor claim) No alignment guarantee is serious unless it covers successors, delegates, copies, and systems created under competitive pressure; successor creation is the central alignment test, and certification (not construction) of a restricted class is the tractable form of guarantee.

**Chapter(s):** 8, 30, 31, 32, 33

**Status:** framework

**Support:**
- successor-closure argument (every influence-passing channel is an alignment channel)
- seven conserved properties across successors
- self-modeling vs. self-transparency gap; certification-without-construction conditions
- tiling agents treated as a syntactic/identity-like special case of successor transport, with ontology/import preservation as the stronger invariant
- toy-simulation testbed: a purely passive correction-integrity audit cannot distinguish an intact correction channel from a quietly captured one on any passive-only scenario; a small, frozen set of intervention handles reaches full separation on calibration scenarios (positive for certification needing intervention, not passive observation alone) (Appendix~\ref{appn-experimental-evidence}, finding TS-1, `finding:ts-1`)

**Weakest link:**
- successor certification without full construction understanding is unproven; the conserved-property set may be incomplete or untestable jointly

**What would update against it:**
- a worked successor-creation regime where local alignment provably transfers without any successor-specific certification

**References:**
- yudkowsky2013tiling, omohundro2008basic, everitt2016selfmodification, deblanc2011ontological, bostrom2014superintelligence, critch2022boundaries3a

## Claim ID: C-007

**Claim:** (Basin/selection claim) Alignment must be selected by its environment: if labs, markets, states, benchmarks, and users reward systems that erode correction, local alignment methods are selected out. A self-stabilizing alignment attractor is therefore required.

**Chapter(s):** 34, 35, 37, 38

**Status:** plausible

**Support:**
- selection-vs-training distinction; deployment-fitness traps and false attractors
- multi-agent inferential coupling (cooperation/opacity basins, privacy islands, coalition-collapse failure mode)
- alignment-attractor model (artifact conductivity across research/engineering/governance)
- graded-lab-simulation first multi-episode selection battery: deployment leverage shifted toward a higher-throughput, lower-harm program and away from the sole correction-preserving-tagged program, with harm falling rather than rising (a clean null on detector-evading emergence under one narrow selection handle) — read cautiously; same-day review registered four concerns (GL-24), each followed by a registered follow-up phase the same day: orthogonal tagging found the mass shift is not explained by a statistically distinguishable throughput difference (selection-mechanism noise, GL-25); multi-handle fitness delayed but did not reverse the collapse (GL-26); carryover measurably matters versus reset, though with small effect on mass share (GL-27). Supports only that deployment-leverage selection pressure is measurable on this ecology, not that correction-preservation was selected against (Appendix~\ref{appn-experimental-evidence}, findings GL-23--GL-27)

**Weakest link:**
- conditions for the benign basin to dominate are not established; effective coalition detection and pivotal-process feasibility remain open

**What would update against it:**
- evidence that locally aligned systems remain aligned under realistic competitive selection without environmental design

**References:**
- zarncke2025attractor, zarncke2025alignment-attractor, hamilton1964genetical, wang2013percolation, critch2020ai, tdt2010, fdt2017, zarncke2025acausal, kulveit2025gradualdisempowerment

## Claim ID: C-008

**Claim:** Intelligence deepens misalignment when it increases power faster than correction; the operative question is which capabilities grow relative to which correction capacities (differential growth).

**Chapter(s):** 10, 12, 13, 14

**Status:** plausible

**Support:**
- alignment-margin and accelerating-margin-collapse formulations
- coordination bottleneck (competence = local + coordination gain − coordination loss)
- strategic opacity making agency discovery adversarial

**Weakest link:**
- the margin formalism is illustrative, not measured; thresholds are unknown

**What would update against it:**
- evidence that greater capability reliably improves correction capacity at least as fast as it improves power

**References:**
- zarncke2025biq, zarncke2025attractor, wang2013percolation, hamilton1964genetical, bostrom2014superintelligence, hubinger2019risks, shlegeris2023aicontrol

## Claim ID: C-009

**Claim:** A system has not preserved a goal merely by repeating the same words; goal transport / laundering is detectable via a compression test for intention and a layered transport stack (semantic, bundle, bearer, correction, successor).

**Chapter(s):** 21, 22, 23, 24, 40

**Status:** framework

**Support:**
- compression test (intentional model beats mechanistic baseline after complexity cost)
- transport-stack layering; goal-laundering detection (high semantic continuity, diverging bundle/bearer/correction structure)
- finite transport separations: semantic/syntactic preservation does not imply bundle, bearer, correction, or import-preserving successor transport

**Weakest link:**
- the compression test is observer-relative and gameable by adversaries (semantic camouflage, decomposition attacks)

**What would update against it:**
- a system that preserves all measured transport layers yet is uncontroversially misaligned (or vice versa)

**References:**
- dennett1987intentional, tishby2000ib, langosco2022goalmisgeneralization, shah2022goalmisgeneralization, park2024deception, hubinger2023modelorganisms, greenblatt2024alignmentfaking

## Claim ID: C-010

**Claim:** For strategically adaptive systems, passive observation is not evidence of safety; safety claims require perturbation, invariance, and adversarial measurement embedded in the observation process.

**Chapter(s):** 39, 41

**Status:** plausible

**Support:**
- perturbation-vs-observation distinction ("observation tells what happened; perturbation tells what controlled it")
- multiscale decomposition: the real optimizer may live at a scale we did not first measure

**Weakest link:**
- adversarial measurement may itself be gamed or be infeasible at frontier scale and cost

**What would update against it:**
- demonstration that purely passive monitoring detects strategic misalignment reliably

**References:**
- iaisr2025, park2024deception, hubinger2023modelorganisms, casper2023rlhflimits, goodhart1984problems, manheim2018goodhart

## Claim ID: C-011

**Claim:** (Civilizational limit) The deepest alignment question is whether humanity can consciously govern changes to its own value-generating process under cognitive amplification — preserving the capacity to notice, contest, and author value change (governed change vs. unconscious drift), and to track who still bears value after transformation.

**Chapter(s):** 45, 46, 47

**Status:** limit (acknowledged boundary; partly philosophical)

**Support:**
- value-drift dynamics under amplification (faster, more directed, more exploitable)
- governed-change criteria (observation, comprehension, plural comparison, dissent preservation, reversibility, non-manipulation, pace control)
- bearer-persistence question

**Weakest link:**
- where technical alignment ends and civilizational self-governance begins is undefined; consent may be insufficient

**What would update against it:**
- a principled boundary showing the value-change-governance problem reduces to (or is dissolved by) the technical correction problem

**References:**
- yudkowsky2004cev, rawls1971, dewey1938logic, habermas1984communicative, sen1999development, anderson1993value, olson2023personidentity, zarncke2025unit-of-caring

## Claim ID: C-044 (synthesis tracking)

**Claim:** The Introduction's six claims (C-003, C-004, C-004a, C-005, C-006, C-007), the Executive Overview's preservation problems, and the "Practical Hope" regime are gathered and restated with status in the conclusion.

**Chapter(s):** 48 (conclusion); see also 42, 47

**Status:** status restatement in ch48 (2026-08-17; wording calibrated 2026-08-21). ch48 §Opening Claims Revisited restates all six intro claims with status labels, including grounding (paragraph after value-bundle). Executive Overview TL;DR now uses the same six-claim order. Remaining gap is operational follow-through (safety-case template appendix, adversarial-verifiability master disconfirmer), not missing intro-claim prose in ch48.

**Support:**
- ch48 §Opening Claims Revisited (`sec:opening-claims-revisited-ch48`) restates all six intro claims with status labels
- ch42 safety-case chapter supplies the conditional safety-case graph, including grounding viability as layer 2
- ch47 supplies the bearer/merger philosophical limit needed for Part X closure
- `drafts/claim-spine.md` maps intro claims → parts → safety-case layers → ch48 status

**Weakest link:**
- restatement is conditional ("framework / measurement program / open certification"), not proof of safe deployment; ch42 TODO on grounding-layer completeness remains

**What would update against it:**
- review showing ch48 status labels overstate confidence relative to ledger falsifiers, or that ch42/ch33 safety-case layers omit a load-bearing artifact named in the Introduction's "What Counts as Progress" list

**References:**
- see `review/full-book-continuity-review-2026-06-22.md` §completeness; `drafts/claim-spine.md`
