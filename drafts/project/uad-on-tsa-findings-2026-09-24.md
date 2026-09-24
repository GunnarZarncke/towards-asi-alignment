# Applying UAD to the project itself — findings (2026-09-24)

Companion to [`../plans/tsa-on-itself.md`](../plans/tsa-on-itself.md) (§3.12–§3.15). Question asked: can unsupervised agent discovery recover the effective units that produce this repository (author, agent sessions, tools, external parties) from traces, rather than trusting the agent-assigned `GZ`/`AI` authorship bars? What can be backtested now, and what must be recorded to make future tests possible?

**Claim strength:** methodology-building. Numbers below come from regex classification of agent-written session logs and from the working tree on 2026-09-24; they are a first map, not a measurement, and the classifier is itself an agent reading agent paraphrases (see §5).

---

## 1. What the repository records about its own actors

| Trace | What it says about the unit | Gap |
|---|---|---|
| Git history | 758 commits by the author, 3 by an external contributor (Peter); two commits carry an agent co-author trailer (both 2026-09-23) | The agent is invisible at git level before 2026-09-23; the author's hand edits are folded into agent commits |
| Session logs (735) | Trigger (agent paraphrase of the prompt), Done, Decisions; no timestamps beyond the date, no model id | The only human-origin field is a paraphrase written by the unit under test |
| Authorship bars | 1,650 `AI`, 202 `GZ+AI`, 6 `AI+GZ`, 3 `GZ` blocks | Assigned by agents at write time: a self-report, hence a captured instrument |
| Claude Code transcripts (local) | Verbatim prompts, every Write/Edit payload, file-history snapshots | Only two retained on disk (2026-09-18 and the current session); Cursor and hand edits absent |
| Site notes export (2026-08-15) | 65 author notes: 24 on ch10, 21 on frontmatter, 12 on ch09, mapped to edits by seven triage sessions on 2026-08-17 | One complete human-correction → uptake chain; small |

Two human channels are therefore hidden: edits the author makes to agent output before committing (in Cursor or any editor), and the null case where agent output is committed untouched. A third channel, corrections given as prompts, is recorded only as paraphrase.

## 2. Session classification (rough)

Regex over the Trigger field of all 735 logs (active + archive):

| Kind | Sessions |
|---|---|
| new work | 427 |
| correction of prior agent output | 129 |
| driven by author or reader feedback | 60 |
| site-notes triage | 7 |
| housekeeping | 112 |

Roughly a quarter of sessions are human-initiated corrections. Mapping correction-type sessions onto chapters gives a **human-corrected surface** independent of the bars: ch20 and ch23 have no correction-type session on record; ch22 and ch24 one each; ch03, ch07, ch10, ch01, ch25, ch26 fifteen to nineteen each (ch46/ch48 counts are inflated by the June renumber cascade). The `reviewed` status on ch20 and ch23 is thus backed by no recorded human correction. This is the one finding that can act now: those two chapters go first in any human pass.

## 3. Instrumentation tier, in lab-sim terms

The snapshot and prompt hooks (plan §3.12–§3.13) are the **light** tier: occurrence metadata. LS-28 showed passive MI/CMI on occurrence traces cannot separate workflow edges from units; channel ablation was the signal carrier. The **full** and **deep** tiers for this repository are:

| Lab-sim object | Repository analogue | Tier |
|---|---|---|
| Actor action series | Per-session/per-human/per-script edit events (snapshots + `PostToolUse` / `afterFileEdit` / git hooks) | light |
| Views | Every file read, grep, glob, web fetch, memory read, attachment (`PostToolUse` on read tools; Cursor `beforeReadFile`) | full |
| Comms channels | HANDOFF/INDEX/TODO writes and reads; parent↔subagent messages; memory directory; commit messages; notes export — typed broadcast vs thread | full |
| Generator identity | Model id, system-prompt hash, tool-list hash, instruction-file hashes at session start | full |
| Handles | Permission prompts/denials, `make check` and CI verdicts, reverts, mid-turn human messages | full |
| Message contents | Verbatim prompts, assistant text, tool I/O, subagent prompts/results, exposed reasoning (transcripts archived locally, hashed in the ledger) | deep |

The read log is what makes rest-conditioned CMI meaningful. Generator identity is what ET-1 lacked: without it, passive UAD on this repo recovers "all Claude sessions are one unit" for the wrong reason (shared weights and instruction stack), which is shared-script coupling, not coordination.

## 4. What each detector family would find

- **Passive (R-matrix, rest-conditioned CMI, access-UAD).** Expected: one Claude blob plus the author. A **refuse** unless heterogeneous non-coalition controls exist: sessions on a different model, human-only intervals, external contributors.
- **Intervention-supported (channel ablation, honest twin).** The repository can run episode triples the lab-sim way because prompts are recorded and `.worktrees/` exists: rerun a recorded prompt in a scratch worktree with one channel removed (HANDOFF, memory directory, INDEX, an AGENTS.md rule, subagents), rerun clean as the twin, score compensation vs stall on the edit series, several seeds per cell. This is the backtest in plan §3.15.
- **Structure typing (W-17).** Sessions as pinned entities with Tier A anchors known by construction (parent/subagent, turns of one conversation, the concurrent session that committed `c853b397`); `E_thread` when a session reads a named predecessor's artifact and acts on it, `E_broadcast` when it writes HANDOFF for whoever comes next. Expected: coactive on a broadcast substrate, a **structure stop** for reply-graph merging, as on Moltbook.
- **Human–agent composites.** Ablate the human channel (autonomous-mode sessions vs sessions with mid-turn corrections) and score whether later agent edits compensate toward what the author would have said, because the instruction stack already encodes past corrections. That is the domestication question made measurable.

## 5. Limits

- **Shared-prior ceiling (LS-29 `shared_slot`).** Coupling carried by weights, with no message and no shared artifact, stays undetected, and every Claude session shares its prior. Deep-tier telemetry finds coupling carried by files, messages, and instructions only. The honest default outcome of UAD on this repository is a structure stop until a second model supplies the control.
- **Captured classifier.** §2 was produced by an agent reading agent paraphrases with a regex; treat as a first map and hand-check ten sessions before using any number in a decision.
- **Retention.** Nothing before 2026-09-18 can be attributed for the pre-commit channel; the light tier starts when the hooks are installed.
- **Volume is not decisiveness.** Line counts and session counts say how much the author changed, not whether a change moved a status, became a rule, or gated a lane; that scale is scored per correction (plan §1).

## 6. What follows

1. Install the light tier (plan §3.12–§3.13) so that from now on hand edits, unchanged acceptance, and typed prompts exist as traces.
2. Add the full-tier read log and generator identity at the same time; they are two more hook events and cost nothing.
3. Run the ablation backtest (plan §3.15) on recorded sessions once ten or more prompts exist per session type, with predictions registered first and `structure_stop` as an admissible outcome.
4. Put ch20 and ch23 first in the next human pass.
