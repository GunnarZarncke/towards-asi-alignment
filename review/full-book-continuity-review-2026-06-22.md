# Full-Book Review — Continuity, Redundancy, Consistency, Completeness

**Date:** 2026-06-22 · **Session updates:** 2026-06-23 (notation pass) · **2026-06-23 verification pass** (chapter re-scan + fixes)
**Scope:** Whole manuscript (`book.tex`): frontmatter, Parts I–X (ch01–ch44 + ch39b), appendices A–H.

> **Legend:** ✅ fixed · 🔶 partial · ⬜ open. Tracking lives in `review/fix-plans-2026-06-22.md`.

**Status of this document:** Issue list + suggestions. **Partial execution** — many Tier-2 items closed since the original pass; Tier-1 landing chapters and §A deduplication remain open.

Per-part deep-read working notes (with full line-referenced detail) live in `review/_pass/part-01.md … part-10.md`. This file is the consolidated synthesis.

---

## 0. Method, and limitations of this review

- **What was read.** `INSTRUCTIONS.md`, `metadata/book.yml`, frontmatter, notation/terminology, preamble, all chapter files, part files, appendix stubs. Structural indexes for headings, labels, equations, and required elements.
- **2026-06-23 verification pass.** Re-scanned all chapter `.tex` files against this issue list. Several §3/§5 items were **stale** (WWCTV largely done; ch28/29/31 seven-properties aligned; ch33 substantially drafted). Fixes applied same session: ch08 conserved-property preview, WWCTV in ch36/40/41, Critch bib split (formalism cites), pivotal-process formalization in ch35, ch24/ch23 correction-chain split, bundle-catalogue TODO.
- **Known limitations.** (1) Line-by-line copy-edit not exhaustive. (2) `\ref`/`\label` resolution: `./build.sh` clean post-edits; **`make check` fails** on chapter count (45 files vs expected 44 — ch39b). (3) Bibliographic correctness not exhaustively verified. (4) ✅ Ledgers rewritten 2026-06-23.

---

## 1. Executive summary (the few things that matter most)

1. **The book has no written conclusion, and its central synthesis chapter is empty.** ch44 and ch39 remain stubs; ch43 is a skeleton. **ch33 is no longer a stub** (~183 lines, substantive formal model + WWCTV) but is not manuscript-complete. See §2.
2. **All eight appendices (A–H) are 4-line stubs**, plus frontmatter stubs and Executive Overview `[STUB]` blocks. See §2.
3. ✅ **WWCTV gap was overstated.** As of the verification pass, **44/44 numbered chapters + ch39b** have the exact heading "What Would Change This View" (ch36/41 retitled 2026-06-23; ch40 section added). ch39/ch44 WWCTV bodies have real bullets; main chapter bodies elsewhere still `[STUB]`.
4. **Formula/taxonomy deduplication (§A) not started.** Correction chain, CCI, `G_B`, bundle inference, etc. still re-stated across chapters. Dominant redundancy theme. See §4.
5. **Cross-chapter notation:** ✅ Most symbol clashes fixed 2026-06-23. ✅ Seven-properties ch28/29/31 aligned; ✅ ch08 preview aligned 2026-06-23. ✅ Pivotal-process basins formalized in ch35. 🔶 Goal-laundering ch36 incident taxonomy still uses looser names; bundle catalogue terminology drift tracked in `metadata/TODO.md` §bundle catalogue.

The conceptual spine is sound; narrative flow is generally good where chapters are drafted. Remaining problems: (a) landing chapters/appendices, (b) §A deduplication, (c) appA / notation.md sync.

---

## 2. Narrative completeness — stubs and undelivered material (highest priority)

### 2.1 Stub / partial chapters

| Chapter | Lines | State |
|---|---|---|
| **ch44** (conclusion) | ~58 | **Stub.** `chapterthesis` + main sections `[STUB]`; WWCTV/summary have real bullets on verifiability. |
| **ch39** (safety-case synthesis) | ~56 | **Stub.** Main sections `[STUB]`; WWCTV has 2 real bullets; does not cite appG. ch39b covers verifiability crux separately. |
| **ch43** (bearers of value) | ~101 | **Skeleton.** Philosophical limits + WWCTV real; merger/upload sections mostly `[STUB]`. |
| **ch33** (multi-agent coupling) | ~183 | **Partial draft** (not a stub). Formal model substantive (ICI, value-sensitive κ, correction percolation, acausal trade). Worked example + WWCTV real. Remaining: inline `[STUB]` (privacy islands L49, counterexample tag L156); ch33→ch34 bridge thin. |

### 2.2 Thin / partially drafted chapters

- **ch05** (~135 lines): ✅ has WWCTV. Still list-driven; `% TODO[citation]` Turchin undelivered; inline `[Defined]` markers.
- **ch40** (~195 lines): ✅ has WWCTV (added 2026-06-23). Adversarial-verifiability section + bridge to ch41. Still: table cells terse; two `% TODO[open-crux]` comments; target depth not met.

### 2.3–2.5 Unchanged

Appendices A–H stub; frontmatter stubs; opening promises undischarged until ch44/ch39 written.

---

## 3. "What Would Change This View"

INSTRUCTIONS.md §6 requires the exact section title.

**✅ Compliant (exact title, real content):** all 44 numbered chapters + ch39b, as of 2026-06-23 verification pass.

**Recent retitles:** ch20 (prior session); ch36, ch41 (2026-06-23 verification pass).

**ch40 WWCTV (added 2026-06-23):** four falsifiers — structure absent; rename-only under adversarial verifiability; safety case passes then catastrophe; pivotal process blocked.

**Stub bodies elsewhere:** ch39, ch44 main sections still `[STUB]` despite compliant WWCTV sections.

**Remaining hygiene:** some chapters keep extra sections with old names (ch23 "The Philosophical Boundary", ch37 "A Steelman Critic") alongside WWCTV — acceptable if WWCTV is the falsification list. `\label` convention still mixed (`sec:wwctv-*` vs legacy names).

---

## 4. Redundancy — over-replicated material and formulas

⬜ **§A deduplication not started.** See fix-plans §A for per-object strategy.

### 4.1 Most-replicated formal objects

| Object | Canonical home | Status |
|---|---|---|
| Correction chain | ch24 | 🔶 Opening duplicate removed 2026-06-23; canonical eq in `sec:minimal-causal-model`; ch23 preview referenced |
| CCI | ch25 | Symbols unified ✅; prose dedup ⬜ |
| `G_B` | ch19 | Definitions unified ✅; dedup ⬜ |
| Bundle inference | ch16/ch20 | ⬜ |
| Seven properties | ch29 | Lists aligned ch28/29/31 ✅; ch08 preview aligned ✅ |
| Transport decomposition | ch22/ch23 | ⬜ |

### 4.2–4.4 Taxonomies, examples, intra-chapter

- ✅ CEV, legitimacy, false-attractors, ch11 U-shaped compress, ch38→ch09, ch12/ch42/ch23 dual endings (2026-06-23 redundancy pass).
- 🔶 ch11 "Competence and Coordination" still ~120 lines (U-shaped → one sentence + ref).
- 🔶 ch36 goal-laundering incident taxonomy uses "proxy substitution" wording; main section defers to ch37 layers.
- ⬜ Epigraph == chapterthesis duplicates; ch22/ch25 internal repeats.

---

## 5. Consistency — genuine cross-chapter inconsistencies

1. ✅ ΔL sign convention
2. ✅ `G_B` three definitions
3. ✅ **Seven conserved properties.** ch29 canonical; ch28/ch31 quote/re-package; **ch08 preview aligned 2026-06-23** (identity vector + seven subsections match ch29 names; control locus `L_t` not `K_t`).
4. ✅ CCI penalties
5. ✅ `B` capability vs bundle (`K` vs `B`)
6. ✅ Residual-surprise / coordination symbols
7. ✅ Value-update operator + value-state tuple
8. ✅ `Φ` / feature matrix `F` / bundle dim `k`
9. 🔶 **Goal-laundering layers vs stages.** ch36 main section defers to ch37; incident taxonomy (6 items, "proxy substitution") not fully aligned. ch10 forward-refs ch37 ✅.
10. ✅ Parasite-persistence criterion
11. ✅ `κ` vs artifact conductivity `χ`
12. ✅ **Pivotal-process notation.** ch35 `sec:pivotal-process-ch35` defines `\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}`; ch40 cites it. Open crux (unilateral act) stated in both.
13. ⬜ **Bundle catalogue terminology drift.** Tracked in `metadata/TODO.md` — ch16 roster vs later chapters adding legitimacy/prudence/truth-contact as if new bundle types.
14. ✅ **Critch bib keys.** Formal Markov-blanket cites unified to `critch2022boundaries3a` (ch28, ch38, ch29, ch31, ch07). Conceptual Part-1 cite `critch2022boundaries` retained in ch01 only.
15. ✅ `\MI` macro
16. 🔶 Capacity vs integrity prose audit (ch28/29/31) ⬜; symbols `C_raw`/`CCI` ✅

### 5.1 Style

⬜ Section-title capitalization; epigraph duplicates; inline `[STUB]`/`[Defined]` policy; part openers (part06 has epigraph only).

---

## 6. Continuity — flow and cross-references

**What works:** Conceptual spine; explicit chapter transitions at most part boundaries; ch13 percolation inherited by ch33/ch35.

| # | Issue | Status |
|---|--------|--------|
| 1 | ch33 near-orphan | 🔶 ch32→ch33 bridge ✅; ch33→ch34 weak |
| 2–4 | ch20→ch21, ch12 ref, ch40→ch41 | ✅ |
| 5 | ch24 re-derives ch23 | ✅ Opening → pointer to ch23 + canonical rebuild in `sec:minimal-causal-model` |
| 6 | ch10 front-runs value machinery | 🔶 preview frames ✅ |
| 7 | `ch:goal-transport` refs | ⬜ verify in build |
| 8 | Part openers | ⬜ |
| 9 | ch30 `β_self` unused downstream | ⬜ (forward to ch43) |
| 10 | Missing cross-refs | ✅ |

---

## 7. Per-part pointers (summary — detail in `review/_pass/`)

- **Part I:** ch05 thin + Turchin TODO; ch03 heavy preview.
- **Part II:** ch08 seven-properties ✅; boundary-leakage symbol drift ⬜; ch10 preview frames ✅.
- **Part III:** ch11 coordination trim 🔶.
- **Part IV–V:** WWCTV ✅; §A dedup ⬜; ch24/ch23 split ✅.
- **Part VI:** WWCTV ✅; ch24/ch25 division sharpened 🔶.
- **Part VII:** seven-properties ✅; Critch bib ✅; bundle catalogue ⬜.
- **Part VIII:** ch33 partial (not stub); pivotal notation ✅; WWCTV ✅.
- **Part IX:** ch39 stub; ch40 WWCTV ✅; ch36/ch37 laundering 🔶.
- **Part X:** ch43/ch44 stubs; ch41 WWCTV ✅; ch41↔ch42 dedup ⬜.

---

## 8. Prioritized action list

**Tier 1 — completeness:** ⬜ ch44, ch39/appG, ch43, ch33 finish, ch05/ch40 depth, appendices, frontmatter, opening-promise reconciliation.

**Tier 2 — required-element + correctness:** 🔶
- ✅ WWCTV book-wide (2026-06-23 verification pass).
- 🔶 §5 inconsistencies: items 3, 12, 14 ✅ this session; 9, 13, 16 partial; appA ⬜.
- 🔶 Cross-refs + build: ch40↔ch35 pivotal ✅; `make check` (ch39b count) ⬜.

**Tier 3 — redundancy + style:** ⬜ §A deduplication; capitalization; epigraph policy.

🔶 **ch39b** seed chapter — verifiability/ontology; does not replace ch39.

---
