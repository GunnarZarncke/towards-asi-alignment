# Book statistics

Generated: 2026-10-22 09:20 UTC

## Summary

- **PDF pages** (built): 1,549
- **Page spans** source: book.toc (+ book.log for PDF total)
- **Frontmatter files**: 7
- **Chapters**: 48
- **Appendices**: 10
- **Contributing files (PDF build)**: 123 (88 TeX, 10 `.bib`, 25 figures)
- **All book sources (PDF + Lean)**: 187 files
- **Body words** (frontmatter + chapters + appendices): 310,490
- **All counted TeX words** (+ metadata/tables): 313,079
- **Book text sources, no `context/`** (TeX + `.bib` + Lean): 162 files, 483,428 words, ~929,501 LLM tokens
- **Context source extracts only** (`context/extracts/*.md`): 23 files, 68,831 words, ~121,655 LLM tokens
- **Book text sources + context extracts**: 185 files, 552,259 words, ~1,051,156 LLM tokens
- **TeX LOC (body)**: 41,647 code lines (41,700 non-blank, 49,025 total)
- **TeX LOC (all counted)**: 42,232 code lines (42,348 non-blank, 49,718 total)
- **Body PDF pages** (sum of TOC spans): 1,472
- **Unique citation keys used**: 324
- **Bibliography entries** (all `.bib` files): 557
- **Uncited bibliography entries**: 233
- **Unique anchors** (`\label{...}`): 1,995
- **Display math blocks**: 1,985
- **Figures / tables**: 25 / 0
- **Sections / subsections**: 875 / 813
- **TODO markers**: 2
- **Lean modules**: 64
- **Lean LOC**: 11,560 code lines (11,735 non-blank, 14,053 total)
- **Lean spine P nodes** (unique `P*` IDs): 50 (62 named theorems/lemmas)
- **Lean spine MB bridges** (unique `MB*` axioms): 15
- **Lean declarations**: 642 theorems, 0 lemmas, 488 defs, 140 structures, 173 axioms
- **Reading the axiom count**: only the `MB*` bridges and `S07`/`S10` are epistemic assumptions; the other `axiom` declarations are abstract carriers, typed predicates, certificate adapters, defeater signals, and source-cited field handles (see the Lean dependency spine appendix, *How to read the axiom count*). Bridge footprints per headline theorem: `formal/axiom-ledger.json`.
- **\leanspine cross-refs** in manuscript: 132 (64 distinct node IDs cited)

## Source material extracts

Markdown extracts in `context/extracts/` are the book-local readable copies of source PDFs.
Token counts are approximate LLM-token estimates using `ceil(UTF-8 bytes / 4)`, not a model-specific tokenizer.
Combined text-source total including book sources and context extracts: 185 files, 552,259 words, ~1,051,156 LLM tokens.

| File | Words | Approx. tokens | Chars | Lines |
| --- | --- | --- | --- | --- |
| context/extracts/acausal-trade-uad-formalization.md | 1,210 | 2,024 | 7,929 | 248 |
| context/extracts/access-uad.md | 3,944 | 6,451 | 25,281 | 886 |
| context/extracts/ai-safety-interventions.md | 3,926 | 8,312 | 33,231 | 775 |
| context/extracts/attractor-basins.md | 828 | 1,517 | 5,995 | 259 |
| context/extracts/bitwise-iq.md | 4,114 | 7,282 | 28,445 | 1,077 |
| context/extracts/consciousness-agency-backbone.md | 1,285 | 2,331 | 9,278 | 193 |
| context/extracts/construction-without-understanding.md | 2,883 | 5,049 | 19,931 | 577 |
| context/extracts/embedded-value-formation.md | 8,230 | 14,880 | 59,243 | 1,323 |
| context/extracts/endogenized-intentional-stance.md | 1,087 | 1,923 | 7,609 | 213 |
| context/extracts/free-energy-loops.md | 2,533 | 4,618 | 18,292 | 514 |
| context/extracts/lhcv-model-v2.md | 1,840 | 3,444 | 13,694 | 372 |
| context/extracts/literature-review-of-units-of-caring-pain-suffering-measurement-and-aggregation.md | 3,798 | 6,452 | 25,401 | 328 |
| context/extracts/loop-hub-value-model.md | 1,442 | 2,613 | 10,300 | 317 |
| context/extracts/low-rank-control-interfaces.md | 8,328 | 14,856 | 59,032 | 1,357 |
| context/extracts/maintained-blanket.md | 3,464 | 5,887 | 23,391 | 574 |
| context/extracts/preference-capability.md | 649 | 1,120 | 4,370 | 143 |
| context/extracts/smooth-uad.md | 2,904 | 4,802 | 18,883 | 706 |
| context/extracts/status-regulation-as-free-energy-loops.md | 1,255 | 2,253 | 8,877 | 238 |
| context/extracts/stealth-capability-bounds.md | 3,855 | 6,565 | 25,741 | 1,069 |
| context/extracts/uad-literature-review.md | 2,233 | 4,068 | 16,222 | 244 |
| context/extracts/unit-of-caring.md | 5,385 | 8,965 | 35,666 | 675 |
| context/extracts/unsupervised-agent-discovery.md | 2,202 | 3,747 | 14,765 | 487 |
| context/extracts/value-bundle-drift.md | 1,436 | 2,496 | 9,895 | 170 |
| **Total** | **68,831** | **~121,655** | **481,471** | **12,745** |

## Contributing files

Files reached from `book.tex` via `\input`, `\addbibresource`, and `\includegraphics`.

| Category | Files |
| --- | --- |
| Root | 1 |
| Parts | 10 |
| Chapters | 48 |
| Frontmatter | 7 |
| Appendices | 10 |
| Metadata | 7 |
| Tables | 4 |
| References (TeX) | 1 |
| Bibliography (`.bib`) | 10 |
| Figures | 25 |
| **PDF build total** | **123** |
| Lean spine (`.lean`, not in PDF) | 64 |
| **All book sources** | **187** |

## TeX LOC

| Scope | Files | Total | LOC | Code |
| --- | --- | --- | --- | --- |
| Frontmatter | 7 | 409 | 322 | 322 |
| Chapters | 48 | 42,453 | 36,077 | 36,024 |
| Appendices | 10 | 6,163 | 5,301 | 5,301 |
| Metadata | 7 | 617 | 572 | 517 |
| Tables | 4 | 76 | 76 | 68 |
| **Body** | 65 | **49,025** | **41,700** | **41,647** |
| **All counted** | 76 | **49,718** | **42,348** | **42,232** |

## Frontmatter

| File | Words | Total | LOC | Code | Pages | Cites | Labels | Formulas | TODOs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontmatter/titlepage.tex | 11 | 11 | 11 | 11 | — | 0 | 0 | 0 | 0 |
| frontmatter/dedication.tex | 42 | 10 | 9 | 9 | 1 | 0 | 0 | 0 | 0 |
| frontmatter/acknowledgements.tex | 382 | 32 | 23 | 23 | 2 | 0 | 0 | 0 | 0 |
| frontmatter/preface.tex | 358 | 50 | 40 | 40 | 2 | 0 | 0 | 0 | 0 |
| frontmatter/introduction.tex | 1,745 | 220 | 172 | 172 | 7 | 0 | 9 | 0 | 0 |
| frontmatter/executive-overview.tex | 699 | 65 | 51 | 51 | 3 | 0 | 0 | 0 | 0 |
| frontmatter/current-status.tex | 145 | 21 | 16 | 16 | 1 | 0 | 0 | 0 | 0 |
| **Subtotal** | **3,382** | **409** | **322** | **322** | **16** | **0** | **9** | **0** | **0** |

## Chapters

| # | File | Title | Words | Total | LOC | Code | Pages | Cites | Labels | Formulas | Secs | TODOs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | chapters/ch01-wrong-object.tex | The Wrong Object of Alignment | 4,268 | 734 | 612 | 611 | 20 | 14 | 4 | 7 | 11 | 0 |
| 2 | chapters/ch02-artificial-civilization.tex | From Artificial Intelligence to Artificial Civilization | 5,267 | 438 | 328 | 327 | 20 | 18 | 5 | 2 | 19 | 0 |
| 3 | chapters/ch03-dynamical-guarantee.tex | Alignment as a Dynamical Guarantee | 5,062 | 798 | 683 | 682 | 25 | 24 | 23 | 36 | 15 | 0 |
| 4 | chapters/ch04-fixed-values-wrong-target.tex | Why Fixed Values Are the Wrong Target | 5,059 | 744 | 609 | 608 | 23 | 18 | 20 | 11 | 16 | 0 |
| 5 | chapters/ch05-assumptions-scope-failure-coverage.tex | Assumptions, Scope, and Failure Coverage | 2,521 | 381 | 337 | 336 | 13 | 6 | 11 | 2 | 9 | 0 |
| 6 | chapters/ch06-agent-without-anthropomorphism.tex | What Is an Agent? | 4,809 | 788 | 668 | 667 | 20 | 11 | 19 | 28 | 9 | 0 |
| 7 | chapters/ch07-finding-boundary.tex | Finding the Boundary | 9,741 | 1,342 | 1,171 | 1,170 | 40 | 30 | 29 | 50 | 22 | 0 |
| 8 | chapters/ch08-grow-split-merge.tex | Agents That Grow, Split, and Merge | 6,336 | 1,106 | 940 | 939 | 27 | 14 | 34 | 45 | 14 | 0 |
| 9 | chapters/ch09-composite-agent.tex | The Real Agent May Be Composite | 5,389 | 963 | 824 | 821 | 26 | 18 | 21 | 52 | 16 | 0 |
| 10 | chapters/ch10-strategic-opacity.tex | Agency Under Strategic Opacity | 6,787 | 1,082 | 949 | 948 | 32 | 21 | 36 | 35 | 20 | 0 |
| 11 | chapters/ch11-capability-without-task-ontology.tex | Measuring Capability Without Task Ontology | 6,235 | 1,187 | 994 | 993 | 30 | 30 | 52 | 52 | 26 | 0 |
| 12 | chapters/ch12-boundary-expansion.tex | Capability Growth Is Boundary Expansion | 6,038 | 1,345 | 1,126 | 1,125 | 31 | 12 | 54 | 43 | 20 | 0 |
| 13 | chapters/ch13-coordination-bottleneck.tex | The Coordination Bottleneck | 6,062 | 1,143 | 936 | 935 | 25 | 11 | 66 | 19 | 18 | 0 |
| 14 | chapters/ch14-intelligence-deepens-misalignment.tex | When Intelligence Deepens Misalignment | 4,825 | 998 | 839 | 838 | 28 | 24 | 53 | 26 | 18 | 0 |
| 15 | chapters/ch15-values-compressed-control.tex | Values Are Compressed Control Signals | 7,556 | 1,268 | 1,087 | 1,086 | 31 | 16 | 33 | 59 | 23 | 0 |
| 16 | chapters/ch16-value-bundle-model.tex | The Value-Bundle Model | 6,432 | 1,419 | 1,233 | 1,232 | 30 | 12 | 64 | 57 | 16 | 0 |
| 17 | chapters/ch17-low-dimensional-value-learning.tex | When Low Dimensionality Helps Value Learning | 6,490 | 1,125 | 976 | 975 | 30 | 16 | 23 | 64 | 21 | 0 |
| 18 | chapters/ch18-bearer-maps.tex | What Values Apply To | 7,257 | 1,503 | 1,261 | 1,260 | 32 | 14 | 46 | 82 | 27 | 0 |
| 19 | chapters/ch19-tradeoffs-bundle-geometry.tex | Tradeoffs and Bundle Geometry | 4,323 | 871 | 780 | 779 | 22 | 6 | 25 | 66 | 15 | 0 |
| 20 | chapters/ch20-measuring-stress-testing-bundle-geometry.tex | Measuring and Stress-Testing Bundle Geometry | 2,176 | 515 | 452 | 451 | 16 | 6 | 19 | 28 | 10 | 0 |
| 21 | chapters/ch21-reward-to-bundle-inference.tex | From Rewards to Values | 6,436 | 1,352 | 1,201 | 1,199 | 34 | 18 | 42 | 92 | 23 | 1 |
| 22 | chapters/ch22-compression-test-intention.tex | The Compression Test for Intention | 5,014 | 1,062 | 912 | 911 | 23 | 9 | 58 | 34 | 20 | 0 |
| 23 | chapters/ch23-goal-transport.tex | Has the Goal Really Survived? | 4,172 | 955 | 851 | 850 | 22 | 13 | 43 | 53 | 16 | 0 |
| 24 | chapters/ch24-transport-types.tex | When the Words Survive but the Meaning Doesn't | 4,337 | 924 | 798 | 797 | 23 | 12 | 44 | 51 | 17 | 0 |
| 25 | chapters/ch25-correction-causal-channel.tex | Correction Is a Causal Channel | 7,552 | 1,454 | 1,277 | 1,276 | 37 | 16 | 52 | 95 | 27 | 0 |
| 26 | chapters/ch26-correction-channel-integrity.tex | Correction-Channel Integrity | 4,913 | 728 | 644 | 643 | 21 | 13 | 26 | 41 | 12 | 0 |
| 27 | chapters/ch27-correction-channels-adversarial-pressure.tex | Correction Channels under Adversarial Pressure | 3,817 | 892 | 773 | 772 | 24 | 16 | 40 | 43 | 19 | 0 |
| 28 | chapters/ch28-extrapolative-correction.tex | Beyond Following Instruction | 3,925 | 728 | 619 | 618 | 20 | 18 | 37 | 40 | 12 | 0 |
| 29 | chapters/ch29-manipulation-false-consent.tex | Manipulation, Domestication, and False Consent | 5,998 | 1,034 | 785 | 784 | 31 | 22 | 22 | 62 | 19 | 0 |
| 30 | chapters/ch30-successor-central-test.tex | Successor Creation as the Central Alignment Test | 4,527 | 734 | 622 | 621 | 25 | 19 | 23 | 44 | 16 | 0 |
| 31 | chapters/ch31-conserved-properties.tex | Conserved Properties Across Successors | 5,403 | 1,115 | 985 | 984 | 28 | 19 | 39 | 49 | 19 | 0 |
| 32 | chapters/ch32-self-modeling-self-opacity.tex | Better Self-Modeling Can Be Worse | 5,788 | 923 | 768 | 767 | 26 | 11 | 42 | 49 | 17 | 0 |
| 33 | chapters/ch33-certification-without-construction.tex | Certification Without Construction | 5,280 | 821 | 688 | 687 | 29 | 23 | 34 | 40 | 13 | 0 |
| 34 | chapters/ch34-selection-environment.tex | Alignment Is Selected or Destroyed by Its Environment | 8,188 | 1,124 | 939 | 938 | 39 | 39 | 51 | 49 | 23 | 0 |
| 35 | chapters/ch35-multi-agent-strategic-coupling.tex | Multi-Agent Superintelligence and Inferential Coupling | 5,055 | 450 | 388 | 387 | 19 | 14 | 10 | 15 | 7 | 0 |
| 36 | chapters/ch36-parasites-correction-system.tex | Parasites in the Correction System | 5,447 | 924 | 761 | 760 | 25 | 8 | 46 | 67 | 24 | 0 |
| 37 | chapters/ch37-alignment-attractor.tex | The Alignment Attractor | 2,858 | 465 | 384 | 383 | 15 | 11 | 22 | 24 | 10 | 0 |
| 38 | chapters/ch38-conductive-artifacts-pivotal-processes.tex | Conductive Artifacts and Pivotal Processes | 4,012 | 876 | 732 | 730 | 25 | 14 | 51 | 27 | 19 | 1 |
| 39 | chapters/ch39-passive-observation-not-enough.tex | Passive Observation Is Not Enough | 6,294 | 1,188 | 997 | 996 | 31 | 17 | 53 | 64 | 14 | 0 |
| 40 | chapters/ch40-goal-laundering.tex | Detecting Goal Laundering | 4,525 | 964 | 835 | 834 | 24 | 15 | 43 | 60 | 16 | 0 |
| 41 | chapters/ch41-multiscale-decomposition.tex | Checking a System at Every Level | 5,297 | 832 | 699 | 698 | 26 | 16 | 29 | 55 | 21 | 0 |
| 42 | chapters/ch42-safety-case.tex | A Safety Case for Superintelligence Alignment | 2,865 | 344 | 297 | 296 | 14 | 14 | 5 | 8 | 8 | 0 |
| 43 | chapters/ch43-verifiability-and-ontology-adequacy.tex | What Survives an Adversary: Verifiability and Representabili… | 3,871 | 312 | 267 | 266 | 16 | 13 | 8 | 3 | 11 | 0 |
| 44 | chapters/ch44-lethality-stress-test-open-issues.tex | Lethality Stress Test and Open Issues | 3,930 | 492 | 443 | 441 | 19 | 18 | 11 | 5 | 10 | 0 |
| 45 | chapters/ch45-value-change-at-stake.tex | When Value Change Is the Thing at Stake | 5,275 | 607 | 447 | 446 | 22 | 12 | 18 | 24 | 17 | 0 |
| 46 | chapters/ch46-unconscious-value-drift.tex | The End of Unconscious Value Drift | 5,211 | 740 | 600 | 599 | 24 | 15 | 43 | 25 | 18 | 0 |
| 47 | chapters/ch47-bearers-of-value.tex | Who Still Counts After Transformation | 1,755 | 322 | 273 | 272 | 9 | 12 | 4 | 14 | 11 | 0 |
| 48 | chapters/ch48-towards-alignment.tex | Towards Superintelligence Alignment | 2,015 | 341 | 287 | 286 | 10 | 4 | 5 | 8 | 8 | 0 |
|  | **Subtotal** |  | **246,393** | **42,453** | **36,077** | **36,024** | **1,182** | **752** | **1,538** | **1,905** | **792** | **2** |

## Appendices

| File | Title | Words | Total | LOC | Code | Pages | Cites | Labels | Formulas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| appendices/appA-notation.tex | Notation Index | 110 | 17 | 13 | 13 | 8 | 0 | 1 | 0 |
| appendices/appB-bridge-crosswalk.tex | Bridges and the Field: A Crosswalk | 5,181 | 314 | 281 | 281 | 21 | 44 | 8 | 0 |
| appendices/appC-institutional-translation.tex | Human Institutions as Alignment Translation Guide | 6,227 | 700 | 607 | 607 | 30 | 48 | 26 | 0 |
| appendices/appM-institutional-histories.tex | Institutional Genesis, Memory, and Decay: Historic… | 6,209 | 261 | 208 | 208 | 28 | 54 | 15 | 0 |
| appendices/appD-worked-example.tex | A Worked Example: The BioShield Deployment Gate | 3,683 | 377 | 312 | 312 | 14 | 0 | 15 | 1 |
| appendices/appE-glossary.tex | Operational Glossary | 3,301 | 278 | 241 | 241 | 10 | 4 | 10 | 6 |
| appendices/appF-research-program.tex | Research Program | 4,948 | 482 | 391 | 391 | 19 | 7 | 8 | 0 |
| appendices/appP-bridge-predictions.tex | Dated Predictions on the Bridges | 11,715 | 1,239 | 1,063 | 1,063 | 41 | 37 | 34 | 5 |
| appendices/appG-lean-proof-spine.tex | Lean Dependency Spine in Mathematical Form | 12,770 | 1,964 | 1,725 | 1,725 | 70 | 41 | 243 | 68 |
| appendices/appN-experimental-evidence.tex | Experimental Evidence: Findings by Line | 6,571 | 531 | 460 | 460 | 33 | 2 | 84 | 0 |
| **Subtotal** |  | **60,715** | **6,163** | **5,301** | **5,301** | **274** | **237** | **444** | **80** |

## Bibliography

| File | Entries |
| --- | --- |
| dynamical-systems.bib | 108 |
| external-alignment.bib | 120 |
| governance-institutions.bib | 25 |
| institutional-histories.bib | 32 |
| internal-project-sources.bib | 31 |
| lw-wiki.bib | 33 |
| main.bib | 0 |
| manuscript-citations.bib | 98 |
| neuroscience-values.bib | 62 |
| philosophy.bib | 48 |
| **Total unique keys** | **557** |

## Lean proof spine

| Module | Total | LOC | Code | Thms | Lems | Defs | Struct | Axioms | P* | MB* |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| formal/AlignmentProofSpine/Adversarial.lean | 102 | 83 | 78 | 5 | 0 | 4 | 1 | 0 | 4 | 0 |
| formal/AlignmentProofSpine/AlignmentConstruction.lean | 276 | 215 | 206 | 14 | 0 | 22 | 7 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/AlignmentRegime.lean | 68 | 53 | 52 | 2 | 0 | 5 | 2 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/BacktestC2Instance.lean | 96 | 71 | 70 | 2 | 0 | 7 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Boundaries.lean | 190 | 160 | 159 | 20 | 0 | 4 | 0 | 0 | 10 | 0 |
| formal/AlignmentProofSpine/BridgeCruxes.lean | 124 | 90 | 83 | 11 | 0 | 12 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Bundles.lean | 564 | 453 | 446 | 43 | 0 | 45 | 7 | 0 | 10 | 0 |
| formal/AlignmentProofSpine/Capability.lean | 498 | 418 | 415 | 42 | 0 | 10 | 8 | 9 | 9 | 0 |
| formal/AlignmentProofSpine/Certification.lean | 498 | 443 | 442 | 26 | 0 | 13 | 7 | 2 | 5 | 1 |
| formal/AlignmentProofSpine/Chokepoint.lean | 237 | 208 | 204 | 4 | 0 | 10 | 3 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/CooperationGraph.lean | 388 | 307 | 299 | 22 | 0 | 20 | 12 | 0 | 1 | 0 |
| formal/AlignmentProofSpine/Core.lean | 650 | 505 | 497 | 7 | 0 | 28 | 5 | 102 | 0 | 12 |
| formal/AlignmentProofSpine/Correction.lean | 1,283 | 1,073 | 1,068 | 68 | 0 | 82 | 14 | 4 | 4 | 1 |
| formal/AlignmentProofSpine/Defeaters.lean | 439 | 352 | 349 | 11 | 0 | 24 | 4 | 16 | 0 | 0 |
| formal/AlignmentProofSpine/Evidence.lean | 193 | 145 | 139 | 13 | 0 | 1 | 3 | 19 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Amplification.lean | 61 | 51 | 50 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/CIRL.lean | 191 | 165 | 162 | 10 | 0 | 4 | 2 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Common.lean | 76 | 62 | 61 | 0 | 0 | 2 | 3 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Corrigibility.lean | 53 | 42 | 41 | 5 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Debate.lean | 108 | 91 | 88 | 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/ELK.lean | 96 | 81 | 78 | 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/AmplificationTree.lean | 127 | 106 | 105 | 4 | 0 | 6 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Basic.lean | 45 | 31 | 30 | 3 | 0 | 4 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/BellmanQ.lean | 271 | 241 | 238 | 10 | 0 | 4 | 1 | 3 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/CompositePathBypass.lean | 127 | 100 | 98 | 5 | 0 | 7 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Contraction.lean | 48 | 36 | 35 | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/DebateGame.lean | 311 | 273 | 269 | 10 | 0 | 13 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/DynamicChoice.lean | 211 | 182 | 178 | 9 | 0 | 6 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/ELKIdentifiability.lean | 158 | 132 | 131 | 7 | 0 | 6 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/IncompletePreferences.lean | 249 | 211 | 209 | 11 | 0 | 12 | 2 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Interruptibility.lean | 124 | 101 | 100 | 8 | 0 | 5 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/LobTiling.lean | 115 | 99 | 99 | 3 | 0 | 1 | 2 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/MDP.lean | 108 | 88 | 87 | 3 | 0 | 9 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Nonrealizability.lean | 166 | 137 | 136 | 8 | 0 | 9 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/OffSwitchGame.lean | 196 | 169 | 167 | 10 | 0 | 4 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/PMF.lean | 91 | 71 | 70 | 6 | 0 | 3 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Probability.lean | 448 | 392 | 390 | 21 | 0 | 21 | 5 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/QuantilizerMaximin.lean | 114 | 98 | 97 | 6 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Reachability.lean | 165 | 126 | 124 | 4 | 0 | 13 | 3 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/RegretSafety.lean | 175 | 145 | 142 | 7 | 0 | 8 | 2 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/ShannonMI.lean | 244 | 219 | 218 | 7 | 0 | 5 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/ShutdownIncentives.lean | 192 | 166 | 164 | 8 | 0 | 4 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean | 1,278 | 1,127 | 1,126 | 61 | 0 | 41 | 13 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Finite/Weights.lean | 75 | 57 | 56 | 4 | 0 | 6 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Impact.lean | 139 | 123 | 122 | 10 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Imported.lean | 150 | 122 | 121 | 1 | 0 | 11 | 0 | 10 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Interruptibility.lean | 140 | 122 | 120 | 7 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Quantilization.lean | 188 | 167 | 165 | 10 | 0 | 2 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field/Shutdown.lean | 172 | 146 | 142 | 6 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Field.lean | 63 | 56 | 55 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/FieldInterfaces.lean | 195 | 160 | 159 | 12 | 0 | 0 | 5 | 3 | 0 | 0 |
| formal/AlignmentProofSpine/FieldSubsumptions.lean | 37 | 27 | 26 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Forgeability.lean | 213 | 183 | 178 | 5 | 0 | 7 | 1 | 4 | 0 | 1 |
| formal/AlignmentProofSpine/MB2Identifiability.lean | 117 | 91 | 85 | 3 | 0 | 6 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/MB4CorrectionIntegrity.lean | 121 | 92 | 88 | 9 | 0 | 8 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Mathlib.lean | 56 | 45 | 43 | 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Philosophy.lean | 63 | 49 | 48 | 4 | 0 | 6 | 0 | 0 | 4 | 0 |
| formal/AlignmentProofSpine/SpineModel.lean | 345 | 271 | 255 | 21 | 0 | 29 | 12 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/Successors.lean | 149 | 125 | 121 | 9 | 0 | 0 | 2 | 0 | 3 | 0 |
| formal/AlignmentProofSpine/ToyDeploymentGate.lean | 66 | 53 | 52 | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| formal/AlignmentProofSpine/WorkedInstance.lean | 413 | 361 | 358 | 5 | 0 | 15 | 0 | 1 | 0 | 0 |
| formal/AlignmentProofSpine.lean | 85 | 78 | 77 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| formal/playgrounds/P01-basin-invariant.lean | 50 | 40 | 40 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| formal/playgrounds/P15-bundle-geometry.lean | 62 | 49 | 49 | 3 | 0 | 4 | 1 | 0 | 1 | 0 |
| **Subtotal** | **14,053** | **11,735** | **11,560** | **642** | **0** | **585** | **140** | **173** | **50** | **15** |

### Spine node inventory

- **P nodes** (50): P01, P02, P05, P06, P07, P08, P09, P10, P10H, P11, P12, P12W, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22a, P22b, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34, P34A, P34K, P35, P35M, P35Mplus, P36, P36R, P37, P38H, P40, P41, P42, P43, P44, P45
- **MB bridges** (15): MB1, MB10, MB11, MB3, MB4, MB4a, MB5, MB6a, MB6b, MB7a, MB7b, MB7c, MB7d, MB8, MB9

### \leanspine cross-refs by chapter

| Chapter file | Refs |
| --- | --- |
| chapters/ch10-strategic-opacity.tex | 3 |
| chapters/ch11-capability-without-task-ontology.tex | 1 |
| chapters/ch16-value-bundle-model.tex | 1 |
| chapters/ch17-low-dimensional-value-learning.tex | 2 |
| chapters/ch18-bearer-maps.tex | 1 |
| chapters/ch21-reward-to-bundle-inference.tex | 2 |
| chapters/ch25-correction-causal-channel.tex | 7 |
| chapters/ch26-correction-channel-integrity.tex | 2 |
| chapters/ch27-correction-channels-adversarial-pressure.tex | 3 |
| chapters/ch28-extrapolative-correction.tex | 4 |
| chapters/ch29-manipulation-false-consent.tex | 1 |
| chapters/ch30-successor-central-test.tex | 4 |
| chapters/ch31-conserved-properties.tex | 3 |
| chapters/ch33-certification-without-construction.tex | 1 |
| chapters/ch35-multi-agent-strategic-coupling.tex | 6 |
| chapters/ch39-passive-observation-not-enough.tex | 2 |
| chapters/ch41-multiscale-decomposition.tex | 1 |
| chapters/ch42-safety-case.tex | 4 |
| chapters/ch43-verifiability-and-ontology-adequacy.tex | 4 |
| chapters/ch47-bearers-of-value.tex | 2 |
| chapters/ch48-towards-alignment.tex | 3 |
| **Total** | **132** |

## Notes

- **Words**: LaTeX commands and comments stripped; approximate prose count.
- **TeX LOC**: **Code** = non-blank lines excluding comment-only (`%`, respecting `\%`); **LOC** = all non-blank lines.
- **Contributing files**: Transitive closure from `book.tex`; figures only if the path resolves on disk.
- **Pages**: Per-unit spans from `book.toc` when present; run `./build.sh` first for accurate values.
- **Formulas**: Counts `equation`, `align`, `gather`, `multline`, and `\[` environments (not inline `$...$`).
- **Cites**: Counts `\autocite`, `\cite`, `\parencite`, `\textcite`, `\footcite` invocations.
- **Labels**: Counts `\label{...}` anchors (includes chapters, sections, figures, equations).
- **Lean P\***: Unique proof-spine node IDs from `theorem`/`lemma` names (`P01`, `P22a`, `P36R`, …).
- **Lean MB\***: Explicit bridge axioms (`MB1`–`MB9`, including split `MB6a`/`MB6b`, `MB7a`–`MB7d`).
- **Lean LOC**: **Code** = non-blank lines excluding comment-only (`--` and single-line `/- -/`); **LOC** = all non-blank lines.
- **Lean counts**: Line-anchored declarations; multi-line signatures count at the opening line only.
