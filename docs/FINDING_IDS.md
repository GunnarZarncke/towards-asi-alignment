# Global finding IDs

Every recorded finding or negative result across experiment lines uses a **line-unique prefix**. Do not reuse bare `G-`, `F-`, or `N-` numbers across lines.

| Line | Prefix | Ledger | Notes |
|------|--------|--------|-------|
| Agency-detect (sibling) | `AD-` | sibling `docs/FINDINGS.md` | Methodological precursor; not in-repo |
| Deployment-pipeline-simulator (sibling) | `DP-` | sibling `README.md` / `pipeline_audit/TECHNICAL_NOTE.md` | Pipeline-lab precursor; not in-repo |
| Toy simulation | `TS-` | `experiments/toy-simulation/results/` | Curated appendix entries only today |
| Embedded audit simulation | `ES-` | `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` | Was `N-` |
| Goal-agent simulation | `GA-` | `experiments/goal-agent-simulation/results/FINDINGS.md` | Was `F-` |
| Lab-layer simulation | `LS-` | `experiments/lab-simulation/results/FINDINGS.md` | Was `G-` |
| Graded-capability lab simulation | `GL-` | `experiments/graded-lab-simulation/results/FINDINGS.md` | Was `G-` (collided with lab line) |

**Suffix letters** (e.g. `LS-1a`, `LS-3a`) keep their letter after the prefix.

**Appendix I** (`appendices/appN-experimental-evidence.tex`) cites a curated subset using the **same global IDs as each line's ledger** (not a second numbering scheme). Labels are `\label{finding:<lowercase-prefix-id>}` (e.g. `finding:gl-11`, `finding:ls-32`). Toy-simulation uses `TS-1`…`TS-3` for appendix-only curated entries (no numbered ledger yet).

**Deprecated:** unqualified `G-`, `F-`, and `N-` in older session logs may refer to the pre-2026-07-14 scheme. Resolve by line context or check the ledger above.
