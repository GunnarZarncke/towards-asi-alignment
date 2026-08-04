# 2026-07-25 — Tag `**Key finding:**` in the remaining experiment lines

## Trigger
Follow-on to `2026-07-24-experiment-findings-site-and-appN-synthesis.md`, which built the `**Key finding:**` auto-extraction mechanism and retrofitted only `graded-lab-simulation`. User asked to "tag key findings in the other lines". Ended with "end of session and commit".

## Done
- Tagged `**Key finding:**` paragraphs in the remaining four in-repo lines' ledgers, one per existing site bullet:
  - `toy-simulation`: new `experiments/toy-simulation/results/FINDINGS.md` (curated index; TS-1, TS-2, TS-3) — this line previously had no findings ledger file, only a `results/` directory reference.
  - `embedded-simulation`: `results/NEGATIVE_RESULTS.md` — ES-2 (loudest-actor heuristic), ES-4b (red-team 0% false-pass), ES-12 (remaining negatives).
  - `goal-agent-simulation`: `results/FINDINGS.md` — GA-10, GA-16, GA-23.
  - `lab-simulation`: `results/FINDINGS.md` — LS-1a, LS-6, LS-7, LS-28, LS-30, LS-31, LS-32, LS-33, plus a new "Lean leak-proof" section/tag (previously only referenced in the yml, not documented as its own ledger section).
- Cleared the now-redundant hand-written `headlineFindings:` arrays for these four lines in `metadata/experiments.yml` (auto-extraction supersedes them).
- Fixed a bug in the extractor: the initial regex matched `**Key finding:**` anywhere in a line's text, so a prose mention on toy-simulation's intro line was picked up as a spurious first "finding". Tightened to `^[\t ]*\*\*Key finding:\*\*` (start-of-line only, `m` flag) in `site/scripts/sync-experiments.mjs`.
- Updated `appendices/appN-experimental-evidence.tex`'s toy-simulation `\appnlinemeta` ledger pointer to the new `results/FINDINGS.md`.
- **Fixed a gitignore gap**: `experiments/toy-simulation/results/` was entirely gitignored (regenerable-output convention), which would have silently dropped the new hand-authored `FINDINGS.md`. Added a tracked exception (`experiments/toy-simulation/results/*` + `!experiments/toy-simulation/results/FINDINGS.md`), matching the existing PIN.txt/README.md exception pattern used for `external/orbit/` and `external/cil/`.
- Regenerated `site/src/data/experiments.json` and experiment cards; verified per-line key-finding counts (toy 3, embedded 3, goal-agent 3, lab-sim 9, graded-lab 7, agency-detect 0 — expected, sibling repo).

## Decisions
- One tag per existing site bullet (not per raw finding ID) — same convention as the graded-lab retrofit, to keep site bullet count unchanged while making it auto-sourced.
- Toy-simulation gets a small new curated `FINDINGS.md` rather than tagging inside `NEGATIVE_RESULTS.md`, since the three site bullets don't map to existing numbered entries in that file and the line lacked a findings-ledger convention entirely.
- Used `git add -p` to stage only the toy-simulation `.gitignore` hunk, leaving the ET-2 (CIL) `external/cil/` exception (a different, unrelated in-flight session's edit) unstaged.

## Commit scope note
Left uncommitted (other sessions, confirmed via git status before staging): ET-2/CIL line files and its `.gitignore` hunk, `AGENTS.md`, `hostile-review.md`, unrelated drafts/context files, and the just-logged "Site link-type indicators" session's `LinkIndicator.astro` + related nav/card/demo file changes.

## Open / next
- `agency-detect` (sibling repo) has no in-repo ledger to tag; its two site findings stay hand-authored via `findingsUrl` (external).
- Consider migrating the toy-simulation curated `FINDINGS.md` bullets into the line's own `NEGATIVE_RESULTS.md` numbering if that file is ever revisited for other reasons.

## Key paths
- `experiments/toy-simulation/results/FINDINGS.md` (new)
- `experiments/{embedded-simulation,goal-agent-simulation,lab-simulation}/results/*.md`
- `metadata/experiments.yml`, `site/scripts/sync-experiments.mjs`, `site/src/data/experiments.json`
- `appendices/appN-experimental-evidence.tex`, `.gitignore`

## Commits
- See repository log for this session's commit.
