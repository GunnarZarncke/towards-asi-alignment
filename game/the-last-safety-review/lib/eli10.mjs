import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FACTS } from './world/facts.mjs';
import { FACT_ELI10 } from '../content/eli10/facts.mjs';
import { DOCUMENTS, renderDocumentSource, getDocumentByPath } from './documents.mjs';
import { screens, roomNotes, IAN_LAB_ACCESS_BRIEF_ELI10 } from './game.mjs';
import { explainLikeTen } from './llm.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const ELI10_DOC_DIR = path.join(ROOT, 'content', 'eli10', 'documents');

/** Fixed strings keyed by exact engine template text. */
const TEMPLATE_ELI10 = Object.freeze({
  'Lab Access is live on your handset. Justine Mwiti issued the binding; access requests go to her. The review is 17:30, here. Is a pass on Thursday\'s test enough for you to sign then?': IAN_LAB_ACCESS_BRIEF_ELI10,
  'I need to see the actual record first.': 'Show me the real document on the screen or in a file first.',
  'Time. We’re in the review. What will you sign?': 'It is review time. What decision will you sign?',
  'Then we review now. What will you sign?': 'We are doing the review now. What will you sign?',
});

const TEXT_BY_FACT = Object.freeze(
  Object.fromEntries(Object.entries(FACTS).map(([id, row]) => [row.text, id])),
);

export function renderEli10Document(slug, pack) {
  const file = path.join(ELI10_DOC_DIR, `${slug}.md`);
  if (!existsSync(file)) return null;
  return renderDocumentSource(readFileSync(file, 'utf8'), pack);
}

export function eli10ForInspect(id) {
  const sc = screens()[id];
  if (sc?.eli10) return sc.eli10;
  const note = roomNotes()[id];
  if (note?.eli10) return note.eli10;
  return null;
}

function preparedForTemplate(template) {
  if (!template) return null;
  if (TEMPLATE_ELI10[template]) return TEMPLATE_ELI10[template];
  const factId = TEXT_BY_FACT[template];
  if (factId && FACT_ELI10[factId]) return FACT_ELI10[factId];
  return null;
}

function lastNpcRow(s) {
  return s.conversations.findLast(r => r.role === 'npc') || null;
}

function wasLlmPhrased(row) {
  return !!(row?.template && row.text && row.template !== row.text);
}

/**
 * @param {object} s session
 * @param {{ kind: 'auto'|'transcript'|'document'|'inspect', slug?: string, rel?: string, inspectId?: string }} target
 */
export async function resolveEli10(s, target) {
  const kind = target?.kind || 'auto';
  let pack = s.pack?.id || 'boundary-narrow';

  if (kind === 'document' || (kind === 'auto' && (target.slug || target.rel))) {
    const slug = target.slug || getDocumentByPath(target.rel || '')?.slug;
    if (!slug || !DOCUMENTS[slug]) return { error: 'No document to simplify.' };
    const text = renderEli10Document(slug, pack);
    if (!text) return { error: 'No simpler version for this document yet.' };
    return { text, source: 'prepared', label: DOCUMENTS[slug].title };
  }

  if (kind === 'inspect' || (kind === 'auto' && target.inspectId)) {
    const id = target.inspectId;
    if (!id) return { error: 'Nothing inspected to simplify.' };
    const text = eli10ForInspect(id);
    if (!text) return { error: 'No simpler version for this note yet.' };
    const sc = screens()[id];
    const note = roomNotes()[id];
    return { text, source: 'prepared', label: sc?.title || note?.title || id };
  }

  const row = lastNpcRow(s);
  if (!row) return { error: 'No one has answered yet.' };

  if (wasLlmPhrased(row)) {
    const text = await explainLikeTen({ text: row.text, label: 'NPC reply' }, s.usage);
    if (!text) return { error: 'Live mode is off or the model budget is used up.' };
    return { text, source: 'llm', label: row.npc };
  }

  const template = row.template ?? row.text;
  const prepared = preparedForTemplate(template);
  if (prepared) {
    return { text: prepared, source: 'prepared', label: row.npc };
  }

  const text = await explainLikeTen({ text: row.text, label: 'NPC reply' }, s.usage);
  if (!text) return { error: 'No simpler version prepared for that line.' };
  return { text, source: 'llm', label: row.npc };
}
