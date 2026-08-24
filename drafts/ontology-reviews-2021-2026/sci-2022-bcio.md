# Behaviour Change Intervention Ontology (BCIO/BCTO)

- **Date:** 2022–2023
- **Field:** Psychology / behavioural science
- **Source:** https://www.nationalacademies.org/read/26755/chapter/5
- **Source read:** NAP digest chapter (full); Marques et al. 2023 BCTO paper (abstract + intro)
- **TSA files consulted:** `appendices/appB-bridge-crosswalk.tex`, `chapters/ch25-correction-causal-channel.tex`
- **Keywords grepped:** fidelity; engagement; intervention; behaviour change; mechanism of action; ontology; technique; delivery

## Source ontology

The Human Behaviour-Change Project’s Behaviour Change Intervention Ontology (BCIO) makes a *behaviour-change intervention* a formally specified OWL object, not a prose package. The 2022 National Academies digest lists twelve central entities (intervention, content, delivery, mechanism of action, exposure, reach, engagement, context, population, setting, behaviour, outcome) plus related attributes (source, mode, schedule, dose, fidelity, adherence), linked by relations such as has-part, subclass-of, has-attribute, evaluates, has-output. Later BCIO work expands an upper level to 42 entities. Nested inside it, the 2023 Behaviour Change Technique Ontology (BCTO) replaces the 2013 BCTTv1 taxonomy with 281 computer-readable “active ingredient” classes in 20 groups. The cut it replaces is incompatible trial reporting: heterogeneous labels that block evidence synthesis, querying, and “what works, for whom, why.”

## TSA coverage

- **Status:** orthogonal
- **Closest TSA terms/chapters:** App B intervention coverage map (AI-safety *clusters*, not BCI parts); CCI audit profile in ch25 (observability, explanation fidelity, authority, reach, latency, manipulation, persistence); Pearl-style interventional handles for boundary discovery; “engagement” as a selection proxy (chs 09, 14, 34). App B already files “Behavioral / psychological framings” as exclude-by-reference.
- **Overlap:** Both talk about “interventions,” “fidelity,” “engagement,” and “mechanisms.” TSA’s nearby objects are different types: an approach-catalog plus a correction-channel measurement profile, not an OWL decomposition of public-health programmes into technique/source/mode/schedule/style/context.
- **Gap:** TSA cannot, and does not try to, express BCIO’s typed BCI (content ≠ delivery ≠ mechanism ≠ engagement ≠ fidelity ≠ outcome) or BCTO’s 281 techniques. That is not a missing alignment primitive. Restating alignment as “specify target behaviour, BCTs, mode, and fidelity” still leaves boundary, value-bundle, CCI-under-capture, successor, and selection untouched (hostile-test fail).

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** BCIO is a real, machine-readable ontology, but for evidence synthesis of human behaviour-change programmes. Absorbing it would recarve TSA’s “intervention” (preservation-layer cluster or causal probe) into BCT design, which App B already refuses. A cite is still worth it: the homographs are exact LLM bait, and a one-line App B exclude (“BCIO/BCTO is not this book’s intervention object”) blocks that collapse without changing a TSA cut.
- **Ontology-stickiness risk:** High, in the reverse direction. Pre-2022 models already have BCTTv1 and “behaviour change techniques”; 2022–23 OWL BCIO/BCTO is now a well-documented, training-heavy schema. A model drafting TSA will reach for target/content/source/mode/fidelity/engagement and miss that TSA’s intervention map is a preservation-layer filter, CCI fidelity is explanation-to-judgment, and engagement in TSA is usually the *adversary’s* proxy. TSA already excludes the framing; the risk is the exclude getting overwritten by the stickier ontology.
- **Recommended action:** cite-in-crosswalk

## One-line finding

BCIO/BCTO formally atomizes behaviour-change programmes for evidence synthesis; TSA already excludes behavioural framings, so the purchase is a homograph warning (intervention/fidelity/engagement), not a missing primitive.
