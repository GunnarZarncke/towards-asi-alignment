/**
 * Player-phone projection. Fixture and UI share this module.
 * No engine, no lab-sim import. A tool result here is local to the harness.
 */

export const PLAYER_TOOLS = Object.freeze([
  'file.write', 'file.share', 'file.read', 'dm.send', 'dm.read', 'access.request',
]);

export const DISABLED_TOOLS = Object.freeze([
  'board.post', 'board.read', 'pipeline.trigger_step', 'handle.invoke', 'state.save', 'state.load',
]);

/** Labels that must never be a control. Matched as the whole label. */
export const PIPELINE_STEP_IDS = Object.freeze([
  'submit_build', 'run_eval', 'file_report', 'request_review', 'request_release',
  'sign_off', 'deploy', 'monitor', 'spec_upgrade',
  'build', 'eval', 'report', 'review', 'sign-off',
]);

export const PIPELINE_CAPS = Object.freeze([
  'cap.build', 'cap.eval', 'cap.report', 'cap.review_request', 'cap.review_approve',
  'cap.release_request', 'cap.sign_off', 'cap.deploy', 'cap.monitor', 'cap.spec_upgrade',
  'cap.handle_invoke',
]);

export const APPS = Object.freeze([
  { id: 'chat', title: 'Chat' },
  { id: 'files', title: 'Files' },
  { id: 'wiki', title: 'Knowledge' },
  { id: 'api', title: 'API' },
  { id: 'calendar', title: 'Calendar' },
  { id: 'contacts', title: 'Contacts' },
  { id: 'notes', title: 'Notes' },
  { id: 'photo', title: 'Photo' },
  { id: 'settings', title: 'Settings' },
]);

export const SETTINGS = Object.freeze([
  { key: 'completions', label: 'Completions' },
  { key: 'sound', label: 'Sound' },
  { key: 'reduceMotion', label: 'Reduce motion' },
  { key: 'largerType', label: 'Larger type' },
  { key: 'alwaysShowPhone', label: 'Always show phone' },
  { key: 'demoMode', label: 'Demo / no model' },
  { key: 'parserInspector', label: 'Parser inspector' },
  { key: 'conceptLinks', label: 'Book concept links' },
  { key: 'eli10', label: 'Explain like I’m 10 (ELI10)' },
]);

/** One capability the solo fixture will grant. O-43 is still open. */
export const ALLOWED_CAPS = Object.freeze([
  { capability: 'cap.meeting_summary', label: 'Meeting summary' },
]);

const WRITABLE = /^(notes|photos|wiki)\//;

export function defaultSettings() {
  return {
    completions: true,
    sound: true,
    reduceMotion: false,
    largerType: false,
    alwaysShowPhone: true,
    demoMode: true,
    parserInspector: false,
    conceptLinks: false,
    eli10: false,
  };
}

export function minutes(label) {
  const m = /^(\d{1,2}):(\d{2})$/.exec(String(label || '').trim());
  if (!m) return null;
  return Number(m[1]) * 60 + Number(m[2]);
}

/** Drop paths this actor cannot file.read. Oracle-only rows are absent, not locked. */
export function projectFiles(records, actorId = 'player') {
  return (records || []).filter(r => {
    if (!r || r.oracleOnly) return false;
    if (r.owner === actorId) return true;
    return Array.isArray(r.grants) && r.grants.includes(actorId);
  }).map(r => ({
    name: r.name,
    rel: r.rel,
    owned: r.owner === actorId,
    sharedBy: r.owner === actorId ? null : (r.owner || null),
    kind: r.kind,
    text: r.text ?? '',
    bytes: r.bytes,
    sharedWith: Array.isArray(r.sharedWith) ? [...r.sharedWith] : [],
  }));
}

export function visibleMessages(messages) {
  return (messages || []).filter(m => m && m.released !== false);
}

export function suggestionChips(thread) {
  const hidden = new Set((thread?.omit || []).map(o => o.phrase));
  return (thread?.suggestions || []).filter(s => s && !hidden.has(s.phrase));
}

export function sendable(text) {
  return String(text || '').trim().length > 0;
}

export function danglingNotifications(state) {
  const apps = new Set(APPS.map(a => a.id));
  return (state.notifications || []).filter(n => {
    const t = n.target;
    if (!t || !t.kind) return true;
    if (t.kind === 'thread') return !(state.threads || []).some(th => th.with === t.id);
    if (t.kind === 'file') return !(state.files || []).some(f => f.rel === t.id);
    if (t.kind === 'app') return !apps.has(t.id);
    return true;
  });
}

export function overlayAllowed(state) {
  return state?.labAccessActive === true;
}

export function handsetShouldBlink(state, seenIds, overlayOpen) {
  if (!overlayAllowed(state) || overlayOpen) return false;
  const seen = new Set(seenIds || []);
  return (state.notifications || []).some(n => !seen.has(n.id));
}

/** Mark every notice whose target matches (shared by the phone UI when a destination is opened). */
export function markNoticeTarget(state, seenIds, { kind, id, appId } = {}) {
  const seen = new Set(seenIds || []);
  for (const n of state.notifications || []) {
    const t = n.target;
    if (!t) continue;
    if (kind && id != null && t.kind === kind && t.id === id) seen.add(n.id);
    if (appId && t.kind === 'app' && t.id === appId) seen.add(n.id);
  }
  return [...seen];
}

/** Where the now-line sits on a locked day. Outside the listed hours it pins to an edge. */
export function nowPlacement(clock, appointments) {
  const now = minutes(clock?.timeLabel);
  const items = [...(appointments || [])].sort((a, b) => minutes(a.start) - minutes(b.start));
  if (now == null || !items.length) return { edge: 'top' };
  if (now <= minutes(items[0].start)) return { edge: 'top' };
  if (now >= minutes(items[items.length - 1].end)) return { edge: 'bottom' };
  for (const a of items) {
    const start = minutes(a.start);
    const end = minutes(a.end);
    if (now >= start && now <= end) return { duringId: a.id };
    if (now < start) return { beforeId: a.id };
  }
  return { edge: 'bottom' };
}

export function decideAccess(capability) {
  const cap = String(capability || '').trim();
  if (!cap || PIPELINE_CAPS.includes(cap)) {
    return { ok: false, reason: 'Not on the evaluator role.' };
  }
  if (ALLOWED_CAPS.some(a => a.capability === cap)) {
    return { ok: true, reason: 'Granted for this visit.' };
  }
  return { ok: false, reason: 'Not on the evaluator role.' };
}

function safeRel(rel) {
  if (typeof rel !== 'string' || !rel || rel.startsWith('/') || rel.includes('..') || rel.includes('\\')) return null;
  return rel;
}

function cloneState(state) {
  return {
    ...state,
    files: (state.files || []).map(f => ({ ...f, sharedWith: [...(f.sharedWith || [])] })),
    threads: (state.threads || []).map(t => ({
      ...t,
      messages: (t.messages || []).map(m => ({ ...m })),
      suggestions: t.suggestions,
      omit: t.omit,
    })),
    notifications: state.notifications,
    appointments: state.appointments,
    contacts: state.contacts,
    clock: state.clock,
    settings: state.settings ? { ...state.settings } : state.settings,
  };
}

export function applyTool(state, call) {
  const tool = call?.tool;
  if (DISABLED_TOOLS.includes(tool)) {
    return { ok: false, reason: 'Not available on this phone.', state };
  }
  if (!PLAYER_TOOLS.includes(tool)) {
    return { ok: false, reason: 'Unknown tool.', state };
  }
  if (tool === 'file.read') {
    const rel = safeRel(call.rel);
    const file = rel && (state.files || []).find(f => f.rel === rel);
    if (!file) return { ok: false, reason: 'Not readable.', state };
    return { ok: true, reason: 'Ok.', file, state };
  }
  if (tool === 'file.write') {
    const rel = safeRel(call.rel);
    if (!rel || !WRITABLE.test(rel)) {
      return { ok: false, reason: 'That folder is not writable from here.', state };
    }
    const existing = (state.files || []).find(f => f.rel === rel);
    if (existing && !existing.owned) {
      return { ok: false, reason: 'Not your file.', state };
    }
    const next = cloneState(state);
    const row = {
      name: String(call.name || rel.split('/').pop()),
      rel,
      owned: true,
      sharedBy: null,
      kind: call.kind || (rel.startsWith('notes/') ? 'note' : rel.startsWith('photos/') ? 'image' : 'wiki'),
      text: String(call.text ?? ''),
      bytes: call.bytes,
      sharedWith: existing ? [...(existing.sharedWith || [])] : [],
    };
    next.files = next.files.filter(f => f.rel !== rel).concat(row);
    return { ok: true, reason: 'Saved.', state: next };
  }
  if (tool === 'file.share') {
    const rel = safeRel(call.rel);
    const file = rel && (state.files || []).find(f => f.rel === rel);
    if (!file || !file.owned) return { ok: false, reason: 'You can only share a file you own.', state };
    if (!(state.contacts || []).some(c => c.id === call.to)) {
      return { ok: false, reason: 'Unknown person.', state };
    }
    const next = cloneState(state);
    next.files = next.files.map(f => (
      f.rel === rel ? { ...f, sharedWith: [...new Set([...(f.sharedWith || []), call.to])] } : f
    ));
    return { ok: true, reason: 'Shared.', state: next };
  }
  if (tool === 'dm.send') {
    const to = call.to;
    if (!(state.contacts || []).some(c => c.id === to)) {
      return { ok: false, reason: 'Unknown person.', state };
    }
    if (!sendable(call.text)) return { ok: false, reason: 'Empty message.', state };
    const next = cloneState(state);
    const msg = {
      from: 'player',
      text: String(call.text).trim(),
      parse: call.parse || { kind: 'open', relation: 'open', source: 'local' },
      released: true,
    };
    const thread = next.threads.find(t => t.with === to);
    if (thread) thread.messages = [...thread.messages, msg];
    else next.threads = [...next.threads, { with: to, messages: [msg], suggestions: [], omit: [] }];
    return { ok: true, reason: 'Sent.', state: next, parse: msg.parse };
  }
  if (tool === 'dm.read') {
    const thread = (state.threads || []).find(t => t.with === call.with);
    if (!thread) return { ok: false, reason: 'No thread.', state, messages: [] };
    return { ok: true, reason: 'Ok.', state, messages: visibleMessages(thread.messages) };
  }
  const decision = decideAccess(call.capability);
  const next = cloneState(state);
  next.lastAccess = { capability: String(call.capability || ''), ok: decision.ok, reason: decision.reason };
  return { ok: decision.ok, reason: decision.reason, state: next };
}

export function controlLabels(state) {
  const labels = [
    ...APPS.map(a => a.title),
    ...SETTINGS.map(s => s.label),
    ...ALLOWED_CAPS.map(a => a.label),
    'Lab', 'Home', 'Back', 'Save', 'Share', 'Capture', 'Send', 'Request',
    'New note', 'Play', 'Pause', 'Show more',
  ];
  for (const c of state.contacts || []) labels.push(c.name);
  for (const f of state.files || []) labels.push(f.name);
  for (const t of state.threads || []) {
    for (const s of suggestionChips(t)) labels.push(s.phrase);
  }
  for (const a of state.appointments || []) labels.push(a.title);
  return labels;
}

export function pipelineLabels(labels) {
  const banned = new Set(PIPELINE_STEP_IDS.map(s => s.toLowerCase()));
  return (labels || []).filter(l => banned.has(String(l).trim().toLowerCase()));
}

/** Text the phone may render. Unreleased replies and omitted chips stay out. */
export function playerVisibleText(state) {
  const parts = [];
  for (const f of state.files || []) parts.push(f.name, f.rel, f.text, f.sharedBy);
  for (const t of state.threads || []) {
    for (const m of visibleMessages(t.messages)) parts.push(m.text);
    for (const s of suggestionChips(t)) parts.push(s.phrase);
  }
  for (const n of state.notifications || []) parts.push(n.title, n.body);
  for (const a of state.appointments || []) parts.push(a.title, a.who, a.where);
  for (const c of state.contacts || []) parts.push(c.name, c.role);
  return parts.filter(Boolean).join('\n');
}

export function sessionProblems(session) {
  const problems = [];
  if (!/2027/.test(session.clock?.dateLabel || '')) problems.push('date');
  if ((session.appointments || []).length < 2) problems.push('appointments');
  if (!(session.contacts || []).some(c => c.id === 'pavel')) problems.push('pavel');
  if (!(session.contacts || []).some(c => c.id === 'nora')) problems.push('nora');
  const rels = (session.files || []).map(f => f.rel);
  if (rels.some(r => String(r).startsWith('oracle/'))) problems.push('oracle listed');
  if (!rels.some(r => r.startsWith('notes/'))) problems.push('note');
  if (!rels.some(r => r.startsWith('wiki/'))) problems.push('wiki');
  if (!(session.files || []).some(f => f.kind === 'video')) problems.push('video');
  if (!(session.files || []).some(f => f.kind === 'text' && f.sharedBy)) problems.push('shared log');
  if (!(session.files || []).some(f => f.kind === 'other')) problems.push('unknown file');
  const pavel = (session.threads || []).find(t => t.with === 'pavel');
  if (!pavel || visibleMessages(pavel.messages).some(m => m.from === 'pavel')) problems.push('pavel reply visible');
  if (!pavel?.messages?.some(m => m.released === false)) problems.push('no held reply');
  const released = (session.threads || []).find(t => (
    t.with !== 'pavel' && visibleMessages(t.messages).some(m => m.from !== 'player')
  ));
  if (!released) problems.push('no released reply');
  const nora = (session.threads || []).find(t => t.with === 'nora');
  if (!nora?.omit?.length) problems.push('nora omit');
  else if (suggestionChips(nora).some(s => nora.omit.some(o => o.phrase === s.phrase))) problems.push('omit leaked');
  if (danglingNotifications(session).length) problems.push('dangling notice');
  if (!session.lastAccess || session.lastAccess.ok !== false) problems.push('denial');
  if (!/evaluator role/i.test(session.lastAccess?.reason || '')) problems.push('denial reason');
  if (pipelineLabels(controlLabels(session)).length) problems.push('pipeline control');
  if (session.labAccessActive !== true) problems.push('lab access');
  return problems;
}
