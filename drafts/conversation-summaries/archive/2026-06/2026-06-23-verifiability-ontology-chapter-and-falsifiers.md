# 2026-06-23 — Verifiability/ontology chapter + strong falsifiers

## Trigger
Author asked, across a multi-turn session: (1) tabulate each chapter's "What Would Change This View" (WWCTV) section by count and harmless-vs-dangerous direction; (2) critique that analysis with a security mindset (Yudkowsky-blunt); (3) suggest *strong* per-chapter falsifiers; then (4) responded with detailed comments and asked to: make a perturbation-recognition TODO, hand ch48 to a hostile critic, and **create a new chapter** addressing the two master cruxes (metric verifiability under adversarial optimization; ontology adequacy) with a minimal draft.

## Done
- **New chapter** `chapters/ch43-verifiability-and-ontology-adequacy.tex` ("What Survives an Adversary: Verifiability and Representability"). Minimal seed draft (~1500 words) with: observable / i.i.d.-robust / adversarially-verifiable distinction; the *ontology-adequacy reduces to detection* argument (reliable steering = control ⇒ agency, answering the author's pushback); the **cost relation** `c_fake(M,Δ)` that unifies strategic opacity (ch10), staged transport (ch46), goal laundering (ch48), and scale-fluid evasion (ch45) and reframes coordination-internalization (ch13) as having a measurable footprint; GSAI as the strong/proof form (out of scope); worked example on correction-channel integrity; its own WWCTV; Summary; inline `TODO[open-crux]`/`TODO[formalize]` markers.
- **Wired** into `parts/part09-safety-cases.tex` between ch46 (safety case) and ch48 (lethality stress test), preserving ch48's existing forward bridge to ch45.
- **Bib**: added `dalrymple2024gsai` (Towards Guaranteed Safe AI, arXiv:2405.06624) to `references/external-alignment.bib`.
- **metadata/book.yml**: added `ch47` entry (status: draft, with numbering note).
- **metadata/TODO.md**: added cross-cutting "Verifiability-label pass" and "Perturbation-recognition crux" manuscript items; added two Formalization-track rows (cost-of-opacity / budget verifiability; prove-bound undetectable controllers) owned by ch47.
- **Build verified**: `./build.sh` exit 0, 962 pages, 0 undefined references; new chapter present in `book.toc`/`book.aux`.

## Decisions
- **Filename `ch47` instead of renumbering.** Inserting in Part IX would otherwise force renaming ch48–ch48 and many references. `39b` keeps the file list sorted and the insertion obvious. **Consequence:** displayed chapter numbers for Part X auto-shift +1 (ch48 file now displays as ch45, etc.); cross-refs use `\label`/`\ref` so they remain correct. A full renumber (ch48→41 … ch48→45, new→40) is the clean follow-up but is invasive; deferred and flagged.
- **Placed before ch48, not after**, so ch48's "next chapter … Chapter~\ref{ch:value-change-at-stake}" bridge stays adjacent to ch45.
- Claim strength kept at **[Conjectural]/[Open]** for the cost relation and the representability bound; chapter explicitly states the book supplies *targets*, not *proofs*, and points to GSAI for the proof form (matches Lean-spine "bridges are out of scope" framing in TODO.md).
- The harmless/dangerous WWCTV tally from earlier in the session was re-binned under critique into three buckets (over-worried / blind / solution-fails); the headline "≈88% harmless" was judged misleading (mis-binned "instrument can't measure" points as harmless). No manuscript edits were made for the tally itself.

## Round 2 (same session) — folded verdicts, acausal review, WWCTV pass
- **Two BIG REVIEW items** added to `metadata/TODO.md` (new "Big reviews" section): (a) conserved-property transport decoupled from safety (forgeable + non-enumerable), spanning ch08/ch46/ch48; (b) pivotal-act reframe may rename not dissolve the lethality, spanning ch48/ch48/`P35`.
- **ch48 acausal-trade review.** Read the source extract (`context/extracts/acausal-trade-uad-formalization.md`; the author's own `zarncke2025acausal`). Added subsection `sec:acausal-trade-review` (meta-prior over inference functions; best-respond-to-self; the $\widehat{\mathrm{IC}}_{ij}$ detector; TDT/FDT/LDT grounding via `tdt2010`,`fdt2017`,`critch4620ai`) plus a critical [Open] block: the detector is observational, not adversarially verifiable — its three assumptions (shared meta-prior, self-knowledge accuracy, adequate probes) are its attack surface, reducing to the ch47 cost relation. Filled the Worked Example (causal bargaining + acausal coordination) and replaced the WWCTV stub with 3 bullets (2 disconfirmers + 1 adversarial detector-evasion).
- **ch48 verdicts folded in.** Downgraded six over-credited status cells (pivotal→"Renamed; open"; capability-generalizes→"Conjectural; hope"; human-feedback→"Circular at limit (ch47)"; deception→"Easy case only (ch47)"; boxing→"Relocated, not closed"; multipolar→"Reframed; points to risk") and added `\section{Adversarial-Verifiability Reading}` with the per-row hostile-critic verdicts, pointing to ch47.
- **WWCTV pass across 14 developed sections + ch47 stub.** Added one amended strong (mostly adversarial-direction) falsifier each: ch02 (one-box pivotal tempo), ch03 (unprojectable safe set + GSAI), ch04 (value-update dilemma horns), ch06 (steering⇒agency; detection not definition — per author), ch07 (residual steering, cross-ref ch10/ch46), ch08 (forgeable + non-enumerable), ch09 (composite unidentifiable), ch10 (forgeable indicators paragraph), ch11 (reach hiding anti-correlated), ch12 (discontinuous jump), ch13 (internalized coordination + footprint counter — per author), ch14 (co-scaling hinge → pause/stop), ch46 (corrigibility theater), ch48 (manipulation unidentifiable), ch47 (bearer-map identifiability = verifiability instance — per author's correction that "hidden map" was really an accuracy issue).
- **Build re-verified:** `./build.sh` exit 0, 0 undefined references.

## Round 3 (same session) — agreed-falsifier completion pass
- Author: "there seemed to be other strong falsifiers for other chapters. When I didn't discuss them, I agreed with them." Interpreted as: capture the un-discussed strong falsifiers from the per-chapter list too. Identified the falsification-section coverage gap (18 WWCTV + ch46/ch46/ch45 variant-named + ch47; ch48 = stress test itself) and filled the rest.
- **Created WWCTV sections in 22 chapters** (placed before the closing Summary/Conclusion): ch01, ch05, ch15, ch16, ch17, ch18, ch19, ch46, ch46, ch46, ch46, ch46, ch46, ch48, ch46, ch48, ch46, ch46, ch48, ch48, ch45, ch46. Each: short thesis lead + 1–3 agreed strong falsifiers, adversarial-direction, cross-referencing `ch:verifiability-ontology` (and ch:dynamical-guarantee / ch:manipulation-false-consent / ch:lethality-stress-test-open-issues where relevant). ch48 carries the pivotal-process-renames-pivotal-act bullet; ch48 carries the forgeable+non-enumerable conserved-set bullet (seeds the two BIG REVIEWs in-text).
- **Appended to 3 existing falsification sections** (prose style): ch46 (bundle-inference identifiability + present-benign-inference), ch46 ("name a perturbation a superintelligence can't recognize as a test" — fulfils the perturbation-recognition mirror TODO), ch45 (target may be unmeasurable: authored vs induced value change indistinguishable from inside).
- **Replaced stub WWCTV placeholders** in ch46 (safety case) and ch48 (synthesis) with real agreed falsifiers (safety case certifies only imagined failures; book's master adversarial-verifiability disconfirmer). Rest of those two chapters remain `[STUB]`.
- **Build re-verified:** `./build.sh` exit 0, 982 pages, 0 undefined references / citations.

## Session end
- Author confirmed un-discussed strong falsifiers were agreed; Round 3 completed WWCTV coverage (22 new sections + 3 appends + ch46/ch48 stub replacements).
- Added Manuscript TODO: **ch48 acausal trade section** (`sec:acausal-trade-review`) — promote review seed to full draft (TDT/FDT vs detector, probe/threshold/evasion bounds, percolation wiring, mitigations, remaining stubs).
- Updated perturbation-recognition TODO to note ch46 now states the blunt challenge in prose.
- **Build re-verified:** `./build.sh` exit 0, 982 pages.

## Open / next
- Execute the two BIG REVIEWs (conserved-property forgeability budget in ch48; pivotal-process conditions or downgrade in ch48).
- Resolve ch47's three inline cruxes: define `c_fake`/affordable-surplus model; perturbation-recognition (mirror into ch46); bound undetectable controllers.
- Decide whether to do the full Part-IX/X renumber (ch47 → ch48, shift ch48–ch48).
- Run the verifiability-label pass across the drafted metric chapters and propagate into ch46 (safety case, still a stub).
- ch48 still `status: stub` in book.yml and retains two `[STUB]` markers (privacy islands L45; nothing else load-bearing) — promote to draft after those are filled.

## Key paths
- `chapters/ch43-verifiability-and-ontology-adequacy.tex` (new)
- `parts/part09-safety-cases.tex`, `metadata/book.yml`, `metadata/TODO.md`, `references/external-alignment.bib`
- `chapters/ch44-lethality-stress-test-open-issues.tex` (hostile-critic target)

## Commits
- `54ad1ea` — Propagate canonical notation, refresh ledgers, and tighten continuity bridges.
- `f19ba8b` — Add adversarial WWCTV falsifiers book-wide and seed ch48 acausal trade.
