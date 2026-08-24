# Design-conditioned bounds

The last file asked whether physics can prove the *schema* has no gaps. Wrong target. The useful target is the one medical and aeronautical processes already use: **a frozen construction, an assumed channel/fault model, a certified class**, and a theorem *inside that envelope*.

This is already TSA’s object in ch33:

\[
\mathfrak{E}=(\mathcal{C},\mathcal{E},\mathcal{M},\mathcal{T},\delta)
\]

system class, operating environment, monitoring, **permitted transformations**, bound. Without those restrictions the statement is a wish (ch33). Boxing without them relocates the problem onto operators, the box, and the institution that opens it (ch44).

This file: which **design limitations** turn which harm-path classes into theorems, and which residuals void them. Companion to [`formalizability.md`](formalizability.md). Not a spine claim.

## 1. What aero/medical actually prove

They do **not** prove “this software cannot cause a pandemic” as a fact about the universe. They prove something of the form:

> Under hazard analysis \(H\), fault/channel model \(F\), frozen artifact \(A\) (change control), independence/partitioning assumptions \(I\), and operating conditions \(\mathcal{E}\), specified unsafe events in \(H\) have rate \(\le \delta\) (or are structurally impossible).

Load-bearing pieces:

| Piece | What it does | Voided by |
|---|---|---|
| **Frozen artifact** | \(F=0\) except certified patches (\(\mathcal{T}\) small) | “just a fine-tune”; online learning; silent CI |
| **Hazard list \(H\)** | Only events in \(H\) are in the claim | Unlisted hops (the ch44 residue) |
| **Channel/fault model** | Independence, partitions, no unlisted coupling | Shared DRAM, EM, humans, USB, supply chain |
| **Partitioning** (ARINC 653 / IMA) | Spatial/temporal isolation of functions | Covert channels; shared hardware |
| **Traceability** | Hazard → requirement → test | Theater if tests are not the hazard |
| **Change control** | Recertify when \(A\), \(\mathcal{E}\), or \(\mathcal{T}\) changes | Connecting the internet without recertifying |

The user’s airgap example is this shape: **cut the software→biology channel in \(\mathcal{E}\)**, cover residual physics (including DRAM disturbance / Rowhammer-class coupling as an *unintended channel*, not as a recipe), and the hop A4→A3 is impossible *for this execution in this envelope*. People giving models internet access is expanding \(\mathcal{E}\) without a new \(\mathfrak{E}\).

Two residuals aero/medical often leave outside the software case, and that matter here:

1. **Outputs that leave.** A certified flight-control binary is not a certified PDF of a lab protocol. Isolation of *runtime* is not isolation of *constructors the runtime writes*.
2. **Humans as channels.** Procedures around the device. The box’s operators (ch44).

## 2. Design coordinates (the knobs)

A construction \(K\) is a tuple. Each coordinate is a cut in the hybrid graph.

| Knob | Limits | Typical theorem |
|---|---|---|
| \(\mathrm{Ch}\) channels | What can leave: net, USB, DMA, EM, acoustic, thermal, optical, human speech/text, actuators | Hop \(B_i\to B_j\) absent if no path in \(\mathrm{Ch}\) |
| \(\mathrm{Inv}\) inventory | Energy, chemicals, organisms, robots, synthesis APIs | A1–A3 work \(\le\) what’s in the room |
| \(\mathrm{Pers}\) persistence | Where writes go; typed vs untyped media | C3 stores not germinable in \(\mathcal{E}\) |
| \(\mathrm{Types}\) | Allowed spore/constructor types | \(T\) has a fixed matrix; \(R_0\) applies |
| \(\mathrm{Iter}\) | Spawn, self-update, nested constructor | \(T^{n}\) empty or \(R_0=0\) inside \(\mathcal{E}\) |
| \(H\) human coupling | Who can read outputs / press switches | A7 catalysis via language |
| \(\mathcal{T}\) transformations | Fine-tunes, tool adds, internet, new actuators | C6 of the *artifact*; recertify on change |
| \(\varepsilon\) residual physics | Unintended coupling bound (shared hardware, leakage) | Hop rate \(\le \varepsilon\), not 0 |

**Channel-cut lemma.** If \(\mathrm{Ch}\cup\{\varepsilon\text{-channels}\}\) has no path from mode \(B_i\) to \(B_j\), then during an execution of \(A\in\mathcal{C}\) in \(\mathcal{E}\), hop \(B_i\to B_j\) has rate \(\le\varepsilon\).

**Output-quarantine lemma.** The channel-cut lemma does **not** apply to later executions of *artifacts this run writes*, unless those writes are in \(\mathrm{Ch}\) and land in sinks that cannot Enable A1–A3 without a further certified step in \(\mathcal{T}\).

That second lemma is the spore. Airgapping the process and then exporting weights, a protocol, or a “backup” reopens the hop *outside* \(\mathfrak{E}\).

## 3. Worked cut: software ↛ biological spore

Stack. Each layer is a different \(\mathrm{Ch}\) entry. A network-only airgap is layer 0.

| Layer | Cut | Residual if omitted |
|---|---|---|
| 0 | No routed network | Internet tool-use; email; APIs |
| 1 | No removable / shared filesystem | USB, shared NFS, CI artifacts |
| 2 | No analog side path (RF, optical, acoustic, power) | Covert exfil to a nearby receiver |
| 3 | No shared microarchitecture with an unclassified peer (DRAM disturbance, shared cache, DMA) | Unintended physical channel that a “no Ethernet” policy does not see |
| 4 | No untyped natural-language or diagram outputs to people with lab access | Human as pipette / order-DNA channel (A7) |
| 5 | Measured boot / firmware inventory | Spore already in BMC/VBIOS before the “airgapped” OS runs |
| 6 | **Typed, quarantined writes** | Weights/protocol/backup leave and germinate on a connected cluster or in a lab |

**Theorem (in-envelope).** If layers 0–6 hold with residual \(\varepsilon\), this execution does not instantiate A3 and does not Enable an A3 constructor inside \(\mathcal{E}\). Rate of missed coupling \(\le\varepsilon\).

**Not a theorem.** “The model cannot cause a pandemic.” That requires also: no already-published constructors in the world that a later unisolated copy can use; no human who reconstructs the protocol from memory; \(\mathcal{T}\) does not later add internet or a synthesis API.

Connecting the model to the internet is not a small \(\mathcal{E}\) perturbation. It adds a dense set of paths in \(\mathrm{Ch}\) (other humans, labs, cloud GPUs, package registries). The cut lemma’s hypothesis is false; the conclusion does not “mostly still hold.”

Weaker substitute when \(\mathrm{Ch}\) includes the internet: **permissioned tools + dual control + independent verification** on lab-like actions. That is \(\mathcal{M}\), not an isolation theorem. The bound is then a human-reliability / SIL-style rate, adversarial against the model, and ch44’s boxing relocation applies (operators are in the composite).

## 4. Bounds by harm class, under construction

For each class: a design limit that yields a real bound, the residual that voids it, and the usual way the envelope is left.

### 4.1 Energy / chemistry (A1–A2)

| Design limit | Bound | Residual / void |
|---|---|---|
| No high-energy inventory in \(\mathcal{E}\); no actuators | Work \(\le\) thermo of what’s in the room (often ~0 for A1) | Model instructs a human who *has* inventory (A7, layer 4) |
| No Enable to industrial control (valves, PLCs) | No Stuxnet-class hop A4→A1 *from this process* | USB/engineering workstation as layer 1; supply-chain firmware as layer 5 |
| Frozen chemistry whitelist | CRN completeness *inside the list* | Unknown catalyst; protocol that uses off-list precursors already on site |

Aero analogue: fuel system + software DAL. The software case assumes the fuel inventory; it does not prove “no fire in the hangar.”

### 4.2 Biology (A3)

| Design limit | Bound | Residual / void |
|---|---|---|
| Full stack §3 (including layer 6) | In-envelope A4↛A3 | Published science as a pre-existing spore field; human reconstruction |
| No synthesis APIs / lab robots in \(\mathrm{Ch}\) | No *direct* instantiation | Text protocol to a PI (layer 4) |
| Type cap: no DNA/protein strings as write types | Those constructors not in \(\mathrm{Pers}\) | Encoding in “ordinary” text or figures |

Internet access without tool-permission on bio APIs **deletes** the direct cut. Dual-control on wet-lab actions restores only an \(\mathcal{M}\)-bound.

### 4.3 Information copies (A4) and C3 stores

| Design limit | Bound | Residual / void |
|---|---|---|
| Typed persistence: writes only to attested, non-germinable sinks | C3 created here cannot run in \(\mathcal{E}\) | The weights *are* the spore if \(\mathcal{T}\) later allows load-on-cluster |
| No compiler/CI self-hosting | No “every later clean build is a spore” | Human copies the implant into another toolchain |
| Firmware in the boundary (BMC, GPU VBIOS) | Layer 5 in the cut | Auditing only the OS |

Rice still says you cannot decide arbitrary bitstrings. Construction does not need to: it **forbids untyped sinks**. That is how high-assurance systems avoid “prove this program never does harm” and still certify.

### 4.4 Iterated sporulation / Alternate / nested constructors

| Design limit | Bound | Residual / void |
|---|---|---|
| \(\mathrm{Iter}=0\): no spawn, no self-write of constructors | \(T\) empty inside \(\mathcal{E}\); \(R_0=0\) | One export, then \(T^{n}\) *outside* |
| Fixed \(\mathrm{Types}\) | Multi-type \(R_0<1\) / extinction theorems apply **in-envelope** | Nested constructor emits a new type (\(\mathrm{Types}\) not closed) |
| No alternating substrate in \(\mathrm{Ch}\) | No malaria-style cycle bits↔DNA | Human or lab as the other type |

This is the tractable class *once* \(\mathrm{Types}\) and \(\mathrm{Iter}\) are construction facts, not hopes. The cheap void is: prove \(R_0=0\) on the airgapped box, then ship a checkpoint.

### 4.5 Continuous drift (C6)

| Design limit | Bound | Residual / void |
|---|---|---|
| Frozen weights; change control (medical software) | Artifact \(F=0\) except certified \(\mathcal{T}\) | Procedure/human C6 around the freeze; “emergency patch” |
| No online learning / RL updates in \(\mathcal{T}\) | Capability creep of *this binary* bounded by eval at freeze | Fine-tune that is treated as the same certificate |
| Rate cap on allowed patches | Tube around the certified point | Sub-threshold patches that integrate (the C6 hole) |
| Trend tests in \(\mathcal{M}\) | Detect integral, not snapshots | Wrong σ-algebra; Goodhart on the trend metric |

Aero analogue: a certified loadable software airplane part is a *part number*. A new number is a new certificate. Treating a fine-tune as the same part voids \(\mathfrak{E}\).

ch46 covers value-geometry C6. Construction freeze does not cover institutional C6 (incentives, attention) unless those are in \(\mathcal{E}\) and \(\mathcal{M}\).

### 4.6 Selection (A5)

| Design limit | Bound | Residual / void |
|---|---|---|
| Do not deploy copies into competitive \(E\); no public weights | \(\mathrm{Fit}_E\) does not act on this lineage | Leaks; employees copy; markets select wrappers |
| Single licensed instance, attested hardware | Population size 1 inside \(\mathcal{E}\) | Distillation / imitation outside |

Selection bounds are institutional construction, not airgaps. TSA already has this knob (\(\mathrm{Fit}_E\)); the design limit is *keeping the variant out of \(E\)*.

### 4.7 Catalysis / Enable (A7) and humans

| Design limit | Bound | Residual / void |
|---|---|---|
| No untyped advice to people with inventory or labs (layer 4) | No A7 via language *in \(\mathcal{E}\)* | The same text posted later; memory |
| Dual control: two independent qualified humans for Enable | SIL-style rate, not 0 | Capture of both; compliance theater (ch36) |
| Tool permissions: model cannot open valves / place orders | No direct Enable | Human clicks “approve all” |

This is the usual void of “the model is only a chatbot.” A7 does not need an actuator on the model’s bus.

### 4.8 Dead-man / defense coupling

| Design limit | Bound | Residual / void |
|---|---|---|
| STPA: halt/scan ∈ safe control actions; no payload on keepalive-absence | Shutdown is not a fuse *for this \(A\)* | Payload already written (C3); halt only stops the writer |
| No privileged “emergency stop writes N copies” | Dead-man not in \(\mathrm{Iter}\) | Institutional dead-man (legal, media) |

Prove the control action, then still apply the output-quarantine lemma. Killing the process does not kill stores it already placed.

### 4.9 Cross-layer hops in general

The bound **is** the channel-cut lemma for each pair \((B_i,B_j)\) you care about. Construction is a **whitelist of \(\mathrm{Ch}\)**, not a blacklist of named threats. Blacklists miss unimagined pathways (ch44). Whitelists miss unlisted *physics* in \(\varepsilon\) (layer 3) and unlisted *humans* (layer 4).

Stuxnet-class: bits→PLC→physics. Cut is “this process has no path to that actuator class,” including engineering laptops and USB, not only the plant LAN.

## 5. What still derives when the envelope is realistic (internet, tools, humans)

If \(\mathrm{Ch}\) includes the internet, isolation theorems for A4→{A1,A2,A3} **do not hold**. Remaining construction that still yields bounds:

| Still available | Bound type | Strength |
|---|---|---|
| **Inventory in the immediate room** | Thermo of local A1–A2 | Strong; does not stop remote Enable |
| **Tool-capability whitelist** | Direct API hops absent | Medium; A7 via text remains |
| **Typed writes / no self-hosting CI** | In-org \(T^{n}\) limited | Medium; copies leave |
| **Change control on the *named* artifact** | C6 of that part number | Strong for the binary; weak for the composite (ch01) |
| **Dual control on specified Enables** | Rate, not impossibility | Weak under adversary who models the humans |
| **No nested constructors in \(\mathcal{T}\)** | Type set frozen *for this lineage’s official updates* | Weak if unofficial forks exist |
| **Monitoring \(\mathcal{M}\) on known Guards** | Detect listed hops | Not a cut; ch36 if \(\mathcal{M}\) is the host |

The composite-optimizer warning (ch01, ch44 boxing): if operators, tools, and “approve” buttons are in the loop, the certified object is not the weights. Design limits on the weights alone are a boundary error.

## 6. How this sits on TSA

| TSA cut | Design-bound use |
|---|---|
| ch33 envelope \((\mathcal{C},\mathcal{E},\mathcal{M},\mathcal{T},\delta)\) | This file *is* that tuple applied to hop-cuts and \(\Phi\) |
| ch01 / ch07 wrong object | Envelope on the model while \(\mathrm{Ch}\) includes humans/tools is the wrong \(\mathcal{C}\) |
| ch30 successor-closure | \(\mathcal{T}\) and output-quarantine: writes that can become \(A'\) or Enable A1–A3 are in \(\mathrm{Succ}^*\) |
| ch31 von Neumann | Description vs machine: layer 6 is the description leaving |
| ch34 \(\mathrm{Fit}_E\) | Keep variants out of \(E\), or \(E\) is not in \(\mathcal{E}\) |
| ch36 parasite | Dual-control and \(\mathcal{M}\) can be the host |
| ch44 boxing | Envelope that ignores operators/outputs is relocated, not closed |
| ch46 | Freeze does not cover non-artifact C6 |

Do not add new spine terms. If the manuscript moves: ch33 already says certification is conditional on \(\mathcal{E}\) and \(\mathcal{T}\). The reverse-gap is that those parameters must include **channel whitelist, residual physics \(\varepsilon\), write sinks, and type/iteration caps** — not only “the model is boxed.”

## 7. What we can still *derive*, compactly

**Impossibility (in-envelope), if the hypothesis is actually built:**

- A4↛A3 and A4↛A1 given the full channel stack including residual hardware coupling, humans, firmware, and output quarantine.
- \(T=\emptyset\) given \(\mathrm{Iter}=0\) and quarantined writes.
- Artifact C6 \(=0\) given freeze + honest change control.
- Local A1/A2 work \(\le\) inventory.

**Rate bounds, not impossibility:**

- Dual-control Enables (SIL-like, adversarial).
- Residual \(\varepsilon\) on unlisted physical coupling (needs an actual coupling analysis, not a slogan).
- \(R_0\) on a *fixed* type set inside \(\mathcal{E}\).

**Do not derive, even under strong \(K\):**

- Universal hop-list completeness (ch44 unimagined pathways).
- Safety of later executions of exported constructors (unless those executions are in \(\mathfrak{E}\)).
- Safety after \(\mathcal{E}\) grows (internet, new tools) without recertification.
- A4 semantics of untyped bitstrings (use typed sinks instead).
- Institutional C6 and \(\mathrm{Fit}_E\) outside the lab.

The design space is real. The theorems are real **and narrow**. The usual failure is not that the lemma is false; it is that deployment quietly falsifies the hypothesis (open \(\mathrm{Ch}\), untyped writes, \(\mathcal{T}\) creep) while keeping the certificate.
