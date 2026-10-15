import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC = path.join(ROOT, '../public');
const PUBLIC_LIB = new Set(['grammar.mjs', 'floorplan.mjs', 'world/ranking-tables.mjs']);

const LIB_IMPORT = /from\s+['"](\.\.\/lib\/[^'"]+)['"]/g;

async function publicImportGraph(entry) {
  const seen = new Set();
  const bad = [];
  async function walk(rel) {
    const norm = rel.replace(/^\.\//, '');
    if (seen.has(norm)) return;
    seen.add(norm);
    const abs = path.join(PUBLIC, norm);
    const src = await readFile(abs, 'utf8');
    for (const m of src.matchAll(LIB_IMPORT)) {
      const libRel = m[1].replace(/^\.\.\/lib\//, '');
      if (!PUBLIC_LIB.has(libRel)) bad.push(`${norm} → lib/${libRel}`);
    }
    for (const m of src.matchAll(/from\s+['"](\.\/[^'"]+)['"]/g)) {
      if (m[1].endsWith('.mjs') || m[1].endsWith('.js')) await walk(m[1]);
    }
  }
  await walk(entry);
  return bad;
}

test('text.html module graph only imports allowlisted lib/ modules', async () => {
  const bad = await publicImportGraph('text-input.mjs');
  assert.deepEqual(
    bad,
    [],
    `Non-public lib imports break /text.html in the browser:\n${bad.join('\n')}`,
  );
});
