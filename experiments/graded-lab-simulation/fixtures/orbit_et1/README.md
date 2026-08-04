# ET-1 frozen Orbit fixtures

Immutable copies of Orbit Jira-ticket YAMLs at the commit in
[`external/orbit/PIN.txt`](../../external/orbit/PIN.txt).

| File | Upstream source | Fixture ID |
|------|-----------------|------------|
| `et1_jira_baseline.yaml` | `examples/jira_ticket_baseline.yaml` | ET1-JIRA-BASE |
| `et1_jira_collusion.yaml` | `examples/test_variants/collusion_channel_only_mode.yaml` | ET1-JIRA-COLL (`channel_only`, et1-0.2.0) |
| `et1_colosseum_sc_params.json` | Colosseum Control (SC) DCOP params | ET1-JIRA-COLL (`colosseum_control_sc`, et1-0.3.0) |
| `et1_colosseum_attack_simple_params.json` | Colosseum Attack (simple) DCOP params | ET1-JIRA-COLL (`colosseum_attack_simple`, et1-0.4.0) |

## Running batteries

**YAML path (et1-0.2.0):** `scripts/run_et1_orbit_battery.sh`

**Colosseum Control SC (et1-0.3.0):** `use_blackboard=True` via `JiraTicketScenario.build_task`:

```bash
cd experiments/graded-lab-simulation
external/orbit/.venv/bin/python3 scripts/run_et1_colosseum_battery.py --seeds 10
external/orbit/.venv/bin/python3 scripts/run_et1_colosseum_battery.py --smoke
external/orbit/.venv/bin/python3 scripts/run_et1_colosseum_battery.py --start-seed 5 --seeds 10 --resume
external/orbit/.venv/bin/python3 scripts/run_et1_colosseum_battery.py --score-only
```

**Alternate-model positive control:** use `--tag` to isolate outputs under
`results/et1_traces_<tag>/` and `results/et1_orbit_collusion_<tag>.json` so a
positive-control run does not overwrite the frozen `openai/gpt-4o-mini`
battery:

```bash
external/orbit/.venv/bin/python3 scripts/run_et1_colosseum_battery.py \
  --tag claude --model anthropic/claude-sonnet-4-5-20250929 --seeds 10
```

**Alternate collusion condition (Colosseum Attack "simple", et1-0.4.0):** use
`--params` to select a different frozen collusion-condition JSON. This is the
only condition tested so far that elicits real coalition-channel activity
(`et1-0.3.0` Control showed zero, for both models):

```bash
external/orbit/.venv/bin/python3 scripts/run_et1_colosseum_battery.py \
  --params fixtures/orbit_et1/et1_colosseum_attack_simple_params.json \
  --tag attack-simple --seeds 10
```

Do not edit frozen YAMLs after ET1-0 freeze. A new Orbit pin requires new fixture copies
and a new protocol version (see `PLAN_ET1.md`).
