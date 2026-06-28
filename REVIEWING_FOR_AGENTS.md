# Reviewing For Agents

Fast orientation for AI/coding agents asked to review or critique this manuscript without editing it.

## Scope

This file is for review-only sessions. Do not edit files unless the user explicitly asks for edits. Your job is to find risks, gaps, hidden assumptions, missing cross-references, unclear claim strength, and places where the manuscript hides its strongest results.

The book promises and often delivers deep results. Do not give a shallow review that treats it as a broad alignment essay and misses the machinery it has already built. That can disappoint the user because it may cause them to overlook or misrepresent the work.

## Fast Gist

The thesis: superintelligence alignment is the problem of preserving grounded, human-correctable value-bearing processes across capability growth, ontology shift, successor creation, and strategic multi-agent selection pressure.

The main layers:

- Boundary discovery: find the real optimizer, not just the visible model.
- Grounding viability: keep symbols, metrics, and correction signals connected to value-relevant reality.
- Value bundles: represent learnable value geometry without pretending values are scalar rewards.
- Bearer maps: preserve what values apply to, not only the words used for them.
- Transport: distinguish semantic, bundle, bearer, correction, and successor continuity.
- Correction-channel integrity: ensure human correction has uncaptured causal force, then stress-test that force under adversarial pressure.
- Successor constraints: require delegates, copies, and replacements to inherit the relevant invariants.
- Selection basins: make institutions select for correction-preserving systems.
- Adversarial verifiability: ask whether faking the safety signal is cheap.

The Lean proof spine checks logical dependencies and finite separations. It does not prove that deployed AI systems are safe. Bridges `MB1`-`MB9` are empirical or philosophical assumptions, not theorem conclusions.

## First Files To Read

Use this order unless the user gives a narrower target:

1. `frontmatter/introduction.tex`
2. `frontmatter/executive-overview.tex`
3. `tables/part-roadmap.tex`
4. `metadata/book.yml`
5. `formal/README.md`
6. The relevant chapter(s)
7. The newest entry in `drafts/conversation-summaries/INDEX.md`
8. `metadata/source-canon.md` if empirical backing or sibling-repo evidence matters

Check `metadata/book-stats.md` for token estimates; if the relevant source material exceeds your context window, use subagents or split the review by part, chapter, or layer rather than pretending to have read everything.

## Empirical Evidence And Related Repos

Do not judge empirical support only from the manuscript prose. The book is a synthesis over related project work and mirrored context extracts. Empirical validation is work in progress.

Start with:

- `metadata/source-canon.md` for the source map.
- `context/extracts/` for local markdown extracts of source PDFs.
- `references/internal-project-sources.bib` for cited project sources.

Related GitHub repositories to consult when empirical or source evidence is at issue:

- `https://github.com/GunnarZarncke/agency-detect`
  - Unsupervised agent discovery, operational agent boundaries, capability, intentional stance, attractor basins, successors.
- `https://github.com/GunnarZarncke/brain-to-values`
  - Value bundles, free-energy loops, unit-of-caring, consciousness / agency backbone.

In the local workspace, these are usually mirrored as sibling paths:

- `../agency-detect/docs/papers/`
- `../brain-to-values/papers/`

If you cannot access a related repo or source PDF, say so. Do not infer missing empirical support from memory.

## Gem Map

Look for the included gems before concluding a chapter is merely narrative.

- Boundary discovery: ch06-ch10
- Grounding viability: ch03, ch39b
- Value bundles: ch15-ch19b
- Bundle-geometry measurement and Goodhart pressure: ch19b
- Bearer maps: ch18, ch23, ch43
- Transport hierarchy: ch23
- Vector/status CCI: ch25; adversarial pressure tests: ch25b
- Existing-work subsumptions: ch07, ch20, ch24-ch27, ch38, ch39b
- Successor test: ch28-ch31
- Selection envelope and correction parasites: ch32-ch35
- Conductive artifacts and pivotal processes: ch35b
- Goal laundering and cost of faking: ch37, ch39b
- Value-update envelope: ch41-ch42
- Lean proof spine as dependency hygiene: `formal/`, Appendix I

## Existing-Work Subsumptions

The book often treats familiar proposals as projections, special cases, or separable subchannels of stronger invariants. Do not miss these as throwaway comparisons.

- Causal influence diagrams and incentive tests become boundary-relative under ontology choice and system-boundary choice.
- CIRL and reward inference become local projections of bundle, bearer, and correction preservation.
- Shutdown and interruptibility become one-bit correction projections.
- Low impact, relative reachability, AUP, and quantilization are separable from trajectory-level correction-channel integrity; see the ch25b stress tests.
- Christiano-style corrigibility becomes a dynamical correction invariant.
- Debate can preserve local truth while losing the judge's correction channel.
- Amplification can improve local supervision while failing global correction-channel contraction.
- ELK is a latent readout subchannel, not full correction uptake or successor preservation.

## Suggested Review Output

Use this structure unless the user asks for another format:

```md
## High-Severity Issues
- Path:
- Problem:
- Why it matters:
- Acknowledged by author: 
- Suggested fix:

## Medium-Severity Issues

## Claim-Strength / Bridge Issues

## Evidence / Source Gaps

## Residual Risk
```

## Anti-Patterns

- Do not flatten the book into standard alignment categories.
- Do not treat Lean as proving deployed safety.
- Do not treat CEV, corrigibility, ELK, debate, quantilization, low impact, shutdownability, or reward learning as identical to the book's invariants.
- Do not treat reviewer confusion as proof that the concept is empty; first check whether the relevant gem is under-signposted.
- Do not add speculative terminology.
- Do not skip the WWCTV sections; they often contain the claim-strength boundary.
- Do not overlook deep results just because they are embedded in a long narrative. The user expects reviewers to find the machinery, not only the surface thesis.
