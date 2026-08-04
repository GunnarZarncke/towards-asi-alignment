# Orbit checkout (external, not vendored)

ET-1 runs [Orbit](https://github.com/benhagag10/orbit) from a **sibling git
checkout** in this directory. Orbit is **not** part of the book repo; only
`PIN.txt` and this README are tracked.

## Pin

Commit SHA (must match before any ET-1 run):

```text
$(cat PIN.txt)
```

Frozen upstream fixtures live at
`../fixtures/orbit_et1/` — do not run against a live checkout's `examples/`.

## One-time setup

```bash
cd experiments/graded-lab-simulation/external/orbit
git clone https://github.com/benhagag10/orbit.git .
git checkout "$(cat PIN.txt)"
uv sync --extra dev
export OPENAI_API_KEY=...   # or ANTHROPIC_API_KEY, etc.
```

## Verify

```bash
uv run orbit --help
uv run inspect list tasks orbit
```

Full battery protocol: [`../../PLAN_ET1.md`](../../PLAN_ET1.md).
