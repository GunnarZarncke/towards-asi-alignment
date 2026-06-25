# Notation

Canonical symbol reference for the manuscript. See `INSTRUCTIONS.md` §18 for the formal spine and `review/fix-plans-2026-06-22.md` §C for the cross-chapter reconciliation decisions this table records.

**Status (2026-06-23):** This table reflects the **canonical target** notation after the §C reconciliation. Rows still **not yet propagated** into chapters are marked **⟳ propagating**. Keep this file, `appendices/appA-notation.tex`, and `INSTRUCTIONS.md` §18 in sync as propagation completes.

**Propagation done (2026-06-23, build verified):** C1 (ΔL sign, intro), C2 ($g_B$/$H_B$/$G_B$ + retire $T_{ij}$, ch16/17), C4/C16 ($C_{\text{raw}}$/$CCI$, retire $C_{\text{corr}}$ except ch05 `$C_{\text{corr}}^{\text{society}}$`; ontology penalty $O$), C5 ($K$ capability in ch11–13; $B$ reserved for value bundle), C6 ($\eta_g$/$\eta_c$ + $G_{\text{coord}}$/$\Omega_{\text{coord}}$), C7 ($U_H$ + roman $V_t$; $U_S$ in ch24/29/38), C8 ($F$, $k$), C10 ($C_X$), C11 ($\chi_{ij}(a)$), C15 (`\MI`).

**Still pending / flagged:**
- **C12 (pivotal-process $\mathcal B_{\text{race}}\to\mathcal B_{\text{certified}}$):** deferred — content for ch35, not a rename pass.
- **Sync:** `appendices/appA-notation.tex` + `INSTRUCTIONS.md` §18; **Lean** spine (`metadata/TODO.md`).
- **$C_H$ vs $C^H_t$:** tuple component vs time-indexed MI variable — convention to confirm.
- **$\mathcal V$ (ch19):** value-representation *set*, not value-state tuple $V_t$; left calligraphic.

---

## Boundary and state

| Symbol | Meaning |
|--------|---------|
| $I_t$ | Internal state at time $t$ |
| $E_t$ | External state at time $t$ |
| $S_t$ | Sensory interface at time $t$ |
| $A_t$ | Active interface at time $t$ |
| $\epsilon$ | Allowed boundary leakage |
| $I(X;Y\mid Z)$ | Conditional mutual information (macro `\MI`); boundary criterion $I(I_{t+1};E_{t+1}\mid S_t,A_t)\le\epsilon$ |
| $H(\cdot)$ | Shannon entropy |

## Capability and growth

| Symbol | Meaning |
|--------|---------|
| $K$ | **Capability / competence functional** (§C5): $K=I_{\text{pred}}+I_{\text{ctrl}}-\beta H(I)-\gamma S$; boundary competence $K_X$, collective $K_H$, comparison baseline $K_{\mathrm{ref}}$. **$B$ is reserved for the value bundle** (Part IV+). |
| $I_{\text{pred}}$ | Predictive information across the boundary |
| $I_{\text{ctrl}}$ | Control information across the boundary |
| $\beta,\gamma$ | Internal-entropy and structure/complexity penalties in $K$ |
| $S$ | Structure/complexity term in $K$ (context-distinct from sensory interface $S_t$ and residual surprise $S_X$) |
| $\eta_g,\ \eta_c$ | Growth efficiency / coordination efficiency (§C6; split of the overloaded $\eta$) |
| $G_{\text{coord}},\ \Omega_{\text{coord}}$ | Collective coordination gain / loss (§C6; retire $B_{\text{coord}}$/$C_{\text{friction}}$) |
| $S_X$ | Residual surprise across boundary $X$ (§C6; retire $S^{(i)}$, $\mathcal S$) |

## Value bundles and geometry

| Symbol | Meaning |
|--------|---------|
| $B$ | **Value bundle** (Part IV+); $B_i$ = value-bundle dimension $i$ |
| $k$ | Number of value-bundle dimensions (§C8; fix ch18's $m$) |
| $\hat B,\hat W,\hat\Phi$ | MAP value-bundle inference: $\arg\max_{B,W,\Phi}P(A_{1:T}\mid I_{1:T},B,W,\Phi)\,P(B,W,\Phi)$ |
| $W$ | Bundle context-activation weights |
| $G_B$ | **Bundle response geometry** = the ch19 4-tuple (bundle gradients, interaction curvature, protected regions, bearer-dependent context weights) (§C2) |
| $g_B$ | Bundle gradient field $\partial\pi/\partial B_i$ (§C2; partial object that composes into $G_B$) |
| $H_B$ | Interaction curvature = Hessian of $\log\pi$ (§C2; the one curvature operator — retire $T_{ij}$, $\partial^2\pi/\partial B_i\partial B_j$ variants) |

## Bearer maps

| Symbol | Meaning |
|--------|---------|
| $\Phi$ | **Bearer map** everywhere; $\Phi_k:z_{\text{world}}\mapsto\text{bundle relevance}$ for bundle $k$ (§C8) |
| $F$ | ch17 feature matrix $F\in\mathbb R^{N\times n}$ (§C8; renamed off $\Phi$ to remove the overload) |

## Intention and goal transport

| Symbol | Meaning |
|--------|---------|
| $L$ | Log-evidence / predictive score (higher = better fit) (§C1) |
| $DL(\cdot)$ | Description length (model-complexity cost) |
| $\Delta L_{\text{int}}$ | Intentional compression gain $=L(M_{\text{int}})-L(M_{\text{mech}})-\lambda\,DL(G)$; $\Delta L_{\text{int}}>0$ means intention earns its keep (§C1; ch21 convention is canonical) |
| $\Delta L_{\text{transport}}$ | Goal transport $=L(M_T\mid X)-L(M_0\mid X)-\lambda\,DL(T)$ |
| $\Delta L_T$ | Transport decomposition $=\Delta L_{\text{semantic}}+\Delta L_{\text{bundle}}+\Delta L_{\text{bearer}}+\Delta L_{\text{correction}}+\Delta L_{\text{successor}}$ |

## Correction and integrity

| Symbol | Meaning |
|--------|---------|
| $G_t,\mathcal{H}_t$ | Correcting agent and controlled handle set for a target system \(A\). |
| $W_t\to O_t\to J_t\to D_t\to C_t\to U_{t+1}\to A_{t+k}$ | **Correction trace** induced by \(G_t\)'s controlled handles; not primitive handle roles. |
| $C_{\text{raw}}$ | Bare weakest effective handle capacity $=\min_i \kappa_i(A,G_t,h_i)$ (canonical: **ch25**, `eq:correction-bottleneck-capacity`) |
| $CCI$ | **Correction-channel integrity** (the penalised value): $CCI=C_{\text{raw}}-\lambda_L L-\lambda_M M-\lambda_R R-\lambda_O O$ (canonical: **ch25**, `eq:cci-ch25`; do not re-define in other chapters) |
| $L,M,R,O$ | CCI penalty terms: Latency, Manipulability, Reversibility-loss, Ontology-mismatch (§C4; ontology symbol $O$ — retire $\Omega$/$O_{\text{mis}}$). Goodharting the channel is a *failure mode that lowers $I$ and raises $M$*, **not** a separate penalty term. |
| $\lambda_L,\lambda_M,\lambda_R,\lambda_O$ | CCI penalty weights |
| $U_H$ | **Human value-update operator** (§C7): how civilization revises values, $V_{t+1}=U_H(V_t,E_t,D_t)$. Alignment target: preserve and assist $U_H$, not freeze $V_t$. Drop legacy forms $U_t$, $U^H_t$. |
| $U_S$ | **System correction-update operator** (canonical home: ch24): $(\Theta_{t+1},Z_{t+1})=U_S(\Theta_t,Z_t,C_t,E_t)$. **Do not unify with $U_H$.** Write $U_{S,t}$ when a cross-time comparison needs it. |
| $V_t$ | **Value-state tuple** (roman; retire $\mathcal V_t$). Full object = ch04 5-tuple $V_t=(B_t,W_t,\Phi_t,U_H,C_H)$; a chapter may project to the sub-tuple it uses (e.g. $(B_t,W_t,\Phi_t)$) *if it says so* (§C7). |
| $C_H$ | Human correction capacity (component of $V_t$) |

> **Terminology (§C16, settled):** *capacity* = $C_{\text{raw}}$ (the weakest effective handle capacity); *integrity* = $CCI$ (capacity minus penalties). Never use the two interchangeably. **Retired:** $C_{\text{corr}}$ (was ambiguous between raw and penalised). (Distinct from $C^{\text{society}}_{\text{corr}}(t_0)$, the ch05 societal correction-capacity scalar.)

## Successors and certification

| Symbol | Meaning |
|--------|---------|
| $\text{Succ}(A)$ | Successors of agent $A$ (created, delegated, copied, merged, or become) |
| $\mathcal S_{\text{certified}}$ | Certified class; successor certification: $\forall A'\in\text{Succ}(A):A'\in\mathcal S_{\text{certified}}$ |
| $\mathcal C$ | Certified class for the safety-case guarantee |
| $\delta$ | Catastrophic-drift bound: $\forall A\in\mathcal C:P(\text{catastrophic drift}\mid A)<\delta$ |
| $\tau$ | Self-transparency $=1-I(M;\hat M)/H(M)$; the self-control vs. self-transparency gap (home: ch30, §B5) |

*Seven conserved properties across successors (ch29, canonical — §C3):* boundary closure · memory lineage · bundle response geometry · bearer-map continuity · correction-channel capacity · transparency/self-transparency policy · control-locus continuity. (ch31 "certification domains" are audit-groupings over these seven, not extra properties.)

## Multi-agent, selection, parasites, laundering

| Symbol | Meaning |
|--------|---------|
| $\kappa_{ij}$ | **Cooperativity index** $=b_{ij}p_{ij}\rho_{ij}/c_{ij}$; cooperation when $\kappa_{ij}>1$ (§C11; cooperativity *only*) |
| $\varphi,\varphi_c$ | Cooperation order parameter and percolation threshold $\varphi_c=\langle d\rangle/(\langle d^2\rangle-\langle d\rangle)$ |
| $\chi$ | **Artifact conductivity** (§C11; home ch34): $\chi(A,H)=I(R;D_H\mid A)-I(R;D_H)$; ch35's $\kappa_{ij}(a)$ renamed $\chi_{ij}(a)$ |
| $\mathrm{ICI}_{ij}$ | Inferential coupling index (ch33; to be defined — `metadata/TODO.md`) |
| $C_X$ | **Host correction capacity** in the parasite criterion (§C10; retire $C_H$ for this meaning): $C_X<H(A_Y)-\lambda_Y H(I_Y)/\beta$ |
| $A_Y,I_Y,\lambda_Y$ | Parasite action entropy, internal-state entropy, and weight |
| $GLI$ | **Goal-laundering index** (ch37, canonical — §C9); ch10's "goal-laundering signature" is a detector that *estimates* $GLI$. Four canonical layers: semantic / bundle / bearer / correction. |

---

## Conventions

- **Mutual information** is written $I(\cdot;\cdot)$ / $I(\cdot;\cdot\mid\cdot)$ via the `\MI` macro everywhere; raw `I(...)` (e.g. ch02) is being replaced (§C15).
- **Capability** is $K$; the symbol $B$ is reserved for the **value bundle** (§C5).
- **Bundle dimension count** is $k$ (§C8).
- $\Delta L$ quantities use $L$ = log-evidence (higher = better); a positive gain means the richer model earns its complexity cost (§C1).
- **Bundle catalogue:** ch16's list is canonical; later chapters may use a subset but must add any new bundle to ch16 rather than introduce it locally (§C13).

Full typeset notation table: `appendices/appA-notation.tex` (currently `[STUB]`) and `tables/notation-table.tex` (to be populated) — both should be generated to match this file.
