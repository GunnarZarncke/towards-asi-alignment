/** Walkable grid over a room floor, A* with string-pulled waypoints. Pure; no Three.js. */

const SQRT2 = Math.SQRT2;
const NEIGHBOURS = [[1, 0, 1], [-1, 0, 1], [0, 1, 1], [0, -1, 1], [1, 1, SQRT2], [1, -1, SQRT2], [-1, 1, SQRT2], [-1, -1, SQRT2]];

export class NavGrid {
  constructor({ minX, maxX, minZ, maxZ, cell = 0.2 }) {
    Object.assign(this, { minX, maxX, minZ, maxZ, cell });
    this.cols = Math.floor((maxX - minX) / cell) + 1;
    this.rows = Math.floor((maxZ - minZ) / cell) + 1;
    this.blocked = new Uint8Array(this.cols * this.rows);
  }

  idx(i, j) {
    return j * this.cols + i;
  }
  inside(i, j) {
    return i >= 0 && j >= 0 && i < this.cols && j < this.rows;
  }
  free(i, j) {
    return this.inside(i, j) && !this.blocked[this.idx(i, j)];
  }
  toCell(x, z) {
    return [Math.round((x - this.minX) / this.cell), Math.round((z - this.minZ) / this.cell)];
  }
  toWorld(i, j) {
    return [this.minX + i * this.cell, this.minZ + j * this.cell];
  }
  clampCell(i, j) {
    return [Math.max(0, Math.min(this.cols - 1, i)), Math.max(0, Math.min(this.rows - 1, j))];
  }

  /** Block an axis-aligned footprint (rotation in degrees, multiples of 90 are exact). */
  blockRect(cx, cz, w, d, rotDeg = 0, inflate = 0) {
    const a = (rotDeg * Math.PI) / 180;
    const c = Math.abs(Math.cos(a)), s = Math.abs(Math.sin(a));
    const hw = (w * c + d * s) / 2 + inflate;
    const hd = (w * s + d * c) / 2 + inflate;
    for (let j = 0; j < this.rows; j++)
      for (let i = 0; i < this.cols; i++) {
        const [x, z] = this.toWorld(i, j);
        if (Math.abs(x - cx) <= hw && Math.abs(z - cz) <= hd) this.blocked[this.idx(i, j)] = 1;
      }
  }

  nearestFree(i, j) {
    [i, j] = this.clampCell(i, j);
    if (this.free(i, j)) return [i, j];
    const seen = new Uint8Array(this.cols * this.rows);
    const queue = [[i, j]];
    seen[this.idx(i, j)] = 1;
    while (queue.length) {
      const [ci, cj] = queue.shift();
      for (const [di, dj] of NEIGHBOURS) {
        const ni = ci + di, nj = cj + dj;
        if (!this.inside(ni, nj) || seen[this.idx(ni, nj)]) continue;
        if (this.free(ni, nj)) return [ni, nj];
        seen[this.idx(ni, nj)] = 1;
        queue.push([ni, nj]);
      }
    }
    return null;
  }

  /** Nearest walkable world point to (x, z). */
  snap(x, z) {
    const c = this.nearestFree(...this.toCell(x, z));
    if (!c) return [x, z];
    const [ci, cj] = this.toCell(x, z);
    if (c[0] === ci && c[1] === cj && x >= this.minX && x <= this.maxX && z >= this.minZ && z <= this.maxZ) return [x, z];
    return this.toWorld(...c);
  }

  lineOfSight(a, b) {
    const [ax, az] = a, [bx, bz] = b;
    const len = Math.hypot(bx - ax, bz - az);
    const steps = Math.max(1, Math.ceil(len / (this.cell * 0.35)));
    for (let k = 0; k <= steps; k++) {
      const t = k / steps;
      const [i, j] = this.toCell(ax + (bx - ax) * t, az + (bz - az) * t);
      if (!this.free(i, j)) return false;
    }
    return true;
  }

  /** Waypoints from `from` to `to` (world [x, z]), excluding the start. Null when unreachable. */
  findPath(from, to) {
    const start = this.nearestFree(...this.toCell(...from));
    const goalPoint = this.snap(...to);
    const goal = this.nearestFree(...this.toCell(...goalPoint));
    if (!start || !goal) return null;

    const n = this.cols * this.rows;
    const g = new Float32Array(n).fill(Infinity);
    const came = new Int32Array(n).fill(-1);
    const closed = new Uint8Array(n);
    const heap = new MinHeap();
    const s = this.idx(...start), e = this.idx(...goal);
    const h = (i, j) => {
      const dx = Math.abs(i - goal[0]), dy = Math.abs(j - goal[1]);
      return dx + dy + (SQRT2 - 2) * Math.min(dx, dy);
    };
    g[s] = 0;
    heap.push(s, h(...start));
    while (heap.size) {
      const cur = heap.pop();
      if (cur === e) break;
      if (closed[cur]) continue;
      closed[cur] = 1;
      const ci = cur % this.cols, cj = (cur / this.cols) | 0;
      for (const [di, dj, cost] of NEIGHBOURS) {
        const ni = ci + di, nj = cj + dj;
        if (!this.free(ni, nj)) continue;
        if (di && dj && (!this.free(ci + di, cj) || !this.free(ci, cj + dj))) continue;
        const k = this.idx(ni, nj);
        const ng = g[cur] + cost;
        if (ng < g[k]) {
          g[k] = ng;
          came[k] = cur;
          heap.push(k, ng + h(ni, nj));
        }
      }
    }
    if (s !== e && came[e] < 0) return null;

    const cells = [];
    for (let k = e; k >= 0; k = k === s ? -1 : came[k]) cells.push(this.toWorld(k % this.cols, (k / this.cols) | 0));
    cells.reverse();
    cells[cells.length - 1] = goalPoint;

    const out = [];
    let anchor = from;
    for (let k = 1; k < cells.length; k++) {
      if (!this.lineOfSight(anchor, cells[k])) {
        out.push(cells[k - 1]);
        anchor = cells[k - 1];
      }
    }
    out.push(goalPoint);
    return out;
  }
}

class MinHeap {
  constructor() {
    this.items = [];
    this.keys = [];
  }
  get size() {
    return this.items.length;
  }
  push(item, key) {
    const a = this.items, k = this.keys;
    a.push(item);
    k.push(key);
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (k[p] <= k[i]) break;
      [a[p], a[i]] = [a[i], a[p]];
      [k[p], k[i]] = [k[i], k[p]];
      i = p;
    }
  }
  pop() {
    const a = this.items, k = this.keys;
    const top = a[0];
    const lastItem = a.pop(), lastKey = k.pop();
    if (a.length) {
      a[0] = lastItem;
      k[0] = lastKey;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < a.length && k[l] < k[m]) m = l;
        if (r < a.length && k[r] < k[m]) m = r;
        if (m === i) break;
        [a[m], a[i]] = [a[i], a[m]];
        [k[m], k[i]] = [k[i], k[m]];
        i = m;
      }
    }
    return top;
  }
}
