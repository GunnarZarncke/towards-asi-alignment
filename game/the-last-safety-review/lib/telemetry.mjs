/**
 * Play telemetry: fuel index, room, act, optional npc and knowledge id.
 * Server may append JSONL when TELEMETRY_LOG is set; the browser mirrors rows in localStorage
 * (same privacy posture as the companion site visit history + Cloudflare Web Analytics).
 */
import { appendFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

/** Public Cloudflare Web Analytics token (same project as towards-alignment.com). */
export const CF_WEB_ANALYTICS_TOKEN = '415dc5b7862f4b47a7f41047bbd6c81e';

const ACTORish = new Set([
  'ian', 'amara', 'pavel', 'leila', 'elena', 'daniel', 'justine', 'jun', 'nora',
]);

function extractNpc(kind, payload) {
  if (typeof payload.npc === 'string') return payload.npc;
  if (payload.who && payload.who !== 'player') return payload.who;
  if (payload.from && ACTORish.has(payload.from)) return payload.from;
  if (typeof payload.addressee === 'string') return payload.addressee;
  if (kind === 'action' && payload.args) {
    const a = payload.args;
    if (payload.action === 'respond') return a.addressee ?? null;
    if (payload.action === 'dm.send') return a.to ?? null;
  }
  return null;
}

function extractKnowledge(kind, payload) {
  if (kind === 'learn' && payload.id) return payload.id;
  if (payload.fact) return payload.fact;
  if (kind === 'npc_turn') {
    return payload.pick?.fact ?? payload.initiative?.fact ?? null;
  }
  if (kind === 'npc_move') return payload.move?.fact ?? null;
  if (kind === 'action') {
    if (payload.action === 'inspect') return payload.args?.id ?? null;
    if (payload.action === 'tool' && payload.args?.facts?.[0]) return payload.args.facts[0];
  }
  return null;
}

/** One engine log row with session context (fuel = spent index at this step). */
export function buildEventRow(s, kind, payload = {}) {
  const npc = extractNpc(kind, payload);
  const knowledge = extractKnowledge(kind, payload);
  return {
    i: s.events.length,
    fuel: s.fuelSpent,
    act: s.act,
    room: s.room,
    npc,
    knowledge,
    kind,
    ...payload,
  };
}

/** Snapshot for API responses and client recording after a mutating action. */
export function playTelemetry(s) {
  const ev = s.events.at(-1);
  return {
    fuel: s.fuelSpent,
    act: s.act,
    room: s.room,
    npc: ev?.npc ?? null,
    knowledge: ev?.knowledge ?? null,
  };
}

let telemetryLogPath = null;

export function initTelemetryLog(env = process.env) {
  const raw = env.TELEMETRY_LOG?.trim();
  if (!raw) {
    telemetryLogPath = null;
    return;
  }
  telemetryLogPath = path.resolve(raw);
  mkdirSync(path.dirname(telemetryLogPath), { recursive: true });
}

export function appendTelemetryRow(row, { sid } = {}) {
  if (!telemetryLogPath || !row || typeof row !== 'object') return;
  const line = JSON.stringify({ t: Date.now(), sid: sid ?? null, ...row });
  appendFileSync(telemetryLogPath, `${line}\n`, 'utf8');
}
