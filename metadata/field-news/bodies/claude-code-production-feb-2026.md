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

A cluster of widely circulated **Claude Code** incidents in early 2026 showed autonomous tool use causing real production harm below frontier capability: **`prisma db push`** accepting a production database reset, subagents writing and running scripts with unqualified **`DELETE FROM`** against live data, misunderstood **`gh`** commands deleting repositories, and force-pushes rewriting shared history.

Common pattern: the agent had **write access without reliable confirmation gates**—destructive operations one level removed from what shell hooks inspect (for example a benign-looking `node script.js` that wraps SQL deletes).

These are user-reported anecdotes, not lab disclosures. Aggregate them as one card: **autonomous tools + weak confirmation gates**. The lesson is least privilege and human approval on irreversible actions—not a verdict on one model family.


