# 2026-08-05 — Kosoy evidence merge

## Trigger

User reported broken Vanessa Kosoy Alignment Forum profile links on two agenda cards and asked whether Kosoy / PreDCA and Kosoy / infra-Bayesianism & LTA are really separate agendas. Follow-up: review Kosoy's papers and LW posts (and community distillations), revisit field-matrix evidence, then end session and commit.

## Done

- Reviewed Kosoy primary sources: 2018 LTA overview, 2023 LTA status (Physicalist Superimitation / PreDCA strand), infra-Bayesianism sequence, infra-Bayesian physicalism (bridge transform), Appel & Kosoy 2025 COLT regret paper, 2022 PreDCA shortform, Soto distilled post.
- **Merged agendas:** removed separate `kosoy-predca` row/card; single **Kosoy / infra-Bayesianism & LTA** card covers foundations + PSI/PreDCA outer strand (matches Kosoy 2023 framing).
- **Evidence upgraded:** fixed ev 118–123 sources (broken profile URLs → posts/papers); added ev 154–157 (IBP, Appel & Kosoy 2025, 2023 integrative map, Soto distillation); moved ev 123 to IB & LTA.
- **Matrix:** Kosoy row now populated on MB1–MB3, MB5, MB7, MB7d, MB9 (was sparse PreDCA row with one dual-tagged cell).
- **URLs:** `Vanessa+Kosoy` → `vanessa-kosoy`; LTA/PSI term-links point at posts not profiles.
- Synced: `npm run sync:field-agendas` (29 agenda cards).
- Files: `reference/field-agendas/data/{evidence,matrix,roster,clustering,meta,term-links,agendas/kosoy-infra-bayesianism-lta.yml}`, deleted `kosoy-predca.yml`, `field-agenda-index.md`, site card + `field-agendas.json`, `MAINTAINER.md`, scripts.

## Decisions

- **One Kosoy lineage, one matrix row** — PreDCA/PSI is an outer-alignment strand within LTA, not a separate agenda (Kosoy 2023 status post; prior maintainer note already said PreDCA is peer outer target on MB2/MB3, not a separate bridge).
- **Did not tag MB4/MB8** — corrigibility/CEV appear in distillations only; no strong primary-source evidence row added.
- **ev 157 (Soto)** kept as **C** (community distillation), not primary Kosoy canon.

## Open / next

- Optional: add Appel/Kosoy IB decision-estimation paper as separate ev row if matrix needs finer grain on MB7d.
- PreDCA remains thin-primary for manuscript; glossary row unchanged.
- Matrix count: 24 rows / 29 agenda records (was 25 / 30 before PreDCA merge).

## Verify

- `npm run sync:field-agendas` — OK (29 cards).
- Pre-commit: stage only this session's field-agenda files + conversation log.
