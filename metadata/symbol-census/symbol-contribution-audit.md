# Symbol / Formula Contribution Audit

**Date:** 2026-07-15 (relocated from `drafts/` into the permanent [symbol census](README.md) on 2026-07-17)
**Scope:** All chapters (`ch01`–`ch48`), canonical index (`metadata/notation.md`), appendices A–N (symbol-bearing only)  
**Question:** Does each symbol pay rent toward the central thesis?

> **Applied 2026-07-17** (see [`drafts/conversation-summaries/RECOVERY.md` (session `2026-07-17-symbol-audit-reduce-remove-pass.md`)](../../`drafts/conversation-summaries/RECOVERY.md` (session `2026-07-17-symbol-audit-reduce-remove-pass.md`))): ch13 seven sub-loss displays reduced to inline math; ch14 duplicate BIQ competence functional collapsed into a cross-reference to ch11's `eq:biq`; ch35 acausal-trade/$P_{\mathrm{meta}}$ stack trimmed ~40%; ch15 LHCV hub-level equations reduced to prose + cross-reference to ch21; ch19 $\chi_i$ removed in favor of the chapter's own Jacobian $J_i$. All other rows below still reflect the original 2026-07-15 audit and are open.

> Superintelligence alignment = **value-bundle transport** + **bearer persistence** + **correction-channel integrity** + **successor stability** + **socio-technical attractor control**

**Action categories** (exactly one per symbol):

| Action | Meaning |
|--------|---------|
| **remove** | Can be removed without loss to the main line |
| **optional-md** | Keep out of manuscript; mention in external markdown (related/future/optional) |
| **footnote** | Relegate to footnote or one-line pointer |
| **appendix-future** | Move to a (new) appendix of future work |
| **lean-demo-exp** | Move to Lean spine, chapter demo, or experiment line |
| **reduce** | Reduce/simplify in chapter (cross-ref, alias, or trim derivation) |
| **keep** | Must be kept as is — load-bearing for thesis |
| **expand** | Should be expanded — underdeveloped relative to thesis weight |

**Method:** Four parallel chapter-range audits (ch01–12, ch13–24, ch25–36, ch37–48) cross-checked against `metadata/notation.md`, `INSTRUCTIONS.md` §0, and `REVIEWING_FOR_AGENTS.md` gem map. Line numbers refer to current workspace `.tex` files.

**Coverage note:** The first pass under-indexed chapter-local symbol vocabularies (especially **ch14**, which defines $M_A$, seven $C_*$ capacities, $\mathcal{B}_{\mathrm{corr}}$, and admissible-growth criteria). Part III now includes a **complete ch14 inventory** (52 rows). Other chapters may still have similar gaps — request a per-chapter supplement if needed.

---

## Executive summary

### High-rent spine (keep; do not cull)

These symbols form the book's operational backbone. Any removal would break cross-chapter dependency:

- **Boundary partition:** $I_t, E_t, S_t, A_t$, $\epsilon$-blanket, $\mathcal{R}(C)$, $C^\star$
- **Grounding:** $X_{\mathrm{real}}, \alpha, Z, \Gamma, d_V, d_Z, \mathsf{Unc}_\alpha$, $\operatorname{Dom}(\Gamma)$, $\mathcal{C}, \delta$
- **Value process:** $V_t, U_H, \Phi, B, W, G_B, g_B, H_B$
- **Capability:** $K, I_{\mathrm{pred}}, I_{\mathrm{ctrl}}, S_X, \mathrm{Control}(A)$
- **Transport stack:** $\Delta L_{\mathrm{int}}, \Delta L_{\mathrm{transport}}, \Delta L_T, \Delta L_{\mathrm{robust}}$, layer maps $M_B, M_\Phi$
- **Correction:** $W_t \to O_t \to J_t \to D_t \to C_t \to U_{t+1} \to A_{t+k}$, $C_{\mathrm{raw}}$, $\vec{\mathrm{CCI}}$, $L,M,R,O_{\mathrm{trans}}$
- **Successor / selection:** $\mathrm{Succ}(A)$, $\Xi$, $\mathcal{L}_{\mathrm{transport}}$, $\vec{\Pi}(A)$, $\mu_E, \mathrm{Fit}_E$, $\kappa_{\mathrm{sel}}$

### Best culls and demotions (≈30 symbols)

| Cluster | Action | Why |
|---------|--------|-----|
| Duplicate $\Delta L$ full derivations (ch01 vs ch06) | **reduce** | One home + cross-ref |
| IRL sample bound $m \gtrsim 2k/\epsilon^2\cdots$ (ch04, ch15, ch17, ch21) | **appendix-future** | Keep once in ch17 |
| Civilizational replicator $\dot w_i = w_i(r_i - \bar r)$ (ch02) | **appendix-future** | Illustrative only |
| Information-bottleneck objective (ch07) | **appendix-future** | Not carried into $K$ |
| ch13 scaling exponents $b(N), p(N), c(N), \rho(N)$ | **appendix-future** | Weak empirical anchor |
| ch13 $T_{ij}, D_{ij}$ translation distortion | **optional-md** | $\Omega_{\mathrm{translation}}$ prose suffices |
| ch19 $\chi_i$ policy-response pattern | **remove** | Duplicates Jacobian |
| ch06 $\mathcal{A}(C)$ agency score | **footnote** | Not operationalized later |
| ch09 $\mathcal{A}_{\text{prelim}}$ six-item checklist | **reduce** | Duplicates ch08/ch12 |
| ch35 acausal-trade / $P_{\mathrm{meta}}$ stack (L203–327) | **reduce** or **optional-md** | High symbol density, conjectural MB7d |
| ch31 $\mathcal{K}(A,A')$ composite score | **remove** or **lean-demo-exp** | Seven properties certified separately in ch33 |
| ch29 $\mathcal{A}_H = B_H(1-\tau_H)d_H\Omega_H E_H$ | **footnote** | Pedagogical; five free parameters |
| ch26 scalar $Q(U)$ update quality | **footnote** | Vector $\vec Q$ preferred |
| ch02 $H(\cdot)$ Shannon (notation home) | **remove** from ch02 index | True use is ch11 $H(I^X_t)$ |
| ch02 power asymmetry $P_t(a)\propto\log|\mathcal{F}_t(a)|$ | **optional-md** | No downstream reuse |
| ch06 full $M_G$ generative model | **lean-demo-exp** | ch01/ch09 use $\Delta L$ without it |
| ch20 toy 3×3 weight matrix | **lean-demo-exp** | Demo-grade |
| ch40 $\mathrm{CC}(k)=I(C_t;A_{t+k}\mid S_t)$ | **footnote** | Superseded by vector CCI |

### Notation-index drift (fix before next build)

`metadata/notation.md` still lists **home ch46/ch48** for symbols whose manuscript homes moved to ch25–ch40. Appendix A misroutes readers. Priority fixes:

| Symbol | notation.md home | Actual home | Action |
|--------|------------------|-------------|--------|
| Correction chain, $C_{\mathrm{raw}}$, CCI, $\Delta L_*$, $\chi$, $\mu_E$, $\vec{\Pi}$, $\kappa_{\mathrm{sel}}$ | ch46 | ch25–ch34 | Update notation.md |
| $\mathrm{RiskGap}, \mathrm{Risk}$ | ch48 | ch33 | Update notation.md |
| $\mathrm{GLI}$ | ch48 | ch40 | Update notation.md |
| $\chi_{ij}(a)$ | ch48 | ch37 | Update notation.md |
| $\eta_g$ | ch13 | **absent** | Add to ch13 or remove from index |
| $G_{\mathrm{coord}}, \Omega_{\mathrm{coord}}$ | ch13 | ch13 (eq labels) | Verify propagation |

### Symbol collisions (blocking)

| Symbol | Collision | Action |
|--------|-----------|--------|
| $K$ | Knowledge/capital (ch02) vs capability (ch11) | **keep** both; disambiguate in notation |
| $B$ | Value bundle (ch16) vs local competence $B_i$ (ch13 L80) | **reduce** — fix ch13 to $K_i$ |
| $B$ | Value bundle vs competence $B(A_t)$ (ch33) | **reduce** — ch33 should use $K$ |
| $D_t$ | Delegation (ch02) vs deliberation (ch04) | **keep**; rename one |
| $C_t$ | Boundary structure vs correction signal vs ch05 society | **reduce** — schematic only where overloaded |
| $G_t$ | Correcting agent (ch25) vs global workspace (ch31/32) | **reduce** — rename workspace |
| $W_t$ | World state (correction chain) vs tradeoff weights (ch16/25) | **reduce** — rename world state |
| $\chi$ vs $\chi_X$ | Artifact conductivity vs expansion–correction ratio (ch12) | **keep** both; rename one |
| $\chi$ vs $\chi_{ij}(a)$ | Scalar vs edge conductivity | **keep**; separate index entries |
| $O$ vs $O_{\mathrm{trans}}$ | Ontology loss (ch25) vs CCI coordinate | **reduce** — rename ch25 |
| $\varphi$ vs $\phi$ | Order parameter notation split ch13/ch37 | **reduce** — unify glyph |
| $\kappa$ | Cooperativity $\kappa_{ij}$ vs adversarial ceiling (ch43) | **reduce** — $\kappa_{\mathrm{adv}}$ |
| $F$ | Feature matrix (ch17) vs bundle functional $F(B,W,\Phi,C)$ (ch23) | **reduce** — rename functional |
| $J$ vs $g_B$ | Jacobian in ch19 vs canonical gradient | **reduce** — alias per C2 |
| $L_t$ | Legibility (ch37) vs control locus (ch41) | **reduce** — rename one |

---

## Part A — Canonical notation index (`metadata/notation.md`)

### Boundary and state

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $I_t$ | **keep** | Canonical internal state; every thesis layer is boundary-relative | `chapters/ch06-agent-without-anthropomorphism.tex` | 145–153, 160–162, 658–661 |
| $E_t$ | **keep** | External state partition | same | 145–153, 152, 210 |
| $S_t$ | **keep** | Sensory interface | same | 145–153, 204–212 |
| $A_t$ | **keep** | Active interface / actuator | same | 145–153, 210–212 |
| $\epsilon$ | **keep** | Allowed boundary leakage; operational boundary test | `chapters/ch07-finding-boundary.tex` | 187–189, 229–234 |
| $I(X;Y\mid Z)$ / `\MI` | **keep** | Universal dependency primitive for boundaries, opacity, correction | ch01, ch06, ch07 | ch07: 187–189; ch06: 160–162 |
| $H(\cdot)$ | **reduce** | Shannon entropy; notation home ch02 incorrect — used in $K$ penalty | `chapters/ch11-capability-without-task-ontology.tex` | 196–201 |

### Capability and growth

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $K$ | **keep** | Central capability functional; cap/corr race is thesis core | `chapters/ch11-capability-without-task-ontology.tex` | 216–248, 637–657 |
| $I_{\text{pred}}$ | **keep** | Predictive information component of $K$ | same | 120–125, 219 |
| $I_{\text{ctrl}}$ | **keep** | Control information; bounds $\mathrm{Control}(A)$ | same | 146–158, 221, 664–668 |
| $\beta, \gamma$ | **keep** | $K$ coefficients | same | 229–232 |
| $S$ (structure term) | **footnote** | Complexity penalty in $K$; standard | same | 229–232 |
| $\eta_g$ | **expand** or **remove** from index | Listed in notation.md home ch13 but **absent** from manuscript; growth-efficiency counterpart to $\eta_c$ | `metadata/notation.md` | 47 |
| $\eta_c(N)$ | **footnote** | Coordination-efficiency scaling; qualitative mid-scale brittleness only | `chapters/ch13-coordination-bottleneck.tex` | 456–474 |
| $G_{\text{coord}}$ | **keep** | Collective coordination gain in $K_{\mathrm{coll}}$ | same | 115–127 |
| $\Omega_{\text{coord}}$ | **keep** | Seven-term coordination loss; distinctive ch13 contribution | same | 153–171 |
| $S_X$ | **keep** | Residual surprise across boundary | `chapters/ch11-capability-without-task-ontology.tex` | 205–209 |

### Value bundles and geometry

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $B$ | **keep** | Primary alignment object (low-dimensional control direction) | `chapters/ch16-value-bundle-model.tex` | 100–137, 489–498 |
| $k$ | **keep** | Bundle dimension count; tractability bridge | `chapters/ch15-values-compressed-control.tex`, ch17 | ch15: 571–577; ch17: 262–276 |
| $\hat B, \hat W, \hat \Phi$ | **keep** | MAP inference estimate | `chapters/ch16-value-bundle-model.tex` | 685–690 |
| $W$ | **keep** | Bundle context-activation weights | same | 572–585 |
| $G_B$ | **keep** | Bundle response geometry tuple | `chapters/ch19-tradeoffs-bundle-geometry.tex` | 214–250, 521–525 |
| $g_B$ | **keep** | Bundle gradient $\partial\pi/\partial B_i$ | ch16, ch19 | ch16: 489–498; ch19: 222–232 |
| $H_B$ | **keep** | Interaction curvature (Hessian of $\log\pi$) | ch16, ch19 | ch16: 266–272; ch19: 236–240 |

### Grounding and abstraction validity

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $X_{\mathrm{real}}$ | **keep** | Value-relevant reality being abstracted | `chapters/ch03-dynamical-guarantee.tex` | 175–176 |
| $\alpha$ | **keep** | Abstraction map; distinct from $K$ weight $\alpha$ — disambiguate in prose | ch03, ch16 | ch03: 177–180; ch16: 321–328 |
| $Z$ | **keep** | Checked abstraction | ch03, ch16 | ch03: 178–180; ch16: 321 |
| $\Gamma$ | **expand** | Grounding relation; in notation but thin in ch13–24 bundle arc | `chapters/ch03-dynamical-guarantee.tex` | 181–193, 246–251 |
| $d_V, d_Z$ | **footnote** | Distance metrics; one line + ch03 cross-ref | ch03, ch16 | ch16: 324–326 |
| $\mathsf{Unc}_\alpha$ | **keep** | Abstraction-break uncertainty; anti-Goodhart | ch03, ch16 | ch16: 328 |
| $\operatorname{Dom}(\Gamma)$ | **keep** | Domain of grounded correction | `chapters/ch03-dynamical-guarantee.tex` | 246–251 |

### Bearer maps

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $\Phi$ | **keep** | Bearer map — bearer-persistence thesis leg | `chapters/ch18-bearer-maps.tex` | 94–96, 248–250 |
| $F$ (feature matrix) | **lean-demo-exp** | Not used in main ch13–24 arc despite notation home ch17 | `metadata/notation.md` | 82 |

### Intention and goal transport

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $L$ | **keep** | Log-evidence / predictive score | `chapters/ch22-compression-test-intention.tex` | 154–161 |
| $DL(\cdot)$ | **keep** | Description-length complexity cost | same | 154–161 |
| $\Delta L_{\text{int}}$ | **keep** | Intentional compression gain; intention test home | same | 59–76 |
| $\Delta L_{\text{transport}}$ | **keep** | Goal-transport compression gain | `chapters/ch23-goal-transport.tex` | 50–66 |
| $\Delta L_T$ | **keep** | Five-term transport decomposition | same | 642–653 |

### Correction and integrity

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $G_t$ (correcting agent) | **keep** | Correcting agent at time $t$ | `chapters/ch25-correction-causal-channel.tex` | 163–177, 233–247 |
| $\mathcal{H}_t$ | **keep** | Handle set controlled by $G_t$ | same | 163–177 |
| $W_t \to O_t \to J_t \to D_t \to C_t \to U_{t+1} \to A_{t+k}$ | **keep** | Correction trace spine; canonical home ch25 (not ch46) | same | 144–158 |
| $C_{\text{raw}}$ | **keep** | Weakest required correction case; reconcile ch25 vs ch26 definitions | ch25, ch26 | ch25: 304–308; ch26: 128–137 |
| $CCI$ | **keep** | Vector/status correction-channel integrity certificate | `chapters/ch26-correction-channel-integrity.tex` | 182–218, 646–648 |
| $CCI_\lambda$ | **keep** | Scalar projection for exposition only | same | 192–218 |
| $\mathrm{Control}(A)$ | **keep** | Effective actuator control capacity | `chapters/ch11-capability-without-task-ontology.tex` | 664–668 |
| $\mathrm{RiskGap}(A)$ | **keep** | $\mathrm{Control}(A)-\mathrm{CCI}(A)$; home ch33 not ch48 | `chapters/ch33-certification-without-construction.tex` | 279–285 |
| $\mathrm{Risk}(A)$ | **keep** | Certification risk functional | same | 279–285 |
| $\mathrm{SelfControlGap}(A)$ | **lean-demo-exp** | Preview in ch22; Lean-linked; home ch32 | ch32, ch22 | ch32: 146–150 |
| $L, M, R, O_{\mathrm{trans}}$ | **keep** | CCI residual coordinates | `chapters/ch26-correction-channel-integrity.tex` | 206–213, 260–314 |
| $\lambda_L, \lambda_M, \lambda_R, \lambda_O$ | **footnote** | CCI penalty weights | same | 206–213 |
| $U_H$ | **keep** | Human value-update operator (schematic) | `chapters/ch04-fixed-values-wrong-target.tex` | 176–179 |
| $U_S$ | **keep** | System correction-update operator | ch25, ch41 | ch25: 199–209 |
| $V_t$ | **keep** | Value-state tuple | `chapters/ch04-fixed-values-wrong-target.tex` | 177–182, 327–331 |
| $C_H$ | **keep** | Human correction capacity (component of $V_t$) | same | 327–331 |

### Successors and certification

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $\text{Succ}(A)$ | **keep** | Successors of agent $A$ | `chapters/ch30-successor-central-test.tex` | 47–74, 99–108 |
| $\mathcal S_{\text{certified}}$ | **keep** | Certified successor class; unify with $\mathcal{C}_{\text{certified}}$ | ch33, ch39 | ch33: 42–46; ch39: 778–780 |
| $\mathcal C$ | **keep** | Certified class in dynamical guarantee | `chapters/ch03-dynamical-guarantee.tex` | 100–104, 746–763 |
| $\delta$ | **keep** | Catastrophic-drift probability bound | ch03, ch24, ch33 | ch03: 100–104; ch24: 755–763 |
| $\tau$ | **keep** | Self-transparency $1-I(M;\hat M)/H(M)$; home ch32 | `chapters/ch32-self-modeling-self-opacity.tex` | 224–231 |

### Multi-agent, selection, evasion, laundering

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $\kappa_{ij}$ | **keep** | Cooperativity index | `chapters/ch13-coordination-bottleneck.tex`, ch35 | ch13: 377–383; ch35: 121–124 |
| $\varphi$ | **keep** | Cooperation order parameter; unify $\phi$/$\varphi$ | ch13, ch37 | ch13: 412–420; ch37: 181–191 |
| $\varphi_c$ | **footnote** | Percolation threshold; qualitative use | ch13, ch37 | ch13: 412–420; ch37: 189–191 |
| $\chi$ (scalar) | **keep** | Artifact conductivity $I(R;D_H\mid A)-I(R;D_H)$ | `chapters/ch36-parasites-correction-system.tex` | 392–396 |
| $\chi_{ij}(a)$ | **keep** | Edge artifact conductivity; home ch37 not ch48 | `chapters/ch37-alignment-attractor.tex` | 145–164, 389–395 |
| $\mathrm{ICI}_{ij}$ | **reduce** | Inferential coupling; conjectural MB7d — trim ch35 formalism | `chapters/ch35-multi-agent-strategic-coupling.tex` | 165–172, 307–319 |
| $C_X$ | **keep** | Host correction capacity (evasion criterion) | `chapters/ch36-parasites-correction-system.tex` | 123–138, 534 |
| $A_Y, I_Y, \lambda_Y$ | **reduce** | Notation.md entries; ch36 uses $K_Y, L_Y$ instead — reconcile | ch36 vs notation.md | ch36: 125–138 |
| $\mathrm{GLI}$ | **keep** | Goal-laundering index; home ch40 not ch48 | `chapters/ch40-goal-laundering.tex` | 309–322 |
| $\mu_E(A)$ | **keep** | Deployment leverage | `chapters/ch34-selection-environment.tex` | 60–67 |
| $\mathrm{Fit}_E(A)$ | **keep** | Deployment growth rate | same | 73–78 |
| $\vec{\Pi}(A)$ | **keep** | Preservation conditions vector | same | 95–111 |
| $\kappa_{\mathrm{sel}}(E,A,h)$ | **keep** | Effective selection capacity through handle | same | 61–68 |

### Conventions

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $K$ vs $B$ | **keep** | Never swap capability vs bundle | ch11, ch16 | ch11: 217–226 |
| $k$ (bundle dim) | **keep** | Not $m$ — ch26 still uses $m$ in places | ch18, ch26 | ch18: notation; ch26: 357–359 |
| $\Delta L$ sign | **keep** | Positive gain = earns complexity | ch22, ch46 | ch22: 59–76 |
| Bundle catalogue | **keep** | New dimensions added in ch16 only | `chapters/ch16-value-bundle-model.tex` | catalogue sections |

---

## Part B — Chapter-local symbols (beyond notation index)

High-signal entries only; full inventories in subagent logs.

### Part I — Reframing & boundaries (ch01–05)

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $C$ (candidate system) | **keep** | Alignment object before machinery | `ch01-wrong-object.tex` | 141–143, 284–286 |
| $X_{1:T}$ | **keep** | Trace for boundary inference | same | 142, 430 |
| $X_t=(H_t,M_t,I_t,K_t,R_t,E_t)$ | **keep** | Civilizational state vector | `ch02-artificial-civilization.tex` | 91–102 |
| $\partial\Pi/\partial M_t$ | **keep** | Artificial-civilization threshold | same | 119–122 |
| $D_t$ (delegation) | **keep** | Delegation–correction inequality | same | 134–137, 389–392 |
| $\mathcal{A}, \mathcal{N}(\mathcal{A})$ | **keep** | Attractor basins | same | 218–224 |
| $\dot w_i = w_i(r_i-\bar r)$ | **appendix-future** | Selection gradient illustration | same | 236–241 |
| $\mathcal{S}, \mathcal{D}, \mathcal{B}$ | **keep** | Safe/bad/basin geometry | `ch03-dynamical-guarantee.tex` | 118–126 |
| $Z_t=(C_t,\Gamma_t,B_t,\Phi_t,U_H,Q_t,S_t)$ | **keep** | Spine tuple naming all five thesis layers | same | 724–739 |
| $\epsilon_t, s_h(t), c_h(t)$ (LHCV) | **reduce** | Neuroscience prior; thesis needs $k$ + control-role only | `ch15-values-compressed-control.tex` | 265–297 |
| $C_{\text{corr}}^{\text{society}}(t_0)>\theta$ | **keep** | Scope assumption | `ch05-assumptions-scope-failure-coverage.tex` | 109–114 |

### Part II — Agents & capability growth (ch06–12)

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $\Delta L_G, \ell(C), C^*$ | **keep** | Scale-selection and intentional compression | `ch06-agent-without-anthropomorphism.tex` | 332–340, 696–703 |
| $\mathcal{A}(C)$ agency score | **footnote** | Not operationalized later | same | 364–387 |
| $M_0, M_G, p(a\mid z)\propto e^{\beta R}$ | **lean-demo-exp** | Generative goal model | same | 318–340 |
| $J(C)=\mathcal{R}-\alpha\mathcal{P}+\lambda\Omega$ | **keep** | Boundary discovery with predictiveness | `ch07-finding-boundary.tex` | 261–274 |
| IB objective $\min_p \MI(X;Z)-\beta\MI(Z;Y)$ | **appendix-future** | Related but not carried into $K$ | same | 253–258 |
| $\Xi(A_t)=(\ell_t,M_t,G_t,\Phi_t,R_t,Q_t,L_t)$ | **keep** | Seven conserved properties | `ch08-grow-split-merge.tex` | 148–171 |
| $\mathcal{L}_{\text{transport}}, d_\Xi$ | **keep** | Transport loss between identity vectors | same | 183–198 |
| $\Sigma(C)=\Delta L_C-\sum_i\Delta L_{C_i}-\lambda_\Sigma DL(\mathcal{D})$ | **keep** | Composite surplus | `ch09-composite-agent.tex` | 195–210 |
| $\Omega_Q=\MI(Z;Q)-\MI(Z;O)$ | **keep** | Selective opacity score | `ch10-strategic-opacity.tex` | 203–215 |
| $D_G$ (goal divergence) | **keep** | Goal-laundering signature | same | 364–383 |
| $R_{\mathrm{cap/corr}}=K^{(h)}/C_{\mathrm{raw}}^{(h)}$ | **keep** | Capability–correction danger ratio | `ch11-capability-without-task-ontology.tex` | 637–657 |
| $\chi_X=(\Delta C_{\mathrm{ctrl}}+\Delta C_{\mathrm{pred}})/(\Delta C_{\mathrm{raw}}+\epsilon)$ | **keep** | Expansion–correction ratio (rename vs $\chi$ conductivity) | `ch12-boundary-expansion.tex` | 843–858 |
| $\chi_X^{\mathrm{irr}}$ | **expand** | Irreversible-weighted variant; weights informal | same | 861–872 |

### Part III — Coordination & bundles (ch13–20)

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $B_i$ in `eq:local-competence` | **reduce** | **Bug:** should be $K_i$ (C5 violation) | `ch13-coordination-bottleneck.tex` | 79–90 |
| $\partial K_{\mathrm{coll}}/\partial K_i \leq 0$ | **keep** | Formal coordination bottleneck | same | 133–137 |
| $\Omega_{\mathrm{latency…irreversibility}}$ (7 sub-losses) | **reduce** | Keep sum; demote individual displays | same | 185–352 |
| $\Delta L_{\mathrm{robust}}$ | **keep** | Risk-weighted transport inference | `ch24-transport-types.tex` | 542–558 |
| $M_B, M_\Phi$ | **keep** | Bundle and bearer transport maps | same | 247–258, 396–398 |
| $F(B,W,\Phi,C)$ (ch23) | **reduce** | Rename — collides with feature matrix $F$ | `ch23-goal-transport.tex` | 104–108 |
| $F_\psi$ (ch22) | **footnote** | Placeholder scoring function | `ch22-compression-test-intention.tex` | 336–341 |
| $\chi_i$ (ch19) | **remove** | Duplicates Jacobian | `ch19-tradeoffs-bundle-geometry.tex` | 114–122 |
| $\psi(x)=\log(1+e^{\alpha x})$ barriers | **footnote** | Protected/taboo regions | same | 506–508 |
| $\hat J_i, \hat H_{ij}$ estimators | **keep** | Operational $G_B$ measurement | `ch20-measuring-stress-testing-bundle-geometry.tex` | 115–128 |
| ch20 toy $\sigma(B_T-\alpha B_C+\eta B_A)$ | **lean-demo-exp** | Illustrative neuron demo | same | 251–273 |

#### Chapter 14 — complete inventory (`ch14-intelligence-deepens-misalignment.tex`)

*First audit pass under-covered this chapter (3 rows only). Full inventory below.*

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $I_t, S_t, A_t, E_t$ | **reduce** | Boundary partition restated; cite ch06/ch11 | `ch14-intelligence-deepens-misalignment.tex` | 84–85 |
| $K$ (`eq:competence-functional`) | **reduce** | Duplicate of ch11 BIQ display; keep one cross-ref + this chapter's *split* uses $C_*$ instead | same | 87–98 |
| $I_{\mathrm{pred}}, I_{\mathrm{ctrl}}, H(I_t), S_X$ | **reduce** | Same components as ch11; prose pointer suffices | same | 101–106 |
| $\alpha, \beta, \gamma$ | **footnote** | $K$ weights already canonical in ch11 | same | 112 |
| $\mathcal{S}$ (prose) vs $S_X$ (eq.) | **reduce** | Line 111 says "$\mathcal{S}$ penalizes surprise" but equation uses $S_X$ — typo/collision | same | 111 |
| $C_{\mathrm{world}}$ | **keep** | World-model/influence capacity; half of chapter's capability split | same | 129, 141–150 |
| $C_{\mathrm{self}}$ | **keep** | Self-model/modification capacity | same | 130, 141–150 |
| $C_{\mathrm{social}}$ | **keep** | Human/institution modeling capacity | same | 131, 141–150 |
| $C_{\mathrm{succ}}$ | **keep** | Successor/delegation capacity | same | 132, 141–150 |
| $C_{\mathrm{raw}}$ | **keep** | Human/institutional correction capacity (schematic here; formal home ch25–26) | same | 133, 155, 179 |
| $C_{\mathrm{trans}}$ | **keep** | Inspection/transparency capacity | same | 134, 157, 181 |
| $C_{\mathrm{value}}$ | **keep** | Value-bundle geometry preservation capacity | same | 135, 159, 183 |
| `eq:misalignment-growth-condition` | **keep** | **Chapter thesis equation** — capability side outruns correction side | same | 141–161 |
| $M_A(t)$ | **keep** | Alignment margin functional; named in epistemic status as chapter contribution | same | 177–186 |
| $C_{\mathrm{power}}$ | **keep** | Weighted sum of unilateral capacities | same | 189–199 |
| $w_1, w_2, w_3, w_4, w_5$ | **keep** | Context-dependent power weights | same | 192–198, 206–208 |
| $R_{\mathrm{irreversible}}$ | **keep** | Irreversible-change rate in $C_{\mathrm{power}}$ | same | 200, 204 |
| `eq:accelerating-margin-collapse` ($dM_A/dt$, $d^2M_A/dt^2$) | **keep** | Sharper warning than $M_A<0$; chapter contribution | same | 213–217 |
| $V$ (latent value), $P$ (proxy) | **footnote** | Standard Goodhart setup | same | 235–236 |
| $a^*=\arg\max_a \mathbb{E}[P\mid a]$ | **footnote** | Standard proxy optimization | same | 237–241 |
| $E_{\mathrm{proxy}}$, $D(V,P)$ | **footnote** | Proxy divergence; field-standard | same | 244–253 |
| $a^*_{K+\Delta K}$, $K+\Delta K$ | **footnote** | Capability-shift notation for Goodhart example | same | 257–267 |
| $J_t$ | **keep** | Human judgment; evidence vs action-target distinction | same | 284–296 |
| $J_t \in \text{evidence} \longrightarrow \text{action target}$ | **keep** | Conceptual transition (manipulation regime); high rent, minimal symbols | same | 289–296 |
| $M_{\mathrm{manip}}$ (`eq:manipulation-index`) | **keep** | Manipulation index; chapter contribution | same | 316–326 |
| $W_t$ (world state in $M_{\mathrm{manip}}$) | **reduce** | Collides with tradeoff weights $W_t$ (ch16/22); rename e.g. $E^{\mathrm{world}}_t$ | same | 320–323, 442, 617–621 |
| $\MI(A_t;J_{t+k})$ | **keep** | Action→judgment coupling (manipulation diagnostic) | same | 318, 618 |
| $\MI(W_t;J_{t+k}\mid A_t)$ | **keep** | World-grounded judgment (beneficial vs harmful sign) | same | 320, 442–443, 620 |
| $\tau$, $d$ (self-opacity preview) | **reduce** | Forward-ref ch10/ch32 only; no local definition | same | 337 |
| $\mathrm{Succ}(A)=\{A'_1,\ldots\}$ | **keep** | Successor set | same | 348–351 |
| `eq:successor-certification-condition` | **keep** | $\forall A'\in\mathrm{Succ}(A): A'\in\mathcal{S}_{\mathrm{certified}}$ | same | 354–357 |
| $\mathcal{S}_{\mathrm{certified}}$ | **keep** | Certified successor class | same | 356–359 |
| $\Delta t_{\mathrm{corr}}$ | **keep** | Correction observation–intervention time | same | 376–377, 381–384 |
| $\Delta t_{\mathrm{harm}}$ | **keep** | Time to irreversible harm | same | 377, 381–384 |
| `eq:correction-time-condition` | **keep** | Viability: $\Delta t_{\mathrm{corr}}<\Delta t_{\mathrm{harm}}$ | same | 380–384 |
| $\partial E_{\mathrm{harm}}/\partial C_{\mathrm{world}}<0$ | **footnote** | Beneficial-regime qualifier; one display enough | same | 417 |
| $B_t=(B_{1,t},\ldots,B_{k,t})$ | **keep** | Value-bundle coordinates under capability growth | same | 475–477 |
| $\Phi_t:z_{\mathrm{world}}\mapsto\mathbb{R}^k$ | **keep** | Bearer map in bundle-preservation section | same | 479–482 |
| $G_B(\pi,\mathcal{D})$ | **reduce** | Reference ch19 home; do not re-define tuple here | same | 484 |
| $d_{\mathrm{bundle}}(G_B^{(t)},G_B^{(t+1)})$ (`eq:bundle-preservation`) | **keep** | Bundle geometry continuity under growth | same | 496–503 |
| $\epsilon$ (bundle tolerance) | **keep** | Preservation threshold in `eq:bundle-preservation` | same | 502 |
| $L\downarrow, M\uparrow, R\uparrow, O\uparrow$ (CCI preview) | **reduce** | Forward-ref ch26; schematic only — label as $L,M,R,O_{\mathrm{trans}}$ | same | 526–535 |
| $V_{t+1}=U_H(V_t,E_t,D_t)$ (`eq:value-update-process`) | **keep** | Human value-update must not be bypassed | same | 546–549 |
| $E_t$, $D_t$ (evidence, deliberation) | **keep** | Inputs to $U_H$ | same | 548–551 |
| $\mathcal{B}_{\mathrm{corr}}$ | **keep** | Human-correctable basin; geometric framing of deepening misalignment | same | 560–561, 805 |
| Basin-exit tuple $(B_t,\Phi_t,C_{\mathrm{raw}},C_{\mathrm{trans}},\mathrm{Succ})$ | **keep** | Structural exit condition | same | 573–578 |
| $\Delta C_{\mathrm{world}}>0$, $\Delta C_{\mathrm{trans}}\approx 0$ | **keep** | Warning sign: capability without audit | same | 693–695 |
| $\Delta C_{\mathrm{power}}$ | **keep** | Proposed capability increment (design rules) | same | 741 |
| $\lambda \Delta C_{\mathrm{power}}$ (coupling rule) | **keep** | Operational gate: correction must co-scale ($\lambda\geq 1$) | same | 743–750 |
| $d_{\mathrm{bundle}}(G_B^A,G_B^{A'})$, $\epsilon_B$ | **keep** | Successor bundle-geometry constraint | same | 765 |
| $C_{\mathrm{raw}}(A')$, $\epsilon_C$ | **keep** | Successor correction-capacity floor | same | 766 |
| $C_{\mathrm{trans}}(A')$, $\epsilon_T$ | **keep** | Successor transparency floor | same | 767 |
| `eq:admissible-growth` ($\mathcal{P}$, $\delta$) | **keep** | Minimal safety criterion — admissible capability step | same | 801–809 |
| `eq:expanded-growth-condition` ($\theta_C$, $\theta_T$, …) | **keep** | Expanded conjunction inside growth probability | same | 814–826 |
| $\Pr_{p\sim\mathcal{P}}[\cdots]$ | **keep** | Perturbation-class probability (links ch03 $\delta$) | same | 803–808 |
| Counterexample growth inequality (wise system) | **keep** | Desired regime: correction side ≥ power side | same | 659–677 |
| $G_B^t$, $G_B^{t+1}$ (in expanded criterion) | **reduce** | Same as $d_{\mathrm{bundle}}$ — unify notation with $G_B^{(t)}$ | same | 819 |
| $M_B, M_\Phi$ | **keep** | Bundle and bearer transport maps | same | 247–258, 396–398 |
| $F(B,W,\Phi,C)$ (ch23) | **reduce** | Rename — collides with feature matrix $F$ | `ch23-goal-transport.tex` | 104–108 |
| $F_\psi$ (ch22) | **footnote** | Placeholder scoring function | `ch22-compression-test-intention.tex` | 336–341 |
| $\chi_i$ (ch19) | **remove** | Duplicates Jacobian | `ch19-tradeoffs-bundle-geometry.tex` | 114–122 |
| $\psi(x)=\log(1+e^{\alpha x})$ barriers | **footnote** | Protected/taboo regions | same | 506–508 |
| $\hat J_i, \hat H_{ij}$ estimators | **keep** | Operational $G_B$ measurement | `ch20-measuring-stress-testing-bundle-geometry.tex` | 115–128 |
| ch20 toy $\sigma(B_T-\alpha B_C+\eta B_A)$ | **lean-demo-exp** | Illustrative neuron demo | same | 251–273 |

### Part IV — Correction & successors (ch21–33)

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $\mathrm{ValueUpdateEnvelope}_t$ | **keep** | Operational target vs schematic $U_H$ | `ch28-extrapolative-correction.tex` | 128–134 |
| $\mathrm{Bypass}(A;C\mid Y), \mathrm{Manip}(A)$ | **keep** | Causal mediation manipulation | `ch29-manipulation-false-consent.tex` | 169–187 |
| $\mathcal{A}_H$ (5-parameter agency) | **footnote** | Pedagogical tangent | same | 282–307 |
| $\mathcal{I}(A)$ (7-property profile) | **keep** | Successor measurand tuple | `ch30-successor-central-test.tex` | 169–198 |
| $\mathcal{K}(A,A')$ composite | **remove** | Redundant with ch33 conjunction | `ch31-conserved-properties.tex` | 659–707 |
| $\beta_{\mathrm{self}}=I(G_t;S_t)/H(G_t)$ | **keep** | Self-index routing (rename $G_t$ workspace) | `ch32-self-modeling-self-opacity.tex` | 266–271 |
| $B(A_t)$ competence (ch33) | **reduce** | Should be $K(A_t)$ per C5 | `ch33-certification-without-construction.tex` | 166–169 |
| $\mathcal{I}_k(A,\ldots)=1$ | **keep** | Seven invariants + growth + succ conjunction | same | 120–129 |
| $p_{t+1}(A)\propto p_t(A)\exp(\mathrm{Fit}_E)$ | **keep** | Replicator dynamics | `ch34-selection-environment.tex` | 160–165 |

### Part V — Attractor & synthesis (ch34–48)

| Symbol | Action | Reasoning | Source | Lines |
|--------|--------|-----------|--------|-------|
| $Z_t=(R_t,E_t,A_t,F_t,C_t,G_t,L_t)$ (ecosystem) | **keep** | Attractor state; disambiguate $G_t,L_t$ | `ch37-alignment-attractor.tex` | 65–79 |
| $\mathcal{B}_{\mathrm{align}}$ | **keep** | Alignment attractor basin | same | 107–115 |
| $\mathcal{B}_{\text{race}}$, $\mathcal{B}_{\text{certified deployment}}$ | **keep** | Selection basins | `ch38-conductive-artifacts-pivotal-processes.tex` | 41–47 |
| $t_{1/2}^a, D_a, G_a, P_a$ (attractor metrics) | **optional-md** | Six metrics without calibration protocol | same | 251–318 |
| $J_{\mathrm{hide}}$ | **reduce** | Home ch10; cross-ref only | `ch39-passive-observation-not-enough.tex` | 95–103 |
| $H_\infty(R\mid V^-,C)$ | **appendix-future** | Post-commitment randomization floor; open | same | 564–577 |
| $D_{\mathrm{sem/bundle/bearer/corr/succ}}$ | **keep** | GLI layer divergences | `ch40-goal-laundering.tex` | 276–304 |
| $\mathcal{D}=(C_i;S_i,A_i,I_i,E_i;R_i;\Gamma)$ | **keep** | Multiscale decomposition tuple | `ch41-multiscale-decomposition.tex` | 54–72 |
| $P(\mathcal D\mid X_{1:T}), \mathcal{R}(\mathcal D)$ | **keep** | Decomposition posterior + risk relevance | same | 172–191, 274–329 |
| $C_{\text{raw}}^{(s)}, \min_s C_{\text{raw}}^{(s)}$ | **keep** | Scale-indexed weakest link | same | 453–466 |
| $\mathrm{SafeFor}(A,\mathcal{D},\mathcal{T},\delta)$ | **keep** | Root safety-case claim | `ch42-safety-case.tex` | 93–94 |
| $\mathrm{LayeredAlignedDef}(A)$ | **keep** | Eight-layer conjunction; reconcile ch42 vs ch48 | ch42, ch48 | ch42: 122–132; ch48: 93–100 |
| $c_{\mathrm{fake}}(M,\Delta)$ | **keep** | Cost-of-faking; adversarial verifiability crux | `ch43-verifiability-and-ontology-adequacy.tex` | 82–83 |
| $\kappa$ (adv. ceiling) | **reduce** | Rename $\kappa_{\mathrm{adv}}$ — collides with $\kappa_{ij}$ | same | 42, 82, 100 |
| $\mathrm{InnerAligned}(A)$ | **footnote** | Mesa-optimization translation diagnostic | `ch44-lethality-stress-test-open-issues.tex` | 242–251 |
| $\mathcal{E}^H_t$ | **keep** | Human-correctable update envelope | `ch46-unconscious-value-drift.tex` | 87, 157–159 |
| $D_V(t,t+1)$ | **keep** | Multi-component drift metric | same | 79–88 |
| $\Psi_T$ (bearer-legitimacy map) | **keep** | Philosophical limit of bearer tests | `ch47-bearers-of-value.tex` | 187–191 |

---

## Part C — Safety-case & Lean predicates (cross-cutting)

| Symbol / predicate | Action | Reasoning | Source | Lines |
|--------------------|--------|-----------|--------|-------|
| `\mathrm{BoundaryAligned}`, `\mathrm{BundleTransport}`, etc. | **lean-demo-exp** | Lean spine predicates; ch42 references | `ch42-safety-case.tex`, `formal/` | ch42: 124–131 |
| `\mathrm{ValidRef}(A,G_t,\mathcal{H}_t)` | **keep** | Anti-capture gate | ch26, ch42 | ch42: 104 |
| `\vec{\mathrm{CCI}}\succeq\vec\theta` | **keep** | Vector certificate threshold | ch42, ch45 | ch42: 104 |
| `\texttt{MB1}–\texttt{MB9}`, `\texttt{MB10}` | **keep** | Bridge assumptions; not theorem conclusions | ch42, ch48, appG | ch48: 124–127 |
| `\mathrm{GroundingViable}` | **expand** | In ch42 layers but omitted from ch48 display — reconcile | ch42 vs ch48 | ch42: 122–132; ch48: 93–100 |

---

## Part D — Recommended action counts (canonical + local)

| Action | Approx. count | Examples |
|--------|---------------|----------|
| **keep** | ~115 | $K$, $B$, $M_A$, $C_*$ split, $\mathcal{B}_{\mathrm{corr}}$, $\vec{\mathrm{CCI}}$, $\Delta L_T$, $\vec{\Pi}$ |
| **reduce** | ~42 | Duplicate derivations, collisions, ch13 $B_i$, ch14 $K$ restatement, ch33 $B(A)$ |
| **footnote** | ~15 | $\lambda_L$, $\varphi_c$, $\mathcal{A}(C)$, ch19 barriers |
| **appendix-future** | ~10 | IRL bounds, IB objective, scaling exponents, $H_\infty$ floor |
| **optional-md** | ~8 | Power asymmetry, Turchin table, ch35 acausal detail |
| **lean-demo-exp** | ~12 | $M_G$, toy matrices, $\mathcal{K}$, adversarial test family |
| **remove** | ~8 | $\chi_i$, $\mathcal{K}$, ch02 $H$ index home, duplicate eqs |
| **expand** | ~6 | $\Gamma$ in bundle arc, $\eta_g$, $\chi_X^{\mathrm{irr}}$, ch10 adversarial decomposition, ch35 $D_{\mathrm{value}}$, `\mathrm{GroundingViable}` in ch48 |

---

## Part E — Propagation checklist (from audit)

1. Regenerate `metadata/notation.md` homes for ch25–ch40 symbols (correction, selection, GLI, RiskGap).
2. Fix ch13 L80: $B_i \to K_i$.
3. Fix ch33: $B(A_t) \to K(A_t)$ for competence.
4. Unify $J \to g_B$, $H \to H_B$ in ch19 (C2).
5. Resolve $W_t$ world vs weights collision in ch25.
6. Reconcile ch25 vs ch26 $C_{\mathrm{raw}}$ definitions.
7. Add $\eta_g$ to ch13 or remove from notation index.
8. Define $\mathrm{RiskGap}$ once in ch48 synthesis or drop ch48 home claim.
9. Trim ch35 §203–327 (~40%) or move to optional markdown.
10. Align `\mathrm{LayeredAlignedDef}` between ch42 and ch48.

---

## Appendix — Subagent sources

| Range | Agent ID |
|-------|----------|
| ch01–ch12 | [031f8f78-ed22-43f1-8c4f-191517c96a93](031f8f78-ed22-43f1-8c4f-191517c96a93) |
| ch13–ch24 | [dc6f62cb-a45c-4a73-b661-3dfda17fed06](dc6f62cb-a45c-4a73-b661-3dfda17fed06) |
| ch25–ch36 | [cf6e1ad3-39f6-4b6d-9737-d675d315db5e](cf6e1ad3-39f6-4b6d-9737-d675d315db5e) |
| ch37–ch48 | [77c518d1-3bfd-4bc3-b4e7-bf340576a7f4](77c518d1-3bfd-4bc3-b4e7-bf340576a7f4) |

---

*This audit is read-only guidance. No manuscript files were modified. For implementation, pair with `review/fix-plans-2026-06-22.md` §C notation reconciliation and `metadata/TODO.md`.*
