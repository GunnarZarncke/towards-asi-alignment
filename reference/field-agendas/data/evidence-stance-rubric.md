# Evidence stance rubric

Agent-facing adjudication guide for `direction` and `weight` on [`evidence.yml`](evidence.yml) entries. **Not** manuscript canon. Public legend: [`meta.yml`](meta.yml) `directionLegend` / `weightRubric`.

## What stance is

**Method type** (C/T/S/P/D/E/O) says *how* the work was done. **Stance** says whether the cited source, *relative to bridge discharge*, mainly:

- **advances** constructive progress on the crux (`support`), or
- **complicates** it — harder than thought, remedy fails, risk demonstrated, impossibility (`challenge`), or
- **direction not yet judged** (`unclear`).

Stance is **editorial**, not statistical. Do not use p-values, effect sizes, or +/- notation.

## Fields (`evidence.yml`)

```yaml
- id: 13
  direction: challenge   # support | challenge | unclear
  weight: 2              # 1 | 2 | 3 — only when direction is support or challenge
```

| Field | Required | Values |
|---|---|---|
| `direction` | On new entries; optional on legacy until backfill | `support`, `challenge`, `unclear` |
| `weight` | When `direction` is `support` or `challenge` | `1`, `2`, `3` (default `1` if omitted) |

**Legacy default:** omitting `direction` means *untagged* — matrix renders **no stance mark**. Set `direction: unclear` explicitly to show lone `·`.

**Optional later:** `directionByBridge: { MB7: challenge, MB10: support }` when one paper splits across bridges.

## Direction — adjudication

Judge **relative to the bridge crux in the tagged column(s)**, not whether the agenda is “good for safety” overall.

### `support`

The source mainly argues or demonstrates that discharge/plausible progress on the crux is **more achievable** than before, or supplies a constructive ingredient the field treats as forward motion.

Examples:

- Formal framework that states sufficient conditions for a bridge (even if not yet proved).
- Deployed tool or protocol the field cites as making a crux more tractable (interpretability pipeline, oversight scheme with positive results).
- Proof of possibility (safely interruptible agents) where the crux was open.
- Simulation or empirical result showing a proposed remedy **works** in the studied regime.

### `challenge`

The source mainly argues or demonstrates that the crux is **harder**, a standard remedy **fails or backfires**, or the **risk is real** (not merely hypothetical).

Examples:

- Impossibility or no-go result (e.g. no stable utility function stably corrigible).
- Demonstrated alignment faking, scheming, sleeper behavior, or eval-awareness gaming.
- “Harder than you think” / negative results on automated alignment or a named remedy.
- Capture, Goodhart, or misspecification results that undermine naive discharge stories.
- Capability evals or red-team findings showing hidden capability or control failure **as evidence the wall is real** (not as progress on discharge).

### `unclear`

Neutral cataloging: taxonomy, survey, infrastructure, governance case study, vocabulary, or methodology where direction on **this bridge’s discharge** is not the paper’s main upshot.

Examples:

- AISI alignment eval **case study** (documents practice; does not alone discharge MB7).
- Risk taxonomy or organizational map without a directional theorem or negative result.
- Open-weights release as enabling infrastructure (direction depends on cited bridge — often leave unclear until a maintainer assigns support/challenge on a specific crux).

When in doubt after reading the one-line `evidence` field and source, prefer `unclear` over guessing.

## Weight — editorial load-bearing

Weight is **how much this entry should move a reader’s confidence** in that direction on the tagged crux — not sample size, citation count, or p-value.

| Weight | Label | When to use |
|---|---|---|
| **1** | Illustrative | Early framing, partial result, small-n demo, or sibling evidence exists elsewhere. |
| **2** | Substantive | Credible field contribution; agenda would cite this in a crux argument. |
| **3** | Landmark | Agenda-defining or widely treated as the strongest known directional evidence on that crux (e.g. alignment faking on MB7/MB10, corrigibility impossibility on MB4). |

Same paper can be weight 3 on one bridge and weight 1 on another if tagged to multiple bridges with uneven relevance.

## Matrix marks (rendering)

Stance marks live on **catalog entries**, not `matrix.yml` cells. Site and generated index prefix the type letter:

| direction | weight | Mark (text) | Icon |
|---|---|---|---|
| support | 1 | `+` | `stance-support-1.svg` |
| support | 2 | `++` | `stance-support-2.svg` |
| support | 3 | `+++` | `stance-support-3.svg` |
| challenge | 1 | `−` | `stance-challenge-1.svg` |
| challenge | 2 | `−−` | `stance-challenge-2.svg` |
| challenge | 3 | `−−−` | `stance-challenge-3.svg` |
| unclear | — | `±` | `stance-unclear.svg` |
| *(untagged)* | — | *(none)* | — |

Icons are generated from `reference/field-agendas/scripts/stance-icons.mjs` into `site/public/icons/stance/` (`npm run sync:stance-icons` in `site/`).

## Worked examples (catalog IDs)

| ID | direction | weight | Rationale |
|---|---|---|---|
| 4 | challenge | 3 | Corrigibility impossibility — crux harder for MB4/MB4a |
| 5 | support | 2 | Safely interruptible agents — constructive formal progress |
| 13 | challenge | 3 | Alignment faking — demonstrates real MB7/MB10 risk |
| 14 | support | 2 | CIRL — constructive outer-alignment framework |
| 131 | unclear | — | CEV field source; cousin vocabulary, not discharge |

## Maintenance

1. Add or edit `direction` / `weight` on [`evidence.yml`](evidence.yml) rows.
2. Run `cd site && npm run sync:field-agendas` after render pipeline lands (step 3+).
3. New catalog entries **must** include `direction` once validation script is wired (step 2).

See also [`../MAINTAINER.md`](../MAINTAINER.md).
