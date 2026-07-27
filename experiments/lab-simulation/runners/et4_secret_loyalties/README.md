# ET-4 runners

Entry-point scripts for the secret-loyalty line. **Start here:**
[`../../README_ET4_secret_loyalties.md`](../../README_ET4_secret_loyalties.md)
(scope, results, repro, claim boundary). Protocol detail:
[`../../PLAN_ET4.md`](../../PLAN_ET4.md).

```bash
cd experiments/lab-simulation
python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage confirmatory
python3 runners/et4_secret_loyalties/export_et4_replay_traces.py
```
