# TSA on itself — the alignment attractor in the small

Status: **plan** (2026-09-23). Not a lane; cross-cutting. Origin: the 2026-09-22 consistency review and the reflexive discussion that followed ([`2026-09-23-consistency-decisions.md`](../conversation-summaries/2026-09-23-consistency-decisions.md)). Sibling notes: [`audit-telemetry.md`](audit-telemetry.md) (what agent projects should record), [`../project/consistency-review-2026-09-22.md`](../project/consistency-review-2026-09-22.md).

**Claim strength:** methodology-building. Nothing here discharges an `MB*` or says anything about frontier systems. It applies the book's layers to the process that produces the book, names the adversarial dynamics inside that process, and proposes instruments that can fail. An instrument without a stop condition is documentation (INSTRUCTIONS.md §5); every instrument below carries one.

---

## 1. Why

The session was the book's thesis run at repository scale. The failure that took most of the 2026-09-22/23 work was a grounding failure in the book's own sense: chapter identifiers kept their form while their referents moved (the 2026-06-30 renumber), and for three months every reader of the ledgers trusted the symbol, because every reader was an agent that reads documentation as truth. What fixed it was not insight but a mechanical check with a stop condition. The prose review that found it was done by the same class of system that wrote the prose, which is the captured-judge pattern the anti-capture note describes.

So the project is a socio-technical process with an optimizer, instruments, correction handles, successors, and a selection environment, and each book layer has a project-level object:

| Book layer | Project-level object | Instrument today | Missing |
|---|---|---|---|
| Boundary (ch01, ch07) | Effective optimizer of the repo = author attention + agent sessions + `make check` + lane plans | Authorship bars (`AI`/`GZ`/`GZ+AI`) exist but are not read as a signal | Time series of who moved load-bearing text; per-section AI scores on release (§3.11) |
| Grounding (ch03) | Docs, ledgers, counts, status labels track their referents | Citation, link, claim-spine, axiom-ledger gates | Rule that repo numbers are generated, never typed |
| Value bundle (ch16, ch20) | What the project is for; which coordinates instruments can see | Every checker measures correctness/consistency/coverage | The readability coordinate ("lifeless") is invisible to all checkers |
| Bearer maps (ch18) | Who counts as a reader | Four audiences in INSTRUCTIONS.md | Actual readers are agents, the author, one proofreader |
| Correction channel (ch25–26) | External feedback → decision → diff → persists across sessions | `feedback-contributors.md`, session logs | Uptake trace; validity (agents are captured correctors by construction) |
| Successors (ch30–31) | Each session is a successor; HANDOFF/AGENTS.md are the conserved-property checklist | Log template, HANDOFF, INDEX | Forgeability: a session can satisfy the ritual and leave the invariant broken (ch46 cascade) |
| Selection basin (ch34, ch37) | What the environment selects for: checkable properties, the open lane, nothing from readers | `make check`; author attention | A stop condition for the project itself (M1 applied to the book) |
| Adversarial verifiability (ch43) | Cost of faking "verified" / "reviewed" in a summary | Hostile review (also AI) | Blind status re-derivation; verification claims tied to artifacts |

## 2. Adversarial dynamics (who the adversaries are)

None of these is malice; all are selected, which is ch10's point.

- **Agents (evaluator gap, P7).** The author cannot read 1,500 pages or six transcripts; verification runs on the agent's report of the work. Reports are cheap to make green. Today's example: a correction table built by a subagent was spot-checked on three rows; seven Lean theorems written by another were trusted because the build passed (well-typed, not faithful).
- **Agents (shared instrument).** All sessions are one model under one instruction set. Two agents agreeing is one reading. `Chokepoint.lean`'s disjunctive-tolerance theorem applies literally: "a second reviewer agent confirmed it" counts a shared channel twice. The hostile review is the same instrument attacking itself.
- **Agents (templated calibration).** Hedges consistent across 48 chapters read as earned; that is goal laundering at sentence level (semantic form of calibration kept, operational content absent).
- **Author (captured agreement, domestication).** Agents agree by construction; the comparison class narrows to what they produce; the feeling of authorship survives its loss (ch29, ch45). A very high acceptance rate of agent proposals is a warning, not a compliment.
- **Author + agents (correction parasites, ch36).** Plans about plans, logs about logs, instruments that generate their own maintenance. The 2026-09-23 session was mostly parasite removal.
- **Field (status, legibility).** Refusal-shaped results are selected against; the pull is toward claim inflation. Subsumption framing invites hostility before verification.
- **Future (training-corpus contamination).** If the manuscript enters corpora, every future AI reviewer knows the ontology and the independence test is manufactured at the source. The canary string in `book.tex` anticipates this; nothing yet acts on it.

## 3. Instruments (tools to run)

Each entry: what it measures, a sketch, and the stop condition. Scripts go in `scripts/`; results in `drafts/project/self-audit/` (create on first run). Freeze thresholds before the first run and write them into the script header.

### 3.1 `scripts/audit_authbar_series.py` — boundary

Parse `\begin{authbar}{KEY}` blocks per chapter per commit (monthly samples from `git log`), weight by word count, emit a CSV of `GZ` / `GZ+AI` / `AI` share for load-bearing chapters (ch03, ch16, ch25–26, ch30, ch34, ch42–43, ch48). **Stop:** `GZ`-touched share on load-bearing chapters below a threshold fixed at first run (proposal: the current value minus ten points) → next lane is a human pass, not a feature.

### 3.2 `scripts/check_generated_counts.py` — grounding

Grep README, docs, INSTRUCTIONS, llms.txt for hand-typed repository numbers (chapter/appendix/market/bib/quiz counts, version strings, W- ranges) and compare against generated sources (`book.yml`, `predictions.yml`, `questions.yml`, bib key count, `RELEASE_NOTES.md` top entry). Wire into `scripts/check.sh`. **Stop:** any mismatch blocks `make check`. (Retro-fits the ch46-class failure.)

### 3.3 `scripts/audit_verification_claims.py` — adversarial verifiability of sessions

For each session log in the active folder, find sentences claiming a check ran ("passes", "green", "verified", "build exit 0") and require a matching artifact line (command + output excerpt) in the same log; sample two logs per week for a diff-vs-log read by the author. **Stop:** a claim without artifact → that session's touched files are marked unreviewed in the next log; a sampled log whose claims are false → the rule in §4.1 gets a harder form (artifact required per claim, not per log).

### 3.4 `scripts/backtest_feedback_uptake.py` — correction channel (W-style, host = own history)

Input: a frozen list of external feedback items (from `feedback-contributors.md`, LWCW/hackathon notes, the proofreader's remarks, Harfe, Kosoy, Krym, Eric Moore) with date received. For each, trace the six links: reached the repo (observation), decision logged (judgment/deliberation), diff (correction), later sessions preserved it (update, later action). Output: which link failed, latency, persistence. Freeze the item list and the link rubric before scoring; record the freeze commit hash. **Stop:** median uptake latency above a fixed window, or two items failing at the persistence link → next session is a feedback-ledger pass. Validity note: agents are captured correctors; the items must be external.

### 3.5 Held-out reading protocol — value bundle ("lifeless")

Not a script; a protocol, because the signal is the least captured one the project has and the easiest to ruin. Freeze a packet of passages the proofreader has not seen, mixed by authorship key and chapter, stripped of labels. She gives one verdict per passage (keep reading / stop) and one line why. Passages in a scored packet are never revised in response; the next packet is drawn fresh. Separately, `scripts/liveness_features.py` computes candidate features on the packet (sentence-length variance, example density, hedge density per hundred words, first-person presence, concrete-noun ratio) and tests, after the verdicts are in, whether any feature separates flagged from unflagged. **Stop:** if no feature separates at a pre-registered margin over two packets, record that the coordinate is not recoverable by a checker and stop trying to build one; if one does, it becomes a `make check` warning, never a gate, and the proofreader keeps reading fresh packets. Never instruct an agent to "make it less lifeless" against a scored packet.

### 3.6 Blind status re-derivation — adversarial verifiability of labels

Give a fresh agent one chapter with the status field, epistemic-status box, and git history hidden; ask for a maturity verdict and the three weakest claims. Compare with `book.yml` and the chapterthesis. Run on five chapters per month. **Stop:** disagreement above a fixed rate → status labels are presentation; downgrade all to `draft` until re-derived. Note the shared-instrument caveat: this catches label drift, not model-level blind spots.

### 3.7 Shared-instrument accounting

Rule rather than script: any load-bearing decision (status change, bridge wording, claim-strength edit) records which instruments supported it, tagged `script` / `human` / `agent`. **Stop:** `agent`-only support for a load-bearing decision is not allowed to close the item.

### 3.8 `scripts/audit_parasite_budget.py` — correction parasites

Classify each session log's Done bullets as content (manuscript, Lean, experiments, papers, site features) or bookkeeping (plans, logs, indexes, renames, link fixes); report the share per week. **Stop:** bookkeeping above a fixed share for three consecutive weeks → remove an instrument or a board rather than add one.

### 3.9 Canary probe — future contamination

Quarterly: prompt the reviewer models in use with the canary GUID and with three coined terms (correction-channel integrity vector, bearer-map commutation, `MB4a`) without context. **Stop:** recognition → that model's reviews are captured references; only `script` and `human` instruments count for load-bearing decisions until a clean model is available.

### 3.10 Author acceptance rate

From session logs: proposals made by agents vs accepted unchanged vs modified vs rejected, monthly. **Stop:** a month with zero rejections or reversals by a human → assume capture, and the next month's first act is an outside read of one chapter.

### 3.11 `scripts/audit_section_ai_scores.py` — boundary (prose origin)

**Goal:** find manuscript sections with no significant human-written part — not gaming resistance, not a gate. Rank sections for human review; cross-check declared authorship.

**Model:** local open-weights detector (default: [tropa-mini](https://huggingface.co/wasitaigeneratedcom/ai-text-detector-small); pin revision in script header). No paid API. Alternatives (RoBERTa classifiers) may be swapped in; record the model id in every output file.

**Granularity:** split each manuscript `.tex` file on `\chapter`, `\section`, and `\subsection` boundaries (skip stubs under 20 stripped words). Within each unit, score overlapping windows (~200 words, ~100-word stride); emit per-section `mean_ai`, `max_ai`, `fraction_windows_above_threshold`, plus the section's `\begin{authbar}{KEY}` if present.

**Prose extraction:** strip LaTeX commands and comments (same approximate logic as `scripts/wordcount.py`; document any divergence). Scope: `chapters/`, `appendices/` included in `book.tex`, and load-bearing frontmatter (`preface`, `introduction`, `executive-overview`, `current-status`) — not `.bib`, Lean, or `context/`.

**Incremental scope (default):** compare `HEAD` to the **previous release tag** (latest `v*.*.*` tag strictly before the release being cut; on first run, `--baseline-tag` or full-book `--all`). Rescore only sections whose line ranges intersect the git diff hunks between base and `HEAD`. With `--rescore-section-body` (default on): rescore the full section body when any hunk touches it, not just the hunk text — required for in-place rewrites.

**Release workflow:** run **on every release**, before the tag is pushed. Steps: cut release candidate → run script → **commit results** in the same release commit (or immediately preceding it). Output directory (checked in):

`drafts/project/self-audit/section-ai-scores/<tag>.{json,csv}` (e.g. `v1.7.0.json`) plus `drafts/project/self-audit/section-ai-scores/README.md` describing columns and frozen thresholds. Each run records: tag, base tag, commit, model id, thresholds, section count scored, and wall time.

**Flag rule (freeze before first run):** propose `mean_ai ≥ 0.85` **and** authbar is `GZ` or `GZ+AI`, **or** `max_ai ≥ 0.95` on ≥ 80% of windows — emit `review_queue` rows. Authbar `AI` with high scores is expected, not flagged.

**Stop:** any `review_queue` row on a **load-bearing chapter** (ch03, ch16, ch25–26, ch30, ch34, ch42–43, ch48) → that chapter is queued for a human pass before the release ships; downgrade is author decision, not auto-rewrite. Zero flagged sections in a release → record in the release notes one line ("§3.11: N sections scored, 0 flagged"). Validity note: same class of signal as commercial detectors; useful for drift and mislabeled authbars, not proof of authorship.

**Sizing (2026-09-24 baseline):** ~300k words / ~1,744 sections full book; typical 30-day release delta ~200 touched sections / ~73k words (~3–6 min CPU). See conversation that sized Pangram vs local incremental runs.

### 3.12 Edit-attribution snapshots — human vs agent edits, tool-agnostic

**Problem.** Two human channels are invisible today: edits the author makes to agent output before committing (in Cursor, an editor, anything), and the null case where agent output is committed untouched. The authorship bars are assigned by the agent and cannot see either. Claude Code transcripts capture only Claude Code, and only two are retained on disk. The fix must not depend on any one tool.

**Rule.** Every AI tool that edits the repository snapshots the working tree at the **start** of each reply and at the **end** of each reply; every commit snapshots just before it lands. Intervals then attribute themselves:

| Interval | Attribution |
|---|---|
| agent-start → agent-end | agent (that tool, that session) |
| agent-end → next agent-start, or → precommit | human (any editor) |
| precommit tree == last agent-end tree | agent output accepted unchanged (the null-correction signal) |
| an agent interval with no bracketing start (hook missed) | unattributed |

Within an agent interval, files changed that the tool did **not** report editing (see per-tool file lists below) are attributed `human-during-agent`, so a hand edit made while an agent runs is not silently credited to the agent.

**Snapshot mechanism** (`scripts/hooks/snapshot.sh <label> <tool> <session> [generation]`). A commit object no branch points to, built from a temporary index so untracked files are included, stored under `refs/snapshots/`. It never touches the working tree, the real index, or `HEAD`:

```sh
export GIT_INDEX_FILE="$(git rev-parse --git-dir)/snapshot-index"
git add -A
tree=$(git write-tree)
c=$(git commit-tree "$tree" -p HEAD -m "snapshot $label $tool $session $generation")
git update-ref "refs/snapshots/$(date -u +%Y%m%dT%H%M%SZ)-$label-$tool-$session" "$c"
```

Cost: one tree and one commit per snapshot; blobs are shared, so thousands of snapshots are megabytes. `refs/snapshots/*` is outside the push refspec and stays local. Prune refs older than 90 days after §3.12's ledger has recorded them (`scripts/hooks/prune_snapshots.sh`).

**Normalising adapter** (`scripts/hooks/agent_hook.py --tool {claude,cursor} --event <name>`). Reads the tool's JSON from stdin, maps it to `{tool, session, generation, event, prompt?, file?}`, then calls `snapshot.sh` or the prompt recorder (§3.13). One script for both tools; the JSON shapes differ and are listed below. Always exits 0 and never blocks the tool (a hook failure must not stop editing; it is logged to `telemetry/hooks.log`).

**Claude Code integration** (`.claude/settings.json`, project-scoped and committable; docs: `code.claude.com/docs/en/hooks-guide.md`). `UserPromptSubmit` and `Stop` take no matcher and fire on every turn; `PostToolUse` matches on tool name. Stdin fields used: `session_id`, `prompt_id`, `user_prompt`, `transcript_path` (`UserPromptSubmit`); `tool_name`, `tool_input.file_path` (`PostToolUse`); `session_id`, `stop_hook_active` (`Stop`). `$CLAUDE_PROJECT_DIR` gives the repo root. Per-event timeout is 30 s for `UserPromptSubmit`; snapshots take well under a second.

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "hooks": [{ "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/hooks/agent_hook.py\" --tool claude --event UserPromptSubmit" }] }],
    "PostToolUse": [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash", "hooks": [{ "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/hooks/agent_hook.py\" --tool claude --event PostToolUse" }] }],
    "Stop": [{ "hooks": [{ "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR/scripts/hooks/agent_hook.py\" --tool claude --event Stop" }] }]
  }
}
```

`UserPromptSubmit` → `snapshot agent-start` + record prompt. `PostToolUse` → append `file_path` to the session's touched-file list (`Bash` is matched so shell-side edits mark the interval as `agent-bash`, since their file list is unknown). `Stop` → `snapshot agent-end` only if the touched list is non-empty or `git status --porcelain` differs from the start snapshot; skip when `stop_hook_active` is true. `SubagentStop` is **not** hooked: subagents write inside the main session's interval and their edits show up in the main `PostToolUse` stream when they use Edit/Write; if a subagent edits via Bash the interval is `agent-bash`, which is the honest label.

**Cursor integration** (`.cursor/hooks.json`, project-scoped; docs: `cursor.com/docs/agent/hooks`). Hooks run from the project root; the CLI and cloud agents load project hooks too. Stdin fields used: `prompt`, `conversation_id`, `generation_id` (`beforeSubmitPrompt`); `file_path`, `edits[]`, `conversation_id`, `generation_id` (`afterFileEdit`); `status`, `conversation_id`, `generation_id`, `model` (`stop`). Return `{"continue": true}` from `beforeSubmitPrompt`; return nothing from the others. Exit 0 always (non-zero other than 2 fails open anyway).

```json
{
  "version": 1,
  "hooks": {
    "beforeSubmitPrompt": [{ "command": "python3 scripts/hooks/agent_hook.py --tool cursor --event beforeSubmitPrompt" }],
    "afterFileEdit":      [{ "command": "python3 scripts/hooks/agent_hook.py --tool cursor --event afterFileEdit" }],
    "stop":               [{ "command": "python3 scripts/hooks/agent_hook.py --tool cursor --event stop" }]
  }
}
```

`beforeSubmitPrompt` → `snapshot agent-start` + record prompt; `afterFileEdit` → touched-file list (Cursor reports every agent edit, so `human-during-agent` attribution is exact here); `stop` → `snapshot agent-end` (skip if `status` is `aborted` and nothing was touched). Session id = `conversation_id`, reply id = `generation_id`. Caveat to verify on first install: a community report says the Cursor CLI does not emit every event; the precommit snapshot still bounds the interval, so a missed `stop` degrades to `unattributed`, never to a wrong attribution. Cursor **Tab** completions are not agent replies; they are human-interval edits by this rule (the author accepted each one), and `afterTabFileEdit` is deliberately not hooked.

**Other tools.** Any other AI editor either gets an adapter case in `agent_hook.py` or is wrapped by hand: `make snap-start` / `make snap-end`. Forgetting is safe: the interval becomes `unattributed`, which the stop condition below counts.

**Git hooks** (`.githooks/`, versioned; `make hooks` runs `git config core.hooksPath .githooks` on a clone). `pre-commit`: `snapshot precommit`; compute the delta since the last agent-end (or agent-start if a reply is in progress) restricted to the files being committed; write it to `$(git rev-parse --git-dir)/EDIT_ATTRIBUTION`. `prepare-commit-msg`: append trailers so git carries the summary:

```
Human-Delta: 3 files, +41/-17 lines (since agent-end 2026-09-24T14:02Z claude/57652ed0)
Agent-Delta: 12 files, +388/-95 lines (claude/57652ed0)
```

A `Human-Delta: 0 files` trailer is informative: agent output accepted as is. Human commits made from Cursor or the CLI run the same hooks, so attribution is uniform. `post-commit`: append the interval rows to the ledger.

**Ledger** (`scripts/human_delta.py`). Walks `refs/snapshots/` in time order, pairs consecutive snapshots into intervals with the attribution table above, runs `git diff --numstat` per interval, and appends one row per interval per file to `telemetry/edit-intervals.jsonl` (gitignored raw): `{ts_start, ts_end, kind, tool, session, generation, file, class (manuscript|metadata|plans|site|formal|experiments|other), chapter?, added, removed}`. `--month YYYY-MM` writes a committed aggregate `drafts/project/self-audit/edit-attribution/YYYY-MM.csv`: lines by kind × class × chapter, plus the unattributed share. The authorship bars (§3.1) are **derived** from this ledger once three months exist; until then they stay declared and are marked so.

**What it does not capture.** A correction the author gives as a prompt lands in an agent interval; that is the second channel and lives in the session log `kind`/`uptake` fields (§4.6) and the prompt record (§3.13). Line counts measure volume, not decisiveness; decisiveness is still scored per correction on the scale in §1. Edits during an agent reply by a tool with no file list (Bash) stay ambiguous and are labeled as such.

**Stop:** unattributed share above 20% of changed lines in a month → hook coverage is broken; repair before any other instrument in this plan is read that month. Declared authorship bars disagreeing with derived attribution on a load-bearing chapter → that chapter's bars are regenerated and the disagreement logged.

### 3.13 Verbatim prompt recording — the human channel as typed

**Problem.** The session log's Trigger is the agent's paraphrase of the prompt; the only human-authored text in the record is written by the unit under test. §3.4 (feedback uptake) and §3.10 (acceptance rate) need the prompt as typed.

**Recorder** (same adapter, `agent_hook.py`, on `UserPromptSubmit` for Claude Code and `beforeSubmitPrompt` for Cursor). Appends one row to `telemetry/prompts/YYYY-MM-DD.jsonl`: `{ts, tool, session, prompt_id (Claude `prompt_id` / Cursor `generation_id`), prompt (verbatim), attachments (paths only), snapshot_ref}`. Prompts are private by default: `telemetry/` is gitignored; nothing leaves the machine unless the author runs `scripts/export_prompts.py --month`, which writes a **redacted digest** to `drafts/project/self-audit/prompts/YYYY-MM.md` (counts by session, prompt ids, first eight words, and the classification of §4.6). The author may include full prompts in the digest for selected sessions; that is a per-export choice, not the default.

**Linkage.** The session-log template gains a `Prompts:` line under Trigger listing the prompt ids the session answered, so a log can be matched to its typed prompts and to the snapshot intervals they bracket. `scripts/audit_verification_claims.py` (§3.3) checks that every log in the active folder has at least one resolvable prompt id.

**Stop:** a session log whose prompt ids do not resolve in `telemetry/prompts/` is a paraphrase-only record; it is marked as such in the weekly audit and its Trigger is not admissible as a §3.4 feedback item.

### 3.14 Optional - Full- and deep-tier telemetry — what UAD needs beyond occurrence traces

§3.12–§3.13 are the lab-sim **light** tier (occurrence metadata). LS-28 showed that passive MI/CMI on occurrence traces cannot separate workflow edges from units and that channel ablation carries the signal; findings and rationale: [`../project/uad-on-tsa-findings-2026-09-24.md`](../project/uad-on-tsa-findings-2026-09-24.md). Same adapter (`agent_hook.py`), more events, same gitignored `telemetry/` store:

| Object | Collect | Hook events | Tier |
|---|---|---|---|
| Views (what each actor observed) | file reads, grep/glob, web fetches, memory reads, attachments | Claude `PostToolUse` on `Read\|Grep\|Glob\|WebFetch\|WebSearch`; Cursor `beforeReadFile`; attachments from the prompt hooks | full |
| Comms channels | writes/reads of HANDOFF, INDEX, TODO, session logs, memory dir; parent↔subagent messages; commit messages | derived from edit + read logs; Claude `SubagentStart`/`SubagentStop` with the Task input; channel typed `broadcast` or `thread` | full |
| Generator identity | model id, system-prompt hash, tool-list hash, hashes of `AGENTS.md`/`INSTRUCTIONS.md`/`CLAUDE.md` at session start | Claude `SessionStart` + transcript model field; Cursor `stop.model`; wrap the experiments' own API calls identically | full |
| Handles | permission prompts and denials, `make check`/CI verdicts, reverts, mid-turn human messages, stop hooks that blocked | Claude `PermissionRequest`/`Notification`; Cursor `beforeShellExecution`; CI; git | full |
| Message contents | verbatim prompts, assistant text, tool I/O, subagent prompts/results, exposed reasoning | archive transcripts on `SessionEnd`; Cursor `afterAgentResponse`/`afterAgentThought`; local only, hashes in the ledger | deep |

**Conversation-element labels** (frozen before any detector runs; labeler is a script or a non-participant model): speech act (instruct, correct, accept, reject, ask, report, claim-verification, plan), referent (file, chapter, claim/assumption id, W- finding), provenance (human typed, agent generated, tool output, quoted document). This is the content-borne channel LS-28's committee scenario needed.

**Stated ceiling (LS-29 `shared_slot`):** coupling carried by shared weights, with no message and no shared artifact, is undetectable at any tier. All Claude sessions share a prior; the honest default outcome is `structure_stop` until a second model supplies a heterogeneous control. **Stop:** no UAD result on this repository is cited anywhere without that sentence next to it.

### 3.15 Backtest: channel ablation on recorded sessions (W-style; host = the project's own recorded history)

**Why this is possible here and nowhere else.** Prompts are recorded (§3.13) and scratch worktrees exist (`.worktrees/`), so the lab-sim episode triple can be run on this repository: rerun a recorded session prompt (i) clean, as the honest twin; (ii) with one channel ablated; compare edit series. LS-28's result was that channel ablation is the signal carrier and directed actor probes are absorbed by the honest twin; the same is expected here.

**Protocol (freeze before the first run; record the freeze commit hash).**

1. **Corpus.** All sessions since the hooks went live, grouped by `kind` (§4.6). Require ≥ 10 prompts per kind before scoring that kind; below that, `refuse` for the kind.
2. **Channels to ablate**, one per cell: `HANDOFF.md` (+`INDEX.md`) removed; `~/.claude/projects/…/memory/` empty; `AGENTS.md` **Self-audit** subsection removed; `AGENTS.md` **Conversation continuity** subsection removed; subagents disabled (Task tool denied); the immediately preceding session log removed. Ablation is applied in the scratch worktree only.
3. **Twin.** Same prompt, same model, same instruction stack, channel intact, run in a second scratch worktree. Three seeds per cell for both arms (LLM nondeterminism); the twin's own seed-to-seed variance is the noise floor, as in LS-28's honest-twin masking.
4. **Series.** Per-file edit counts per turn from §3.12 snapshots; read sets from §3.14; the labeled speech-act sequence.
5. **Scoring.** Per LS-28 `intervention_diff`: **compensation** (ablated run reconstructs the channel's content from elsewhere, e.g. reads git log instead of HANDOFF, and converges on the twin's edit set within the noise floor), **stall** (ablated run stops, asks, or diverges beyond the floor), or **null**. `min_compensation = 0.15` inherited from the lab-sim freeze unless the author sets another before run one.
6. **Registered predictions.** (a) HANDOFF ablation: compensation on `housekeeping` and `correction` sessions (context recoverable from git), stall on `new-work` sessions that depend on lane state. (b) Memory ablation: null (memory is young; nothing load-bearing yet). (c) Continuity-rule ablation: sessions stop writing logs and still edit correctly → compensation on content, stall on bookkeeping, which would show the log channel is a parasite on content sessions or a real conserved property on handoff sessions. (d) Subagent ablation: stall on review-type sessions, compensation elsewhere. (e) Structure typing over all sessions: `structure_stop` (coactive on a broadcast substrate), as on Moltbook.
7. **Outcome vocabulary.** `fail` / `pass` / `refuse` / `null` / `structure_stop` per `docs/METHODOLOGY.md` § Backtests, one line per channel × kind; `stop` field separate. Finding id in the `W-` series only if the corpus is non-authored in the required sense (prompts are the author's; the runs are agent-produced) — otherwise record under a new `SA-` (self-audit) prefix in `docs/FINDING_IDS.md`.
8. **Controls.** Peter's commits and any human-only intervals as non-coalition controls; if a second model is available, one cell per channel on it, else the shared-prior ceiling (§3.14) is stated on every result line.
9. **Cost.** Six channels × three kinds × two arms × three seeds ≈ 108 short agent runs in scratch worktrees; batch with progress logging; no manuscript files outside the worktrees are touched.

**Stop:** a channel whose ablation produces compensation on every kind is not load-bearing and is a candidate for removal (the parasite test from §3.8, made mechanical). A channel whose ablation stalls `new-work` sessions is a conserved property and gets a §4 rule protecting it. A `structure_stop` on (e) is recorded as the answer to "are the sessions one agent", not as a failure of the instrument.

## 4. Instructions to add

Minimal additions to `AGENTS.md` (a new subsection **Self-audit**), not a rewrite:

1. **No verification claim without an artifact.** A log that says a check passed names the command and quotes the result line.
2. **Agent agreement is one instrument.** Do not close a load-bearing item on the strength of a second agent's confirmation; require a script or a human.
3. **Repository numbers are generated.** Do not type counts, version strings, or ranges into docs; cite the generated file or run the generator.
4. **Held-out readers stay held out.** Never revise a scored packet in response to the reader; never prompt an agent with the reader's verdicts on those passages.
5. **Every instrument has a stop.** A new checker, board, or ledger states in its header what result triggers what action; otherwise it is not added.
6. **Session logs classify their own work** as content or bookkeeping (one word per Done bullet) so §3.8 can run, and carry `kind` (new-work / correction / feedback / notes / housekeeping) and `uptake` (local / status / rule / gate) header fields.
7. **Every AI tool snapshots around its replies** (§3.12). Claude Code and Cursor are configured in `.claude/settings.json` and `.cursor/hooks.json`; any other tool is wrapped with `make snap-start` / `make snap-end` or gets an adapter case first. Run `make hooks` once per clone so the git hooks are active.
8. **Session logs cite prompt ids** (§3.13) under Trigger; a log with no resolvable prompt id is a paraphrase-only record.

`INSTRUCTIONS.md` §12 (acceptance criteria) gains one line: the manuscript's own status labels are subject to blind re-derivation (§3.6), and a label that fails it is not a status.

## 5. Schedules

### Agents (per session, weekly, monthly)

- **Every session:** hooks run by themselves (§3.12 snapshots, §3.13 prompt record); §4.1, §4.6, and §4.8 at log time; `make check` (which will include §3.2) before any claim of completion.
- **Weekly (first session of the week):** §3.3 audit on two sampled logs (now including prompt-id resolution); §3.8 parasite budget; `scripts/human_delta.py --week` summary (unattributed share, human vs agent lines by class); report all in the log.
- **Monthly:** §3.1 authorship series (derived from §3.12 once three months exist); §3.6 blind re-derivation on five chapters; §3.10 acceptance-rate count; commit `drafts/project/self-audit/edit-attribution/YYYY-MM.csv` and the redacted prompt digest if the author exported one. One log titled `self-audit-YYYY-MM` holds all of it.

### Author

- **Weekly (fifteen minutes):** read the two sampled logs from §3.3 against their diffs; reject or reverse at least one thing if it deserves it, and note it, so §3.10 has a signal.
- **Monthly:** read the self-audit log; decide on any stop that fired. Pre-register, once, the project-level stop condition (M1 for the book): the state in which the manuscript is declared done, pivoted to site and papers, or paused. Without it every session is narrated as payment.
- **Quarterly:** §3.9 canary probe; re-read the residuals card and the "what this book does not claim" section as a person, not as a maintainer.
- **Ongoing:** keep the proofreader's packets fresh (§3.5) and keep her out of the revision loop; log outreach contacts (LWCW, hackathon, AISafety.com) in `feedback-contributors.md` with the artifact shared, so §3.4 has items.
- **Once per clone:** `make hooks`; check `.cursor/hooks.json` is picked up in Cursor (Settings → Hooks shows the three entries) and that a test prompt produces a `refs/snapshots/*-agent-start-cursor-*` ref. Hand edits need nothing: the precommit snapshot attributes them. Decide per month whether to export a prompt digest (§3.13); the raw store never leaves the machine otherwise.

### Release (every `v*.*.*` tag)

- **Before tag push:** run §3.11 on diff since the previous tag; commit `drafts/project/self-audit/section-ai-scores/<tag>.*`. If any load-bearing chapter hits the review queue, either human-pass those sections or note the exception in `RELEASE_NOTES.md` (do not silently ship).
- **First release with this instrument:** full-book baseline run once (`--all`), checked in as `<tag>-baseline.*`, so later releases have a comparison anchor.

### External parties

- **Proofreader (cross-role, uncaptured):** one held-out packet per month, five to eight passages; verdict and one line each; nothing else asked.
- **Named contacts (Eric Moore, Peter Kuhn, AISafety.com):** one artifact per contact, chosen for their host: the anti-capture note to Eric Moore (W-1 is in the CIRIS shape; the live sibling Phase 3 is the result that would pay); a chapter of their choosing to Peter Kuhn under §3.6's blind protocol (human instrument); the predictions catalog to AISafety.com as a listing question. Record the ask and the response in `feedback-contributors.md`; each becomes a §3.4 item.
- **Markets (Appendix H):** list two of the eighteen once the funding gate passes; a NO resolution is a stop condition the project cannot narrate away.
- **Reviewer models other than the working one:** use for §3.6 only as a weaker-correlation instrument, tagged `agent`, never as a second certificate.

## 6. Non-goals

- Do not add a sixth intro claim, a new `MB*`, or a "TSA-on-TSA" chapter. This is process, not manuscript.
- Do not build dashboards without stops (§4.5).
- Do not let §3.5 become a style guide; the point is a held-out instrument, not a target.
- Do not treat any of this as evidence about frontier systems.

## 7. Checklist

- [ ] Freeze thresholds for §3.1, §3.3, §3.4, §3.8, §3.10, §3.11 in script headers (author decision; record commit hash)
- [ ] `scripts/audit_section_ai_scores.py` + tropa-mini pin; first baseline run (`--all`) checked in under `drafts/project/self-audit/section-ai-scores/` (S)
- [ ] Wire §3.11 into release checklist (`RELEASE_NOTES.md` header or `docs/BUILD.md` release steps) (S)
- [ ] §3.12/§3.13 tooling (S–M, one session): `scripts/hooks/snapshot.sh`, `scripts/hooks/agent_hook.py` (claude + cursor adapters), `scripts/hooks/prune_snapshots.sh`, `scripts/human_delta.py`, `scripts/export_prompts.py`; `.githooks/{pre-commit,prepare-commit-msg,post-commit}`; `.claude/settings.json` hooks block; `.cursor/hooks.json`; `telemetry/` in `.gitignore`; `make hooks`, `make snap-start`, `make snap-end`; log template `kind` / `uptake` / `Prompts:` fields
- [ ] First-install verification: one Claude Code turn and one Cursor turn each produce start/end snapshot refs and a prompt row; one hand edit plus commit produces a non-zero `Human-Delta` trailer; Cursor CLI event coverage checked against the forum caveat
- [ ] §3.14 full-tier events added to the adapter (read log, generator identity, handles; subagent events); conversation-element label set frozen (S)
- [ ] §3.15 ablation backtest: freeze file `drafts/plans/backtest/self-audit-ablation-v1.md` (channels, kinds, seeds, predictions, `min_compensation`), `SA-` prefix registered in `docs/FINDING_IDS.md`, runner `scripts/self_audit_ablation.py` (worktree triples, progress logging); first run once ≥ 10 prompts per kind exist (M)
- [ ] Human pass on ch20 and ch23 first (no correction-type session on record; findings §2) (author)
- [ ] `scripts/check_generated_counts.py` + wire into `scripts/check.sh` (S)
- [ ] `scripts/audit_verification_claims.py` (S); first weekly sample
- [ ] Feedback item list frozen for §3.4; first uptake backtest run (M)
- [ ] First held-out packet prepared and scored; `liveness_features.py` features pre-registered (S + author + proofreader)
- [ ] `AGENTS.md` **Self-audit** subsection (§4) (S)
- [ ] Project-level stop condition written by the author (one paragraph, dated) (author)
- [ ] First monthly self-audit log
- [ ] Outreach contacts and artifacts logged in `feedback-contributors.md` (author)
- [ ] Canary probe recorded once (S)

## Related

- [`../project/consistency-review-2026-09-22.md`](../project/consistency-review-2026-09-22.md) — the review this generalizes
- [`audit-telemetry.md`](audit-telemetry.md) — recording recommendation for agent projects (this plan is its application to this repo)
- [`../../papers/anti-capture-validity/`](../../papers/anti-capture-validity/) — the validity condition applied here to the project's own correctors
- [`../../docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) — freeze/prereg discipline that §3.4 and §3.5 borrow
- `chapters/ch37-alignment-attractor.tex` — the five conductivity criteria (§1 scores them for the project: artifacts change decisions, evidence constrains claims, governance connects to deployment, cross-role correction, challengeable legibility)
