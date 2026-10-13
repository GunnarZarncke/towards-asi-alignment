/**
 * Verified courtyard plan. Metres from the north-west corner of the 22 × 17 m envelope.
 * +x is east, +y is south. Each door sits on one shared edge.
 * `required` is the badge clearance that opens that door.
 * Drawing: public/floorplan.svg.
 */

export const VISITOR_CLEARANCE = 2;

/** @type {Record<string, {title: string, level: number, area: number, x: number, y: number, w: number, d: number, people: string, role: string, windows: string, label: string}>} */
export const ROOMS = {
  platform: {
    title: 'Platform Operations', level: 2, area: 23.1, x: 0, y: 0, w: 5.5, d: 4.2,
    people: 'Pavel', role: 'Runtime queues, deployment pipeline, durable tasks and tool permissions.',
    windows: 'North and west exterior', label: 'Runtime · queues · tool permissions',
  },
  test: {
    title: 'Controlled Test Bay', level: 3, area: 27.3, x: 5.5, y: 0, w: 6.5, d: 4.2,
    people: 'Leila / Pavel (authorized)', role: 'Isolated experiments and model shutdown tests.',
    windows: 'North screened exterior', label: 'Shutdown tests · restricted',
  },
  evaluation: {
    title: 'Evaluation Suite', level: 2, area: 23.1, x: 12, y: 0, w: 5.5, d: 4.2,
    people: 'Leila', role: 'Safety case, testing specifications and remote user interview.',
    windows: 'North exterior', label: 'Certification · test harness',
  },
  security: {
    title: 'Security Control', level: 3, area: 18.9, x: 17.5, y: 0, w: 4.5, d: 4.2,
    people: 'Farah', role: 'Camera feeds, access histories, identity and permission records.',
    windows: 'North and east screened exterior', label: 'Cameras · access records',
  },
  tech: {
    title: 'Technical Circulation', level: 2, area: 35.2, x: 0, y: 4.2, w: 22, d: 1.6,
    people: 'Transit only', role: 'Restricted 1.6 m corridor serving the four technical rooms. Its glazing overlooks the courtyard.',
    windows: 'South onto the open courtyard', label: 'Technical spine · 1.6 m',
  },
  people: {
    title: 'People + Product', level: 1, area: 38.3, x: 0, y: 5.8, w: 8.5, d: 4.5,
    people: 'Elena / Daniel', role: 'Task matching, staffing, promotions, product metrics and release planning.',
    windows: 'West exterior and east courtyard', label: 'Staffing · matching · reviews',
  },
  courtyard: {
    title: 'Open-air Courtyard', level: 1, area: 22.5, x: 8.5, y: 5.8, w: 5, d: 4.5,
    people: 'Anyone taking a break', role: 'An outdoor place for rest and informal conversation. Three entrances.',
    windows: 'Open to the sky', label: 'Open sky',
  },
  model: {
    title: 'Model Studio', level: 1, area: 38.3, x: 13.5, y: 5.8, w: 8.5, d: 4.5,
    people: 'Jun', role: 'Model demonstrations, behavior analysis and transcript investigation.',
    windows: 'East exterior and west courtyard', label: 'Demos · transcripts',
  },
  service: {
    title: 'Staff Services', level: 1, area: 17, x: 0, y: 10.3, w: 5, d: 3.4,
    people: 'Staff facilities', role: 'WC, lockers, kitchenette and service storage.',
    windows: 'West exterior', label: 'WC · lockers · kitchenette',
  },
  collab: {
    title: 'Collaboration Bay', level: 1, area: 40.8, x: 5, y: 10.3, w: 12, d: 3.4,
    people: 'Shared work', role: 'Main pass-through and social workspace, with access to the courtyard and both adjacent teams.',
    windows: 'North courtyard', label: 'Shared work · pass-through',
  },
  quiet: {
    title: 'Quiet / Support', level: 1, area: 17, x: 17, y: 10.3, w: 5, d: 3.4,
    people: 'Ad hoc individual use', role: 'A small retreat for confidential calls, focused work or storing equipment.',
    windows: 'East exterior', label: 'Calls · focused work',
  },
  commons: {
    title: 'Commons / Arrival', level: 0, area: 36.3, x: 0, y: 13.7, w: 11, d: 3.3,
    people: 'Mara welcomes the visitor', role: 'Arrival, seating and introductory conversations. The main entrance is on the south wall.',
    windows: 'South and west exterior', label: 'Arrival · main entrance',
  },
  review: {
    title: 'Review Room', level: 0, area: 36.3, x: 11, y: 13.7, w: 11, d: 3.3,
    people: 'Mara / final meeting', role: 'Formal external and executive conversations. The final review returns to the front of the building.',
    windows: 'South and east exterior', label: 'Meetings · final review',
  },
};

/**
 * axis `h`: the wall runs east–west. `at` is metres south of the north exterior.
 * `from` and `to` are metres east of the west exterior.
 * axis `v`: the wall runs north–south. `at` is metres east. `from` and `to` are metres south.
 */
export const EDGES = [
  { a: 'commons', b: 'review', required: 0, axis: 'v', at: 11, from: 15.15, to: 16.25 },
  { a: 'commons', b: 'collab', required: 1, axis: 'h', at: 13.7, from: 7.6, to: 8.8 },
  { a: 'review', b: 'collab', required: 1, axis: 'h', at: 13.7, from: 13.7, to: 14.9 },
  { a: 'collab', b: 'service', required: 1, axis: 'v', at: 5, from: 11.5, to: 12.5 },
  { a: 'collab', b: 'quiet', required: 1, axis: 'v', at: 17, from: 11.5, to: 12.5 },
  { a: 'people', b: 'collab', required: 1, axis: 'h', at: 10.3, from: 6.4, to: 7.5 },
  { a: 'model', b: 'collab', required: 1, axis: 'h', at: 10.3, from: 14.5, to: 15.6 },
  { a: 'courtyard', b: 'collab', required: 1, axis: 'h', at: 10.3, from: 10.4, to: 11.6 },
  { a: 'people', b: 'courtyard', required: 1, axis: 'v', at: 8.5, from: 7.55, to: 8.55 },
  { a: 'model', b: 'courtyard', required: 1, axis: 'v', at: 13.5, from: 7.55, to: 8.55 },
  { a: 'people', b: 'tech', required: 2, axis: 'h', at: 5.8, from: 3.6, to: 4.8 },
  { a: 'model', b: 'tech', required: 2, axis: 'h', at: 5.8, from: 17.25, to: 18.45 },
  { a: 'platform', b: 'tech', required: 2, axis: 'h', at: 4.2, from: 2.2, to: 3.3 },
  { a: 'test', b: 'tech', required: 3, axis: 'h', at: 4.2, from: 8.15, to: 9.35 },
  { a: 'evaluation', b: 'tech', required: 2, axis: 'h', at: 4.2, from: 14.1, to: 15.2 },
  { a: 'security', b: 'tech', required: 3, axis: 'h', at: 4.2, from: 19.1, to: 20.3 },
];

export function doorBetween(a, b) {
  return EDGES.find(e => (e.a === a && e.b === b) || (e.a === b && e.b === a)) || null;
}

function wallOf(room, edge) {
  if (edge.axis === 'h') {
    if (Math.abs(edge.at - room.y) < 1e-6) return 'back';
    if (Math.abs(edge.at - (room.y + room.d)) < 1e-6) return 'front';
  } else {
    if (Math.abs(edge.at - room.x) < 1e-6) return 'left';
    if (Math.abs(edge.at - (room.x + room.w)) < 1e-6) return 'right';
  }
  return null;
}

/** Doors of one room in local metres: origin at the room centre, +x east, +z south (toward the camera). */
export function doorsOn(roomId) {
  const room = ROOMS[roomId];
  if (!room) return [];
  const cx = room.x + room.w / 2;
  const cz = room.y + room.d / 2;
  const out = [];
  for (const edge of EDGES) {
    if (edge.a !== roomId && edge.b !== roomId) continue;
    const wall = wallOf(room, edge);
    if (!wall) throw new Error(`Door ${edge.a}–${edge.b} is not on the boundary of ${roomId}`);
    const mid = (edge.from + edge.to) / 2;
    const along = wall === 'left' || wall === 'right' ? mid - cz : mid - cx;
    out.push({
      to: edge.a === roomId ? edge.b : edge.a,
      wall,
      at: along,
      w: edge.to - edge.from,
      required: edge.required,
    });
  }
  return out;
}

export function passageError(from, to, clearance) {
  if (!ROOMS[to]) return 'Unknown room.';
  if (from === to) return null;
  const edge = doorBetween(from, to);
  if (!edge) return 'No door from here.';
  if (edge.required > clearance) return 'That door needs a higher clearance.';
  return null;
}

/** Rooms reachable from `origin` through doors the badge can open. */
export function reachable(clearance, origin = 'commons') {
  const seen = new Set([origin]);
  let changed = true;
  while (changed) {
    changed = false;
    for (const edge of EDGES) {
      if (edge.required > clearance) continue;
      if (seen.has(edge.a) && !seen.has(edge.b)) { seen.add(edge.b); changed = true; }
      else if (seen.has(edge.b) && !seen.has(edge.a)) { seen.add(edge.a); changed = true; }
    }
  }
  return seen;
}
