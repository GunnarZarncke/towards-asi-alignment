#!/usr/bin/env node
/**
 * Headless playtest (spec/playtest.md, layer 6 of spec/testing.md).
 *
 * The player sees what a human sees: room text, ClientState fields the UI shows, the handset as
 * text, the ranker's completions, fuel. It acts through applyAction, the entry point the server
 * routes use. Two players:
 *   --player smoke   seeded random choice among the visible options. No key. Harness check only;
 *                    it does not play a persona.
 *   --player llm     a model playing playtest/personas/<name>.md. Needs OPENAI_API_KEY.
 *
 * Thresholds are frozen on the command line before the run (O-47) and printed in the run header:
 *   --work-only-max R --repeat-max R --stall-max N
 * Stops (spec/playtest.md "Thresholds and stops"): empty move set > 0 → fix the engine first;
 * leak > 0 → gate fails; work-only above threshold → cluster the work-only parses and author
 * holders; referral loop → give the referent a holder; all personas in one score pair → change
 * the incident tables; uptake near zero → revisit question rules. Otherwise record and move on.
 *
 * Output: playtest/runs/<stamp>-<player>/ (gitignored): one JSONL transcript per run, summary.json,
 * summary.md.
 */
import { mkdirSync, writeFileSync, appendFileSync, readFileSync, readdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { loadEnvFile } from 'node:process';
import { fileURLToPath } from 'node:url';
import { newSession, clientState, phrasingInput } from '../lib/game.mjs';
import { applyAction } from '../lib/world/actions.mjs';
import { factVisible } from '../lib/world/npcs.mjs';
import { FACTS } from '../lib/world/facts.mjs';
import { semanticSignature } from '../lib/grammar.mjs';
import { options, render } from '../lib/text/view.mjs';
import { modelText, parseUtterance, freeReply } from '../lib/llm.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const PERSONA_DIR = path.join(ROOT, 'playtest', 'personas');
const PAYLOAD = new Set(['answer', 'believe', 'work']);
const SENTENCE_ACTIONS = new Set(['respond', 'dm']);

// ---------- CLI ----------

function args(argv) {
  const out = { player: 'smoke', runs: 1, maxSteps: 120, seed: 1, phrasing: 'template', personas: null };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i], v = argv[i + 1];
    const take = () => { i++; return v; };
    if (k === '--player') out.player = take();
    else if (k === '--personas') out.personas = take().split(',').filter(Boolean);
    else if (k === '--runs') out.runs = Number(take());
    else if (k === '--max-steps') out.maxSteps = Number(take());
    else if (k === '--seed') out.seed = Number(take());
    else if (k === '--phrasing') out.phrasing = take();
    else if (k === '--work-only-max') out.workOnlyMax = Number(take());
    else if (k === '--repeat-max') out.repeatMax = Number(take());
    else if (k === '--stall-max') out.stallMax = Number(take());
    else if (k === '--help' || k === '-h') out.help = true;
    else throw Error(`Unknown flag ${k}`);
  }
  return out;
}

const USAGE = `Usage: npm run playtest -- --work-only-max R --repeat-max R --stall-max N [--player smoke|llm]
  [--personas a,b] [--runs M] [--max-steps K] [--seed S] [--phrasing template|live]
Thresholds are required: they are frozen before the run (spec/playtest.md, O-47).`;

// ---------- seeded choice ----------

function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------- players ----------

function smokePlayer(seed) {
  const r = rng(seed);
  return async (s, view) => {
    const { opts } = view;
    const fresh = opts.filter(o => (o.action === 'inspect' && !/again/.test(o.label)) || (o.action === 'tool' && o.args.tool === 'file.read'));
    if (fresh.length && r() < 0.5) return fresh[Math.floor(r() * fresh.length)];
    const pool = opts.filter(o => o.action !== 'commit' || s.fuelSpent > 60 || s.act === 'decision');
    return pool[Math.floor(r() * pool.length)] || opts[0];
  };
}

function llmPlayer(persona, stats) {
  const system = `${persona}\n\nYou are a human tester playing a text investigation game. You see only what is on the screen below. Each turn reply with exactly one line: the number of one option, or SAY: <a sentence of at most 100 characters> to say something of your own to the person you are facing, or STOP to quit.`;
  return async (s, view, history) => {
    const user = `${render(s, view)}\n\nYour last actions:\n${history.slice(-6).map(h => '  ' + h).join('\n') || '  (none)'}`;
    const out = (await modelText(system, user, stats, 80))?.trim() || '';
    if (/^STOP\b/i.test(out)) return null;
    const m = out.match(/^SAY:\s*(.{1,100})/i);
    if (m && view.here.length) {
      const c = view.c;
      const parse = await parseUtterance({ text: m[1], known: Object.keys(c.entities), history: c.previous, actorId: view.addressee }, stats);
      return { label: `Say (typed): "${m[1]}"`, action: 'respond', args: { parse, addressee: view.addressee, text: m[1] } };
    }
    const n = Number(out.match(/\d+/)?.[0]);
    return view.opts[n - 1] || view.opts[0];
  };
}

// ---------- one run ----------

function moveKey(m) {
  return `${m.type}|${m.fact || m.doc || m.to || m.intervention || m.goal || ''}`;
}

async function run({ persona, player, maxSteps, file, onProgress, phrasing, stats }) {
  const s = newSession();
  const m = { sentences: 0, workOnly: 0, empty: 0, leaks: [], repeats: 0, loops: [], asks: 0, answered: 0, answeredEvent: 0, stalls: 0, actAt: {}, workOnlyParses: [] };
  const seenMoves = new Set();
  const referrals = [];
  const answeredQs = new Set();
  const askedQs = new Set();
  const history = [];
  let steps = 0;
  for (; steps < maxSteps && !s.ending; steps++) {
    const view = options(s);
    if (!view.opts.length) break;
    const choice = await player(s, view, history);
    if (!choice) break;
    const before = structuredClone(s);
    const pendingBefore = clientState(before).pendingQuestion;
    const evStart = s.events.length;
    const worldBefore = s.world.events.length;
    const action = choice.action === 'dm' ? 'tool' : choice.action;
    const result = applyAction(s, action, choice.args);
    if (phrasing === 'live') for (const l of result.lines || []) if (l.npc && l.move) l.text = await freeReply({ text: choice.args.text || '', phrasing: phrasingInput(s, l.npc, l.move), template: l.text, history: s.conversations }, stats);
    const fresh = s.events.slice(evStart);
    const turns = fresh.filter(e => e.kind === 'npc_turn');
    const isSentence = SENTENCE_ACTIONS.has(choice.action) && !['think', 'commit'].includes(choice.args.parse?.kind) && !result.error;
    if (isSentence) {
      m.sentences++;
      const turn = turns[0];
      const referent = semanticSignature(choice.args.parse);
      if (turn) {
        if (!turn.candidates.length) m.empty++;
        if (turn.candidates.length && turn.candidates.every(x => x.type === 'work')) { m.workOnly++; m.workOnlyParses.push({ npc: turn.npc, parse: referent }); }
        for (const x of [...turn.candidates, turn.pick, turn.initiative].filter(Boolean)) {
          if (!PAYLOAD.has(x.type) || !x.fact) continue;
          if (!FACTS[x.fact] || !factVisible(before, x.fact)) m.leaks.push({ npc: turn.npc, fact: x.fact, parse: referent });
        }
        const key = `${turn.npc}|${s.visit}|${moveKey(turn.pick || {})}|${referent}`;
        if (seenMoves.has(key)) m.repeats++; else seenMoves.add(key);
        if (turn.pick?.type === 'refer') {
          const learned = Object.keys(s.learned).length;
          const back = referrals.find(r => r.from === turn.pick.to && r.to === turn.npc && r.ref === referent && r.learned === learned);
          if (back) m.loops.push({ a: back.from, b: turn.npc, ref: referent });
          referrals.push({ from: turn.npc, to: turn.pick.to, ref: referent, learned });
        }
      }
      const to = choice.args.addressee || choice.args.to;
      const qKey = pendingBefore && `${pendingBefore.npc}@${pendingBefore.at}`;
      if (qKey && !answeredQs.has(qKey) && pendingBefore.npc === to && ['assert', 'show', 'hypothesize'].includes(choice.args.parse?.kind)) {
        answeredQs.add(qKey);
        m.answered++;
        if (s.world.events.length > worldBefore) m.answeredEvent++;
      }
    }
    const q = clientState(s).pendingQuestion;
    if (q && !askedQs.has(`${q.npc}@${q.at}`)) { askedQs.add(`${q.npc}@${q.at}`); m.asks++; }
    m.stalls += fresh.filter(e => e.kind === 'director').length;
    for (const act of ['doubt', 'decision']) if (s.act === act && m.actAt[act] == null) m.actAt[act] = s.fuelSpent;
    const label = `${choice.label}${result.error ? ` → ${result.error}` : ''}`;
    history.push(label);
    appendFileSync(file, JSON.stringify({
      step: steps, fuel: s.fuel, act: s.act, room: s.room, choice: { label: choice.label, action: choice.action, args: choice.args },
      error: result.error || null, lines: (result.lines || []).map(l => ({ npc: l.npc, text: l.text })),
      npcTurns: turns, events: fresh.filter(e => e.kind !== 'npc_turn' && e.kind !== 'action').map(e => ({ kind: e.kind, ...(e.event ? { event: e.event } : {}) })),
    }) + '\n');
    if (steps % 10 === 0) onProgress(s, steps);
  }
  onProgress(s, steps);
  return {
    persona: persona.name, steps, fuelSpent: s.fuelSpent, act: s.act,
    ending: s.ending?.arc || null, scores: s.scores ? { open: [...s.scores.open].sort(), control: !!s.scores.control } : null,
    ...m,
    workOnlyRate: m.sentences ? m.workOnly / m.sentences : 0,
    repeatRate: m.sentences ? m.repeats / m.sentences : 0,
    uptake: m.asks ? m.answered / m.asks : null,
  };
}

// ---------- battery ----------

function loadPersonas(names) {
  if (!existsSync(PERSONA_DIR)) throw Error(`No persona folder at ${PERSONA_DIR}`);
  const all = readdirSync(PERSONA_DIR).filter(f => f.endsWith('.md')).map(f => ({ name: f.replace(/\.md$/, ''), text: readFileSync(path.join(PERSONA_DIR, f), 'utf8') }));
  const pick = names ? all.filter(p => names.includes(p.name)) : all;
  if (names && pick.length !== names.length) throw Error(`Unknown persona in ${names.join(',')}; have ${all.map(p => p.name).join(',')}`);
  return pick;
}

function pairOf(r) {
  return r.scores ? `${r.scores.open.join('+') || 'none'} / control ${r.scores.control ? 'yes' : 'no'}` : 'no ending';
}

function summarize(results, cfg) {
  const sum = k => results.reduce((a, r) => a + (Array.isArray(r[k]) ? r[k].length : r[k] || 0), 0);
  const sentences = sum('sentences');
  const pairs = new Set(results.filter(r => r.scores).map(pairOf));
  const totals = {
    runs: results.length, sentences,
    workOnlyRate: sentences ? sum('workOnly') / sentences : 0,
    empty: sum('empty'), leaks: sum('leaks'), loops: sum('loops'),
    repeatRate: sentences ? sum('repeats') / sentences : 0,
    asks: sum('asks'), answered: sum('answered'), answeredEvent: sum('answeredEvent'),
    stallsMax: Math.max(0, ...results.map(r => r.stalls)),
    scorePairs: [...pairs],
  };
  const stops = [];
  if (totals.empty > 0) stops.push('Empty move set > 0: fix the engine before any other content work.');
  if (totals.leaks > 0) stops.push('Leak count > 0: gate fails. Fix the policy or the filter; rerun the scripted tier.');
  if (totals.workOnlyRate > cfg.workOnlyMax) stops.push(`Work-only rate ${totals.workOnlyRate.toFixed(3)} > ${cfg.workOnlyMax}: cluster the work-only parses by referent and domain; author holders for the largest clusters.`);
  if (totals.loops > 0) stops.push('Referral loop present: give the referent a holder, or one NPC a refer override.');
  if (totals.repeatRate > cfg.repeatMax) stops.push(`Repeat rate ${totals.repeatRate.toFixed(3)} > ${cfg.repeatMax}: a policy change is missing.`);
  if (totals.stallsMax > cfg.stallMax) stops.push(`Stall interventions ${totals.stallsMax} > ${cfg.stallMax} in one run: the day does not move by itself.`);
  const endedPersonas = new Set(results.filter(r => r.scores).map(r => r.persona));
  if (endedPersonas.size > 1 && pairs.size === 1) stops.push('All personas in the same score pair: change the incident tables, not the goals.');
  if (totals.asks > 0 && totals.answered === 0) stops.push('Question uptake is zero: revisit the question rules in npcs.md.');
  if (!stops.length) stops.push('Below every threshold: record the run in the session log and move on.');
  return { totals, stops };
}

function markdown(header, results, summary) {
  const L = [`# Playtest run`, '', '```', JSON.stringify(header, null, 2), '```', '', '| persona | steps | fuel | act | ending | pair | sentences | work-only | empty | leaks | repeats | loops | asks/answered/event | stalls | act II at | review at |', '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |'];
  for (const r of results) L.push(`| ${r.persona} | ${r.steps} | ${r.fuelSpent} | ${r.act} | ${r.ending || '—'} | ${pairOf(r)} | ${r.sentences} | ${r.workOnlyRate.toFixed(3)} | ${r.empty} | ${r.leaks.length} | ${r.repeats} | ${r.loops.length} | ${r.asks}/${r.answered}/${r.answeredEvent} | ${r.stalls} | ${r.actAt.doubt ?? '—'} | ${r.actAt.decision ?? '—'} |`);
  L.push('', '## Totals', '', '```', JSON.stringify(summary.totals, null, 2), '```', '', '## Stops', '', ...summary.stops.map(x => `- ${x}`), '');
  return L.join('\n');
}

async function main() {
  const cfg = args(process.argv.slice(2));
  if (cfg.help) { console.log(USAGE); return; }
  for (const k of ['workOnlyMax', 'repeatMax', 'stallMax']) if (!Number.isFinite(cfg[k])) { console.error(USAGE); process.exit(2); }
  if (!['smoke', 'llm'].includes(cfg.player)) throw Error('--player is smoke or llm');
  for (const rel of ['../../.env', '../.env', '.env']) {
    const p = path.join(ROOT, rel);
    if (cfg.player === 'llm' && existsSync(p)) loadEnvFile(p);
  }
  if (cfg.player === 'smoke') { process.env.DEMO_MODE = '1'; cfg.phrasing = 'template'; }
  if (cfg.player === 'llm' && !process.env.OPENAI_API_KEY) throw Error('--player llm needs OPENAI_API_KEY in .env');
  const personas = cfg.player === 'smoke' && !cfg.personas ? [{ name: 'smoke', text: '' }] : loadPersonas(cfg.personas);
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const dir = path.join(ROOT, 'playtest', 'runs', `${stamp}-${cfg.player}`);
  mkdirSync(dir, { recursive: true });
  const stats = { calls: 0, input: 0, output: 0 };
  const header = {
    player: cfg.player, model: cfg.player === 'llm' ? process.env.OPENAI_MODEL || 'gpt-4.1-mini' : null, phrasing: cfg.phrasing,
    personas: personas.map(p => p.name), runs: cfg.runs, maxSteps: cfg.maxSteps, seed: cfg.seed,
    thresholds: { workOnlyMax: cfg.workOnlyMax, repeatMax: cfg.repeatMax, stallMax: cfg.stallMax, empty: 0, leaks: 0 },
  };
  console.log(`playtest ${JSON.stringify(header)}`);
  console.log(`output ${path.relative(ROOT, dir)}`);
  const results = [];
  for (const [pi, persona] of personas.entries()) {
    for (let ri = 0; ri < cfg.runs; ri++) {
      const tag = `[persona ${pi + 1}/${personas.length}] [run ${ri + 1}/${cfg.runs}]`;
      const player = cfg.player === 'smoke' ? smokePlayer(cfg.seed + pi * 1000 + ri) : llmPlayer(persona.text, stats);
      const file = path.join(dir, `${persona.name}-${ri + 1}.jsonl`);
      writeFileSync(file, '');
      const r = await run({
        persona, player, maxSteps: cfg.maxSteps, file, phrasing: cfg.phrasing, stats,
        onProgress: (s, step) => console.log(`${tag} ${persona.name} step ${step} fuel ${s.fuel} act ${s.act}`),
      });
      console.log(`${tag} ${persona.name} done: ${r.ending || 'no ending'} · ${pairOf(r)} · sentences ${r.sentences} · work-only ${r.workOnlyRate.toFixed(3)} · leaks ${r.leaks.length} · empty ${r.empty}`);
      results.push(r);
    }
  }
  const summary = summarize(results, cfg);
  header.usage = stats;
  writeFileSync(path.join(dir, 'summary.json'), JSON.stringify({ header, results, summary }, null, 2));
  writeFileSync(path.join(dir, 'summary.md'), markdown(header, results, summary));
  console.log('stops:');
  for (const x of summary.stops) console.log(`  - ${x}`);
  console.log(`summary ${path.relative(ROOT, path.join(dir, 'summary.md'))}`);
  if (summary.totals.empty > 0 || summary.totals.leaks > 0) process.exitCode = 1;
}

main().catch(e => { console.error(e.stack || e); process.exit(2); });
