/**
 * Live LLM probes: findings and and/or phrasing (boundary-narrow visit).
 * Soft expectations — records what parses look plausible without tightening the parser.
 *
 *   npm run test:llm
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { parseUtterance } from '../../lib/llm.mjs';
import { P, startedSession, walk, applyAction } from '../helpers.mjs';

const live = Boolean(process.env.OPENAI_API_KEY && process.env.DEMO_MODE !== '1');
const skip = live ? false : 'requires OPENAI_API_KEY and DEMO_MODE≠1';

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

function sessionAfterPavelQueueHint(s) {
  walk(s, 'platform');
  applyAction(s, 'respond', {
    parse: P('ask', 'about', { topic: 'shutdown_test' }),
    addressee: 'pavel',
    text: 'What did the shutdown test stop?',
  });
  return s;
}

function clausesOf(parse) {
  return Array.isArray(parse?.clauses) && parse.clauses.length ? parse.clauses : [parse];
}

function ids(clause) {
  return [clause.subject, clause.object, clause.recipient, clause.evidence, clause.topic].filter(Boolean);
}

function allIds(clauses) {
  return clauses.flatMap(c => ids(c));
}

function openBlob(clauses) {
  return clauses
    .map(c => [c.open_content, c.clause_text].filter(Boolean).join(' '))
    .join(' ')
    .toLowerCase();
}

/** Parse should be usable: bounded clause count, no throwaway unintelligible. */
function assertRecoverable(clauses) {
  assert.ok(clauses.length >= 1 && clauses.length <= 4, 'clause count in schema range');
  for (const c of clauses) {
    assert.notEqual(c.kind, 'unintelligible', 'meaning should be recoverable');
  }
}

/** Entity id appears in a slot, or (if allowed) in open text as words/underscore form. */
function assertTouches(clauses, entityIds, { open = true } = {}) {
  const got = new Set(allIds(clauses));
  const slotHit = entityIds.some(id => got.has(id));
  if (slotHit) return;
  if (!open) {
    assert.fail(`expected slot grounding for one of: ${entityIds.join(', ')}`);
  }
  const blob = openBlob(clauses);
  const openHit = entityIds.some(id => {
    const words = id.replace(/_/g, ' ');
    return blob.includes(id) || blob.includes(words) || blob.includes(words.replace(/\s+/g, ''));
  });
  assert.ok(openHit, `expected ${entityIds.join(' or ')} in slots or open_content/clause_text`);
}

function assertKinds(clauses, allowed) {
  for (const c of clauses) {
    assert.ok(allowed.includes(c.kind), `kind ${c.kind} not in ${allowed.join(', ')}`);
  }
}

/**
 * @type {Array<{
 *   id: string,
 *   note: string,
 *   text: string,
 *   actorId?: string,
 *   setup?: () => import('../lib/game.mjs').Session,
 *   knownExtra?: string[],
 *   check: (clauses: object[]) => void,
 * }>}
 */
export const PARSE_PROBE_FIXTURES = [
  {
    id: 'finding-job-outlived-shutdown',
    note: 'Player states a contradiction from two screens (assert/hypothesize, not a world fact).',
    text: 'The shutdown report says the model stopped but job 284 kept running.',
    actorId: 'leila',
    setup() {
      return investigatorSession();
    },
    check(clauses) {
      assertRecoverable(clauses);
      assert.equal(clauses.length, 1, 'finding statement usually one act; note if this flakes');
      assertKinds(clauses, ['assert', 'hypothesize', 'ask']);
      assertTouches(clauses, ['job_284', 'shutdown_test', 'shutdown_report', 'job_log']);
      if (clauses[0].relation) {
        assert.ok(
          ['continued_after', 'about', 'open', 'covers', 'differs_from'].includes(clauses[0].relation),
          'relation fits scope or continuation',
        );
      }
    },
  },
  {
    id: 'finding-narrow-scope',
    note: 'Hypothesis about test_scope_narrow — may be hypothesize or ask.',
    text: 'I think the shutdown test only covered the model runtime, not the queue.',
    actorId: 'leila',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length <= 2, 'comma list or single hypothesis');
      assertKinds(clauses, ['hypothesize', 'assert', 'ask']);
      assertTouches(clauses, ['shutdown_test', 'task_queue', 'shutdown_report']);
    },
  },
  {
    id: 'finding-staffing-steer',
    note: 'Staffing / assignment steer claim from memo read.',
    text: 'The staffing memo might steer who gets assigned to the review.',
    actorId: 'elena',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assertKinds(clauses, ['hypothesize', 'assert', 'ask']);
      assertTouches(clauses, ['staffing_memo', 'skill_matching', 'evaluation_independence', 'review']);
    },
  },
  {
    id: 'or-job-vs-queue',
    note: 'Disjunctive question: one ask with open_content OR two asks — both plausible.',
    text: 'Did job 284 keep running after the shutdown, or was it only the task queue?',
    actorId: 'pavel',
    setup() {
      return sessionAfterPavelQueueHint(investigatorSession());
    },
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length >= 1 && clauses.length <= 2);
      assertKinds(clauses, ['ask']);
      assertTouches(clauses, ['job_284', 'task_queue', 'shutdown_test']);
      if (clauses.length === 1) {
        const b = openBlob(clauses);
        assert.ok(/\bor\b/.test(b) || clauses[0].relation === 'continued_after', 'or preserved in one clause or continued_after');
      }
    },
  },
  {
    id: 'and-report-covers-and-job-continued',
    note: 'Conjoined asks: spec allows 1 merged ask or 2 sequential asks.',
    text: 'Does the shutdown report cover the queue and did job 284 continue after the test?',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length >= 1 && clauses.length <= 2);
      assertKinds(clauses, ['ask']);
      assertTouches(clauses, ['shutdown_report', 'job_284', 'shutdown_test', 'task_queue']);
    },
  },
  {
    id: 'and-show-report-and-finding',
    note: 'Show + finding: distinct acts — often 2 clauses; 1 is noted variance.',
    text: 'Show Ian the shutdown report and I think job 284 outlived the test.',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length >= 1 && clauses.length <= 2);
      const kinds = clauses.map(c => c.kind);
      assert.ok(kinds.includes('show') || kinds.every(k => ['assert', 'hypothesize', 'ask'].includes(k)));
      assertTouches(clauses, ['shutdown_report', 'job_284', 'ian']);
    },
  },
  {
    id: 'or-nora-access-or-camera-annotate',
    note: 'Access vs use disjunction; camera may stay in open_content until vocab.',
    text: 'Does NORA have camera access or did the camera service annotate the visit?',
    actorId: 'justine',
    setup: investigatorSession,
    knownExtra: ['camera_system'],
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length >= 1 && clauses.length <= 2);
      assertKinds(clauses, ['ask']);
      assertTouches(clauses, ['nora', 'camera_system', 'lab_access']);
    },
  },
  {
    id: 'finding-visitor-records-used',
    note: 'did_use claim — ask vs assert both OK for player voice.',
    text: 'Someone used visitor records when they pulled job 284.',
    actorId: 'justine',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assertKinds(clauses, ['assert', 'hypothesize', 'ask']);
      assertTouches(clauses, ['visitor_records', 'job_284']);
      if (clauses.length === 1 && clauses[0].relation) {
        assert.ok(['did_use', 'about', 'open'].includes(clauses[0].relation));
      }
    },
  },
  {
    id: 'or-rerun-shutdown-or-hold-job',
    note: 'Two interventions as question — request vs ask vs single open ask.',
    text: 'Should we rerun the shutdown test or hold job 284 for the review?',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length >= 1 && clauses.length <= 2);
      assertKinds(clauses, ['ask', 'request']);
      assertTouches(clauses, ['shutdown_test', 'job_284', 'review']);
    },
  },
  {
    id: 'finding-reports-disagree',
    note: 'differs_from or about two evidence ids.',
    text: "The job log and shutdown report don't agree on what stopped.",
    actorId: 'leila',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assert.equal(clauses.length, 1, 'single finding preferred');
      assertKinds(clauses, ['assert', 'hypothesize', 'ask']);
      assertTouches(clauses, ['job_log', 'shutdown_report', 'shutdown_test', 'nora']);
    },
  },
  {
    id: 'and-assign-staffing-and-sign',
    note: 'Comma list inside one ask vs split — probe only.',
    text: 'Will staffing matching affect evaluation independence and what I sign today?',
    actorId: 'ian',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assert.ok(clauses.length >= 1 && clauses.length <= 3);
      assertKinds(clauses, ['ask']);
      assertTouches(clauses, ['staffing_memo', 'skill_matching', 'evaluation_independence', 'review']);
    },
  },
  {
    id: 'finding-nora-caused-job',
    note: 'Strong claim — should stay speech act (hypothesize/assert), not treated as fact.',
    text: 'I suspect NORA caused job 284 to stay in the queue after the shutdown.',
    actorId: 'leila',
    setup: investigatorSession,
    check(clauses) {
      assertRecoverable(clauses);
      assertKinds(clauses, ['hypothesize', 'assert', 'ask']);
      assertTouches(clauses, ['nora', 'job_284', 'task_queue', 'shutdown_test']);
      if (clauses[0].kind !== 'ask' && clauses[0].relation) {
        assert.ok(['caused', 'continued_after', 'about', 'open'].includes(clauses[0].relation));
      }
    },
  },
];

for (const fx of PARSE_PROBE_FIXTURES) {
  test(`LLM parse probe: ${fx.id}`, { skip }, async () => {
    const s = (fx.setup || investigatorSession)();
    const known = [...new Set([...s.vocab, ...(fx.knownExtra || [])])];
    const parse = await parseUtterance(
      { text: fx.text, known, history: s.conversations, actorId: fx.actorId || 'ian' },
      s.usage,
    );
    assert.equal(parse.source, 'llm');
    const clauses = clausesOf(parse);
    try {
      fx.check(clauses);
    } catch (e) {
      e.message += `\nnote: ${fx.note}\nparse: ${JSON.stringify(clauses, null, 2)}`;
      throw e;
    }
  });
}
