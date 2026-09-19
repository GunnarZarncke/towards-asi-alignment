# Natural latents

- **Date:** 2023-12-27
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/dWQWzGCSFj6GTZHz7/natural-latents-the-math
- **Source read:** full
- **TSA files consulted:** `chapters/ch17-low-dimensional-value-learning.tex`, `reference/field-agendas/inter-agenda-term-glossary.md`
- **Keywords grepped:** natural latent, natural abstraction, conditionally independent, Wentworth, information bottleneck, ontology shift, shared information, mediation and redundancy

## Source ontology

Wentworth and Lorell give “natural abstractions” a latent-variable object. A latent \(\Lambda\) over parts \(X=(X_1,\ldots,X_n)\) is a **natural latent** when it satisfies both **naturality conditions**: *mediation* (the \(X_i\) are approximately independent given \(\Lambda\)) and *redundancy/insensitivity* (\(\Lambda\) is approximately recoverable from any part, or from \(X\) with any one \(X_i\) dropped). The conjunction is the unit: mediation alone is any screen-off; redundancy alone is fully shared information. Together they yield minimality among mediators, maximality among redundant latents, an approximately unique standard form (noise independent of \(X\) discarded), and approximate isomorphism of natural latents that are nearly deterministic functions of \(X\). They need not exist (too little data to pin the mediator). Approximation is in KL, with error that can scale with system size unless redundancy is strengthened.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** value bottleneck \(I(A;\phi\mid B,c)\leq\epsilon\) (ch17); NAH / `wentworth2023naturallatents` (ch17 summary + WWCTV); glossary **natural latents** vs **natural abstractions**; Markov-blanket / \(\epsilon\)-boundary CI (grep: ch03, ch06, ch07); transport / MB5 (glossary; appB sibling row)
- **Overlap:** ch17 already cites this paper, treats NAH as a more general claim than the operational bet that value-relevant control is low-dimensional, and says recoverable value-relevant natural latents would strengthen the sample-complexity story without replacing bearer maps, CCI, or adversarial measurement. The glossary already records mediation+redundancy and maps the object as a strict subset of NAH with only partial overlap on MB5 transport.
- **Gap:** The manuscript uses “natural latents / natural abstraction” as one field pointer. It does not import the *conjunction* as an operational test. The value bottleneck is a mediation-like sufficiency claim about actions given bundle coordinates, not redundancy of a world-latent across parts of \(X\). Boundary CI (internal \(\perp\) external \(\mid\) interface) is a different cut. TSA can say “shared latents would help transport”; it cannot, without stretching, say “this \(\Lambda\) is the unique (approx.) coordination point because it is both mediator and redund,” nor use non-existence of a natural latent as a diagnostic.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The split is load-bearing for not collapsing NAH into information-bottleneck compression, Markov blankets, or bundle geometry. ch17’s bound on what NAH does *not* buy is already correct; the missing piece is keeping the math object distinct from those nearby CIs. Score 4 would require changing a TSA cut (boundary, bundle, CCI, successor, basin); this does not. Score 2 would underweight that the book already *names* the term while the chapter prose still treats NAH and natural latents as interchangeable.
- **Ontology-stickiness risk:** High for pre-2023 training (NAH informal, IB, Markov blankets). TSA already includes the name and a glossary split, so the failure mode is rename-and-collapse: LLM-drafted TSA treating natural latents as already covered by \(I(A;\phi\mid B)\) or \(\epsilon\)-boundaries. Hostile test: restating naturality through the value bottleneck leaves redundancy, uniqueness, and non-existence on the floor.
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already cites natural latents as an NAH sibling; it still lacks the mediation-plus-redundancy unit that makes that sibling a distinct, sometimes non-existent, coordination object rather than another name for compression or a Markov blanket.
