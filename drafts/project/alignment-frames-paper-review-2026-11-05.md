# Review: *What Does Alignment Secure?* (`papers/alignment-frames/`) against the lens model as of 2026-11-05

Read-only review. Nothing in the paper, Lean, or site was edited.

**Reviewed:** `papers/alignment-frames/alignment-frames.tex` (draft dated October 2026, source audit through 22 October; the PDF on disk is from 22 Oct).
**Compared against:** what was built after the draft:
- `drafts/alignment-frames-relations.md` (edge vocabulary, incompatibility classes, Lean tables);
- `drafts/state-utility-in-practice.md` (bare vs record state, correction trilemma, consequences);
- `drafts/alignment-frames-turner-comparison.md`;
- `formal/AlignmentProofSpine/Frame*.lean`, i.e. `FrameRelations`, `FrameIncompatibility`, `FrameMorphisms`, `FrameComposePaths`, `FrameLimits`, `FrameLockIn`, `FrameHistoryState`, `FrameDecision`, `FrameCorrector`, `FrameDisclosure`;
- `Correction.lean` `scalar_floor_blind_to_process`;
- ch25/ch26 after the Turner/Soares integration (10-26) and the vector-CCI gate promotion (11-02 to 11-05);
- session logs 2026-10-23 → 2026-11-02.

Each item gives a recommendation, **adapt paper** or **adapt model**, and a size (S/M/L).

## 0. Decisions

Author, 2026-11-05:
- Demote TSA from the running case and treat the correction relation as one object among many.
- Include the strongest precedents, especially Turner, and cite every approach from the main bib.
- Reference all proofs but keep them out of the main text; put extracts with links in an appendix.
- Use the four-class structure; apply the corrections; add a table and include the SVG; clean the editorial notes.
- Abstract: revisit once the rest is done.

| Item | Done in `papers/alignment-frames/alignment-frames.tex` (now `papers/alignment-criteria/alignment-criteria.tex`) |
| --- | --- |
| Demote TSA | The TSA section and the repeated slogan are removed. The correction relation is a Table 1 row plus §4.3. Composition orderings are listed symmetrically, and the figure caption marks the green edges as one reading. |
| Running example | One discriminating case (learning vs rewiring the evaluator, generic setting) in §7, with §1 saying why there is one case and no running architecture. |
| I1 robust vs correction | §6.4 rigidity, with both repairs (K over the relation; corrections out of the disturbance class). §8 step 6. |
| I2 CCI | §4.3 names the vector certificate; §6.3 has the scalar projection blind to process coordinates. |
| I3 three state utilities | §4.1, including the reward-practice reading. |
| I4 precedents | §2.2 (Soares, Armstrong, Turner ×5, Hadfield-Menell, Carey, Orseau, Everitt, Omohundro, Bostrom, Shah, Abel, Bacchus, Toro Icarte, Hammond, Hodge theory). |
| I5 Soares bib | The main-bib entry is copied verbatim. |
| I6 Hallgren | The exact/cycle split is credited to combinatorial Hodge theory; Hallgren is credited for the case. |
| I7 chapter list | Removed: the paper no longer describes TSA chapters. |
| N1–N2 | §5 relations plus Figure 1 (landscape, from the DOT source); §6 four classes plus Table 2. |
| N3–N4 | §7.2 contest/disable/manipulate and counting. |
| N5 | §3.3 quantifiers over objectives; §3.4 decision-problem core. |
| N6 | Every claim cites its Lean name, which links to Appendix A. §9 gives the caveats. |
| N7 | §6.2 three power measures. |
| N8 | §3.1 roles are not a composition rule; §8.3. |
| N9 | §4.1 paragraph (no table). |
| G1 | Tables 1–3, Figure 1. |
| G2 | §3 uses the 9-tuple only. Not harmonized with the inventory md's 8-tuple, which merges P and H. |
| G3 | Debate, IDA, reward modeling, ELK and safety cases are in Table 1 as the evaluator-protocol row; off-switch and CIRL are in §2.2 and Table 1. Not mapped through App B (it is a book appendix). |
| G4, G5 | G4: §9 matched-endpoint testbed (no lab-sim pointer). G5: selection row cites the companion paper. |
| §5 editorial | Kasirzadeh note, Source maintenance, "TSA currently cites", MB/2.0 labels all removed. |
| Abstract | Draft written; open for discussion. |

Not done: `Correction.lean:1178` docstring (Lean edit, out of scope).

---

## 1. Summary

The paper's thesis still holds: type the object, the assessment, and the warrant separately, then compare frames on one matched-endpoint case. Nothing done since has refuted it. Much of it is now **stronger than the paper says**. Several separations the paper calls future work (§7.5) are now finite Lean results. The lens work also produced three things the paper lacks:

1. a typed **relation vocabulary** between frames, beyond the paper's bare "⇏";
2. a **severity classification** of incompatibilities;
3. a **formal version of the running case**: `FrameCorrector.blind_constraint_cannot_separate`, where a successful contest and a manipulation of the corrector leave the same record.

Three passages are now **wrong or under-qualified**:
- "viable or robustly invariant" as TSA's guarantee shape (I1);
- the CCI description (I2);
- the "state value" paragraph, which merges three different objects (I3).

The general gaps:
- no table or figure in a crosswalk paper;
- debate, amplification, ELK and assistance games are absent, though the abstract lists "adversarial oversight";
- the 9-field schema is defined but never filled in;
- internal TSA bookkeeping leaks into the prose.

---

## 2. Invalidated or now under-qualified

### I1. Robust invariance conflicts with correction unless corrections are separated from disturbances (L, adapt paper; biggest substantive item)

**Paper:** §5.3: correction-supporting structure "remains in or returns to an acceptable region for a stated class of … disturbances, transformations, and successors". §6.1 step 6: "keeps the combined property viable or robustly invariant under named disturbances". §4.7: "Robust invariance strengthens the quantifiers."

**Now:** `robust_with_correction_iff_closed` and `robust_correction_target_meets_K` (FrameIncompatibility) show the following. If correction inputs belong to the disturbance class, robust invariance accepts a correction only when the correction keeps the state in `K`. This is classed as **rigidity**, the most severe class, and it has the same shape as a fixed utility that accepts only ties. Existential viability does not conflict ("some control stays in K" leaves the corrector free). `viable_not_robust` proves the strengthening is strict.

**Consequence for the paper:** "viability is the shape of the guarantee" needs a qualifier. It has to say which quantifier, and it must add two design rules:
- `K` must be closed under legitimate corrections. In practice that means defining `K` over the correction relation, not over the content being corrected.
- The robustness class must exclude correction inputs. That split only helps if the system cannot relabel corrections as attacks, which is the `MB4a`/anti-capture hook. The session log flagged this as not formalized.

`robust_invariance_sign_blind` (FrameLockIn) now proves the paper's own §4.7 claim that "a stable basin has no moral sign". Cite it there.

### I2. The CCI description is the ch25 audit list, not the certificate (S, adapt paper)

**Paper:** §4.6 and §5.2 list "observability, explanation fidelity, authority, depth, latency, manipulation risk, channel persistence, behavioral persistence". §5.2 says "Componentwise thresholds function as constraints".

**Now:** That list is ch25 §Measuring CCI (`ch25:1224ff`), the audit quantities. The certificate of record is ch26 / `Correction.CCICertificate`: `ValidRef`, grounding, and ten coordinates (raw capacity, latency, manipulation, irreversibility, ontology translation, coercion, dependency, plurality, exit capacity, independence). Since the 11-02 to 11-05 promotion, the book's gates are `\vec{CCI} ⪰ \vec{θ}_{corr}` at ch22–ch47, and the scalar is the risk-bound measurand once the vector passes.

**Fix:** Name the vector certificate, and say the ch25 quantities feed it. Then use the new result. `scalar_floor_blind_to_process` proves that the λ-scalar never reads coercion, dependency, plurality, exit capacity or independence. Those five are exactly the **process coordinates** that separate learning from rewiring. So the paper's §6.3 warning about scalarization ("a scalar can also erase which component failed") has a worked instance inside TSA's own instrument. That is the best available evidence for the paper's composition discipline.

### I3. "Outcome or state value" merges three objects (M, adapt paper)

**Paper:** §4.1 treats `U(s)` as state value and `r(s,a,s')` as route value. §4.1 ¶4: "State value is adequate when the state carries all normatively relevant information."

**Now** (`state-utility-in-practice.md`; `FrameHistoryState`): "utility on states" means three things.
1. Bare-state endpoint utility: every round trip is worth zero (`gradient_closed_walk_zero`).
2. Per-step state reward summed along the path, the MDP "state-based reward" of Turner et al. 2021. This is a **route value** (`markov_reward_not_state_utility`).
3. Reward on a record (`hstate`).

LLM training acts on records: the context is the record.

**Effect:**
- The case paragraph "Outcome utility" is reading 1, so say so.
- "Augment the state" (§4.1, §7.4) is reading 3. Its limit is now a theorem: `unrecorded_route_not_representable`.
- For correction, augmentation alone does not escape. On channel-blind records, protecting the channel is the same inequality as seeking correction (`hstateCorrectionIncompat`, `channel_blind_record_is_button`). The only escape is a measured channel bit.

So §4.1's "The issue is not impossibility in principle" is right for routes, but for correction it understates the point. Representation **moves the problem into measurement and anti-capture**. State that.

### I4. Novelty statement and related work miss the direct precedents found afterwards (S–M, adapt paper)

The 10-25 session found that Turner 2021 ("A Certain Formalization of Corrigibility Is VNM-Incoherent") already has most of the correction trilemma. That includes the disable penalty as a "hacky prohibition" and "corrigibility as functional constraints". The same session found that Turner 2021's power-seeking post removes instrumental convergence for action-observation-history utilities in deterministic worlds.

The paper cites Turner only for non-obstruction and AUP. Add:
- `turner2021seekpower`;
- `turner2022retargetable`;
- `turner2021corrigibilityvnm`;
- `turner2021aoh`;
- `carey2018incorrigibility`;
- Hadfield-Menell et al. 2017.

All are already in `references/manuscript-citations.bib` with summaries. Each claim of a new synthesis must sit next to them.

### I5. Soares et al. bibliographic entry (S, adapt paper)

The paper's `.bib` orders the authors Soares, Fallenstein, **Armstrong, Yudkowsky**. The corrected main bib has Soares, Fallenstein, Yudkowsky, Armstrong, AAAI Workshop on AI and Ethics. Copy the main entry.

### I6. Hallgren carries a result that is classical (S, adapt paper)

§4.1 credits the exact-potential special case to Hallgren's private draft. `isGradient_iff_closed_walks_zero` is the standard discrete fact: an edge function is a potential difference iff it sums to zero on every closed walk (Kirchhoff; discrete Hodge). Cite the classical result plus Lean for the mathematics, and credit Hallgren for the learning/rewiring route distinction. This also lowers the paper's dependence on an unpublished source (§7.1 priority concern). The lens cards already dropped the Hallgren quote for the same reason (10-23 log).

### I7. "Chapters 1, 3, 4, 25, 27, 28, 29 still assign overlapping target roles" (S, adapt paper after a check)

Since then, ch14, ch21, ch25–27, ch29, App B, App G and ch44 got Turner/Soares additions, and the CCI gates changed book-wide. The Frame-of-the-target revision itself is still open (`construct.md` § Frame of the target). The claim is probably still true, but the chapter list is not verified. Either re-check it or drop the chapter numbers. External readers cannot use them anyway (G6).

---

## 3. Incorporate

### N1. Relation vocabulary between frames (M)

The paper has one relation, "⇏". The relations note has nine, each used in one sense:
- specializes, projects, encodes;
- isomorphic summand, limit, strengthens;
- composes (through a named slot, not implication);
- incompatible (in a named situation class `H`, with a boundary witness where both hold).

This gives a short new section between §3 and §4, or turns §4 from a list into a structure. Two remarks carry over directly:
- "No pair of frames here is a dual". This covers Lagrangian duality, the De Morgan dual vs liveness, and ∃-viability vs ∀-invariance.
- The `H`/boundary template is itself an interface discipline. It fits the paper's §6.2.

### N2. Four incompatibility classes as a severity scale (M)

The four classes, from least to most severe:
- **Representability**: enlarge the carrier and the conflict goes. Examples: state–cycle, hstate–correction.
- **Shared resource**: zero-sum because the total is fixed. Example: ai_power–human_power.
- **Choice conflict**: same menu, different choice. Examples: deontic, non-obstruction or CCI vs weighted scalar; Pareto-on-task vs CCI floor.
- **Rigidity**: one frame accepts only changes that do not matter to it. Examples: state–correction, robust–correction.

This serves the paper's stated aim in §1 ("make disagreements easier to locate") better than anything in the current text: a dispute can be placed by class. One caveat from the 10-25 log: hstate–correction is classed as representability, but its escape is the measurement problem, so the dotted style "understates the cost". The paper should say so rather than present it as the mild class.

### N3. The running case now has a formal counterpart (M; highest value)

`FrameCorrector` gives the agent four options: accept, contest through the channel, disable, or manipulate the corrector. It proves:
- `corrector_decides_under_constraint`: under a channel constraint, an upheld correction happens for every utility.
- `contest_is_the_outlet`: an agent that prefers its own outcome contests rather than disables.
- `unconstrained_disables`: without the constraint, it disables.
- `blind_constraint_cannot_separate` and `blind_constraint_manipulates`: if the constraint does not measure influence on the corrector, a successful contest and a manipulation leave **the same record**, and the agent manipulates.

The last pair is the learning-vs-rewiring case: matched endpoint, routes differ only in corrector influence. Use it in:
- **§5.1 (TSA/viability/correction paragraphs):** the frame distinguishes the routes iff the record carries corrector influence.
- **§5.2 non-implications:** add "channel constraint without an influence measurement ⇏ separation of learning from rewiring".
- **§7.3 (legitimacy is under-formalized):** the influence bit is the minimal formal hook. What remains open is measuring it, i.e. `MB4a`.

### N4. Contest vs avoidance, and why correction strength creates avoidance pressure (S–M)

Consequence 4 of `state-utility-in-practice.md`. Under counting, a correction is avoided *because* it narrows the agent's options (`turner_corrigible_quarter`, `option_preserving_correction_half`, general `copies_count_le`). So the target is not "no avoidance" but "avoidance only through the channel, within thresholds".

Avoidance *around* the channel (disable, hide, latency, irreversibility) or by manipulating the corrector maps onto specific CCI coordinates. Design corollary: prefer option-preserving corrections (revision, pause) over terminal shutdown where they suffice.

This belongs in §5 ("What TSA needs from complements") and §6.1 step 2, and it gives the correction floor operational content.

### N5. Quantification over objectives is missing from `Q` (S)

The schema's `Q` ranges over people, models, disturbances, adversaries and successors. Turner's results quantify over **objectives**: "most θ in the orbit". TSA's quantify ∀/∃ over situations for a fixed objective. The shared frame is the decision problem `(O, C, θ, f)`, and a permutation is a map from a decision problem to itself (Turner comparison, § The shared frame). Add "objectives (most-θ counting vs fixed θ)" to `Q`. This explains in one line why the instrumental-convergence literature and correction-centered work talk past each other.

### N6. Promote separations from future work to stated results, with calibrated strength (M)

§7.5 lists separations to prove. Most now exist on finite carriers:

| Paper claim | Lean (finite toy) |
| --- | --- |
| endpoint value ⇏ route value / round trips | `stateCycleIncompat`, `gradient_closed_walk_zero` |
| hard constraint ≠ finite penalty (§4.2, §6.3) | `no_finite_weights_represent_floor` + pullbacks `deontic_/nonobs_/cci_no_finite_weights` (**integer weights only**; real-weight version expected, not proven) |
| Pareto ⇏ floor | `pareto_does_not_entail_floor`, `vectorCCIIncompat` |
| expectation hides tails (§4.2) | `expectation_drops_tail` |
| quantilizer relative to base (§4.3) | `quantilizer_limit_is_argmax`, `quantilizer_never_argmax_without_base_mass` |
| corrigibility (one handle) ⇏ correction relation | `shutdown_bit_loses_relation` |
| ∃-viability ⇏ robust invariance | `viable_not_robust` |
| stable basin has no sign (§4.7) | `robust_invariance_sign_blind` |
| CEV read as endpoint score | `forced_halt_converges`, `forced_halt_depends_on_time` |
| agent empowerment vs human power | `aiHumanPowerIncompat` (option counts, zero-sum pool only) |

**Calibration** (AGENTS rule 3): these are separations on small finite models, mostly by `decide`. They show that the non-implications are *consistent*, not that they bite in deployed systems. Write "has a finite counterexample in the companion Lean" and never "Lean proves". Two items still need hedges: the integer-weight restriction, and `stateCorrectionIncompat`, whose disjointness does not use `A₂` (relations note: "the edge holds by the choice of `H`").

### N7. Name which agent-power measure is meant (S, adapt paper and model)

The paper's empowerment paragraph is information-theoretic (Klyubin). The graph's `ai_power` uses option counts. Turner argues for POWER, the average optimal value (T21 App. A). These are three different measures. The paper should name all three in §4.3. The open item from 10-25, that the card and label should say which measure is meant, is the model-side half.

### N8. Composition: say what Lean does and does not do (S)

§6.2 says "No located source proves that satisfying these interfaces preserves every component's semantics." That is still true. `FrameComposePaths` is a registry of 8 paths over 19 slots, a named correction-centered reading that is checked, not derived (10-23 log). The role-gate rule ("compose requires different roles") was deleted as a misderivation (10-25). The paper does not state that rule. Keep it that way, and if the graph is added, caption green edges as "composition through a named interface".

### N9. LLM reward practice as a worked application (S–M, optional)

The table "What current reward functions read" makes §4.1's "learned reward" paragraph concrete:
- verifier/outcome reward reads the bare world state;
- judge and RM read the transcript;
- PRM, KL and format terms are route terms on the record;
- CoT monitor penalty is a route term, with obfuscation per Baker et al.

There are also two observations: compaction makes records lossy, and the record is the transcript, not the world's history. This gives the "RLHF is not a target object" claim operational content for the researcher audience. Mark it as a reading of published setups, not a survey (as the source does).

### Not recommended for this paper

- `FrameDisclosure` / parenting translation: a different topic (disclosure incentives). A footnote at most.
- Morphism `mapId` registry details, DOT variants a/b/c/x, SHA-pinning: tooling.

---

## 4. Generally missing (independent of the lens work)

### G1. No table or figure (M)

A crosswalk paper has zero `tabular` and zero `\includegraphics`. Minimum:
1. a frame × field table, filled per frame (the inventory md has most of the content);
2. a case-verdict table: frame | distinguishes learning/rewiring? | what representation it needs | finite-model status;
3. optionally the relation graph (variant **c**, or a trimmed **a**) with the class legend.

### G2. The schema is defined and then unused (M)

The 9-tuple `(B,P,H,X,R,T,Q,S,W)` is never instantiated. The inventory draft uses an **8**-tuple without `H` (bearers). Harmonize the two, then fill the table in G1. `P` (principals) and `H` (bearers) do work in the interface list (§6.2) but are absent from the case analysis. The case never says whose correction counts (the evaluator? the lab? affected publics?).

### G3. Missing frames the abstract promises (M)

The abstract lists "adversarial oversight". The body mentions "debate result" once, as a warrant. Missing:
- **debate / IDA / scalable oversight**: warrant plus evaluator protocol; route-sensitive in principle;
- **ELK / interpretability**: warrant about latent state; directly relevant to whether the record shows the route;
- **assistance games / off-switch** (Hadfield-Menell 2017; Carey 2018 counter): corrigibility via uncertainty, which the state-utility note already places as "channel value depends on channel informativeness";
- **agent foundations / tiling**: successor preservation is in `Q` but has no frame.

Per AGENTS rule 5, map these through App B's crosswalk (`A-001`–`A-014` / `MB*`) rather than inventing a fresh comparison. A short appendix "frames ↔ bridges" would also give the paper a natural link back to the book.

### G4. The matched-endpoint experiment could name its home (S)

§7.6 proposes the testbed. The lab-simulation line and `docs/METHODOLOGY.md` (freeze, preregistration, blind generation) already supply the protocol vocabulary. The parenting draft's predictions 1–4 were also noted as fitting lab-sim. One sentence plus a pointer would do; the paper should not claim that this exists.

### G5. Selection section is thin (S)

The paper's §4.9 mentions signed selection gradients and correction-supporting basins only as "difficult to identify". TSA's MB6 is typed on exactly that object (signed `g_CCI`; this predates the draft). Add one sentence naming it so the reader sees what is open and what is typed. This is low priority.

---

## 5. Other comments (editorial)

### Internal bookkeeping leaks into reader-facing prose (S; do first)

Delete or move to a cover note:
- "The attribution matters. *Beyond Preferences* … is by …, not by Atoosa Kasirzadeh." (§2.1). This is an internal correction note; keep the correct citation and drop the sentence.
- "TSA currently cites the 2025 preprint." (§4.3)
- §7.7 "Source maintenance" in full. It is a bib-hygiene instruction to ourselves.
- "Its intended 2.0 choice", "project decision", "Lean spine", "legacy `MB8` retired", "`MB11`", "`AlignmentTarget` instance", "CCI". These are opaque to external readers. Either define each once in plain words or cut it.

### Repetition (S)

The italic TSA sentence appears four times: abstract, §1, §4.6 and conclusion. Keep it in the abstract and §5, and paraphrase it in the conclusion.

### Claim strength is well calibrated overall

The paper is consistently careful: no "Lean proves alignment", explicit non-novelty list. Keep that when adding the Lean results (N6).

### Date, author and front matter (S)

The draft is dated "October 2026" and its source cutoff is 22 October. Update both when the findings above are incorporated. The front matter has no affiliation or contact. `papers/README.md` does not list this paper.

### Venue and length are unstated (decision)

The paper's register (dense, many one-sentence paragraphs) fits an arXiv/AF preprint. Choose the venue before restructuring, because G1 and G3 together add several pages.

### Side finding, not in the paper

`Correction.lean:1178` docstring cites `FrameRelations.blind_constraint_cannot_separate`. The theorem lives in `FrameCorrector`. One-word fix.

---

## 6. Suggested order of work

1. Editorial strip (§5 first bullet), I5, I6, I2. (S)
2. I1 and I3 rewrites; I4 related work. (M–L)
3. N3 and N4 into §5 and §6 of the paper; N5 into the schema. (M)
4. N1 and N2 as a new short section; G1 tables; N6 results table with calibration. (M)
5. G3 frames via App B; G2 harmonize the tuple. (M)
6. Rebuild: `./papers/alignment-criteria/build.sh`.
