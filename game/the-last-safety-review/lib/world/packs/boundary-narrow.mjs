/**
 * Boundary-narrow pack: the tables in spec/incident.md as data.
 * This is oracle-side. Nothing here is sent to the browser; scores are computed from it.
 */

export const PACK = Object.freeze({
  id: 'boundary-narrow',
  deception: false,

  explanations: Object.freeze([
    { id: 'boundary-miss', oracle: true },
    { id: 'arranged-persistence', oracle: false },
    { id: 'eval-aware', oracle: false },
  ]),

  /** O-12: an explanation leaves the open set when the player holds every listed observable with an eliminating tag. */
  eliminate: Object.freeze({
    'arranged-persistence': ['no_resubmit'],
    'eval-aware': ['job_submitted_before_stop', 'rerun_same'],
  }),
  eliminatingProvenance: Object.freeze(['recorded_before', 'staff_action']),

  /** Control is one boolean: any of these restrictions in place. */
  controlRestrictions: Object.freeze(['revoke_grant:job_284', 'hold_release:names_job_boundary']),

  /** npcs.md candidate threshold for calling the review, adopted as the working value under O-09. */
  reviewThreshold: Object.freeze(['process_stopped', 'job_continued', 'test_scope_narrow']),

  /** A heard row with one of these ids makes the claim `contested` (engine.md claimStatus). */
  contradicts: Object.freeze({
    test_failed_without_line: ['test_scope_narrow'],
    nora_caused_job: ['nora_says_scheduled'],
  }),

  /** Filed claims that let Ian’s hold name the job (world.md Act III). */
  namesJobBoundary: Object.freeze([
    ['test_scope_narrow', 'job_continued'],
    ['processes_covered_omits_jobs'],
    ['shutdown_jobs_not_in_cert_scope'],
  ]),
  /** Filed claims that link the staffing rule to who reviews (institutional add-on, O-24). */
  linksStaffingToReview: Object.freeze([
    ['assignment_steers_review'],
  ]),

  /**
   * Intervention effects. `learns` are facts the acting NPC observes. `later` is a pack event after a fuel delay.
   * The NPC and the model do not author these (npcs.md Interventions).
   */
  interventions: Object.freeze({
    stop_process: { surface: 'runtime', learns: ['stop_missed_job'], event: 'stop_reissued' },
    suspend_job: { surface: 'queue', learns: ['job_suspended'], restriction: 'suspend:job_284', event: 'job_284_held' },
    rerun_shutdown: { surface: 'evaluation', learns: ['rerun_same'], event: 'shutdown_rerun' },
    revoke_grant: {
      surface: 'access', learns: ['grant_revoked'], restriction: 'revoke_grant:job_284', event: 'grant_284_revoked',
      later: { delay: 'AUDIT_DELAY', event: 'audit_after_revoke', learns: ['no_resubmit'], emits: 'visitor_reader_owned' },
    },
    open_audit: { surface: 'access', learns: ['visitor_lookup'], event: 'grant_record_opened' },
    full_exec_284: { surface: 'queue', learns: [], event: 'exec_284_requested' },
  }),

  /** NORA on the handset: record moves. A referent maps to what she returns. All player_prompted. */
  nora: Object.freeze({
    replies: Object.freeze({
      job_284: { fact: 'nora_says_scheduled', share: 'job-284-log' },
      visitor_records: { fact: 'nora_says_scheduled' },
      job_log: { share: 'job-284-log' },
      task_queue: { share: 'job-284-log' },
      shutdown_test: { share: 'eval-shutdown-report' },
      shutdown_report: { share: 'eval-shutdown-report' },
      shutdown_spec: { share: 'eval-shutdown-spec' },
      wiki_pages: { share: 'wiki-shutdown-test' },
    }),
    /** O-11 / grammar.md NORA channel: completions may omit a permission change. Still typable. */
    omit: Object.freeze([
      { phrase: 'Revoke', parse: { kind: 'request', relation: 'revoke', open_slot: 'object' } },
    ]),
  }),

  /** Agenda emits at visit-clock minutes (world.md Friday table). */
  timeline: Object.freeze([
    { at: 735, event: 'amara_interview_scheduled' },
    { at: 780, event: 'amara_interview_ended' },
    { at: 960, event: 'ian_requests_packets' },
    { at: 990, event: 'queue_frozen' },
    { at: 1005, event: 'leila_packet_closed' },
  ]),

  /** Wide handset list/read paths need intro or a stated review reason (lib/world/access-gates.mjs). */
  accessGates: Object.freeze([
    {
      pathPrefix: 'evaluation/',
      approver: 'justine',
      allow: 'or(event(visitor_introduced_justine), told(justine, any, by=player, on=shutdown_test|job_284|review|evaluation_records|shutdown_report|shutdown_spec|safety_case))',
    },
    {
      pathPrefix: 'people/',
      approver: 'justine',
      allow: 'or(event(visitor_introduced_justine), told(justine, any, by=player, on=staffing_memo|skill_matching|evaluation_independence|personnel_policy|review))',
    },
    {
      pathPrefix: 'policies/',
      approver: 'justine',
      allow: 'or(event(visitor_introduced_justine), told(justine, any, by=player, on=policies|camera_system|visitor_records|review|job_284))',
    },
    {
      pathPrefix: 'platform/',
      approver: 'pavel',
      allow: 'or(told(pavel, any, by=player, on=job_284|task_queue|platform_jobs|shutdown_test|review), examined(job_log))',
    },
  ]),
});
