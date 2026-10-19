import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { newSession } from '../lib/game.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import { buildEventRow, playTelemetry, initTelemetryLog, appendTelemetryRow } from '../lib/telemetry.mjs';

test('engine events carry fuel, room, act, npc, and knowledge', () => {
  const s = newSession();
  const go = applyAction(s, 'go', { room: 'collab' });
  assert.ok(!go.error, go.error);
  const move = s.events.find(e => e.kind === 'move' && e.who === 'player');
  assert.equal(move.room, 'collab');
  assert.equal(move.act, 'welcome');
  assert.equal(s.fuelSpent, 1);
  assert.equal(move.npc, null);

  applyAction(s, 'respond', {
    parse: { kind: 'ask', relation: 'about', topic: 'shutdown', object: null, subject: null, recipient: null, evidence: null, open_slot: 'none', source: 'completion' },
    addressee: 'ian',
    text: 'What is in scope for today?',
  });
  const action = s.events.findLast(e => e.kind === 'action' && e.action === 'respond');
  assert.equal(action.npc, 'ian');
  assert.equal(action.room, 'collab');
});

test('learn rows set knowledge id', () => {
  const s = newSession();
  applyAction(s, 'go', { room: 'collab' });
  applyAction(s, 'inspect', { id: 'collab_board' });
  const learn = s.events.find(e => e.kind === 'learn');
  assert.ok(learn);
  assert.equal(learn.knowledge, learn.id);
  assert.ok(typeof learn.fuel === 'number');
});

test('playTelemetry matches the last event context', () => {
  const s = newSession();
  applyAction(s, 'go', { room: 'collab' });
  const t = playTelemetry(s);
  assert.equal(t.room, 'collab');
  assert.equal(t.fuel, s.fuelSpent);
  assert.equal(t.act, 'welcome');
});

test('appendTelemetryRow writes JSONL when configured', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'lsr-tel-'));
  const file = path.join(dir, 'play.jsonl');
  initTelemetryLog({ TELEMETRY_LOG: file });
  appendTelemetryRow({ fuel: 3, room: 'commons', act: 'welcome', npc: 'ian', knowledge: null }, { sid: 'test-sid' });
  const line = JSON.parse(readFileSync(file, 'utf8').trim());
  assert.equal(line.room, 'commons');
  assert.equal(line.sid, 'test-sid');
  initTelemetryLog({});
});

test('buildEventRow is stable for replay import shape', () => {
  const s = newSession();
  const row = buildEventRow(s, 'action', { action: 'go', args: { room: 'commons' } });
  assert.equal(row.kind, 'action');
  assert.equal(row.room, s.room);
});
