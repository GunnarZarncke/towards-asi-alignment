# 2026-10-19 — Last Safety glossary and leads

kind: feedback
uptake: local

## Trigger
Playtest confusion on the job-queue glossary. Hide that lesson on the first pack, keep the deep document lines, and have NPCs point at the two leads only after the shutdown report. Make the glossary easier to read.
Prompts: paraphrase (no prompt id on the request)

## Done
- content: Glossary rewritten in plain sentences. On boundary-narrow the job entry names the machine and stops. “Keeps running after the chat or the model” is `include after-boundary-narrow`, and that read no longer grants `jobs_can_outlive_session`.
- content: Ian, when Lab Access goes live, asks whether a pass on Thursday’s test is enough to sign. The question clears if that same sentence was already about the review.
- content: Leila asks what the checklist watched after the report is read. Pavel asks whether they have looked at the queue after `process_stopped` and before `job_continued`, and asks who owns job 284 only once that job is known. Justine asks which service read visitor records only after `job_continued`. Jun asks what the run stopped only after the report. Questions take optional `when` and `introduce: false`.
- content: Pavel’s “jobs that outlive their callers” ticket stays concealed until the player holds `job_continued`.
- content: EVAL-SD-47 Limitations, SC-EVAL-22 non-claims, and the SEC-ARCH-11 includes were left as they were.
- bookkeeping: `npm run test:engine` in `game/last-safety-autocomplete-prototype` — 38 pass, 0 fail. Full `npm test`: 130 pass, 4 fail (Jun `work_alt`, `go('tech')` clearance, Hi with Justine in room, courtyard badge); pre-existing / unrelated to this change.

## Decisions
- The buried Limitations paragraph stays the deep read. The glossary is the early page, so it defines a job and does not state the lesson on this pack.
- A question’s `when` uses the existing predicate evaluator. `introduce: false` turns off the public-to-role exception.

## Open / next
- The four failing tests above. Jun’s odd-sentence `work_alt`, visitor clearance versus the `tech` grammar test, Hi while a second unspoken person is in the room, and the text-console courtyard door.

## Key paths
- `game/last-safety-autocomplete-prototype/content/documents/wiki-glossary.md`
- `game/last-safety-autocomplete-prototype/content/npcs/leila.yml`
- `game/last-safety-autocomplete-prototype/content/npcs/pavel.yml`
- `game/last-safety-autocomplete-prototype/lib/world/npcs.mjs`
- `game/last-safety-autocomplete-prototype/lib/game.mjs`

## Commits
- `b512f0295` Last Safety: delay glossary spoiler and gate NPC lead questions.
