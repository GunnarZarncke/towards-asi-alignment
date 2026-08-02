# Glossary term audit (working notes)

**Status:** manuscript demotion pass — **partially shipped** (2026-08-02). Inter-agenda glossary prose pass complete; chapter/appendix plain-first edits below applied. **App E sync shipped** (homographs, new headwords, nearest-field deltas); site `concepts.yml` still open.

**Source rules:** v1.1 demotion ([`archive/2026-07/2026-07-08-glossary-terminology-demotion-release-notes.md`](conversation-summaries/archive/2026-07/2026-07-08-glossary-terminology-demotion-release-notes.md)); field translation from [`reference/field-agendas/inter-agenda-term-glossary.md`](../reference/field-agendas/inter-agenda-term-glossary.md).

**Out of scope here:** thin field-only headwords ([`glossary-prose-pass/THIN.md`](glossary-prose-pass/THIN.md)); App E rewrite; `metadata/concepts.yml` sync.

---

## What the inter-agenda glossary teaches this project

1. **Book-native terms are not field-default.** Each load-bearing coinage now has an explicit nearest field neighbor and a relation tag (*same crux*, *strict subset*, *partial overlap*, *homograph*, *orthogonal*). Manuscript prose should not imply equivalence where the glossary records projection or homograph.

2. **Homographs are the main reader-confusion risk.** Highest-impact collisions for editors:
   - **selection** — Zarncke deployment ecology (`selection environment`, `selection handle`) vs Demski in-optimizer search vs Wentworth selection theorems vs Goodhart selection
   - **corrigibility** — MIRI/CHAI shutdown-incentive vs Christiano dynamical basin vs book **CCI** (trajectory + capture resistance)
   - **verify / verifiability** — CIRIS identity attestation vs book **adversarial verifiability** (measurand survives optimization)
   - **alignment / cooperation / corrigibility (CIRIS)** — ops marketing vs Hubinger inner/outer vs book measurement spine

3. **Field “wins” are often strict subsets of book predicates.** AUP, quantilizers, interruptibility, ELK latent readout, debate local truth, off-switch — each can hold while **CCI** fails. Do not collapse these in chapter prose or bridge rows without the projection qualifier App E already uses.

4. **Plain-first demotion is confirmed, not replaced.** Inter-agenda entries use **deployment leverage**, **deployment growth rate** (`Fit_E`), **preservation conditions**, **point of control over deployment** as reader-facing labels. **`selection environment`** remains a justified book headword (MB6 / ch34) but must keep the Demski disambiguator when “selection” appears outside ch34.

5. **Rename already decided:** `correction parasite` → **correction-audit evasion** (operational); `preservation envelope` → **preservation conditions** (retired). Parasite stays metaphor in ch36 only.

6. **CIRIS is a falsifier agenda, not a synonym stack.** Verify, Lens, WA, signed traces map to MB1/MB4/adversarial-verifiability surfaces; green traces ⇏ CCI. Useful when calibrating ch36, certification, and composite-agency claims.

---

## Classification key (manuscript pass)

| Class | Manuscript action |
|---|---|
| **A** | Plain/field term in prose; symbol or book shorthand parenthetical after definitional home only |
| **B** | Keep book-native; definitional home + App E + inter-agenda headword |
| **C** | Plain or field term locally; book superclass when the finer distinction matters |
| **D** | Retired; grep and replace remnants |
| **H** | Homograph watch — keep book term but add one-line disambiguation at first use in chapter |
| **P** | Projection — field cousin named as *strict subset* / *partial overlap*, never as equivalent |

---

## Book-native inventory (from inter-agenda “Zarncke / book” row + demotion list)

| Term | Class | Plain / reader-facing | Field neighbor | Relation | Definitional home | Drift priority |
|---|---|---|---|---|---|---|
| selection handle | A/C | point of control over deployment | compute governance gate, RSP deploy gate | *strict subset* instances | ch34 | **high** — appendices + ch02/35/38 |
| fitness | A | deployment growth rate (`Fit_E`) | Wentworth selection (homograph) | symbol-only after def | ch34 | low — formulas |
| preservation envelope | D | preservation conditions (`Π⃗`) | — | renamed | ch34 | low — grep remnants |
| selection environment | B + H | deployment environment (plain in ch34 body) | Demski selection-vs-control; Wentworth theorems | *homograph* | ch34 | **high** — ch02/05/35/38/48 |
| deployment leverage | B | (canonical plain) | institutional deploy footprint | book-native | ch34 | low |
| deployment growth rate / Fit_E | B | (canonical plain) | selection theorems (homograph) | book-native | ch34 | low |
| preservation conditions | B | (canonical plain) | GSAI spec coverage (cousin) | *partial overlap* | ch34 | medium |
| correction-audit evasion | B | compliance theater ( gloss ) | Goodhart-as-selector, capture theater | *same crux* | ch36 | medium |
| correction channel | B | human judgment → handles | MIRI off-switch, CIRIS WA/deferral | *partial overlap* | ch25 | medium |
| CCI | B + P | correction-channel integrity | corrigibility family, interruptibility, AUP | *strict strengthening* / projections | ch26 | medium — don’t equate |
| corrigibility (field) | C | name agenda explicitly | MIRI vs Christiano homograph | *homograph* | ch27 / App B | medium |
| UAD | B | unit-attribution discovery | CIRIS Verify (identity) | *partial overlap* / falsifier | ch07, App N | low |
| boundary (operational) | B | discoverable agent cut | embedded agency, NAH latents | *partial overlap* | ch07 | low |
| value bundle | B + P | low-dimensional value directions | shard theory, CIRL k=1, reward component | *partial overlap* | ch16–17 | low |
| bearer map | B | who values attach to | ontology identification, pointing | *partial overlap* | ch18+ | low |
| transport | B | bundle/bearer/correction/successor layers | — | book-native | ch20–23 | low |
| conserved properties | B | successor invariants | MB10 forgeability counterexample | book-native | ch29–31 | low |
| adversarial verifiability | B | measurand under optimization | lie detection, Lens triage, eval pass | *strict strengthening* | ch43 | medium |
| certification-under-manipulation | B | cert signal gameability | frontier eval, RSP gates | *partial overlap* | ch43 | low |
| strategic opacity | B | hidden control locus / capability | scheming, situational awareness | *partial overlap* | ch10 | medium |
| substitution hazards | C | nearest-unblocked, channel sub, edge inst. | problem substitution (Meta) | *orthogonal* Meta vs object-level | ch07, App F | medium |
| ICI / inferential coupling | B + P | residual coupling after severance | acausal trade / ECL | *same crux* at limit | ch35 | low |
| grounding viability | B + P | no silent meaning gaps | GSAI specification coverage | *partial overlap*; book weaker | MB9 | low |
| hidden productive B-IQ bound | B | MB7a–c bridge quantity | strategic opacity, hidden reasoning | empirics open | ch10 / MB7 | low |
| alignment basin | B + P | stable region under dynamics | Christiano corrigibility basin | *partial overlap* / metaphor cousin | ch03/35/37 | low — paraphrase at first use |
| goal (operational) | B | operational goal predicate | outer alignment target | *partial overlap* | ch20+ | low |
| BIQ / EAI | B | bounded / effective agency index | capability metrics | book-native | experiments | low |
| VFS | B | audit-plane artifact store (method) | CIRIS signed traces | *partial overlap* methodology | App N | low |

---

## Manuscript edit queue (priority)

### Shipped (2026-08-01)

1. **`selection environment` → deployment environment** — ch02, ch05, ch07, ch13, ch35 (footnote), ch36, ch38, ch48, intro, part08, appC, appN, appM; ch34 scenario prose. Retained at definitional home (ch34 §opening, appE) with Demski homograph note.
2. **`selection handle` → point of control over deployment** — ch05, ch48, appG definition, appM table. Retained as shorthand in ch34/appE after plain definition.
3. **`deployment mass` retired** — use **deployment leverage** (`\mu_E`) everywhere; ch34/appE definitions simplified (no “for short” alias). Equation labels `eq:deployment-mass-*` unchanged.
4. **ch10 anthropic cite hygiene** — removed `zarncke2026anthropics` from predictor-genesis references; disambiguated anthropic capture vs completion in §Perils of predictors.
5. **Projection hygiene** — already present ch25 (corrigibility vs CCI), ch27 (field invariants ⇏ CCI), ch43 (ELK ⇏ adversarial verifiability); no App B collapse found.

### Still open

- Residual ch34 in-chapter shorthand (`selection handle`, `fitness` in formulas) after definitional block — acceptable at home.
- Site `metadata/concepts.yml` / MB6 and CCI cards parity spot-check.
- Full appendices grep for any missed downstream coined shorthand.

### Shipped (2026-08-02) — App E sync

- Homograph patches: CCI (Christiano vs MIRI/CHAI); selection environment + Demski/Wentworth on `Fit_E`; experimental BIQ vs hidden productive B-IQ.
- New headwords: strategic opacity, hidden productive B-IQ bound, ICI, adversarial verifiability, certification-under-manipulation, selection environment.
- Nearest-field deltas: boundary (Friston homograph), goal, transport, deployment leverage, alignment basin (Christiano), value bundle (shard/CIRL), conserved properties (tiling/MB10).
- Preservation conditions list: `hidden productive-control bounds` → `hidden productive B-IQ bounds`.

## Verification (per file class)

| Surface | Check |
|---|---|
| Chapters | grep demotion list + homograph watchlist; first-use plain paraphrase for A/C |
| App E | headwords match inventory B rows; *nearest field term* deltas still accurate post glossary pass |
| App B | bridge rows use projection language consistent with inter-agenda Cross-agenda tags |
| Appendices C/G/D/F | selection handle / deployment leverage / selection environment drift |
| Site cards | parity with App E plain-first (2026-07 sweep; re-spot-check MB6/CCI cards) |
| `metadata/notation.md` | symbols unchanged; labels match plain terms |

---

## Not in scope (this audit)

- Inter-agenda glossary thin entries (`THIN.md`)
- App E ↔ inter-agenda automated sync
- Lean predicate renames
