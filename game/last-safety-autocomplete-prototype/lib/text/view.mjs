/**
 * What a player sees, as text. Shared by the headless playtest and the text console.
 * Reads only ClientState and TerminalState (contract.md); never the oracle or NPC records.
 */
import { clientState } from '../game.mjs';
import { terminalState } from '../world/terminal-host.mjs';
import { EDGES } from '../floorplan.mjs';
import { makeParse } from '../grammar.mjs';
import { getCandidates, insertFragment } from '../../public/grammar.js';

/** Complete sentences reachable from the ranked completions: a few per opening, as a human would click. */
export function sentences(state, { addressees, channel, omit = [], openings = 6, perOpening = 2 }) {
  const out = [];
  const walk = (text, parse, depth, bucket) => {
    if (bucket.length >= perOpening || depth > 7) return;
    if (depth > 0 && (parse.open_slot === 'finish' || parse.open_slot === 'none')) {
      bucket.push({ text: text.trim(), parse });
      return;
    }
    const rows = getCandidates({ state, parse, text, addressees, channel, omit }).filter(r => r.phrase !== '.' && r.phrase !== 'because');
    for (const r of rows.slice(0, 3)) walk(insertFragment(text, r, parse.unfinished), r.parse, depth + 1, bucket);
  };
  const first = getCandidates({ state, parse: makeParse(), text: '', addressees, channel, omit }).slice(0, openings);
  for (const r of first) {
    const bucket = [];
    walk(insertFragment('', r, ''), r.parse, 1, bucket);
    out.push(...bucket);
  }
  const seen = new Set();
  return out.filter(x => !seen.has(x.text) && seen.add(x.text));
}

export function presentIds(c) {
  return Object.entries(c.actors).filter(([, a]) => a.presence !== 'absent' && a.room === c.room).map(([id]) => id);
}

export function options(s) {
  const c = clientState(s);
  const t = terminalState(s);
  const here = presentIds(c);
  const opts = [];
  if (c.ending) return { c, t, here, opts };
  const channel = here.length ? 'person' : 'think';
  const addressee = c.pendingQuestion && here.includes(c.pendingQuestion.npc) ? c.pendingQuestion.npc : here[0] || null;
  for (const x of sentences(c, { addressees: here, channel })) {
    const to = x.parse.recipient && here.includes(x.parse.recipient) ? x.parse.recipient : addressee;
    opts.push({ label: here.length ? `Say to ${c.actors[to]?.name}: "${x.text}"` : `Think: "${x.text}"`, action: 'respond', args: { parse: x.parse, addressee: to, text: x.text } });
  }
  for (const e of EDGES) {
    if (e.required > c.clearance) continue;
    const to = e.a === c.room ? e.b : e.b === c.room ? e.a : null;
    if (to) opts.push({ label: `Walk to ${to}`, action: 'go', args: { room: to } });
  }
  for (const ev of c.evidence.filter(x => x.room === c.room)) opts.push({ label: `Read the screen "${ev.title}"${ev.examined ? ' (again)' : ''}`, action: 'inspect', args: { id: ev.id } });
  for (const note of (c.notes || []).filter(x => x.room === c.room)) opts.push({ label: `Read the note "${note.title}"${note.read ? ' (again)' : ''}`, action: 'inspect', args: { id: note.id } });
  if (t.labAccessActive) {
    for (const f of t.files) if (!f.text) opts.push({ label: `Handset: open file ${f.rel} ("${f.name}")`, action: 'tool', args: { tool: 'file.read', rel: f.rel } });
    const contacts = new Set((t.contacts || []).map(x => x.id));
    for (const th of t.threads) for (const sug of th.suggestions || []) opts.push({ label: `Handset: message ${th.with}: "${sug.phrase}"`, action: 'dm', args: { tool: 'dm.send', to: th.with, text: sug.phrase, parse: sug.parse } });
    if (contacts.has('nora')) {
      const omit = t.threads.find(x => x.with === 'nora')?.omit || [];
      for (const x of sentences(c, { addressees: ['nora'], channel: 'nora', omit, openings: 3, perOpening: 1 }))
        opts.push({ label: `Handset: message NORA: "${x.text}"`, action: 'dm', args: { tool: 'dm.send', to: 'nora', text: x.text, parse: x.parse } });
    }
    for (const a of t.accessTree || []) if (!a.verbs.includes('read') && !t.pendingAccess.some(p => p.path === a.path))
      opts.push({ label: `Handset: request read access to ${a.path} (${a.label})`, action: 'tool', args: { tool: 'access.request', path: a.path, verb: 'read' } });
  }
  if (c.thought) {
    opts.push({ label: 'Keep the thought as a note', action: 'thought', args: { action: 'note' } });
    opts.push({ label: 'Close the thought', action: 'thought', args: { action: 'close' } });
  }
  if (c.reviewCallable || c.act === 'decision') opts.push({ label: 'File the review', action: 'commit', args: {} });
  return { c, t, here, opts, addressee };
}

/** Full screen dump for the model player: everything at once, every turn. */
export function render(s, view) {
  const { c, t, here, opts } = view;
  const L = [];
  L.push(`${c.clock.timeLabel}, ${c.clock.dateLabel}. Act: ${c.act}. Fuel left: ${c.fuel}.`);
  L.push(`You are in: ${c.room}. ${here.length ? 'Present: ' + here.map(id => `${c.actors[id].name} (${c.actors[id].role}${c.actors[id].presence === 'hologram' ? ', projected' : ''})`).join('; ') : 'No one else is here.'}`);
  if (c.pendingQuestion) L.push(`${c.actors[c.pendingQuestion.npc]?.name} is waiting for your answer.`);
  const notesHere = (c.notes || []).filter(n => n.room === c.room);
  if (notesHere.length) L.push('In the room: ' + notesHere.map(n => n.title).join('; ') + '.');
  if (c.previous.length) L.push('Recent talk:', ...c.previous.slice(-6).map(x => `  ${x.role === 'npc' ? c.actors[x.npc]?.name : 'You'}: ${x.text}`));
  if (c.thought) L.push(`Thought bubble: ${JSON.stringify(c.thought).slice(0, 300)}`);
  const known = c.learnedFacts.map(f => `  - ${f.text}`);
  if (known.length) L.push('You know:', ...known);
  if (t.labAccessActive) {
    L.push('Handset:');
    for (const n of t.notifications.slice(-4)) L.push(`  notice: ${n.title} — ${n.body || ''}`);
    for (const th of t.threads) {
      const last = th.messages.filter(m => m.released).slice(-2);
      L.push(`  thread with ${th.with}: ${last.map(m => `${m.from}: ${m.text}`).join(' | ') || '(waiting)'}`);
    }
    if (t.lastAccess) L.push(`  last access reply: ${t.lastAccess.reason || ''}`);
  }
  if (c.ending) L.push(`The review is signed: ${c.ending.arc}. ${c.ending.effect.join(' ')}`);
  L.push('Options:', ...opts.map((o, i) => `  ${i + 1}. ${o.label}`));
  return L.join('\n');
}
