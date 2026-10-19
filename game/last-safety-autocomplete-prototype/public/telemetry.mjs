/** Client play telemetry (local history + optional beacon), aligned with the companion site visit recorder. */
export const PLAY_TELEMETRY_KEY = 'lsr-play-telemetry-v1';
export const PLAY_TELEMETRY_MAX = 500;

/** Same token as site/src/lib/seo.ts — public, cookieless page analytics when hosted. */
export const CF_WEB_ANALYTICS_TOKEN = '415dc5b7862f4b47a7f41047bbd6c81e';

export function parsePlayHistory(raw) {
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter(row => row && typeof row === 'object' && Number.isFinite(row.fuel) && typeof row.room === 'string' && typeof row.act === 'string')
      .slice(0, PLAY_TELEMETRY_MAX);
  } catch {
    return [];
  }
}

function sameStep(a, b) {
  return a.fuel === b.fuel && a.room === b.room && a.act === b.act && a.npc === b.npc && a.knowledge === b.knowledge;
}

export function prependPlayStep(history, row) {
  const entry = {
    fuel: row.fuel,
    room: row.room,
    act: row.act,
    npc: row.npc ?? null,
    knowledge: row.knowledge ?? null,
    t: Date.now(),
  };
  if (history[0] && sameStep(history[0], entry)) return history;
  return [entry, ...history].slice(0, PLAY_TELEMETRY_MAX);
}

export function recordPlayStep(row) {
  if (!row || typeof row !== 'object') return;
  try {
    const history = parsePlayHistory(localStorage.getItem(PLAY_TELEMETRY_KEY));
    localStorage.setItem(PLAY_TELEMETRY_KEY, JSON.stringify(prependPlayStep(history, row)));
  } catch {
    // private mode / blocked storage
  }
}

export function maybeSendPlayBeacon(row) {
  if (!row || typeof navigator.sendBeacon !== 'function') return;
  try {
    navigator.sendBeacon('/api/telemetry', JSON.stringify(row));
  } catch {
    // ignore
  }
}

export function installCloudflareWebAnalytics() {
  const host = location.hostname;
  if (!CF_WEB_ANALYTICS_TOKEN || host === 'localhost' || host === '127.0.0.1') return;
  if (document.querySelector('script[data-cf-beacon]')) return;
  const s = document.createElement('script');
  s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  s.dataset.cfBeacon = JSON.stringify({ token: CF_WEB_ANALYTICS_TOKEN });
  document.head.appendChild(s);
}
