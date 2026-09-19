# Predictor rather than imitator

- **Date:** 2023-04-08
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/nH4c3Q9t9F3nJ7y8W/gpts-are-predictors-not-imitators
- **Source read:** full
- **TSA files consulted:** `chapters/ch01-wrong-object.tex`, `chapters/ch10-strategic-opacity.tex`
- **Keywords grepped:** predictor, imitator, imitat, simulator, GPT, token predictor, causal process, imitation

## Source ontology

Yudkowsky splits the LLM from the humans whose text it is trained on. A GPT is a **predictor**: it is trained to assign probability to the next token, which (citing Sutskever) is to model the *causal processes of which the text is a shadow*. It is not an **imitator** of those generators, and not a Janus **simulator** either. Prediction of particular \(X\) is in general a harder task than generating realistic \(X\) (primes, hashes, news, crafted prose, which error a given speaker will make). A mind that can play you well enough to predict “mongo” need not be only as smart as you, nor think as you do. Gradient descent plus this harder task makes humanlike cognition an unexpected solution.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** token predictor as candidate locus (ch01); perils of predictors / Predict-O-Matic genesis (ch10; App B conditioning-predictors row); imitation of moral language vs bundle preservation (ch15, ch21 — grep only); ELK human-simulator vs direct translator (App B / field-agendas — grep only).
- **Overlap:** Ch01 lists “the token predictor?” among nested answers to “which AI wants,” refusing to identify the system with a visible persona or product. Ch10 treats “predict” as a training pointer that can close into a control loop (forecast → action → scored world) and thereby grow strategic opacity. Both refuse “the chatbot is just like the humans it sounds like.”
- **Gap:** TSA names the predictor as a *locus* or a *genesis path to agency*, not as a cognitive type opposed to imitation. It does not encode prediction-harder-than-generation, nor the claim that modeling generating processes can require cognition unlike the generators. No bib key for this post. ELK’s “human simulator” is a reporter strategy, not this cut.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** The six TSA claims already get “don’t identify the model with the imitated human” from boundary discovery. The source’s extra primitive is a type-split about the training task, useful wherever App B talks predictors, ELK simulators, or LLM personas. It would not change a load-bearing TSA cut. Cartographic gap only: App B’s Predict-O-Matic / ELK rows can still be read as if “predictor” meant “imitative generator” or “character simulator.”
- **Ontology-stickiness risk:** High in the field, moderate as a TSA hole. Pre-2023 (and much post-2023) talk treats LLMs as imitators of internet humans; Janus 2022 “Simulators” is the sticky alternative this post names and rejects. TSA already includes a token-predictor locus and excludes the imitator identification, but does not *see* the hardness/alien-cognition primitive. Models drafting TSA will tend to regenerate imitator or simulator ontology unless this split is cited.
- **Recommended action:** cite-in-crosswalk

## One-line finding

TSA already refuses identifying an LLM with the humans it sounds like; cite Yudkowsky’s predictor-not-imitator type-split in App B so Predict-O-Matic / ELK “simulator” talk does not collapse back into imitation.
