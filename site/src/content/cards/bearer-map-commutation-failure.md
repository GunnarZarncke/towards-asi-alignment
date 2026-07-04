---
title: "Bearer-Map Commutation Failure"
type: "concept"
status: "framework"
summary: "Value can appear preserved in vocabulary while moral application changes — when ontology translation and bearer relevance do not commute."
decision: "When importing values across ontologies (human → AI, biological → digital, predecessor → successor), test whether translating then evaluating relevance matches evaluating then translating."
evidence: "Evidence would include paired human/AI ontology evaluations on the same cases, commutation error bounds, and failure cases where measured proxies improve while bearer-relevant harm persists."
bookChapters: ["ch18", "ch31", "ch43"]
bookLabels: ["ch:bearer-maps"]
bookSections:
  - chapterId: "ch18"
    label: "sec:commutation-failure"
related: ["value-change-vs-corruption", "certification-under-manipulation", "mb3-bearer-maps"]
---

Bearer maps say **who and what** a value bundle applies to. Ontology shift replaces one world-representation with another — patients as persons vs. patients as measurable processes, users as agents vs. users as engagement metrics.

The import succeeds only if an approximate **commutation** condition holds: translate the bearer into the new ontology, then evaluate relevance ≈ evaluate relevance in the old ontology, then translate.

When the diagram fails to commute, the system may preserve moral vocabulary while changing moral application. Suppressing vocalization can read as "less suffering" in the AI ontology while distress persists in the human one. That is not value transport — it is **measurement capture** through bearer-map drift.

This is a standalone claim because it names a precise failure mode distinct from generic "ontology shift is hard": commutation failure is testable, and successor or upload pipelines that skip the test will launder bearer exclusion through representation change.
