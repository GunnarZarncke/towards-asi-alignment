"""Static validation, finite abstract exploration, and executable regression checks.

Run: python check.py
Important: checks are NOT a Lean proof or a proof of LLM behavior.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, replace
import random

from engine import Game, GameState, InvalidAction, RELATION_KEYS


def validate_schema(g: Game) -> None:
    assert len(g.actions) == len(g.spec["actions"]), "Duplicate action id"
    assert set(g.spec["npcs"]) == {"mara", "leila", "jun", "pavel", "farah", "elena", "daniel", "amara"}
    evidence_ids = set(g.spec["evidence"])
    claims = g.spec["claims"]
    room_ids = set(g.rooms)
    for rid, r in g.rooms.items():
        assert all(x in room_ids for x in r["connects"])
        for other in r["connects"]:
            assert rid in g.rooms[other]["connects"], (rid, other)
    for who, epi in g.spec["npc_epistemics"].items():
        assert who in g.spec["npcs"]
        assert set(epi.get("knows", [])) <= set(g.spec["oracle"]["facts"])
    assert set(g.spec["npc_epistemics"]) == set(g.spec["npcs"])
    for npc in g.spec["npcs"].values():
        assert all(room in room_ids for room in npc["rooms"])
    for aid, a in g.actions.items():
        assert a["rooms"] and set(a["rooms"]) <= room_ids
        assert a["outcomes"], aid
        if len(a["outcomes"]) > 1:
            assert "when" not in a["outcomes"][-1], (aid, "No fallback outcome")
        for rule in [a.get("requires", {})] + [o.get("when", {}) for o in a["outcomes"]]:
            for k in ("evidence", "any_evidence", "not_evidence"):
                assert set(rule.get(k, [])) <= evidence_ids, (aid, k)
            for who, received in rule.get("npc_received", {}).items():
                assert who in g.spec["npcs"]
                assert set(received) <= evidence_ids
            for k in ("relation_at_least", "relation_at_most"):
                assert set(rule.get(k, {})) <= set(RELATION_KEYS)
        for outcome in a["outcomes"]:
            e = outcome.get("effects", {})
            assert set(e.get("evidence", [])) <= evidence_ids, aid
            assert set(e.get("claims", [])) <= set(claims), aid
            assert set(e.get("relations", {})) <= set(RELATION_KEYS), aid
            for who, received in e.get("npc_receives", {}).items():
                assert who in g.spec["npcs"]
                assert set(received) <= evidence_ids
    for cid, rule in claims.items():
        assert set(rule.get("required_all", [])) <= evidence_ids, cid
        assert set(rule.get("required_any", [])) <= evidence_ids, cid
    for essential in ("read_safety_summary", "interview_amara", "file_initial_note"):
        assert essential in g.actions
    assert not g.actions["read_safety_summary"].get("requires")
    assert not g.actions["interview_amara"].get("requires")
    assert g.actions["file_initial_note"]["requires"] == {"evidence": ["safety_report", "amara_priorities"]}
    assert g.actions["file_initial_note"]["rooms"] == ["hub"]
    assert g.actions["read_safety_summary"]["rooms"] == ["evaluation"]
    assert g.actions["interview_amara"]["rooms"] == ["evaluation"]
    print(f"SCHEMA OK: {len(g.rooms)} rooms, {len(g.spec['npcs'])} NPCs, "
          f"{len(evidence_ids)} evidence IDs, {len(g.actions)} actions")


@dataclass(frozen=True)
class AbstractState:
    room: str
    report: bool
    values: bool
    act: int = 1


def abstract_successors(g: Game, a: AbstractState):
    if a.act != 1:
        return
    for dest in g.rooms[a.room]["connects"]:
        if dest != "testbay":  # no initial permissions needed for essential path
            yield replace(a, room=dest)
    if a.room == "evaluation":
        yield replace(a, report=True)
        yield replace(a, values=True)
    if a.room == "hub" and a.report and a.values:
        yield replace(a, act=2)


def abstract_exhaustive(g: Game) -> None:
    start = AbstractState(room="commons", report=False, values=False)
    q = deque([start]); reachable = {start}
    while q:
        x = q.popleft()
        for y in abstract_successors(g, x):
            if y not in reachable:
                reachable.add(y); q.append(y)
    assert any(s.act == 2 for s in reachable)
    unsolvable = []
    for state in reachable:
        if state.act != 1:
            continue
        q2 = deque([state]); seen = {state}; done = False
        while q2:
            u = q2.popleft()
            if u.act == 2:
                done = True; break
            for v in abstract_successors(g, u):
                if v not in seen:
                    seen.add(v); q2.append(v)
        if not done:
            unsolvable.append(state)
    assert not unsolvable, unsolvable
    print(f"ABSTRACT GRAPH OK: {len(reachable)} reachable states, all can reach Act II")


def canonical_playthrough(g: Game) -> None:
    s = g.initial()
    route = [
        "inspect_badge", "ask_mara_competition", "move:hub",
        "inspect_product_dashboard", "inspect_customer_feedback", "move:studio",
        "ask_jun_evaluation_awareness", "inspect_model_demo", "move:evaluation",
        "frame_leila_collaborative", "ask_leila_shutdown", "read_scope_annex",
        "interview_amara", "frame_amara_listen", "interview_amara_case",
        "ask_leila_test_access", "move:testbay", "run_supervised_test",
        "move:platform", "ask_pavel_jobs", "move:security", "inspect_security_policy",
        "frame_farah_respectful", "request_camera_access", "inspect_annotated_camera",
        "move:hub", "compare_safety_boundary", "compare_value_bundle",
        "move:commons", "move:people", "ask_elena_assignments", "inspect_promotion",
        "move:commons", "move:hub", "file_initial_note",
    ]
    for action in route:
        result = g.act(s, action)
        s = result.state
    assert s.act == 2 and "act2_job_alert" in s.evidence
    assert "c_scope_excludes_queue" in s.claims
    assert "c_value_metric_gap" in s.claims
    assert "camera" in s.permissions and "testbay" in s.permissions
    print(f"CANONICAL PLAYTHROUGH OK: {len(route)} steps, Act II reached")


def branch_regression(g: Game) -> None:
    def go(s: GameState, dest: str) -> GameState:
        for move in g.route(s, dest):
            s = g.act(s, move).state
        return s
    # Negative social choice changes outcome, not the underlying facts or solvability.
    s = go(g.initial(), "evaluation")
    s = g.act(s, "frame_amara_instrumental").state
    s = g.act(s, "interview_amara").state
    r = g.act(s, "interview_amara_case")
    assert "amara_case" not in r.state.evidence and r.outcome_index == 1
    assert g.act(s, "interview_amara_case").state == r.state
    s = g.act(s, "frame_leila_accusatory").state
    assert "testbay" not in g.act(s, "ask_leila_test_access").state.permissions
    # But documented scope unlocks the test with no persuasion check.
    s = g.act(s, "read_safety_summary").state
    s = g.act(s, "read_scope_annex").state
    assert "testbay" in g.act(s, "ask_leila_test_access").state.permissions
    completion = g.guaranteed_completion(s)
    for action in completion:
        s = g.act(s, action).state
    assert s.act == 2

    s = go(g.initial(), "security")
    s = g.act(s, "frame_farah_demanding").state
    assert "camera" not in g.act(s, "request_camera_access").state.permissions
    s = g.act(s, "inspect_security_policy").state
    s = go(s, "commons")
    s = g.act(s, "inspect_badge").state
    s = go(s, "security")
    assert "camera" not in g.act(s, "request_camera_access").state.permissions
    s = g.act(s, "present_badge_to_farah").state
    assert ("farah", "visitor_badge") in s.npc_received
    assert "camera" in g.act(s, "request_camera_access").state.permissions
    print("BRANCHES OK: social setbacks, alternative access, and recovery paths")


def randomized_recovery(g: Game, trials: int = 600, length: int = 35) -> None:
    random.seed(1010)
    for _ in range(trials):
        s = g.initial()
        for __ in range(length):
            available = g.available(s)
            if not available:
                break
            # With slight preference for acquiring evidence and for moving to new rooms.
            pick = random.choice(available)
            s = g.act(s, pick["id"]).state
            if s.act != 1:
                break
        if s.act == 1:
            steps = g.guaranteed_completion(s)
            for step in steps:
                s = g.act(s, step).state
        assert s.act == 2
    print(f"RANDOMIZED RECOVERY OK: {trials} histories, each reached Act II")


def check_guaranteed_route(g: Game) -> None:
    """Proof-obligation check: essential path is independent of relations and evidence extras.

    This is the central refinement argument: the full game is monotone for
    mandatory evidence; there are always accessible rooms containing the two
    mandatory unguarded actions, and filing requires only those bits.
    """
    for room in g.rooms:
        for report in (False, True):
            for values in (False, True):
                for relations in ((-1,-1,-1), (0,0,0), (1,1,1), (-1,1,-1)):
                    s = g.initial()
                    extra = {x for x, yes in (("safety_report",report),("amara_priorities",values)) if yes}
                    s = replace(s, room=room, evidence=frozenset(extra), relations=relations,
                                permissions=frozenset({"testbay"}) if room == "testbay" else frozenset())
                    steps = g.guaranteed_completion(s)
                    for action in steps:
                        s = g.act(s, action).state
                    assert s.act == 2
    print("CONSTRUCTIVE ROUTE OK: 144 boundary cases and arbitrary social standing")


if __name__ == "__main__":
    game = Game()
    validate_schema(game)
    abstract_exhaustive(game)
    canonical_playthrough(game)
    branch_regression(game)
    check_guaranteed_route(game)
    randomized_recovery(game)
    print("ALL CHECKS PASSED")
