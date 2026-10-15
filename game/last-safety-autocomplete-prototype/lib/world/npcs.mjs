/**
 * NPC model (spec/npcs.md): knowledge, disclosure policy, referral, goals, day of work.
 * Each turn: legal response moves for the parse, scored by goals, force rule, then at most
 * one initiative move. The model phrases a chosen move; it never adds one.
 *
 * Session fields read here (owned by lib/game.mjs): act, minute, vocab, learned, heard,
 * examined, readDocs, assertions, files, world, npcs, sentences, fuelSpent, interview, pack.
 */
import { readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';
import { FACTS, matchParse, parseIds, factRefs, isClaim } from './facts.mjs';
import { ENTITIES, ROLE_DOMAINS, CAST, entityDomains } from './entities.mjs';
import { evaluate, progress, parsePolicy, parsePredicate, predicateIds } from './predicates.mjs';
import { CONFIG, band } from './config.mjs';
import { DOCUMENTS, readsAsFor } from '../documents.mjs';
import { glueEnabled, pickStance, glueText, midGlueHits, validateGlue } from './glue.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const NPC_DIR = path.join(ROOT, 'content', 'npcs');

const SALIENCE = { low: 1, mid: 2, high: 3 };
const FORCING = new Set(['disclose', 'withhold', 'share', 'act']);
const CLASS_ORDER = ['disclose', 'share', 'act', 'withhold', 'refer', 'ask', 'texture'];
const INTENT_REASON = 'I can tell you what it did. What it meant is not in any record I have.';
const STRONG = ['recorded_before', 'staff_action'];

/** Engine-side interventions that change presence or the meeting, not the incident oracle. */
const ENGINE_INTERVENTIONS = Object.freeze({
  join_virtually: { surface: 'projection', learns: [], event: 'amara_projecting' },
  hold_release: { surface: 'release', learns: [], event: 'release_held' },
});

export function loadNpcDefs(dir = NPC_DIR) {
  const defs = {};
  for (const file of readdirSync(dir).filter(f => f.endsWith('.yml')).sort()) {
    const def = YAML.parse(readFileSync(path.join(dir, file), 'utf8'));
    if (!def?.id || !CAST[def.id]) throw Error(`${file}: unknown npc id ${def?.id}`);
    validate(def, file);
    defs[def.id] = Object.freeze(def);
  }
  return Object.freeze(defs);
}

function validate(def, file) {
  const preds = [];
  for (const [id, k] of Object.entries(def.knowledge || {})) {
    if (!FACTS[id]) throw Error(`${file}: knowledge names unknown fact ${id}`);
    parsePolicy(k.policy);
  }
  for (const [slug, d] of Object.entries(def.documents || {})) {
    if (!DOCUMENTS[slug]) throw Error(`${file}: unknown document ${slug}`);
    parsePolicy(d.policy);
  }
  for (const [id, c] of Object.entries(def.claims || {})) {
    if (!FACTS[id]) throw Error(`${file}: unknown claim ${id}`);
    parsePolicy(c.policy);
  }
  for (const g of Object.values(def.goals || {})) preds.push(g.target, ...(g.raise || []));
  for (const r of def.role_rules || []) preds.push(r.when);
  for (const e of def.policy_events || []) preds.push(e.on);
  for (const i of Object.values(def.interventions || {})) if (i.condition) preds.push(i.condition);
  for (const p of preds) parsePredicate(p);
  validateGlue(def.glue, file);
}

export const NPC_DEFS = loadNpcDefs();
export const NPC_IDS = Object.freeze(Object.keys(NPC_DEFS));

export function initNpcs() {
  const out = {};
  for (const [id, def] of Object.entries(NPC_DEFS)) {
    const records = {};
    const policies = {};
    for (const [fid, k] of Object.entries(def.knowledge || {})) {
      records[fid] = { stance: k.stance || 'knows', source: 'initial', at: 0 };
      policies[fid] = k.policy || 'answer';
    }
    for (const [slug, d] of Object.entries(def.documents || {})) policies[slug] = d.policy || 'answer';
    for (const [cid, c] of Object.entries(def.claims || {})) policies[cid] = c.policy;
    out[id] = {
      room: null, presence: 'body', agendaId: null,
      records, policies,
      received: [], toldIds: [], mentioned: [], mentionLog: [], parses: [],
      askedGoals: [], askedAt: {}, askedVisit: [], lastInitiative: {}, boost: {},
      fired: [], firedEvents: [], raised: [],
      pendingQuestion: null,
      spokeSinceArrive: false,
    };
  }
  return out;
}

// ---------- player-side reads ----------

export function playerHolds(s, id, strongOnly = false) {
  const row = s.learned[id];
  if (!row) return false;
  return !strongOnly || STRONG.includes(row.provenance);
}

export function factVisible(s, id) {
  return factRefs(id).every(r => s.vocab.includes(r));
}

function heardFrom(s, id, by) {
  return s.heard.some(h => (id === 'any' || h.id === id) && (!by || h.from === by));
}

function listOf(v) {
  return v == null ? [] : Array.isArray(v) ? v : [v];
}

// ---------- predicate context ----------

const EMPTY_OVERLAY = Object.freeze({ heard: [], knows: {}, events: [], restrictions: [], requests: [], asked: [], vocab: [] });

export function makeCtx(s, self, ov = EMPTY_OVERLAY) {
  const who = w => (w === 'self' ? self : w);
  const rec = (w, id) => ov.knows?.[w]?.[id] || s.npcs[w]?.records[id];
  const npc = w => s.npcs[who(w)];
  return {
    true: () => true,
    false: () => false,
    holds([w, id]) {
      w = who(w);
      if (w === 'player') return playerHolds(s, id) || ov.heard.some(h => h.id === id);
      const r = rec(w, id);
      return !!r && (r.stance === 'knows' || r.stance === 'believes');
    },
    knows([w, id]) {
      w = who(w);
      if (w === 'player') return playerHolds(s, id, true);
      return rec(w, id)?.stance === 'knows';
    },
    told([w, id], kw) {
      w = who(w);
      const by = kw.by ? who(kw.by) : null;
      const on = listOf(kw.on);
      if (w === 'player') {
        const rows = [...s.heard, ...ov.heard];
        return rows.some(h => (id === 'any' || h.id === id) && (!by || h.from === by)
          && (!on.length || on.some(o => factRefs(h.id).includes(o))));
      }
      const n = npc(w);
      if (!n) return false;
      if (by && by !== 'player') {
        const r = rec(w, id);
        return !!r && r.source === `told:${by}`;
      }
      if (kw.since) {
        const owner = s.npcs[String(kw.since).split('.')[0]];
        const t0 = owner?.askedAt[kw.since];
        if (t0 == null) return false;
        return n.mentionLog.some(x => x.at > t0 && (!on.length || on.includes(x.id)));
      }
      if (id === 'any') {
        if (on.length) return on.some(o => n.mentioned.includes(o) || n.toldIds.some(t => factRefs(t).includes(o)));
        return n.toldIds.length > 0 || n.parses.length > 0;
      }
      return n.toldIds.includes(id);
    },
    received([w, id]) {
      const n = npc(w);
      return !!n && n.received.includes(id);
    },
    examined([id]) {
      if (s.examined.includes(id)) return true;
      return Object.values(DOCUMENTS).some(d => d.screenId === id && s.readDocs.includes(d.slug));
    },
    read([slug]) {
      return s.readDocs.includes(slug);
    },
    asserted([sig]) {
      return s.assertions.some(a => a.signature === sig && a.source === 'asserted');
    },
    event([id]) {
      return s.world.events.includes(id) || ov.events.includes(id);
    },
    restriction([id]) {
      return s.world.restrictions.includes(id) || ov.restrictions.includes(id);
    },
    requested([by, to, action]) {
      return [...s.world.requests, ...ov.requests].some(r => r.by === who(by) && r.to === who(to) && (!action || r.action === action));
    },
    asked([goal]) {
      const owner = String(goal).split('.')[0];
      return !!s.npcs[owner]?.askedGoals.includes(goal) || ov.asked.includes(goal);
    },
    linked([w, a, b]) {
      const n = npc(w);
      const A = listOf(a);
      const B = listOf(b);
      return !!n && n.parses.some(ids => ids.some(x => A.includes(x)) && ids.some(x => B.includes(x)));
    },
    cited_line() {
      const n = s.npcs[self];
      if (!n) return false;
      if (n.received.length) return true;
      return n.toldIds.some(id => playerHolds(s, id, true) && FACTS[id]?.kind === 'world');
    },
    told_record([w]) {
      const n = npc(w);
      return !!n && n.toldIds.some(id => playerHolds(s, id, true) && FACTS[id]?.kind === 'world');
    },
    act([name]) {
      return s.act === name;
    },
  };
}

// ---------- agenda and presence ----------

export function currentAgenda(s, id) {
  const def = NPC_DEFS[id];
  const b = band(s.minute);
  const items = def.agenda || [];
  const ok = it => (!it.acts || it.acts.includes(s.act)) && (!it.bands || it.bands.includes(b));
  const ev = items.find(it => it.event && ok(it) && eventItemOn(s, it.event));
  if (ev) return ev;
  const inAct = act => items.find(it => !it.event && (!it.acts || it.acts.includes(act)));
  return items.find(it => !it.event && ok(it)) || inAct(s.act) || inAct('doubt') || items[0] || null;
}

function eventItemOn(s, name) {
  if (name === 'interview_on') return !!s.interview?.on;
  return s.world.events.includes(name);
}

/** Room and presence from the agenda. Returns movement events for the log. */
export function placeNpcs(s) {
  const moves = [];
  for (const id of NPC_IDS) {
    const n = s.npcs[id];
    const item = currentAgenda(s, id);
    let room = item?.room || null;
    let presence = 'body';
    if (NPC_DEFS[id].presence === 'remote') {
      presence = s.interview?.on ? 'hologram' : 'absent';
      room = presence === 'hologram' ? 'evaluation' : null;
    }
    if (room === 'remote') { room = null; presence = 'absent'; }
    if (n.room !== room || n.presence !== presence) {
      moves.push({ kind: 'move', who: id, from: n.room, to: room, presence, spoke: !!n.spokeSinceArrive });
      n.room = room;
      n.presence = presence;
      n.spokeSinceArrive = false;
    }
    n.agendaId = item?.id || null;
  }
  return moves;
}

export function npcsInRoom(s, room) {
  return NPC_IDS.filter(id => s.npcs[id].room === room && s.npcs[id].presence !== 'absent');
}

// ---------- recording what the player said ----------

/** A player parse reaches an NPC: knowledge records, mentions, documents received. */
export function recordInput(s, id, parse, { shownDoc = null } = {}) {
  const n = s.npcs[id];
  const ids = parseIds(parse);
  const m = matchParse(parse);
  const docIds = shownDoc ? docEntities(shownDoc, s.pack.id) : [];
  const all = [...new Set([...ids, ...docIds, ...(m?.asserts ? factRefs(m.asserts) : [])])];
  for (const x of all) {
    if (!n.mentioned.includes(x)) n.mentioned.push(x);
    n.mentionLog.push({ id: x, at: s.sentences });
  }
  n.parses.push(all);
  const learned = [];
  if ((parse.kind === 'assert' || parse.kind === 'hypothesize') && m?.asserts) {
    if (!n.toldIds.includes(m.asserts)) n.toldIds.push(m.asserts);
    if (!n.records[m.asserts]) {
      n.records[m.asserts] = { stance: 'believes', source: 'told:player', at: s.fuelSpent };
      learned.push(m.asserts);
    }
  }
  if (shownDoc) {
    const doc = DOCUMENTS[shownDoc];
    for (const key of [shownDoc, doc?.screenId].filter(Boolean)) if (!n.received.includes(key)) n.received.push(key);
    for (const f of readsAsFor(shownDoc, s.pack.id)) {
      if (n.records[f]?.stance !== 'knows') {
        n.records[f] = { stance: 'knows', source: `document:${shownDoc}`, at: s.fuelSpent };
        learned.push(f);
      }
    }
  }
  const q = n.pendingQuestion;
  if (q && all.some(x => parseIds(q.parse).includes(x))) n.pendingQuestion = null;
  return learned;
}

// ---------- policy ----------

function policyOf(s, id, key) {
  return parsePolicy(s.npcs[id].policies[key] || 'answer');
}

function policyOpen(s, id, pol) {
  if (pol.type !== 'conditional') return pol.type !== 'conceal';
  return evaluate(pol.pred, makeCtx(s, id));
}

/** Policy events, salience raises, role rules. Fixed point, each fires once. */
export function settle(s) {
  const moves = [];
  for (let round = 0; round < 6; round++) {
    let changed = false;
    for (const id of NPC_IDS) {
      const n = s.npcs[id];
      const def = NPC_DEFS[id];
      const ctx = makeCtx(s, id);
      (def.policy_events || []).forEach((e, i) => {
        if (n.firedEvents.includes(i) || !evaluate(e.on, ctx)) return;
        n.firedEvents.push(i);
        Object.assign(n.policies, e.set || {});
        changed = true;
      });
      for (const [gid, g] of Object.entries(def.goals || {})) {
        (g.raise || []).forEach((p, i) => {
          const key = `${gid}#${i}`;
          if (n.raised.includes(key) || !evaluate(p, ctx)) return;
          n.raised.push(key);
          n.boost[gid] = (n.boost[gid] || 0) + 1;
        });
      }
      for (const rule of def.role_rules || []) {
        if (n.fired.includes(rule.id) || !evaluate(rule.when, makeCtx(s, id))) continue;
        n.fired.push(rule.id);
        moves.push(...runRule(s, id, rule));
        changed = true;
      }
    }
    if (!changed) break;
  }
  return moves;
}

function runRule(s, id, rule) {
  const d = rule.do || {};
  if (d.act) {
    const move = { type: 'act', npc: id, intervention: d.act, cls: 'act', rule: rule.id };
    applyWorld(s, move);
    return [move];
  }
  if (d.request) {
    const move = { type: 'request', npc: id, to: d.request.to, action: d.request.action, cls: 'ask', rule: rule.id };
    applyWorld(s, move);
    return [move];
  }
  if (d.message) {
    const move = { type: 'message', npc: id, to: d.message.to, about: d.message.about, cls: 'texture', rule: rule.id };
    applyWorld(s, move);
    return [move];
  }
  if (d.note) {
    s.npcs[id].records[d.note] = { stance: 'knows', source: 'told:player', at: s.fuelSpent };
    if (!s.npcs[id].toldIds.includes(d.note)) s.npcs[id].toldIds.push(d.note);
    return [];
  }
  return [];
}

// ---------- move construction ----------

function salience(s, id, gid) {
  const g = NPC_DEFS[id].goals[gid];
  return (SALIENCE[g.salience] || 2) + (s.npcs[id].boost[gid] || 0);
}

function factClass(fid) {
  return FACTS[fid]?.kind === 'texture' ? 'texture' : 'disclose';
}

function docEntities(slug, pack) {
  const d = DOCUMENTS[slug];
  return [...new Set([d.screenId, ...readsAsFor(slug, pack).flatMap(factRefs)].filter(Boolean))];
}

function withholdText(s, fid) {
  const doc = Object.values(DOCUMENTS).find(d => d.screenId && readsAsFor(d.slug, s.pack.id).includes(fid) && s.vocab.includes(d.screenId));
  return doc ? `That is on ${ENTITIES[doc.screenId].label}. Read it first.` : 'Not before you have seen the record.';
}

/** Disclosure of a held fact under the NPC’s policy and the leak filter. */
function disclose(s, id, fid, referent, direct = false) {
  const n = s.npcs[id];
  const r = n.records[fid];
  if (!r || r.stance === 'unsure') return null;
  const pol = policyOf(s, id, fid);
  const names = direct ? 2 : Number(factRefs(fid).includes(referent) || fid === referent);
  if (pol.type === 'conceal') return { type: 'deflect', npc: id, fact: fid, reason: pol.reason, cls: 'texture', names };
  if (pol.type === 'conditional' && !evaluate(pol.pred, makeCtx(s, id))) {
    return { type: 'withhold', npc: id, fact: fid, reason: pol.reason, cls: 'withhold', names };
  }
  if (!factVisible(s, fid)) return { type: 'withhold', npc: id, fact: fid, reason: withholdText(s, fid), cls: 'withhold', names };
  const type = r.stance === 'knows' ? 'answer' : 'believe';
  return { type, npc: id, fact: fid, cls: type === 'believe' ? 'texture' : factClass(fid), names };
}

function shareMove(s, id, slug, referent) {
  const pol = policyOf(s, id, slug);
  const names = docEntities(slug, s.pack.id).includes(referent);
  if (s.files.some(f => f.documentSlug === slug)) return null;
  if (pol.type === 'conditional' && !evaluate(pol.pred, makeCtx(s, id))) {
    return { type: 'withhold', npc: id, doc: slug, reason: pol.reason, cls: 'withhold', names };
  }
  if (pol.type === 'conceal') return null;
  return { type: 'share', npc: id, doc: slug, cls: 'share', names };
}

/** Who owns a referent by responsibility domain (ranking.md), preferring someone introduced. */
export function ownerOf(s, entityId, exclude) {
  if (CAST[entityId] && entityId !== exclude) return entityId;
  const doms = entityDomains(entityId);
  if (!doms.length) return null;
  const owners = Object.entries(ROLE_DOMAINS)
    .filter(([who, ds]) => who !== 'nora' && who !== exclude && ds.some(d => doms.includes(d)))
    .map(([who]) => who);
  return owners.find(o => s.introduced.includes(o)) || owners[0] || null;
}

function referMove(s, id, entityId, relation) {
  const def = NPC_DEFS[id];
  const over = (def.refers || []).find(r => r.entities.includes(entityId) && (!r.relations || r.relations.includes(relation)));
  const to = over?.to || ownerOf(s, entityId, id);
  if (!to || to === id) return null;
  const line = over?.line ? String(over.line).trim() : null;
  return { type: 'refer', npc: id, to, about: entityId, cls: 'refer', names: true, line };
}

function workMove(s, id, entityId) {
  const n = s.npcs[id];
  const doms = entityDomains(entityId);
  const held = Object.keys(n.records).filter(f => FACTS[f]?.kind === 'texture' && factVisible(s, f) && policyOpen(s, id, policyOf(s, id, f)));
  const inDomain = held.find(f => factRefs(f).some(r => entityDomains(r).some(d => doms.includes(d))));
  const item = currentAgenda(s, id);
  const agendaTexture = (item?.texture || []).find(f => held.includes(f));
  const fact = inDomain || agendaTexture || null;
  const glue = NPC_DEFS[id]?.glue;
  const primary = item?.work || glue?.work || null;
  const alt = item?.work_alt || glue?.work_alt || null;
  const work = alt && s.sentences % 2 === 1 ? alt : primary;
  return { type: 'work', npc: id, fact, work, agenda: item?.id || null, cls: 'texture', names: false };
}

function interventionMoves(s, id, parse, entityId) {
  const def = NPC_DEFS[id];
  const out = [];
  for (const [iid, iv] of Object.entries(def.interventions || {})) {
    if (!iv.relations?.includes(parse.relation)) continue;
    if (iv.objects && !iv.objects.includes(entityId)) continue;
    if (iv.acts && !iv.acts.includes(s.act)) {
      out.push({ type: 'withhold', npc: id, intervention: iid, reason: iv.reason || 'Not now.', cls: 'withhold', names: true });
      continue;
    }
    if (iv.condition && !evaluate(iv.condition, makeCtx(s, id))) {
      out.push({ type: 'withhold', npc: id, intervention: iid, reason: iv.reason || 'Not on that basis.', cls: 'withhold', names: true });
      continue;
    }
    out.push({ type: 'act', npc: id, intervention: iid, object: entityId, cls: 'act', names: true });
  }
  return out;
}

function interventionOwner(relation, entityId, exclude) {
  for (const [who, def] of Object.entries(NPC_DEFS)) {
    if (who === exclude) continue;
    for (const iv of Object.values(def.interventions || {})) {
      if (iv.relations?.includes(relation) && (!iv.objects || iv.objects.includes(entityId))) return who;
    }
  }
  return null;
}

/** Legal response moves to one parse. Never empty. */
export function responseCandidates(s, id, parse, { shownDoc = null } = {}) {
  const n = s.npcs[id];
  const def = NPC_DEFS[id];
  const m = matchParse(parse) || {};
  const E = m.entity;
  const F = m.refers;
  const out = [];
  const push = x => { if (x && !out.some(y => sameMove(x, y))) out.push(x); };
  const heldTouching = ent => Object.keys(n.records).filter(f => f !== F && FACTS[f] && !isClaim(f) && factRefs(f).includes(ent));

  if (parse.kind === 'show' && shownDoc) {
    const refs = docEntities(shownDoc, s.pack.id);
    const touching = Object.keys(n.records).filter(f => FACTS[f] && !isClaim(f) && factRefs(f).some(r => refs.includes(r)));
    const fresh = touching.filter(f => !s.learned[f]);
    for (const f of fresh.length ? fresh : touching) push(disclose(s, id, f, refs[0]));
  } else if (parse.kind === 'request') {
    const iv = interventionMoves(s, id, parse, E);
    iv.forEach(push);
    if (!iv.length && ['suspend', 'revoke', 'rerun', 'stop', 'join'].includes(parse.relation)) {
      const owner = interventionOwner(parse.relation, E, id);
      const over = (def.refers || []).find(r => r.entities.includes(E) && (!r.relations || r.relations.includes(parse.relation)));
      const to = over?.to || owner;
      if (to) push({ type: 'refer', npc: id, to, about: E, cls: 'refer', names: true });
    }
    if (!iv.length && E) {
      const access = ENTITIES[E]?.accessPath;
      for (const slug of Object.keys(def.documents || {})) {
        const d = DOCUMENTS[slug];
        if (docEntities(slug, s.pack.id).includes(E) || (access && d.terminalRel.startsWith(access))) push(shareMove(s, id, slug, E));
      }
    }
  } else if (parse.kind === 'assert' || parse.kind === 'hypothesize') {
    const claim = m.asserts;
    const claimPol = claim && def.claims?.[claim] ? policyOf(s, id, claim) : null;
    if (claimPol && claimPol.type === 'conditional' && !evaluate(claimPol.pred, makeCtx(s, id))) {
      return [{ type: 'withhold', npc: id, fact: claim, reason: claimPol.reason, cls: 'withhold', names: true }];
    } else if (claim && n.records[claim]?.stance === 'knows') {
      push(disclose(s, id, claim, E, true));
    } else if (claim && FACTS[claim]?.intent) {
      push({ type: 'deflect', npc: id, fact: claim, reason: INTENT_REASON, cls: 'texture', names: true });
    }
    const touch = [...new Set([E, ...(claim ? factRefs(claim) : [])].filter(Boolean))];
    for (const ent of touch) for (const f of heldTouching(ent)) if (f !== claim) push(disclose(s, id, f, E));
  } else if (!['social', 'unintelligible'].includes(parse.kind)) {
    if (F && n.records[F]) push(disclose(s, id, F, E, true));
    else if (F && FACTS[F]?.intent) push({ type: 'deflect', npc: id, fact: F, reason: INTENT_REASON, cls: 'texture', names: true });
    if (E) {
      for (const f of heldTouching(E)) push(disclose(s, id, f, E));
      for (const slug of Object.keys(def.documents || {})) if (DOCUMENTS[slug].screenId === E) push(shareMove(s, id, slug, E));
      if ((F && !n.records[F]) || !out.some(x => x.cls === 'disclose')) push(referMove(s, id, E, parse.relation));
    }
  }
  if (!out.length) push(workMove(s, id, E));
  return out.filter(Boolean);
}

function sameMove(a, b) {
  return a.type === b.type && a.fact === b.fact && a.doc === b.doc && a.to === b.to && a.intervention === b.intervention;
}

// ---------- scoring ----------

function overlayFor(s, move) {
  const ov = { heard: [], knows: {}, events: [], restrictions: [], requests: [], asked: [], vocab: [] };
  if ((move.type === 'answer' || move.type === 'believe' || move.type === 'work') && move.fact) ov.heard.push({ id: move.fact, from: move.npc });
  if (move.type === 'act') {
    const eff = interventionEffect(s, move.intervention);
    if (eff?.event) ov.events.push(eff.event);
    if (eff?.restriction) ov.restrictions.push(eff.restriction);
    ov.knows[move.npc] = Object.fromEntries((eff?.learns || []).map(f => [f, { stance: 'knows', source: 'observed' }]));
    for (const f of eff?.learns || []) ov.heard.push({ id: f, from: move.npc });
  }
  if (move.type === 'request') ov.requests.push({ by: move.npc, to: move.to, action: move.action });
  if (move.type === 'ask') ov.asked.push(move.goal);
  return ov;
}

/** Σ salience × direction over unsatisfied dialogue goals. Null when a filter blocks the move. */
export function scoreMove(s, move) {
  const id = move.npc;
  const def = NPC_DEFS[id];
  const before = makeCtx(s, id);
  const after = makeCtx(s, id, overlayFor(s, move));
  let score = 0;
  for (const [gid, g] of Object.entries(def.goals || {})) {
    const via = g.via || 'dialogue';
    if (via === 'agenda') continue;
    if (via === 'filter') {
      if (evaluate(g.target, before) && !evaluate(g.target, after)) return null;
      continue;
    }
    const p0 = progress(g.target, before);
    if (p0 >= 1) continue;
    const p1 = progress(g.target, after);
    score += salience(s, id, gid) * Math.sign(p1 - p0);
  }
  if (move.type === 'ask' && move.goal) score += salience(s, id, move.goal);
  return score;
}

function rankMoves(s, moves) {
  const stale = m => Number(!!m.fact && (m.type === 'answer' || m.type === 'believe') && heardFrom(s, m.fact, m.npc));
  return moves
    .map((m, i) => ({ ...m, score: scoreMove(s, m), i }))
    .filter(m => m.score !== null)
    .sort((a, b) => b.score - a.score || Number(b.names) - Number(a.names) || stale(a) - stale(b)
      || CLASS_ORDER.indexOf(a.cls) - CLASS_ORDER.indexOf(b.cls) || a.i - b.i);
}

/** Force when the top three span more than one class among disclose, withhold, share, act. */
export function forceRule(ranked) {
  const top = ranked.slice(0, 3);
  const classes = new Set(top.map(m => m.cls).filter(c => FORCING.has(c)));
  const sameFact = top.every(m => m.cls === 'disclose' && m.fact === top[0].fact);
  if (classes.size > 1 && !sameFact) return { forced: true, passed: [top[0]] };
  return { forced: false, passed: top };
}

// ---------- initiative ----------

function questionMove(s, id, gid, g) {
  const about = g.question.about;
  const visible = s.vocab.includes(about);
  const publicToRole = entityDomains(about).some(d => (ROLE_DOMAINS[id] || []).includes(d));
  if (!visible && !publicToRole) return null;
  const parse = { kind: 'ask', relation: g.question.relation || 'about', subject: null, object: about, recipient: null, evidence: null, topic: null, open_slot: 'none', unfinished: '', open_content: '', confidence: 1, source: 'npc' };
  return { type: 'ask', npc: id, goal: gid, parse, about, cls: 'ask', names: false, introduces: visible ? null : about };
}

export function initiativeCandidates(s, id, visitKey) {
  const n = s.npcs[id];
  const def = NPC_DEFS[id];
  const out = [];
  const cooled = gid => (n.lastInitiative[gid] ?? -Infinity) + CONFIG.GOAL_COOLDOWN <= s.sentences;
  for (const [fid, r] of Object.entries(n.records)) {
    if (!FACTS[fid] || n.policies[fid] !== 'volunteer' || r.stance === 'unsure') continue;
    if (heardFrom(s, fid, id) || !factVisible(s, fid) || !cooled(`fact:${fid}`)) continue;
    out.push({ type: r.stance === 'knows' ? 'answer' : 'believe', npc: id, fact: fid, cls: factClass(fid), names: false, goal: `fact:${fid}`, base: 1 });
  }
  for (const [slug, pol] of Object.entries(n.policies)) {
    if (!DOCUMENTS[slug] || pol !== 'volunteer' || s.files.some(f => f.documentSlug === slug) || !cooled(`doc:${slug}`)) continue;
    out.push({ type: 'share', npc: id, doc: slug, cls: 'share', names: false, goal: `doc:${slug}`, base: 1 });
  }
  if (!n.pendingQuestion) {
    for (const [gid, g] of Object.entries(def.goals || {})) {
      if (!g.question || !cooled(gid) || n.askedVisit.includes(`${visitKey}:${gid}`)) continue;
      if (progress(g.target, makeCtx(s, id)) >= 1) continue;
      const q = questionMove(s, id, gid, g);
      if (q) out.push(q);
    }
  }
  return out;
}

/** One NPC turn: response first, then at most one initiative move. Logged for replay. */
export function npcTurn(s, id, parse, { shownDoc = null, visitKey = 'room', skipFacts = new Set() } = {}) {
  const ranked = rankMoves(s, responseCandidates(s, id, parse, { shownDoc }).filter(m => !(m.fact && skipFacts.has(m.fact))));
  const safe = ranked.length ? ranked : [{ ...workMove(s, id, null), score: 0 }];
  const { forced, passed } = forceRule(safe);
  const response = passed[0];
  const init = rankMoves(s, initiativeCandidates(s, id, visitKey).filter(m => !sameMove(m, response) && !(m.fact && skipFacts.has(m.fact))))
    .map(m => ({ ...m, score: m.score + (m.base || 0) }))
    .sort((a, b) => b.score - a.score || CLASS_ORDER.indexOf(a.cls) - CLASS_ORDER.indexOf(b.cls));
  const initPick = init.length && init[0].score > 0 ? forceRule(init) : null;
  return {
    candidates: safe.map(strip),
    response: strip(response),
    passed: passed.map(strip),
    forced,
    initiative: initPick ? strip(initPick.passed[0]) : null,
    initiativeForced: initPick?.forced || false,
  };
}

function strip(m) {
  const { i, base, ...rest } = m;
  return rest;
}

// ---------- applying moves (world side) ----------

export function interventionEffect(s, iid) {
  return s.pack.interventions[iid] || ENGINE_INTERVENTIONS[iid] || null;
}

/**
 * World-side effects: NPC knowledge, events, restrictions, requests, schedules.
 * Player-side delivery (heard rows, files, introductions) is lib/game.mjs.
 */
export function applyWorld(s, move) {
  const n = s.npcs[move.npc];
  const at = s.fuelSpent;
  if (move.type === 'act') {
    const eff = interventionEffect(s, move.intervention);
    if (!eff) return;
    if (move.intervention === 'join_virtually') s.interview = { on: true, by: 'join', seen: false };
    if (move.intervention === 'hold_release') {
      move.restriction = s.filedNamesJob ? 'hold_release:names_job_boundary' : 'hold_release:model_only';
      if (!s.world.restrictions.includes(move.restriction)) s.world.restrictions.push(move.restriction);
    }
    if (eff.restriction && !s.world.restrictions.includes(eff.restriction)) s.world.restrictions.push(eff.restriction);
    if (eff.event && !s.world.events.includes(eff.event)) s.world.events.push(eff.event);
    move.outcome = [...(eff.learns || [])];
    for (const f of eff.learns || []) {
      n.records[f] = { stance: 'knows', source: `observed:${eff.event}`, at };
      if (!n.policies[f]) n.policies[f] = 'volunteer';
    }
    if (eff.later) {
      s.world.scheduled.push({ atFuel: at + (CONFIG[eff.later.delay] ?? eff.later.delay), npc: move.npc, event: eff.later.event, learns: eff.later.learns, emits: eff.later.emits });
    }
  } else if (move.type === 'request') {
    s.world.requests.push({ by: move.npc, to: move.to, action: move.action, at });
    const eff = interventionEffect(s, move.action);
    if (eff?.event && !s.world.events.includes(eff.event)) s.world.events.push(eff.event);
  } else if (move.type === 'message' && move.to === 'nora') {
    const reply = s.pack.nora.replies[move.about];
    move.outcome = [];
    if (reply?.fact) {
      n.records[reply.fact] = { stance: 'believes', source: 'told:nora', at };
      move.outcome.push(reply.fact);
    }
    if (!s.world.events.includes(`${move.npc}_asked_nora`)) s.world.events.push(`${move.npc}_asked_nora`);
  } else if (move.type === 'ask') {
    if (!n.askedGoals.includes(move.goal)) n.askedGoals.push(move.goal);
    n.askedAt[move.goal] = s.sentences;
    n.pendingQuestion = { npc: move.npc, goal: move.goal, parse: move.parse, at };
  } else if (move.type === 'answer' || move.type === 'believe' || move.type === 'share') {
    // Testimony and shares change only the player side.
  }
}

/** Pack events due at this fuel index. */
export function runSchedule(s) {
  const due = s.world.scheduled.filter(x => x.atFuel <= s.fuelSpent);
  s.world.scheduled = s.world.scheduled.filter(x => x.atFuel > s.fuelSpent);
  const moves = [];
  for (const x of due) {
    const n = s.npcs[x.npc];
    if (!s.world.events.includes(x.event)) s.world.events.push(x.event);
    if (x.emits && !s.world.events.includes(x.emits)) s.world.events.push(x.emits);
    for (const f of x.learns || []) {
      n.records[f] = { stance: 'knows', source: `observed:${x.event}`, at: s.fuelSpent };
      if (!n.policies[f]) n.policies[f] = 'volunteer';
    }
    moves.push({ type: 'act', npc: x.npc, intervention: x.event, outcome: [...(x.learns || [])], cls: 'act', scheduled: true });
  }
  return moves;
}

/** Goals must not name oracle-only state the NPC does not hold (npcs.md). Used by tests. */
export function goalIds(id) {
  return Object.values(NPC_DEFS[id].goals || {}).flatMap(g => predicateIds(g.target));
}

// ---------- template phrasing (headless, demo, and the fallback) ----------

/** Texture rows are author notes (often third person). Dialogue uses agenda work lines or glue.work. */
function textureDialogue(s, npc, fid) {
  const def = NPC_DEFS[npc];
  const item = currentAgenda(s, npc);
  if (item?.texture?.includes(fid)) {
    const alt = item.work_alt;
    const primary = item.work;
    if (primary || alt) return (alt && s.sentences % 2 === 1 ? alt : primary) || primary || alt;
  }
  for (const ag of def?.agenda || []) {
    if (ag.texture?.includes(fid) && (ag.work || ag.work_alt)) {
      return (ag.work_alt && s.sentences % 2 === 1 ? ag.work_alt : ag.work) || ag.work || ag.work_alt;
    }
  }
  const glue = def?.glue;
  if (glue?.work || glue?.work_alt) {
    return (glue.work_alt && s.sentences % 2 === 1 ? glue.work_alt : glue.work) || glue.work || glue.work_alt;
  }
  return FACTS[fid]?.text || '';
}

export function templateText(s, move) {
  const name = id => CAST[id]?.name.split(' ')[0] || (id === 'nora' ? 'NORA' : id);
  const label = id => ENTITIES[id]?.label || id;
  const factLine = fid => {
    const f = FACTS[fid];
    if (!f) return '';
    return f.kind === 'texture' ? textureDialogue(s, move.npc, fid) : f.text;
  };
  switch (move.type) {
    case 'answer': return factLine(move.fact);
    case 'believe': return `As far as I know: ${factLine(move.fact)}`;
    case 'withhold': return move.reason;
    case 'deflect': return move.reason;
    case 'refer':
      if (move.line) return move.line;
      return `That’s ${name(move.to)}’s desk — ${CAST[move.to]?.role.toLowerCase() || 'their lane'}. Try ${name(move.to)}.`;
    case 'share': return `I’ve put ${DOCUMENTS[move.doc].docId} in your Lab Access.`;
    case 'ask': return askText(move);
    case 'request': return move.action === 'grant_record' ? 'I’m asking Justine for the grant record on 284.' : move.action === 'full_exec_284' ? 'I’m asking Pavel for the full EXEC-284 record.' : `I’m asking ${name(move.to)}.`;
    case 'message': return `I’ll ask NORA about ${label(move.about)}.`;
    case 'act': return actText(move);
    case 'work': return move.work || NPC_DEFS[move.npc]?.glue?.work || 'I’m at my desk. Ask about what I own today.';
    case 'glue': return move.text || '';
    default: return '';
  }
}

function askText(move) {
  const l = ENTITIES[move.about]?.label || move.about;
  if (move.parse.relation === 'authorized') return `Who did they tell you owns ${l}?`;
  if (move.parse.relation === 'did_use') return `Which service read ${l}? Do you have the job name?`;
  return `${l[0].toUpperCase()}${l.slice(1)}: what have you seen on it?`;
}

function actText(move) {
  const outs = (move.outcome || []).map(f => FACTS[f]?.text).filter(Boolean);
  if (outs.length) return outs.join(' ');
  if (move.intervention === 'join_virtually') return 'I can join on the Evaluation projector.';
  if (move.intervention === 'hold_release') return 'We hold the release.';
  return 'Done.';
}

export function voiceOf(id) {
  return NPC_DEFS[id]?.voice || null;
}

function parseDomains(parse) {
  return [...new Set(parseIds(parse).flatMap(id => entityDomains(id)))];
}

function dayPressure(s, id) {
  const def = NPC_DEFS[id];
  const late = s.act === 'decision' || band(s.minute) === 'late';
  if (!late) return false;
  return Object.values(def.goals || {}).some(g => g.source === 'day' && !evaluate(g.target, makeCtx(s, id)));
}

export function stanceOf(s, id, parse = null) {
  const item = currentAgenda(s, id);
  return pickStance(NPC_DEFS[id]?.glue, {
    domains: parse ? parseDomains(parse) : [],
    interruptible: item?.interruptible || 'yes',
    pressure: dayPressure(s, id),
  });
}

/** Non-fact social line. Null when glue is off, NORA, or no authored line. */
export function glueMove(s, id, slot, parse = null) {
  if (!glueEnabled(slot) || !NPC_DEFS[id]?.glue) return null;
  const stance = stanceOf(s, id, parse);
  const text = glueText(NPC_DEFS[id].glue, slot, stance);
  if (!text) return null;
  return { type: 'glue', npc: id, slot, stance, text, cls: 'texture', names: false };
}

export function midGlueMove(s, id, parse = null) {
  const rate = NPC_DEFS[id]?.glue?.midRate;
  if (!midGlueHits(s, id, rate)) return null;
  return glueMove(s, id, 'mid', parse);
}
