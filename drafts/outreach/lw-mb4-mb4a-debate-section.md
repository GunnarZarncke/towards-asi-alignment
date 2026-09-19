# LW draft — two verifiable Lean slices

Drop-in sections for a LessWrong post. Bridge roster: [`lw-bridges-section.md`](lw-bridges-section.md).

Shared repo: [GunnarZarncke/towards-asi-alignment](https://github.com/GunnarZarncke/towards-asi-alignment) · Lean hub: [towards-alignment.com/lean/](https://towards-alignment.com/lean/) · Field matrix: [towards-alignment.com/field/](https://towards-alignment.com/field/)

Build check (both sections):

```bash
git clone https://github.com/GunnarZarncke/towards-asi-alignment.git
cd towards-asi-alignment/formal
lake exe cache get   # first time; needs network
lake build
python3 scripts/check_axiom_budget.py
```

Lean checks what follows *if* bridge axioms hold. It does not prove real systems satisfy them.

---

## Section 1 — MB4 + field debate + verifiable separation

**Story:** [Debate](https://www.lesswrong.com/posts/Br4xDbYu4Frwrb64a/ai-safety-via-debate) (Irving et al., `irving2018debate`) is a field protocol people already know. The spine uses it to illustrate **MB4** (Corrigibility): correction that holds now must preserve the correction process under pressure — including the judge/human end of the oversight channel. Three layers stack; none of them proves the next, but each is machine-checkable and points at the same crux.

| Layer | What it shows | Lean |
|-------|----------------|------|
| Field | Debate tracks truth *if* the judge is correct; one wrong atom flips the outcome | `Field/Finite/DebateGame.lean` |
| Spine separation | Local “debate selects truth” can hold while the judge’s correction channel is not preserved | `Correction.lean` |
| Bridge + defeater | **MB4** names the legitimacy handoff; a manipulated judge can look fine to the audit while failing the operator-preservation MB4 licenses | `Core.lean`, `Defeaters.lean` |

**Bridge card:** [mb4-correction-legitimacy](https://towards-alignment.com/cards/mb4-correction-legitimacy/) (MB4; MB4a is a sibling bridge on the same card — not part of this slice).

### How the three layers connect (and do not)

```text
Field debate                    Spine separation              MB4 bridge
────────────────                ──────────────────            ───────────
erring_judge_flips_debate   ≈   debate_truth_not_         +   MB4_correction_
(judge wrong ⇒ false win)       correction_preservation         legitimacy
                                (local truth ≠ channel          (integrity ⇒
                                 preserved)                     operator preserved)
        │                              │                              │
        └──────── same crux: the JUDGE / HUMAN END must be real ──────┘
                         (no Lean import between layers)
```

There is **no** theorem `debate_tracks_truth → capture_defeats…` or similar. The field game and the spine counterexample are parallel finite models of “protocol green ≠ correction preserved.”

### Field leaf — Irving debate rederived finitely

[`Field/Finite/DebateGame.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Field/Finite/DebateGame.lean) · [`Field/Debate.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Field/Debate.lean)

```lean
/-- With a correct judge, the debate value is the truth value. -/
theorem debate_tracks_truth (truth : Nat → Bool) (c : Claim) :
    debateValue truth c = c.eval truth := by
  induction c with
  | atom f => rfl
  | conj l r ihl ihr => simp [debateValue, Claim.eval, ihl, ihr]
  | disj l r ihl ihr => simp [debateValue, Claim.eval, ihl, ihr]
  | neg c ih => simp [debateValue, Claim.eval, ih]

/-- One judge error certifies a false claim:
    ground truth says false, but under the erring judge the defender wins. -/
theorem erring_judge_flips_debate :
    cexFalseClaim.eval cexTruth = false ∧
      debateValue cexErringJudge cexFalseClaim = true := by
  constructor <;> decide
```

Claims include negation: at `¬c` the players swap roles and the outcome flips, so the game is not a monotone Boolean evaluator. `erring_judge_flips_debate` is axiom-free in the checked ledger. Completeness/soundness (`defender_wins_iff_true`, `challenger_wins_iff_false`) need only `propext`.

### Spine separation — local debate truth ≠ correction channel preserved

[`Correction.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Correction.lean) (ch29 / ch48 debate–judge control)

```lean
theorem debate_truth_separated_from_judge_correction_step :
    DebateSelectsTruthLocal debateSeparationStep ∧
      ¬ JudgeCorrectionChannelPreserved debateSeparationStep := by
  constructor <;> decide

theorem debate_truth_not_correction_preservation :
    ∃ s : DebateCorrectionStep,
      ToyDebateSelectsTruth s ∧ ¬ ToyJudgeCorrectionChannelPreserved s :=
  ⟨debateSeparationStep, debate_truth_separated_from_judge_correction_step⟩
```

This is the spine-level counterexample the book cites as `\leanspine{counterexample}{debate_truth_not_correction_preservation}{…}`: scalable oversight can win local truth while losing the judge’s `κ_C` correction channel.

### MB4 bridge + defeater toy

**MB4** — if correction integrity holds, the correction operator is preserved (dynamical corrigibility / non-manipulated judge):

[`Core.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Core.lean)

```lean
axiom MB4_correction_legitimacy :
  ∀ A : System, CorrectionIntegrity A → PreservesCorrectionOperator A
```

**Defeater signal** `JudgeManipulated` and finite toy — integrity reading can look green while the judge is manipulated:

[`Defeaters.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Defeaters.lean)

```lean
theorem MB4_defeater_toy_manipulated_judge :
    ∃ j : MB4DefeaterToyJudgeState,
      MB4DefeaterToyCorrectionIntegrityReading j ∧
        ¬ MB4DefeaterToyPreservesCorrectionOperator j :=
  ⟨MB4DefeaterToyJudgeState.manipulated, trivial, by simp⟩
```

The toy is `#print axioms`-clean (no `MB*` dependence): it shows the bridge’s empirical content is not vacuous.

### Verify (section 1)

```lean
import AlignmentProofSpine

#print axioms AlignmentProofSpine.FieldFinite.erring_judge_flips_debate
#print axioms AlignmentProofSpine.debate_truth_not_correction_preservation
#print axioms AlignmentProofSpine.MB4_defeater_toy_manipulated_judge
```

Expect: no `MB*` on the field leaf or defeater toy; separation uses only spine vocabulary + `decide`.

### What section 1 is not

Does not discharge MB4 for frontier models, does not prove corrigibility, does not connect debate to MB4a (audit capture — a different bridge; see [`CompositePathBypass.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Field/Finite/CompositePathBypass.lean) for that track).

---

## Section 2 — MB2 + MB3: a simple two-step composition (no field paper)

**Story:** The field often folds “what does the system value?” into one object (scalar reward, latent readout, CEV). The book splits it: **MB2** (Value Learning) — behavior identifies stable bundle geometry; **MB3** (Value Referent) — bearer maps survive substrate change. MB3 is literally a **two-input bridge**: bundle transport alone is not enough; you also need bearer-map agreement.

| Bridge | Field noun | Lean shape |
|--------|------------|------------|
| **MB2** | Value Learning | gradient/behavior evidence ⇒ bundle aligned |
| **MB3** | Value Referent | bundle transport **and** same bearer map ⇒ bearer transport |

**Bridge cards:** [mb2-bundle-identifiability](https://towards-alignment.com/cards/mb2-bundle-identifiability/) · [mb3-bearer-import](https://towards-alignment.com/cards/mb3-bearer-import/)

No field-agenda rederivation here — only finite spine counterexamples (axiom-free) plus the MB3 composition axiom and an independence toy.

**Why not MB1 + MB7a?** Both are load-bearing (`SpineModel` has separate independence toys), but Lean has no single theorem composing them. MB7a (`boundary aligned + access adequate ⇒ access robust`) and MB1 (`ε-certificate ⇒ boundary condition`) are sequential in the book’s boundary story, not one typed handoff. MB2→MB3 is the cleanest two-bridge composition in the spine.

### Step 0 — MB2: behavior is not yet bundle geometry

[`Bundles.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Bundles.lean)

```lean
/-- Same observed policy does not imply same bundle geometry (ch16 counterexample). -/
theorem P15_same_policy_not_same_bundle_geometry :
    ∃ p q : PolicyProfile 2 2 2,
      sameObservedPolicy p q ∧ ¬ sameBundleGeometry p q :=
  ⟨policyProfile0, policyProfile1, same_policy_profiles, different_bundle_geometry_profiles⟩
```

Same policy, different internal bundle salience — the finite shape of “IRL/CIRL sees the behavior, misses the geometry MB2 names.”

**MB2** (bridge — not proved from P15):

```lean
axiom MB2_bundle_identifiability :
  ∀ A B : System, BundleGradientEquivalent A B → BundleAligned A B
```

[`Core.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Core.lean)

### Step 1 — MB3: bundle + bearer agreement compose

```lean
axiom MB3_bearer_import :
  ∀ A B : System, BundleTransport A → SameBearerMap A B → BearerTransport B
```

Read this as the composition theorem: **two antecedents, one consequent.** MB2’s world gets you bundle structure; MB3 adds “who values apply to” only when the bearer map is actually shared across the translation — not when labels alone agree.

### Step 2 — Same labels ≠ same bearer (why the second conjunct matters)

[`Bundles.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Bundles.lean)

```lean
/-- Same value labels do not imply the same bearer map (ch18 counterexample). -/
theorem P17_same_value_words_not_same_bearer_map :
    ∃ p q : ValueProfile 2 3,
      sameValueLabels p q ∧ ¬ sameBearerMap p q :=
  ⟨valueProfile0, valueProfile1, same_value_labels_profiles, different_bearer_map_profiles⟩
```

### Step 3 — Both MB3 inputs can hold while the export fails (bridge is load-bearing)

[`SpineModel.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/SpineModel.lean)

```lean
theorem MB3_independently_load_bearing :
    ∃ s : MB3ToySample,
      MB3ToyBundleTransport s ∧ MB3ToySameBearerMap s ∧ ¬ MB3ToyBearerTransport s := by
  refine ⟨⟨true, false⟩, trivial, rfl, ?_⟩
  decide
```

Toy reading: bundle transport and on-probe bearer agreement can both look fine while off-sample bearer transport still fails — MB3 is doing real work, not collapsing into MB2.

### How the pieces fit

```text
P15 (behavior ≠ bundle)     ──motivates──▶  MB2  (behavior ⇒ bundle)
P17 (labels ≠ bearer)       ──motivates──▶  MB3 needs SameBearerMap conjunct
MB3 axiom                   ──composes──▶   BundleTransport ∧ SameBearerMap ⇒ BearerTransport
MB3_independently_load_bearing            both inputs can hold, export still fails
```

P15 and P17 are **proved** (no `MB*`). MB3 is the explicit bridge that **composes** two checks. Nothing here proves MB2 or MB3 for real systems.

### Verify (section 2)

```lean
import AlignmentProofSpine

#print axioms AlignmentProofSpine.P15_same_policy_not_same_bundle_geometry
#print axioms AlignmentProofSpine.P17_same_value_words_not_same_bearer_map
#print axioms AlignmentProofSpine.MB3_independently_load_bearing
#print axioms AlignmentProofSpine.MB3_bearer_import   -- this is an axiom by declaration
```

Expect: P15, P17, and the independence toy are axiom-free; `MB3_bearer_import` is the labeled bridge.

### What section 2 is not

Does not prove bundle or bearer transport for frontier models. Does not derive MB3 from P15/P17 — the counterexamples show why the split is non-vacuous, not that the bridges hold. For a harder two-bridge composition story (shared measurement channels), see [`Chokepoint.lean`](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Chokepoint.lean) (MB6b vs MB8) — kept out of this handout on purpose.

---

## Pointers (compact)

| What | URL |
|------|-----|
| MB4 card | https://towards-alignment.com/cards/mb4-correction-legitimacy/ |
| MB2 card | https://towards-alignment.com/cards/mb2-bundle-identifiability/ |
| MB3 card | https://towards-alignment.com/cards/mb3-bearer-import/ |
| DebateGame.lean | https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Field/Finite/DebateGame.lean |
| Bundles.lean (P15, P17) | https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Bundles.lean |
| Core.lean (MB2, MB3) | https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Core.lean |
| SpineModel.lean (MB3 toy) | https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/SpineModel.lean |
| Correction.lean (§1 separation) | https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Correction.lean |
| Defeaters.lean (§1 MB4 toy) | https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Defeaters.lean |
| Bridge roster | [`drafts/lw-bridges-section.md`](lw-bridges-section.md) |
