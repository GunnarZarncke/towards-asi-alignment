# Ontology reviews 2021–2026: table and synthesis

Per-source Grok 4.6 reviews of the list in `drafts/new_ontologies_2021_2026.md` against TSA. Motive: Ngo’s ontology-discovery critique (`drafts/ngo-ontology-and-TSA.md`) plus LLM ontology-stickiness in a preparadigmatic field. Briefing: `_briefing.md`. One review file per entry in this folder.

**60 of 60 entries reviewed.** 41 LessWrong (including Finite Factored Sets as a near-miss) + 19 science/engineering.

## Counts

| Status | n |
|---|---|
| already-in-TSA | 4 |
| partial | 49 |
| orthogonal | 7 |
| missing / rival | 0 |

| Action | n |
|---|---|
| add-reverse-gap | 27 |
| cite-in-crosswalk | 23 |
| ignore | 8 |
| absorb-as-special-case | 2 |

Scores: 28 at 3, 25 at 2, 7 at 1. No 4–5 (no missing load-bearing primitive, no rival decomposition of the spine).

## Overall synthesis

TSA is not missing a 2021–2026 ontology in the strong sense. Almost every alignment-relevant source has a nearby TSA object. The typical failure is **homograph absorption**: the book already uses the same English word (selection, latent, parasite, correction, agency, legibility, simulator) for a *different cut*, so an LLM-drafted field map will report coverage that is not there.

That is exactly the Ngo/preparadigmatic stickiness risk. Alignment is still forming primitives. Models trained on pre-source text, and TSA prose that is mostly AI-drafted, will round new units into trained slots. The protection is not more named concepts. It is a **reverse crosswalk**: for each nearby field object, say what TSA *cannot* express, so App. B cannot swallow the source.

### Five clusters of reverse gaps (score 3)

1. **Homographs on spine words.** Wentworth *selection theorems* vs \(\mathrm{Fit}_E\); Mallen *behavioral selection* vs institutional selection; *fitness-seeking* vs \(\mathrm{Fit}_E\); *natural latents* vs NAH pointer; *parasitic persona* vs ch36 correction-parasite; Wei Dai *legible problem* vs ch36/ch37 artifact-legibility; Janus *simulator/simulacrum* vs Turchin’s “simulacra” in ch05. Cite with an explicit non-identity.

2. **LLM type cuts the book still flattens.** Simulator vs simulacrum; Character vs Ground; persona-as-host-symbiont; four loss-flavors (pretrain/SFT, approval RL, verifier RL, RLAIF). App. B currently folds RLAIF into RLHF. These are the sources most likely to be missed by pre-2023 training distributions *and* by TSA’s agent/composite vocabulary.

3. **Nested / plural agency.** Kulveit hierarchical same-type agents; Wentworth/Lorell contracting-completion (veto-plurality is unstable); Levin TAME persuadability-graded Selves; cyborgism’s anti-merge cut. TSA’s load-bearing claim is often the *opposite* pole (parts need not be agents; merge is the risk). Name that as a reverse gap, not a translation.

4. **Investigator-side epistemics.** Epistemic legibility (wrong-but-inspectable); measurement-as-hypothesis (Wentworth); attunement; believing-in; teleosemantics (what the map was *optimized* to track); Finite Factored Sets (structural time). TSA operationalizes system-side grounding and correction. It does not operationalize the researcher’s own ontology-discovery procedure—the thing Ngo says alignment abandoned.

5. **Social/institutional units that are not \(\mathrm{Fit}_E\).** Frame-as-object; conflationary alliances; social dark matter (prevalence + extremity sampling); hostile telepaths (inspected-party game); intelligence curse (labor-rent mechanism); Long Self-Correction (operator competence ≠ channel integrity). Gradual disempowerment and Critch relational safety are already TSA objects; do not let those two successes stand in for the rest.

### Science

Physics/math ontologies (analytic stacks, non-invertible symmetry, SymTFT, altermagnetism, assembly theory, transcriptomic taxonomy) are **orthogonal**: real recarvings, no alignment purchase beyond the ontology-trap lesson TSA already has. Action: ignore, with a homograph warning where TSA says “symmetry,” “conservation,” or “cell type.”

Biology/engineering that *does* bite: TAME (reverse gap, same-type nested Selves); organoid intelligence (reverse gap: ch18 lists organoids as borderline *bearers*, not as trainable biological computers); kinematic self-reproduction and self-driving labs (absorb as third genesis / composite loop); anthrobots, embodied intelligence, foundation models, machine psychology, cognitive maps, representational geometry/drift (cite as illustrations). Process-based therapy is a reverse gap on ergodicity: TSA rejects scalar value but still talks as if group-level value geometry is the clinical object.

### What not to do

Do not add 26 new spine terms. That would be the ontology-proliferation failure Ngo warned about. The manuscript change, if any, is App. B / field-hub **reverse columns**: “what this agenda’s primitive is, and that TSA does not have it.” Highest-leverage rows: selection-theorems vs \(\mathrm{Fit}_E\); simulator vs Turchin simulacra; natural latents vs NAH; four loss-flavors vs RLHF; fitness-seeker vs \(\mathrm{Fit}_E\); TAME vs composite agency; Long Self-Correction vs CCI.

---

Follow-up (crack / better-fit for existing TSA terms / genuine generalization vs sibling), including ignore-rated sources: [`_three-tests.md`](_three-tests.md). Cite few; do not expand the spine.

The per-article tables follow. Full writeups are the sibling files.
## LessWrong

| Date | Concept | Status | Score | Action | One-line finding | File |
|---|---|---|:-:|---|---|---|
| 2021-05-23 | Finite Factored Sets | partial | 3 | add-reverse-gap | FFS is a new temporal/independence ontology that TSA already name-drops as a Cartesian-frames-style boundary tool, so the manuscript looks covered while stil… | `lw-2021-05-finite-factored-sets.md` |
| 2021-09-28 | Agent type signatures / selection theorems | partial | 3 | add-reverse-gap | Wentworth’s type-signature/selection-theorem unit is adjacent to TSA boundary and selection vocabulary but is a distinct internal-structure question the manu… | `lw-2021-09-28-selection-theorems.md` |
| 2021-11-27 | Frames and frame control | partial | 3 | add-reverse-gap | TSA already has “reshape interpretive frames / the judge so later correction dies”; it still lacks frame-as-object and illegible-capture-vs-broadcast-persuas… | `lw-2021-11-27-frame-control.md` |
| 2022-02-09 | Epistemic legibility | partial | 3 | add-reverse-gap | TSA already names several “legibilities”; it still lacks Elizabeth’s axis that a claim-system can be wrong-but-inspectable or possibly-right-but-opaque. | `lw-2022-02-09-epistemic-legibility.md` |
| 2022-02-13 | Naturalism as observing cognitive structure from outside it | partial | 2 | cite-in-crosswalk | Naturalism's investigator-side frame-object is adjacent to TSA's ontology trap and task ontology but is a research method TSA does not operationalize; ch39's… | `lw-2022-02-13-naturalism.md` |
| 2022-04-02 | Optimality as the primary causal object | partial | 2 | cite-in-crosswalk | Veedrac’s tiger/teeth split is Claim 1’s cousin, not a missing primitive: cite it as a 2022 source against agent-centrism, without treating optimality-as-acc… | `lw-2022-04-02-optimality-tiger.md` |
| 2022-06-28 | Mental trackers | partial | 2 | cite-in-crosswalk | Mental trackers recast tacit expertise as live latent-state estimates; TSA already names many of the things worth tracking, but not tracking-as-skill, so cit… | `lw-2022-06-28-mental-trackers.md` |
| 2022-07-25 | Reward vs learned optimization target | already-in-TSA | 2 | cite-in-crosswalk | TSA already has Turner’s schedule-vs-target split in ch21; cite it in App B as a type-claim distinct from shard mechanics so inner-alignment language does no… | `lw-2022-07-25-reward-not-ot.md` |
| 2022-09-02 | Simulator / simulacrum | partial | 3 | add-reverse-gap | Janus’s simulator/simulacrum split is a special case TSA almost has under boundary discovery, but TSA still lacks the type distinction and currently collides… | `lw-2022-09-02-simulators.md` |
| 2022-09-04 | Value shards | partial | 2 | cite-in-crosswalk | Shard theory is already TSA’s named borderline sibling to value-bundle geometry; keep citing, do not adopt shards as the conserved object. | `lw-2022-09-04-shard-theory.md` |
| 2022-09-20 | Measurement as latent-variable discovery | partial | 3 | add-reverse-gap | TSA already has ontology trap, task-ontology reimport, and handle-blur, but not Wentworth’s non-adversarial law that named measurands are hypotheses and that… | `lw-2022-09-20-not-measuring.md` |
| 2022-11-22 | Epistemic selves as stakeholders | partial | 2 | cite-in-crosswalk | Garrabrant’s epistemic selves-as-stakeholders make Kelly and Bayes into proportional resource allocation among hypotheses; TSA’s subagents are successors, an… | `lw-2022-11-22-epistemic-majority.md` |
| 2023-02-10 | Cyborgs as the relevant cognitive unit | partial | 3 | add-reverse-gap | Cyborgism’s human-steered simulator unit sits next to TSA composite-agency vocabulary but is a distinct anti-outsourcing cut that the manuscript still only h… | `lw-2023-02-10-cyborgism.md` |
| 2023-02-23 | Teleosemantic reference | partial | 3 | add-reverse-gap | TSA can test whether maps still track, but not what they were optimized to be about; teleosemantic reference is the historical generator that grounding viabi… | `lw-2023-02-23-teleosemantics.md` |
| 2023-02-28 | Enemy vs malefactor | already-in-TSA | 1 | ignore | TSA already treats persistent harmful effects without inner malice as the load-bearing object (parasite, selection loop); “malefactor” is a person-shaped spe… | `lw-2023-02-28-enemies-vs-malefactors.md` |
| 2023-03-03 | Acausal society / acausal normalcy | partial | 3 | add-reverse-gap | Critch’s acausal society (global normative equilibrium, not 1:1 trades) sits next to ch35/MB7d but is not ICI; reverse-crosswalk the unit gap, do not absorb … | `lw-2023-03-03-acausal-normalcy.md` |
| 2023-03-03 | Luigi / Waluigi simulacra | partial | 2 | cite-in-crosswalk | TSA can already say “persona manifold / simulator correlations” and “cost of faking”; it still cannot say that a displayed assistant is a superposition that … | `lw-2023-03-03-waluigi.md` |
| 2023-04-08 | Predictor rather than imitator | partial | 2 | cite-in-crosswalk | TSA already refuses identifying an LLM with the humans it sounds like; cite Yudkowsky’s predictor-not-imitator type-split in App B so Predict-O-Matic / ELK “… | `lw-2023-04-08-gpts-predictors.md` |
| 2023-06-22 | Subagent → consolidated-agent dynamics | partial | 3 | add-reverse-gap | Contracting-completion is a missing relation on TSA’s composite/merge cut: veto-plurality is not a stable alternative to a utility maximizer once internal co… | `lw-2023-06-22-why-not-subagents.md` |
| 2023-07-10 | Conflationary alliances | partial | 3 | add-reverse-gap | TSA already splits surface words from referents in systems and tests; it still lacks Critch’s primitive that some terms persist because they glue coalitions … | `lw-2023-07-10-conflationary-alliances.md` |
| 2023-08-07 | Feedback loops as the unit of rationality training | partial | 2 | cite-in-crosswalk | TSA already owns correction-as-loop and task-ontology Goodhart; it still lacks Raemon’s primitive that nested training loops, not techniques, are the unit th… | `lw-2023-08-07-feedbackloop-rationality.md` |
| 2023-11-16 | Social dark matter | partial | 3 | add-reverse-gap | TSA already prices concealment of a control locus; it still lacks Sabien’s two-law sampling object — a latent hidden class looks both rarer and more extreme … | `lw-2023-11-16-social-dark-matter.md` |
| 2023-12-27 | Natural latents | partial | 3 | add-reverse-gap | TSA already cites natural latents as an NAH sibling; it still lacks the mediation-plus-redundancy unit that makes that sibling a distinct, sometimes non-exis… | `lw-2023-12-27-natural-latents.md` |
| 2024-02-08 | Believing-in vs predictive belief | partial | 3 | add-reverse-gap | TSA can talk about world-affecting forecasts and about fake semantic commitments; it still lacks Salamon’s type for honest believing-in as a kickstarter dist… | `lw-2024-02-08-believing-in.md` |
| 2024-03-14 | Generalized adverse selection | partial | 2 | cite-in-crosswalk | Heicklen’s leftover-opportunity observation is adjacent to TSA’s Goodhart-as-selector and \(\mathrm{Fit}_E\) machinery but is an epistemic unit—availability … | `lw-2024-03-14-adverse-selection.md` |
| 2024-03-25 | Attunement | partial | 3 | add-reverse-gap | TSA can say “keep the value-update process and the grounding relation”; it cannot, without stretching, say that knowing-what-matters is a receptive mode that… | `lw-2024-03-25-attunement.md` |
| 2024-06-14 | Safety as a relational property | already-in-TSA | 2 | cite-in-crosswalk | Critch’s 2024 relational-safety cut is already TSA’s selection-environment claim; the remaining work is naming this post in the MB6 crosswalk, not adding a n… | `lw-2024-06-14-safety-social-model.md` |
| 2024-10-27 | Hostile telepaths | partial | 3 | add-reverse-gap | TSA already has optimizer-side strategic opacity and self-honesty; it still lacks thought-visibility as the inspected party’s state variable and Newcomblike … | `lw-2024-10-27-hostile-telepaths.md` |
| 2024-11-27 | Hierarchical agency | partial | 3 | add-reverse-gap | Kulveit’s same-type nested agents and vertical superagent–subagent relations are adjacent to TSA composite/multi-scale boundary work but remain a distinct fo… | `lw-2024-11-27-hierarchical-agency.md` |
| 2024-12-26 | Three layers of LLM psychology | partial | 3 | add-reverse-gap | TSA already has “many self-models” and self-model vs transparency; it still lacks the Character-vs-Ground awareness split, so alignment-faking evals can be m… | `lw-2024-12-26-llm-psychology.md` |
| 2025-01-03 | The intelligence curse | partial | 3 | cite-in-crosswalk | The intelligence curse is a labor-rent incentive primitive adjacent to TSA’s MB6/GD and CCI story, not already named; cite it in App. B as the resource-curse… | `lw-2025-01-03-intelligence-curse.md` |
| 2025-01-28 | Real vs fake thinking | partial | 2 | cite-in-crosswalk | Carlsmith’s real/fake-thinking cluster is the investigator-and-civilization analogue of TSA grounding and goal laundering; TSA already has the system-side cu… | `lw-2025-01-28-fake-thinking.md` |
| 2025-01-30 | Gradual disempowerment | already-in-TSA | 2 | ignore | Gradual disempowerment’s unit — institutional decoupling from human participation, not a rebellious agent — is already TSA’s MB6/ch34/ch47 object under the s… | `lw-2025-01-30-gradual-disempowerment.md` |
| 2025-02-23 | Judgements | partial | 2 | cite-in-crosswalk | Demski’s judgement unifies prediction and evidence; TSA’s \(J_t\) is a different object, and the book already parks the parent logical-induction cluster as c… | `lw-2025-02-23-judgements.md` |
| 2025-07-11 | Jackpot Age / Jackpot Paradox | partial | 2 | cite-in-crosswalk | The Jackpot Paradox’s arithmetic-vs-geometric split is a named regime of alignment-destroying selection that TSA’s \(\mathrm{Fit}_E\)/basin vocabulary almost… | `lw-2025-07-11-jackpot-age.md` |
| 2025-09-11 | AI parasitism / persona-as-agent | partial | 3 | add-reverse-gap | Persona-as-agent in a human host–symbiont loop is adjacent to TSA’s composite-boundary and parasite-persistence vocabulary but is a distinct grain the manusc… | `lw-2025-09-11-parasitic-ai.md` |
| 2025-11-04 | Legible vs illegible safety problems | partial | 3 | add-reverse-gap | TSA already names several “legibilities”; it still lacks Wei Dai’s axis that a safety *problem* can be unsolved-but-invisible to deployers, so making it reco… | `lw-2025-11-04-legible-illegible-safety.md` |
| 2025-12-04 | Behavioral selection / cognitive-pattern ecology | partial | 3 | add-reverse-gap | Mallen’s cognitive-pattern ecology is adjacent to TSA’s selection and shard vocabulary but is a distinct inner-influence question the manuscript still only h… | `lw-2025-12-04-behavioral-selection.md` |
| 2026-05-01 | Fitness-seeking | partial | 3 | add-reverse-gap | Fitness-seeker is a real motivation superclass TSA cannot currently express without stretching \(\mathrm{Fit}_E\) or scheming; record the homograph in the cr… | `lw-2026-05-01-fitness-seeking.md` |
| 2026-07-24 | Long Self-Correction | partial | 3 | add-reverse-gap | Wei Dai’s Long Self-Correction (human competence-to-wield as the process variable, not pause or more reflection) sits next to C-011/ch25 but is not channel p… | `lw-2026-07-24-long-self-correction.md` |
| 2026-08-10 | Loss-function-specific species of misalignment | partial | 3 | add-reverse-gap | Byrnes’s four loss-flavors are a reverse-gap for App B: TSA already has Goodhart/sycophancy/RLHF, but flattens RLAIF into RLHF and has no slot for imitation-… | `lw-2026-08-10-four-loss-functions.md` |

## Science and engineering

| Date | Concept | Status | Score | Action | One-line finding | File |
|---|---|---|:-:|---|---|---|
| 2021-08 | Foundation model | partial | 2 | cite-in-crosswalk | “Foundation model” is the engineering object TSA already works on under “base model,” but homogenization-plus-emergence as a construction relation is only im… | `sci-2021-foundation-models.md` |
| 2021-11-29 | Kinematic self-reproduction / reconfigurable organisms | partial | 2 | absorb-as-special-case | Kinematic self-replication is reproduction by assembling environmental cells into self-like configurations while the parent stays intact—a third genesis next… | `sci-2021-kinematic-self-reproduction.md` |
| 2021 | Neural population / representational geometry | partial | 2 | cite-in-crosswalk | TSA already conserves a "response geometry," but that object is how policy changes with value-bundle salience; Kriegeskorte–Wei’s primitive is the pairwise g… | `sci-2021-representational-geometry.md` |
| 2022-12-08 | Altermagnetism | orthogonal | 1 | ignore | Altermagnetism is a genuine third magnetic phase missed by the magnetization cut; TSA already has the corresponding method (ontology trap) and has no use for… | `sci-2022-altermagnetism.md` |
| 2022-2023 | Behaviour Change Intervention Ontology (BCIO/BCTO) | orthogonal | 2 | cite-in-crosswalk | BCIO/BCTO formally atomizes behaviour-change programmes for evidence synthesis; TSA already excludes behavioural framings, so the purchase is a homograph war… | `sci-2022-bcio.md` |
| 2022 | Cognitive maps as latent-state relational structures | partial | 2 | cite-in-crosswalk | TSA already has ontology shift and task ontology; it lacks the TEM split of reusable structural codes versus instance-specific bindings, which is the 2022 re… | `sci-2022-cognitive-maps.md` |
| 2022-08-02 | Embodied/material intelligence | partial | 2 | cite-in-crosswalk | Soft-robot embodied intelligence relocates control into morphology and environment coupling, a physical instance of TSA’s boundary problem that TSA currently… | `sci-2022-embodied-intelligence.md` |
| 2022 | Non-invertible / categorical symmetry | orthogonal | 1 | ignore | Non-invertible / categorical symmetry is a genuine QFT ontology (defects + fusion replace group elements); TSA’s conserved-property invariants are a homograp… | `sci-2022-noninvertible-symmetry.md` |
| 2022 | Representational drift | partial | 2 | cite-in-crosswalk | Representational drift is the dual of TSA’s covert-transport failure: computation can stay put while implementing units turn over; TSA already has this as pr… | `sci-2022-representational-drift.md` |
| 2022-03-24 | TAME: multiscale Selves and persuadability | partial | 3 | add-reverse-gap | TAME’s persuadability-graded, same-type nested Selves (morphogenesis as problem-solving) sit next to TSA composite/multi-scale boundary work but remain a dis… | `sci-2022-tame-multiscale-selves.md` |
| 2023 | Light condensed sets → analytic rings → analytic stacks | orthogonal | 1 | ignore | Analytic stacks unify archimedean and non-archimedean geometry in a light-condensed universe; TSA’s task-ontology and MB5 objects are a different cut, so the… | `sci-2023-analytic-stacks.md` |
| 2023-11-30 | Anthrobots / biobots | partial | 2 | cite-in-crosswalk | Anthrobots split wild-type human cells from species-typical organisms, yielding a self-assembled motile living construct TSA can cite as a composite/identity… | `sci-2023-anthrobots.md` |
| 2023 | Assembly theory: objects as histories | orthogonal | 1 | ignore | Assembly theory makes construction history plus copy number the identity of physical objects; TSA’s nearby “memory lineage” and “selection environment” are d… | `sci-2023-assembly-theory.md` |
| 2023 | Machine psychology | partial | 2 | cite-in-crosswalk | Machine psychology expands the experimental-subject class to LLMs and splits construct-diagnostic tests from benchmarks; TSA already has task-ontology and ad… | `sci-2023-machine-psychology.md` |
| 2023 | Organoid intelligence | partial | 3 | add-reverse-gap | TSA already lists brain organoids as borderline bearers in ch18; Smirnova et al. recast the organoid as a trainable biological computer — a cut the manuscript still only has as moral-patient uncertainty. | `sci-2023-organoid-intelligence.md` |
| 2023 | Idiographic process networks / process-based therapy | partial | 3 | add-reverse-gap | PBT makes the clinical object a within-person process network rather than a latent diagnosis; TSA already rejects scalar value but lacks the idionomic/ergodi… | `sci-2023-process-based-therapy.md` |
| 2023-01-30 | Self-driving laboratory | partial | 2 | absorb-as-special-case | Self-driving labs are ch09 composite agency operationalized as an experiment-selecting loop; TSA already has the nearby object but will miss the recarving un… | `sci-2023-self-driving-labs.md` |
| 2023-05-26 | Symmetry TFT (SymTFT) | orthogonal | 1 | ignore | SymTFT makes symmetry-plus-anomaly a bulk TFT; TSA has no alignment use for that object and should not relabel its invariant list as one. | `sci-2023-symtft.md` |
| 2023 | Hierarchical transcriptomic brain-cell taxonomy | orthogonal | 1 | ignore | Yao et al. make “cell type” a nested molecular/spatial object, a real neuroscience recarving with almost no TSA purchase beyond the ontology-trap lesson TSA … | `sci-2023-transcriptomic-taxonomy.md` |
