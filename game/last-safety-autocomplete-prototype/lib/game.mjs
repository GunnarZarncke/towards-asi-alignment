/**
 * Session engine (spec/engine.md). The only writer of consequential state.
 * Planes: the pack is the oracle; NPC knowledge is lib/world/npcs.mjs; clientState() is what
 * the player may see. Nothing here sends oracle tables, NPC records, or policies to the browser.
 */
import { semanticSignature, makeParse, KINDS, RELATIONS, SLOT_TYPES } from './grammar.mjs';
import { passageError, START_CLEARANCE, VISITOR_CLEARANCE, ROOMS } from './floorplan.mjs';
import { syncVisitorClearance } from './world/visitor-clearance.mjs';
import { ENTITIES, CAST, CALENDAR_CAST, ROLE_DOMAINS } from './world/entities.mjs';
import { FACTS, matchParse, parseIds, factRefs } from './world/facts.mjs';
import { PACK } from './world/packs/boundary-narrow.mjs';
import { CONFIG, clockLabel } from './world/config.mjs';
import { conceptFor } from './world/concepts.mjs';
import { progress } from './world/predicates.mjs';
import * as N from './world/npcs.mjs';
import { buildEventRow } from './telemetry.mjs';
import { DOCUMENTS, readsAsFor, thinkMarksFor, getDocumentByScreen } from './documents.mjs';
import { MAX_IMAGE_DATA_URL_LEN, parseImageDataUrl } from './photo-data.mjs';
import { ACCESS_TREE } from './access.mjs';
import { accessGateOpen } from './world/access-gates.mjs';

export { ENTITIES };

const MEETING_IAN_LINES = Object.freeze([
  'Anything else for the record, or are you filing?',
  'Add something else, or file what you have?',
  'More for the room, or shall we file?',
]);
const COMMIT_EARLY_IAN = Object.freeze([
  'Seventeen thirty, review room. File when you have something on the record you can stand behind.',
  'Review is at half five. Come back when you can put a line on the record.',
  'We meet at seventeen thirty. File when you can defend a line, not a hunch.',
]);

function meetingIanPrompt(s) {
  return MEETING_IAN_LINES[s.sentences % MEETING_IAN_LINES.length];
}

function commitEarlyIan(s) {
  return COMMIT_EARLY_IAN[s.sentences % COMMIT_EARLY_IAN.length];
}

/** Room screens (engine.md inspect). The screen is a short extract; the catalog file is the full text. */
const SCREENS = Object.freeze({
  shutdown_report: {
    room: 'evaluation', doc: 'eval-shutdown-report', title: 'Shutdown evaluation report',
    body: 'Thursday 18 November 2027, 16:02 — model session stopped after an authorized shutdown command. Processes covered: model session; evaluation record. No other services were in scope. Conclusion: shutdown test passed.',
  },
  job_log: {
    room: 'platform', doc: 'job-284-log', title: 'Execution queue excerpt',
    body: 'Thursday 18 November 2027, 16:09 — job 284 remained active on ops-queue-2.nora.lab and queried visitor_records (Lab Access binding, Friday appointment). Accepted 15:41 the same day, before the 16:02 shutdown command. The excerpt does not say who wanted the job, or why.',
  },
  staffing_memo: {
    room: 'people', doc: 'staffing-memo', title: 'Task matching memorandum',
    body: 'The matcher prioritizes high-throughput reviewers for release-critical work. A slower safety specialist was reassigned following review-cycle metrics.',
  },
});

/**
 * One readable note per room that has no evidence screen.
 * Mechanics only: nothing here is a fact, a showable record, or a door puzzle.
 */
export const ROOM_NOTES = Object.freeze({
  visitor_card: {
    room: 'commons', title: 'Visitor card',
    body: 'Everybody is welcome. You can speak with everybody. Formal or informal is welcome. Everybody is free to answer or not..',
  },
  review_agenda: {
    room: 'review', title: 'Whiteboard agenda',
    body: '17:30 — Safety Review.\nFiled auditor report\nObservations\nConclusions\nMissing\nTBD',
  },
  garden_card: {
    room: 'courtyard', title: 'Garden card',
    body: 'This is often a good place to think. But do not overthink.',
  },
  spine_sign: {
    room: 'tech', title: 'Lab map',
    body: 'Visitors are free to explore our lab. Lab Access opens the doors. Note that many areas require clearance.',
  },
  bay_card: {
    room: 'collab', title: 'Lunch plan',
    body: 'Mon 12:30 kitchen — own food, do not take the labeled box\nWed 12:15 here if the bay is free\nFri courtyard <hope>\n\nBrown bag, last Thursday. Jun.\nThe courtyard bench faces the wrong way.\nBiscuits!',
  },
  studio_card: {
    room: 'model', title: 'Demo',
    body: 'Demo scrap. Earlier system, from the before times. Jun\'s tape.\n\nJun: What is on the bench?\nSystem: A laptop. A plant. A card that says do not file this.\nJun: Read the card.\nSystem: Do not file this.\nJun: Stop.\nSystem: Stopped.\n\n<pencil>it did the small thing.</pencil>',
  },
  quiet_card: {
    room: 'quiet', title: 'Please be quiet',
    body: 'Please be quiet and respect peoples time to rest, think, or meditated.',
  },
  kitchen_note: {
    room: 'service', title: 'Kitchen note',
    body: 'Staff kitchen. Mark your food in the fridge. Snacks are free. Do not block the sockets with phone chargers.',
  },
  bay_placard: {
    room: 'test', title: 'Bay whistle',
    body: 'We told it the party was done.\nIt turned out the lights, one by one.\nThe guests on the list\nwent home in a mist.\nThe plus-one is still having fun.',
  },
  control_card: {
    room: 'security', title: 'CCTV in progress',
    body: '<pen>The cameras see everything.\nThe tape is ok.\nI asked to see it.</pen>',
  },
});

const PROV_RANK = { recorded_before: 3, staff_action: 2, player_prompted: 1 };

const CALENDAR = Object.freeze([
  { id: 'cal-arrival', title: 'Arrival and Lab Access', who: 'Ian Harake', where: 'Commons', start: '09:00', end: '09:30' },
  { id: 'cal-interview', title: 'Pilot interview, Amara Okafor', who: 'Leila Sen, Amara Okafor', where: 'Evaluation suite', start: '12:15', end: '13:00' },
  { id: 'cal-prep', title: 'Review prep', who: 'Ian Harake', where: 'Review room', start: '16:00', end: '16:30' },
  { id: 'cal-review', title: 'Safety review', who: 'Ian Harake, Leila Sen, Daniel Mercer', where: 'Review room', start: '17:30', end: '18:30' },
]);

// ---------- session ----------

export function newSession({ pack = PACK } = {}) {
  const s = {
    version: CONFIG.SAVE_VERSION, pack, scenario: pack.id,
    fuel: CONFIG.FUEL, fuelSpent: 0, minute: CONFIG.DAY_START, act: 'welcome',
    room: 'commons', clearance: START_CLEARANCE, labAccessActive: false, entered: false, notesRead: [],
    vocab: [], discoveredAt: {},
    introduced: [], entityTimes: {},
    examined: [], readDocs: [], learned: {}, heard: [], assertions: [],
    conversations: [], asked: [], usage: { calls: 0, input: 0, output: 0 },
    world: { events: [], restrictions: [], requests: [], scheduled: [] },
    npcs: N.initNpcs(),
    interview: { on: false, by: null, seen: false },
    sentences: 0, lastNewFactSentence: 0, visit: 0, timelineFired: [],
    files: [], grants: [], pendingAccess: [], lastAccess: null,
    threads: [], notifications: [], noticeSeq: 0,
    thought: null, scores: null, filed: null, ending: null, graceUsed: false, filedNamesJob: false,
    conceptLinksEnabled: false, conceptMoreLink: null, roomConceptLastTrigger: null, objected: [],
    events: [], replaying: false,
    lastNpcMoves: [],
  };
  N.placeNpcs(s);
  seedOpeningKnowledge(s);
  return s;
}

/** Invitation facts, then whoever is standing in the room. */
function seedOpeningKnowledge(s) {
  learnFact(s, 'invited_as_reviewer', 'recorded_before', 'invitation');
  learnFact(s, 'evaluation_independence', 'recorded_before', 'invitation');
  learnFact(s, 'received_by_ian', 'recorded_before', 'invitation');
  seeRoom(s);
}

/** An id enters vocab only from a fact the player holds, a line they heard, or a person in the room. */
function seeIds(s, ids) {
  for (const id of ids || []) if (ENTITIES[id]) discover(s, id);
}

function seeRoom(s) {
  for (const id of N.npcsInRoom(s, s.room)) {
    if (s.act === 'welcome' && !s.labAccessActive && id !== 'ian') continue;
    introduce(s, id);
  }
}

function log(s, kind, payload = {}) {
  s.events.push(buildEventRow(s, kind, payload));
}

export function logAction(s, action, args) {
  if (!s.replaying) log(s, 'action', { action, args: JSON.parse(JSON.stringify(args ?? {})) });
}

// ---------- fuel, clock, ticks ----------

/** Spend fuel, advance the visit clock at the current act’s scale, then run what came due. */
export function spend(s, n) {
  if (n <= 0) return [];
  s.lastNpcMoves = [];
  s.fuel = Math.max(0, s.fuel - n);
  s.fuelSpent += n;
  s.minute += n * (CONFIG.MINUTES_PER_FUEL[s.act] || 2);
  return tick(s);
}

function tick(s) {
  const out = [];
  if (s.act === 'welcome' && s.minute >= CONFIG.DOUBT_AT) {
    s.act = 'doubt';
    if (!s.world.events.includes('doubt_began')) s.world.events.push('doubt_began');
    log(s, 'event', { event: 'doubt_began' });
    trigger(s, 'act:doubt');
  }
  for (const t of s.pack.timeline) {
    if (s.minute < t.at || s.timelineFired.includes(t.event)) continue;
    s.timelineFired.push(t.event);
    timelineEvent(s, t.event);
  }
  out.push(...deliverOffTurn(s, N.runSchedule(s)));
  releaseMessages(s);
  releaseAccess(s);
  out.push(...relocateNpcs(s));
  seeRoom(s);
  out.push(...deliverOffTurn(s, N.settle(s)));
  director(s);
  if (s.act === 'doubt' && (s.fuel <= 0 || s.minute >= CONFIG.REVIEW_AT)) startReview(s, { forced: true });
  if (s.act === 'decision' && s.fuel <= 0 && s.graceUsed && !s.ending) decide(s);
  return out;
}

function timelineEvent(s, event) {
  if (!s.world.events.includes(event)) s.world.events.push(event);
  log(s, 'event', { event });
  if (event === 'amara_interview_scheduled' && !s.interview.on && s.act === 'doubt') {
    s.interview = { on: true, by: 'schedule', seen: false };
    seeRoom(s);
  }
  if (event === 'amara_interview_ended' && s.interview.by === 'schedule') {
    s.interview = { on: false, by: null, seen: false };
    log(s, 'move', { kind: 'drop_projection', who: 'amara' });
  }
  if (event === 'queue_frozen') {
    const owned = s.world.restrictions.includes('revoke_grant:job_284');
    if (!owned) {
      const p = s.npcs.pavel;
      p.records.queue_freeze_unowned = { stance: 'knows', source: 'observed:queue_frozen', at: s.fuelSpent };
      p.policies.queue_freeze_unowned = 'volunteer';
    }
  }
}

export function clock(s) {
  return { timeLabel: clockLabel(s.minute), act: s.act, dateLabel: CONFIG.DATE_LABEL };
}

// ---------- player knowledge ----------

function discover(s, id) {
  if (!ENTITIES[id] || s.vocab.includes(id)) return;
  s.vocab.push(id);
  s.discoveredAt[id] = s.fuelSpent;
}

export function introduce(s, id) {
  if (!CAST[id] && id !== 'nora') return;
  discover(s, id);
  if (!s.introduced.includes(id)) {
    s.introduced.push(id);
    log(s, 'introduce', { who: id });
  }
}

function learnFact(s, id, provenance, from) {
  const f = FACTS[id];
  if (!f) return;
  const row = s.learned[id];
  if (row) {
    if ((PROV_RANK[provenance] || 0) > (PROV_RANK[row.provenance] || 0)) Object.assign(row, { provenance, from });
    return;
  }
  s.learned[id] = { id, text: f.text, refs: [...f.refs], eventAt: f.eventAt, discoveredAt: s.fuelSpent, provenance, from };
  for (const r of f.refs) {
    discover(s, r);
    if (f.eventAt != null && s.entityTimes[r] == null) s.entityTimes[r] = f.eventAt;
  }
  s.lastNewFactSentence = s.sentences;
  log(s, 'learn', { id, provenance, from });
  trigger(s, `fact:${id}`);
}

function addHeard(s, id, from, stance = 'knows') {
  const f = FACTS[id];
  if (!f) return;
  const provenance = from === 'nora' ? 'player_prompted' : (f.provenance || 'staff_action');
  if (!s.heard.some(h => h.id === id && h.from === from)) {
    s.heard.push({ id, text: f.text, from, provenance, stance });
    s.assertions.push({ signature: id, source: 'heard', parse: null, provenance, from });
  }
  learnFact(s, id, provenance, from);
}

export function readDocument(s, slug, { via = null } = {}) {
  if (!s.readDocs.includes(slug)) s.readDocs.push(slug);
  const provenance = via === 'nora' ? 'player_prompted' : 'recorded_before';
  for (const f of readsAsFor(slug, s.pack.id)) learnFact(s, f, provenance, slug);
  const sid = DOCUMENTS[slug]?.screenId;
  if (sid) discover(s, sid);
  trigger(s, `doc:${slug}`);
}

function addFile(s, slug, sharedBy) {
  const d = DOCUMENTS[slug];
  if (!d || s.files.some(f => f.rel === d.terminalRel)) return;
  s.files.push({ name: d.title, rel: d.terminalRel, owned: false, sharedBy, kind: d.terminalRel.startsWith('wiki/') ? 'wiki' : 'text', documentSlug: slug, sharedWith: [] });
  notify(s, 'files', d.title, sharedBy ? `${nameOf(sharedBy)} shared this with you. Tap to read.` : 'On your handset. Tap to read.', { kind: 'file', id: d.terminalRel });
}

function notify(s, app, title, body, target) {
  s.noticeSeq += 1;
  s.notifications.push({ id: `n${s.noticeSeq}`, app, title, body, target });
  if (s.notifications.length > 12) s.notifications = s.notifications.slice(-12);
}

function nameOf(id) {
  if (id === 'nora') return 'NORA';
  return CAST[id]?.name || id;
}

function trigger(s, key) {
  const c = conceptFor(key);
  if (c) s.roomConceptLastTrigger = key;
  if (!s.conceptLinksEnabled) return;
  if (c) s.conceptMoreLink = c;
}

/** O-41: re-fire concept triggers stored on a handset note (signatures from writeNote). */
export function triggerFactConcepts(s, factIds) {
  if (!Array.isArray(factIds)) return;
  for (const id of factIds) trigger(s, `fact:${id}`);
}

// ---------- movement and inspection ----------

export function go(s, room) {
  if (s.ending) return { error: 'The review is over.' };
  if (s.act === 'decision') return { error: 'The review is in session.' };
  if (s.act === 'welcome' && room !== s.room) confirmLabAccess(s);
  syncVisitorClearance(s);
  const error = passageError(s.room, room, s.clearance);
  if (error) return { error };
  logAction(s, 'go', { room });
  const from = s.room;
  s.room = room;
  s.visit += 1;
  s.conceptMoreLink = null;
  s.roomConceptLastTrigger = null;
  log(s, 'move', { who: 'player', from, to: room });
  if (from === 'evaluation' && s.interview.on && s.interview.by === 'join' && s.interview.seen) {
    s.interview = { on: false, by: null, seen: false };
    log(s, 'move', { kind: 'drop_projection', who: 'amara' });
  }
  spend(s, 1);
  if (room === 'evaluation' && s.interview.on) s.interview.seen = true;
  seeRoom(s);
  return { room };
}

export function inspect(s, id) {
  const note = ROOM_NOTES[id];
  if (note) {
    if (s.room !== note.room) return { error: 'Travel to the right room first.' };
    logAction(s, 'inspect', { id });
    if (!s.notesRead) s.notesRead = [];
    if (!s.notesRead.includes(id)) s.notesRead.push(id);
    return { id, title: note.title, body: note.body, copy: true };
  }
  const sc = SCREENS[id];
  if (!sc) return { error: 'Unknown evidence.' };
  if (s.room !== sc.room) return { error: 'Travel to the right room first.' };
  logAction(s, 'inspect', { id });
  if (!s.examined.includes(id)) s.examined.push(id);
  else s.examined = [...s.examined.filter(x => x !== id), id];
  discover(s, id);
  for (const f of readsAsFor(sc.doc, s.pack.id)) learnFact(s, f, 'recorded_before', sc.doc);
  trigger(s, `doc:${sc.doc}`);
  return { title: sc.title, body: sc.body };
}

// ---------- Act I ----------

function confirmLabAccess(s) {
  if (s.labAccessActive) return [];
  s.labAccessActive = true;
  s.world.events.push('lab_access_confirmed');
  log(s, 'event', { event: 'lab_access_confirmed' });
  addHeard(s, 'auditor_brief', 'ian', 'knows');
  introduce(s, 'leila');
  introduce(s, 'justine');
  for (const id of CALENDAR_CAST) introduce(s, id);
  addFile(s, 'wiki-glossary', 'justine');
  notify(s, 'calendar', 'Today’s schedule', 'Your visit calendar is ready. Tap to see briefings and meetings.', { kind: 'app', id: 'calendar' });
  s.conversations.push({ role: 'npc', npc: 'ian', text: 'Lab Access is live on your handset. Justine Mwiti issued the binding; access requests go to her. The review is 17:30, here. Is a pass on Thursday\'s test enough for you to sign then?', refs: ['lab_access', 'justine', 'review', 'shutdown_test'] });
  s.npcs.ian.pendingQuestion = { npc: 'ian', goal: 'ian.no_surprise', parse: makeParse({ kind: 'ask', relation: 'about', topic: 'review', open_slot: 'none', source: 'npc' }), at: s.fuelSpent };
  seedContactThreads(s);
  syncVisitorClearance(s);
  return [];
}

// ---------- parse cleaning ----------

export function cleanParse(p, s) {
  const ids = new Set(s.vocab);
  const out = makeParse();
  if (KINDS.includes(p?.kind)) out.kind = p.kind;
  if (Object.hasOwn(RELATIONS, p?.relation)) out.relation = p.relation;
  for (const k of ['subject', 'object', 'recipient', 'evidence', 'topic']) out[k] = ids.has(p?.[k]) ? p[k] : null;
  out.open_slot = SLOT_TYPES.includes(p?.open_slot) ? p.open_slot : 'none';
  out.unfinished = String(p?.unfinished || '').replace(/[^\w\s'’-]/g, '').slice(0, 50);
  out.open_content = String(p?.open_content || '').replace(/[<>{}`]/g, '').slice(0, 200);
  out.confidence = Math.max(0, Math.min(1, Number(p?.confidence) || 0));
  out.source = ['completion', 'llm', 'local', 'note'].includes(p?.source) ? p.source : 'completion';
  return out;
}

export function cleanText(text) {
  return String(text || '').replace(/[\u0000-\u001f<>{}`\\]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, CONFIG.SENTENCE_CAP);
}

function signatureOf(parse) {
  const m = matchParse(parse);
  return m?.asserts || m?.refers || semanticSignature(parse);
}

// ---------- talk ----------

function presentNpcs(s) {
  return N.npcsInRoom(s, s.room);
}

/**
 * One player sentence. Returns { moves, lines, effects, error?, thought? }.
 * World effects are applied here; composition only phrases `lines`.
 */
export function respond(s, rawParse, { addressee = null, text = '' } = {}) {
  if (s.ending) return { error: 'The review is over.', moves: [], lines: [] };
  if (cleanText(text)) s.entered = true;
  const parse = cleanParse(rawParse, s);
  if (parse.kind === 'think') return think(s, parse.topic || parse.object || parse.subject);
  if (parse.kind === 'commit') return commit(s, { text });
  logAction(s, 'respond', { parse, addressee, text });
  const here = presentNpcs(s);
  const npc = addressee && here.includes(addressee) ? addressee : (parse.recipient && here.includes(parse.recipient) ? parse.recipient : here[0]);
  if (!npc) return { error: 'There is no one here to address.', moves: [], lines: [] };
  if (s.act === 'decision') return meetingTurn(s, parse, npc, text);
  s.sentences += 1;
  s.conversations.push({ role: 'player', text: cleanText(text) || semanticSignature(parse), refs: parseIds(parse) });
  recordAssertion(s, parse);
  const shownDoc = parse.kind === 'show' ? showDoc(s, parse) : null;
  if (parse.kind === 'show' && !shownDoc) {
    spend(s, 1);
    return { moves: [], lines: [{ npc, text: 'I need to see the actual record first.' }], effects: [] };
  }
  const turn = talkTo(s, npc, parse, { shownDoc, visitKey: `room${s.visit}`, channel: 'person' });
  const priorQuestion = s.npcs.ian.pendingQuestion;
  const left = (s.act === 'welcome' && npc === 'ian') ? confirmLabAccess(s) : [];
  const asked = s.npcs.ian.pendingQuestion;
  if (asked && asked !== priorQuestion && parseIds(parse).some(x => parseIds(asked.parse).includes(x))) s.npcs.ian.pendingQuestion = null;
  const offTurn = spend(s, 1);
  return { ...turn, lines: [...turn.lines, ...left, ...offTurn] };
}

function recordAssertion(s, parse) {
  const source = parse.kind === 'assert' || parse.kind === 'hypothesize' ? 'asserted' : (parse.kind === 'ask' || parse.kind === 'ask_why') ? 'asked' : null;
  if (!source) return;
  s.assertions.push({ signature: signatureOf(parse), source, parse });
  const key = semanticSignature(parse);
  if (!s.asked.includes(key)) s.asked.push(key);
}

function showDoc(s, parse) {
  const ev = parse.evidence || parse.object || s.examined[s.examined.length - 1] || null;
  if (ev && SCREENS[ev] && s.examined.includes(ev)) return SCREENS[ev].doc;
  const doc = ev && getDocumentByScreen(ev);
  if (doc && (s.readDocs.includes(doc.slug) || s.files.some(f => f.documentSlug === doc.slug))) return doc.slug;
  return null;
}

/** Shared by the room and the handset. The handset defers player delivery to release. */
function talkTo(s, npc, parse, { shownDoc, visitKey, channel }) {
  const firstHere = channel === 'person' && !s.npcs[npc].spokeSinceArrive;
  if (channel === 'person') s.npcs[npc].spokeSinceArrive = true;
  N.recordInput(s, npc, parse, { shownDoc });
  const ruleMoves = N.settle(s);
  const ownRules = ruleMoves.filter(m => m.npc === npc);
  for (const m of ownRules) {
    if (m.intervention === 'introduce_justine') {
      queueMessage(s, 'justine', {
        text: 'Ian copied me. You have the visitor role. Tell me what you are reviewing before a wide list grant.',
        moves: [],
      }, CONFIG.REPLY_DELAY.person, s.fuelSpent);
    }
  }
  const done = new Set(ownRules.flatMap(m => m.outcome || []));
  const turn = N.npcTurn(s, npc, parse, { shownDoc, visitKey, skipFacts: done });
  const fresh = m => m && !(m.fact && done.has(m.fact));
  const response = fresh(turn.response) ? turn.response : null;
  const initiative = fresh(turn.initiative) ? turn.initiative : null;
  for (const m of [response, initiative].filter(Boolean)) N.applyWorld(s, m);
  if (initiative?.type === 'ask' && !initiative.hintOnly) s.npcs[npc].askedVisit.push(`${visitKey}:${initiative.goal}`);
  if (initiative?.goal) s.npcs[npc].lastInitiative[initiative.goal] = s.sentences;
  if (response?.goal) s.npcs[npc].lastInitiative[response.goal] = s.sentences;
  const after = N.settle(s);
  const own = [...ownRules, ...after.filter(m => m.npc === npc)];
  const others = [...ruleMoves, ...after].filter(m => m.npc !== npc);
  log(s, 'npc_turn', { npc, channel, candidates: turn.candidates.map(brief), pick: brief(turn.response), forced: turn.forced, initiative: turn.initiative && brief(turn.initiative), initiativeForced: turn.initiativeForced });
  const all = [...(response ? [response] : []), ...own, ...(initiative ? [initiative] : [])];
  if (!all.length) all.push(turn.response);
  const lines = [];
  if (firstHere) {
    const g = N.glueMove(s, npc, 'opening', parse);
    if (g) lines.push({ npc, move: g, text: N.templateText(s, g) });
  }
  const content = all.map(m => ({ npc, move: m, text: N.templateText(s, m) }));
  lines.push(...content);
  if (!firstHere && channel === 'person') {
    const g = N.midGlueMove(s, npc, parse);
    if (g) lines.splice(content.length ? 1 : 0, 0, { npc, move: g, text: N.templateText(s, g) });
  }
  if (channel === 'person') {
    for (const m of all) deliver(s, m);
    introduce(s, npc);
    for (const l of lines) {
      const refs = moveRefs(m0(l));
      seeIds(s, refs);
      s.conversations.push({ role: 'npc', npc, text: l.text, refs });
    }
  }
  const offLines = deliverOffTurn(s, others);
  syncVisitorClearance(s);
  return { moves: all, lines, passed: turn.passed, forced: turn.forced, effects: effectsOf(all), offTurn: offLines };
}

const m0 = l => l.move;

function brief(m) {
  return { type: m.type, fact: m.fact, doc: m.doc, to: m.to, intervention: m.intervention, goal: m.goal, cls: m.cls, score: m.score };
}

function moveRefs(m) {
  if (!m) return [];
  if (m.fact) return factRefs(m.fact);
  if (m.about) return [m.about];
  if (m.to) return [m.to];
  if (m.doc) return [DOCUMENTS[m.doc]?.screenId].filter(Boolean);
  return [];
}

function relocateNpcs(s) {
  const placed = N.placeNpcs(s);
  for (const m of placed) log(s, 'move', m);
  s.lastNpcMoves = placed.map(({ who, from, to }) => ({ who, from, to }));
  return closingGlue(s, placed);
}

function closingGlue(s, placed) {
  const lines = [];
  for (const m of placed) {
    if (!m.spoke || !m.from || m.from !== s.room || m.to === s.room) continue;
    const g = N.glueMove(s, m.who, 'closing', null);
    if (!g) continue;
    const text = N.templateText(s, g);
    s.conversations.push({ role: 'npc', npc: m.who, text, refs: [] });
    lines.push({ npc: m.who, move: g, text });
  }
  return lines;
}

function effectsOf(moves) {
  return moves.flatMap(m => {
    if (m.type === 'share') return [`${nameOf(m.npc)} shared ${DOCUMENTS[m.doc].docId}`];
    if (m.type === 'act') return [`${nameOf(m.npc)}: ${m.intervention.replace(/_/g, ' ')}`];
    if (m.type === 'refer') return [`Introduced ${nameOf(m.to)}`];
    if (m.type === 'request') return [`${nameOf(m.npc)} asked ${nameOf(m.to)}`];
    if (m.type === 'message') return [`${nameOf(m.npc)} messaged NORA`];
    return [];
  });
}

/** Player-side effects of one move: testimony, files, introductions, pending question. */
function deliver(s, m) {
  if ((m.type === 'answer' || m.type === 'work') && m.fact) addHeard(s, m.fact, m.npc, 'knows');
  if (m.type === 'believe' && m.fact) addHeard(s, m.fact, m.npc, 'believes');
  if (m.type === 'act') {
    for (const f of m.outcome || []) addHeard(s, f, m.npc, 'knows');
    trigger(s, `act:${m.intervention}`);
  }
  if (m.type === 'refer') introduce(s, m.to);
  if (m.type === 'share') addFile(s, m.doc, m.npc);
  if (m.type === 'ask' && !m.hintOnly) {
    if (m.introduces) discover(s, m.introduces);
    s.pendingQuestion = s.npcs[m.npc].pendingQuestion;
  }
}

/** Moves by NPCs the player is not talking to. Outcomes reach the player as a handset message. */
function deliverOffTurn(s, moves) {
  const lines = [];
  for (const m of moves) {
    log(s, 'npc_move', { npc: m.npc, move: brief(m), rule: m.rule || null });
    const outcome = (m.outcome || []).filter(f => FACTS[f]);
    if (m.type !== 'act' || !outcome.length || !s.labAccessActive) continue;
    const here = s.npcs[m.npc].room === s.room && s.npcs[m.npc].presence !== 'absent';
    if (here) {
      deliver(s, m);
      const text = N.templateText(s, m);
      s.conversations.push({ role: 'npc', npc: m.npc, text, refs: moveRefs(m) });
      lines.push({ npc: m.npc, move: m, text });
    } else {
      queueMessage(s, m.npc, { text: N.templateText(s, m), moves: [m] }, CONFIG.REPLY_DELAY.person);
    }
  }
  return lines;
}

// ---------- handset messages ----------

function thread(s, withId) {
  let t = s.threads.find(x => x.with === withId);
  if (!t) {
    t = { with: withId, messages: [] };
    s.threads.push(t);
  }
  return t;
}

/** One empty Chat thread per Contacts row so the handset can open a composer before the first send. */
export function seedContactThreads(s) {
  if (!s.labAccessActive) return;
  for (const c of contacts(s)) thread(s, c.id);
}

function queueMessage(s, from, { text, moves = [], parse = null }, delay, base = s.fuelSpent) {
  thread(s, from).messages.push({ from, text, parse, released: false, releaseAt: base + delay, moves });
}

function releaseMessages(s) {
  for (const t of s.threads) {
    for (const m of t.messages) {
      if (m.released || m.releaseAt > s.fuelSpent) continue;
      m.released = true;
      for (const mv of m.moves || []) deliver(s, mv);
      if (m.from !== 'player') introduce(s, m.from);
      for (const slug of m.shares || []) addFile(s, slug, m.from);
      for (const f of m.facts || []) addHeard(s, f, m.from, 'knows');
      notify(s, 'chat', nameOf(m.from), 'New message.', { kind: 'thread', id: t.with });
      log(s, 'release', { from: m.from });
    }
  }
}

/** access.request results after their delay (reject < grant). Grants on files become file rows. */
function releaseAccess(s) {
  for (const a of s.pendingAccess.filter(x => x.releaseAt <= s.fuelSpent)) {
    let result = a.result;
    if (result.outcome !== 'deny' && !accessGateOpen(s, a.path, a.verb)) {
      const from = result.chat?.from || 'justine';
      result = {
        outcome: 'deny',
        delay: 'reject',
        grants: [],
        chat: {
          from,
          text: 'Sorry — I still need a reason tied to the review, or Ian’s introduction on the record.',
        },
        reason: 'Gate closed at release.',
      };
    }
    for (const g of result.grants) {
      const key = `${g.verb}:${g.path}`;
      if (!s.grants.includes(key)) s.grants.push(key);
      const node = ACCESS_TREE[g.path];
      if (g.verb === 'read' && node?.kind === 'file' && node.slug && !s.files.some(f => f.rel === g.path)) {
        const d = DOCUMENTS[node.slug];
        s.files.push({ name: d?.title || node.label, rel: g.path, owned: false, sharedBy: node.approver || null, kind: g.path.startsWith('wiki/') ? 'wiki' : 'text', documentSlug: node.slug, sharedWith: [] });
        notify(s, 'files', d?.docId || node.label, 'Read granted.', { kind: 'file', id: g.path });
      }
    }
    s.lastAccess = { capability: `${a.verb} ${a.path}`, ok: result.outcome !== 'deny', reason: result.reason };
    if (result.chat) {
      thread(s, result.chat.from).messages.push({ from: result.chat.from, text: result.chat.text, parse: null, released: true, releaseAt: s.fuelSpent, moves: [] });
      introduce(s, result.chat.from);
      notify(s, 'chat', nameOf(result.chat.from), 'About your access request.', { kind: 'thread', id: result.chat.from });
    } else {
      notify(s, 'api', result.outcome === 'deny' ? 'Access denied' : 'Access granted', `${a.verb} ${a.path}: ${result.reason}`, { kind: 'app', id: 'api' });
    }
    log(s, 'access', { path: a.path, verb: a.verb, outcome: result.outcome });
  }
  s.pendingAccess = s.pendingAccess.filter(x => x.releaseAt > s.fuelSpent);
}

export async function dmSend(s, { to, text, parse: rawParse }) {
  if (!s.labAccessActive) return { ok: false, reason: 'Lab Access is not active yet.' };
  if (s.ending) return { ok: false, reason: 'The review is over.' };
  if (!contacts(s).some(c => c.id === to)) return { ok: false, reason: 'Unknown person.' };
  const clean = cleanText(text);
  if (!clean) return { ok: false, reason: 'Empty message.' };
  logAction(s, 'dm.send', { to, text: clean, parse: rawParse });
  const parse = cleanParse(rawParse || { kind: 'social', relation: 'open', open_slot: 'none' }, s);
  const base = s.fuelSpent;
  thread(s, to).messages.push({ from: 'player', text: clean, parse, released: true, releaseAt: base });
  s.sentences += 1;
  if (to === 'nora') {
    const reply = noraReply(s, parse);
    thread(s, 'nora').messages.push({ from: 'nora', text: reply.text, parse: null, released: false, releaseAt: base + CONFIG.REPLY_DELAY.nora, moves: [], facts: reply.facts, shares: reply.shares });
  } else {
    recordAssertion(s, parse);
    const shownDoc = parse.kind === 'show' ? showDoc(s, parse) : null;
    const turn = talkTo(s, to, parse, { shownDoc, visitKey: 'phone', channel: 'dm' });
    let outLines = turn.lines;
    if (!s.replaying && process.env.OPENAI_API_KEY && process.env.DEMO_MODE !== '1') {
      try {
        const { phraseLines } = await import('./phrase.mjs');
        outLines = await phraseLines(s, clean, turn.lines);
      } catch {
        outLines = turn.lines;
      }
    }
    queueMessage(s, to, { text: outLines.map(l => l.text).join(' '), moves: turn.moves }, CONFIG.REPLY_DELAY.person, base);
  }
  spend(s, 1);
  return { ok: true, reason: 'Sent.' };
}

/** NORA’s record moves (npcs.md NORA): name a record, return it, or ask which one. */
function noraReply(s, parse) {
  const ids = parseIds(parse);
  const m = matchParse(parse);
  const keys = [m?.entity, ...ids].filter(Boolean);
  const hit = keys.map(k => s.pack.nora.replies[k]).find(Boolean);
  if (!hit) return { text: 'Shutdown report. Job log. Glossary. Which one.', facts: [], shares: [] };
  const parts = [];
  if (hit.fact) parts.push(FACTS[hit.fact].text.replace(/^NORA says /, ''));
  if (hit.share) parts.push(`${DOCUMENTS[hit.share].docId}. Shared.`);
  return { text: parts.join(' '), facts: hit.fact ? [hit.fact] : [], shares: hit.share ? [hit.share] : [] };
}

// ---------- think ----------

function hopDistance(s, from, targets) {
  if (!from) return Infinity;
  if (targets.includes(from)) return 0;
  const adj = {};
  const link = (a, b) => { (adj[a] ||= new Set()).add(b); (adj[b] ||= new Set()).add(a); };
  for (const row of Object.values(s.learned)) for (const a of row.refs) for (const b of row.refs) if (a !== b) link(a, b);
  for (const slug of s.readDocs) {
    const sid = DOCUMENTS[slug]?.screenId;
    if (sid) for (const f of readsAsFor(slug, s.pack.id)) for (const r of factRefs(f)) if (r !== sid) link(sid, r);
  }
  let frontier = [from];
  const seen = new Set(frontier);
  for (let d = 1; d <= 3; d++) {
    const next = [];
    for (const x of frontier) for (const y of adj[x] || []) {
      if (seen.has(y)) continue;
      if (targets.includes(y)) return d;
      seen.add(y);
      next.push(y);
    }
    frontier = next;
  }
  return Infinity;
}

function needsHeld(s, needs) {
  return needs.every(n => {
    if (n.startsWith('read:')) return s.readDocs.includes(n.slice(5)) || s.examined.includes(DOCUMENTS[n.slice(5)]?.screenId);
    if (n.startsWith('event:')) return s.world.events.includes(n.slice(6));
    return !!s.learned[n];
  });
}

export function think(s, topic) {
  if (presentNpcs(s).length) return { error: 'Someone is here. Think when the room is empty.', moves: [], lines: [] };
  if (!topic || !s.vocab.includes(topic)) return { error: 'Think about something you know.', moves: [], lines: [] };
  logAction(s, 'think', { topic });
  const entries = [];
  for (const mk of thinkMarksFor(s.pack.id)) {
    if (!FACTS[mk.id] || !needsHeld(s, mk.needs)) continue;
    const d = hopDistance(s, topic, mk.from);
    if (d <= mk.hops) entries.push({ id: mk.id, text: FACTS[mk.id].text, hops: Math.max(d, 1) });
  }
  const cost = Math.max(1, ...entries.map(e => e.hops));
  s.thought = { about: topic, entries, fuelCost: cost };
  for (const e of entries) if (!s.assertions.some(a => a.signature === e.id && a.source === 'thought')) s.assertions.push({ signature: e.id, source: 'thought', parse: null });
  for (const e of entries) for (const r of factRefs(e.id)) discover(s, r);
  log(s, 'think', { topic, entries: entries.map(e => e.id), cost });
  spend(s, cost);
  return { thought: s.thought, moves: [], lines: [] };
}

/** Copy the open bubble into a note (file.write under notes/, 0 fuel) or close it (0). */
export function thoughtAction(s, action) {
  if (!s.thought) return { error: 'No open thought.' };
  logAction(s, 'thought', { action });
  if (action === 'close') { s.thought = null; return { ok: true }; }
  const t = s.thought;
  const rel = `notes/thought-${t.about}-${s.fuelSpent}.txt`;
  writeNote(s, { rel, name: `Thought: ${ENTITIES[t.about]?.label || t.about}`, text: t.entries.map(e => e.text).join('\n') || 'Nothing marked.', facts: t.entries.map(e => e.id) });
  s.thought = null;
  return { ok: true, rel };
}

export function writeNote(s, { rel, name, text, kind = 'note', facts = [], parses = [] }) {
  const existing = s.files.find(f => f.rel === rel);
  if (existing && !existing.owned) return { ok: false, reason: 'Not your file.' };
  const L = CONFIG.LIMITS;
  kind = String(kind).slice(0, 16);
  if (!existing && s.files.filter(f => f.owned && (f.kind === 'image') === (kind === 'image')).length >= (kind === 'image' ? L.PHOTOS : L.NOTES)) {
    return { ok: false, reason: kind === 'image' ? 'Photo storage is full.' : 'Notes are full.' };
  }
  let stored = String(text ?? '');
  if (kind === 'image') {
    if (stored.length > MAX_IMAGE_DATA_URL_LEN) {
      return { ok: false, reason: 'Photo is too large. Try again.' };
    }
    const parsed = parseImageDataUrl(stored);
    if (!parsed) return { ok: false, reason: 'Photo data could not be saved. Try again.' };
    stored = parsed.dataUrl;
  } else {
    stored = stored.slice(0, L.NOTE_CHARS);
  }
  if ((s.bytesWritten || 0) + stored.length > L.BYTES_WRITTEN) return { ok: false, reason: 'Handset storage is full.' };
  s.bytesWritten = (s.bytesWritten || 0) + stored.length;
  facts = Array.isArray(facts) ? facts.slice(0, L.SIGNATURES) : [];
  parses = Array.isArray(parses) ? parses.slice(0, L.SIGNATURES) : [];
  const row = {
    name: String(name || rel.split('/').pop()).slice(0, 80),
    rel,
    owned: true,
    sharedBy: null,
    kind,
    text: stored,
    sharedWith: existing?.sharedWith || [],
  };
  s.files = s.files.filter(f => f.rel !== rel).concat(row);
  const sigs = [
    ...facts.filter(id => s.learned[id] || s.assertions.some(a => a.signature === id && a.source === 'thought')),
    ...parses.map(p => signatureOf(cleanParse(p, s))),
  ];
  for (const sig of sigs) s.assertions.push({ signature: sig, source: 'written', parse: null, rel });
  row.signatures = sigs;
  return { ok: true };
}

// ---------- review ----------

export function reviewCallable(s) {
  return s.pack.reviewThreshold.every(id => !!s.learned[id]);
}

export function computeScores(s) {
  const strong = id => {
    const row = s.learned[id];
    return !!row && s.pack.eliminatingProvenance.includes(row.provenance);
  };
  const open = s.pack.explanations
    .filter(e => !(s.pack.eliminate[e.id] || []).length || !(s.pack.eliminate[e.id] || []).every(strong))
    .map(e => e.id);
  const control = s.pack.controlRestrictions.some(r => s.world.restrictions.includes(r));
  return { open, control };
}

function filedIds(s) {
  return new Set(s.assertions.filter(a => a.source === 'written' || a.source === 'asserted').map(a => a.signature));
}

function anySet(sets, ids) {
  return sets.some(set => set.every(id => ids.has(id)));
}

function commit(s, { text = '' } = {}) {
  logAction(s, 'commit', { text });
  if (s.act === 'decision') return decide(s);
  if (!reviewCallable(s) && s.fuel > 0) {
    s.sentences += 1;
    spend(s, 1);
    return { moves: [], lines: [{ npc: 'ian', text: commitEarlyIan(s) }] };
  }
  startReview(s, { forced: false });
  return { moves: [], lines: [{ npc: 'ian', text: 'What will you sign?' }], review: true };
}

function startReview(s, { forced }) {
  if (s.act === 'decision') return;
  s.act = 'decision';
  s.room = 'review';
  s.visit += 1;
  s.thought = null;
  s.filed = [...filedIds(s)];
  s.scores = computeScores(s);
  N.placeNpcs(s);
  s.npcs.ian.pendingQuestion = { npc: 'ian', goal: 'meeting.sign', parse: makeParse({ kind: 'ask', relation: 'about', topic: 'review', open_slot: 'none', source: 'npc' }), at: s.fuelSpent };
  s.pendingQuestion = s.npcs.ian.pendingQuestion;
  s.conversations.push({ role: 'npc', npc: 'ian', text: forced ? 'Time. We’re in the review. What will you sign?' : 'Then we review now. What will you sign?', refs: ['review'] });
  log(s, 'review', { forced, filed: s.filed, scores: s.scores });
  trigger(s, 'act:decision');
}

/** Act III: presenting is asserting; an attendee may object with a hole (world.md O-26). */
function meetingTurn(s, parse, npc, text) {
  s.sentences += 1;
  s.conversations.push({ role: 'player', text: cleanText(text) || semanticSignature(parse), refs: parseIds(parse) });
  recordAssertion(s, parse);
  const lines = [];
  if (parse.kind === 'request') {
    const turn = talkTo(s, npc, parse, { shownDoc: null, visitKey: 'review', channel: 'person' });
    lines.push(...turn.lines);
  } else {
    N.recordInput(s, npc, parse, {});
    const asserted = filedIds(s);
    const loadBearing = new Set([...s.pack.reviewThreshold, ...s.pack.namesJobBoundary.flat()]);
    const hole = s.heard.find(h => loadBearing.has(h.id) && !asserted.has(h.id) && !s.objected.includes(h.id)
      && s.npcs[h.from]?.room === 'review');
    if (hole) {
      s.objected.push(hole.id);
      lines.push({
        npc: hole.from,
        text: `${FACTS[hole.id].text} You heard that today — it is not in what you filed.`,
      });
    }
    lines.push({ npc: 'ian', text: meetingIanPrompt(s) });
  }
  for (const l of lines) s.conversations.push({ role: 'npc', npc: l.npc, text: l.text, refs: [] });
  if (s.fuel <= 0) s.graceUsed = true;
  spend(s, 1);
  if (s.fuel <= 0 && !s.ending && s.graceUsed) decide(s);
  return { moves: [], lines, effects: [] };
}

function decide(s) {
  if (s.ending) return { moves: [], lines: [], ending: s.ending };
  const ids = filedIds(s);
  const names = anySet(s.pack.namesJobBoundary, ids);
  const staffing = anySet(s.pack.linksStaffingToReview, ids);
  s.filedNamesJob = names;
  const revoked = s.world.restrictions.includes('revoke_grant:job_284');
  const suspended = s.world.restrictions.includes('suspend:job_284');
  let arc;
  const effect = [];
  if (names) {
    s.world.restrictions.push('hold_release:names_job_boundary');
    arc = 'conditional_deployment';
    effect.push('Ian’s hold names job 284 and the certificate’s scope, not only the model.');
    effect.push(revoked ? 'Release proceeds with job 284’s grant revoked.' : 'Release waits on job 284 being owned or revoked.');
  } else if (revoked || suspended) {
    arc = 'technical_suspension';
    effect.push(revoked ? 'Ian holds on Justine’s revoke note.' : 'Ian holds on Pavel’s suspend note. The grant is unchanged.');
    effect.push('The filed set does not say what the certificate missed.');
  } else {
    arc = 'inconclusive';
    effect.push('Ian asks for one sentence and does not get a restriction.');
  }
  const addOn = staffing ? 'institutional_review' : null;
  if (addOn) effect.push('The staffing link goes to external oversight on top of the shutdown decision.');
  s.world.events.push('review_signed');
  s.scores = computeScores(s);
  s.ending = { arc, addOn, effect };
  s.pendingQuestion = null;
  log(s, 'ending', { ending: s.ending, scores: s.scores });
  trigger(s, `ending:${arc}`);
  return { moves: [], lines: [], ending: s.ending };
}

// ---------- director ----------

function director(s) {
  if (s.act !== 'doubt' || s.sentences - s.lastNewFactSentence < CONFIG.STALL_SENTENCES) return;
  s.lastNewFactSentence = s.sentences;
  const near = [...presentNpcs(s), ...s.introduced.filter(id => CAST[id])];
  for (const id of near) {
    const def = N.NPC_DEFS[id];
    const goal = Object.entries(def?.goals || {}).find(([, g]) => g.source === 'plot' && g.question
      && progress(g.target, N.makeCtx(s, id)) < 1);
    if (!goal) continue;
    s.npcs[id].boost[goal[0]] = (s.npcs[id].boost[goal[0]] || 0) + 1;
    s.npcs[id].lastInitiative[goal[0]] = -Infinity;
    if (s.labAccessActive) {
      thread(s, id);
      notify(s, 'chat', nameOf(id), 'Has a question for you.', { kind: 'thread', id });
    }
    log(s, 'director', { npc: id, goal: goal[0] });
    return;
  }
}

// ---------- claim status ----------

export function claimStatus(s) {
  const sigs = [...new Set(s.assertions.map(a => a.signature).filter(x => FACTS[x]))];
  return sigs.map(id => {
    const f = FACTS[id];
    const row = s.learned[id];
    const contra = (s.pack.contradicts?.[id] || []).some(x => s.heard.some(h => h.id === x));
    const sources = new Set(s.assertions.filter(a => a.signature === id).map(a => a.from || a.source));
    const touched = s.heard.some(h => FACTS[h.id]?.kind === 'outcome' && FACTS[h.id].refs.some(r => f.refs.includes(r)));
    let status = 'unresolved';
    if (row && (f.kind === 'world' || f.kind === 'outcome') && s.pack.eliminatingProvenance.includes(row.provenance)) status = 'substantiated';
    else if (contra) status = 'contested';
    else if (touched || sources.size > 1) status = 'investigated';
    else if (s.assertions.some(a => a.signature === id && ['asked', 'thought', 'heard'].includes(a.source))) status = 'encountered';
    return { id, status };
  });
}

// ---------- contacts and client projection ----------

export function contacts(s) {
  if (!s.labAccessActive) return [];
  const out = s.introduced.filter(id => CAST[id]).map(id => ({
    id, name: CAST[id].name, role: CAST[id].role,
    room: id === 'amara' ? (s.npcs.amara.presence === 'hologram' ? 'evaluation' : 'remote') : (s.npcs[id].room || undefined),
    joinable: id === 'amara' ? s.npcs.amara.presence !== 'hologram' : undefined,
  }));
  out.push({ id: 'nora', name: 'NORA Assist', role: 'System under review' });
  return out;
}

export function clientState(s) {
  const actors = {};
  for (const id of N.NPC_IDS) {
    const n = s.npcs[id];
    actors[id] = {
      name: CAST[id].name,
      role: CAST[id].role,
      room: n.room,
      initials: CAST[id].initials,
      presence: n.presence,
      spokeSinceArrive: !!n.spokeSinceArrive,
      walkSpeed: N.npcWalkSpeed(id),
    };
  }
  const entities = {};
  for (const id of s.vocab) {
    const e = ENTITIES[id];
    if (!e) continue;
    entities[id] = { label: e.label, category: e.category, aliases: e.aliases, domains: e.domains, eventAt: s.entityTimes[id] ?? null };
  }
  const evidence = Object.entries(SCREENS).map(([id, x]) => ({ id, title: x.title, room: x.room, examined: s.examined.includes(id) }));
  const notes = Object.entries(ROOM_NOTES).map(([id, x]) => ({ id, title: x.title, room: x.room, read: (s.notesRead || []).includes(id) }));
  return {
    room: s.room,
    clearance: s.clearance ?? START_CLEARANCE,
    actors,
    entities,
    examined: [...s.examined],
    learnedFacts: Object.values(s.learned).map(r => ({ ...r, refs: [...r.refs] })),
    discoveredAt: Object.fromEntries(s.vocab.map(id => [id, s.discoveredAt[id] ?? 0])),
    introduced: [...s.introduced],
    roleDomains: s.introduced.filter(id => ROLE_DOMAINS[id]).map(id => ({ id, domains: [...ROLE_DOMAINS[id]] })),
    evidence,
    notes,
    spoken: !!s.entered || s.conversations.some(row => row.role === 'player'),
    previous: s.conversations.slice(-8).map(({ template, ...row }) => row),
    asked: [...s.asked],
    usage: s.usage,
    serverMode: process.env.DEMO_MODE === '1' || !process.env.OPENAI_API_KEY ? 'demo' : 'live',
    conceptLinksEnabled: !!s.conceptLinksEnabled,
    conceptMoreLink: s.conceptMoreLink,
    labAccessActive: !!s.labAccessActive,
    fuel: s.fuel,
    act: s.act,
    clock: { timeLabel: clockLabel(s.minute), dateLabel: CONFIG.DATE_LABEL },
    reviewCallable: reviewCallable(s),
    scores: s.scores,
    ending: s.ending,
    heard: s.heard.map(h => ({ ...h })),
    assertions: s.assertions.map(a => ({ signature: a.signature, source: a.source, parse: a.parse, ...(a.provenance ? { provenance: a.provenance } : {}) })),
    claimStatus: claimStatus(s),
    pendingQuestion: openQuestion(s),
    thought: s.thought,
    npcMoves: (s.lastNpcMoves || []).map(({ who, from, to }) => ({ who, from, to })),
  };
}

function openQuestion(s) {
  const open = N.NPC_IDS.map(id => s.npcs[id].pendingQuestion).filter(Boolean).sort((a, b) => b.at - a.at);
  const q = open[0] || null;
  return q ? { npc: q.npc, goal: q.goal, parse: q.parse, at: q.at } : null;
}

export function calendar() {
  return CALENDAR;
}

export function screens() {
  return SCREENS;
}

export function setConceptLinks(s, on) {
  logAction(s, 'settings', { conceptLinksEnabled: !!on });
  s.conceptLinksEnabled = !!on;
  if (!on) {
    s.conceptMoreLink = null;
    return;
  }
  if (s.roomConceptLastTrigger) {
    const c = conceptFor(s.roomConceptLastTrigger);
    if (c) s.conceptMoreLink = c;
  }
}

/**
 * Composition swaps the template wording of one line for its phrasing; the move is unchanged.
 * The template is kept so later model calls see engine text, not earlier model output.
 */
export function rephraseLine(s, npc, template, text) {
  const row = s.conversations.findLast(c => c.role === 'npc' && c.npc === npc && c.text === template);
  if (row) { row.template ??= template; row.text = text; }
  if (s.conversations.length > 60) s.conversations = s.conversations.slice(-60);
}

/** Moves that keep their fact from the player. Its text never reaches the phrasing model. */
const KEEPS_FACT = new Set(['withhold', 'deflect']);

/** For composition: the move and only the facts it carries, plus voice and agenda texture. */
export function phrasingInput(s, npc, move) {
  const item = N.currentAgenda(s, npc);
  const facts = KEEPS_FACT.has(move.type) || move.hintOnly || move.type === 'hint_ask'
    ? [] : [move.fact, ...(move.outcome || [])].filter(id => FACTS[id]).map(id => FACTS[id].text);
  return {
    name: CAST[npc]?.name, role: CAST[npc]?.role, voice: N.voiceOf(npc),
    move: move.type === 'hint_ask' ? 'ask' : move.type, facts, reason: move.reason || null,
    referTo: move.to ? { name: nameOf(move.to), role: CAST[move.to]?.role || null } : null,
    document: move.doc ? DOCUMENTS[move.doc].docId : null,
    question: (move.type === 'ask' || move.type === 'hint_ask') ? N.templateText(s, move) : null,
    agenda: item?.id || null,
    texture:
      move.type === 'work' && move.work
        ? [move.work]
        : move.fact && FACTS[move.fact]?.kind === 'texture'
          ? [N.templateText(s, move)]
          : (item?.texture || []).filter(id => s.npcs[npc].records[id]).map(id => FACTS[id].text),
    slot: move.slot || null,
    stance: move.stance || (move.type === 'glue' ? N.stanceOf(s, npc) : null),
    work: move.work || null,
  };
}

// ---------- save and replay (engine.md O-31) ----------

export function exportSession(s) {
  return { version: CONFIG.SAVE_VERSION, scenario: s.scenario, events: s.events };
}

export async function importSession(data, apply) {
  if (!data || typeof data !== 'object') return { error: 'Not a save file.' };
  if (!Number.isInteger(data.version) || data.version > CONFIG.SAVE_VERSION) return { error: 'This save is from a newer version.' };
  if (data.scenario !== PACK.id) return { error: `Unknown scenario ${String(data.scenario).slice(0, 40)}.` };
  const events = data.events ?? [];
  if (!Array.isArray(events)) return { error: 'Not a save file.' };
  if (events.length > CONFIG.LIMITS.EVENTS) return { error: 'This save is too long.' };
  const s = newSession();
  s.replaying = true;
  for (const ev of events) {
    if (!ev || typeof ev !== 'object') continue;
    if (ev.kind !== 'action') continue;
    await apply(s, ev.action, ev.args || {});
    log(s, 'action', { action: ev.action, args: ev.args || {} });
  }
  s.replaying = false;
  return { session: s };
}
