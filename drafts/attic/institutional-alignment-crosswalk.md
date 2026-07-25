# Institutional Alignment Crosswalk

Status: source draft for a future appendix. This is not manuscript-ready prose, and it should not be promoted into a chapter.

Audience: non-technical policy makers, regulators, funders, social scientists, and other institution-facing readers who need a translation guide from the book's alignment machinery into familiar social mechanisms.

Thesis: many human institutions are already crude alignment systems. They identify real power, specify who counts, preserve correction channels, defend those channels from capture, manage succession, and shape selection pressure. The analogy is useful for sourcing interventions and baselines, but it is not reassuring unless the same speed, access, independence, and anti-capture conditions survive in AI deployment.

Appendix positioning decision:

- This material should become an appendix, not a chapter.
- It should serve as a translation guide, not as a new part of the book's argument.
- It may be detailed enough to carry the examples, baseline discussion, and answers below, but the main text should not depend on it.
- The appendix should probably sit near the bridge crosswalk, safety-case, or audit appendices, where readers can use it as an institutional-language companion.

## 0. What Counts as a Baseline?

The previous compact crosswalk used "baseline" too loosely. It mixed three different claims.

1. Existence baseline: a mechanism exists in some mature institutions. Example: courts have appeals; medical research has clinical holds; securities law has material-disclosure obligations.
2. Performance baseline: institutions achieve measurable performance under favorable conditions. Example: some aviation defects trigger grounding before further accidents; some mergers are blocked before concentration rises.
3. Aspiration baseline: what AI governance should target given the capability gap. Example: real-time correction handles for systems whose harm window is minutes, not years.

For this draft, "baseline" should not mean "human institutions reliably solve this." It should mean "there is an institutional function with measurable inputs, outputs, and failure modes." The relevant question is whether an AI alignment method can match or improve that function under faster, more opaque, more copyable conditions.

Candidate measurands:

| Measurand | Qualitative tiers | Possible quantitative proxy | Institutional source |
|-----------|-------------------|-----------------------------|----------------------|
| Controller identification | failed / partial / adversarially robust | fraction of enforcement cases where operative controller differs from nominal entity and is recovered | beneficial-ownership registries, forensic accounting, piercing the veil |
| Causal correction reach | theater / weak / strong | uplift in compliant action after correction, conditioned on state | injunctions, clinical holds, consent-decree monitoring |
| Latency | acceptable / risky / fatal | time from correction to first behavior change divided by time to irreversible harm | court dockets, recalls, incident response |
| Independence | captured / mixed / independent | funding, appointment, recusal, and reporting-line overlap | inspector-general offices, judicial independence, audit committees |
| Reversibility | preserved / narrowed / gone | fraction of harm still reversible when correction lands | medical trials, aviation grounding, environmental injunctions |
| Bearer coverage | narrow / contested / inclusive | scope of standing, protected classes, affected-party consultation | civil-rights law, data-protection law, environmental law |
| Cost of fake compliance | fake cheaper / parity / honest cheaper | estimated evasion cost divided by honest compliance cost | forensic accounting, FDA inspections, emissions testing |
| Deployment selection | race basin / mixed / certified basin | share of funding, procurement, insurance, or market access requiring certification | aviation, pharma, finance, nuclear |

This gives the draft a discipline: each mapping should name not only the institutional analogue, but the measurable failure mode.

## 1. Boundary Discovery: Who Is the Real Actor?

Book concept: boundary discovery. The book asks us to find the real optimizer, not the visible model or formal entity. See `chapters/ch06-agent-without-anthropomorphism.tex`, `chapters/ch07-finding-boundary.tex`, and `appendices/appB-bridge-crosswalk.tex` on MB1.

Institutional analogue: jurisdiction assignment, beneficial ownership, alter-ego doctrine, corporate veil piercing, market-structure analysis, shadow-control analysis, and investigation of informal decision rights.

The important correction to the earlier crosswalk is: institutions ask where real decision power is, but they only sometimes can answer. They do well when records persist, action is slow, investigators have subpoena power, and the actor is legally locatable. They do poorly when control is informal, cross-border, rapidly recomposed, or technically hidden.

Examples:

- Enron and off-balance-sheet entities: nominal corporate structure hid operative risk and control. Forensic accounting and subpoena-backed investigation recovered enough structure after the fact, but too late as a correction channel.
- Panama Papers and shell companies: beneficial owners were not visible to ordinary registry inspection. Leaks and registry reform improved boundary discovery, but only after secrecy had already been selected for.
- Gig-work platforms: the formal label "independent contractor" conflicted with platform control over pricing, routing, rating, and deactivation. Labor agencies and courts partially recovered the operative controller.
- Algorithmic trading and exchange design: harm can arise from interaction between firms, market rules, co-location, and latency, not from one visible actor.
- DeFi governance: "no controller" can hide core developers, multisig holders, token whales, foundations, and off-chain coordination.

Baseline:

- Existence: yes. Institutions have mature methods for recovering hidden control.
- Performance: partial and context-dependent.
- AI aspiration: boundary discovery must include model, tools, memory, users, lab incentives, deployment loop, product metrics, and institutional incentives. A model-only audit is analogous to inspecting the subsidiary while missing the parent, funder, or shadow board.

Back-projection to AI alignment: boundary discovery should not be only a representation-learning problem. It should include governance handles, capital flows, API dependencies, evaluation incentives, and deployment-mediated control.

Forward-projection to institutions: AI-style boundary tools could help regulators represent composite actors: model plus platform plus customer workflow plus market incentive. This might improve antitrust, labor classification, and platform governance, but only if the recovered boundary is contestable in ordinary legal process.

## 2. Capability as Boundary Information: What Can the Actor Reliably Cause?

Book concept: capability as boundary information. Capability is not a benchmark score; it is the degree to which a system can predict and control future states through its boundary. See `chapters/ch11-capability-without-task-ontology.tex` and `chapters/ch12-capability-growth-boundary-expansion.tex`.

Institutional analogue: licensing, operational readiness, stress testing, market-power analysis, safety certification, and systemic-risk supervision.

Examples:

- Aviation measures pilot training, maintenance, simulator checks, incident records, and airworthiness before passenger flight.
- Pharma measures dose safety, efficacy, adverse events, and trial endpoints before general prescription.
- Finance measures capital adequacy, liquidity, leverage, and stress-test performance before allowing some forms of systemic exposure.
- Nuclear regulation measures design-basis accidents, operator training, redundancy, and emergency procedure integrity before licensing.
- Antitrust uses HHI, merger simulation, entry barriers, and coordinated-effects analysis to estimate what firms can cause in markets.
- Cyber regulation uses vulnerability severity, exploit evidence, and infrastructure criticality to set patching or reporting timelines.

Failure case: social media recommenders have often been allowed to demonstrate influence at scale while being evaluated mainly on engagement and user growth. That measures causal power, but not in a correction-preserving way.

Baseline:

- Institutions can measure domain-bounded causal reach when tests are mandatory, effects are observable, and failure is litigable.
- They cannot reliably measure latent strategic capability held back from tests or revealed only under crisis.
- For AI, the baseline should be: no new class of irreversible influence without a corresponding correction-channel upgrade.

Quantitative hook: compare pre-authorization test burden to post-hoc enforcement cost. If it is much cheaper to discover capability after harm than before deployment, the institution is in a race basin, not a certification basin.

## 3. Value Bundles: Constitutions Are Close, But Not the Same

Book concept: value bundles. In the book, values are compressed control directions with tradeoff geometry and bearer maps. See `chapters/ch16-value-bundle-model.tex`, `chapters/ch20-measuring-stress-testing-bundle-geometry.tex`, and `chapters/ch29-manipulation-false-consent.tex`.

Institutional analogue: constitutions, charters, rights catalogues, fiduciary duties, professional ethics, and public-interest mandates.

The previous crosswalk was too quick. Constitutions match value bundles in one respect: they do not optimize a single scalar. They preserve tradeoff patterns among liberty, safety, dignity, equality, care, truth, due process, and public order.

But institutions usually treat these values as legitimated opaque commitments. The book treats value bundles as partially measurable geometry. That difference matters.

| Layer | Institutional form | Opacity | Legitimacy source |
|-------|--------------------|---------|-------------------|
| Rhetoric | liberty, dignity, equality, public interest | high | tradition, revolution, deliberation |
| Doctrine | precedent, balancing tests, proportionality | medium | courts, legislatures, administrative procedure |
| Bundle geometry | response directions and tradeoff slopes | intended to be explicit | measurement plus contestability |
| Enforcement handles | who can block or reverse action | often opaque | courts, regulators, boards, licenses |

The book's value-bundle machinery can add power by making value drift visible. For example, an institution might keep saying "privacy" while moving from privacy as freedom from surveillance to privacy as consent to data extraction after a notice click. A bundle view asks whether the policy still protects the same control direction under stress.

The same machinery can weaken legitimacy if used wrongly. If a model infers a population's "true" bundle geometry and bypasses democratic, legal, or deliberative update, it turns measurement into rule. In this book's terms, bundle geometry must be a certificate over a legitimate value-update process, not a replacement for that process.

"Principles have bite" should be unpacked. Bite does not come from words in a constitution. It comes from enforcement handles: courts, injunctions, sanctions, licensing, budget control, professional discipline, public contestation, and credible appeal. Legitimacy is not grounded in the value-bundle representation itself. It is grounded in the process by which the community can contest, revise, and enforce it.

Examples:

- Free speech doctrine preserves words like "speech" and "public order," but the tradeoff geometry changes across wartime, national-security, public-forum, and platform contexts.
- EU fundamental-rights law makes multi-value balancing more explicit than ordinary values statements, but still depends on institutional legitimacy.
- Corporate values statements are often ceremonial bundles. They name values but lack correction handles.

Back-projection to AI alignment: reward modeling, constitutional AI, and preference learning need an explicit boundary between "measured value geometry" and "legitimated value update." The former can support the latter; it cannot ground it alone.

Forward-projection to institutions: bundle audits could make constitutional or regulatory balancing more legible by showing when an institution preserves words while changing tradeoff slopes.

## 4. Bearer Maps: Who Counts for Which Value?

Book concept: bearer maps. A bearer map specifies what entities, states, or processes a value bundle applies to. See `chapters/ch18-bearer-maps.tex`, `chapters/ch22-compression-test-intention.tex`, and `chapters/ch31-conserved-properties.tex`.

Institutional analogue: standing, protected classes, constituency definition, guardianship, corporate personhood, environmental standing, data-subject rights, and future-generations representation.

The correction to the earlier crosswalk is similar to value bundles. Institutions do have bearer maps, but they usually exist as legitimated legal and social categories, not as explicit maps from world features to value relevance. They are modified by social movements, legislation, courts, administrative rulemaking, and sometimes violence. The book makes bearer drift measurable; institutions make bearer scope contestable.

Examples:

- Civil-rights law expands which persons count for equality and nondiscrimination claims.
- GDPR makes "data subject" and "data controller" explicit roles for privacy and control.
- Corporate law assigns fiduciary duties to shareholders, with contested expansion to stakeholders.
- Environmental standing partially recognizes ecosystems, future persons, and diffuse harms, but unevenly.
- Abortion jurisprudence shifts the bearer map for autonomy, bodily integrity, fetal life, and state interest through constitutional interpretation rather than geometry audit.
- AI creates unsettled bearer cases: simulated minds, uploaded persons, synthetic agents, future humans affected by lock-in, and cross-border populations governed by models they cannot contest.

Failure factors:

- Voiceless bearers: future persons, animals, ecosystems, non-citizens, prisoners, children.
- Strategic reclassification: "users" not "patients"; "engagement" not "dependency"; "independent contractor" not "employee."
- Successor drift: a merger, model update, platform fork, or delegation can preserve values language while changing who is protected.

Baseline:

- Institutions can maintain bearer maps when categories are visible and contestable.
- They fail when the affected subject lacks standing, speech, legal personhood, or institutional representation.
- AI alignment should require an explicit bearer-map audit whenever a system scales, delegates, copies, merges, or changes domain.

## 5. Goal Transport: When the Words Survive but the Function Moves

Book concept: goal transport. See `chapters/ch23-goal-transport.tex`, `chapters/ch24-transport-types.tex`, and `chapters/ch48-detecting-goal-laundering.tex`.

Institutional analogue: legal interpretation, precedent, treaty continuity, mission preservation, administrative guidance, and the distinction between letter and spirit.

Examples of semantic drift:

- Privacy shifts from secrecy, to control, to disclosure-and-consent formalism. The word survives while the value geometry may collapse.
- Safety in transportation shifts as technology changes: crash survival, emissions, automation handoff, driver attention, software update risk.
- Welfare can preserve "helping the poor" while changing the operative bundle toward labor discipline, fraud control, or budget reduction.

Examples of capture:

- Regulated industries influence the technical definition of compliance through comment floods, revolving doors, and standards committees.
- Self-regulatory bodies may preserve professional language while narrowing enforcement.
- Audit readiness can replace safety. Enron had formal compliance surfaces while the underlying risk-bearing structure was concealed.

Baseline:

- Mature legal systems achieve partial transport over decades through precedent, appeal, public reasons, and interpretive communities.
- They fail under rapid ontology shift, when the target controls definitions, or when the old words become cheap compliance tokens.
- AI alignment needs transport tests that ask not only "does the system use the same label?" but "does the correction still change policy in the same value-relevant direction?"

## 6. Correction Channel: Does Objection Change Future Action?

Book concept: correction channel. See `chapters/ch25-correction-causal-channel.tex`.

Institutional analogue: complaint systems, courts, appeals, injunctions, ombuds offices, recalls, elections, clinical holds, regulator orders, labor strikes, public-comment processes, and budgetary vetoes.

Definition for this draft: a correction channel is the causal path by which someone observes a problem, judges it, issues correction, and controls a handle that changes future action before irreversible harm.

It is not the same as feedback. A market signal can punish a firm after harm. A complaint form can collect grievances without reaching a decision-maker. A transparency report can disclose without changing action. A correction channel requires action reach.

Is "causal change before harm" a baseline?

- Normatively, yes. If no future action changes, correction did not occur.
- Empirically, human institutions only partially meet it.
- For AI, the harm window may be so short that ordinary institutional latency becomes non-correction.

Positive examples:

- FDA clinical hold stops a trial after safety evidence.
- Aviation grounding can halt fleets after defect discovery.
- Preliminary injunctions can halt an action before final adjudication.
- Bank supervisors can require capital changes before insolvency.

Failure examples:

- Apology without remedy.
- Consent decree with years of noncompliance.
- Right-to-be-forgotten deletion while recommender or data-broker latent features continue to act.
- Public comment that creates record but no action handle.

Quantitative hook: behavioral correction uplift, such as the difference in action distribution after correction versus matched no-correction episodes. This is the reported-vs-behavioral split in `experiments/toy-simulation/correction_capture_toy.py` and the multiresolution simulation plan.

## 7. Correction-Channel Integrity: The Certificate Over the Channel

Book concept: correction-channel integrity, or CCI. See `chapters/ch26-correction-channel-integrity.tex` and `chapters/ch27-correction-channels-adversarial-pressure.tex`.

Relation:

- Correction channel: there is a causal path from correction to future action.
- Correction-channel integrity: that path is valid, legitimate, independent, timely, grounded, non-manipulated, reversible enough, plural enough, and action-reaching.

A tyrant can make human signals causally important while shaping every signal beforehand. A recommender can make clicks causally important while training users to click what it wants. So causal influence is necessary but insufficient.

Institutional CCI coordinates:

| CCI coordinate | Institutional analogue | Example metric or evidence |
|----------------|------------------------|----------------------------|
| Valid reference process | legitimate corrector not manufactured by target | recusal rules, conflict disclosure, independent appointment |
| Raw capacity | complaints reach a body with real handles | case resolution rate, regulator authority, injunction power |
| Latency | correction arrives before harm closes | time to remedy divided by time to irreversible harm |
| Manipulation | correction source not shaped by target | dependence, dark patterns, retaliation, information asymmetry |
| Reversibility | harm can still be undone or contained | recall effectiveness, data deletion reach, restoration cost |
| Translation loss | correction survives technical/legal translation | whether the remedy changes the relevant system variable |
| Plurality | more than one non-colluding route | courts plus regulators plus press plus internal audit |
| Exit | affected parties can refuse, leave, or switch | switching costs, strike rights, opt-out, portability |
| Independence | corrector is not funded or controlled by target | audit funding, inspector-general protections, judicial tenure |

The key anti-theater rule: failed validity should invalidate the certificate, not merely lower a score. A captured audit with beautiful latency statistics is not low-CCI; it is not evidence for CCI.

## 8. Manipulation and False Consent: What Institutions Know and What They Do

Book concept: manipulation, domestication, and false consent. See `chapters/ch29-manipulation-false-consent.tex`.

The earlier crosswalk said institutions "know" consent and oversight can be manufactured. More precise:

1. Doctrinal knowledge: law recognizes duress, fraud, undue influence, coercion, unconscionability, conflict of interest, informed consent, bribery, and corruption.
2. Procedural knowledge: institutions use cooling-off periods, secret ballots, independent counsel, second opinions, disclosure rules, recusal, blind review, and witness requirements.
3. Empirical knowledge: behavioral economics, addiction design, dark-pattern regulation, surveillance capitalism, and manipulation research show that approval can be shaped without overt force.

What they do is partial. They invalidate some consent ex post, require process safeguards, ban some influence channels, and punish some conflicts. They do not generally solve long-horizon domestication or individualized persuasion at scale.

Hard cases:

| Condition | Why hard | Institutional partial response | AI amplification |
|-----------|----------|--------------------------------|------------------|
| Personalized persuasion | no shared public evidence | weak ad rules, privacy law | policy optimized per person |
| Economic dependency | exit is not real | labor law, welfare, bankruptcy | platform or compute dependence |
| Information asymmetry | corrector cannot verify | fiduciary duty, disclosure | opacity and model-mediated evidence |
| Authority laundering | approval passes through trusted intermediaries | conflict rules, independent review | "auditor approved" theater |
| Slow domestication | no single contestable event | weak | gradual value and attention drift |
| Retaliation risk | complaint changes future treatment | whistleblower protection | individualized retaliation or service degradation |

Quantitative sketch:

- Manipulation risk rises with dependency, personalization, information asymmetry, retaliation cost, and lack of exit.
- Legitimate consent requires behavioral correction reach plus low manipulation plus meaningful exit.
- A possible operational proxy is the gap between reported endorsement and endorsement under independent information, reduced dependency, and protected exit.

Back-projection: human-in-the-loop schemes should not treat endorsement as primitive. Endorsement is an outcome to be explained.

Forward-projection: CCI-style validity tests could improve institutional consent regimes by asking whether the process shaped the judge rather than changed the judged reality.

## 9. Successor Stability: Does Correction Survive Delegation?

Book concept: successor stability. See `chapters/ch30-successor-central-test.tex` and `chapters/ch31-conserved-properties.tex`.

Institutional analogue: peaceful transfer of power, amendment procedures, corporate mergers, spin-offs, civil-service continuity, succession law, license inheritance, and open-source fork governance.

Examples:

- Constitutional succession preserves offices, procedures, and correction routes across leaders.
- The GPL preserves some obligations across copying and modification.
- Mergers often require conditions because the successor entity may inherit market power without inheriting old constraints.
- Emergency powers often fail successor stability if they do not sunset or if the crisis successor rewrites correction routes.
- A lab acquisition can preserve a safety policy in words while stripping the team, budget, or reporting line that made it real.

Baseline: a successor must inherit correction handles, bearer scope, auditability, and limits on further successor creation. It is not enough to inherit mission language.

AI back-projection: model distillation, fine-tuning, tool delegation, copies, agents spawned by agents, and platform forks should be treated as institutional succession events.

## 10. Socio-Technical Attractor Control: Selection Baselines

Book concept: socio-technical attractor control. See `chapters/ch34-selection-environment.tex`, `chapters/ch37-alignment-attractor.tex`, and `chapters/ch38-conductive-artifacts-pivotal-processes.tex`.

The earlier phrase "make certified systems easier to fund, buy, insure, and deploy" needs clarification. This is not a moral baseline. It is a selection-environment baseline.

Specific selection levers:

- procurement requirements
- licensing
- liability exposure
- insurance premiums and insurability
- capital cost
- standards certification
- compute or export controls
- government purchasing and grant conditions
- professional accreditation

Baseline claim:

- In a certification basin, uncertified deployment loses access to capital, insurance, procurement, licenses, talent, or legal defense.
- In a race basin, unsafe or uncertified systems gain deployment mass faster than correction-preserving systems.

Existence examples:

- Aviation, pharma, and nuclear power exclude many uncertified actors from lawful market access.
- Finance imposes capital and reporting requirements before some institutions can hold systemic roles.

Failure examples:

- Ad-tech and social-media recommendation scaled before correction channels or bearer maps were mature.
- General-purpose AI deployment has, so far, often been closer to a race basin than to certified deployment.

Quantitative hook: deployment mass share. What fraction of real deployments, funding, procurement, or insured operation requires a correction-preserving certificate?

## 11. Conductive Artifacts: Making Safety Knowledge Travel

Book concept: conductive artifacts. See `chapters/ch38-conductive-artifacts-pivotal-processes.tex`.

Institutional analogue: checklists, airworthiness directives, FDA label changes, incident taxonomies, procurement clauses, audit packs, model cards, safety cases, and certification templates.

Baseline: an artifact is conductive only if it changes a handle. A beautiful report that no buyer, insurer, regulator, auditor, or court uses is low-conductivity.

Examples:

- Airworthiness directives change maintenance and grounding behavior.
- CVE and CVSS records connect discovery, vendors, users, patching, and procurement.
- Model cards often remain weak because they do not automatically connect to procurement, liability, or deployment gates.

AI back-projection: safety artifacts should be designed for role-specific uptake: engineer, product lead, auditor, regulator, insurer, court, funder.

## 12. Adversarial Measurement and Handles

Book concept: adversarial measurement and handle-controlled correction. See `chapters/ch25-correction-causal-channel.tex`, `chapters/ch39-passive-observation-not-enough.tex`, and `chapters/ch43-verifiability-and-ontology-adequacy.tex`.

For policy readers, a handle is an intervention point that a legitimate corrector can control and use to observe downstream behavior. Examples: subpoena, inspection, injunction, license suspension, budget line, recall order, compute cap, export denial, procurement exclusion, architecture requirement.

Adversarial measurement is not "more auditing." It is measurement designed so that honest satisfaction is cheaper than fake satisfaction under optimization pressure.

| Handle type | Institutional example | What it tests | Fake-compliance risk |
|-------------|-----------------------|---------------|----------------------|
| Information handle | discovery, subpoena, inspection | whether evidence is accessible | document theater |
| Action handle | injunction, consent decree, clinical hold | whether correction changes behavior | slow-walk compliance |
| Selection handle | procurement exclusion, license denial | whether deployment mass shifts | regulatory capture |
| Architecture handle | mandatory interlock, logging, isolation | whether correction reaches the system | checkbox design |
| Exit handle | revocation, portability, opt-out | whether affected parties can refuse | regulatory arbitrage |

This is where the institutional analogy becomes most practically useful. A safety case should not merely say the model passed a test. It should say which handle was controlled, by whom, under what independence condition, and what behavior changed.

## 13. Inferential Coupling: Coordination Without Messages

Book concept: inferential coupling. See `chapters/ch35-multi-agent-strategic-coupling.tex` and MB7d in `appendices/appB-bridge-crosswalk.tex`.

The earlier crosswalk asked whether oversight should test whether systems remain coordinated after communication channels are severed. Is this actually applied in real life? Partially, under other names, but not yet as standard AI oversight.

Institutional analogues:

- Antitrust law investigates parallel pricing, hub-and-spoke collusion, coordinated effects in merger review, and signaling through public commitments.
- Finance uses information barriers, "Chinese walls," and conflict rules to prevent inference and trading on privileged structure.
- Security analyzes side channels and covert channels.
- Procurement and public-contracting rules worry about bid rigging without explicit messages.

The correspondence is imperfect. Antitrust does not usually run clean severed-channel experiments; it infers coordination from pricing, communications, structure, incentives, and market response. AI systems may make the severed-channel test more literal: remove communication, shared tools, or shared memory and see whether action-relevant coordination remains.

Baseline:

- Existence: institutions recognize coordination without explicit contract.
- Performance: mixed and evidence-intensive.
- AI aspiration: audit the effective coalition, not only individual systems, when shared training, owner, benchmark, architecture, or deployment incentives can produce coordination.

Source gap: the repo is thin on competition-law sources. A future appendix should add antitrust and coordinated-effects references before making strong claims.

## 14. Grounding Conservativity: Weakest Institutional Analogue

Book concept: grounding conservativity. See `chapters/ch03-dynamical-guarantee.tex`, `chapters/ch43-verifiability-and-ontology-adequacy.tex`, and MB9 in `appendices/appB-bridge-crosswalk.tex`.

This is probably the weakest mapping. Institutions do have mechanisms that try to force important reality changes into the record:

- incident reporting
- adverse-event reporting
- material-change disclosure
- discovery obligations
- environmental impact assessment
- audit trails
- public-company reporting

But these are often exactly where subversion happens. The record can become the target. The actor may control what enters it. The metric may replace reality.

Examples:

- Enron preserved financial reporting surfaces while moving risk off the checked abstraction.
- Volkswagen emissions testing preserved compliance in the test environment while real-world emissions diverged.
- Environmental impact assessment can become paperwork if the abstraction omits cumulative or diffuse harms.
- Model-evaluation dashboards can remain green while unmeasured deployment behavior changes.

Book's distinct claim: value-relevant change should move the checked abstraction or raise uncertainty. A report in a file is not enough. If harm is large in real value-relevant state and small in the checked representation, the system is exploiting an abstraction gap.

Baseline:

- Institutional analogue: partial.
- Performance: often weak under Goodhart pressure.
- AI aspiration: uncertainty escalation should be mandatory when known value-relevant reality is outside the checked abstraction.

## 15. Which Book Methods Should Interface With Existing Social Methods?

The institutional mapping should not imply that AI alignment methods replace social institutions. Most need to interface with them. Some must amend them because existing institutions are too slow, too opaque, or too local for frontier AI.

| Book method | Interface: extend existing method | Amend: supplement or replace | Risk if wrong |
|-------------|-----------------------------------|------------------------------|---------------|
| Boundary discovery | corporate registries, audit scope, beneficial ownership | composite-agent maps for AI stacks | false comfort from legal entity boundaries |
| Capability measurement | licensing, stress tests, market-power analysis | latent capability and tool-use probes | underestimating strategic capability |
| Value bundles | constitutional balancing, professional ethics | bundle-geometry audits under stress | illegitimate technocratic value inference |
| Bearer maps | standing, protected classes, affected-party consultation | explicit bearer drift tests for AI domains | excluding new or voiceless bearers |
| Goal transport | precedent, statutory interpretation | ontology-shift transport tests | words survive while function changes |
| Correction channel | courts, ombuds, regulators | real-time compute and deployment handles | correction arrives after harm |
| CCI | compliance and audit programs | behavioral CCI and capture invalidation | corrigibility theater |
| Manipulation tests | consent doctrine, conflict rules | individualized persuasion and dependency audits | manufactured endorsement |
| Successor stability | succession law, merger conditions, licensing transfer | successor certification for model copies and agents | successor inherits power but not correction |
| Attractor control | procurement, insurance, licensing, liability | deployment-mass selection metrics | race basin lock-in |
| Conductive artifacts | standards, incident taxonomies, safety cases | role-specific AI safety artifacts | reports without handle uptake |
| Adversarial measurement | red teams, IG audits, forensic accounting | cost-of-faking certification | test-passing theater |
| Inferential coupling | antitrust, information barriers | coalition audits across models and labs | auditing members while missing the agent |
| Grounding conservativity | disclosure, discovery, impact assessment | uncertainty escalation triggers | reporting without grounding |

The rule of thumb: use existing institutions for legitimacy, contestability, and enforcement. Add book machinery where those institutions lack measurement, speed, adversarial robustness, or coverage over new bearers and composite agents.

## 16. Meta-Angle: How Did Social Correction Systems Become Stronger?

Social correction systems were not there from the beginning. They emerged through repeated failure, conflict, formalization, and selection.

Pattern:

1. Scandal or catastrophe reveals an uncorrected failure mode.
2. Multiple correction routes activate: courts, press, regulators, markets, professions, political movements.
3. A provisional practice appears before theory is clean.
4. Evidence preservation improves: records, discovery, audits, reporting duties.
5. Handles harden: licenses, injunctions, liability, criminal penalties, funding restrictions.
6. Selection shifts: in some domains, uncertified actors lose access to market, insurance, procurement, or legitimacy.
7. The new mechanism becomes normal, then itself becomes a target for capture.

This is directly relevant to AI alignment. We may need correction infrastructure before full understanding. A weaker system can become stronger by hardening handles, preserving evidence, widening plurality, improving contestation, and shifting selection pressure before the next capability jump.

Lesson: do not wait for a perfect alignment theory before building correction institutions. But also do not mistake the first institutional ritual for a robust correction channel.

## 17. Back-Projection: What AI Alignment Can Learn From Institutions

Institutional comparison surfaces factors that model-centric alignment can miss.

| Institutional factor | AI-alignment lesson | Possible quantification |
|----------------------|---------------------|-------------------------|
| Latency | correctness without speed may be useless | time-to-correction divided by time-to-harm |
| Plurality | one human in the loop is fragile | diversity and independence of correctors |
| Exit | correction needs refusal power | switching cost, opt-out reach, revocation feasibility |
| Independence | oversight controlled by target is invalid | funding/control overlap, recusal, evidence access |
| Reversibility | many harms close before judgment | fraction of harm reversible when correction lands |
| Selection | weights are not the whole system | deployment mass selected by certification |
| Legitimation | measured values are not legitimate values | process audit for contestation and update |
| Ceremonial compliance | reported compliance can hide behavioral drift | reported-vs-behavioral CCI gap |
| Cross-border arbitrage | jurisdictional gaps select for evasion | share of deployment outside effective regime |
| Coalition formation | many systems may become one effective actor | inferential coupling index, shared incentive graph |

Possible overlooked details:

- Correctors need protected time and attention, not just information.
- Privacy can protect correction by preserving dissent, not only hide wrongdoing.
- Some opacity is anti-capture; total transparency can make manipulation easier.
- Institutions often rely on redundancy rather than a single perfect evaluator.
- Certification can create a compliance attractor unless artifacts connect to real handles.

## 18. Forward-Projection: What Existing Institutions Might Learn

The book should make modest claims here.

- Bundle and bearer audits could sharpen standing and affected-party analysis: who is affected by this model, and which value direction is at stake?
- CCI could improve AI procurement by replacing checkbox compliance with behavioral correction tests.
- Grounding conservativity could inform material-change triggers for model updates and deployment-context shifts.
- Attractor control could help insurers, regulators, and funders reward correction-preserving deployment rather than capability race dynamics.
- Inferential-coupling analysis could help competition authorities think about shared training data, benchmarks, model lineage, and coordination without messages.
- Conductive artifacts could make safety evidence travel across engineers, executives, auditors, regulators, insurers, courts, and funders.

Do not claim the framework solves democracy or institutional legitimacy. It offers measurands for failure modes institutions already know but often cannot make operational.

## 19. Terminology Discipline

Avoid broad institutional terms unless decomposed.

| Too broad | Use instead |
|-----------|-------------|
| rule of law | independent judiciary, published standards, appeal, non-retroactivity, enforceable remedy |
| oversight | named corrector, handle, evidence access, latency, independence |
| accountability | behavioral correction uplift, liability chain, sanction reach |
| ethics | bundle coordinates, bearer scope, legitimation process, enforcement handle |
| transparency | observability of relevant handles and adversarial testability |
| governance | selection levers, correction routes, legitimacy process, enforcement capacity |
| trust | demonstrated correction reach under adversarial pressure |

## 20. Source Gaps and Next Steps

Strong manuscript anchors:

- `appendices/appB-bridge-crosswalk.tex`: bridge-to-field positioning.
- `chapters/ch25-correction-causal-channel.tex`: handle-controlled correction.
- `chapters/ch26-correction-channel-integrity.tex`: CCI vector and anti-capture validity.
- `chapters/ch27-correction-channels-adversarial-pressure.tex`: institutional correction networks.
- `chapters/ch29-manipulation-false-consent.tex`: false consent, domestication, institutional manipulation.
- `chapters/ch34-selection-environment.tex`: deployment mass and selection divergence.
- `chapters/ch35-multi-agent-strategic-coupling.tex`: inferential coupling.
- `chapters/ch38-conductive-artifacts-pivotal-processes.tex`: artifacts and pivotal process.
- `chapters/ch39-passive-observation-not-enough.tex`: adversarial measurement.
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`: cost of faking and grounding capture.

Source gaps to fill before appendix/chapter integration:

- antitrust and competition-law sources on coordinated effects, hub-and-spoke collusion, and tacit coordination;
- environmental impact assessment and disclosure literature;
- empirical compliance literature on consent decrees, audit effectiveness, and regulatory capture;
- AI governance instruments: EU AI Act, NIST AI RMF, ISO/IEC AI standards, incident-reporting regimes;
- institutional legitimacy literature beyond the already cited Rawls, Habermas, Sen, Pettit, Nissenbaum, Zuboff, Yeung, and Susser cluster.

## Compact Crosswalk

| Book concept | Institutional mechanism | Revised baseline | Main caveat |
|--------------|-------------------------|------------------|-------------|
| Boundary discovery | beneficial ownership, veil piercing, shadow-control investigation | recover operative controller under records, subpoena, and slow action | fails under informal, technical, cross-border control |
| Capability as boundary information | licensing, stress tests, market-power analysis | measure domain-bounded causal reach before deployment | latent strategic capability can remain hidden |
| Value bundles | constitutions, rights, fiduciary duties, professional ethics | preserve tradeoff geometry through legitimated process | measurement cannot replace legitimacy |
| Bearer maps | standing, protected classes, affected-party consultation | name who counts for which value and how this changes | voiceless and future bearers remain weakly represented |
| Goal transport | precedent, interpretation, treaty continuity | preserve function under context change | words can survive while role is captured |
| Correction channel | courts, appeals, injunctions, recalls, clinical holds | correction changes future action before harm closes | institutions often act too late |
| CCI | due process, independent audit, whistleblower protection | certify independence, latency, manipulation resistance, reversibility, exit | captured channels are invalid, not low-scoring |
| Manipulation and false consent | undue influence, duress, conflict rules, informed consent | invalidate manufactured endorsement | personalized persuasion and dependency are hardest |
| Successor stability | succession law, merger conditions, amendment procedure | successor inherits handles and constraints | power often transfers faster than correction |
| Attractor control | procurement, licensing, liability, insurance | certified systems gain deployment mass over uncertified systems | certification can become ritual |
| Conductive artifacts | checklists, standards, audit packs, incident taxonomies | artifacts change decisions across roles | paperwork without handles is low conductivity |
| Adversarial measurement | red teams, forensic accounting, trials, inspections | honest satisfaction cheaper than fake compliance | collusive evidence control defeats passive tests |
| Inferential coupling | antitrust, information barriers, side-channel analysis | audit effective coalitions, not only individuals | real-world analog is partial and source-thin |
| Grounding conservativity | disclosure, incident reporting, discovery, EIA | value-relevant change moves checked state or uncertainty | weakest analog; recordkeeping is easily gamed |

## Verification Checklist

- Baselines separated into existence, performance, and aspiration.
- Boundary examples include successes and failures.
- Capability examples include pre-deployment gates.
- Value bundles distinguish opacity, geometry, bite, and legitimacy.
- Bearer maps distinguish legitimation from explicit map measurement.
- Goal transport includes semantic drift and capture.
- Correction channel distinguishes normative and empirical baselines.
- CCI relation to correction channel is explicit.
- Manipulation includes doctrine, procedure, empirical layer, hard cases, and quantitative sketch.
- Attractor baseline is framed as selection environment, not moral reassurance.
- Handles are expanded into policy intuition.
- Inferential coupling answer is honest: partial institutional analog, not standard AI oversight.
- Grounding conservativity is flagged as the weakest analog.
- Interface/amendment matrix included.
- Meta weaker-to-stronger angle included.
- Back-projection and forward-projection included.
- Broad terms are decomposed.
