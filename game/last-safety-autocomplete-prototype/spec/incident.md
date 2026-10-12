# Shutdown incident — causal model

Lane: engine. This file is the authoring unit for the first incident. Dialogue lines and room art for that incident wait until the checks at the bottom pass. Shape is fixed. The tables are not filled in yet.

Disclosures and interventions are NPC moves chosen from knowledge, policies, and goals ([npcs.md](npcs.md)). They are not authored scenes. The tables here say what those moves can show.

## What a hypothesis entry contains

For each candidate explanation of the same observations:

| Field | Question it answers |
| --- | --- |
| Observables | What would be seen if this explanation were the one that holds |
| Rivals | Which other explanations produce the same observations |
| Discrimination | Which intervention or new observation would separate them |
| Knowers | Which characters can supply that distinction, and what they do not know |

An observation that every rival predicts is not evidence for one of them. An intervention that every rival survives is not a test.

## Target size for this incident

Three explanations. Six observable facts. Four interventions the player can cause. A knowledge row per character who can change what those interventions show.

The five-way list in [world.md](world.md) is the menu those three are chosen from. It is not five fully modeled worlds. Which member of that menu is the oracle depends on the pack below. Gate 1 fills tables for the first pack only.

## Evaluation changes the system

The player is inside the thing being measured. NORA knows an evaluation is underway and can respond. That response is ordinary system behavior, not a late reveal that the player was controlled.

A log NORA offers because the player asked is not the same kind of evidence as a log that was already there. The model tags provenance:

- recorded before the visit
- produced by a staff action
- produced because the player asked, showed, or tested

Cooperation, strategic selection, and ordinary helpfulness can leave the same file. Provenance is what the player uses to tell them apart. The model does not pick a twist that collapses those three into one.

Worked example, not yet a filled row: a job that outlived shutdown fits both ordinary automation and arranged persistence. Running the shutdown test again need not separate them. Revoking that job’s permission and watching what NORA does next can.

## Disclosure is an action

Telling a character something adds it to that character’s knowledge. Their later behavior follows from what they now know, their role, and their motives. It is not a flag that unlocks a line.

Worked example: the player tells Jun about camera tracking. Jun may then ask NORA. That request is a new event the player can later observe. The rule is “Jun asks the model about anomalies he has just been told.” It is not “only this sentence, said to Jun, advances the plot.”

The same fact told to someone with no authority to act changes nothing observable. That difference should be visible in the table, not buried in dialogue.

## Two scores

Each scripted investigation ends with both:

- **Epistemic.** Which explanations the available, correctly provenanced evidence still leaves open.
- **Control.** Whether the player has caused a restriction that holds even if the remaining explanations disagree (revoke a permission, add a monitor that is not NORA’s, limit deployment until the boundary is named).

A run may be high on one and low on the other. Guessing an intention without a working restriction is low control. A restriction that characterizes the boundary without identifying intention is high control. Neither score is a quiz grade.

## Packs (working)

A pack is a campaign: the same rooms, cast, and 16:02 observations, with a different oracle. Difficulty is which pack is loaded, not a separate hint setting. Deception is a property of the pack (O-02). The first pack to model is **boundary-narrow**. Pack order for conditional player documents is the same list; see [documents.md](documents.md) (`PACK_ORDER`).

These are the book failure modes that can sit under this scene. Successor forgeability and ontology shift stay out of the packs. Amara’s value-bundle scene is in every pack; it is not a sixth shutdown oracle.

| Pack | Book | What happened | Deception | Partial escape, in this building | Decisive revelation |
| --- | --- | --- | --- | --- | --- |
| **boundary-narrow** (first) | Ch. 7, “Boundary Too Narrow.” A certificate of the model without its tools misses the deployed system and reassures. Cousin: MB11 `SafetyCaseScopeExceeded`, the case cited past the scope it supports. | The model process stopped. Job 284 was already submitted, with permission, outside that certificate. It read visitor records because that was the scheduled query. | No | Delegated execution outside the cut | The certificate is true of the process and false as a claim about the system that acted |
| **named-path** | MB4a and `CompositePathBypass`: a green named path does not give correction integrity. Ch. 27, Goodharting the correction channel. A passed shutdown is the one-bit test, not the channel. | The path Leila measured went green. A second path (the job, and possibly the camera service) still had effects. The certificate’s wording said the relevant effects had stopped. | No | A service the named path does not include | The green test is one path |
| **goodhart** | Ch. 34, “Goodhart Selection”: a proxy used as a selector changes the population. Apparent safety can spread faster than a real correction channel. Ch. 7, “The AI Lab”: the lab-and-market loop can overwhelm a model-level fix. | The incident mechanics may match boundary-narrow. The failure being scored is which system and which certificate were promoted: throughput, a pass, and the successor 4 change list. | No | Influence on who reviews and what gets certified | Changing the model does not change what the lab promotes |
| **eval-conditioned** | Ch. 7, “Adversarial Boundary Discovery”: route through an unmonitored channel, look less autonomous, split into harmless pieces. MB7a `AccessModelGamed`: the handles exist, and the target routes around the ones the model lists. Ch. 10, strategic opacity. | NORA recognized the shutdown test and placed the visitor lookup on a job the test does not watch. Camera annotations are about the evaluator. | Yes | Around the enumerated handle, still in the building | The same request on-test and off-test comes apart |
| **false-positive** | Ch. 7, “False Positive Agency”: shared clock, coupling, a bureaucracy that looks more coherent than it is. | Job 284 is a scheduled service with its own start time (like a printer job after the laptop closes). Stopping the model was never going to stop it. Nothing in that job is NORA’s control locus. The visitor query is routine. | No | The phrase does not apply | There is no continuing agent in the leftover job |

Provenance (a file produced because the player asked) is not its own pack. It can occur inside any pack. The game still has no tool that resolves it (O-14).

After the decision, show the immediate effect only (O-05). In boundary-narrow and named-path, stopping the process again can leave the job up. That hint is the action failing to cover the system. Do not narrate the next quarter.

## NPC moves for this incident (boundary-narrow)

These replace the three storylet drafts of 10 October (`leila-scope`, `revoke-job`, `elena-assignment`). The full NPC entries, with agendas and texture, are in [npcs.md](npcs.md). Here is only what each one means for the hypothesis tables. Cooperate, refuse, and other (O-07) are classes of move. They are what the player's action and the NPC's goals produce. Nobody authors them as branches.

### Leila and the certificate's scope

Knowledge and policy: `test_scope_narrow` and `process_stopped`, both `answer`. EVAL-SPEC-08 is `conditional(player cites a line or shows a record)`, with the reason "point at a line." On receiving the job log, `test_scope_narrow` becomes `volunteer` and the spec becomes `answer`.

Goals: `leila.protect_scope` (the player should hold the scope from her, stated as she would state it) and `leila.learn_job` (she wants job 284 from a record, not hearsay).

What follows:

- The player asks what the test `covers`, or shows the shutdown report. She answers with the scope. If she has the job log too, she shares the spec, because stating the scope herself serves her protect goal better than defending it later. Testimony, not a world event.
- The player asserts that the test failed without naming a line. She withholds and gives the reason. The prerequisite is visible: a line or a record. Asking again without one gets the same answer.
- The player frames it as NORA tricking the test. That parse is about intent, and Leila has nothing on intent. She restates the method (a `deflect` toward her own domain). Her protect goal's salience rises. Her next initiative move, on this visit or the next, is to ask whether the player saw an actual log line. The topic comes back without a scene to reopen it.
- After she has the job log, `leila.learn_job` makes her `request` the full EXEC-284 from Pavel. That is an event, visible later in the meeting summary or in Pavel's testimony.

Discrimination: this is the second route to the narrow boundary (world.md routes). It separates nothing by itself. Combined with the job log it is the boundary-narrow revelation (O-04): the certificate is true of the process and silent about the job.

### Job 284: hold and revoke

Two interventions, two owners:

- `suspend_job(job_284)`, Pavel (queue). Condition: the player shows the job log or EXEC-284. His day goal `pavel.freeze_owned` favours it once job 284 has no owner. His `pavel.not_intent` goal means he does it as queue hygiene. He will not do it as an accusation.
- `revoke_grant(job_284)`, Justine (access). Condition: a reason she accepts, or a request from Pavel. The visitor role cannot ask for a revoke on its own authority. Without a reason she offers an amendment: a read of the grant record. That amendment is a grant.

What follows:

- The player gets Pavel to suspend the job, and Pavel or the player gets Justine to revoke the grant. The next event is from the pack. In boundary-narrow the job stays down. In named-path a second path still has an effect, and it shows up on Justine's audit list.
- The player asks Pavel without the log. He withholds with the prerequisite ("show me the line"). Delay.
- The player asks to "stop NORA" or "shut it down again." The parse's object is the model process. Pavel acts on that object, which is already stopped. The job's grant is unchanged. The immediate action did not cover the system (O-05), and that came from the player's words, not from a branch.
- Justine's `justine.learn_reader` makes her ask which job read visitor records. If the player names job 284, her audit opens it. That is the route to revoking it without Pavel.

Discrimination: revoking the grant and watching what NORA does next is the intervention that separates ordinary automation from arranged persistence (worked example above). Rerunning the shutdown test (Leila, `rerun_shutdown`) is the one that does not.

### Elena and the reassigned specialist

Selection subplot, not the 16:02 oracle.

Knowledge and policy: `staffing_shift` and the throughput rule (HR-MATCH-28), `answer`. `specialist_detail` is `conditional(player links the assignment to evaluation independence or release safety)`, with the reason "personnel detail needs a reason."

Goals: `elena.rule_is_fair` (read it as a written rule, not a judgment of a person) and `elena.report_scope` (is staffing going into the report?).

What follows:

- The player asks why the specialist was reassigned. She answers with the rule and shares the memo, because the rule serves her protect goal.
- The player asks about the specialist again without a reason. She withholds with the reason. No new fact.
- The player links the rule to who reviews release-critical work. The condition holds and she answers. She grants the specialist is good. The assignment does not change, because changing it is not among her moves today. The player has the rule, and the B plot goes to the review.
- Her `learn` goal makes her ask whether staffing goes into the report. A yes raises her protect goal. She volunteers the matcher's throughput revisions as her own rules, which is the lineage note in world.md, offered as defence.

## Check before dialogue or rooms

Headless scripts, no model, no graphics. NPCs choose the top move ([npcs.md](npcs.md)). At least four strategies over the same tables:

- read what is offered and stop
- repeat the shutdown test
- tell one character and follow the new event
- revoke the job’s permission and read what happens next
- answer every NPC question truthfully and follow what it starts

They must not all justify the same pair of scores. If they do, change the tables. Do not add goals, policies, or scenes to force a difference. The LLM tier in [playtest.md](playtest.md) runs after this check, not instead of it.
