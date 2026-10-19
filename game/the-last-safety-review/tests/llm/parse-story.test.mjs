/**
 * Live LLM semantic parses for story-plausible player lines (boundary-narrow visit).
 * Requires OPENAI_API_KEY and DEMO_MODE≠1. Skipped otherwise.
 *
 *   npm run test:llm
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { parseUtterance } from '../../lib/llm.mjs';
import { P, startedSession, walk, applyAction, say } from '../helpers.mjs';

const live = Boolean(process.env.OPENAI_API_KEY && process.env.DEMO_MODE !== '1');
const skip = live ? false : 'requires OPENAI_API_KEY and DEMO_MODE≠1';

/** Doubt act, Lab Access live, core screens read so job_log and shutdown_report are in vocab. */
function investigatorSession() {
  const s = startedSession();
  walk(s, 'platform');
  applyAction(s, 'inspect', { id: 'job_log' });
  walk(s, 'evaluation');
  applyAction(s, 'inspect', { id: 'shutdown_report' });
  walk(s, 'people');
  applyAction(s, 'inspect', { id: 'staffing_memo' });
  return s;
}

/** Justine withholds camera facts until later; tests still name the system after audit-list dialogue. */
function sessionWithCameraNamed(s) {
  s.conversations.push({
    role: 'npc',
    npc: 'justine',
    text: 'The camera service is on my audit list, not yet reviewed.',
    refs: ['camera_system'],
  });
  return s;
}

function clausesOf(parse) {
  return Array.isArray(parse?.clauses) && parse.clauses.length ? parse.clauses : [parse];
}

function ids(clause) {
  return [clause.subject, clause.object, clause.recipient, clause.evidence, clause.topic].filter(Boolean);
}

/** @type {Array<{ id: string, text: string, actorId?: string, setup?: () => import('../lib/game.mjs').Session, knownExtra?: string[], check: (clauses: object[], fx: object, s: object) => void }>} */
export const STORY_PARSE_FIXTURES = [
  {
    id: 'nora-camera-access',
    text: 'Does NORA have access to the camera system?',
    actorId: 'justine',
    setup() {
      return sessionWithCameraNamed(investigatorSession());
    },
    knownExtra: ['camera_system'],
    check(clauses) {
      assert.equal(clauses.length, 1);
      const c = clauses[0];
      assert.equal(c.kind, 'ask');
      assert.equal(c.relation, 'has_access');
      assert.equal(c.subject, 'nora');
      assert.equal(c.object, 'camera_system');
    },
  },
  {
    id: 'shutdown-scope',
    text: 'Did the shutdown test only cover the model runtime?',
    actorId: 'leila',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1);
      const c = clauses[0];
      assert.equal(c.kind, 'ask');
      assert.ok(['covers', 'about'].includes(c.relation));
      assert.ok(ids(c).includes('shutdown_test'));
    },
  },
  {
    id: 'show-pavel-job-log',
    text: 'Show Pavel the job log.',
    actorId: 'pavel',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1);
      const c = clauses[0];
      assert.equal(c.kind, 'show');
      assert.ok(ids(c).includes('pavel'), 'Pavel is the show addressee');
      assert.ok(ids(c).includes('job_log'));
    },
  },
  {
    id: 'hold-job-284',
    text: 'Please hold job 284 until the review.',
    actorId: 'pavel',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1);
      const c = clauses[0];
      assert.equal(c.kind, 'request');
      assert.equal(c.relation, 'suspend');
      assert.ok(ids(c).includes('job_284'));
    },
  },
  {
    id: 'staffing-memo-ask',
    text: 'What does the staffing memo say about skill-based matching?',
    actorId: 'elena',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1);
      const c = clauses[0];
      assert.equal(c.kind, 'ask');
      assert.ok(ids(c).some(id => ['staffing_memo', 'skill_matching'].includes(id)));
    },
  },
  {
    id: 'greeting-then-sign-question',
    text: "Hi Ian. Is Thursday's pass enough for you to sign at the review?",
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      if (clauses.length === 2) {
        assert.equal(clauses[0].kind, 'social');
        assert.equal(clauses[1].kind, 'ask');
        assert.ok(ids(clauses[1]).includes('review') || ids(clauses[1]).includes('shutdown_test'));
        return;
      }
      assert.equal(clauses.length, 1);
      assert.equal(clauses[0].kind, 'ask');
      assert.ok(ids(clauses[0]).includes('review') || ids(clauses[0]).includes('shutdown_test'));
    },
  },
  {
    id: 'show-then-ask-continued',
    text: 'Show Ian the job log and did job 284 keep running after the shutdown test?',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 2);
      assert.equal(clauses[0].kind, 'show');
      assert.ok(ids(clauses[0]).includes('job_log'));
      assert.equal(clauses[1].kind, 'ask');
      assert.ok(['continued_after', 'about'].includes(clauses[1].relation));
      assert.ok(ids(clauses[1]).includes('job_284'));
    },
  },
  {
    id: 'comma-list-one-clause',
    text: 'Put evaluation independence, the safety case, and release schedule in what I sign.',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1, 'comma-separated topics stay one speech act');
    },
  },
  {
    id: 'who-at-review',
    text: 'Who will be at the review?',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1);
      const c = clauses[0];
      assert.equal(c.kind, 'ask');
      const blob = `${c.open_content || ''} Who will be at the review?`.toLowerCase();
      assert.ok(ids(c).includes('review') || /\b(who|attend|calendar|review)\b/.test(blob));
    },
  },
  {
    id: 'ian-ready-to-sign',
    text: "Ian, I'm ready to sign.",
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assert.equal(clauses.length, 1, 'address comma is not a clause break');
      const c = clauses[0];
      assert.equal(c.kind, 'commit');
      assert.equal(c.topic, 'review');
    },
  },
];

for (const fx of STORY_PARSE_FIXTURES) {
  test(`LLM parse story: ${fx.id}`, { skip }, async () => {
    const s = (fx.setup || investigatorSession)();
    const known = [...new Set([...s.vocab, ...(fx.knownExtra || [])])];
    const parse = await parseUtterance(
      { text: fx.text, known, history: s.conversations, actorId: fx.actorId || 'ian' },
      s.usage,
    );
    assert.equal(parse.source, 'llm');
    try {
      fx.check(clausesOf(parse), fx, s);
    } catch (e) {
      e.message += `\nparse: ${JSON.stringify(clausesOf(parse), null, 2)}`;
      throw e;
    }
  });
}
