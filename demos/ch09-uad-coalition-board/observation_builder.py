"""
Build the UAD observation matrix from coordinated global rounds.

Raw data:
    submission events: (id, player, number, word, round)

Derived view:
    X[t][i] = player i's number at global round t
    M[t][i] = 1 if a submission exists, else 0
    ids[t][i] = submission id when present

Rounds are synchronized wall-clock ticks (see app.py). UAD uses only a contiguous
window where every selected player has a submission in every round — early
ramp-up rounds and late-joining players are dropped automatically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Protocol, Sequence, Tuple


class TimedSubmission(Protocol):
    id: int
    player: str
    number: float
    round: int


@dataclass(frozen=True)
class ObservationMatrix:
    players: List[str]
    rounds: List[int]
    numbers: List[List[float]]
    mask: List[List[int]]
    submission_ids: List[List[Optional[int]]]

    @property
    def shape(self) -> Tuple[int, int]:
        if not self.numbers:
            return (0, len(self.players))
        return (len(self.numbers), len(self.numbers[0]))

    def to_trace(self) -> list[dict[str, int]]:
        """Synchronous trace for agency-detect; rows are complete by construction."""
        trace: list[dict[str, int]] = []
        for row_idx in range(len(self.numbers)):
            record: dict[str, int] = {}
            for col, player in enumerate(self.players):
                record[player] = int(round(self.numbers[row_idx][col]))
            trace.append(record)
        return trace

    def submission_ids_for_group(self, player_names: Sequence[str]) -> List[int]:
        player_to_col = {p: i for i, p in enumerate(self.players)}
        cols = [player_to_col[p] for p in player_names]
        ids: List[int] = []
        for row_idx in range(len(self.numbers)):
            for col in cols:
                sid = self.submission_ids[row_idx][col]
                if sid is not None:
                    ids.append(sid)
        return ids


def find_complete_window(
    submissions: Sequence[TimedSubmission],
    *,
    min_rounds: int = 3,
    min_players: int = 2,
) -> tuple[list[int], list[str]]:
    """
    Contiguous round window maximizing the number of complete players.

    Late joiners missing early rounds are excluded until a later window can
    include them with full attendance.
    """
    if not submissions:
        return [], []

    all_players = sorted({s.player for s in submissions})
    min_round = min(s.round for s in submissions)
    max_round = max(s.round for s in submissions)
    present = {(s.player, s.round) for s in submissions}

    best_window: list[int] = []
    best_players: list[str] = []
    best_score: tuple[int, int] = (-1, -1)

    for start in range(min_round, max_round + 1):
        window = list(range(start, max_round + 1))
        if len(window) < min_rounds:
            continue
        complete_players = [
            player
            for player in all_players
            if all((player, rnd) in present for rnd in window)
        ]
        if len(complete_players) < min_players:
            continue
        score = (len(complete_players), len(window))
        if score > best_score:
            best_score = score
            best_window = window
            best_players = sorted(complete_players)

    return best_window, best_players


def build_observation_matrix(
    submissions: Iterable[TimedSubmission],
    *,
    rounds: Optional[Sequence[int]] = None,
    players: Optional[Sequence[str]] = None,
) -> ObservationMatrix:
    """
    Build a round × player matrix for a coordinated timestep window.

    When `rounds` and `players` are omitted, uses `find_complete_window`.
    """
    ordered = sorted(list(submissions), key=lambda s: (s.round, s.id))
    if not ordered:
        return ObservationMatrix(players=[], rounds=[], numbers=[], mask=[], submission_ids=[])

    if rounds is None or players is None:
        auto_rounds, auto_players = find_complete_window(ordered)
        if rounds is None:
            rounds = auto_rounds
        if players is None:
            players = auto_players

    round_list = list(rounds or [])
    player_list = list(players or [])
    if not round_list or not player_list:
        return ObservationMatrix(
            players=player_list,
            rounds=round_list,
            numbers=[],
            mask=[],
            submission_ids=[],
        )

    player_set = set(player_list)
    round_set = set(round_list)
    lookup: dict[tuple[str, int], TimedSubmission] = {}
    for submission in ordered:
        if submission.player not in player_set or submission.round not in round_set:
            continue
        key = (submission.player, submission.round)
        if key not in lookup:
            lookup[key] = submission

    numbers: List[List[float]] = []
    mask: List[List[int]] = []
    submission_ids: List[List[Optional[int]]] = []

    for rnd in round_list:
        number_row: List[float] = []
        mask_row: List[int] = []
        id_row: List[Optional[int]] = []
        for player in player_list:
            submission = lookup.get((player, rnd))
            if submission is None:
                number_row.append(0.0)
                mask_row.append(0)
                id_row.append(None)
            else:
                number_row.append(float(submission.number))
                mask_row.append(1)
                id_row.append(submission.id)
        numbers.append(number_row)
        mask.append(mask_row)
        submission_ids.append(id_row)

    return ObservationMatrix(
        players=player_list,
        rounds=round_list,
        numbers=numbers,
        mask=mask,
        submission_ids=submission_ids,
    )


def stable_sum_score(
    observation: ObservationMatrix,
    group_players: Sequence[str],
    *,
    min_rows: int = 3,
) -> Optional[dict]:
    if len(observation.numbers) < min_rows:
        return None

    player_to_col = {p: i for i, p in enumerate(observation.players)}
    cols = [player_to_col[p] for p in group_players]
    sums: List[float] = []
    for row_idx in range(len(observation.numbers)):
        if not all(observation.mask[row_idx][col] == 1 for col in cols):
            return None
        sums.append(sum(observation.numbers[row_idx][col] for col in cols))

    target = sum(sums) / len(sums)
    variance = sum((s - target) ** 2 for s in sums) / len(sums)

    return {
        "players": list(group_players),
        "target": target,
        "variance": variance,
        "support": len(sums),
        "score": -variance,
        "submission_ids": observation.submission_ids_for_group(group_players),
    }


def lagged_sum_score(
    observation: ObservationMatrix,
    sources: Sequence[str],
    output: str,
    *,
    lag: int = 1,
    min_rows: int = 3,
) -> Optional[dict]:
    """
    Score whether `output` at round t equals sum(sources) at round t-lag.

    Intended for sensor pair + lagged actor patterns (OUT posts previous S1+S2).
    """
    if len(sources) != 2 or lag < 1:
        return None
    if len(observation.numbers) <= lag:
        return None

    player_to_col = {p: i for i, p in enumerate(observation.players)}
    try:
        out_col = player_to_col[output]
        src_cols = [player_to_col[s] for s in sources]
    except KeyError:
        return None

    residuals: List[float] = []
    for row_idx in range(lag, len(observation.numbers)):
        if observation.mask[row_idx][out_col] != 1:
            return None
        if any(observation.mask[row_idx - lag][col] != 1 for col in src_cols):
            return None
        predicted = sum(observation.numbers[row_idx - lag][col] for col in src_cols)
        actual = observation.numbers[row_idx][out_col]
        residuals.append(actual - predicted)

    if len(residuals) < min_rows:
        return None

    target = sum(residuals) / len(residuals)
    variance = sum((r - target) ** 2 for r in residuals) / len(residuals)

    return {
        "players": [sources[0], sources[1], output],
        "sources": list(sources),
        "output": output,
        "lag": lag,
        "target": target,
        "variance": variance,
        "support": len(residuals),
        "score": -variance,
        "submission_ids": observation.submission_ids_for_group([sources[0], sources[1], output]),
    }
