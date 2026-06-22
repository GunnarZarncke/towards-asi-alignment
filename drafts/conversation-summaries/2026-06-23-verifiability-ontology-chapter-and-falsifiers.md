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

## Open / next
- **ch40 hostile-critic pass** delivered in chat (not yet written into the manuscript). If wanted, fold the surviving lethalities into ch40's prose / status column (ch40 is already flagged in TODO.md as needing flesh-out to ~9k words).
- Resolve ch39b's three inline cruxes: define `c_fake`/affordable-surplus model; the perturbation-recognition question (mirror into ch36); bound undetectable controllers.
- Decide whether to do the full Part-IX/X renumber.
- Optionally run the verifiability-label pass across the drafted metric chapters and propagate into ch39 (safety case, still a stub).

## Key paths
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex` (new)
- `parts/part09-safety-cases.tex`, `metadata/book.yml`, `metadata/TODO.md`, `references/external-alignment.bib`
- `chapters/ch40-lethality-stress-test-open-issues.tex` (hostile-critic target)

## Commits
- `8ee4956` — Propagate canonical notation, refresh ledgers, and tighten continuity bridges.
