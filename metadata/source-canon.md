# Source Canon

Durable record of the manuscript's source material: which prior papers ground each
part of the book, where their book-local copies and extracts live, and the canonical
TeX/PDF sources in the sibling repositories. This file is the source of truth for
source paths. `INSTRUCTIONS.md` §3 summarizes themes; this file holds paths and tables.

## Book-local notes

- `context/Alignment Attractor.md` — executive summary and platform framing
- `context/legible-alignment-messageing.md` — legibility constraints for funders and policy-adjacent readers
- `context/writing-style-gunnar.md` — author voice and calibration
- `context/lw-references.md` — chapter-indexed curated LessWrong and external alignment references (URLs, summaries); consult when wiring chapter citations; not auto-imported into `.bib` (see `INSTRUCTIONS.md` §7)
- `context/towards-asi-alignment-deep-research-report.md` — external literature synthesis (German); maps field gaps to book thesis; chapter-indexed addition guide below
- `context/lean_proof_dependency_graph.dot` / `.png` — full Lean proof dependency DAG (developer reference)
- `context/lean_proof_graphs/` — four sub-spine diagrams + overview for the book; rendered to `figures/lean_proof/`

## Formal proof spine (`formal/`)

Machine-checked logical skeleton of the alignment argument. Builds with `cd formal && lake build` (Lean 4, no Mathlib). See `formal/README.md` for module map and the proof / counterexample / bridge taxonomy.

| Artifact | Role |
|----------|------|
| `formal/AlignmentProofSpine.lean` | Root Lean 4 module |
| `formal/AlignmentProofSpine/*.lean` | Layer modules (`P01`–`P45`, bridges `MB1`–`MB8`) |
| `formal/README.md` | Build, status, book-facing interpretation |
| `LeanProofSpineImplementationBrief.md` | Agent spec and theorem inventory (brief numbering is the implementation target) |
| `context/lean_proof_dependency_graph.dot` / `.png` | Full dependency DAG (developer reference) |
| `context/lean_proof_graphs/*.dot` | Book sub-spine diagrams + overview; output in `figures/lean_proof/` |

## External literature syntheses

Synthesis documents that are not sibling-repo papers but ground chapter drafting, citation gaps, and funder-facing claims.

| Book copy (`context/`) | Extract | Repo | TeX source | Built PDF |
|------------------------|---------|------|------------|-----------|
| `towards-asi-alignment-deep-research-report.md` | — | — | *(context-only; Deep Research synthesis, 2026)* | — |

**Use.** Consult before drafting stub chapters in Parts III–X and before expanding chapter references. The report's inline `cite turn…` markers are Deep Research placeholders, not BibTeX keys; use the **annotated Kernliteratur** paragraphs and the bibliography-candidate list below when importing into `.bib`.

**Thesis distilled.** The field has strong partial tools (boundaries, IRL, corrigibility, evals, safety cases, governance) but no integrated theory for boundary-stable agency, value-faithful successor creation, ontology-crossing goal transport, deception-resistant correction channels, and socially legitimate value aggregation. Behavior alignment alone is insufficient.

### Report sections → book chapters

| Report section | Primary chapters | Secondary chapters |
|----------------|------------------|-------------------|
| Kurzfassung (field gaps, negative result) | ch03, ch44 | ch05, frontmatter executive-overview |
| Agentur, Grenzen und Repräsentationen | ch06, ch07, ch11 | ch08, ch38 |
| Ziel- und Wertinferenz | ch04, ch20, ch21 | ch15, ch37 |
| Wertbündel und Trägermaps | ch16, ch17, ch18, ch19 | ch43, ch41 |
| Korrekturkanäle und zivilisatorische Deliberation | ch24, ch25, ch26 | ch27, ch35 |
| Nachfolgerstabilität, Ontologieshift, Zieltransport | ch08, ch22, ch23, ch28, ch29 | ch30, ch31, ch11 |
| Selektionsdruck, Governance, Förderlandschaft | ch32, ch33, ch35, ch39 | ch34, ch40 |
| Zertifizierung, Empirie, Forschungsagenda | ch39, ch40, ch36 | ch31, ch44 |

### Chapter addition suggestions

Prioritized by report emphasis. **Drafted** chapters: surgical inserts. **Stub** chapters: outline seeds.

**Part I — Reframing**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch03 | One paragraph on the negative literature result: behavior alignment (RLHF, IRL, corrigibility) gives local signals but fails on identifiability, Goodhart, pluralism, deception; positions the book's transport frame as filling an integration gap. |
| ch04 | IRL underdetermination (many rewards explain same behavior); CIRL as cooperative game not solution; RLHF limits survey (Casper et al. 2023); sample-complexity warning (Komanduru & Honorio). |
| ch05 | Crosswalk report's open-problem priority table to Turchin/Yudkowsky coverage audit; note funding gap (interpretability/evals over transport, bearer maps, correction-channel engineering). |

**Part II — Agents and boundaries**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch06 | Method comparison table (Markov blanket / causal reps / IB / embedded agency): assumptions, observability, adversarial robustness, scaling; FEP overreach caveat (Biehl, Pollock & Kanai 2020). |
| ch07 | IB objective $\min_{p(z\mid x)} I(X;Z)-\beta I(Z;Y)$ as representation criterion; Schölkopf et al. (2021) on causal structure in $Z$; gap: nonstationary, self-modifying, deception-resistant boundaries. |
| ch08 | de Blanc (2011) ontological crisis; Everitt et al. (2016) self-modification; transport loss $\Delta L_{\text{transport}}$ heuristic from report; link conserved properties to report's structure bundle. |
| ch09 | Composite-agent blindness failure mode (report §Selektionsdruck / ch11 draft); joint intentional compression already present — add Goodhart-on-metrics institutional parallel. |
| ch10 | Alignment-faking / sleeper agents as model-organism evidence for selective opacity; cite alongside Hubinger model-organisms. |
| ch11 | External-growth vs internal-growth diagnostic already present; add report's funding-gap note: capability evals dominate, transport/bearer underinvested; percolation analogy preview for ch33. |

**Part III — Capability (stubs)**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch12 | If retained: BIQ/competence measure formalization (bitwise-iq source); benchmark vs boundary distinction already in ch11 — avoid duplication. |
| ch13 | Coordination expansion + Wang/Szolnoki/Perc percolation threshold: cooperation best near percolation; audit capacity must scale network-wise. |
| ch14 | World-model vs correction-model improvement distinction (ch11 §model expansion); deception when prediction of humans/auditors outruns correction. |

**Part IV — Value bundles (stubs)**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch15 | Panksepp primary emotional systems; values as compressed control signals anchored in affect/neuroscience cluster. |
| ch16 | Value-bundle working definition from report; bundle-axis table (care, fairness, loyalty, authority, purity, play/seeking, social warmth, identity continuity) with operational proxies and failure modes. |
| ch17 | IB + low-rank bundle structure; conflict/context/träger-dependent weighting. |
| ch18 | Bearer map definition; Olson person-identity criteria; semantic similarity ≠ value bearing. |
| ch19 | Arrow / AI social-choice impossibility for "align with all"; MFT tradeoff geometry. |

**Part V — Goal inference (stubs)**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch20 | IRL toolbox survey (Abbeel & Ng, Bayesian IRL, MaxEnt, AIRL, deep variants); bundle-first vs reward-first; Baker/Saxe/Tenenbaum Bayesian inverse planning. |
| ch21 | Compression test linked to IB; which causal structure must survive in $Z$. |
| ch22–ch23 | Transport difference $\Delta L_{\text{transport}}$; conserved structure bundle (bundles, correction, identity, audit); ontology-shift as silent failure. |

**Part VI — Correction (stubs)**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch24 | Correction-channel capacity $C_{\mathrm{corr}}$ formalization (report eq.); four requirements: bandwidth, interpretability stability, incentive compatibility, legitimacy. |
| ch25 | Soares et al. corrigibility; off-switch game; channel must survive adversariality. |
| ch26 | CEV as normative upper idea not implementable procedure; extrapolative correction vs frozen values. |
| ch27 | False consent + simulated empathy without obligation (ANPS/social-warmth row). |

**Part VII — Successors (stubs)**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch28–ch29 | Successor certification schema; transport tests; tiling/Löb hurdles (cite from lw-references / Yudkowsky–Herreshoff). |
| ch30 | Report's core failure mode: $d\uparrow,\tau\uparrow$ (better self-model, worse transparency); alignment-faking evidence. |
| ch31 | Certification without construction; conserved-property checklist from report transport section. |

**Part VIII–X — Selection, safety cases, civilizational limit**

| Ch | Suggested additions from report |
|----|----------------------------------|
| ch32 | Manheim & Garrabrant Goodhart taxonomy; selection pressure on safety culture. |
| ch33 | Percolation of cooperation subsection; network scaling of audit norms. |
| ch35 | UNESCO / OECD / German Ethics Council as legitimacy anchors for correction channel; deliberation loop diagram from report. |
| ch36 | Model organisms + dangerous-capability evals + NIST AI RMF as three empirical lines. |
| ch39 | Tiered assurance: formal where spec tight; safety cases above; no global ASI proof; dynamic safety cases; Seoul Commitments / EU AI Act as governance artifacts. |
| ch40 | Sleeper agents, alignment-faking, ontological crisis, IRL underdetermination as checklist rows; link to report priority table. |
| ch43–ch44 | Bearer persistence philosophy; research pitch one-pager from report §Forschungspitch. |

### Bibliography candidates (not yet in `.bib` or under-cited)

Import or verify before drafting stubs above. Keys are suggested slugs.

| Work | Suggested key | Target chapters |
|------|---------------|-----------------|
| Biehl, Pollock & Kanai (2020) — FEP/blanket critique | `biehl2020fepcritique` | ch06, ch07 |
| Schölkopf et al. (2021) — causal representations | `scholkopf2021causalreps` | ch07, ch21 |
| Strouse & Schwab (2016); Kolchinsky et al. (2017) — deep IB | `strouse2016ib`, `kolchinsky2017ib` | ch07, ch17 |
| Baker, Saxe & Tenenbaum (2009) — Bayesian inverse planning | `baker2009inverseplanning` | ch20, ch21 |
| Ramachandran & Amir (2007) — Bayesian IRL | `ramachandran2007bayesianirl` | ch20 |
| Casper et al. (2023) — RLHF limits | `casper2023rlhflimits` | ch04, ch20 |
| Komanduru & Honorio — IRL sample complexity | `komanduru2019irlcomplexity` | ch04, ch20 |
| de Blanc (2011) — ontological crises | `deblanc2011ontological` | ch08, ch22, ch40 |
| Everitt et al. (2016) — self-modification | `everitt2016selfmodification` | ch08, ch28, ch29 |
| Manheim & Garrabrant (2018) — Goodhart taxonomy | `manheim2018goodhart` | ch32, ch34, ch37 |
| Wang, Szolnoki & Perc — cooperation near percolation | `wang2013percolation` | ch13, ch33 |
| Panksepp — affective neuroscience | `panksepp1998affective` | ch15, ch16 |
| Olson — person identity (SEP) | `olson2023personidentity` | ch18, ch43 |
| Seoul AI Summit commitments (2024) | `seoul2024commitments` | ch35, ch39 |
| International AI Safety Report (2025) | `iaisr2025` | ch39, ch40 |
| UNESCO Recommendation on AI Ethics (2021) | `unesco2021aiethics` | ch25, ch35 |

Already present and should be wired where stubs draft: `soares2015corrigibility`, `ng2000irl`, `ziebart2008maxent`, `hadfieldmenell2016`, `tishby2000ib`, `friston2010free`, `hubinger2023modelorganisms`, `hubinger2019risks`, `park2024deception`.


## PDF extracts

Each PDF under `context/` has a markdown extract in `context/extracts/` (generated by
`scripts/extract_pdf_to_md.py`). Prefer extracts for agent reading. Formulas in
extracts use `$$...$$` and LaTeX symbol names where auto-conversion succeeded. When in
doubt about a formula, consult the PDF or the TeX source below.

## Sibling repositories

Canonical LaTeX sources and built PDFs live in sibling repositories (paths relative to
this repo). The `context/*.pdf` copies are book-local snapshots; rebuild from TeX when
formulas or claims must be verified exactly.

- `../brain-to-values/papers/` — value bundles, free-energy loops, unit-of-caring, consciousness/agency backbone
- `../agency-detect/docs/papers/` — UAD, capability, intentional stance, attractor basins, construction/successor work

## Source map

| Book copy (`context/`) | Extract | Repo | TeX source | Built PDF |
|------------------------|---------|------|------------|-----------|
| `unsupervised-agent-discovery.pdf` | `extracts/unsupervised-agent-discovery.md` | agency-detect | `../agency-detect/docs/papers/unsupervised-agent-discovery/unsupervised-agent-discovery.tex` | `../agency-detect/docs/papers/unsupervised-agent-discovery/unsupervised-agent-discovery.pdf` |
| `uad_literature_review.pdf` | `extracts/uad-literature-review.md` | agency-detect | `../agency-detect/docs/papers/uad-literature-review/uad_literature_review.tex` | `../agency-detect/docs/papers/uad-literature-review/uad_literature_review.pdf` |
| `acausal_trade_uad_formalization.pdf` | `extracts/acausal-trade-uad-formalization.md` | agency-detect | `../agency-detect/docs/papers/acausal-trade-uad-formalization/acausal_trade_uad_formalization.tex` | `../agency-detect/docs/papers/acausal-trade-uad-formalization/acausal_trade_uad_formalization.pdf` |
| `endogenized-intentional-stance.pdf` | `extracts/endogenized-intentional-stance.md` | agency-detect | `../agency-detect/docs/papers/endogenized-intentional-stance/endogenized-intentional-stance.tex` | `../agency-detect/docs/papers/endogenized-intentional-stance/endogenized-intentional-stance.pdf` |
| `bitwise_iq.pdf` | `extracts/bitwise-iq.md` | agency-detect | `../agency-detect/docs/papers/bitwise-iq/bitwise_iq.tex` | `../agency-detect/docs/papers/bitwise-iq/bitwise_iq.pdf` |
| `preference-capability.pdf` | `extracts/preference-capability.md` | agency-detect | `../agency-detect/docs/papers/preference-capability/preference-capability.tex` | `../agency-detect/docs/papers/preference-capability/preference-capability.pdf` |
| `attractor-basins.pdf` | `extracts/attractor-basins.md` | agency-detect | `../agency-detect/docs/papers/attractor-basins/attractor-basins.tex` | `../agency-detect/docs/papers/attractor-basins/attractor-basins.pdf` |
| `construction_without_understanding.pdf` | `extracts/construction-without-understanding.md` | agency-detect | `../agency-detect/docs/papers/construction-without-understanding/construction_without_understanding.tex` | `../agency-detect/docs/papers/construction-without-understanding/construction_without_understanding.pdf` |
| `access-uad.pdf` | `extracts/access-uad.md` | agency-detect | `../agency-detect/docs/papers/access-uad/access-uad.tex` | `../agency-detect/docs/papers/access-uad/access-uad.pdf` |
| `smooth-uad.pdf` | `extracts/smooth-uad.md` | agency-detect | `../agency-detect/docs/papers/smooth-uad/smooth-uad.tex` | `../agency-detect/docs/papers/smooth-uad/smooth-uad.pdf` |
| `stealth-capability-bounds.pdf` | `extracts/stealth-capability-bounds.md` | agency-detect | `../agency-detect/docs/papers/stealth-capability-bounds/stealth-capability-bounds.tex` | `../agency-detect/docs/papers/stealth-capability-bounds/stealth-capability-bounds.pdf` |
| `loop-hub-value-model.pdf` | `extracts/loop-hub-value-model.md` | brain-to-values | `../brain-to-values/papers/loop-hub-value-model/loop-hub-value-model.tex` | `../brain-to-values/papers/loop-hub-value-model/loop-hub-value-model.pdf` |
| `lhcv-model-v2.pdf` | `extracts/lhcv-model-v2.md` | brain-to-values | `../brain-to-values/papers/loop-hub-control-value/lhcv-model-v2.tex` | `../brain-to-values/papers/loop-hub-control-value/lhcv-model-v2.pdf` |
| `unit-of-caring.pdf` | `extracts/unit-of-caring.md` | brain-to-values | `../brain-to-values/papers/unit-of-caring/unit-of-caring.tex` | `../brain-to-values/papers/unit-of-caring/unit-of-caring.pdf` |
| `value-bundle-drift.pdf` | `extracts/value-bundle-drift.md` | brain-to-values | `../brain-to-values/papers/value-bundle-drift/value-bundle-drift.tex` | `../brain-to-values/papers/value-bundle-drift/value-bundle-drift.pdf` |
| `free_energy_loops.pdf` | `extracts/free-energy-loops.md` | brain-to-values | `../brain-to-values/papers/free-energy-loops/free_energy_loops.tex` | `../brain-to-values/papers/free-energy-loops/free_energy_loops.pdf` |
| `status_regulation_as_free_energy_loops.pdf` | `extracts/status-regulation-as-free-energy-loops.md` | brain-to-values | `../brain-to-values/papers/status-regulation-loops/status_regulation_as_free_energy_loops.tex` | `../brain-to-values/papers/status-regulation-loops/status_regulation_as_free_energy_loops.pdf` |
| `consciousness_agency_backbone.pdf` | `extracts/consciousness-agency-backbone.md` | brain-to-values | `../brain-to-values/papers/consciousness-agency-backbone/consciousness_agency_backbone.tex` | `../brain-to-values/papers/consciousness-agency-backbone/consciousness_agency_backbone.pdf` |
| `Literature Review of Units of Caring, Pain & Suffering Measurement, and Aggregation.pdf` | `extracts/literature-review-of-units-of-caring-pain-suffering-measurement-and-aggregation.md` | — | *(no TeX in canonical repos; context-only)* | — |
