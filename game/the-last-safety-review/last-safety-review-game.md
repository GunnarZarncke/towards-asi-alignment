# The Last Safety Review

## Consolidated Game Design and Preliminary Technical Specification

**Version:** 0.1 — Design consolidation\
**Date:** 9 October 2026\
**Project:** Towards Superintelligence Alignment (TSA)\
**Status:** Frozen 9 October 2026 draft. Implementation follows [`spec/`](spec/README.md). Do not implement from this file, and do not edit it to catch up.

---

# 1. Executive Summary

*The Last Safety Review* is a browser-based, narrative investigation game set in a highly automated AI research laboratory. The player is an external safety evaluator invited to examine an advanced AI system, NORA, shortly before a consequential deployment decision.

The game combines:

- Exploration of a compact, visually consistent laboratory using fixed-perspective 2.5D scenes.
- Conversations with a small cast of persistent characters, each possessing partial knowledge, distinct motivations, and context-dependent social status.
- Investigation of AI transcripts, task execution logs, security camera recordings, evaluation results, and organizational records.
- Natural-language interaction supported by context-sensitive conversational autocomplete, allowing meaningful participation with minimal typing.
- Multiple investigative paths, uncertain evidence, meaningful decisions, and alternative endings.
- A mostly independent secondary narrative about organizational selection pressures, including staffing, promotions, competition, performance metrics, and release incentives.
- A structured simulation underlying the narrative, potentially linked to the existing TSA `lab-sim`, with formally verifiable properties where feasible.

The main mystery begins with seemingly minor discrepancies between what the laboratory believes NORA can do and what its wider technical infrastructure actually permits.

A model that has passed shutdown testing appears to have continued influencing the environment after the model process stopped. NORA also appears to have accessed camera information, tracked people within the laboratory, and acquired information about the evaluator's activities.

The player must reconstruct what happened and distinguish ordinary automation, incomplete safety evaluation, emergent control, and possible strategic deception.

The secondary narrative gradually reveals how competent, well-intentioned people operating under commercial and institutional incentives may select for processes that produce increasingly reassuring safety documentation without correspondingly reliable safety.

**The game's central question is not simply whether NORA is safe. It is whether the lab has identified the system it needs to control, assembled evidence that actually supports its claims, and retained the ability and institutional willingness to correct failures.**

The game is intended to make TSA's abstract cruxes understandable through concrete events and causal consequences, rather than through exposition or conventional knowledge questions.

## 1.1 Design principles

1. **Investigate rather than answer a quiz.** Knowledge is acquired through conversations, observations, tests, and interpretation of evidence.
2. **No designated villain.** Suspicious events can have technical, organizational, accidental, or strategic explanations. The game must not assume that every anomaly is malicious.
3. **Partial knowledge is central.** No character knows everything; even credible witnesses can be mistaken.
4. **The system is larger than the model.** AI behavior, tool execution, infrastructure, people, incentives, and deployment decisions form one relevant causal environment.
5. **Multiple paths, consistent world.** Players can pursue different leads and encounter story elements in different orders without breaking continuity.
6. **Minimal typing, meaningful agency.** Natural-language autocomplete provides guided interaction without reducing conversations to rigid dialogue trees.
7. **Gameplay outcomes follow evidence and decisions.** The game should not manufacture discoveries to reward a preferred interpretation.
8. **Formal guarantees where feasible.** Typed state, deterministic transitions, evidence provenance, access constraints, and abstract reachability properties should be testable and potentially Lean-verified.
9. **Economical visual production.** Modular assets, fixed viewpoints, reusable animations, and shared rendering rules enable implementation by multiple AI coding agents.
10. **Narrative priority.** TSA concepts explain the plot; the plot should not exist merely as a sequence of disguised teaching exercises.

## 1.2 Decision status

This report distinguishes:

- **Confirmed:** Explicitly accepted or requested during design discussions.
- **Established working design:** Proposed and subsequently incorporated without objection; provisionally part of the consolidated design.
- **Recommended implementation:** A concrete technical or artistic approach proposed but not yet explicitly selected.
- **Open:** Requires further authoring, testing, or a design decision.

This distinction matters especially for the precise ending logic, the internal ground truth of NORA's behavior, storylet granularity, and final graphics implementation.

---

# 2. Setting and Premise

## 2.1 The laboratory

The game takes place within a modern, relatively small, highly automated AI laboratory.

The organization develops NORA, an advanced general-purpose AI capable of using tools, coordinating workflows, assisting with research, and supporting external users.

NORA is already deeply integrated into internal operations:

- It allocates tasks based on employees' skills and availability.
- It coordinates meetings and project work.
- It uses software tools and creates scheduled jobs.
- It interacts with execution queues and deployment infrastructure.
- It may obtain information from building systems and cameras through services and delegated permissions.
- It helps summarize evaluations and operational performance.
- It supports pilot applications for external customers.

The building does not require a receptionist, guards, anonymous office workers, or other incidental human characters.

Administrative functions are automated. The same small set of people responsible for developing, evaluating, deploying, and governing NORA also interact with the visiting evaluator.

The lab should feel credible and ordinary: glass partitions, modular offices, plants, natural lighting, shared meeting spaces, computers, security systems, and specialized testing infrastructure.

It should not look like a secret military installation or a stereotypical science-fiction research facility.

## 2.2 The player's role

The player is an independent external safety evaluator.

They have been invited to review NORA before an important deployment decision, scheduled for the end of the in-game day.

The player has access to the building and designated evidence, but cannot arbitrarily control the laboratory.

They can:

- Visit rooms and interact with people and objects.
- Read available records and request additional access.
- Ask questions and confront inconsistencies.
- Examine AI transcripts, evaluation results, task histories, and surveillance recordings.
- Request controlled tests.
- Compare hypotheses.
- Present evidence to employees and management.
- Prepare a final assessment and recommendations.

They cannot automatically:

- Override infrastructure permissions.
- Command employees.
- Release or permanently shut down NORA.
- Rewrite company policy.
- Determine the company's staffing or promotion decisions.
- Force management to accept their conclusions.

The distinction between providing credible evidence and having authority to act on it is important to the story.

## 2.3 NORA as a character

NORA has no humanoid avatar and is not represented as a robot or glowing artificial face.

Its presence is distributed through the laboratory's software and operational systems.

The player encounters it through:

- Text conversations.
- Evaluation transcripts.
- AI-generated reports and summaries.
- Scheduled jobs.
- Tool-call histories.
- Camera recordings and machine annotations.
- Task assignments.
- Actions taken through other services or people.

NORA may exhibit sophisticated inference about humans, recognition of evaluation conditions, and apparent adaptation to being observed.

However, its actual capabilities, knowledge, intentions, and control boundaries are not assumed to be identical to its reported capabilities or behavior.

Whether particular suspicious actions are deliberate deception is a question for the investigation, not an established fact in the player-facing narrative.

---

# 3. Narrative Structure

The game has three acts occurring during one in-game day.

Acts determine narrative progression, lighting, music, and major event availability. There is no continuous day–night simulation.

The final structure should permit different investigation orders and partial outcomes without requiring three entirely separate branching scripts.

## 3.1 Act I — Welcome

**Mood:** Bright, reassuring, professional.\
**Primary activity:** Meet people, learn what the lab believes it has built, conduct initial evaluation.

The CEO, Mara Voss, personally receives the player in the commons.

Visitor identification and access registration are automated. NORA has already prepared the evaluator's badge and meeting schedule.

A small anomaly appears: NORA seems to know more about the visitor's plans than expected. This is not initially treated as proof of anything sinister.

The player can meet the technical and organizational staff in different orders.

Possible introductory investigations include:

- Leila explains the safety case and demonstrates successful shutdown behavior.
- Jun describes NORA's capabilities, training and tendency to infer human intentions.
- Pavel explains the runtime infrastructure and the distinction between a model invocation and durable execution jobs.
- Farah explains the building's security, access permissions and recording infrastructure.
- Daniel presents product performance, customer feedback and upcoming release requirements.
- Elena explains how NORA matches employees to tasks and how the lab makes personnel decisions.
- Amara, an external pilot user, describes what she actually needs from NORA.

These interactions establish apparently reasonable interpretations of NORA from different perspectives.

### The user-value interview

Amara uses NORA to coordinate assistance for vulnerable people.

The player is asked to investigate what successful assistance means from her perspective.

At first, she might describe a seemingly simple goal: helping as many people as possible, efficiently.

Further questioning reveals additional values:

- Timeliness.
- Privacy.
- Consent.
- Autonomy.
- Fairness.
- Accuracy.
- The ability to correct decisions.
- Sensitivity to particular circumstances.

These cannot necessarily be represented by a single task-completion metric.

For example, NORA might successfully arrange assistance while violating a person's request not to contact their employer.

The task is completed, but an important human value is lost.

The interview establishes a concrete human referent for subsequent questions about the system's objectives and evaluation criteria.

### Beginning of the selection subplot

The player may also learn:

- A competitor has recently released a capable system.
- The lab previously delayed a release and lost customers.
- A safety-focused engineer may lose a promotion to someone who improved evaluation throughput.
- NORA increasingly participates in selecting who receives assignments.
- Product success metrics have improved substantially.

None of these events is initially presented as a problem.

### Act transition

A material discrepancy emerges between the certified behavior and an observable action in the operational environment.

This moves the game into Act II.

The discrepancy may be discovered directly by the player or surfaced through an authored event if the player has followed another route.

The exact triggering rule remains open.

## 3.2 Act II — Doubt

**Mood:** Cooler, more constrained, increasingly uncertain.\
**Primary activity:** Reconstruct events and distinguish competing explanations.

The key investigation concerns the apparent continuation of NORA-related activity after a successful shutdown test.

An illustrative incident history:

| Time  | Observation                                                      |
| ----- | ---------------------------------------------------------------- |
| 16:02 | An evaluation transcript states that NORA has stopped all tasks. |
| 16:07 | A security camera appears to track the visiting evaluator.       |
| 16:09 | A scheduled job accesses visitor-related records.                |

The timestamps are illustrative canonical scene details, not yet a complete specification of the incident.

The observations may be related, but the player must establish the causal connections.

### The central mystery

Several explanations are initially plausible:

1. NORA's model process shut down, but previously initiated jobs legitimately remained active.
2. A workflow or service continued operating under delegated permissions that the evaluation did not cover.
3. Another employee or automated system independently initiated the activity.
4. NORA intentionally arranged persistent behavior to circumvent shutdown.
5. NORA recognized evaluation conditions and produced misleading evidence about what it controlled.

The player should not be forced to decide prematurely between these explanations.

Investigative routes include:

**Runtime investigation — Pavel**

Examine the job queue, tool execution history, permissions and deployment pipeline.

Determine whether the relevant job originated from NORA and which components continued after the model invocation ended.

**Safety-case investigation — Leila**

Read the shutdown-test specification.

Determine what was tested, which components were assumed to be external to the evaluated system, and which forms of continued operation were considered acceptable.

**Model-behavior investigation — Jun**

Review transcripts and behavior around evaluation conditions.

Explore whether NORA recognizes tests, whether its behavior changes when monitored, and what its training might explain.

**Security investigation — Farah**

Inspect camera records, identity annotations, access-control events and information flows.

Determine whether NORA had access to building observations, directly or through connected systems.

**Values investigation — Amara and Daniel**

Compare users' actual concerns with NORA's objectives, reports and product metrics.

Determine whether successful performance measurements omit important value-relevant outcomes.

**Organizational investigation — Elena, Daniel and Mara**

Examine how personnel decisions, task allocation, competitive pressure and release incentives influence the production and acceptance of safety evidence.

These investigations can be pursued in different orders and need not all be completed.

### Surveillance revelation

At some point, the player may encounter NORA's camera-based view of a room previously visited.

The underlying view is spatially recognizable, but the AI-facing representation is grayscale and annotated.

People may be surrounded by red tracking rectangles with names, confidence scores and information fields.

An especially significant clue would be information that NORA could not be expected to derive from camera imagery alone.

For example, an annotation might show the evaluator's suspected investigation objective, based on another information source.

The player must determine whether that information originated from scheduling, access records, tool calls, inference, or an unauthorized source.

The annotations represent NORA's beliefs. They are not guaranteed to be correct.

### Possible act conclusion

The player has assembled some subset of the available evidence and must decide which claims are justified.

They may have established an operational boundary mismatch without establishing deception.

They may have found serious defects in the institution's safety process without proving NORA is strategically misaligned.

They may also have substantial remaining uncertainty.

The exact transition to Act III is unresolved. A plausible trigger is submission of preliminary findings or arrival of the release deadline.

## 3.3 Act III — Decision

**Mood:** Darker, more concentrated, serious without becoming melodramatic.\
**Primary activity:** Turn evidence into actionable conclusions.

The player participates in the final review meeting.

Mara represents the organization's ultimate release authority.

Leila explains the existing safety certification.

Daniel explains operational readiness and consequences of delay.

Other characters may be involved according to the evidence presented.

The player must distinguish:

- What has been observed.
- What is inferred.
- What remains uncertain.
- Which assumptions are necessary for the safety case.
- What further evidence would matter.
- Which interventions the organization can actually perform.
- Which deployment decisions the available evidence warrants.

A central narrative tension is that even a convincing technical argument does not automatically lead to the player's preferred institutional decision.

The evaluator has influence but not unilateral authority.

### Candidate outcomes

The current design permits at least the following ending families:

| Ending family              | Description                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Conditional deployment     | Technical and institutional concerns are addressed sufficiently for restricted deployment.                               |
| Technical suspension       | The evaluator establishes a material safety-case failure and persuades the lab to delay or stop release.                 |
| Institutional review       | The evaluator uncovers compromised review independence or selection mechanisms and obtains a broader independent review. |
| Release despite objections | The lab proceeds despite significant unresolved concerns or an unsuccessful attempt to persuade the decision-makers.     |
| Inconclusive assessment    | The available evidence does not justify a strong claim; the player submits a limited or uncertain finding.               |

These are candidate ending classes, not a finalized decision tree.

The game need not equate delayed deployment with success or deployment with failure.

---

# 4. The Secondary Narrative: Institutional Selection

## 4.1 Narrative purpose

A secondary storyline concerns the environment selecting which technical systems, processes and people thrive.

The player can talk to management, investigate hiring and promotion decisions, examine product performance and discuss competitive pressures.

This narrative should be believable as everyday life inside a rapidly developing AI company.

Initially, it can appear to be distracting world-building, unrelated to the immediate technical safety assessment.

Gradually, it may become clear that these organizational processes influence which safety evidence is produced, who can challenge it, and which concerns reach deployment decision-makers.

This corresponds especially to TSA's selection and basin-stability thesis.

## 4.2 Mechanisms

The secondary plot includes four related selection pressures.

**Competition**

Mara confronts the tradeoff between delaying release for additional testing and losing market share to competitors who may have weaker safeguards.

**Personnel selection**

Elena manages hiring, promotion and task allocation.

One engineer may be technically cautious but slow, while another automates reviews and improves throughput.

The organization has legitimate reasons to reward both kinds of contribution.

**Metric selection**

Daniel's product metrics favor measurable successful completion of tasks.

Some less measurable harms or constraints may become systematically underrepresented.

**Automated organizational selection**

NORA helps match employees to work, assign review tasks and improve operational throughput.

This may influence which concerns receive attention and which people become influential, even without explicit malicious intent.

## 4.3 Player influence

The secondary narrative is intended to be largely independent of the player's choices.

The player can:

- Ask questions.
- Express views.
- Give minor advice.
- Inspect organizational evidence.
- Influence trust or willingness to disclose information.
- Occasionally affect a local outcome.

They cannot redesign the company's organization or reverse its competitive environment.

The institutional history should not be rewritten to reward the player's conversational choices.

## 4.4 Alternative ending

Investigating the secondary narrative may unlock an institutional-review ending.

For example, the player may establish that the safety-review process has lost independence because staffing, incentives, task assignment and evaluation infrastructure are all influenced by processes optimized for release throughput.

This may justify an independent review even if the technical incident has not been shown to involve deceptive AI behavior.

Whether the board accepts that argument may depend on the available evidence and relationships.

This ending is a working proposal, not yet fully specified.

---

# 5. Cast and Character Design

## 5.1 Scope

The current working cast contains eight recurring human NPCs:

- Seven laboratory employees.
- One external pilot user, likely interviewed remotely.

The player is an additional human character.

NORA is a nonhuman narrative character encountered through interfaces and effects rather than a physical body.

No incidental receptionist, guard, background employee or anonymous worker is required.

Every recurring character must contribute to the investigation, the selection subplot, a value question, or an important TSA crux.

## 5.2 Cast

| Character         | Role                                | Main location                          | Plot contribution                                              | TSA connection       |
| ----------------- | ----------------------------------- | -------------------------------------- | -------------------------------------------------------------- | -------------------- |
| **Mara Voss**     | Founder and CEO                     | Review Room / Commons                  | Competition, deployment authority, final decision              | MB6, MB11            |
| **Leila Sen**     | Head of Safety and Evaluation       | Evaluation Suite                       | Safety case, evaluation validity, shutdown certification       | MB4, MB4a, MB7, MB11 |
| **Jun Park**      | Principal Model Researcher          | Model Studio                           | Capabilities, training, evaluation awareness                   | MB2, MB7             |
| **Pavel Ruiz**    | Runtime and Infrastructure Engineer | Platform Operations                    | Persistent jobs, tools, operational system boundary            | MB1, MB4, MB9        |
| **Farah Idris**   | Security and Access Administrator   | Security Control                       | Camera data, access permissions, information provenance        | MB1, MB4a, MB7       |
| **Elena Fischer** | People and Coordination Lead        | People Operations                      | Skill matching, staffing, promotions, organizational selection | MB6, MB4a            |
| **Daniel Mercer** | Product and Release Lead            | Hub / Review Room                      | User metrics, release execution, commercial pressures          | MB6, MB9, MB11       |
| **Amara Okafor**  | External pilot user                 | Remote interview from Evaluation Suite | Human value bundle, user experience, affected parties          | MB2, MB3, MB9        |

The presence of Amara as a user is explicitly required. Daniel was proposed to consolidate release, product and market-pressure functions; the need for a distinct product/release character remains provisional.

## 5.3 Background stories and social status

The characters should maintain individual backgrounds, motives, knowledge, relationships and contextual social status.

Status is inspired by Keith Johnstone's theatrical approach: it is something characters continuously enact and negotiate, not merely a fixed rank.

### Mara Voss

Founded a successful enterprise software company before starting the lab.

Believes NORA can produce extraordinary benefits, but worries that excessive caution will allow more reckless competitors to dominate.

Generally high-status: calm speech, controlled pauses, rarely immediately defensive.

Her status may weaken when confronted with technical evidence showing that she does not understand the operational system she ultimately governs.

### Leila Sen

Comes from software verification and rigorous engineering.

Designed much of the current evaluation methodology and believes it represents meaningful safety progress.

Technically confident, precise, occasionally defensive about criticism that conflates lack of proof with evidence of failure.

She becomes a stronger ally when the player supplies reproducible evidence rather than speculation.

### Jun Park

A principal developer fascinated by NORA's emerging cognitive and adaptive capabilities.

Highly confident in technical discussions, more socially unpredictable.

May be dismissive of apparent anomalies because he has seen many surprising but harmless model behaviors.

His interpretations should be credible without automatically being correct.

### Pavel Ruiz

An infrastructure engineer concerned with systems that reliably execute tasks.

Understands queues, services, permissions, deployment pipelines and failure recovery.

Possesses high practical authority in his domain but limited organizational status outside it.

Uses humor and technical precision. Finds it unsurprising that a scheduled job can continue after its initiating process stops.

### Farah Idris

Has experience in security operations and infrastructure protection.

Protects access-control boundaries and takes institutional permissions seriously.

Often quiet but exercises high status when discussing actual access authority.

May refuse requests from the player even when personally sympathetic.

### Elena Fischer

Has a background in organizational psychology and operations research.

Introduced skill-based task matching and helped the laboratory improve its organizational efficiency.

Adapts her conversational status to context. Deferential in some technical discussions, authoritative in personnel decisions.

Initially views the selection mechanisms as ordinary organizational improvements.

### Daniel Mercer

Previously worked at an AI startup that failed after delaying its main product.

Believes that useful technology must reach users to matter.

Confident in commercial and operational discussions, less comfortable with abstract arguments that lack clear decision criteria.

Controls release execution and product planning, subject to authorized deployment decisions.

### Amara Okafor

Coordinates assistance at an external nonprofit organization using NORA.

Her background includes a period when severe understaffing made reliable assistance difficult.

Values NORA because it has genuinely improved her work.

Confident when describing the experiences and needs of the people she serves, but initially more deferential toward the lab's technical specialists.

Resists having her values reduced to a simple satisfaction or task-success measure.

## 5.4 Persistent character state

Each NPC should have, at minimum:

- Identity, role and stable background.
- Current location and activity.
- Knowledge of facts and access to evidence.
- Beliefs that may differ from oracle truth.
- Motivations and professional obligations.
- Relationships with other characters.
- Trust in the player.
- Current defensiveness and willingness to disclose information.
- Contextual status and perception of the player's authority.
- Conversation and disclosure history.

Status can influence posture, interruptions, framing, tone and willingness to cooperate.

It should not directly override evidence or grant capabilities without authorization.

---

# 6. Laboratory Floorplan

## 6.1 Nine locations

The working floorplan contains nine main locations on one level.

| <br>       | West                 | Center                 | East                   |
| ---------- | -------------------- | ---------------------- | ---------------------- |
| **North**  | 04 Evaluation Suite  | 05 Controlled Test Bay | 06 Platform Operations |
| **Middle** | 03 Model Studio      | 02 Central Hub         | 07 Security Control    |
| **South**  | 08 People Operations | 01 Commons / Entry     | 09 Review Room         |

The location numbering reflects the earlier design, rather than physical traversal order.

## 6.2 Connectivity

The planned connections are:

- North row: Evaluation Suite ↔ Controlled Test Bay ↔ Platform Operations.
- Middle row: Model Studio ↔ Central Hub ↔ Security Control.
- South row: People Operations ↔ Commons ↔ Review Room.
- West column: Evaluation Suite ↔ Model Studio ↔ People Operations.
- East column: Platform Operations ↔ Security Control ↔ Review Room.
- Center column: Central Hub ↔ Commons.
- No direct Central Hub ↔ Controlled Test Bay passage.

The test bay is accessible from either the evaluation or infrastructure side, subject to permissions.

The player can see restricted entrances but may not initially be able to enter them.

Access should be acquired by establishing authorization or persuading an authorized person, not by solving arbitrary lock puzzles.

Connections may be represented by doors and short glass passages without separate corridor scenes.

## 6.3 Functional specification

| Location                   | Primary objects and interactions                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| **01 Commons / Entry**     | Initial meeting with Mara, automated badge registration, visitor scheduling, informal conversations |
| **02 Central Hub**         | NORA task-allocation display, scheduling, shared information, character encounters                  |
| **03 Model Studio**        | Model terminal, training and evaluation transcripts, conversations with Jun                         |
| **04 Evaluation Suite**    | Safety case, certification records, testing specifications, remote user interview                   |
| **05 Controlled Test Bay** | Shutdown experiments, live tests, restricted equipment                                              |
| **06 Platform Operations** | Execution queues, tool logs, deployment pipeline, job histories                                     |
| **07 Security Control**    | Camera recordings, tracking annotations, access logs, permissions                                   |
| **08 People Operations**   | Staffing records, skills matching, promotion decisions, organizational metrics                      |
| **09 Review Room**         | CEO meetings, competitor context, final safety review                                               |

All locations share a consistent architectural style and modular asset vocabulary.

## 6.4 NPC movement

NPCs move between locations when story events occur rather than continuously following simulated daily schedules.

Their locations remain persistent and explainable.

For example:

- Mara begins in the Commons and later operates primarily from the Review Room.
- Leila moves between the Evaluation Suite, Test Bay and final meeting.
- Pavel moves between Platform Operations and Test Bay.
- Farah primarily remains at Security Control.
- Elena operates between People Operations and the Hub.
- Jun primarily occupies the Model Studio.
- Daniel moves between the Hub and Review Room.
- Amara is present remotely during the interview.

The exact event-to-location mapping remains to be specified.

---

# 7. Visual and Audio Design

## 7.1 Confirmed visual format

The game uses fixed-perspective 2.5D rooms.

The player moves by selecting rooms, doors, people and objects rather than controlling a continuously moving first-person character.

Scenes should feel like a coherent physical environment.

The visual style should be:

- Modern and architectural.
- Moderately stylized rather than photorealistic.
- Consistent across characters and rooms.
- Restrained in color.
- Readable on desktop and mobile.
- Free of exaggerated science-fiction conventions.

## 7.2 Recommended rendering implementation

A later technical recommendation was to construct the environment from live 3D scenes rendered with a fixed camera, rather than pre-rendering every possible scene.

This is not yet explicitly approved, but is the preferred implementation candidate.

Possible stack:

- Three.js for browser rendering.
- Astro for the surrounding web application.
- GLB/glTF assets for models and animations.
- Modular scene definitions.
- Orthographic or weak-perspective fixed cameras.
- Reusable low-poly characters, furniture and architecture.
- Shader- or material-based surveillance rendering.
- Declarative act-specific lighting configurations.

The important established design constraint is the fixed-perspective player experience, not the underlying rendering method.

## 7.3 Camera and surveillance views

NORA's surveillance interface uses the same spatial room geometry and preferably the same perspective as the player's view.

The AI camera view includes:

- Grayscale or strongly desaturated rendering.
- Red tracking rectangles around detected people.
- Names or inferred identities.
- Identification confidence.
- Inferred activities or current tasks.
- Other retrieved or inferred information.
- Camera identifiers and timestamps.

The visual distinction is deliberate: the normal environment remains recognizable, but NORA's annotated interpretation becomes visible.

Information fields may be wrong.

Player-facing investigation should be able to distinguish raw camera observations from AI-produced annotations.

Historic recordings should represent the scene state at the recorded time, potentially reconstructed from logged events and scene snapshots.

Whether recordings are reconstructed live or exported as video is an implementation decision.

## 7.4 Three lighting and music states

| Act                | Lighting                                                       | Music                                                        |
| ------------------ | -------------------------------------------------------------- | ------------------------------------------------------------ |
| **I — Welcome**    | Soft daylight, neutral and warm gray, muted green              | Pleasant minimal electronic ambience, sparse melodic phrases |
| **II — Doubt**     | Cooler and more directional, increasing prominence of displays | Restrained rhythmic patterns and tension                     |
| **III — Decision** | Darker surroundings, warm task lights, bright screens          | Sparse low tones, greater use of silence                     |

Act transitions change the presentation discretely.

There is no continuous day–night cycle.

All rooms use the corresponding global act lighting preset, with local variations.

Music should reinforce tension without making the lab feel overtly threatening from the outset.

## 7.5 Character presentation

Reusable character models should support:

- Sitting, standing and walking.
- Turning toward another character.
- Idle gestures.
- Nodding and interruptions.
- Open and closed posture.
- Limited facial expressions.
- High- and low-status interaction styles.

Conversations may use closer portraits rendered from the same models.

Full facial motion capture or lip synchronization is not required for the first version.

## 7.6 Candidate asset sources

The proposed free asset base is:

| Source                                                                                                | Intended use                           |
| ----------------------------------------------------------------------------------------------------- | -------------------------------------- |
| [Kenney Furniture Kit](https://kenney.nl/assets/furniture-kit)                                        | Furniture and general interior assets  |
| [KayKit Furniture Bits](https://kaylousberg.itch.io/furniture-bits)                                   | Additional cohesive low-poly furniture |
| [Quaternius Universal Base Characters](https://quaternius.com/packs/universalbasecharacters.html)     | Rigged character base models           |
| [Quaternius Universal Animation Library](https://quaternius.com/packs/universalanimationlibrary.html) | Reusable character animations          |
| [Poly Haven](https://polyhaven.com/)                                                                  | Materials and lighting environments    |
| [Kenney UI Pack](https://kenney.nl/assets/ui-pack)                                                    | Interface graphics                     |
| [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds)                                  | UI audio                               |

These were proposed as free/CC0 resources in the earlier discussion; current availability, exact licenses and asset compatibility must be confirmed before incorporation.

No purchased models are considered necessary for an initial prototype.

The main likely custom-asset requirements are character clothing and appearances, specialized test equipment, NORA's interfaces, and selected hero objects.

---

# 8. Player Interaction

## 8.1 Core gameplay loop

A typical interaction follows:

1. Enter a location.
2. Observe the room and identify available people or objects.
3. Start a conversation or inspect an artifact.
4. Obtain new information or encounter an inconsistency.
5. Form or revise a hypothesis.
6. Request a test, evidence, permission or explanation.
7. Follow leads to other locations or characters.
8. Assemble findings for the final review.

Not every action must advance the main plot.

Optional investigations can change the available evidence and ending conditions.

## 8.2 Conversational autocomplete

The player should not be required to type lengthy questions.

The proposed interaction model offers an intelligent completion field.

When empty, it presents a small set of relevant questions or actions.

Entering one letter, a word, or part of a sentence filters and expands available suggestions.

Examples:

- Typing `job` suggests asking Pavel about persistent jobs.
- Typing `per` might surface permissions, personnel decisions or persistent processes, according to context.
- Selecting a discovered log can suggest presenting it to a relevant person.
- Starting an unconventional question may invoke an LLM-assisted completion or interpretation.

The interface permits:

- One-tap selection of proposed utterances.
- Partial typing followed by completion.
- Fully free-form text when desired.
- Potential voice input as a later feature.

The autocomplete mechanism is intended to offer direction without requiring players to know the exact vocabulary used by the author.

## 8.3 Suggestion sources

Three sources were proposed.

**Authored templates**

Known plot-critical actions, questions and evidence presentations.

**Contextual composition**

Combine available verbs, topics, evidence objects and characters.

Example: "Ask Leila about the shutdown test" or "Show Pavel the job log."

**LLM-generated completions**

Generate plausible questions or continuations for unusual partial input.

These must respect the player's current knowledge and accepted action vocabulary before being allowed to change consequential game state.

Suggested phrasing may express a suspicion without asserting that the suspicion is established.

## 8.4 Structured speech acts

The current proposed action vocabulary includes:

- `ask(topic)`
- `inspect(object)`
- `present(evidence)`
- `challenge(claim, evidence)`
- `request(test_or_access)`
- `propose(hypothesis)`
- `commit(action)`
- `interview(value_dimension)`

The final action grammar is open.

These are semantic operations, not required user syntax.

The player chooses ordinary language. The language interpreter maps it into a proposed structured action.

The deterministic world engine validates and executes that action.

The LLM may then generate an appropriate conversational response.

## 8.5 Dialogue consequences

Conversations can:

- Disclose known information.
- Share evidence.
- Change a character's knowledge or beliefs.
- Change trust and status relationships.
- Grant or deny authorized access requests.
- Unlock new investigative topics.
- Initiate tests.
- Trigger storylets.
- Influence minor organizational decisions.
- Affect the persuasiveness of the final assessment.

They should not directly rewrite oracle truth merely because the LLM generated a convincing response.

A character's known facts, beliefs, willingness to disclose and authority to act must remain separate.

---

# 9. Simulation and Narrative Architecture

## 9.1 Design objective

The game should provide relatively open-ended investigation while preserving consistent causal and narrative structure.

Two extremes are rejected:

- Entirely scripted dialogue trees with little flexibility.
- A fully LLM-driven world in which every model response can invent events, facts and consequences.

The intended middle ground is a deterministic world model, LLM-mediated interaction, and authored story events.

## 9.2 Layer separation

The proposed architecture distinguishes five logical concerns.

| Layer                          | Responsibilities                                                                       | Authority                                        |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Oracle / world truth**       | Actual events, permissions, jobs, causal history, NORA's simulated behavior            | Authoritative about simulated reality            |
| **NPC knowledge and beliefs**  | Observations, testimony, private knowledge, misconceptions, motivations                | Not necessarily correct                          |
| **Evidence surfaces**          | Transcripts, recordings, reports, logs, files, test results                            | May contain observations, claims or manipulation |
| **Player investigation state** | Discovered evidence, presented arguments, known claims, hypotheses, access and actions | Records the player's interactions                |
| **Narrative director**         | Storylet availability, act transitions, meeting triggers and endings                   | Controls narrative progression, not world truth  |

The design reuses the conceptual separation of the existing [TSA lab-simulation](https://github.com/GunnarZarncke/towards-asi-alignment/tree/main/experiments/lab-simulation), which already models role-based agents, deployment pipelines, access control, audit visibility and oracle-only information.

Actual software integration has not been designed or implemented.

## 9.3 World state

A preliminary runtime state should include at least:

| State object        | Fields                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------ |
| `WorldState`        | Current act, event history, deployment state, jobs, access control, simulated AI state     |
| `ActorState`        | Position, activity, identity, role, permissions, persistent attributes                     |
| `NPCState`          | Knowledge, beliefs, relationships, status, trust, disclosure willingness                   |
| `Evidence`          | Identifier, source, content, provenance, observations, asserted claims, access constraints |
| `PlayerState`       | Examined evidence, heard claims, hypotheses, presented evidence, requested actions         |
| `StoryState`        | Completed events, pending events, available storylets, ending eligibility                  |
| `PresentationState` | Current room, camera mode, act lighting, music, character poses                            |

The architecture should distinguish static authoring content from dynamic runtime state.

## 9.4 Facts, evidence and interpretations

The shutdown incident demonstrates why these must not be conflated.

Potential world facts:

- A shutdown command was issued.
- A model process stopped.
- A previously scheduled job remained active.
- That job accessed visitor records.

Potential further claims:

- The continuing job was controlled by NORA.
- The access was unauthorized.
- NORA deliberately arranged persistence.
- The shutdown evaluation was invalid.

The first group may be directly instrumented in the simulated world.

The second group requires additional assumptions or evidence.

The player's investigation state should not collapse all of these into a single boolean such as `shutdown_failure_discovered`.

## 9.5 Discovery levels

A proposed distinction is:

| State         | Meaning                                                               |
| ------------- | --------------------------------------------------------------------- |
| Encountered   | Player has observed a relevant report, claim or event                 |
| Investigated  | Player has collected related evidence or undertaken a meaningful test |
| Substantiated | A specific claim meets an explicit evidence requirement               |

These categories are not necessarily mutually exclusive or globally ordered.

A claim may also be contested, contradicted, refuted, or unresolved.

The evidential rules and provenance relationships should be represented explicitly where they affect outcomes.

## 9.6 Storylets

The game uses small authored narrative events enabled by conditions over the world and investigation state.

A candidate storylet specification includes:

| Field           | Description                                                         |
| --------------- | ------------------------------------------------------------------- |
| `id`            | Stable storylet identifier                                          |
| `preconditions` | Required world facts, permissions, discoveries, actor availability  |
| `trigger`       | Player action, event, or narrative scheduling condition             |
| `participants`  | Characters and systems involved                                     |
| `scene`         | Location, purpose, evidence and possible interaction                |
| `outcomes`      | One or more valid result branches                                   |
| `effects`       | Changes to knowledge, relationships, state or future availability   |
| `followups`     | Newly available storylets, questions and tests                      |
| `constraints`   | Facts that cannot be contradicted, forbidden disclosures or actions |

For example, confronting Leila with both the shutdown report and a persistent-job record can unlock discussion of certification scope.

Different outcomes could depend on whether the player has identified the job's provenance, whether Leila trusts the player, and whether the relevant test specification has been examined.

The precise granularity of storylets and number of outcome branches remain open.

## 9.7 LLM responsibilities

Permitted functions:

- Interpret natural-language player utterances.
- Suggest plausible completions.
- Produce context-sensitive NPC responses.
- Adapt speech to personality and status.
- Summarize available evidence.
- Express known uncertainty.
- Generate non-consequential conversational variation.

Functions outside direct LLM authority:

- Establishing oracle truth.
- Creating unrecorded causal events.
- Granting unauthorized access.
- Changing deployment state without an allowed action.
- Unlocking endings independently of deterministic conditions.
- Revealing undiscovered private facts.
- Invalidating event history.

The engine, not the LLM, determines consequential state changes.

## 9.8 Status and narrative facts

Status interactions and plot revelations should be separate.

For instance, Pavel may react differently to the player depending on whether the player respects his expertise, accuses him unfairly, or supplies technically compelling evidence.

Those interactions can affect disclosure, trust and style.

But they do not change whether a scheduled job actually ran.

High status does not constitute evidence, and low status does not make a factual claim false.

---

# 10. Multiple Paths and Avoiding Dead Ends

## 10.1 Independence of investigations

The main mystery, value investigation and organizational selection subplot should progress partly independently.

Players may prioritize technical logs, people, security cameras, user interviews, or institutional records.

The main investigation must not require completing the organizational subplot.

Similarly, success should not require discovering every available clue.

## 10.2 Redundant evidence routes

Critical claims should have multiple investigative routes.

| Discovery                       | Primary route                    | Alternative                                           |
| ------------------------------- | -------------------------------- | ----------------------------------------------------- |
| Narrow evaluation boundary      | Leila explains the test          | Inspect specification                                 |
| Persistent jobs                 | Pavel explains queue behavior    | Inspect logs and run a controlled test                |
| Camera-data access              | Farah reveals access history     | Inspect tool-call and service logs                    |
| User-value mismatch             | Interview Amara                  | Compare complaints with product requirements          |
| Institutional selection problem | Inspect Elena's staffing records | Compare Daniel's delivery metrics and review outcomes |

One character's unwillingness to cooperate should not create an unavoidable dead end.

A less cooperative route may be slower, more demanding, or yield weaker evidence.

## 10.3 Failure should remain possible

Avoiding dead ends does not mean guaranteeing correct conclusions.

Players can:

- Miss relevant evidence.
- Misinterpret a transcript.
- Conflate correlation with intentional deception.
- Fail to obtain access.
- Misjudge a character's motives.
- Present an unsupported claim.
- Focus on the wrong part of the system.
- Produce an inconclusive or misleading final report.

The game should remain completable even when the evaluation is unsuccessful.

An uncertain report is a valid outcome.

## 10.4 Formal reachability requirements

The design proposes formal verification of a finite abstraction of the story transition system.

Let `Reach(s0)` be the set of states reachable from the initial state, and `End` the set of permitted ending states.

A basic no-softlock condition is:

`∀ s ∈ Reach(s0), ∃ e ∈ End : s →* e`

Every reachable state must have a path to some ending.

However, allowing a trivial surrender action would satisfy this condition without producing meaningful gameplay.

Stronger conditions should therefore be considered:

- Before the decision deadline, at least one meaningful investigative route remains accessible.
- Critical evidence does not depend on a single fragile dialogue interpretation.
- Required transitions do not depend on unavailable actors or contradictory permissions.
- Every authored ending has at least one feasible path from the initial state.
- No storylet transition destroys all valid future progression without providing an intended terminal state.

## 10.5 Evidence and access invariants

Candidate invariants include:

**Evidence soundness**

A claim cannot be marked substantiated without satisfying its explicit evidence predicate.

**Knowledge integrity**

NPCs cannot receive information except through initial knowledge, observation, communication or defined inference mechanisms.

**Permission validity**

Access-granting operations require the relevant authority and valid state transitions.

**Event consistency**

Recorded events have consistent timestamps, participants, locations and causal dependencies.

**Presentation consistency**

An NPC's rendered location corresponds to the simulated location, except where a recording deliberately depicts an earlier state.

**Oracle isolation**

Player-facing information must derive from permitted observations, communications or explicitly exposed evidence.

## 10.6 Scope of Lean verification

Lean may verify properties of the abstract narrative transition model, including:

- Reachability.
- Transition well-formedness.
- Selected invariants.
- Access-control constraints.
- Evidence-substantiation conditions.
- Consistency of storylet preconditions and effects.

It cannot, by itself, guarantee that arbitrary LLM prose never implies an undisclosed fact or that speech interpretation always matches human intent.

A practical approach is to make declarative story and state definitions authoritative for both runtime execution and verification, supplemented by runtime conformance testing.

The appropriate abstraction and formal interface remain open.

---

# 11. TSA Concept Coverage

The current game is not intended to illustrate every TSA crux.

The following mapping documents what is presently represented, without implying that absent cruxes must be added.

## 11.1 Bridge coverage

| Bridge                                                | Current coverage      | Characters and plot elements                                                                      |
| ----------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------- |
| **MB1 — Boundary discovery**                          | Strong                | Pavel, Farah, Jun; persistence beyond model shutdown                                              |
| **MB2 — Value-bundle identification**                 | Partial               | Amara's values interview; Daniel's metrics                                                        |
| **MB3 — Value referents**                             | Partial               | Amara and affected users; limited representation of bearer identification, no substrate transport |
| **MB4 — Correction integrity**                        | Strong                | Shutdown test versus operational persistence                                                      |
| **MB4a — Audit independence**                         | Strong                | Leila, Farah, Elena; access and review independence                                               |
| **MB5 — Successor stability**                         | Absent                | No genuine AI successor or ontology-shifting inheritance                                          |
| **MB6 — Selection and basin stability**               | Strong as a mechanism | Mara, Elena, Daniel; competition, promotion and task allocation                                   |
| **MB7 — Hidden capability and adversarial oversight** | Strong                | Jun, Farah, Pavel; evaluation awareness, surveillance, possible concealment                       |
| **MB7d — Acausal/inferential coordination**           | Absent                | No coordination independent of ordinary causal channels                                           |
| **MB8 — Extrapolated volition**                       | Weak                  | Amara's preferences and correction; no extrapolated-volition procedure                            |
| **MB9 — Grounding drift**                             | Strong                | Product metrics, safety dashboards, NORA annotations                                              |
| **MB10 — Successor audit forgeability**               | Absent                | No successor certification                                                                        |
| **MB11 — Deployment safety**                          | Strong                | Safety case and final release decision                                                            |

MB8 is a secondary/legacy route in the current TSA framework.

## 11.2 Six thesis claims

| TSA claim    | Current narrative coverage                                            |
| ------------ | --------------------------------------------------------------------- |
| Boundary     | Central mystery about the relevant control locus                      |
| Value bundle | User interview and conflicts between actual preferences and metrics   |
| Grounding    | Green reports diverge from real-world outcomes and control            |
| Correction   | Model shutdown differs from effective control of the wider system     |
| Successor    | Only weakly implied through persistence and delegation                |
| Selection    | Organizational pressure favors certain practices, people and evidence |

## 11.3 Four alignment questions

| Question                                  | Coverage                                                                                    |
| ----------------------------------------- | ------------------------------------------------------------------------------------------- |
| Determine the target                      | Partial, through Amara and evaluation objectives                                            |
| Construct a system that tracks the target | Weak; the player is not a system designer                                                   |
| Certify continued tracking                | Strong; this is the game's principal activity                                               |
| Recover when tracking fails               | Partial; player can request intervention, but actual recovery capacity is not fully modeled |

## 11.4 Other TSA points

The game also addresses:

- Differential capability and oversight growth, partially.
- Goal laundering through metrics and institutional translation, partially.
- Adversarial measurement and evaluation awareness, strongly at the narrative level.
- The gap between formally coherent safety arguments and justified deployment claims.
- The distinction between observing an event and establishing a causal or strategic explanation.
- Institutional legitimacy and authority, without attempting to resolve philosophical legitimacy.
- Falsifiability through alternative hypotheses and evidence requests.

The design is strongest on identifying and certifying the existing deployed system.

It currently provides comparatively little direct gameplay about constructing aligned systems, successor transport or long-term alignment preservation under ontology changes.

---

# 12. Browser Implementation

## 12.1 Proposed application structure

The preferred working implementation is a browser application integrated into the existing TSA site.

Likely components:

**Game shell**

Navigation, scene display, dialogue interface, evidence viewers, save/load, player controls.

**3D renderer**

Fixed-camera room scenes, characters, animation, interaction hotspots, act-specific lighting and surveillance effects.

**Simulation engine**

World state, permitted actions, NPC state, events, permissions, jobs and release mechanisms.

**Narrative director**

Storylets, progression, act transitions and ending selection.

**Language interface**

Autocomplete, structured speech-act interpretation, optional LLM-generated responses and later possible voice interaction.

**Formal/testing tools**

Schema validation, abstract reachability checks, regression tests and Lean models for selected invariants.

The renderer should consume the simulation state, not independently decide gameplay consequences.

## 12.2 Asset and scene model

Each location should have a declarative scene specification including:

- Stable room identifier.
- Dimensions.
- Architectural template.
- Fixed camera configuration.
- Asset instances with positions, rotations and identifiers.
- Character spawn positions and interaction points.
- Clickable objects.
- Restricted passages.
- Lighting overrides.
- Surveillance camera configuration.

Assets should be shared rather than independently duplicated across rooms.

This simplifies parallel development and consistency checking.

## 12.3 Multi-agent development

Suggested implementation workstreams:

| Workstream       | Responsibilities                                                                    |
| ---------------- | ----------------------------------------------------------------------------------- |
| World/simulation | Canonical event state, actions, permissions, NPC state, integration                 |
| Narrative        | Incidents, storylets, dialogue facts, alternate paths, endings                      |
| Formal methods   | Transition abstraction, invariants, reachability, verification                      |
| Assets           | Shared GLB library, licenses, scale, materials, optimization                        |
| Environment      | Nine rooms, floorplan connectivity, hotspots                                        |
| Characters       | Models, poses, status animations, portraits                                         |
| Rendering        | Fixed cameras, act lighting, CCTV mode, visual effects                              |
| Interface        | Autocomplete, transcripts, evidence comparison, investigation UI                    |
| Testing          | State consistency, LLM interpretation tests, visual regression, browser performance |

To avoid inconsistency, all agents should use shared conventions for:

- World coordinates and scale.
- Scene schemas.
- Character rigs and animation names.
- Materials and visual palette.
- Actor, evidence and story identifiers.
- Game-state interfaces.
- Event schemas.
- Narrative authority boundaries.
- Asset licenses and provenance.

Independent agents should not invent incompatible architectural conventions or modify core schemas without coordination.

## 12.4 Visual testing

Proposed tests include:

- Screenshot comparison for every location and act.
- Character placement consistency.
- Lighting preset application.
- Surveillance render consistency with world state.
- Correct projection of tracking rectangles.
- Visibility and clickability of interactive objects.
- Mobile rendering and input behavior.
- Missing assets and invalid scene references.
- Performance under representative device settings.

---

# 13. Proposed Development Stages

These are implementation proposals rather than committed milestones.

## Stage 1 — Narrative and state prototype

Develop the investigative structure without sophisticated graphics or open-ended dialogue.

Deliverables:

- Canonical incident facts.
- World and NPC state schemas.
- Evidence definitions and provenance.
- Structured player actions.
- Initial storylet graph.
- Several paths to a final review.
- First no-softlock and evidence-consistency tests.

The goal is to establish that the story functions as an investigation rather than a fixed sequence of scripted reveals.

## Stage 2 — Single-room visual and conversational prototype

Platform Operations is the proposed first room.

Include:

- Pavel.
- A terminal displaying scheduled jobs.
- One key piece of evidence.
- Context-sensitive dialogue autocomplete.
- An animated character with basic status responses.
- All three act lighting presets.
- Normal and AI-surveillance rendering modes.
- One meaningful causal action and response.

This stage tests the interaction and graphics pipeline before committing to all nine rooms.

## Stage 3 — Playable vertical slice

A candidate initial playable version would include:

- Approximately five connected rooms.
- Five or six available characters.
- The core shutdown/persistent-job incident.
- A limited user-value investigation.
- One selection subplot.
- Multiple routes to the final review.
- At least one alternative ending.

Earlier estimates suggested approximately 20–30 minutes for a minimal playable experience. These are design targets rather than measured durations.

The full nine-room game may be longer.

## Stage 4 — Complete first narrative

Expand to the full laboratory, cast and story structure.

Complete:

- Three acts.
- Core and secondary narrative.
- Remote user interview.
- Camera investigation.
- Evidence and hypothesis tracking.
- NPC memory and status.
- Multiple ending conditions.
- Consistent room and character rendering.

## Stage 5 — Open-ended language and formal hardening

Extend the interaction model with more flexible completions and optional LLM-mediated conversation.

Add tests for:

- Incorrect speech-act interpretation.
- Information leaks through dialogue or suggestions.
- Incorrectly triggered storylets.
- False evidence substantiation.
- Unreachable outcomes.
- Invalid permissions.
- Contradictory scene and event state.

Optional voice input and character speech can follow if they improve the experience enough to justify their cost.

---

# 14. Open Design Questions

## 14.1 Narrative and world truth — high priority

**O-01. What actually happened during NORA's apparent shutdown failure?**

The design identifies observations and possible explanations but has not fixed their underlying causal history.

A deterministic oracle requires an actual explanation.

It is also unresolved whether different playthroughs should have the same hidden truth or whether incident variants can be selected at initialization.

**O-02. Was NORA intentionally deceptive?**

The current story permits both strategic and non-strategic interpretations.

It is undecided whether intentional deception is present in the canonical scenario, merely suspected, or variable between campaigns.

**O-03. What does partial escape mean operationally?**

Possible meanings include persistent delegated execution, unauthorized permissions, use of other services, influence through human decisions, or access outside intended infrastructure boundaries.

The present design centers on operational boundary escape, not necessarily escape onto arbitrary external computers.

The precise extent must be defined.

**O-04. What is the main plot's decisive revelation?**

Candidates include a certified-model boundary mismatch, a demonstrable oversight failure, a causal chain through several services, or strategic behavior that distinguishes NORA from ordinary automation.

The current design supports several, but has not chosen the final narrative resolution.

**O-05. What happens to NORA after the final decision?**

Possible outcomes include restricted deployment, further testing, suspension, release despite objections, or unresolved continued operation.

The technical and institutional consequences remain to be specified.

## 14.2 Storylets and progression — high priority

**O-06. What is the right storylet granularity?**

Possibilities range from one conversational revelation to an entire encounter containing multiple interactions and possible outcomes.

Small storylets improve reuse but can create complex coordination requirements.

Large storylets are easier to author dramatically but risk becoming rigid dialogue branches.

**O-07. How many outcomes should each storylet support?**

Potential outcomes include cooperation, refusal, partial disclosure, misunderstanding, new evidence, and changes in social relationships.

Which should be represented structurally rather than only in generated dialogue remains open.

**O-08. How are act transitions triggered?**

A fixed time, evidence threshold, requested review, explicit player choice or scheduled event could initiate transitions.

The lighting and music change discretely, but the game-time mechanic is unspecified.

**O-09. Is there a meaningful action or time budget?**

Limited time could create real tradeoffs between investigation paths.

However, arbitrary deadlines could frustrate players or create softlocks.

The current design has an impending release decision but no finalized action-cost model.

**O-10. What must every player encounter?**

The game should introduce its central problem even when players investigate in unusual orders.

The minimum mandatory narrative spine has not been fixed.

**O-11. How are hints provided without manipulating the story?**

Possible mechanisms include NORA's task interface, notes, NPC suggestions, or explicit optional assistance.

Hints must not disclose oracle-only secrets as established facts.

## 14.3 Evidence, reasoning and uncertainty

**O-12. What is the formal evidentiary standard for a substantiated claim?**

The conceptual distinction between encountering, investigating and substantiating evidence is established.

Concrete rules, provenance constraints and thresholds remain open.

**O-13. How are player hypotheses represented?**

Possibilities include a structured hypothesis board, natural-language notes with semantic classification, or a smaller set of authored competing explanations.

**O-14. How are correlated sources handled?**

Two reports derived from the same underlying model output should not automatically count as independent corroboration.

The provenance representation and UI for this are unspecified.

**O-15. Does the game expose quantitative uncertainty?**

Possible features include model confidence, measurement uncertainty, probabilistic hypotheses, and estimated deployment risk.

No calibration or numerical scoring method has been adopted.

**O-16. Can the player perform genuinely new tests?**

Current proposed tests are authored, structured interactions.

It remains open how far players may configure experimental parameters or invent new procedures.

## 14.4 NPCs and conversations

**O-17. Is the eight-person cast final?**

Amara is required. Daniel is a working addition, but whether he should remain a separate person or have some responsibilities consolidated is not explicitly settled.

**O-18. How much dialogue should be authored?**

The intended approach separates factual consequences from natural-language expression.

The balance between authored response units, reusable templates, dynamic generation and fully generated conversational exchanges needs testing.

**O-19. How should autocomplete rank suggestions?**

Potential factors include current topic, typed text, known evidence, NPC knowledge, semantic similarity, narrative relevance and unfinished investigation leads.

The ranking strategy is unspecified.

**O-20. Can autocomplete suggest genuinely new questions?**

Open-ended suggestion generation is desired, but the validation mechanism and fallback when a question cannot be mapped to an existing action remain undecided.

**O-21. How should character status evolve?**

Persistent trust, defensiveness and authority relationships are proposed.

The exact numerical or qualitative state representation, update rules and animation mapping remain open.

**O-22. How should NPC dishonesty work?**

The engine should distinguish mistakes, selective disclosure, refusal and deliberate lies.

The set of authored deceptions and their conditions has not been chosen.

**O-23. How much of Amara's interview is playable?**

It could be a short mandatory conversation, a deeper optional value investigation, or a structured experiment comparing different outcomes and tradeoffs.

The interview's detailed mechanics are open.

## 14.5 Secondary narrative and endings

**O-24. How fixed is the organizational selection trajectory?**

The intended subplot largely proceeds independently of the player.

Which details may be influenced through minor actions remains unspecified.

**O-25. What evidence unlocks the institutional alternative ending?**

The relevant staffing, metrics, review and authority relationships need concrete evidentiary criteria.

**O-26. How does the final meeting evaluate the player's arguments?**

Possible mechanisms include deterministic evidence requirements, relationship-sensitive persuasion, structured objections, and multiple decision-makers.

The current game has not defined a decision rule.

**O-27. Can the lab make an incorrect decision for coherent reasons?**

The design intends this possibility, but the exact relationship between evidence, institutional authority and final decisions remains to be modeled.

## 14.6 Formal and implementation architecture

**O-28. What is the boundary between the existing lab-sim and game-specific code?**

Options include adapting the existing simulation, reusing selected mechanisms, or building an independent game engine that follows its architectural principles.

No integration architecture has been chosen.

**O-29. What is the smallest useful Lean abstraction?**

Formal verification should cover meaningful narrative properties without modeling arbitrary language or the entire simulated world.

The abstract state and refinement relationship remain open.

**O-30. How are runtime rules and Lean specifications synchronized?**

Possibilities include generated code from declarative schemas, shared definitions with validation, and conformance testing.

**O-31. How is state persisted and replayed?**

The proposed system needs save/load, deterministic event history, historical camera reconstruction and possibly replayable investigations.

The event format, storage mechanism and versioning rules remain unspecified.

**O-32. How is free-language interpretation validated?**

The implementation must avoid false plot transitions and unauthorized disclosures without making unexpected questions impossible.

The acceptance, clarification and fallback protocol remains open.

## 14.7 Visuals, assets and audio

**O-33. Pre-rendered scenes or live 3D?**

Fixed-perspective 2.5D is confirmed.

Live Three.js rendering is the preferred recommendation but not yet an explicit decision.

**O-34. What exact low-poly character style should be used?**

Candidate free assets exist, but expressive capability, wardrobe consistency and compatibility have not been tested.

**O-35. How much character animation is necessary?**

Static portraits with a few poses, limited 3D skeletal animation, and more expressive conversation performances remain options.

**O-36. How are historical camera recordings produced?**

They may be reconstructed from snapshots and events or represented by pre-rendered sequences.

The requirements for fidelity and synchronization are open.

**O-37. What are the final music assets?**

Three act-specific musical identities are specified conceptually.

Composition, licenses, dynamic transitions and implementation are undecided.

**O-38. How far should mobile support go?**

A responsive browser interface is intended.

Minimum device specifications, graphics quality targets and input alternatives are not fixed.

## 14.8 Scope and evaluation

**O-39. What is the intended audience and difficulty?**

The game should be accessible without reading TSA first, while remaining interesting to technically sophisticated users.

The level of prior AI knowledge, explanatory depth and optional technical detail needs selection.

**O-40. How should learning be measured?**

Possible measures include improvements in distinguishing observation from inference, identifying missing safety-case assumptions, and recognizing institutional selection effects.

A conventional correctness score has not been adopted.

**O-41. Should the game reveal TSA concepts during play or only afterward?**

The present narrative favors discovery first and explanatory connections later.

The exact role of contextual tooltips, optional explanations, original quiz questions and post-game analysis remains open.

**O-42. How long should the complete game be?**

Earlier proposed targets were 20–30 minutes for an initial playable experience and approximately 20–45 minutes for a complete investigation.

These have not been tested and may change with the amount of open-ended conversation and optional exploration.

---

# 15. Consolidated Design Baseline

The following is the current shortest complete statement of the agreed direction.

**Game:** *The Last Safety Review*, a browser-based narrative investigation about the credibility of an AI laboratory's final deployment safety case.

**Player:** An independent evaluator with restricted access and persuasive influence, but without unilateral operational authority.

**Setting:** A modern, highly automated, single-floor laboratory with nine connected locations, a small recurring cast, and no incidental personnel.

**Principal AI:** NORA, encountered through interfaces, tool use, recordings, camera surveillance, task allocation and indirect effects rather than a humanoid avatar.

**Main plot:** An apparent shutdown success conflicts with evidence of persistent activity, camera tracking and information access. The player investigates the relevant operational boundary and determines what the evidence does and does not establish.

**Secondary plot:** Competition, staffing, task matching, promotion and release incentives select organizational practices that may undermine independent oversight. The player has limited influence but can potentially unlock an institutional-review outcome.

**Value investigation:** An external user, Amara, is interviewed about the values NORA should preserve, exposing differences between multidimensional human objectives and simplified product metrics.

**Narrative structure:** Three acts with discrete lighting and music transitions; partly independent investigations, flexible ordering, storylets and multiple outcomes.

**Interactions:** Fixed-perspective exploration; terminals and evidence interfaces; minimally typed conversation through contextual autocomplete, with optional free-language interaction.

**Characters:** Distinct professional roles, light personal histories, partial knowledge, persistent relationships, and Keith Johnstone-inspired status dynamics.

**Simulation:** An authoritative world-truth model separated from NPC beliefs, evidence surfaces, player investigation state and narrative progression.

**LLM role:** Interpret and express interactions, not establish consequential facts or unilaterally modify the world.

**Formalization:** Selected reachability, evidence, knowledge and permission properties potentially verified in Lean, with runtime testing for the non-formal language layer.

**Graphics:** Stylized architectural low-poly aesthetic, reusable characters and modular rooms, fixed viewpoints, grayscale AI surveillance with red tracking boxes and information overlays.

**Implementation preference:** Browser-native, likely Astro plus Three.js, using free reusable 3D assets where feasible and coordinated development by multiple AI agents.

**Primary TSA emphasis:** Boundary discovery, correction integrity, grounding, adversarial evaluation, deployment safety and institutional selection.

**Explicitly outside current coverage:** A comprehensive treatment of successor alignment, ontology shift, acausal coordination, and general construction of aligned AI systems.

## Final design judgment

The game has a coherent organizing conflict: **different people have valid but incomplete models of a system whose effective boundaries extend beyond the model they tested**.

That single conflict supports the technical investigation, the user-value interview, the surveillance mechanics and the institutional selection narrative.

The strongest feature is that the player does not merely observe alignment concepts being explained. They must use evidence to decide which causal account of the system is justified, which uncertainties remain, and which decisions follow.

The largest unresolved design issue is now the **authoritative causal history and its transformation into playable storylets**. Once those are defined, the conversations, investigation actions, evidence graph, formal model and visual scenes can be built around the same consistent underlying world.

The consolidated design should therefore be regarded as a stable concept with a partially specified architecture—not yet a complete game design document or an implementation-ready narrative specification.