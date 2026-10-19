/**
 * O-19 ranking cases (spec/ranking.md "Tests") plus the channel cases in spec/grammar.md.
 * Hand-built projections; no session, network, or model.
 * Stop: a failure here is a ranker bug or a spec conflict for meta.md, never a content change.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { makeParse, semanticSignature } from '../lib/grammar.mjs';
import { ENTITIES, ROLE_DOMAINS } from '../lib/world/entities.mjs';
import { getCandidates, relevance, distancesFrom, temporalEdge, localPrefixParse, RANKING } from '../public/grammar.js';

function proj({ ids, introduced = [], facts = [], previous = [], examined = [], discoveredAt = {}, eventAt = {}, actors = {}, room = 'commons', asked = [], pendingQuestion = null }) {
  const entities = Object.fromEntries(ids.map(id => [id, { label: ENTITIES[id].label, category: ENTITIES[id].category, aliases: ENTITIES[id].aliases, domains: ENTITIES[id].domains, eventAt: eventAt[id] ?? null }]));
  return {
    room, actors, entities, introduced, examined, previous, asked, pendingQuestion,
    learnedFacts: facts,
    discoveredAt,
    roleDomains: introduced.filter(id => ROLE_DOMAINS[id]).map(id => ({ id, domains: [...ROLE_DOMAINS[id]] })),
  };
}
const topicParse = makeParse({ kind: 'ask', relation: 'about', open_slot: 'topic' });
const order = list => list.map(x => x.entityId || x.phrase);
const idx = (list, id) => list.findIndex(x => x.entityId === id);

test('1. introducing NORA adds her role row and changes order', () => {
  const ids = ['personnel_policy', 'task_queue'];
  const before = getCandidates({ state: proj({ ids }), parse: topicParse, addressees: ['nora'] });
  assert.deepEqual(order(before), ids);
  const after = getCandidates({ state: proj({ ids: ['nora', ...ids], introduced: ['nora'] }), parse: topicParse, addressees: ['nora'] });
  assert.ok(idx(after, 'task_queue') < idx(after, 'personnel_policy'));
});

test('2. addressee role domains: Justine lifts the camera system; a union does not double access', () => {
  const ids = ['camera_system', 'shutdown_test', 'skill_matching', 'release_schedule', 'personnel_policy'];
  const state = proj({ ids, introduced: ['justine', 'leila'] });
  const forJ = getCandidates({ state, parse: topicParse, addressees: ['justine'] });
  const forL = getCandidates({ state, parse: topicParse, addressees: ['leila'] });
  assert.ok(idx(forJ, 'camera_system') < idx(forL, 'camera_system'));
  const rJ = relevance(state, topicParse, ['justine']).get('camera_system');
  const rJL = relevance(state, topicParse, ['justine', 'leila']).get('camera_system');
  assert.equal(rJ, RANKING.WEIGHT.role);
  assert.equal(rJL, rJ);
});

test('3. temporal neighbors: shared ref seven minutes apart costs 7/15; shared discovery fuel links an old fact', () => {
  const ids = ['job_284', 'visitor_records'];
  const facts = [
    { id: 'f_stop', refs: ['job_284'], eventAt: 962, discoveredAt: 9 },
    { id: 'f_now', refs: ['job_284', 'visitor_records'], eventAt: 969, discoveredAt: 5 },
    { id: 'f_old', refs: ['visitor_records'], eventAt: 600, discoveredAt: 5 },
  ];
  const state = proj({ ids, facts });
  assert.ok(Math.abs(temporalEdge(state, 'f_stop', 'f_now') - 7 / 15) < 1e-9);
  assert.equal(temporalEdge(state, 'f_now', 'f_old'), 0, 'discovery clock: same fuel index');
});

test('4. close times without a shared ref or domain are not temporal neighbors', () => {
  const ids = ['personnel_policy', 'camera_system'];
  const facts = [
    { id: 'f_staff', refs: ['personnel_policy'], eventAt: 962, discoveredAt: 4 },
    { id: 'f_cam', refs: ['camera_system'], eventAt: 963, discoveredAt: 4 },
  ];
  const state = proj({ ids, facts });
  assert.equal(temporalEdge(state, 'f_staff', 'f_cam'), null);
  assert.equal(distancesFrom(state, 'f_staff').get('f_cam'), RANKING.COST.lab);
});

test('5. a prefix that matches one surface drops the rest, even the role favourite', () => {
  const ids = ['task_queue', 'job_284', 'camera_system'];
  const state = proj({ ids, introduced: ['pavel'] });
  const list = getCandidates({ state, parse: { ...topicParse, unfinished: 'cam' }, text: 'What about cam', addressees: ['pavel'] });
  assert.deepEqual(order(list), ['camera_system']);
});

test('6. two surfaces of one signature are one row; an asked signature is still offered', () => {
  const state = proj({ ids: ['nora', 'camera_system'] });
  const p = makeParse({ kind: 'ask', relation: 'about', subject: 'nora', open_slot: 'relation' });
  const rows = getCandidates({ state, parse: p, addressees: [] });
  assert.equal(rows.filter(x => x.parse.relation === 'has_access').length, 1);
  const asked = semanticSignature({ ...p, relation: 'has_access', open_slot: 'object' });
  const again = getCandidates({ state: { ...state, asked: [asked] }, parse: p, addressees: [] });
  assert.ok(again.some(x => x.parse.relation === 'has_access'));
});

test('7. diversity bonus needs a new branch and a new action type (Selection step 4)', () => {
  const ids = ['personnel_policy', 'camera_system', 'task_queue'];
  const list = getCandidates({ state: proj({ ids }), parse: topicParse, text: 'What about ', addressees: [] });
  assert.deepEqual(order(list), ids, 'same action type: only the first pick gets the bonus, so expansion order holds');
  const state = proj({ ids: ['nora'], introduced: [] });
  const openings = getCandidates({ state, parse: makeParse(), text: ' ', addressees: [] });
  const hold = openings.findIndex(x => x.phrase === 'Hold');
  const revoke = openings.findIndex(x => x.phrase === 'Revoke');
  const show = openings.findIndex(x => x.phrase === 'Show');
  assert.ok(show < revoke && hold < revoke, 'a second request opening shares the branch and waits behind a new branch');
});

test('8. same arguments, same order; page two is a slice; every id is in the projection', () => {
  const ids = ['task_queue', 'job_284', 'camera_system', 'personnel_policy', 'skill_matching', 'release_schedule', 'shutdown_test'];
  const state = proj({ ids, introduced: ['pavel', 'elena'], previous: [{ role: 'npc', npc: 'pavel', refs: ['job_284'] }], discoveredAt: { job_284: 3, task_queue: 0 } });
  const a = getCandidates({ state, parse: topicParse, addressees: ['pavel'] });
  const b = getCandidates({ state, parse: topicParse, addressees: ['pavel'] });
  assert.deepEqual(order(a), order(b));
  assert.deepEqual(order(a.slice(RANKING.PAGE_SIZE, 2 * RANKING.PAGE_SIZE)), order(b).slice(RANKING.PAGE_SIZE, 2 * RANKING.PAGE_SIZE));
  for (const x of a) if (x.entityId) assert.ok(state.entities[x.entityId]);
});

test('9. oracle state the client never received does not change the list', () => {
  const ids = ['task_queue', 'camera_system', 'personnel_policy'];
  const state = proj({ ids, introduced: ['justine'] });
  const leaky = { ...state, oracleKnows: ['visitor_lookup'], npcGoals: { justine: ['protect'] }, policies: { camera_system: 'conceal' } };
  assert.deepEqual(order(getCandidates({ state, parse: topicParse, addressees: ['justine'] })), order(getCandidates({ state: leaky, parse: topicParse, addressees: ['justine'] })));
});

test('10. a selected row carries its parse patch; typed openings parse locally', () => {
  const state = proj({ ids: ['nora', 'camera_system'] });
  const row = getCandidates({ state, parse: makeParse(), text: '', addressees: [] }).find(x => x.phrase === 'Can');
  assert.equal(row.parse.kind, 'ask');
  assert.equal(row.parse.open_slot, 'subject');
  assert.equal(row.parse.source, 'completion');
  assert.equal(localPrefixParse('Revoke').relation, 'revoke');
});

test('NORA channel drops the omit list; the omitted move stays typable', () => {
  const state = proj({ ids: ['nora', 'job_284'] });
  const omit = [{ phrase: 'Revoke', parse: { kind: 'request', relation: 'revoke' } }];
  const nora = getCandidates({ state, parse: makeParse(), text: '', addressees: ['nora'], channel: 'nora', omit });
  assert.ok(!nora.some(x => x.phrase === 'Revoke'));
  assert.ok(nora.some(x => x.phrase === 'Hold'));
  assert.equal(localPrefixParse('Revoke').kind, 'request');
});

test('note channel ranks with no addressee and ignores the NORA omit list', () => {
  const state = proj({ ids: ['nora', 'job_284'] });
  const omit = [{ phrase: 'The', parse: { kind: 'assert', relation: 'about' } }];
  const note = getCandidates({ state, parse: makeParse(), text: '', addressees: [], channel: 'note', omit });
  assert.ok(note.some(x => x.phrase === 'The'));
  assert.ok(note.every(x => ['assert', 'hypothesize'].includes(x.parse.kind)));
});

test('Think is absent with a hologram in the room; its topics may include a document id', () => {
  const ids = ['amara', 'shutdown_report'];
  const withHolo = proj({ ids, room: 'evaluation', actors: { amara: { room: 'evaluation', presence: 'hologram' } } });
  assert.ok(!getCandidates({ state: withHolo, parse: makeParse(), text: '' }).some(x => x.parse.kind === 'think'));
  const empty = proj({ ids, room: 'quiet', actors: { amara: { room: null, presence: 'absent' } } });
  assert.ok(getCandidates({ state: empty, parse: makeParse(), text: '', channel: 'think' }).some(x => x.parse.kind === 'think'));
  const topics = getCandidates({ state: empty, parse: makeParse({ kind: 'think', relation: 'about', open_slot: 'topic' }), channel: 'think', addressees: [] });
  assert.ok(topics.some(x => x.entityId === 'shutdown_report'));
});

test('a pending question adds reply openings for that NPC only', () => {
  const state = proj({ ids: ['pavel', 'job_284'], actors: { pavel: { name: 'Pavel Novak', room: 'platform', presence: 'body' } }, room: 'platform',
    pendingQuestion: { npc: 'pavel', goal: 'pavel.freeze_owned', parse: makeParse({ kind: 'ask', relation: 'authorized', object: 'job_284', open_slot: 'none' }) } });
  const rows = getCandidates({ state, parse: makeParse(), text: '', addressees: ['pavel'] });
  assert.equal(rows[0].phrase, 'Tell Pavel job 284');
  assert.equal(rows[0].parse.subject, 'job_284');
  assert.ok(!getCandidates({ state, parse: makeParse(), text: '', addressees: ['nora'], channel: 'nora' }).some(x => /^Tell [A-Z]/.test(x.phrase)));
});

test('a selected opening is not reread as a typed prefix; the subject is not offered as its object', () => {
  const ids = ['pavel', 'shutdown_test', 'safety_case'];
  const state = proj({ ids, introduced: ['pavel'] });
  const afterOpening = makeParse({ kind: 'ask', relation: 'about', open_slot: 'topic', source: 'completion' });
  assert.ok(getCandidates({ state, parse: afterOpening, text: 'What about', addressees: [] }).some(x => x.entityId === 'pavel'));
  const obj = makeParse({ kind: 'assert', relation: 'covers', subject: 'shutdown_test', open_slot: 'object', source: 'completion' });
  const rows = getCandidates({ state, parse: obj, text: 'I think the shutdown test was not covered by', addressees: [] });
  assert.ok(rows.some(x => x.entityId === 'safety_case'));
  assert.ok(!rows.some(x => x.entityId === 'shutdown_test'));
  const afterThe = makeParse({ kind: 'assert', relation: 'about', open_slot: 'subject', source: 'completion' });
  const subjects = getCandidates({ state, parse: afterThe, text: 'The', addressees: [] });
  assert.ok(subjects.some(x => x.entityId === 'shutdown_test') && !subjects.some(x => x.entityId === 'pavel'));
});
