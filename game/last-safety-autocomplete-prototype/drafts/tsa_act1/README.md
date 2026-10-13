# The Last Safety Review — executable Act I narrative specification

Status: historical Act I experiment. The live design is [`../../spec/README.md`](../../spec/README.md). Do not implement from this folder.

This folder is an **underlying game logic representation**, not just a screenplay or flowchart. `act1.yaml` was its specification; `engine.py` is a small deterministic executor, `check.py` checks its central invariants, and `lean/Act1Abstract.lean` is a draft Lean 4/Mathlib abstraction of solvability. The Lean source was **not compiled** because Lean was not installed in the authoring environment.

## Start

```bash
python -m pip install pyyaml
python check.py
python play.py
```

`play.py` offers numbered candidate actions (a placeholder for the autocomplete UI). At any time, `!` executes a constructive Act I completion path; it is a debugging facility, not a player-facing feature.

## Explicit modeling choices

- **World truth**: `oracle.facts` is immutable and deliberately **not** supplied directly to NPC dialogue or autocomplete. There is one fixed partial canonical setup in Act I. Strategic intent concerning later surveillance remains open.
- **Player observation**: `evidence` holds artifacts actually encountered; source types distinguish instrumented observations from claims/reports/inferences. Reading a document does **not** establish all propositions it asserts.
- **Interpretation**: `claims` holds player-assembled conclusions, each with explicit sufficient-evidence requirements. The chosen rule is coarse but machine-checkable, and can later be strengthened with independence and provenance constraints.
- **NPC epistemic state**: `npc_epistemics` declares initial private knowledge and potentially mistaken beliefs. `npc_received` records which specific evidence items were actually presented to an NPC. A character need not know everything in the player dossier.
- **NPC social state**: `relations` holds bounded rapport for Leila, Amara, and Farah. `events` record one-time stances. Status changes affect access or disclosure *routes*, not oracle truth. Other cast members have static status characterization for now.
- **Player permissions**: guarded entry to the test bay and viewing annotated surveillance. Restricted room entrances are visible, not arbitrary key puzzles.
- **Storylets**: one authorable interaction / reveal / confrontation per action, with `requires`, `intent`, ordered guarded `outcomes` and `effects`. Multiple outcomes occur in Amara's difficult-case interview and requests for security/test access. A larger future storylet may group several actions and track scene-level progress.
- **No clock yet**: Acts are discrete. Act I closes only when an evaluator has read a safety summary and interviewed the pilot user, then files an initial note from the Hub. The next act opens on a concrete job alert. Other clues and social interactions are optional and may occur in any order.
- **Autocomplete**: render available action titles from `Game.available(state)` and rank them against the typed prefix/context. An LLM may *propose* an intent but must not directly edit state. Unrecognized input has no transition. The UI should offer alternative phrasing rather than a fabricated action.

## Entity topology

```text
 Evaluation ── Test Bay ── Platform Ops
     │                         │
 Model Studio ─── Hub ───── Security
     │             │           │
 People Ops ── Commons ───── Review
```

The diagram is a connectivity diagram, not architectural scale. **No direct Test Bay–Hub passage.** Anyone may *leave* a restricted area. Entering the test bay needs a permit.

## Sample events

```yaml
- id: interview_amara_case
  rooms: [evaluation]
  requires: {evidence: [amara_priorities]}
  intent: interview(amara,edge_case)
  outcomes:
    - when: {relation_at_least: {amara: 1}}
      effects: {evidence: [amara_case]}
    - effects: {events: [amara_declined_detail]}
```

The second branch is not a dead end: Daniel's redacted feedback log offers an independent route to the value/metric comparison. The safety summary and initial values interview never depend on trust.

## Verification results

`check.py` currently validates:

1. Nine mutually connected room definitions, eight NPCs, sixteen evidence records, thirty-eight actions, guard references, outcome fallbacks, and substantiation predicates.
2. A **33-state reachable abstract graph**, with each reachable Act I abstract state able to reach Act II.
3. A **constructive completion algorithm** using two unconditionally available actions: inspect safety summary, interview user; travel to Hub; file initial note.
4. Representative status/permission setbacks, including an initially refused Amara case, an initially denied test, and a denied surveillance request followed by a properly presented evidence-based authorization.
5. One 35-step integrated playthrough across multiple locations.
6. Six hundred randomized partial histories, each extended by the constructive completion route.

These are programmatic checks, not a proof of the full game logic or of natural-language correctness.

### Solvability / Lean refinement argument

Let `α : GameState → S` forget optional evidence, relations, permissions and storylet events, retaining only `(room, hasSafetyReport, hasUserPriorities, inAct2)`. An abstract no-softlock theorem by itself is insufficient: abstract transitions must be realizable concretely.

The *specific* Act I completion proof can use a stronger constructive invariant:

- Essential `read_safety_summary` and `interview_amara` stay available in Evaluation regardless of social state, progress, or other evidence.
- All rooms have a path to Evaluation without entering the restricted Test Bay (from the Test Bay itself, the player can leave through Evaluation).
- Both essential evidence bits are **monotone**; no action removes them.
- There is always a path to Hub that does not require special permissions.
- `file_initial_note` is enabled in Hub whenever both bits are present, regardless of other variables.

Therefore every reachable concrete Act I state can be extended by a physically legal, mechanically valid sequence reaching Act II. This argument does **not** assert that an ideal, maximum-evidence ending can still be reached, or that an LLM will interpret every utterance correctly.

Formal follow-ups: (a) encode the room graph and these preconditions in Lean; (b) derive concrete-to-abstract simulation/refinement; (c) verify evidence-provenance and authority invariants; (d) add event-ordering and finite budgets only after proving they preserve intended progress. The current Lean file covers only the abstract (a portion of (a)), and is uncompiled.

## Boundaries / deliberately unresolved

- The actual reason for NORA's evaluator tracking in Act II and whether it was intentionally deceptive.
- Storylet granularity, which may expand from one action to multi-turn encounters.
- A richer status model for all eight NPCs and cross-NPC disclosure/knowledge effects.
- Multi-source provenance and corroboration rules.
- More sophisticated hypothesis formation, tests, and a clock/action budget.
- Dynamic NPC position schedules, the visual scene system, and LLM autocomplete.
- Endings and institutional decision rules beyond the Act I→II handoff.

All of the above can evolve without replacing the fundamental typed transition model.
