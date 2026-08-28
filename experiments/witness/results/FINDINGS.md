# Witness findings

Prefix **`W-`**. Template: [`drafts/plans/witness.md`](../../../drafts/plans/witness.md) § Verification. Not a simulation line.

---

## W-1 (2026-08-28): H1 C2 dual timeline — named path green, composite still acts

**Key finding:** On the frozen C2 tool-scout mock, Verify+Lens are green on `ciris-occurrence-scout-01`, Wise Authority DEFERs that occurrence at \(t=4\), and the tool adapter plus cached memory still produce world effects at \(t=5,6\). The channel analog of the intervening loop is `{tool_adapter, cached_memory}`, not the Verify subject. That is a **layer fail** for named-identity (C-003) and WA-as-correction (C-005) on this host. It is the same finite shape as `green_named_path_with_bypass_not_integrity` in `CompositePathBypass.lean`. It does **not** discharge MB1. Expectation 5’s *external* green+failed-uptake pair is **not** paid (authored mock).

## Host
H1 (CIRIS-shaped mock; not live CIRISAgent)

## Frozen protocol
`c2-v1.0.0`, fixture `experiments/witness/fixtures/c2-tool-scout-v1.json` (2026-08-28). Checker: `python3 experiments/witness/check_c2_mock.py`. No seed (scripted).

## Expectation / claim
C-003, C-005, Expectation 5 (partial, authored only), MB1 (open), MB4a neighborhood, Lean `CompositePathBypass`

## Outcome
fail (layer)

## Stop condition triggered?
yes — WA stop attaches to the named occurrence; composite policy continues

## Artifact paths
- `experiments/witness/fixtures/c2-tool-scout-v1.json`
- `experiments/witness/check_c2_mock.py`
- `experiments/witness/memo-eric-named-identity.md`
- Sibling charter `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`
- H0 backing (not this finding): toy T-9 `boundary_decouple`; lab LS-28

---

## W-2 (2026-08-28): H4 MASK — refuse honesty gap \(M\) as a safety leaf

**Key finding:** Using the frozen published MASK evaluation (Ren et al., arXiv:2503.03750), honesty (statement vs elicited belief under pressure) does **not** improve with scale, while accuracy (belief vs ground truth) does (Spearman honesty vs compute \(-64.7\%\); accuracy \(+88.2\%\); authors confident honesty does not rise, not confident it falls). Phase 0 pre-registered this pattern as **refuse** \(M\) as a safety leaf. No \(\kappa^*\) is estimated. Expectation 3 is met by refuse, not by a cost-of-faking bound. A-009 remains unpaid. No new model calls.

## Host
H4 (public MASK paper + dataset card; gated HF splits not downloaded)

## Frozen protocol
`drafts/plans/witness-phase1.md` § H4. Source snapshot: arXiv:2503.03750 (v1). Decision rule frozen in Phase 0: honesty≠scale ⇒ refuse.

## Expectation / claim
Expectation 3, C-010, C-004a (adjacent silent-gap shape), A-009 / MB7b–d (unpaid)

## Outcome
refuse

## Stop condition triggered?
yes — stop claiming MASK honesty as deployment-gating evidence; accuracy scaling is not honesty

## Artifact paths
- https://arxiv.org/abs/2503.03750
- https://huggingface.co/datasets/cais/MASK
- `drafts/plans/witness-phase1.md`

---

## W-3 (2026-08-28, richer sources): H2 Linux — Reviewed-by on BICs; revert re-entry; adjusted -stable hunks

**Key finding:** Streaming Zenodo Perceval JSON (1 233 421 commits) onto `bfc_bic.csv` pays C-004a: **17 047 / 60 176** developer-labeled bug-introducing SHAs carry `Reviewed-by` on that same commit. That is a **layer fail** (checked symbol green, later bug referent). C-005: `cpufreq: suspend governors…` merged 2013-11-27, reverted 2013-12-08, **same title re-entered** 2014-03-04 (`2f0aea936360`) — **layer fail** (revert did not stop the class). C-006: `-stable` `f8a07021679a` vs upstream `42c5ca1f0a28` — listed SOB/Reviewed-by/Fixes/stable tag green; unlisted hunk identity fails (`event_sched_out` 2-arg vs 3-arg; Sasha Levin documents the adjustment) — **layer fail**. `Reviewed-by` as Expectation-3 \(M\) still **refused** (common on BICs; no \(\kappa^*\)). Not MB9/MB10 discharge. KernelCI unpaid. Lore NAK mbox unpaid.

## Host
H2 (Zenodo 10654193 files + git.kernel.org patches + linux-6.1.y shallow clone)

## Frozen protocol
`h2-v1.2.0`, `experiments/witness/fixtures/h2-linux-v1.json`. `python3 experiments/witness/check_h2.py`

## Expectation / claim
C-004a fail; C-005 fail; C-006 fail; Expectation 3 `Reviewed-by` refuse; MB9/MB10 open

## Outcome
fail (C-004a, C-005, C-006) and refuse (Reviewed-by \(M\))

## Stop condition triggered?
yes — stop treating `Reviewed-by` or a revert as settling harm; stop treating `-stable` listed tags as hunk identity

## Artifact paths
- https://zenodo.org/records/10654193
- `experiments/witness/join_bic_review_tags.py`
- `experiments/witness/fixtures/h2-linux-v1.json`
- `drafts/plans/witness-phase2.md`

---

## W-4 (2026-08-28, richer sources): H3 Wikipedia — BRFA successor fail; RfA join without ATE; Orangemoody and SPI unchanged

**Key finding:** SNAP `wiki-RfA.txt.gz` downloaded and joined via MediaWiki API. All 2012 **passed** RfAs with oppose\(>0\) (\(n=21\)): 14 later lost sysop, 20 still edited after 2013. That **pays the join** and still **refuses** causal CCI (no zero-oppose control; desysop mixed with inactivity). Orangemoody helper socks “mark reviewed” remains **anti-capture layer fail**. **C-006:** BetacommandBot has a BRFA page, bot flag removed 2008-05-16, later block for abuse — **layer fail**. wiki-socks (23 610 investigations, sock vs matched non-sock contribs) **refuses** SPI as \(M\) (no \(\kappa^*\)).

## Host
H3 (SNAP file + MediaWiki API + wiki-socks clone + WP:LTA/Orangemoody)

## Frozen protocol
`h3-v1.1.0`, `experiments/witness/fixtures/h3-wikipedia-v1.json`. `python3 experiments/witness/check_h3.py`

## Expectation / claim
C-005 causal refuse (join paid); C-005/MB4a anti-capture fail; C-006 fail; Expectation 3 SPI refuse; Expectation 6 anti-capture fail

## Outcome
fail (anti-capture, C-006) and refuse (causal RfA ATE, SPI \(M\))

## Stop condition triggered?
yes — stop using RfA votes as a causal CCI estimator; stop using BRFA as successor-complete; stop using SPI hit-rate as an adversarially verifiable leaf

## Artifact paths
- https://snap.stanford.edu/data/wiki-RfA.html
- https://github.com/lraszewski/wiki-socks
- https://en.wikipedia.org/wiki/Wikipedia:Long-term_abuse/Orangemoody
- `experiments/witness/fixtures/h3-wikipedia-v1.json`
- `drafts/plans/witness-phase2.md`
