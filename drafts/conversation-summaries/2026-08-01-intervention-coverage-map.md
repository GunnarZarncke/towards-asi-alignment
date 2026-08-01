# 2026-08-01 — AI Safety Interventions coverage map

## Trigger
User requested implementation of the intervention-coverage plan: map LessWrong AI Safety Interventions index against book scope; explicit exclusions, borderline agendas, and minimal cites.

## Done
- Archived `context/ai-safety-interventions.pdf` (GitHub master) + `context/extracts/ai-safety-interventions.md`; linked from `context/lw-references.md`.
- Added **Intervention coverage map** section to `appendices/appB-bridge-crosswalk.tex` (`sec:intervention-coverage-map`) with cluster table, LLM-opacity rule, exclude-by-reference default.
- **App. B notes:** Cartesian frames/CCD as alternative boundary agendas; RLAIF/CAI minimal cites; shard theory as borderline MB2/MB3 exception.
- **Ch. 5:** Out-of-scope bullet + forward ref to coverage map and external index.
- **Ch. 7:** WWCTV falsifier for factorization-based boundary discovery.
- **Ch. 14:** Generalization control vs goal misgeneralization distinction.
- **Ch. 17:** Shard theory borderline paragraph + cite in Chapter References.
- **Ch. 27:** Adversarial-training WWCTV falsifier.
- **Ch. 43:** Steganography/monitorability + simulator ontology note near ELK.
- **Ch. 48:** Logical induction WWCTV bullet.
- **App. C:** RSP + hardware_tag cross-ref vs commercial hardware security.
- Bib keys: `garrabrant2021cartesian`, `turner2022shard`, `bai2022constitutional`, `bai2022rlaif`, `anthropic2024rsp`, `zarncke2025interventions` + `\bibsummary` lines.
- Updated `metadata/TODO.md` (interventions partial; IAISR still open) and `HANDOFF.md`.

## Review round (same session)
User feedback after first pass:
- **Ch. 5:** user rewrote the exclusion as "LLM whitebox methods" with a prose gloss (inner-alignment agendas, important but out of scope). Kept as edited.
- **Ch. 7 — de-privilege UAD.** Interventional discovery was reading as the correct method with CCD as a mere "baseline / not a substitute." Revised: CCD paragraph now states what a directed graph does and does not supply, followed by "the interventional route has the complementary profile"; new paragraph states the book's preference is a *coverage* argument (same handles reused for correction probes, successor certification, adversarial measurement), explicitly "not demonstrated superiority," and names Cartesian frames/FFS and object-centric decomposition as co-equal live instruments. WWCTV bullet reframed from "factorization works" to "intervention handles turn out not to be necessary."
- **App. B MB1** rewritten to match: MB1 is a bet about recoverability, not one instrument; a cheaper passive route would *discharge* MB1, not refute it. Table row now "Alternative boundary instruments / co-equal routes."
- **Ch. 43** paragraph simplified: dropped the simulator-ontology aside; steganography now connects directly to the paragraph's budget logic ("what would it cost to keep the visible trace compliant while the decision is made somewhere unread?").
- **Hardware-backed boundaries:** App. C sentence removed (user: no good home yet). Coverage-map row demoted to "Named, not developed." New TODO records the open question and the failed App. C placement.
- Fixed 5 broken `\ref` labels in the new table (`appk-worked-example`, `appj-institutional-translation`, `ch:fixed-values-wrong-target`, `ch:intelligence-deepens-misalignment`).

## Decisions
- PDF canonical in `context/`; markdown extract for grep.
- Shard theory = named exception to MI opacity rule, not bridge elevation.
- Adversarial training excluded as alignment method but falsifier added (training robustness ≠ correction preservation).
- Boundary discovery presented as an open measurement problem with several live instruments; UAD justified by cross-chapter reuse only.

## Verification
- `check_bibliography_summaries.py` 443/443; `check_structure.py` pass.
- `./build.sh` clean — 1373 pages, zero undefined references.
- `check_citations.py` still fails on pre-existing `kwon2026` (ET-4 paper, unrelated).

## Open / next
- International AI Safety Report crosswalk (remaining half of external-report-review TODO).
- Hardware-backed causal boundaries need a home (ch07 / ch33 / ch39 candidates).

## Key paths
- `appendices/appB-bridge-crosswalk.tex` (§intervention-coverage-map)
- `context/ai-safety-interventions.pdf`
- `chapters/ch17-low-dimensional-value-learning.tex`, `ch27-correction-channels-adversarial-pressure.tex`
