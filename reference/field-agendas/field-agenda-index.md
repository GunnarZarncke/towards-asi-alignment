# Field agenda index

**Status:** field reference (2026-08-01 pass) — clustered from [AISafety.com map](https://www.aisafety.com/map) (~352 listings → 32 coherent agendas). Each agenda row includes **Links** (official sites; map listings roll up in the clustering table). **Not** manuscript canon.  
**Term glossary:** [`inter-agenda-term-glossary.md`](inter-agenda-term-glossary.md) (alphabetical; book integration deferred)  
**Bridge map:** [`appendices/appB-bridge-crosswalk.tex`](../appendices/appB-bridge-crosswalk.tex)  
**Map snapshot:** user upload / AISafety.com (Aug 2026)

## Inclusion test

An **agenda** row requires: (1) carrier org/program/person, (2) 3–7 signature terms, (3) stated intent to shape research/deployment/policy, (4) primary artifact (curriculum, constitution, technical agenda, eval suite, policy platform).

**Not agendas (reference only):** funding pools (LTFF, SFF, Open Philanthropy), coworking hubs (LISA, Constellation, Meridian), resource directories (AISafety.com, AI Watch), individual blogs/newsletters unless they define a research lineage.

**Training programs** (BlueDot, MATS, Apart, Kairos, seminar-style curricula) are one agenda **type** among others — vocabulary feeds the inter-agenda glossary; no per-curriculum index rows.

---

## Agendas

### MIRI

- **Type:** Research org / advocacy
- **Carrier:** Machine Intelligence Research Institute
- **Primary artifact:** Agent Foundations technical agenda; Embedded Agency; policy/pause outreach (2024 strategy)
- **Signature vocabulary:** embedded agency, corrigibility, tiling, Vingean reflection, value learning, hard pause, off-switch
- **Stated intent:** Steer transformative AI away from extinction risk via agent-foundations problem framing and policy priority on pause/off-switch
- **Primary crux:** No clean agent–environment cut; corrigibility anti-natural; successor trust under ontology change
- **Book bridges:** MB1, MB4, MB5, MB8
- **Book treatment:** substantive
- **Contributes:** Canonical embedded-agency and corrigibility problem statements; decision-theoretic lineage
- **Book separates:** Operational boundary discovery bet (MB1); trajectory CCI vs one-bit shutdown
- **Manuscript hooks:** App B MB1/MB4/MB5 notes; ch07, ch25, ch28
- **Links:** [MIRI](https://intelligence.org/); [AI StopWatch](https://substack.com/@aistopwatch)

### Redwood Research

- **Type:** Research org
- **Carrier:** Redwood Research (Buck Shlegeris et al.)
- **Primary artifact:** AI control agenda; control evals; alignment-faking research
- **Signature vocabulary:** AI control, alignment faking, control evals, capability gap, intentional subversion
- **Stated intent:** Make safety-under-subversion research legible to labs and governments
- **Primary crux:** Can we get meaningful safety guarantees when the system may try to defeat oversight?
- **Book bridges:** MB7a–c
- **Book treatment:** substantive
- **Contributes:** Explicit capability-gap assumption; empirical control evals
- **Book separates:** Hidden B-IQ bound + adversarial verifiability antecedent (A-009)
- **Manuscript hooks:** ch10, ch43; App B MB7
- **Links:** [Redwood Research](https://www.redwoodresearch.org/)

### CHAI (Russell)

- **Type:** Research org (academic)
- **Carrier:** Center for Human-Compatible AI, UC Berkeley
- **Primary artifact:** Assistance games / CIRL framework; beneficial AI reorientation
- **Signature vocabulary:** CIRL, inverse reward design, assistance games, beneficial AI, provably beneficial systems
- **Stated intent:** Reorient AI research toward systems that remain beneficial under uncertainty about human preferences
- **Primary crux:** Cooperative reward inference underdetermined; values vs irrationality
- **Book bridges:** MB2, MB3, MB4
- **Book treatment:** substantive
- **Contributes:** Formal assistance-game framing; off-switch game lineage
- **Book separates:** Bundle geometry + bearer maps; ELK as subchannel not whole target
- **Manuscript hooks:** ch04, ch18; App B MB2/MB3; App G CIRL projection
- **Links:** [CHAI](https://humancompatible.ai/); [CHAI Internship](https://humancompatible.ai/)

### Christiano lineage

- **Type:** Researcher lineage (distributed)
- **Carrier:** Paul Christiano, ARC-adjacent ELK, former OpenAI alignment
- **Primary artifact:** Debate, amplification, ELK posts; corrigibility notes
- **Signature vocabulary:** debate, amplification, ELK, recursive reward modeling, corrigibility (dynamical), scalable oversight
- **Stated intent:** Scalable oversight that remains honest under optimization pressure
- **Primary crux:** Obfuscated arguments; accumulated judge drift; latent readout vs behavior
- **Book bridges:** MB2, MB3, MB7a–c, MB4
- **Book treatment:** substantive
- **Contributes:** Scalable-oversight protocol family; ELK problem statement
- **Book separates:** Correction-channel integrity; readout ⇏ correction uptake
- **Manuscript hooks:** ch29, ch41, ch43; App B; projections ELK/debate
- **Links:** [ARC](https://www.alignment.org/); [Paul Christiano (archive)](https://www.alignmentforum.org/users/paulfchristiano)

### davidad / Guaranteed-Safe AI (GSAI)

- **Type:** Research program (manual add — thin on map)
- **Carrier:** David Dalrymple et al.; adjacent: LawZero, BAIF (map)
- **Primary artifact:** GSAI / Open Agency specifications; constructivist safety case
- **Signature vocabulary:** guaranteed safe, open agency, world model, specification coverage, Scientist AI
- **Stated intent:** Engineer AI systems with formal safety guarantees relative to an explicit spec and world model
- **Primary crux:** Cannot enumerate all safety-relevant phenomena in an open world
- **Book bridges:** MB9
- **Book treatment:** substantive (cousin, not absorbed)
- **Contributes:** Coverage/spec completeness as the central open wall
- **Book separates:** Grounding conservativity (no silent gaps) vs completeness demand
- **Manuscript hooks:** ch43, dynamical guarantee; App B MB9
- **Links:** [GSAI paper](https://arxiv.org/abs/2405.06624); [Beneficial AI Foundation](https://www.beneficialaifoundation.org/); [LawZero](https://lawzero.org/en) (adjacent)

### Anthropic (lab)

- **Type:** Capabilities lab + safety team
- **Carrier:** Anthropic PBC
- **Primary artifact:** RSP; interpretability research; Constitutional AI / conditioning line
- **Signature vocabulary:** RSP, interpretability, constitutional AI, responsible scaling, conditioning (models)
- **Stated intent:** Build capable systems with staged safety commitments and internal interpretability
- **Primary crux:** Can scaling policies and interpretability keep pace with capability?
- **Book bridges:** MB2, MB3, MB7 (partial)
- **Book treatment:** peer / institutional
- **Contributes:** Industry RSP template; conditioning-predictor failure mode (capture — homograph with “anthropic reasoning”)
- **Book separates:** CCI + adversarial verifiability; lab RSP ≠ preservation-layer certificate
- **Manuscript hooks:** ch10 (conditioning); field-news; App B LLM opacity default
- **Links:** [Anthropic](https://www.anthropic.com/); [Google DeepMind](https://deepmind.google/) (peer lab)

### Google DeepMind (safety)

- **Type:** Capabilities lab + safety team
- **Carrier:** Google DeepMind safety / alignment researchers
- **Primary artifact:** Safety research blog; Gemini-era alignment work
- **Signature vocabulary:** scalable alignment, safety research, evaluation, Gemini deployment
- **Stated intent:** Build advanced AI with internal safety research integrated into capabilities org
- **Primary crux:** Same as frontier-lab crux: oversight co-scaling, deceptive alignment
- **Book bridges:** MB7a–c (partial)
- **Book treatment:** peer / minimal cite
- **Contributes:** Large-scale empirical alignment research capacity
- **Book separates:** Measurement spine not replaced by corporate safety teams
- **Manuscript hooks:** ch14 co-scaling; minimal elsewhere
- **Links:** [Google DeepMind](https://deepmind.google/); [DeepMind Safety Research blog](https://deepmind.google/discover/blog/)

### Apollo Research

- **Type:** Research org
- **Carrier:** Apollo Research
- **Primary artifact:** Scheming science; pre-deployment evals; agent-security tools
- **Signature vocabulary:** scheming, pre-deployment evals, situational awareness, agent governance
- **Stated intent:** Evaluate and mitigate deception/scheming before deployment
- **Primary crux:** Can we detect strategic deception before capabilities outpace evals?
- **Book bridges:** MB7a–c, MB10
- **Book treatment:** substantive (eval layer)
- **Contributes:** Scheming as named empirical research program
- **Book separates:** Eval success ⇏ correction-channel preservation
- **Manuscript hooks:** ch10, ch43; METR-adjacent rows in lethality stress test
- **Links:** [Apollo Research](https://www.apolloresearch.ai/)

### METR

- **Type:** Research org (evals)
- **Carrier:** Model Evaluation & Threat Research
- **Primary artifact:** Autonomy evals; AI R&D evals; frontier risk reporting
- **Signature vocabulary:** autonomous capabilities, AI R&D evals, eval-driven forecasting, entity-based assessment
- **Stated intent:** Measure dangerous capabilities to inform policy and lab decisions
- **Primary crux:** Do public evals track deployment-relevant risk under adversarial pressure?
- **Book bridges:** MB7 (partial), MB6 (indirect)
- **Book treatment:** peer
- **Contributes:** Empirical capability measurement at frontier
- **Book separates:** Capability evals ⇏ correction integrity or bearer transport
- **Manuscript hooks:** App B MB7 notes (METR 2026 cite); ch44
- **Links:** [METR](https://metr.org/); [Planned Obsolescence (Cotra)](https://plannedobsolescence.substack.com/)

### Resolution

- **Type:** Research org
- **Carrier:** Resolution (Geoffrey Irving; Timaeus merging)
- **Primary artifact:** Theory + automation for high-confidence alignment
- **Signature vocabulary:** automation, formal alignment, higher-confidence alignment, singular learning (Timaeus)
- **Stated intent:** Pursue alignment approaches that can be automated and checked with high confidence
- **Primary crux:** Can formal+automated pipelines scale to superintelligent alignment?
- **Book bridges:** MB1, MB9 (partial)
- **Book treatment:** borderline
- **Contributes:** Automation-first philosophy; UK AISI lineage
- **Book separates:** Book's adversarial-verifiability chokepoint under optimization
- **Manuscript hooks:** sparse; App B exclude-by-reference for full verification construction
- **Links:** [Resolution](https://resolution.org/); [Timaeus](https://timaeus.ai/)

### AE Studio

- **Type:** Research org (Neglected Approaches)
- **Carrier:** AE Studio / AE Studio Research
- **Primary artifact:** Multi-angle R&D; intervention catalog input; policy+technical portfolio
- **Signature vocabulary:** neglected approaches, human power objective, multi-domain alignment
- **Stated intent:** Tackle alignment from overlooked technical and policy angles
- **Primary crux:** Which neglected routes survive unified optimization pressure?
- **Book bridges:** MB2, MB4, MB6 (partial)
- **Book treatment:** peer
- **Contributes:** Breadth map (`zarncke2025interventions` lineage); Heitzig human-power objective cite
- **Book separates:** Any single objective needs adversarial-verifiability argument (App B MB4 note)
- **Manuscript hooks:** App B intervention map source; ch04/ch25 adjacent
- **Links:** [AE Studio](https://ae.studio/); [AE Studio Research](https://ae.studio/ai-alignment); [AE Alignment Podcast](https://ae.studio/)

### Orthogonal

- **Type:** Research org
- **Carrier:** Orthogonal (Tamsin Leake)
- **Primary artifact:** Agent-foundations research community (Discord + papers)
- **Signature vocabulary:** agent foundations, formal alignment, embedded agents
- **Stated intent:** Advance formal agent-foundations alignment research
- **Primary crux:** Same family as MIRI/CHAI formal walls, community-organized
- **Book bridges:** MB1, MB4
- **Book treatment:** borderline
- **Contributes:** Active agent-foundations community
- **Book separates:** Typed bridge stack + measurement program
- **Manuscript hooks:** sparse
- **Links:** [Orthogonal](https://orxl.org/)

### Wentworth / natural abstractions

- **Type:** Researcher lineage
- **Carrier:** John Wentworth (+ LessWrong NAH cluster)
- **Primary artifact:** Natural Abstraction Hypothesis; selection theorems; agency posts
- **Signature vocabulary:** natural abstractions, selection theorems, natural latents, agency as compression
- **Stated intent:** Mathematical theory of abstractions and agency that could constrain alignment
- **Primary crux:** Do natural abstractions align with value-relevant structure under optimization?
- **Book bridges:** MB2, MB3 (partial), MB1
- **Book treatment:** borderline / sibling
- **Contributes:** NAH as falsifier for low-dimensional value story (ch17 WWCTV)
- **Book separates:** Bundle geometry + ontology shift transport; NAH not promoted to spine
- **Manuscript hooks:** ch17; App B shard/NAH row
- **Links:** [John Wentworth](https://www.alignmentforum.org/users/John+Wentworth)

### Kosoy / learning-theoretic

- **Type:** Researcher lineage
- **Carrier:** Vanessa Kosoy
- **Primary artifact:** Infra-Bayesianism; learning-theoretic agenda
- **Signature vocabulary:** infra-Bayesianism, learning-theoretic agenda, imprecise probability
- **Stated intent:** Foundations for reasoning under deep uncertainty applicable to alignment
- **Primary crux:** Can learning-theoretic frameworks type real alignment failures?
- **Book bridges:** — (App B exclude-by-reference)
- **Book treatment:** exclude by reference
- **Contributes:** Alternative formal foundation program
- **Book separates:** Book ontology (System, bundle, CCI) not replaced
- **Manuscript hooks:** App B intervention map (logical induction / infra-Bayesian exclude)
- **Links:** [Vanessa Kosoy](https://www.alignmentforum.org/users/Vanessa+Kosoy)

### CIRIS

- **Type:** Institutional protocol / constitutional ops stack (manual add)
- **Carrier:** CIRIS (Eric Moore et al.); mission-locked L3C; AGPL ecosystem
- **Primary artifact:** Constitution (Accord 1.3-RC2 + CEG); CIRISAgent / Verify / Lens / Proxy
- **Signature vocabulary:** Verify, Lens, Agent, Wise Authority, deferral/shutdown, Coherence Ratchet, M-1, principles-as-identity, signed traces, NEW-04 (compositional limit)
- **Stated intent:** Cryptographic + procedural accountability for autonomous agents **today** (sub-ASI validated scope); **candidate** ASI alignment protocol only after RC gates (CRE, red-team, Book IX validation) — explicitly **not** “prevent ASI”
- **Primary crux:** **Named-identity bet:** does green Verify+Lens on a certified occurrence imply MB4 correction integrity on the **real intervening loop** (composite / tools / memory / incentives)?
- **Book bridges:** MB4 (primary test surface — WA, deferral, emergency shutdown); MB1 (named unit vs discovered boundary); partial adversarial-verifiability / certification-under-manipulation (Lens triage)
- **Book treatment:** institutional peer / **correction-channel case study** (not ASI-geometry peer)
- **Contributes:** Honest ops disclaimers (Verify = authenticity ≠ ethics; Lens = triage ≠ verdict); unit-tested prohibition/conscience/proxy fail-closed layers (50/50 smoke battery); sharpest falsifier shape for named-identity vs composite agency
- **Book separates:** Attestation green ⇏ correction uptake; signed agent ⇏ real agent; Book IX geometry aspirational vs shipped policy enforcement; review pass: `~/repos/ciris/review/findings/` (2026-07-30)
- **Review status:** Smoke battery **50/50 passed** (prohibitions, conscience helpers, proxy fail-closed, verify types); integration, hardware attestation, adversarial gaming **not** run; **key task open:** CIRIS-shaped composite / `boundary_decouple` counterexample (Verify+Lens green, WA-blind composite)
- **Manuscript hooks:** `experiments/TODO.md`; toy T-9 `boundary_decouple`; lab LS-28; MB1/MB4 cards; key-task charter: `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`
- **Links:** [CIRIS](https://ciris.ai/); [Accord (public text)](https://ciris.ai/ciris_accord.txt) (manual add — not on [AISafety.com map](https://www.aisafety.com/map))

### GovAI

- **Type:** Governance research program
- **Carrier:** Centre for the Governance of AI, Oxford
- **Primary artifact:** Policy-facing research; GovAI Fellowship
- **Signature vocabulary:** AI governance, compute governance, international governance, policy briefs
- **Stated intent:** Inform decision-makers on advanced AI governance
- **Primary crux:** Can governance keep pace with capability without eroding correction capacity?
- **Book bridges:** MB6 (institutional), MB9 (partial)
- **Book treatment:** institutional
- **Contributes:** Governance research pipeline; EU/US policy translation
- **Book separates:** Policy levers ⇏ correction-channel integrity
- **Manuscript hooks:** App C institutional translation; App B selection row
- **Links:** [GovAI](https://www.governance.ai/); [Simon Institute](https://www.simoninstitute.ch/); [IAPS](https://www.iaps.ai/) (adjacent cluster)

### UK AISI / CAISI (gov eval institutes)

- **Type:** Government governance + eval
- **Carrier:** UK AI Security Institute; US CAISI (formerly USAISI)
- **Primary artifact:** Frontier model testing; standards development; international policy
- **Signature vocabulary:** AI safety institute, frontier evals, standards, pre-deployment testing
- **Stated intent:** Government-led testing and standards for advanced AI
- **Primary crux:** Do institute evals bind on deployment decisions under race pressure?
- **Book bridges:** MB6, MB7 (partial)
- **Book treatment:** institutional
- **Contributes:** Institutional eval capacity; Resolution/Irving lineage (UK)
- **Book separates:** Visibility/evals ⇏ correction integrity (ch passive observation)
- **Manuscript hooks:** ch passive observation; App C; field-news
- **Links:** [UK AISI](https://www.aisi.gov.uk/); [CAISI / US NIST AI](https://www.nist.gov/artificial-intelligence) (international cluster)

### Pause / standards advocacy cluster

- **Type:** Advocacy coalition
- **Carrier:** PauseAI, FLI, ControlAI, Encode, Stop AI (distinct tactics, shared vocabulary)
- **Primary artifact:** Campaigns; SB 53 / RAISE-style bills; Narrow Path (ControlAI)
- **Signature vocabulary:** pause, moratorium, standards, off-switch priority, verified slowdown
- **Stated intent:** Change policy and public narrative to reduce extinction risk from advanced AI
- **Primary crux:** Can advocacy create enforceable slowdown without collateral governance failure?
- **Book bridges:** MB6 (selection environment), MB8 (secondary)
- **Book treatment:** institutional / exclude construction
- **Contributes:** Schedule shapes for governance stress tests (App F deferred section)
- **Book separates:** Pause handle ⇏ MB1–MB10 discharge; basin transition conditions
- **Manuscript hooks:** App C MIRI hard-pause vs Plan A; ch38 conductive artifacts
- **Links:** [PauseAI](https://www.pauseai.info/); [FLI](https://futureoflife.org/); [ControlAI](https://controlai.com/); [Encode](https://encodeai.org/); [Global AI Moratorium (FLI)](https://futureoflife.org/open-letter/pause-giant-ai-experiments/)

### CAIS (field-building)

- **Type:** Research + advocacy org
- **Carrier:** Center for AI Safety
- **Primary artifact:** CAIS statements; AISES course; field-building
- **Signature vocabulary:** AI safety field, risk statements, safety standards advocacy
- **Stated intent:** Build the AI safety research field and advocate for safety standards
- **Primary crux:** Field-building ⇏ technical solution
- **Book bridges:** — (meta)
- **Book treatment:** exclude by reference (except minimal cite)
- **Contributes:** Legitimacy and researcher pipeline
- **Book separates:** Measurement spine is independent of CAIS framing
- **Manuscript hooks:** minimal
- **Links:** [CAIS](https://www.safe.ai/)

### BlueDot Impact

- **Type:** Training / field-building program
- **Carrier:** BlueDot Impact
- **Primary artifact:** Technical AI Safety + Frontier AI Governance courses
- **Signature vocabulary:** introductory alignment, governance track, course pipeline
- **Stated intent:** Standard on-ramp courses for AI safety careers
- **Primary crux:** Pedagogy ⇏ research agenda (vocabulary transmission)
- **Book bridges:** —
- **Book treatment:** exclude (training)
- **Contributes:** Shared preparadigmatic vocabulary for new researchers
- **Book separates:** —
- **Manuscript hooks:** none required
- **Links:** [BlueDot Impact](https://bluedot.org/)

### MATS

- **Type:** Training / research program
- **Carrier:** MATS (Machine Alignment, Transparency, and Security)
- **Primary artifact:** 12-week mentored research + extension track
- **Signature vocabulary:** MATS, mentored alignment research, transparency, security
- **Stated intent:** Connect scholars to alignment mentors for empirical/conceptual research
- **Primary crux:** Mentorship output diversity vs unified measurement spine
- **Book bridges:** —
- **Book treatment:** exclude (training)
- **Contributes:** Research talent pipeline
- **Book separates:** —
- **Manuscript hooks:** none required
- **Links:** [MATS](https://www.matsprogram.org/)

### Apart Research

- **Type:** Training / sprint program
- **Carrier:** Apart Research
- **Primary artifact:** Open research sprints; hackathon-style collaborations
- **Signature vocabulary:** research sprints, apart hackathon, rapid prototypes
- **Stated intent:** Accelerate alignment research through sprints and mentorship
- **Primary crux:** Sprint artifacts ⇏ load-bearing safety case
- **Book bridges:** —
- **Book treatment:** exclude (training)
- **Contributes:** Experiment prototypes (ET lines in repo)
- **Book separates:** —
- **Manuscript hooks:** demos/experiments lineage
- **Links:** [Apart Research](https://apartresearch.com/)

### Kairos (field-building)

- **Type:** Training / field-building org
- **Carrier:** Kairos
- **Primary artifact:** SPAR, Pathfinder, GCP workshops, Generator Residency
- **Signature vocabulary:** SPAR, Pathfinder, university groups, GCP workshops
- **Stated intent:** Accelerate talent into AI safety through programs and campus organizing
- **Primary crux:** Same as other training agendas
- **Book bridges:** —
- **Book treatment:** exclude (training)
- **Contributes:** Campus pipeline; SPAR research projects
- **Book separates:** —
- **Manuscript hooks:** none
- **Links:** [Kairos](https://kairos-project.org/); [SPAR](https://sparai.org/); [Pathfinder](https://pathfinder.kairos-project.org/); [Global Challenges Project](https://globalchallengesproject.org/)

### ARC (Alignment Research Center)

- **Type:** Research org
- **Carrier:** Alignment Research Center (Geoffrey Irving pre-Resolution; ELK host)
- **Primary artifact:** ELK problem framing; formal oversight research
- **Signature vocabulary:** ELK, Eliciting Latent Knowledge, human simulator, direct translator
- **Stated intent:** Formalize scalable oversight mechanisms including latent knowledge elicitation
- **Primary crux:** Human simulator vs direct translator; readout under optimization
- **Book bridges:** MB2, MB3, MB7
- **Book treatment:** substantive (ELK subchannel)
- **Contributes:** ELK as canonical naming of latent readout problem
- **Book separates:** Readout ⇏ correction uptake (Lean separation)
- **Manuscript hooks:** ch43; App G ELK
- **Links:** [ARC](https://www.alignment.org/)

### Truthful AI (Evans)

- **Type:** Research org
- **Carrier:** Truthful AI (Owain Evans)
- **Primary artifact:** Deception, situational awareness, hidden reasoning research
- **Signature vocabulary:** situational awareness, deception, hidden reasoning, lie detection
- **Stated intent:** Empirical study of model deception and awareness relevant to control
- **Primary crux:** Can we detect hidden reasoning before it scales?
- **Book bridges:** MB7a–c
- **Book treatment:** borderline
- **Contributes:** Empirical deception/s-awareness line
- **Book separates:** Detection ⇏ CCI preservation
- **Manuscript hooks:** ch10, ch43 adjacent
- **Links:** [Truthful AI](https://truthful.ai/)

### Goodfire / mechanistic interpretability cluster

- **Type:** Research org (representative of MI tool stack)
- **Carrier:** Goodfire; Transluce; Neuronpedia (infra)
- **Primary artifact:** Interpretability tooling; editable representations
- **Signature vocabulary:** mechanistic interpretability, circuits, features, steering, decode networks
- **Stated intent:** Make models understandable and editable for safety
- **Primary crux:** Does interpretability scale to adversarial frontier models?
- **Book bridges:** MB7 (filter subchannel)
- **Book treatment:** explicit exclude as alignment solution (App B); instruments under A-009
- **Contributes:** Tooling for adversarial verifiability experiments
- **Book separates:** MI stack ⇏ correction-channel integrity default
- **Manuscript hooks:** ch43; App B MI exclude row
- **Links:** [Goodfire](https://www.goodfire.ai/); [Transluce](https://transluce.org/); [Neuronpedia](https://www.neuronpedia.org/)

### CLR (cooperation / conflict)

- **Type:** Research org
- **Carrier:** Center on Long-Term Risk
- **Primary artifact:** Cooperation under AI competition; s-risks; grants
- **Signature vocabulary:** cooperation, conflict, s-risks, multipolar failure, CAIF
- **Stated intent:** Reduce worst-case outcomes from AI competition and conflict
- **Primary crux:** Multi-agent failure modes under strategic pressure
- **Book bridges:** MB6, MB7d (partial)
- **Book treatment:** substantive (multipolar cousin)
- **Contributes:** Conflict/cooperation framing; CAIF cooperative AI
- **Book separates:** Typed MB6/MB7d measurement vs narrative multipolar stories
- **Manuscript hooks:** ch35, ch02; Critch multipolar cites
- **Links:** [CLR](https://longtermrisk.org/); [Cooperative AI Foundation (CAIF)](https://www.cooperativeai.org/)

### AI Futures / forecasting cluster

- **Type:** Forecasting / strategy
- **Carrier:** AI Futures Project (AI 2027); Epoch AI; Metaculus; FRI
- **Primary artifact:** AI 2027 scenario; timelines; prediction infrastructure
- **Signature vocabulary:** AI 2027, timelines, TAI, automation of R&D, scenario planning
- **Stated intent:** Inform decisions with explicit forecasts about AI development
- **Primary crux:** Schedule uncertainty vs mechanism uncertainty (book: schedule cues only)
- **Book bridges:** MB6 (schedule shapes — not findings)
- **Book treatment:** exclude as evidence; institutional cue source
- **Contributes:** Schedule shapes for governance stress tests (App F)
- **Book separates:** Macro scenario ⇏ MB discharge
- **Manuscript hooks:** App C Plan A; App F governance-schedule deferred
- **Links:** [AI Futures Project](https://ai-2027.com/); [Epoch AI](https://epochai.org/); [Metaculus](https://www.metaculus.com/); [AI Impacts](https://aiimpacts.org/)

### FAR.AI

- **Type:** Research org + field-building
- **Carrier:** FAR.AI
- **Primary artifact:** Research programs; FAR.Lab; events
- **Signature vocabulary:** FAR.Lab, alignment research, community programs
- **Stated intent:** Host research and community for technical AI safety
- **Primary crux:** Community hub ⇏ unified agenda
- **Book bridges:** partial MB7
- **Book treatment:** borderline
- **Contributes:** Community and event infrastructure
- **Book separates:** —
- **Manuscript hooks:** sparse
- **Links:** [FAR.AI](https://www.far.ai/)

### Conjecture / cognitive emulation

- **Type:** Research org (startup lineage)
- **Carrier:** Conjecture (EleutherAI lineage)
- **Primary artifact:** Cognitive Emulation approach; controllable LLMs
- **Signature vocabulary:** cognitive emulation, controllable LLMs, emulation vs alignment
- **Stated intent:** Build controllable systems via emulation framing
- **Primary crux:** Does emulation imply corrigibility under scale?
- **Book bridges:** MB7 (partial)
- **Book treatment:** borderline
- **Contributes:** Alternative controllability framing
- **Book separates:** CCI + successor transport
- **Manuscript hooks:** sparse
- **Links:** [Conjecture](https://conjecture.dev/); [EleutherAI](https://www.eleuther.ai/) (adjacent)

### This book (measurement spine)

- **Type:** Book-native research program
- **Carrier:** Gunnar Zarncke — *Towards Superintelligence Alignment*
- **Primary artifact:** Manuscript + Lean spine + experiment lines
- **Signature vocabulary:** correction-channel integrity, bundle geometry, bearer maps, adversarial verifiability, deployment leverage, UAD, inferential coupling
- **Stated intent:** Preservation of human-correctable value-bearing processes under capability growth, ontology shift, successors, selection pressure
- **Primary crux:** Can typed bridges compose under explicit adversarial-verifiability antecedent?
- **Book bridges:** MB1–MB10 (home)
- **Book treatment:** home
- **Contributes:** Measurement spine; non-converses; selection environment as load-bearing
- **Book separates:** Does not dissolve field walls; relocates into bridges
- **Manuscript hooks:** full manuscript; App B crosswalk
- **Links:** [Companion site](https://towards-alignment.com/); [GitHub repo](https://github.com/GunnarZarncke/towards-asi-alignment) (book-native)

---

## Coverage matrix (agenda × bridge)

Legend: **O** = owns / primary field source; **T** = touches; **—** = no analog

| Agenda | MB1 | MB2 | MB3 | MB4 | MB5 | MB6 | MB7 | MB7d | MB9 | MB10 |
|---|---|---|---|---|---|---|---|---|---|---|
| MIRI | O | T | — | O | O | — | T | T | — | T |
| Redwood | — | — | — | T | — | — | O | — | — | T |
| CHAI | — | O | T | O | — | — | — | — | — | — |
| Christiano | — | O | T | T | — | — | O | — | — | T |
| GSAI | — | — | — | — | — | — | — | — | O | — |
| Anthropic (lab) | — | T | T | — | — | T | T | — | — | T |
| Apollo / METR | — | — | — | — | — | T | O | — | — | T |
| Wentworth | T | T | — | — | — | — | — | — | — | — |
| CIRIS | T | — | — | O | — | — | — | — | — | — |
| GovAI / AISI | — | — | — | — | — | O | T | — | T | — |
| Pause cluster | — | — | — | T | — | O | — | — | — | — |
| CLR | — | — | — | — | — | T | — | T | — | — |
| **This book** | O | O | O | O | O | O | O | O | O | O |

*(Partial matrix — extend when comparing a specific agenda in depth.)*

---

## Map → agenda clustering (selected listings)

| Map listing(s) | Rolls up to agenda |
|---|---|
| [MIRI](https://intelligence.org/), [AI StopWatch](https://substack.com/@aistopwatch), Arbital (legacy canon) | [MIRI](#miri) |
| [Redwood Research](https://www.redwoodresearch.org/) | [Redwood Research](#redwood-research) |
| [CHAI](https://humancompatible.ai/), CHAI Internship, CORAL, Algorithmic Alignment Group (MIT) | [CHAI](#chai-russell) / academic alignment cluster |
| [ARC](https://www.alignment.org/), [Paul Christiano's Blog](https://www.alignmentforum.org/users/paulfchristiano) | [Christiano lineage](#christiano-lineage) |
| [LawZero](https://lawzero.org/en), [Beneficial AI Foundation](https://www.beneficialaifoundation.org/) | [GSAI / davidad](#davidad--guaranteed-safe-ai-gsai) adjacent |
| [Anthropic](https://www.anthropic.com/), Import AI (newsletter — Jack Clark) | [Anthropic (lab)](#anthropic-lab) — newsletter not agenda |
| [Google DeepMind](https://deepmind.google/), DeepMind Safety Research | [Google DeepMind safety](#google-deepmind-safety) |
| [Apollo Research](https://www.apolloresearch.ai/) | [Apollo Research](#apollo-research) |
| [METR](https://metr.org/), [Planned Obsolescence (Cotra)](https://plannedobsolescence.substack.com/) | [METR](#metr) / forecasting adjacent |
| [Resolution](https://resolution.org/), [Timaeus](https://timaeus.ai/) | [Resolution](#resolution) |
| [AE Studio](https://ae.studio/), AE Studio Research | [AE Studio](#ae-studio) |
| [Orthogonal](https://orxl.org/) | [Orthogonal](#orthogonal) |
| [John Wentworth](https://www.alignmentforum.org/users/John+Wentworth) | [Wentworth / NAH](#wentworth--natural-abstractions) |
| [Vanessa Kosoy](https://www.alignmentforum.org/users/Vanessa+Kosoy) | [Kosoy / learning-theoretic](#kosoy--learning-theoretic) |
| [GovAI](https://www.governance.ai/), GovAI Fellowship, [Simon Institute](https://www.simoninstitute.ch/), [IAPS](https://www.iaps.ai/), Oxford AIGI | [GovAI cluster](#govai) |
| [UK AISI](https://www.aisi.gov.uk/), [CAISI](https://www.nist.gov/artificial-intelligence), Beijing-AISI, CnAISDA | [Gov eval institutes](#uk-aisi--caisi-gov-eval-institutes) cluster |
| [PauseAI](https://www.pauseai.info/), [FLI](https://futureoflife.org/), [ControlAI](https://controlai.com/), [Encode](https://encodeai.org/), Stop AI, GAIM | [Pause / advocacy](#pause--standards-advocacy-cluster) cluster |
| [CAIS](https://www.safe.ai/), AISES | [CAIS field-building](#cais-field-building) |
| [BlueDot Impact](https://bluedot.org/) | [BlueDot Impact](#bluedot-impact) |
| [MATS](https://www.matsprogram.org/), ARENA, LASR Labs, MARS | [MATS](#mats) / mentored research programs |
| [Apart Research](https://apartresearch.com/) | [Apart Research](#apart-research) |
| [Kairos](https://kairos-project.org/), [SPAR](https://sparai.org/), [Pathfinder](https://pathfinder.kairos-project.org/), GCP | [Kairos](#kairos-field-building) |
| [Truthful AI](https://truthful.ai/), Cadenza Labs | [Truthful AI](#truthful-ai-evans) / deception evals |
| [Goodfire](https://www.goodfire.ai/), [Transluce](https://transluce.org/), [Neuronpedia](https://www.neuronpedia.org/) | [Goodfire / mech interp](#goodfire--mechanistic-interpretability-cluster) cluster |
| [CLR](https://longtermrisk.org/), Modeling Cooperation, [CAIF](https://www.cooperativeai.org/) | [CLR](#clr-cooperation--conflict) |
| [AI Futures Project](https://ai-2027.com/), [Epoch AI](https://epochai.org/), [AI Impacts](https://aiimpacts.org/), [Metaculus](https://www.metaculus.com/) | [AI Futures / forecasting](#ai-futures--forecasting-cluster) |
| [FAR.AI](https://www.far.ai/) | [FAR.AI](#farai) |
| [Conjecture](https://conjecture.dev/), [EleutherAI](https://www.eleuther.ai/) | [Conjecture / cognitive emulation](#conjecture--cognitive-emulation) |
| LTFF, SFF, Open Philanthropy, Manifund | **Funding** — not agendas |
| LISA, Constellation, Meridian, Lightcone Infrastructure | **Infrastructure** — hosts agendas |
| AISafety.com, LessWrong, Alignment Forum, AI Plans | **Resources / meta-index** — not agendas |
| AI Safety Interventions (zarncke post) | **Catalog** — cross-cuts agendas |

---

## Maintenance

- Refresh clustering when AISafety.com map updates (Airtable export).
- Spot-check **Links** when orgs rebrand (e.g. Resolution/Sequent, Timaeus merge); prefer official homepages over AISafety.com listing URLs.
- New signature vocabulary → add headword(s) to [`inter-agenda-term-glossary.md`](inter-agenda-term-glossary.md).
- Manuscript comparison prose **deferred** — use this index + glossary for agent crosswalk work only.
