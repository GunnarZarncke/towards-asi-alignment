# `ch46` correction table (post-renumber pre-image recovery)

> **Applied 2026-09-23.** Every `fix` row below and the adjacent-damage appendix were applied by hand. Decisions taken on the open rows: `notation.md` `χ`/`χ_ij(a)` → ch37 (definition home); `κ_ij`, `φ`, `φ_c` → ch13 (content: `eq:kappa-coordination`, `eq:cooperation-percolation`; not ch35 as the map suggested); `assumptions-ledger.md:23` → ch25–29; `:80` → ch25, ch27–29 (ch26 is canonical); `uncertainty-ledger.md:11` → ch39; `claims-ledger.md:115` drops 46. Survivors: `uncertainty-ledger.md:15` and `REVIEWING_FOR_AGENTS.md:89` (both correct). Kept as the audit trail.

**Provenance.** Commit `bd8f82f` (2026-06-30, "Renumber chapters and appendices to
sequential print order") replaced chapter ids with a cascading substitution: in
files that were not re-derived afterwards, most old ids between `ch20` and
`ch36` (plus old `ch39`/`ch42`) collapsed to `ch46`, and most old ids between
`ch29` and `ch40` collapsed to `ch48` (with `ch38`/`ch41`→`ch45`,
`ch39b`/`ch43`→`ch47`). `ch46` is now *The End of Unconscious Value Drift*
(`chapters/ch46-unconscious-value-drift.tex`), so nearly every `ch46` in the
files below points at the wrong chapter. Some lines were hand-touched later
(`ede0ac3d`, `35edd4ac`, `e3cc3c81`), which is why a few rows already carry a
correct canonical home next to a stale `ch46`. Corrections are tabulated here
and **not yet applied**: `ch46` also appears legitimately (two rows below), the
same lines carry adjacent `ch45`/`ch47`/`ch48` damage from the same cascade, and
several range rows need a human choice of span. Pre-images were read from
`git diff bd8f82f^ bd8f82f -- <file>`; "correct chapter" was decided by content
(`grep chapters/` for the label, symbol, `ass:A-0xx` key or section) and the map
was used only as a cross-check. Where they disagree the row says so.

## Recovered renumber map (RELEASE_NOTES.md v1.0.0 §Renumbering map)

| Old id | New id | Old id | New id |
|--------|--------|--------|--------|
| ch01–ch19 | unchanged | ch35b | ch38 |
| ch19b | ch20 | ch36–ch39 | ch39–ch42 |
| ch20–ch24 | ch21–ch25 | ch39b | ch43 |
| ch25b | ch27 | ch40–ch44 | ch44–ch48 |
| ch26–ch35 | ch28–ch37 | (old ch42 = value drift) | ch46 |

Current part wiring (from `parts/*.tex`), useful for the range rows:
P4 ch15–20 value bundles · P5 ch21–24 goal inference · P6 ch25–29 correction
channels · P7 ch30–33 successors · P8 ch34–38 attractor basins · P9 ch39–44
safety cases · P10 ch45–48 civilizational limit.

Assumption-key homes (`\label{ass:A-0xx}` in `chapters/`): A-001 ch16 ·
A-002 ch26 · A-003/A-005 ch05 · A-004 ch07 · A-006 ch22 · A-007 ch30 ·
A-008 ch34 · A-009 ch43 · A-010/A-014 ch03 · A-011 ch02 · A-012 ch14 ·
A-013 ch35.

Status legend: **fix** = replace as shown · **correct as-is** = leave ·
**unsure** = needs a human decision (reason given).

## `metadata/notation.md` (14 occurrences)

| Line | Current text (short) | Old id (pre-bd8f82f) | Correct chapter | Evidence (label/section grep) | Status |
|------|----------------------|----------------------|-----------------|-------------------------------|--------|
| 91 | `$L$` log-evidence / predictive score | ch21 | ch22 | `\label{eq:intentional-gain}` and `DL(` in ch22-compression-test-intention | fix |
| 92 | `$DL(\cdot)$` description length | ch21 | ch22 | same as above | fix |
| 93 | `$\Delta L_{\text{int}}$` intentional compression gain | ch21 | ch22 | `eq:intentional-gain` defined in ch22 (ch06 only cites it) | fix |
| 94 | `$\Delta L_{\text{transport}}$` goal-transport gain | ch22 | ch23 | `\Delta L_{\mathrm{transport}}` ch23-goal-transport:58,71,241 | fix |
| 95 | `$\Delta L_T$` transport decomposition (semantic, bundle, bearer, …) | ch23 | ch23 | `\Delta L_T = ΔL_semantic + ΔL_bundle + ΔL_bearer …` at ch23:698, `sec:pipeline-step5`. **Map says ch24; content wins (ch23).** | fix |
| 111 | `$L,M,R,O_{\mathrm{trans}}$` CCI residual coordinates | ch25 | ch26 | `O_{\mathrm{trans}}` and `\lambda_O` only in ch26-correction-channel-integrity | fix |
| 112 | `$\lambda_L,\lambda_M,\lambda_R,\lambda_O$` CCI penalty weights | ch25 | ch26 | `\lambda_O` ch26 only | fix |
| 114 | `$U_S$` system correction-update operator | ch24 | ch25 | ch25-correction-causal-channel:217 "We write $U_S$ for the system correction-update operator" | fix |
| 122 | `$\text{Succ}(A)$` successors of agent $A$ | ch28 | ch30 | `\mathrm{Succ}(A)` introduced ch30-successor-central-test:117 (central test) | fix |
| 141 | `$\chi$` artifact conductivity | ch34 | ch37 (content) / ch36 (map) | `\chi_{ij}(a)` artifact conductivity defined ch37-alignment-attractor:156–198; ch38 has the "conductivity equation" prose; ch36 only mentions conductivity. Sibling row 142 `$\chi_{ij}(a)$` says ch48 (also wrong; ← old ch35 → ch37). Recommend both rows → ch37. | unsure (ch37 vs ch38) |
| 144 | `$C_X$` host correction capacity (correction-audit-evasion criterion) | ch34 | ch36 | `C_X` in ch36-parasites-correction-system (and ch10) | fix |
| 145 | `$A_Y,I_Y,\lambda_Y$` evasion-process entropies | ch34 | ch36 | `A_Y` in ch36 (and ch10) | fix |
| 156 | `$\kappa_{\mathrm{sel}}(E,A,h)$` effective selection capacity | ch32 | ch34 | `\kappa_{\mathrm{sel}}` only in ch34-selection-environment | fix |
| 165 | `$\Delta L$ sign` positive gain = richer model earns its cost | ch21 | ch22 | MDL convention of the compression test, ch22 | fix |

## `metadata/assumptions-ledger.md` (32 occurrences on 24 lines)

| Line | Current text (short) | Old id (pre-bd8f82f) | Correct chapter | Evidence (label/section grep) | Status |
|------|----------------------|----------------------|-----------------|-------------------------------|--------|
| 21 (×2) | "ch46 WWCTV five bundle-inference dependencies … (split in ch46; … canonical homes ch16, ch26, ch22)" | ch20, ch20 | ch21, ch21 | ch21 `sec:wwctv-reward-to-bundle-inference` lists exactly five ("First … Fifth": structure, inferability, bearer maps, geometry preservation, correction channels). "canonical homes" clause was added later and is right. | fix |
| 22 | "ch46 compression test / MDL" | ch21 | ch22 | `\label{ass:A-006}` ch22:80 | fix |
| 23 | "ch46–27 correction channel" | ch24–27 | ch25–29 (two-sided: right end "27" is stale too) | Old ch24,25,25b,26,27 → new ch25,26,27,28,29 = Part VI exactly. A-002 canonical ch26. Tighter reading "ch25–27" (the CCI trio) is defensible. | fix (decide 25–29 vs 25–27) |
| 24 | "ch46–31 successors / certification" | ch28–31 | ch30–33 (two-sided) | Part VII = ch30–33; A-007 ch30:54, A-010 ch03 | fix |
| 25 | "ch46–35 selection / basins" | ch32–35 | ch34–37 (two-sided) | old ch32,33,34,35 → ch34,35,36,37; A-008 ch34:33; ch38 (old 35b) not in original span | fix |
| 26 | "ch46–40 adversarial measurement" | ch36–40 | ch39–44 (two-sided) | old ch36…40 (incl. 39b) → ch39…44 = Part IX; A-009 canonical ch43 (already noted on the line) | fix |
| 31 | "ch46 'do not assume agent/sensors/goal'" | ch21 | ch22 | phrase "do not assume" only in ch22-compression-test-intention | fix |
| 55 | "S07 MDL: positive gain ⇒ preferred model" | ch21 | ch22 | MDL ordering is ch22's compression test; S07 not stated in chapters by name | fix |
| 66 (×2) | A-001 also stated in: "ch46 (WWCTV items 1, 4), ch46, ch45–43" | ch20, ch21 (and ch41–43) | ch21 (WWCTV items 1, 4), ch22, **ch45–47** | ch21 WWCTV items 1 and 4 = bundle structure / geometry preservation; ch22 restates A-006-adjacent inferability. Adjacent "ch45–43" is a broken range (old ch41–43 → ch45–47). | fix |
| 80 (×3) | A-002 also stated in: "ch46–27, ch46, ch46 (WWCTV item 5), ch48" | ch25–27, ch34, ch20 (and ch40) | ch26–29 (two-sided), ch36, ch21 (WWCTV item 5), **ch44** | old ch25,25b,26,27 → ch26–29; ch34 → ch36 (host correction capacity $C_X$); ch21 WWCTV "Fifth … correction channels"; ch48 ← old ch40 → ch44. Since canonical is now ch26, "also stated in" may better read "ch25, ch27–29". | fix (decide span) |
| 96 | A-004 also stated in: "ch06–07, ch09–10, ch46, ch45" | ch36, ch38 | ch39, **ch41** | old ch36 → ch39 (passive observation; 10 "boundar" hits), old ch38 → ch41 (multiscale decomposition; 19 hits). ch45 is adjacent damage. | fix |
| 106 | A-006 assumption text: "ch46 items 2–3 (bundle/bearer inferability)" | ch20 | ch21 | ch21 WWCTV items 2–3 = inferability and bearer maps | fix |
| 114 | A-007 also stated in: "ch08, ch46–31" | ch28–31 | ch30–33 (two-sided) | Part VII | fix |
| 126 (×2) | A-009 also stated in: "ch48, ch46, ch46–39b, ch48" | ch33, ch36, ch39–39b, ch40 | **ch35**, ch39, ch42–43 (two-sided; drop stale "39b"), **ch44** | old ch33 → ch35 (A-013 home), ch36 → ch39, ch39–39b → ch42–43, ch40 → ch44 | fix |
| 132 | A-010 also stated in: "ch48, ch46" | ch31, ch39 | **ch33**, ch42 | old ch31 → ch33 certification; old ch39 → ch42 safety case | fix |
| 156 (×3) | A-014 canonical: "ch16/ch46 value-bundle validity, ch46 correction validity, ch46 safety-case layer, and ch47 adversarial verifiability" | ch20, ch25, ch39 (and ch39b) | ch21, ch26, ch42 (and **ch43**) | ch21 line 792 "abstraction moves or becomes uncertain"; A-002/`uncertainty escalation` in ch26; safety case = ch42; adversarial verifiability A-009 = ch43 (ch47 is adjacent damage) | fix |
| 226 | Appendix index A-006 "compression gain … (MDL / ΔL)" | ch21 | ch22 | `ass:A-006` ch22:80 | fix |
| 233 | Appendix index A-002 "handle-controlled causal chain … CCI" | ch24 | ch26 | `\label{ass:A-002}` ch26:32; ledger's own line 23 says canonical ch26. **Map says ch25; content wins (ch26).** | fix |
| 243 | Appendix index A-007 successor channels | ch28 | ch30 | `ass:A-007` ch30:54 | fix |
| 244 | Appendix index A-008 socio-technical selection | ch32 | ch34 | `ass:A-008` ch34:33 | fix |
| 250 | Appendix index S07 MDL ordering | ch21 | ch22 | as line 55 | fix |
| 255 | Appendix index MB4 CCI ⇒ correction-operator preservation | ch25 | ch26 | `MB4` in ch26 (also cited ch25, ch28, ch42); CCI certificate chapter | fix |
| 257 | Appendix index MB5 transport + bearer ⇒ successor safety | ch28 | ch30 | `MB5` in ch30 (and ch42) | fix |
| 264 | Appendix index MB8 legacy CEV-style bridge | ch26 | ch28 | `MB8` in ch28-extrapolative-correction (and ch43) | fix |

## `metadata/uncertainty-ledger.md` (8 occurrences)

| Line | Current text (short) | Old id (pre-bd8f82f) | Correct chapter | Evidence (label/section grep) | Status |
|------|----------------------|----------------------|-----------------|-------------------------------|--------|
| 11 | U-03 chapters "ch25–27, ch42, ch46, ch47, ch48" | ambiguous: bd8f82f wrote "ch46, ch48, ch46, ch47" from "ch25, ch27, ch36, ch39b"; `ede0ac3d` then hand-added "ch25–27, ch42" but kept ch46 | ch39 (old ch36) — or drop | old ch25 is now covered by "ch25–27", so the surviving ch46 stands for old ch36 → ch39 (passive observation not enough). ch46 itself has only 2 "reference process/independence" hits vs 5 in ch27; nothing in ch46 is about CCI measurement. Adjacent: ch47 ← 39b → ch43; ch48 ← old ch27 → ch29. | unsure (ch39 vs drop) |
| 12 | U-04 chapters "ch08, ch31, ch46, ch48" | ch28 (ch48 ← ch29/ch31) | ch30 (ch48 → **ch33**) | old ch28 → ch30 successor central test; ch31 already listed; old ch31 → ch33 certification | fix |
| 14 | U-06 chapters "ch12, ch14, ch46" | ch30 | ch32 | self-transparency $\tau$ / self-opacity, ch32 (52 "transparen" hits) | fix |
| 15 | U-07 chapters "ch28, ch45, ch46, ch48" | ch42 (old) — hand-fixed in `ede0ac3d` from "ch45–42" to "ch45, ch46" | ch46 | old ch41–42 → ch45–46 = value change at stake / unconscious value drift; exactly U-07's topic. Adjacent ch48 ← old ch27 → ch29. | **correct as-is** |
| 17 | U-09 chapters "ch46, ch48" | ch21 (ch48 ← ch37) | ch22 (ch48 → **ch40**) | compression test ch22; goal laundering ch40 | fix |
| 18 | U-10 chapters "ch46, ch48" | ch32 (ch48 ← ch35) | ch34 (ch48 → **ch37**) | selection environment ch34; alignment attractor ch37 | fix |
| 22 | U-14 chapters "ch42, ch46, ch47, appG" | ch39 (ch47 ← ch39b) | delete ch46 (ch42 already added by `ede0ac3d`); ch47 → **ch43** | old ch39 → ch42 safety case, now duplicated | fix (remove) |
| 24 | U-16 chapters "ch03, ch16, ch42, ch46, ch47" | ch20 and ch25 (bd8f82f had three ch46; `ede0ac3d` collapsed to one, adding ch42 for old ch39) | ch21, ch26 (ch47 → **ch43**) | matches A-014 canonical line: ch21 value-bundle validity, ch26 correction validity, ch42 safety-case layer, ch43 adversarial verifiability | fix |

## `REVIEWING_FOR_AGENTS.md` (10 occurrences)

| Line | Current text (short) | Old id (pre-bd8f82f) | Correct chapter | Evidence (label/section grep) | Status |
|------|----------------------|----------------------|-----------------|-------------------------------|--------|
| 79 | "Value bundles: ch15-ch46" | ch15-ch19b | ch15-ch20 (two-sided range) | Part IV = ch15–20 | fix |
| 80 | "Bundle-geometry measurement and Goodhart pressure: ch46" | ch19b | ch20 | `ch20-measuring-stress-testing-bundle-geometry.tex`; book.yml part04 `sec:from-geometry-to-measurement-ch20` | fix |
| 81 | "Bearer maps: ch18, ch46, ch47" | ch23 (ch47 ← ch43, correct) | ch24 | old ch23 → ch24 transport types (39 "bearer" hits; bearer transport); ch47 = bearers of value is right | fix |
| 82 | "Transport hierarchy: ch46" | ch23 | ch24 | "The hierarchy matters" ch24-transport-types:105; no "hierarchy" in ch23 | fix |
| 83 | "Vector/status CCI: ch46; adversarial pressure tests: ch48" | ch25 (ch48 ← ch25b) | ch26 (ch48 → **ch27**) | CCI vector/status certificate ch26; adversarial pressure ch27 | fix |
| 84 (×2) | "Existing-work crosswalk …: ch07, ch46, ch46-ch48, ch45, ch47" | ch20, ch24-ch27 (ch45 ← ch38, ch47 ← ch39b) | ch21, ch25-ch29 (two-sided), **ch41**, **ch43** | Part V summary: reward/CIRL as special case (ch21); Part VI: shutdown/interruptibility/low-impact/quantilization as special cases (ch25–29); old ch38 → ch41 multiscale decomposition (debate/amplification); old ch39b → ch43 | fix |
| 85 | "Successor test: ch46-ch48" | ch28-ch31 | ch30-ch33 (two-sided) | Part VII | fix |
| 86 | "Selection envelope and correction parasites: ch46-ch48" | ch32-ch35 | ch34-ch37 (two-sided) | ch34 selection env … ch37 attractor; parasites = ch36 | fix |
| 89 | "Value-update envelope: ch45-ch46" | ch41-ch42 | ch45-ch46 | old ch41–42 → ch45–46 per map; value-update envelope is ch45/ch46 content | **correct as-is** |

Site mirror: `site/public/reviewing-for-agents.md` is gitignored and copied from
`REVIEWING_FOR_AGENTS.md` by `site/scripts/sync-bot-orientation.mjs` (which also
builds `llms-full.txt` from `llms.txt`); it regenerates at build and needs no
separate edit.

## `llms.txt` (1 occurrence)

| Line | Current text (short) | Old id (pre-bd8f82f) | Correct chapter | Evidence (label/section grep) | Status |
|------|----------------------|----------------------|-----------------|-------------------------------|--------|
| 68 | "ch46 stress-tests bundle-geometry measurement under Goodhart pressure" | ch19b | ch20 | same claim as REVIEWING line 80; chapter title | fix |

Adjacent on the same file: line 100 "the ch48 stress tests" ← ch25b → ch27.

## `metadata/claims-ledger.md` — errors found (included because found)

The file was believed clean, but the C-012 block (lines 115–124) still carries
cascade damage. It uses bare numbers on the "Chapter(s)" line, which a `ch46`
grep does not catch.

| Line | Current text (short) | Old id (pre-bd8f82f) | Correct chapter | Evidence | Status |
|------|----------------------|----------------------|-----------------|----------|--------|
| 122 | "ch16/ch46 require value-bundle abstractions to move or become uncertain under value-relevant change" | ch20 | ch21 | ch21-reward-to-bundle-inference:792 "when value-relevant reality moves, the abstraction moves or becomes uncertain" (ch16:361 has the sibling statement) | fix |
| 123 | "ch46 treats independent evidence, monitor integrity, dissent, exit, and uncertainty escalation as … anti-capture validity conditions" | ch25 | ch26 | "uncertainty escalation" only in ch26-correction-channel-integrity; A-002 home | fix |
| 115 | "**Chapter(s):** Introduction, 3, 16, 20, 25, 42, 46, 47" | (not touched by bd8f82f; old numbering never updated) | Introduction, 3, 16, 21, 26, 42, 43 | 20→21, 25→26 per rows above; 46 has no support bullet once 122–123 move; 47 → 43 (see 124) | fix (human confirm "46") |
| 124 | "ch47 ties metric honesty to capture of grounding" | ch39b | ch43 | ch47-bearers-of-value has 0 "grounding" hits; ch43 has 4 and hosts `ass:A-009` | fix |

Recommendation: re-check the other claim blocks' "Chapter(s)" lines for bare
old numbers (20, 25, 29–40) the same way.

## Adjacent damage on the same lines (not `ch46`, same cascade, same files)

Not requested, but the fixer will be editing these lines anyway. Pre-images are
from the same `bd8f82f` diff; "→" is the map result unless a content note says
otherwise.

| File | Line | Token | Pre-image → correct |
|------|------|-------|---------------------|
| notation.md | 17 | ch48 ×3 (seven conserved properties) | ch29, ch29, ch31 → ch31, ch31, ch33 |
| notation.md | 109 | `Risk(A)` ch48 | ch31 → ch33 |
| notation.md | 123 | `S_certified` ch48 | ch31 → ch33 |
| notation.md | 138–140 | `κ_ij`, `φ`, `φ_c` ch48 | ch33 → ch35 (ch37:198 says the cooperation graph is inherited from ch13; check) |
| notation.md | 142 | `χ_ij(a)` ch48 | ch35 → ch37 (defined ch37:156) |
| assumptions-ledger.md | 27, 156, 236, 261, 262 | ch47 | ch39b → ch43 (A-009 home) |
| assumptions-ledger.md | 30 | ch48 ×2 (safety-case example assumptions) | ch31 → ch33 |
| assumptions-ledger.md | 82 | "Manuscript ch48 now ties the anti-capture condition …" | ch27 → ch29 |
| assumptions-ledger.md | 102 | "ch48–32, ch48" | ch31–32, ch35 → ch33–34, ch37 |
| assumptions-ledger.md | 112 | "(seven conserved properties, ch48)" | ch29 → ch31 |
| assumptions-ledger.md | 120 | "ch48, ch48, ch48" | ch33, ch35, ch40 → ch35, ch37, ch44 |
| assumptions-ledger.md | 150 | "deferred to ch43/ch48" | ch39b/ch40 → ch43/ch44 (first half already fixed) |
| assumptions-ledger.md | 235, 263 | A-013 / MB7d ch48 | ch33 → ch35 (`ass:A-013` ch35:184; the ledger's own line 150 says ch35) |
| assumptions-ledger.md | 258, 259 | MB6a / MB6b ch48 | ch33, ch35 → ch35, ch37 |
| uncertainty-ledger.md | 13 | U-05 ch45 | ch38 → ch41 |
| uncertainty-ledger.md | 19 | U-11 "ch45 `sec:pivotal-process-ch48`", "ch45, ch48" | ch35b → ch38; label is actually `sec:pivotal-process-ch37` (ch38:44); ch40 → ch44 |
| uncertainty-ledger.md | 20 | U-12 ch47, ch48 | ch39b → ch43; ch40 → ch44 (ch37, ch38 were hand-fixed) |
| uncertainty-ledger.md | 21 | U-13 ch48 | ch31 → ch33 |
| uncertainty-ledger.md | 10, 16 | U-02 ch47; U-08 ch45, ch47 | ch43 → ch47; ch41, ch43 → ch45, ch47 — **correct as-is** |
| REVIEWING_FOR_AGENTS.md | 78 | "Grounding viability: ch03, ch47" | ch39b → ch43 |
| REVIEWING_FOR_AGENTS.md | 87 | "Conductive artifacts and pivotal processes: ch45" | ch35b → ch38 |
| REVIEWING_FOR_AGENTS.md | 88 | "Goal laundering and cost of faking: ch48, ch47" | ch37, ch39b → ch40, ch43 |
| REVIEWING_FOR_AGENTS.md | 103 | "see the ch48 stress tests" | ch25b → ch27 |
| llms.txt | 100 | "in the ch48 stress tests" | ch25b → ch27 |

## Apply procedure

Fixes must be applied **by hand, line by line — no sed/replace-all**: `ch46`
is a legitimate target on `uncertainty-ledger.md:15` and
`REVIEWING_FOR_AGENTS.md:89`, and the correct replacement differs from row to
row (ch21, ch22, ch23, ch24, ch25, ch26, ch28, ch30, ch32, ch34, ch36, ch37,
ch39, ch42, or deletion).

Safest order:

1. `metadata/notation.md` — 14 independent one-token rows; no ranges. Decide
   row 141/142 (`χ` → ch37 recommended) first.
2. `metadata/assumptions-ledger.md` — do the Appendix index (lines 226–264)
   first (they anchor to `ass:` labels and are unambiguous), then Section I
   "Also stated in" lines, then the Verification table (lines 21–31) last
   because its range rows need the span decisions below. Fix the two-sided
   ranges (23, 24, 25, 26, 66, 80, 114, 126) in one edit each so no
   half-corrected range is left behind.
3. `metadata/uncertainty-ledger.md` — leave line 15 alone; delete the `ch46`
   on line 22; the rest are one-token swaps. Decide line 11 first.
4. `REVIEWING_FOR_AGENTS.md` — leave line 89 alone; five of the rows are ranges
   (79, 84, 85, 86) and must be edited as whole ranges. Rebuild the site
   afterwards so `site/public/reviewing-for-agents.md` regenerates.
5. `llms.txt` — one token (line 68); `llms-full.txt` regenerates with the site.
6. `metadata/claims-ledger.md` — the four C-012 rows above, then a pass over
   the other claim blocks' bare-number "Chapter(s)" lines.
7. Run `make check` and grep `ch46` again; the only survivors in these files
   should be `uncertainty-ledger.md:15` and `REVIEWING_FOR_AGENTS.md:89`
   (plus legitimate `ch46` mentions in claims-ledger, if any remain after
   step 6).

Lines needing a human decision:

- `assumptions-ledger.md:23` — span ch25–29 (= pre-image span, Part VI) or
  ch25–27 (CCI trio only).
- `assumptions-ledger.md:80` — A-002 "also stated in" span: ch26–29 (literal)
  or ch25, ch27–29 (since ch26 is now canonical).
- `notation.md:141` — bare `χ` home: ch37 (definition) vs ch38 (usage).
- `uncertainty-ledger.md:11` — replace `ch46` with ch39, or drop it.
- `claims-ledger.md:115` — whether "46" stays once the two support bullets move.

## Summary counts

| | Count |
|---|---|
| `ch46` occurrences in the five in-scope files | **65** (notation 14, assumptions-ledger 32, uncertainty-ledger 8, REVIEWING_FOR_AGENTS 10, llms.txt 1) |
| to fix | **61** |
| correct as-is | **2** (`uncertainty-ledger.md:15` U-07; `REVIEWING_FOR_AGENTS.md:89`) |
| unsure | **2** (`notation.md:141` ch37 vs ch38; `uncertainty-ledger.md:11` ch39 vs drop) |
| additional errors in `metadata/claims-ledger.md` | 4 lines (115, 122, 123, 124) |
| adjacent `ch45`/`ch47`/`ch48` cascade tokens on the same files | ~40 (tabulated above; 3 are correct as-is) |

Pre-image was recoverable for every row. The only ambiguity is
`uncertainty-ledger.md:11`, where a later hand edit (`ede0ac3d`) merged two
cascade tokens so the surviving `ch46` could stand for either old ch25 (now
covered by the added "ch25–27") or old ch36; the row treats it as old ch36.
