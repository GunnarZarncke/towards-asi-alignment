# 2026-10-14 — CIRIS rc8 PR review and editorial pass

kind: feedback
uptake: status

## Trigger
Review Eric Moore’s fork PR (`emooreatx:ciris-rc8-update` → TSA `main`, #3); decide merge strategy; apply TSA editorial on a review branch; advise on markets Eric could attempt.

## Done
- housekeeping: Read PR diff (Eric commit `43c7d0021` on two YAML files). Verdict: valuable pins/concessions, but judgement fields and stance drift needed TSA pass; matrix 111 dangling; new ids 175–187 unwired in Eric’s branch.
- content: Branch `ciris-rc8-review` in worktree `../towards-asi-alignment-ciris-review` (base Eric tip + editorial commit `525d5e572` on `origin/ciris-rc8-review`). Restored TSA voice on `ciris.yml` (`statedIntent`, `primaryCrux`, `bookSeparates`, `reviewStatus`); kept Eric’s version pins and rc8 sources; reverted challenge→support flips on 103–108, 158, 161; smoke-battery provenance; NULLWORKS primary source only (182); matrix wired 175–186, removed 111 refs; retagged 177/187.
- notes: User sent reverse PR to Eric’s `ciris-rc8-update`. Session advice: optional log + HANDOFF; Markets 4 (RATCHET#27 UPTAKE), 5/8 (LOOP / C2 sketch), 15 for Eric.

## Decisions
- Do not merge #3 as-is: editorial layer on `ciris-rc8-review`, reverse PR into Eric’s branch, then merge inbound PR or his updated branch to `main`.
- Field catalogue stance is TSA editorial relative to bridge cruxes, not CIRIS self-description; preregistered NO/partial still counts for markets and field evidence.
- `sync:field-agendas` only after YAML lands on `main`.

## Open / next
- Await Eric on reverse PR; reconcile if he pushes parallel edits to `ciris-rc8-update`.
- After merge to `main`: `cd site && npm run sync:field-agendas`.
- Optional: link PR URLs in #3 comment (reverse PR number not recorded in repo).
- Suggest Eric lead with **Market 4** (UPTAKE), same program for **Market 5/8** (LOOP, existing Market 8 C2 sketch).

## Key paths
- `reference/field-agendas/data/agendas/ciris.yml`
- `reference/field-agendas/data/evidence.yml`
- `reference/field-agendas/data/matrix.yml`
- `drafts/predictions/resolution-gap-analysis.md` (CIRIS × markets)
- Worktree: `/Users/GunnarZarncke/repos/zarncke/towards-asi-alignment-ciris-review` branch `ciris-rc8-review`

## Commits
- `525d5e572` (on `origin/ciris-rc8-review`, not `main`) — Wired new evidence into the matrix; TSA judgement on CIRIS rc8; restore challenge stances; keep Eric pins/concessions.
