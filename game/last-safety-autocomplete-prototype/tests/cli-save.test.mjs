import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { exportSession, importSession, newSession } from '../lib/game.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import {
  DEFAULT_SAVE_FILE,
  parseTextPlayArgv,
  formatSaveJson,
  loadSaveFile,
} from '../lib/text/cli-save.mjs';

test('parseTextPlayArgv picks flags, --file, and positional save path', () => {
  assert.deepEqual(parseTextPlayArgv(['node', 'text-play.mjs']), {
    demo: false,
    debug: false,
    saveFile: DEFAULT_SAVE_FILE,
  });
  assert.deepEqual(parseTextPlayArgv(['node', 'text-play.mjs', '--demo', '--debug']), {
    demo: true,
    debug: true,
    saveFile: DEFAULT_SAVE_FILE,
  });
  assert.deepEqual(parseTextPlayArgv(['node', 'text-play.mjs', '--file', 'foo.json']), {
    demo: false,
    debug: false,
    saveFile: 'foo.json',
  });
  assert.deepEqual(parseTextPlayArgv(['node', 'text-play.mjs', '-f', 'bar.json']), {
    demo: false,
    debug: false,
    saveFile: 'bar.json',
  });
  assert.deepEqual(parseTextPlayArgv(['node', 'text-play.mjs', 'custom.json', '--demo']), {
    demo: true,
    debug: false,
    saveFile: 'custom.json',
  });
  assert.throws(() => parseTextPlayArgv(['node', 'text-play.mjs', '--file']));
});

test('formatSaveJson matches web export shape', () => {
  const s = newSession();
  const json = formatSaveJson(exportSession(s));
  const parsed = JSON.parse(json);
  assert.ok(Number.isInteger(parsed.version));
  assert.ok(typeof parsed.scenario === 'string');
  assert.ok(Array.isArray(parsed.events));
});

test('loadSaveFile imports a written save', () => {
  const dir = mkdtempSync(join(tmpdir(), 'lsr-save-'));
  const file = join(dir, 'test-save.json');
  const s = newSession();
  writeFileSync(file, formatSaveJson(exportSession(s)));
  const imp = (data) => importSession(data, applyAction);
  assert.deepEqual(loadSaveFile(join(dir, 'missing.json'), imp), {
    session: null,
    error: null,
    missing: true,
  });
  const loaded = loadSaveFile(file, imp);
  assert.equal(loaded.error, null);
  assert.equal(loaded.missing, false);
  assert.ok(loaded.session);
  rmSync(dir, { recursive: true });
});
