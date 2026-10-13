# Coding Instructions: Contextual Autocomplete Ranking

Status: decision record for O-19. The normative spec is [../spec/ranking.md](../spec/ranking.md). Implement from that file.

Implement the following in the existing game. Reuse its semantic grammar, parser, completion generator, and player-state representation. The ranking graph is a projection of that state, built per call. Do not create a stored knowledge graph.

## 1. Extend the existing graph

Add domain associations, public NPC roles, and temporal metadata. Preserve existing nodes and relationships.

```typescript
// Illustrative extensions, not replacement schemas.

type GraphNodeExtensions = {
  domains?: DomainId[];
  eventAt?: GameTime;       // When the represented event occurred
  discoveredAt?: GameTime;  // When the player encountered this information
};

type PublicNPCProfile = {
  npcId: EntityId;
  introduced: boolean;
  responsibilities: DomainId[];
  labId: EntityId;
};
```

Define approximately 12–20 domains based on the actual project's existing concepts. Derive each NPC's responsibilities from their existing role description. Assign domains to facts through their referenced entities, activities, and existing relationships.

An NPC's profile becomes available when the NPC introduces themselves or another character introduces them. This includes NORA.

Add graph edges or equivalent virtual relationships:

| Relationship | Distance |
|---|---:|
| Existing explicit factual relationship | 1 |
| Evidence refers to an event/object | 1 |
| Explicit conversational association | 1 |
| NPC role → directly responsible domain | 0 |
| Fact → directly associated domain | 0 |
| Closely related domains | 1 |
| Shared broader category | 2 |
| Same lab, otherwise unrelated | 3 |

Generic lab connections must not create short paths through ubiquitous nodes such as NORA.

Use only information available from the player's perspective. Never derive autocomplete relevance from NPCs' actual private knowledge.

## 2. Add temporal graph distance

Treat time as an additional source of graph distance, not a separate ranking bonus.

Keep event time and discovery time distinct.

```typescript
const TIME_SCALE = 15; // In-game minutes; configurable

function temporalDistance(a, b, clock) {
  const ta = a[clock];
  const tb = b[clock];

  if (ta == null || tb == null) return Infinity;

  return abs(ta - tb) / TIME_SCALE;
}

function temporalNeighbors(node, graph) {
  return graph.findNodesSharingSpecificContext(node)
    .filter(other =>
      sharesSpecificSubjectProcessLocationOrTopic(node, other)
    )
    .flatMap(other => [
      edgeIfFinite(
        other,
        temporalDistance(node, other, "eventAt")
      ),
      edgeIfFinite(
        other,
        temporalDistance(node, other, "discoveredAt")
      )
    ]);
}
```

Do not connect facts merely because they occurred at similar times. Generic shared entities, lab membership, or NORA alone are insufficient context.

Temporal edges can be virtual and computed through indexed neighbors; avoid constructing all possible fact pairs.

## 3. Build the contextual neighborhood

Use the graph's existing player-visible projection, augmented by the additions above.

```typescript
function contextAnchors(parse, playerView, npc, dialogue) {
  return [
    ...refs(parse).map(ref => anchor(ref, 1.00)),

    ...refs(playerView.focusedEvidence)
      .map(ref => anchor(ref, 0.90)),

    ...refs(dialogue.at(-1))
      .map(ref => anchor(ref, 0.80)),

    ...refs(dialogue.at(-2))
      .map(ref => anchor(ref, 0.55)),

    ...refs(playerView.recentDiscoveries)
      .map(ref => anchor(ref, 0.60)),

    ...publicRoleDomains(npc, playerView)
      .map(ref => anchor(ref, 0.45))
  ];
}
```

`publicRoleDomains()` returns nothing until that NPC has been introduced. The weights describe conversational relevance, not probabilities of factual truth.

Calculate relevance using weighted shortest paths:

\[
R(v)=\max_{a\in A}\left(w_a2^{-d(a,v)}\right)
\]

```typescript
function spreadActivation(graph, anchors) {
  const relevance = new Map<NodeId, number>();

  for (const { node, weight } of anchors) {
    const distances = shortestPaths(graph, node, {
      maxDistance: 3,
      neighbors: [
        existingGraphNeighbors,
        domainNeighbors,
        publicRoleNeighbors,
        temporalNeighbors
      ]
    });

    for (const [v, distance] of distances) {
      const score = weight * 2 ** (-distance);

      relevance.set(
        v,
        max(relevance.get(v) ?? 0, score)
      );
    }
  }

  return relevance;
}
```

Use Dijkstra or another shortest-path implementation supporting nonnegative, noninteger edge costs.

For a candidate introducing several semantic references, use the maximum relevance of its principal references. A completion without a specific referent receives a small configurable default score.

## 4. Implement five-stage selection

Use the existing incremental parse. Selected completions contribute directly to that parse; they must not require another LLM interpretation.

```typescript
function getCompletions(
  parse,
  playerView,
  npc,
  dialogue
): CompletionPage {

  // 1. Expand the current grammar element.
  const candidates = grammar.expand(parse);

  // 2. Filter.
  const eligible = candidates
    .filter(c => grammar.compatible(parse, c))
    .filter(c => matchesTypedPrefix(c, parse))
    .filter(c => referencesPlayerAvailableVocabulary(c, playerView));

  // Remove duplicate aliases within this candidate batch.
  const unique = deduplicateBySemanticContribution(eligible);

  // 3. Contextual neighborhood relevance.
  const graph = augmentPlayerVisibleGraph(
    playerView.knowledgeGraph
  );

  const relevance = spreadActivation(
    graph,
    contextAnchors(parse, playerView, npc, dialogue)
  );

  const scored = unique.map(c => ({
    ...c,
    score: principalReferents(c).length
      ? max(principalReferents(c).map(
          ref => relevance.get(ref) ?? 0
        ))
      : GENERIC_COMPLETION_PRIOR,

    branch: grammar.semanticBranch(c, parse)
  }));

  // 4. Jointly select a relevance/diversity-balanced order.
  const ordered = diverseOrder(scored);

  // 5. Stable pagination.
  return {
    visible: ordered.slice(0, 5),
    remaining: ordered.slice(5)
  };
}
```

Diversity selection:

```typescript
const DIVERSITY_BONUS = 0.15;

function diverseOrder(candidates) {
  const remaining = [...candidates];
  const selected = [];

  while (remaining.length > 0) {
    const best = argmax(remaining, c => {
      const alreadyRepresented = selected.some(
        s => sameSemanticBranch(s, c)
      );

      return c.score +
        (alreadyRepresented ? 0 : DIVERSITY_BONUS);
    });

    selected.push(best);
    remove(remaining, best);
  }

  return selected;
}
```

The semantic branch depends on the active grammar slot: utterance type, topic family, predicate/relation, or object referent.

The current typed prefix is a filtering constraint, not a weighted relevance signal.

Do not implement history-based repetition penalties, special anti-spoiler rules, truth-based ranking, next-storylet weighting, or future-conversation lookahead.

## 5. Parser and UI integration

Retain the shared completion/interpretation grammar.

```typescript
function onInputChanged(text) {
  parse = incrementalParser.update(parse, text);

  if (!parse.usable) {
    parse = await smallLLM.parsePartial({
      text,
      existingParse: parse,
      grammar: compactSemanticGrammar,
      relevantVocabulary: playerVisibleVocabulary(),
      previousUtterances: dialogue.slice(-2)
    });
  }

  refreshCompletions(parse);
}

function onCompletionSelected(candidate) {
  text = replaceRange(
    text,
    candidate.replacementRange,
    candidate.surface
  );

  parse = grammar.apply(
    parse,
    candidate.semanticContribution
  );

  refreshCompletions(parse);
}
```

The previous two utterances support back-reference resolution (`it`, `that`, `the other one`). Preserve semantic references and player-typed spans in the incremental parse.

The first page displays up to five suggestions. *Show more* displays subsequent entries in the previously computed order. Recompute only when the prefix, parse, conversational context, player-visible state, NPC, or relevant in-game time changes.

Submitting a completed utterance finalizes its existing parse rather than parsing it again.

## 6. Required tests

Implement tests covering:

1. Introducing an NPC, including NORA, activates their public role/domain associations.
2. The same fact ranks differently when talking to NPCs with different publicly known responsibilities.
3. Recent related events become closer through event time; recently discovered old evidence remains contextually relevant through discovery time.
4. Temporal proximity alone does not connect unrelated facts.
5. A more specific player prefix overrides broad NPC-role relevance.
6. Semantic aliases occupy only one candidate slot; previously asked questions remain eligible.
7. Show more preserves ordering and exposes no additional vocabulary outside the player's visible graph.
8. Changing hidden oracle state without changing player-visible state leaves autocomplete unchanged.
9. Selected completions preserve their semantic interpretation; free typing and back-references use the same grammar.

Keep graph-edge costs, temporal scale, anchor weights, generic-completion prior, and diversity bonus configurable for subsequent playtesting.