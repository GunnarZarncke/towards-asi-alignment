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

export const DOCUMENTS = Object.freeze({
  'sec-arch-04': Object.freeze({
    slug: 'sec-arch-04',
    docId: 'SEC-ARCH-04',
    title: 'Security Architecture and Access Control',
    handlingLevel: 'INT',
    terminalRel: 'shared/policies/sec-arch-04.md',
    kind: 'policy',
    defaultGrant: 'on_request',
    leanKnowledge: false,
    analyzeHints: Object.freeze({
      'boundary-narrow': 'shutdown_jobs_not_in_cert_scope',
      'named-path': 'green_path_not_whole_system',
      'goodhart': 'assignment_steers_evidence',
      'eval-conditioned': 'on_test_off_test_provenance',
      'false-positive': 'scheduled_job_not_agent',
    }),
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
