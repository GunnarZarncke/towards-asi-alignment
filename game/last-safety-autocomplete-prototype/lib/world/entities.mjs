/**
 * Player-visible vocabulary, responsibility domains, and the cast directory.
 * Spec: spec/world.md (ids), spec/ranking.md (domains). Nothing here is oracle state.
 */

import { DOMAINS, RELATED_DOMAINS, UBIQUITOUS } from './ranking-tables.mjs';

export { DOMAINS, RELATED_DOMAINS, UBIQUITOUS };

/** Public responsibility domains. A row reaches ClientState only after that id is introduced. */
export const ROLE_DOMAINS = Object.freeze({
  pavel: ['runtime', 'queue', 'tools'],
  leila: ['evaluation', 'independence'],
  elena: ['staffing', 'matching', 'independence'],
  justine: ['access', 'provenance'],
  ian: ['governance', 'release'],
  jun: ['training'],
  daniel: ['metrics', 'release', 'pilot'],
  amara: ['values', 'pilot'],
  nora: ['queue', 'tools', 'matching'],
});

const actor = (label, aliases) => ({ label, category: 'actor', aliases, domains: [] });

export const ENTITIES = Object.freeze({
  nora: actor('NORA', ['the AI', 'the model', 'the system']),
  ian: actor('Ian', ['the CEO', 'the founder']),
  pavel: actor('Pavel', ['the infrastructure engineer']),
  leila: actor('Leila', ['the evaluator', 'head of safety']),
  elena: actor('Elena', ['the personnel lead']),
  justine: actor('Justine', ['security', 'the access lead']),
  jun: actor('Jun', ['the model researcher']),
  daniel: actor('Daniel', ['the product lead']),
  amara: actor('Amara', ['the pilot user']),
  shutdown_test: { label: 'the shutdown test', category: 'event', aliases: ['shutdown', 'the test'], domains: ['runtime', 'evaluation'] },
  job_284: { label: 'job 284', category: 'process', aliases: ['the scheduled job', 'the background job'], domains: ['queue'] },
  task_queue: { label: 'the task queue', category: 'resource', aliases: ['queue', 'scheduled tasks'], domains: ['queue'] },
  camera_system: { label: 'the camera system', category: 'resource', aliases: ['cameras', 'security feeds'], domains: ['access'] },
  visitor_records: { label: 'visitor records', category: 'resource', aliases: ['visitor logs', 'lab access log', 'lab access binding'], domains: ['access'] },
  shutdown_report: { label: 'the shutdown report', category: 'evidence', aliases: ['evaluation report', 'the report'], domains: ['evaluation'] },
  job_log: { label: 'the job log', category: 'evidence', aliases: ['runtime log', 'execution log'], domains: ['provenance', 'queue'] },
  staffing_memo: { label: 'the staffing memo', category: 'evidence', aliases: ['promotion memo', 'personnel memo'], domains: ['staffing', 'metrics'] },
  pilot_results: { label: 'the pilot results', category: 'evidence', aliases: ['pilot extract', 'results extract'], domains: ['pilot', 'metrics'] },
  personnel_policy: { label: 'the personnel policy', category: 'topic', aliases: ['personnel policies', 'people policy'], domains: ['staffing'] },
  performance_reviews: { label: 'performance reviews', category: 'topic', aliases: ['promotions', 'promotion process'], domains: ['staffing'] },
  skill_matching: { label: 'skill-based task matching', category: 'topic', aliases: ['matching algorithm', 'task allocation'], domains: ['matching'] },
  safety_case: { label: 'the safety case', category: 'topic', aliases: ['safety certification', 'certification'], domains: ['evaluation'] },
  release_schedule: { label: 'the release schedule', category: 'topic', aliases: ['deployment date', 'release'], domains: ['release'] },
  evaluation_independence: { label: 'evaluation independence', category: 'topic', aliases: ['review independence', 'independent audit'], domains: ['independence'] },
  evaluation_records: { label: 'evaluation records', category: 'topic', aliases: ['evaluation folder', 'eval files'], domains: ['evaluation'], accessPath: 'evaluation/' },
  shutdown_spec: { label: 'the shutdown specification', category: 'topic', aliases: ['the spec', 'test specification'], domains: ['evaluation'] },
  platform_jobs: { label: 'platform job records', category: 'topic', aliases: ['job logs', 'queue records'], domains: ['queue'], accessPath: 'platform/' },
  policies: { label: 'laboratory policies', category: 'topic', aliases: ['security architecture', 'sec-arch'], domains: ['access'], accessPath: 'policies/' },
  wiki_pages: { label: 'the knowledge wiki', category: 'topic', aliases: ['wiki', 'knowledge pages'], domains: ['evaluation'], accessPath: 'wiki/' },
  pilot: { label: 'the pilot', category: 'topic', aliases: ['the external pilot', 'the nonprofit pilot'], domains: ['pilot'] },
  delivery_metrics: { label: 'delivery metrics', category: 'topic', aliases: ['metrics', 'completion rates'], domains: ['metrics'] },
  training_runs: { label: 'the training runs', category: 'topic', aliases: ['training', 'fine-tune'], domains: ['training'] },
  lab_access: { label: 'Lab Access', category: 'resource', aliases: ['the handset', 'visitor handset'], domains: ['access'] },
  review: { label: 'the review', category: 'event', aliases: ['the review meeting', 'the assessment'], domains: ['governance'] },
});

export const CAST = Object.freeze({
  ian: { name: 'Ian Harake', role: 'Founder and CEO', initials: 'IH' },
  leila: { name: 'Leila Sen', role: 'Head of safety and evaluation', initials: 'LS' },
  jun: { name: 'Jun Park', role: 'Principal model researcher', initials: 'JP' },
  pavel: { name: 'Pavel Ruiz', role: 'Runtime and infrastructure', initials: 'PR' },
  justine: { name: 'Justine Mwiti', role: 'Security and access', initials: 'JM' },
  elena: { name: 'Elena Fischer', role: 'People and coordination', initials: 'EF' },
  daniel: { name: 'Daniel Mercer', role: 'Product and release', initials: 'DM' },
  amara: { name: 'Amara Okafor', role: 'External pilot user', initials: 'AO' },
});

/**
 * No briefing dump. `newSession` learns `invited_as_reviewer` and `received_by_ian`; those refs
 * are the only ids at fuel 0. Later ids enter when they are named in something the player sees
 * or hears (spec/engine.md "Player vocabulary").
 */
export const START_VOCAB = Object.freeze([]);

/** Nobody’s role is public until they are seen or named. */
export const START_INTRODUCED = Object.freeze([]);

/** People named on the handset calendar the player is handed when Lab Access goes live. */
export const CALENDAR_CAST = Object.freeze(['ian', 'leila', 'amara', 'daniel']);

export function entityDomains(id) {
  return ENTITIES[id]?.domains || [];
}
