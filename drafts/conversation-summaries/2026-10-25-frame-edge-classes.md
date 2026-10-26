# 2026-10-25 — Frame edge classes, Turner comparison, Soares, pinned links, ledger

kind: new-work
uptake: gate

## Trigger
User:
- write up the bare-vs-record finding (done 2026-10-24 as `drafts/state-utility-in-practice.md`);
- check Turner and add the hstate–correction edge;
- then split red edges by visual class (shared resource orange; red dotted representability, dashed choice conflict, solid rigidity);
- Turner 2022 coverage table with Lean candidates;
- elaborate Soares;
- SHA-pinned links;
- Frame theorems in the axiom ledger;
- explain the role gate and options.
- Follow-up: what shared frame made the Turner mapping possible and should we use it; consequences of the channel-record result; check the origin of the roles rule and delete it if baseless.
Prompts: paraphrase-only

## Done
- content: Lean `IncompatClass` and `IncompatKind.cls` (representability, choice conflict, rigidity, shared resource) in `FrameIncompatibility`. New kind `unrecordedChannel` for hstate–correction. `incompatExt` carries kinds.
- content: DOT **a**/**b**/**c** restyled:
  - red dotted = representability (state–cycle, hstate–correction);
  - red dashed = choice conflict (deontic/au_floor/cci_cert–weighted_scalar, criteria_vector–cci_cert);
  - red solid = rigidity (state–correction, robust–correction);
  - orange `#E8590C` = shared resource (ai_power–human_power);
  - limit edges moved from orange to blue `#1565C0` to avoid two oranges.
  Legends, x renderer, SVGs, site map hint and overview text updated.
- content: `check_frame_graph.py` checks each drawn edge's colour/style against the Lean class. Negative test: a dashed state–cycle edge is reported.
- content: `markov_reward_not_state_utility` (per-step state reward summed along a path is a route value). The write-up now distinguishes three meanings of "utility on states".
- content: `drafts/alignment-frames-turner-comparison.md`: coverage table (subagent draft, key quotes re-checked against extracted text), Lean candidates.
- content: write-up: Soares et al. 2015 section (Theorems 1, 2, 4; §4.1, §4.2, §5 quotes checked), plain-language boundary paragraph.
- content: `site/scripts/lib/repo-pin.mjs`: Lean links in the lens map and `lean-spine.json` pinned to the built commit (`GITHUB_SHA` or `HEAD`); warns when `formal/AlignmentProofSpine` is dirty. Both outputs are gitignored, so no tracked churn.
- content: axiom ledger: 54 Frame entries with `"scope": "frames"`, checked but left out of the book table. Book table unchanged (diffed before/after).
- bookkeeping: verification:
  - `lake build AlignmentProofSpine` → "Build completed successfully (2271 jobs).";
  - `./formal/check.sh --no-build` → "Axiom budget check passed (102 theorems, no drift).";
  - frame axioms ⊆ `[propext, Classical.choice, Quot.sound]`;
  - `python3 scripts/check_frame_graph.py` → "Frame graph check passed (19 compose, 9 incompatible, 18 morphism, 3 limit/strengthens edges match Lean).";
  - `./scripts/check.sh`: only markdown links fail (new untracked files and other sessions' files).

- content (follow-up: shared frame, consequences of the correction result, role rule):
  - **Role rule deleted.** "Compose requires different roles" was a misderivation. The inventory draft says the four roles must not be collapsed into one objective; the relations note turned that into a composition rule, the converse. No user statement found in transcripts. Removed `RoleCompose`, `roleCompose_trivial`, `roleCompose_necessary_slot`, `roleComposeAllowed` and their ledger rows. Note and site overview now say green = composition through a named interface. Roles remain node labels (`interfaceOf`).
  - **Novelty corrected.** Turner's 2021 posts already contain most of the correction trilemma (reward blind to correction status → only ties / constant reward; reward sees status → manipulation into correction; disable penalty called "a hacky prohibition"; "corrigibility as functional constraints"). They also show instrumental convergence disappears for action-observation-history utilities in deterministic worlds. The write-up now has a Turner-2021 section, a consequences section (measurement, finite channel weight fails at scale, constraint not weight, correction strength vs avoidance, process rewards need an out-of-reach record), and interventions. The comparison file has a shared-frame section (decision problems; Turner = automorphisms, ours = maps between problems) and two new rows. The "records do not escape counting" claim is corrected in the write-up, card and note.
  - Verification: `lake build AlignmentProofSpine` → "Build completed successfully (2271 jobs)."; `check_axiom_budget.py` → "Axiom budget check passed (100 theorems, no drift)."; frame graph check passed; `sync-lenses --check` up to date.

- content (third request: role change approved; build the decision-problem frame; place consequences in chapters; cite Turner and Soares; CCI criteria; avoidance through the channel; process rewards):
  - New `formal/AlignmentProofSpine/FrameDecision.lean`:
    - `ArgmaxOn`, general square `argmax_pullback`;
    - map functions and squares: `readAtRecordEnd`/`state_hstate_square`, `induceGradient`/`state_route_square`, `expectationFunctional`/`dist_state_square` (loss `expectation_drops_tail`), `scalar_optimal_is_pareto`, `pareto_not_scalar_optimal`, `lex_optimal_is_pareto`, `approval_one_edge`;
    - `mapImpls` registry plus `mapImpls_registered`;
    - Turner-style orbit counts by `decide` (`turner_corrigible_quarter`, `option_preserving_correction_half`) next to the ∀ form `subset_branch_never_strictly_better`.
  - Checker verifies `mapImpls` ids and declarations; site map edges link to the squares; ledger +15 frame entries.
  - Bibliography: `soares2015corrigibility` and `turner2021seekpower` had wrong authors (fixed, venues added). Added `turner2022retargetable`, `turner2021corrigibilityvnm`, `turner2021aoh`, `carey2018incorrigibility` with summaries.
  - Write-up: the channel bit is the CCI certificate; ch25 already states constraint-not-weight in prose (our contribution is the formal reason); avoidance through the channel is acceptable, around it (disable, hide, latency, irreversibility) or by manipulating the corrector is the failure; process rewards help on harness-written records with tamper detection the agent cannot reach. Two new interventions.
  - Relations note: decision-problem section with map table and counting-vs-∀ table.
  - New `drafts/plans/turner-soares-integration.md`: chapter placements (ch25, ch26, ch27, ch14, ch21, ch29, ch42, appB, appG, ch44), awaiting approval.
  - Verification:
    - `lake build AlignmentProofSpine` → "Build completed successfully (2272 jobs).";
    - `./formal/check.sh --no-build` → "Axiom budget check passed (115 theorems, no drift).";
    - `check_frame_graph.py` → "Frame graph check passed (19 compose, 9 incompatible, 18 morphism (8 with map functions), 3 limit/strengthens edges match Lean).";
    - `check_bibliography_summaries.py` → "Bibliography summary check passed (561 summaries for 561 bib keys).";
    - markdown links: all 21 failures are untracked-but-existing files.

- content (2026-10-26, fourth request: open edge proofs, Turner's general count, corrector model, apply chapter edits):
  - `FrameDecision`:
    - `isGradient_iff_closed_walks_zero` (exact = zero closed-walk sums; summand edges now rest on it), `closed_walk_ignores_exact` (route → cycle);
    - handle maps `corrig_correction_square`, `shutdown_bit_loses_relation`;
    - graph **b** certificate maps `cci_coordinate_floor_square`, `subvector_gate`, `gate_bounds_scalar_gap`;
    - `hist_hstate_square`, `mapImpls_cover` (17 of 18 maps; `correction → cci_cert` is the `MB4a` measurement step, not a proof gap);
    - general argmax n-fold retargetability `copies_count_le` and `correction_avoided_card_fold` (every objective, via `Equiv.Perm` and `Finset.card_le_card_of_injOn`).
  - New `FrameCorrector.lean`: accept / contest / disable / manipulate; `corrector_decides_under_constraint`, `contest_is_the_outlet`, `unconstrained_disables`, `blind_constraint_cannot_separate`, `blind_constraint_manipulates`. Site: `deontic → correction` edge links there; summand edges link to `isGradient_iff_closed_walks_zero`.
  - Chapter edits (user approved), additions only:
    - ch25 Relation to Corrigibility (decision-problem reason, Soares Thms 1/2/4, Turner count, floor theorem, constraint model) and Shutdown section (counting, contest vs avoidance);
    - ch26 validity (anti-capture reason) and CCI vector (manipulation coordinate);
    - ch27 Goodharting (drills, harness-written records), capability growth (priced vs constrained), quantilization (Turner 2022), Claim 5 evidence;
    - ch14 (power-seeking qualifications, two design rules);
    - ch21 (three meanings of state utility, LLM reward terms);
    - ch29 (contest vs shaping the corrector);
    - appB MB4; appG record view; ch44 corrigibility paragraph.
    - New bib `baker2025monitoring`.
    - Note: appG already rederives Soares in `Field/Finite/ShutdownIncentives.lean`; the new paragraph sits next to it.
  - Verification:
    - `lake build AlignmentProofSpine` → "Build completed successfully (2273 jobs).";
    - `check_axiom_budget.py` → "Axiom budget check passed (135 theorems, no drift)."; frame axioms ⊆ `[propext, Classical.choice, Quot.sound]`;
    - `check_frame_graph.py` → "Frame graph check passed (19 compose, 9 incompatible, 18 morphism (17 with map functions), 3 limit/strengthens edges match Lean).";
    - bibliography summaries "562 summaries for 562 bib keys"; PDF build: see below.

## Decisions
- robust–correction classed as **rigidity**, not choice conflict (earlier plan): `robust_with_correction_iff_closed` is "accepts only corrections that stay in K". Flagged to the user.
- hstate–correction classed as **representability** (recording the channel removes it). The dotted style understates the cost of that escape. Flagged.
- Ledger frame entries excluded from the book appendix table via `scope`.

## Open / next
- Review the chapter additions (listed above); close `drafts/plans/turner-soares-integration.md` after review.
- Lean: Conjecture B.13 cases; record refinement multiplies copies; orbit-sum POWER on a shared pool; tie `FrameCorrector`'s record to the full CCI vector; canonical (orthogonal) cycle part.
- Turner Lean candidates: correction records under orbit counting; Conjecture B.13 small cases; record refinement multiplies copies; orbit-sum POWER on a shared pool.
- `ai_power` uses option counts; Turner argues for POWER. Card and label should say which measure is meant.

## Key paths
- `drafts/alignment-frames-turner-comparison.md`
- `drafts/state-utility-in-practice.md`
- `site/scripts/lib/repo-pin.mjs`
- `formal/axiom-ledger.json`

## Commits
- `6c88bcad7e` Lean: decision problems, record-carrying state, corrector model, classes, ledger.
- `97243f9385` Graphs and graph check by conflict class.
- `7ccdab60a2` Site: record-carrying state lens, pinned Lean links.
- `6a35d050d8` Bibliography: Soares and Turner fixes and additions.
- `f2d5e0bb6a` Manuscript: Turner and Soares integration.
- Drafts: state-utility and Turner comparison notes, relations note, plan (commit before the session-log commit).
- Session logs, HANDOFF, INDEX (this commit).
- PDF build after the chapter edits: `./build.sh` → "Built dist/pdf/towards-superintelligence-alignment.pdf"; no new citation key or label undefined.
