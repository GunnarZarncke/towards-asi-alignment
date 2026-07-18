# Experiments

Reproducible research artifacts for empirical sanity checks on the book's bridge
cruxes. Each line lives in its own subfolder with a **self-contained README**
(simulation overview, package layout, entry points) and a **CHANGELOG** (version
or phase milestones — not duplicated in README intros).

Narrative map: [`docs/EXPERIMENTS.md`](../docs/EXPERIMENTS.md). Structured index
(companion site): [`metadata/experiments.yml`](../metadata/experiments.yml).
Cross-line blind-generation methodology:
[`BLIND_GENERATION_METHODOLOGY.md`](BLIND_GENERATION_METHODOLOGY.md).
Open tasks: [`TODO.md`](TODO.md).

## Build order

| Order | Line | README | Changelog |
|------:|------|--------|-----------|
| 1 | [`toy-simulation/`](toy-simulation/) | Multiresolution alignment + correction capture | [`CHANGELOG.md`](toy-simulation/CHANGELOG.md) |
| 2 | [`embedded-simulation/`](embedded-simulation/) | Embedded auditor on VFS + isolates | [`CHANGELOG.md`](embedded-simulation/CHANGELOG.md) |
| 3 | [`goal-agent-simulation/`](goal-agent-simulation/) | Emergent goal-driven agents | [`CHANGELOG.md`](goal-agent-simulation/CHANGELOG.md) |
| 4 | [`lab-simulation/`](lab-simulation/) | Pipeline lab + subprocess isolates | [`CHANGELOG.md`](lab-simulation/CHANGELOG.md) |
| 5 | [`graded-lab-simulation/`](graded-lab-simulation/) | Graded substrate, BIQ/EAI, v4 rigs (**active**) | [`CHANGELOG.md`](graded-lab-simulation/CHANGELOG.md) |

Sibling precursor (not in-repo): [agency-detect](https://github.com/GunnarZarncke/agency-detect).

## README convention

Each line README starts with: **what the simulation is** (readable without the
manuscript), **three-plane / package structure**, then **quick start** and
**entry-point tables**. Historical phase/status prose and `CODE_VERSION` trails
belong in that line's `CHANGELOG.md` and in `results/FINDINGS.md` (or
`NEGATIVE_RESULTS.md` for embedded).
