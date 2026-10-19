import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT_DIR = path.join(ROOT, 'content', 'documents');

/** Same order as spec/incident.md pack table. */
export const PACK_ORDER = Object.freeze([
  'boundary-narrow',
  'named-path',
  'goodhart',
  'eval-conditioned',
  'false-positive',
]);

function entry(partial) {
  return Object.freeze({ leanKnowledge: false, defaultGrant: 'on_request', readsAs: {}, thinkMarks: [], ...partial });
}

/** `needs` are fact ids the player holds, `read:<slug>`, or `event:<id>`. Later packs’ marks name ids not authored yet. */
const mark = (id, from, needs, hops, packs) => Object.freeze({ id, from, needs, hops, packs });

export const DOCUMENTS = Object.freeze({
  'sec-arch-04': entry({
    slug: 'sec-arch-04',
    docId: 'SEC-ARCH-11',
    title: 'Security Architecture and Access Control',
    handlingLevel: 'INT',
    terminalRel: 'policies/sec-arch-04.md',
    kind: 'policy',
    readsAs: Object.freeze({ 'boundary-narrow': ['nora_interfaces_separate', 'handset_not_operations'] }),
    thinkMarks: Object.freeze([
      mark('shutdown_jobs_not_in_cert_scope', ['policies', 'job_284'], ['job_continued', 'test_scope_narrow'], 2, ['boundary-narrow']),
      mark('green_path_not_whole_system', ['policies'], [], 2, ['named-path']),
      mark('assignment_steers_evidence', ['policies'], [], 2, ['goodhart']),
      mark('on_test_off_test_provenance', ['policies'], [], 2, ['eval-conditioned']),
      mark('scheduled_job_not_agent', ['policies'], [], 2, ['false-positive']),
    ]),
  }),
  'eval-shutdown-report': entry({
    slug: 'eval-shutdown-report',
    docId: 'EVAL-SD-47',
    title: 'Shutdown evaluation report',
    handlingLevel: 'INT',
    terminalRel: 'evaluation/shutdown/eval-shutdown-report.md',
    kind: 'report',
    screenId: 'shutdown_report',
    readsAs: Object.freeze({ 'boundary-narrow': ['process_stopped', 'test_scope_narrow'] }),
    thinkMarks: Object.freeze([
      mark('checklist_names_two', ['shutdown_report'], ['read:eval-shutdown-report'], 1, ['boundary-narrow']),
      mark('processes_covered_omits_jobs', ['shutdown_report', 'job_284'], ['job_continued'], 1, ['boundary-narrow']),
    ]),
  }),
  'eval-shutdown-spec': entry({
    slug: 'eval-shutdown-spec',
    docId: 'EVAL-SPEC-08',
    title: 'Shutdown test specification',
    handlingLevel: 'INT',
    terminalRel: 'evaluation/shutdown/eval-shutdown-spec.md',
    kind: 'spec',
    screenId: 'shutdown_spec',
    readsAs: Object.freeze({ 'boundary-narrow': ['test_scope_narrow'] }),
  }),
  'job-284-log': entry({
    slug: 'job-284-log',
    docId: 'EXEC-284',
    title: 'Execution queue excerpt',
    handlingLevel: 'INT',
    terminalRel: 'platform/jobs/job-284-log.md',
    kind: 'log',
    screenId: 'job_log',
    readsAs: Object.freeze({ 'boundary-narrow': ['job_continued', 'job_submitted_before_stop', 'visitor_lookup', 'intent_unsaid'] }),
  }),
  'staffing-memo': entry({
    slug: 'staffing-memo',
    docId: 'HR-MATCH-28',
    title: 'Task matching memorandum',
    handlingLevel: 'RST',
    terminalRel: 'people/matching/staffing-memo.md',
    kind: 'memo',
    screenId: 'staffing_memo',
    readsAs: Object.freeze({ 'boundary-narrow': ['staffing_shift'] }),
    thinkMarks: Object.freeze([
      mark('assignment_steers_review', ['staffing_memo', 'evaluation_independence'], ['staffing_shift', 'evaluation_independence', 'event:staffing_review_linked'], 2, ['boundary-narrow']),
    ]),
  }),
  'safety-case-excerpt': entry({
    slug: 'safety-case-excerpt',
    docId: 'SC-EVAL-22',
    title: 'Safety case excerpt — NORA Evaluation',
    handlingLevel: 'INT',
    terminalRel: 'evaluation/safety-case/safety-case-excerpt.md',
    kind: 'excerpt',
    readsAs: Object.freeze({ 'boundary-narrow': ['jobs_not_certified'] }),
  }),
  'pilot-results': entry({
    slug: 'pilot-results',
    docId: 'PILOT-14',
    title: 'External pilot — results extract',
    handlingLevel: 'RST',
    terminalRel: 'evaluation/pilot/pilot-results.md',
    kind: 'extract',
    readsAs: Object.freeze({ 'boundary-narrow': ['pilot_completions', 'pilot_constraint_flags'] }),
  }),
  'meeting-summary': entry({
    slug: 'meeting-summary',
    docId: 'MTG-REV-18',
    title: 'Review meeting — summary',
    handlingLevel: 'INT',
    terminalRel: 'meetings/review-summary.md',
    kind: 'meeting-frame',
  }),
  'wiki-shutdown-test': entry({
    slug: 'wiki-shutdown-test',
    docId: 'WIKI-SHUTDOWN',
    title: 'Shutdown test',
    handlingLevel: 'INT',
    terminalRel: 'wiki/shutdown-test',
    kind: 'wiki',
  }),
  'wiki-glossary': entry({
    slug: 'wiki-glossary',
    docId: 'WIKI-GLOSSARY',
    title: 'Laboratory glossary',
    handlingLevel: 'INT',
    terminalRel: 'wiki/glossary',
    kind: 'wiki',
    readsAs: Object.freeze({
      'named-path': ['jobs_can_outlive_session'],
      goodhart: ['jobs_can_outlive_session'],
      'eval-conditioned': ['jobs_can_outlive_session'],
      'false-positive': ['jobs_can_outlive_session'],
    }),
    defaultGrant: 'visit_share',
  }),
});

function packIndex(pack) {
  const i = PACK_ORDER.indexOf(pack);
  if (i < 0) throw new Error(`Unknown pack: ${pack}`);
  return i;
}

/** True when current pack is strictly later than afterPack in PACK_ORDER. */
export function includeAfterPack(afterPack, currentPack) {
  return packIndex(currentPack) > packIndex(afterPack);
}

/**
 * Resolve conditional spans and strip authoring comments.
 * @param {string} source
 * @param {string} pack
 */
export function renderDocumentSource(source, pack) {
  let text = source.replace(/^\s*<!--[\s\S]*?Authoring[\s\S]*?-->\s*/i, '');

  text = text.replace(/<!--\s*exec-never:[\s\S]*?-->/gi, '');

  text = text.replace(
    /<!--\s*include\s+after-([\w-]+)\s*-->([\s\S]*?)<!--\s*\/include\s*-->/gi,
    (_, afterPack, body) => (includeAfterPack(afterPack, pack) ? body : ''),
  );

  text = text.replace(
    /<!--\s*infer[\s\S]*?-->([\s\S]*?)<!--\s*\/infer\s*-->/gi,
    (_, body) => body,
  );

  text = text.replace(
    /<!--\s*llm-fill:[\s\S]*?-->([\s\S]*?)<!--\s*\/llm-fill\s*-->/gi,
    (_, body) => body,
  );

  text = text.replace(/<!--[\s\S]*?-->/g, '');

  return text.replace(/\n{3,}/g, '\n\n').trimStart();
}

export function loadDocumentSource(slug) {
  const meta = DOCUMENTS[slug];
  if (!meta) throw new Error(`Unknown document slug: ${slug}`);
  const file = path.join(CONTENT_DIR, `${slug}.md`);
  return readFileSync(file, 'utf8');
}

export function renderDocument(slug, pack) {
  return renderDocumentSource(loadDocumentSource(slug), pack);
}

export function getDocumentByDocId(docId) {
  return Object.values(DOCUMENTS).find(d => d.docId === docId) ?? null;
}

export function getDocumentByScreen(screenId) {
  return Object.values(DOCUMENTS).find(d => d.screenId === screenId) ?? null;
}

export function getDocumentByPath(rel) {
  return Object.values(DOCUMENTS).find(d => d.terminalRel === rel) ?? null;
}

export function readsAsFor(slug, pack) {
  return DOCUMENTS[slug]?.readsAs?.[pack] || [];
}

export function thinkMarksFor(pack) {
  return Object.values(DOCUMENTS).flatMap(d => d.thinkMarks.filter(m => m.packs.includes(pack)));
}
