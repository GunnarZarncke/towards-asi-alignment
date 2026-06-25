# Notation

Single source for Appendix A (notation index). Regenerate the typeset index with `python3 scripts/generate_notation_appendix.py` (also run from `./build.sh`).

Cross-chapter reconciliation: `review/fix-plans-2026-06-22.md` §C. Formal predicates: `formal/README.md`, Appendix I. Operational terms (not symbols): `metadata/terminology.md`, Appendix F.

## Maintainer notes

**Status (2026-06-23):** Canonical target notation after §C reconciliation. Rows marked **⟳** in Home are not yet fully propagated in the manuscript.

**Propagation done (2026-06-23):** C1 (ΔL sign, intro), C2 ($g_B$/$H_B$/$G_B$ + retire $T_{ij}$), C4/C16 ($C_{\text{raw}}$/$CCI$), C5 ($K$ vs $B$), C6 ($\eta_g$/$\eta_c$, $G_{\text{coord}}$/$\Omega_{\text{coord}}$), C7 ($U_H$, roman $V_t$; $U_S$), C8 ($F$, $k$), C10 ($C_X$), C11 ($\chi_{ij}(a)$), C15 (`\MI`).

**Still pending:** C12 pivotal-process basins (ch35 content, not rename); $C_H$ vs $C^H_t$ convention; $\mathcal V$ (ch19 value-representation set) vs $V_t$ tuple.

**§C16 terminology:** *capacity* = $C_{\text{raw}}$; *integrity* = $CCI$. Retired: $C_{\text{corr}}$ (except ch05 $C_{\text{corr}}^{\text{society}}$). Goodharting lowers integrity via $M$ and $O$, not a separate penalty term.

**Seven conserved successor properties (ch29):** boundary closure, memory lineage, bundle response geometry, bearer-map continuity, correction-channel capacity, transparency policy, control-locus continuity — defined in ch29; ch31 groups them for audit.

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
| $G_{\text{coord}}$ | Collective coordination gain | ch13 |
| $\Omega_{\text{coord}}$ | Collective coordination loss | ch13 |
| $S_X$ | Residual surprise across boundary $X$ | ch11 |

### Value bundles and geometry

| Symbol | Definition | Home |
|--------|------------|------|
| $B$ | Value bundle (low-dimensional control direction); $B_i$ = dimension $i$ | ch16 |
| $k$ | Number of value-bundle dimensions | ch18 |
| $\hat B,\hat W,\hat\Phi$ | MAP value-bundle inference estimate | ch16 |
| $W$ | Bundle context-activation weights | ch16 |
| $G_B$ | Bundle response geometry (gradients, curvature, protected regions, bearer weights) | ch19 |
| $g_B$ | Bundle gradient field $\partial\pi/\partial B_i$ | ch19 |
| $H_B$ | Interaction curvature (Hessian of $\log\pi$ in bundle space) | ch19 |

### Bearer maps

| Symbol | Definition | Home |
|--------|------------|------|
| $\Phi$ | Bearer map: world features to bundle relevance | ch18 |
| $F$ | Feature matrix $F\in\mathbb{R}^{N\times n}$ (ch17; not the bearer map) | ch17 |

### Intention and goal transport

| Symbol | Definition | Home |
|--------|------------|------|
| $L$ | Log-evidence / predictive score (higher = better fit) | ch21 |
| $DL(\cdot)$ | Description length (model-complexity cost) | ch21 |
| $\Delta L_{\text{int}}$ | Intentional compression gain | ch21 |
| $\Delta L_{\text{transport}}$ | Goal-transport compression gain | ch22 |
| $\Delta L_T$ | Transport decomposition (semantic, bundle, bearer, correction, successor) | ch23 |

### Correction and integrity

| Symbol | Definition | Home |
|--------|------------|------|
| $G_t$ | Correcting agent at time $t$ | ch24 |
| $\mathcal{H}_t$ | Handle set controlled by $G_t$ | ch24 |
| $W_t\to O_t\to J_t\to D_t\to C_t\to U_{t+1}\to A_{t+k}$ | Correction trace induced by controlled handles | ch24 |
| $C_{\text{raw}}$ | Bare weakest effective handle capacity | ch25 |
| $CCI$ | Correction-channel integrity ($C_{\text{raw}}$ minus penalties) | ch25 |
| $\mathrm{Control}(A)$ | Effective actuator control capacity | ch11 |
| $\mathrm{RiskGap}(A)$ | $\mathrm{Control}(A)-\mathrm{CCI}(A)$ | ch31 |
| $\mathrm{Risk}(A)$ | Certification risk functional | ch31 |
| $\mathrm{SelfControlGap}(A)$ | Self-control minus correction demand | ch30 |
| $L,M,R,O$ | CCI penalties: latency, manipulability, reversibility loss, ontology mismatch | ch25 |
| $\lambda_L,\lambda_M,\lambda_R,\lambda_O$ | CCI penalty weights | ch25 |
| $U_H$ | Human value-update operator | ch04 |
| $U_S$ | System correction-update operator | ch24 |
| $V_t$ | Value-state tuple (full object in ch04; chapters may project) | ch04 |
| $C_H$ | Human correction capacity (component of $V_t$) | ch04 |

### Successors and certification

| Symbol | Definition | Home |
|--------|------------|------|
| $\text{Succ}(A)$ | Successors of agent $A$ | ch28 |
| $\mathcal S_{\text{certified}}$ | Certified successor class | ch31 |
| $\mathcal C$ | Certified class in the dynamical guarantee | ch03 |
| $\delta$ | Catastrophic-drift probability bound | ch03 |
| $\tau$ | Self-transparency $1-I(M;\hat M)/H(M)$ | ch30 |

### Multi-agent, selection, parasites, laundering

| Symbol | Definition | Home |
|--------|------------|------|
| $\kappa_{ij}$ | Cooperativity index | ch33 |
| $\varphi$ | Cooperation order parameter | ch33 |
| $\varphi_c$ | Percolation threshold for cooperation | ch33 |
| $\chi$ | Artifact conductivity | ch34 |
| $\chi_{ij}(a)$ | Artifact conductivity on edge $(i,j)$ for artifact $a$ | ch35 |
| $\mathrm{ICI}_{ij}$ | Inferential coupling index | ch33 |
| $C_X$ | Host correction capacity (parasite criterion) | ch34 |
| $A_Y,I_Y,\lambda_Y$ | Parasite action entropy, internal entropy, weight | ch34 |
| $GLI$ | Goal-laundering index | ch37 |
| $\mu_E(A)$ | Deployment / control mass in selection environment $E$ | ch32 |
| $\mathrm{Fit}_E(A)$ | Fitness (log-rate of $\mu_E$ growth) | ch32 |
| $P(A)$ | Preservation score | ch32 |
| $\kappa_{\mathrm{sel}}(E,A,h)$ | Effective selection capacity through handle $h$ | ch32 |

### Conventions

| Symbol | Definition | Home |
|--------|------------|------|
| $K$ vs $B$ | $K$ = capability; $B$ = value bundle (never swap) | ch11 |
| $k$ | Bundle dimension count (not $m$) | ch18 |
| $\Delta L$ sign | Positive gain = richer model earns its complexity cost | ch21 |
| Bundle catalogue | New bundle dimensions are added in ch16, not locally elsewhere | ch16 |
