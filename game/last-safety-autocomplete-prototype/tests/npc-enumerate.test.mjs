/**
 * Layer 3 (spec/testing.md, spec/npcs.md invariants): for each NPC and act, every parse in the
 * finite grid kind × relation × id yields a non-empty legal move set, and no move carries a fact
 * the player could not have encountered or the NPC's policy forbids.
 * Stop: an empty set is an engine bug; a leak by id is a policy or filter bug.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { RELATIONS } from '../lib/grammar.mjs';
import { ENTITIES } from '../lib/world/entities.mjs';
import { FACTS } from '../lib/world/facts.mjs';
import { NPC_DEFS, NPC_IDS, npcTurn, responseCandidates, factVisible, goalIds } from '../lib/world/npcs.mjs';
import { P, startedSession, walk, applyAction, commit } from './helpers.mjs';

const KINDS = ['ask', 'ask_why', 'assert', 'hypothesize', 'request'];
const PAYLOAD = new Set(['answer', 'believe', 'work']);

function states() {
  const fresh = startedSession();
  const read = startedSession();
  walk(read, 'platform'); applyAction(read, 'inspect', { id: 'job_log' });
  walk(read, 'evaluation'); applyAction(read, 'inspect', { id: 'shutdown_report' });
  walk(read, 'people'); applyAction(read, 'inspect', { id: 'staffing_memo' });
  const review = startedSession();
  walk(review, 'platform'); applyAction(review, 'inspect', { id: 'job_log' });
  walk(review, 'evaluation'); applyAction(review, 'inspect', { id: 'shutdown_report' });
  commit(review);
  return { doubt_start: fresh, doubt_read: read, decision: review };
}

function* grid(s) {
  for (const kind of KINDS) for (const relation of Object.keys(RELATIONS)) for (const id of s.vocab) {
    if (!ENTITIES[id]) continue;
    yield relation === 'about' ? P(kind, relation, { topic: id }) : P(kind, relation, { object: id });
  }
}

const STATES = states();

for (const [label, base] of Object.entries(STATES)) {
  test(`no dead end and no leak: ${label}`, () => {
    let parses = 0;
    for (const npc of NPC_IDS) {
      for (const parse of grid(base)) {
        parses++;
        const s = structuredClone(base);
        const moves = responseCandidates(s, npc, parse);
        assert.ok(moves.length > 0, `${npc} has no move for ${parse.kind}/${parse.relation}/${parse.topic || parse.object}`);
        const { response, initiative } = npcTurn(s, npc, parse);
        for (const m of [...moves, response, initiative].filter(Boolean)) {
          if (PAYLOAD.has(m.type) && m.fact) {
            assert.ok(FACTS[m.fact], `${npc} carries unknown id ${m.fact}`);
            assert.ok(factVisible(s, m.fact), `${npc} leaks ${m.fact} (refs not encountered) on ${parse.relation}/${parse.topic || parse.object}`);
          }
          if (m.type === 'share') assert.ok(NPC_DEFS[npc].documents?.[m.doc], `${npc} shares ${m.doc}, which is not theirs`);
          if (m.type === 'act') assert.ok(NPC_DEFS[npc].interventions?.[m.intervention], `${npc} acts on ${m.intervention} without owning it`);
        }
        if (response && initiative) assert.notDeepEqual(initiative, response, 'initiative never replaces the response');
      }
    }
    assert.ok(parses > 0);
  });
}

test('goals do not read the oracle: no goal names an explanation id', () => {
  const s = STATES.doubt_start;
  const oracle = new Set(Object.keys(s.pack.explanations));
  for (const npc of NPC_IDS) for (const id of goalIds(npc)) assert.ok(!oracle.has(id), `${npc} goal reads ${id}`);
});
