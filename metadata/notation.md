# Notation

Single source for Appendix A (notation index). Regenerate the typeset index with `python3 scripts/generate_notation_appendix.py` (also run from `./build.sh`).

Cross-chapter reconciliation: `review/fix-plans-2026-06-22.md` §C. Formal predicates: `formal/README.md`, Appendix I. Operational terms (not symbols): `metadata/concepts.yml`, Appendix F.

## Maintainer notes

**Status (2026-06-23):** Canonical target notation after §C reconciliation. Rows marked **⟳** in Home are not yet fully propagated in the manuscript.

**Propagation done (2026-06-23):** C1 (ΔL sign, intro), C2 ($g_B$/$H_B$/$G_B$ + retire $T_{ij}$), C4/C16 ($C_{\mathrm{raw}}$/$CCI$), C5 ($K$ vs $B$), C6 ($\eta_g$/$\eta_c$, $G_{\text{coord}}$/$\Omega_{\text{coord}}$), C7 ($U_H$, roman $V_t$; $U_S$), C8 ($F$, $k$), C10 ($C_X$), C11 ($\chi_{ij}(a)$), C15 (`\MI`).

**Still pending:** C12 pivotal-process basins — notation rows added (ch38); **operationalize** $\mathbb{B}_{\mathrm{race}}$ / $\mathbb{B}_{\mathrm{certified}}$ beyond loose set descriptions (percolation/$\tilde{\kappa}$, $\mu_E$, basin-stability predicates; see `metadata/TODO.md`); propagate in synced concept cards; $C_H$ vs $C^H_t$ convention; $\mathcal V$ (ch19 value-representation set) vs $V_t$ tuple.

**§C16 terminology:** *capacity* = $C_{\mathrm{raw}}$; *integrity* = vector/status $CCI$; scalar projections should be marked $CCI_\lambda$. Retired: $C_{\text{corr}}$ (except ch05 $C_{\text{corr}}^{\text{society}}$). Goodharting lowers integrity via $M$ or invalidates grounding; residual ontology translation loss is \(O_{\mathrm{trans}}\).

**Seven conserved successor properties (ch48):** boundary closure, memory lineage, bundle response geometry, bearer-map continuity, correction-channel capacity, transparency policy, control-locus continuity — defined in ch48; ch48 groups them for audit.

---

## Appendix index

Tables below are parsed into `metadata/notation-index.tex` for Appendix A. Keep definitions to one line; full derivations stay in the home chapter.

### Boundary and state

| Symbol | Definition | Home |
|--------|------------|------|
| $I_t$ | Internal state at time $t$ | ch06 |
| $E_t$ | External state at time $t$ | ch06 |
| $S_t$ | Sensory interface at time $t$ | ch06 |
| $A_t$ | Active interface at time $t$ | ch06 |
| $\epsilon$ | Allowed boundary leakage tolerance | ch07 |
| $I(X;Y\mid Z)$ | Conditional mutual information | ch07 |
| $H(\cdot)$ | Shannon entropy | ch02 |

### Capability and growth

| Symbol | Definition | Home |
|--------|------------|------|
| $K$ | Capability / competence functional across a boundary | ch11 |
| $I_{\text{pred}}$ | Predictive information across the boundary | ch11 |
| $I_{\text{ctrl}}$ | Control information across the boundary | ch11 |
| $\beta,\gamma$ | Internal-entropy and structure penalties in $K$ | ch11 |
| $S$ | Structure / complexity term in $K$ (distinct from $S_t$, $S_X$) | ch11 |
| $\eta_g$ | Growth efficiency | ch13 |
| $\eta_c$ | Coordination efficiency | ch13 |
| $B_i$ | Local competence of component $i$ (distinct from value-bundle coordinate $B_i$ in ch16) | ch13 |
| $K_{\mathrm{coll}}$ | Effective collective competence | ch13 |
| $G_{\text{coord}}$ | Collective coordination gain | ch13 |
| $\Omega_{\text{coord}}$ | Collective coordination loss | ch13 |
| $S_X$ | Residual surprise across boundary $X$ | ch11 |

### Value bundles and geometry

| Symbol | Definition | Home |
|--------|------------|------|
| $B$ | Value bundle (low-dimensional control direction); $B_i$ = dimension $i$ | ch16 |
| $\mathsf{VB}_i$ | Value-bundle pair $(B_i,\Phi_i)$ | ch19 |
| $k$ | Number of value-bundle dimensions | ch18 |
| $\hat B,\hat W,\hat\Phi$ | MAP value-bundle inference estimate | ch16 |
| $W$ | Bundle context-activation weights | ch16 |
| $G_B$ | Bundle response geometry (gradients, curvature, protected regions, bearer weights) | ch19 |
| $g_B$ | Bundle gradient field $\partial\pi/\partial B_i$ | ch19 |
| $H_B$ | Interaction curvature (Hessian of $\log\pi$ in bundle space) | ch19 |

### Grounding and abstraction validity

| Symbol | Definition | Home |
|--------|------------|------|
| $X_{\mathrm{real}}$ | Value-relevant real-world state or history being abstracted | ch03 |
| $\alpha$ | Abstraction map from value-relevant reality into the checked representation | ch03 |
| $Z$ | Checked value-relevant abstraction: bundle coordinates, bearer maps, monitor states, or safety-case variables | ch03 |
| $\Gamma$ | Grounding relation connecting real-world history, checked abstraction, correction signal, and update | ch03 |
| $d_V$ | Distance over value-relevant real-world structure | ch03 |
| $d_Z$ | Distance in the checked abstraction | ch03 |
| $\mathsf{Unc}_{\alpha}$ | Uncertainty about whether abstraction $\alpha$ still applies | ch03 |
| $\operatorname{Dom}(\Gamma)$ | Domain in which grounded correction remains meaningful | ch03 |

### Bearer maps

| Symbol | Definition | Home |
|--------|------------|------|
| $\Phi$ | Bearer map: world features to bundle relevance | ch18 |
| $F$ | Feature matrix $F\in\mathbb{R}^{N\times n}$ (ch17; not the bearer map) | ch17 |

### Intention and goal transport

| Symbol | Definition | Home |
|--------|------------|------|
| $L$ | Log-evidence / predictive score (higher = better fit) | ch46 |
| $DL(\cdot)$ | Description length (model-complexity cost) | ch46 |
| $\Delta L_{\text{int}}$ | Intentional compression gain | ch46 |
| $\Delta L_{\text{transport}}$ | Goal-transport compression gain | ch46 |
| $\Delta L_T$ | Transport decomposition (semantic, bundle, bearer, correction, successor) | ch46 |

### Correction and integrity

| Symbol | Definition | Home |
|--------|------------|------|
| $G_t$ | Correcting agent at time $t$ | ch25 |
| $\mathcal{H}_t$ | Handle set controlled by $G_t$ | ch25 |
| $W_t\to O_t\to J_t\to D_t\to C_t\to U_{t+1}\to A_{t+k}$ | Correction trace induced by controlled handles | ch25 |
| $C_{\mathrm{raw}}$ | Weakest required correction case after bottlenecking over certified correction traces | ch25 |
| $CCI$ | Correction-channel integrity as a vector/status certificate with validity and per-coordinate thresholds | ch26 |
| $CCI_\lambda$ | Scalar projection of the CCI vector for exposition, not the certification object | ch26 |
| $\mathrm{Control}(A)$ | Effective actuator control capacity | ch11 |
| $\mathrm{RiskGap}(A)$ | $\mathrm{Control}(A)-\mathrm{CCI}(A)$ | ch33 |
| $\mathrm{Risk}(A)$ | Certification risk functional | ch48 |
| $\mathrm{SelfControlGap}(A)$ | Self-control minus correction demand | ch32 |
| $L,M,R,O_{\mathrm{trans}}$ | CCI residual coordinates: latency, manipulation, irreversibility, and grounded-correction translation loss | ch46 |
| $\lambda_L,\lambda_M,\lambda_R,\lambda_O$ | CCI penalty weights | ch46 |
| $U_H$ | Schematic human value-update notation; operational certification uses `ValueUpdateEnvelope` / human-correctable update conditions | ch04 |
| $U_S$ | System correction-update operator | ch46 |
| $V_t$ | Value-state tuple (full object in ch04; chapters may project) | ch04 |
| $C_H$ | Human correction capacity (component of $V_t$) | ch04 |

### Successors and certification

| Symbol | Definition | Home |
|--------|------------|------|
| $\text{Succ}(A)$ | Successors of agent $A$ | ch46 |
| $\mathcal S_{\text{certified}}$ | Certified successor class | ch48 |
| $\mathcal C$ | Certified class in the dynamical guarantee | ch03 |
| $\delta$ | Catastrophic-drift probability bound | ch03 |
| $\tau$ | Self-transparency $1-I(M;\hat M)/H(M)$ | ch32 |
| $B_{\mathrm{race}}$ | Race selection basin ($\mathbb{B}_{\mathrm{race}}$ in typeset math) | ch38 |
| $B_{\mathrm{certified}}$ | Certified-deployment basin ($\mathbb{B}_{\mathrm{certified}}$) | ch38 |
| $B_{\mathrm{align}}$ | Alignment attractor basin | ch37 |
| $B_{\mathrm{corr}}$ | Human-correctable basin | ch14 |
| $B_{\mathrm{safe}}$ | Safety basin (subscripted; generic ch03 basin may appear as bare $\mathcal{B}$) | ch33 |
| $B_{\mathrm{bearer}}$ | Bearer set after transformation | ch47 |

### Multi-agent, selection, correction-audit evasion, laundering

| Symbol | Definition | Home |
|--------|------------|------|
| $\kappa_{ij}$ | Cooperativity index | ch48 |
| $\varphi$ | Cooperation order parameter | ch48 |
| $\varphi_c$ | Percolation threshold for cooperation | ch48 |
| $\chi$ | Artifact conductivity | ch46 |
| $\chi_{ij}(a)$ | Artifact conductivity on edge $(i,j)$ for artifact $a$ | ch48 |
| $\mathrm{ICI}_{ij}$ | Inferential coupling index | ch35 |
| $C_X$ | Host correction capacity (correction-audit-evasion criterion) | ch46 |
| $A_Y,I_Y,\lambda_Y$ | Evasion-process action entropy, internal entropy, weight | ch46 |
| $GLI$ | Goal-laundering index | ch40 |
| $D_G$ | Goal-layer divergence score | ch40 |
| $\Omega_Q$ | Selective opacity score | ch10 |
| $\mu_E(A)$ | Deployment leverage in deployment environment $E$ | ch34 |
| $\mathrm{Fit}_E(A)$ | Deployment growth rate (fitness, for short in formulas); log-rate of $\mu_E$ growth | ch34 |
| $\vec{\Pi}(A)$ | Preservation conditions (vector-status list) for selection alignment | ch34 |
| $N_{\mathrm{proxy}}$ | Proxy-throughput count between independent target checks (feedback-horizon exposure) | ch34 |
| $\mathrm{InvFit}_E(a\mid D)$ | Invasion fitness: rare-type deployment growth in resident environment $D$ | ch34 |
| $M_{\mathrm{sel}}$ | Selector manipulation bound in $\vec{\Pi}(A)$ | ch34 |
| $\mathrm{AdvVerif}$ | Adversarial verification meaningful (preservation coordinate) | ch34 |
| $\kappa_{\mathrm{sel}}(E,A,h)$ | Effective selection capacity through handle $h$ | ch46 |

### Conventions

| Symbol | Definition | Home |
|--------|------------|------|
| $K$ vs $B$ | $K$ = capability; $B$ = value bundle (never swap) | ch11 |
| $N_{\mathrm{proxy}}$ vs $K_X$ vs $K_{\mathrm{coll}}$ | Proxy-throughput count (ch34) vs blanket competence (ch11) vs collective competence (ch13) | ch34 |
| $k$ | Bundle dimension count (not $m$) | ch18 |
| $\Delta L$ sign | Positive gain = richer model earns its complexity cost | ch46 |
| Bundle catalogue | New bundle dimensions are added in ch16, not locally elsewhere | ch16 |
