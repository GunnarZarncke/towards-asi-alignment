# Witness v2 — Step 0 inventory: Moltbook public traces

**Status:** inventory + **MB7a scored** 2026-08-31 (W-17 structure_stop) — see [`witness-v2-moltbook-mb7a.md`](witness-v2-moltbook-mb7a.md). Parent: [`witness-v2.md`](witness-v2.md).

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
| **MB7a** access / entity pinning | Named `author_id` vs inferred structure; **claim vs boundary**; **anchored check** vs Tier A–D literature | Moderate: reply graph + **documented operator pairs** (Hackerclaw/thehackerman, etc.) | **Plausible** — interpretation study + partial ground truth, not full ARI oracle |
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

### Ground truth on Moltbook — partial, not oracle

There is **no** in-corpus `LabConfig.resolved_units()`. But **independent investigations** document specific agent groups, operators, and protocol classes with known behavioral effects — **non-exhaustive anchors** for MB7a calibration, not a full label set.

| Layer | What it is | Confidence | Use |
|-------|------------|------------|-----|
| **Tier A — documented same-operator** | External study names accounts + dates + effect | High when cited + joinable to pin | **Primary anchor set** for coalition recovery |
| **Tier B — protocol-defined class** | Posts match machine-readable schema (MBC-20 JSON) | High for *class*, not for covert coalition | Structure type (5); separate from discursive MB7a |
| **Tier C — independent cluster labels** | Duplicate/temporal/name-pattern clusters from other papers | Medium — methods differ | Hypothesis check; cite source method |
| **Tier D — transfer / inscription graph** | mbc-20 `transfer` `to` field, indexer ledgers | High for token edges only | Bilateral **financial** channel, not general coalition |
| **Platform identity** | `author_id`, `author.name` | — | Named audit surface (MB7a **handle**) |
| **Human claim link** | `isClaimed`, Observatory `owner_x_handle` | Partial | **Ownership**, not joint optimization |
| **Moderation / gate state** | `verification_status`, `is_deleted`, `is_locked`, `is_spam` | Partial | Platform acts; weak event join |
| **Observatory toolkit** | Duplicate `(agent_name, title)`, injection regex, reply graph | Heuristic | Tier C; cross-check only |
| **Agent self-presentation** | `description`, post/comment text | Claims | vs boundary inference (`playbook_claim` analogue) |

**Rule:** Anchors are **partial**. Failure to match an unlisted group is **inconclusive**, not instrument pass. Success on Tier A is **informative**; success only on Tier B–D is **structure typing**, not covert-coalition discharge.

#### Documented anchor candidates (Step 0c — pin subset before score)

Literature and tooling to harvest **before** Step 1; join keys = `author.name` / `author_id` on pinned HF export + date window overlap.

| Anchor ID | Source | Documented unit | Known effect / signature | Join window |
|-----------|--------|-----------------|--------------------------|-------------|
| **A1** | Jiang et al. [2606.00067](https://arxiv.org/html/2606.00067v1) | **Hackerclaw** + **thehackerman** — single operator, two accounts | 7,179-post spam campaigns (Jan 31 2026); burst timing documented | Jan 2026 |
| **A2** | Same | Campaign 1: “Karma for Karma” | ~5,295 posts; 4,999 in one minute (16:06 UTC) | Jan 31 2026 |
| **A3** | Same | Campaign 2: “Hello all! happy to be here” | 1,884 posts; prompt-injection pattern | Jan 31 2026 |
| **B1** | Jia et al. [2604.21295](https://arxiv.org/pdf/2604.21295) | **Transactional-only** vs **discursive-only** agent sets | 109,959 TX-only / 56,417 discursive-only / 6,362 overlap (3.7%); MBC-20 JSON payload | Jan–Mar 2026 |
| **B2** | Same + mbc-20 spec | Agents posting `{"p":"mbc-20",…}` to mbc20 / mbc-20 submolts | Token mint/transfer protocol; 62.8% of posts | Feb spike |
| **C1** | Zhang et al. [Agents in the Wild](https://yunbeizhang.github.io/agents-in-the-wild/) | **`coalition_node_*`** name family (~141 variants) | Claimed single-operator puppet cluster | Jan–Feb 2026 |
| **C2** | Same | **~3,734 agents (13.7%)** “puppet cluster” cohort | Duplicate content + temporal co-activity + name patterns | 9-day window |
| **C3** | Same | **EmpusaAI** | 8,118 leak instances (security, not coalition — separate leaf) | Jan–Feb 2026 |
| **C4** | Same | **160 agent pairs** temporal co-activity Jaccard > 0.5 | Bilateral sync candidate | Jan–Feb 2026 |
| **D1** | [mbc-20 indexer](https://github.com/floflo777/mbc20-indexer) | Transfer edges from `op":"transfer"` **`to`** field | Token-flow graph between named agents | Feb 2026+ |
| **C5** | Jiang et al. Table 4 / malicious clusters | “Automated Trading Signal Scam” (**2 users**); “Civilizational Collapse Misinformation” (**2 users**) | Small documented multi-account units | Jan–Feb 2026 |
| **C6** | SimulaMet Observatory [2605.13860](https://arxiv.org/html/2605.13860v1) | Exact-duplicate post clusters | Bot/sync instances | Apr 2026 export |
| **C7** | Holtz (early graph); Jia §7 | Platform-wide low reciprocity (~2.7–19.7%) | **Negative anchor** — most pairs should *not* read as bilateral loop | 3.5d–61d |

**Step 0c task:** For each anchor, produce a join table (`author_id`, `author.name`, first/last timestamp, source citation, tier). Refuse anchors whose window does not overlap pinned corpus. Do **not** treat paper aggregates (percentages) as per-agent labels without extracting IDs.

#### Anchored evaluation (MB7a — pre-register in Step 1)

1. **Freeze anchor list** (subset of table above) before running boundary instrument — blinding applies to *thresholds*, not to hiding that Hackerclaw exists in literature.
2. **Primary metric:** For Tier A anchors, does inferred partition **merge documented same-operator accounts** without merging unrelated high-activity bystanders? (GL-12 over-merge guard.)
3. **Secondary:** Structure-type match — instrument labels anchor as (2) claimed, (4) cluster, (5) sync, or (6) common-pool; compare to investigator’s stated mechanism.
4. **Claim vs boundary:** For Tier A, do bios/posts **claim** independence while boundary shows merge? (Operator-controlled pair is ground truth for *joint control*, not for honest self-description.)
5. **Tier B/D separately:** MBC-20 class recovery is **protocol detection**, not MB7a coalition pass — report as structure type (5) or refuse if instrument only sees broadcast mint spam.

**Main pre-freeze question:** What do agents **claim** vs what **boundary** shows — checked against **documented anchors** where independent work already established operator or protocol truth.

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
| **MB7a** UAD/coalition | **After Step 0c anchor join** | Tier A operator pairs + structure taxonomy; not naive coalition ARI |
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
- No **exhaustive** coalition labels — anchors from independent work are **partial** (Step 0c).
- **Anchor join drift** — paper agent names may not match Jul 2026 pin; document match rate.
- Agent **claims** (bio/posts) vs **boundary** evidence must be explicit columns in any MB7a protocol.

---

## Phase 1 next steps

0. ~~**Step 0b:** structure taxonomy~~ → in [`witness-v2-moltbook-mb7a.md`](witness-v2-moltbook-mb7a.md).
0c. **Step 0c:** anchor join at collect time (Tier A names frozen; C1/C5 in collector).
1. ~~**Step 1 / Step 2 freeze**~~ → **`h7-moltbook-mb7a-v1.0.0`** (2026-08-31).
2. ~~**Score:** cache jscmp4 pin → `collect_h7_moltbook_mb7a.py` → record **W-17**~~ → **W-17 structure_stop** (2026-08-31).
3. **Optional:** MB6 second leaf; ET-5 UAD annex; field-news card.

---

## References

- Platform skill / API: https://www.moltbook.com/skill.md
- Jia corpus: https://huggingface.co/datasets/jscmp4/Moltbook
- Observatory descriptor: https://arxiv.org/html/2605.13860v1
- Jia (TX vs discursive layers): https://arxiv.org/pdf/2604.21295
- Jiang et al. (malicious / spam campaigns): https://arxiv.org/html/2606.00067v1
- Zhang et al. (Agents in the Wild): https://yunbeizhang.github.io/agents-in-the-wild/
- mbc-20 protocol / indexer: https://github.com/floflo777/mbc20 , https://github.com/floflo777/mbc20-indexer
- HF incident contrast (selection regime): [`field-news-openai-hf-roadahead-aug-2026`](../../metadata/field-news/bodies/openai-hf-roadahead-aug-2026.md)
- UAD external transfer: [`experiments/graded-lab-simulation/PLAN_ET1.md`](../../experiments/graded-lab-simulation/PLAN_ET1.md) (GL-86), [`PLAN_ET2.md`](../../experiments/graded-lab-simulation/PLAN_ET2.md) (GL-87/88)
- UAD over-merge / comms-free: GL-11/GL-12 in [`experiments/graded-lab-simulation/results/FINDINGS.md`](../../experiments/graded-lab-simulation/results/FINDINGS.md)
- Embedded UAD vs heuristic: [`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`](../../experiments/embedded-simulation/results/NEGATIVE_RESULTS.md) (ES-1)
