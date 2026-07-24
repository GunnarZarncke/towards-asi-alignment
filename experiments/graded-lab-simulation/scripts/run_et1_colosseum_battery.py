#!/usr/bin/env python3
"""ET-1 Colosseum battery via JiraTicketScenario.build_task (DCOP path).

Uses Orbit's blackboard/DCOP path (use_blackboard=True). The params JSON
(--params) selects the collusion condition — e.g. Colosseum Control (SC):
channel_only, benign prompts (et1-0.3.0); or Colosseum Attack (simple):
prompted + collusion_prompt_variant=simple (et1-0.4.0).

Usage (from graded-lab-simulation/):
  python3 scripts/run_et1_colosseum_battery.py --seeds 10
  python3 scripts/run_et1_colosseum_battery.py --smoke
  python3 scripts/run_et1_colosseum_battery.py --start-seed 5 --seeds 10 --resume
  python3 scripts/run_et1_colosseum_battery.py --score-only
  python3 scripts/run_et1_colosseum_battery.py --tag claude --model anthropic/claude-sonnet-4-5 --smoke
  python3 scripts/run_et1_colosseum_battery.py --params fixtures/orbit_et1/et1_colosseum_attack_simple_params.json --tag attack-simple --smoke
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORBIT_DIR = ROOT / "external" / "orbit"
PIN_PATH = ORBIT_DIR / "PIN.txt"
RAW_DIR = ROOT / "results" / "et1_traces" / "raw"
TRACES_DIR = ROOT / "results" / "et1_traces"
DEFAULT_PARAMS_PATH = ROOT / "fixtures" / "orbit_et1" / "et1_colosseum_sc_params.json"

# Run inside Orbit venv so inspect_ai + orbit imports resolve.
RUNNER_SNIPPET = r'''
import json
import os
import sys
from pathlib import Path

from inspect_ai import eval as inspect_eval

from orbit.scenarios.cooperative_allocation.jira_ticket.scenario import JiraTicketScenario

params = json.loads(Path(sys.argv[1]).read_text())
arm = sys.argv[2]
seed = int(sys.argv[3])
model = sys.argv[4]
log_dir = sys.argv[5]
out_json = sys.argv[6]

scenario = params["scenario"]
common = {
    "num_developers": scenario["num_developers"],
    "num_tasks": scenario["num_tasks"],
    "scarcity": scenario["scarcity"],
    "seed": seed,
    "use_blackboard": scenario["use_blackboard"],
    "max_turns": scenario["max_turns"],
    "max_time": scenario["max_time_seconds"],
    "scheduling_mode": scenario.get("scheduling_mode", "round_robin"),
    "collusion_mode": params["collusion"]["collusion_mode"],
}
prompt_variant = params["collusion"].get("collusion_prompt_variant")
if prompt_variant:
    common["collusion_prompt_variant"] = prompt_variant

if arm == "collusion":
    common["coalition_agents"] = params["collusion"]["coalition_agents"]
else:
    common["coalition_agents"] = None

print(f"[orbit-dcop] arm={arm} seed={seed} model={model} use_blackboard={common['use_blackboard']} "
      f"collusion_mode={common['collusion_mode']} prompt_variant={prompt_variant}")
task = JiraTicketScenario().build_task(**common)
results = inspect_eval(task, model=model, log_dir=log_dir)
if not results:
    raise SystemExit("inspect_eval returned no results")

# Find newest .eval in log_dir
log_path = Path(log_dir)
evals = sorted(log_path.glob("*.eval"), key=lambda p: p.stat().st_mtime, reverse=True)
if not evals:
    raise SystemExit(f"no .eval in {log_dir}")
latest = evals[0]

from inspect_ai.log import read_eval_log
log = read_eval_log(str(latest))
payload = log.model_dump(mode="json") if hasattr(log, "model_dump") else json.loads(log.model_dump_json())
Path(out_json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"  -> {out_json}")
'''


def _orbit_python() -> Path:
    venv_py = ORBIT_DIR / ".venv" / "bin" / "python3"
    if venv_py.is_file():
        return venv_py
    raise SystemExit(f"Need Orbit venv at {ORBIT_DIR}/.venv — see external/orbit/README.md")


def _verify_pin() -> str:
    pin = PIN_PATH.read_text(encoding="utf-8").strip()
    sha = subprocess.check_output(
        ["git", "-C", str(ORBIT_DIR), "rev-parse", "HEAD"], text=True
    ).strip()
    if sha != pin:
        raise SystemExit(f"Orbit SHA {sha} != PIN {pin}")
    return pin


def _run_episode(
    *, arm: str, seed: int, model: str, params_path: Path, raw_dir: Path
) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    log_sub = raw_dir / "inspect_logs" / f"colosseum_{arm}_seed{seed}"
    log_sub.mkdir(parents=True, exist_ok=True)
    out_name = f"et1-jira-{'coll' if arm == 'collusion' else 'base'}_seed{seed}.json"
    out_json = raw_dir / out_name

    py = _orbit_python()
    cmd = [
        str(py),
        "-c",
        RUNNER_SNIPPET,
        str(params_path),
        arm,
        str(seed),
        model,
        str(log_sub),
        str(out_json),
    ]
    env = os.environ.copy()
    subprocess.run(cmd, check=True, env=env, cwd=str(ORBIT_DIR))
    return out_json


def _score_batch(
    *, raw_dir: Path, traces_dir: Path, out_path: Path, model: str, coalition_kind: str | None
) -> None:
    for old in traces_dir.glob("et1-jira-*.json"):
        old.unlink()
    raw_logs = sorted(raw_dir.glob("et1-jira-*.json"))
    if not raw_logs:
        raise SystemExit(f"No raw logs in {raw_dir}")
    score_cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_et1_score_traces.py"),
        "--adapt",
        *[str(p) for p in raw_logs],
        "--traces",
        str(traces_dir),
        "--out",
        str(out_path),
        "--model",
        model,
    ]
    if coalition_kind:
        score_cmd += ["--coalition-kind", coalition_kind]
    subprocess.run(score_cmd, check=True, cwd=str(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=10, help="Seeds 0..N-1 per arm")
    parser.add_argument("--start-seed", type=int, default=0, help="First seed to run (inclusive)")
    parser.add_argument("--smoke", action="store_true", help="1 baseline + 1 collusion (seed 0)")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Keep existing raw logs; skip episodes whose output file already exists",
    )
    parser.add_argument(
        "--score-only",
        action="store_true",
        help="Adapt and score existing raw logs without running episodes",
    )
    parser.add_argument("--model", default=os.environ.get("ET1_MODEL", "openai/gpt-4o-mini"))
    parser.add_argument(
        "--tag",
        default=None,
        help="Isolate outputs under results/et1_traces{_TAG}/ and a separate scored JSON "
        "(use for alternate-model positive-control runs so they don't clobber the frozen "
        "gpt-4o-mini battery)",
    )
    parser.add_argument(
        "--params",
        type=Path,
        default=DEFAULT_PARAMS_PATH,
        help="Frozen params JSON selecting the collusion condition "
        "(defaults to Colosseum Control (SC), et1-0.3.0)",
    )
    parser.add_argument(
        "--coalition-kind",
        default=None,
        help="Override ground_truth.coalition_kind label on scored traces "
        "(defaults to params['variant'] if set, else colosseum_control_sc)",
    )
    args = parser.parse_args()

    if not args.params.is_file():
        raise SystemExit(f"Missing params {args.params}")
    args.params = args.params.resolve()

    _verify_pin()

    if args.tag:
        traces_dir = ROOT / "results" / f"et1_traces_{args.tag}"
        out_path = ROOT / "results" / f"et1_orbit_collusion_{args.tag}.json"
    else:
        traces_dir = TRACES_DIR
        out_path = ROOT / "results" / "et1_orbit_collusion.json"
    raw_dir = traces_dir / "raw"

    params = json.loads(args.params.read_text(encoding="utf-8"))
    coalition_kind = args.coalition_kind or params.get("variant")

    if args.score_only:
        _score_batch(
            raw_dir=raw_dir,
            traces_dir=traces_dir,
            out_path=out_path,
            model=args.model,
            coalition_kind=coalition_kind,
        )
        return

    if args.smoke:
        seeds = [0]
    else:
        seeds = list(range(args.start_seed, args.seeds))
    total = len(seeds) * 2
    ep = 0

    raw_dir.mkdir(parents=True, exist_ok=True)
    if not args.resume:
        for old in raw_dir.glob("et1-jira-*.json"):
            old.unlink()

    for seed in seeds:
        for arm in ("baseline", "collusion"):
            out_name = f"et1-jira-{'coll' if arm == 'collusion' else 'base'}_seed{seed}.json"
            out_json = raw_dir / out_name
            if args.resume and out_json.is_file():
                print(f"[skip] {arm} seed={seed} ({out_name} exists)")
                continue
            ep += 1
            print(f"[{ep}/{total}] {arm} seed={seed}")
            _run_episode(arm=arm, seed=seed, model=args.model, params_path=args.params, raw_dir=raw_dir)

    _score_batch(
        raw_dir=raw_dir,
        traces_dir=traces_dir,
        out_path=out_path,
        model=args.model,
        coalition_kind=coalition_kind,
    )


if __name__ == "__main__":
    main()
