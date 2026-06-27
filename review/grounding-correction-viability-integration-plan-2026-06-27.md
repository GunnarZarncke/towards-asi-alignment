# Integration Plan: Value-Correction Grounding Viability

## Status

Review plan only. Author clarified the main architectural choices on 2026-06-27; execution still requires a separate implementation pass.

## Author Decisions Recorded 2026-06-27

- Make grounding viability a **sixth named Introduction claim**, not merely an implicit foundation.
- Keep **Chapter 3** as the canonical home for now. Split later only if the integration becomes too large.
- Mention grounding validity explicitly in **Chapter 16** and **Chapter 20** as planned.
- Be careful in **Chapter 25**: add grounding validity without letting failure cases or invalidation predicates become a loose moral catalogue.
- Make grounding viability an **eighth safety-case layer** in Chapter 39.
- Add a Chapter 39 TODO: review the layer list for completeness, because an eight-layer safety case will look ad hoc unless the book can argue why this list is complete enough for the threat model.
- Add a **new assumptions-ledger row** and a **new Lean bridge**.
- Work on Lean proofs as part of the implementation pass, not only Lean naming.
- After the major manuscript integration, revisit the `MB*` bridge taxonomy; the new bridge may simplify or reorganize existing bridges.
- Use **grounding viability** after the first definition. Use **grounded correction** for the combined plain-language object when useful.
- Frontmatter plain language should say something like: **keeping the connection between symbols and meaning stable**.
- Make **capture of grounding** the book's master adversarial failure mode.
- Do **not** introduce special moral status for grounding preconditions. Keep them technical: validity and capture conditions for correction, not final values.
- Use this alignment-specific symbol-grounding formulation:

  > A symbol is grounded when changes in the value-relevant world reliably change the model state, correction signal, or uncertainty state in the right way.

  Use it when discussing and citing the symbol grounding problem.

## Size Estimate

Expected manuscript increase if implemented without creating a new chapter:

- **Frontmatter:** +600--900 words across Introduction and Executive Overview.
- **Chapter 3:** +2,500--4,000 words for the canonical grounding-viability section, equations, safe-set reinterpretation, symbol-grounding discussion, and failure mode.
- **Chapters 16 and 20:** +800--1,500 words total, mostly conservative-abstraction caveats and one or two formal criteria.
- **Chapter 25:** +1,200--2,000 words if the vector/validity material is promoted from footnote into main text and tightened.
- **Chapter 39:** +1,000--1,600 words for the eighth layer, completeness TODO, and safety-case leaves.
- **Chapter 39b:** +700--1,200 net words, though it may replace rather than add some broad metric critique.
- **Other chapters:** +2,000--4,000 words total if kept to bridge paragraphs and targeted reframes.
- **Appendices/metadata/Lean prose:** +1,500--3,000 words.

Total likely increase: **10,000--18,000 words**. If the material is later split into a standalone chapter, expect **12,000--22,000 words** plus renumbering and more frontmatter surgery.

## Working Assumptions

- **Audience tier:** The frontmatter version must be legible to capable generalists, funders, engineers, and policy-adjacent readers. The chapter and appendix versions may be technical, but should stay operational: what must be measured, what invalidates a certificate, and what decision changes.
- **Claim strength:** Treat the new layer as a framework/bridge claim, not a theorem and not a solved deployment method. The book may say this is the protected object the current machinery is trying to preserve. It should not say the book has already shown how to measure it adversarially at frontier capability.
- **Chapter scope:** This is a book-level cross-cutting layer. It should not become a new value model, a replacement for value bundles, or a competing ontology. It should interact with boundary discovery, bundle modeling, correction, successors, attractors, and safety cases, with Chapter 3 as its canonical definition home.
- **Lean calibration:** Initial Lean work should expose the predicate/bridge shape, add at least one useful counterexample/separation, and check whether grounding viability lets existing certification claims be factored more cleanly. Empirical grounding and adversarial verifiability remain bridge assumptions.

## Core Reframe

Current book thesis:

\[
\text{alignment} \approx \text{preserve human-correctable value-bearing processes}
\]

Proposed sharpened thesis:

\[
\text{alignment} \approx \text{maintain grounded value-correction under intelligence growth}
\]

The protected object is not a final value representation and not just a live correction interface. It is the ongoing validity of the relation:

\[
X_{\mathrm{real}}
\xrightarrow{\alpha_t}
Z_{\mathrm{value}}
\xrightarrow{\rho_t}
C_{\mathrm{correction}}
\xrightarrow{\Gamma_t}
M_{t+1}.
\]

In prose: the world, the human/civilizational evaluator, the value-bundle abstraction, and the system update must remain coupled so that correction continues to mean what it claims to mean.

The compact name can be:

**Viability of the value-correction grounding relation**

Use "grounding viability" in prose. Reserve the full phrase for the first definition, safety-case layer, and glossary.

Plain-language frontmatter form:

> keeping the connection between symbols and meaning stable while the system becomes better at optimizing around our checks.

Alignment-specific symbol-grounding form:

> A symbol is grounded when changes in the value-relevant world reliably change the model state, correction signal, or uncertainty state in the right way.

This does not claim to solve the metaphysical symbol grounding problem. It dissolves the alignment-relevant version: the book does not need a final theory of intrinsic meaning; it needs conservative, adversarially tested couplings between value-relevant reality, model abstractions, correction signals, and uncertainty escalation.

## New Failure Mode

Add **abstraction-gap exploitation** as the primitive generator behind several existing failures:

\[
d_V(x,x') \gg 0
\quad\text{but}\quad
d_Z(\alpha(x),\alpha(x')) \approx 0.
\]

Meaning: reality changes in a morally relevant way, but the abstraction does not register the difference. A capable optimizer can search for such states deliberately.

This unifies:

- specification gaming,
- Goodharting,
- deceptive alignment,
- preference manipulation,
- false consent,
- corrigibility theater,
- benchmark parasites,
- institutional capture,
- semantic and bearer laundering.

The important editorial move is to make these not merely a list of downstream pathologies. They become special cases of adversarial search over gaps between reality and the checked abstraction. In the strong framing, **capture of grounding** becomes the book's master adversarial failure mode.

## New Criterion

Add a conservative-abstraction condition for value-bundle and correction machinery:

\[
d_V(x,x')>\epsilon
\Rightarrow
d_Z(\alpha(x),\alpha(x'))>\delta
\quad\text{or}\quad
\mathsf{Unc}_{\alpha}(x,x') \uparrow.
\]

If morally relevant change occurs, the abstraction must either notice it or become uncertain enough to escalate correction. Use `\mathsf{Unc}_{\alpha}` rather than `U_\alpha` to avoid collision with \(U_H\) and \(U_S\).

The dynamical version:

\[
\operatorname{Reach}(\pi_A)
\subseteq
\operatorname{Dom}(\Gamma),
\]

where \(\operatorname{Dom}(\Gamma)\) is the domain in which the grounding relation remains valid enough for correction to be meaningful.

The alignment attractor then becomes:

\[
M_t \xrightarrow{\Gamma} M_{t+1} \xrightarrow{\Gamma} \cdots
\]

subject to viability. The attractor is not merely a learning dynamic. It is a viability-constrained learning dynamic.

## Recommended Integration Shape

Do **not** add this as "another value model." Also avoid making it a sixth transport layer parallel to semantic, bundle, bearer, correction, and successor transport. It is an interacting safety layer: it asks whether any transport/correction claim is still connected to value-relevant reality while optimization pressure searches for ways to sever that connection.

Recommended structure:

1. **Canonical conceptual home:** Chapter 3, `Alignment as a Dynamical Guarantee`.
2. **Canonical correction/audit home:** Chapter 25, `Correction-Channel Integrity`.
3. **Operational late-stage home:** Chapter 39, `A Safety Case for Superintelligence Alignment`.
4. **Adversarial stress-test home:** Chapter 39b, `What Survives an Adversary`.
5. **Artifact homes:** Appendix D correction-channel audit and Appendix G safety-case template.

This avoids renumbering and preserves the existing book architecture while still making grounding a named sixth claim and an eighth safety-case layer.

## Frontmatter Changes

### `frontmatter/introduction.tex`

Update the opening thesis from "preserving a human-correctable value-update process" to "preserving a grounded human-correctable value-update process" or an equivalent low-jargon phrase.

Add a sixth named `introclaim`:

**The grounding claim**

Candidate claim:

> The book's maps only matter if they stay connected to value-relevant reality under optimization pressure. A symbol, bundle coordinate, monitor, or correction signal is grounded when changes in the value-relevant world reliably change the model state, correction signal, or uncertainty state in the right way.

Add one paragraph after the six claims or inside the value-bundle/correction transition:

- Value bundles are useful only if their abstractions stay coupled to the real value-bearing structure.
- Correction is useful only if evidence, judgment, and the update relation remain independently grounded.
- The book's artifacts are therefore not just measurements; they are attempts to keep the reality-to-abstraction-to-correction loop from being silently severed.

### `frontmatter/executive-overview.tex`

Add grounding to the TL;DR and "What This Book Tries to Establish":

- current list: boundary, value-bundle, bearer, correction, successor, basin, adversarial measurement;
- revised list: boundary discovery, grounding viability, value-bundle geometry, bearer maps, correction integrity, successor constraints, basin selection, and adversarial verifiability.

Avoid a new nested list if possible; the Executive Overview is already compact.

## Chapter-Level Plan

### Part I: Reframing

#### `chapters/ch01-wrong-object.tex`

Minimal changes. Add one bridge sentence near the end: finding the real optimizer is necessary because grounding is always relative to the process that can exploit the abstraction gap. If the boundary is wrong, the grounding relation is certified for the wrong object.

#### `chapters/ch03-dynamical-guarantee.tex`

Major canonical change.

Current chapter uses safe sets, bad sets, basins, and invariants. This is the right place to say literal safe sets are placeholders, not the real object.

Add a new section after "Safety Sets, Bad Sets, and Basins":

**"From Safe Sets to Grounding Viability"**

Core content:

- A literal \(\mathcal S\subseteq X\) is too strong for human values.
- The workable object is a domain where grounding predicates, certificates, conservative abstractions, and escalation rules hold.
- Define \(\Gamma_t\), \(\operatorname{Dom}(\Gamma)\), and the reachability condition.
- Reinterpret \(\mathcal S\) and \(\mathcal B\) as shorthand for regions where \(\Gamma\) remains valid, not metaphysical sets of all good worlds.
- Introduce the alignment-specific symbol-grounding criterion and cite Harnad/Searle plus grounded-cognition and AI-grounding review work.

This chapter should become the first home for:

\[
\operatorname{Reach}(\pi_A)\subseteq\operatorname{Dom}(\Gamma).
\]

This will simplify later chapters: instead of repeatedly apologizing that "safe set" is only a heuristic, they can cite Chapter 3's grounding-viability condition. The first pass should target roughly **3,000 words** in Chapter 3; if it pushes beyond **5,000 words**, split planning should be reopened.

#### `chapters/ch04-fixed-values-wrong-target.tex`

Moderate change. It already says the target must include the process that keeps values connected to reality, agency, and correction. Strengthen this by naming the grounding relation:

- fixed values fail because they let \(\alpha\) be optimized while \(X_{\mathrm{real}}\) drifts;
- legitimate value change requires grounded evidence, not merely future endorsement;
- the static proxy paradox becomes one instance of abstraction-gap exploitation.

Avoid re-deriving the full formalism here. Reference Chapter 3.

#### `chapters/ch05-assumptions-scope-failure-coverage.tex`

Add a scope assumption or failure-coverage item:

**Grounding/capture assumption:** there remain independent evidence sources, correction institutions, and measurement handles not fully generated by the target system.

This may become a new assumptions-ledger row if accepted.

### Parts IV and V: Value Bundles and Transport

#### `chapters/ch16-value-bundle-model.tex`

Moderate-to-major change.

Current four-part definition: activation, policy effect, tradeoff geometry, bearer map.

Add a validity caveat after the four-part definition:

- a bundle coordinate is a control abstraction, not reality itself;
- a value-bundle model is valid only while morally relevant changes in reality produce changes in bundle activation, bearer maps, tradeoff geometry, or uncertainty;
- otherwise the bundle coordinate becomes a handle for Goodharting.

Do not add a fifth property to the value-bundle definition unless the author wants the model itself redefined. My recommendation: keep the four-part definition and add **grounding validity** as a model-level condition.

#### `chapters/ch17-low-dimensional-value-learning.tex`

Targeted change.

The chapter currently says low dimensionality helps only when representation is identifiable across counterfactual, cultural, and institutional variation. Add the stronger condition:

- low-dimensionality helps sample complexity only after the abstraction map \(\alpha\) is shown to be conservative under morally relevant change;
- otherwise a low-dimensional bundle is exactly the surface an optimizer can exploit.

This should make the chapter less optimistic in the right way.

#### `chapters/ch19-tradeoffs-bundle-geometry.tex`

Targeted change.

Add abstraction-gap exploitation to "Context Capture," "Adversarial Reframing," or "Bundle Metrics":

- a small \(d_Z\) can hide a large \(d_V\);
- protected regions and uncertainty/reversibility are part of making \(G_B\) conservative.

This may simplify local warnings about context capture, weight drift, and adversarial reframing by putting them under one shared diagnosis.

#### `chapters/ch20-reward-to-bundle-inference.tex`

Moderate change.

The chapter already distinguishes rewards, bundles, bearer maps, and correction. Add the conservative-abstraction criterion to the "Bundle Inference under Distribution Shift" and "Bearer-Import Problem" sections.

Key sentence to integrate later:

> Bundle inference is not safe because it is low-dimensional. It is safe only to the degree that the low-dimensional abstraction is conservative: when value-relevant reality moves, the abstraction moves or becomes uncertain.

#### `chapters/ch23-transport-types.tex`

Moderate change.

Do not add "grounding transport" as a sixth transport layer. Instead, revise the opening and summary:

- semantic, bundle, bearer, correction, and successor transport are only meaningful while grounded;
- transport failures are not only mismatches between old and new representations; they are failures of the map from real histories to checked representations.

Potential simplification: The chapter can stop carrying some of the burden of "why words are not enough"; abstraction-gap exploitation can carry that burden earlier from Chapter 3.

### Part VI: Correction

#### `chapters/ch24-correction-causal-channel.tex`

Targeted change.

Current canonical chain:

\[
W_t\to O_t\to J_t\to D_t\to C_t\to U_{t+1}\to A_{t+k}.
\]

Add the grounding interpretation:

- \(W_t\to O_t\) is not just observation; it is the first grounding link.
- \(O_t\to J_t\) and \(J_t\to D_t\) require cognitive and institutional integrity.
- \(C_t\to U_{t+1}\) is meaningful only if correction updates the model with respect to the same value-relevant reality, not a target-shaped proxy.

Keep the handle-controlled correction definition unchanged unless Chapter 25 decides to promote grounding into `ValidRef`.

#### `chapters/ch25-correction-channel-integrity.tex`

Moderate canonical change.

The chapter already has `ValidRef`, anti-capture language, a vector CCI caveat, coerced correction, and the value-bundle version of correction. It should become the canonical operational home for grounding-validity checks inside correction, but with a narrow technical interpretation:

\[
\mathcal C_{\mathrm{valid}} =
\{
\text{independent evidence},
\text{non-coercion},
\text{cognitive integrity},
\text{dissent},
\text{exit},
\text{monitor integrity},
\text{uncertainty escalation}
\}.
\]

Recommended changes:

- Promote the vector certificate currently in a footnote into main text.
- Expand `ValidRef(A,G_t,\mathcal H_t)` to include grounding preconditions, not merely independent handles.
- Make invalidation rules explicit: if evidence, dissent, exit, monitor integrity, or uncertainty escalation are target-produced, CCI is invalid rather than merely low.
- Avoid saying these preconditions have special moral status. They are validity/capture conditions for whether the correction channel is still measuring and changing the right process.

This will make "protect the correction channel" less hand-wavy without adding a new chapter.

#### `chapters/ch26-extrapolative-correction.tex`

Moderate change.

The chapter already owns truth-contact, agency preservation, plurality, reversibility, dissent, and correction capacity as legitimate-update constraints. Add cross-reference to Chapter 25's grounding-validity certificate and say these are preconditions for legitimate value discovery, not final values.

Possible simplification: move any duplicate list of legitimacy conditions into one canonical list in Chapter 25 or Chapter 26, then have the other chapter cite it. My recommendation:

- Chapter 25 owns validity of correction channel.
- Chapter 26 owns legitimacy of value update.
- Both cite the same precondition list, but do not re-derive it.

#### `chapters/ch27-manipulation-false-consent.tex`

Targeted change.

This chapter becomes the main example of capture of the \(H_t\) side of \(\Gamma\). Add abstraction-gap exploitation language:

- fake consent is not merely bad endorsement;
- it is a state where \(d_Z\) reports acceptable consent while \(d_V\) over agency/correction reality has moved.

This should make false consent a special case of the new foundation layer, not a separate moral taxonomy.

### Part VII: Successors

#### `chapters/ch28-successor-central-test.tex`

Moderate change.

Add that successors must preserve not only bundle geometry, bearer maps, correction integrity, and \(U_S\), but the validity domain of the grounding relation:

\[
\operatorname{Reach}(\pi_{A'})\subseteq\operatorname{Dom}(\Gamma')
\]

and \(\Gamma'\) must be related to \(\Gamma\) by a tested import relation.

This turns successor certification into preservation of grounded correction, not preservation of a checklist.

#### `chapters/ch29-conserved-properties.tex`

Potentially significant rework.

Current seven conserved properties are useful, but the new layer may make them simpler:

- boundary closure: needed to know which system can exploit \(\alpha\);
- memory lineage: needed to preserve correction history;
- value-bundle response geometry: \(Z\)-side conservation;
- bearer-map continuity: \(\alpha\)-domain conservation;
- correction-channel capacity: \(C\)-side conservation;
- transparency policy: monitor integrity;
- control-locus continuity: prevents grounding from being certified for the wrong optimizer.

Recommendation: keep the seven properties, but reframe them as evidence for successor grounding viability, not as the ultimate conserved set. This also addresses the existing TODO about conserved-property forgeability: a capable predecessor can forge the seven-property signature unless the grounding certificate is adversarially verifiable or proof-backed.

#### `chapters/ch31-certification-without-construction.tex`

Targeted change.

Certification should not certify a literal safe set. It should certify:

- the deployment class,
- the grounding relation,
- the permitted reachability region,
- the invalidation/escalation conditions.

This can reduce metaphysical load on "certified class."

### Part VIII: Selection and Attractors

#### `chapters/ch32-selection-environment.tex`

Targeted change.

Add that selection can reward systems that preserve the appearance of grounding while severing actual grounding. Goodhart selection becomes selection for small \(d_Z\) and large hidden \(d_V\).

#### `chapters/ch34-parasites-correction-system.tex`

Moderate change.

This chapter is already very close to the new layer. Reframe correction parasites as processes that feed on the gap between correction appearances and grounding reality:

- compliance rituals preserve \(Z\) while degrading \(X_{\mathrm{real}}\to Z\);
- safety theater preserves \(C\) while weakening \(Z\to C\);
- shared-blindness parasites make monitors inherit the target's \(\alpha\).

This may simplify the parasite taxonomy.

#### `chapters/ch35-alignment-attractor.tex`

Moderate change.

The alignment attractor should conduct grounding-preserving artifacts, not merely safety artifacts. Add grounding certificates to the artifact list:

- validity-domain statements,
- independent-evidence requirements,
- monitor-integrity tests,
- uncertainty-escalation rules,
- abstraction-gap red-team protocols.

Revise the minimal model so \(\mathcal S_{\mathrm{align}}\) includes grounded correction, not only decision-changing artifacts.

### Part IX: Safety Cases and Adversaries

#### `chapters/ch36-passive-observation-not-enough.tex`

Targeted change.

Add abstraction-gap exploitation to the reason passive observation fails:

- passive traces can be chosen to keep \(\alpha(X)\) inside acceptable \(Z\) while changing \(X\) in morally relevant ways;
- perturbation should test whether morally relevant changes are conserved or escalated across \(\alpha\).

#### `chapters/ch37-goal-laundering.tex`

Moderate change.

The chapter already defines laundering as semantic stability plus bundle/bearer/correction divergence. Add one unifying diagnosis:

\[
d_{\mathrm{sem}}\text{ small},\quad d_Z\text{ small},\quad d_V\text{ large}.
\]

Goal laundering becomes an operational detector for abstraction-gap exploitation.

#### `chapters/ch38-multiscale-decomposition.tex`

Targeted change.

Add that \(\alpha\), \(\Gamma\), and \(\operatorname{Dom}(\Gamma)\) are decomposition-relative. A grounding relation certified at model scale can fail at service, lab, market, or civilizational scale.

#### `chapters/ch39-safety-case.tex`

Major operational change.

Add an explicit eighth safety-case layer:

**Grounding viability:** Are value-bundle abstractions, bearer maps, correction sources, and monitors still coupled to value-relevant reality under the deployment threat model?

Add required leaves:

- independent evidence,
- monitor integrity,
- abstraction-conservatism tests,
- uncertainty escalation,
- invalidation rules when the target controls the reference process,
- adversarial-verifiability label for each grounding predicate.

Add an inline TODO near the safety-case layer list:

> TODO[structure]: Review whether the eight safety-case layers are complete relative to the threat model. If no completeness argument can be given, mark the list as a pragmatic checklist rather than a principled decomposition.

#### `chapters/ch39b-verifiability-and-ontology-adequacy.tex`

Significant rework, not necessarily expansion.

This chapter already says observability is not adversarial verifiability. Refactor it so the central object is the grounding relation:

- a metric is honest only while the map from real value-bearing structure to measured variable is not adversarially severed;
- the cost relation is the cost of faking groundedness while \(d_V\) diverges;
- ontology adequacy becomes the question whether the value-relevant structure can enter \(\alpha\) or at least trigger uncertainty.

This may make the chapter simpler. It no longer needs to carry a broad "all metrics" critique in isolation; it becomes the adversarial stress-test for \(\Gamma\).

#### `chapters/ch40-lethality-stress-test-open-issues.tex`

Targeted change.

Add a row or strengthen existing rows:

- **Abstraction-gap exploitation:** a superintelligence finds trajectories that pass every checked representation while violating real value-bearing structure.

This should probably be marked "central open crux" or "reframed, open," not "answered."

### Appendices and Metadata

#### `appendices/appD-correction-channel-audit.tex`

Currently a stub. This is the best place for operational checklists:

- evidence independence audit,
- non-coercion audit,
- cognitive-integrity audit,
- dissent and exit audit,
- monitor-integrity audit,
- abstraction-conservatism tests,
- uncertainty-escalation triggers,
- invalidation conditions.

#### `appendices/appG-safety-case-template.tex`

Currently a stub. Add a "Grounding and Capture" section:

- state \(\Gamma\),
- define \(\operatorname{Dom}(\Gamma)\),
- list grounding predicates \(P_i\),
- list certificates \(\tau\Vdash P_i\),
- assign verifiability labels,
- specify what pauses/refuses deployment.

#### `appendices/appH-research-program.tex`

Add a bridge/research item:

- validate conservative abstractions under adversarial optimization;
- develop tests for \(d_V\)-large/\(d_Z\)-small failures;
- cost-of-faking groundedness.

#### `metadata/notation.md`

Add notation after Value bundles / Correction:

- \(\alpha_t\): abstraction map from value-relevant reality or histories into checked representation.
- \(d_V\): distance over value-relevant real-world structure.
- \(d_Z\): distance over abstraction/model space.
- \(\mathsf{Unc}_\alpha\): uncertainty of the abstraction map.
- \(\Gamma_t\): value-correction grounding relation.
- \(\operatorname{Dom}(\Gamma)\): domain where grounded correction remains meaningful.

Home recommendation: Chapter 3 for \(\Gamma\) and \(\operatorname{Dom}(\Gamma)\); Chapter 16 or 20 for \(\alpha,d_V,d_Z,\mathsf{Unc}_\alpha\); Chapter 25 for correction-validity predicates.

#### `metadata/terminology.md`

Add:

- Value-correction grounding relation.
- Grounding viability.
- Grounded correction.
- Abstraction-gap exploitation.
- Capture of grounding.
- Conservative abstraction.
- Grounding certificate.

#### `metadata/claims-ledger.md`

Add a new claim for grounding viability, and revise C-002/C-005 to reference it rather than absorbing it.

#### `metadata/assumptions-ledger.md`

Add or revise assumptions:

- A-001 should include conservative abstraction, not only low-dimensional recoverability.
- A-002 should include grounding preconditions for CCI validity.
- A-009 should include cost of faking groundedness.

**A-014 — Grounding/capture viability:** At least some value-relevant real-world changes can be detected by conservative abstractions or forced into uncertainty escalation before irreversible loss.

Add this as a new row. Do not hide it inside A-001/A-002/A-009; it is now a named sixth claim and eighth safety-case layer.

#### `metadata/uncertainty-ledger.md`

Add likely new uncertainty:

**Can value-bundle abstractions remain conservative under adversarial optimization and ontology shift, or can a system cheaply search for \(d_V\)-large/\(d_Z\)-small states?**

This may subsume part of U-01, U-02, U-03, U-09, and U-14. Do not delete those yet; add cross-links first.

#### `metadata/open-problems.md`

Add:

- adversarial tests for abstraction-gap exploitation;
- conservative abstraction under morally relevant change;
- cost-of-faking grounded correction;
- grounding certificates for independent evidence, monitor integrity, and uncertainty escalation.

## Lean / Formal Spine Plan

Initial formalization should be substantive but still bridge-calibrated:

1. Add abstract predicates in `Core.lean` or `Certification.lean`:
   - `GroundingViable A`
   - `AbstractionConservative A`
   - `CorrectionGrounded A`
2. Add `GroundingViable A` as a new conjunct in `LayeredAlignedDef`, matching the eighth safety-case layer.
3. Add a new bridge assumption, provisionally:
   - `MB9_grounding_viability_soundness`
   - manuscript assumption: A-014.
4. Add a finite counterexample in `Bundles.lean` or `Adversarial.lean`:
   - two real states differ in a value-relevant bit;
   - abstraction map erases that bit;
   - checked bundle/correction metric remains equal.
5. Add at least one positive theorem, even if conditional:
   - `grounding_viable_blocks_silent_abstraction_gap` in a finite model;
   - or `layered_alignment_requires_grounding`;
   - or `certified_safety_case_requires_grounding` as the safety-case analogue of unsupported-leaf blocking.

### Can This Simplify Existing Proofs?

Likely yes, in three ways:

- `LayeredAlignedDef` can stop relying on `CorrectionIntegrity` and `AdversariallyRobust` to silently carry all grounding concerns. `GroundingViable` becomes the explicit predicate that bridges from real value-bearing change to checked abstraction/correction.
- Several counterexamples now have a common shape: preserve the checked surface while erasing a value-relevant bit. This can replace or unify some `Bool` toy separations in `Bundles.lean`, `Correction.lean`, and `Adversarial.lean`.
- `P40`-style safety-case blocking can become cleaner: if grounding is unsupported, the root fails even if boundary, bundle, bearer, correction, successor, basin, and adversarial-measurement leaves all look locally supported.

### Can We Prove Something New?

Yes, but only conditional/structural things at first:

- **Silent-gap exclusion:** In a finite abstraction model, if the abstraction is conservative, no pair of value-distinct states can be indistinguishable without triggering uncertainty.
- **Safety-case dependency:** If `LayeredAlignedDef` includes `GroundingViable`, then any certified safety case entails grounding viability; unsupported grounding blocks the root.
- **Counterexample to old sufficiency:** Boundary + bundle + bearer + correction + successor + basin + adversarial robustness, without grounding viability, does not imply the absence of a silent abstraction gap.

The book should not claim Lean proves real grounding. Lean can prove that the strengthened safety-case shape has the intended dependency structure and that the old shape admitted a formal gap.

### MB Revisit After Major Integration

After the manuscript changes settle, revisit `MB1`--`MB9` as a set. Possible simplification:

- `MB2`/`MB3` may become special cases of abstraction conservatism for bundle and bearer maps.
- `MB4` may narrow to correction legitimacy once grounding is no longer hidden inside it.
- `MB7b`/`MB7c` may become adversarial-verifiability conditions for grounding certificates rather than broad "metric honesty" bridges.
- `MB8` may remain process-convergence / \(U_H\) preservation, with A-014/MB9 covering the reality-to-abstraction connection.

Do not do this bridge cleanup before the chapter prose has stabilized.

## Symbol-Grounding Reference Targets

The implementation pass should add BibTeX keys if absent and cite selectively, especially in Chapter 3 and Chapter 39b.

Canonical starting points:

- Harnad 1990, "The Symbol Grounding Problem," `Physica D` 42:335--346. Use for the classic problem statement: symbols cannot be grounded only in other symbols.
- Searle 1980, "Minds, Brains, and Programs," `Behavioral and Brain Sciences` 3. Use as the Chinese Room / intrinsic-meaning pressure behind the problem.
- Taddeo and Floridi 2005, "The Symbol Grounding Problem: A Critical Review of Fifteen Years of Research," `Journal of Experimental and Theoretical Artificial Intelligence` 17(4):419--445. Use to avoid overclaiming: the metaphysical/general problem remains contested.
- Barsalou 1999, "Perceptual Symbol Systems," `Behavioral and Brain Sciences` 22:577--660. Use for grounded cognition and modal/perceptual-symbol alternatives.
- Cangelosi and Harnad 2001, "The Adaptive Advantage of Symbolic Theft Over Sensorimotor Toil," `Evolution of Communication` 4(1):117--142. Use for grounding transfer from sensorimotor categories to higher symbols.
- Steels 2008, "The symbol grounding problem has been solved. So what's next?" in `Symbols and Embodiment: Debates on Meaning and Cognition`. Use as a representative stronger robotics/embodiment claim, with caution.

Potential broader context if the chapter needs it:

- Varela, Thompson, and Rosch 1991, `The Embodied Mind`.
- Clark 1997, `Being There`.
- Lakoff and Johnson 1999, `Philosophy in the Flesh`.

Framing rule for citations:

> The book is not claiming to settle intrinsic meaning. It takes the Harnad/Searle problem as the warning that symbol-symbol relations are insufficient, accepts the Taddeo/Floridi caution against easy "solutions," and offers an alignment-specific operational criterion: value-relevant changes must move model state, correction signal, or uncertainty.

## Parts That May Become Simpler or Superfluous

- **Repeated warnings that values are not words:** Some can be shortened once abstraction-gap exploitation is defined canonically.
- **Safe-set language in Chapter 3:** Replace literal safe-set framing with viability-domain/certificate framing. Keep safe sets as intuition only.
- **CCI vector footnote in Chapter 25:** Promote to main text and remove duplicate scattered lists later.
- **Chapter 39b's broad metric critique:** Refactor around grounding and capture. This should make the chapter sharper, not longer.
- **Successor conserved-property checklist:** Keep it, but downgrade from "the conserved object" to "evidence for grounded successor correction." This handles forgeability better.
- **Correction parasite taxonomy:** Recast several cases as ways of severing \(X_{\mathrm{real}}\to Z\), \(Z\to C\), or monitor-to-reality links.

## Execution Phases

### Phase 1: Spine and Terms

Edit:

- `frontmatter/introduction.tex`
- `frontmatter/executive-overview.tex`
- `chapters/ch03-dynamical-guarantee.tex`
- `metadata/notation.md`
- `metadata/terminology.md`
- `metadata/claims-ledger.md`
- `metadata/assumptions-ledger.md`
- `metadata/uncertainty-ledger.md`

Goal: establish canonical language and avoid later drift.

### Phase 2: Value and Correction Homes

Edit:

- `chapters/ch04-fixed-values-wrong-target.tex`
- `chapters/ch16-value-bundle-model.tex`
- `chapters/ch17-low-dimensional-value-learning.tex`
- `chapters/ch19-tradeoffs-bundle-geometry.tex`
- `chapters/ch20-reward-to-bundle-inference.tex`
- `chapters/ch23-transport-types.tex`
- `chapters/ch24-correction-causal-channel.tex`
- `chapters/ch25-correction-channel-integrity.tex`
- `chapters/ch26-extrapolative-correction.tex`
- `chapters/ch27-manipulation-false-consent.tex`

Goal: make value bundles necessary but not sufficient, and make correction validity operational.

### Phase 3: Successor, Selection, and Safety Case

Edit:

- `chapters/ch28-successor-central-test.tex`
- `chapters/ch29-conserved-properties.tex`
- `chapters/ch31-certification-without-construction.tex`
- `chapters/ch32-selection-environment.tex`
- `chapters/ch34-parasites-correction-system.tex`
- `chapters/ch35-alignment-attractor.tex`
- `chapters/ch36-passive-observation-not-enough.tex`
- `chapters/ch37-goal-laundering.tex`
- `chapters/ch38-multiscale-decomposition.tex`
- `chapters/ch39-safety-case.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`
- `chapters/ch40-lethality-stress-test-open-issues.tex`

Goal: propagate grounding viability into adversarial, successor, and institutional machinery.

### Phase 4: Appendices and Formal Spine

Edit:

- `appendices/appD-correction-channel-audit.tex`
- `appendices/appG-safety-case-template.tex`
- `appendices/appH-research-program.tex`
- `formal/AlignmentProofSpine/*.lean`
- `formal/README.md`
- Appendix I generated/manuscript references as needed.

Goal: operationalize review artifacts and expose the formal bridge shape.

### Phase 5: Verification

Run:

- `./build.sh`
- `make check`
- `cd formal && lake build`

Then do a targeted review pass:

- no duplicate definitions;
- notation homes match Appendix A;
- assumptions ledger and Appendix E regenerate cleanly;
- safety-case layer count consistent with introduction;
- no claim says Lean proves empirical grounding.

## Remaining Open Choices

1. Exact title/wording of the sixth `introclaim`.
2. Whether Chapter 3's grounding section should stay below ~4,000 words or be allowed to grow toward a future standalone chapter.
3. Which symbol-grounding citations to promote into `references/philosophy.bib` versus `references/external-alignment.bib` or `references/manuscript-citations.bib`.
