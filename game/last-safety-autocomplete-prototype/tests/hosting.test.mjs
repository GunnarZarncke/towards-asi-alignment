/**
 * Public-hosting guards: what the phrasing model may see, per-session caps, and the model budget.
 * Stop: a failure here is a leak or an unbounded resource; fix the engine, do not raise the cap.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession, phrasingInput, rephraseLine, clientState, writeNote, importSession } from '../lib/game.mjs';
import { FACTS } from '../lib/world/facts.mjs';
import { CONFIG } from '../lib/world/config.mjs';
import { freeReply } from '../lib/llm.mjs';
import { parseImageDataUrl } from '../lib/photo-data.mjs';
import { applyAction } from './helpers.mjs';

const photo = (n = 0) => `data:image/jpeg;base64,${Buffer.alloc(320, n).toString('base64')}`;

test('withheld and deflected facts never reach the phrasing model', () => {
  const s = newSession();
  for (const type of ['withhold', 'deflect']) {
    const input = phrasingInput(s, 'pavel', { type, npc: 'pavel', fact: 'job_continued', reason: 'Not before you have seen the record.' });
    assert.deepEqual(input.facts, []);
    assert.ok(!JSON.stringify(input).includes(FACTS.job_continued.text), `${type} input carries the fact text`);
  }
  const answer = phrasingInput(s, 'pavel', { type: 'answer', npc: 'pavel', fact: 'job_continued' });
  assert.deepEqual(answer.facts, [FACTS.job_continued.text]);
});

test('rephrased lines keep the engine template for later prompts, and the browser does not get it', () => {
  const s = newSession();
  s.conversations.push({ role: 'npc', npc: 'pavel', text: 'Template line.' });
  rephraseLine(s, 'pavel', 'Template line.', 'Model wording.');
  const row = s.conversations.at(-1);
  assert.equal(row.text, 'Model wording.');
  assert.equal(row.template, 'Template line.');
  assert.ok(clientState(s).previous.every(r => !('template' in r)));
});

test('over the session model budget, phrasing falls back to the template without a call', async () => {
  const saved = { key: process.env.OPENAI_API_KEY, demo: process.env.DEMO_MODE };
  process.env.OPENAI_API_KEY = 'test-key-never-sent';
  delete process.env.DEMO_MODE;
  try {
    const stats = { calls: 1e9, input: 0, output: 0 };
    const phrasing = { name: 'Pavel', role: 'x', move: 'answer', facts: [] };
    assert.equal(await freeReply({ text: 'hi', phrasing, template: 'Template line.', history: [] }, stats), 'Template line.');
    assert.equal(stats.limited, 1);
  } finally {
    if (saved.key === undefined) delete process.env.OPENAI_API_KEY; else process.env.OPENAI_API_KEY = saved.key;
    if (saved.demo !== undefined) process.env.DEMO_MODE = saved.demo;
  }
});

test('photos are raster only: an SVG data URL is refused', () => {
  const svg = `data:image/svg+xml;base64,${Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script>${' '.repeat(300)}</svg>`).toString('base64')}`;
  assert.equal(parseImageDataUrl(svg), null);
  const s = newSession();
  assert.equal(writeNote(s, { rel: 'photos/x.svg', text: svg, kind: 'image' }).ok, false);
  assert.equal(parseImageDataUrl(photo())?.mime, 'jpeg');
});

test('per-session caps: photo count, note length, total bytes written', () => {
  const s = newSession();
  for (let i = 0; i < CONFIG.LIMITS.PHOTOS; i++) assert.equal(writeNote(s, { rel: `photos/${i}.jpg`, text: photo(i), kind: 'image' }).ok, true);
  assert.equal(writeNote(s, { rel: 'photos/extra.jpg', text: photo(), kind: 'image' }).ok, false);
  assert.equal(writeNote(s, { rel: 'photos/0.jpg', text: photo(9), kind: 'image' }).ok, true, 'overwriting an existing photo is allowed');
  writeNote(s, { rel: 'notes/long.txt', text: 'x'.repeat(CONFIG.LIMITS.NOTE_CHARS * 2) });
  assert.equal(s.files.find(f => f.rel === 'notes/long.txt').text.length, CONFIG.LIMITS.NOTE_CHARS);
  s.bytesWritten = CONFIG.LIMITS.BYTES_WRITTEN;
  assert.equal(writeNote(s, { rel: 'notes/more.txt', text: 'x' }).ok, false);
});

test('refused file writes are not logged, and a full event log refuses further actions', () => {
  const s = newSession();
  s.labAccessActive = true;
  const before = s.events.length;
  assert.equal(applyAction(s, 'tool', { tool: 'file.write', rel: 'photos/bad.jpg', text: 'not an image', kind: 'image' }).ok, false);
  assert.equal(s.events.length, before);
  s.events.length = CONFIG.LIMITS.EVENTS;
  assert.ok(applyAction(s, 'go', { room: 'collab' }).error);
});

test('import refuses saves longer than the event cap', () => {
  const events = Array.from({ length: CONFIG.LIMITS.EVENTS + 1 }, () => ({ kind: 'action', action: 'go', args: { room: 'commons' } }));
  assert.ok(importSession({ version: CONFIG.SAVE_VERSION, scenario: newSession().scenario, events }, applyAction).error);
  assert.ok(importSession({ version: CONFIG.SAVE_VERSION, scenario: newSession().scenario, events: 'nope' }, applyAction).error);
});
