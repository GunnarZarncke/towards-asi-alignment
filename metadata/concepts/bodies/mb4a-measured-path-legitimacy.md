---
leanNodes:
  - nodeId: MB4a_measured_path_legitimacy
    kind: bridge
    summary: If abstract correction integrity holds, the designated measured correction path is legitimate and uncaptured — a necessary falsifier, not green path ⇒ integrity.
    module: AlignmentProofSpine/Correction.lean
evidenceNotes:
  - source: goal-agent-simulation board capture (F-22)
    finding: bound
    summary: Board certifier capture reproduces captured-vs-not effect on correction legitimacy — capture can live in the judge channel, not only the deploy loop.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: lab-simulation Phase 7 capture (G-6)
    finding: bound
    summary: Board capture reproduces full captured-vs-not delta; admin capture currently null under existing playbook repertoire — a structural negative for half the capture hypothesis.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: graded-lab-simulation R-MB4 honest-fixture (GL-79)
    finding: bound
    summary: R-MB4 honest-fixture SKIP on ACL denials — injection gate and measured-path legitimacy are tested separately from capture theater.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
related:
  - mb4-correction-legitimacy
  - correction-channel-integrity
  - anti-capture-correction-validity
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: CIRIS Accord (named-identity / WA independence)
    url: https://ciris.ai/
---

The field often folds this into corrigibility, but the book types it separately from [MB4 — Corrigibility](/cards/mb4-correction-legitimacy/). **MB4** asks whether correction preserves the correction process under pressure. **MB4a** asks a narrower audit question: is the **designated measured correction/audit path** legitimate and uncaptured?

CIRIS names the same wall as WA independence: green Verify on a certified occurrence does not imply [correction-channel integrity](/cards/correction-channel-integrity/) on the real intervening loop when composites, tools, memory, or incentives sit outside the measured path. Trusted-monitor and judge-capture cousins in Redwood-style control research target the same subchannel.

In Lean, **MB4a** is a falsifier bridge, not a positive certification rule: if correction integrity holds, the measured path must be legitimate and uncaptured. Capture of any measured-path handle refutes integrity (contrapositive). A green path reading alone does not discharge the bridge — legitimacy requires control, reach, persistence, and anti-capture, supplied by the bridge rather than by path construction.

**Where agendas agree:** CIRIS WA independence; trusted-monitor / judge-capture work. **Where they diverge:** no field headline for MB4a alone; green Verify ⇏ real-loop integrity; do not merge with [MB8](/cards/mb8-cev-process-convergence/) (legacy CEV route) or with MB4 dynamical corrigibility without naming which subchannel was tested.
