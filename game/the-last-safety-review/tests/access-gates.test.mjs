import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveAccessRequestGated } from '../lib/world/access-gates.mjs';
import { newSession } from '../lib/game.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import { startedSession, dm, idle, say, P } from './helpers.mjs';
import { CONFIG } from '../lib/world/config.mjs';
import { placeNpcs } from '../lib/world/npcs.mjs';

test('evaluation list is denied without intro or reason', () => {
  const s = newSession();
  say(s, 'ian', P('ask', 'about', { topic: 'review' }));
  const r = resolveAccessRequestGated(s, 'evaluation/', 'list');
  assert.equal(r.outcome, 'deny');
  assert.equal(r.chat.from, 'justine');
});

test('evaluation list amends after Ian introduction event', () => {
  const s = startedSession();
  s.world.events.push('visitor_introduced_justine');
  const r = resolveAccessRequestGated(s, 'evaluation/', 'list');
  assert.equal(r.outcome, 'amend');
  assert.ok(r.grants.some(g => g.path.endsWith('eval-shutdown-report.md')));
});

test('Ian introduction fires in commons when the player names Justine', () => {
  const s = newSession();
  applyAction(s, 'go', { room: 'collab' });
  applyAction(s, 'go', { room: 'commons' });
  applyAction(s, 'respond', {
    parse: P('ask', 'about', { topic: 'justine' }),
    addressee: 'ian',
    text: 'Could Justine know I am here for the review?',
  });
  assert.ok(s.world.events.includes('visitor_introduced_justine'));
});

test('lunch band sends Pavel to commons', () => {
  const s = startedSession();
  s.minute = CONFIG.LUNCH[0] + 5;
  s.room = 'quiet';
  for (let i = 0; i < 24; i++) {
    s.fuelSpent += 1;
    placeNpcs(s);
  }
  assert.equal(s.npcs.pavel.room, 'commons');
});

test('accepted meeting moves Leila toward the player room', () => {
  const s = startedSession();
  dm(s, 'leila', P('request', 'meet', { object: 'leila' }), 'Can we meet in the commons?');
  idle(s, CONFIG.REPLY_DELAY.person + 1);
  assert.ok(s.world.events.some(e => e === 'meeting_accepted:leila'));
  s.room = 'quiet';
  for (let i = 0; i < 40; i++) {
    s.fuelSpent += 1;
    placeNpcs(s);
  }
  assert.equal(s.npcs.leila.room, 'commons');
  s.room = 'commons';
  say(s, 'leila', P('ask', 'about', { topic: 'shutdown_report' }), 'Thanks for meeting.');
  assert.ok(s.world.events.includes('meeting_held:leila'));
});
