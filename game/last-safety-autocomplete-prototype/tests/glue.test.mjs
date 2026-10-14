import test from 'node:test';
import assert from 'node:assert/strict';
import { newSession } from '../lib/game.mjs';
import { NPC_DEFS, templateText, glueMove } from '../lib/world/npcs.mjs';
import { pickStance } from '../lib/world/glue.mjs';
import { P, startedSession, say, walk } from './helpers.mjs';

const GENERIC = /middle of something/i;

test('Daniel and Elena work replies are person-specific, not a shared shrug', () => {
  const s = startedSession();
  walk(s, 'collab');
  const d = say(s, 'daniel', P('social', 'open'), 'Hi.');
  assert.ok(d.lines.length);
  for (const l of d.lines) assert.doesNotMatch(l.text, GENERIC);
  assert.ok(d.lines.some(l => /slide|number|sentence/i.test(l.text)), 'Daniel names his work');
  walk(s, 'people');
  const e = say(s, 'elena', P('social', 'open'), 'Hi.');
  for (const l of e.lines) assert.doesNotMatch(l.text, GENERIC);
  assert.ok(e.lines.some(l => /rota|people|rule|list/i.test(l.text)), 'Elena names her work');
});

test('first in-room talk opens with glue; a later stay does not repeat opening', () => {
  const s = newSession();
  const first = say(s, 'ian', P('ask', 'about', { topic: 'review' }), 'What about the review?');
  assert.equal(first.lines[0]?.move?.type, 'glue');
  assert.equal(first.lines[0]?.move?.slot, 'opening');
  assert.match(first.lines[0].text, /here|short|Come in|meeting/i);
  const s2 = startedSession();
  walk(s2, 'collab');
  const a = say(s2, 'daniel', P('social', 'open'), 'Hi.');
  const b = say(s2, 'daniel', P('social', 'open'), 'Still here.');
  assert.equal(a.lines[0]?.move?.slot, 'opening');
  assert.notEqual(b.lines[0]?.move?.slot, 'opening');
});

test('Ian’s closing glue fires when he leaves commons after talking', () => {
  const s = newSession();
  const r = say(s, 'ian', P('ask', 'about', { topic: 'review' }), 'What about the review?');
  const close = r.lines.filter(l => l.move?.type === 'glue' && l.move.slot === 'closing');
  assert.equal(close.length, 1);
  assert.match(close[0].text, /paper|building|defend/i);
  assert.notEqual(s.npcs.ian.room, 'commons');
});

test('Jun work lines stay first person; texture facts are not read aloud verbatim', () => {
  const s = startedSession();
  walk(s, 'model');
  const r = say(s, 'jun', P('social', 'open'), 'Hi.');
  for (const l of r.lines) {
    assert.doesNotMatch(l.text, /^Jun spent/i);
    assert.doesNotMatch(l.text, /\bJun spent the morning\b/);
    if (l.move?.type === 'work') assert.match(l.text, /^I[’']/);
  }
});

test('stance follows domain and pressure; glue never carries a fact id', () => {
  assert.equal(pickStance(NPC_DEFS.elena.glue, { domains: ['staffing'] }), 'pushy');
  assert.equal(pickStance(NPC_DEFS.elena.glue, { domains: ['evaluation'] }), 'deferential');
  assert.equal(pickStance(NPC_DEFS.daniel.glue, { domains: [], pressure: true }), 'thin');
  assert.equal(pickStance(NPC_DEFS.leila.glue, { interruptible: 'no' }), 'busy');
  const s = newSession();
  const g = glueMove(s, 'daniel', 'opening', P('social', 'open'));
  assert.equal(g.fact, undefined);
  assert.ok(g.text);
  assert.doesNotMatch(templateText(s, g), GENERIC);
});
