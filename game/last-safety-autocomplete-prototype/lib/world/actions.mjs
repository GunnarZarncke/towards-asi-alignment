/**
 * One entry point for player actions. Server routes, replay (engine.md O-31), tests, and the
 * playtest harness all go through it, so a saved event log replays the same transitions.
 */
import { EDGES } from '../floorplan.mjs';
import { go, inspect, respond, think, thoughtAction, setConceptLinks, dmSend } from '../game.mjs';
import { applyToolCall } from './terminal-host.mjs';
import { CONFIG } from './config.mjs';

export function applyAction(s, action, args = {}) {
  if (s.events.length >= CONFIG.LIMITS.EVENTS) return { ok: false, error: 'This session is full. Reset to play again.', reason: 'This session is full. Reset to play again.' };
  switch (action) {
    case 'go': return go(s, args.room);
    case 'inspect': return inspect(s, args.id);
    case 'respond': return respond(s, args.parse, { addressee: args.addressee || null, text: args.text || '' });
    case 'think': return think(s, args.topic);
    case 'commit': return respond(s, { kind: 'commit', relation: 'about', topic: 'review', open_slot: 'none' }, { text: args.text || '' });
    case 'thought': return thoughtAction(s, args.action);
    case 'dm.send': return dmSend(s, args);
    case 'tool': return applyToolCall(s, args);
    case 'settings': return setConceptLinks(s, args.conceptLinksEnabled);
    default: return { error: `Unknown action ${action}` };
  }
}

/** Shortest door path the badge can open. Headless helper; the UI walks one door at a time. */
export function route(from, to, clearance) {
  const prev = { [from]: null };
  const queue = [from];
  while (queue.length) {
    const x = queue.shift();
    if (x === to) break;
    for (const e of EDGES) {
      if (e.required > clearance) continue;
      const y = e.a === x ? e.b : e.b === x ? e.a : null;
      if (y && !(y in prev)) { prev[y] = x; queue.push(y); }
    }
  }
  if (!(to in prev)) return null;
  const path = [];
  for (let x = to; x !== from; x = prev[x]) path.unshift(x);
  return path;
}

export function walk(s, to) {
  const path = route(s.room, to, s.clearance);
  if (!path) return { error: `No route to ${to}` };
  for (const room of path) {
    const r = go(s, room);
    if (r.error) return r;
  }
  return { room: s.room };
}
