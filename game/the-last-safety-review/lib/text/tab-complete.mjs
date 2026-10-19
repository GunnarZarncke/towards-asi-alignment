/**
 * Tab completion for speech and console commands (terminal readline + browser text-input).
 */
import { clientState, cleanParse } from '../game.mjs';
import { terminalState } from '../world/terminal-host.mjs';
import { makeParse } from '../grammar.mjs';
import { parseUtterance } from '../llm.mjs';
import { doorsOn, ROOMS } from '../floorplan.mjs';
import { getCandidates, insertFragment, localPrefixParse, RANKING } from '../../public/grammar.js';
import { CONSOLE_COMMANDS, utteranceSlice } from '../../public/text-tab-slice.mjs';
import { presentIds } from './view.mjs';

export { CONSOLE_COMMANDS, utteranceSlice } from '../../public/text-tab-slice.mjs';

export const PAGE = RANKING.PAGE_SIZE;

function channelFor(state) {
  return presentIds(state).length ? 'person' : 'think';
}

function facing(state) {
  const here = presentIds(state);
  const asker = state.pendingQuestion?.npc;
  return here.includes(asker) ? asker : here[0] || null;
}

async function resolveParse(session, utterance, actorId = null) {
  const text = utterance.trimEnd();
  if (!text.trim()) return makeParse();
  const local = localPrefixParse(text);
  if (local) return local;
  const who = actorId ?? facing(clientState(session));
  const parse = await parseUtterance(
    { text, known: [...session.vocab], history: session.conversations, actorId: who },
    session.usage,
  );
  return cleanParse({ ...parse, source: parse.source || 'llm' }, session);
}

function contactChoices(state, terminal) {
  return (terminal?.contacts || []).map(c => ({
    id: c.id,
    name: state.actors?.[c.id]?.name || c.id,
  }));
}

function pickContact(token, state, terminal) {
  const q = String(token ?? '').trim().toLowerCase();
  if (!q) return null;
  const items = contactChoices(state, terminal);
  return items.find(x => q === x.id.toLowerCase() || q === x.name.toLowerCase())
    || items.find(x => matchPrefixIgnoreCase(q, x.name, x.id))
    || null;
}

/** @returns {{ prefix: string, contactToken: string, message: string } | null} */
export function parseMsgLine(line) {
  const lead = String(line ?? '').match(/^\s*/)?.[0] || '';
  const body = String(line ?? '').slice(lead.length);
  const m = body.match(/^(msg|dm)\s+(\S+)(?:\s+(.*))?$/i);
  if (!m) return null;
  return {
    prefix: `${lead}${m[1]} ${m[2]} `,
    contactToken: m[2],
    message: m[3] ?? '',
  };
}

async function msgSpeechCompletions(session, line, page, state, terminal) {
  const parsed = parseMsgLine(line);
  if (!parsed || !terminal?.labAccessActive) return null;
  const contact = pickContact(parsed.contactToken, state, terminal);
  if (!contact) return null;
  const exact = parsed.contactToken.toLowerCase() === contact.id.toLowerCase()
    || parsed.contactToken.toLowerCase() === contact.name.toLowerCase();
  const rest = String(line ?? '').match(/^\s*(?:msg|dm)\s+\S+\s*(.*)$/i)?.[1];
  if (!exact && !rest?.length && !String(line ?? '').match(/^\s*(?:msg|dm)\s+\S+\s+/i)) return null;

  const { prefix, message } = parsed;
  const thread = terminal.threads?.find(t => t.with === contact.id);
  const omit = thread?.omit || [];
  const channel = contact.id === 'nora' ? 'nora' : 'person';
  const lines = [];
  if (!message.trim()) {
    for (const s of thread?.suggestions || []) lines.push(prefix + s.phrase);
  }
  const parse = await resolveParse(session, message, contact.id);
  const all = getCandidates({
    state,
    parse,
    text: message,
    addressees: [contact.id],
    channel,
    omit,
  });
  for (const opt of all) {
    lines.push(prefix + insertFragment(message, opt, parse.unfinished));
  }
  const start = page * PAGE;
  return lines.slice(start, start + PAGE);
}

/** Case-insensitive prefix match on display label and optional id slug. */
export function matchPrefixIgnoreCase(q, label, id = '') {
  const a = String(q ?? '').trim().toLowerCase();
  if (!a) return true;
  const b = String(label ?? '').toLowerCase();
  const slug = String(id ?? '').toLowerCase();
  return b.startsWith(a) || slug.startsWith(a);
}

export function reachableRoomChoices(state) {
  return doorsOn(state.room)
    .filter(d => d.required <= state.clearance)
    .map(d => ({ id: d.to, title: ROOMS[d.to]?.title || d.to }));
}

function fileHits(files, rest) {
  return files.filter(f => matchPrefixIgnoreCase(rest, f.name, f.rel)
    || matchPrefixIgnoreCase(rest, f.rel.split('/').pop() || f.rel, f.rel));
}

/** @returns {string[] | null} null → treat line as speech */
function commandCompletions(line, state, terminal, { saveFile = '' } = {}) {
  const raw = String(line ?? '');
  const lead = raw.match(/^\s*/)?.[0] || '';
  const t = raw.slice(lead.length);
  if (!t) return null;

  const cmd = t.match(/^(\S+)\s*(.*)$/);
  if (!cmd) return null;
  const verb = cmd[1].toLowerCase();
  const rest = cmd[2] || '';

  if (!rest.trim() && !CONSOLE_COMMANDS.has(verb)) {
    const verbs = [...CONSOLE_COMMANDS].filter(c => c.startsWith(verb));
    if (verbs.length) return verbs.map(v => `${lead}${v} `);
    return null;
  }
  if (!CONSOLE_COMMANDS.has(verb)) return null;

  const afterVerb = `${lead}${cmd[1]} `;

  if (verb === 'go' || verb === 'walk') {
    const all = Object.keys(ROOMS).map(id => ({ id, title: ROOMS[id]?.title || id }));
    const pool = rest.trim() ? all : reachableRoomChoices(state);
    const hits = pool.filter(r => matchPrefixIgnoreCase(rest, r.title, r.id));
    return hits.map(r => `${afterVerb}${r.title}`);
  }
  if (verb === 'to' || verb === 'face') {
    const people = presentIds(state).map(id => ({ id, name: state.actors[id].name }));
    const hits = people.filter(p => matchPrefixIgnoreCase(rest, p.name, p.id));
    return hits.map(p => `${afterVerb}${p.name}`);
  }
  if (verb === 'read' || verb === 'inspect' || verb === 'x') {
    const screens = state.evidence.filter(e => e.room === state.room);
    const hits = screens.filter(e => matchPrefixIgnoreCase(rest, e.title, e.id));
    return hits.map(e => `${afterVerb}${e.title}`);
  }
  if (verb === 'open') {
    const files = terminal?.files || [];
    const hits = rest.trim() ? fileHits(files, rest) : files;
    return hits.map(f => `${afterVerb}${f.name}`);
  }
  if (verb === 'save' && saveFile) {
    if (!rest.trim()) return [`${afterVerb}${saveFile}`];
    if (saveFile.toLowerCase().startsWith(rest.trim().toLowerCase())) return [`${afterVerb}${saveFile}`];
  }
  if (verb === 'load' && saveFile) {
    if (!rest.trim()) return [`${afterVerb}${saveFile}`];
    if (saveFile.toLowerCase().startsWith(rest.trim().toLowerCase())) return [`${afterVerb}${saveFile}`];
  }
  if (verb === 'say' && !rest.trim()) return [afterVerb.trimEnd()];

  if (verb === 'msg' || verb === 'dm') {
    if (!terminal?.labAccessActive) return [];
    const people = contactChoices(state, terminal);
    if (!rest.trim()) return people.map(p => `${afterVerb}${p.name} `);
    const tok = rest.split(/\s+/)[0] || '';
    const contact = pickContact(tok, state, terminal);
    const exact = contact && (tok.toLowerCase() === contact.id.toLowerCase()
      || tok.toLowerCase() === contact.name.toLowerCase());
    if (contact && (exact || rest.includes(' '))) return null;
    const hits = people.filter(p => matchPrefixIgnoreCase(tok, p.name, p.id));
    return hits.map(p => `${afterVerb}${p.name} `);
  }

  if (!rest.trim()) return [afterVerb.trimEnd()];
  return [];
}

/**
 * Up to PAGE full-line completions for readline (page 0 = first five).
 * @param {object} session engine session
 * @param {string} line current input line
 * @param {number} page 0-based page index
 */
export async function tabCompleteLines(session, line, page = 0, opts = {}) {
  const state = clientState(session);
  const terminal = terminalState(session);
  const msgHits = await msgSpeechCompletions(session, line, page, state, terminal);
  if (msgHits !== null) return msgHits;

  const cmd = commandCompletions(line, state, terminal, opts);
  if (cmd !== null) {
    const start = page * PAGE;
    return cmd.slice(start, start + PAGE);
  }

  const slice = utteranceSlice(line);
  if (!slice) return [];

  const parse = await resolveParse(session, slice.utterance);
  const here = presentIds(state);
  const alone = !here.length;
  const all = getCandidates({
    state,
    parse,
    text: slice.utterance,
    addressees: alone ? [] : here,
    channel: channelFor(state),
  });
  const start = page * PAGE;
  return all.slice(start, start + PAGE).map(opt =>
    slice.prefix + insertFragment(slice.utterance, opt, parse.unfinished),
  );
}
