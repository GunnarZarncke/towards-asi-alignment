#!/usr/bin/env node
/**
 * Graphics solo harness: static UI + fixture state/scene. No engine, no model.
 */
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { passageError, VISITOR_CLEARANCE } from '../lib/floorplan.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const PUBLIC = path.join(ROOT, 'public');
const FIX = path.join(ROOT, 'fixtures');
const PORT = Number(process.env.UI_DEV_PORT || 3001);

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
};

let sessionState = null;
let sceneOverlay = null;
let cameraMode = 'play';
let actPreset = 'doubt';

async function loadJson(rel) {
  return JSON.parse(await readFile(path.join(FIX, rel), 'utf8'));
}

async function resetSession() {
  sessionState = await loadJson('client-state.json');
  sceneOverlay = await loadJson('scene-platform-doubt.json');
  cameraMode = sceneOverlay.camera || 'play';
  actPreset = sceneOverlay.act || 'doubt';
}

function sceneForRoom(roomId) {
  if (roomId === 'platform' && sceneOverlay?.roomId === 'platform') return { ...sceneOverlay, camera: cameraMode, act: actPreset };
  return { roomId, act: actPreset, camera: cameraMode, lightingPreset: actPreset, annotations: [] };
}

function json(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(data));
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://127.0.0.1:${PORT}`);
    if (url.pathname.startsWith('/api/')) {
      if (url.pathname === '/api/state' && req.method === 'GET') {
        return json(res, 200, { ...sessionState, _devScene: sceneForRoom(sessionState.room) });
      }
      if (url.pathname === '/api/scene' && req.method === 'GET') {
        return json(res, 200, sceneForRoom(sessionState.room));
      }
      if (req.method === 'POST') {
        let body = {};
        try {
          body = JSON.parse((await readBody(req)) || '{}');
        } catch {
          return json(res, 400, { error: 'Invalid JSON' });
        }
        if (url.pathname === '/api/reset') {
          await resetSession();
          return json(res, 200, { state: sessionState, scene: sceneForRoom(sessionState.room) });
        }
        if (url.pathname === '/api/go') {
          const error = passageError(sessionState.room, body.room, sessionState.clearance ?? VISITOR_CLEARANCE);
          if (error) return json(res, 400, { error });
          sessionState.room = body.room;
          return json(res, 200, { state: sessionState, scene: sceneForRoom(body.room) });
        }
        if (url.pathname === '/api/inspect') {
          const id = body.id;
          const ev = sessionState.evidence.find(e => e.id === id);
          if (!ev) return json(res, 400, { error: 'Unknown evidence.' });
          if (ev.room !== sessionState.room) return json(res, 400, { error: 'Travel to the right room first.' });
          ev.examined = true;
          if (!sessionState.examined.includes(id)) sessionState.examined.push(id);
          return json(res, 200, {
            title: ev.title,
            body: '[Fixture] Record text omitted in UI harness — use npm start for full inspect copy.',
            state: sessionState,
          });
        }
        if (url.pathname === '/api/dev/camera') {
          cameraMode = body.camera === 'surveillance' ? 'surveillance' : 'play';
          return json(res, 200, { scene: sceneForRoom(sessionState.room) });
        }
        if (url.pathname === '/api/dev/act') {
          const next = body.act;
          if (['welcome', 'doubt', 'decision'].includes(next)) actPreset = next;
          return json(res, 200, { scene: sceneForRoom(sessionState.room) });
        }
        if (url.pathname === '/api/parse' || url.pathname === '/api/respond') {
          return json(res, 200, {
            parse: { kind: 'open', relation: 'open', confidence: 0.4, source: 'llm' },
            reply: '[UI harness] Parser and NPC replies are disabled. Use npm start for live dialogue.',
            effects: [],
            state: sessionState,
          });
        }
        if (url.pathname === '/api/text' || url.pathname === '/api/tab-complete') {
          return json(res, 503, {
            error: 'Text console needs the full engine. Stop dev:ui and run npm start, then open /text.html on port 3000.',
          });
        }
      }
      return json(res, 404, { error: 'Unknown API endpoint' });
    }

    if (req.method !== 'GET') return json(res, 405, { error: 'Only GET supported' });
    const publicPath = url.pathname === '/' ? '/index.html' : url.pathname;
    const publicLib = new Set(['grammar.mjs', 'floorplan.mjs', 'world/ranking-tables.mjs']);
    const libName = publicPath.startsWith('/lib/') ? publicPath.slice('/lib/'.length) : '';
    if (publicLib.has(libName)) {
      const data = await readFile(path.join(ROOT, 'lib', libName));
      res.writeHead(200, { 'Content-Type': mime['.mjs'], 'Cache-Control': 'no-store' });
      return res.end(data);
    }
    const threeRoot = path.join(ROOT, 'node_modules', 'three', 'build');
    const absolute = publicPath.startsWith('/vendor/three/')
      ? path.resolve(threeRoot, `.${publicPath.slice('/vendor/three'.length)}`)
      : path.resolve(PUBLIC, `.${publicPath}`);
    if (!absolute.startsWith(PUBLIC + path.sep) && !absolute.startsWith(threeRoot + path.sep)) return json(res, 403, { error: 'Forbidden' });
    const data = await readFile(absolute);
    res.writeHead(200, { 'Content-Type': mime[path.extname(absolute)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    res.end(data);
  } catch (e) {
    const m = String(e?.message || e);
    json(res, m.includes('ENOENT') ? 404 : 502, { error: m.slice(0, 280) });
  }
});

async function readBody(req) {
  let s = '';
  for await (const c of req) {
    s += c;
    if (s.length > 50_000) throw new Error('Request too large');
  }
  return s;
}

await resetSession();
server.listen(PORT, '127.0.0.1', () => {
  console.log(`Last Safety Review — UI harness: http://127.0.0.1:${PORT} (fixtures only)`);
});
