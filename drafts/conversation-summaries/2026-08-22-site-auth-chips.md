# Session log — 2026-08-22 site authorship chips

## Shipped

- **Companion site Option C:** section (`h2`) and subsection (`h3`) authorship chips synced from LaTeX `\authbar{…}` keys via `scanAuthHeadingKeys()` in `site/scripts/lib/tex-convert.mjs`.
- Chips hidden by default; toggle in Notes panel (people icon, next to highlight). Preference: `localStorage` key `site-auth-chips-visible`; class `html.auth-chips-on`.
- Chip styling in `site/src/styles/global.css` (solid / dashed / label-only modes mirror PDF semantics).
- Re-synced all book markdown (`npm run sync` in `site/`); site build passes.

## Notes

- Pre-scan + index approach avoids deferred-heading bug when `convertInlineText` nested `convertDocument` shared `ctx.pendingHeading`.
- Empty section shells (e.g. ch01 “The Boundary Error” before first subsection) correctly get no chip; following subsection gets `{GZ+AI}`.

## Open

- Image prompt pages `{AI}`; reader legend (preface now mentions PDF bars + site chips).

## Docs updated

- Preface authorship note, Current Status (Companion Website), README, About page, `metadata/authorship-bars.tex`, `site/README.md`, `docs/BUILD.md`.

## Commits

- `10df5ed0` — Add companion site authorship chips synced from LaTeX authbars.
