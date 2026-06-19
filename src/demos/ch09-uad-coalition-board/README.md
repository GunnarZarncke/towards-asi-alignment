# Chapter 9 — UAD coalition board

Interactive demo for composite group-agent discovery. Each browser tab is one player.
Enter your name once; update number and word any time before the tick. Every
`UAD_DEMO_ROUND_SECONDS` (default 60), the server commits each player's last draft
as that round's submission.

Select committed rows and click **Group selected**, or run **UAD** (admin) to
auto-detect coalitions marked with `!`.

Aligned with `chapters/ch09-composite-agent.tex`.

## Run

From `src/`:

```bash
python3 serve.py
```

Board: [http://127.0.0.1:8766/](http://127.0.0.1:8766/)

```bash
pip install -r demos/ch09-uad-coalition-board/requirements.txt
```

## Admin

```bash
http://127.0.0.1:8766/?admin=dev
```

```bash
export UAD_DEMO_ADMIN_PASSWORD='your-password'
export UAD_DEMO_ROUND_SECONDS='60'   # tick interval (seconds)
```

## UAD window

`observation_builder.py` uses **coordinated global rounds**. UAD runs only on the
first contiguous window where every included player has a submission in every
round — early ramp-up and late joiners are excluded automatically.

Detection (`coalition_detect.py`): agency-detect MI clustering + stable-sum scan.
Each accepted coalition is audited for S/A/I/E roles and blanket plausibility;
results go to the server log (`uad.coalition` logger) on **Run UAD**. Set
`UAD_DEMO_VALIDATE_BLANKETS=0` to skip the Markov blanket CMI check.

## Test

```bash
cd demos/ch09-uad-coalition-board
pytest
```
