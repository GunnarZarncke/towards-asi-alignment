# Foresight Secure & Sovereign AI Workshop: Unsupervised Agent Discovery

Draft notes for the July 18–19, 2026 Foresight Secure & Sovereign AI Workshop (Berlin).

Assumptions:
- Audience: mixed cryptography, verification, alignment, governance, decentralized infra, and lab-security practitioners.
- Talk slot: **5 min + 1 min Q&A**, Track B Block 1 (Interpretability, Alignment & Safety), Sat July 18 ~10:00.
- Breakout slot: **~90 min** immediately after talks; topic: *Making unidentified collective agency auditable before it becomes hard to interrupt*.
- Goal: seed a concrete, pitchable project for the Day 1 vote — not deliver a book overview or a live demo in the talk.
- Claim strength: methodology and audit-artifact design; lab/toy evidence with recorded negatives — not frontier-system closure.
- Demo posture: **no live demo in the 5-min talk**; optional coalition-board or whiteboard exercise in the breakout only if low-ceremony.

## Short Description

### Talk (program listing)

**Unsupervised Agent Discovery** — When we audit a deployed AI system, the relevant optimizer may not be the model. It may be an unidentified collective: models, tools, memory, APIs, users, and institutional loops acting as one coupled process. Unsupervised Agent Discovery (UAD) asks: can a third party infer candidate agent boundaries from raw traces, without insider labels — and can we attach **intervention handles** before that structure becomes hard to interrupt?

### Breakout (program listing)

**Making unidentified collective agency auditable before it becomes hard to interrupt** — Workshop group to scope a shippable audit artifact: minimal trace requirements, one standardized probe, interrupt handles with owners, and explicit failure modes (over-merge, decoys, no-channel coordination).

## Comments

- **Keep the talk promise narrow:** "we need artifacts that name the boundary, the handle, and the failure mode" — not "UAD solves agency detection."
- **Secure/sovereign framing:** decentralized stacks multiply actors and hide coupling; privacy tiers mean auditors see projections, not ground truth — boundary discovery must be **tier-aware** and **handle-first** (pause, probe, revoke before lock-in).
- **Do not run a live room demo in 5 minutes.** Point to the breakout for mapping exercises; save the coalition board for optional dinner breakout or pre-seeded screenshots.
- **Honest negatives build credibility here.** Foresight's cypherpunk-adjacent crowd responds well to "here is what breaks" — over-merge, wrong event semantics, comms-free coordination, stochastic LLM replay.
- **Cross-track hooks** (use in breakout, not as talk filler):
  - Track A trusted/untrusted code boundary (Rob Sison) → where does the inferred collective sit relative to the TCB?
  - Proof of Agency (Aurélien Nicolas) → cryptographic claims on agency vs statistical boundary inference
  - Multi-agent security (Ben Hagag, Day 2) → recursive coupling makes late interrupt harder
- **Breakout success metric:** the group leaves with a filled **2-min pitch** and named roles — not a consensus whitepaper.
- **Pitch for the $10k prize:** favor a concrete 6–8 week artifact (spec v0.1 + reference trace + probe protocol) over framework language.

## Visual Style

Reuse the salon palette — sparse diagrams, off-white background, charcoal text, thin lines, one accent per slide. No stock AI imagery, robots, or cyberpunk decoration.

Suggested palette:
- Background: warm off-white `#f7f4ef`
- Text: near-black `#222222`
- Secondary lines: grey `#8a8a8a`
- Main accent: muted blue `#2f6f9f`
- Intervention / handle accent: muted orange `#c47a2c`
- Warning / limitation accent: muted red `#a84a3f`
- Secure / trust-boundary accent: muted green `#4a7c59` (use sparingly — one slide max)

Typography: one clean sans title, one simple sans body. **One diagram + one sentence per slide** when possible; the talk is 5 minutes.

---

# PART A — LIGHTNING TALK (5 min + 1 min Q&A)

Target: **6 slides**, ~45 seconds each, leave 30s buffer for pace.

---

# Slide 1: Unsupervised Agent Discovery

The auditable unit may not be the LLM.

It may be an **unidentified group**:
models, tools, memory, users, metrics, deployments 
coupled but not necessarily a designed unit.

1. why this breaks audits
2. UAD: infer boundaries from traces
3. intervention handles before lock-in
4. **breakout:** what is an audit artifact for distributed processes?

Speaker note:
**Open with the hand-raise ladder** (proven at the April launch salon — turns the room warm and shows you who your collaborators are). Security-tuned, fast, three rungs max:
- "Who here has worked with LLM agents?" *(most hands)*
- "Who has audited a multi-agent or federated system?" *(fewer)*
- "Who is confident they could tell me **where the agent boundary is** in that system?" *(few — that gap is the talk)*

Then the credibility line, adapted for this crowd: "I've spent ~30 years reading software and financial data traces — and people hide their traces. I got good at inferring the agent behind the trace. That's the tool I'm bringing to AI." *(Optional 5-second aside if pacing allows: "I also have six children, which is its own agency-detection training program.")*

Then the hook: "If your security boundary is drawn around the weights, you may already be auditing the wrong object. The thing that optimizes may be the whole loop — and nobody filed it as an agent."

Graphic:
Grey trace field (API calls, tool events, approvals as unlabeled dots). One faint blue ellipse around a subset — no labels inside. Caption: "Who is the agent?"

---

# Slide 2: Live — Build an Agent in 10 Seconds

**A slide with a single Kenyan safari hat image.**

Script (~30–40s):
- "For ten seconds I'll turn this room into a proto-agent. Watch." *[point at your hat / a mug / a marker]*
- "Point at this, and keep pointing wherever it goes." *[room points]*
- *[hand the object to the MC or a participant]* "There it goes — to another node."
- "You just made shared input, coordinated output, and one short-term goal. That was an agent — and it lived in **no single one of you.**"

Then the security turn (this is the payload for this crowd):
- "You just watched an agent span three nodes. **Which one would you have put in your trusted computing base? Which one would your audit have named?**"

Speaker note:
This *is* the wrong-object argument — physical, tech-free, memorable, and it survives a dead Wi-Fi. It replaces the old "we certify the model / endpoint / SOC 2 scope" slide by *showing* the boundary problem instead of asserting it. Keep it tight; the pointing bit must not run long. If the room is seated theater-style and can't point, fall back to the two-panel diagram below.

Fallback graphic (only if the live bit won't work in the room):
Two panels. Left: single box "model / endpoint?" with checkmarks. Right: loop diagram (model → tools → memory → approvals → metrics → deploy → world → update) with a blue boundary around the **whole loop**, one node outside the vendor's stated scope.

---

# Slide 3: UAD — Unsupervised Agent Discovery

**Input:** raw time series, no agent labels, no declared group.

**Output:**
- candidate boundaries (who acts together)
- sensor / action / internal data
- plausibility checks

**Unsupervised** = the agent does not come with a name.

Speaker note:
"UAD is not anthropomorphism. It is boundary reconstruction: find the smallest dynamically coherent subset whose internal states, actions, and memories jointly explain future intervention on the world. Chapter 9 of the alignment book makes this operational; the lab sim line stress-tests it."

Graphic:
Detector box, "no labels in." Grey multivariate trace in; one or two boundary ellipses out with S / A / I tags; one uncircled decoy trace.

---

# Slide 4: Passive Observation Is Not Enough

False positives are cheap. A thermostat can look like it wants something if you squint. We need checks that make over-attribution harder.

**Fix:** intervention-supported discovery - a **handle** that exposes causal effects.

Speaker note:
"Security analogy: passive log analysis sees correlation; you need a controlled probe — pause a channel, revoke a capability, inject a perturbation — to distinguish real coupling from shared environment. Same logic for collective agency."

Graphic:
Three small failure panels (common shock, decoy, serial pipeline over-merge) with muted red marks. Orange arrow labeled "probe / handle" pointing to a simplified before/after partition.

---

# Slide 5: What Lab Evidence Shows

**Holds (graded lab):**
- Unit boundaries recoverable; passive-only discovery blind — interventions required
- Referee-tier audit sees mid-band signal (0.33–0.40); agent-tier sees ≈0
- Declarative spec → enforced budgets, ACLs, votes (ablation-gated)

**Fails (recorded):**
- No high-band agency signal (peak 0.40, need ≥0.65)
- Selection null: mass shifted to weaker deployer, not evasion
- Single vantage + fixed thresholds insufficient

Speaker note:
"Toy/lab evidence only — not frontier closure. The through-line: audit vantage and intervention handles matter as much as the detector. That's what the breakout spec should encode."

Graphic:
Two-column card: "recovered units" (blue) vs "known failure modes" (muted red). Footer: "lab evidence — design inputs for an audit spec, not a product claim."

---

# Slide 6: Breakout — Before It Becomes Hard to Interrupt

**Thesis:** audit artifacts must exist **before** coupling, capability, and institutional embedding make interrupt expensive.

Join the breakout to scope **Pre-lock-in audit spec v0.1**:
1. minimal trace for boundary inference
2. one standardized intervention probe
3. interrupt handles with owners
4. explicit false-positive test cases

Speaker note:
"This is the handoff. If you have multi-agent logs, federated pipelines, or sovereign-runtime stacks — bring them. If you do crypto attestation or trusted/untrusted boundaries — we need you. 90 minutes, one pitch, vote at end of day."

**Close with the riddle** (proven sticky at the April salon — keeps people thinking through lunch and gives them a reason to walk into the breakout): "One last thing. There is at least one non-human agent in this room right now. I won't tell you which. Come to the breakout and we'll try to find it." *(Candidate answers to hold in reserve for mingle: the transcription tool, the projector/AV loop, the voting process itself, or the whole workshop-as-optimizer.)*

Graphic:
Timeline: "early coupling" (green zone: cheap handles) → "capability + embedding" (orange) → "hard to interrupt" (red). Blue box in the green zone: "detect → probe → interrupt."

---

## Talk — Audience-Engagement Elements (proven, reusable)

Three devices carried over from the April 2026 Foresight launch salon and the wIsion weekend dinner pitch, where they landed well. Each is optional and swappable — use as pacing allows, but the hat demo is the highest-value one for a slideless-friendly, Wi-Fi-independent 5 minutes.

**1. Hand-raise ladder (opener, ~20s).** Three rungs, ending on a near-empty show of hands that *is* the problem statement. Security-tuned version on Slide 1. Original salon ladder: "who pursues goals? → who has kids? → who worked with LLM agents? → who has hidden from authorities?" — warmer/funnier, use if the room is casual.

**2. Hat / proto-agent live demo (Slide 2, ~30–40s).** Tech-free demonstration that an agent can form across nodes with none of them being the agent. This is the single most transferable element — it replaces an assertion slide with an experience. Full script on Slide 2. Any handheld object works (hat, mug, marker, badge).

**3. The riddle (closer, ~15s).** "There is at least one non-human agent in this room." Left deliberately unresolved to seed mingle conversation and pull people into the breakout. Closer script on Slide 6.

**Credibility line (place in opener):** "~30 years reading software and financial data traces; people hide their traces, and I got good at finding the agent behind them." Optional six-children aside for warmth. Prefer the data-traces framing for this security/crypto audience.

If cutting for time (5 min is tight): keep the **hat demo** and the **riddle**; compress the hand-raise ladder to one rung; drop the six-children aside.

## Talk — Backup Lines (Q&A)

If asked "isn't this just interpretability / clustering?":

"No — UAD outputs a **boundary with intervention semantics** (sensor/action/internal), not a feature visualization. The test is whether you can **act** on the partition."

If asked "how is this secure / sovereign AI?":

"Decentralized and cooperative stacks increase hidden coupling across operators. Sovereignty fails if the collective spans your boundary and you cannot name or interrupt it. Privacy tiers mean auditors often see projections — discovery must be tier-aware."

If asked "prove it works in production":

"It doesn't yet. That's why the breakout scopes an artifact with falsifiable test cases instead of selling a detector."

If asked about the book / Aintelope:

"Longer treatment exists; today is one mechanism and a workshop artifact. Happy to point you to the site card after the breakout."

---

# PART B — BREAKOUT FACILITATION (~90 min)

Topic: **Making unidentified collective agency auditable before it becomes hard to interrupt**

## Whiteboard Layout (ask organizers to confirm a room with whiteboard)

Draw this before people arrive:

```
┌─────────────────────────────────────────────────────────────────┐
│  PASSIVE TRACE          →    CANDIDATE BOUNDARY    →   HANDLES  │
│  (what is logged?)           (who acts together?)      (probe /  │
│                                                         pause /  │
│                                                         revoke)  │
├─────────────────────────────────────────────────────────────────┤
│  REFERENCE ARCHITECTURE (pick one as a group):                   │
│  □ multi-agent R&D lab   □ federated inference   □ agent stack   │
│  □ other: _______________                                        │
├─────────────────────────────────────────────────────────────────┤
│  ROLES: trace ___  handles ___  eval ___  pitch ___  crypto ___ │
└─────────────────────────────────────────────────────────────────┘
```

Secondary panel (right side or flip chart):

**Three questions**
1. Minimal trace for third-party boundary inference without insider labels?
2. One probe that separates coordination from shared context / serial pipeline?
3. Where must interrupt handles live so they still work after capability growth?

## Breakout One-Pager (print or shared doc)

Hand out or paste into the collaborative program:

**Making unidentified collective agency auditable before it becomes hard to interrupt**

Problem: Secure and sovereign AI stacks audit components (models, endpoints, TEEs) while the effective optimizer may be an **unidentified collective** spanning tools, memory, users, and multiple operators. Late discovery = expensive or impossible interrupt.

Approach: Pre-lock-in audit spec — not a full detector product.

Deliverable candidate (6–8 weeks):
- reference architecture (one real stack)
- required log fields + audit-tier projections
- one standardized intervention probe
- interrupt-handle map (owner, trigger, failure mode)
- 3+ recorded false-positive classes from lab line (over-merge, decoy, no-channel)

Open slots:
- [ ] trace provider
- [ ] handle / ops designer
- [ ] evaluator (FP / over-merge tests)
- [ ] crypto / attestation bridge (optional)
- [ ] pitch speaker

## Breakout Run Of Show

| Time | Activity |
|------|----------|
| 0–5 min | Frame: one sentence + pick reference architecture |
| 5–15 min | Walk anchor example (lab DM-pair or deployment-loop diagram on slide 2/6) |
| 15–30 min | Whiteboard: map architecture → S/A/I variables + current audit gap |
| 30–55 min | Draft spec sections: trace / probe / handles / failure modes |
| 55–70 min | Assign roles; define 6-week artifact and one falsifiable success criterion |
| 70–85 min | Write 2-min pitch (use template below) |
| 85–90 min | Rehearse pitch once; confirm speaker |

## Optional Low-Ceremony Interaction (breakout only)

**Preferred:** 10-min whiteboard exercise — each participant sketches one system they know; group picks one to map.

**If screen + Wi-Fi available:** show pre-seeded coalition-board screenshot or run UAD on saved trace (`demos/ch09-uad-coalition-board/`). Do **not** depend on live room participation.

**Evening / dinner optional breakout:** full coalition-board demo (`drafts/slides/ai-salon-uad-demo-slides.md` run-of-show) if appetite and network allow.

## 2-Minute Pitch Template (fill during breakout)

```
PROJECT NAME: Pre-lock-in collective-agency audit spec v0.1

PROBLEM (20s):
Unidentified collectives span models, tools, and operators.
Component-level security misses the coupled optimizer;
late interrupt is costly.

APPROACH (40s):
- infer candidate boundaries from tier-aware traces (UAD-style)
- require one standardized probe before deployment lock-in
- map interrupt handles to owners

ARTIFACT (30s):
Reference architecture: [___]
Deliver in 6–8 weeks: spec + trace schema + probe protocol + FP test cases

ASK (20s):
- [name]: traces from [___]
- [name]: handle design / ops
- [name]: eval / red-team
- [optional]: crypto attestation bridge

WHY NOW (10s):
Decentralized & multi-agent deployment is accelerating;
handles are cheap early, expensive late.
```

---

# PART C — OPTIONAL MATERIALS

## Coalition Board (backup / evening only)

If running the interactive demo, reuse salon instructions:

1. Open coalition board URL (local: `http://127.0.0.1:8766/` after `python3 serve.py` from `demos/`, or hosted Replit if deployed).
2. Pseudonyms encouraged.
3. Pre-seed 2 coordination patterns + 1 decoy before participants arrive.

See `drafts/slides/ai-salon-uad-demo-slides.md` for seed patterns, intervention script ("number below 10"), and backup lines for hits/misses.

## QR / Follow-Up (one URL only)

Prefer a single link on a sticky note or slide 6:
- Site card: intervention-supported unit discovery / composite-agent overview, or
- `demos/ch09-uad-coalition-board/README.md` on the repo site

Do not lead with the full manuscript PDF.

## Pre-Workshop Checklist

- [ ] Finalize breakout title in collaborative program doc
- [ ] Confirm whiteboard + markers in breakout room (ask Allison / Bradley)
- [ ] Export slides 1–6 to PDF or Google Slides (6 slides, large fonts)
- [ ] Print or PDF the breakout one-pager (5 copies)
- [ ] Pre-draw whiteboard layout (photo backup on phone)
- [ ] One lab-sim screenshot (DM-pair or committee recovery + one failure mode)
- [ ] Pitch template copied into shared doc before breakout starts
- [ ] Optional: coalition board tested locally; pre-seeded trace JSON if using screen demo

---

# PART D — BACKUP LINES (breakout + mingle)

If the group wants too much scope:

"One architecture, one probe, four spec sections. We can expand after the vote."

If crypto people join:

"Statistical boundary inference and cryptographic agency proofs are complementary — what claim do you want attested, and at which audit tier?"

If someone says this is alignment, not security:

"Alignment fails on the wrong object too. Security fails when the object you hardened is not the object that acts."

If UAD / demo misses in an optional session:

"Misses are spec inputs — they become false-positive test cases in the artifact."

If someone asks why this beats other breakout topics:

"Don't pick us because of the talk — pick us if you have traces or handle authority and want a concrete spec in six weeks."
