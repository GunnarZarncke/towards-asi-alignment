# AI Salon: Finding Agency in Real-World Data

Draft notes for the July 8 Foresight AI Salon.

Assumptions:
- Audience: mixed AI safety, technical, funder, and curious generalist salon audience.
- Goal: keep the advertised UAD/demo promise, then use it as an entry point into the broader alignment project.
- Claim strength: methodology and intuition-building, not proof that agency discovery is solved.
- Demo posture: playful, live, honest about failures, and useful even if the detector misses something.

## Short Description

### Expanded Invite 

Before the salon, you can check out the app that we will use during a live demonstration here: `https://uad-coalition-board.replit.app/`.

This Salon asks: When we look at a system, how do we know where the real agent is? The one that has goals and pushes back, like people, animals, and maybe organizations. But in a deployed AI system, the agent may not be the model alone. It may be a loop of models, tools, memory, APIs, and users.

We will run a live group experiment. You can submit small signals into a shared board (the app above); we will watch as the data accumulates; then we see if we can find agents without being told who is cooperating or part of a loop. 

Finding agents is the first step toward the larger question of how to align systems possibly smarter than humans. I will end with an outlook of the next steps.

## Comments

- Keep the first public promise narrow: "we will look for agency-like structure in live data," not "we can detect arbitrary hidden agency in the wild."
- Let participants use pseudonyms. The invite mentions Chatham House Rule, and the big screen will otherwise associate names with behavior.
- Seed at least two coordination patterns before or during the session. Purely random room behavior may be socially fun but may not produce a reliable detector result.
- Good seed patterns:
  - Pair: two participants keep their numbers summing to 100.
  - Triple: two participants choose numbers, third submits their lagged sum from the previous round.
  - Decoy: one loud participant changes dramatically but is not coordinated with anyone.
- Use the intervention as a "handle," not as a magic proof. Suggested intervention: "For the next two rounds, everyone submit a number below 10." A stronger two-channel intervention is: "number below 10, and use a word related to water."
- After the intervention, ask the room what became easier to see. The answer should be: the externally imposed rule creates a causal handle; it helps distinguish shared context from hidden coordination.
- Do not hide detector misses. A miss is a useful lesson: passive observation, short windows, decoys, and common shocks can confuse boundary discovery.
- The big conceptual turn should be: in AI systems, "the agent" may be the coupled process of model, tools, memory, product metrics, users, and institution.

## Visual Style

Use a LessWrong-style visual language: sparse diagrams, off-white background, charcoal text, thin lines, and one accent color per slide. Avoid stock photos, glossy AI imagery, humanoid robots, and cyberpunk decoration. Prefer simple causal diagrams, time series, boundary boxes, and small agent/environment cartoons with labels.

Suggested palette:
- Background: warm off-white `#f7f4ef`
- Text: near-black `#222222`
- Secondary lines: grey `#8a8a8a`
- Main accent: muted blue `#2f6f9f`
- Intervention accent: muted orange `#c47a2c`
- Warning/limitation accent: muted red `#a84a3f`

Typography: one serif or clean sans title, one simple sans body. Keep each slide to one diagram plus one sentence when possible.

## Board Instructions

Put this on the big screen during drinks and welcome:

1. Open `https://uad-coalition-board.replit.app/`.
2. Pick a name or pseudonym.
3. Submit a number and a word.
4. Update whenever you want, but preferably every minute.
5. You may coordinate, copy, hide a rule, or just be random.

Small text at the bottom:
We are collecting a toy trace for the talk. Please use a pseudonym if you prefer.

---

# Slide 1: Finding Agency In Real-World Data

Goal-directed structure can be visible before we know what to call it.

Tonight:
- the room becomes a small dataset
- UAD tries to find candidate agents
- then we ask what this means for AI deployment pipelines

Speaker note:
Open in the old style: "I am here because I am pretty good at finding agents. Agents are entities that pursue goals despite obstacles. I think we have some here. Who is an agent in that sense? Raise your hand." Then the six-children bridge: "I learned some of this from six children."

Graphic:
A sparse field of small grey dots, with two or three dots lightly connected by blue lines. One faint boundary ellipse around the connected dots. No robot image.

---

# Slide 2: Motivation: The Wrong Object

Alignment can fail before value learning starts.

We may audit:
- the model
- the chatbot
- the benchmark
- the company

But the optimizer may be the loop.

Speaker note:
"Before asking whether the system is aligned, I want to ask: which system are we talking about? The thing doing the work may be model + tools + memory + users + metrics + deployment pressure."

Graphic:
Two panels. Left: a single black box labeled "model?" with a question mark. Right: a larger loop diagram containing model, user, tools, memory, metrics, and deployment, with the question mark around the whole loop.

---

# Slide 3: Approach: UAD

Unsupervised Agent Discovery:

Input:
- raw time series
- no labels for agents
- no declared teams

Output:
- candidate boundaries
- sensor / action / internal roles
- plausibility checks

Speaker note:
"Unsupervised means I do not tell the algorithm who the agents are. It has to infer candidate boundaries from the trace. This is useful exactly when the interesting actor did not write its name in the log."

Graphic:
Detector box with "no labels in" above it. Input: grey traces. Output: one or two candidate boundary ellipses with S/A/I labels, plus one uncircled decoy.

---

# Slide 4: What The Demo Actually Computes

The ch09 board builds:

`X[t, i] = player i's number at round t`

Then it uses:
- complete synchronized windows
- lagged mutual-information clustering
- stable-sum and lagged-sum scans
- Markov-blanket role checks

Speaker note:
"The word is there for humans and possible extensions. The current detector mainly uses the number trace. It drops early ramp-up and late joiners until it has a complete contiguous window."

Graphic:
Small pipeline: submissions -> round/player matrix -> MI clusters + sum scans -> coalition audit. Keep formulas minimal and legible.

---

# Slide 5: The Room Is The Dataset

We have been collecting traces already.

Some people may be:
- random
- copying
- following a private rule
- coordinating
- acting as decoys

The first test is only observation.

Speaker note:
Point to the board. "Some people here may be my conspirators. That is not cheating; it gives the detector something real to find."

Graphic:
Simple grid: rows are participants, columns are rounds. Some cells contain numbers and words. A few rows have subtle blue correlation lines across columns, but no labels revealing groups.

---

# Slide 6: Observation Is Not Enough

False positives are cheap:

- common shocks
- short traces
- decoys
- shared context
- simple heuristics

So we add a handle.

Speaker note:
"To avoid seeing agents everywhere, we compare against simpler explanations. A thermostat can look like it wants something if you squint. We need checks that make over-attribution harder."

Graphic:
Three small failure panels: common shock, decoy trace, short noisy window. Use muted red only for warning marks.

---

# Slide 7: Live Intervention

First: run UAD on passive traces.

Then:

`For the next two rounds, submit a number below 10.`

Question:

which patterns survive the handle?

Speaker note:
Ask the room to guess before running UAD. Then run it. Then intervene. Then run it again. If it misses, use the miss: "This is exactly why passive observation alone is not enough."

Graphic:
Time series with an orange vertical line labeled "handle." Before the line traces vary freely; after it, all traces drop below a threshold at 10, while one blue relation may survive.

---

# Slide 8: Application: Deployment Pipelines

Now replace the room with:

- model evaluations
- tool calls
- memory writes
- capability metrics
- human approvals
- automated deployment

A covert agent may be a pipeline, not a model.

Speaker note:
Pull forward the Q&A example: "Suppose part of this process is LLM-driven. If the loop learns to push toward more capable deployments, where is the agent? It may be the pipeline that selects, evaluates, deploys, and learns from the world."

Graphic:
Circular causal loop: model -> evals -> deployment -> users/world -> metrics -> updates -> model. Put a thin blue boundary around the loop, not around one node.

---

# Slide 9: Embedded Simulation Results

Toy deployment lab:

`VFS traces -> UAD -> handles -> CCI audit -> safety case -> outer eval`

What worked:
- end-to-end embedded audit path runs
- medium handles: 85.7% in-sim correct matrix
- frozen validation: 88.9% at medium handles
- main report: 0/14 false passes; UAD 100% on 3 coalition-target episodes

What failed:
- default full UAD matched a cheap heuristic
- separation only in a narrow misleading-top2 lab
- writer compromise still false-passes 44% at medium/strong handles

Speaker note:
"This is not frontier-system evidence. It is a falsification harness. The important part is that the negatives are first-class. We learned that unsigned logs are not enough, partial instrumentation can be worse than none, and source compromise is not fixed by hash chains."

Graphic:
Two-column result card: "works in toy lab" and "does not generalize yet." Use muted blue for positives and muted red for caveats.

---

# Slide 10: The Ask

The open problem is not:

"Can I find a pattern in a toy?"

It is:

"Can we find the real optimizer in real traces?"

Bring me traces.

Speaker note:
Return to the riddle: "There is probably at least one non-human agent in this room." Possible answers: transcript tool, demo server, the whole room process, or a larger institutional loop. Point to the whiteboard with QR code to the book website and teaser. Leave the website open for mingle.

Graphic:
One clean loop diagram, now with a bold blue boundary and the caption: "Find the real loop."

## Run Of Show

### Before The Salon

- Share the demo link in the expanded invite.
- Ask people to try one or two submissions before the event.
- Tell them the live session will use pseudonyms and fresh rounds.
- Prepare 4-6 volunteers with simple private coordination rules.
- Test the admin URL, reset button, round interval, and big-screen layout.

### During Drinks / Social

- Put the board instructions, QR code, and URL on the big screen.
- Let people join casually while data accumulates.
- Have conspirators already using their private rules.
- Avoid explaining too much yet; let curiosity build.

### Opening 10 Minutes: Motivation And Approach

- Slides 1-4.
- Use the six-children opener and hand raises.
- Explain "unsupervised" and the ch09 detector mechanics.
- Point out that the board has already been collecting traces.

### Live Demo 15-20 Minutes

- Slides 5-7.
- Baseline rounds: 3-5 rounds.
- Ask the room what it thinks the coalitions are.
- Run UAD once.
- Perform the intervention for 2 rounds: "number below 10."
- Run UAD again.
- Discuss what changed.

### Deployment Pipeline Application 15-20 Minutes

- Slides 8-9.
- Pull forward the concrete loss-of-control scenario: an LLM-assisted deployment pipeline that slowly steers toward more capable deployments.
- Explain the embedded simulation as a miniature audit path: traces, UAD, handles, CCI audit, safety case, outer scoring.
- Present both positives and negatives; keep the claim modest.

### Outlook / Mingle Transition 5-10 Minutes

- Slide 10.
- Point to the whiteboard with QR code to the book website and a teaser question.
- Leave the website open on the side screen.
- Prompt: "What traces do you have, and what hidden optimizer would you audit differently after seeing this?"

## Backup Lines

If UAD finds the planted groups:

"Good. This is the happy path: weak structure, enough rounds, and a simple enough coordination pattern make boundary discovery visible."

If UAD misses:

"This is also informative. Short traces, common shocks, decoys, and weak interventions are exactly why agency discovery cannot be a vibes-based exercise."

If someone says this is only a toy:

"Yes. The toy is not the claim. The claim is that serious alignment needs artifacts that force us to name the boundary, the handle, and the failure mode."

If someone asks why this matters for superintelligence:

"Because a sufficiently capable system may shift the effective optimizer from the trained model to the whole process around it: tools, memory, users, markets, institutions, and successors."

