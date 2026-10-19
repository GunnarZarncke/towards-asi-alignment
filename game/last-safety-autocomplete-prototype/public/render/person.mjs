/**
 * Procedural low-poly bodies with walk and idle motion. Stand-in until O-34 (character style) closes.
 * Local forward is +z. Appearance is presentation only.
 */
import * as THREE from 'three';

const LOOKS = {
  player: { skin: '#d1a98a', hair: '#5a4434', hairStyle: 'short', top: '#d9dfdc', bottom: '#36495a', shoes: '#2a2a2a', scale: 0.98, badge: true },
  pavel: { skin: '#c9a184', hair: '#2f2b28', hairStyle: 'short', top: '#4f6b62', bottom: '#3a4248', shoes: '#1f1f1f', scale: 1.02, build: 1.08 },
  leila: { skin: '#a87556', hair: '#1d1a1a', hairStyle: 'bun', top: '#2f4058', bottom: '#2b2f36', shoes: '#1a1a1a', scale: 0.96, glasses: true },
  elena: { skin: '#e2bfa3', hair: '#a8743e', hairStyle: 'bob', top: '#b56a4e', bottom: '#4b4f58', shoes: '#3a2c24', scale: 0.95 },
};

const FALLBACK_TOPS = ['#6b7f8a', '#8a6b5a', '#5a7a6b', '#7a6b8a'];

export function appearanceFor(id) {
  if (LOOKS[id]) return LOOKS[id];
  let h = 0;
  for (const ch of String(id)) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return { skin: '#c9a184', hair: '#3a332d', hairStyle: 'short', top: FALLBACK_TOPS[h % FALLBACK_TOPS.length], bottom: '#3a4248', shoes: '#222', scale: 1 };
}

function createBody(look) {
  const m = c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.8 });
  const skin = m(look.skin), hair = m(look.hair), top = m(look.top), bottom = m(look.bottom), shoes = m(look.shoes);
  const build = look.build || 1;

  const root = new THREE.Group();
  const body = new THREE.Group();
  root.add(body);
  const mesh = (geo, mat, x, y, z, parent = body) => {
    const o = new THREE.Mesh(geo, mat);
    o.position.set(x, y, z);
    o.castShadow = true;
    o.receiveShadow = true;
    parent.add(o);
    return o;
  };

  const hipY = 0.92;
  const legGeo = new THREE.CapsuleGeometry(0.075, 0.7, 4, 10);
  const shoeGeo = new THREE.BoxGeometry(0.11, 0.07, 0.25);
  const legs = [-1, 1].map(side => {
    const pivot = new THREE.Group();
    pivot.position.set(side * 0.1 * build, hipY, 0);
    body.add(pivot);
    mesh(legGeo, bottom, 0, -0.43, 0, pivot);
    mesh(shoeGeo, shoes, 0, -0.88, 0.04, pivot);
    return pivot;
  });

  const torso = mesh(new THREE.CapsuleGeometry(0.17, 0.34, 4, 14), top, 0, 1.22, 0);
  torso.scale.set(1.12 * build, 1, 0.72);

  const armGeo = new THREE.CapsuleGeometry(0.055, 0.5, 4, 8);
  const handGeo = new THREE.SphereGeometry(0.058, 10, 8);
  const arms = [-1, 1].map(side => {
    const pivot = new THREE.Group();
    pivot.position.set(side * 0.235 * build, 1.46, 0);
    pivot.rotation.z = side * 0.08;
    body.add(pivot);
    mesh(armGeo, top, 0, -0.3, 0, pivot);
    mesh(handGeo, skin, 0, -0.63, 0, pivot);
    return pivot;
  });

  mesh(new THREE.CylinderGeometry(0.05, 0.055, 0.1, 10), skin, 0, 1.6, 0);
  const head = new THREE.Group();
  head.position.set(0, 1.74, 0);
  body.add(head);
  const skull = mesh(new THREE.SphereGeometry(0.125, 20, 14), skin, 0, 0, 0, head);
  skull.scale.set(0.92, 1.05, 0.95);
  const eyeGeo = new THREE.SphereGeometry(0.014, 8, 6);
  const eyeMat = m('#1d1d1d');
  for (const sx of [-1, 1]) mesh(eyeGeo, eyeMat, sx * 0.042, 0.015, 0.11, head);

  const capTheta = look.hairStyle === 'bob' ? Math.PI * 0.62 : Math.PI * 0.5;
  const cap = mesh(new THREE.SphereGeometry(0.135, 20, 12, 0, Math.PI * 2, 0, capTheta), hair, 0, 0.012, -0.008, head);
  cap.rotation.x = -0.42;
  if (look.hairStyle === 'bun') mesh(new THREE.SphereGeometry(0.06, 12, 10), hair, 0, 0.08, -0.12, head);
  if (look.glasses) mesh(new THREE.BoxGeometry(0.17, 0.028, 0.012), m('#222'), 0, 0.017, 0.118, head);
  if (look.badge) {
    mesh(new THREE.BoxGeometry(0.07, 0.09, 0.012), m('#f5f5f0'), 0.05, 1.27, 0.13);
    mesh(new THREE.BoxGeometry(0.05, 0.014, 0.004), m('#3f7a6c'), 0.05, 1.3, 0.137);
  }

  const s = look.scale || 1;
  root.scale.setScalar(s);
  return { root, body, legs, arms, torso, head, height: 1.9 * s };
}

function wrapAngle(a) {
  return Math.atan2(Math.sin(a), Math.cos(a));
}

export class Walker {
  constructor(id, look) {
    const b = createBody(look);
    Object.assign(this, { id, group: b.root, body: b.body, legs: b.legs, arms: b.arms, torso: b.torso, head: b.head, height: b.height });
    this.group.userData.personId = id;
    this.x = 0;
    this.z = 0;
    this.heading = 0;
    this.targetHeading = 0;
    this.path = [];
    this.speed = 3.2;
    this.phase = Math.random() * 6;
    this.walkBlend = 0;
    this.onArrive = null;
    this.finalHeading = null;
    this.idleSeed = Math.random() * 10;
  }

  place(x, z, heading) {
    this.x = x;
    this.z = z;
    this.heading = this.targetHeading = heading;
    this.path = [];
    this.sync();
  }

  get moving() {
    return this.path.length > 0;
  }

  setPath(points, finalHeading = null, onArrive = null) {
    this.path = points.slice();
    this.finalHeading = finalHeading;
    this.onArrive = onArrive;
    if (!this.path.length) this.arrive();
  }

  arrive() {
    this.path = [];
    if (this.finalHeading != null) this.targetHeading = this.finalHeading;
    const cb = this.onArrive;
    this.onArrive = null;
    cb?.();
  }

  faceToward(x, z) {
    if (this.moving) return;
    this.targetHeading = Math.atan2(x - this.x, z - this.z);
  }

  update(dt, t) {
    if (this.path.length) {
      const [tx, tz] = this.path[0];
      const dx = tx - this.x, dz = tz - this.z;
      const dist = Math.hypot(dx, dz);
      if (dist < 0.02) {
        this.path.shift();
        if (!this.path.length) this.arrive();
      } else {
        const step = Math.min(dist, this.speed * dt);
        this.x += (dx / dist) * step;
        this.z += (dz / dist) * step;
        this.targetHeading = Math.atan2(dx, dz);
      }
    }
    this.heading += wrapAngle(this.targetHeading - this.heading) * Math.min(1, dt * 9);
    this.walkBlend += ((this.moving ? 1 : 0) - this.walkBlend) * Math.min(1, dt * 8);
    if (this.moving) this.phase += dt * this.speed * 5.2;

    const swing = Math.sin(this.phase) * 0.6 * this.walkBlend;
    const idle = 1 - this.walkBlend;
    this.legs[0].rotation.x = swing;
    this.legs[1].rotation.x = -swing;
    this.arms[0].rotation.x = -swing * 0.75 + Math.sin(t * 0.9 + this.idleSeed) * 0.04 * idle;
    this.arms[1].rotation.x = swing * 0.75 + Math.sin(t * 0.8 + this.idleSeed + 1) * 0.04 * idle;
    this.torso.scale.y = 1 + Math.sin(t * 2.1 + this.idleSeed) * 0.012 * idle;
    this.head.rotation.y = Math.sin(t * 0.35 + this.idleSeed) * 0.18 * idle;
    this.body.position.y = Math.abs(Math.sin(this.phase)) * 0.04 * this.walkBlend;
    this.sync();
  }

  sync() {
    this.group.position.set(this.x, 0, this.z);
    this.group.rotation.y = this.heading;
  }
}
