# 2026-07-18 — Correction "in the small" vs "in the large"

## Trigger
User found the ch26 title/concept "Correction-Channel Integrity" too technical and asked about renaming it to "Keeping the Human in the Loop," relating the former as implementing the latter. Discussion surfaced that ch14/ch25 already explicitly reject the naive "human in the loop" framing as insufficient, which would contradict a straight rename. User reframed as two levels: correction "in the small" (individual human-in-the-loop) vs "in the large" (keeping humanity, or all entities of moral concern, in the loop), and asked to separate these explicitly in the chapters.

## Done
- Surveyed scope of the `correction-channel-integrity` term/label (`ch:correction-channel-integrity`, `CCI`): used across ~50 files (chapters, `metadata/concepts.yml`, `metadata/book.yml`, glossary, Lean-spine crosswalk, `appB-bridge-crosswalk.tex`). Concluded a full rename was not warranted; kept all labels, filenames, and the `CCI` term unchanged.
- `chapters/ch25-correction-causal-channel.tex`: renamed closing section "Correction as Civilizational Self-Modification" → **"Correction in the Large"** (label `sec:civilizational-self-modification` unchanged, no external refs to it). Rewrote opening to name the small/large distinction explicitly, credit ch26 as the "in the small" formalization, forward-point to ch28 (`ch:extrapolative-correction`) for the large-scale formal treatment, and added a flagged-open-question sentence on whether "in the large" correction should extend to non-reflective non-human moral patients (e.g. animals), pointing to ch47 (`ch:bearers-of-value`) as the closest existing treatment without resolving the question.
- `chapters/ch26-correction-channel-integrity.tex`: added a sentence to the "Chapter Thesis" section stating the chapter formalizes correction *in the small* (single correcting agent, single target system), with forward pointers to ch25 §"Correction in the Large" and ch28.
- Left `ch14-intelligence-deepens-misalignment.tex` L488 ("Correction is not a button, a preference label, or a human in the loop") untouched — it's a compact forward-pointer, not a place needing the small/large distinction spelled out.
- Did not touch `metadata/concepts.yml`, `appendices/appE-glossary.tex`, or `metadata/book.yml` — user had provisionally chosen to update the site concept card too, but the small/large split was addressed via the chapter-prose route instead; concepts.yml/glossary updates were not requested in the follow-up and were not made.

## Decisions
- Rejected renaming the ch26 chapter title or the `CCI` term/label itself: it's the book's central formal quantity, referenced by label from ~50 files and the Lean proof spine (`P24`); a full rename was high-risk/low-benefit for what is fundamentally a framing request.
- Named the two levels "correction in the small" / "correction in the large" (mirrors "programming in the small/large" idiom) rather than reusing "human in the loop" as the large-scale term, to avoid contradicting ch14/ch25's existing rejection of the naive human-in-the-loop framing.
- Flagged the animal/moral-patient scope question rather than resolving it, per house style (surface tradeoffs, don't invent answers to open philosophical forks).

## Open / next
- If desired later: extend `metadata/concepts.yml` (`correction-channel-integrity` slug) and `appendices/appE-glossary.tex` (L104 entry) to mention the small/large split for the site-facing concept card and glossary — not done this session, was explicitly out of scope for the final ask.
- `chapters/ch47-bearers-of-value.tex` does not currently discuss animals/non-reflective moral patients; the ch25 cross-reference points there as "the closest existing treatment," but the chapter itself would need new material to actually answer the question if that's ever wanted.
- No build (`./build.sh`) was run this session to confirm the two edited chapters compile; edits are prose-only within existing sections/labels, low risk, but worth a build pass before next full compile check.

## Key paths
- `chapters/ch25-correction-causal-channel.tex` (§"Correction in the Large", L1220–1233)
- `chapters/ch26-correction-channel-integrity.tex` (Chapter Thesis section, small/large pointer)
- `chapters/ch47-bearers-of-value.tex` (bearer-continuity question, referenced but not edited)

## Commits
- `e6ff088` Name correction "in the small" vs "in the large" in ch25/ch26
