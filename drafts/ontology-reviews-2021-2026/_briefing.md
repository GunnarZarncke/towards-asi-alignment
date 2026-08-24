# TSA briefing for ontology-source reviews

Low-effort reviews of 2021–2026 ontology-forming sources against **Towards Superintelligence Alignment (TSA)**. Parent list: `drafts/new_ontologies_2021_2026.md`. Motive: `drafts/ngo-ontology-and-TSA.md` plus the risk that LLMs (and AI-drafted TSA prose) stick to trained ontologies and miss preparadigmatic primitives.

Do **not** edit the manuscript, Lean, site, or experiments. Write only your assigned result file.

## What TSA is

Alignment = preserve grounded, human-correctable value-bearing processes across capability growth, ontology shift, successor creation, and strategic selection. Six intro claims:

| # | Claim | Core question | Parts / chs |
|---|--------|---------------|-------------|
| 1 | Boundary | Where is the real optimizer? | II, ch06–ch10 |
| 2 | Value-bundle | Do compressed values, bearers, and correction survive change? | IV–V, ch15–ch24 |
| 3 | Grounding | Do symbols stay tied to value-relevant reality? | I, IV, VI, IX, X |
| 4 | Correction | Does human value-update stay causally effective (CCI)? | VI, ch25–ch29 |
| 5 | Successor | Do constraints inherit to copies/delegates/replacements? | VII, ch30–ch33 |
| 6 | Basin / selection | Does the deployment environment select for preservation? | VIII, ch34–ch38 |

Second-tier: differential growth, transport/laundering, adversarial measurement, civilizational limit (ch45–ch48).

Lean spine is a **conditional skeleton** (proof / counterexample / bridge). Bridges `MB1`–`MB11` are assumptions, not “ASI alignment is proved.” Field map: `appendices/appB-bridge-crosswalk.tex`, `reference/field-agendas/`. Experiments are toy sanity checks with recorded negatives.

## Fast TSA vocabulary (do not invent synonyms)

- **Boundary discovery** — find the real optimizer, not the visible model; composite / growing / merging agents.
- **Ontology trap / task ontology** — capability and incentive tests are relative to a chosen ontology (ch11).
- **Value bundle** — low-dimensional control geometry, not scalar reward; **bearer map** — what values apply to.
- **Transport** — semantic / bundle / bearer / correction / successor continuity (words surviving ≠ meaning surviving).
- **CCI** — correction-channel integrity: uncaptured causal force of human correction.
- **Successor stability** — inheritance of invariants, not label preservation.
- **Selection environment / attractor** — institutions, funding, prestige select which systems reproduce.
- **Goal laundering / cost of faking** — safety signal cheap to fake.
- **Hostile test** (ch44) — if the original problem can be restated through the proposed response, it was renamed not solved.

Grep first: `chapters/`, `appendices/appB-bridge-crosswalk.tex`, `reference/field-agendas/`, `metadata/concepts/`, `REVIEWING_FOR_AGENTS.md`. Read **at most two** matching TSA files after grep.

## Coverage labels (use exactly one)

- `already-in-TSA` — same primitive, possibly different name; deletion would not change TSA.
- `partial` — TSA has a nearby object; source adds a split, unit, or relation TSA underspecifies.
- `missing` — TSA cannot currently express the source’s object without stretching.
- `orthogonal` — real ontology, little alignment/TSA purchase.
- `rival` — alternative decomposition that would compete with a load-bearing TSA cut.

## Recommended action (use exactly one)

`ignore` | `cite-in-crosswalk` | `absorb-as-special-case` | `add-reverse-gap` | `rival-decomposition`

## Output file schema (required)

```md
# <Concept name>

- **Date:** YYYY-MM-DD or year
- **Field:** LessWrong | <science field>
- **Source:** URL
- **Source read:** full | abstract-only | failed
- **TSA files consulted:** paths
- **Keywords grepped:** list

## Source ontology
2–4 sentences. What new primitive, unit, relation, or state variable is introduced? What does it replace?

## TSA coverage
- **Status:** already-in-TSA | partial | missing | orthogonal | rival
- **Closest TSA terms/chapters:**
- **Overlap:** 1–3 sentences with chapter numbers.
- **Gap:** 1–3 sentences. What TSA cannot express, or only by renaming.

## Applicability to TSA
- **Score (0–5):** 0 ignore; 1 background; 2 cite; 3 reverse-crosswalk / gap; 4 should change a TSA cut; 5 rival or missing load-bearing primitive
- **Why:** 2–4 sentences.
- **Ontology-stickiness risk:** Would a model trained before this source miss it? Does TSA already include, rename, exclude, or fail to see this primitive?
- **Recommended action:** ignore | cite-in-crosswalk | absorb-as-special-case | add-reverse-gap | rival-decomposition

## One-line finding
One sentence.
```

Keep the file under ~800 words. If the source cannot be fetched, score conservatively from the list summary and say so. Do not pad with TSA recap.
