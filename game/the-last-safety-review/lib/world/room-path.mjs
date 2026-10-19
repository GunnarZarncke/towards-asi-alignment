/**
 * Shortest staff paths on the lab floorplan (clearance ignored — staff keys).
 */
import { EDGES, ROOMS } from '../floorplan.mjs';

export const STAFF_ENTRY = 'commons';

const ADJ = (() => {
  const m = new Map(Object.keys(ROOMS).map(id => [id, []]));
  for (const e of EDGES) {
    m.get(e.a).push(e.b);
    m.get(e.b).push(e.a);
  }
  return m;
})();

/** Shortest room id path including start and end; null if unreachable. */
export function roomPath(from, to) {
  if (!from || !to) return null;
  if (from === to) return [to];
  if (!ROOMS[from] || !ROOMS[to]) return null;
  const prev = new Map([[from, null]]);
  const q = [from];
  while (q.length) {
    const u = q.shift();
    for (const v of ADJ.get(u) || []) {
      if (prev.has(v)) continue;
      prev.set(v, u);
      if (v === to) {
        const path = [to];
        for (let x = v; prev.get(x); x = prev.get(x)) path.push(prev.get(x));
        path.reverse();
        return path;
      }
      q.push(v);
    }
  }
  return null;
}

/** Next placement room when walking toward goal (one edge per engine tick). */
export function transitStep(n, goalRoom, goalPresence) {
  if (goalPresence !== 'body') {
    n.transit = null;
    return { room: goalRoom, presence: goalPresence };
  }
  if (goalRoom == null || goalPresence === 'absent') {
    n.transit = null;
    return { room: goalRoom, presence: goalPresence };
  }
  const cur = n.presence === 'absent' ? null : n.room;
  if (cur === goalRoom && n.presence === goalPresence) {
    n.transit = null;
    return { room: goalRoom, presence: goalPresence };
  }

  const start = cur ?? STAFF_ENTRY;
  if (!n.transit || n.transit.goal !== goalRoom) {
    const via = roomPath(start, goalRoom);
    if (!via || via.length <= 1) {
      n.transit = null;
      return { room: goalRoom, presence: goalPresence };
    }
    n.transit = { goal: goalRoom, via, at: via.indexOf(cur) };
    if (cur == null) n.transit.at = 0;
    else if (n.transit.at < 0) {
      n.transit = null;
      return { room: goalRoom, presence: goalPresence };
    }
  }

  const { via, at } = n.transit;
  if (cur == null) return { room: via[0], presence: 'body' };
  if (cur !== via[at]) return { room: via[at], presence: 'body' };
  if (at < via.length - 1) return { room: via[at + 1], presence: 'body' };
  n.transit = null;
  return { room: goalRoom, presence: goalPresence };
}
