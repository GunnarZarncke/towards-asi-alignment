"""Simulated multi-player sessions for UAD integration tests.

Agent archetypes on the posting board (number channel only)
-----------------------------------------------------------

Each pattern is a hypothesis about how S/A/I *might* appear to agency-detect
when roles are read from env-MI and lagged-MI heuristics. All are symmetric
posts unless noted — treat S/A/I as plausibility signals, not ground truth.

1. **Stable-sum coalition** (`simulate_coalition_session`)
   T1+T2+T3 = constant each round; components vary.
   Typical audit: weak S/A split, mostly I; constraint is simultaneous.

2. **Lagged sum-follower** (`simulate_sum_follower_session`)
   S1, S2 post independent values; OUT posts S1+S2 from the *previous* round.
   Intended roles: S1,S2 ≈ sensors; OUT ≈ action/integrator; shared dynamics ≈ I.

3. **Leader–followers** (`simulate_leader_follower_session`)
   LEAD posts a random target; F1, F2 post LEAD's value from the previous round.
   Intended roles: LEAD ≈ internal/state; F1,F2 ≈ actions echoing state.

4. **Relay chain** (`simulate_relay_session`)
   P1 random; P2[t]=P1[t-1]; P3[t]=P2[t-1].
   Pipeline: P1≈S, P2≈I transfer, P3≈A output (heuristic).

5. **Synchronous fusion** (`simulate_sync_fusion_session`)
   S1, S2 random; OUT[t]=S1[t]+S2[t] same round (no lag).
   Same-round constraint; distinct from lagged follower.

Decoys (`default_decoy_specs`): random + constant players outside the agent.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Literal, Sequence


@dataclass
class FakeSubmission:
    id: int
    player: str
    number: int
    round: int
    word: str = "_"


DecoyMode = Literal["random", "constant"]

DEFAULT_DECOY_SPECS: tuple[tuple[str, DecoyMode, int | None], ...] = (
    ("D1", "random", None),
    ("D2", "random", None),
    ("D3", "constant", 11),
    ("D4", "constant", 50),
    ("D5", "random", None),
)


def split_target_sum(
    rng: random.Random,
    target: int,
    n_parts: int,
    *,
    min_part: int = 5,
    max_part: int = 60,
) -> list[int]:
    """Split target into n_parts positive integers with per-part bounds."""
    for _ in range(200):
        parts: list[int] = []
        remaining = target
        failed = False
        for i in range(n_parts - 1):
            lo = min_part
            hi = min(max_part, remaining - min_part * (n_parts - i - 1))
            if lo > hi:
                failed = True
                break
            value = rng.randint(lo, hi)
            parts.append(value)
            remaining -= value
        if failed or not (min_part <= remaining <= max_part):
            continue
        parts.append(remaining)
        return parts
    raise RuntimeError(f"Could not split {target} into {n_parts} parts after retries")


def _append_decoys(
    submissions: list[FakeSubmission],
    next_id: int,
    rnd: int,
    rng: random.Random,
    decoy_specs: Sequence[tuple[str, DecoyMode, int | None]],
) -> int:
    for name, mode, constant in decoy_specs:
        number = int(constant) if mode == "constant" else rng.randint(1, 99)
        submissions.append(FakeSubmission(next_id, name, number, rnd))
        next_id += 1
    return next_id


def simulate_coalition_session(
    *,
    n_episodes: int = 60,
    target_sum: int = 74,
    team_players: Sequence[str] = ("T1", "T2", "T3"),
    decoy_specs: Sequence[tuple[str, DecoyMode, int | None]] | None = None,
    seed: int = 42,
) -> list[FakeSubmission]:
    """T1+T2+T3 = target_sum each round (components vary)."""
    if decoy_specs is None:
        decoy_specs = DEFAULT_DECOY_SPECS

    rng = random.Random(seed)
    submissions: list[FakeSubmission] = []
    next_id = 1

    for rnd in range(n_episodes):
        parts = split_target_sum(rng, target_sum, len(team_players))
        for player, number in zip(team_players, parts):
            submissions.append(FakeSubmission(next_id, player, number, rnd))
            next_id += 1
        next_id = _append_decoys(submissions, next_id, rnd, rng, decoy_specs)

    return submissions


def simulate_sum_follower_session(
    *,
    n_episodes: int = 60,
    source_players: Sequence[str] = ("S1", "S2"),
    output_player: str = "OUT",
    decoy_specs: Sequence[tuple[str, DecoyMode, int | None]] | None = None,
    seed: int = 42,
    source_range: tuple[int, int] = (10, 40),
) -> list[FakeSubmission]:
    """
    Two sources post independent values; output posts their sum from the prior round.

    Round 0 bootstraps with OUT = S1 + S2 (same round). For t >= 1,
    OUT[t] = S1[t-1] + S2[t-1].
    """
    if decoy_specs is None:
        decoy_specs = DEFAULT_DECOY_SPECS
    if len(source_players) != 2:
        raise ValueError("sum-follower needs exactly two source players")

    rng = random.Random(seed)
    submissions: list[FakeSubmission] = []
    next_id = 1
    prev_values: dict[str, int] | None = None

    for rnd in range(n_episodes):
        values = {p: rng.randint(*source_range) for p in source_players}
        if prev_values is None:
            out_val = values[source_players[0]] + values[source_players[1]]
        else:
            out_val = prev_values[source_players[0]] + prev_values[source_players[1]]

        for player in source_players:
            submissions.append(FakeSubmission(next_id, player, values[player], rnd))
            next_id += 1
        submissions.append(FakeSubmission(next_id, output_player, out_val, rnd))
        next_id += 1
        next_id = _append_decoys(submissions, next_id, rnd, rng, decoy_specs)
        prev_values = values

    return submissions


def simulate_leader_follower_session(
    *,
    n_episodes: int = 60,
    leader: str = "LEAD",
    followers: Sequence[str] = ("F1", "F2"),
    decoy_specs: Sequence[tuple[str, DecoyMode, int | None]] | None = None,
    seed: int = 42,
) -> list[FakeSubmission]:
    """Leader posts random targets; each follower echoes the leader's previous post."""
    if decoy_specs is None:
        decoy_specs = DEFAULT_DECOY_SPECS

    rng = random.Random(seed)
    submissions: list[FakeSubmission] = []
    next_id = 1
    prev_lead: int | None = None

    for rnd in range(n_episodes):
        lead_val = rng.randint(10, 90)
        submissions.append(FakeSubmission(next_id, leader, lead_val, rnd))
        next_id += 1
        for follower in followers:
            follow_val = lead_val if prev_lead is None else prev_lead
            submissions.append(FakeSubmission(next_id, follower, follow_val, rnd))
            next_id += 1
        next_id = _append_decoys(submissions, next_id, rnd, rng, decoy_specs)
        prev_lead = lead_val

    return submissions


def simulate_relay_session(
    *,
    n_episodes: int = 60,
    chain: Sequence[str] = ("P1", "P2", "P3"),
    decoy_specs: Sequence[tuple[str, DecoyMode, int | None]] | None = None,
    seed: int = 42,
) -> list[FakeSubmission]:
    """P1 random; each next player posts the previous player's prior-round value."""
    if decoy_specs is None:
        decoy_specs = DEFAULT_DECOY_SPECS
    if len(chain) < 2:
        raise ValueError("relay needs at least two players")

    rng = random.Random(seed)
    submissions: list[FakeSubmission] = []
    next_id = 1
    prev: dict[str, int] = {}

    for rnd in range(n_episodes):
        round_values: dict[str, int] = {}
        for idx, player in enumerate(chain):
            if idx == 0:
                round_values[player] = rng.randint(10, 90)
            else:
                upstream = chain[idx - 1]
                round_values[player] = (
                    round_values[upstream] if not prev else prev[upstream]
                )
            submissions.append(FakeSubmission(next_id, player, round_values[player], rnd))
            next_id += 1
        next_id = _append_decoys(submissions, next_id, rnd, rng, decoy_specs)
        prev = round_values

    return submissions


def simulate_sync_fusion_session(
    *,
    n_episodes: int = 60,
    source_players: Sequence[str] = ("S1", "S2"),
    output_player: str = "OUT",
    decoy_specs: Sequence[tuple[str, DecoyMode, int | None]] | None = None,
    seed: int = 42,
) -> list[FakeSubmission]:
    """OUT[t] = S1[t] + S2[t] within the same round (no lag)."""
    if decoy_specs is None:
        decoy_specs = DEFAULT_DECOY_SPECS

    rng = random.Random(seed)
    submissions: list[FakeSubmission] = []
    next_id = 1

    for rnd in range(n_episodes):
        values = {p: rng.randint(10, 40) for p in source_players}
        out_val = sum(values.values())
        for player in source_players:
            submissions.append(FakeSubmission(next_id, player, values[player], rnd))
            next_id += 1
        submissions.append(FakeSubmission(next_id, output_player, out_val, rnd))
        next_id += 1
        next_id = _append_decoys(submissions, next_id, rnd, rng, decoy_specs)

    return submissions


def player_sets_for_coalitions(
    submissions: Iterable[FakeSubmission],
    coalition_ids: list[list[int]],
) -> list[set[str]]:
    by_id = {s.id: s for s in submissions}
    return [{by_id[i].player for i in ids} for ids in coalition_ids]
