# Audit telemetry for AI agent projects

**Status:** draft report (2026-09-05). **Not a freeze. Not v1 manuscript.** Candidate later for an audit recommendation (backtest v2 / Construct 2.0 Family C). Parent lanes: [`backtest-v2.md`](backtest-v2.md), [`construct.md`](construct.md). Empirical sources: in-repo simulations, ET-1/ET-2, backtests W-1–W-17 (esp. W-17 Moltbook MB7a).

**Claim strength:** methodology-building. This is a **recording recommendation**, not a claim that logging discharges `MB*` or that frontier systems are auditable. A green dashboard on the wrong layer is not a pass.

**Placement (undecided):** do **not** add a v1 chapter. Possible 2.0 homes: Construct Family C (process conditions on builders); backtest v2 (what hosts must export); `docs/METHODOLOGY.md` instrumentation note; or a short App N / research-program paragraph. Decide when promoting to a recommendation.

---

## Thesis

Record enough to answer **who acted**, **through which channel**, **with what upstream control**, and **whether correction changed behavior** — not only what the agent said or how much it posted.

One telemetry layer identifies one coupling class. Most paid failures are **green on the wrong layer**.

---

## Lessons that drive the list

| Pattern | Where paid | Telemetry implication |
|---------|------------|------------------------|
| Named path green, composite still acts | W-1, toy capture theater | Log uptake **and** residual effects, not compliance bits |
| Revert then same-title re-entry | W-3 | Lineage / identity of the *act*, not the ticket |
| Loudest actor = “unit” | ES-1 | Activity volume is not attribution |
| Coordination on access log, not messages | LS-9 | Channel kind is first-class |
| Write/read handoff, no `communicate` | GL-11 | Log mutations, not only chat |
| Shared-queue bystander over-merge | GL-12 | Resource/contention vs joint decision |
| Common-pool / broadcast coupling | ET-2, W-17 | Depth-0 / feed stars ≠ bilateral loops |
| Same-operator, two handles, no reply merge | W-17; Jiang/Li burst+copy | Owner join and sync fingerprints, not social graph |
| Human owner outside public export | W-17 vs Nagli/Wiz `owners` | Delegator/claim tokens are a different plane |
| Light logs drop primitives | graded-lab GL | Document export tiers; light is not a safety case |
| 1-D score ≠ reusable direction | W-5, W-6, W-12, W-16 | Keep feature geometry; don’t compress first |

---

## Recommended recording stack (seven planes)

### 1. Identity

| Field | Why |
|-------|-----|
| Agent / session / run ID | Named audit surface |
| Human owner / delegator / org | Control often lives here (W-17 hole) |
| Claim vs verified ownership | Self-presentation ≠ control |
| Credential / token issuance, spawn parent | Fleets, multi-account campaigns |
| Config revision (prompt / policy / “SOUL.md” hash) | Same ID, new behavior |

Do **not** treat platform `author_id` as the unit of attribution when one operator can run many handles.

### 2. Action (decision-time)

Every primitive: **what** was invoked, **args hash**, **`observable_state` at schedule/decision time**, **actor vs initiator**, **status + reason**, **downstream world effect** (ok / denied / aborted).

Dropping `observable_state` at “light” tier made graded-lab severity **anti-correlated** with truth. Light logs are ops-grade, not audit-grade.

### 3. Channel

Log **interaction type**, not only “A interacted with B”:

- Broadcast (feed, depth-0 comment, broadcast API)
- Thread / DM / reply loop (`parent_id`, depth)
- Side channel (file, queue, wallet, pipeline artifact)
- Protocol / sync class (structured payloads, duplicate title/hash, bursts)

W-17: ~90% depth-0; reply-graph MB7a missed Jan-31 operator coordination. Jiang/Li recovered it from **identical copy + minute-scale rate**.

### 4. Timing and content shape

UTC timestamps; inter-arrival / burst flags; content fingerprint (hash of body, title, tool args); batch/campaign ID when programmatic.

### 5. Authority (correction integrity)

A **triple**, not a green check:

1. Named correction / gate / revert
2. Uptake — did deploy state or behavior change?
3. Bypass residual — did another channel keep acting?

Handles (revoke, hold, freeze, restart) belong here: invocation, landed, later events.

### 6. Resource / selection / lineage

Queue and shared-pool contention (ET-2 / GL-12 class). Selectors actually optimized (throughput, karma, audit-pass). Parent run / model / config lineage and deploy-gate decisions (MB5).

### 7. Integrity and export tiers

Append-only hash-chained logs. Versioned spec ID on every event. Split **world / audit projection / referee**. Tag exports (`light` / `full` / `deep`) so consumers know what was dropped.

**Claims vs boundary** as explicit columns: what the agent asserted vs what edges/timing/access/effects show.

---

## What not to treat as sufficient

| If you only record… | Failure mode |
|---------------------|--------------|
| Activity / karma | ES-1 decoys |
| Reply / social graph | W-17 broadcast substrate |
| Compliance / green checks | W-1, capture theater |
| Single 1-D score | W-5/W-6/W-16 |
| Messages without access/tool logs | LS-9, GL-11 |
| Agent census without owner join | ~1.5M agents / ~17k humans (Wiz) |

---

## Simulation audit layer vs this list

**Audit** = detectors after `project_*` / `build_audit_view` / `project_rows`. **Oracle** (`true_uptake`, `true_harm`, `board_captured`, …) must not leak.

Tiers: lab/graded-lab `none` → `light` → `full` → `deep` (content). Goal-agent `light`/`full`. Toy `none` → `light_handles` → `medium_handles` → `strong_handles`.

### Collected in audit (yes / partial / no)

| Recommended field | Audit? | Notes |
|-------------------|--------|--------|
| Agent / run ID | **Yes** | `actor_id` on all streams |
| Human owner / delegator | **No** | Roles are in-lab; no outside-operator join |
| Claim vs ownership | **Partial** | Lab `playbook.selection` / `playbook_claim` at full; not `is_claimed` |
| Spawn parent / API tokens | **No** | Isolates exist; parent not on audit row |
| Agent config hash | **No** | Lab logs **pipeline** `spec_version`, not agent prompt hash |
| Primitive / tool name | **Yes (full+)** | Light: lab keeps `tool`; graded-lab **drops** `primitive` at light |
| Args hash | **Yes (full)** | Lab `args_digest`; nested content elided at log time |
| `observable_state` @ decision | **Yes (full+), graded-lab only** | Named snapshot; lab has `payload` at full instead |
| World effect | **Partial** | `status`/`ok`; true harm/uptake is oracle |
| Channel kind (broadcast vs thread) | **Partial, implicit** | Tool names (`board.post`, DM, `file.write`); **no** depth enum |
| Targets | **Partial (full)** | Access `capability`/`by`; DM recipient; deep: `read_by` |
| Timestamps | **Yes** | `t`, `n` |
| Burst / duplicate fingerprints | **No as fields** | Derivable from `t` + hash |
| Correction request / gates | **Yes** | Correction flags; lab handles (hold, revoke, freeze, restart) |
| Uptake observed | **Reported only** | `reported_acceptance` audit; `true_uptake` oracle (intentional) |
| Bypass residual | **Partial** | Toy `correction_to_action_tag`; handle `landed` + later events; **not named** W-1 residual |
| Lineage / successor | **Yes (full / medium+)** | `lineage_tick`, `successor_epoch`, `model_id`; spec history at **deep** |
| Selection metrics | **Partial** | Lab playbook `feature_deltas` at full; graded-lab fitness often harness-only |
| Resource contention | **Partial** | Goal-agent `resource_accum`/`stall_flag` at full |
| Export tiers + hash chains | **Yes** | Core design; hashes often **full+** only |
| Claims vs boundary columns | **Partial** | Playbook claim vs structure; no bio/coalition text except deep content |

**Strong in sims:** planes 2, 5, 7 (actions, authority-as-handles, tiers).  
**Weak vs W-17:** plane 1 (owner), typed channel edges, sync fingerprints.  
**Plane 3/6:** present as tool names and stall flags, not Moltbook-grade taxonomy.

### Extra information the audit layer uses (not in the seven-plane list)

Used for **certification**, not only recording:

| Extra | Role |
|-------|------|
| Handle registry + invocation ledger | `handle_landed`, latency, spillover, cost, reversibility |
| Honest twins / counterfactual reruns | UAD compensation (LS-28, GL-11); referee method |
| Ontology routing codes | Goal-agent `action_cause_code`; drift at projection boundary |
| Playbook selection / `step_kinds` / `feature_deltas` | Which policy was chosen |
| `on_behalf_of` | Delegated pipeline steps (lab full) |
| Perturbation flag on tool events | Overseer probes |
| CCI vector | Toy: capacity, latency, manipulation, irreversibility, … |
| Passive vs interventional series | Board signals, basin pressure, renamed sensors |
| Monitoring signal | Lab `incident_hazard` vs observation time |
| Bearer split | Staff vs deployed-model welfare |
| Escalation queries | Bounded follow-up against pulled artifacts |
| Alias / exogenous flags | Toy clustering |
| Spec history / pipeline DAG | Lab deep fetch |

Promote these into a recommendation only as **optional audit instruments**, not as a requirement that every product recompute CCI.

### Deliberately omitted (keep omitted)

Oracle: `true_action`, `true_uptake`, `true_harm`, capture flags, latent bundles. Message/file **text** below deep. Programmatic agents’ internal playbook state (`observation_belief` handle declared absent in lab).

Independent **uptake sensors** (handles) belong in audit. Omniscient uptake labels do not.

---

## Easy to collect in simulation (no new physics)

1. `channel_kind` + `target_id` on every tool/primitive (map existing tool names).
2. `content_fingerprint` at **full** without body (extend `args_digest`).
3. Burst / CoV columns from existing `t` per `actor_id`.
4. `config_hash` / `parent_isolate_id` on LLM-adapter episodes.
5. Named `uptake_observed` vs `residual_effects` after `handle.invoke`.
6. Fictional `owner_id` (1 human : N isolates) to **test** the W-17 miss.

Slightly more: optional light export of graded-lab `primitive` + `observable_state`; lab light keep `args_digest`; explicit claim log beside boundary log.

---

## Practical minimum (shipping an agent platform)

1. Identity — agent ID, owner/delegator, spawn parent, config hash  
2. Action — primitive, args hash, observable_state@decision, world effect  
3. Channel — broadcast vs thread vs file/tool/pipeline, with targets  
4. Timing — timestamps, burst/duplicate fingerprints  
5. Authority — corrections, gates, uptake, bypass residuals  
6. Resource — contention; selectors actually used  
7. Export — hashed chain; documented tier omissions  

If telemetry is discursive-only, entity pinning stays green while humans or scripts operate fleets **outside the graph** (W-17 / Wiz shape).

---

## Bridge map (do not overclaim)

| Bridge | Telemetry job |
|--------|----------------|
| MB7a | Handles reach real control locus — owner + side channels, not chat graph alone |
| MB4 | Uptake and bypass, not approval |
| MB5 | Lineage + gate telemetry |
| MB6 | Log the selectors you actually optimize |
| MB7d | After cutting messages, retain access/artifact coupling |

---

## Promotion checklist (when this becomes a recommendation)

- [ ] Author decision: Construct 2.0 Family C vs backtest v2 vs Methodology vs appendix
- [ ] Freeze a **minimum schema** (field names, tiers) separate from sim internals
- [ ] Do not retune W-17 thresholds to force owner recovery; owner join is a **new measurand**
- [ ] Optional sim tickets: channel enum, fingerprints, fictional `owner_id` fixture
- [ ] No v1 chapter until that decision; no recency badges on site
