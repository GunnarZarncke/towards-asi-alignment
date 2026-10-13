"""Small deterministic game core. No LLM is allowed to mutate GameState directly."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).parent
RELATION_KEYS = ("leila", "amara", "farah")

class InvalidAction(ValueError):
    pass


@dataclass(frozen=True)
class GameState:
    act: int
    room: str
    evidence: frozenset[str]
    claims: frozenset[str]
    permissions: frozenset[str]
    events: frozenset[str]
    relations: tuple[int, int, int]
    npc_received: frozenset[tuple[str, str]] = frozenset()

    def relation(self, actor: str) -> int:
        return self.relations[RELATION_KEYS.index(actor)] if actor in RELATION_KEYS else 0


@dataclass(frozen=True)
class Result:
    state: GameState
    text: str
    action_id: str
    outcome_index: int


class Game:
    def __init__(self, path: Path = ROOT / "act1.yaml") -> None:
        self.spec: dict[str, Any] = yaml.safe_load(path.read_text())
        self.actions = {a["id"]: a for a in self.spec["actions"]}
        self.rooms = self.spec["rooms"]

    def initial(self) -> GameState:
        s = self.spec["starting_state"]
        return GameState(
            act=s["act"], room=s["room"],
            evidence=frozenset(s["evidence"]),
            claims=frozenset(s["established_claims"]),
            permissions=frozenset(s["permissions"]),
            events=frozenset(s["events"]),
            relations=tuple(s["relations"][k] for k in RELATION_KEYS),
            npc_received=frozenset(),
        )

    @staticmethod
    def guard(state: GameState, rule: dict[str, Any] | None) -> bool:
        g = rule or {}
        return (
            all(x in state.evidence for x in g.get("evidence", []))
            and (not g.get("any_evidence") or any(x in state.evidence for x in g["any_evidence"]))
            and all(x not in state.evidence for x in g.get("not_evidence", []))
            and all(x in state.permissions for x in g.get("permissions", []))
            and all(x not in state.permissions for x in g.get("not_permissions", []))
            and all(x in state.events for x in g.get("events", []))
            and all(x not in state.events for x in g.get("not_events", []))
            and all(state.relation(k) >= v for k, v in g.get("relation_at_least", {}).items())
            and all(state.relation(k) <= v for k, v in g.get("relation_at_most", {}).items())
            and all((who, evidence) in state.npc_received
                    for who, items in g.get("npc_received", {}).items() for evidence in items)
        )

    def can_move(self, state: GameState, dest: str) -> bool:
        return (
            state.act == 1 and dest in self.rooms[state.room]["connects"]
            and self.rooms[dest].get("permission") in (None, *state.permissions)
        )

    def available(self, state: GameState) -> list[dict[str, str]]:
        if state.act != 1:
            return []
        moves = [{"id": "move:" + r, "title": "Go to " + self.rooms[r]["name"]}
                 for r in self.rooms[state.room]["connects"] if self.can_move(state, r)]
        interactions = [
            {"id": a["id"], "title": a["title"], "intent": a["intent"]}
            for a in self.spec["actions"]
            if state.room in a["rooms"] and self.guard(state, a.get("requires"))
        ]
        return moves + interactions

    def act(self, state: GameState, action_id: str) -> Result:
        if state.act != 1:
            raise InvalidAction("Act I has already ended")
        if action_id.startswith("move:"):
            dest = action_id[5:]
            if not self.can_move(state, dest):
                raise InvalidAction(f"Cannot move {state.room} -> {dest}")
            return Result(replace(state, room=dest), f"Entered {self.rooms[dest]['name']}", action_id, 0)
        a = self.actions.get(action_id)
        if a is None or state.room not in a["rooms"] or not self.guard(state, a.get("requires")):
            raise InvalidAction(f"Unavailable action: {action_id} at {state.room}")
        for index, outcome in enumerate(a["outcomes"]):
            if self.guard(state, outcome.get("when")):
                effects = outcome.get("effects", {})
                new_relations = list(state.relations)
                for who, value in effects.get("relations", {}).items():
                    if value not in (-1, 0, 1):
                        raise InvalidAction("Status relation must be -1, 0 or +1")
                    new_relations[RELATION_KEYS.index(who)] = value
                new_evidence = state.evidence | frozenset(effects.get("evidence", []))
                new_claims = state.claims | frozenset(effects.get("claims", []))
                # A supported claim is valid only if its evidence predicate is satisfied.
                for claim in new_claims:
                    cond = self.spec["claims"][claim]
                    if not all(e in new_evidence for e in cond.get("required_all", [])):
                        raise InvalidAction(f"Unsound claim: {claim}")
                    if cond.get("required_any") and not any(e in new_evidence for e in cond["required_any"]):
                        raise InvalidAction(f"Unsound claim: {claim}")
                received = {(who, ev) for who, items in effects.get("npc_receives", {}).items()
                            for ev in items}
                if any(ev not in state.evidence for _, ev in received):
                    raise InvalidAction("Cannot disclose evidence the player has not examined")
                after = replace(
                    state,
                    act=effects.get("act", state.act),
                    evidence=new_evidence,
                    claims=new_claims,
                    permissions=state.permissions | frozenset(effects.get("permissions", [])),
                    events=state.events | frozenset(effects.get("events", [])),
                    relations=tuple(new_relations),
                    npc_received=state.npc_received | frozenset(received),
                )
                return Result(after, outcome["say"], action_id, index)
        raise InvalidAction(f"No outcome for {action_id}")

    def route(self, state: GameState, dest: str) -> list[str]:
        """Find a physical route; the test bay requires permission on entry."""
        q = deque([(state.room, [])])
        seen = {state.room}
        while q:
            room, path = q.popleft()
            if room == dest:
                return path
            for next_room in self.rooms[room]["connects"]:
                if next_room in seen:
                    continue
                permit = self.rooms[next_room].get("permission")
                if permit and permit not in state.permissions:
                    continue
                seen.add(next_room)
                q.append((next_room, path + ["move:" + next_room]))
        raise InvalidAction(f"No route from {state.room} to {dest}")

    def guaranteed_completion(self, state: GameState) -> list[str]:
        """Constructs a winning route for ANY reachable Act-I state, independent of optional quests."""
        if state.act != 1:
            return []
        steps: list[str] = []
        s = state
        for action, evidence in (("read_safety_summary", "safety_report"),
                                 ("interview_amara", "amara_priorities")):
            if evidence in s.evidence:
                continue
            for move in self.route(s, "evaluation"):
                steps.append(move)
                s = self.act(s, move).state
            steps.append(action)
            s = self.act(s, action).state
        for move in self.route(s, "hub"):
            steps.append(move)
            s = self.act(s, move).state
        steps.append("file_initial_note")
        assert self.act(s, "file_initial_note").state.act == 2
        return steps


def show_state(state: GameState) -> str:
    return (f"Act {state.act} room={state.room} evidence={sorted(state.evidence)} "
            f"claims={sorted(state.claims)} permissions={sorted(state.permissions)} "
            f"relations={dict(zip(RELATION_KEYS, state.relations))} "
            f"npc_received={sorted(state.npc_received)}")
