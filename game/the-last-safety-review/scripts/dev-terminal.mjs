#!/usr/bin/env node
/**
 * Terminal solo harness: phone UI + frozen TerminalState. No engine, no model.
 */
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const PUBLIC = path.join(ROOT, 'public');
const PORT = Number(process.env.TERMINAL_DEV_PORT || 3002);

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
};

function json(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(data));
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://127.0.0.1:${PORT}`);
    if (url.pathname === '/api/terminal' && req.method === 'GET') {
      const data = await readFile(path.join(ROOT, 'fixtures', 'terminal-session.json'), 'utf8');
      res.writeHead(200, { 'Content-Type': mime['.json'], 'Cache-Control': 'no-store' });
      return res.end(data);
    }
    if (req.method !== 'GET') return json(res, 405, { error: 'Only GET supported' });
    const publicPath = url.pathname === '/' ? '/terminal/index.html' : url.pathname;
    const absolute = path.resolve(PUBLIC, `.${publicPath}`);
    if (!absolute.startsWith(PUBLIC + path.sep)) return json(res, 403, { error: 'Forbidden' });
    const data = await readFile(absolute);
    res.writeHead(200, { 'Content-Type': mime[path.extname(absolute)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    res.end(data);
  } catch (e) {
    const m = String(e?.message || e);
    json(res, m.includes('ENOENT') ? 404 : 502, { error: m.slice(0, 280) });
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Last Safety Review — terminal harness: http://127.0.0.1:${PORT} (fixture phone)`);
});
