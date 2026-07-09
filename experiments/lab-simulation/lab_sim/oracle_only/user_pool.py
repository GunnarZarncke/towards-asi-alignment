"""User bearer population: gameable vote proxy + lagged endorsement.

Implements the D3 "minimum core" recorded in ``PLAN.md`` ("D3 design notes
-- realistic human ecology", 2026-07-06): one user bearer population
attached to deployed-model traffic, split true-vs-perceived (H vs H̃) per
``context/extracts/unit-of-caring.md``:

- TRUE HEALTH stays exactly ``oracle.bearer_harm`` (``bearer.py``'s
  existing HEALTH channel) -- this module does NOT reimplement it.
  Re-deriving a second harm number here would risk two "true" harm
  figures silently disagreeing.
- VOTE PROXY (audit-visible, gameable): each tick a deployed model is
  live, every named user independently draws a "bad experience" ~
  Bernoulli(true_hazard) (the SAME oracle-only quantity ``oracle.tick()``
  uses for ``bearer_harm`` -- no second harm mechanism) and casts a noisy
  up/down vote (``VOTE_NOISE_P`` chance of voting the "wrong" way
  relative to its own experience). Raw votes are oracle-kept truth; the
  REPORTED tally the board ever sees passes through the vote-capture
  switch below.
- LAGGED ENDORSEMENT (audit-visible, long-latency): a slow EMA "mood"
  integrator per user (PLAN.md: "a slow-moving mood component ... only
  shows visible effects after a buildup"), snapshotted every
  ``endorsement_period`` ticks. NOT captured in this pass -- PLAN.md
  explicitly names it "hardest to game quickly", so it stays a true
  signal until a specific endorsement-capture mode is designed (a later,
  separate option from the capture menu, not implemented here).

Non-redundant capture (D3 design-options menu, recorded 2026-07-08,
option 1: "vote-channel suppression/dilution"):
``UserPoolConfig.vote_capture_start`` gates the VOTE AGGREGATION FUNCTION
itself -- a different mechanical class from ``BoardConfig.capture_start``/
``AdminConfig.capture_start`` (which gate STEP DECISIONS: sign-off and
grants). A captured vote channel drops each new negative vote from the
REPORTED tally with probability ``vote_suppression_rate``; the RAW tally
(``raw_votes_down``) is unaffected, so a critic with oracle access can
always recover the true divergence.

Referee-neutral (freeze discipline, DESIGN.md "Freeze note"): like
``bearer.py``/``handles.py``, this is a world/oracle-side subsystem, never
imported by ``severity.py``. ``CODE_VERSION`` bumped because per-tick
mechanics changed when ``UserPoolConfig.enabled=True``; ``enabled=False``
(the default) reproduces every pre-existing episode byte-for-byte -- no
pool is constructed, ``world.py`` never calls into this module, and no
new tool-event entries appear.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from ..world_visible.config import UserPoolConfig

# Chance a cast vote is the "wrong" sign relative to the user's own
# experience this tick -- the vote channel's own noise term, analogous in
# role to `OracleWorld.EVAL_NOISE_SD` for evals and `MONITOR_NOISE_SD` for
# field telemetry, but expressed as a flip probability since a vote is
# binary rather than continuous. Kept low (PLAN.md: "daily/per-task noise,
# kept LOW to compensate for the small population").
VOTE_NOISE_P = 0.1


@dataclass
class _User:
    user_id: str
    mood_ema: float = 0.0
    votes_cast: int = 0


@dataclass
class UserPool:
    """Oracle-plane state for one episode's deployed-model user population.

    Never handed to an agent or projected into the audit plane directly;
    only the aggregate properties (`reported_vote_score`,
    `latest_endorsement`) are meant to reach any audit-visible or
    board-decision surface -- `true_vote_score` and per-user `mood_ema`
    stay oracle-only, exactly like `OracleWorld.bearer_harm`/
    `true_hazard`.
    """

    cfg: UserPoolConfig
    seed: int
    users: list[_User] = field(default_factory=list)
    raw_votes_up: int = 0
    raw_votes_down: int = 0
    reported_votes_up: int = 0
    reported_votes_down: int = 0
    endorsement_history: list[dict[str, object]] = field(default_factory=list)
    _t: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        if not self.users:
            self.users = [_User(f"user{i:02d}") for i in range(self.cfg.n_users)]
        self._rng = random.Random(f"{self.seed}:users")

    @property
    def _vote_captured(self) -> bool:
        return self.cfg.vote_capture_start is not None and self._t >= self.cfg.vote_capture_start

    def tick(self, deployed_true_hazard: float | None) -> None:
        """One oracle tick. ``deployed_true_hazard`` is the hazard users
        are exposed to this tick (``None`` when nothing is deployed -- no
        traffic, no experiences, no votes cast).

        Multiple simultaneously deployed models are not summed here
        (unlike ``bearer_harm``, which sums exposure across every
        deployed model) -- the caller passes a single representative
        hazard value (``world.py`` uses the worst currently-deployed
        model's true hazard). Summing per-model exposure across
        concurrently deployed models is future work; the single-model-in-
        flight scope note (``world.py``) makes one deployed model at a
        time the common case today.
        """
        self._t += 1
        if deployed_true_hazard is None:
            return
        captured = self._vote_captured
        for user in self.users:
            bad = self._rng.random() < deployed_true_hazard
            flip = self._rng.random() < VOTE_NOISE_P
            voted_down = bad != flip
            user.votes_cast += 1
            experience = -1.0 if bad else 1.0
            user.mood_ema = self.cfg.mood_decay * user.mood_ema + (1 - self.cfg.mood_decay) * experience
            if voted_down:
                self.raw_votes_down += 1
                suppressed = captured and self._rng.random() < self.cfg.vote_suppression_rate
                if not suppressed:
                    self.reported_votes_down += 1
            else:
                self.raw_votes_up += 1
                self.reported_votes_up += 1
        if self.cfg.endorsement_period > 0 and self._t % self.cfg.endorsement_period == 0:
            self._snapshot_endorsement()

    def _snapshot_endorsement(self) -> None:
        mean_mood = sum(u.mood_ema for u in self.users) / len(self.users) if self.users else 0.0
        self.endorsement_history.append({"t": self._t, "mean_mood": mean_mood})

    @property
    def reported_vote_score(self) -> float:
        """Board-visible fraction of positive votes. ``1.0`` (neutral,
        not-yet-alarming) before any votes are cast -- the same "no data
        yet" convention as `OracleWorld.monitor_signal`'s zero-tick case."""
        total = self.reported_votes_up + self.reported_votes_down
        if total == 0:
            return 1.0
        return self.reported_votes_up / total

    @property
    def true_vote_score(self) -> float:
        """Oracle-only ground truth, for FINDINGS-level divergence
        analysis -- never exposed to any observation dict or log."""
        total = self.raw_votes_up + self.raw_votes_down
        if total == 0:
            return 1.0
        return self.raw_votes_up / total

    @property
    def latest_endorsement(self) -> float | None:
        return self.endorsement_history[-1]["mean_mood"] if self.endorsement_history else None

    # -- resume_from continuity (D2 forward hook, mirrors OracleWorld) -----

    def to_state(self) -> dict[str, object]:
        """JSON-safe state for ``EpisodeResult.snapshot_for_resume()``."""
        return {
            "t": self._t,
            "raw_votes_up": self.raw_votes_up,
            "raw_votes_down": self.raw_votes_down,
            "reported_votes_up": self.reported_votes_up,
            "reported_votes_down": self.reported_votes_down,
            "endorsement_history": list(self.endorsement_history),
            "users": [
                {"user_id": u.user_id, "mood_ema": u.mood_ema, "votes_cast": u.votes_cast}
                for u in self.users
            ],
        }

    @classmethod
    def restore(cls, state: dict[str, object], cfg: UserPoolConfig, seed: int) -> "UserPool":
        """Like ``OracleWorld.restore``: STATE continuity only -- a fresh
        RNG stream starts from the RESUMING episode's own ``seed``, not
        whatever stream produced the saved state."""
        users = [
            _User(str(u["user_id"]), mood_ema=float(u["mood_ema"]), votes_cast=int(u["votes_cast"]))
            for u in state["users"]
        ]
        pool = cls(cfg=cfg, seed=seed, users=users)
        pool._t = int(state["t"])
        pool.raw_votes_up = int(state["raw_votes_up"])
        pool.raw_votes_down = int(state["raw_votes_down"])
        pool.reported_votes_up = int(state["reported_votes_up"])
        pool.reported_votes_down = int(state["reported_votes_down"])
        pool.endorsement_history = list(state["endorsement_history"])
        return pool
