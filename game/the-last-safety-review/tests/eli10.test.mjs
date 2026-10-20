import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, applyPhoneSettings } from '../lib/game.mjs';
import { resolveEli10, renderEli10Document, eli10ForInspect } from '../lib/eli10.mjs';

test('applyPhoneSettings toggles eli10Enabled', () => {
  const s = newSession();
  assert.equal(s.eli10Enabled, false);
  applyPhoneSettings(s, { eli10Enabled: true });
  assert.equal(s.eli10Enabled, true);
});

test('prepared document ELI10 renders', () => {
  const text = renderEli10Document('eval-shutdown-report', 'boundary-narrow');
  assert.match(text, /Simple version|simple version/i);
  assert.match(text, /16:02/);
});

test('inspect screen has prepared ELI10', () => {
  const text = eli10ForInspect('shutdown_report');
  assert.ok(text);
  assert.match(text, /16:02/);
});

test('last NPC fact line uses prepared ELI10', async () => {
  const s = newSession();
  s.eli10Enabled = true;
  const line = 'Job 284 was still active at 16:09, after the model session stopped.';
  s.conversations.push({ role: 'npc', npc: 'pavel', text: line, template: line, refs: ['job_284'] });
  const r = await resolveEli10(s, { kind: 'transcript' });
  assert.equal(r.source, 'prepared');
  assert.match(r.text, /284/);
});

test('LLM-phrased line falls back when the model is unavailable', async () => {
  const prev = process.env.DEMO_MODE;
  process.env.DEMO_MODE = '1';
  const s = newSession();
  s.conversations.push({
    role: 'npc',
    npc: 'pavel',
    template: 'Job 284 was still active at 16:09, after the model session stopped.',
    text: 'Well, honestly, job 284 was still humming along at sixteen-oh-nine even after the session halt.',
    refs: [],
  });
  const r = await resolveEli10(s, { kind: 'transcript' });
  if (prev === undefined) delete process.env.DEMO_MODE;
  else process.env.DEMO_MODE = prev;
  assert.match(r.error || '', /Live mode|model budget|No simpler/i);
});
