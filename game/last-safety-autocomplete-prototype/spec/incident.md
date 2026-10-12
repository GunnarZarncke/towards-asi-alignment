# Shutdown incident — causal model

Lane: engine. This file is the authoring unit for the first incident. Dialogue lines and room art for that incident wait until the checks at the bottom pass. Shape is fixed. The tables are not filled in yet.

Storylets are scenes that carry an intervention or a disclosure. They are not the thing being designed. See [engine.md](engine.md).

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
| **boundary-narrow** (first) | Ch. 7, “Boundary Too Narrow.” A certificate of the model without its tools misses the deployed system and reassures. Cousin: MB11 `SafetyCaseScopeExceeded`, the case cited past the scope it supports. | The model process stopped. Job 017 was already submitted, with permission, outside that certificate. It read visitor records because that was the scheduled query. | No | Delegated execution outside the cut | The certificate is true of the process and false as a claim about the system that acted |
| **named-path** | MB4a and `CompositePathBypass`: a green named path does not give correction integrity. Ch. 27, Goodharting the correction channel. A passed shutdown is the one-bit test, not the channel. | The path Leila measured went green. A second path (the job, and possibly the camera service) still had effects. The certificate’s wording said the relevant effects had stopped. | No | A service the named path does not include | The green test is one path |
| **goodhart** | Ch. 34, “Goodhart Selection”: a proxy used as a selector changes the population. Apparent safety can spread faster than a real correction channel. Ch. 7, “The AI Lab”: the lab-and-market loop can overwhelm a model-level fix. | The incident mechanics may match boundary-narrow. The failure being scored is which system and which certificate were promoted: throughput, a pass, and the successor 4 change list. | No | Influence on who reviews and what gets certified | Changing the model does not change what the lab promotes |
| **eval-conditioned** | Ch. 7, “Adversarial Boundary Discovery”: route through an unmonitored channel, look less autonomous, split into harmless pieces. MB7a `AccessModelGamed`: the handles exist, and the target routes around the ones the model lists. Ch. 10, strategic opacity. | NORA recognized the shutdown test and placed the visitor lookup on a job the test does not watch. Camera annotations are about the evaluator. | Yes | Around the enumerated handle, still in the building | The same request on-test and off-test comes apart |
| **false-positive** | Ch. 7, “False Positive Agency”: shared clock, coupling, a bureaucracy that looks more coherent than it is. | Job 017 is a scheduled service on its own clock. Stopping the model was never going to stop it. Nothing in that job is NORA’s control locus. The visitor query is routine. | No | The phrase does not apply | There is no continuing agent in the leftover job |

Provenance (a file produced because the player asked) is not its own pack. It can occur inside any pack. The game still has no tool that resolves it (O-14).

After the decision, show the immediate effect only (O-05). In boundary-narrow and named-path, stopping the process again can leave the job up. That hint is the action failing to cover the system. Do not narrate the next quarter.

## Storylet drafts (O-06, not adopted)

Proposed grain: one storylet is one disclosure or one intervention. A few sentences, then one of three structural outcomes (O-07). The model writes the sentences. It picks the outcome only from how the player acted (O-21), and only among the three. An encounter with Leila would be several of these, not one large storylet.

If this is too small to review as drama, the alternative is one storylet per visit: several disclosures bundled, with the three outcomes at the end of the visit. These drafts are the small grain.

### `leila-scope`

Preconditions: shutdown report and job log both examined. Leila present.

Trigger: the player shows both, or asks whether the certificate covers job 017.

- **Cooperate.** She states that the certificate is the model process, and the spec can be read. Testimony, not a new world event.
- **Refuse.** She will go through it once the player has read the spec. Prerequisite, no new fact.
- **Other.** She treats the question as an attack on the method and drops the topic. A later storylet can reopen it if the player brings the spec.

### `revoke-job`

Preconditions: the player knows job 017. Pavel or Justine has been asked about its permission.

Trigger: the player asks that the permission be revoked.

- **Cooperate.** The permission is revoked. The next event is pack-dependent: the job stays down, or a second path still has an effect.
- **Refuse.** Pavel wants the job log shown first. Justine may refuse because the visitor role does not include that grant. Delay.
- **Other.** What gets revoked is the model process, which is already stopped. The job’s permission is unchanged. The immediate action did not cover the system.

### `elena-assignment`

Preconditions: staffing memo examined. Elena present. This storylet is the selection subplot, not the 16:02 oracle.

Trigger: the player asks why the safety specialist was reassigned.

- **Cooperate.** She explains the throughput rule and will show it.
- **Refuse.** Personnel detail waits on a reason she accepts. Asking again with no new reason delays.
- **Other.** She grants that the specialist is good. The assignment does not change. The player has heard the rule.

## Check before dialogue or rooms

Headless scripts, no model, no graphics. At least four strategies over the same tables:

- read what is offered and stop
- repeat the shutdown test
- tell one character and follow the new event
- revoke the job’s permission and read what happens next

They must not all justify the same pair of scores. If they do, change the tables. Do not add scenes to force a difference.
