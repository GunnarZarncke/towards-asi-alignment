# 2026-09-29 — LW prose into chapters

kind: correction
uptake: local

## Trigger
Use Gunnar's LessWrong prose in the manuscript where it replaces a paraphrase or covers a missing aspect. Adjust authorship bars: `{GZ}` when the block is his; drop `AI` by cutting the section. Do not glue a new passage on by pointing at the surrounding prose. Additions are allowed when they cover a missing aspect.
Prompts: paraphrase-only (no prompt id in this session)

## Done
- content: Ch. 7 ontology-trap opening and leaky-boundary opening replaced from the UAD post; `{GZ}` bars split off. Anesthesia case was tried and removed.
- content: Ch. 16 inconsistency opening and Ch. 17 problem, readout gloss, and pairwise-comparison elbow replaced from the value-learning post; `{GZ}` bars split off. The stronger "only because evolution" sentence was not imported.
- content: Ch. 32 interface-versus-implementation and approval-legibility tell replaced from Friendly Telepaths; `{GZ}` bars split off.
- content: Ch. 9 new subsection `sec:continual-learning-lineage-ch09` from the continual-learning comment (lineage learns across deployments; developer tuning counts inside the socio-technical boundary). `{GZ}`. Cite `douglas2026artificialself`. Local-alignment count six to seven. One WWCTV bullet.
- content: Ch. 11 replaces the competence gloss with the four names from the measuring-intelligence comment (`I_pred` bits you can see coming, `I_ctrl` bits you can steer, memory bits you have to keep alive, residual surprise bits you fail to see coming). `{GZ}` split off the `{AI}` formula.
- content: Ch. 2 opens Value Change with the unfriendly-natural-intelligence prior: extreme food, drugs, and games are already the damage, and markets sell every desire. `{GZ}`. One WWCTV bullet. The desire catalog, anti-meme jargon, and "markets are worse than FAI" were not imported.
- content: Ch. 15 subsection `sec:higher-loops-acquired-ch15` from the control-theory comment: full comment text restored verbatim (2015-01-24). `{GZ}`. One WWCTV bullet. First pass had paraphrased; corrected on author request.
- content: Ch. 43 section `sec:checkable-delegation-ch43` from the Löbian-comment upshot only, verbatim blockquote. `{GZ}`. One WWCTV bullet. The ChatGPT thread summary was not used. First pass had paraphrased; corrected on author request.
- correction: Review pass on all LW `{GZ}` insertions — restored verbatim wording (shortening OK, rewriting not). Ch. 7 UAD ontology + leaky boundaries, Ch. 9 continual-learning comment, Ch. 11 four nicknames, Ch. 2 UNI opening, Ch. 16 inconsistency, Ch. 17 three blocks, Ch. 32 two telepath blocks. Ch. 15 control-theory and Ch. 43 Löbian upshot already verbatim.
- housekeeping: `drafts/project/self-audit/edit-attribution/author-provenance.jsonl` records that agent-committed `{GZ}` blocks are Gunnar's LessWrong prose. Pre-commit derive-bars initially flipped them to `GZ+AI`; span-ledger + `author_provenance_override` rows in `bar-updates.jsonl` restore `GZ`.
- bookkeeping: Bibliography summary check passed (518 keys) after the Ch. 9 cite. This pass added no cites.

## Decisions
- A new section is in scope when it covers a missing aspect. It still has to stand without a backward pointer into the previous paragraph.
- The ChatGPT exchange pasted inside the continual-learning comment is not GZ prose and was not used. The same exclusion covers the ChatGPT summary inside the Löbian comment; only the upshot came in.
- Invisible Hand and AI Safety Interventions stay out: both contain model-generated material.
- Developer-tuning-as-learning was missing. Composite-agency chapters already said the loop is the agent; they did not say that cross-deployment update is the lineage's continual learning.

## Open / next
- Senexism (2014) is the next unused post that still looks like his prose, for the thin successor chapters. Thou Art Rainbow and Unexpected Conscious Entities look model-assisted.

## Key paths
- `chapters/ch09-composite-agent.tex`
- `chapters/ch07-finding-boundary.tex`
- `chapters/ch16-value-bundle-model.tex`
- `chapters/ch17-low-dimensional-value-learning.tex`
- `chapters/ch32-self-modeling-self-opacity.tex`
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch02-artificial-civilization.tex`
- `chapters/ch15-values-compressed-control.tex`
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`

## Commits
- `9938a5627` Integrate Gunnar's LessWrong prose as {GZ} blocks across nine chapters.
