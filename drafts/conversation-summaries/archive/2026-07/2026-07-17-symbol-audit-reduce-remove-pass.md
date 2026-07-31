# 2026-07-17 — Symbol-audit reduce/remove pass (ch13, ch14, ch35, ch15, ch19)

## Trigger

Following the 2026-07-15 symbol-contribution audit (`drafts/symbol-contribution-audit-2026-07-15.md`), the user asked to apply five specific recommended actions and review surrounding context, epistemic status, and WWCTV sections:

- ch13 seven sub-loss displays (reduce)
- ch14 duplicate BIQ components (reduce)
- ch35 ICI stack (reduce)
- ch15 LHCV neuroscience prior (reduce)
- ch19 χ_i (remove)

## Done

- **ch13** (`chapters/ch13-coordination-bottleneck.tex`): demoted the eight individually labeled sub-loss/threshold displays (latency, bandwidth, translation map + distortion, authority, incentives, trust, irreversibility) from numbered `equation` blocks to inline math. Kept the seven-term sum (`eq:coordination-losses`) and the bottleneck definition (`eq:coordination-bottleneck`) as the only displays in that section. Confirmed none of the removed labels were `\eqref`'d elsewhere before deleting them.
- **ch14** (`chapters/ch14-intelligence-deepens-misalignment.tex`): collapsed the restated BIQ competence functional (`eq:competence-functional` + its `align` breakdown of $I_{\mathrm{pred}}, I_{\mathrm{ctrl}}, H(I_t), S_X$) into a single cross-reference sentence pointing at ch11's canonical `eq:biq`. Fixed the one internal reference (`Eq.~\ref{eq:competence-functional}` → prose + `Eq.~\ref{eq:biq}`). This also incidentally cleaned up the `$\mathcal{S}$ (prose) vs $S_X$ (eq.)` naming collision the audit flagged, since the informal `$\mathcal{S}$` sentence was part of the deleted paragraph.
- **ch35** (`chapters/ch35-multi-agent-strategic-coupling.tex`): trimmed the acausal-trade / $P_{\mathrm{meta}}$ formal stack inside "Inferential Coupling and Acausal Trade" (~125 lines → ~80 lines, close to the audit's suggested ~40% cut of §203–327). Removed the fully redundant mapping table (`tab:inferential-coupling-uad-mapping-ch35`) and merged the "Meta-prior over inference functions," "The crucial move…," and "Full acausal-trade equilibrium" paragraphs into one shorter passage; moved the fixed-point equilibrium equations into a footnote. Kept: the "Gem" framing paragraph, the four-case taxonomy, the `\leanspine{proof}{inferential-ici}{...}` anchor, the detector formula and threshold, and all WWCTV/"why it bites"/"not adversarially verifiable" caveats untouched (they reference $\epsilon_{ij}$, $D_i$ downstream and still resolve).
- **ch15** (`chapters/ch15-values-compressed-control.tex`): reduced the LHCV loop→hub→control→value pipeline's mechanistic equations ($s_h(t)=\sigma_h(\sum w_{ih}\|\epsilon_i\|)$, policy form with $\lambda_h c_h(t)\phi_h$, softmax readout $P(v_k\mid\ldots)$) to prose description of the three compression steps, keeping only the qualitative pipeline and the $k$-dimensionality claim. Added a forward cross-reference to ch21 (`ch:reward-to-bundle-inference`), which already restates the same $\epsilon_i(t)\to s_h(t)\to c_h(t)\to B(t)$ chain operationally for its IRL-tractability argument — confirming the ch15 formulas were duplicated, not novel.
- **ch19** (`chapters/ch19-tradeoffs-bundle-geometry.tex`): removed $\chi_i$ ("characteristic policy-response pattern") as an undefined placeholder symbol in two places — the initial value-bundle triple `$(B_i,\Phi_i,\chi_i)$` (now a pair, with a forward-reference to the formally defined Jacobian $J_i$) and the substrate-transfer role-preservation chain (now uses $J_i$/$J'_i$ throughout instead of $\chi_i$/$\chi'_i$). This eliminates the duplicate-of-the-Jacobian symbol the audit flagged while keeping the substrate-transfer argument's structure intact.
- **metadata/notation.md**: fixed the $\mathrm{ICI}_{ij}$ home from `ch48` to `ch35` (one row of the audit's larger "notation-index drift" list; only this row was touched since it directly relates to the ch35 edit — the rest of that drift list is unaddressed).
- Verified: `python3 scripts/check_bibliography_summaries.py` passes; no dangling `\ref`/`\eqref`/`\label` left for any removed label (`eq:latency-bottleneck`, `eq:bandwidth-bound`, `eq:translation-map`, `eq:translation-distortion`, `eq:authority-information`, `eq:truthful-signaling`, `eq:trust-weighted-information`, `eq:reversibility-correction`, `eq:competence-functional`, `tab:inferential-coupling-uad-mapping-ch35`, `\chi_i`).
- Checked each touched chapter's `epistemicstatus` and "What Would Change This View" sections — none referenced the removed/reduced formalism directly, so none required prose changes beyond the reductions themselves.

## Decisions

- Where a symbol's *concept* is reused downstream (ch35's `\leanspine` anchor; ch15's ICI/LHCV pipeline referenced by ch17/ch21/ch48; ch19's Jacobian), kept the concept and only demoted or removed duplicate/undefined formal machinery, rather than deleting cross-chapter dependencies.
- For ch19's $\chi_i$, chose to substitute $J_i$ (the chapter's own later-defined Jacobian) rather than delete the "policy-response pattern" idea outright, since the *idea* (does activating a bundle change consent-seeking, disclosure, etc.) is used in the substrate-transfer argument — only the redundant undefined symbol was removed, matching "remove" at the symbol level without gutting the surrounding prose.
- Left the broader "notation-index drift" list (propagation checklist item 1) and other audit items (ch13 $B_i\to K_i$ bug, ch33 $B(A_t)\to K(A_t)$, etc.) untouched — out of scope for this specific request; only the ICI_ij home row was fixed since it was directly entangled with the ch35 edit.

## Open / next

- Remaining propagation-checklist items from the audit (notation.md ch25–ch40 homes, ch13 $B_i\to K_i$, ch33 $B(A_t)\to K(A_t)$, $J\to g_B$/$H\to H_B$ unification in ch19, $W_t$ collision in ch25, etc.) are still open — not requested this session.
- The 5 unresolved `\leanspine{}` anchors (`P34A`, `P34K`, `P35M`, `P38H`, `inferential-ici`) noted in the 2026-07-16 symbol-formula-graph work are still unresolved; `inferential-ici` in particular is inside the ch35 section trimmed this session, so worth checking whether the corresponding Lean declaration needs adding or renaming.
- No LaTeX build was run this session (text-only edits, no new packages/figures); recommend `./build.sh` before the next PDF release to confirm no downstream breakage.

## Key paths

- `drafts/symbol-contribution-audit-2026-07-15.md` — source audit driving this pass.
- `chapters/ch13-coordination-bottleneck.tex`, `ch14-intelligence-deepens-misalignment.tex`, `ch15-values-compressed-control.tex`, `ch19-tradeoffs-bundle-geometry.tex`, `ch35-multi-agent-strategic-coupling.tex` — edited chapters.
- `metadata/notation.md` — one row fixed (ICI_ij home).

## Commits

- None (no commit requested this session).
