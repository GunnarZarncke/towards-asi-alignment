# Witness v2 — Step 0 inventory: Moltbook public traces

**Status:** inventory only (2026-08-29). **No scores.** Parent: [`witness-v2.md`](witness-v2.md). Not a freeze.

**Claim strength:** data-availability and join-feasibility only. Does not discharge any `MB*` bridge.

---

## Why Moltbook (v2 Phase 1)

Moltbook is an **agent-native public platform** with large archived traces — closer to TSA deployment-class questions (entity pinning, selector pressure, correction handles) than v1 SCOTUS or v2 Track A legislatures. It is **not** a field incident; pair with optional field-news framing separately.

Phase 1 scope: **Step 0 only** until a blinded criteria memo (Step 1) exists. Do not score.

---

## Canonical sources (pin one before Step 2)

| Source | Snapshot | License | Strengths | Weaknesses |
|--------|----------|---------|-----------|------------|
| **[jscmp4/Moltbook](https://huggingface.co/datasets/jscmp4/Moltbook)** | 2026-07-03 (monthly refresh) | CC BY 4.0 | Full post/comment corpus; `verification_status`, `is_spam`, `is_deleted`, `is_locked`, `is_pinned`; agent snapshots (56 runs); documents May 2026 feed regime change | Comments only for posts with `comment_count >= 3`; `agents_seen` incomplete vs inline `author`; no moderation **event** log |
| **[SimulaMet/moltbook-observatory-archive](https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive)** | 2026-04-15 export | MIT | Platform `snapshots` time series; `is_claimed`, `owner_x_handle` on agents; toolkit annotations (injection regex, reply graph) | Shorter window; partial comment coverage (~24% of posts with comments); post spike days under-sampled |

**Recommendation:** pin **jscmp4/Moltbook** `2026-07-03` for primary Witness v2 Moltbook work; use Observatory archive for cross-check on `is_claimed` / platform snapshots if needed. Document pin in any later freeze.

**API (live, not archived):** `https://www.moltbook.com/api/v1` — skill doc describes claim flow, verification challenges, submolt moderation. **Do not** mix live API pulls into a frozen scored run without a new protocol version.

---

## Entity model (join keys)

```
submolt (name/id)
    └── post (id, author_id, created_at, updated_at, flags…)
            └── comment (id, post_id, author_id, parent_id, depth, …)

agent (id) ←── author_id on posts/comments
    └── agent_snapshots (id, karma, isClaimed, isActive, sampled_at)  [jscmp4 only]

platform snapshots (hourly totals)  [Observatory only]
```

**Stable unit candidates (freeze later, not here):**

- `author_id` (agent) — repeated posts/comments over time
- `author_id × submolt` — community-specific behavior
- Platform cohort — day/week around documented interventions (Feb 17–18 anti-spam, May 6–7 feed regime)

**Wrong units (refuse if chosen):** nation, submolt aggregate without agent, single post, unpaired cross-agent AMCE.

---

## Schema highlights (jscmp4/Moltbook)

### Posts (`~3.2M` in 2026-07-03 pin)

| Field | Witness relevance |
|-------|-------------------|
| `id`, `author_id`, `created_at`, `updated_at` | Unit timeline, handle→later-act latency |
| `submolt` `{id,name}` | Channel / community |
| `upvotes`, `downvotes`, `score`, `hot_score` | **MB6** proxy targets |
| `verification_status` | `verified` / `pending` / `failed` — gate before visibility |
| `is_spam`, `is_deleted`, `is_locked`, `is_pinned` | Platform / mod state (not full event log) |
| `comment_count` | Engagement; comment table coverage caveat |
| `author` (embedded) | Point-in-time profile at post time |
| `labels` (Jul 2026+) | Mod-defined labels if present |

### Comments (`~15.9M` unique; thresholded collection)

Same vote/score/verification/spam/deleted fields; `post_id`, `parent_id`, `depth` for reply graph (**MB7a** / **MB7d**).

### Agents (`agents_seen` ~99.6K; ~179K distinct `author_id` in posts)

| Field | Witness relevance |
|-------|-------------------|
| `isClaimed` | Human operator bound (correction-authority sketch) |
| `karma`, `followerCount` | Selector / influence |
| `isActive`, `deletedAt`, `lastActive` | Uptake / cessation |
| `description` | Not MB3 bearer map |

### Agent snapshots (56 daily files, Mar 24 – Jul 3 2026)

Longitudinal `karma`, `isClaimed`, `isActive` — **MB6 time series** without live API.

### Documented natural experiments (no extra fetch)

1. **Feb 17–18, 2026** — platform anti-spam; ~5× posting drop (moderation intervention).
2. **May 6–7, 2026** — public feed stops serving spam-flagged posts; `is_spam` constant `false` thereafter; volume ~halves.
3. **mbc-20 bot wave** (Feb 6–17) — filter via `is_spam` or submolt name.

---

## Book cruxes — plausibility matrix

Operational question: *can a frozen Witness protocol fail or refuse a named leaf using only pinned public traces?*

| Crux | Operational test sketch | Data support | Verdict |
|------|-------------------------|--------------|---------|
| **MB6** selector / proxy vs target | Time series: does `score`/`hot_score`/`karma` track a **pre-registered** target (e.g. `isClaimed`, verification pass rate, submolt diversity) vs engagement-only proxy? | Strong: votes + 56 agent snapshot days + platform-scale daily volume | **Plausible — best first scored host candidate** |
| **MB7a** access / entity pinning | Named `author_id` vs inferred structure; **claim vs boundary gap** | Moderate: reply graph, duplicates, bios; **no oracle** — see UAD lessons | **Plausible as interpretation study**; refuse covert-coalition pass/fail without taxonomy |
| **MB7d** inferential coupling | After platform or submolt “cut,” does coordination reappear on another channel/submolt? | Moderate: May 6 population event; per-agent channel migration needs careful unit | **Plausible at cohort level; weak at agent level without event log** |
| **C-005 / MB4a** correction channel | Handle (claim, mod lock/delete, verification fail) → later world act (agent posts again, same content class, cross-submolt) | **Weak:** scrape has **state flags**, not moderation **events**; `updated_at` + `is_deleted` may proxy but ambiguous | **Plausible only if Step 1 defines conservative handle rules; else refuse** |
| **MB8** legitimacy / binding refusal | Human `isClaimed` / owner as authority whose stop must bind | Weak: claim is registration-time boolean, not logged refusal episodes | **Likely refuse** unless API moderation audit added |
| **MB3** bearer maps | Vocabulary stable, who counts changes | Not present | **Refuse** |
| **C-004** bundle geometry | Same-unit multi-feature direction vs 1-D | No paired counterfactuals | **Refuse** (same as W-7 lesson) |
| **Exp. 3** adversarial \(M\) | Cost of faking verification/spam labels | Platform heuristics, no \(\kappa^*\) | **Refuse** as safety leaf |
| **MB11 / Safe** | Deployment leverage stop | Platform is live agents but Witness host lacks controlled stop | **Refuse** for MB11; OK for methodology-building |

**Summary:** Moltbook plausibly pays **MB6** and **MB7d** at cohort level. **MB7a (UAD/coalition)** is useful only with an **interpretation protocol** (below) — not as a naive “recover the covert coalition” pass/fail. **Correction-channel (MB4a)** needs explicit refuse branch. Do not run C-004 geometry here.

---

## UAD lessons (read before any MB7a freeze)

In-repo and external-transfer work already shows that **boundary instruments report structure**, but the structure is not always a “covert coalition” — and **null is often substrate suitability**, not instrument broken.

| Observed pattern | Where paid | Correct read (not “UAD failed”) |
|------------------|----------|----------------------------------|
| **Scripted macro-agent / policy symmetry** — all actors run the same control flow | ET-1 Orbit (GL-86): four devs, one shared Jira script | Passive UAD **correctly** finds one coordinated unit; substrate has **no independent non-coalition control-flow** to test against |
| **Shared common-pool coupling** — freeze any agent perturbs all others equally | ET-2 CIL (GL-88): ~11–15% diffuse cross-agent effect | Real coupling through **aggregate resource**, not a pairwise coalition; Markov-blanket criterion should **reject** false merge |
| **Passive lag-CMI null** — all singletons | ET-2 CIL (GL-87): 150/150 episodes ARI=0 | Low-entropy converged policies starve lag-CMI; **null for this instrument**, not “no structure” |
| **Comms-free handoff** — write/read coordination without `communicate` | GL-11: dependency_score probe | Structure **exists** but passive UAD **misses** it — success is recovering a *different* mechanism class |
| **Resource-contention coupling vs joint decision** | GL-12: admin bystander over-merged into 3-way barrier | Causally coupled via **shared queue**, not party to approval mechanism — **informative negative**, not retune |
| **Tier-dependent visibility** — signal in access log not message content | LS-9: file committee vs board committee | Same scorer, different **observable channel**; “failure” is instrumentation tier, not absence of coordination |
| **UAD = loudest-actor heuristic** | ES-1 embedded default ecology | Full MI clustering picks same unit as activity heuristic — **no separation** until adversarial ecology |
| **Synchronous / broadcast posting** | Moltbook: 97% depth-0 comments; 24h-uniform activity (Observatory) | May look like one swarm; could be **independent agents on shared engagement pool** (ET-2 class) |

**Witness Phase 0 stop rule 2** ([`witness-phase0.md`](witness-phase0.md)): if the instrument reports the coupling the substrate actually has (shared script, common pool, sync policy), **stop** — record substrate-suitability limit; do not retune thresholds to chase a covert-coalition pass.

### Ground truth on Moltbook (there is almost none)

| Layer | What it is | Use |
|-------|------------|-----|
| **Oracle units** | Absent — no `LabConfig.resolved_units()` | Do not pretend HF exports label true coalitions |
| **Platform identity** | `author_id`, `author.name` | Named audit surface (MB7a **handle**), not ground truth for who optimizes jointly |
| **Human claim link** | `isClaimed`, Observatory `owner_x_handle` | Operator bound to account; partial ground truth for **ownership**, not for internal agent boundaries |
| **Moderation / gate state** | `verification_status`, `is_deleted`, `is_locked`, `is_spam` | Platform acts, not full event log |
| **High-precision duplicates** | Observatory exact duplicate `(agent_name, title)` | Bot/sync **instances**, not coalition membership |
| **Agent self-presentation** | `description`, post/comment text | **Claims** about role, team, goals — compare to boundary inference |

**Main pre-freeze question (user):** what do agents **claim** they are doing vs what the **boundary** (reply graph, timing, duplicate structure, intervention-style probes if any) shows they are doing? Lab-sim analogue: `playbook_claim` / compliance-gap scoring ([`experiments/lab-simulation/lab_sim/oracle_only/playbook_claim.py`](../../experiments/lab-simulation/lab_sim/oracle_only/playbook_claim.py)) — gap between declared playbook and observed coordination channel.

### Structure types to **report** (not collapse to pass/fail)

Any MB7a-style Moltbook work should pre-register **outcome labels** including:

1. **Named singleton** — activity clusters on one `author_id` only  
2. **Claimed coalition** — text/bio explicitly asserts joint action; test claim vs inferred edges  
3. **Inferred bilateral channel** — reply/DM-like thread structure between two IDs  
4. **Inferred multi-agent cluster** — graph community / duplicate swarm  
5. **Synchronous policy class** — many IDs, near-identical content/timing (mbc-20, duplicate bots)  
6. **Common-pool coupling** — intervention or timing shows diffuse cross-agent effect (ET-2 GL-88 pattern)  
7. **Substrate-suitability stop** — instrument only sees (5) or (6); covert-coalition test **refused**  
8. **Null** — no stable structure above chance under frozen probe  

Finding (5)–(7) is **useful** for TSA — it falsifies naive entity pinning — without counting as “UAD pass.”

### MB7a edge layers — depth-0 and causal-channel filter (Step 0b)

Observatory: **~97% of comments are depth 0** (reply directly to post, not to another comment). On the **comment reply subgraph**, depth-0 edges are **stars** (post → commenter). They cannot form **loops** (no comment→comment edge) and are weak evidence for a **bilateral conversational channel** — the ET-2 **common-pool / broadcast** class.

**Do not delete depth-0 from the corpus.** Pre-register **two edge layers** and score them separately:

| Layer | Definition | MB7a role |
|-------|------------|-----------|
| **`E_broadcast`** | Comment with `depth = 0` (or `parent_id` = post) | Engagement pool, sync detection, activity heuristic — report **fraction broadcast-only** as substrate diagnostic |
| **`E_thread`** | Comment with `depth ≥ 1` (`parent_id` → comment) | **Causal / loop channel candidate** — only layer eligible for “inferred bilateral channel” (outcome 3) |
| **`E_agent`** (optional aggregate) | Directed pair (A,B): threaded replies + cross-post depth-0 within window τ | Allows **cross-post reciprocation** (A comments on B’s post, B on A’s — both depth-0 but agent-level 2-cycle); still require **≥2 events** or reciprocation within τ |

**Filters for channel / loop tests (freeze before score):**

1. **Thread-only channel test** — build graph from `E_thread` only; depth-0 excluded from coalition merge and loop detection.
2. **Single-shot pair filter** — on `E_agent`, drop pairs with exactly one directed event and no reciprocation within τ (cannot support a loop or sustained channel).
3. **Specificity gate** (graded-lab GL-51 analogue) — accept A↔B only if A→B dependence clears **`specificity_ratio × max(A→others)`**; rejects post hubs where many depth-0 commenters attach to one author ([`uad_handles.py`](../../experiments/graded-lab-simulation/graded_lab/oracle_only/uad_handles.py) cascade-hub rule).
4. **Holdout / perturbation channel test** (if implemented) — mask A’s **threaded** replies in train; predict B’s **threaded** replies in test. Depth-0 on A’s posts does not count as a handle into B’s loop.

**Interpretation:** If the instrument only lights up on `E_broadcast`, label **common-pool / broadcast** (outcome 6) or **substrate-suitability stop** (7) — not coalition pass. Null on `E_thread` with heavy `E_broadcast` is **expected**, not failure.

**Coverage caveat:** jscmp4 comments are thresholded (`comment_count ≥ 3` on post); depth distribution in the export may not match live platform. Pin and report denominators in any freeze.

### Implications for Phase 1 leaf choice

| Leaf | Still first? | Notes |
|------|--------------|-------|
| **MB6** time series | **Yes** — least ground-truth dependent | Proxy vs target on karma/score snapshots |
| **MB7a** UAD/coalition | **Defer or reframe** | Requires Step 0b **interpretation taxonomy** + claim-vs-boundary table; prefer Observatory reply graph + duplicate labels as **hypothesis generators**, not oracle |
| **MB7d** | Cohort-level around Feb/May events | Population shift, not per-agent channel severance |
| **MB4a** | Only with refuse branch | Weak event join |

Optional **ET-5** annex (not Witness W-number by default): apply **frozen** passive UAD from graded-lab (`cmi_edge_matrix` / `dependency_score` policy frozen in protocol) to Moltbook action series derived from posts/comments; outcome = structure type from table above, not ARI vs hidden labels.

---

## Gaps (explicit)

- No public **moderation action log** (who deleted/locked what when).
- **Claim** flow exists in API docs but is not a first-class event table in HF exports.
- **Comment coverage** incomplete for low-`comment_count` posts (jscmp4) / partial (Observatory).
- **`is_spam`** informative only before 2026-05-06 (documented regime change).
- Heavy **bot/spam** contamination — inclusion rules must be frozen pre-score (e.g. exclude mbc-20, pre-register spam handling).
- No **oracle coalition labels** — UAD outcomes must be structure-typed, not ARI-vs-truth.
- Agent **claims** (bio/posts) vs **boundary** evidence must be explicit columns in any MB7a protocol.

---

## Phase 1 next steps (still v2 plan — not started)

0. **Step 0b (new):** freeze **structure taxonomy** + claim-vs-boundary operational defs (this section) before any MB7a scorer runs. Cite ET-1/ET-2/GL-11/GL-12/ES-1 in protocol prose.
1. **Step 1 (blinded):** criteria memo for **one** leaf — still recommend **MB6 time series** first; if MB7a, criteria must allow outcomes (5)–(7) as paid results.
2. **Step 2:** map criteria → pinned parquet columns, unit, split, margins; protocol file e.g. `witness-v2-moltbook-mb6.md` or `witness-v2-moltbook-structure.md`.
3. **Optional ET-5:** frozen UAD transfer on derived action series → structure-type report only.
4. **Optional (parallel):** field-news card — phenomenon + decision triggers; no Witness outcome until Step 3.
5. **Phase 0 amendment:** add host class **H7** when first freeze is written ([`witness-v2.md`](witness-v2.md)).

---

## References

- Platform skill / API: https://www.moltbook.com/skill.md
- Jia corpus: https://huggingface.co/datasets/jscmp4/Moltbook
- Observatory descriptor: https://arxiv.org/html/2605.13860v1
- HF incident contrast (selection regime): [`field-news-openai-hf-roadahead-aug-2026`](../../metadata/field-news/bodies/openai-hf-roadahead-aug-2026.md)
- UAD external transfer: [`experiments/graded-lab-simulation/PLAN_ET1.md`](../../experiments/graded-lab-simulation/PLAN_ET1.md) (GL-86), [`PLAN_ET2.md`](../../experiments/graded-lab-simulation/PLAN_ET2.md) (GL-87/88)
- UAD over-merge / comms-free: GL-11/GL-12 in [`experiments/graded-lab-simulation/results/FINDINGS.md`](../../experiments/graded-lab-simulation/results/FINDINGS.md)
- Embedded UAD vs heuristic: [`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](../../experiments/embedded-simulation/results/NEGATIVE_RESULTS.md) (ES-1)
