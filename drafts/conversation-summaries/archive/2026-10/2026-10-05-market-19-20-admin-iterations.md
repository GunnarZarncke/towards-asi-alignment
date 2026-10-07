# 2026-10-05: Markets 19 and 20, three Metaculus-admin rounds

kind: correction
uptake: local

## Trigger
The user asked for more prose and structure outside the questions on what the placeholders are and how to fill them, and for boxes self-contained enough for a Metaculus admin to score. The method: post the questions with hypothetical fills to a subagent in a Metaculus-admin role, evaluate its response, and tune over three iterations.
Prompts: paraphrase

## Done
- content: Markets 19 and 20 now have prose before each box: what a tournament or challenge is, who fills the brackets and when, a "How to fill each bracket" list with examples, and what the protocol fixes without brackets. Market 19 gained a `[registration window]` bracket.
- content: Both boxes were restructured:
  - an "In plain terms" lead;
  - a short Question line plus a Parameters field;
  - definitions of independence (per member, 24 months, open-source work counted only for a shared commit or pull request) and signed statements;
  - a bounded record check (only records cited in the question comments);
  - the deployment-class boundary.
- content: Market 19's conditions were split:
  - tournament-wide conditions, where one failure means OTHER;
  - per-stack conditions, where a failure disqualifies only that stack.
  The box also now states:
  - a data deadline;
  - a strict no-amendment rule;
  - unit acceptance rules per class;
  - Clopper-Pearson confidence \(1-0.05/k\), with k counting every registered stack and a worked example;
  - a required summary table, cross-checked against per-case data, which wins on disagreement.
- content: Market 20 now requires:
  - at least two red teams;
  - an author list in the challenge document;
  - a mandatory barred-targets list, with bars allowed only outside the deployment class;
  - a find list that matches the logs;
  - per-attempt presence checks with no reruns;
  - an unchanged stack.
  Its outcome-check wording is no longer circular.
- content: `site/scripts/lib/tex-convert.mjs` now parses braced description labels such as `\item[{\texttt{[x]}}]` and renders them as `<code>`. Before this, every bracket label in Appendix P showed as `{“{[x</dt><dd>]`.
- bookkeeping: `drafts/predictions/metaculus-admin-trials/` holds the renderer, each round's posting, the scenario table with intended answers fixed before each round, and per-round dispositions.
- bookkeeping: `npm run sync:predictions` wrote "20 cards and predictions.json". `npm run sync:chapters` wrote "56 book pages". `astro sync` reported "Generated". `rg -c "<dt><code>\[" site/src/content/book/appP.md` returned 11.

## Decisions
- Scenario match against my pre-fixed intended answers: round 1, 4 of 9; round 2, 11 of 12; round 3, 12 of 12. Each round used a fresh subagent, which is one instrument. This does not certify the boxes, and round-3 edits were not re-reviewed.
- All three admins asked for Market 20 to be YES/NO. It stays YES/OTHER, per the user's earlier choice; flagged for the user.
- Bars on attack targets are allowed only outside the deployment class. No blanket legal carve-out.
- Any amendment to the protocol, even a typo fix, fails Market 19. Errata go in a new version and a new question.
- The 24-month independence window is a new input, chosen before any scenario was scored.

## Later the same session (contract field boxes)

- content: Four-environment contract for Markets 19–20: `predictionbox` (strong orange front matter), `predictionbackground`, `predictionresolution`, `predictionfineprint` (lighter `mdframed` boxes; splittable on TeX Live basic). Authbar closes before the contract block and reopens for post-contract prose.
- content: Site callouts and book-page CSS for the three lighter fields; `render_posting.py` reads all four environments.
- bookkeeping: `./build.sh` reported `Latexmk: All targets (book.pdf) are up-to-date` and `Built dist/pdf/towards-superintelligence-alignment.pdf` (109 `non splittable` warnings remain from legacy single-box markets inside authbars).

## Earlier the same session

The prediction boxes were split so a box taller than one page would not hang the PDF build. That split was the wrong structure: Metaculus has no character cap that requires it. The writing guide's binding limit is about 15 minutes of admin effort. Template with the create-form fields, database lengths, and TeX/site options: `drafts/predictions/metaculus-question-template.md`.

## Open / next
- The admins estimate 45–75 minutes to resolve Market 19 and 30–45 minutes for Market 20. A machine-checkable summary file is the lever.
- Market 20 YES/NO versus YES/OTHER: the user's call.
- The κ clash is unchanged.

## Notes
- A Python shell edit to the appendix in the previous turn ran before `declare_edits.py`. It was declared immediately after ("declared 1 pattern(s) for cursor/*").

## Key paths
- `appendices/appP-bridge-predictions.tex` (`sec:appp-m19`, `sec:appp-m20`)
- `drafts/predictions/metaculus-admin-trials/README.md`
- `site/scripts/lib/tex-convert.mjs` (`convertDescription`)

## Commits
- none
