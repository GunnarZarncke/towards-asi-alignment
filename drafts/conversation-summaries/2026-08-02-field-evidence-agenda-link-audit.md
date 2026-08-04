# 2026-08-02 — Field evidence and agenda card link audit

## Trigger
User reported hallucinated links on the MIRI / field evidence catalog; asked to check all field evidence URLs, then agenda card links (AE Studio inconsistencies called out explicitly). End-of-session commit requested.

## Done
- Audited all **153** evidence-catalog URLs in `reference/field-agendas/data/evidence.yml`; fixed **8** wrong destinations and synced bib keys.
- Audited all **32** agenda cards vs YAML source + `clustering.yml`; fixed wrong/stale URLs and regenerated cards via `sync-field-agendas.mjs`.

### Evidence catalog fixes (`evidence.yml` + bib)
| Row | Fix |
|-----|-----|
| 1 | Embedded Agency arXiv `1902.09402` → `1902.09469` |
| 13 | Greenblatt alignment faking `2412.14069` → `2412.14093` |
| 73 | Park deception survey `2403.03185` → `2308.14752` |
| 124 | Logical induction `1709.08079` → `1609.03543` |
| 41 | AE Studio research `ae.studio/ai-alignment` → `/alignment` |
| 45 | QACI tag 404 → Leake & Persson 2023 LessWrong post |
| 86, 89, 91, 95, 101 | Companion appendix URLs `appB`/`appC` → lowercase `appb`/`appc` |

Also updated `demski2019embedded`, `greenblatt2024alignmentfaking`, `park2024deception`, `qaci2023` in `references/*.bib`; `meta.yml` + sync script for `appb` casing.

### Agenda card fixes (YAML + clustering)
- **AE Studio:** research URL, podcast `#podcast` anchor, clustering link for AE Studio Research.
- **MIRI:** AI StopWatch `substack.com/@aistopwatch` (redirected to wrong profile) → `https://aistop.watch/`.
- **CHAI:** internship → `humancompatible.ai/people#interns`.
- **CIRIS:** stale covenant PDF → accord PDF; AISafety map canonical URL.
- **Pause cluster:** ControlAI `.com` → `.org`.
- Canonical redirects aligned across agenda YAML + clustering: Goodfire, Cooperative AI, Epoch, PauseAI, CAIS, Simon Institute, Timaeus, Conjecture, DeepMind blog, Kosoy `/w/` tag paths, Global Challenges Project.

Regenerated: `field-agenda-index.md`, `site/src/data/field-agendas.json`, 15 agenda card markdown files.

## Decisions
- Prefer canonical final URLs (post-redirect) in YAML source so card frontmatter, Links section, and map clustering stay consistent.
- HTTP 403 on HEAD checks (MIRI, Metaculus, Encode) treated as bot-blocking, not wrong URLs — left unchanged.
- Did not stage unrelated untracked drafts (`context/David-low-dim-personality-tweets.md`, `drafts/secret-loyalties-hackathon-2026-07-27-entries.md`).

## Open / next
- Optional: grep manuscript/site for stale arXiv IDs (`2412.14069`, `2403.03185`, `1709.08079`, `1902.09402`) outside field hub.
- Optional: add Orthogonal QACI post to `orthogonal.yml` links (currently evidence-only).

## Key paths
- `reference/field-agendas/data/evidence.yml`
- `reference/field-agendas/data/agendas/*.yml`
- `reference/field-agendas/data/clustering.yml`
- `references/manuscript-citations.bib`, `references/external-alignment.bib`
- `site/scripts/sync-field-agendas.mjs`
