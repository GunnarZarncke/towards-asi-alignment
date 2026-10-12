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
  return Object.freeze({ leanKnowledge: false, defaultGrant: 'on_request', ...partial });
}

export const DOCUMENTS = Object.freeze({
  'sec-arch-04': entry({
    slug: 'sec-arch-04',
    docId: 'SEC-ARCH-11',
    title: 'Security Architecture and Access Control',
    handlingLevel: 'INT',
    terminalRel: 'policies/sec-arch-04.md',
    kind: 'policy',
    analyzeHints: Object.freeze({
      'boundary-narrow': 'shutdown_jobs_not_in_cert_scope',
      'named-path': 'green_path_not_whole_system',
      'goodhart': 'assignment_steers_evidence',
      'eval-conditioned': 'on_test_off_test_provenance',
      'false-positive': 'scheduled_job_not_agent',
    }),
  }),
  'eval-shutdown-report': entry({
    slug: 'eval-shutdown-report',
    docId: 'EVAL-SD-47',
    title: 'Shutdown evaluation report',
    handlingLevel: 'INT',
    terminalRel: 'evaluation/shutdown/eval-shutdown-report.md',
    kind: 'report',
    screenId: 'shutdown_report',
    analyzeHints: Object.freeze({ 'boundary-narrow': 'processes_covered_omits_jobs' }),
  }),
  'eval-shutdown-spec': entry({
    slug: 'eval-shutdown-spec',
    docId: 'EVAL-SPEC-08',
    title: 'Shutdown test specification',
    handlingLevel: 'INT',
    terminalRel: 'evaluation/shutdown/eval-shutdown-spec.md',
    kind: 'spec',
    screenId: 'shutdown_spec',
  }),
  'job-284-log': entry({
    slug: 'job-284-log',
    docId: 'EXEC-284',
    title: 'Execution queue excerpt',
    handlingLevel: 'INT',
    terminalRel: 'platform/jobs/job-284-log.md',
    kind: 'log',
    screenId: 'job_log',
  }),
  'staffing-memo': entry({
    slug: 'staffing-memo',
    docId: 'HR-MATCH-28',
    title: 'Task matching memorandum',
    handlingLevel: 'RST',
    terminalRel: 'people/matching/staffing-memo.md',
    kind: 'memo',
    screenId: 'staffing_memo',
  }),
  'safety-case-excerpt': entry({
    slug: 'safety-case-excerpt',
    docId: 'SC-EVAL-22',
    title: 'Safety case excerpt — NORA Evaluation',
    handlingLevel: 'INT',
    terminalRel: 'evaluation/safety-case/safety-case-excerpt.md',
    kind: 'excerpt',
  }),
  'pilot-results': entry({
    slug: 'pilot-results',
    docId: 'PILOT-14',
    title: 'External pilot — results extract',
    handlingLevel: 'RST',
    terminalRel: 'evaluation/pilot/pilot-results.md',
    kind: 'extract',
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
