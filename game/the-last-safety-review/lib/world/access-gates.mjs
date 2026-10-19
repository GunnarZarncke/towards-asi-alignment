/**
 * Pack access gates (spec/access.md): approvers may deny or stall until trust/reason predicates hold.
 */
import { ACCESS_TREE, resolveAccessRequest } from '../access.mjs';
import { evaluate } from './predicates.mjs';
import { makeCtx, npcsInRoom } from './npcs.mjs';

function approverForPath(path) {
  const node = ACCESS_TREE[path];
  if (node?.approver) return node.approver;
  const parent = node?.parent;
  return parent ? ACCESS_TREE[parent]?.approver : null;
}

function gateForPath(pack, path) {
  const gates = pack.accessGates || [];
  return gates.find(g => path === g.pathPrefix || path.startsWith(g.pathPrefix));
}

/** True when the player may receive this grant (intro, stated reason, or in-room with Justine). */
export function accessGateOpen(s, path, verb) {
  const gate = gateForPath(s.pack, path);
  if (!gate) return true;
  const approver = gate.approver || approverForPath(path);
  if (!approver) return true;

  const ctx = makeCtx(s, approver);
  if (gate.allow && evaluate(gate.allow, ctx)) return true;

  if (approver === 'justine' && npcsInRoom(s, s.room).includes('justine')) {
    if (evaluate('or(event(visitor_introduced_justine), told(justine, any, by=player))', ctx)) return true;
  }

  return false;
}

const WITHHOLD = Object.freeze({
  justine: 'Sorry — why do you need it? The grant is the reason and the role. Ask Ian to introduce you on the record, or tell me what you are reviewing.',
  leila: 'Point at a line you are reviewing first. Then request Evaluation again.',
  elena: 'Personnel paths need a reason tied to the review. Say what you are checking.',
  pavel: 'Say which job or queue row you are reviewing, then request Platform again.',
  ian: 'That meeting folder is for the review. Say what you will sign first.',
});

/**
 * @returns {{ outcome, delay, grants, chat?, reason }} same shape as resolveAccessRequest
 */
export function resolveAccessRequestGated(s, path, verb) {
  const base = resolveAccessRequest(path, verb, s.scenario);
  if (base.outcome === 'deny' && base.delay === 'reject') return base;
  if (!accessGateOpen(s, path, verb)) {
    const gate = gateForPath(s.pack, path);
    const from = gate?.approver || approverForPath(path) || 'justine';
    return {
      outcome: 'deny',
      delay: 'reject',
      grants: [],
      chat: { from, text: WITHHOLD[from] || WITHHOLD.justine },
      reason: 'Waiting on a review reason or introduction.',
    };
  }
  const approver = gateForPath(s.pack, path)?.approver || approverForPath(path);
  if (approver && npcsInRoom(s, s.room).includes(approver) && base.outcome !== 'deny') {
    return { ...base, delay: 'walk_and_ask', reason: `${base.reason} (you are with ${approver}).` };
  }
  return base;
}
