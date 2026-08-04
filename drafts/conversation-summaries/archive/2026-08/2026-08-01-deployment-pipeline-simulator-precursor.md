# 2026-08-01 — Deployment-pipeline-simulator experiment precursor

## Trigger
User asked to list the sibling repo [deployment-pipeline-simulator](https://github.com/GunnarZarncke/deployment-pipeline-simulator) as a methodological precursor to `experiments/`, alongside agency-detect.

## Done
- Indexed the repo across the experiment map: `docs/EXPERIMENTS.md` (build order + section 0′), `metadata/experiments.yml` (line entry, `DP-` prefix, how-to-read, coverage matrix), `experiments/README.md`, `docs/FINDING_IDS.md`.
- Added Appendix I section with curated findings DP-1 / DP-2 in `appendices/appN-experimental-evidence.tex`.
- Regenerated `site/src/data/experiments.json` (7 experiment lines / cards).
- Cross-linked in `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `llms.txt`, `REVIEWING_FOR_AGENTS.md`, `docs/MANUSCRIPT.md`.

## Decisions
- Framed as **pipeline-lab precursor** (secret-loyalty / self-preservation audit under perturbations), distinct from agency-detect's boundary-discovery precursor role.
- Order 0.5 in `experiments.yml`; ledger pointer to sibling `README.md` / `pipeline_audit/TECHNICAL_NOTE.md` (no in-repo FINDINGS.md).

## Open / next
- Harvest DP-1/DP-2 into manuscript chapters if ET-4 or pipeline-opacity prose should cite Appendix I directly.
- Optional: add `**Key finding:**` tags in sibling repo if site auto-extraction should surface headline bullets.

## Commit
`08a86b46` — Index deployment-pipeline-simulator as a sibling experiment precursor.
