/** Build a cutaway room from a layout. Walls are the back and left; front and right stay open, and doors may sit on any side. */
import * as THREE from 'three';
import { NavGrid } from './nav.mjs';

export const WALL_T = 0.18;
const DEG = Math.PI / 180;
const DOOR_H = 2.2;

/** LED strip above each door: green when badge clearance opens it, red when not. */
export const CLEARANCE_SIGN_OPEN = { color: '#2f9e64', emissive: '#4fd18b', emissiveIntensity: 1.1 };
export const CLEARANCE_SIGN_CLOSED = { color: '#b83a3a', emissive: '#ff5555', emissiveIntensity: 1.0 };

export function applyClearanceSign(sign, canPass) {
  const c = canPass ? CLEARANCE_SIGN_OPEN : CLEARANCE_SIGN_CLOSED;
  sign.material.color.set(c.color);
  sign.material.emissive.set(c.emissive);
  sign.material.emissiveIntensity = c.emissiveIntensity;
}

function wallSegments(u0, u1, H, openings) {
  const out = [];
  let cur = u0;
  for (const o of [...openings].sort((a, b) => a.u0 - b.u0)) {
    if (o.u0 > cur) out.push({ u0: cur, u1: o.u0, y0: 0, y1: H });
    if (o.y0 > 0) out.push({ u0: o.u0, u1: o.u1, y0: 0, y1: o.y0 });
    if (o.y1 < H) out.push({ u0: o.u0, u1: o.u1, y0: o.y1, y1: H });
    cur = o.u1;
  }
  if (cur < u1) out.push({ u0: cur, u1, y0: 0, y1: H });
  return out;
}

function floorTexture(layout) {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  g.fillStyle = layout.floor;
  g.fillRect(0, 0, 256, 256);
  g.strokeStyle = layout.floorLine;
  if (layout.floorStyle === 'planks') {
    g.lineWidth = 2;
    for (let y = 0; y <= 256; y += 32) {
      g.beginPath();
      g.moveTo(0, y);
      g.lineTo(256, y);
      g.stroke();
      const off = (y / 32) % 2 ? 64 : 160;
      g.beginPath();
      g.moveTo(off, y);
      g.lineTo(off, y + 32);
      g.stroke();
    }
  } else {
    g.lineWidth = 3;
    g.strokeRect(0, 0, 256, 256);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  const [W, D] = layout.size;
  const tile = layout.floorStyle === 'planks' ? 2.4 : 1.2;
  tex.repeat.set(W / tile, D / tile);
  tex.anisotropy = 8;
  return tex;
}

function skyTexture() {
  const c = document.createElement('canvas');
  c.width = 128;
  c.height = 128;
  const g = c.getContext('2d');
  const grad = g.createLinearGradient(0, 0, 0, 128);
  grad.addColorStop(0, '#ffffff');
  grad.addColorStop(0.7, '#eef2ee');
  grad.addColorStop(1, '#dfe6df');
  g.fillStyle = grad;
  g.fillRect(0, 0, 128, 128);
  g.fillStyle = '#b9c9bb';
  for (let i = 0; i < 7; i++) {
    g.beginPath();
    g.arc(10 + i * 19, 118 - (i % 3) * 5, 16 + (i % 2) * 6, 0, Math.PI * 2);
    g.fill();
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

export function buildRoom(layout, kit) {
  const group = new THREE.Group();
  const [W, D] = layout.size;
  const H = layout.wallHeight || 2.9;
  const T = WALL_T;
  const hotspotObjects = new Map();
  const interact = new Map();
  const doors = new Map();
  const lights = [];
  const ceilingLights = [];
  const nav = new NavGrid({ minX: -W / 2 + 0.3, maxX: W / 2 - 0.35, minZ: -D / 2 + 0.3, maxZ: D / 2 - 0.35, cell: 0.2 });

  const placeOnWall = (obj, wall, u, y, offset = 0) => {
    // Local −z points out of the room. A negative offset moves the object outward.
    if (wall === 'left') {
      obj.position.set(-W / 2 + offset, y, u);
      obj.rotation.y = Math.PI / 2;
    } else if (wall === 'right') {
      obj.position.set(W / 2 - offset, y, u);
      obj.rotation.y = -Math.PI / 2;
    } else if (wall === 'front') {
      obj.position.set(u, y, D / 2 - offset);
      obj.rotation.y = Math.PI;
    } else {
      obj.position.set(u, y, -D / 2 + offset);
      obj.rotation.y = 0;
    }
  };
  const mesh = (geo, mat, parent = group, shadow = true) => {
    const m = new THREE.Mesh(geo, mat);
    m.castShadow = shadow;
    m.receiveShadow = true;
    parent.add(m);
    return m;
  };

  const floor = mesh(new THREE.BoxGeometry(W, 0.12, D), new THREE.MeshStandardMaterial({ color: '#ffffff', map: floorTexture(layout), roughness: 0.85 }), group, false);
  floor.position.y = -0.06;
  floor.userData.floor = true;
  const slab = mesh(new THREE.BoxGeometry(W + T + 0.5, 0.36, D + T + 0.5), new THREE.MeshStandardMaterial({ color: '#4f5b59', roughness: 0.9 }), group, false);
  slab.position.set(-T / 2, -0.3, -T / 2);

  const wallMat = new THREE.MeshStandardMaterial({ color: layout.wall, roughness: 0.92 });
  const capMat = new THREE.MeshStandardMaterial({ color: '#3a4849', roughness: 0.8 });
  const baseMat = new THREE.MeshStandardMaterial({ color: '#9aa29e', roughness: 0.7 });
  const frameMat = new THREE.MeshStandardMaterial({ color: '#dfe4e2', roughness: 0.4, metalness: 0.4 });
  const accentMat = new THREE.MeshStandardMaterial({ color: layout.accent, roughness: 0.6 });

  const openings = { back: [], left: [], front: [], right: [] };
  const punched = wall => wall === 'back' || wall === 'left';
  for (const d of layout.doors || []) if (punched(d.wall)) openings[d.wall].push({ u0: d.at - d.w / 2, u1: d.at + d.w / 2, y0: 0, y1: DOOR_H });
  for (const w of layout.windows || []) if (punched(w.wall)) openings[w.wall].push({ u0: w.at - w.w / 2, u1: w.at + w.w / 2, y0: w.y0, y1: w.y1 });

  const buildWall = (wall, u0, u1) => {
    for (const s of wallSegments(u0, u1, H, openings[wall])) {
      const w = s.u1 - s.u0, h = s.y1 - s.y0, uc = (s.u0 + s.u1) / 2;
      const seg = mesh(new THREE.BoxGeometry(w, h, T), wallMat);
      placeOnWall(seg, wall, uc, (s.y0 + s.y1) / 2, -T / 2);
      if (s.y1 === H) {
        const cap = mesh(new THREE.BoxGeometry(w, 0.035, T + 0.01), capMat, group, false);
        placeOnWall(cap, wall, uc, H + 0.017, -T / 2);
      }
      if (s.y0 === 0 && h > 0.5) {
        const base = mesh(new THREE.BoxGeometry(w, 0.09, 0.02), baseMat, group, false);
        placeOnWall(base, wall, uc, 0.045, 0.01);
      }
    }
  };
  buildWall('back', -W / 2 - T, W / 2);
  buildWall('left', -D / 2, D / 2);

  for (const c of layout.ceiling || []) {
    const [x, z] = c.at;
    const pw = c.w || 1.2;
    const pd = c.d || 0.6;
    const span = Math.max(pw, pd);
    const pl = new THREE.PointLight('#f8faf5', 0, span + 9, 1);
    pl.position.set(x, H - 0.22, z);
    group.add(pl);
    ceilingLights.push({ light: pl });
  }

  const skyMap = skyTexture();
  for (const win of layout.windows || []) {
    const g = new THREE.Group();
    placeOnWall(g, win.wall, win.at, 0, 0);
    group.add(g);
    const h = win.y1 - win.y0, yc = (win.y0 + win.y1) / 2;
    const glass = mesh(new THREE.BoxGeometry(win.w, h, 0.012), new THREE.MeshStandardMaterial({ color: '#cfe3e6', roughness: 0.1, metalness: 0.1, transparent: true, opacity: 0.18, depthWrite: false }), g, false);
    glass.position.set(0, yc, -T / 2);
    for (const [w, hh, x, y] of [[win.w + 0.08, 0.05, 0, win.y0], [win.w + 0.08, 0.05, 0, win.y1], [0.05, h, -win.w / 2, yc], [0.05, h, win.w / 2, yc], [0.04, h, 0, yc]]) {
      const f = mesh(new THREE.BoxGeometry(w, hh, T + 0.02), frameMat, g);
      f.position.set(x, y, -T / 2);
    }
    const sill = mesh(new THREE.BoxGeometry(win.w + 0.12, 0.04, 0.14), frameMat, g);
    sill.position.set(0, win.y0 - 0.02, 0.06);
    const skyMat = new THREE.MeshBasicMaterial({ color: '#ffffff', map: skyMap });
    kit.sky(skyMat);
    const sky = mesh(new THREE.PlaneGeometry(win.w + 1.6, h + 0.5), skyMat, g, false);
    sky.receiveShadow = false;
    sky.position.set(0, yc - 0.1, -T - 0.7);
  }

  const doorInset = Math.min(0.65, W / 2 - 0.4, D / 2 - 0.4);
  for (const d of layout.doors || []) {
    const g = new THREE.Group();
    placeOnWall(g, d.wall, d.at, 0, 0);
    group.add(g);
    for (const sx of [-1, 1]) {
      const jamb = mesh(new THREE.BoxGeometry(0.07, DOOR_H + 0.04, T + 0.05), accentMat, g);
      jamb.position.set(sx * (d.w / 2 + 0.035), (DOOR_H + 0.04) / 2, -T / 2);
    }
    const head = mesh(new THREE.BoxGeometry(d.w + 0.14, 0.08, T + 0.05), accentMat, g);
    head.position.set(0, DOOR_H + 0.04, -T / 2);
    const hinge = new THREE.Group();
    hinge.position.set(-d.w / 2 + 0.02, 0, -T);
    hinge.rotation.y = 1.1;
    g.add(hinge);
    const leaf = mesh(new THREE.BoxGeometry(d.w - 0.04, DOOR_H - 0.05, 0.04), new THREE.MeshStandardMaterial({ color: '#f1f0eb', roughness: 0.6 }), hinge);
    leaf.position.set((d.w - 0.04) / 2, (DOOR_H - 0.05) / 2, 0);
    const corridor = mesh(new THREE.PlaneGeometry(d.w + 0.6, DOOR_H + 0.4), new THREE.MeshStandardMaterial({ color: '#7d8986', roughness: 1 }), g, false);
    corridor.position.set(0, (DOOR_H + 0.4) / 2, -T - 1.1);
    const strip = mesh(new THREE.BoxGeometry(d.w, 0.12, 1.2), new THREE.MeshStandardMaterial({ color: layout.floor, roughness: 0.85 }), g, false);
    strip.position.set(0, -0.06, -T - 0.5);
    const sign = mesh(
      new THREE.BoxGeometry(0.3, 0.1, 0.03),
      new THREE.MeshStandardMaterial({ ...CLEARANCE_SIGN_OPEN }),
      g,
      false,
    );
    sign.position.set(0, DOOR_H + 0.25, 0.02);
    g.userData.clearanceSign = sign;
    const hit = new THREE.Mesh(new THREE.PlaneGeometry(d.w, DOOR_H), new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false }));
    hit.position.set(0, DOOR_H / 2, 0.02);
    g.add(hit);

    const stand = {
      back: { x: d.at, z: -D / 2 + doorInset, face: 180, enter: 0 },
      front: { x: d.at, z: D / 2 - doorInset, face: 0, enter: 180 },
      left: { x: -W / 2 + doorInset, z: d.at, face: -90, enter: 90 },
      right: { x: W / 2 - doorInset, z: d.at, face: 90, enter: -90 },
    }[d.wall];
    if (!stand) continue;
    const id = `exit_${d.to}`;
    hotspotObjects.set(id, g);
    interact.set(id, { x: stand.x, z: stand.z, heading: stand.face * DEG });
    doors.set(d.to, { x: stand.x, z: stand.z, heading: stand.enter * DEG });
  }

  for (const p of layout.props || []) {
    const fn = kit.props[p.type];
    if (!fn) {
      console.warn(`[scene] unknown prop type "${p.type}"`);
      continue;
    }
    const out = fn(p.opts || {});
    const g = out.group;
    if (p.wall) placeOnWall(g, p.wall, p.at, p.y || 0, 0);
    else {
      g.position.set(p.at[0], 0, p.at[1]);
      g.rotation.y = (p.rot || 0) * DEG;
      if (out.footprint) nav.blockRect(p.at[0], p.at[1], out.footprint[0], out.footprint[1], p.rot || 0, 0.26);
    }
    group.add(g);
    for (const l of out.lights || []) {
      const light = new THREE.PointLight('#ffd9a8', 0, 12, 1);
      light.userData.taskTier = 'main';
      light.position.set(l[0], l[1] + 0.15, l[2]);
      g.add(light);
      lights.push(light);
      const uplight = new THREE.PointLight('#ffe8c8', 0, 14, 1);
      uplight.userData.taskTier = 'fill';
      uplight.position.set(l[0], l[1] + 0.55, l[2]);
      g.add(uplight);
      lights.push(uplight);
    }
    if (p.hotspot) hotspotObjects.set(p.hotspot, g);
  }

  for (const [id, [x, z, hd]] of Object.entries(layout.interact || {})) interact.set(id, { x, z, heading: hd * DEG });

  return { group, hotspotObjects, interact, doors, nav, lights, ceilingLights, size: [W, D], height: H };
}
