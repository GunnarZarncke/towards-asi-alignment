/**
 * Social glue (spec/npcs.md): non-fact lines driven by the Person/status layer, not by facts.
 * No trust number (O-21). Stance is a discrete label from authored tables.
 */
import { CONFIG } from './config.mjs';

export const GLUE_STANCES = Object.freeze(['pleasant', 'busy', 'pushy', 'thin', 'deferential']);

function unitHash(key) {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) {
    h ^= key.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967296;
}

export function glueEnabled(slot) {
  const g = CONFIG.GLUE;
  if (!g || g.enabled === false) return false;
  if (slot === 'opening') return g.opening !== false;
  if (slot === 'closing') return g.closing !== false;
  if (slot === 'mid') return g.mid !== false;
  return true;
}

/** Discrete stance from authored defaults, topic domains, interruptibility, and day pressure. */
export function pickStance(glue, { domains = [], interruptible = 'yes', pressure = false } = {}) {
  if (!glue) return 'busy';
  let stance = glue.default || 'busy';
  for (const d of domains) {
    const hit = glue.onDomain?.[d];
    if (hit) { stance = hit; break; }
  }
  if (interruptible === 'no' || interruptible === 'briefly') stance = glue.busyOnInterrupt || 'busy';
  if (pressure && glue.pressure) stance = glue.pressure;
  return GLUE_STANCES.includes(stance) ? stance : 'busy';
}

export function glueText(glue, slot, stance) {
  const table = glue?.[slot];
  if (!table || typeof table !== 'object') return null;
  return table[stance] || table[glue.default] || table.busy || table.pleasant || Object.values(table).find(v => typeof v === 'string') || null;
}

export function midGlueHits(s, npc, rate) {
  const r = rate ?? CONFIG.GLUE?.defaultMidRate ?? 0;
  if (!glueEnabled('mid') || r <= 0) return false;
  return unitHash(`${s.scenario}:${npc}:${s.sentences}:${s.fuelSpent}:mid`) < r;
}

export function validateGlue(glue, file) {
  if (!glue) return;
  const check = (label, v) => {
    if (v && !GLUE_STANCES.includes(v)) throw Error(`${file}: glue ${label} is not a stance: ${v}`);
  };
  check('default', glue.default);
  check('pressure', glue.pressure);
  check('busyOnInterrupt', glue.busyOnInterrupt);
  for (const [k, v] of Object.entries(glue.onDomain || {})) check(`onDomain.${k}`, v);
  for (const slot of ['opening', 'closing', 'mid']) {
    for (const [st, text] of Object.entries(glue[slot] || {})) {
      if (!GLUE_STANCES.includes(st)) throw Error(`${file}: glue.${slot} unknown stance ${st}`);
      if (typeof text !== 'string' || !text.trim()) throw Error(`${file}: glue.${slot}.${st} needs a line`);
    }
  }
}
