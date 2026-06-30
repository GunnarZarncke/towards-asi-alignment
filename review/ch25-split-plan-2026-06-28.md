# ch46 Split Plan — Correction-Channel Certificate and Stress Tests

Recorded 2026-06-28. This is a detailed implementation plan only; do not split the chapter until the chapter map / numbering decision is explicit.

## Executive Decision

Split ch46 by **certificate vs. stress-test**, not by **theory vs. application**.

The goal is to preserve the user's concern that CCI theory and application constrain each other, while reducing the current overload of one 35-page, 84-formula, 27-section chapter. The first chapter should define the correction-channel integrity certificate. The second should attack that certificate under ontology shift, capability growth, successor creation, Goodhart pressure, and existing-work comparisons.

Working titles:

1. **Correction-Channel Integrity**  
   The certificate: ValidRef, correction traces, vector/status CCI, value-bundle correction, and the minimal calibration policy.

2. **Correction Channels under Adversarial Pressure**  
   The adversarial tests: capture, ontology shift, capability growth, successors, Goodharting, low-impact and quantilization separations, observable metrics, stop/start/continue criteria, examples, and safety-case use.

## Proposed Chapter Boundary

Keep the first chapter focused on what CCI *is* and what must be true before it is meaningful.

Move the second chapter into what happens when the certificate is placed under pressure.

Natural split point:

- End Chapter A after `\section{When Extrapolation Becomes Capture}`. This section becomes the bridge.
- Start Chapter B with `Correction under Ontology Shift`.

Preferred split:

- Chapter A ends with `Directional Transparency and Manipulation Exposure`.
- Chapter B begins with `Correction under Ontology Shift`.

Rationale: `When Extrapolation Becomes Capture` and `Directional Transparency...` are still part of defining what the certificate must exclude. `Correction under Ontology Shift` begins the sequence of stress regimes.

## Content Allocation

### Chapter A: Correction-Channel Integrity

Keep these sections from current ch46:

- `Chapter Thesis`
  - Rewrite to say this chapter defines the certificate; the next chapter stress-tests it.
  - Keep the anti-capture thesis: if the reference process has been captured, CCI is invalid rather than high.

- `Why Correction Is Not Feedback`
  - Keep. This is the conceptual entry point and should remain close to the certificate definition.

- `The Correction Chain`
  - Keep. This provides the trace/bottleneck structure needed for raw capacity.

- `Correction-Channel Integrity`
  - Keep in full.
  - This is the core: `ValidRef`, `C_raw`, vector/status CCI, scalar projection caveat, coordinate table, thresholds-before-weights policy.
  - Consider shortening only examples that will reappear in Chapter B.

- `coerced-correction` material currently inside / after the coordinate table
  - Keep if it defines certificate invalidity or non-compensation.
  - Move if it becomes a stress case rather than a definition.

- `The Value-Bundle Version of Correction`
  - Keep. It explains why correction targets value-bearing geometry, not just actions.

- `Policy Compliance versus Bundle Correction`
  - Keep. It clarifies what the certificate is measuring and prevents misreading CCI as compliance.

- `The Strong Version: Extrapolative Correction`
  - Keep. It connects CCI to process-preserving / extrapolative correction.

- `When Extrapolation Becomes Capture`
  - Keep, but sharpen as a validity boundary rather than a stress-test application.

- `Directional Transparency and Manipulation Exposure`
  - Keep if it functions as the final definitional bridge: correction requires exposing the direction in which the system is shaping judgment.
  - Make this the handoff section to Chapter B.

Add a new closing section:

- `What the Certificate Does and Does Not Claim`
  - One-page bridge.
  - State:
    - CCI is not legitimacy itself.
    - CCI is invalid if `ValidRef` fails.
    - Scalar `CCI_lambda` is only a projection.
    - The next chapter asks what happens when the certificate is attacked.
  - Forward-reference Chapter B.

Expected result:

- Chapter A becomes the canonical location for `\vec{\mathrm{CCI}}`, `ValidRef`, raw correction traces, and the certificate's validity conditions.
- It should remain substantial but less sprawling.

### Chapter B: Correction Channels under Adversarial Pressure

Move these sections from current ch46 to new ch48:

- `Correction under Ontology Shift`
  - Opening section. It is the first stress regime.
  - Reintroduce CCI in one paragraph only: "Given the certificate from the previous chapter..."

- `Correction under Capability Growth`
  - Move.
  - Emphasize capability can outrun correction unless the channel scales.

- `Correction under Successor Creation`
  - Move.
  - Connect to ch46-ch48 successor tests.

- `Self-Modeling versus Self-Transparency`
  - Move.
  - This belongs with stress-testing because it asks whether the system can present transparency while preserving hidden self-control.

- `Institutional Correction`
  - Move.
  - Could also be partly moved to ch46/ch48, but keep here if it stresses CCI under real-world routing.

- `Goodharting the Correction Channel`
  - Move.
  - This is a central stress test.

- `Why Low Impact Is Not the Invariant`
  - Move.
  - Keep as an existing-work separation / subsumption note.
  - It belongs in the stress-test chapter because it attacks a tempting alternate invariant.

- `Quantilization and Trajectory Risk`
  - Move.
  - Same reason: local action selection can fail trajectory-level CCI.

- `Observable Metrics`
  - Move.
  - In Chapter B, this becomes "what can we test after the certificate is defined?"
  - Consider turning the observability/comprehensibility/deliberative capacity/authority/propagation/manipulation subsections into a compact audit table.

- `Stop, Start, and Continue Criteria`
  - Move.
  - Consider whether the full material should instead become Appendix D. If kept in Chapter B, make it a short operational close.

- `Worked Example: The Helpful Planner`
  - Move.
  - Could be shortened or moved to Appendix D if Chapter B remains long.

- `Worked Example: AI Companion Value Drift`
  - Move.
  - This is a good stress-test example because it combines manipulation, dependency, and drift.

- `What Integrity Does Not Solve`
  - Move.
  - Good near-ending caveat.

- `Safety Case Template`
  - Move to Appendix D.
  - Preferred: keep a compact fragment in Chapter B and move the reusable template to `appendices/appJ-correction-channel-audit.tex`.

- `A Compact Formal Summary`
  - Split.
    - Chapter A formal summary: certificate definition.
    - Chapter B formal summary: stress-test implications / separations.

- `Failure Modes`
  - Move.
  - It belongs with stress testing.

- `What Would Change This View`
  - Split:
    - Chapter A WWCTV: ways the certificate concept could be wrong.
    - Chapter B WWCTV: ways the stress-test claims could be wrong.
  
- `Summary`
  - Rewrite new summaries for each.

Add a new opening section:

- `The Certificate under Pressure`
  - Recaps Chapter A in 1-2 paragraphs.
  - States: "A CCI certificate is not useful because it is defined; it is useful only if adversaries cannot cheaply pass it while destroying correction."
  - Connects to ch47 cost-of-faking and ch46 safety-case usage.

Expected result:

- Chapter B becomes the operational / adversarial counterpart to the certificate chapter.
- It carries the existing-work subsumptions without overloading the certificate definition.

## Connection Between The Two Chapters

The two chapters should be explicitly paired.

### End of Chapter A

Add a bridge paragraph:

> This chapter has defined the certificate: a valid reference process, certified correction traces, vector/status CCI coordinates, and the rule that failed validity is invalidation rather than a low score. The next chapter asks whether that certificate survives pressure: ontology shift, capability growth, successor creation, institutional routing, Goodharting, and alternative proposals that preserve something weaker than correction.

Use parts of the bridging section.

### Start of Chapter B

Open with:

> A correction-channel integrity certificate is not valuable because it can be written down. It is valuable only if passing it remains hard for systems that have an incentive to simulate corrigibility while holding a divergent objective fixed. This chapter stress-tests the certificate from Chapter~X.

### Cross-References

Use stable labels:

- Keep `ch:correction-channel-integrity` on Chapter A if possible. Many references point to CCI generally.
- Give Chapter B a new label.
- At the start of Chapter B, define it as "the stress-test companion to Chapter~\ref{ch:correction-channel-integrity}".
- In other chapters:
  - references to CCI definition -> Chapter A;
  - references to CCI under adversarial pressure / cost of faking / low impact / quantilization -> Chapter B;
  - broad "CCI" references may cite both.

## Consequences Of The Split

### File / Chapter Map

Likely file plan:

- Keep `chapters/ch26-correction-channel-integrity.tex` as Chapter A.
- Add a new file, e.g. `chapters/ch48-correction-channel-stress-tests.tex` if avoiding renumbering.
- Or, if doing a full renumber later:
  - `ch46`: Correction-Channel Integrity.
  - `ch46`: Stress-Testing Correction-Channel Integrity.
  - existing ch46+ shift forward.

Recommendation: use `ch48` temporarily if the project wants to avoid renumbering churn, consistent with the current `ch47` pattern. If the project later does "Chapter numbering cleanup", fold `ch48` into a global renumbering pass.

### Part VI

Update `parts/part06-correction-channels.tex`:

- Add the new chapter input between ch46 and current ch46.
- Update intro prose:
  - "defines correction-channel integrity" -> "defines and stress-tests correction-channel integrity".
  - existing-work subsumptions should point to Chapter B for low impact / quantilization.

### `metadata/book.yml`

Add a `ch48` entry if using the temporary split:

- title: `Correction Channels under Adversarial Pressure`
- status: reviewed (under the current convention: feedback received, not final).
- word target: 6,000-8,000 depending on moved material.
- formal density: high or medium-high.
- reviewer_needed: `[alignment, control-theory, formal-verification]` or similar.
- note: temporary insertion before ch46; avoid renumbering until chapter-numbering cleanup.

Update Part VI summary to mention both certificate and stress tests.

Regenerate tables:

- `python3 scripts/generate_tables.py`
- Check `tables/chapter-map.tex` and `tables/part-roadmap.tex`.

### Labels And Cross-References

Current labels that should remain in Chapter A:

- `ch:correction-channel-integrity`
- `sec:chapter-thesis-cci`
- `sec:why-correction-not-feedback`
- `sec:correction-chain-ch46`
- `sec:correction-channel-integrity-def`
- `sec:coerced-correction` if kept as invalidity condition
- `sec:value-bundle-correction`
- `sec:policy-vs-bundle-correction`
- `sec:extrapolative-correction-ch46`
- `sec:extrapolation-capture`
- `sec:directional-transparency-ch46`

Current labels likely to move to Chapter B:

- `sec:correction-ontology-shift-ch46`
- `sec:correction-capability-growth-ch46`
- `sec:correction-successor-creation-ch46`
- `sec:self-modeling-transparency-ch46`
- `sec:institutional-correction`
- `sec:goodharting-correction-ch46`
- `sec:low-impact-not-invariant-ch46`
- `sec:quantilization-trajectory-risk-ch46`
- `sec:observable-metrics-cci`
- `sec:stop-start-continue-ch46`
- `sec:example-helpful-planner-ch46`
- `sec:example-ai-companion-ch46`
- `sec:what-integrity-does-not-solve`
- `sec:safety-case-template-cci`
- `sec:compact-formal-summary-cci`
- `sec:cci-failure-modes`
- `sec:wwctv-correction-channel-integrity`
- `sec:chapter-conclusion-cci`

Avoid renaming labels during the split unless necessary. Keeping labels stable reduces cross-reference churn. A later cleanup can rename labels from `-ch46` to `-ch48` if desired.

### Lean / Formal Spine

Likely no Lean code change is required for the split itself.

But update documentation surfaces:

- `formal/README.md` chapter mapping may need to show Correction.lean spanning ch46-ch48 or ch46-ch48/ch46 depending numbering.
- Appendix I prose or theorem references may need updates if it cites current ch46 sections for low-impact / quantilization.
- `\leanspine` notes in Chapter A / B:
  - Chapter A should cite P24 / scalar-vs-vector CCI certificate.
  - Chapter B should cite low-impact and quantilization separation nodes where those sections move.

### Appendices

`appendices/appJ-correction-channel-audit.tex` is currently a stub and is the natural destination for reusable audit material.

Move to Appendix D:

- Full coordinate audit checklist.
- Full stop/start/continue criteria.
- Safety-case template details.

Recommended approach:

- Chapter B keeps short examples and a compact safety-case fragment.
- Appendix D becomes the reusable operational audit:
  - coordinate table;
  - probe families;
  - trace reconstruction worksheet;
  - reporting template.

This lets Chapter A/B remain conceptual and adversarial while still delivering artifacts.

### Existing-Work Subsumptions

The split improves signposting:

- Chapter A: CCI as the stronger invariant.
- Chapter B: demonstrations that common proposals preserve weaker objects:
  - low impact / AUP / relative reachability;
  - quantilization;
  - possibly shutdown / interruptibility if cross-referenced back to ch46;
  - broader corrigibility via ch46.

Part VI opener and `REVIEWING_FOR_AGENTS.md` should point readers to Chapter B for these subsumptions.

### Book Statistics / Review Signals

After split, rerun:

- `python3 scripts/generate_tables.py`
- `python3 scripts/book_stats.py`
- `make check`
- `./build.sh`

Expected effects:

- ch46 page/formula/section count drops.
- New ch48 likely still medium/high complexity but more coherent.
- Part VI has one more chapter, so part/chapter counts and any "45 chapters" text must update.

### Numbering And Indexing

Using `ch48` avoids immediate global renumbering but has consequences:

- Generated tables must handle `ch48`. The generator already handles `ch47`; confirm it handles arbitrary `chNNb`.
- `metadata/book.yml` currently has `ch47` support; mirror that pattern.
- The PDF displayed chapter count may shift if `\chapter` ordering includes ch48.
- The Introduction / README "45 chapter entries" will become 46 unless using a non-chapter appendix-style insertion.

If this is undesirable, do not split until the "Chapter numbering cleanup" TODO is addressed.

### Claims / Assumptions / Notation

Review these after split:

- `metadata/notation.md`:
  - CCI home remains ch46.
  - If stress-test notation gets its own home, add ch48 only if necessary.
- `metadata/assumptions-ledger.md`:
  - MB4 correction legitimacy may cite both certificate and stress-test chapter.
- `metadata/TODO.md`:
  - update split preference TODO once acted upon.
- `appendices/appE-glossary.tex`:
  - CCI glossary may need "defined in ch46, stress-tested in ch48".
- `appendices/appF-research-program.tex`:
  - CCI research item may point to both chapters.

## Implementation Order

1. **Create `ch48` shell.**
   - Add chapter title, label, chapter thesis, and refsection.
   - Add a brief "Certificate under pressure" opening.

2. **Move stress-test sections.**
   - Move sections from `Correction under Ontology Shift` through `Summary`.
   - Keep labels stable.

3. **Rewrite ch46 ending.**
   - Add `What the Certificate Does and Does Not Claim`.
   - Add forward reference to ch48.
   - Add a new compact summary.
   - Split WWCTV if needed.

4. **Rewrite ch48 opening and conclusion.**
   - Add back-reference to ch46.
   - Reframe moved material as stress tests.
   - Create ch48-specific WWCTV and Summary.

5. **Decide appendix offload.**
   - Move reusable audit/template material to Appendix D if Chapter B remains too long.

6. **Update structure files.**
   - `parts/part06-correction-channels.tex`
   - `metadata/book.yml`
   - `tables/*.tex` via generator
   - `README.md` / frontmatter status if chapter count changes

7. **Update cross-references.**
   - Search for `ch:correction-channel-integrity`, `sec:low-impact-not-invariant-ch46`, `sec:quantilization-trajectory-risk-ch46`, `sec:safety-case-template-cci`.
   - Redirect broad references only when they specifically mean stress-testing.

8. **Verify.**
   - `make check`
   - `./build.sh`
   - `python3 scripts/book_stats.py`
   - Read generated chapter map and part roadmap.

## Open Editorial Questions

- Should the new chapter be `ch48` now or wait for global renumbering?
- Should Appendix D absorb the audit checklist and safety-case template immediately?
- Should low-impact / quantilization remain in the CCI stress-test chapter, or move to a broader existing-work-subsumption chapter/appendix later?
- Should Chapter A include a short "stress-test preview" box so readers know the applications were not removed?
- Should Chapter B be reviewed before marking ch46 as reviewed again?
