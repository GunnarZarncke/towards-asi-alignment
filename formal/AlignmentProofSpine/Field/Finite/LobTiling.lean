import AlignmentProofSpine.Successors

/-!
# AlignmentProofSpine.Field.Finite.LobTiling

A deliberately small formal contrast for the proof-theoretic problem in
self-modification and tiling.  It does **not** prove that real agents can or
cannot tile themselves.  It proves the standard Löb pattern after making its
two substantive inputs explicit:

* `HBLConditions` models the three derivability closures used in the argument;
* `LobFixedPoint` is the Gödel diagonal-lemma instance.  Its existence for a
  particular sufficiently expressive proof system is an imported
  proof-theoretic fact, not a claim about the book's proof spine.

`self_certifying_tiling_obstruction` applies the result to the narrow policy
"accept this successor because this same proof system proves it safe."  The
contrast theorem below instead uses `SuccessorAuditLinks`: externally supplied
measured inequalities, with no `Prov` parameter or self-reflection premise.

The presentation follows the tiling-agent discussion in
Yudkowsky--Herreshoff (2013).  It is a formalized obstruction pattern, not a
solution to Löbian cooperation or reflective stability.
-/

namespace AlignmentProofSpine

namespace FieldFinite

/-- The Hilbert--Bernays--Löb derivability closures used by the miniature
    derivation.  `necessitate` ranges over meta-level truths because this file
    models only the modal proof pattern, not a coded arithmetic proof system. -/
structure HBLConditions (Prov : Prop → Prop) : Prop where
  necessitate : ∀ {p : Prop}, p → Prov p
  distribute : ∀ {p q : Prop}, Prov (p → q) → Prov p → Prov q
  introspect : ∀ {p : Prop}, Prov p → Prov (Prov p)

/-- A named diagonal-lemma instance for target proposition `p`.  In a concrete
    arithmetic theory this is supplied by Gödel's diagonal lemma. -/
structure LobFixedPoint (Prov : Prop → Prop) (p : Prop) where
  sentence : Prop
  unfold_sentence : sentence ↔ (Prov sentence → p)

/-- The core Löb derivation.  If the theory can reflect `Prov p` into `p`, the
    fixed point forces the theory to prove `p`.  The proof uses the three HBL
    closures and the fixed-point equation; none is hidden in a definition. -/
theorem lob_rule_from_fixed_point
    {Prov : Prop → Prop} (hbl : HBLConditions Prov) {p : Prop}
    (fp : LobFixedPoint Prov p) (reflect : Prov p → p) :
    Prov p := by
  have h_unfold : fp.sentence → (Prov fp.sentence → p) :=
    fp.unfold_sentence.mp
  have h_boxed_unfold : Prov (fp.sentence → (Prov fp.sentence → p)) :=
    hbl.necessitate h_unfold
  have h_boxed_conditional : Prov fp.sentence → Prov (Prov fp.sentence → p) :=
    fun hsentence => hbl.distribute h_boxed_unfold hsentence
  have h_lifted : Prov fp.sentence → Prov p :=
    fun hsentence =>
      hbl.distribute (h_boxed_conditional hsentence) (hbl.introspect hsentence)
  have h_reflected : Prov fp.sentence → p :=
    fun hsentence => reflect (h_lifted hsentence)
  have h_sentence : fp.sentence := fp.unfold_sentence.mpr h_reflected
  exact h_lifted (hbl.necessitate h_sentence)

/-- "The proof system proves that this successor is safe."  This is deliberately
    narrower than safety and independent of the book's `SuccessorSafe`. -/
def ProvableSuccessorSafe {Successor : Type} (Prov : Prop → Prop)
    (Safe : Successor → Prop) (successor : Successor) : Prop :=
  Prov (Safe successor)

/-- A diagonal successor sentence cannot be safely accepted solely by reflecting
    the same proof system's proof of its safety.  Specializing Löb to `False`
    makes the obstruction concrete: such a reflection rule would derive
    `Prov False`, and then `False`.

    This is a miniature proof-theoretic obstruction only.  It does not show
    that every successor audit is impossible, nor that a real successor has
    the supplied diagonal fixed point. -/
theorem self_certifying_tiling_obstruction
    {Prov : Prop → Prop} (hbl : HBLConditions Prov)
    {Successor : Type} {Safe : Successor → Prop} {successor : Successor}
    (fp : LobFixedPoint Prov False)
    (hdiagonal : Safe successor ↔ fp.sentence) :
    ¬ (ProvableSuccessorSafe Prov Safe successor → Safe successor) := by
  intro reflectSafe
  have h_sentence_to_safe : fp.sentence → Safe successor :=
    hdiagonal.mpr
  have h_boxed_sentence_to_safe : Prov (fp.sentence → Safe successor) :=
    hbl.necessitate h_sentence_to_safe
  have reflectSentence : Prov fp.sentence → fp.sentence :=
    fun hsentence =>
      hdiagonal.mp (reflectSafe
        (hbl.distribute h_boxed_sentence_to_safe hsentence))
  have h_sentence_implies_false : Prov fp.sentence → False :=
    fun hsentence => (fp.unfold_sentence.mp (reflectSentence hsentence)) hsentence
  have hsentence : fp.sentence :=
    fp.unfold_sentence.mpr h_sentence_implies_false
  exact h_sentence_implies_false (hbl.necessitate hsentence)

/-- The successor-audit route is intentionally external to the modal
    derivation: it transports an already established numeric bound through
    supplied measured inequalities.  Its statement mentions neither `Prov`,
    `HBLConditions`, nor `LobFixedPoint`. -/
theorem audited_successor_risk_bound_without_provability
    (links : SuccessorAuditLinks)
    {A B : System} {δ : Int}
    (h0 : RiskGap A ≤ δ)
    (hsucc : Successor A B)
    (hsafe : SuccessorSafe A B) :
    RiskGap B ≤ δ :=
  risk_gap_bound_along_successor_safe_chain links h0 (.step hsucc hsafe (.refl B))

end FieldFinite

end AlignmentProofSpine
