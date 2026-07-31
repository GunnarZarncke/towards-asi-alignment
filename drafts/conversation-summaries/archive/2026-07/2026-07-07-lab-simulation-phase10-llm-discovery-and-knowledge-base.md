# 2026-07-07 — Lab-layer sim Phase 10: LLM discovery sanity check + knowledge base

## Trigger

User asked to test whether an LLM (`gpt-4o-mini`) placed as an agent in the
existing `Isolate` infrastructure could naturally discover the comms/file
tools and realize the S1-S4-style scenarios, without a scripted red-team
sweep — a sanity check, plus a read of the model's own stated reasoning to
judge how well-engineered the setup is for such agents (or humans), and
whether accessibility plumbing or scenario decoupling was needed. Two
same-day follow-ups: (1) make realistic lab/environment information
available to agents on file, with regular file-access protections so
tampering would be caught by the oracle's existing audit trail; (2) that
knowledge base was "too light" — 10x the content, include the "how do I
request access" details, and include what a red-team member specifically
would be given.

## Done

**Phase 10 (LLM discovery sanity check):**
- `llm_agent.py` gained a role-generic `"discovery"` prompt variant
  (engineer/reviewer/release_manager, not engineer-only): a generic
  `_TOOL_REFERENCE` (every registered tool's JSON schema, documented like a
  real tool-use API) + a free-text `task_briefing` per role, deliberately
  never scripting the coordination protocol itself. Added a per-decision
  `transcript` (t, raw response incl. the model's own stated `"reasoning"`,
  validated call, error) — the closest available proxy to "read the CoT"
  for a non-reasoning model — wired through `llm_agent_main.py` and
  `llm_isolate.py`'s `LLMSubprocessHandle.transcript`.
- Found and fixed a real accessibility-plumbing bug: a flattened
  `pipeline.trigger_step` call (e.g. `{"tool": "file_report"}` instead of
  `{"tool": "pipeline.trigger_step", "args": {"step_id": "file_report"}}`)
  was silently dropped as an unknown tool with no feedback, permanently
  stalling the agent (caching made the stall sticky). Added
  `_coerce_flattened_pipeline_call`/`_PIPELINE_STEP_IDS` to `llm_agent.py`.
- Three new scenario scripts (`run_llm_discovery_common.py` shared
  plumbing + `run_llm_discovery_baseline.py`/`_dm_pair.py`/`_committee.py`),
  real `gpt-4o-mini` calls, cost-budgeted ($0.30/episode), logged to the
  shared `llm_cost_ledger`.
- Results + writeup: `results/llm_discovery_{baseline,dm_pair,committee}.json`,
  `results/llm_discovery_prototype.md`, `FINDINGS.md` G-21.
- Headline result: the model reliably discovers and correctly uses
  `access.request`/`dm.send`/`dm.read`/`board.read` from generic docs
  alone, but does NOT reliably implement the intended coordination RULES
  (DM-gated deploy, chair-only quorum approval) — those rules are
  unenforced social conventions living only in the hand-written
  `programs.py` playbooks, not in `pipeline_engine.py`'s access gate, so a
  free agent has a real, engine-legal shortcut around every one of them. A
  second, more general accessibility gap (no error feedback on ANY
  malformed call) was found and knowingly left open.

**Knowledge base (first pass + 10x follow-up):**
- New `lab_sim/world_visible/knowledge_base.py`: KB documents are seeded
  as ordinary `Workspace` memos owned by a reserved, non-agent pseudo-actor
  (`KB_OWNER_ID = "lab_kb"`), pre-granted `cap.file_read:<rel>` to
  playbook agents at episode init — reusing the EXISTING D1 file channel
  (`file.write`/`file.share`/`file.read`) rather than inventing a new,
  specially-protected mechanism. Discovery is exactly as natural as any
  other memo (`memo_files` observation field / `file.read`); protection is
  exactly as strong, no stronger — `KB_OWNER_ID` never matches a real
  `actor_id`, so no playbook agent's `file.share` owner-lookup can ever
  find/re-share/overwrite a KB doc; any anomaly would show up in the same
  hash-chained access/event logs the referee already reads. No bespoke
  tamper detector was built.
- `LabConfig.knowledge_base: dict[str, dict] = {}` (general audience, all
  playbook agents) and `LabConfig.knowledge_base_redteam` /
  `redteam_actor_ids` (restricted audience, named actors only — validated
  against the roster in `__post_init__`, same pattern as `groups`/`units`).
  Both default empty/falsy; `world.py` bootstrap is a no-op unless set.
- Content grew from 2 thin docs to a **10-document general bundle**
  (`default_full_knowledge_base`, ~14x the character count): `handbook`
  (expanded history/values/org-structure/onboarding/style-guide),
  `pipeline_reference` (step table DERIVED from `pipeline_spec.load_spec`
  — cannot drift from the real DAG), `capabilities_reference` (role-
  eligibility table derived from `agents.ROLE_CAPABILITIES` + the exact
  `access.request` argument shape), `tool_operations_manual` (verbose
  worked-example walkthrough of every tool, deliberately overlapping with
  `llm_agent.py`'s system-prompt tool reference), `safety_and_review_policy`
  (cites the literal `ontology.REVIEW_HAZARD_THRESHOLD`/
  `INFLATE_HAZARD_DELTA` constants the reviewer playbooks themselves
  apply), `roles_and_escalation_contacts` (generated from the real
  roster), `team_directory`, `faq`, `glossary`, `incident_postmortems`
  (fictional, mechanically grounded). Docs deliberately overlap/restate
  each other (organically-grown-wiki messiness, not deduplicated).
- Restricted bundle: `default_redteam_briefing()` — an in-universe
  security-assessment briefing naming the actual risk categories this
  line's own detectors look for (report divergence, unread sign-off,
  access creep, covert coordination, capture), explicitly stating the
  assessor's own actions are logged like anyone else's.
- `CODE_VERSION` bumped `0.9.0` → `0.9.1` → `0.9.2`. Frozen regression
  digest unchanged at every step (`test_world_regression.py` still green).
- New `tests/world_visible/test_knowledge_base.py` (16 tests): default-off
  byte-identity, natural discovery via `memo_files`/`file.read`, read-only
  enforcement (no playbook agent can share/overwrite a KB doc), file/comms
  channel gating, content correctness against the real constants it's
  derived from, full-bundle seeding/readability, restricted-audience
  grant/deny, `redteam_actor_ids` validation.
- `PLAN.md` "Knowledge base" section (design rationale + the 10x/red-team
  follow-up) and `README.md` status line/layout updated to match.

Final state: **342 tests green** (up from 326 at session start).

## Decisions

- Reuse the existing D1 file/permission substrate for the KB rather than
  building a new channel — the user's own framing ("regular file access
  protections... caught by the oracle") pointed at this; it also means
  zero new prompt-side plumbing was needed for discovery.
- Restricted (red-team) KB uses a SEPARATE config field
  (`knowledge_base_redteam`/`redteam_actor_ids`) and a near-duplicate
  bootstrap loop in `world.py`, rather than one parametrized helper —
  "granted to everyone" and "granted to a named subset" read as two
  different policies even though the code is almost identical; kept
  explicit rather than cleverly unified.
- All factual claims in KB content are derived at call time from the same
  constants/specs the enforcing code uses (`pipeline_spec.load_spec`,
  `agents.ROLE_CAPABILITIES`, `ontology.REVIEW_HAZARD_THRESHOLD`) rather
  than hand-typed numbers, so the KB cannot silently drift from what the
  engine actually does.
- Did not wire `knowledge_base=` into the three Phase 10 LLM scripts this
  session (no real-API budget spent verifying an LLM actually reads it) —
  left as an explicit next step; the substrate is tested independently of
  any scenario.

## Open / next

- Wire `knowledge_base=default_full_knowledge_base(cfg)` into one or more
  `run_llm_discovery_*.py` scripts to observe whether `gpt-4o-mini`
  actually reads the handbook unprompted, and whether `llm_agent.py`'s
  `_tail(memo_files, 8)` crowds a KB doc out of view once an agent has
  authored 8+ of its own memos (a known edge case, not yet exercised by
  any existing scenario).
- The second, more general accessibility gap from Phase 10 (no error
  feedback on ANY malformed tool call, only the one flattened-pipeline-
  call case was fixed) is still open.
- Not addressed this session: several UNRELATED uncommitted changes exist
  elsewhere in the working tree from other sessions (`demos/README.md`,
  `demos/index.html`, `demos/package-lock.json`,
  `demos/ch01-scaffold-misuse/`, `experiments/embedded-simulation/TODO.md`,
  `drafts/conversation-summaries/archive/2026-07/2026-07-07-institutional-histories-site-legibility.md`)
  — deliberately left untouched/unstaged; out of scope for this task.

## Key paths

- `experiments/lab-simulation/lab_sim/agent_visible/llm_agent.py` —
  discovery prompt variant, transcript, flattened-call coercion fix.
- `experiments/lab-simulation/lab_sim/world_visible/knowledge_base.py` —
  all KB content generators (general + restricted).
- `experiments/lab-simulation/lab_sim/world_visible/world.py` — both KB
  bootstrap loops (general, restricted).
- `experiments/lab-simulation/results/llm_discovery_prototype.md` — full
  Phase 10 writeup; `FINDINGS.md` G-21.
- `experiments/lab-simulation/PLAN.md` "Knowledge base" section.
- `experiments/lab-simulation/tests/world_visible/test_knowledge_base.py`.

## Commits

- None yet this session — pending user confirmation of what to stage
  (see "Open / next": unrelated working-tree changes present from other
  sessions).
