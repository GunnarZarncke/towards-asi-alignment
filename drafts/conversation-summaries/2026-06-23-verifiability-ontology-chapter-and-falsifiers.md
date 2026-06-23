# 2026-06-23 — Verifiability/ontology chapter + strong falsifiers

## Trigger
Author asked, across a multi-turn session: (1) tabulate each chapter's "What Would Change This View" (WWCTV) section by count and harmless-vs-dangerous direction; (2) critique that analysis with a security mindset (Yudkowsky-blunt); (3) suggest *strong* per-chapter falsifiers; then (4) responded with detailed comments and asked to: make a perturbation-recognition TODO, hand ch40 to a hostile critic, and **create a new chapter** addressing the two master cruxes (metric verifiability under adversarial optimization; ontology adequacy) with a minimal draft.

## Done
- **New chapter** `chapters/ch39b-verifiability-and-ontology-adequacy.tex` ("What Survives an Adversary: Verifiability and Representability"). Minimal seed draft (~1500 words) with: observable / i.i.d.-robust / adversarially-verifiable distinction; the *ontology-adequacy reduces to detection* argument (reliable steering = control ⇒ agency, answering the author's pushback); the **cost relation** `c_fake(M,Δ)` that unifies strategic opacity (ch10), staged transport (ch22), goal laundering (ch37), and scale-fluid evasion (ch38) and reframes coordination-internalization (ch13) as having a measurable footprint; GSAI as the strong/proof form (out of scope); worked example on correction-channel integrity; its own WWCTV; Summary; inline `TODO[open-crux]`/`TODO[formalize]` markers.
- **Wired** into `parts/part09-safety-cases.tex` between ch39 (safety case) and ch40 (lethality stress test), preserving ch40's existing forward bridge to ch41.
- **Bib**: added `dalrymple2024gsai` (Towards Guaranteed Safe AI, arXiv:2405.06624) to `references/external-alignment.bib`.
- **metadata/book.yml**: added `ch39b` entry (status: draft, with numbering note).
- **metadata/TODO.md**: added cross-cutting "Verifiability-label pass" and "Perturbation-recognition crux" manuscript items; added two Formalization-track rows (cost-of-opacity / budget verifiability; prove-bound undetectable controllers) owned by ch39b.
- **Build verified**: `./build.sh` exit 0, 962 pages, 0 undefined references; new chapter present in `book.toc`/`book.aux`.

## Decisions
- **Filename `ch39b` instead of renumbering.** Inserting in Part IX would otherwise force renaming ch40–ch44 and many references. `39b` keeps the file list sorted and the insertion obvious. **Consequence:** displayed chapter numbers for Part X auto-shift +1 (ch40 file now displays as ch41, etc.); cross-refs use `\label`/`\ref` so they remain correct. A full renumber (ch40→41 … ch44→45, new→40) is the clean follow-up but is invasive; deferred and flagged.
- **Placed before ch40, not after**, so ch40's "next chapter … Chapter~\ref{ch:value-change-at-stake}" bridge stays adjacent to ch41.
- Claim strength kept at **[Conjectural]/[Open]** for the cost relation and the representability bound; chapter explicitly states the book supplies *targets*, not *proofs*, and points to GSAI for the proof form (matches Lean-spine "bridges are out of scope" framing in TODO.md).
- The harmless/dangerous WWCTV tally from earlier in the session was re-binned under critique into three buckets (over-worried / blind / solution-fails); the headline "≈88% harmless" was judged misleading (mis-binned "instrument can't measure" points as harmless). No manuscript edits were made for the tally itself.

## Round 2 (same session) — folded verdicts, acausal review, WWCTV pass
- **Two BIG REVIEW items** added to `metadata/TODO.md` (new "Big reviews" section): (a) conserved-property transport decoupled from safety (forgeable + non-enumerable), spanning ch08/ch28/ch29; (b) pivotal-act reframe may rename not dissolve the lethality, spanning ch35/ch40/`P35`.
- **ch33 acausal-trade review.** Read the source extract (`context/extracts/acausal-trade-uad-formalization.md`; the author's own `zarncke2025acausal`). Added subsection `sec:acausal-trade-review` (meta-prior over inference functions; best-respond-to-self; the $\widehat{\mathrm{IC}}_{ij}$ detector; TDT/FDT/LDT grounding via `tdt2010`,`fdt2017`,`critch2020ai`) plus a critical [Open] block: the detector is observational, not adversarially verifiable — its three assumptions (shared meta-prior, self-knowledge accuracy, adequate probes) are its attack surface, reducing to the ch39b cost relation. Filled the Worked Example (causal bargaining + acausal coordination) and replaced the WWCTV stub with 3 bullets (2 disconfirmers + 1 adversarial detector-evasion).
- **ch40 verdicts folded in.** Downgraded six over-credited status cells (pivotal→"Renamed; open"; capability-generalizes→"Conjectural; hope"; human-feedback→"Circular at limit (ch39b)"; deception→"Easy case only (ch39b)"; boxing→"Relocated, not closed"; multipolar→"Reframed; points to risk") and added `\section{Adversarial-Verifiability Reading}` with the per-row hostile-critic verdicts, pointing to ch39b.
- **WWCTV pass across 14 developed sections + ch43 stub.** Added one amended strong (mostly adversarial-direction) falsifier each: ch02 (one-box pivotal tempo), ch03 (unprojectable safe set + GSAI), ch04 (value-update dilemma horns), ch06 (steering⇒agency; detection not definition — per author), ch07 (residual steering, cross-ref ch10/ch36), ch08 (forgeable + non-enumerable), ch09 (composite unidentifiable), ch10 (forgeable indicators paragraph), ch11 (reach hiding anti-correlated), ch12 (discontinuous jump), ch13 (internalized coordination + footprint counter — per author), ch14 (co-scaling hinge → pause/stop), ch26 (corrigibility theater), ch27 (manipulation unidentifiable), ch43 (bearer-map identifiability = verifiability instance — per author's correction that "hidden map" was really an accuracy issue).
- **Build re-verified:** `./build.sh` exit 0, 0 undefined references.

## Round 3 (same session) — agreed-falsifier completion pass
- Author: "there seemed to be other strong falsifiers for other chapters. When I didn't discuss them, I agreed with them." Interpreted as: capture the un-discussed strong falsifiers from the per-chapter list too. Identified the falsification-section coverage gap (18 WWCTV + ch20/ch36/ch41 variant-named + ch39b; ch40 = stress test itself) and filled the rest.
- **Created WWCTV sections in 22 chapters** (placed before the closing Summary/Conclusion): ch01, ch05, ch15, ch16, ch17, ch18, ch19, ch21, ch22, ch23, ch24, ch25, ch28, ch29, ch30, ch31, ch32, ch34, ch35, ch37, ch38, ch42. Each: short thesis lead + 1–3 agreed strong falsifiers, adversarial-direction, cross-referencing `ch:verifiability-ontology` (and ch:dynamical-guarantee / ch:manipulation-false-consent / ch:lethality-stress-test-open-issues where relevant). ch35 carries the pivotal-process-renames-pivotal-act bullet; ch29 carries the forgeable+non-enumerable conserved-set bullet (seeds the two BIG REVIEWs in-text).
- **Appended to 3 existing falsification sections** (prose style): ch20 (bundle-inference identifiability + present-benign-inference), ch36 ("name a perturbation a superintelligence can't recognize as a test" — fulfils the perturbation-recognition mirror TODO), ch41 (target may be unmeasurable: authored vs induced value change indistinguishable from inside).
- **Replaced stub WWCTV placeholders** in ch39 (safety case) and ch44 (synthesis) with real agreed falsifiers (safety case certifies only imagined failures; book's master adversarial-verifiability disconfirmer). Rest of those two chapters remain `[STUB]`.
- **Build re-verified:** `./build.sh` exit 0, 982 pages, 0 undefined references / citations.

## Session end
- Author confirmed un-discussed strong falsifiers were agreed; Round 3 completed WWCTV coverage (22 new sections + 3 appends + ch39/ch44 stub replacements).
- Added Manuscript TODO: **ch33 acausal trade section** (`sec:acausal-trade-review`) — promote review seed to full draft (TDT/FDT vs detector, probe/threshold/evasion bounds, percolation wiring, mitigations, remaining stubs).
- Updated perturbation-recognition TODO to note ch36 now states the blunt challenge in prose.
- **Build re-verified:** `./build.sh` exit 0, 982 pages.

## Open / next
- Execute the two BIG REVIEWs (conserved-property forgeability budget in ch29; pivotal-process conditions or downgrade in ch35).
- Resolve ch39b's three inline cruxes: define `c_fake`/affordable-surplus model; perturbation-recognition (mirror into ch36); bound undetectable controllers.
- Decide whether to do the full Part-IX/X renumber (ch39b → ch40, shift ch40–ch44).
- Run the verifiability-label pass across the drafted metric chapters and propagate into ch39 (safety case, still a stub).
- ch33 still `status: stub` in book.yml and retains two `[STUB]` markers (privacy islands L45; nothing else load-bearing) — promote to draft after those are filled.

## Key paths
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex` (new)
- `parts/part09-safety-cases.tex`, `metadata/book.yml`, `metadata/TODO.md`, `references/external-alignment.bib`
- `chapters/ch40-lethality-stress-test-open-issues.tex` (hostile-critic target)

## Commits
- `54ad1ea` — Propagate canonical notation, refresh ledgers, and tighten continuity bridges.
- `f19ba8b` — Add adversarial WWCTV falsifiers book-wide and seed ch33 acausal trade.
