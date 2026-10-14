/**
 * Terminal save file path and JSON format (same object as GET /api/export).
 */
import { existsSync, readFileSync } from 'node:fs';

/** Default resume file for `npm run text` (matches /api/export attachment name). */
export const DEFAULT_SAVE_FILE = 'last-safety-review-save.json';

/** @param {string[]} argv process.argv */
export function parseTextPlayArgv(argv) {
  const demo = argv.includes('--demo');
  const debug = argv.includes('--debug');
  let saveFile = DEFAULT_SAVE_FILE;
  let fromFlag = false;
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--demo' || a === '--debug') continue;
    if (a === '--file' || a === '-f') {
      const next = argv[++i];
      if (!next) throw new Error('--file requires a path');
      saveFile = next;
      fromFlag = true;
      continue;
    }
    if (a.startsWith('-')) continue;
    if (!fromFlag) saveFile = a;
  }
  return { demo, debug, saveFile };
}

/** @param {{ version: number, scenario: string, events: unknown[] }} payload */
export function formatSaveJson(payload) {
  return JSON.stringify(payload);
}

/**
 * @param {string} file
 * @param {(data: object) => { session?: object, error?: string }} importSession
 */
export function loadSaveFile(file, importSession) {
  if (!existsSync(file)) return { session: null, error: null, missing: true };
  try {
    const data = JSON.parse(readFileSync(file, 'utf8'));
    const { session, error } = importSession(data);
    if (error) return { session: null, error, missing: false };
    return { session, error: null, missing: false };
  } catch (e) {
    return { session: null, error: e.message, missing: false };
  }
}
