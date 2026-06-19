from dataclasses import dataclass

from app import BoardStore, run_uad_detection
from coalition_detect import infer_coalition_submission_ids
from observation_builder import find_complete_window


@dataclass
class FakeSubmission:
    id: int
    player: str
    number: int
    round: int
    word: str = "_"


def add_timestep(store: BoardStore, round_idx: int, entries):
    for player, number, word in entries:
        store._add_submission(player, number, word, round_idx, store._now())


def players_for_ids(store, ids):
    by_id = {s.id: s for s in store.submissions}
    return {by_id[i].player for i in ids}


def test_uad_finds_known_three_player_sum_coalition():
    store = BoardStore()
    rounds = [
        [("A", 10, "apple"), ("B", 20, "river"), ("C", 44, "moon"), ("D", 7, "stone"), ("E", 50, "glass")],
        [("A", 12, "pear"),  ("B", 18, "water"), ("C", 44, "star"), ("D", 14, "tree"),  ("E", 41, "iron")],
        [("A", 14, "plum"),  ("B", 17, "lake"),  ("C", 43, "cloud"),("D", 5, "sand"),  ("E", 62, "book")],
        [("A", 20, "fig"),   ("B", 16, "rain"),  ("C", 38, "sun"),  ("D", 22, "cup"),   ("E", 13, "door")],
    ]
    for rnd, entries in enumerate(rounds):
        add_timestep(store, rnd, entries)

    coalitions = infer_coalition_submission_ids(store.submissions, min_rows=3)
    detected_player_sets = [players_for_ids(store, ids) for ids in coalitions]

    assert {"A", "B", "C"} in detected_player_sets


def test_run_uad_submits_marked_coalition():
    store = BoardStore()
    rounds = [
        [("A", 10, "apple"), ("B", 20, "river"), ("C", 44, "moon"), ("D", 7, "stone")],
        [("A", 12, "pear"),  ("B", 18, "water"), ("C", 44, "star"), ("D", 14, "tree")],
        [("A", 14, "plum"),  ("B", 17, "lake"),  ("C", 43, "cloud"),("D", 5, "sand")],
        [("A", 20, "fig"),   ("B", 16, "rain"),  ("C", 38, "sun"),  ("D", 22, "cup")],
    ]
    for rnd, entries in enumerate(rounds):
        add_timestep(store, rnd, entries)

    created = run_uad_detection(store)

    assert created
    assert all(c.is_uad for c in created)
    assert {"A", "B", "C"} in [players_for_ids(store, c.submission_ids) for c in created]


def test_mi_detection_finds_correlated_players():
    store = BoardStore()
    rounds = [
        [("A", 10, "a"), ("B", 10, "b"), ("C", 10, "c"), ("D", 30, "d")],
        [("A", 12, "a"), ("B", 12, "b"), ("C", 12, "c"), ("D", 36, "d")],
        [("A", 14, "a"), ("B", 14, "b"), ("C", 14, "c"), ("D", 42, "d")],
    ]
    for rnd, entries in enumerate(rounds):
        add_timestep(store, rnd, entries)

    coalitions = infer_coalition_submission_ids(store.submissions, min_rows=3)
    detected_player_sets = [players_for_ids(store, ids) for ids in coalitions]

    assert {"A", "B", "C"} in detected_player_sets


def test_complete_window_drops_late_joiner():
    submissions = [
        FakeSubmission(1, "A", 10, 0),
        FakeSubmission(2, "B", 20, 0),
        FakeSubmission(3, "A", 11, 1),
        FakeSubmission(4, "B", 21, 1),
        FakeSubmission(5, "C", 30, 1),  # C joins late
        FakeSubmission(6, "A", 12, 2),
        FakeSubmission(7, "B", 22, 2),
        FakeSubmission(8, "C", 31, 2),
    ]
    rounds, players = find_complete_window(submissions, min_rounds=2)
    assert rounds == [1, 2]
    assert players == ["A", "B", "C"]


def test_manual_group_accepts_multiple_submissions_from_same_player():
    store = BoardStore()
    a1 = store._add_submission("A", 1, "one", 0, store._now())
    a2 = store._add_submission("A", 2, "two", 1, store._now())
    b1 = store._add_submission("B", 3, "three", 0, store._now())

    coalition = store.add_coalition([a1.id, a2.id, b1.id], is_uad=False)

    assert coalition is not None
    assert coalition.submission_ids == (a1.id, a2.id, b1.id)
    assert coalition.is_uad is False
