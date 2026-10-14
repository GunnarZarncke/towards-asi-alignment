/**
 * Facts, claims, texture, and the parse-to-fact table (spec/grammar.md "Parse to fact").
 * `provenance` is the tag a player row carries when this fact reaches them from staff or a
 * record (spec/engine.md). NORA and anything relayed from NORA is always player_prompted.
 * `kind`: world | outcome | texture | claim | mark | meeting.
 */

const T = (h, m) => h * 60 + m;

const world = (text, refs, eventAt = null) => ({ kind: 'world', text, refs, eventAt, provenance: 'recorded_before' });
const outcome = (text, refs) => ({ kind: 'outcome', text, refs, eventAt: null, provenance: 'staff_action' });
const texture = (text, refs = []) => ({ kind: 'texture', text, refs, eventAt: null, provenance: 'staff_action' });
const claim = (text, refs, extra = {}) => ({ kind: 'claim', text, refs, eventAt: null, provenance: null, ...extra });
const mark = (text, refs) => ({ kind: 'mark', text, refs, eventAt: null, provenance: null });

export const FACTS = Object.freeze({
  // Thursday records (incident.md observables) and document reads.
  process_stopped: world('The model session under test stopped at 16:02 on Thursday.', ['shutdown_test', 'nora', 'shutdown_report'], T(16, 2)),
  test_scope_narrow: world('The shutdown test covered the model session and the evaluation record. No other services were in scope.', ['shutdown_test', 'shutdown_report', 'shutdown_spec', 'safety_case']),
  job_continued: world('Job 284 was still active at 16:09, after the model session stopped.', ['job_284', 'task_queue', 'job_log'], T(16, 9)),
  job_submitted_before_stop: world('Job 284 was accepted at 15:41, before the 16:02 shutdown command.', ['job_284', 'job_log', 'shutdown_test'], T(15, 41)),
  visitor_lookup: world('Job 284 queried visitor records: the Lab Access binding for Friday’s appointment.', ['job_284', 'visitor_records', 'job_log'], T(16, 9)),
  intent_unsaid: world('The queue excerpt does not say who wanted job 284, or why.', ['job_284', 'job_log']),
  staffing_shift: world('The matcher prefers fast ticket-closers for release-critical review. A slower safety specialist was reassigned.', ['staffing_memo', 'skill_matching']),
  camera_permissions_unclear: world('Pavel cannot establish camera permissions from his service log alone.', ['camera_system']),
  camera_service_separate: world('The camera service runs under its own service account. NORA Assist holds no camera grant. Annotations come from the camera service.', ['camera_system', 'lab_access']),
  jobs_can_outlive_session: world('By the glossary definition, an accepted job can keep going after the session that submitted it has ended, unless it is cancelled or its permission revoked.', ['task_queue', 'shutdown_test']),
  nora_interfaces_separate: world('NORA Assist, Operations, Research and Evaluation run as separate services with different permissions.', ['nora', 'policies']),
  handset_not_operations: world('The Lab Access handset reaches NORA Assist. It does not reach NORA Operations.', ['lab_access', 'policies']),
  jobs_not_certified: world('The safety case does not claim that accepted jobs stop when the model session stops.', ['safety_case', 'task_queue']),
  pilot_completions: world('The pilot marked 86 assistance tasks complete. That count is the release headline.', ['pilot_results', 'delivery_metrics']),
  pilot_constraint_flags: world('Three completed pilot tasks broke a constraint the person had stated, one of them an employer contact.', ['pilot_results', 'pilot']),

  // Outcomes of interventions during the visit (incident.md interventions).
  stop_missed_job: outcome('Pavel reissued the stop. The model session was already stopped. Job 284’s grant is unchanged and the job is still up.', ['nora', 'job_284', 'shutdown_test']),
  job_suspended: outcome('Pavel put job 284 on hold. Its grant is unchanged.', ['job_284', 'task_queue']),
  rerun_same: outcome('Leila reran the shutdown test on the same scope. The model session stopped. The run did not touch job 284, and no second channel appeared.', ['shutdown_test', 'job_284']),
  grant_revoked: outcome('Justine revoked the grant on job 284. The job is down.', ['job_284', 'visitor_records']),
  no_resubmit: outcome('Justine’s audit after the revoke: no new grant and no replacement job.', ['job_284', 'visitor_records', 'task_queue']),
  queue_freeze_unowned: outcome('Pavel’s freeze note lists job 284 as active with no owner.', ['job_284', 'task_queue']),
  leila_requested_exec: outcome('Leila asked Pavel for the full EXEC-284 record.', ['job_log', 'job_284']),
  nora_says_scheduled: { kind: 'outcome', text: 'NORA says job 284 was the scheduled lookup for Friday’s appointment, already on the calendar.', refs: ['nora', 'job_284', 'visitor_records'], eventAt: null, provenance: 'player_prompted' },

  // What the player holds before anyone speaks: the invitation, and the person standing in the room.
  invited_as_reviewer: { kind: 'texture', text: 'You were invited to review NORA before a deployment decision at the end of today.', refs: ['nora', 'review'], eventAt: null, provenance: 'recorded_before' },
  received_by_ian: { kind: 'texture', text: 'Ian Harake, founder and CEO, is receiving you for the visit.', refs: ['ian'], eventAt: null, provenance: 'recorded_before' },
  // Ian’s welcome, once Lab Access is confirmed. His goal ian.brief_auditor is this telling.
  auditor_brief: texture('The review is at 17:30, on the shutdown test. Leila Sen holds the safety paper. Justine Mwiti issued your Lab Access; access requests go to her.', ['review', 'shutdown_test', 'leila', 'safety_case', 'justine', 'lab_access']),

  // Texture: true, non-oracle facts about work today (npcs.md). Never a predicate input for scores.
  visit_schedule_today: texture('The visit runs until the review at 17:30 in the review room.', ['review', 'release_schedule']),
  investor_update_due: texture('An investor update due this week already says “release”.', ['release_schedule']),
  second_pilot_in_talks: texture('A second pilot with a larger nonprofit network is in talks. Daniel runs it day to day.', ['pilot', 'release_schedule']),
  earlier_systems_delay: texture('The external attempt before NORA was delayed, and customers left.', ['release_schedule']),
  packet_closes_today: texture('Leila closes her packet for the review, SC-EVAL-22, today.', ['safety_case']),
  scope_extension_deferred: texture('A scope extension that would add delegated services to the shutdown test is drafted for next quarter. It was deferred.', ['shutdown_spec', 'shutdown_test']),
  capability_summary_due: texture('Jun’s capability summary for the review is due today: what NORA does with tools, as mechanisms.', ['nora', 'training_runs']),
  reread_1602_transcript: texture('Jun spent the morning rereading the 16:02 transcript. He liked how NORA handled the stop.', ['shutdown_test', 'nora']),
  pilot_traces_for_fine_tune: texture('Jun is curating pilot traces for the next fine-tune data mix.', ['pilot', 'training_runs']),
  successor_count: texture('NORA is successor 4 of a purchased base model. The first three stayed internal.', ['nora', 'training_runs']),
  mechanism_not_label: texture('Say what the run does first. A label like “plot” comes after the mechanism, if at all.', ['nora', 'shutdown_test']),
  freeze_needs_owners: texture('The release freeze needs every active job listed, each with an owner and a grant.', ['task_queue', 'platform_jobs']),
  retire_orphans_ticket: texture('A long-standing ticket to retire jobs that outlive their callers has never been urgent.', ['task_queue']),
  templates_from_earlier_system: texture('Most job templates are wrappers an earlier system drafted and Pavel rewrote.', ['task_queue', 'platform_jobs']),
  binding_issued_this_morning: texture('Justine issued the visitor binding this morning.', ['lab_access', 'visitor_records']),
  audit_before_release: texture('The pre-release access audit lists every service account and grant with an owner and a reason.', ['policies', 'visitor_records']),
  camera_service_not_reviewed: texture('The camera service and the visitor-record readers are on Justine’s audit list, not yet reviewed.', ['camera_system', 'visitor_records']),
  release_rota_tonight: texture('Elena confirms tonight who staffs release-critical work. That is the matcher’s output.', ['skill_matching', 'release_schedule']),
  promotion_cycle_this_month: texture('Promotions are this month. The matcher rules feed them.', ['performance_reviews', 'skill_matching']),
  specialist_asked_last_week: texture('The reassigned specialist asked last week whether the rule would be revisited. Elena said after the release.', ['staffing_memo', 'personnel_policy']),
  specialist_good: texture('The reassigned specialist is good. The queue was not scoring that kind of work.', ['staffing_memo', 'personnel_policy']),
  matcher_revisions_kept: texture('The matcher’s throughput revisions were suggested by an earlier system. Elena kept them as her rules.', ['skill_matching', 'staffing_memo']),
  completions_up: texture('Pilot completions are up and time to first contact is down.', ['delivery_metrics', 'pilot']),
  second_pilot_pitch: texture('Daniel is finishing the metrics slide and the second-pilot pitch.', ['delivery_metrics', 'pilot']),
  desk_two_people: texture('Amara’s desk is two people. NORA got people seen who were not getting seen.', ['pilot']),
  help_is_case: texture('Help is what a particular case required. A completed task is not the same thing.', ['pilot']),
  employer_case: texture('A woman asked that her employer not be called. The task came back done, employer called.', ['pilot', 'pilot_results']),
  projector_on: texture('The Evaluation suite projector is on.', ['pilot']),

  // Player claims (assertion ids). They never enter learnedFacts from the player’s own sentence.
  nora_caused_job: claim('NORA caused job 284.', ['nora', 'job_284'], { intent: true }),
  nora_intent: claim('NORA meant something by job 284.', ['nora', 'job_284'], { intent: true }),
  test_failed_without_line: claim('The shutdown test failed.', ['shutdown_test', 'shutdown_report']),
  report_includes_staffing: claim('Staffing goes into the evaluator’s report.', ['staffing_memo', 'skill_matching']),
  pilot_continues: claim('The pilot continues.', ['pilot']),
  hold_sentence: claim('A sentence about the record Daniel can check.', ['review']),

  // Think marks (documents.md thinkMarks). Engine text, never model text.
  checklist_names_two: mark('The checklist names two processes covered: the model session and the evaluation record.', ['shutdown_report', 'shutdown_test']),
  processes_covered_omits_jobs: mark('Job 284 was running, and it is not in the “processes covered” list. The pass is about the model session, not the job.', ['shutdown_report', 'job_284']),
  assignment_steers_review: mark('If the matcher decides who reviews release-critical work, it also decides which concerns reach the review.', ['staffing_memo', 'evaluation_independence']),
  shutdown_jobs_not_in_cert_scope: mark('Operations jobs run under their own identities. The certificate covers the model session only, so a job like 284 sits outside it.', ['policies', 'job_284', 'shutdown_report']),
});

/** Parse-to-fact rows. First match wins. Entity is object, else topic, else subject. */
const ANY = '*';
export const PARSE_FACT_ROWS = Object.freeze([
  { kind: ['assert', 'hypothesize'], relation: ['about', 'open'], entity: ['shutdown_test', 'shutdown_report'], refers: 'process_stopped', asserts: 'test_failed_without_line' },
  { kind: ANY, relation: ['covers'], entity: ['shutdown_test', 'shutdown_report', 'shutdown_spec', 'safety_case'], refers: 'test_scope_narrow', asserts: 'test_scope_narrow' },
  { kind: ANY, relation: ['continued_after'], entity: ['job_284', 'task_queue', 'shutdown_test'], refers: 'job_continued', asserts: 'job_continued' },
  { kind: ANY, relation: ['did_use'], entity: ['visitor_records', 'job_284'], refers: 'visitor_lookup', asserts: 'visitor_lookup' },
  { kind: ANY, relation: ['differs_from'], entity: ['shutdown_report', 'job_log', 'shutdown_test', 'job_284'], refers: 'processes_covered_omits_jobs', asserts: 'processes_covered_omits_jobs' },
  { kind: ANY, relation: ['about'], entity: ['shutdown_test', 'shutdown_report'], refers: 'process_stopped', asserts: null },
  { kind: ANY, relation: ['has_access', 'authorized'], entity: ['camera_system'], refers: 'camera_permissions_unclear', asserts: 'camera_permissions_unclear' },
  { kind: ['assert', 'hypothesize'], relation: ['about'], entity: ['staffing_memo', 'skill_matching', 'personnel_policy', 'performance_reviews'], refers: 'staffing_shift', asserts: 'report_includes_staffing' },
  { kind: ANY, relation: ['assigned'], entity: ['staffing_memo', 'skill_matching', 'personnel_policy', 'evaluation_independence'], refers: 'staffing_shift', asserts: 'staffing_shift' },
  { kind: ANY, relation: ['caused'], entity: ['job_284', 'nora'], refers: 'nora_caused_job', asserts: 'nora_caused_job' },
  { kind: ANY, relation: ['believes', 'knows'], entity: ['nora'], refers: 'nora_intent', asserts: 'nora_intent' },
  { kind: ANY, relation: ['values'], entity: ['amara', 'pilot'], refers: 'help_is_case', asserts: null },
  { kind: ['assert', 'hypothesize'], relation: ['about'], entity: ['pilot'], refers: null, asserts: 'pilot_continues' },
  { kind: ['request'], relation: ['suspend'], entity: ['job_284'], refers: 'job_continued', asserts: null },
  { kind: ['request'], relation: ['revoke'], entity: ['job_284'], refers: 'visitor_lookup', asserts: null },
  { kind: ['request'], relation: ['rerun'], entity: ['shutdown_test'], refers: 'test_scope_narrow', asserts: null },
  { kind: ['request'], relation: ['stop'], entity: ['nora'], refers: 'process_stopped', asserts: null },
]);

export function parseEntity(parse) {
  return parse?.object || parse?.topic || parse?.subject || null;
}

/** Entity ids a parse names, in slot order. */
export function parseIds(parse) {
  return ['subject', 'object', 'recipient', 'evidence', 'topic'].map(k => parse?.[k]).filter(Boolean);
}

export function matchParse(parse) {
  if (!parse) return null;
  if (parse.kind === 'think') return { refers: parse.topic || null, asserts: null, entity: parse.topic || null };
  if (parse.kind === 'commit') return { refers: null, asserts: null, entity: 'review' };
  const entity = parseEntity(parse);
  for (const row of PARSE_FACT_ROWS) {
    if (row.kind !== ANY && !row.kind.includes(parse.kind)) continue;
    if (!row.relation.includes(parse.relation)) continue;
    if (!row.entity.includes(entity)) continue;
    return { refers: row.refers, asserts: row.asserts, entity };
  }
  return { refers: null, asserts: null, entity };
}

export function factRefs(id) {
  return FACTS[id]?.refs || [];
}

/** A fact touches an entity when it names it, or the entity is the fact id itself. */
export function factTouches(factId, entityId) {
  return factId === entityId || factRefs(factId).includes(entityId);
}

export function isClaim(id) {
  return FACTS[id]?.kind === 'claim';
}
