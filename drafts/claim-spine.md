# Claim spine (Phase 0 audit)

Canonical map from the Introduction's six thesis claims through the manuscript arc to ch48 discharge.
Maintained manually; update when intro claims, safety-case layers, or ch48 status labels change.

**Last cross-check:** 2026-08-17 (Phase 0–1 of six-claims spine plan).

**Ledger IDs:** C-003 (boundary), C-004 (value-bundle), C-004a (grounding), C-005 (correction), C-006 (successor), C-007 (basin). Synthesis: C-044 → ch48 §Opening Claims Revisited.

**Second-tier spine claims** (load-bearing but not in the Introduction six): C-002 (value-update thesis), C-008 (differential growth), C-009 (transport/laundering), C-010 (adversarial measurement), C-011 (civilizational limit).

---

## Six intro claims — spine table

| Intro claim | Ledger | Part(s) | Anchor chapters | WWCTV home | Safety-case layer | ch48 status | Open gaps |
|-------------|--------|---------|-----------------|------------|-------------------|-------------|-----------|
| **Boundary** | C-003 | I (preview), II, IX | ch01, ch06–10, ch41 | ch07, ch09, ch10 | ch03 Claim 1; ch33 boundary | Strong framing; empirical recovery open | Estimator soundness (MB1); UAD transfer nulls (GL-76/79); task-ontology leakage in \(I_{\mathrm{ctrl}}\) (GL-13) |
| **Value-bundle** | C-004 | IV–V | ch15–20, ch21–24 | ch16, ch19, ch20 | ch03 Claim 3; ch33 bundle | More confident under fixed ontology; transport conditional | Low-dimensionality unmeasured (A-001); bearer/ontology shift; tradeoff curvature estimation |
| *(bearer sub-layer)* | part of C-004 | IV, X | ch18, ch47 | ch18, ch47 | ch03 Claim 4; ch33 bearer | Folded into value-bundle discharge; ch47 philosophical limit | Bearer-map commutation; merger/substrate cases |
| **Grounding** | C-004a | I, IV, VI, IX, X | ch03, ch16, ch24, ch42, ch46–47 | ch03, ch46 | ch03 Claim 0; ch42 layer 2 | Strong necessary condition; deployment-grade certification open | \(d_V\)/\(d_Z\) domain-specific; abstraction-gap exploitation; conservative-abstraction bridges |
| **Correction** | C-005 (+ C-002 thesis) | I (ch04), VI, X | ch25–29, ch45–46 | ch25, ch26, ch29 | ch03 Claim 5; ch33 correction | Strong necessary condition; sufficiency conditional | CCI capture/domestication; adversarial verifiability (MB7); legitimacy bridges |
| **Successor** | C-006 | VII–VIII (ch08 preview) | ch08, ch30–33 | ch30, ch31 | ch03 Claim 6; ch33 successor | Strong necessity; certification method open | MB10 forgeability; passive-only audit null (TS-1); conserved-property set completeness |
| **Basin / selection** | C-007 | VIII | ch34–38 | ch34, ch37, ch38 | ch42 layer 7; ch33 implicit | Plausible; pivotal-process time budget open | Coalition detection; slow vs fast path (ch37); Goodhart under pressure (GL-85 null) |

---

## Operational layers not named as intro claims

| Layer | Ledger | Part(s) | Anchor chapters | Maps to intro | Notes |
|-------|--------|---------|-----------------|---------------|-------|
| Capability envelope | *(no intro claim)* | III | ch11–14 | Supports boundary + correction (C-008) | ch03 Claim 2; ch33 capability; differential growth margin |
| Adversarial measurement | C-010 | IX | ch39, ch41, ch43 | Grounding + correction (+ boundary) | ch33 adversarial claim; ch42 layer 8; master disconfirmer in ch48 |
| Transport / laundering | C-009 | V, IX | ch21–24, ch40 | Value-bundle + correction + successor | Five-layer stack in ch24; not a seventh intro claim |
| Transparency / self-modeling | *(operational)* | VII | ch32 | Successor + correction audit | ch33 transparency claim; ch42 does not duplicate as separate intro claim |
| Operating envelope | *(operational)* | VII | ch33 | Certification scope | ch33 item 2; deployment class \(\mathcal{D}\) |
| Civilizational limit | C-011 | X | ch45–47 | Ceiling on correction claim | Governed value change; who still counts |

---

## Safety-case enumeration crosswalk

| Schema | Count | Location | Role |
|--------|-------|----------|------|
| Intro thesis claims | 6 | `frontmatter/introduction.tex` | Reader contract |
| ch03 safety-case shape | 7 (Claims 0–6) | `chapters/ch03-dynamical-guarantee.tex` | Dynamical guarantee preview (+ capability, bearer split) |
| ch33 minimal certification | 9 | `chapters/ch33-certification-without-construction.tex` | Deployment checklist (+ envelope, transparency, adversarial) |
| ch42 safety-case layers | 8 | `chapters/ch42-safety-case.tex` | Full GSN-style graph |

**ch03 → intro mapping:** Claim 0 → grounding; Claim 1 → boundary; Claim 2 → capability (no intro claim); Claim 3 → value-bundle; Claim 4 → bearer (sub-layer of C-004); Claim 5 → correction; Claim 6 → successor. Basin and adversarial layers arrive in Parts VIII–IX.

---

## Part → intro claim (reading order)

| Part | Chapters | Intro claim(s) developed |
|------|----------|---------------------------|
| I | 1–5 | Boundary preview; grounding preview (ch03); scope for all six |
| II | 6–10 | **Boundary** (formal); C-008 margin preview |
| III | 11–14 | Capability envelope (supports boundary/correction) |
| IV | 15–20 | **Value-bundle** (+ bearers ch18) |
| V | 21–24 | Transport stack (C-009); tests bundle/correction/successor jointly |
| VI | 25–29 | **Correction** |
| VII | 30–33 | **Successor**; certification checklist |
| VIII | 34–38 | **Basin** / selection |
| IX | 39–44 | Adversarial measurement (C-010); safety case assembly |
| X | 45–48 | Civilizational limit (C-011); **C-044 discharge** (ch48) |

---

## ch48 §Opening Claims Revisited — status labels (2026-08-17)

| Intro claim | ch48 status (paraphrase) |
|-------------|--------------------------|
| Boundary | Strong framing; empirical boundary recovery open |
| Value-bundle | Learnable structure under fixed ontology stronger; transport/bearer conditional |
| Grounding | Strong necessary validity condition; deployment-grade measurement open |
| Correction | Strong necessary condition; sufficiency needs adversarial verifiability + legitimacy bridges |
| Successor | Strong necessity; deployment-grade certification open |
| Basin | Plausible; pivotal-process checklist vs time budget open |

---

## Phase 1 fixes applied (2026-08-17)

- ch48 summary: "five opening claims" → "six opening claims" ✓
- ch30: "ten-claim" → "nine-claim" (matches ch33 enumeration) ✓
- `metadata/claims-ledger.md` C-044: grounding discharge noted; stale "five promises" text removed ✓
- `frontmatter/executive-overview.tex`: six preservation problems reordered to match Introduction claim order; boundary added as first item ✓

## Phase 2 navigational spine applied (2026-08-17)

- `\label{claim:boundary}` … `\label{claim:basin}` on each `introclaim` in `frontmatter/introduction.tex` ✓
- New subsection `sec:how-claims-unfold` + `tables/claim-spine.tex` in Introduction ✓
- Part openers (`parts/part01`–`part10`) tag which intro claim(s) each part develops ✓
