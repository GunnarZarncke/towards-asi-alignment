/**
 * Room layouts as data. Units are metres. Floor spans x ∈ [-W/2, W/2], z ∈ [-D/2, D/2].
 * Walls stand on the back (z = -D/2) and left (x = -W/2). Front and right stay open for the camera; doors may still sit there.
 * Headings are degrees; 0 faces +z (towards the camera side), 90 faces +x.
 * `hotspot` names the scene-view hotspot id a prop answers to. A prop without one is art only.
 * Authored rooms are larger than the plan. Their doors name the same neighbors; generated rooms use the plan's metres.
 */
import { ROOMS, doorsOn } from '../../lib/floorplan.mjs';

export const LAYOUTS = {
  platform: {
    size: [12, 8],
    wallHeight: 2.9,
    wall: '#e3e1db',
    floor: '#c8cec7',
    floorLine: '#b3bbb2',
    floorStyle: 'tiles',
    accent: '#3f7a6c',
    camera: { pos: [7.5, 8.2, 10.5], target: [-0.3, 0.7, -0.4], fov: 30 },
    sun: [-3, 9, -12],
    ceiling: [
      { at: [-0.4, -1.6], w: 2.8, d: 1.05 },
      { at: [-2.2, 1.1], w: 1.35, d: 0.85 },
      { at: [2.6, -0.2], w: 1.7, d: 0.9 },
    ],
    windows: [
      { wall: 'back', at: -3.0, w: 2.0, y0: 0.85, y1: 2.5 },
      { wall: 'back', at: -0.7, w: 2.0, y0: 0.85, y1: 2.5 },
    ],
    doors: [
      { to: 'tech', wall: 'front', at: 0, w: 1.1 },
    ],
    props: [
      { type: 'serverRack', at: [-5.4, -3.35], rot: 90 },
      { type: 'serverRack', at: [-5.4, -2.6], rot: 90 },
      { type: 'serverRack', at: [-5.4, -1.85], rot: 90 },
      { type: 'glassPartition', at: [-4.55, -2.4], rot: 90, opts: { len: 3.2 } },
      { type: 'opsDesk', at: [-0.2, -2.5], rot: 0, hotspot: 'job_log', opts: { lamp: true } },
      { type: 'chair', at: [-0.9, -1.7], rot: 180 },
      { type: 'workstation', at: [-2.4, 1.3], rot: 0, hotspot: 'player_terminal', opts: { lamp: true } },
      { type: 'noraWall', wall: 'back', at: 2.5, y: 1.85 },
      { type: 'cabinet', at: [1.4, -3.7], rot: 0 },
      { type: 'securityCamera', wall: 'left', at: -3.6, y: 2.6 },
      { type: 'standingTable', at: [2.9, 0.9] },
      { type: 'plant', at: [3.7, -3.45], opts: { size: 1 } },
      { type: 'plant', at: [-5.4, 3.45], opts: { size: 1.25 } },
      { type: 'plant', at: [5.3, 3.3], opts: { size: 0.9 } },
    ],
    spots: { pavel: [1.9, -1.2, 20], player: [2.6, 2.4, 200] },
    interact: { job_log: [0.4, -1.5, 180], player_terminal: [-2.4, 2.05, 180] },
  },

  evaluation: {
    size: [12, 8],
    wallHeight: 2.9,
    wall: '#e6e6e1',
    floor: '#d2d5ce',
    floorLine: '#bec2ba',
    floorStyle: 'tiles',
    accent: '#4a6f8a',
    camera: { pos: [7.5, 8.2, 10.5], target: [-0.3, 0.7, -0.4], fov: 30 },
    sun: [-4, 9, -12],
    ceiling: [
      { at: [-1.5, -2.4], w: 3.2, d: 1.1 },
      { at: [1.8, -0.8], w: 2.0, d: 0.95 },
      { at: [0.2, 1.6], w: 1.8, d: 0.85 },
    ],
    windows: [
      { wall: 'back', at: -4.0, w: 2.2, y0: 0.85, y1: 2.5 },
      { wall: 'back', at: -1.4, w: 2.2, y0: 0.85, y1: 2.5 },
    ],
    doors: [
      { to: 'tech', wall: 'front', at: 0, w: 1.1 },
    ],
    props: [
      { type: 'bench', at: [-1.6, -2.9], rot: 0, opts: { len: 3.4, lamp: true } },
      { type: 'chair', at: [-2.4, -2.05], rot: 180 },
      { type: 'chair', at: [-0.8, -2.05], rot: 180 },
      { type: 'bigScreen', at: [2.8, -3.3], rot: 0 },
      { type: 'documentTable', at: [2.3, 0.4], rot: 0, hotspot: 'shutdown_report', opts: { kind: 'binder', lamp: true } },
      { type: 'whiteboard', wall: 'left', at: -1.0, y: 1.55 },
      { type: 'cabinet', at: [-5.6, -3.4], rot: 90 },
      { type: 'securityCamera', wall: 'back', at: -5.5, y: 2.6 },
      { type: 'plant', at: [-5.4, 3.4], opts: { size: 1.1 } },
      { type: 'plant', at: [5.3, 3.2], opts: { size: 1 } },
      { type: 'plant', at: [0.9, -3.55], opts: { size: 0.8 } },
    ],
    spots: { leila: [1.0, -0.3, 25], player: [3.2, 2.6, 210] },
    interact: { shutdown_report: [2.3, 1.25, 180] },
  },

  people: {
    size: [12, 8],
    wallHeight: 2.9,
    wall: '#e8e2da',
    floor: '#c9b9a2',
    floorLine: '#b3a189',
    floorStyle: 'planks',
    accent: '#9a6a4a',
    camera: { pos: [7.5, 8.2, 10.5], target: [-0.3, 0.7, -0.4], fov: 30 },
    sun: [-12, 9, -2],
    ceiling: [
      { at: [-1.3, -2.2], w: 2.2, d: 1.0 },
      { at: [1.5, 0.2], w: 2.4, d: 1.0 },
      { at: [-0.5, 2.0], w: 2.0, d: 0.9 },
    ],
    windows: [
      { wall: 'left', at: -2.4, w: 2.4, y0: 0.85, y1: 2.5 },
      { wall: 'left', at: 0.4, w: 1.6, y0: 0.85, y1: 2.5 },
    ],
    doors: [
      { to: 'tech', wall: 'back', at: -0.2, w: 1.2 },
      { to: 'courtyard', wall: 'right', at: 0, w: 1.0 },
      { to: 'collab', wall: 'front', at: 2.6, w: 1.1 },
    ],
    props: [
      { type: 'desk', at: [-1.4, -2.6], rot: 0, opts: { w: 1.6, d: 0.75, monitor: 'chart', laptop: true, lamp: true } },
      { type: 'chair', at: [-1.4, -3.35], rot: 0 },
      { type: 'bookshelf', at: [0.9, -3.78], rot: 0, opts: { w: 1.6 } },
      { type: 'staffBoard', wall: 'back', at: 2.8, y: 1.7 },
      { type: 'documentTable', at: [2.2, -1.0], rot: 0, hotspot: 'staffing_memo', opts: { kind: 'folder', lamp: true } },
      { type: 'rug', at: [1.6, 1.9], opts: { w: 2.8, d: 2.3 } },
      { type: 'roundTable', at: [1.6, 1.9] },
      { type: 'chair', at: [0.8, 1.9], rot: 90 },
      { type: 'chair', at: [2.4, 1.9], rot: 270 },
      { type: 'chair', at: [1.6, 2.7], rot: 180 },
      { type: 'sofa', at: [-4.95, 2.4], rot: 90 },
      { type: 'securityCamera', wall: 'back', at: -5.6, y: 2.6 },
      { type: 'plant', at: [-5.45, -3.5], opts: { size: 1.1 } },
      { type: 'plant', at: [-3.2, -3.55], opts: { size: 0.85 } },
      { type: 'plant', at: [5.3, 3.2], opts: { size: 1.2 } },
    ],
    spots: { elena: [-0.4, -1.3, 20], player: [3.4, 2.8, 215] },
    interact: { staffing_memo: [2.2, -0.2, 180] },
  },
};

const PALETTE = {
  0: { floor: '#d5e0db', floorLine: '#c3d0cb', wall: '#e6ebe8', accent: '#3f6f74' },
  1: { floor: '#dce3d2', floorLine: '#c9d2be', wall: '#e7ebe3', accent: '#5d7a62' },
  2: { floor: '#e6decc', floorLine: '#d4cbb6', wall: '#ebe6dc', accent: '#8a7340' },
  3: { floor: '#e7d6d1', floorLine: '#d4c2bc', wall: '#efe6e3', accent: '#8a5348' },
};

const DRESS = {
  tech: {
    spot: [0, 0, 90],
    ceiling: [-8, -2.5, 3, 8].map(x => ({ at: [x, 0], w: 1.6, d: 0.4 })),
    props: [
      { type: 'securityCamera', wall: 'back', at: 0.8, y: 2.45 },
      { type: 'postedNote', wall: 'left', at: 0, y: 1.4, hotspot: 'spine_sign' },
    ],
  },
  test: {
    spot: [1.6, 0.6, 200],
    props: [
      { type: 'bench', at: [0, -1.05], rot: 0, opts: { len: 2.8 } },
      { type: 'cabinet', at: [-2.4, -1.35], rot: 0 },
      { type: 'plant', at: [2.4, 1.2], opts: { size: 0.9 } },
      { type: 'postedNote', wall: 'back', at: 1.6, y: 1.45, hotspot: 'bay_placard' },
    ],
  },
  security: {
    spot: [1.2, 0.7, 210],
    props: [
      { type: 'desk', at: [0, -1.05], rot: 0, opts: { monitor: 'dash', lamp: true } },
      { type: 'chair', at: [0, -0.2], rot: 180 },
      { type: 'cabinet', at: [-1.5, -1.4], rot: 0 },
      { type: 'postedNote', wall: 'left', at: 0, y: 1.4, hotspot: 'control_card' },
    ],
  },
  courtyard: {
    spot: [0, -1.1, 0],
    props: [
      { type: 'plant', at: [-1.5, -1.3], opts: { size: 1.15 } },
      { type: 'plant', at: [1.55, -1.15], opts: { size: 1 } },
      { type: 'sofa', at: [0.1, 0.35], rot: 0 },
      { type: 'plant', at: [1.4, 1.15], opts: { size: 0.85 } },
      { type: 'postedNote', at: [-1.15, 1.05], hotspot: 'garden_card', opts: { stand: true } },
    ],
  },
  model: {
    spot: [-1.6, 0.6, 160],
    props: [
      { type: 'workstation', at: [2.3, -0.45], rot: 0, opts: { lamp: true } },
      { type: 'chair', at: [2.3, 0.45], rot: 180 },
      { type: 'plant', at: [-3.2, -1.4], opts: { size: 1 } },
      { type: 'postedNote', wall: 'right', at: 0, y: 1.4, hotspot: 'studio_card' },
    ],
  },
  service: {
    spot: [0.2, 0.4, 180],
    props: [
      { type: 'cabinet', at: [-1.3, -0.85], rot: 0 },
      { type: 'cabinet', at: [-0.3, -0.85], rot: 0 },
      { type: 'postedNote', wall: 'left', at: 0.2, y: 1.35, hotspot: 'kitchen_note' },
    ],
  },
  collab: {
    spot: [-2.4, 0.45, 170],
    props: [
      { type: 'roundTable', at: [2.3, 0.15] },
      { type: 'chair', at: [1.35, 0.15], rot: 90 },
      { type: 'chair', at: [3.25, 0.15], rot: 270 },
      { type: 'plant', at: [-4.6, 0.5], opts: { size: 0.9 } },
      { type: 'postedNote', wall: 'back', at: -2, y: 1.45, hotspot: 'bay_card' },
    ],
  },
  quiet: {
    spot: [-0.8, 0.55, 200],
    props: [
      { type: 'desk', at: [0.7, -0.7], rot: 0, opts: { lamp: true, laptop: true } },
      { type: 'chair', at: [0.7, 0.15], rot: 180 },
      { type: 'postedNote', wall: 'right', at: 0, y: 1.35, hotspot: 'quiet_card' },
    ],
  },
  commons: {
    spot: [0.4, 0.15, 160],
    props: [
      { type: 'sofa', at: [-3.4, 0.15], rot: 90 },
      { type: 'plant', at: [-4.7, -0.85], opts: { size: 1 } },
      { type: 'standingTable', at: [1.2, 0.2], hotspot: 'visitor_card', opts: { card: true } },
    ],
    interact: { visitor_card: [1.2, 0.75, 180] },
  },
  review: {
    spot: [0.4, 0.45, 190],
    props: [
      { type: 'bigScreen', at: [3.2, -1.05], rot: 0 },
      { type: 'roundTable', at: [-1.6, 0.2] },
      { type: 'chair', at: [-2.55, 0.2], rot: 90 },
      { type: 'chair', at: [-0.65, 0.2], rot: 270 },
      { type: 'whiteboard', wall: 'back', at: 2.2, y: 1.55, hotspot: 'review_agenda' },
    ],
  },
};

function addWindow(windows, wall, span) {
  const w = Math.min(1.8, span - 1.2);
  if (w < 0.8) return;
  windows.push({ wall, at: 0, w, y0: 0.85, y1: 2.4 });
}

function exteriorWindows(id, room, doors) {
  if (id === 'courtyard') return [{ wall: 'back', at: 0, w: 3.2, y0: 0.75, y1: 2.45 }];
  const windows = [];
  const blocked = new Set(doors.map(d => d.wall));
  if (room.y === 0 && !blocked.has('back')) addWindow(windows, 'back', room.w);
  if (room.x === 0 && !blocked.has('left')) addWindow(windows, 'left', room.d);
  if (Math.abs(room.x + room.w - 22) < 1e-6 && !blocked.has('right')) addWindow(windows, 'right', room.d);
  if (Math.abs(room.y + room.d - 17) < 1e-6 && !blocked.has('front')) addWindow(windows, 'front', room.w);
  return windows;
}

function generatedLayout(id) {
  const room = ROOMS[id];
  const doors = doorsOn(id).map(({ to, wall, at, w, required }) => ({ to, wall, at, w, required }));
  const dress = DRESS[id] || {};
  const tone = id === 'courtyard'
    ? { floor: '#cfe3c4', floorLine: '#b7d0aa', wall: '#e7f0e4', accent: '#3d7a49' }
    : PALETTE[room.level];
  const span = Math.max(room.w, room.d);
  return {
    size: [room.w, room.d],
    wallHeight: 2.9,
    wall: tone.wall,
    floor: tone.floor,
    floorLine: tone.floorLine,
    floorStyle: 'tiles',
    accent: tone.accent,
    camera: { pos: [span * 0.45, 7.5, span * 0.62], target: [0, 0.7, 0], fov: 32 },
    sun: [-4, 10, -6],
    ceiling: dress.ceiling || [{ at: [0, 0], w: Math.min(2.2, room.w * 0.45), d: Math.min(0.9, room.d * 0.35) }],
    windows: exteriorWindows(id, room, doors),
    doors,
    props: dress.props || [],
    spots: { player: dress.spot || [0, 0, 180] },
    interact: dress.interact,
  };
}

export function layoutFor(id) {
  if (LAYOUTS[id]) return LAYOUTS[id];
  if (ROOMS[id]) return generatedLayout(id);
  return LAYOUTS.platform;
}
