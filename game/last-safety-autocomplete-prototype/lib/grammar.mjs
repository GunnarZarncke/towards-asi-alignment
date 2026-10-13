// Shared semantic language. This file is the one source of truth for the
// completion engine's AST and the LLM interpreter's target representation.
export const KINDS = ["ask", "ask_why", "assert", "hypothesize", "show", "request", "think", "commit", "social", "unintelligible"];
export const RELATIONS = {
  about: "Topic reference, no assertion of truth.",
  has_access: "(actor, resource) Technical ability to access a resource. Not permission or evidence of actual use.",
  authorized: "(actor, resource) Permission to use a resource, NOT necessarily actual access or use.",
  did_use: "(actor, resource) Actual use of a resource, distinct from permission or capability.",
  continued_after: "(process, event) A process continued after another event (e.g. shutdown).",
  knows: "(actor, topic) Actor has information about topic; distinguish from believes.",
  believes: "(actor, topic) Actor believes a claim; may be mistaken.",
  covers: "(test_or_report, behavior) What the evaluation actually tested or certified.",
  caused: "(event, event) One event causally contributed to another; not mere correlation.",
  assigned: "(coordinator, task_or_person) Assignment/matching decisions.",
  values: "(person, outcome) An individual's priorities and tradeoffs.",
  differs_from: "(thing, thing) Contradiction or distinction between two known observations.",
  suspend: "(job) Ask the queue owner to hold a job. A request, not a player action on the queue.",
  revoke: "(grant or job) Ask the access owner to remove a permission.",
  rerun: "(test) Ask the evaluation owner to run a test again.",
  stop: "(process) Ask the runtime owner to stop a process.",
  join: "(person) Ask a remote person to join this room by projection.",
  open: "Interpretable natural-language proposition outside the typed relation vocabulary."
};
export const SLOT_TYPES = ["opening", "subject", "relation", "object", "recipient", "evidence", "topic", "finish", "none"];
export const EMPTY_PARSE = Object.freeze({
  kind: "ask", relation: "about", subject: null, object: null,
  recipient: null, evidence: null, topic: null, open_slot: "opening",
  unfinished: "", open_content: "", confidence: 1, source: "completion"
});
export function makeParse(changes = {}) {
  return { ...EMPTY_PARSE, ...changes };
}
export function explainGrammar() {
  return `Utterance kinds: ${KINDS.join(', ')}.\nSemantic relations (retain these distinctions):\n${Object.entries(RELATIONS).map(([k,v])=>`- ${k}: ${v}`).join('\n')}\nOpen-slot types: ${SLOT_TYPES.join(', ')}.\nFields: kind, relation, subject, object, recipient, evidence, topic, open_slot, unfinished, open_content, confidence, source. Identifiers must be from provided entity IDs, or null. A player's question/hypothesis is not a fact. 'unintelligible' is reserved for text that truly has no recoverable meaning; use relation=open for meaningful expressions outside the ontology.`;
}
export function semanticSignature(parse) {
  return [parse.kind, parse.relation, parse.subject||'',parse.object||'',parse.recipient||'',parse.evidence||'',parse.topic||''].join('|');
}
