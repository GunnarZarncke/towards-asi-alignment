# ch35 Split Plan — Alignment Attractor and Conductive Artifacts

## Executive Decision

Split ch35 by **alignment-attractor theory vs. artifact / conductivity / pivotal-process governance**.

The current chapter is 32 pages with 26 sections and 39 subsections. It contains two strong but different chapters:

- the theory of alignment attractors and false attractors;
- the practical program for creating high-conductivity artifacts, governance demand, safety cases, dashboards, and role-specific adoption.

Titles:

1. **The Alignment Attractor**  
   Theory of structural non-conductance, minimal attractor dynamics, percolation, feedback loops, false attractors, and what the attractor attracts.

2. **Conductive Artifacts and Pivotal Processes**  
   Artifact conductivity, pivotal-process governance, Monday-morning operationalization, metrics, safety-case use, examples, funder/lab/regulator/public roles, and open failure modes.

## Proposed Chapter Boundary

Preferred split point:

- Chapter A ends after `\section{False Attractors}`.
- Chapter B begins with `\section{Pivotal Process as Basin Transition}`.

Rationale:

- Through `False Attractors`, the chapter defines the attractor problem: why alignment does not automatically conduct through institutions, what feedback loops could create a basin, and what counterfeit basins look like.
- `Pivotal Process as Basin Transition` starts the "what do we build / govern / fund" answer.
- This split preserves a clean question transition:
  - Chapter A: what is the attractor and what can go wrong?
  - Chapter B: what artifacts and processes can move society into the better basin?

## Content Allocation

### Chapter A: The Alignment Attractor

Keep these sections from current ch35:

- `The Problem of Structural Non-Conductance`
  - Keep as opener.
  - This names why good technical work does not automatically change institutions.

- `A Minimal Model`
  - Keep.
  - This is the theoretical core.

- `Artifact Conductivity`
  - Split.
  - Keep only the short conceptual definition needed for the theory chapter.
  - Move detailed artifact design criteria to Chapter B.
  - If moving the whole section would make Chapter A too abstract, retain 1-2 pages as "conductivity as a state variable" and make Chapter B responsible for artifact construction.

- `Percolation of Alignment Practice`
  - Keep.
  - This is still attractor theory.

- `The Attractor as a Feedback System`
  - Keep.
  - Keep subsections:
    - `research-to-artifact-ch35`;
    - `artifact-to-evidence-ch35`;
    - `evidence-to-funding-ch35`;
    - `funding-to-capacity-ch35`;
    - `governance-to-demand-ch35`;
    - `legibility-to-correction-ch35`.
  - These define the feedback loop.

- `What the Attractor Attracts`
  - Keep.
  - This clarifies the target basin.

- `False Attractors`
  - Keep.
  - Keep subsections:
    - `reputation-attractor-ch35`;
    - `compliance-attractor-ch35`;
    - `benchmark-attractor-ch35`;
    - `centralization-attractor-ch35`;
    - `transparency-absolutism-attractor-ch35`.
  - These belong in the theory chapter as basin confusions.

Add a new closing section:

- `Why Attractor Theory Is Not Enough`
  - Short bridge.
  - State that a theory of the basin does not by itself create conductance.
  - The next chapter asks which artifacts, thresholds, safety cases, and governance roles make the basin reachable.

### Chapter B: Conductive Artifacts and Pivotal Processes

Move these sections from current ch35:

- `Pivotal Process as Basin Transition`
  - Opening section.
  - It ties directly to governance, artifact strategy, and basin transition.

- `What Makes an Artifact High-Conductivity?`
  - Move.
  - This becomes the central design section.
  - Keep subsections:
    - `operational-artifact-ch35`;
    - `role-specific-artifact-ch35`;
    - `failure-modes-attached-ch35`;
    - `changes-incentives-ch35`;
    - `updateable-artifact-ch35`;
    - `ontology-light-meaning-ch35`.

- `The Monday-Morning Version`
  - Move.
  - This is execution guidance.
  - Keep subsections:
    - `step1-decision-graph-ch35`;
    - `step2-artifact-per-decision-ch35`;
    - `step3-attach-threshold-ch35`;
    - `step4-translation-loss-ch35`;
    - `step5-feedback-loop-ch35`.

- `Metrics for the Attractor`
  - Move.
  - This section operationalizes the theory.
  - Keep subsections:
    - `artifact-half-life-ch35`;
    - `decision-influence-ch35`;
    - `correction-latency-metric-ch35`;
    - `cross-role-adoption-ch35`;
    - `goodhart-resistance-metric-ch35`;
    - `plural-correction-metric-ch35`.

- `Attractor Design Principles`
  - Move.
  - This is artifact/governance design.

- `How This Relates to Superintelligence`
  - Move or split.
  - Preferred:
    - Chapter A gets a short paragraph on why attractors matter under fast capability growth.
    - Chapter B keeps the detailed relation because the practical question is how artifacts survive superintelligent pressure.

- `A Safety-Case View`
  - Move.
  - This belongs with operational artifacts and review.

- `A Worked Example: Correction-Channel Dashboard`
  - Move.
  - Strong example for Chapter B.

- `A Worked Example: Successor Certification`
  - Move.
  - Strong example for Chapter B.

- `Why Centralization Is Insufficient`
  - Move.
  - This is a governance consequence of artifact design.

- `The Role of Funders`
  - Move.

- `The Role of Labs`
  - Move.

- `The Role of Regulators and Auditors`
  - Move.

- `The Role of Public Narratives`
  - Move.

- `Open Failure Modes`
  - Move.
  - This is best placed after the practical program.

- `What Success Looks Like`
  - Split.
    - Chapter A gets "what a real attractor would attract" and false-attractor contrast.
    - Chapter B keeps the success conditions for implementation.

- `Connection to Later Chapters`
  - Do not make a separate section but distribute across the sections of the chapters or include in the summaries as appropriate.
  - Connect the artifact chapter to safety cases and civilizational limits.

- `What Would Change This View`
  - Split.
    - Chapter A WWCTV: evidence that basin dynamics / conductance framing is misleading.
    - Chapter B WWCTV: evidence that artifacts cannot materially alter selection / governance incentives.

- `Summary`
  - Rewrite for both ChapterS.

Add a new opening section:

- `From Basin Theory to Conductive Artifacts`
  - Recap Chapter A in one page.
  - State that attractor theory only matters if it changes the survival and adoption of safety-relevant artifacts.

## Connection Between The Two Chapters

### End of Chapter A

Add a bridge paragraph:

> The attractor picture explains why alignment-relevant work can fail to conduct: it can be too abstract, too role-unspecific, too easy to counterfeit, too slow, or too weakly connected to the decisions that allocate deployment mass. But the theory is only useful if it changes what researchers, funders, labs, auditors, regulators, and publics build and demand. The next chapter turns the attractor into an artifact program.

### Start of Chapter B

Open with:

> The previous chapter described the alignment attractor as a basin of feedback among research, artifacts, evidence, funding, governance demand, legibility, and correction. This chapter asks what can make that basin reachable: high-conductivity artifacts, pivotal processes, decision thresholds, safety cases, and role-specific adoption paths.

### Cross-References

Use stable labels:

- Keep `ch:alignment-attractor` on Chapter A.
- Give Chapter B a new label, e.g. `ch:conductive-artifacts-pivotal-processes`.
- References to attractor theory / false attractors -> Chapter A.
- References to artifacts / conductivity / pivotal process / dashboards / funders / labs / regulators -> Chapter B.

Avoid renaming section labels during the split unless necessary. Current `-ch35` labels can stay stable even if moved.

## Consequences Of The Split

### File / Chapter Map

Likely file plan:

- Keep `chapters/ch35-alignment-attractor.tex` as Chapter A.
- Add `chapters/ch35b-conductive-artifacts-pivotal-processes.tex` as Chapter B if avoiding renumbering.

Alternative:

- Wait for global chapter renumbering and make Chapter B the new ch36, shifting current ch36+.

Recommendation: use temporary `ch35b` only if the project is comfortable with another `b` chapter before global numbering cleanup. Otherwise, keep this as a plan and execute during a chapter-map revision pass.

### Part VIII

Update `parts/part08-attractor-basins.tex`:

- Insert Chapter B after ch35.
- Update the part intro so it distinguishes:
  - selection and preservation envelopes (ch32);
  - strategic coupling (ch33);
  - correction parasites (ch34);
  - attractor theory (ch35);
  - conductive artifacts / pivotal process governance (ch35b).

The current part gem sentence already points to preservation envelope and correction parasites. Consider adding a second sentence:

> The payoff is the conductive-artifact program: make safety artifacts hard to counterfeit, useful to decision-makers, and durable enough to change the selection environment.

### `metadata/book.yml`

Add `ch35b` if using temporary numbering:

- title: `Conductive Artifacts and Pivotal Processes`
- status: reviewed (under the current convention: feedback received, not final)
- word_target: 7000-9000
- formal_density: medium
- reviewer_needed: `[alignment, governance, institutional-design]`
- note: inserted after ch35; avoid renumbering until chapter-numbering cleanup.

Regenerate tables:

- `python3 scripts/generate_tables.py`

### Labels And Cross-References

Labels likely to remain in Chapter A:

- `ch:alignment-attractor`
- `sec:structural-non-conductance-ch35`
- `sec:minimal-model-ch35`
- `sec:percolation-alignment-practice-ch35`
- `sec:attractor-feedback-system-ch35`
- `sec:research-to-artifact-ch35`
- `sec:artifact-to-evidence-ch35`
- `sec:evidence-to-funding-ch35`
- `sec:funding-to-capacity-ch35`
- `sec:governance-to-demand-ch35`
- `sec:legibility-to-correction-ch35`
- `sec:what-attractor-attracts-ch35`
- `sec:false-attractors-ch35`
- `sec:reputation-attractor-ch35`
- `sec:compliance-attractor-ch35`
- `sec:benchmark-attractor-ch35`
- `sec:centralization-attractor-ch35`
- `sec:transparency-absolutism-attractor-ch35`

Labels likely to move to Chapter B:

- `sec:pivotal-process-ch35`
- `sec:high-conductivity-artifact-ch35`
- `sec:operational-artifact-ch35`
- `sec:role-specific-artifact-ch35`
- `sec:failure-modes-attached-ch35`
- `sec:changes-incentives-ch35`
- `sec:updateable-artifact-ch35`
- `sec:ontology-light-meaning-ch35`
- `sec:monday-morning-version-ch35`
- `sec:step1-decision-graph-ch35`
- `sec:step2-artifact-per-decision-ch35`
- `sec:step3-attach-threshold-ch35`
- `sec:step4-translation-loss-ch35`
- `sec:step5-feedback-loop-ch35`
- `sec:metrics-attractor-ch35`
- `sec:artifact-half-life-ch35`
- `sec:decision-influence-ch35`
- `sec:correction-latency-metric-ch35`
- `sec:cross-role-adoption-ch35`
- `sec:goodhart-resistance-metric-ch35`
- `sec:plural-correction-metric-ch35`
- `sec:attractor-design-principles-ch35`
- `sec:lower-cost-ch35`
- `sec:raise-benefit-reporting-ch35`
- `sec:increase-probability-decisions-ch35`
- `sec:improve-semantic-alignment-ch35`
- `sec:keep-correction-channels-ch35`
- `sec:relation-superintelligence-ch35`
- `sec:safety-case-view-ch35`
- `sec:correction-channel-dashboard-ch35`
- `sec:successor-certification-example-ch35`
- `sec:centralization-insufficient-ch35`
- `sec:role-funders-ch35`
- `sec:role-labs-ch35`
- `sec:role-regulators-auditors-ch35`
- `sec:role-public-narratives-ch35`
- `sec:open-failure-modes-ch35`
- `sec:too-slow-ch35`
- `sec:outcompeted-ch35`
- `sec:captured-ch35`
- `sec:become-illegible-ch35`
- `sec:become-shallow-ch35`
- `sec:optimize-for-artifacts-ch35`
- `sec:what-success-looks-like-ch35`
- `sec:wwctv-alignment-attractor`
- `sec:summary-ch35`

### Downstream Consequences

Review and potentially update:

- `chapters/ch32-selection-environment.tex`
  - References to artifacts that rotate selection should likely point to Chapter B.

- `chapters/ch34-parasites-correction-system.tex`
  - Parasite-countermeasure references may point to Chapter B.

- `chapters/ch36-passive-observation.tex`
  - If ch36 discusses observation artifacts, cite Chapter B.

- `chapters/ch40-...` / safety-case chapters
  - Safety-case references should point to Chapter B's `A Safety-Case View`.

- `frontmatter/introduction.tex`
  - The "How to Read" roadmap may need the Part VIII sentence to include both attractor theory and conductive artifacts.

- `REVIEWING_FOR_AGENTS.md` and `llms.txt`
  - If they mention the alignment attractor, add "conductive artifacts / pivotal processes" after the split so reviewers do not miss the practical program.

- `metadata/TODO.md`
  - Mark ch35 split plan as drafted.

## Implementation Order

1. Create new chapter shell.
2. Move `Pivotal Process as Basin Transition` and all later implementation sections to Chapter B.
3. Decide whether `Artifact Conductivity` stays in Chapter A, moves to Chapter B, or is split into definition vs. design criteria.
4. Rewrite Chapter A close and Chapter B open.
5. Split WWCTV, success, summary, and superintelligence relation sections.
6. Update Part VIII, `metadata/book.yml`, generated tables.
7. Search/review cross-references to ch35 and moved section labels.
8. Run:
   - `python3 scripts/generate_tables.py`
   - `make check`
   - `./build.sh`
   - `python3 scripts/book_stats.py`

## Open Editorial Questions

- Should `Artifact Conductivity` be split or moved wholesale?
- Should `Pivotal Process as Basin Transition` open Chapter B or close Chapter A?
- Should dashboards and successor certification remain in Chapter B, or should one worked example move to an appendix?
- Does Part VIII become too long after the split, or is that acceptable because the new chapter is a practical culmination of the part?
