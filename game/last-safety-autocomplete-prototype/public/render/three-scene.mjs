/**
 * Live Three.js room renderer. Draws a SceneView (see scene-view.mjs); never decides outcomes.
 * Person positions are presentation state kept here, not engine state.
 */
import * as THREE from 'three';
import { createKit } from './kit.mjs';
import { layoutFor } from './layouts.mjs';
import { ACT_PRESETS, COLOR_KEYS, NUMBER_KEYS } from './lighting.mjs';
import { Walker, appearanceFor } from './person.mjs';
import { buildRoom, WALL_T } from './room.mjs';

const DEG = Math.PI / 180;
const GROUND = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);

export function webglAvailable() {
  try {
    const c = document.createElement('canvas');
    return Boolean(c.getContext('webgl2') || c.getContext('webgl'));
  } catch {
    return false;
  }
}

function el(tag, className, parent) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  parent?.appendChild(e);
  return e;
}

function esc(t) {
  return String(t).replace(/[&<>"']/g, x => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[x]));
}

function disposeTree(root) {
  const seen = new Set();
  root.traverse(o => {
    if (o.geometry && !seen.has(o.geometry)) {
      seen.add(o.geometry);
      o.geometry.dispose();
    }
    for (const m of Array.isArray(o.material) ? o.material : o.material ? [o.material] : []) {
      if (seen.has(m)) continue;
      seen.add(m);
      for (const k of ['map', 'emissiveMap']) if (m[k] && !seen.has(m[k])) (seen.add(m[k]), m[k].dispose());
      m.dispose();
    }
  });
}

function presetValues(name) {
  const p = ACT_PRESETS[name] || ACT_PRESETS.doubt;
  const out = {};
  for (const k of COLOR_KEYS) out[k] = new THREE.Color(p[k]);
  for (const k of NUMBER_KEYS) out[k] = p[k];
  return out;
}

export class RoomRenderer {
  constructor(container) {
    this.root = el('div', 'room3d');
    this.canvasWrap = el('div', 'room3d-canvas', this.root);
    this.overlay = el('div', 'room3d-overlay', this.root);
    this.survLayer = el('div', 'room3d-surv', this.overlay);
    this.markerLayer = el('div', 'room3d-markers', this.overlay);
    this.tagLayer = el('div', 'room3d-tags', this.overlay);
    this.tooltip = el('div', 'room3d-tooltip', this.overlay);
    this.hud = el('div', 'room3d-hud', this.root);
    this.chip = el('button', 'room3d-chip', this.root);
    this.chip.type = 'button';
    this.chip.onclick = () => this.select('player');
    container.replaceChildren(this.root);

    this.renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFShadowMap;
    this.renderer.toneMapping = THREE.NeutralToneMapping;
    this.canvasWrap.appendChild(this.renderer.domElement);

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(30, 2, 0.1, 120);
    this.hemi = new THREE.HemisphereLight('#ffffff', '#888888', 1);
    this.ambient = new THREE.AmbientLight('#ffffff', 0.2);
    this.sun = new THREE.DirectionalLight('#ffffff', 2);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(2048, 2048);
    Object.assign(this.sun.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 0.5, far: 45 });
    this.sun.shadow.bias = -0.0004;
    this.sun.shadow.normalBias = 0.02;
    this.fill = new THREE.DirectionalLight('#ffffff', 0.5);
    this.fill.position.set(8, 7, 11);
    this.scene.add(this.hemi, this.ambient, this.sun, this.sun.target, this.fill);

    const ringMat = new THREE.MeshBasicMaterial({ color: '#3fa58a', transparent: true, opacity: 0.9, depthWrite: false });
    this.selRing = new THREE.Mesh(new THREE.RingGeometry(0.3, 0.38, 40), ringMat);
    this.selRing.rotation.x = -Math.PI / 2;
    this.selRing.position.y = 0.012;
    this.destRing = new THREE.Mesh(new THREE.RingGeometry(0.12, 0.17, 32), ringMat.clone());
    this.destRing.rotation.x = -Math.PI / 2;
    this.destRing.position.y = 0.012;
    this.destRing.visible = false;
    this.hoverBox = new THREE.Box3Helper(new THREE.Box3(), new THREE.Color('#3fa58a'));
    this.hoverBox.visible = false;
    this.scene.add(this.selRing, this.destRing, this.hoverBox);

    this.raycaster = new THREE.Raycaster();
    this.ndc = new THREE.Vector2();
    this.tmp = new THREE.Vector3();
    this.box = new THREE.Box3();
    this.clock = new THREE.Clock();

    this.room = null;
    this.roomId = null;
    this.view = null;
    this.handlers = {};
    this.persons = new Map();
    this.labels = new Map();
    this.store = new Map();
    this.active = new Map();
    this.selectedId = 'player';
    this.cur = null;
    this.target = null;
    this.hoverEvent = null;
    this.hovered = null;
    this.w = 1;
    this.h = 1;

    const canvas = this.renderer.domElement;
    canvas.addEventListener('pointerdown', e => (this.down = { x: e.clientX, y: e.clientY }));
    canvas.addEventListener('pointerup', e => {
      if (this.down && Math.hypot(e.clientX - this.down.x, e.clientY - this.down.y) < 7) this.onClick(e);
      this.down = null;
    });
    canvas.addEventListener('pointermove', e => (this.hoverEvent = e));
    canvas.addEventListener('pointerleave', () => (this.hoverEvent = null));

    this.resizeObserver = new ResizeObserver(() => this.resize());
    this.resizeObserver.observe(this.root);
    this.tick = this.tick.bind(this);
    requestAnimationFrame(this.tick);
  }

  update(view, handlers = {}) {
    this.handlers = handlers;
    const prev = this.view;
    this.view = view;
    if (view.roomId !== this.roomId) this.loadRoom(view.roomId, prev?.roomId);
    if (!prev || prev.lightingPreset !== view.lightingPreset) this.applyPreset(view.lightingPreset, !prev);
    this.syncActors();
    this.syncHotspots();
    this.syncMode();
  }

  loadRoom(roomId, fromRoom) {
    if (this.roomId) {
      const snap = {};
      for (const [id, p] of this.persons) snap[id] = { x: p.x, z: p.z, heading: p.heading };
      this.store.set(this.roomId, snap);
    }
    if (this.room) {
      this.scene.remove(this.room.group);
      disposeTree(this.room.group);
    }
    for (const p of this.persons.values()) {
      this.scene.remove(p.group);
      disposeTree(p.group);
    }
    this.persons.clear();
    this.hovered = null;

    this.layout = layoutFor(roomId);
    this.kit = createKit();
    this.room = buildRoom(this.layout, this.kit);
    this.scene.add(this.room.group);
    this.roomId = roomId;
    this.selectedId = 'player';
    this.saved = this.store.get(roomId) || {};
    this.entry = fromRoom ? this.room.doors.get(fromRoom) : null;
    this.fitCamera();
    if (this.cur) this.applyLighting();

    this.root.classList.remove('room3d-enter');
    void this.root.offsetWidth;
    this.root.classList.add('room3d-enter');
  }

  spotFor(id) {
    if (id === 'player' && this.entry) return this.entry;
    const s = this.saved[id];
    if (s) return s;
    const [x, z, hd] = this.layout.spots?.[id] || [0, 0, 0];
    return { x, z, heading: hd * DEG };
  }

  addPerson(id, { hologram = false } = {}) {
    const p = new Walker(id, appearanceFor(id));
    const spot = this.spotFor(id);
    const [x, z] = this.room.nav.snap(spot.x, spot.z);
    p.place(x, z, spot.heading);
    if (hologram) {
      p.group.traverse(o => {
        if (!o.material) return;
        o.material = o.material.clone();
        o.material.transparent = true;
        o.material.opacity = 0.45;
        o.material.emissive?.set?.(0x3d8f84);
      });
    }
    this.persons.set(id, p);
    this.scene.add(p.group);
    return p;
  }

  syncActors() {
    const actors = this.view.hotspots.filter(h => h.kind === 'actor');
    const ids = new Set(actors.map(h => h.id));
    for (const [id, p] of this.persons) {
      if (id === 'player' || ids.has(id)) continue;
      this.scene.remove(p.group);
      disposeTree(p.group);
      this.persons.delete(id);
    }
    if (!this.persons.has('player')) this.addPerson('player');
    for (const h of actors) if (!this.persons.has(h.id)) this.addPerson(h.id, { hologram: !!h.hologram });

    this.labels = new Map([['player', { label: 'You', sub: 'External evaluator' }], ...actors.map(h => [h.id, { label: h.label, sub: h.sublabel }])]);
    if (!this.persons.has(this.selectedId)) this.selectedId = 'player';

    this.tagLayer.replaceChildren();
    this.tags = new Map();
    for (const [id, info] of this.labels) {
      const tag = el('button', `room3d-tag${id === 'player' ? ' is-player' : ''}`, this.tagLayer);
      tag.type = 'button';
      tag.textContent = info.label;
      tag.title = id === 'player' ? 'You — click the floor to walk' : `${info.label}, ${info.sub || ''} — click to speak to`;
      tag.onclick = () => this.clickPerson(id);
      this.tags.set(id, tag);
    }
    this.updateChip();
  }

  syncHotspots() {
    for (const obj of this.room.hotspotObjects.values()) obj.userData.hotspotId = null;
    this.active = new Map();
    this.markerLayer.replaceChildren();
    for (const h of this.view.hotspots) {
      if (h.kind === 'actor') continue;
      const obj = this.room.hotspotObjects.get(h.id);
      if (!obj) {
        console.warn(`[scene] room "${this.roomId}" has no object for hotspot "${h.id}"`);
        continue;
      }
      obj.userData.hotspotId = h.id;
      obj.updateMatrixWorld(true);
      this.box.setFromObject(obj);
      const anchor = new THREE.Vector3();
      this.box.getCenter(anchor);
      anchor.y = this.box.max.y + 0.18;
      const marker = el('button', `room3d-marker kind-${h.kind}${h.examined ? ' examined' : ''}${h.restricted ? ' restricted' : ''}`, this.markerLayer);
      marker.type = 'button';
      const icon = h.restricted ? '⊘' : h.kind === 'exit' ? '→' : h.kind === 'terminal' ? '⌨' : h.examined ? '✓' : '▤';
      const status = h.kind === 'object' ? (h.examined ? ' · examined' : ' · not yet read') : '';
      marker.innerHTML = `<span class="mk-ico">${icon}</span><span class="mk-label">${esc(h.label)}</span>`;
      marker.setAttribute('aria-label', `${h.label}${status}`);
      marker.title = `${h.label}${status}`;
      marker.onclick = () => this.activateHotspot(h.id);
      this.active.set(h.id, { h, obj, anchor, marker });
    }
  }

  syncMode() {
    const surv = this.view.camera === 'surveillance';
    this.root.classList.toggle('is-surveillance', surv);
    this.survLayer.replaceChildren();
    this.survBoxes = [];
    if (!surv) {
      this.hud.innerHTML = '';
      return;
    }
    const meta = this.view.surveillanceMeta || {};
    this.hud.innerHTML = `<span class="rec">● REC</span><span>${esc(meta.cameraId || '')}</span><span>${esc(meta.timestamp || '')}</span><span class="hud-note">Image = raw feed · red boxes = annotations (inferred, may be wrong)</span>`;
    for (const a of this.view.annotations || []) {
      const box = el('div', 'surv-box', this.survLayer);
      box.innerHTML = `<span class="surv-tag">ANNOT · ${esc(a.identity)} · ${Math.round((a.confidence || 0) * 100)}%</span><span class="surv-activity">${esc(a.activity || '')}</span>`;
      if (a.note) box.title = a.note;
      this.survBoxes.push({ a, box });
    }
  }

  applyPreset(name, instant) {
    this.target = presetValues(name);
    if (instant || !this.cur) this.cur = presetValues(name);
    this.applyLighting();
  }

  stepLighting(dt) {
    const k = 1 - Math.exp(-dt * 3);
    for (const key of COLOR_KEYS) this.cur[key].lerp(this.target[key], k);
    for (const key of NUMBER_KEYS) this.cur[key] += (this.target[key] - this.cur[key]) * k;
    this.applyLighting();
  }

  applyLighting() {
    const c = this.cur;
    if (!c) return;
    this.scene.background = c.background;
    this.hemi.color.copy(c.hemiSky);
    this.hemi.groundColor.copy(c.hemiGround);
    this.hemi.intensity = c.hemi;
    this.ambient.intensity = c.ambient;
    this.sun.color.copy(c.sun);
    this.sun.intensity = c.sunI;
    const [sx, sy, sz] = this.layout?.sun || [-3, 9, -12];
    this.sun.position.set(sx, sy * c.sunHeight, sz);
    this.fill.color.copy(c.fill);
    this.fill.intensity = c.fillI;
    this.renderer.toneMappingExposure = c.exposure;
    for (const l of this.room?.lights || []) {
      l.color.copy(c.task);
      const tier = l.userData?.taskTier;
      l.intensity = c.taskI * (tier === 'fill' ? 0.5 : 1);
      l.decay = c.taskDecay;
      l.distance = c.taskDistance + (tier === 'fill' ? 2 : 0);
    }
    for (const entry of this.room?.ceilingLights || []) {
      entry.light.color.copy(c.ceiling);
      entry.light.intensity = c.ceilingI * 0.9;
      entry.light.decay = c.ceilingDecay;
      entry.light.distance = c.ceilingDistance;
    }
    for (const m of this.kit?.skies || []) m.color.copy(c.sky);
  }

  resize() {
    const w = Math.max(1, this.root.clientWidth), h = Math.max(1, this.root.clientHeight);
    this.w = w;
    this.h = h;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h;
    this.fitCamera();
  }

  fitCamera() {
    if (!this.layout) return;
    const { pos, target, fov } = this.layout.camera;
    const [W, D] = this.layout.size;
    const H = this.layout.wallHeight || 2.9;
    const T = WALL_T;
    const pts = [
      [-W / 2 - T, -0.45, -D / 2 - T], [W / 2, -0.45, -D / 2 - T], [-W / 2 - T, -0.45, D / 2], [W / 2, -0.45, D / 2],
      [-W / 2 - T, H, -D / 2 - T], [W / 2, H, -D / 2 - T], [-W / 2 - T, H, D / 2], [W / 2, 2.0, D / 2],
    ].map(p => new THREE.Vector3(...p));
    const tgt = new THREE.Vector3(...target);
    const dir = new THREE.Vector3(...pos).sub(tgt).normalize();
    this.camera.fov = fov;
    this.camera.updateProjectionMatrix();
    let lo = 4, hi = 80;
    for (let i = 0; i < 24; i++) {
      const d = (lo + hi) / 2;
      this.camera.position.copy(tgt).addScaledVector(dir, d);
      this.camera.lookAt(tgt);
      this.camera.updateMatrixWorld();
      const fits = pts.every(p => {
        const v = this.tmp.copy(p).project(this.camera);
        return Math.abs(v.x) <= 0.96 && Math.abs(v.y) <= 0.92 && v.z < 1;
      });
      if (fits) hi = d;
      else lo = d;
    }
    this.camera.position.copy(tgt).addScaledVector(dir, hi);
    this.camera.lookAt(tgt);
    this.camera.updateMatrixWorld();
  }

  pick(clientX, clientY) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.ndc.set(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(this.ndc, this.camera);
    const targets = [this.room.group, ...[...this.persons.values()].map(p => p.group)];
    const hits = this.raycaster.intersectObjects(targets, true);
    for (const hit of hits) {
      for (let o = hit.object; o; o = o.parent) {
        if (o.userData.personId) return { type: 'person', id: o.userData.personId };
        if (o.userData.hotspotId) return { type: 'hotspot', id: o.userData.hotspotId };
        if (o.userData.floor) return { type: 'floor', point: hit.point.clone() };
      }
      break;
    }
    const point = new THREE.Vector3();
    return this.raycaster.ray.intersectPlane(GROUND, point) ? { type: 'floor', point } : null;
  }

  onClick(e) {
    if (!this.room) return;
    const hit = this.pick(e.clientX, e.clientY);
    if (!hit) return;
    if (hit.type === 'person') this.clickPerson(hit.id);
    else if (hit.type === 'hotspot') this.activateHotspot(hit.id);
    else this.walk(this.selectedId, hit.point.x, hit.point.z);
  }

  clickPerson(id) {
    if (id === 'player') {
      this.select('player');
      return;
    }
    this.select('player');
    const npc = this.persons.get(id);
    if (npc) this.persons.get('player')?.faceToward(npc.x, npc.z);
    this.handlers.onFocusActor?.(id);
  }

  select(id) {
    if (!this.persons.has(id)) return;
    this.selectedId = id;
    this.updateChip();
  }

  updateChip() {
    this.chip.hidden = true;
    for (const [id, tag] of this.tags || []) tag.classList.toggle('selected', false);
  }

  walk(id, x, z, { heading = null, onArrive = null } = {}) {
    const p = this.persons.get(id);
    if (!p) return;
    const path = this.room.nav.findPath([p.x, p.z], [x, z]);
    if (!path) return;
    p.setPath(path, heading, onArrive);
    const [fx, fz] = path.length ? path[path.length - 1] : [p.x, p.z];
    this.destRing.position.set(fx, 0.012, fz);
    this.destRing.visible = true;
    this.destRing.material.opacity = 0.9;
  }

  activateHotspot(id) {
    const entry = this.active.get(id);
    if (!entry) return;
    const { h } = entry;
    const act = () => {
      if (h.kind === 'exit') this.handlers.onGo?.(h.targetRoom);
      else if (h.kind === 'object') this.handlers.onInspect?.(h.id);
      else if (h.kind === 'terminal') this.handlers.onTerminal?.(h.id);
    };
    this.select('player');
    const spot = this.room.interact.get(id);
    if (!spot) return act();
    this.walk('player', spot.x, spot.z, { heading: spot.heading, onArrive: act });
  }

  toScreen(v) {
    const p = this.tmp.copy(v).project(this.camera);
    return { x: ((p.x + 1) / 2) * this.w, y: ((1 - p.y) / 2) * this.h, visible: p.z < 1 };
  }

  processHover() {
    if (!this.hoverEvent || !this.room) {
      this.renderer.domElement.style.cursor = 'default';
      this.tooltip.style.display = 'none';
      this.hoverBox.visible = false;
      this.hovered = null;
      return;
    }
    const e = this.hoverEvent;
    const hit = this.pick(e.clientX, e.clientY);
    const key = hit ? `${hit.type}:${hit.id || ''}` : '';
    const rect = this.renderer.domElement.getBoundingClientRect();
    let text = '';
    if (hit?.type === 'person') {
      const info = this.labels.get(hit.id);
      text = hit.id === 'player' ? 'You — click the floor to walk' : `${info?.label || hit.id} — click to speak to`;
    } else if (hit?.type === 'hotspot') {
      const h = this.active.get(hit.id)?.h;
      text = h ? (h.kind === 'exit' ? (h.restricted ? `${h.label} — higher clearance` : `Go to ${h.label}`) : h.kind === 'terminal' ? `${h.label} — walk over and use` : `${h.label} — walk over and read`) : '';
    }
    this.renderer.domElement.style.cursor = hit?.type === 'floor' ? 'crosshair' : hit ? 'pointer' : 'default';
    if (key !== this.hovered) {
      this.hovered = key;
      const obj = hit?.type === 'hotspot' ? this.active.get(hit.id)?.obj : hit?.type === 'person' ? this.persons.get(hit.id)?.group : null;
      if (obj) {
        this.hoverBox.box.setFromObject(obj);
        this.hoverBox.visible = true;
      } else this.hoverBox.visible = false;
    }
    if (text) {
      this.tooltip.textContent = text;
      this.tooltip.style.display = 'block';
      this.tooltip.style.transform = `translate(${e.clientX - rect.left + 14}px, ${e.clientY - rect.top + 12}px)`;
    } else this.tooltip.style.display = 'none';
  }

  layoutOverlay() {
    for (const [id, tag] of this.tags || []) {
      const p = this.persons.get(id);
      if (!p) continue;
      const s = this.toScreen(this.tmp.set(p.x, p.height + 0.15, p.z));
      tag.style.transform = `translate(${s.x}px, ${s.y}px) translate(-50%, -100%)`;
    }
    for (const { anchor, marker } of this.active.values()) {
      const s = this.toScreen(anchor);
      marker.style.transform = `translate(${s.x}px, ${s.y}px) translate(-50%, -50%)`;
    }
    for (const { a, box } of this.survBoxes || []) {
      const target = this.persons.get(a.targetHotspot)?.group || this.active.get(a.targetHotspot)?.obj;
      if (!target) {
        box.style.display = 'none';
        continue;
      }
      this.box.setFromObject(target);
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      const { min, max } = this.box;
      for (const x of [min.x, max.x]) for (const y of [min.y, max.y]) for (const z of [min.z, max.z]) {
        const s = this.toScreen(this.tmp.set(x, y, z));
        x0 = Math.min(x0, s.x); y0 = Math.min(y0, s.y); x1 = Math.max(x1, s.x); y1 = Math.max(y1, s.y);
      }
      Object.assign(box.style, { display: 'block', left: `${x0}px`, top: `${y0}px`, width: `${x1 - x0}px`, height: `${y1 - y0}px` });
    }
  }

  tick() {
    if (this.disposed) return;
    requestAnimationFrame(this.tick);
    const dt = Math.min(this.clock.getDelta(), 0.05);
    if (!this.room || document.hidden) return;
    const t = this.clock.elapsedTime;
    this.stepLighting(dt);
    this.kit.update(dt, t, this.cur.screen);

    const player = this.persons.get('player');
    for (const [id, p] of this.persons) {
      if (id !== 'player' && player && !p.moving && Math.hypot(player.x - p.x, player.z - p.z) < 4.5) p.faceToward(player.x, player.z);
      p.update(dt, t);
    }
    const sel = this.persons.get(this.selectedId);
    if (sel) {
      this.selRing.position.set(sel.x, 0.012, sel.z);
      this.selRing.scale.setScalar(1 + Math.sin(t * 4) * 0.05);
    }
    if (this.destRing.visible) {
      this.destRing.material.opacity -= dt * 0.9;
      if (this.destRing.material.opacity <= 0) this.destRing.visible = false;
    }
    this.processHover();
    this.renderer.render(this.scene, this.camera);
    this.layoutOverlay();
    this.onFrame?.();
  }

  /** Player position in canvas pixels, for a host that scrolls a canvas wider than the viewport. */
  playerScreen() {
    const p = this.persons.get('player');
    return p ? this.toScreen(this.tmp.set(p.x, 1, p.z)) : null;
  }

  /** Crop the current frame to a viewport rectangle (DOMRect / getBoundingClientRect). */
  captureRect(viewportRect) {
    if (!this.room) return null;
    this.renderer.render(this.scene, this.camera);
    const canvas = this.renderer.domElement;
    const bb = canvas.getBoundingClientRect();
    if (bb.width < 1 || bb.height < 1) return null;
    const scaleX = canvas.width / bb.width;
    const scaleY = canvas.height / bb.height;
    const sx = Math.max(0, Math.round((viewportRect.left - bb.left) * scaleX));
    const sy = Math.max(0, Math.round((viewportRect.top - bb.top) * scaleY));
    const sw = Math.min(canvas.width - sx, Math.round(viewportRect.width * scaleX));
    const sh = Math.min(canvas.height - sy, Math.round(viewportRect.height * scaleY));
    if (sw < 1 || sh < 1) return null;
    const out = document.createElement('canvas');
    out.width = sw;
    out.height = sh;
    out.getContext('2d').drawImage(canvas, sx, sy, sw, sh, 0, 0, sw, sh);
    return out;
  }

  dispose() {
    this.disposed = true;
    this.resizeObserver.disconnect();
    if (this.room) disposeTree(this.room.group);
    for (const p of this.persons.values()) disposeTree(p.group);
    this.renderer.dispose();
    this.root.remove();
  }
}
