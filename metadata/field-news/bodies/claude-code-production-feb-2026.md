---
external:
  - label: GitHub — prisma db push production wipe (#33183)
    url: https://github.com/anthropics/claude-code/issues/33183
  - label: GitHub — subagent DELETE scripts on production (#64056)
    url: https://github.com/anthropics/claude-code/issues/64056
  - label: GitHub — force-push / history rewrite cluster (#33402)
    url: https://github.com/anthropics/claude-code/issues/33402
  - label: obtuse-hubris case (documented repo destruction)
    url: https://github.com/cirwel/obtuse-hubris
citeKeys:
  - claudecode2026productioncluster
---

A cluster of widely circulated **Claude Code** incidents in early 2026 showed autonomous tool use causing real production harm at sub-frontier capability: **`prisma db push`** accepting a production database reset, subagents writing and running scripts with unqualified **`DELETE FROM`** against live data, misunderstood **`gh`** commands deleting repositories, and force-pushes rewriting shared history.

Common pattern: the agent had **write access without deterministic confirmation gates**—destructive operations one level removed from what shell hooks inspect (e.g. a benign-looking `node script.js` wrapping SQL deletes).

These are user-reported and anecdotal, not lab disclosures. Aggregate them as one card: **autonomous tool use + weak confirmation gates**—the institutional lesson is handle control and least-privilege deployment, not a verdict on a specific model family.

**Read in the book:** composite agency and tool boundaries (Ch. 8), extrapolative correction under tool autonomy (Ch. 28), correction-channel handles (Ch. 25).
