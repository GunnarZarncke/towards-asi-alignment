# Claim Checklist

For each chapter under review:

- [ ] Chapter thesis is stated in one paragraph
- [ ] Decision relevance is explicit
- [ ] Plain-language model precedes formal model
- [ ] At least one worked example
- [ ] At least one counterexample or failure mode
- [ ] "What would change this view" section present
- [ ] Summary has 5–8 bullets
- [ ] Major claims added to `metadata/claims-ledger.md`
- [ ] Intro-claim tag (`Claim~\ref{claim:…}`) or ledger ID noted in part opener / first chapter of part where applicable
- [ ] Major assumptions added to `metadata/assumptions-ledger.md`
- [ ] Claim strength labeled (established / plausible / speculative / limit)
- [ ] References span at least three categories where relevant

## Lenses on a proposed solution (Kosoy 2026)

Vanessa Kosoy, [The Alignment Problem: Computer Science Meets Analytic Philosophy](https://www.lesswrong.com/s/iKtxSpGeRSwdyNZd6/p/Emp7awtxsYn8MusNq) (18 October 2026). She offers these as lenses that must be applied to any proposed solution, including this book. A review of a safety claim that does not say how the claim handles each applicable lens is incomplete. Record the answer, or mark the lens open. A nearby chapter using related words does not discharge a lens.

- [ ] **Hypercomplexity.** Does the passage specify preferences or a world model outside a narrow domain? If it does, where does learning take over, and what happens under Goodhart pressure once the domain is left?
- [ ] **Alignment grounding.** What is the type of the learned object (preferences, beliefs, decisions)? What data is supposed to ground it? Does the target stay fixed while the policy can change the user's values?
- [ ] **Alignment convergence.** Do the guarantees assume a reset, reachable states, or a later try? Where does an irreversible mistake (first critical try, successor, death) void the bound? Home for this book's concession: [Ch. 44](https://towards-alignment.com/cards/chapters/ch44/).
- [ ] **Side-channel resilience.** Do the guarantees and tests refer only to the intended interface? What happens if benign interface behavior coexists with a malign side channel, including an internal computation that copies an unaligned successor? Home for this book's concession: [Ch. 10](https://towards-alignment.com/cards/chapters/ch10/).

On this book, convergence and side channels are the two lenses that bite existing claims. Grounding restates open bearer, value-change, and nonrealizability work. Hypercomplexity restates the refusal to hand-specify a complete utility.
