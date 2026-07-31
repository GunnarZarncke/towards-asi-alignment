# 2026-07-18 — Catchy accessible phrases for dry glossary terms

## Trigger
Follow-on to the ch25/ch26 "correction in the small vs in the large" session. User asked to go through `appendices/appE-glossary.tex` and find other dry technical terms that could use a short, memorable phrase a mixed-audience reader could relay to someone else, on the model of "keeping the human in the loop" for correction-channel integrity.

## Done
- Surveyed all glossary entries; proposed catchy leads for grounding viability, bearer map, correction-audit evasion, transport, conserved properties, value bundle, and (with a caution flag) deployment growth rate/fitness. Left `agent`, `boundary`, `goal`, `correction channel`/CCI alone as already well-served or risking over-simplification.
- User selected only **bearer map** initially; implemented "who still counts" (matches ch47's own title, `ch:bearers-of-value`).
- User found the other proposed phrases too long, and "audit theater" ambiguous; iterated to shorter versions.
- Implemented in `appendices/appE-glossary.tex`:
  - Value bundle: lead "steering, not scoring."
  - Transport: lead "surviving development."
  - Grounding viability: lead "silent meaning gap" (upgraded from the entry's existing "silent gap," applied consistently at both occurrences, L64/L71/L73).
  - Correction-audit evasion: "checkbox compliance" woven into the existing sentence, not as a headline lead (per user instruction it should drive intuition in text, not be the marquee phrase).
- Dropped "conserved properties" catchy phrase ("inherited, not resembled") — user didn't follow it and said "if it fails me it is no good"; no replacement forced.
- Did not implement the fitness/"survival of the most-deployed" or preservation-conditions lead sentence — not selected/revisited by the user.

## Decisions
- Kept catchy phrases as inline lead clauses within existing sentences (matching the ch25/ch26 pattern and the existing "who still counts"-style edits), not as new bolded headers or separate glossary structure changes.
- When a proposed phrase failed the user's plain read-through, dropped it rather than adding an explanation — per house style, a phrase that needs explaining has failed its purpose.

## Open / next
- `deployment growth rate` / `fitness` ("survival of the most-deployed") and `preservation conditions` lead-sentence options were presented but not decided on; revisit if wanted.
- `conserved properties` still has no catchy lead; open if a better one occurs to either of us later.
- No build (`./build.sh`) run this session; edits are prose-only within existing sentences, low risk.

## Key paths
- `appendices/appE-glossary.tex` (all edits in the "Values, bundles, and bearers," "Grounding," and "Correction" sections)

## Commits
- `e35d47d` Add catchy accessible leads to five glossary entries
