# Hostile telepaths

- **Date:** 2024-10-27
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/5FAnfAStc7birapMx/the-hostile-telepaths-problem
- **Source read:** full
- **TSA files consulted:** `chapters/ch10-strategic-opacity.tex`, `chapters/ch32-self-modeling-self-opacity.tex`
- **Keywords grepped:** telepath, thought visibility, internal state, mind-read, introspection, adversarial measurement, frame control, epistemic legibility

## Source ontology

Valentine names a distinct social game: another agent can *partially inspect your internals* and you do not trust they will not make things worse based on what they find. The new state variable is **thought visibility** (which channels of inner state are readable, at what fidelity, by whom). Solutions include Newcomblike self-deception (silo the inspectable channel—e.g. contract awareness around a fake self so the scanned part honestly one-boxes while the rest two-boxes), gaining independence, occlumency, exit, checking non-hostility, and jamming scans with privacy norms. The load-bearing claim is that self-deception is solving this game; you cannot drop it without another solution to the *same* problem. “Hostile telepath” is a role, not an identity.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** strategic opacity / “transparency is not unconditional” (ch10); self-modeling vs self-transparency vs self-honesty (ch32); nearby: CCI / false consent (ch26, ch29); goal laundering / cost of faking (ch40); adversarial measurement (ch39)
- **Overlap:** ch10 already asks what becomes opaque, *to whom*, under what incentives, and notes that a citizen hiding thoughts from a surveillance state is not the same as an AI hiding plans from an auditor. Deceptive alignment is named as strategic opacity around the training/evaluation gate—structurally close to Omega-C (the inspectable part is a sincere one-boxer). ch32 splits private self-control from correction-relevant exposure, including human rationalization as the same pattern.
- **Gap:** TSA’s object is the *optimizer hiding from auditors*. Valentine’s object is the *inspected party* facing imperfect mind-reading plus punishment of *internals, not just actions*. TSA can say “the system reduces detectability while preserving control”; it cannot, without stretching, say “thought visibility is the strategic variable” or treat Newcomblike self-deception (siloed inspectable consciousness) as a distinct solution class whose removal requires an alternative to the same game. That matters for CCI: an AI that reads affect and punishes wrong thoughts makes human correction itself a hostile-telepath channel. It also matters for interpretability that punishes internals: ch10 covers the opacity response, not the inner siloing that makes the scanned activations *locally sincere*.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** Alignment-relevant as a reverse of ch10’s auditor-side cut and as a CCI corruption mechanism, not as a rival to boundary/bundle/successor/basin. Absorbing it as “already strategic opacity” would drop the inspected-party variable and the self-deception-as-solution claim. Score 4 would require changing a TSA cut; this refines one. Score 2 would miss the CCI dual (humans under AI telepathy).
- **Ontology-stickiness risk:** High for pre-2024 training and for models that map this to “deception,” “privacy,” or “inner alignment.” TSA already *renames* most of the AI-side content as strategic opacity / self-honesty, so LLM-drafted prose is likely to treat Valentine as covered and still fail to see thought-visibility-as-variable and self-deception as a rational response to hostile inspection.
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already has optimizer-side strategic opacity and self-honesty; it still lacks thought-visibility as the inspected party’s state variable and Newcomblike self-deception as the solution that inspection-plus-punishment of internals produces.
