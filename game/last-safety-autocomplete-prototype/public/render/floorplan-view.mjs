/** Courtyard plan overlay. Clicks ask the engine to walk one door; this view does not move the player. */
import { ROOMS, doorBetween } from '../../lib/floorplan.mjs';

let root = null;
let svgHost = null;
let svgPromise = null;
let onGo = null;
let onClose = null;
let current = null;
let clearance = 2;
let focus = null;
let note = '';

function esc(t) {
  return String(t).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
}

function ensure() {
  if (root) return;
  root = document.createElement('div');
  root.className = 'floorplan-scrim';
  root.hidden = true;
  root.innerHTML = `<div class="floorplan-sheet" role="dialog" aria-modal="true" aria-label="Lab floorplan">
    <div class="floorplan-map" data-map></div>
    <aside class="floorplan-side">
      <div class="floorplan-side-top"><span class="eyebrow">LAB FLOOR</span><button type="button" class="minor" data-close>Back to the room</button></div>
      <p class="floorplan-badge" data-badge></p>
      <h3 data-title></h3>
      <div class="status" data-status></div>
      <p data-role></p>
      <p class="small muted" data-meta></p>
      <p class="floorplan-legend"><span><i style="background:#E2EBE7"></i>L0</span><span><i style="background:#E8EEE0"></i>L1</span><span><i style="background:#F3E9D1"></i>L2</span><span><i style="background:#EFDCD6"></i>L3</span><span><i style="background:#D9EACD"></i>Court</span></p>
    </aside>
  </div>`;
  document.body.appendChild(root);
  svgHost = root.querySelector('[data-map]');
  root.querySelector('[data-close]').onclick = () => onClose?.();
  root.addEventListener('click', e => { if (e.target === root) onClose?.(); });
  root.querySelector('.floorplan-sheet').addEventListener('click', e => e.stopPropagation());
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && root && !root.hidden) {
      e.preventDefault();
      onClose?.();
    }
  });
}

function loadSvg() {
  if (!svgPromise) {
    svgPromise = fetch('/floorplan.svg').then(res => {
      if (!res.ok) throw new Error('Floorplan drawing failed to load');
      return res.text();
    });
  }
  return svgPromise;
}

function statusFor(id) {
  if (note && id === focus) return note;
  if (id === current) return 'You are here';
  const door = current ? doorBetween(current, id) : null;
  if (!door) return 'No door from here';
  if (door.required > clearance) return `Needs clearance ${door.required}`;
  return 'Door from here';
}

function paint() {
  if (!svgHost) return;
  for (const el of svgHost.querySelectorAll('.room')) {
    const id = el.dataset.room;
    const door = current ? doorBetween(current, id) : null;
    el.classList.toggle('here', id === current);
    el.classList.toggle('active', id === focus);
    el.classList.toggle('next', Boolean(door) && door.required <= clearance && id !== current);
    el.classList.toggle('gated', Boolean(door) && door.required > clearance);
    if (id === current) el.setAttribute('aria-current', 'location');
    else el.removeAttribute('aria-current');
  }
  const room = ROOMS[focus] || ROOMS[current];
  if (!room) return;
  root.querySelector('[data-badge]').textContent = `Badge clearance ${clearance}`;
  root.querySelector('[data-title]').textContent = room.title;
  root.querySelector('[data-status]').textContent = statusFor(focus || current);
  root.querySelector('[data-role]').textContent = room.role;
  root.querySelector('[data-meta]').textContent = `${room.area} m² · ${room.people} · ${room.windows}`;
}

function bindRooms() {
  for (const el of svgHost.querySelectorAll('.room')) {
    el.addEventListener('click', () => {
      const id = el.dataset.room;
      if (!id || id === current) {
        focus = current;
        note = '';
        paint();
        return;
      }
      onGo?.(id);
    });
    el.addEventListener('keydown', e => {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      e.preventDefault();
      el.click();
    });
  }
}

export function floorplanOpen() {
  return Boolean(root && !root.hidden);
}

export function openFloorplan(view, handlers = {}) {
  ensure();
  onGo = handlers.onGo || onGo;
  onClose = handlers.onClose || onClose;
  current = view.roomId;
  clearance = view.clearance;
  focus = view.roomId;
  note = '';
  root.hidden = false;
  if (!svgHost.querySelector('svg')) {
    svgHost.innerHTML = '<p class="floorplan-loading">Loading the plan…</p>';
    loadSvg().then(text => {
      svgHost.innerHTML = text;
      bindRooms();
      paint();
    }).catch(err => {
      svgHost.innerHTML = `<p class="floorplan-loading">${esc(err.message)}</p>`;
    });
  } else paint();
  root.querySelector('[data-close]')?.focus();
}

export function closeFloorplan() {
  if (root) root.hidden = true;
}

/** After a refused move, keep the plan open and say why. */
export function floorplanNotice(roomId, message) {
  if (!floorplanOpen()) return;
  focus = roomId;
  note = message;
  paint();
}

export function syncFloorplan(view, handlers = {}) {
  if (!floorplanOpen()) return;
  onGo = handlers.onGo || onGo;
  onClose = handlers.onClose || onClose;
  current = view.roomId;
  clearance = view.clearance;
  focus = view.roomId;
  note = '';
  paint();
}
