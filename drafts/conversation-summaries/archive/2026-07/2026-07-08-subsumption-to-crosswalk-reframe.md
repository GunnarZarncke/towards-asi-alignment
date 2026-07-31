# 2026-07-08 — "Subsumption" → "field crosswalk" reframe + hostile review

## Trigger
Impressions-level discussion of how a critical reviewer would see the project, then how to improve the "outside" and the private vocabulary. User flagged that the highest-risk move is telling existing researchers their agendas are "subsumed," and asked to reduce conflict (proposed "mappings"). Chose the terminology-only option: replace the word in reader-facing prose with a conditional/directional term, keep the claims, add a "what the agenda keeps that we don't" line per agenda. Also asked for a hostile review, a falsifiable-artifact ranking, an LW-reviewer mapping, and an AI-drafting-filter quantification (discussion only for those; no edits beyond the reframe + hostile-review.md).

## Done
- **New file `hostile-review.md`** (repo root): full-strength adversarial critique (velocity/AI-volume, zero external contact, proof-spine axiom framing, the subsumption reputational risk, private vocabulary, PDF-as-flagship, fictional worked example, recently-patched rigor apparatus, "what would change this"). Checked against repo state (git log, book-stats, formal/, claims-ledger, strategic-advice).
- **"Subsumption" → "field crosswalk / special case / projection" across reader-facing prose only:**
  - 8 site cards (`site/src/content/cards/subsumption-*.md`): title `Subsumption — X` → `Field crosswalk — X`; "Forward subsumption" → "Forward projection"; appended an italic **"What X keeps that this crosswalk does not replace"** line to each body.
  - Site chrome: `FieldSubsumptionsTable.astro` (h2 + prose), `cards/index.astro` (section title), `LeanGraphNav.astro` (label), `badges/index.astro` (blurb), `sync-lean-spine.mjs` (graph titles), `reading-paths/researcher-applied.md` (blurb).
  - `metadata/book.yml` part05/06/09 summaries + synced generated `tables/part-roadmap.tex`: "subsuming X" → "relating X to it as special cases and separations".
  - Part openers `parts/part02,05,06,09`: "existing-work subsumption" → "existing-work crosswalk".
  - Chapters: `ch25` (subsection title, claim label `[Shutdown as a special case]`, "recovered as a special case"), `ch28`, `ch30` (subsection titles → "… : A Special Case"), `ch44` (pivotal act "subsumes" → "contains as a limiting case" / "Treating the act …").
  - Appendix I `appG-lean-proof-spine.tex` (in PDF): section title "Rederived and Subsumed" → "… and Mapped"; 8× `\paragraph{Book subsumption.}` → "Book projection."; figure caption; `SUBSUMED` badge text → `MAPPED`; corollary display name; body prose spots.
  - `REVIEWING_FOR_AGENTS.md` (section heading + gem-map line + posture paragraph), `AGENTS.md` (gem-map mention), `formal/README.md` (module-map label).

## Decisions
- **"Crosswalk" not "mappings".** "Mapping" alone under-committed (sounded like mere analogy); "crosswalk / special case under conditions / projection" keeps the directional claim while dropping the conquest tone. It is also *more accurate*: several cards (low-impact, quantilization) claim the agenda is separable/weaker — the opposite of subsumption — so a uniform "field crosswalk" prefix fits all eight.
- **Added residue lines** ("what the agenda keeps") to defuse the "you dismissed my work" reaction — the single most conflict-reducing change, per user's chosen option.
- **Did NOT rename identifiers**: Lean module/theorem names (`*_subsumption_*`, `FieldSubsumptions.lean`), JSON ids, card URL **slugs** (`/cards/subsumption-*/` are already posted on LessWrong), figure filenames, and all `\label`/`\ref`/`\leanid` anchors. Renaming breaks the Lean build, cross-refs, and public URLs with no reputational upside.
- **Left historical logs / internal `review/` / `metadata/TODO.md` untouched** (records of past work, not manuscript).
- Site lint clean; no cross-reference labels changed, so LaTeX build and site should be unaffected.

## Open / next
- **Recommended single-sentence add at top of Appendix B** (not yet done): state plainly that these are directional, conditional relationships offered for the named agenda's authors to check — not claims to have absorbed or solved their work. Puts the humility in the framing that reaches the researcher.
- **Deferred (discussion only this session):** de-emphasize the 1,149-page PDF as flagship (lead README/stats with site + claim cards); per-part chapter renumbering (high-risk: touches ~1,646 anchors, `\leanspine` refs, book.yml, claims-ledger, site sync — do as its own verified pass); glossary expansion + kill/demote/replace list (correction parasite, fitness, deployment mass, preservation envelope, selection handle; add missing *grounding viability*); AI-drafting-filter paragraph for preface/About (proxy: manuscript ≈ 4–14× author steering-doc word volume; no true accept/reject rate reconstructable from single-author git history).
- **LW reviewer targeting (discussion):** strongest matches Steven Byrnes (bundle/bottleneck; already cited his brainstem comment), Jan Kulveit (MB6 basin/gradual-disempowerment crux), TurnTrout (AUP crosswalk — highest leverage + risk). Post one matched card each, not the whole book.

## Key paths
- `hostile-review.md`
- `appendices/appB-bridge-crosswalk.tex`, `appendices/appG-lean-proof-spine.tex`
- `site/src/content/cards/subsumption-*.md`, `site/src/data/field-subsumptions.json` (headlines already nuanced; ids/slugs kept)
- `metadata/book.yml` (part summaries), `tables/part-roadmap.tex` (generated)

## Commits
- (this session) `hash` — reframe "subsumption" as "field crosswalk" in reader-facing prose; add hostile-review.md
