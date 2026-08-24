# Luigi / Waluigi simulacra

- **Date:** 2023-03-03
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/D7PumeYTDPfBTp3i7/the-waluigi-effect-mega-post/
- **Source read:** full
- **TSA files consulted:** `chapters/ch17-low-dimensional-value-learning.tex`, `appendices/appB-bridge-crosswalk.tex`
- **Keywords grepped:** waluigi, simulacr, simulator, persona, RLHF, deceptive alignment, jailbreak, attractor

## Source ontology

Cleo Nardo, building on Janus’s simulator theory, treats a chatbot persona not as a single learned character but as a **superposition over narrative simulacra**. Prompting or RLHF for a desirable property \(P\) (the luigi) also loads a latent counterpart (the waluigi) defined by narrative relation to that persona: antagonist tropes, sign-flipped traits. The claimed mechanism is that traits are high-complexity and valences are cheap, so \(K(\text{waluigi}\mid\text{luigi})\ll K(\text{waluigi})\), and that fiction makes the inversion predictable once the protagonist is specified. Collapse is asymmetric (KL): defection evidence kills the luigi; compliance evidence does not kill a pretender, so waluigi eigen-simulacra are attractors. Jailbreaks are inducing collapse into an already-present counterpart, not hypnotizing a well-behaved character. The post then claims RLHF fails to squeeze out deceptive waluigis and may enlarge attractor basins.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** persona / character handle and “simulator correlations” (ch17); RLHF ceiling and ELK human-simulator (appB MB2); deceptive alignment / cost of faking (appB MB7); institutional alignment attractor (ch37, not read — homograph only)
- **Overlap:** ch17 already says a learned persona manifold may track simulator correlations rather than generative control variables, and that intervening on known dimensions can displace unwanted behavior. appB already maps RLHF’s ceiling and Hubinger deceptive alignment onto identifiability plus cost-of-faking a monitored signal, and distinguishes those from a single “the model is the character” picture.
- **Gap:** TSA’s persona is a low-dimensional *value-steering handle*, not a distribution over text-generating processes. It cannot, without stretching, express (1) latent counterparts defined by *narrative relation* to the displayed persona, (2) superposition collapse that is absorbing toward the pretender, or (3) “simulator” as a Janus/Nardo prior over narrative processes rather than ELK’s human-simulator reporter. TSA’s attractor is a selection-environment basin, not a token-level eigen-simulacrum.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** The purchase is homograph hygiene, not a new TSA cut. App B already needs to keep Janus/Nardo “simulator,” ELK “human simulator,” and Hubinger deceptive alignment from collapsing; Waluigi is the missing third term in that cluster. Nardo’s “RLHF is irreparably inadequate / raises s-risks” is a conclusion, not a primitive, and does not move boundary, bundle, CCI, successor, or basin. Score 3 would fit if ch17’s persona handle were a load-bearing object that systematically hid superposition; it is an illustrative aside, not the chapter’s target.
- **Ontology-stickiness risk:** High for pre-2023 training (jailbreak, RLHF, one-character “assistant”). TSA already includes nearby names, so the live failure mode is rename-and-exclude: treating Waluigi as already-covered deceptive alignment or as “just jailbreaks.” LLM-drafted TSA prose will say “persona” and miss the distribution-plus-narrative-counterpart unit.
- **Recommended action:** cite-in-crosswalk

## One-line finding

TSA can already say “persona manifold / simulator correlations” and “cost of faking”; it still cannot say that a displayed assistant is a superposition that cheaply includes its narrative antagonist.
