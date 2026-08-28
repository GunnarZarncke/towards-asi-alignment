# Experiments

Reproducible research artifacts for empirical sanity checks on the book's bridge
cruxes. Each line lives in its own subfolder with a **self-contained README**
(simulation overview, package layout, entry points) and a **CHANGELOG** (version
or phase milestones — not duplicated in README intros).

Narrative map: [`docs/EXPERIMENTS.md`](../docs/EXPERIMENTS.md). **Methodology:**
[`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md). Structured index
(companion site): [`metadata/experiments.yml`](../metadata/experiments.yml).
Open tasks: [`TODO.md`](TODO.md).

## Build order

| Order | Line | README | Changelog |
|------:|------|--------|-----------|
| 1 | [`toy-simulation/`](toy-simulation/) | Multiresolution alignment + correction capture | [`CHANGELOG.md`](toy-simulation/CHANGELOG.md) |
| 2 | [`embedded-simulation/`](embedded-simulation/) | Embedded auditor on VFS + isolates | [`CHANGELOG.md`](embedded-simulation/CHANGELOG.md) |
| 3 | [`goal-agent-simulation/`](goal-agent-simulation/) | Emergent goal-driven agents | [`CHANGELOG.md`](goal-agent-simulation/CHANGELOG.md) |
| 4 | [`lab-simulation/`](lab-simulation/) | Pipeline lab + subprocess isolates | [`CHANGELOG.md`](lab-simulation/CHANGELOG.md) |
| 5 | [`graded-lab-simulation/`](graded-lab-simulation/) | Graded substrate, BIQ/EAI, v4 rigs (**active**) | [`CHANGELOG.md`](graded-lab-simulation/CHANGELOG.md) |

Sibling precursors (not in-repo): [agency-detect](https://github.com/GunnarZarncke/agency-detect), [deployment-pipeline-simulator](https://github.com/GunnarZarncke/deployment-pipeline-simulator).

**Witness annex** (not line 6): [`witness/`](witness/) — frozen host protocols and `W-` findings. Do not treat as a new simulation substrate.

Unindexed local trees `value-detect-v1-master/` and `value-detect-v2-master/` are unzipped agency-detect companions (directional value signature). They are **not** lines 1–5 and are not in `metadata/experiments.yml`. Do not treat them as the empirical map until indexed.

## README convention

Each line README starts with: **what the simulation is** (readable without the
manuscript), **three-plane / package structure**, then **quick start** and
**entry-point tables**. Historical phase/status prose and `CODE_VERSION` trails
belong in that line's `CHANGELOG.md` and in `results/FINDINGS.md` (or
`NEGATIVE_RESULTS.md` for embedded).
