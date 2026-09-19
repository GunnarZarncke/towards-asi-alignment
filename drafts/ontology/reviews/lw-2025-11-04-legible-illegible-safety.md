# Legible vs illegible safety problems

- **Date:** 2025-11-04
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/PMc65HgRFvBimEpmJ/legible-vs-illegible-ai-safety-problems
- **Source read:** full
- **TSA files consulted:** `chapters/ch36-parasites-correction-system.tex`, `chapters/ch37-alignment-attractor.tex`
- **Keywords grepped:** legibility, illegible, recognizability, decision-maker, safety theater, shallow legibility, timeline, accelerate

## Source ontology

Wei Dai isolates **recognizability of a safety problem to company leaders and government policymakers** as an independent axis (spectrum, treated as binary). A *legible* problem that still looks unsolved is, on his halt assumption, a deployment blocker; an *illegible* problem (obscure, hard to understand, or in a cognitive blind spot) is not, so leaders may deploy anyway. The new strategic relation is that **making an illegible problem highly legible is almost as good as solving it**, while working on already-legible problems has low or negative x-risk EV by bringing forward AGI/ASI deployment—analogous to capabilities work. Priority order: make-illegible-problems-legible > directly attacking either class. The unit is the *problem*, not a model, a claim-system, or a field. Comments contest the halt assumption and add Wentworth’s variant: progress on legible problems (e.g. RLHF) can *worsen* illegible ones, not merely burn timeline.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** legibility trap / shallow vs deep legibility (ch36); field \(L_t\) and “legibility to correction” (ch37); conductive artifacts / \(G_t\) (ch37–ch38); selection environment (ch34); goal laundering (ch40)
- **Overlap:** ch36 already says decision-makers need compressed artifacts and that fundability ≈ legibility ≉ risk relevance; shallow vs deep is “easy to repeat” vs “can the host predict failure.” ch37’s \(L_t\) is how much of the *work* outsiders can understand without the originating ontology, and treats illegibility as a priesthood risk. ch34/ch38 want properties and artifacts legible enough to enter institutional selection and change deployment.
- **Gap:** TSA’s “legibility” is overloaded onto artifacts, fields, and systems, not onto *problems as deployment gates*. It cannot, without stretching, say “this x-risk is unsolved but invisible to the people who could halt, so solving a visible proxy is net-negative.” The ch36 trap warns that *demand for* legibility selects shallow work; it does not isolate make-legible ≈ solve, nor the negative-EV claim about already-legible safety research. \(L_t\) tracks outsider-understandability of a research program, not whether a *danger* is in the decision-maker’s ontology. TSA’s selection chapters actually undercut the halt assumption: incentives can ignore even obvious problems.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The split is load-bearing for TSA’s own attractor story (\(L_t\), \(G_t\), conductive artifacts) and for how the book would prioritize making bridges and hostile-test failures *visible to deployers*, without competing with boundary, bundle, CCI, successor, or basin. A reverse-gap note would stop collapsing Wei Dai into the ch36 parasite or into \(L_t\). Score 4 would require changing a TSA cut; this is a research-strategy axis, not a replacement primitive. Score 2 would underweight that TSA already uses the *word* while missing the *gate*.
- **Ontology-stickiness risk:** High for pre-2025 training (Scott-statecraft, interpretability, “transparency,” Elizabeth’s 2022 epistemic legibility). TSA already includes Scott, \(L_t\), and shallow/deep, so the failure mode is rename-and-exclude: treating “legible vs illegible problems” as already covered, and losing the halt-gate, make-legible ≈ solve, and negative EV of visible safety work. LLM-drafted TSA prose is likely to treat “more legibility” as always-good (ch37 priesthood) and miss both the timeline effect and Wentworth’s “solving the visible problem can worsen the invisible one.”
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already names several “legibilities”; it still lacks Wei Dai’s axis that a safety *problem* can be unsolved-but-invisible to deployers, so making it recognizable can matter almost as much as solving it.
