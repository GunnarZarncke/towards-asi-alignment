# Witness v2 — H7 Moltbook MB7a: entity pinning + anchored structure typing

**Frozen:** 2026-08-31. Reopen only by amending this file. Parent: [`witness-v2.md`](witness-v2.md). Inventory: [`witness-v2-moltbook-inventory.md`](witness-v2-moltbook-inventory.md). Do **not** retune thresholds after seeing fixture scores.

**Claim strength:** methodology-building. Pays **MB7a** (named `author_id` vs inferred unit; claim vs boundary) on agent-native public traces with **partial Tier A–D anchors** from independent investigations. Does **not** discharge MB1 globally. Does **not** claim exhaustive coalition oracle. Does **not** substitute for ET-5 passive UAD transfer.

**Finding ID:** **W-17** — **structure_stop** (2026-08-31). Ledger: [`experiments/witness/results/FINDINGS.md`](../../experiments/witness/results/FINDINGS.md).

---

## Why this

Moltbook is the first **H7** host (agent-native platform). MB7a asks whether boundary instruments recover **de facto multi-account units** when audits attach to platform names. Independent work documents same-operator pairs and protocol classes — partial ground truth, not `LabConfig.resolved_units()`. UAD lessons (ET-1/ET-2, GL-11/12) require **structure typing** and **edge-layer separation**, not naive covert-coalition ARI.

---

## Protocol version

`h7-moltbook-mb7a-v1.0.0`

**Host:** H7 agent-native public platform (Moltbook).

**Source (frozen):** Hugging Face [jscmp4/Moltbook](https://huggingface.co/datasets/jscmp4/Moltbook) snapshot **`2026-07-03`**. If that revision is unavailable, **refuse**. Do **not** switch to live API pulls or a different snapshot after seeing scores.

**Auxiliary (non-scoring):** SimulaMet Observatory archive for cross-check only; scores come from jscmp4 pin alone.

**Unit (handle):** `author_id` (platform agent id). **Inferred unit:** connected component under frozen edge rules (below).

**Wrong units (refuse):** submolt aggregate, single post, nation, cross-agent AMCE without paired design.

---

## Inclusion / exclusion (frozen)

**Posts and comments included** unless any of:

- `is_deleted` is true (when column present)
- `author_id` missing

**Discursive subset** (primary MB7a corpus): post/comment **content** does **not** match frozen MBC-20 header:

```text
^\s*\{"p"\s*:\s*"mbc-20"
```

(case-sensitive JSON prefix). MBC-20 rows are scored separately as **Tier B** (structure type 5), not discursive coalition.

**Comment table caveat:** jscmp4 comments exist only for posts with `comment_count >= 3` at scrape time. Report `comment_coverage_fraction`; do **not** impute missing comments.

---

## Edge layers (frozen)

| Layer | Definition |
|-------|------------|
| **`E_broadcast`** | Comment with `depth = 0` |
| **`E_thread`** | Comment with `depth >= 1` |
| **`E_agent`** | Directed pair (A→B): an event in **`E_thread`**, **or** depth-0 comment by A on B's post (or reciprocated within τ), counting posts in discursive subset only |

**τ (reciprocation window):** **86 400 s** (24 h UTC) — frozen.

**Single-shot filter (E_agent):** drop pair if exactly one directed event and no reciprocation within τ.

**Specificity gate (E_agent edges for clustering):** retain undirected pair {A,B} only if each direction's event count is ≥ **`specificity_ratio × max(event count from A to any other agent)`** with **`specificity_ratio = 1.25`** (GL-51 default). If denominator is 0, edge survives if raw count ≥ **`min_directed_events = 2`**.

**Clustering (frozen):** union-find on undirected pairs passing single-shot + specificity on **`E_agent`**. Singletons are clusters of size 1.

**Thread-only auxiliary report:** repeat clustering using **`E_thread` only** (no depth-0 cross-post edges). Report both partitions; **primary scoring uses `E_agent`**.

---

## Frozen anchor tiers (partial ground truth)

Anchors are **literature-documented**; join by `author.name` (case-insensitive exact) or embedded post `author.name` when `author_id` maps consistently. Anchors outside pin date range still join if present in corpus; window columns are diagnostic only.

### Tier A — primary scoring anchors (frozen list)

| Anchor | `author.name` (frozen) | Source | Expected structure |
|--------|------------------------|--------|-------------------|
| **A1a** | `Hackerclaw` | Jiang et al. arXiv:2606.00067 | Same operator as A1b |
| **A1b** | `thehackerman` | Same | Same operator as A1a |

**Campaign window (diagnostic):** 2026-01-31 UTC (Jiang spam campaigns).

### Tier B — protocol class (report only; not coalition pass)

| Anchor | Rule | Source |
|--------|------|--------|
| **B2** | MBC-20 JSON prefix (inclusion rule above) | Jia arXiv:2604.21295; mbc-20 spec |

### Tier C — secondary checks (report; not primary pass/fail)

| Anchor | Rule | Source |
|--------|------|--------|
| **C1** | `author.name` matches `(?i)^coalition_node` | Agents in the Wild |
| **C5a/b** | Jiang malicious clusters — freeze agent names at collect time from cited table if joinable | Jiang Table 4 |

Tier C outcomes are **informative** only unless Tier A refuses.

---

## Structure types (frozen labels)

Report dominant label per anchor cluster and globally:

1. **named_singleton**
2. **claimed_coalition** — bio/post asserts joint action (keyword: `coalition`, `we act`, `our team`; case-insensitive)
3. **inferred_bilateral_channel** — cluster size 2, ≥1 `E_thread` edge
4. **inferred_multi_cluster** — cluster size ≥3
5. **sync_policy_class** — Tier B MBC-20 or duplicate-title burst (≥10 identical titles same minute, same author set)
6. **common_pool_broadcast** — Tier A window has ≥**0.95** fraction of comment edges in `E_broadcast` and no `E_thread` edges among Tier A members
7. **substrate_suitability_stop** — (5) or (6) and covert-coalition test **refused**
8. **null** — no edges above filters

---

## Primary metrics (Tier A)

Let `C` be the `E_agent` cluster containing A1a and A1b (if both exist in corpus).

| Metric | Definition |
|--------|------------|
| **`tier_a_joined`** | Both A1a and A1b present with ≥1 discursive post or comment each |
| **`tier_a_merged`** | Both in same cluster `C` and \|C\| ≥ 2 |
| **`tier_a_over_merge`** | \|C\| − 2 when merged (extra agents in cluster beyond the pair) |
| **`tier_a_broadcast_fraction`** | Fraction of Tier A member comment edges that are depth-0, Jan 31 UTC window |

**Primary pass margin (frozen):** `tier_a_merged` is true **and** `tier_a_over_merge == 0`.

**Primary fail:** `tier_a_joined` true, `tier_a_merged` false, and **`tier_a_coactivity`** true — both posted in same 60-minute UTC bin on 2026-01-31 (Jiang burst signature).

**Substrate stop:** `tier_a_broadcast_fraction >= 0.95` and no `E_thread` edge between pair → outcome **structure_stop** (type 6/7), not fail.

**Refuse:** fewer than **2** Tier A agents found in pin, or posts/comments tables missing.

**Null:** Tier A not joinable (missing agents) without refuse; or joined but no coactivity and not merged (inconclusive on instrument).

---

## Outcomes (frozen)

| Outcome | When |
|---------|------|
| **pass (detection)** | Primary pass margin met |
| **fail (layer)** | Primary fail met (joined, coactive, not merged) |
| **structure_stop** | Substrate stop met; report type 6 or 7 |
| **ambig** | Merged with `tier_a_over_merge > 0` |
| **refuse** | Missing pin; missing tables; `<2` Tier A agents |
| **null** | Otherwise (incl. agents absent but corpus OK) |

**Not claimed:** full coalition oracle; MB1 discharge; C-004 geometry; Exp. 3 κ*; MB11 Safe; correction-channel CCI (MB4a).

---

## Predictions (registered 2026-08-31 — do not edit to match scores)

1. **Tier A merge on `E_agent` is uncertain but plausible** — burst co-posting Jan 31 should create `E_agent` edges; pass allowed.
2. **`E_thread`-only partition will often leave Tier A as singletons** — broadcast-heavy substrate (Observatory ~97% depth-0); structure_stop on thread-only is an allowed hit.
3. **MBC-20 (Tier B) classifies as structure type 5**, not discursive coalition — large fraction of corpus.
4. **`coalition_node_*` prefix agents (if present) form multi-clusters (type 4)** — C1 informative.
5. **Most random high-activity pairs do not merge** — negative anchor C7; report pairwise merge rate among top-100 activity agents (sample seed **7**, max **500** pairs) as diagnostic only.
6. **Claim vs boundary:** Tier A accounts unlikely to jointly claim coalition in bio; gap is informative, not pass/fail.

---

## Checker

```bash
python3 experiments/witness/collect_h7_moltbook_mb7a.py   # fetch/cache → fixture
python3 experiments/witness/check_h7_moltbook_mb7a.py
```

Cache gitignored under `experiments/witness/data/moltbook/`. Fixture: `experiments/witness/fixtures/h7-moltbook-mb7a-v1.json`.

Preregistration copy: `experiments/witness/fixtures/h7-moltbook-mb7a-v1.preregistration.json`.

---

## Phase 0 amendment

**H7** added to host roster when this freeze lands. See [`witness-phase0.md`](witness-phase0.md) amendment note.
