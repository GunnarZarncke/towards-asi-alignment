# Section de-segmentation: ch01, ch06, ch16

**Date:** 2026-06-22
**Trigger:** Reader feedback that Chapters 1, 6, and 16 read as over-segmented in the TOC ("very finely sliced," half-page beats, "restates one idea fifteen ways"). The reviewer was counting top-level `\section` headings (the TOC shows sections, not subsections).

## What was done

Reduced top-level `\section` counts by grouping related half-page beats under thematic parent sections and demoting the absorbed beats to `\subsection`. **All prose preserved**; this is heading-level restructuring plus a few short connective sentences. Two-level nesting only (no new subsubsections).

### ch01-wrong-object.tex (17 → 8 sections)

1. The First Mistake [+ A Toy Failure, Operational Definition as subsecs]
2. The Boundary Error [absorbs "Why Physical Boundaries…" as intro/subsec; "When the Model Is the Right Object" (was Counterexample) as subsec; deleted the redundant inner `\section{The Boundary Error}` header, now "The Error and Its Forms" subsec]
3. Alignment Becomes a Measurement Problem (was "From Alignment Target to Measurement Problem") [+ Bureaucracy, Composite AI Systems subsecs]
4. Boundary Discovery and Perturbation [+ The Role of Perturbation subsec]
5. Why This Matters for Superintelligence (kept)
6. A Decision-Relevant Test (kept) [+ An Imported-Ontology Audit subsec]
7. Limits and What This Chapter Establishes (was "Failure Modes of Boundary Framing") [+ What This Chapter Establishes subsec]
8. Summary (kept)

### ch06-agent-without-anthropomorphism.tex (17 → 9 sections)

1. The need for a colder definition [+ Why ordinary labels fail subsec]
2. **Building the Definition from Variables** (new umbrella; added one connective sentence) [Variables before objects, blanket as interface, Memory, Action, Goal-directedness as subsecs]
3. Degrees and Scales of Agency [Degrees of agency + Agents as scale-relative processes]
4. Two Examples: A Firm and an AI Service [firm + AI service subsecs]
5. Boundary errors (kept) · 6. Selfhood and agency (kept) · 7. From agent detection to alignment target [+ A minimal formal summary subsec] · 8. What Would Change This View (kept) · 9. Chapter conclusion (kept)

### ch16-value-bundle-model.tex (24 → 14 sections)

Kept as sections: Why a value model is needed [+ basic claim subsec]; Distinguishing values from nearby concepts; The four-part definition; Examples of candidate bundles; Value-bundle preservation; Failure modes; A minimal audit protocol; Open technical questions; Summary. New umbrellas:
- **Bundle Coordinates, and Why Scalar Accounts Fall Short** = bundle coordinates + why labels insufficient + why flat rewards fail
- **What Makes Value Learning Possible** = sample efficiency/low-dim + inconsistency + bundle inference + counterfactual tests
- **Values Across Cultures, Institutions, and Time** = across cultures + institutions + drift
- **Relation to moral philosophy** [+ Why this matters for artificial systems subsec]
- **Worked Examples** = honesty under pressure + autonomy versus welfare

## Non-obvious decisions

- Chose `\subsection` demotion over deleting headers so no content is lost and hierarchy stays legible. Kept nesting to two levels deliberately (avoided subsubsections) even where it meant landing at 14 sections for ch16 rather than a more aggressive ~9.
- Preserved every `\label` (they now attach to subsections); cross-refs still resolve. Renamed sections do not change labels, so `\ref` targets are unaffected.
- ch01: deleted one redundant `\section{The Boundary Error}` header; "Call this failure the boundary error." now follows the physical-boundaries motivation directly and still reads correctly.
- Kept the recurring "What Would Change This View" as its own section in ch06 for cross-chapter consistency.

## Verification

- `make check` passed; full `./build.sh` succeeded (exit 0). Build log scanned: no undefined/duplicate references, no LaTeX errors.

## Status / open items

- Title de-jargoning was committed earlier this session (7e00d20). **These section changes are NOT yet committed** (ch01, ch06, ch16, INDEX, this log are modified/untracked in the working tree). Commit when ready.
- Unrelated pre-existing change `drafts/conversation-summaries/2026-06-19-frontmatter-status-tldr.md` remains untouched/unstaged.
