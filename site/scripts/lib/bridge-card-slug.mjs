/** Map Lean / graph node ids (MB1, MB4a, MB7d, …) to companion bridge card slugs. */

export function bridgeCardSlug(nodeId) {
  if (nodeId.startsWith("MB4a")) return "mb4a-measured-path-legitimacy";
  if (nodeId.startsWith("MB7d")) return "mb7d-acausal-coordination";
  const mb = nodeId.match(/^MB(\d+)/);
  if (!mb) return null;
  const names = {
    1: "mb1-boundary-estimator-soundness",
    2: "mb2-bundle-identifiability",
    3: "mb3-bearer-import",
    4: "mb4-correction-legitimacy",
    5: "mb5-successor-ontology-shift",
    6: "mb6-selection-and-basin-stability",
    7: "mb7-hidden-capability-and-access",
    8: "mb8-cev-process-convergence",
    9: "mb9-grounding-certificate",
    10: "mb10-successor-forgeability",
    11: "mb11-deployment-safety"
  };
  const key = nodeId.startsWith("MB6") ? 6 : nodeId.startsWith("MB7") ? 7 : Number(mb[1]);
  return names[key] || null;
}
