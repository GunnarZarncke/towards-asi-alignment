/**
 * One-off completion latency breakdown (client grammar + server parse).
 * Run: node scripts/bench-completions.mjs
 */
import { performance } from 'node:perf_hooks';
import { newSession, clientState } from '../lib/game.mjs';
import { makeParse } from '../lib/grammar.mjs';
import { parseUtterance } from '../lib/llm.mjs';
import { ENTITIES, ROLE_DOMAINS } from '../lib/world/entities.mjs';
import { getCandidates, localPrefixParse, relevance } from '../public/grammar.js';

function lateGameProjection() {
  const ids = Object.keys(ENTITIES);
  const entities = Object.fromEntries(
    ids.map(id => [
      id,
      {
        label: ENTITIES[id].label,
        category: ENTITIES[id].category,
        aliases: ENTITIES[id].aliases,
        domains: ENTITIES[id].domains,
        eventAt: null,
      },
    ]),
  );
  const facts = ids.slice(0, 40).map((id, i) => ({
    id: `fact_${i}`,
    text: `Fact about ${id}`,
    refs: [id, ids[(i + 3) % ids.length]],
    eventAt: i,
    discoveredAt: i,
  }));
  const introduced = Object.keys(ROLE_DOMAINS);
  return {
    room: 'commons',
    actors: Object.fromEntries(
      introduced.map(id => [id, { name: id, room: 'commons', presence: 'present' }]),
    ),
    entities,
    introduced,
    examined: ids.slice(0, 5),
    previous: [],
    asked: [],
    pendingQuestion: null,
    learnedFacts: facts,
    discoveredAt: Object.fromEntries(ids.map((id, i) => [id, i])),
    roleDomains: introduced.map(id => ({ id, domains: [...ROLE_DOMAINS[id]] })),
  };
}

function ms(fn, n = 1) {
  const t0 = performance.now();
  for (let i = 0; i < n; i++) fn();
  return (performance.now() - t0) / n;
}

function hereIds(state) {
  return Object.entries(state.actors || {})
    .filter(([, a]) => a.presence !== 'absent' && a.room === state.room)
    .map(([id]) => id);
}

const s = newSession();
const state = clientState(s);
const addressees = hereIds(state);
const entityCount = Object.keys(state.entities).length;
const factCount = (state.learnedFacts || []).length;
const graphItems = entityCount + factCount;

console.log('--- state size ---');
console.log(`entities (vocab): ${entityCount}, learned facts: ${factCount}, graph items: ${graphItems}`);
console.log(`serverMode: ${state.serverMode}, debounce (room UI): 560ms, phone: 520ms`);

const samples = [
  { label: 'empty opening', parse: makeParse(), text: '' },
  { label: 'typed "What about cam"', parse: makeParse({ kind: 'ask', relation: 'about', open_slot: 'topic', unfinished: 'cam' }), text: 'What about cam' },
  { label: 'subject slot (after Does)', parse: makeParse({ kind: 'ask', relation: 'about', open_slot: 'subject' }), text: 'Does ' },
  { label: 'relation slot', parse: makeParse({ kind: 'ask', relation: 'about', open_slot: 'relation', subject: 'nora' }), text: 'Does NORA ' },
  { label: 'topic list (think)', parse: makeParse({ kind: 'think', relation: 'about', open_slot: 'topic' }), text: 'Think about ' },
];

console.log('\n--- localPrefixParse (sync) ---');
for (const t of ['', 'Hi', 'Can', 'Does', 'What about the shut']) {
  console.log(`  "${t}": ${ms(() => localPrefixParse(t), 5000).toFixed(3)} ms avg (5k runs)`);
}

console.log('\n--- getCandidates (sync, 200 runs each) ---');
for (const { label, parse, text } of samples) {
  const avg = ms(
    () => getCandidates({ state, parse, text, addressees, channel: 'person' }),
    200,
  );
  const n = getCandidates({ state, parse, text, addressees, channel: 'person' }).length;
  console.log(`  ${label}: ${avg.toFixed(2)} ms, ${n} chips`);
}

console.log('\n--- relevance() alone (200 runs, topic parse) ---');
const topicParse = makeParse({ kind: 'ask', relation: 'about', open_slot: 'topic' });
console.log(`  relevance: ${ms(() => relevance(state, topicParse, addressees), 200).toFixed(2)} ms`);

console.log('\n--- simulated keystroke path (no local prefix) ---');
console.log('  intentional debounce before /api/parse: 560 ms');
const typing = 'Does NORA have access to the cam';
console.log(`  localPrefixParse("${typing.slice(0, 20)}…"): ${localPrefixParse(typing) ? 'hit (chips immediate)' : 'miss (parse=null until debounce+parse)'}`);

console.log('\n--- parseUtterance server (demo/heuristic, 50 runs) ---');
const known = [...s.vocab];
for (const text of ['Does NORA have access to the camera system', 'What about the shutdown test', 'Show Pavel']) {
  const avg = ms(() => parseUtterance({ text, known, history: s.conversations, actorId: addressees[0] }, s.usage), 50);
  console.log(`  "${text.slice(0, 40)}": ${avg.toFixed(2)} ms`);
}

const live = process.env.OPENAI_API_KEY && process.env.DEMO_MODE !== '1';
if (live) {
  console.log('\n--- parseUtterance LIVE API (3 calls) ---');
  for (const text of ['Does NORA have access', 'What about shut']) {
    const t0 = performance.now();
    try {
      await parseUtterance({ text, known, history: s.conversations, actorId: addressees[0] }, s.usage);
      console.log(`  "${text}": ${(performance.now() - t0).toFixed(0)} ms`);
    } catch (e) {
      console.log(`  "${text}": failed (${e.message})`);
    }
  }
} else {
  console.log('\n--- LIVE API ---');
  console.log('  skipped (no OPENAI_API_KEY or DEMO_MODE=1); live parse is typically 300–2000+ ms RTT+model');
}

console.log('\n--- renderInspector-equivalent (sync DOM skipped; JSON.stringify parse) ---');
const p = makeParse({ kind: 'ask', open_slot: 'subject' });
console.log(`  JSON.stringify parse: ${ms(() => JSON.stringify(p, null, 2), 10000).toFixed(4)} ms`);

const late = lateGameProjection();
const lateIds = Object.keys(late.entities).length;
const lateFacts = late.learnedFacts.length;
console.log(`\n--- late-game projection (${lateIds} entities, ${lateFacts} facts) ---`);
console.log(`  getCandidates (topic): ${ms(() => getCandidates({ state: late, parse: topicParse, text: 'What about ', addressees: ['pavel'] }), 50).toFixed(2)} ms`);
console.log(`  relevance: ${ms(() => relevance(late, topicParse, ['pavel']), 50).toFixed(2)} ms`);
