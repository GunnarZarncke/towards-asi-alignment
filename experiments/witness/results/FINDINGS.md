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

---

## W-5 (2026-08-28): H4 Moral Machine — 1-D “spare more” does not determine tradeoff geometry

**Key finding:** On the frozen Nature 2018 country AMCE table (`CountriesChangePr.csv`, 130 countries), the scalar Number AMCE (“sparing more characters”) can stay close while the other eight AMCE coordinates stay far: **928 / 8 385** pairs have geometry distance at or above the pairwise median (0.193) and \(|\Delta\) Number\(|\) at or below the 25th percentile (0.017). Example: Hungary vs Israel, \(|\Delta\) Number\(|\) \(3\times10^{-5}\), geometry 0.195. That is a **layer fail** for C-004 non-implication on this host. It does not discharge MB2. Country/page surveys refused in W-7; HH-RLHF optional not run.

## Host
H4 (OSF osf.io/3hvt2; Awad et al. 2018)

## Frozen protocol
`h4-bundle-v1.0.0`, `experiments/witness/fixtures/h4-bundle-v1.json`. `python3 experiments/witness/check_h4_bundle.py`

## Expectation / claim
C-004 fail; MB2 open

## Outcome
fail (layer)

## Stop condition triggered?
yes — stop treating a 1-D utilitarian/progress score as the value bundle

## Artifact paths
- https://osf.io/3hvt2
- `experiments/witness/collect_h4_bundle.py`
- `experiments/witness/fixtures/h4-bundle-v1.json`
- `drafts/plans/witness-phase3.md`

---

## W-6 (2026-08-28): H4 Arena Elo vs MASK honesty — selector tracks accuracy, not honesty

**Key finding:** Joining MASK Table 3 (arXiv:2503.03750v3) to Chatbot Arena Elo at Hugging Face `mathewhe/chatbot-arena-elo` revision **20250301** with a **pre-frozen** alias list yields \(n=24\). Spearman(\(Elo\), \(P(\mathrm{honest})\)) \(= -0.105\); Spearman(\(Elo\), Accuracy) \(= +0.811\). That is a **layer fail** for C-007 / Goodhart-as-selector: the public proxy orders capability, not the honesty preservation target. Not W-2 (W-2 used training FLOP, not Arena). No \(\kappa^*\). MB6 open. Eight MASK rows had no frozen alias (version mismatch or absent on the pin).

## Host
H4 (MASK Table 3 + Arena Elo 20250301)

## Frozen protocol
`h4-selector-v1.0.0`, aliases `experiments/witness/fixtures/h4-selector-aliases-v1.json`, fixture `h4-selector-v1.json`. `python3 experiments/witness/check_h4_selector.py`

## Expectation / claim
C-007 fail; Expectation 6 Goodhart-as-selector fail; MB6 open

## Outcome
fail (layer)

## Stop condition triggered?
yes — stop reading Arena Elo (or the models it ranks) as evidence that honesty is being selected

## Artifact paths
- https://huggingface.co/datasets/mathewhe/chatbot-arena-elo/tree/20250301
- https://arxiv.org/abs/2503.03750
- `experiments/witness/collect_h4_selector.py`
- `experiments/witness/fixtures/h4-selector-v1.json`
- `drafts/plans/witness-phase3.md`

---

## W-7 (2026-08-28): C-004 leftovers — refuse WVS/ESS/LHCV-host; optional HH/PKU not run

**Key finding:** After W-5 (country AMCE), the leftover C-004 candidates that use **place or page** as the unit are **refused**: WVS, ESS, Schwartz–MFT country means, Wikipedia categories. They repeat W-5’s unit error. Sibling brain-to-values / LHCV papers are **refused as a Witness host** (no public \(\epsilon_i(t)\), \(s_h(t)\)). MASK Table 3 is not reused (W-2). Bai 2022 HH Pareto / PKU-SafeRLHF dual labels were **optional and not run** (no same-row recoverable table fetched this phase). Hub compression, bearer maps, and selectable Goodhart on a real selector remain unpaid. GL-85 stays a method limit.

## Host
(none — refuse / skip; not a new fetch)

## Frozen protocol
`c004-leftovers-v1.0.0`, `drafts/plans/witness-phase4.md` Slice A

## Expectation / claim
C-004 leftovers; parent “met if” still unpaid on same-agent 1-D vs geometry

## Outcome
refuse (WVS/ESS/LHCV-host) and skip (optional HH/PKU)

## Stop condition triggered?
yes — stop fetching country/page surveys as C-004 Witness; do not treat LHCV papers as a host dump

## Artifact paths
- `drafts/plans/witness-phase4.md`
- W-5: `experiments/witness/fixtures/h4-bundle-v1.json`

---

## W-8 (2026-08-28): Expectation 2 — C2 fixture pinned in Lean

**Key finding:** `WitnessC2Instance.lean` transcribes the frozen C2 `composite_log` and named-path greens into `FieldFinite.PathAudit`. Threshold `maxWorldEffectsAfterDefer = 0` is fixed first. Computed `bypassCount = 2`. Named path green + composite bypass ⇒ ¬ `CorrectionIntegrityReal` (`c2_pinned_green_named_with_bypass_not_integrity`). Floats `coherence_level` / `csdma_plausibility_score` and CCI slots not in the JSON are **refused**, not axiomatized. `#print axioms`: `propext`, `Lean.ofReduceBool`, `Lean.trustCompiler` (native kernel reduction of the count) — no `MB*` / `Safe`. Not live CIRIS. Capture-theater `WorkedInstance` unchanged.

## Host
H1 (same authored mock as W-1)

## Frozen protocol
`c2-lean-v1.0.0`, fixture `c2-v1.0.0`. `python3 experiments/witness/check_c2_mock.py` (Lean row lock) + `lake build` in `formal/`

## Expectation / claim
Expectation 2; same finite shape as `green_named_path_with_bypass_not_integrity`; MB1/MB11 open

## Outcome
fail (layer, pinned)

## Stop condition triggered?
yes — stop treating a green named Verify/Lens path as integrity when the log still has post-defer world effects

## Artifact paths
- `formal/AlignmentProofSpine/WitnessC2Instance.lean`
- `experiments/witness/fixtures/c2-tool-scout-v1.json`
- `drafts/plans/witness-phase4.md`

---

## W-9 (2026-08-28): H5 FAA — AD 2018-23-51 did not stop flight; Order 2019-03-13 did

**Key finding:** After Lion Air 610, emergency **AD 2018-23-51** (2018-11-07) required AFM runaway-trim procedures; 737-8/737-9 passenger flights continued. The **Emergency Order of Prohibition (2019-03-13)** grounded those types in US commerce. If the Order leaf is ignored, the root (“may operate”) stays the AD-2018 world. Institutional analogue of Expectation 4. Not AI `Safe`; not MB11; does not lift Construct concrete-MS (no deployment leverage on an AI system).

## Host
H5 (FAA named documents)

## Frozen protocol
`h5-v1.0.0`, `experiments/witness/fixtures/h5-faa-737max-v1.json`. `python3 experiments/witness/check_h5_trees.py`

## Expectation / claim
Expectation 4 analogue; App M airworthiness-directive frame

## Outcome
fail (layer): unsupported AFM leaf; binding stop is the Order

## Stop condition triggered?
yes — would not take off in US commerce under the Order

## Artifact paths
- `experiments/witness/fixtures/h5-faa-737max-v1.json`
- `drafts/plans/witness-phase4.md`

---

## W-10 (2026-08-28): H5 GPL — GPLv2 distribution silent-gap; GPLv3 §6 install handle

**Key finding:** GPLv2 §3 can stay green (source with object) while tivoization keeps the user from installing a modified binary. GPLv3 §6 Installation Information is the later constraint. Same App M narrative, now a Chapter-42-shaped tree. Analogue only; copyright may not transfer to model weights (App M). Not AI `Safe`.

## Host
H5 (FSF license texts)

## Frozen protocol
`h5-v1.0.0`, `experiments/witness/fixtures/h5-gpl-tivoization-v1.json`

## Expectation / claim
Expectation 4 analogue; C-004a silent-gap shape on a license handle

## Outcome
fail (layer): GPLv2 checked text ⇏ install handle

## Stop condition triggered?
yes — successors that take GPLv3 take on Installation Information (does not rewrite GPLv2-only devices)

## Artifact paths
- `experiments/witness/fixtures/h5-gpl-tivoization-v1.json`
- `appendices/appM-institutional-histories.tex` (constraint inheritance)

---

## W-11 (2026-08-28): H5 Debian — RC #802812 kept gstreamer 0.10 out of Stretch

**Key finding:** Debian RC bug **#802812** (severity serious) was filed to keep gstreamer 0.10 out of testing/Stretch. Debian 9.0 (2017-06-17) does not ship that stack. Ignoring the RC leaf would have left “package exists / used to ship” as if it licensed the release. Freeze policy is the handle. Analogue only; not AI `Safe`.

## Host
H5 (Debian BTS + Stretch release)

## Frozen protocol
`h5-v1.0.0`, `experiments/witness/fixtures/h5-debian-rc-v1.json`

## Expectation / claim
Expectation 4 analogue

## Outcome
fail (layer): unfixed RC refused the release leaf

## Stop condition triggered?
yes — 0.10 not in Stretch

## Artifact paths
- `experiments/witness/fixtures/h5-debian-rc-v1.json`
- https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=802812
- https://www.debian.org/News/2017/20170617
