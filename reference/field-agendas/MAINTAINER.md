# Field agenda index — maintainer notes

Agent-oriented material for editing `reference/field-agendas/data/` and interpreting the coverage matrix. **Not** shown on the public Field hub (`/field/`).

## Matrix cell format (`data/matrix.yml`)

Each cell is a YAML list (empty `[]` when no evidence), not a markdown string:

```yaml
MB4:
  - type: C
    ids: [107]
  - type: P
    ids: [108]
  - type: D
    ids: [54, 55, 56]
```

Multiple IDs under one type are split into chunks of at most **3** per tag (keeps matrix columns narrow on the site). The generated `field-agenda-index.md` matrix table uses: `C<sup>[1](#ev-1),[2](#ev-2)</sup>`.

## Inclusion test

An **agenda** row requires: (1) carrier org/program/person, (2) 3–7 signature terms, (3) stated intent to shape research/deployment/policy, (4) primary artifact (curriculum, constitution, technical agenda, eval suite, policy platform).

**Not agendas (reference only):** funding pools (LTFF, SFF, Open Philanthropy), coworking hubs (LISA, Constellation, Meridian), resource directories (AISafety.com, AI Watch), individual blogs/newsletters unless they define a research lineage.

**Training programs** (BlueDot, MATS, Apart, Kairos, seminar-style curricula) are one agenda **type** among others — vocabulary feeds the inter-agenda glossary; no per-curriculum index rows in the matrix.

## Coverage vs book treatment

The **coverage matrix** catalogs **sourced evidence that an agenda advances a bridge crux**, independent of whether TSA adopts that agenda's constructive bet or ontology.

- **`Book treatment`** on each agenda row states how *Towards Superintelligence Alignment* handles the agenda (substantive, peer, borderline, exclude-by-reference, etc.).
- **Empty matrix cells (`—`)** mean no catalog entry in this pass — not "out of book scope" and not a claim the agenda is silent on the crux.
- **Lean spine** carries bridges **`MB1`–`MB11`** incl. **`MB4a`**; App B crosswalk prose currently lists **`MB1`–`MB10`** only (App B update deferred).

## How to read matrix cells (spine translation)

A filled cell means **field evidence on a crux**, not **automatic discharge to `Safe`**. After the 2026-08-02 Lean review ([`drafts/field-claim-formalization-and-bridge-review-plan.md`](../../drafts/field-claim-formalization-and-bridge-review-plan.md)), partial field claims map in three ways — **no new `MB*` column was added**:

| Mode | Meaning | Examples |
|---|---|---|
| **Direct bridge** | Field work maps to a numbered bridge the spine consumes | **MB4a**, **MB8**, **MB11** columns |
| **Ambient cousin** | Evidence on existing columns; validity stays those bridges + defeaters | Kosoy misspec on **MB1**/**MB9** (`Nonrealizability.lean`; falsifiers in `Defeaters.lean`) |
| **Catalog / side channel** | Field crux neighborhood; not a safety-case discharge path | Kosoy regret on **MB2** (≠ **MB11**/`RiskGap`; `RegretSafety.lean`); LI on **MB5**/**MB7d** (exclude-by-reference) |

**Do not infer from cells alone:** Kosoy **MB1**/**MB9** ⇒ misspec solved; Kosoy **MB2** ⇒ regret ⇒ **`Safe`**; CIRIS **MB4a** ⇒ correction integrity without coverage/no-bypass (`CompositePathBypass.lean`); any **MB9** tag ⇒ off-class safety.

**Kosoy diagnostic:** infra-Bayesianism/LTA advances **MB1–MB9** cousins, not a missing **MB11**. PreDCA is a **peer outer target** on **MB2/MB3**, not a separate bridge. **MB2** (LTA/regret) is a value-learning cousin — **MB11** stays **—** for Kosoy.

**Open spine interfaces** (vocabulary, not matrix columns): `PositiveMeasuredPathCertificate` (CIRIS composite TODO); `SystemRegretSafetyEvidence` (optional harm leaf later); `ConservedPropertySignatureVerifiable_of_chokepoint` (prove or type — `Forgeability.lean`).

## Evidence type letters

| Letter | Type |
|---|---|
| **C** | conceptual |
| **T** | theory (formalization) |
| **S** | simulations |
| **P** | practical (applications) |
| **D** | empirical (software) |
| **E** | empirical (other) |
| **O** | other |

## Maintenance workflow

1. Edit YAML under `data/`.
2. Run `cd site && npm run sync:field-agendas` (regenerates agenda cards, `field-agendas.json`, and this folder's `field-agenda-index.md`).
3. Public intro lives in `site/src/content/field/intro.md` (edit separately from agent meta in `data/meta.yml`).
