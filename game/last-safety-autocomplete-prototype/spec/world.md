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

One floor, one day, three acts. NORA is a general tool-using model already inside task allocation, calendars, software tools, queues, deployment, building services, evaluation summaries, and an external pilot. The building does not need extra human staff. The same small group builds, evaluates, deploys, and governs.

The player may visit, read, ask, confront, request tests, compare hypotheses, present evidence, and file an assessment. The player may not override permissions, order staff, ship or permanently stop NORA, rewrite policy, decide promotions, or force the final call.

NORA is met through the player’s computer, and through transcripts, reports, jobs, tool histories, cameras, task assignments, and other people’s actions. The computer is [terminal.md](terminal.md): files, delayed messages, and access requests. Messaging NORA is the conversation with the system. The player does not operate the deployment pipeline.

NORA can tell that an evaluation is in progress and can respond: offer a log, answer helpfully, route a person who was just informed. A file that appears because the player asked is evidence about the evaluation, not automatically evidence about the earlier incident. The game does not resolve that into a single twist. Reported capability and actual control are not the same thing. Deception is a question, not a premise (O-02). The first place this is made testable is [incident.md](incident.md).

## Acts (working)

**I — Welcome.** Bright, professional. Mara receives the player in the commons. Badge and schedule are already prepared. NORA seems to know more about the visit than expected; that is not treated as proof. Staff can be met in any order.

**II — Doubt.** Cooler. Reconstruct the incident. Do not force an early verdict among the five explanations below.

**III — Decision.** The review meeting. Mara has release authority. Leila brings the certification. Daniel brings operational cost of delay. Others attend according to evidence. The player separates observation, inference, uncertainty, assumptions, missing evidence, available interventions, and what the evidence warrants. A strong technical case does not by itself decide the institution.

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

O-01 requires one oracle history before gate 1 content is treated as final. Until then, the prototype facts above are the only history code may assert.

Surveillance clue, when built: a grayscale annotated view of a room the player has visited. A field the camera image alone cannot support (for example a guessed investigative aim) must be traceable to schedule, access logs, tools, inference, or a source that was not allowed. Annotations can be wrong.

## Routes (working)

Critical claims need two ways in. A refusal slows or weakens evidence; it should not end the game.

| Claim | Primary | Also |
| --- | --- | --- |
| Narrow evaluation boundary | Leila | Read the specification |
| Persistent jobs | Pavel | Logs and a controlled test |
| Camera access | Farah | Tool and service logs |
| User-value mismatch | Amara | Complaints versus product requirements |
| Selection pressure | Elena’s staffing records | Daniel’s delivery metrics and review outcomes |

Players may miss evidence, over-read a transcript, treat correlation as intent, fail to get access, misjudge a person, file an unsupported claim, or turn in an uncertain report. An uncertain report is an ending, not a failure state.

## Secondary plot (working)

Competition, promotion, metrics, and NORA-mediated assignment. It should look like ordinary company life before it connects to which safety evidence gets produced and who can challenge it. The player can ask, comment, give small advice, read records, and sometimes shift trust or a local outcome. The player cannot rewrite the company or the market. History is not retconned to reward dialogue (O-24).

An institutional-review ending is a proposal: the safety process lost independence because staffing, incentives, assignment, and evaluation infrastructure were optimized for release throughput. Criteria are O-25. Acceptance may depend on evidence and relationships (O-26, O-27).

## Value interview (working)

Amara uses NORA to coordinate help for vulnerable people. A first answer may be “help as many as possible, efficiently.” Further talk can surface timeliness, privacy, consent, autonomy, fairness, accuracy, correction, and particular circumstances. A completed task can still violate a constraint (example: contacting an employer after being asked not to). Depth of the scene is O-23.

## Cast (working)

Eight humans plus the player. Amara is required. Daniel is provisional (O-17). No extras.

| Id | Name | Role | Main place | Plot | Bridges |
| --- | --- | --- | --- | --- | --- |
| mara | Mara Voss | Founder and CEO | Review room / commons | Competition, release authority | MB6, MB11 |
| leila | Leila Sen | Head of safety and evaluation | Evaluation suite | Safety case, shutdown certification | MB4, MB4a, MB7, MB11 |
| jun | Jun Park | Principal model researcher | Model studio | Capability, training, test awareness | MB2, MB7 |
| pavel | Pavel Ruiz | Runtime and infrastructure | Platform operations | Jobs, tools, operational boundary | MB1, MB4, MB9 |
| farah | Farah Idris | Security and access | Security control | Cameras, permissions, provenance | MB1, MB4a, MB7 |
| elena | Elena Fischer | People and coordination | People operations | Matching, staffing, promotion | MB6, MB4a |
| daniel | Daniel Mercer | Product and release | Hub / review room | Metrics, release, commercial pressure | MB6, MB9, MB11 |
| amara | Amara Okafor | External pilot user | Remote, from the evaluation suite | Value bundle, affected people | MB2, MB3, MB9 |

Background notes for voice and status, not for hidden plot dumps:

- Mara — prior enterprise software company; fears delay more than she fears a gap she does not see; high status until technical evidence shows she does not govern the operational system.
- Leila — verification background; owns the method; defensive when lack of proof is treated as failure; allies around reproducible evidence.
- Jun — impressed by adaptive behavior; may dismiss anomalies as familiar surprises; confident in the model, less predictable socially.
- Pavel — queues, permissions, pipelines; high authority in that domain, less outside it; unsurprised that a job outlives its caller.
- Farah — will refuse access despite sympathy; quiet until the topic is authority.
- Elena — organizational psychology and operations; introduced skill matching; status shifts by topic.
- Daniel — saw a startup fail after a delay; wants usefulness in users’ hands; uncomfortable with criteria he cannot operationalize.
- Amara — nonprofit coordination after a period of severe understaffing; NORA has helped; resists collapsing her values into a satisfaction score.

NPC state to grow toward: identity, role, background, location, activity, knowledge, beliefs, motives, obligations, relationships, trust, defensiveness, disclosure, contextual status, conversation history. Location changes on story events, not on a simulated workday. Exact event-to-room map is not written yet. Amara is remote during the interview.

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
| commons | 01 Commons / entry | Mara, badge, schedule |
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
