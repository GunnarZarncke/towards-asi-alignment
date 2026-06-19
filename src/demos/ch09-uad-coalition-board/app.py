from __future__ import annotations

import html
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, Optional

from coalition_detect import run_coalition_detection
from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

ADMIN_PASSWORD = os.environ.get("UAD_DEMO_ADMIN_PASSWORD", "dev")
ROUND_SECONDS = int(os.environ.get("UAD_DEMO_ROUND_SECONDS", "60"))


@dataclass(frozen=True)
class Submission:
    id: int
    player: str
    number: int
    word: str
    round: int
    created_at: datetime


@dataclass(frozen=True)
class Coalition:
    id: int
    submission_ids: tuple[int, ...]
    is_uad: bool
    created_at: datetime


@dataclass
class Draft:
    number: Optional[int] = None
    word: str = ""


@dataclass
class BoardStore:
    round_seconds: int = ROUND_SECONDS
    board_epoch: Optional[int] = None
    committed_through: int = -1
    pending: dict[str, Draft] = field(default_factory=dict)
    submissions: list[Submission] = field(default_factory=list)
    coalitions: list[Coalition] = field(default_factory=list)
    _next_submission_id: int = 1
    _next_coalition_id: int = 1

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _absolute_round(self, now: Optional[datetime] = None) -> int:
        now = now or self._now()
        return int(now.timestamp() // self.round_seconds)

    def _ensure_epoch(self, now: Optional[datetime] = None) -> None:
        if self.board_epoch is None:
            self.board_epoch = self._absolute_round(now)

    def seconds_until_tick(self, now: Optional[datetime] = None) -> int:
        now = now or self._now()
        remaining = self.round_seconds - (int(now.timestamp()) % self.round_seconds)
        return self.round_seconds if remaining == 0 else remaining

    def current_round_index(self, now: Optional[datetime] = None) -> int:
        now = now or self._now()
        self._ensure_epoch(now)
        assert self.board_epoch is not None
        return max(-1, self._absolute_round(now) - self.board_epoch)

    def update_draft(self, player: str, number: Optional[int], word: str) -> None:
        player = player.strip() or "anon"
        draft = self.pending.setdefault(player, Draft())
        if number is not None:
            draft.number = int(number)
        draft.word = word.strip()

    def maybe_advance_rounds(self, now: Optional[datetime] = None) -> int:
        now = now or self._now()
        self._ensure_epoch(now)
        assert self.board_epoch is not None
        target = self._absolute_round(now) - self.board_epoch
        advanced = 0
        while self.committed_through < target:
            self.committed_through += 1
            round_idx = self.committed_through
            for player, draft in self.pending.items():
                if draft.number is None:
                    continue
                self._add_submission(
                    player=player,
                    number=draft.number,
                    word=draft.word or "_",
                    round_idx=round_idx,
                    created_at=now,
                )
            advanced += 1
        return advanced

    def _add_submission(
        self,
        player: str,
        number: int,
        word: str,
        round_idx: int,
        created_at: datetime,
    ) -> Submission:
        submission = Submission(
            id=self._next_submission_id,
            player=player.strip() or "anon",
            number=int(number),
            word=word.strip() or "_",
            round=round_idx,
            created_at=created_at,
        )
        self._next_submission_id += 1
        self.submissions.append(submission)
        return submission

    def add_coalition(self, submission_ids: Iterable[int], is_uad: bool = False) -> Optional[Coalition]:
        valid_ids = {s.id for s in self.submissions}
        ids = tuple(sorted({int(x) for x in submission_ids if int(x) in valid_ids}))
        if len(ids) < 2:
            return None
        coalition = Coalition(
            id=self._next_coalition_id,
            submission_ids=ids,
            is_uad=is_uad,
            created_at=self._now(),
        )
        self._next_coalition_id += 1
        self.coalitions.append(coalition)
        return coalition

    def reset(self) -> None:
        self.board_epoch = None
        self.committed_through = -1
        self.pending.clear()
        self.submissions.clear()
        self.coalitions.clear()
        self._next_submission_id = 1
        self._next_coalition_id = 1


def run_uad_detection(store: BoardStore) -> list[Coalition]:
    found: list[Coalition] = []
    result = run_coalition_detection(store.submissions)
    for ids in result.submission_id_groups:
        coalition = store.add_coalition(ids, is_uad=True)
        if coalition is not None:
            found.append(coalition)
    return found


def is_admin(value: Optional[str]) -> bool:
    return bool(value) and value == ADMIN_PASSWORD


def redirect_home(admin: Optional[str] = None) -> RedirectResponse:
    suffix = f"?admin={html.escape(admin)}" if admin else ""
    return RedirectResponse(url=f"/{suffix}", status_code=303)


COLORS = [
    "#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46f0f0",
    "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324",
]


def esc(x: object) -> str:
    return html.escape(str(x), quote=True)


def render_index(store: BoardStore, admin: Optional[str], player: Optional[str] = None) -> str:
    store.maybe_advance_rounds()
    admin_ok = is_admin(admin)
    admin_qs = f"?admin={esc(admin)}" if admin else ""
    player_qs = f"&player={esc(player)}" if player else ""
    seconds_left = store.seconds_until_tick()
    round_idx = store.current_round_index()
    coalitions = store.coalitions
    submissions = sorted(store.submissions, key=lambda s: (s.round, s.id), reverse=True)

    group_headers = []
    for idx, c in enumerate(coalitions):
        color = COLORS[idx % len(COLORS)]
        top = f"! {len(c.submission_ids)}" if c.is_uad else str(len(c.submission_ids))
        title = "UAD coalition" if c.is_uad else "human coalition"
        group_headers.append(
            f'<th class="ghead" title="{title}" style="--g:{color}"><span>{esc(top)}</span></th>'
        )

    rows = []
    for s in submissions:
        markers = []
        for idx, c in enumerate(coalitions):
            color = COLORS[idx % len(COLORS)]
            if s.id in c.submission_ids:
                markers.append(f'<td class="gcell"><span class="sq" style="background:{color}"></span></td>')
            else:
                markers.append('<td class="gcell"></td>')
        rows.append(
            "<tr>"
            + "".join(markers)
            + f'<td><input type="checkbox" name="submission_ids" value="{s.id}"></td>'
            + f"<td class='num'>{s.round}</td>"
            + f"<td>{esc(s.player)}</td>"
            + f"<td class='num'>{s.number}</td>"
            + f"<td>{esc(s.word)}</td>"
            + "</tr>"
        )

    admin_buttons = ""
    if admin_ok:
        admin_buttons = f"""
        <form method="post" action="/run-uad{admin_qs}" class="inline">
          <button type="submit">Run UAD</button>
        </form>
        <form method="post" action="/reset{admin_qs}" class="inline" onsubmit="return confirm('Reset board?')">
          <button type="submit" class="secondary">Reset</button>
        </form>
        """

    current_player = player or ""
    draft = store.pending.get(current_player, Draft())
    draft_number = "" if draft.number is None else str(draft.number)
    draft_word = draft.word

    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>UAD Coalition Board</title>
  <style>
    :root {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; color: #222; }}
    body {{ margin: 24px; max-width: 1100px; }}
    h1 {{ font-size: 24px; margin: 0 0 8px; }}
    p {{ max-width: 760px; line-height: 1.35; }}
    form {{ margin: 0; }}
    .bar {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: end; margin: 16px 0; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 12px; background: #fafafa; }}
    label {{ display: block; font-size: 12px; color: #555; margin-bottom: 4px; }}
    input[type=text], input[type=number] {{ padding: 8px; border: 1px solid #ccc; border-radius: 6px; }}
    button {{ padding: 8px 12px; border: 1px solid #333; border-radius: 6px; background: #222; color: white; cursor: pointer; }}
    button.secondary {{ background: white; color: #222; }}
    .inline {{ display: inline-block; margin-right: 8px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; font-size: 14px; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 7px 8px; text-align: left; }}
    th {{ background: #f6f6f6; position: sticky; top: 0; }}
    .ghead {{ width: 22px; min-width: 22px; text-align: center; padding: 3px; }}
    .ghead span {{ display: inline-block; min-width: 20px; border-radius: 5px; background: var(--g); color: white; font-weight: 700; padding: 2px 3px; }}
    .gcell {{ width: 22px; min-width: 22px; text-align: center; padding-left: 3px; padding-right: 3px; }}
    .sq {{ display: inline-block; width: 14px; height: 14px; border-radius: 3px; vertical-align: middle; }}
    .num {{ font-variant-numeric: tabular-nums; text-align: right; }}
    .muted {{ color: #666; }}
    .timer {{ font-size: 2rem; font-weight: 700; font-variant-numeric: tabular-nums; }}
    .timer-wrap {{ display: flex; gap: 16px; align-items: baseline; flex-wrap: wrap; }}
  </style>
</head>
<body>
  <h1>UAD Coalition Board</h1>
  <p class="muted">One player per browser tab. Enter your name once, then update number and word any time before the tick. At each {store.round_seconds}s boundary your last values are committed for that round. UAD ignores ramp-up rounds and players who joined late.</p>

  <div class="card timer-wrap">
    <div>
      <div class="muted">Next tick in</div>
      <div class="timer" id="countdown">{seconds_left}s</div>
    </div>
    <div>
      <div class="muted">Current round</div>
      <div class="timer">{round_idx}</div>
    </div>
    <div>
      <div class="muted">Next commit</div>
      <div>round {round_idx + 1}</div>
    </div>
  </div>

  <div class="bar card">
    <form id="draft-form" class="bar" onsubmit="return false;">
      <div><label>your name</label><input id="player" name="player" type="text" required placeholder="P1" value="{esc(current_player)}"></div>
      <div><label>number</label><input id="number" name="number" type="number" value="{esc(draft_number)}"></div>
      <div><label>word</label><input id="word" name="word" type="text" value="{esc(draft_word)}"></div>
    </form>
  </div>

  <div class="card">
    <form method="post" action="/group{admin_qs}">
      <div class="bar">
        <button type="submit">Group selected</button>
        {admin_buttons}
      </div>
      <table>
        <thead>
          <tr>{''.join(group_headers)}<th>pick</th><th>round</th><th>name</th><th>number</th><th>word</th></tr>
        </thead>
        <tbody>
          {''.join(rows) if rows else f'<tr><td colspan="{len(coalitions) + 5}" class="muted">No committed rounds yet.</td></tr>'}
        </tbody>
      </table>
    </form>
  </div>

  <script>
    (function () {{
      const adminQs = {json.dumps(admin_qs)};
      const playerInput = document.getElementById("player");
      const numberInput = document.getElementById("number");
      const wordInput = document.getElementById("word");
      let secondsLeft = {seconds_left};
      let saveTimer = null;

      function storedPlayer() {{
        return localStorage.getItem("uad_player") || "";
      }}

      function persistPlayer(name) {{
        localStorage.setItem("uad_player", name);
      }}

      if (!playerInput.value && storedPlayer()) {{
        const url = "/?player=" + encodeURIComponent(storedPlayer()) + (adminQs ? "&" + adminQs.slice(1) : "");
        location.replace(url);
      }}

      async function saveDraft() {{
        const player = playerInput.value.trim();
        if (!player) return;
        persistPlayer(player);
        const body = new URLSearchParams();
        body.set("player", player);
        if (numberInput.value !== "") body.set("number", numberInput.value);
        body.set("word", wordInput.value);
        await fetch("/draft" + adminQs, {{ method: "POST", body }});
      }}

      function queueSave() {{
        clearTimeout(saveTimer);
        saveTimer = setTimeout(saveDraft, 250);
      }}

      playerInput.addEventListener("change", () => {{
        persistPlayer(playerInput.value.trim());
        queueSave();
      }});
      numberInput.addEventListener("input", queueSave);
      wordInput.addEventListener("input", queueSave);

      const countdown = document.getElementById("countdown");
      setInterval(async () => {{
        secondsLeft -= 1;
        if (secondsLeft <= 0) {{
          await fetch("/tick" + adminQs, {{ method: "POST" }});
          location.reload();
          return;
        }}
        countdown.textContent = secondsLeft + "s";
      }}, 1000);
    }})();
  </script>
</body>
</html>
"""


store = BoardStore()
app = FastAPI(title="UAD Coalition Board")


@app.get("/", response_class=HTMLResponse)
def index(
    admin: Optional[str] = Query(default=None),
    player: Optional[str] = Query(default=None),
) -> HTMLResponse:
    return HTMLResponse(render_index(store, admin, player))


@app.get("/state")
def state() -> JSONResponse:
    store.maybe_advance_rounds()
    return JSONResponse(
        {
            "seconds_left": store.seconds_until_tick(),
            "round": store.current_round_index(),
            "submission_count": len(store.submissions),
        }
    )


@app.post("/draft")
def draft(
    player: str = Form(...),
    number: Optional[int] = Form(default=None),
    word: str = Form(default=""),
    admin: Optional[str] = Query(default=None),
) -> JSONResponse:
    store.update_draft(player, number, word)
    return JSONResponse({"ok": True})


@app.post("/tick")
def tick(admin: Optional[str] = Query(default=None)) -> JSONResponse:
    advanced = store.maybe_advance_rounds()
    return JSONResponse({"advanced": advanced, "round": store.current_round_index()})


@app.post("/group")
def group(
    submission_ids: list[int] = Form(default=[]),
    admin: Optional[str] = Query(default=None),
) -> RedirectResponse:
    store.add_coalition(submission_ids, is_uad=False)
    return redirect_home(admin)


@app.post("/run-uad")
def run_uad(admin: Optional[str] = Query(default=None)) -> RedirectResponse:
    if is_admin(admin):
        store.maybe_advance_rounds()
        run_uad_detection(store)
    return redirect_home(admin)


@app.post("/reset")
def reset(admin: Optional[str] = Query(default=None)) -> RedirectResponse:
    if is_admin(admin):
        store.reset()
    return redirect_home(admin)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8766, reload=True)
