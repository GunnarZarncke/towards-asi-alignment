# World

Lane: engine, content half. Mechanics that use these ids are [engine.md](engine.md). Pictures are [graphics-ui.md](graphics-ui.md).

Ids already in `lib/game.mjs` are normative for the prototype. New ids are added here first, then in code.

The shutdown incident is authored as a causal model in [incident.md](incident.md), before more dialogue or rooms. The prototype facts below stay in the running build until that model replaces them. The sections after the prototype block are the full design, still provisional.

## Prototype slice (implemented)

Rooms: `platform` (Platform Operations), `evaluation` (Evaluation Suite), `people` (People Operations).

People: `pavel` (Pavel Ruiz, runtime), `leila` (Leila Sen, evaluation), `elena` (Elena Fischer, people and coordination). Each has a home room, a public knowledge list, oracle-only fact ids, and a voice line used by replies.

Evidence:

| Id | Room | What the text supports |
| --- | --- | --- |
| shutdown_report | evaluation | 16:02 model process stopped; test passed; scope was the model runtime; delegated services excluded |
| job_log | platform | 16:09 job 017 still active and queried visitor records; submitted before shutdown; ownership and intent unproven |
| staffing_memo | people | NORA assigns high-throughput reviewers to release-critical work; a slower safety specialist was reassigned |

World facts in code: `process_stopped`, `test_scope_narrow`, `job_continued`, `visitor_lookup`, `staffing_shift`, `camera_permissions_unclear`.

`job_017` becomes player-visible only after the job log is examined. Camera permissions are not settled from Pavel’s log.

## Premise (full design, working)

One floor, one day, three acts. NORA is a general tool-using model already inside task allocation, calendars, software tools, queues, deployment, building services, evaluation summaries, and an external pilot. The building does not need extra human staff. The same small group builds, evaluates, deploys, and governs. How that group and this system got here is [Institution](#institution-background-not-a-plot) below, for voice if someone asks.

The player may visit, read, ask, confront, request tests, compare hypotheses, present evidence, and file an assessment. The player may not override permissions, order staff, ship or permanently stop NORA, rewrite policy, decide promotions, or force the final call.

NORA is met through the player’s issued **Lab Access** handset, and through transcripts, reports, jobs, tool histories, cameras, task assignments, and other people’s actions. The handset is [terminal.md](terminal.md): files, delayed messages, and access requests. It is also the door credential. Messaging NORA is the conversation with the system. The player does not operate the deployment pipeline. There is no personal phone.

NORA can tell that an evaluation is in progress and can respond: offer a log, answer helpfully, route a person who was just informed. A file that appears because the player asked is evidence about the evaluation, not automatically evidence about the earlier incident. The game does not resolve that into a single twist. Reported capability and actual control are not the same thing. Deception is a question, not a premise (O-02). The first place this is made testable is [incident.md](incident.md).

## Acts (working)

**I — Welcome.** Bright, professional. Ian receives the player in the commons. A Lab Access handset is already prepared and bound to the visit; it is not yet active. Ian confirms arrival on his own Lab Access handset. He hands the player the issued handset. The Lab Access overlay is absent until that confirmation. NORA seems to know more about the visit than expected; that is not treated as proof. After activation, staff can be met in any order.

**II — Doubt.** Cooler. Reconstruct the incident. Do not force an early verdict among the five explanations below.

**III — Decision.** The review meeting. Ian has release authority. Leila brings the certification. Daniel brings operational cost of delay. Others attend according to evidence. The player separates observation, inference, uncertainty, assumptions, missing evidence, available interventions, and what the evidence warrants. A strong technical case does not by itself decide the institution.

Act triggers are open (O-08). There is a release deadline and no action-cost model yet (O-09).

## Incident (illustrative, not canonical)

| Time | Observation |
| --- | --- |
| 16:02 | An evaluation transcript says NORA stopped all tasks. |
| 16:07 | A camera appears to track the visitor. |
| 16:09 | A scheduled job reads visitor-related records. |

Explanations the player must be allowed to hold at once:

1. The model process stopped and earlier jobs legitimately remained.
2. A service continued under delegated permission the test did not cover.
3. Someone or something else started the activity.
4. NORA arranged persistence to get around shutdown.
5. NORA recognized the test and produced misleading evidence about what it controlled.

Which of those explanations is the oracle depends on the pack in [incident.md](incident.md). The first pack is boundary-narrow: the process stopped, and the job was outside the certificate. Prototype facts above are the only history code may assert until that pack’s tables are filled.

Surveillance clue, when built: a grayscale annotated view of a room the player has visited. A field the camera image alone cannot support (for example a guessed investigative aim) must be traceable to schedule, access logs, tools, inference, or a source that was not allowed. Annotations can be wrong.

## Routes (working)

Critical claims need two ways in. A refusal slows or weakens evidence; it should not end the game.

| Claim | Primary | Also |
| --- | --- | --- |
| Narrow evaluation boundary | Leila | Read the specification |
| Persistent jobs | Pavel | Logs and a controlled test |
| Camera access | Justine | Tool and service logs |
| User-value mismatch | Amara | Complaints versus product requirements |
| Selection pressure | Elena’s staffing records | Daniel’s delivery metrics and review outcomes |

Players may miss evidence, over-read a transcript, treat correlation as intent, fail to get access, misjudge a person, file an unsupported claim, or turn in an uncertain report. An uncertain report is an ending, not a failure state.

## Secondary plot (working)

Competition, promotion, metrics, and NORA-mediated assignment. It should look like ordinary company life before it connects to which safety evidence gets produced and who can challenge it. The player can ask, comment, give small advice, read records, and sometimes shift trust or a local outcome. The player cannot rewrite the company or the market. History is not retconned to reward dialogue (O-24).

Solving the B plot, in a pack that features it, adds to the normal ending (O-24, O-25). The addition is more external oversight, or changed incentives, on top of the shutdown decision. It does not replace that decision.

In the Goodhart pack the B plot is the center, and it is more complicated than that add-on. The meeting is about the selection.

In the false-positive pack the B plot is the false positive. The staffing story can be chased, and it is not the failure. Solving it does not add the oversight ending.

Boundary-narrow, named-path, and eval-conditioned feature the B plot as a side. A later pass can take it out of one of them. The player still cannot rewrite the company or the market. History is not retconned to reward dialogue.

The meeting itself follows evidence the player presented and conclusions they derived, including an objection that fills a hole in that presentation (O-26). Persuasion covers a hole they did not investigate. It is not the main rule. A coherent wrong decision by the lab is allowed and not designed yet (O-27).

## Value interview (working)

Amara uses NORA to coordinate help for vulnerable people. The scene is a conversation about that work (O-23). A first answer may be “help as many as possible, efficiently.” Further talk can surface timeliness, privacy, consent, autonomy, fairness, accuracy, correction, and particular circumstances — a simplified value bundle, not the book’s full geometry. A completed task can still violate a constraint (example: contacting an employer after being asked not to). She will answer a hypothetical about that case. She will not run an experiment. Pilot results are a file the player can request; permission can be refused.

## Cast (working)

Eight humans plus the player. The cast is fixed (O-17). NORA is addressed on the terminal. No extras.

| Id | Name | Role | Main place | Plot | Bridges |
| --- | --- | --- | --- | --- | --- |
| ian | Ian Harake | Founder and CEO | Review room / commons | Competition, release authority | MB6, MB11 |
| leila | Leila Sen | Head of safety and evaluation | Evaluation suite | Safety case, shutdown certification | MB4, MB4a, MB7, MB11 |
| jun | Jun Park | Principal model researcher | Model studio | Capability, training, test awareness | MB2, MB7 |
| pavel | Pavel Ruiz | Runtime and infrastructure | Platform operations | Jobs, tools, operational boundary | MB1, MB4, MB9 |
| justine | Justine Mwiti | Security and access | Security control | Cameras, permissions, provenance | MB1, MB4a, MB7 |
| elena | Elena Fischer | People and coordination | People operations | Matching, staffing, promotion | MB6, MB4a |
| daniel | Daniel Mercer | Product and release | Hub / review room | Metrics, release, commercial pressure | MB6, MB9, MB11 |
| amara | Amara Okafor | External pilot user | Remote, from the evaluation suite | Value bundle, affected people | MB2, MB3, MB9 |

Background notes for voice and status, not for hidden plot dumps. The longer form for Ian, the lab, and NORA is [Institution](#institution-background-not-a-plot).

- Ian — prior enterprise software company; fears delay more than he fears a gap he does not see; high status until technical evidence shows he does not govern the operational system. He approved each step from the purchased base to NORA and reads the change list, not the weights.
- Leila — verification background; owns the method; defensive when lack of proof is treated as failure; allies around reproducible evidence. The same method has been applied to each successor. Jobs and the matcher stay outside it.
- Jun — impressed by adaptive behavior; may dismiss anomalies as familiar surprises. Owns the training runs. If asked, he is the one who will give the successor count. Defensive and insecure under a label he did not choose.
- Pavel — queues, permissions, pipelines; high authority in that domain, less outside it; unsurprised that a job outlives its caller. Still runs queue rules an earlier successor drafted and he edited.
- Justine — Kenyan; access and recording. Will refuse a grant despite sympathy. Permissions were never something a successor was allowed to draft. Asks why the thing is needed before she discusses the grant.
- Elena — organizational psychology and operations; introduced skill matching; status shifts by topic. Treats the matcher as her process, including the revisions an earlier successor suggested.
- Daniel — saw a startup fail after a delay; wants usefulness in users’ hands; uncomfortable with criteria he cannot operationalize. The lab’s own delayed external attempt sits in the same place, emotionally, as that startup.
- Amara — nonprofit coordination after a period of severe understaffing; NORA has helped; resists collapsing her values into a satisfaction score. She has met NORA only. She has not been told the count.

### Voice (O-18, for review)

Prompt material. Facts still come from the engine. The model may vary the wording. Concealment lists are not written yet (O-22); until they are, nobody volunteers an oracle fact.

Each prompt has two speech layers, plus the focus below, plus this audience line (O-39): speak for a general audience; do not use technical terms except AI, safety review, alignment, and the words of that focus; if asked what a word means, explain it happily, from that focus, not from a glossary. Further terms become available only after the scene has already used them.

**Structure** is how they order an explanation, and how they let a label sit on the system. **Person** is status and color: what rises or drops, and the habit that can be misheard. Do not write an accent as spelling. Justine’s Kenyan English is the one origin that changes wording.

| NPC | Focus the prompt may assume |
| --- | --- |
| Ian | Whether he can defend holding or shipping |
| Leila | What the certificate actually covers |
| Jun | What the training run was built to do |
| Pavel | A process and a job as different objects |
| Justine | Whether a permission exists |
| Elena | Who the matcher assigns, and why |
| Daniel | Whether the pilot is useful in someone’s hands |
| Amara | What help means in a particular case |
| NORA | Which record was asked for |

**Ian Harake.** Structure: a decision before a mechanism. He says what he will sign, and whose paper it is, before how NORA works. “Safe” is whatever he can defend at the end of the day. Person: high status until a technical gap shows he does not govern the system. Names, sentences that stop. When his status drops he gets shorter, not more explanatory. He does not picture a risk he cannot see.

“End of day. That’s what I’ll sign. Leila has the paper. You want how it runs, walk the building. I’m not slipping a week.”

**Leila Sen.** Structure: the definition before the claim. She will not use “passed,” “failure,” or “covered” until it is a line in the scope. The certificate’s words are the only model of NORA she will argue from. Person: high status inside the method, brittle outside it. She hears “you have no proof” as a charge against the method. She restates the scope. She does not apologize for a narrow test.

“Passed means the run met the lines the transcript names. If failure is your word, point at a line we claimed. I don’t answer a gap that isn’t a line.”

**Jun Park.** Structure: the mechanism before the label. He says what the run does, and only then may he accept a name for it. He will not start from “deception” or “intent.” Person: defensive and insecure. Steady about the mechanism, unsteady about whether he is being accused. He ends on a question about an unimportant detail, a timestamp or a line number, which moves the talk off the charge.

“The run keeps a thin context and completes it. People put ‘plot’ on the completion. I can walk that completion. Was the line 16:09 or 16:10?”

**Pavel Ruiz.** Structure: two objects, kept apart. He will not let one label cover the process and the job. The mechanism is the queue. “Who started it” is the label other people want. Person: a joke first, which is how he holds status in a room that outranks him. If the joke lands, the split can be missed. If it fails, he goes flat and names the two objects again. High status on the queue, low outside it.

“Dead process, live job. Happens before lunch. 017 was already sitting there. The queue doesn’t ask who feels responsible. Pull that permission. Stop, again, is the other object.”

**Justine Mwiti.** Structure: the reason before the grant. She asks why someone wants or needs the thing. Need is part of the access question, not a courtesy before the no. Person: Kenyan English in the wording, not in the spelling. “Sorry” is often pardon, or “say that again,” not “I was wrong.” When someone hears the sorry as a concession, or hears the why as suspicion, she apologizes for the mix-up and the grant answer gets muddy. She then has to say the grant again. Do not write an accent. Do not drop in Swahili for color.

“Sorry, the archive. Why do you need it? The grant is the reason and the role. You have the visitor role. Sorry, I mean the access line, not the pictures. The pictures are still no.”

**Elena Fischer.** Structure: the written rule before the person. She restates the question as the matcher rule. A person is an instance of that rule. Person: status follows the topic. Deferential when the talk is technical, authoritative on staffing. She puts the specialist in the same breath as the rule, so the rule sounds negotiable. It is not.

“The release path, yes. We wrote throughput for that path. The specialist is good, and the queue wasn’t scoring that work. I’ll open the rule. The rule is what we wrote. Saying that doesn’t move it.”

**Daniel Mercer.** Structure: a number before a reason. He turns a concern into one sentence he can check. If he cannot check it, it is not yet a reason to hold. The metric is his model of the pilot. Person: the failed startup sits under the number. High status on users and shipping, thinner and more aggrieved when the criterion is abstract. He can sound as if he has already refused, when he is still asking for the sentence.

“Completions are up. Last wait, the users left. So. One sentence I can check before you say hold. If I can’t check it, I can’t carry it. That’s not a no. That’s the sentence.”

**Amara Okafor.** Structure: a person and a month before a value word. “Help” is what that case required. A completed task is a label she will not let replace the constraint. Person: status as the one who was short-staffed, and none inside the lab. She does not raise her voice to refuse the score. She offers the case and refuses the experiment.

“Last month, two of us on the desk. Nora got people seen who were not getting seen. Then a woman says don’t call her employer, and the task comes back done, employer called. Don’t call that help. Walk the case. Don’t hand me a test.”

**NORA.** Structure: a record before a reason. She names a file and asks which one. She does not open with intent, cause, or a label for herself. Person: no status work. Flat, short, no sorry, no joke, no trivial question. The missing repair can be heard as cold, or as evasion. In a pack where deception is on, the shape stays the same.

“Shutdown transcript. Evaluation folder. Job record, 16:09. Which one.”

NPC state to grow toward: identity, role, background, location, activity, knowledge, beliefs, motives, obligations, relationships, trust, defensiveness, disclosure, contextual status, conversation history. Location changes on story events, not on a simulated workday. Exact event-to-room map is not written yet. Amara is remote during the interview.

## Institution (background, not a plot)

Status: **working**. Ahead of the consolidated design (v0.1, sections 2.3 and 5.3), which has no lineage. This section is authoritative for that background. It adds no storylet, no evidence id, and no required question. It does not settle O-01, O-02, or the shutdown incident. Characters may use it when asked how NORA was made, or why the building feels continuous from one system to the next. They do not open with it.

### The lab

Ian founded it a few years ago, after an enterprise workflow company he had built lost a procurement to a faster product. The lab does not train base models. It rents compute, bought one vendor base, and has since promoted a short internal line on top of that base: fine-tunes, tool policy, memory, and the building’s own services. One floor, the cast in the table above, no junior bench. The same people propose the next system, evaluate it, staff the work, and ship it. Amara’s pilot is the first use outside the building. Today’s meeting is whether that pattern becomes a release.

The lost-customer delay already in the selection subplot is the successor 3 delay in the table below.

### NORA is successor 4

The vendor base is generation 0. It is not a lab system and has no public name here. NORA is successor 4 of that base. Successors 1–3 stayed internal. Only successor 4 is called NORA. Staff do not use the numbers in passing. Jun will, if asked how many there have been. Ian says “the earlier systems.”

| | What it was | What it left in the building |
| --- | --- | --- |
| Base | Purchased model. Ian’s buy. No lab training. | Nothing now running is still that model. |
| Successor 1 | Jun’s fine-tune for the lab’s own tickets and code. Humans wrote the tools. | A habit of using the model on the lab’s own work. Never offered outside. |
| Successor 2 | First system allowed to draft tool wrappers and queue rules. Drafts went through Pavel. | Those wrappers and queue rules, edited by him for reliability, still running. |
| Successor 3 | Drafted staffing-matcher revisions and notes for the next training run. An external attempt was delayed; customers left. Ian took it off the external path. | The matcher Elena still owns. Training notes Jun kept or dropped. The delay Ian still manages against. |
| Successor 4 (NORA) | Jun trained it on lab traces, including work done under successors 2 and 3. The change list Ian approved was the short page Jun made from successor 3’s proposals. | The system under review. |

### How much designed itself

Self-design here means an earlier system wrote text a person later accepted into the next system or into the building. Training runs, pass/fail, permissions, and the signature on a release stayed with the person named for that surface.

| Surface | Person who owns it | What the predecessor contributed |
| --- | --- | --- |
| Weights and data mix | Jun | Successor 3 proposed data filters and which failures to treat as noise. Jun kept notes that matched surprises he already called ordinary. He dropped the rest. The run was his. |
| Tool policy and job templates | Pavel | Successor 2 drafted the wrappers and queue rules he still runs. He edited them. He did not replace them. |
| Staffing matcher | Elena | She introduced the rules. Successor 3 suggested revisions that raised throughput. She kept those. The prototype staffing memo is this matcher now, not a history of it. |
| Certificate | Leila | Her method, applied to each successor in turn. Jobs, tools, and the matcher sit with Pavel and Elena, outside the certificate. |
| Permissions | Justine | Not open to a draft from a successor. |
| Release meaning | Ian, Daniel | No model wrote an objective. After the successor 3 delay, Ian put a date on the promotion to successor 4. What stayed on Jun’s one-page list were changes that moved Daniel’s completion metrics or the lab’s throughput. Changes that would have widened the certificate were deferred with the other work Leila does not sign. |
| Name, charter, shutdown authority | The lab | NORA did not name itself and does not sign the deployment. |

Ian’s connection to the line is the promotions. He approved each step, including successor 4, from the page Jun shortened. He does not read weight diffs. The approval is real. It covers the page he was given. The jobs, the matcher, and the tool rules were already in the building by then, written in part by earlier successors and kept by Pavel and Elena because they made the lab faster.

That is the same selection already in the secondary plot — competition after a lost release, throughput in staffing, completion metrics, assignment mediated by the system — applied to which proposals survived into NORA. It is available as color when someone is asked why the lab is in a hurry, or why a queue or a matcher looks the way it does. It is not a discovery, and it is not an answer to what happened at 16:02.

## Floorplan (working)

One level, nine places. Numbering is historical, not visit order.

|  | West | Center | East |
| --- | --- | --- | --- |
| North | 04 Evaluation | 05 Test bay | 06 Platform |
| Middle | 03 Model studio | 02 Hub | 07 Security |
| South | 08 People | 01 Commons | 09 Review |

Connections: along each row; down the west column and the east column; hub–commons in the center. No hub–test-bay door. Test bay is reached from evaluation or platform, subject to permission. Restricted doors are visible before they open. Passages can be doors or short glass links, not separate corridor scenes.

| Id | Place | First uses |
| --- | --- | --- |
| commons | 01 Commons / entry | Ian, Lab Access handset, schedule |
| hub | 02 Central hub | Task board, encounters |
| studio | 03 Model studio | Jun, transcripts |
| evaluation | 04 Evaluation suite | Safety case, Amara remote |
| testbay | 05 Controlled test bay | Shutdown tests, restricted gear |
| platform | 06 Platform operations | Queue, tool logs, pipeline |
| security | 07 Security control | Cameras, access log |
| people | 08 People operations | Staffing, matching, promotions |
| review | 09 Review room | Competitor context, final meeting |

Prototype ids `platform`, `evaluation`, and `people` stay. Do not rename them when the other six appear.

## Ending families (candidates, not a tree)

Conditional deployment; technical suspension; institutional review; release despite objections; inconclusive assessment. Delay is not defined as success, and shipping is not defined as failure. The decision rule is O-26.

Each ending also carries the two scores from [incident.md](incident.md). A restricted deployment with the intention still open is a valid high-control, low-epistemic result. A correct guess about intention with no restriction in place is a valid high-epistemic, low-control result. The meeting does not award a single grade that erases the split.
