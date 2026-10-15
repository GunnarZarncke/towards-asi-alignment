import { makeParse } from '../lib/grammar.mjs';
import { newSession, clientState } from '../lib/game.mjs';
import { CONFIG } from '../lib/world/config.mjs';
import { applyAction, walk } from '../lib/world/actions.mjs';

export const P = (kind, relation, fields = {}) => makeParse({ kind, relation, open_slot: 'none', source: 'completion', ...fields });

/**
 * Lab Access is live and the clock has reached Ian’s investor update, so the act is doubt.
 * The clock moves by logged walks, so a save replays to the same state.
 */
export function startedSession() {
  const s = newSession();
  applyAction(s, 'respond', { parse: P('ask', 'about', { topic: 'review' }), addressee: 'ian', text: 'What about the review?' });
  let guard = 0;
  while (s.minute < CONFIG.DOUBT_AT && guard < 80) {
    applyAction(s, 'go', { room: s.room === 'commons' ? 'collab' : 'commons' });
    guard++;
  }
  if (s.room !== 'commons') applyAction(s, 'go', { room: 'commons' });
  return s;
}

export function say(s, addressee, parse, text = '') {
  return applyAction(s, 'respond', { parse, addressee, text });
}

export function dm(s, to, parse, text = 'message') {
  return applyAction(s, 'tool', { tool: 'dm.send', to, text, parse });
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
