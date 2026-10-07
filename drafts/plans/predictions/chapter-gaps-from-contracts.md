# Chapter gaps found by the registry contracts

Status: **all items applied** (2026-10-06/07). Stop condition met once the author has reviewed the chapter edits; then delete this file.

**Stop:** delete this file when every follow-up below is applied or recorded as an accepted limit. Mirror: `metadata/TODO.md` "Chapter gaps from registry contracts".

Lane: Predictions. Source: settling the `openQuestions` of `ai-safety-claims/market-contracts/market-01/contract-v2.yaml` and `market-04/contract-v3.yaml` against the chapters and Lean (session log `2026-10-06-eval-registry-scaffold.md`). Order for each change: chapter first, then the Appendix P box (which cites the chapter), then the registry contract (copied from the box). Claim strength stays at bridge level.

## Applied (2026-10-06)

- **G1** Ch. 7 §Boundary Too Narrow: calibration is needed, and we must decide whether and what share of complete-boundary claims may be wrong; declining is recorded, not a false claim. No numbers, no new symbol (ε is leakage, δ is Ch. 3's failure probability; neither fits).
- **G2** Ch. 7 §Adversarial Boundary Discovery: when an audit has met adversarial pressure (independently built generator frozen after the method, stated minimum share of real hidden or split controllers, checked on planted controls, access as strong as the audit assumes). The false-safe rate is the result, not the qualifying condition. Appendix P: Market 1 moved to the serious budget; "meaningful adversarial component" now names Market 8 only.
- **G3** Ch. 7 §Estimator Feasibility: training the generator–detector game is development, an audit needs a fresh frozen generator; recovery counts on independently constructed systems; "previously unseen" defined; setting-specific testbeds are not the only evidence; failures on self-built systems still count. Market 1 box cites it.
- **G4** Ch. 7 §Boundary Too Narrow (`sec:boundary-too-narrow`): complete-boundary claim defined; a too-narrow boundary is such a claim that fails. Market 1 sidebar cites it.
- **G5** Ch. 25: `Pers_beh` (`eq:behavioral-persistence`, `\symboldef`), added to the profile tuple (`\symbolref`), Surface Compliance sentence; `metadata/notation.md` rows for `P_corr` and `Pers_beh`; Market 4 box cites the equation.
- **G6** Ch. 26 after `eq:correction-bottleneck-capacity`: each case is estimated separately on one system; pooling would hide a weak case.
- **G7** Market 4 sidebar: tests shallow uptake only; deeper updates would be a separate market.

## Follow-ups

### F1. One adversarial-validation procedure (applied 2026-10-07)

Ch. 43 §Testing a Certificate Under Attack (`sec:adversarial-validation-ch43`): freeze first; independent hidden cases; stated attack strength; controls both ways (incl. a planted-vulnerability check); false-safe rate with a bound next to a true-pass or coverage floor; toys never sole evidence, deployment claims need a broadly capable system; stop rule (no retuning, nulls recorded, a pass is a snapshot). Calibrated: a pass is evidence at one attack strength, not proof of adversarial verifiability up to κ. Cited (one sentence each, no restatement) from Ch. 7 (adversarial-pressure condition), Ch. 10 §Adversarial Agency Tests, Ch. 25 §Adversarial Testing, Ch. 31 §Adversarial Conservation, Ch. 33 §Adversarial Certification, Ch. 34 (snapshot), Ch. 39 §Red-Team Incentive Design, Ch. 42 adversarial-measurement bullet, App. D adversarial audit item. Not touched: measurement-only passages (perturbation lists) and App. N's backtest freeze discipline, which is its own methodology.

Appendix P: the Common qualification states a condensed version (Common rules paragraph, plus serious and default budgets); every market's fine print repeats the Common rules and its budget verbatim (Markets 14, 19, 20 exempt: they state their own procedures), so each Metaculus question stands alone. `site/scripts/sync-predictions.mjs` fails the sync if a copy drifts (negative-tested).

### F2. Appendix P common rule (applied 2026-10-07)

Generator route = finds at least 80% of the vulnerabilities planted in a copy of the target (failures known by construction), plus 300 independent expert-hours. Default budget defined: one red-team group independent of the method's authors, at least 40 documented expert-hours in total (a weekend hackathon), access frozen in advance. Market 8 moved to the serious budget; the "meaningful adversarial component" sentence is gone. Ch. 7's adversarial-pressure condition and the Market 1 box use the same planted-weakness check (a deliberately weakened copy of the method). Registry shared rules, route schema, and validator follow.

Full wording in every market: done via F1's condensed Common rules in each market's fine print.

### F3. Symbol graph (applied 2026-10-06/07)

`Auth_k` unified; `Pers` is a calibrated lower bound on the CCI vector passing; `\vec{\theta}_{\mathrm{corr}}` defined at its first use (Ch. 24) and used through Ch. 25–29, 34, 36, 42, 45, 46, App. G. θ cleanup per the 2026-08-05 rule: bare θ now means only the causal-influence (MI) threshold (first marked at ch07 `\symboldef[theta]`); other thresholds carry subscripts (`θ_soc` Ch. 5/App. F, `θ_L` Ch. 7/33/41, `θ_dev`/`θ_drift`/`θ_merge` Ch. 8, `θ_E` Ch. 11, `θ_M` Ch. 12, `θ_stab` Ch. 15, `θ_goal` Ch. 16, `θ_k`/`θ_comp` Ch. 18, `θ_i` Ch. 20, `θ_esc` Ch. 25, `θ_Π` Ch. 34, `θ_det` Ch. 36, `θ_s` Ch. 41, `θ_quant` App. G); model parameters stay as subscripts (`p_θ`, `π_θ`). `scripts/extract_symbol_formula_graph.py` now reads `\vec{\theta}_{sub}` as a subscripted symbol and ignores θ used only as a parameter subscript; the graph's bare-θ node now links only the five causal-influence equations. Notation rows for θ, `θ_corr` (home Ch. 24), `θ_Π`.

### F4. Smaller (applied)

Ch. 39 "the following components". MB1: Market 1 sidebar says the Lean bridge assumes a passing estimate is always sound and the market prices how often real methods are wrong.

### Still open in the appendix (not chapter gaps)

- Market 1 sample floor: applied 2026-10-07, 50 scored systems (unscored systems count toward neither the floor nor the families).
- Market 1 denominators (applied 2026-10-07): false-certificate rate per complete certificate issued; coverage over scored systems.
