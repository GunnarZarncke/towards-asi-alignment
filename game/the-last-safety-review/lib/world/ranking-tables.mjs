/**
 * Domain tables for the O-19 ranker (spec/ranking.md). Served to the browser at
 * /lib/world/ranking-tables.mjs, so this file names domains only: no entity ids, no facts.
 */

export const DOMAINS = Object.freeze({
  runtime: 'operations', queue: 'operations', tools: 'operations',
  evaluation: 'assurance', independence: 'assurance',
  access: 'security', provenance: 'security',
  staffing: 'organization', matching: 'organization', metrics: 'organization',
  release: 'ship', training: 'ship', governance: 'ship',
  pilot: 'outside', values: 'outside',
});

export const RELATED_DOMAINS = Object.freeze([
  ['runtime', 'queue'], ['runtime', 'evaluation'], ['evaluation', 'independence'], ['queue', 'access'],
  ['access', 'provenance'], ['staffing', 'matching'], ['staffing', 'metrics'], ['matching', 'metrics'],
  ['metrics', 'release'], ['release', 'governance'], ['training', 'runtime'], ['pilot', 'values'], ['pilot', 'metrics'],
]);

/** Ids a search does not expand through. NORA is introduced from the first screen. */
export const UBIQUITOUS = Object.freeze(['nora']);
