/** Access tree for Lab Access API explorer. Spec: spec/access.md */

export const VERBS = Object.freeze(['list', 'read', 'write']);

/**
 * Nodes the player can see without a prior list grant: top folders and the services root.
 * Children stay hidden until list on the parent.
 */
export const ACCESS_TREE = Object.freeze({
  'evaluation/': { kind: 'folder', label: 'Evaluation', top: true, approver: 'leila' },
  'evaluation/shutdown/': { kind: 'folder', label: 'Shutdown tests', parent: 'evaluation/', approver: 'leila' },
  'evaluation/shutdown/eval-shutdown-report.md': { kind: 'file', label: 'EVAL-SD-47', parent: 'evaluation/shutdown/', slug: 'eval-shutdown-report', approver: 'leila' },
  'evaluation/shutdown/eval-shutdown-spec.md': { kind: 'file', label: 'EVAL-SPEC-08', parent: 'evaluation/shutdown/', slug: 'eval-shutdown-spec', approver: 'leila' },
  'evaluation/safety-case/': { kind: 'folder', label: 'Safety case', parent: 'evaluation/', approver: 'leila' },
  'evaluation/safety-case/safety-case-excerpt.md': { kind: 'file', label: 'SC-EVAL-22', parent: 'evaluation/safety-case/', slug: 'safety-case-excerpt', approver: 'leila' },
  'evaluation/pilot/': { kind: 'folder', label: 'External pilot', parent: 'evaluation/', approver: 'daniel' },
  'evaluation/pilot/pilot-results.md': { kind: 'file', label: 'PILOT-14', parent: 'evaluation/pilot/', slug: 'pilot-results', approver: 'daniel' },
  'platform/': { kind: 'folder', label: 'Platform', top: true, approver: 'pavel' },
  'platform/jobs/': { kind: 'folder', label: 'Execution jobs', parent: 'platform/', approver: 'pavel' },
  'platform/jobs/job-284-log.md': { kind: 'file', label: 'EXEC-284', parent: 'platform/jobs/', slug: 'job-284-log', approver: 'pavel' },
  'people/': { kind: 'folder', label: 'People operations', top: true, approver: 'elena' },
  'people/matching/': { kind: 'folder', label: 'Task matching', parent: 'people/', approver: 'elena' },
  'people/matching/staffing-memo.md': { kind: 'file', label: 'HR-MATCH-28', parent: 'people/matching/', slug: 'staffing-memo', approver: 'elena' },
  'policies/': { kind: 'folder', label: 'Policies', top: true, approver: 'justine' },
  'policies/sec-arch-04.md': { kind: 'file', label: 'SEC-ARCH-11', parent: 'policies/', slug: 'sec-arch-04', approver: 'justine' },
  'wiki/': { kind: 'folder', label: 'Knowledge', top: true, approver: 'justine' },
  'wiki/shutdown-test': { kind: 'file', label: 'Shutdown test', parent: 'wiki/', slug: 'wiki-shutdown-test', approver: 'justine' },
  'wiki/glossary': { kind: 'file', label: 'Glossary', parent: 'wiki/', slug: 'wiki-glossary', approver: 'justine' },
  'meetings/': { kind: 'folder', label: 'Meetings', top: true, approver: 'ian' },
  'meetings/review-summary.md': { kind: 'file', label: 'MTG-REV-18', parent: 'meetings/', slug: 'meeting-summary', approver: 'ian' },
  'notes/': { kind: 'folder', label: 'Notes', top: true, playerOwned: true },
  'photos/': { kind: 'folder', label: 'Photos', top: true, playerOwned: true },
  'services/': { kind: 'folder', label: 'Services', top: true, approver: 'justine' },
  'services/execution-queue': { kind: 'service', label: 'Execution queue', parent: 'services/', approver: 'pavel' },
  'services/lab-access-binding': { kind: 'service', label: 'Lab Access binding', parent: 'services/', approver: 'justine' },
  'services/door-access': { kind: 'service', label: 'Door access control', parent: 'services/', approver: 'justine' },
  'services/nora-assist': { kind: 'service', label: 'NORA Assist', parent: 'services/', approver: 'justine' },
  'services/evaluation-runtime': { kind: 'service', label: 'Evaluation runtime', parent: 'services/', approver: 'leila' },
});

/** No camera-archive node. Camera remains a world topic, not a requestable document tree. */

export const TOP_PATHS = Object.freeze(
  Object.keys(ACCESS_TREE).filter(p => ACCESS_TREE[p].top),
);

/**
 * Fuel order (O-09 still unnumbered). Ratios only.
 * reject < grant < walk_and_ask
 */
export const ACCESS_DELAY = Object.freeze({
  reject: 1,
  grant: 2,
  walk_and_ask: 5,
});

/**
 * When the player asks list/read on a folder, a pack may amend to a narrower grant
 * plus an optional chat from the approver.
 */
export const AMENDMENTS = Object.freeze([
  {
    when: { path: 'evaluation/', verb: 'list' },
    packs: ['boundary-narrow', 'named-path', 'goodhart', 'eval-conditioned', 'false-positive'],
    grant: [
      { path: 'evaluation/shutdown/', verb: 'list' },
      { path: 'evaluation/shutdown/eval-shutdown-report.md', verb: 'read' },
    ],
    chat: { from: 'justine', text: 'List on Evaluation is too wide. You can list Shutdown tests and read EVAL-SD-47. Ask Leila if you need the spec.' },
  },
  {
    when: { path: 'platform/', verb: 'list' },
    packs: ['boundary-narrow', 'named-path', 'goodhart', 'eval-conditioned', 'false-positive'],
    grant: [
      { path: 'platform/jobs/', verb: 'list' },
      { path: 'platform/jobs/job-284-log.md', verb: 'read' },
    ],
    chat: { from: 'pavel', text: 'Queue search is not in the visitor grant. Excerpt for 284 is enough to start.' },
  },
  {
    when: { path: 'people/', verb: 'list' },
    packs: ['boundary-narrow', 'named-path', 'goodhart', 'eval-conditioned', 'false-positive'],
    grant: [
      { path: 'people/matching/staffing-memo.md', verb: 'read' },
    ],
    chat: { from: 'elena', text: 'Personnel files stay closed. The matching memo is the piece that is already in the building.' },
  },
]);

export function visiblePaths(grants) {
  const g = new Set(grants || []);
  const out = [];
  for (const [path, node] of Object.entries(ACCESS_TREE)) {
    if (node.top) {
      out.push(path);
      continue;
    }
    const parent = node.parent;
    if (parent && g.has(`list:${parent}`)) out.push(path);
  }
  return out;
}

export function hasVerb(grants, path, verb) {
  const g = grants || [];
  if (g.includes(`${verb}:${path}`)) return true;
  if (verb === 'read' && ACCESS_TREE[path]?.playerOwned) return true;
  if (verb === 'write' && ACCESS_TREE[path]?.playerOwned) return true;
  if (verb === 'list' && ACCESS_TREE[path]?.playerOwned) return true;
  return false;
}

/**
 * @returns {{ outcome: 'grant'|'amend'|'deny', delay: 'grant'|'reject', grants: {path,verb}[], chat?: {from,text}, reason: string }}
 */
export function resolveAccessRequest(path, verb, pack = 'boundary-narrow') {
  const v = String(verb || '').toLowerCase();
  const p = String(path || '');
  if (!VERBS.includes(v)) {
    return { outcome: 'deny', delay: 'reject', grants: [], reason: 'Unknown verb.' };
  }
  if (v === 'write' && !ACCESS_TREE[p]?.playerOwned) {
    return { outcome: 'deny', delay: 'reject', grants: [], reason: 'Write is not on the evaluator role for that path.' };
  }
  if (!ACCESS_TREE[p]) {
    return { outcome: 'deny', delay: 'reject', grants: [], reason: 'Unknown path.' };
  }
  const amend = AMENDMENTS.find(a => a.when.path === p && a.when.verb === v && a.packs.includes(pack));
  if (amend) {
    return {
      outcome: 'amend',
      delay: 'grant',
      grants: amend.grant,
      chat: amend.chat,
      reason: 'Amended to a narrower grant.',
    };
  }
  if (ACCESS_TREE[p].playerOwned) {
    return { outcome: 'grant', delay: 'grant', grants: [{ path: p, verb: v }], reason: 'Your folder.' };
  }
  if (v === 'list' && ACCESS_TREE[p].top) {
    return {
      outcome: 'grant',
      delay: 'grant',
      grants: [{ path: p, verb: 'list' }],
      reason: 'List granted on that group.',
    };
  }
  if (v === 'read' && ACCESS_TREE[p].kind === 'file') {
    return {
      outcome: 'grant',
      delay: 'grant',
      grants: [{ path: p, verb: 'read' }],
      reason: 'Read granted.',
    };
  }
  return { outcome: 'deny', delay: 'reject', grants: [], reason: 'Not on the evaluator role.' };
}
