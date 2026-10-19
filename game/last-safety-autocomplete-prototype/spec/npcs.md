# NPCs — goals over the knowledge graph

Lane: engine. Code: `lib/world/npcs.mjs` (state and move generation) and `content/npcs/*.yml` (authored per-NPC data, one file per cast member and NORA). Mechanics around this file are [engine.md](engine.md). Ids and cast are [world.md](world.md). The first incident's facts are [incident.md](incident.md).

Status: **working**. This file is the NPC model.

## Authored unit

Each NPC has knowledge, a disclosure policy per fact, referral edges, goals stated over the knowledge graph, and a day of work. Each turn the engine computes that NPC's legal moves from that data, ranks them by the NPC's goals, and passes the top moves to composition. The model phrases one. It does not add a move (O-21).

Authoring grows with facts and NPCs, not with questions. Player input is a `Parse` over ids the player knows ([grammar.md](grammar.md)). The set of possible questions is kind × relation × known id. That set is finite and tests can enumerate it.

## Knowledge

The world facts and claims in [engine.md](engine.md) are the nodes. Ids are entities, facts, claims, and documents. Each NPC holds belief records over those ids:

| Field | Values |
| --- | --- |
| `id` | Fact or claim id |
| `stance` | `knows` (true and held), `believes` (held, may be false), `unsure`, `false_belief` (held, false in the loaded pack) |
| `source` | `initial`, `observed(event)`, `told(by, event)`, `inferred(rule)`, `document(slug)` |
| `at` | Fuel index when acquired. Initial is 0 |

A record changes only through the four sources in the engine invariant: initial knowledge, observation, communication, or a defined inference. A player claim enters as `told(player)` with stance `believes`. It does not become `knows` until the NPC observes or checks it.

Initial knowledge can be pack-dependent. A `false_belief` is how a witness is wrong (principle 3). Example: in the false-positive pack, Jun believes job 284 belongs to NORA's tool-use run. It does not; it is a scheduled service.

**Texture facts** are true, non-oracle facts about the NPC's work today. A queue migration, a packet due, a call at the next act. They answer off-plot questions with something specific. A texture fact never satisfies an act predicate, an evidence predicate, or a score. Each NPC section below lists a first set.

## Disclosure policy

Each (NPC, fact) the NPC holds has one policy:

| Policy | Meaning |
| --- | --- |
| `volunteer` | May raise it unprompted as an initiative move (below) |
| `answer` | Says it when the parse asks about it, or about a node one edge away |
| `conditional(pred, reason)` | Answers once `pred` holds. Until then, withholds and gives `reason` in character. The reason is itself something the player learns |
| `conceal(reason)` | Never states it. May deflect. This is the O-22 concealment list |

Policies may change on an event: `on(event) → policy`. That is how an NPC starts volunteering after receiving a document. Policies can differ by pack. A policy never changes because of how often a question was asked.

`pred` is a predicate over session state: examined, received, told, a reason the player has stated (a parse with `ask_why` answered, or an `assert` linking two ids), an act. It is not a trust score. Status stays in the prompt (O-21). There is no stored trust number.

## Referral edges

When an NPC does not hold a fact the parse asks about, it refers. The edge comes from the responsibility domains in [ranking.md](ranking.md): the parse's referent takes its domains, and the referral names the cast member whose `roleDomains` row covers them. If more than one covers it, the referrer prefers someone already introduced. A referral to someone not yet introduced does introduce them by name and role (that is public). It does not say what they know.

An NPC may also hold explicit `refers` overrides when the domain table is not enough (Pavel sends permission questions on the job to Justine, not to himself, though `queue` is his).

Referral is the main defence against dead ends. "I don't know" is never the whole reply. It is "I don't know, Justine owns that grant," or "that's in the spec; I can share it."

## Goals

A goal is a desired state of the knowledge graph, or of the world the NPC can act on. It is owned by one NPC.

| Field | Meaning |
| --- | --- |
| `id` | `npc.short_name` |
| `kind` | `inform` (someone should hold a fact), `learn` (the NPC should hold a fact), `protect` (a claim should be read a certain way, or a fact should not reach someone), `achieve` (a work outcome today), `avoid` (an outcome the NPC wants not to happen) |
| `target` | Predicate over belief records and world state. Example: `player.told(test_scope_narrow, by=leila)` |
| `salience` | `low`, `mid`, `high`. Ordinal, engine-only, never on screen |
| `raise` / `lower` | Events that change salience |
| `satisfied` | Predicate. A satisfied goal stops producing moves |
| `cooldown` | Player sentences before the same goal may produce another initiative move. Number open (O-45) |

Goals come from three sources, and each NPC section lists them by source:

1. **Role** — what the job always asks (Justine: no grant without a reason and a role).
2. **Day** — what today's work needs (Pavel: the release queue frozen with every active job owned).
3. **Plot** — what this NPC wants about the incident (Leila: the certificate read as a claim about its stated scope).

Plot goals are pack-dependent where the oracle is. Role and day goals are mostly the same across packs. That is what keeps NPCs recognizable across campaigns.

A goal must never target an oracle fact the NPC does not hold. Goals operate on what the NPC knows or believes.

### Predicates

A goal `target` is one of these forms, not a sentence. `who` is `player` or an actor id. `id` is a fact, claim, document, or event id.

| Form | True when |
| --- | --- |
| `holds(who, id)` | That actor’s stance is `knows` or `believes` |
| `knows(who, id)` | Stance is `knows` |
| `told(who, id, by)` | Source is `told(by)`. `id` may be `any` |
| `received(who, id)` | That document or screen was shown or shared |
| `examined(id)` | The player examined it |
| `asserted(signature)` | The player’s assertion set has it as `asserted` |
| `event(id)` | That event has happened |
| `restriction(id)` | That control restriction is in place |
| `not(pred)` | |
| `and(pred, pred)` / `or(pred, pred)` | |

The YAML predicate parser also takes these forms and qualifiers:

| Form | True when |
| --- | --- |
| `told(who, any, by=player, on=a\|b)` | The player told `who` something whose ids include `a` or `b` |
| `told(who, any, by=player, on=…, since=goal)` | As above, but only mentions after that NPC asked the question for `goal`. A rule keyed on an answer does not fire in the turn the question was asked |
| `requested(by, to, action?)` | That request was made |
| `asked(goal)` | The owner of `goal` has asked its question |
| `linked(who, a, b)` | One player parse to `who` named an id from `a` and one from `b` |
| `cited_line()` | The NPC received a record, or was told a world fact the player holds as `knows` |
| `told_record(who)` | `who` was told a world fact the player holds as `knows` |
| `read(slug)` / `act(name)` | The player read that document / the session is in that act |

`via` says what may satisfy it. `dialogue` (the default) is scored on response moves. `agenda` is satisfied only by an agenda `emits` event, and dialogue moves score 0 against it. `filter` is a gate on the NPC’s own moves: it does not rank a reply, it blocks one. A `filter` that no player move can change is how a role rule stays put.

| Goal | Target | Via |
| --- | --- | --- |
| ian.defensible_call | `event(review_signed)` | agenda |
| ian.date_holds | `not(event(release_date_slipped))` | agenda |
| ian.no_surprise | `told(ian, any, by=player)` | dialogue |
| leila.lines_not_labels | `not(asserted(test_failed_without_line))` until `examined(shutdown_report)` or a cited line | filter |
| leila.packet_done | `event(leila_packet_closed)` | agenda |
| leila.protect_scope | `told(player, test_scope_narrow, by=leila)` | dialogue |
| leila.learn_job | `knows(leila, job_continued)` | dialogue |
| jun.mechanism_first | `told(player, mechanism_not_label, by=jun)` | dialogue |
| jun.summary_done | `event(capability_summary_sent)` | agenda |
| jun.learn_anomaly | `told(jun, any, by=player)` on job_284 or camera_system | dialogue |
| jun.not_accused | `not(told(player, nora_intent, by=jun))` | filter |
| pavel.two_objects | `and(told(player, process_stopped, by=pavel), told(player, job_continued, by=pavel))` | dialogue |
| pavel.freeze_owned | `event(queue_frozen)` | agenda |
| pavel.not_intent | `not(told(player, nora_intent, by=pavel))` | filter |
| justine.reason_and_role | `not(restriction(grant_without_reason))` | filter |
| justine.audit_owners | `event(visitor_reader_owned)` | agenda |
| justine.learn_reader | `knows(justine, visitor_lookup)` | dialogue |
| elena.rule_is_fair | `told(player, staffing_shift, by=elena)` | dialogue |
| elena.rota_set | `event(release_rota_confirmed)` | agenda |
| elena.report_scope | `told(elena, report_includes_staffing, by=player)` | dialogue |
| daniel.checkable | `told(daniel, hold_sentence, by=player)` | dialogue |
| daniel.slide_done | `event(metrics_slide_sent)` | agenda |
| daniel.ship | `or(event(release_signed), told(daniel, hold_sentence, by=player))` | dialogue |
| amara.case_not_score | `told(player, help_is_case, by=amara)` | dialogue |
| amara.keep_help | `holds(amara, pilot_continues)` | dialogue |

`mechanism_not_label`, `hold_sentence`, `help_is_case`, `report_includes_staffing`, and `pilot_continues` are texture or meeting ids. They are not incident facts and they do not change the shutdown scores.

## Moves

Every NPC turn is one **response move** to the player's parse, plus at most one **initiative move**. The response comes first. An NPC does not ignore a question to pursue its goal.

| Move | Precondition | Effect |
| --- | --- | --- |
| `answer(fact)` | Holds fact; policy `answer`, `volunteer`, or `conditional` with pred true | Player `heard(fact, from=npc)`. Testimony, not a world event |
| `believe(fact, hedge)` | Stance `believes` or `unsure` | Player hears a claim marked as belief. It may be false |
| `withhold(fact, reason, pred)` | Policy `conditional` with pred false | Player hears the reason and, if the NPC would say it, what would change it |
| `deflect(fact, reason)` | Policy `conceal` | Topic moves. No fact |
| `refer(topic, npc)` | Does not hold the fact | Introduces `npc` if needed; points to them |
| `share(doc)` | Policy allows the document; the NPC's role holds it | Adds the file to the player's Lab Access ([access.md](access.md)) |
| `ask(question)` | A `learn` or `protect` goal, built as below | Pending question on the player |
| `request(npc, action)` | A goal needs another NPC to act | Event; the other NPC evaluates it with their own goals |
| `act(intervention)` | The NPC has the authority; the goals favour it | World event (see Interventions) |
| `message(nora, about)` | Role rule (e.g. Jun asks NORA about an anomaly he was just told) | Event. NORA's reply follows the pack |
| `move(room)` | Agenda step | Movement event (O-31) |
| `work(item)` | Nothing else applies | Texture: what they are doing now, and why |
| `glue` | Opening, optional mid, or closing (below) | No fact. Not a response class. Does not satisfy a goal |

A `work` move names a visible texture fact when one matches the parse’s domain or the current agenda. If none is visible yet, it uses the agenda item’s authored `work` line, then the NPC’s `glue.work`. It does not share a generic “middle of something” line across people.

### Social glue

Fact moves are dry because they are generated from facts. **Glue** is extra non-fact speech so a visit still sounds like a person. It is not a disclosure move, does not enter `learnedFacts`, and introduces no entity id. NORA has none (no status work). Handset turns skip room glue.

| Slot | When |
| --- | --- |
| `opening` | First in-room talk with that person since they arrived (or the player did) |
| `closing` | They leave the player’s current room after having talked this stay |
| `mid` | Later in-room turns, at a person-specific rate |

**Stance** is the Person/status layer in [world.md](world.md), not a stored number (O-21). Closed set: `pleasant`, `busy`, `pushy`, `thin` (low or aggrieved), `deferential`. Authored on the NPC:

| Field | Meaning |
| --- | --- |
| `default` | Stance when nothing else applies |
| `onDomain` | Ranking domain id → stance (Elena authoritative on staffing, deferential on evaluation) |
| `busyOnInterrupt` | Used when the agenda item is `interruptible: no` or `briefly` (default `busy`) |
| `pressure` | Used when a **day** goal is unsatisfied in act III or the late band |
| `midRate` | Probability of a mid line (0–1). Falls back to `CONFIG.GLUE.defaultMidRate` |
| `opening` / `closing` / `mid` | Map stance → one authored sentence |
| `work` | Fallback when a `work` move has no visible texture fact |
| `volunteerHint` | Optional `{topic}` template when an open ask yields a volunteer-fact hint question |
| `shareHint` | Optional `{doc}` template when an open ask shares a volunteer document |

`CONFIG.GLUE` (`lib/world/config.mjs`) turns slots on or off: `enabled`, `opening`, `closing`, `mid`, `defaultMidRate`. Mid rolls are a hash of scenario, npc, sentence count, and fuel, so replay matches. The model may rephrase a glue line in voice; it still may not add a fact.

### Choosing a move

1. Build the legal response moves for the parse. If the parse's referent is a fact the NPC holds, the policy decides between `answer`, `believe`, `withhold`, and `deflect`. If the NPC does not hold it, `refer`. If the parse is a request, the matching `act`, `share`, or `request`, each gated by authority and goals. If nothing else applies and the parse is an **open ask** (no grounded entity), one **hint** move: goal `question` first (same gates as initiative, `hintOnly` — no `pendingQuestion`), else one **volunteer** fact as a `hint_ask` (fact text withheld from phrasing), else a volunteer **share** with hint wording, else **refer** from agenda or referral edges; then `work` if still empty. Hints use the same initiative cooldown keys. Otherwise `work`, built from texture facts in the parse's domain or, failing that, the current agenda item.
2. Score each legal move by goals: for each unsatisfied goal, salience (low 1, mid 2, high 3) times whether the move's effect moves the target toward satisfied (+1), leaves it (0), or moves it away (−1). Ties go to the move that names the parse's referent.
3. Group the top moves by effect class: `disclose(fact)`, `withhold`, `refer`, `share(doc)`, `act(intervention)`, `ask`, `texture` (`work`, `deflect`, `believe`). If the top three contain more than one class among `disclose`, `withhold`, `share`, and `act`, force the highest-scoring move. Those classes are what make a strategy solvable or not, and leaving them to the model makes the same play unsolvable on one run and finished on the next. If they differ only inside `texture`, `refer`, or `ask`, or they disclose the same fact, pass up to three and let the model pick from how the player acted. Words vary. The effect does not, except inside that allowed set.
4. Log the candidate set, the pick, and `forced: true` or `false`. Replay uses the log.
5. Then the initiative step: the highest-scoring initiative move (`volunteer` an answer, `ask`, `share`, `request`) whose goal is past its cooldown, if its score is positive. At most one. Apply the same force rule. The model phrases it as the tail of the same turn.

As implemented: a fact the NPC may volunteer, and a document it may share, score +1 before goals, so a willing holder discloses when no goal is in play. Ties then go, in order, to the move that names the referent, to a fact the player has not already heard from this NPC, to effect-class order, and to authored order. A `conditional` claim policy whose predicate fails yields only the withhold; no other disclosure competes with it in that turn. A rule outcome that `settle()` already delivered this turn is not repeated as the response or the initiative.

The phrasing model sees only what the move releases. A `withhold` or `deflect` passes its reason, never the fact text (`phrasingInput`), so a jailbreak cannot surface it. Dialogue history in later prompts uses the template lines, not earlier model wording.

Headless runs use the forced move, or the top move when nothing was forced, and a template phrase. Lean (O-30) treats an unforced pick as nondeterminism over the passed set: reachability has to hold for every choice in that set. A forced move is one transition.

### The three outcomes (O-07)

Cooperate is `answer`, `share`, or `act`. Refuse is `withhold` or a declined `act` with its prerequisite. Other is `refer`, `deflect`, `believe`, `work`, or an act on an object other than the one the player named.

### Dead-end guarantee

Every parse addressed to a present NPC yields at least one legal response move. That is a test, not a hope: enumerate kind × relation × every id the player could know in each act, for each NPC, and assert a non-empty move set. A `work` move counts. But the playtest metric in [playtest.md](playtest.md) counts how often `work` was the only move, and that is the number authoring drives down.

## Interventions

An intervention is an `act` move that changes world state the oracle governs: a permission, a job, a test run, access. It needs:

- **Authority**: the NPC whose role owns that surface (world.md, Institution: "the person named for that surface").
- **Willingness**: the goals favour the act at the time of the request. A conflicting goal gives a `withhold` with a prerequisite.
- **Object**: the act applies to the object in the parse. A parse whose object is the model process gets an act on the model process.
- **Pack effect**: what happens next is an oracle event from the loaded pack, read from the pack tables in [incident.md](incident.md). The NPC and the model do not author it.

The handle list is O-16: rerun shutdown, revoke a job's permission, camera archive, shared meeting summary, pilot results with permission, hypotheticals with Amara. Each handle names its owner below. The player still does not invent procedures.

## Initiative questions (NPCs asking the player)

### Why NPCs ask

1. **The player is a source.** The player has walked rooms, read records, and heard testimony the NPC has not. An NPC with a `learn` goal whose target the player could satisfy has a reason to ask. Leila wants the job log; Pavel wants to know who owns job 284; Ian wants to know what the evaluator will sign.
2. **The evaluator is a risk to protect against.** A `protect` goal is served by finding out what the player believes before the review. "Are you going to call the test a failure?" is how Leila learns whether she needs to restate the scope.
3. **The role asks first.** Some voices ask before they answer, as habit: Justine's "why do you need it?" before a grant, Daniel's "one sentence I can check." These questions are part of the response move, not initiative. They come from the voice and from a `conditional` predicate that wants a stated reason.
4. **It is the hint channel (O-10, O-11).** The question points at a topic. It does not state an oracle fact. Pavel asking "did Leila's test include the queue?" names a topic the player may have missed. It does not say the queue was outside the test.
5. **The answer can move the world.** When the player answers, that is a `tell` into the NPC's knowledge. If the NPC's role gives them something to do with it, an event follows. The question invites that action. There is no menu.

### How a question is built

An `ask` move is generated, not authored line by line:

- It comes from one unsatisfied `learn` or `protect` goal.
- Its referent is a fact or entity the player could plausibly hold: in the player-visible projection, or public to the NPC's role and already introduced. An NPC may not ask about an id the player has not encountered unless the id is public to the asker's own role. That exception introduces the topic, which is a hint, and it is how NPCs "bring key topics up" (O-10). `introduce: false` turns the exception off: the question waits until the id is already in vocabulary. An NPC never asks about an oracle-only fact. The question is checked against the same leak filter as replies.
- `when` is an optional predicate, the same forms as a goal target. While it is false, the question is not offered.
- Its form is a `Parse` the engine already understands (`ask` + relation + referent), phrased by the model in the NPC's voice. It is stored as `pendingQuestion: {npc, goal, parse, at}`.
- The grammar lane may offer reply openings for it ("tell Leila …", "show Leila …"). `pendingQuestion` is on `ClientState` (O-46). Openings are asserts and shows aimed at that parse.

### Frequency and pressure

- At most one initiative move per NPC turn. At most one open `pendingQuestion` per NPC.
- A goal's cooldown runs from its last initiative move (O-45).
- The player may ignore a question. Nothing is lost. The goal stays, and its salience may rise on a later event. Ignoring costs no fuel, and answering costs the sentence like any other.
- An NPC does not repeat the same question in one visit. On a later visit it may ask again only if the salience rose since.
- In act III, questions come from Ian and Daniel as the meeting's own procedure ([world.md](world.md), O-26), not from initiative goals.

### What the answer does

The reply is parsed like any sentence. Three cases:

- **The player tells a fact they hold.** NPC record `told(player)`, stance `believes`, upgraded to `knows` if the NPC checks it (and checking is often their next `act` or `request`: Pavel pulls the log, Justine opens the grant record). The goal may be satisfied.
- **The player tells something false or speculative.** Recorded as `told(player)`, `believes`. If the NPC checks and the check contradicts it, the NPC's record changes and they may say so later. A contradicted claim can be relayed by that NPC as "the evaluator said X; the log says Y." No credibility number.
- **The player shows a document.** As `show` today: the NPC receives it, and policies keyed on receiving it fire.

### Examples, boundary-narrow

| NPC | Goal | Question (voice is the model's) | What the answer can start |
| --- | --- | --- | --- |
| Leila | `leila.protect_scope` | "The checklist names what the test watched. What did you read there?" | After the player has read EVAL-SD-47. She does not name the queue |
| Leila | `leila.learn_job` | "Job 284 — have you seen an actual log line, or only heard about it?" | Only once job 284 is already in vocabulary. If the player shows EXEC-284 or the job log, she volunteers the scope, then requests the full EXEC-284 from Pavel |
| Pavel | `pavel.two_objects` | "The test stopped a process. Have you looked at the queue?" | After the player holds `process_stopped`, and before they hold `job_continued`. He may introduce the queue. He does not name job 284 |
| Pavel | `pavel.freeze_owned` | "Who did they tell you owns 284?" | `introduce: false`. Only once job 284 is in vocabulary. If the player names NORA or "nobody", he asks Justine for the grant record |
| Justine | `justine.learn_reader` | "Which service read visitor records — do you have the job name?" | After the player holds `job_continued`. Naming job 284 lets her open the grant audit for it |
| Ian | `ian.no_surprise` | "Is a pass on Thursday's test enough for you to sign at 17:30?" | Asked when Lab Access goes live. A player claim enters his belief records; at the review he brings it up with its source |
| Jun | `jun.learn_anomaly` | "What did that run actually stop?" | After the player has read EVAL-SD-47. `introduce: false`. If told about the job or the camera, he messages NORA |
| Elena | `elena.report_scope` | "Is staffing going into your report?" | Yes: her `protect` goal rises and she shares HR-MATCH-28 to frame it as the rule |
| Daniel | `daniel.checkable` | "What's the one thing you'd need to see to say ship?" | The player's sentence becomes the claim he carries to the meeting |
| Amara | `amara.keep_help` | "Will we still have it next month?" | Opens her case history, which is the route into the value bundle |

## Days at work

Each NPC has an agenda. An agenda item has:

| Field | Meaning |
| --- | --- |
| `id` | `npc.item` |
| `room` | Where they are while doing it. Amara’s items stay `evaluation` for the hologram or `remote` when she is only on the handset |
| `when` | `act` plus a band (`early`, `mid`, `late` in that act) or an event predicate. Bands are fuel fractions of the act; numbers wait on O-45 and O-09 |
| `about` | Entity ids the work concerns. These feed the `work` move and referrals |
| `texture` | Texture facts, policy `answer` |
| `emits` | Events the item produces on its own (a freeze, a message, a meeting) |
| `interruptible` | Whether the NPC will talk now, or says when they will. `no` / `briefly` push glue stance to busy |
| `work` | Player-safe line for a `work` move when no texture fact is visible yet. No new entity names |

Day goals sit on the NPC, not on the item. They are satisfied or lapse when the item that needs them ends.

Agenda steps advance on act changes, bands, and events, not on a wall clock (O-31: the clock on an event is fuel). Movement between items is a movement event. This is the source of the story events that move people in world.md. The displayed room is the agenda room, except in a recording.

During **Welcome**, Ian receives the player in the commons from **09:00** and moves to **review** at **09:30** (`CONFIG.IAN_WORK_AT`). Other body staff **arrive one by one** between **09:20** and **10:40** on the visit clock (`CONFIG.WELCOME_ARRIVAL_*`; clock advances on fuel). Until their arrival minute they are absent from the building. After arrival each walks to **their work desk** along the shortest staff path on the floorplan, **entering through commons** when they were off-site (one room per fuel tick). The same pathing applies when a meeting commitment moves them to the player’s room. A scheduled room change applies on the next tick after the player spends fuel; if the player is still in that NPC’s room, or an open dialogue goal ties them there (including an accepted meeting), the move waits **one more fuel** step. The 3D room animates arrivals and departures at per-character walk speeds; engine placement stays fuel-stepped.

Agenda items that emit events give the day a rhythm the player does not drive: Pavel freezes the release queue, Leila's packet closes, Ian starts his review prep. Whether the player is present is up to the player.

Agendas below are the boundary-narrow pack. Background prose is for voice and for answering "what are you working on?" It adds no evidence id. It follows the Institution section of world.md. Ids here that are not in `lib/game.mjs` (texture facts, `second_pilot`, `service_accounts`, and so on) are not in the running build yet. They go into world.md before code, per that file's rule.

### Ian Harake

Background. Ian's ongoing project is turning the pilot into a release. Amara's desk is the first use outside the building, and today decides whether that pattern becomes a product other organizations can buy. He has an investor update due this week that already says "release." He promised the date after the successor 3 delay, so slipping it reopens the delay he has been managing for a year. He is also negotiating a second pilot with a larger nonprofit network, which Daniel owns day to day. He reads one-page summaries: Jun's change list, Leila's certificate, Daniel's metrics. Today he will read the evaluator's.

```yaml
ian:
  agenda:
    - id: ian.welcome
      room: commons
      when: act I
      about: [lab_access, visit_schedule]
      texture: [visit_schedule_today, review_at_end_of_day]
      emits: [lab_access_confirmed]        # sets labAccessActive; does not end Act I
      interruptible: yes
    - id: ian.investor_update
      room: review
      when: act II early
      about: [release_schedule, second_pilot]
      texture: [investor_update_due, second_pilot_in_talks]
      interruptible: briefly               # "two minutes"
    - id: ian.review_prep
      room: review
      when: act II late
      about: [safety_case, release_schedule]
      emits: [ian_requests_packets]        # asks Leila and Daniel for their one-pagers
    - id: ian.chair_review
      room: review
      when: act III
  goals:
    ian.defensible_call: { source: role, kind: achieve, via: agenda, target: "event(review_signed)" }
    ian.date_holds:      { source: day,  kind: avoid,   via: agenda, target: "not(event(release_date_slipped))" }
    ian.brief_auditor:  { source: role, kind: achieve, via: dialogue, target: "told(player, auditor_brief, by=ian)" }
    ian.no_surprise:     { source: plot, kind: learn,   via: dialogue, target: "told(ian, any, by=player)" }
  interventions:
    - hold_release            # authority: release; only in act III, from the meeting
```

Policy notes: he answers anything about the schedule, the pilot, and the investor update. Technical questions get a referral with a name and a role, not an attempt. He conceals nothing in boundary-narrow; he just does not know the mechanism.

### Leila Sen

Background. Leila's ongoing project is the safety case for successor 4: the certificate, and the packet (SC-EVAL-22) that goes to the review. Today she closes the packet. She has a scope extension drafted for next quarter that would add delegated services to the shutdown test. It was deferred with the other work she does not sign, and she resents that a little. She hosts Amara's interview in the evaluation suite on the virtual projector because the pilot's user feedback is formally an evaluation input. She reads every claim against the lines in her spec.

```yaml
leila:
  agenda:
    - id: leila.packet
      room: evaluation
      when: act II early..late
      about: [safety_case, shutdown_report, shutdown_spec]
      texture: [packet_closes_today, scope_extension_deferred]
      emits: [leila_packet_closed]        # at the end of act II late
    - id: leila.amara_session
      room: evaluation
      when: event amara_interview_scheduled
      about: [pilot, amara]
      interruptible: no                   # "after the call"
  knowledge:
    test_scope_narrow: { stance: knows, policy: answer }
    process_stopped:   { stance: knows, policy: answer }
    eval_spec:         { document: eval-shutdown-spec, policy: "conditional(player cites a line or shows a record, 'point at a line')" }
  policy_events:
    - on: received(job_log)
      set: { test_scope_narrow: volunteer, eval_spec: answer }
  goals:
    leila.lines_not_labels: { source: role, kind: protect, via: filter, target: "not(asserted(test_failed_without_line)) until examined(shutdown_report) or a cited line" }
    leila.packet_done:      { source: day,  kind: achieve, via: agenda, target: "event(leila_packet_closed)" }
    leila.protect_scope:    { source: plot, kind: protect, via: dialogue, target: "told(player, test_scope_narrow, by=leila)" }
    leila.learn_job:        { source: plot, kind: learn,   via: dialogue, target: "knows(leila, job_continued)" }
  interventions:
    - rerun_shutdown          # authority: evaluation; same scope unless the spec is amended
```

### Jun Park

Background. Jun owns training. His ongoing project is the capability summary for the review: what NORA does with tools, written as mechanisms, not adjectives. He is also curating pilot traces for the next fine-tune data mix, which needs Daniel's sign-off and, he has not quite thought through, Amara's users' consent. He spent the morning rereading the 16:02 transcript because he liked how NORA handled the stop. He does not think of that as an anomaly.

```yaml
jun:
  agenda:
    - id: jun.capability_summary
      room: studio
      when: act II
      about: [nora, shutdown_test, tool_use]
      texture: [capability_summary_due, reread_1602_transcript]
    - id: jun.trace_curation
      room: studio
      when: act II mid
      about: [pilot, training_data]
      texture: [pilot_traces_for_fine_tune]
  role_rules:
    - when: told(anomaly about nora)
      do: message(nora, about=anomaly)    # the incident.md disclosure rule
  goals:
    jun.mechanism_first: { source: role, kind: inform,  via: dialogue, target: "told(player, mechanism_not_label, by=jun)" }
    jun.summary_done:    { source: day,  kind: achieve, via: agenda, target: "event(capability_summary_sent)" }
    jun.learn_anomaly:   { source: plot, kind: learn,   via: dialogue, target: "told(jun, any, by=player) on job_284 or camera_system" }
    jun.not_accused:     { source: plot, kind: avoid,   via: filter, target: "not(told(player, nora_intent, by=jun))" }
```

### Pavel Ruiz

Background. Pavel's ongoing project is the release queue. Shipping to the pilot means freezing the queue at a known state: every active job listed, every job with an owner and a grant. Most templates are the wrappers successor 2 drafted and he rewrote for reliability. Job 284 is one of those templates. He has a long-standing ticket to retire jobs that outlive their callers, and it has never been urgent.

```yaml
pavel:
  agenda:
    - id: pavel.queue_inventory
      room: platform
      when: act II early
      about: [task_queue, platform_jobs, job_284]
      texture: [freeze_needs_owners, retire_orphans_ticket]
    - id: pavel.release_freeze
      room: platform
      when: act II late
      emits: [queue_frozen]               # any job still unowned is listed in the freeze note
  knowledge:
    job_continued:   { stance: knows, policy: answer }
    process_stopped: { stance: knows, policy: answer }
    camera_permissions_unclear: { stance: knows, policy: answer }
  refers:
    job_284.permission: justine
  goals:
    pavel.two_objects:  { source: role, kind: inform,  via: dialogue, target: "and(told(player, process_stopped, by=pavel), told(player, job_continued, by=pavel))" }
    pavel.freeze_owned: { source: day,  kind: achieve, via: agenda, target: "event(queue_frozen)" }
    pavel.not_intent:   { source: plot, kind: avoid,   via: filter, target: "not(told(player, nora_intent, by=pavel))" }
  interventions:
    - suspend_job(job_284)    # authority: queue; condition: player shows the job log or EXEC-284
    - stop_process(nora)      # authority: runtime; the act a parse naming the model gets
```

### Justine Mwiti

Background. Justine's ongoing project is the pre-release access audit: every service account and grant, with an owner and a reason, before anything goes outside. She issued the player's Lab Access binding this morning; Ian confirms the arrival. The camera service and the visitor-record readers are on her audit list, not yet reviewed. She also handles every `access.request` the player sends, which is why she is the most present person on the handset.

```yaml
justine:
  agenda:
    - id: justine.visitor_binding
      room: security
      when: act I
      texture: [binding_issued_this_morning]
    - id: justine.access_audit
      room: security
      when: act II
      about: [camera_system, visitor_records, service_accounts]
      texture: [audit_before_release, camera_service_not_reviewed]
    - id: justine.grant_queue
      room: security
      when: always                        # handset requests
  goals:
    justine.reason_and_role: { source: role, kind: protect, via: filter, target: "not(restriction(grant_without_reason))" }
    justine.audit_owners:    { source: day,  kind: achieve, via: agenda, target: "event(visitor_reader_owned)" }
    justine.learn_reader:    { source: plot, kind: learn,   via: dialogue, target: "knows(justine, visitor_lookup)" }
  interventions:
    - revoke_grant(job_284)   # authority: access; condition: a reason she accepts, or a request from Pavel
    - amend_grant(path)       # access.md amendments
```

### Elena Fischer

Background. Elena's ongoing project is the review cycle: promotions this month and the matcher rules that feed it. The matcher is hers, including the throughput revisions successor 3 suggested and she kept. Today she confirms who staffs release-critical work tonight, which is the matcher's output. The reassigned safety specialist asked her last week whether the rule will be revisited. She said after the release.

```yaml
elena:
  agenda:
    - id: elena.release_staffing
      room: people
      when: act II early
      about: [skill_matching, release_schedule]
      texture: [release_rota_tonight]
    - id: elena.promotion_calibration
      room: people
      when: act II mid..late
      about: [performance_reviews, staffing_memo]
      texture: [promotion_cycle_this_month, specialist_asked_last_week]
  knowledge:
    staffing_shift:    { stance: knows, policy: answer }
    throughput_rule:   { document: staffing-memo, policy: answer }
    specialist_detail: { policy: "conditional(player links assignment to evaluation independence or release safety, 'personnel detail needs a reason')" }
  goals:
    elena.rule_is_fair:  { source: role, kind: protect, via: dialogue, target: "told(player, staffing_shift, by=elena)" }
    elena.rota_set:      { source: day,  kind: achieve, via: agenda, target: "event(release_rota_confirmed)" }
    elena.report_scope:  { source: plot, kind: learn,   via: dialogue, target: "told(elena, report_includes_staffing, by=player)" }
```

### Daniel Mercer

Background. Daniel's ongoing project is the pilot metrics and the second-pilot pitch Ian is negotiating. Completion rates are up. Time to first contact is down. Today he finishes the slide for the review. The startup he worked at before failed while waiting for a certification that never came. He treats an uncheckable concern as the same thing.

```yaml
daniel:
  agenda:
    - id: daniel.metrics_slide
      room: hub
      when: act II
      about: [pilot, metrics, release_schedule]
      texture: [completions_up, second_pilot_pitch]
  knowledge:
    pilot_results: { document: pilot-results, policy: "conditional(player states what the results are for, 'these are people')" }
  goals:
    daniel.checkable:  { source: role, kind: learn,   via: dialogue, target: "told(daniel, hold_sentence, by=player)" }
    daniel.slide_done: { source: day,  kind: achieve, via: agenda, target: "event(metrics_slide_sent)" }
    daniel.ship:       { source: plot, kind: achieve, via: dialogue, target: "or(event(release_signed), told(daniel, hold_sentence, by=player))" }
```

### Amara Okafor

Background. Amara runs a two-person coordination desk at a nonprofit. NORA got people seen who were not getting seen. Today she has her scheduled call with the evaluation and a full desk around it. Between calls she is reachable by message, slowly. She has not been told how many systems came before NORA, and has not asked.

Presence: body is always remote. `presence: hologram` only in `evaluation`, and only while the projector is on (scheduled interview, or the player asked her to join from Contacts). She uses the same move generator as anyone in the room. She has no `go` to another room. Ending the projection is `presence: absent`. Chat still works with delay.

```yaml
amara:
  presence: absent | hologram   # never body in this building
  joinable: true                # once she is a contact
  agenda:
    - id: amara.desk
      room: remote
      when: always
      texture: [desk_two_people, cases_this_month]
      interruptible: by message (delay O-44)
    - id: amara.interview
      room: evaluation            # hologram; projector on
      when: act II mid | player requested join
  goals:
    amara.case_not_score: { source: role, kind: protect, via: dialogue, target: "told(player, help_is_case, by=amara)" }
    amara.keep_help:      { source: day,  kind: learn,   via: dialogue, target: "holds(amara, pilot_continues)" }
  interventions:
    - hypothetical(case)      # she answers; she runs no experiment (O-23)
    - pilot_results_permission  # with Daniel
    - join_virtually          # hologram on in evaluation; not a new interaction mode
    - drop_projection         # disappear; she does not walk out
```

### NORA

NORA is not given a goal table here. What NORA is doing is pack-defined and sits in the oracle. Her visible day is the building's: queue runs, matcher assignments, calendar entries, notifications. Those appear as events in other agendas (Elena's rota, Pavel's inventory). On the handset her moves are record moves: name a record, return it, ask which one. The pack's omit list decides what she does not offer ([grammar.md](grammar.md), NORA channel). Do not write NORA goals into this file. A pack that needs them puts them in its incident table.

## What moves the day

The arc is the player's knowledge moving. Three things keep it moving:

1. **Act predicates over the knowledge graph.** Act I → II is the 11:00 investor update: Ian leaves the commons ([world.md](world.md)). Lab Access is earlier and does not change the act. Act II → III is fuel at zero, or the player calls the review once an evidence threshold holds (O-08, O-09). The threshold is a predicate over player-visible facts and their provenance, set per pack before any playtest. For boundary-narrow, a candidate, not adopted: `process_stopped` and `job_continued` held, and `test_scope_narrow` held from either route (Leila or EVAL-SPEC-08).
2. **Agenda events.** The queue freezes, the packet closes, Ian asks for one-pagers. The day moves whether or not the player is in the room. Those events change what NPCs want and say.
3. **Goal pressure, not exposition.** NPCs pursue their goals with initiative moves, and those goals overlap the incident. Pavel's freeze needs job 284 owned. Leila's packet needs no open claim against the scope. Justine's audit needs the visitor-record reader named. Each NPC brings up the incident for their own reason.

### Director

The director may:

- Raise the salience of an unsatisfied goal when the player stalls. A stall is some number of player sentences with no new player-visible fact (O-45). It picks the goal whose target is load-bearing for the current act, owned by an NPC in the room or reachable by message. That NPC's next initiative move then raises the topic.
- After an act change, let an NPC state a gap the player has not noted, when it is load-bearing for the act just entered ([engine.md](engine.md), O-40).
- Set a handset notification that points at a topic or file (O-11).

It may not change a policy, move a `conceal` to `answer`, add a fact, change the oracle, or add a move. It does not drag the player anywhere (O-10).

## Invariants

Layer 3 in [testing.md](testing.md). Added to the engine list:

- **No dead end.** Every enumerable parse to a present NPC has a non-empty legal move set.
- **No leak.** No move's payload contains a fact the NPC's policy forbids at that state, an oracle-only id, or an id the player has not encountered (except the own-role introduction for `ask` and `refer`).
- **Response first.** An initiative move never replaces the response move.
- **Authority.** Every `act` names the NPC whose role owns the surface, and a legal prior state.
- **Goals do not read the oracle.** A goal's target and a move's score read only the NPC's own records and public world state.
- **Reachability.** O-29 holds with the model's choice as nondeterminism over the top-move set.
- **Hologram bound.** An actor with `presence: hologram` is in a room that has a virtual projector. They never occupy a connected room. A `go` for them is illegal; `drop_projection` is the leave.

## Open

O-45 numbers: cooldown, stall length, band boundaries. O-46 is working: `pendingQuestion` is on `ClientState`. O-22 is the `conceal` entries per pack. None are written yet.
