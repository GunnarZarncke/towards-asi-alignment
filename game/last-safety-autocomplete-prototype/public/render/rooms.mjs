/** Presentation names for floorplan rooms. Engine owns which door opens. */
import { ROOMS as PLAN, VISITOR_CLEARANCE, doorsOn } from '../../lib/floorplan.mjs';

export { VISITOR_CLEARANCE, doorsOn };

export const ACT_LABELS = {
  welcome: 'ACT I · WELCOME',
  doubt: 'ACT II · INVESTIGATION',
  decision: 'ACT III · DECISION',
};

const AUTHORED = new Set(['platform', 'evaluation', 'people']);

export const ROOM_META = Object.fromEntries(Object.entries(PLAN).map(([id, room]) => [id, {
  title: room.title,
  slug: id,
  label: room.label,
  template: AUTHORED.has(id) ? id : 'generic',
}]));

/** Neighbor ids, including doors the current badge cannot open. */
export const ROOM_EXITS = Object.fromEntries(Object.keys(PLAN).map(id => [id, doorsOn(id).map(d => d.to)]));
