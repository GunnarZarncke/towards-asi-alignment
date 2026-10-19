/**
 * Procedural low-poly furniture kit. Stand-in until an asset kit is chosen.
 * Floor props: origin at floor centre of the footprint, front faces +z.
 * Wall props: origin at the wall surface, extending towards +z.
 * Each prop returns { group, footprint: [w, d] | null, lights: [[x, y, z]] }.
 */
import * as THREE from 'three';

const C = {
  laminate: '#ecebe6',
  benchTop: '#d9dcd7',
  metal: '#9aa3a5',
  dark: '#363e41',
  frame: '#dfe4e2',
  rack: '#262d2f',
  rackDoor: '#323b3d',
  plastic: '#f3f3ef',
  fabric: '#4d6268',
  sofa: '#5b6f73',
  pot: '#d9d3c7',
  soil: '#5a4a3c',
  leaf: '#6e9a70',
  leafDark: '#527a58',
  glass: '#cfe3e6',
  paper: '#f7f6f1',
  binder: '#2f5d8a',
  folder: '#c99a3e',
  instrument: '#c9cdc9',
  rug: '#b98f6e',
  rugBorder: '#8f6a4f',
  books: ['#7a4b3a', '#3f6177', '#88925e', '#c4a35a', '#5a4f72', '#9b5b4f', '#d8d2c2'],
};

function rng(seed) {
  let s = (seed * 2654435761) >>> 0 || 1;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

function screenTexture(kind, seed) {
  const tall = kind === 'queue' || kind === 'code';
  const c = document.createElement('canvas');
  c.width = 256;
  c.height = tall ? 320 : 160;
  const g = c.getContext('2d');
  const r = rng(seed * 31 + kind.length);
  g.fillStyle = kind === 'doc' ? '#eef1ee' : '#0f2427';
  g.fillRect(0, 0, c.width, c.height);

  if (kind === 'queue') {
    for (let y = 8; y < c.height; y += 16) {
      const state = r();
      g.fillStyle = state > 0.9 ? '#e0b45a' : state > 0.35 ? '#5fc3a8' : '#5d7a7c';
      g.fillRect(10, y, 8, 8);
      g.fillStyle = '#9fc9bf';
      g.globalAlpha = 0.75;
      g.fillRect(26, y + 1, 40 + r() * 90, 5);
      g.globalAlpha = 0.4;
      g.fillRect(180, y + 1, 20 + r() * 50, 5);
      g.globalAlpha = 1;
    }
  } else if (kind === 'code') {
    for (let y = 8; y < c.height; y += 12) {
      const indent = Math.floor(r() * 4) * 14;
      g.fillStyle = r() > 0.7 ? '#e6c07b' : r() > 0.5 ? '#7fc8e8' : '#a9c7c0';
      g.globalAlpha = 0.8;
      g.fillRect(12 + indent, y, 30 + r() * 140, 4);
      g.globalAlpha = 1;
    }
  } else if (kind === 'nora') {
    g.fillStyle = '#5fc3a8';
    g.font = '700 30px system-ui, sans-serif';
    g.fillText('NORA', 16, 42);
    g.fillStyle = '#8fb2ab';
    g.font = '500 13px system-ui, sans-serif';
    g.fillText('task allocation · scheduling', 16, 64);
    for (let i = 0; i < 6; i++) {
      const x = 16 + (i % 3) * 80;
      const y = 82 + Math.floor(i / 3) * 38;
      g.fillStyle = '#18383c';
      g.fillRect(x, y, 72, 30);
      g.fillStyle = '#5fc3a8';
      g.globalAlpha = 0.8;
      g.fillRect(x + 6, y + 18, 20 + r() * 40, 5);
      g.globalAlpha = 1;
    }
  } else if (kind === 'dash') {
    for (let i = 0; i < 4; i++) {
      const x = 10 + (i % 2) * 122;
      const y = 10 + Math.floor(i / 2) * 72;
      g.fillStyle = '#17363a';
      g.fillRect(x, y, 114, 64);
      g.strokeStyle = i === 3 ? '#e0b45a' : '#5fc3a8';
      g.lineWidth = 2;
      g.beginPath();
      for (let k = 0; k <= 10; k++) {
        const px = x + 6 + k * 10;
        const py = y + 50 - r() * 34;
        if (k) g.lineTo(px, py);
        else g.moveTo(px, py);
      }
      g.stroke();
    }
  } else if (kind === 'chart') {
    g.fillStyle = '#8fb2ab';
    g.font = '600 13px system-ui, sans-serif';
    g.fillText('assignments', 14, 22);
    for (let i = 0; i < 9; i++) {
      const h = 20 + r() * 100;
      g.fillStyle = i % 3 === 0 ? '#e0b45a' : '#5fc3a8';
      g.fillRect(16 + i * 26, 146 - h, 16, h);
    }
  } else if (kind === 'scope') {
    g.strokeStyle = '#1e4a44';
    for (let x = 0; x < 256; x += 32) g.strokeRect(x, 0, 32, 160);
    g.strokeStyle = '#7ef0b0';
    g.lineWidth = 3;
    g.beginPath();
    for (let x = 0; x < 256; x += 4) {
      const y = 80 + Math.sin(x / 18 + seed) * 40 * Math.exp(-x / 300);
      if (x) g.lineTo(x, y);
      else g.moveTo(x, y);
    }
    g.stroke();
  } else if (kind === 'doc') {
    g.fillStyle = '#b9c3bf';
    for (let y = 18; y < 150; y += 12) g.fillRect(18, y, 120 + r() * 100, 4);
  }

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  if (tall) {
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 0.5);
  }
  return { tex, scroll: tall ? 0.02 + r() * 0.03 : 0 };
}

export function createKit() {
  const mats = new Map();
  const screens = [];
  const blinkers = [];
  const skies = [];

  function mat(color, { rough = 0.85, metal = 0, emissive = null, ei = 0, opacity = 1, flat = false } = {}) {
    const key = [color, rough, metal, emissive, ei, opacity, flat].join('|');
    if (!mats.has(key)) {
      const m = new THREE.MeshStandardMaterial({ color, roughness: rough, metalness: metal, flatShading: flat });
      if (emissive) {
        m.emissive = new THREE.Color(emissive);
        m.emissiveIntensity = ei;
      }
      if (opacity < 1) {
        m.transparent = true;
        m.opacity = opacity;
        m.depthWrite = false;
      }
      mats.set(key, m);
    }
    return mats.get(key);
  }

  function blinker(color, base, rate) {
    const m = new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: base });
    blinkers.push({ material: m, base, rate, phase: Math.random() * 6 });
    return m;
  }

  function add(parent, geo, material, x = 0, y = 0, z = 0, shadow = true) {
    const m = new THREE.Mesh(geo, material);
    m.position.set(x, y, z);
    m.castShadow = shadow;
    m.receiveShadow = true;
    parent.add(m);
    return m;
  }
  const box = (p, w, h, d, material, x, y, z, shadow) => add(p, new THREE.BoxGeometry(w, h, d), material, x, y, z, shadow);
  const cyl = (p, r1, r2, h, material, x, y, z, seg = 18) => add(p, new THREE.CylinderGeometry(r1, r2, h, seg), material, x, y, z);

  function screen(p, w, h, kind, seed, x, y, z) {
    const { tex, scroll } = screenTexture(kind, seed);
    const m = new THREE.MeshStandardMaterial({ color: '#000000', emissive: '#ffffff', emissiveMap: tex, emissiveIntensity: 1, roughness: 0.35 });
    screens.push({ material: m, texture: tex, scroll });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m);
    mesh.position.set(x, y, z);
    p.add(mesh);
    return mesh;
  }

  function monitor(p, { w = 0.56, h = 0.34, kind = 'queue', seed = 1, x = 0, y = 0.74, z = 0, rot = 0 } = {}) {
    const g = new THREE.Group();
    g.position.set(x, y, z);
    g.rotation.y = rot;
    p.add(g);
    box(g, 0.22, 0.015, 0.16, mat(C.dark), 0, 0.008, 0);
    box(g, 0.04, 0.2, 0.03, mat(C.dark), 0, 0.11, -0.03);
    box(g, w + 0.03, h + 0.03, 0.03, mat(C.dark, { rough: 0.5 }), 0, 0.2 + h / 2, -0.01);
    screen(g, w, h, kind, seed, 0, 0.2 + h / 2, 0.0075);
    return g;
  }

  function laptop(p, x, y, z, rot = 0, seed = 5) {
    const g = new THREE.Group();
    g.position.set(x, y, z);
    g.rotation.y = rot;
    p.add(g);
    box(g, 0.32, 0.015, 0.22, mat(C.metal, { rough: 0.4, metal: 0.5 }), 0, 0.008, 0);
    const lid = new THREE.Group();
    lid.position.set(0, 0.015, -0.11);
    lid.rotation.x = -0.25;
    g.add(lid);
    box(lid, 0.32, 0.21, 0.01, mat(C.metal, { rough: 0.4, metal: 0.5 }), 0, 0.105, 0);
    screen(lid, 0.29, 0.18, 'code', seed, 0, 0.105, 0.0065);
  }

  function keyboard(p, x, y, z) {
    box(p, 0.42, 0.02, 0.14, mat(C.plastic), x, y + 0.01, z);
  }

  function lamp(p, x, y, z) {
    cyl(p, 0.06, 0.07, 0.02, mat(C.dark), x, y + 0.01, z);
    box(p, 0.015, 0.36, 0.015, mat(C.dark), x, y + 0.2, z);
    const head = box(p, 0.16, 0.04, 0.08, mat(C.dark), x - 0.05, y + 0.38, z + 0.04);
    head.rotation.z = 0.2;
    box(p, 0.1, 0.006, 0.05, mat('#fff4dd', { emissive: '#ffd9a8', ei: 0.8 }), x - 0.05, y + 0.355, z + 0.04, false);
    return [x - 0.05, y + 0.3, z + 0.12];
  }

  function tableTop(g, w, d, h, color = C.laminate) {
    box(g, w, 0.04, d, mat(color, { rough: 0.6 }), 0, h - 0.02, 0);
    for (const sx of [-1, 1]) box(g, 0.04, h - 0.04, d - 0.06, mat(C.metal, { rough: 0.5, metal: 0.4 }), sx * (w / 2 - 0.05), (h - 0.04) / 2, 0);
    box(g, w - 0.12, 0.32, 0.02, mat(C.metal, { rough: 0.5, metal: 0.4 }), 0, h - 0.24, -d / 2 + 0.05);
  }

  const props = {
    desk(o = {}) {
      const { w = 1.4, d = 0.7, h = 0.74 } = o;
      const g = new THREE.Group();
      tableTop(g, w, d, h);
      const lights = [];
      if (o.monitor) monitor(g, { kind: o.monitor, seed: 3, z: -d / 2 + 0.18, y: h });
      if (o.laptop) laptop(g, -w / 2 + 0.3, h, 0.02, 0.3);
      keyboard(g, 0, h, 0.08);
      if (o.lamp) lights.push(lamp(g, w / 2 - 0.16, h, -d / 2 + 0.14));
      return { group: g, footprint: [w, d], lights };
    },

    opsDesk(o = {}) {
      const w = 3.0, d = 0.9, h = 0.74;
      const g = new THREE.Group();
      tableTop(g, w, d, h);
      monitor(g, { kind: 'queue', seed: 11, x: -0.85, y: h, z: -0.18, rot: 0.25 });
      monitor(g, { kind: 'code', seed: 12, x: 0, y: h, z: -0.24, w: 0.62, h: 0.37 });
      monitor(g, { kind: 'dash', seed: 13, x: 0.85, y: h, z: -0.18, rot: -0.25 });
      keyboard(g, 0, h, 0.12);
      cyl(g, 0.04, 0.035, 0.1, mat('#e8e2d6'), 0.45, h + 0.05, 0.18, 12);
      box(g, 0.22, 0.02, 0.3, mat(C.paper), -0.55, h + 0.01, 0.2);
      const lights = o.lamp ? [lamp(g, 1.3, h, -0.2)] : [];
      return { group: g, footprint: [w, d], lights };
    },

    workstation(o = {}) {
      const w = 1.4, d = 0.7, h = 0.74;
      const g = new THREE.Group();
      tableTop(g, w, d, h);
      monitor(g, { kind: 'code', seed: 21, z: -0.16, y: h, w: 0.62, h: 0.37 });
      keyboard(g, 0, h, 0.1);
      box(g, 0.1, 0.03, 0.14, mat(C.dark), 0.45, h + 0.015, 0.12);
      box(g, 0.05, 0.004, 0.03, mat('#5fc3a8', { emissive: '#5fc3a8', ei: 1 }), 0.45, h + 0.032, 0.1, false);
      const lights = o.lamp ? [lamp(g, -0.52, h, -0.18)] : [];
      return { group: g, footprint: [w, d], lights };
    },

    chair() {
      const g = new THREE.Group();
      cyl(g, 0.27, 0.27, 0.03, mat(C.dark), 0, 0.05, 0, 5);
      cyl(g, 0.025, 0.025, 0.36, mat(C.metal, { metal: 0.5, rough: 0.4 }), 0, 0.25, 0, 8);
      box(g, 0.48, 0.07, 0.46, mat(C.fabric), 0, 0.46, 0);
      box(g, 0.46, 0.5, 0.06, mat(C.fabric), 0, 0.78, -0.21);
      return { group: g, footprint: [0.55, 0.55], lights: [] };
    },

    serverRack() {
      const g = new THREE.Group();
      box(g, 0.7, 2.1, 1.0, mat(C.rack, { rough: 0.6, metal: 0.3 }), 0, 1.05, 0);
      box(g, 0.64, 1.96, 0.02, mat(C.rackDoor, { rough: 0.5, metal: 0.4 }), 0, 1.05, 0.505);
      for (let i = 0; i < 12; i++) box(g, 0.5, 0.012, 0.01, mat('#1b2123'), 0, 0.25 + i * 0.14, 0.52, false);
      const leds = ['#5fe0a0', '#5fe0a0', '#e0b45a', '#5fe0a0'].map((c, i) => blinker(c, i === 2 ? 1.4 : 1.6, 1.3 + i * 0.9 + Math.random()));
      for (let row = 0; row < 11; row++)
        for (let col = 0; col < 2; col++)
          box(g, 0.035, 0.014, 0.01, leds[(row + col * 3) % leds.length], 0.2 + col * 0.06, 0.3 + row * 0.14, 0.525, false);
      return { group: g, footprint: [0.7, 1.0], lights: [] };
    },

    glassPartition(o = {}) {
      const len = o.len || 3, h = 2.4;
      const g = new THREE.Group();
      const alu = mat(C.frame, { rough: 0.4, metal: 0.5 });
      box(g, len, 0.05, 0.07, alu, 0, 0.025, 0);
      box(g, len, 0.05, 0.07, alu, 0, h, 0);
      const posts = Math.max(2, Math.ceil(len / 1.6) + 1);
      for (let i = 0; i < posts; i++) box(g, 0.05, h, 0.07, alu, -len / 2 + (i * len) / (posts - 1), h / 2, 0);
      box(g, len, h - 0.05, 0.012, mat(C.glass, { rough: 0.1, metal: 0.1, opacity: 0.22 }), 0, h / 2, 0, false);
      return { group: g, footprint: [len, 0.12], lights: [] };
    },

    noraWall() {
      const g = new THREE.Group();
      const kinds = ['queue', 'nora', 'dash'];
      kinds.forEach((kind, i) => {
        const x = (i - 1) * 1.02;
        const w = i === 1 ? 0.95 : 0.9, h = i === 1 ? 0.6 : 0.55;
        box(g, w + 0.05, h + 0.05, 0.04, mat(C.dark, { rough: 0.5 }), x, 0, 0.02);
        screen(g, w, h, kind, 40 + i, x, 0, 0.042);
      });
      box(g, 3.1, 0.03, 0.03, mat('#5fc3a8', { emissive: '#5fc3a8', ei: 0.6 }), 0, -0.4, 0.02, false);
      return { group: g, footprint: null, lights: [] };
    },

    staffBoard() {
      const g = new THREE.Group();
      box(g, 1.85, 1.05, 0.04, mat(C.dark, { rough: 0.5 }), 0, 0, 0.02);
      screen(g, 1.8, 1.0, 'chart', 77, 0, 0, 0.042);
      return { group: g, footprint: null, lights: [] };
    },

    whiteboard() {
      const g = new THREE.Group();
      const w = 2.0, h = 1.1;
      box(g, w + 0.05, h + 0.05, 0.03, mat(C.metal, { rough: 0.4, metal: 0.5 }), 0, 0, 0.015);
      box(g, w, h, 0.01, mat('#fbfbf8', { rough: 0.3 }), 0, 0, 0.032, false);
      const ink = [mat('#3f6177'), mat('#9b5b4f'), mat('#527a58')];
      for (let i = 0; i < 7; i++) box(g, 0.3 + (i % 3) * 0.25, 0.012, 0.004, ink[i % 3], -0.55 + (i % 2) * 0.6, 0.38 - i * 0.11, 0.04, false);
      box(g, w * 0.6, 0.03, 0.07, mat(C.metal), 0, -h / 2 - 0.03, 0.04);
      return { group: g, footprint: null, lights: [] };
    },

    /** Wall card, or a floor stand when opts.stand is set. A hotspot id makes it readable. */
    postedNote(o = {}) {
      const g = new THREE.Group();
      const ink = mat('#3f6177');
      const ink2 = mat('#527a58');
      if (o.stand) {
        box(g, 0.34, 0.46, 0.02, mat(C.paper), 0, 0.58, 0);
        box(g, 0.2, 0.012, 0.006, ink, 0, 0.7, 0.012, false);
        box(g, 0.16, 0.008, 0.006, ink2, 0, 0.62, 0.012, false);
        box(g, 0.26, 0.02, 0.16, mat(C.metal, { metal: 0.4, rough: 0.45 }), 0, 0.02, 0.05);
        return { group: g, footprint: [0.4, 0.28], lights: [] };
      }
      box(g, 0.42, 0.32, 0.015, mat(C.paper), 0, 0, 0.02);
      box(g, 0.26, 0.012, 0.004, ink, 0, 0.08, 0.03, false);
      box(g, 0.2, 0.008, 0.004, ink2, 0, 0.02, 0.03, false);
      box(g, 0.16, 0.008, 0.004, mat('#9b5b4f'), 0, -0.05, 0.03, false);
      return { group: g, footprint: null, lights: [] };
    },

    securityCamera() {
      const g = new THREE.Group();
      box(g, 0.08, 0.08, 0.22, mat(C.plastic), 0, 0, 0.11);
      const head = new THREE.Group();
      head.position.set(0, -0.06, 0.26);
      head.rotation.x = 0.45;
      head.rotation.y = 0.5;
      g.add(head);
      box(head, 0.12, 0.1, 0.24, mat(C.plastic, { rough: 0.5 }), 0, 0, 0);
      const lens = cyl(head, 0.035, 0.035, 0.02, mat('#111'), 0, 0, 0.125, 14);
      lens.rotation.x = Math.PI / 2;
      box(head, 0.015, 0.015, 0.01, blinker('#ff3b3b', 2, 1.1), 0.04, 0.035, 0.122, false);
      return { group: g, footprint: null, lights: [] };
    },

    bench(o = {}) {
      const w = o.len || 3.4, d = 0.9, h = 0.86;
      const g = new THREE.Group();
      tableTop(g, w, d, h, C.benchTop);
      [-1.1, -0.45, 1.15].forEach((x, i) => {
        box(g, 0.45, 0.24, 0.34, mat(C.instrument, { rough: 0.6 }), x, h + 0.12, -0.15);
        screen(g, 0.2, 0.12, 'scope', 50 + i, x - 0.08, h + 0.14, 0.022);
        for (let k = 0; k < 3; k++) cyl(g, 0.018, 0.018, 0.02, mat(C.dark), x + 0.08 + k * 0.05, h + 0.1, 0.03, 10).rotation.x = Math.PI / 2;
      });
      monitor(g, { kind: 'dash', seed: 55, x: 0.35, y: h, z: -0.22 });
      const coil = add(g, new THREE.TorusGeometry(0.09, 0.012, 6, 18), mat('#2d3a3d'), -0.1, h + 0.012, 0.22);
      coil.rotation.x = Math.PI / 2;
      const lights = o.lamp ? [lamp(g, w / 2 - 0.25, h, -0.3)] : [];
      return { group: g, footprint: [w, d], lights };
    },

    bigScreen() {
      const g = new THREE.Group();
      for (const sx of [-0.6, 0.6]) {
        box(g, 0.05, 1.9, 0.05, mat(C.dark), sx, 0.95, 0);
        box(g, 0.08, 0.03, 0.5, mat(C.dark), sx, 0.015, 0);
      }
      box(g, 1.66, 0.97, 0.05, mat(C.dark, { rough: 0.5 }), 0, 1.45, 0.03);
      screen(g, 1.6, 0.9, 'dash', 61, 0, 1.45, 0.057);
      return { group: g, footprint: [1.6, 0.5], lights: [] };
    },

    documentTable(o = {}) {
      const w = 1.0, d = 0.7, h = 0.74;
      const g = new THREE.Group();
      box(g, w, 0.04, d, mat(C.laminate, { rough: 0.6 }), 0, h - 0.02, 0);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) box(g, 0.04, h - 0.04, 0.04, mat(C.metal, { metal: 0.4, rough: 0.5 }), sx * (w / 2 - 0.06), (h - 0.04) / 2, sz * (d / 2 - 0.06));
      if (o.kind === 'folder') {
        const f = box(g, 0.24, 0.025, 0.32, mat(C.folder, { rough: 0.7 }), -0.12, h + 0.013, 0.02);
        f.rotation.y = 0.15;
      } else {
        const b = box(g, 0.28, 0.07, 0.32, mat(C.binder, { rough: 0.6 }), -0.14, h + 0.035, 0.02);
        b.rotation.y = -0.12;
        box(g, 0.02, 0.07, 0.32, mat('#f2f2ee'), -0.27, h + 0.035, 0.035).rotation.y = -0.12;
      }
      box(g, 0.22, 0.02, 0.3, mat(C.paper), 0.18, h + 0.01, -0.08);
      box(g, 0.25, 0.012, 0.18, mat(C.dark), 0.24, h + 0.006, 0.18);
      const doc = screen(g, 0.22, 0.15, 'doc', 70, 0.24, h + 0.0135, 0.18);
      doc.rotation.x = -Math.PI / 2;
      const lights = o.lamp ? [lamp(g, 0.4, h, -0.24)] : [];
      return { group: g, footprint: [w, d], lights };
    },

    cabinet() {
      const g = new THREE.Group();
      box(g, 0.8, 0.9, 0.5, mat(C.laminate, { rough: 0.6 }), 0, 0.45, 0);
      for (let i = 0; i < 3; i++) {
        box(g, 0.76, 0.006, 0.01, mat('#c8c8c2'), 0, 0.3 + i * 0.29, 0.252, false);
        box(g, 0.14, 0.02, 0.02, mat(C.metal, { metal: 0.6, rough: 0.3 }), 0, 0.17 + i * 0.29, 0.26);
      }
      return { group: g, footprint: [0.8, 0.5], lights: [] };
    },

    bookshelf(o = {}) {
      const w = o.w || 1.6, h = 1.9, d = 0.38;
      const g = new THREE.Group();
      const wood = mat('#cdb593', { rough: 0.7 });
      for (const sx of [-1, 1]) box(g, 0.03, h, d, wood, sx * (w / 2 - 0.015), h / 2, 0);
      box(g, w, h, 0.02, wood, 0, h / 2, -d / 2 + 0.01);
      const r = rng(9);
      for (let s = 0; s < 5; s++) {
        const y = 0.04 + s * 0.45;
        box(g, w - 0.06, 0.025, d - 0.02, wood, 0, y, 0);
        if (s === 4) continue;
        let x = -w / 2 + 0.06;
        while (x < w / 2 - 0.12) {
          const bw = 0.03 + r() * 0.04, bh = 0.22 + r() * 0.14;
          box(g, bw, bh, 0.22, mat(C.books[Math.floor(r() * C.books.length)], { rough: 0.8 }), x + bw / 2, y + 0.013 + bh / 2, 0.02);
          x += bw + 0.004 + (r() > 0.85 ? 0.08 : 0);
        }
      }
      return { group: g, footprint: [w, d], lights: [] };
    },

    roundTable() {
      const g = new THREE.Group();
      cyl(g, 0.6, 0.6, 0.04, mat(C.laminate, { rough: 0.55 }), 0, 0.73, 0, 32);
      cyl(g, 0.05, 0.05, 0.7, mat(C.metal, { metal: 0.5, rough: 0.4 }), 0, 0.36, 0, 10);
      cyl(g, 0.3, 0.32, 0.03, mat(C.dark), 0, 0.015, 0, 24);
      box(g, 0.21, 0.01, 0.29, mat(C.paper), 0.15, 0.755, -0.1);
      cyl(g, 0.04, 0.035, 0.1, mat('#e8e2d6'), -0.2, 0.8, 0.15, 12);
      return { group: g, footprint: [1.2, 1.2], lights: [] };
    },

    sofa() {
      const w = 2.0, d = 0.85;
      const g = new THREE.Group();
      const f = mat(C.sofa, { rough: 0.95 });
      box(g, w, 0.4, d, f, 0, 0.2, 0);
      box(g, w, 0.45, 0.18, f, 0, 0.62, -d / 2 + 0.09);
      for (const sx of [-1, 1]) box(g, 0.16, 0.55, d, f, sx * (w / 2 - 0.08), 0.28, 0);
      for (const sx of [-1, 1]) box(g, w / 2 - 0.18, 0.12, d - 0.22, mat('#667b7f', { rough: 0.95 }), sx * (w / 4 - 0.04), 0.46, 0.06);
      return { group: g, footprint: [w, d], lights: [] };
    },

    standingTable(o = {}) {
      const g = new THREE.Group();
      cyl(g, 0.36, 0.36, 0.035, mat(C.laminate, { rough: 0.55 }), 0, 1.05, 0, 28);
      cyl(g, 0.035, 0.035, 1.03, mat(C.metal, { metal: 0.5, rough: 0.4 }), 0, 0.52, 0, 10);
      cyl(g, 0.24, 0.26, 0.025, mat(C.dark), 0, 0.012, 0, 20);
      laptop(g, 0, 1.068, 0.03, -0.4, 31);
      if (o.card) {
        box(g, 0.16, 0.006, 0.11, mat(C.paper), 0.16, 1.074, -0.06);
        box(g, 0.1, 0.004, 0.006, mat('#3f6177'), 0.16, 1.08, -0.08, false);
        box(g, 0.08, 0.003, 0.005, mat('#527a58'), 0.16, 1.08, -0.05, false);
      }
      return { group: g, footprint: [0.72, 0.72], lights: [] };
    },

    plant(o = {}) {
      const s = o.size || 1;
      const g = new THREE.Group();
      cyl(g, 0.2 * s, 0.15 * s, 0.38 * s, mat(C.pot, { rough: 0.8 }), 0, 0.19 * s, 0, 16);
      cyl(g, 0.18 * s, 0.18 * s, 0.02, mat(C.soil), 0, 0.37 * s, 0, 16);
      const r = rng(Math.round(s * 100));
      for (let i = 0; i < 6; i++) {
        const rad = (0.14 + r() * 0.12) * s;
        const leaf = add(g, new THREE.IcosahedronGeometry(rad, 0), mat(i % 2 ? C.leaf : C.leafDark, { rough: 0.9, flat: true }),
          (r() - 0.5) * 0.3 * s, (0.55 + r() * 0.55) * s, (r() - 0.5) * 0.3 * s);
        leaf.rotation.set(r() * 3, r() * 3, r() * 3);
      }
      return { group: g, footprint: [0.45 * s, 0.45 * s], lights: [] };
    },

    rug(o = {}) {
      const w = o.w || 2.5, d = o.d || 2;
      const g = new THREE.Group();
      box(g, w, 0.012, d, mat(C.rugBorder, { rough: 1 }), 0, 0.006, 0, false);
      box(g, w - 0.16, 0.014, d - 0.16, mat(C.rug, { rough: 1 }), 0, 0.007, 0, false);
      return { group: g, footprint: null, lights: [] };
    },
  };

  function update(dt, t, screenIntensity) {
    for (const s of screens) {
      s.material.emissiveIntensity = screenIntensity;
      if (s.scroll) s.texture.offset.y = (s.texture.offset.y + dt * s.scroll) % 1;
    }
    for (const b of blinkers) b.material.emissiveIntensity = Math.sin(t * b.rate + b.phase) > -0.2 ? b.base : b.base * 0.12;
  }

  function sky(material) {
    skies.push(material);
  }

  return { props, mat, update, sky, skies };
}
