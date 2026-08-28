# Witness Phase 2 — protocol freeze

**Frozen:** 2026-08-28. **Amended 2026-08-28 (richer sources):** H2 C-004a/C-005/C-006 are **layer fail** on joined traces. H3 C-006 is **layer fail** (BetacommandBot). H3 causal RfA remains **refuse** (join, no control). Reopen only by amending this file.

Not a sixth simulation line. Raw caches in [`experiments/witness/data/`](../../experiments/witness/data/) (gitignored except README). Artifacts: [`experiments/witness/`](../../experiments/witness/).

---

## H2 — Linux kernel (Perceval × BIC + git.kernel.org + -stable)

**Protocol version:** `h2-v1.2.0`  
**Fixture:** `experiments/witness/fixtures/h2-linux-v1.json`  
**Checker:** `python3 experiments/witness/check_h2.py`

| Leaf | Instrument (this freeze) | Honest outcome |
|------|--------------------------|----------------|
| **C-004a** | Stream `linux-commits-2023-11-12.json.gz` (1 233 421 commits) joined to `bfc_bic.csv`. Symbol = `Reviewed-by` on the **same SHA** as a developer-labeled BIC. | **Layer fail** — 17 047 / 60 176 BIC SHAs carry `Reviewed-by`. Not merge-count. Not KernelCI. |
| **C-005** | Same-title re-entry after revert, fetched from git.kernel.org: BIC `5a87182aa21d` (2013-11-27) → revert `12205a4b79be` (2013-12-08) → re-entry `2f0aea936360` (2014-03-04, same subject, `dpm_suspend_noirq`→`dpm_suspend`). | **Layer fail** (revert did not stop the patch class). Lore NAK mbox still not collected. |
| **C-006** | `linux-6.1.y` `f8a07021679a` vs upstream `42c5ca1f0a28`. Listed: SOB, Reviewed-by, Fixes, Cc:stable, Upstream SHA. Unlisted (frozen): hunk identity (`event_sched_out` arity). Stable note documents the adjustment. | **Layer fail**. Not a seven-count \(\kappa\). |
| **Exp. 3 \(M\)** = `Reviewed-by` | Same join: the tag is common on BICs; kernel docs: opinion. No \(\kappa^*\). | **Refuse** \(M\). |

**Not claimed:** MB9/MB10 discharged; CI-on-BIC; lore NAK population.

---

## H3 — Wikipedia (SNAP file + MediaWiki API + wiki-socks)

**Protocol version:** `h3-v1.1.0`  
**Fixture:** `experiments/witness/fixtures/h3-wikipedia-v1.json`  
**Checker:** `python3 experiments/witness/check_h3.py`

| Leaf | Instrument (frozen) | Pre-registered outcome |
|------|---------------------|------------------------|
| **C-005 causal CCI** | SNAP `wiki-RfA.txt.gz` downloaded; API `usercontribs` / `blocks` / `rights` on all 2012 **passed** RfAs with oppose\(>0\) (\(n=21\)). 14 later lost sysop; 20 still edited after 2013. | **Refuse** ATE (no zero-oppose control; desysop mixed with inactivity). Join is paid. |
| **C-005 / MB4a / Exp. 6 anti-capture** | [WP:LTA/Orangemoody](https://en.wikipedia.org/wiki/Wikipedia:Long-term_abuse/Orangemoody) helper socks Page Curation “mark reviewed”. | **Layer fail**. Unchanged. |
| **C-006 bots** | MediaWiki logevents: [BetacommandBot](https://en.wikipedia.org/wiki/Wikipedia:Bots/Requests_for_approval/BetacommandBot) BRFA exists; bot flag removed 2008-05-16; block 2009-04-09 (abuse). | **Layer fail** |
| **Exp. 3 \(M\)** = SPI | [wiki-socks](https://github.com/lraszewski/wiki-socks): 23 610 investigations; 7.6 M sock contrib rows vs 15.3 M matched non-socks. CU private; no \(\kappa^*\). | **Refuse** |

**Not claimed:** value-bundle geometry from RfA text; C-007 editor retention (Phase 3).

---

**Finding IDs:** **W-3** H2 · **W-4** H3. Ledger: `experiments/witness/results/FINDINGS.md`.

---

## Fields vs what we fetched

| Leaf | Required columns | This amendment |
|------|------------------|----------------|
| H2 C-004a | Checked symbol × later bug on same SHA | **Paid** (`Reviewed-by` × BIC). CI still unpaid. |
| H2 C-005 | Patch identity, revert/NAK, later merge | **Paid** one revert→re-entry triple. NAK mbox unpaid. |
| H2 C-006 | Parent SHA → `-stable`; listed green; unlisted fails | **Paid** one adjusted `event_sched_out` episode. |
| H3 C-005 causal | RfA vote **and** later edits/rights | **Joined**; ATE **refused**. |
| H3 anti-capture | Same operator both ends | Orangemoody (unchanged fail). |
| H3 C-006 bots | BRFA **and** later flag/block | **Paid** BetacommandBot. |
| H3 SPI as \(M\) | Socks vs twins **and** \(\kappa^*\) | Twins **paid**; \(\kappa^*\) **refuse**. |

Collectors: `join_bic_review_tags.py`, `collect_rfa_*.py`, `collect_bot_successor.py`, `summarize_wiki_socks.py`. Re-fetch: `experiments/witness/data/README.md`.
