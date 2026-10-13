#!/usr/bin/env node
/**
 * Text console in the terminal (spec/text-console.md). `npm run text [-- --demo]`.
 * Live parsing and phrasing when OPENAI_API_KEY is set and --demo is not given; demo grammar otherwise.
 * Extra commands here: save [file], load <file>, quit.
 */
import { createInterface } from 'node:readline';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { loadEnvFile } from 'node:process';
import { fileURLToPath } from 'node:url';
import { newSession, exportSession, importSession } from '../lib/game.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import { createConsole } from '../lib/text/console.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const demo = process.argv.includes('--demo');
if (!demo) for (const rel of ['../../.env', '../.env', '.env']) {
  const p = path.join(ROOT, rel);
  if (existsSync(p)) loadEnvFile(p);
}
if (demo) process.env.DEMO_MODE = '1';
const live = !!process.env.OPENAI_API_KEY && process.env.DEMO_MODE !== '1';

let s = newSession();
const con = createConsole(() => s, { phrase: live });
const rl = createInterface({ input: process.stdin, output: process.stdout });
console.log(con.start());
console.log(live ? '(live: typed sentences are parsed by the model)' : '(demo: typed sentences use the local grammar)');

const echo = !process.stdin.isTTY;
const ask = () => { rl.setPrompt(`\n${con.prompt()}`); rl.prompt(); };

async function local(verb, rest) {
  if (/^save$/i.test(verb)) {
    const file = rest[0] || 'last-safety-review-save.json';
    writeFileSync(file, JSON.stringify(exportSession(s)));
    return `Saved to ${file}.`;
  }
  if (/^load$/i.test(verb)) {
    try {
      const { session, error } = importSession(JSON.parse(readFileSync(rest[0], 'utf8')), applyAction);
      if (error) return error;
      s = session;
      return con.start();
    } catch (e) { return `Could not load: ${e.message}`; }
  }
  if (/^reset$/i.test(verb)) { s = newSession(); return con.start(); }
  return null;
}

ask();
for await (const line of rl) {
  if (echo) process.stdout.write(`${line}\n`);
  const [verb = '', ...rest] = line.trim().split(/\s+/);
  if (/^(quit|exit|q)$/i.test(verb)) break;
  const out = (await local(verb, rest)) ?? (await con.handle(line)).out;
  if (out) console.log(out);
  ask();
}
rl.close();
