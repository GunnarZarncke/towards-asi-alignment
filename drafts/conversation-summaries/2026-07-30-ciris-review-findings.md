# 2026-07-30 — CIRIS review findings + key counterexample task

## Trigger
Investigate CIRIS (`~/repos/ciris`) vs this project’s alignment problems; clarify ASI stance; identify challenge surfaces; write separate findings for new results; make the composite/boundary_decouple counterexample a key task for Eric Moore.

## Done
- Read CIRIS summary material, five-point battery, Accord 1.3-RC2 / Constitution, Verify/Lens/Agent stance docs.
- Wrote four new CIRIS review findings (plus prior orientation/battery already present):
  - stance & promises (not “prevent ASI”; sub-ASI validated; candidate ASI protocol)
  - MB4 as main challenge/test surface
  - named-identity bet (admission OK; alignment unit fails under boundary discovery)
  - **KEY TASK** charter: CIRIS-shaped Verify+Lens green / WA-blind composite counterexample
- Updated `~/repos/ciris/review/findings/README.md` and `~/repos/ciris/AGENTS.md` key-task pointer.
- Linked key task from `experiments/TODO.md`.

## Decisions
- CIRIS public constitution does **not** say “ASI must be prevented”; scope is candidate ASI alignment with sub-ASI validated today.
- Primary *code* challenge surface now: **MB4** (WA/deferral/shutdown causal bite + capture).
- Sharpest *Eric-facing* boundary ask: named-identity bet vs composite/boundary_decouple (key task).
- Findings live in CIRIS review workspace, not upstream CIRISAI clones.

## Open / next
- Key task: pick scenario C1–C4; narrative mock (A) then CIRISAgent integration test (B); Eric one-pager.
- Optional later drills: H3ERE ThoughtProcessor, Lens ratchet, compliance D-stubs, Rust Verify vectors.
- Interrupted earlier write of stance finding completed in this pass.

## Key paths
- `~/repos/ciris/review/findings/` (all findings; start at README + key-task file)
- `experiments/TODO.md` — key cross-project task link
- Sibling cards: MB1, MB4, composite-agency, boundary-discovery

## Commits
- (none requested)
