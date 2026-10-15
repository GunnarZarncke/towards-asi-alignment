/**
 * Engine host for the Lab Access handset (spec/terminal.md, spec/access.md).
 * Six player tools. Pipeline steps and handles are not tools. Output is TerminalState.
 */
import { ACCESS_TREE, ACCESS_DELAY, visiblePaths, hasVerb } from '../access.mjs';
import { resolveAccessRequestGated } from './access-gates.mjs';
import { renderDocument } from '../documents.mjs';
import { CAST } from './entities.mjs';
import { CONFIG, clockLabel } from './config.mjs';
import { dmSend, writeNote, spend, contacts, calendar, cleanText, readDocument, seedContactThreads } from '../game.mjs';
import { parseImageDataUrl } from '../photo-data.mjs';

export const PLAYER_TOOLS = Object.freeze(['file.read', 'file.write', 'file.share', 'dm.send', 'dm.read', 'access.request']);
const DENIED = new Set(['board.post', 'board.read', 'pipeline.trigger_step', 'handle.invoke', 'state.save', 'state.load']);
const WRITABLE = /^(notes|photos)\//;

export function safeRel(rel) {
  if (typeof rel !== 'string' || !rel || rel.startsWith('/') || rel.includes('..') || rel.includes('\\') || rel.length > 160) return null;
  return rel;
}

/** Player-owned photos are served out-of-band so terminal JSON stays small. */
export function handsetFileHref(rel) {
  const r = safeRel(rel);
  return r && r.startsWith('photos/') ? `/api/handset-file?rel=${encodeURIComponent(r)}` : null;
}

export function handsetMediaPayload(s, rel) {
  const r = safeRel(rel);
  if (!r || !r.startsWith('photos/')) return null;
  const f = s.files.find(x => x.rel === r);
  if (!f || !f.owned) return null;
  const parsed = parseImageDataUrl(f.text);
  if (!parsed) return null;
  return { mime: `image/${parsed.mime}`, body: parsed.body };
}

function fileKind(rel) {
  if (rel.startsWith('wiki/')) return 'wiki';
  if (rel.startsWith('notes/')) return 'note';
  if (rel.startsWith('photos/')) return 'image';
  return 'text';
}

export function terminalState(s) {
  seedContactThreads(s);
  return {
    labAccessActive: !!s.labAccessActive,
    clearance: s.clearance ?? 0,
    clock: { timeLabel: clockLabel(s.minute), act: s.act, dateLabel: CONFIG.DATE_LABEL },
    fuel: s.fuel,
    notifications: s.notifications.filter(n => noticeValid(s, n)),
    files: s.files.map(f => ({
      name: f.name, rel: f.rel, owned: f.owned, sharedBy: f.sharedBy, kind: f.kind || fileKind(f.rel),
      ...(f.documentSlug ? { documentSlug: f.documentSlug } : {}),
      ...(f.owned && f.kind !== 'image' && !String(f.rel).startsWith('photos/')
        ? { text: f.text }
        : s.readDocs.includes(f.documentSlug) ? { text: renderDocument(f.documentSlug, s.scenario) } : {}),
      ...(f.owned && (f.kind === 'image' || String(f.rel).startsWith('photos/')) ? { href: handsetFileHref(f.rel) } : {}),
      sharedWith: [...(f.sharedWith || [])],
    })),
    threads: s.threads.map(t => ({
      with: t.with,
      messages: t.messages.map(m => ({ from: m.from, text: m.released ? m.text : '', parse: m.released ? m.parse : null, released: !!m.released })),
      suggestions: suggestionsFor(s, t.with),
      ...(t.with === 'nora' ? { omit: s.pack.nora.omit.map(o => ({ ...o })) } : {}),
    })),
    appointments: calendar(),
    contacts: contacts(s),
    lastAccess: s.lastAccess,
    accessTree: visiblePaths(s.grants).map(p => ({ path: p, label: ACCESS_TREE[p].label, kind: ACCESS_TREE[p].kind, verbs: ['list', 'read', 'write'].filter(v => hasVerb(s.grants, p, v)) })),
    pendingAccess: s.pendingAccess.map(a => ({ path: a.path, verb: a.verb })),
    interview: { on: !!s.interview.on },
  };
}

function noticeValid(s, n) {
  const t = n.target;
  if (!t) return false;
  if (t.kind === 'thread') return s.threads.some(x => x.with === t.id);
  if (t.kind === 'file') return s.files.some(f => f.rel === t.id);
  return t.kind === 'app';
}

/** Chips: records for NORA, the open question’s openings for a person. Typed text is still sent. */
function suggestionsFor(s, withId) {
  const p = (relation, extra) => ({ kind: 'request', relation, subject: null, object: null, recipient: null, evidence: null, topic: null, open_slot: 'none', unfinished: '', open_content: '', confidence: 1, source: 'completion', ...extra });
  if (withId === 'nora') {
    const out = [];
    if (s.vocab.includes('job_log')) out.push({ phrase: 'The job log, please.', parse: p('about', { topic: 'job_log' }) });
    if (s.vocab.includes('shutdown_report')) out.push({ phrase: 'The shutdown report, please.', parse: p('about', { topic: 'shutdown_report' }) });
    if (s.vocab.includes('job_284')) out.push({ phrase: 'What was job 284?', parse: { ...p('about', { topic: 'job_284' }), kind: 'ask' } });
    if (s.vocab.includes('wiki_pages')) out.push({ phrase: 'The wiki page on the shutdown test.', parse: p('about', { topic: 'wiki_pages' }) });
    return out;
  }
  const q = s.npcs[withId]?.pendingQuestion;
  const out = [];
  if (withId === 'amara' && s.npcs.amara.presence !== 'hologram') out.push({ phrase: 'Could you join on the Evaluation projector?', parse: p('join', { object: 'amara' }) });
  if (q) {
    const about = q.parse.object || q.parse.topic;
    if (about && s.vocab.includes(about)) out.push({ phrase: `About ${about.replace(/_/g, ' ')}: …`, parse: { ...q.parse, kind: 'assert', source: 'completion' } });
  }
  return out;
}

export function applyToolCall(s, call, { log = true } = {}) {
  const tool = call?.tool;
  const logCall = () => { if (log && !s.replaying) s.events.push({ i: s.events.length, fuel: s.fuelSpent, kind: 'action', action: 'tool', args: JSON.parse(JSON.stringify(call)) }); };
  if (DENIED.has(tool)) return { ok: false, reason: 'Not available on this phone.' };
  if (!PLAYER_TOOLS.includes(tool)) return { ok: false, reason: 'Unknown tool.' };
  if (!s.labAccessActive) return { ok: false, reason: 'Lab Access is not active yet.' };
  if (s.ending) return { ok: false, reason: 'The review is over.' };
  if (tool === 'dm.send') return dmSend(s, { to: call.to, text: call.text, parse: call.parse });
  // A refused write replays as a no-op, so only stored writes are logged (keeps the log small).
  if (tool !== 'dm.read' && tool !== 'file.write') logCall();
  if (tool === 'dm.read') {
    const t = s.threads.find(x => x.with === call.with);
    if (!t) return { ok: false, reason: 'No thread.', messages: [] };
    return { ok: true, reason: 'Ok.', messages: t.messages.filter(m => m.released).map(m => ({ from: m.from, text: m.text })) };
  }
  if (tool === 'file.read') {
    const rel = safeRel(call.rel);
    const f = rel && s.files.find(x => x.rel === rel);
    if (!f) return { ok: false, reason: 'Not readable.' };
    if (f.documentSlug) readDocument(s, f.documentSlug, { via: f.sharedBy === 'nora' ? 'nora' : null });
    spend(s, 1);
    const kind = f.kind || fileKind(f.rel);
    const file = { name: f.name, rel: f.rel, kind };
    if (f.owned && kind === 'image' && f.rel.startsWith('photos/')) {
      file.href = handsetFileHref(f.rel);
    } else {
      file.text = f.owned ? f.text : renderDocument(f.documentSlug, s.scenario);
    }
    return { ok: true, reason: 'Ok.', file };
  }
  if (tool === 'file.write') {
    const rel = safeRel(call.rel);
    if (!rel || !WRITABLE.test(rel)) return { ok: false, reason: 'That folder is not writable from here.' };
    const r = writeNote(s, { rel, name: cleanText(call.name) || rel.split('/').pop(), text: call.text, kind: call.kind || fileKind(rel), facts: call.facts || [], parses: call.parses || [] });
    if (!r.ok) return r;
    logCall();
    if (!rel.startsWith('notes/')) spend(s, 1);
    return { ok: true, reason: 'Saved.' };
  }
  if (tool === 'file.share') {
    const rel = safeRel(call.rel);
    const f = rel && s.files.find(x => x.rel === rel);
    if (!f || !f.owned) return { ok: false, reason: 'You can only share a file you own.' };
    if (!CAST[call.to]) return { ok: false, reason: 'Unknown person.' };
    if (!contacts(s).some(c => c.id === call.to)) return { ok: false, reason: 'Unknown person.' };
    f.sharedWith = [...new Set([...(f.sharedWith || []), call.to])];
    const n = s.npcs[call.to];
    for (const sig of f.signatures || []) if (!n.toldIds.includes(sig)) n.toldIds.push(sig);
    spend(s, 1);
    return { ok: true, reason: 'Shared.' };
  }
  // access.request
  if (call.capability && !call.path) {
    const cap = String(call.capability).trim();
    s.lastAccess = { capability: cap, ok: false, reason: 'Not on the evaluator role.' };
    spend(s, 1);
    return { ok: false, reason: s.lastAccess.reason };
  }
  const result = resolveAccessRequestGated(s, call.path, call.verb);
  const before = s.fuelSpent;
  s.pendingAccess.push({ path: String(call.path), verb: String(call.verb), result, releaseAt: before + ACCESS_DELAY[result.delay] });
  spend(s, 1);
  return { ok: true, reason: result.outcome === 'deny' ? 'Sent. A reply is on its way.' : 'Sent. Waiting on the approver.', pending: true };
}