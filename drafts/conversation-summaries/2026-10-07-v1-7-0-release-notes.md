# 2026-10-07 — v1.7.0 release notes

kind: new-work
uptake: status

## Trigger
User asked to prepare the release.
Prompts: paraphrase (no prompt id on this turn)

## Done
- content: **`RELEASE_NOTES.md`:** draft **v1.7.0 — 2026-10-07 — Dated bridge predictions** (Appendix H three-way contracts, manuscript since v1.6.0, `Evidence.lean` / MB6, predictions hub, field news, backtest rename and broken witness URLs). Commit line left `_(pending)_`.
- bookkeeping: **`README.md`** and **`docs/MANUSCRIPT.md`** release row → v1.7.0; milestone **Seventh**; predictions row counts 18 catalog + draft 19–21.
- bookkeeping: **`site/.gitignore`:** `release-v1-7-0.md`.
- bookkeeping: `node site/scripts/sync-releases.mjs` → `sync-releases: wrote 8 version cards + hub (generated).` Card summary is the Appendix H paragraph. Generated cards stay gitignored.

## Decisions
- **v1.7.0 = MINOR.** New appendix object (dated bridge predictions) and site layer. No part/chapter renumber.
- Notes cover `v1.6.0..HEAD` (`bdd225290`, 116 commits). Uncommitted tree stays out: workflow `ubuntu-24.04` pins, two reference redirects, a session-log hash line, and untracked `value-detect` / Metaculus export files.
- §3.11 section-AI scores not run. `scripts/audit_section_ai_scores.py` is still an open checklist item in `drafts/plans/tsa-on-itself.md`, so there is no instrument to run before this tag. Exception recorded here, not in the public notes.
- No commit and no tag until the author reviews the notes.

## Open / next
- Author edit of the v1.7.0 section, then the usual cut: commit notes, fill the commit hash, annotated tag `v1.7.0`, `make check` on that cut.
- Push and site deploy are separate (`/updates/` already generates from `RELEASE_NOTES.md` via `sync-releases.mjs`).
- Listing still waits on a host for `ai-safety-claims`. Market 14 can list from its box.

## Key paths
- `RELEASE_NOTES.md`
- `README.md`
- `docs/MANUSCRIPT.md`
- `site/.gitignore`
- `site/scripts/sync-releases.mjs`

## Commits
- `86815d35f` Release v1.7.0 — Crux Predictions notes.
- `c0178fdec` Record v1.7.0 commit hash in RELEASE_NOTES.
- Tag: `v1.7.0` on `c0178fdec`; pushed; GitHub release created.
