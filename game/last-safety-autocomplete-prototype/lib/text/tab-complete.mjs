/**
 * Tab completion for speech and console commands (terminal readline + browser text-input).
 */
import { clientState, cleanParse } from '../game.mjs';
import { terminalState } from '../world/terminal-host.mjs';
import { makeParse } from '../grammar.mjs';
import { parseUtterance } from '../llm.mjs';
import { doorsOn, ROOMS } from '../floorplan.mjs';
import { getCandidates, insertFragment, localPrefixParse, RANKING } from '../../public/grammar.js';
import { presentIds } from './view.mjs';

export const PAGE = RANKING.PAGE_SIZE;

export const CONSOLE_COMMANDS = new Set([
  'help', '?', 'look', 'l', 'exits', 'doors', 'go', 'walk', 'read', 'inspect', 'x', 'records',
  'to', 'face', 'who', 's', 'suggest', 'think', 'keep', 'close', 'know', 'k', 'file', 'commit',
  'phone', 'p', 'files', 'open', 'msg', 'dm', 'access', 'request', 'note', 'share', 'contacts',
  'calendar', 'status', 'quit', 'save', 'load', 'reset',
]);

/** @returns {{ utterance: string, prefix: string } | null} */
export function utteranceSlice(line) {
  const raw = String(line ?? '');
  const say = raw.match(/^say\s+(.*)$/i);
  if (say) return { utterance: say[1], prefix: raw.slice(0, raw.length - say[1].length) };
  const trimmed = raw.trimStart();
  const verb = trimmed.match(/^(\S+)/)?.[1]?.toLowerCase();
  if (verb && CONSOLE_COMMANDS.has(verb)) return null;
  if (/^\d+$/.test(trimmed)) return null;
  return { utterance: raw, prefix: '' };
}

function channelFor(state) {
  return presentIds(state).length ? 'person' : 'think';
}

function facing(state) {
  const here = presentIds(state);
  const asker = state.pendingQuestion?.npc;
  return here.includes(asker) ? asker : here[0] || null;
}

async function resolveParse(session, utterance) {
  const text = utterance.trimEnd();
  if (!text.trim()) return makeParse();
  const local = localPrefixParse(text);
  if (local) return local;
  const actorId = facing(clientState(session));
  const parse = await parseUtterance(
    { text, known: [...session.vocab], history: session.conversations, actorId },
    session.usage,
  );
  return cleanParse({ ...parse, source: parse.source || 'llm' }, session);
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
