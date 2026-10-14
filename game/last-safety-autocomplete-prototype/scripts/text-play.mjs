#!/usr/bin/env node
/**
 * Text console in the terminal (spec/text-console.md). `npm run text [-- --demo]`.
 * Live parsing and phrasing when OPENAI_API_KEY is set and --demo is not given; demo grammar otherwise.
 * Extra commands here: save [file], load <file>, reset, quit. --debug prints knowledge deltas after each line.
 * Resumes from the save file on start (default last-safety-review-save.json); override with --file or a positional path.
 */
import { createInterface } from 'node:readline';
import { existsSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { loadEnvFile } from 'node:process';
import { fileURLToPath } from 'node:url';
import { newSession, exportSession, importSession, clientState } from '../lib/game.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import { createConsole } from '../lib/text/console.mjs';
import { kbSnapshot, formatKbDelta } from '../lib/text/kb-debug.mjs';
import { tabCompleteLines } from '../lib/text/tab-complete.mjs';
import {
  DEFAULT_SAVE_FILE,
  parseTextPlayArgv,
  formatSaveJson,
  loadSaveFile,
} from '../lib/text/cli-save.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
let cli;
try {
  cli = parseTextPlayArgv(process.argv);
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
const { demo, debug } = cli;
let saveFile = cli.saveFile || DEFAULT_SAVE_FILE;

if (!demo) for (const rel of ['../../.env', '../.env', '.env']) {
  const p = path.join(ROOT, rel);
  if (existsSync(p)) loadEnvFile(p);
}
if (demo) process.env.DEMO_MODE = '1';
const live = !!process.env.OPENAI_API_KEY && process.env.DEMO_MODE !== '1';

function importFromJson(data) {
  return importSession(data, applyAction);
}

const initial = loadSaveFile(saveFile, importFromJson);
let s;
if (initial.session) {
  s = initial.session;
} else {
  if (initial.error) console.error(`Could not load ${saveFile}: ${initial.error}`);
  s = newSession();
}
const resumed = !!initial.session;

const con = createConsole(() => s, { phrase: live });
let tabStreak = { line: '', page: 0 };

const rl = createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: !!process.stdin.isTTY,
  completer: (line, callback) => {
    if (!process.stdin.isTTY) return callback(null, [[], line]);
    if (line !== tabStreak.line) tabStreak = { line, page: 0 };
    else tabStreak.page += 1;
    tabCompleteLines(s, line, tabStreak.page, { saveFile })
      .then(hits => callback(null, [hits.length ? hits : [], line]))
      .catch(() => callback(null, [[], line]));
  },
});
console.log(con.start());
if (resumed) console.log(`(resumed from ${saveFile})`);
console.log(live ? '(live: typed sentences are parsed by the model)' : '(demo: typed sentences use the local grammar)');
if (process.stdin.isTTY) console.log('(Tab completes commands and speech; Tab again for more options)');
if (debug) console.log('(debug: [debug knowledge] after each command)');
let kbBefore = debug ? kbSnapshot(clientState(s)) : null;

const echo = !process.stdin.isTTY;
const ask = () => { rl.setPrompt(`\n${con.prompt()}`); rl.prompt(); };

async function local(verb, rest) {
  if (/^save$/i.test(verb)) {
    const file = rest.join(' ').trim() || saveFile;
    writeFileSync(file, formatSaveJson(exportSession(s)));
    return `Saved to ${file}.`;
  }
  if (/^load$/i.test(verb)) {
    if (!rest.length) return 'Usage: load <file>';
    const file = rest.join(' ');
    const loaded = loadSaveFile(file, importFromJson);
    if (loaded.missing) return `No file: ${file}`;
    if (loaded.error) return `Could not load: ${loaded.error}`;
    s = loaded.session;
    saveFile = file;
    if (debug) kbBefore = kbSnapshot(clientState(s));
    return con.start();
  }
  if (/^reset$/i.test(verb)) {
    s = newSession();
    if (debug) kbBefore = kbSnapshot(clientState(s));
    return con.start();
  }
  return null;
}

ask();
for await (const line of rl) {
  if (echo) process.stdout.write(`${line}\n`);
  const [verb = '', ...rest] = line.trim().split(/\s+/);
  if (/^(quit|exit|q)$/i.test(verb)) break;
  const trimmed = line.trim();
  tabStreak = { line: '', page: 0 };
  if (debug && trimmed) kbBefore = kbSnapshot(clientState(s));
  const localOut = await local(verb, rest);
  const out = localOut ?? (await con.handle(line)).out;
  if (out) console.log(out);
  if (debug && trimmed) {
    const after = kbSnapshot(clientState(s));
    if (kbBefore) console.log(formatKbDelta(kbBefore, after));
    kbBefore = after;
  }
  ask();
}
rl.close();
