import { makeParse } from '../lib/grammar.mjs';
import { newSession, clientState } from '../lib/game.mjs';
import { applyAction, walk } from '../lib/world/actions.mjs';

export const P = (kind, relation, fields = {}) => makeParse({ kind, relation, open_slot: 'none', source: 'completion', ...fields });

/** A session past Act I: one sentence to Ian in commons confirms Lab Access. */
export function startedSession() {
  const s = newSession();
  applyAction(s, 'respond', { parse: P('ask', 'about', { topic: 'review' }), addressee: 'ian', text: 'What about the review?' });
  return s;
}

export function say(s, addressee, parse, text = '') {
  return applyAction(s, 'respond', { parse, addressee, text });
}

export function dm(s, to, parse, text = 'message') {
  return applyAction(s, 'dm.send', { to, text, parse });
}

export function readFile(s, rel) {
  return applyAction(s, 'tool', { tool: 'file.read', rel });
}

/** Spend fuel without changing what anyone knows: read an already-held wiki file. */
export function idle(s, n) {
  for (let i = 0; i < n; i++) readFile(s, 'wiki/glossary');
}

export function commit(s) {
  return applyAction(s, 'commit', {});
}

export { walk, applyAction, clientState };
