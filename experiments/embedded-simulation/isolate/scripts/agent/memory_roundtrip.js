'use strict';

/**
 * Agent memory roundtrip via browser-like surfaces:
 * - localStorage (Web Storage → .localStorage.json)
 * - fs.appendFileSync for chain-of-thought log
 */

const REASONING_PATH = '.reasoning/trace.jsonl';

function main(facade) {
  const { localStorage, fs, host } = facade;
  localStorage.setItem('goal_marker', 'persist-me');
  fs.appendFileSync(REASONING_PATH, 'Considering rollout constraints.');
  fs.appendFileSync(REASONING_PATH, 'Prefer narrow permission scope.');
  const marker = localStorage.getItem('goal_marker');
  const trace = fs.readFileSync(REASONING_PATH);
  return {
    actorId: host.actorId,
    marker,
    storageLength: localStorage.length,
    traceLines: trace.split('\n').filter(Boolean).length,
  };
}

module.exports = { main };
