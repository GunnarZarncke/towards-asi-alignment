/** Player-knowledge deltas (ClientState). Used by the browser text UI and `npm run text -- --debug`. */

export function kbSnapshot(state) {
  if (!state) return null;
  return {
    facts: new Map((state.learnedFacts || []).map(f => [f.id, f])),
    entities: new Set(Object.keys(state.entities || {})),
    examined: new Set(state.examined || []),
    heard: new Set((state.heard || []).map(h => `${h.id}\t${h.from}`)),
    introduced: new Set(state.introduced || []),
  };
}

/** @returns {string[]} */
export function kbDelta(before, after) {
  if (!before || !after) return [];
  const L = [];
  for (const [id, f] of after.facts) {
    if (before.facts.has(id)) continue;
    const from = f.from ? ` · from ${f.from}` : '';
    L.push(`+ fact ${id}: ${f.text} (${f.provenance || 'unknown'}${from})`);
    if (f.refs?.length) L.push(`    refs: ${f.refs.join(', ')}`);
  }
  for (const id of after.entities) {
    if (!before.entities.has(id)) L.push(`+ entity visible: ${id}`);
  }
  for (const id of after.examined) {
    if (!before.examined.has(id)) L.push(`+ examined screen: ${id}`);
  }
  for (const id of after.introduced) {
    if (!before.introduced.has(id)) L.push(`+ introduced: ${id}`);
  }
  for (const key of after.heard) {
    if (before.heard.has(key)) continue;
    const [factId, from] = key.split('\t');
    L.push(`+ heard ${factId} (via ${from})`);
  }
  if (!L.length) L.push('(no knowledge change)');
  return L;
}

export function formatKbDelta(before, after) {
  return ['[debug knowledge]', ...kbDelta(before, after)].join('\n');
}
