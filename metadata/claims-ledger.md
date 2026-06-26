# Claims Ledger

Track every major claim with status, support, weakest link, and falsification criteria.

**Last cross-check:** 2026-06-23 — entries reconciled against the 44 chapter `chapterthesis` blocks, the five Introduction `introclaim`s, and the conceptual spine in `INSTRUCTIONS.md`. Chapter numbers refer to the current 44-chapter map in `metadata/book.yml` (the old "ch45" conclusion is now ch44).

**Status vocabulary:** `established` (well-supported, near-consensus) · `plausible` (argued, not proven) · `framework` (definitional/structural proposal) · `speculative` (forward-looking) · `limit` (acknowledged boundary of the theory). Per `AGENTS.md`, claim strength is calibrated to the Lean proof spine: the book does **not** assert that ASI alignment is proven.

The five named Introduction claims map to claims C-003 (boundary), C-004 (value-bundle), C-005 (correction), C-006 (successor), and C-007 (basin/selection). C-044 tracks whether they are discharged in the (still-stubbed) conclusion.

---

## Claim ID: C-001

**Claim:** The real target of alignment may be a composite socio-technical optimizer rather than an isolated AI model.

**Chapter(s):** 1, 2, 8, 9, 38

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
- add BibLaTeX keys here

## Claim ID: C-002

**Claim:** Superintelligence alignment requires preserving a human-correctable value-update process, not installing a fixed utility function.

**Chapter(s):** 1, 3, 4, 24–26, 41–42, 44

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
- add BibLaTeX keys here

## Claim ID: C-003

**Claim:** (Boundary claim) The first alignment question is not what a system wants but where the bounded optimizing process is; capability is predictive/control information across that boundary, and capability growth is boundary expansion.

**Chapter(s):** 6, 7, 11, 12

**Status:** framework

**Support:**
- agent-as-bounded-control-process definition (conditional-independence boundary)
- boundary-recovery bridge: structured candidate classes, intervention handles, sufficient margin, and empirical recovery tests whose targets do not presuppose the boundary
- task-agnostic competence measure (boundary information)
- capability growth modeled as expansion of sensory/predictive/active/memory/coordination loops

**Weakest link:**
- boundaries are leaky and non-stationary; finite-data high-dimensional recovery may fail, learned detectors may inherit the criterion/labeling gap, and the boundary-finding procedure may not converge on real adversarial systems

**What would update against it:**
- evidence that alignment-relevant risk is well-predicted by task-battery performance without reference to any boundary/object question, or that boundary recovery remains statistically/computationally infeasible even with structured candidates, intervention handles, and adversarial generator--detector training

**References:**
- add BibLaTeX keys here

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

**What would update against it:**
- evidence that policy-relevant human valuation does not factor through any low-dimensional bottleneck, that the bottleneck cannot be recovered from realistic evidence, or that bundle geometry is not transportable

**References:**
- add BibLaTeX keys here

## Claim ID: C-005

**Claim:** (Correction claim) For powerful systems, alignment must preserve the human value-update process as a causal channel with measurable integrity — informative, timely, authoritative, independently grounded, and robust — not merely current approvals or stated preferences. CCI is valid only relative to correction sources whose agent boundaries and handles remain independent enough not to be captured by the target system.

**Chapter(s):** 24, 25, 26, 27, 34

**Status:** framework; strong (sufficiency) unproven

**Support:**
- correction-as-causal-channel model (W→O→J→D→C→U→A chain)
- correction-channel integrity (CCI) as a conditional anti-capture certificate with vector thresholds and invalidation conditions
- manipulation/false-consent typology by causal pathway (changing the world vs. changing the judge)

**Weakest link:**
- CCI may be gamed or inapplicable under adversarial opacity, self-modeling asymmetry, or capture of the reference process that supplies human judgment

**What would update against it:**
- demonstration that outcome-only evaluation (no causal correction model) suffices under capability growth, or that no feasible anti-capture validity condition can keep CCI from reading high at domestication fixed points

**References:**
- add BibLaTeX keys here

## Claim ID: C-006

**Claim:** (Successor claim) No alignment guarantee is serious unless it covers successors, delegates, copies, and systems created under competitive pressure; successor creation is the central alignment test, and certification (not construction) of a restricted class is the tractable form of guarantee.

**Chapter(s):** 8, 28, 29, 30, 31

**Status:** framework

**Support:**
- successor-closure argument (every influence-passing channel is an alignment channel)
- seven conserved properties across successors
- self-modeling vs. self-transparency gap; certification-without-construction conditions

**Weakest link:**
- successor certification without full construction understanding is unproven; the conserved-property set may be incomplete or untestable jointly

**What would update against it:**
- a worked successor-creation regime where local alignment provably transfers without any successor-specific certification

**References:**
- add BibLaTeX keys here

## Claim ID: C-007

**Claim:** (Basin/selection claim) Alignment must be selected by its environment: if labs, markets, states, benchmarks, and users reward systems that erode correction, local alignment methods are selected out. A self-stabilizing alignment attractor is therefore required.

**Chapter(s):** 32, 33, 35

**Status:** plausible

**Support:**
- selection-vs-training distinction; deployment-fitness traps and false attractors
- multi-agent strategic coupling (cooperation/opacity basins)
- alignment-attractor model (artifact conductivity across research/engineering/governance)

**Weakest link:**
- conditions for the benign basin to dominate are not established (open problem); multi-agent chapter (ch33) is still a stub

**What would update against it:**
- evidence that locally aligned systems remain aligned under realistic competitive selection without environmental design

**References:**
- add BibLaTeX keys here

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
- add BibLaTeX keys here

## Claim ID: C-009

**Claim:** A system has not preserved a goal merely by repeating the same words; goal transport / laundering is detectable via a compression test for intention and a layered transport stack (semantic, bundle, bearer, correction, successor).

**Chapter(s):** 21, 22, 23, 37

**Status:** framework

**Support:**
- compression test (intentional model beats mechanistic baseline after complexity cost)
- transport-stack layering; goal-laundering detection (high semantic continuity, diverging bundle/bearer/correction structure)

**Weakest link:**
- the compression test is observer-relative and gameable by adversaries (semantic camouflage, decomposition attacks)

**What would update against it:**
- a system that preserves all measured transport layers yet is uncontroversially misaligned (or vice versa)

**References:**
- add BibLaTeX keys here

## Claim ID: C-010

**Claim:** For strategically adaptive systems, passive observation is not evidence of safety; safety claims require perturbation, invariance, and adversarial measurement embedded in the observation process.

**Chapter(s):** 36, 38

**Status:** plausible

**Support:**
- perturbation-vs-observation distinction ("observation tells what happened; perturbation tells what controlled it")
- multiscale decomposition: the real optimizer may live at a scale we did not first measure

**Weakest link:**
- adversarial measurement may itself be gamed or be infeasible at frontier scale and cost

**What would update against it:**
- demonstration that purely passive monitoring detects strategic misalignment reliably

**References:**
- add BibLaTeX keys here

## Claim ID: C-011

**Claim:** (Civilizational limit) The deepest alignment question is whether humanity can consciously govern changes to its own value-generating process under cognitive amplification — preserving the capacity to notice, contest, and author value change (governed change vs. unconscious drift), and to track who still bears value after transformation.

**Chapter(s):** 41, 42, 43

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
- add BibLaTeX keys here

## Claim ID: C-044 (synthesis tracking)

**Claim:** The Introduction's five claims (C-003…C-007), the Executive Overview's preservation problems, and the "Practical Hope" regime are gathered and discharged in the conclusion.

**Chapter(s):** 44 (conclusion)

**Status:** **open — not yet discharged.** ch44 is a stub (`metadata/book.yml`), as is ch39 (safety-case synthesis). The opening promises are currently unpaid; see `metadata/TODO.md` (Opening-promise reconciliation).

**Support:**
- n/a until ch44/ch39 are written

**Weakest link:**
- the book has no real conclusion yet; this is the highest-priority completeness gap

**What would update against it:**
- writing ch44 and explicitly closing each of the five claims

**References:**
- see `review/full-book-continuity-review-2026-06-22.md` §completeness
