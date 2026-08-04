# Glossary prose-pass quality bar

Working instructions for rewriting entries in [`reference/field-agendas/inter-agenda-term-glossary.md`](../../reference/field-agendas/inter-agenda-term-glossary.md).

## Goal

Replace one-line stubs with **source-backed**, **disambiguating** entries. The reader should learn (1) what the term means in its home agenda, (2) why nearby terms are close but not interchangeable, (3) how to translate to other agendas' concepts.

## Must do

1. **Consult sources** before rewriting:
   - In-repo: `appendices/appE-glossary.tex`, `appendices/appB-bridge-crosswalk.tex`, relevant chapters, `metadata/concepts/bodies/`, `reference/field-agendas/field-agenda-index.md`, `reference/field-agendas/anthropic-acausal-taxonomy.md`, CIRIS findings under `~/repos/ciris/review/findings/` when CIRIS-tagged, Lean field modules under `formal/AlignmentProofSpine/Field/` when applicable.
   - External agendas: official papers / LW posts / org pages named in the agenda index — use WebSearch/WebFetch when the repo lacks the primary text. Prefer primary authors over secondary summaries.
2. **Definition** = 2–4 sentences in the source agenda's mouth (not book-first paraphrase unless the source *is* the book).
3. **Not the same as** = for each nearby term, one clause of *why* (mechanism / criterion / scope). Drop names that are not close enough to confuse.
4. **Cross-agenda** = translate, don't just list. Tag (*same crux* / *strict subset* / *partial overlap* / *homograph* / *orthogonal*) **plus** explanation.
5. Mark uncertainty: if a source was thin or contested, say so in Cross-agenda or a trailing italic note.
6. Do **not** invent manuscript coinages; do **not** edit App E / chapters in this pass.

## Output shape (per batch)

Write a markdown file under `drafts/glossary-prose-pass/` containing **only** rewritten `#### headword` blocks ready to paste into the glossary. Keep alphabetical order within the batch. Note at top which sources were consulted and which entries remain thin.
