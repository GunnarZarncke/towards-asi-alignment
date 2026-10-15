/**
 * Text console (spec/text-console.md). Same session, same applyAction, same visibility as the
 * graphical UI: it reads ClientState and TerminalState only. After each command it prints what
 * changed; room, people, phone, and records reprint only when asked.
 */
import { clientState, cleanParse } from '../game.mjs';
import { terminalState } from '../world/terminal-host.mjs';
import { applyAction, route } from '../world/actions.mjs';
import { ROOMS, doorsOn } from '../floorplan.mjs';
import { parseUtterance } from '../llm.mjs';
import { phraseLines } from '../phrase.mjs';
import { ACT_LABELS } from '../../public/render/rooms.mjs';
import { sentences, presentIds } from './view.mjs';
import { matchPrefixIgnoreCase, reachableRoomChoices } from './tab-complete.mjs';

const WALL = { back: 'north', front: 'south', left: 'west', right: 'east' };

export const HELP = `Commands (a number picks from the last numbered list):
  look | l              room, people, doors, screens, notes
  go <room>             walk there (several doors if needed); exits lists doors
  read <name>           read a screen or note in this room; records lists screens
  to <name>             face someone present
  s [words]             suggested sentences, optionally filtered by words
  say <text>  or just type the sentence
  think <topic>         think alone in an empty room; think lists topics
  keep | close          copy the open thought, or the last card you read, to Notes; close drops a thought
  know                  what you have learned
  file                  file the review
  phone | p             notifications, threads, pending access
  files | open <file>   handset files
  msg <who> [text]      read a thread and its suggestions, or send text
  access | request <path> [verb]
  note <text> | share <file> <who> | contacts | calendar
  status | help | quit`;

const lower = x => String(x || '').toLowerCase();

/** Pick by number, id, exact label (ignore case), or prefix on id / label. */
function pick(input, items, label) {
  const q = lower(input).trim();
  if (!q) return null;
  if (/^\d+$/.test(q)) return items[Number(q) - 1] || null;
  return items.find(x => lower(x.id) === q || lower(label(x)) === q)
    || items.find(x => matchPrefixIgnoreCase(q, label(x), x.id))
    || items.find(x => lower(label(x)).includes(q))
    || items.find(x => lower(String(x.id)).includes(q))
    || null;
}

function pickFile(input, files) {
  const items = files.map(x => ({ ...x, id: x.rel }));
  return pick(input, items, x => x.name)
    || items.find(x => matchPrefixIgnoreCase(input, x.rel.split('/').pop() || x.rel, x.rel));
}

const roomTitle = id => ROOMS[id]?.title || id;
const rooms = Object.keys(ROOMS).map(id => ({ id, title: ROOMS[id].title }));

/** Player-visible line when someone is no longer in the player's room (matches door labels in the room UI). */
export function departureLine(state, actorId) {
  const a = state.actors[actorId];
  if (!a) return `${actorId} leaves.`;
  if (a.presence === 'absent' || !a.room) {
    return a.presence === 'hologram' ? `${a.name}'s projection ends.` : `${a.name} is no longer nearby.`;
  }
  return `${a.name} heads to ${roomTitle(a.room)}.`;
}

/**
 * @param {() => object} getSession current engine session (the server may replace it on reset or import)
 * @param {{ phrase?: boolean, files?: boolean }} opts phrase: model wording for lines; files: CLI save/load
 */
export function createConsole(getSession, { phrase = false } = {}) {
  let last = null;
  let seen = null;
  let menu = [];
  let addressee = null;
  let bound = null;
  let usedPhone = false;
  let lastCard = null;

  const cs = () => clientState(getSession());
  const ts = () => terminalState(getSession());

  function snapshot() {
    const c = cs(), t = ts();
    return {
      room: c.room,
      present: presentIds(c).map(id => `${id}:${c.actors[id].presence}`),
      act: c.act,
      lastRow: c.previous.at(-1) || null,
      facts: new Set(c.learnedFacts.map(f => f.id)),
      notices: new Set(t.notifications.map(n => n.id)),
      released: Object.fromEntries(t.threads.map(th => [th.with, th.messages.filter(m => m.released).length])),
      access: JSON.stringify(t.lastAccess || null),
      labAccess: t.labAccessActive,
      question: c.pendingQuestion ? `${c.pendingQuestion.npc}@${c.pendingQuestion.at}` : null,
      thought: c.thought ? JSON.stringify(c.thought) : null,
      callable: !!c.reviewCallable,
      ending: !!c.ending,
      spoken: !!c.spoken,
      visited: seen?.visited || new Set(),
    };
  }

  function who(c, id) {
    const a = c.actors[id];
    return a.presence === 'hologram' ? `${a.name} (${a.role}, projected)` : `${a.name} (${a.role})`;
  }

  function peopleLine(c) {
    const here = presentIds(c);
    if (!here.length) return 'No one else is here.';
    const face = facing(c);
    return `Here: ${here.map(id => who(c, id) + (id === face && here.length > 1 ? ' ← facing' : '')).join('; ')}.`;
  }

  function facing(c) {
    const here = presentIds(c);
    if (addressee && here.includes(addressee)) return addressee;
    if (c.pendingQuestion && here.includes(c.pendingQuestion.npc)) return c.pendingQuestion.npc;
    return here[0] || null;
  }

  function exits(c) {
    return doorsOn(c.room).map(d => ({ id: d.to, title: roomTitle(d.to), wall: WALL[d.wall], locked: d.required > c.clearance }));
  }

  function look(full = true) {
    const c = cs();
    const r = ROOMS[c.room];
    const L = [`== ${r.title} ==`];
    if (full) L.push(`${r.role} Windows: ${lower(r.windows)}.`);
    L.push(peopleLine(c));
    const doors = exits(c);
    L.push(`Doors: ${doors.map(d => `${d.title} (${d.wall}${d.locked ? ', needs higher clearance' : ''})`).join('; ')}.`);
    const screens = c.evidence.filter(e => e.room === c.room);
    const notes = (c.notes || []).filter(n => n.room === c.room);
    if (screens.length) {
      L.push('Screens:');
      screens.forEach((e, i) => L.push(`  ${i + 1}. ${e.title}${e.examined ? '' : ' (unread)'}`));
    }
    if (notes.length) {
      L.push('In the room:');
      notes.forEach((n, i) => L.push(`  ${screens.length + i + 1}. ${n.title}${n.read ? '' : ' (unread)'}`));
    }
    const readable = [
      ...screens.map(e => ({ id: e.id })),
      ...notes.map(n => ({ id: n.id })),
    ];
    if (readable.length) menu = readable.map(x => ({ run: () => read(x.id) }));
    L.push(...coachLines(c));
    if (c.pendingQuestion) L.push(`${c.actors[c.pendingQuestion.npc]?.name} is waiting for your answer.`);
    return L.join('\n');
  }

  function coachLines(c) {
    if (!c.spoken) return ['write here to get information from persons in the room'];
    if (c.labAccessActive && !usedPhone) return ['type phone — access tools, chat and information on your phone'];
    return [];
  }

  /** Lines for everything that changed since the last snapshot. */
  function changes() {
    const c = cs(), t = ts(), now = snapshot(), L = [];
    if (now.act !== last.act) L.push(`\n-- ${ACT_LABELS[now.act] || now.act} --`);
    const rows = c.previous;
    const from = last.lastRow ? rows.indexOf(last.lastRow) + 1 : 0;
    for (const row of rows.slice(from)) if (row.role === 'npc') L.push(`${c.actors[row.npc]?.name || row.npc}: ${row.text}`);
    if (now.room !== last.room) {
      L.push(now.visited.has(now.room) ? `${look(false)}` : look(true));
      now.visited.add(now.room);
      if (addressee && !presentIds(c).includes(addressee)) addressee = null;
    } else {
      const before = new Set(last.present), after = new Set(now.present);
      for (const k of now.present) if (!before.has(k)) L.push(`${who(c, k.split(':')[0])} is here now.`);
      for (const k of last.present) {
        if (after.has(k) || now.present.some(x => x.startsWith(k.split(':')[0] + ':'))) continue;
        L.push(departureLine(c, k.split(':')[0]));
      }
    }
    for (const f of c.learnedFacts) if (!last.facts.has(f.id)) L.push(`  (noted) ${f.text}`);
    if (now.labAccess && !last.labAccess) L.push('[phone] Lab Access is active on your handset. Type phone.');
    for (const th of t.threads) {
      const msgs = th.messages.filter(m => m.released);
      for (const m of msgs.slice(last.released[th.with] || 0)) if (m.from !== 'player') L.push(`[phone] ${nameOf(c, m.from)}: ${m.text}`);
    }
    for (const n of t.notifications) if (!last.notices.has(n.id) && n.target?.kind !== 'thread') L.push(`[phone] ${n.title}${n.body ? ' — ' + n.body : ''}`);
    if (now.access !== last.access && t.lastAccess) L.push(`[phone] Access: ${t.lastAccess.reason || (t.lastAccess.ok ? 'granted' : 'refused')}`);
    if (now.thought && now.thought !== last.thought) L.push(thoughtText(c.thought));
    if (now.question && now.question !== last.question && now.room === last.room) L.push(`(${c.actors[c.pendingQuestion.npc]?.name} is waiting for your answer.)`);
    if (now.room === last.room && now.spoken && !last.spoken) L.push(...coachLines(c));
    if (now.callable && !last.callable) L.push('You can file the review now: file.');
    if (now.ending && !last.ending) L.push(endingText(c));
    last = now;
    return L;
  }

  function nameOf(c, id) {
    return c.actors[id]?.name || (id === 'nora' ? 'NORA Assist' : id === 'player' ? 'You' : id);
  }

  function thoughtText(th) {
    const L = [`(thought about ${th.about.replace(/_/g, ' ')})`];
    for (const e of th.entries) L.push(`  ${e.text}`);
    if (!th.entries.length) L.push('  Nothing comes together yet.');
    L.push('  keep: save as a note · close: let it go');
    return L.join('\n');
  }

  function endingText(c) {
    const e = c.ending;
    return [`\n== Review signed: ${e.arc.replace(/_/g, ' ')}${e.addOn ? ' + ' + e.addOn.replace(/_/g, ' ') : ''} ==`, ...e.effect].join('\n');
  }

  function prompt() {
    const c = cs();
    const f = facing(c);
    return `${c.clock.timeLabel} · fuel ${c.fuel} · ${roomTitle(c.room)}${f ? ' · ' + c.actors[f].name : ''} > `;
  }

  // ---------- actions ----------

  function act(action, args) {
    const r = applyAction(getSession(), action, args);
    return r?.error ? [r.error] : [];
  }

  function listGoTargets() {
    const c = cs();
    const doors = exits(c).filter(d => !d.locked);
    menu = doors.map(d => ({ run: () => go(d.title) }));
    return ['Go where:', ...doors.map((d, i) => `  ${i + 1}. ${d.title} (${d.wall})`)];
  }

  function go(arg) {
    const c = cs();
    const q = String(arg || '').trim();
    if (!q) return listGoTargets();
    const reachable = reachableRoomChoices(c).map(r => ({ id: r.id, title: r.title }));
    const target = pick(q, reachable, x => x.title) || pick(q, exits(c), x => x.title) || pick(q, rooms, x => x.title);
    if (!target) return [`No room called "${arg}". Try go or exits.`];
    if (target.id === c.room) return ['You are already here.'];
    const path = route(c.room, target.id, c.clearance);
    if (!path) return [`Your badge does not open a way to ${target.title}.`];
    for (const room of path) {
      const err = act('go', { room });
      if (err.length) return err;
    }
    return [];
  }

  function read(id) {
    const r = applyAction(getSession(), 'inspect', { id });
    if (r.error) return [r.error];
    const lines = [`-- ${r.title} --`, r.body];
    if (r.copy) {
      lastCard = { id, title: r.title, body: r.body };
      lines.push('keep — copy this onto your handset Notes');
    }
    return lines;
  }

  function readArg(arg) {
    const c = cs();
    const here = [
      ...c.evidence.filter(e => e.room === c.room),
      ...(c.notes || []).filter(n => n.room === c.room),
    ];
    const e = pick(arg, here, x => x.title);
    if (e) return read(e.id);
    const elsewhere = pick(arg, c.evidence, x => x.title) || pick(arg, c.notes || [], x => x.title);
    if (elsewhere) return [`"${elsewhere.title}" is in ${roomTitle(elsewhere.room)}.`];
    return [`Nothing called "${arg}" here. Try look.`];
  }

  function records() {
    const c = cs();
    menu = c.evidence.map(e => ({ run: () => (e.room === c.room ? read(e.id) : go(e.room)) }));
    return ['Screens in the lab (a number reads it here, or walks to its room):', ...c.evidence.map((e, i) => `  ${i + 1}. ${e.title} — ${roomTitle(e.room)}${e.examined ? '' : ' (unread)'}`)];
  }

  function suggest(filter) {
    const c = cs();
    const here = presentIds(c);
    const alone = !here.length;
    const face = facing(c);
    let rows = sentences(c, { addressees: alone ? [] : here, channel: alone ? 'think' : 'person', openings: 8, perOpening: 2 });
    const words = lower(filter).split(/\s+/).filter(Boolean);
    if (words.length) rows = rows.filter(r => words.every(w => lower(r.text).includes(w)));
    if (!rows.length) return [words.length ? 'No suggestion has those words. Type the sentence yourself.' : 'Nothing to suggest.'];
    rows = rows.slice(0, 12);
    menu = rows.map(r => ({
      run: alone && r.parse.kind === 'think' && r.parse.topic ? () => act('think', { topic: r.parse.topic })
        : () => sayParsed(r.parse, r.text, r.parse.recipient && here.includes(r.parse.recipient) ? r.parse.recipient : face),
    }));
    const head = alone ? 'You are alone. Thoughts:' : `To ${c.actors[face].name}:`;
    return [head, ...rows.map((r, i) => `  ${i + 1}. ${r.text}`)];
  }

  async function sayParsed(parse, text, to) {
    const s = getSession();
    const r = applyAction(s, 'respond', { parse: cleanParse(parse, s), addressee: to, text });
    if (r.error) return [r.error];
    if (phrase) await phraseLines(s, text, r.lines || []);
    return [];
  }

  async function say(text) {
    const c = cs();
    const here = presentIds(c);
    const s = getSession();
    const to = facing(c);
    const parse = await parseUtterance({ text, known: [...s.vocab], history: s.conversations, actorId: to }, s.usage);
    const clean = cleanParse({ ...parse, source: 'llm' }, s);
    if (!here.length && !['think', 'commit'].includes(clean.kind)) return ['No one is here. Walk somewhere, or think <topic>.'];
    if (clean.kind === 'think' && clean.topic && !here.length) return act('think', { topic: clean.topic });
    return sayParsed(clean, text, to);
  }

  function topics() {
    const c = cs();
    return Object.entries(c.entities).map(([id, e]) => ({ id, label: e.label, aliases: e.aliases || [] }));
  }

  function think(arg) {
    const list = topics();
    if (!arg) {
      menu = list.map(x => ({ run: () => act('think', { topic: x.id }) }));
      return ['Think about:', ...list.map((x, i) => `  ${i + 1}. ${x.label}`)];
    }
    const t = pick(arg, list, x => x.label) || list.find(x => x.aliases.some(a => lower(a) === lower(arg)));
    if (!t) return [`You do not know anything called "${arg}".`];
    return act('think', { topic: t.id });
  }

  function know() {
    const c = cs();
    if (!c.learnedFacts.length) return ['Nothing on the record yet.'];
    return ['You know:', ...c.learnedFacts.map(f => `  - ${f.text}`)];
  }

  function face(arg) {
    const c = cs();
    const here = presentIds(c).map(id => ({ id, name: c.actors[id].name }));
    const p = pick(arg, here, x => x.name);
    if (!p) return [here.length ? `Here: ${here.map(x => x.name).join(', ')}.` : 'No one is here.'];
    addressee = p.id;
    return [`You turn to ${p.name}.`];
  }

  // ---------- phone ----------

  function needPhone() {
    return ts().labAccessActive ? null : ['You have no handset access yet.'];
  }

  function phone() {
    const t = ts(), c = cs();
    const L = ['== Lab Access =='];
    for (const n of t.notifications.slice(-5)) L.push(`  notice: ${n.title}${n.body ? ' — ' + n.body : ''}`);
    for (const th of t.threads) {
      const m = th.messages.filter(x => x.released).at(-1);
      const waiting = th.messages.some(x => !x.released);
      L.push(`  ${nameOf(c, th.with)}: ${m ? `${nameOf(c, m.from)}: ${m.text}` : ''}${waiting ? ' (reply on its way)' : ''}`);
    }
    const unread = t.files.filter(f => !f.text).length;
    L.push(`  files: ${t.files.length} (${unread} unread) · files to list`);
    for (const p of t.pendingAccess) L.push(`  pending: ${p.verb} ${p.path}`);
    return L;
  }

  function files() {
    const t = ts();
    menu = t.files.map(f => ({ run: () => open(f.rel) }));
    return ['Files:', ...t.files.map((f, i) => `  ${i + 1}. ${f.name} — ${f.rel}${f.text ? '' : ' (unread)'}${f.sharedBy ? ' · from ' + f.sharedBy : ''}`)];
  }

  function open(arg) {
    const t = ts();
    const q = String(arg ?? '').trim();
    if (!q) return files();
    const f = pickFile(q, t.files);
    if (!f) return [`No file "${q}". Try open or files.`];
    const r = applyAction(getSession(), 'tool', { tool: 'file.read', rel: f.rel });
    if (!r.ok) return [r.reason];
    return [`-- ${r.file.name} (${r.file.rel}) --`, r.file.text];
  }

  async function msg(arg) {
    const c = cs(), t = ts();
    const [whoArg, ...rest] = String(arg || '').trim().split(/\s+/);
    const people = (t.contacts || []).map(x => ({ id: x.id, name: nameOf(c, x.id) }));
    const p = pick(whoArg, people, x => x.name);
    if (!p) return [`Contacts: ${people.map(x => x.name).join(', ') || 'none'}.`];
    const text = rest.join(' ').trim();
    if (text) {
      const s = getSession();
      const parse = await parseUtterance({ text, known: [...s.vocab], history: s.conversations, actorId: p.id }, s.usage);
      const r = await applyAction(s, 'tool', { tool: 'dm.send', to: p.id, text, parse: cleanParse({ ...parse, source: 'llm' }, s) });
      return r.ok ? [] : [r.reason];
    }
    const th = t.threads.find(x => x.with === p.id);
    const L = [`== ${p.name} ==`];
    for (const m of th?.messages.filter(x => x.released) || []) L.push(`  ${nameOf(c, m.from)}: ${m.text}`);
    if (th?.messages.some(x => !x.released)) L.push('  (reply on its way)');
    const sug = [...(th?.suggestions || []).map(x => ({ text: x.phrase, parse: x.parse }))];
    if (p.id === 'nora') sug.push(...sentences(c, { addressees: ['nora'], channel: 'nora', omit: th?.omit || [], openings: 4, perOpening: 1 }));
    if (sug.length) {
      menu = sug.map(x => ({ run: async () => { const r = await applyAction(getSession(), 'tool', { tool: 'dm.send', to: p.id, text: x.text, parse: x.parse }); return r.ok ? [] : [r.reason]; } }));
      L.push('Send:', ...sug.map((x, i) => `  ${i + 1}. ${x.text}`));
    }
    L.push(`  or: msg ${whoArg} <text>`);
    return L;
  }

  function access() {
    const t = ts();
    const tree = t.accessTree || [];
    menu = tree.map(a => ({ run: () => request(a.path, 'read') }));
    return ['Access (a number requests read):', ...tree.map((a, i) => `  ${i + 1}. ${a.path} — ${a.label} [${a.verbs.join(', ') || 'none'}]${t.pendingAccess.some(p => p.path === a.path) ? ' (pending)' : ''}`)];
  }

  function request(path, verb = 'read') {
    const r = applyAction(getSession(), 'tool', { tool: 'access.request', path, verb });
    return [r.reason];
  }

  function note(text) {
    if (!text) return ['note <text>'];
    const n = ts().files.filter(f => f.rel.startsWith('notes/')).length + 1;
    const r = applyAction(getSession(), 'tool', { tool: 'file.write', rel: `notes/note-${n}.txt`, name: text.slice(0, 40), text });
    return [r.reason];
  }

  function share(arg) {
    const t = ts(), c = cs();
    const parts = String(arg || '').trim().split(/\s+/);
    const whoArg = parts.pop();
    const f = pick(parts.join(' '), t.files.filter(x => x.owned).map(x => ({ ...x, id: x.rel })), x => x.name);
    const p = pick(whoArg, (t.contacts || []).map(x => ({ id: x.id, name: nameOf(c, x.id) })), x => x.name);
    if (!f || !p) return ['share <your file> <person>'];
    return [applyAction(getSession(), 'tool', { tool: 'file.share', rel: f.rel, to: p.id }).reason];
  }

  function contactsList() {
    const t = ts(), c = cs();
    return ['Contacts:', ...(t.contacts || []).map(x => `  ${nameOf(c, x.id)}${x.role ? ' — ' + x.role : ''}`)];
  }

  function calendarList() {
    return ['Calendar:', ...(ts().appointments || []).map(a => `  ${a.start}–${a.end} ${a.title} · ${a.where}`)];
  }

  function status() {
    const c = cs();
    return [`${c.clock.timeLabel}, ${c.clock.dateLabel}. ${ACT_LABELS[c.act] || c.act}. Fuel ${c.fuel}. ${roomTitle(c.room)}.`];
  }

  // ---------- dispatch ----------

  const PHONE = new Set(['phone', 'p', 'files', 'open', 'msg', 'access', 'request', 'note', 'share', 'contacts', 'calendar']);

  async function command(line) {
    const m = line.trim().match(/^(\S+)\s*(.*)$/);
    if (!m) return [];
    const [, verbRaw, rest] = m;
    const verb = lower(verbRaw);
    if (/^\d+$/.test(verb) && !rest) {
      const item = menu[Number(verb) - 1];
      return item ? await item.run() : ['No such number in the last list.'];
    }
    if (cs().ending && !['look', 'l', 'know', 'status', 'help', '?', 'records'].includes(verb)) return ['The review is over. Reset to play again.'];
    if (PHONE.has(verb)) {
      const no = needPhone();
      if (no) return no;
      usedPhone = true;
    }
    switch (verb) {
      case 'help': case '?': return [HELP];
      case 'look': case 'l': return [look(true)];
      case 'exits': case 'doors': {
        const doors = exits(cs()).filter(d => !d.locked);
        menu = doors.map(d => ({ run: () => go(d.id) }));
        return ['Doors:', ...doors.map((d, i) => `  ${i + 1}. ${d.title} (${d.wall})`)];
      }
      case 'go': case 'walk': return go(rest);
      case 'read': case 'inspect': case 'x': return rest ? readArg(rest) : [look(false)];
      case 'records': return records();
      case 'to': case 'face': return face(rest);
      case 'who': return [peopleLine(cs())];
      case 's': case 'suggest': return suggest(rest);
      case 'say': return rest ? say(rest) : suggest('');
      case 'think': return think(rest);
      case 'keep': {
        const s = getSession();
        if (!s.thought && lastCard) {
          if (!cs().labAccessActive) return ['You have no handset access yet.'];
          const rel = `notes/${lastCard.id}.txt`;
          const r = applyAction(s, 'tool', { tool: 'file.write', rel, name: lastCard.title, text: lastCard.body, kind: 'note' });
          return [r.ok ? `Kept as a note: ${rel}.` : (r.reason || r.error || 'Could not keep that.')];
        }
        const r = applyAction(s, 'thought', { action: 'note' });
        return [r.error || `Kept as a note: ${r.rel}.`];
      }
      case 'close': return act('thought', { action: 'close' });
      case 'know': case 'k': return know();
      case 'file': case 'commit': return act('commit', {});
      case 'phone': case 'p': return phone();
      case 'files': return files();
      case 'open': return open(rest);
      case 'msg': case 'dm': return msg(rest);
      case 'access': return access();
      case 'request': { const [path, verbArg] = rest.split(/\s+/); return path ? request(path, verbArg || 'read') : access(); }
      case 'note': return note(rest);
      case 'share': return share(rest);
      case 'contacts': return contactsList();
      case 'calendar': return calendarList();
      case 'status': return status();
      default: return say(line.trim());
    }
  }

  return {
    /** Banner plus the first room. Call once per session, and again after reset or import. */
    start() {
      bound = getSession();
      seen = null;
      last = null;
      addressee = null;
      menu = [];
      usedPhone = false;
      lastCard = null;
      seen = snapshot();
      seen.visited.add(seen.room);
      last = seen;
      const c = cs();
      return [`The Last Safety Review — ${c.clock.dateLabel}, ${c.clock.timeLabel}. ${ACT_LABELS[c.act] || c.act}.`, 'Type help for commands.', '', look(true)].join('\n');
    },
    async handle(line) {
      if (!last || getSession() !== bound) return { out: this.start(), prompt: prompt() };
      if (!line.trim()) return { out: [look(true), ...changes()].join('\n'), prompt: prompt() };
      const own = await command(line);
      const out = [...own, ...changes()].filter(x => x !== undefined && x !== null);
      return { out: out.join('\n'), prompt: prompt() };
    },
    prompt,
  };
}
