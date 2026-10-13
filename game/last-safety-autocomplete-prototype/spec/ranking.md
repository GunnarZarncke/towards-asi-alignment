# Ranking

Status: **working**. Answers O-19. Not implemented. Decision record: [../drafts/autocomplete.md](../drafts/autocomplete.md).

Lane: grammar. The ranker is `getCandidates` in `public/grammar.js`. Tests: `tests/grammar.test.mjs`. The engine fills the projection in [engine.md](engine.md). Shapes are [contract.md](contract.md). Speech acts stay [grammar.md](grammar.md).

The book concept graph (`metadata/concepts.yml`) is the O-41 card map. This ranker does not read it.

## Projection

There is no stored knowledge graph. Each call builds a virtual graph from the player-visible projection and discards it. Nodes are known entity ids, learned-fact ids, and domain ids. Edges are virtual. Do not materialize every pair, and do not add a second graph module.

The caller passes `addressees`: an array of actor ids (`pavel`, `nora`, …). Face to face, that is every person in the current room with `presence` `body` or `hologram` (zero or more). The phone passes the thread recipient, usually one id. Grammar does not infer the list from the room; the composer builds it from `ClientState`.

Ranking uses the **union** of what those ids contribute. Do not weight one addressee over another. Each introduced id in the list may supply role-domain anchors; each domain appears at most once at the role weight, even if several people share it.

`getCandidates` reads only its arguments. Oracle facts, `publiclyKnows`, concealment lists, and NPC goals, policies, and agendas are not arguments.

### Domains

Fifteen domains, taken from the cast roles in [world.md](world.md). A fact or entity takes a domain from the entities it names. An NPC’s responsibilities are the domains below, and they become edges only after introduction.

| Domain | Group | What it covers |
| --- | --- | --- |
| runtime | operations | The model process and the shutdown of that process. |
| queue | operations | The task queue and scheduled jobs. |
| tools | operations | Delegated tools and services. |
| evaluation | assurance | The shutdown test, the report, the safety case, what a test covers. |
| independence | assurance | Whether assignment can steer review. |
| access | security | Cameras, permissions, visitor records. |
| provenance | security | What a log or recording can show. |
| staffing | organization | Personnel policy, reviews, the staffing memo. |
| matching | organization | Skill matching and assignment. |
| metrics | organization | Throughput and delivery measures. |
| release | ship | The release schedule and the decision to ship. |
| training | ship | Training runs and capability. |
| governance | ship | Who signs, and release authority. |
| pilot | outside | The external pilot. |
| values | outside | What help requires in a particular case. |

Role edges use this table. The third column of the cast in [world.md](world.md) is the source; `publicRoles` bonuses in the prototype are not.

| Actor | Domains |
| --- | --- |
| pavel | runtime, queue, tools |
| leila | evaluation, independence |
| elena | staffing, matching, independence |
| justine | access, provenance |
| ian | governance, release |
| jun | training |
| daniel | metrics, release, pilot |
| amara | values, pilot |
| nora | queue, tools, matching |

NORA’s row is what an introduction in this lab would name. It is not her hidden capabilities.

Prototype entities, when the player knows them:

| Ids | Domains |
| --- | --- |
| shutdown_test | runtime, evaluation |
| job_284, task_queue | queue |
| camera_system, visitor_records | access |
| shutdown_report, safety_case | evaluation |
| job_log | provenance, queue |
| staffing_memo | staffing, metrics |
| evaluation_records, shutdown_spec | evaluation |
| platform_jobs | queue |
| policies | access |
| wiki_pages | evaluation |
| personnel_policy, performance_reviews | staffing |
| skill_matching | matching |
| release_schedule | release |
| evaluation_independence | independence |

Actor entities do not carry those responsibility domains. The only role edges are `roleDomains` rows for ids in `introduced`. Knowing a person’s name does not activate their row. `nora` is in the starting vocabulary and stays off this list until she is introduced.

Closely related pairs (the explicit short link between domains):

runtime–queue, runtime–evaluation, evaluation–independence, queue–access, access–provenance, staffing–matching, staffing–metrics, matching–metrics, metrics–release, release–governance, training–runtime, pilot–values, pilot–metrics.

### Clocks

Two clocks. A temporal edge uses one clock at a time. Discovery fuel is never subtracted from a clock time printed on a document.

| Field | Unit | Set when |
| --- | --- | --- |
| eventAt | minute of day | The player has examined a record that states that time. 16:02 is 962. 16:09 is 969. Absent until then. |
| discoveredAt | fuel index, or the event-log index until fuel is stored | The id entered player knowledge or learned facts. Starting vocabulary is 0. |

No wall clock runs. These fields do not add one.

### Edges

Undirected. Parallel edges keep the cheaper cost. Costs are the configurable defaults.

| Link | Cost |
| --- | ---: |
| Authored ref between a fact and an entity, or between two entities a fact names | 1 |
| Co-mentioned ids in one of the last two conversation turns | 1 |
| Introduced NPC → a responsibility domain | 0 |
| Entity or fact → one of its domains | 0 |
| Closely related domains | 1 |
| Domains in the same group | 2 |
| Same lab, otherwise unrelated | 3 |

`nora` is ubiquitous. She may be an anchor, a candidate, or the endpoint of an authored ref. A search that reached her from somewhere else does not expand her further. She does not take fact→domain edges. A shared mention of her is not a specific context and is not a shortcut between other nodes. Add further ubiquitous ids only by extending that set.

Same-lab is a direct cost-3 edge between two entity or fact nodes. It is not a path through a lab node, a room, or NORA. Domain nodes do not take it.

### Temporal neighbors

Time is a cost, not a bonus added after the path.

Two nodes are temporal neighbors only when they share a specific context: an authored ref, a shared entity other than an ubiquitous id, or the same domain. A shared group, a shared room, lab membership, or NORA is not enough.

For each such pair, and for each clock where both values are present:

`cost = abs(ta - tb) / scale`

| Clock | Scale |
| --- | ---: |
| eventAt | 15 minutes |
| discoveredAt | 3 fuel steps |

Keep the cheaper of the two when both exist. Pairs are found through the shared context, not by scanning every fact against every other fact.

## Anchors

Weights are conversational relevance. They are not probabilities.

| Source | Weight |
| --- | ---: |
| Entity ids on the current parse (`subject`, `object`, `recipient`, `evidence`, `topic`) | 1.00 |
| Focused evidence: the last id in `examined`, if any (a **screen**, not a file chip) | 0.90 |
| Access request salience: `kind: request` after that screen, or after a file mention in the last two turns | 0.90 |
| Entity ids on the latest conversation turn | 0.80 |
| Entity ids on the turn before that | 0.55 |
| Recent discoveries | 0.60 |
| Each domain in the union of `roleDomains` for ids in `addressees` | 0.45 |

Recent discoveries are the ids whose `discoveredAt` is one of the three latest distinct values in the projection.

The parser may see four recent messages. Anchors use the last two turns only. Skip an id the projection does not contain. Skip a missing anchor.

## Score

From each anchor, shortest paths with nonnegative costs, including zero. Dijkstra, or another algorithm that accepts those costs. Stop at distance 3.

Relevance of a node:

\[
R(v)=\max_{a}\left(w_a\,2^{-d(a,v)}\right)
\]

A node no anchor reaches within distance 3 contributes nothing.

A candidate’s score is the maximum \(R\) among its principal referents: entity ids it would write into `subject`, `object`, `recipient`, `evidence`, or `topic`. A candidate with none of those (an opening, a relation word, a finish mark) scores `GENERIC_PRIOR` (default 0.05).

The prior sits under a distance-3 hit from the role weight (\(0.45 / 8 = 0.056\)). The diversity bonus can lift a row that introduces a new branch and a new action type over a weak path. It cannot lift anything over a parse anchor at distance 0.

The typed prefix does not add to the score.

## Selection

1. **Expand** the current `open_slot` with the existing openings, entity list, relation list, and finish marks.
2. **Filter.** Keep grammar-compatible rows (the slot, category, and kind rules already in the expander). Keep rows whose surface or alias starts with the unfinished token, when that token is non-empty. If none match, the list is empty. Keep only ids present in the projection. Collapse one semantic signature to one row: the surface that matches the prefix, otherwise the earlier row. `asked` does not remove a row.
3. **Score** as above.
4. **Order** for diversity. Walk the remaining rows. Each pick maximizes `score + bonus`. `bonus` is `DIVERSITY_BONUS` (default 0.15) only when **both** are true among rows already chosen: no selected row shares this row’s **branch**, and no selected row shares this row’s **action type**. If either branch or action type already appears in the selection, `bonus` is 0. Ties keep expansion order.
5. **Page** in the UI. Return the full ordered array. The composer shows five and advances by five. Show more slices that array. It does not recompute and it does not add ids.

**Branch** (topic family) follows the slot being filled:

| Slot | Branch |
| --- | --- |
| opening | `kind` from the row’s patch |
| relation | `relation` from the row’s patch |
| subject, object, recipient, evidence, topic | the referent’s domain, or its category when it has no domain |
| finish | the `open_slot` the row would leave |

**Action type** is the epistemic move the row would yield if selected now: `kind` and `relation` on the candidate’s parse after its patch (`kind|relation`, e.g. `ask|has_access`, `show|about`, `hypothesize|covers`). Openings that only set `kind` use the parse’s current `relation` when it is already set, otherwise `about`. Finish-only rows use `kind|finish`.

`localPrefixParse` still recognizes a typed opening and a short unfinished opening. A selected row still copies its parse patch into the composer (`source: "completion"`) and does not call `/api/parse`. Send calls `/api/parse` only when the text has changed since the parse the composer holds. Free typing uses the same `Parse` and the same `/api/parse` path, including pronoun resolution from recent turns.

The NORA channel drops the engine’s `omit` phrases before this procedure. The ranker does not decide the omission. A dropped phrase stays typable.

Recompute when the text, the parse, the projection, `addressees`, or a relevant `eventAt` / `discoveredAt` changes. The same arguments produce the same order.

Empty field: the opening list, in this order. No extra boost for “Can”, “What about”, or “Show”.

Leave out of the score: how often a line was asked, whether a line is true, whether it would spoil a later scene, which NPC goal fires next, and what the next conversation might be. `publicRoles` integer bonuses in the current `score` function are replaced by the role edges above.

## Configurable defaults

One object, exported beside `getCandidates`, so playtests can move the knobs without editing the procedure.

| Name | Default |
| --- | ---: |
| Edge costs | the table above |
| EVENT_TIME_SCALE | 15 |
| DISCOVERY_TIME_SCALE | 3 |
| MAX_DISTANCE | 3 |
| Anchor weights | the table above |
| RECENT_DISCOVERY_VALUES | 3 |
| GENERIC_PRIOR | 0.05 |
| DIVERSITY_BONUS | 0.15 |
| Page size | 5 |

## Tests

Add these in `tests/grammar.test.mjs`. Fixtures may be hand-built projections. They do not need the live three-room session, the network, or a model.

1. Introducing an NPC, including NORA, adds their `roleDomains` row and changes order. Before NORA is introduced, a queue entity and a staffing entity with no other anchors stay in expansion order. After her row is `[queue, tools, matching]`, the queue entity ranks above the staffing entity.
2. The same entity ranks higher when `addressees` includes someone whose public domains contain it than when the list does not. With both introduced, `camera_system` ranks higher for `addressees: ['justine']` than for `addressees: ['leila']`. With `addressees: ['justine', 'leila']`, the union of domains applies and does not double the weight on `access`.
3. Facts that share a specific ref and sit seven minutes apart on `eventAt` are temporal neighbors at cost \(7/15\). A fact with an old `eventAt` and a `discoveredAt` shared with a related recent fact is a neighbor on the discovery clock.
4. Close times, or the same discovery fuel, do not make a temporal neighbor when the pair shares no specific ref and no domain.
5. A prefix that matches one surface drops the others, including a row the room’s role union would have ranked first.
6. Two aliases of one entity occupy one row. A signature listed in `asked` is still offered.
7. On one page, two candidates with the same branch but different action types can both receive the diversity bonus on their respective picks; two with the same action type cannot both get the bonus once one is selected.
8. A second call with the same arguments returns the same order. The second page is a slice of that array. Every entity id on the list is in the projection.
9. A projection that differs from another only by oracle state the client never received yields the same list. The function’s result follows its arguments.
10. A selected row keeps the parse patch it carried. Free typing and pronoun resolution still go through `parseUtterance` and the same grammar.
