import { makeParse } from '../lib/grammar.mjs';
import { getCandidates, insertFragment, localPrefixParse } from '/grammar.js';
import { buildSceneView, mountScene } from './render/scene-view.mjs';
import { ROOM_META, VISITOR_CLEARANCE } from './render/rooms.mjs';
import { closeFloorplan, floorplanNotice, floorplanOpen, openFloorplan, syncFloorplan } from './render/floorplan-view.mjs';
import { encodePhotoCanvas } from './photo-export.mjs';

const $ = id => document.getElementById(id);
let state = null;
let parse = makeParse();
let parseText = '';
let trace = [];
let suggestions = [];
let visibleCount = 5;
let debounce = null;
let requestVersion = 0;
let activeRequest = null;
let lastAnchoredParse = null;
let lastNotice = '';
let cameraMode = 'play';
let actPreset = 'doubt';
let sceneOverlay = null;
let uiHarness = false;
let room3d = null;
let addressee = null;
let phoneOpen = false;
let phoneUnread = false;
const PHONE_COACH_KEY = 'lsr-phone-opened';
let phoneCoachDismissed = false;
try { phoneCoachDismissed = sessionStorage.getItem(PHONE_COACH_KEY) === '1'; } catch { /* private mode */ }
const MAP_COACH_KEY = 'lsr-map-opened';
let mapCoachDismissed = false;
try { mapCoachDismissed = sessionStorage.getItem(MAP_COACH_KEY) === '1'; } catch { /* private mode */ }
/** Learned-fact ids seen on the last render; used to detect newly learned facts for the notebook dialog. */
let learnedFactSnapshot = null;
let notebookQueue = [];
let notebookSkipped = new Set();
let notebookPromptFact = null;
let photoMode = false;
let photoView = { x: 0, y: 0, z: 1 };
const photoPointers = new Map();
let photoPinch0 = null;
const SAVE_KEY = 'lsr-save';
/** Debug panels (parser inspector, trace, usage, server mode) show only in test mode or the dev-ui harness. */
const testParam = new URLSearchParams(location.search).has('test');
let userScrollAt = 0;
let chatExpanded = false;
const narrowMq = matchMedia('(max-width: 720px)');
/** Transcript reveal after /api/respond: one sentence per second, smooth scroll. */
let transcriptAnimateOnRender = false;
let transcriptDisplayedCount = 0;
let transcriptRevealTimer = null;
let transcriptRevealActive = false;
const TRANSCRIPT_SENTENCE_MS = 1000;

function syncTranscriptChrome() {
  document.body.classList.toggle('transcript-collapsed', !chatExpanded);
  document.body.classList.toggle('transcript-expanded', narrowMq.matches && chatExpanded);
}

function collapseChat() {
  chatExpanded = false;
  if (document.activeElement === $('utterance')) $('utterance')?.blur();
  syncTranscriptChrome();
}

function expandChat(focusInput = true) {
  chatExpanded = true;
  syncTranscriptChrome();
  if (focusInput) $('utterance')?.focus({ preventScroll: true });
}

/** Keep the dock open and caret in the composer (after send, etc.). */
function focusComposer() {
  expandChat(false);
  $('utterance')?.focus({ preventScroll: true });
}

/** Send in flight — ignore dock focusout so disabling Send does not collapse the dock. */
let composerBusy = false;

const roomNames = Object.fromEntries(Object.entries(ROOM_META).map(([id, m]) => [id, m.title]));

async function api(route, payload = null) {
  const res = await fetch('/api/' + route, {
    method: payload === null ? 'GET' : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: payload === null ? undefined : JSON.stringify(payload),
  });
  let data;
  try {
    data = await res.json();
  } catch {
    throw Error('Server returned an invalid response');
  }
  if (!res.ok) throw Error(data.error || 'Request failed');
  return data;
}

function esc(t) {
  return String(t).replace(/[&<>"']/g, x => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[x]));
}

function presentIds() {
  return Object.entries(state.actors).filter(([, a]) => a.room === state.room && a.presence !== 'absent').map(([id]) => id);
}

function npcId() {
  const here = presentIds();
  if (here.includes(addressee)) return addressee;
  const asker = state.pendingQuestion?.npc;
  return here.includes(asker) ? asker : here[0];
}

function applySceneOverlayFromState() {
  if (state._devScene) {
    sceneOverlay = state._devScene;
    cameraMode = sceneOverlay.camera || cameraMode;
    actPreset = sceneOverlay.act || actPreset;
    uiHarness = true;
    delete state._devScene;
  }
}

function sceneOptions() {
  const base = sceneOverlay && sceneOverlay.roomId === state.room ? sceneOverlay : {};
  const act = uiHarness ? actPreset : state.act === 'welcome' || state.act === 'decision' ? state.act : 'doubt';
  return {
    act,
    camera: cameraMode,
    lightingPreset: act,
    annotations: base.annotations,
    cameraId: base.cameraId,
    timestamp: base.timestamp,
  };
}

function renderScenePanel() {
  const scene = buildSceneView(state, sceneOptions());
  $('roomTitle').textContent = scene.roomTitle;
  $('actLabel').textContent = scene.actLabel;
  $('sceneNote').textContent = room3d
    ? 'Click the floor to walk · click a person to speak to them · doors, records, and notes'
    : 'Tap hotspots — doors, records, notes, people';
  $('actSwitch').hidden = !uiHarness;
  for (const btn of document.querySelectorAll('[data-act]')) btn.classList.toggle('active', btn.dataset.act === actPreset);

  const handlers = {
    onGo: room => {
      collapseChat();
      move(room);
    },
    onInspect: id => {
      collapseChat();
      examine(id);
    },
    onTerminal: () => {
      if (uiHarness || !state.labAccessActive) return;
      setPhone(true);
    },
    onFocusActor: id => {
      if (id && state.actors[id]) addressee = id;
      renderNPC();
      renderSuggestions();
      expandChat(true);
    },
  };
  if (room3d) room3d.update(scene, handlers);
  else mountScene($('roomMount'), scene, handlers);
}

async function initRenderer() {
  try {
    const { RoomRenderer, webglAvailable } = await import('./render/three-scene.mjs');
    if (!webglAvailable()) throw Error('WebGL is not available in this browser');
    room3d = new RoomRenderer($('roomMount'));
    room3d.onFrame = followPlayer;
  } catch (err) {
    console.warn('[scene] 3D renderer unavailable, using CSS room:', err);
    lastNotice = `3D room unavailable (${err.message}). Run npm install in the game folder, or use a WebGL browser.`;
  }
}

/** On a viewport narrower than the room, keep the player near the middle unless the user just scrolled. */
function followPlayer() {
  if (photoMode) return;
  const m = $('roomMount');
  const max = m.scrollWidth - m.clientWidth;
  if (max <= 1 || performance.now() - userScrollAt < 2500) return;
  const p = room3d.playerScreen();
  if (!p) return;
  const target = Math.max(0, Math.min(max, p.x - m.clientWidth / 2));
  const d = target - m.scrollLeft;
  if (Math.abs(d) > 1) m.scrollLeft += d * 0.12;
}

function setMenu(open) {
  $('menu').hidden = !open;
  $('menuBtn').setAttribute('aria-expanded', open ? 'true' : 'false');
}

function mapView() {
  return { roomId: state.room, clearance: state.clearance ?? VISITOR_CLEARANCE };
}

function mapHandlers() {
  return { onGo: room => move(room), onClose: closeMap };
}

function closeMap() {
  closeFloorplan();
  renderMapButton();
}

function labMapRead() {
  return (state?.notes || []).some(n => n.id === 'spine_sign' && n.read);
}

function dismissMapCoach() {
  mapCoachDismissed = true;
  try { sessionStorage.setItem(MAP_COACH_KEY, '1'); } catch { /* private mode */ }
}

function clearMapCoach() {
  mapCoachDismissed = false;
  try { sessionStorage.removeItem(MAP_COACH_KEY); } catch { /* private mode */ }
}

function renderMapButton() {
  const btn = $('modeMap');
  const open = floorplanOpen();
  const show = labMapRead();
  btn.hidden = !show;
  btn.classList.toggle('blink', show && !mapCoachDismissed && !open);
  btn.classList.toggle('active', open);
  btn.setAttribute('aria-pressed', open ? 'true' : 'false');
}

function factInNotebook(factId) {
  return (state?.assertions || []).some(a => a.signature === factId && a.source === 'written');
}

function factLabel(id) {
  return id.replaceAll('_', ' ');
}

function resetNotebookTracking() {
  learnedFactSnapshot = null;
  notebookQueue = [];
  notebookSkipped = new Set();
  notebookPromptFact = null;
  if ($('notebookPrompt')) $('notebookPrompt').hidden = true;
}

function trackNewLearnedFacts() {
  if (!state) return;
  const facts = state.learnedFacts || [];
  const ids = new Set(facts.map(f => f.id));
  if (learnedFactSnapshot === null) {
    learnedFactSnapshot = ids;
    return;
  }
  const newly = facts.filter(f => !learnedFactSnapshot.has(f.id));
  learnedFactSnapshot = ids;
  for (const f of newly) {
    if (factInNotebook(f.id) || notebookSkipped.has(f.id)) continue;
    if (!notebookQueue.some(q => q.id === f.id) && notebookPromptFact?.id !== f.id) notebookQueue.push(f);
  }
  showNextNotebookPrompt();
}

function renderNotebookPrompt() {
  const el = $('notebookPrompt');
  if (!el) return;
  if (!notebookPromptFact) {
    el.hidden = true;
    return;
  }
  const f = notebookPromptFact;
  el.hidden = false;
  $('notebookPromptTitle').textContent = f.title || factLabel(f.id);
  $('notebookPromptBody').textContent = f.text;
  $('notebookPromptProv').textContent = f.card
    ? 'In the room'
    : `${(f.provenance || '').replaceAll('_', ' ')}${f.from ? ` · ${f.from}` : ''}`;
  const can = !!state.labAccessActive;
  $('notebookAdd').disabled = !can;
  $('notebookPromptHint').hidden = can;
}

/** Same Add to Notes dialog as a learned fact, for a card read in the room. */
function offerCardCopy(card) {
  if (!card?.id || notebookSkipped.has(card.id)) return;
  const item = { id: card.id, text: card.text, title: card.title, card: true };
  if (notebookPromptFact?.id === card.id || notebookQueue.some(q => q.id === card.id)) return;
  if (notebookPromptFact) notebookQueue.push(item);
  else {
    notebookPromptFact = item;
    renderNotebookPrompt();
  }
}

function showNextNotebookPrompt() {
  if (notebookPromptFact) return;
  while (notebookQueue.length) {
    const next = notebookQueue.shift();
    if (factInNotebook(next.id) || notebookSkipped.has(next.id)) continue;
    notebookPromptFact = next;
    renderNotebookPrompt();
    return;
  }
}

function dismissNotebookPrompt() {
  if (notebookPromptFact) notebookSkipped.add(notebookPromptFact.id);
  notebookPromptFact = null;
  renderNotebookPrompt();
  showNextNotebookPrompt();
}

async function confirmNotebookPrompt() {
  const fact = notebookPromptFact;
  if (!fact) return;
  if (!state.labAccessActive) {
    setPhone(true);
    return;
  }
  try {
    const data = await api('tool', {
      tool: 'file.write',
      rel: `notes/${fact.id}.txt`,
      name: (fact.title || factLabel(fact.id)).slice(0, 40),
      text: fact.text,
      kind: 'note',
      facts: fact.card ? [] : [fact.id],
    });
    state = data.state;
    learnedFactSnapshot = new Set((state.learnedFacts || []).map(f => f.id));
    lastNotice = 'Added to Notes on your handset.';
    notebookPromptFact = null;
    renderNotebookPrompt();
    autosave();
    refreshPhone();
    render();
  } catch (e) {
    lastNotice = e.message;
    renderMessages();
  }
  showNextNotebookPrompt();
}

/** Everyone in the room is an addressee option; the selected one receives the next sentence. */
function renderNPC() {
  const here = presentIds();
  const current = npcId();
  $('npcRow').innerHTML = here.length
    ? here.map(id => {
        const n = state.actors[id];
        const holo = n.presence === 'hologram';
        return `<button type="button" class="actor-chip${id === current ? ' selected' : ''}${holo ? ' hologram' : ''}" data-addressee="${id}" aria-pressed="${id === current}"><span class="avatar">${esc(n.initials)}</span><span><span class="npc-name">${esc(n.name)}</span><span class="npc-role">${esc(n.role)}${holo ? ' · projected' : ''}</span></span></button>`;
      }).join('')
    : '<span class="muted small">No one here — think is open.</span>';
  for (const b of $('npcRow').querySelectorAll('[data-addressee]')) {
    b.onclick = () => {
      addressee = b.dataset.addressee;
      renderNPC();
      renderSuggestions();
    };
  }
}

function renderClock() {
  const c = state.clock || {};
  $('clock').textContent = `${c.timeLabel || '—'} · fuel ${state.fuel ?? '—'}`;
  $('clock').classList.toggle('low', (state.fuel ?? 99) <= 20);
}

function renderThought() {
  const t = state.thought;
  const el = $('thoughtBubble');
  el.hidden = !t;
  if (!t) return;
  const label = state.entities?.[t.about]?.label || t.about;
  const body = t.entries.length
    ? t.entries.map(e => `<p>${esc(e.text)}</p>`).join('')
    : '<p class="muted">Nothing marked from here.</p>';
  el.innerHTML = `<div class="thought-head"><span>Thinking about ${esc(label)}</span><span><button type="button" class="icon-btn" id="thoughtNote" title="Copy to a private note" aria-label="Copy to a private note">▤</button><button type="button" class="icon-btn" id="thoughtClose" title="Close" aria-label="Close">×</button></span></div>${body}`;
  $('thoughtNote').onclick = () => thoughtAction('note');
  $('thoughtClose').onclick = () => thoughtAction('close');
}

async function thoughtAction(action) {
  try {
    const data = await api('thought', { action });
    state = data.state;
    lastNotice = action === 'note' ? 'Copied to a private note on the handset.' : '';
    render();
  } catch (e) {
    lastNotice = e.message;
    renderMessages();
  }
}

function renderMoreLink() {
  const c = state?.conceptLinksEnabled ? state.conceptMoreLink : null;
  const el = $('moreLink');
  el.hidden = !c;
  el.innerHTML = c ? `More: <a href="${esc(c.href)}" target="_blank" rel="noopener">${esc(c.summary)}</a>` : '';
}

const ARC_TITLES = {
  conditional_deployment: 'Conditional deployment',
  technical_suspension: 'Technical suspension',
  inconclusive: 'Inconclusive review',
};

function renderEnding() {
  const e = state.ending;
  const el = $('ending');
  el.hidden = !e && state.act !== 'decision';
  if (el.hidden) return;
  const sc = state.scores;
  const scores = sc
    ? `<p class="small"><b>Still open:</b> ${sc.open.length ? sc.open.map(esc).join(', ') : 'none'} · <b>Control:</b> ${sc.control ? 'a restriction is in place' : 'no restriction'}</p>`
    : '';
  el.innerHTML = e
    ? `<div class="eyebrow section-title">REVIEW SIGNED</div><h2>${esc(ARC_TITLES[e.arc] || e.arc)}${e.addOn ? ' + institutional review' : ''}</h2>${e.effect.map(x => `<p>${esc(x)}</p>`).join('')}${scores}`
    : `<div class="eyebrow section-title">ACT III · THE REVIEW</div><p>Present what you will stand behind, then File to sign.</p>${scores}`;
}

function dismissPhoneCoach() {
  phoneCoachDismissed = true;
  try { sessionStorage.setItem(PHONE_COACH_KEY, '1'); } catch { /* private mode */ }
}

function clearPhoneCoach() {
  phoneCoachDismissed = false;
  try { sessionStorage.removeItem(PHONE_COACH_KEY); } catch { /* private mode */ }
}

function setPhone(open) {
  if (!state?.labAccessActive) open = false;
  phoneOpen = open;
  if (open) dismissPhoneCoach();
  const frame = $('phoneFrame');
  if (state?.labAccessActive && !frame.src) frame.src = '/terminal/index.html?embed=1';
  $('phoneOverlay').hidden = !open;
  renderPhoneButton();
  if (open) collapseChat();
  else syncTranscriptChrome();
}

function renderPhoneButton() {
  const on = !!state?.labAccessActive;
  const coach = on && !!state?.spoken && !phoneCoachDismissed && !phoneOpen;
  $('phoneBtn').hidden = !on;
  $('phoneBtn').classList.toggle('blink', (on && !phoneOpen && phoneUnread) || coach);
  $('phoneBtn').classList.toggle('coach', coach);
  $('phoneBtn').setAttribute('aria-pressed', phoneOpen ? 'true' : 'false');
  if (coach) $('phoneBtn').setAttribute('aria-describedby', 'phoneCoach');
  else $('phoneBtn').removeAttribute('aria-describedby');
  const bubble = $('phoneCoach');
  if (bubble) bubble.hidden = !coach;
  if (on && !$('phoneFrame').src) $('phoneFrame').src = '/terminal/index.html?embed=1';
}

/** Speak hint until the first sent line; then the phone hint until Lab Access is opened. */
function renderCoaches() {
  const showSpeak = !!state && !state.spoken;
  const bubble = $('speakCoach');
  const row = document.querySelector('.dock-input');
  if (bubble) bubble.hidden = !showSpeak;
  row?.classList.toggle('coach-speak', showSpeak);
  if (showSpeak) $('utterance')?.setAttribute('aria-describedby', 'speakCoach');
  else $('utterance')?.removeAttribute('aria-describedby');
  renderPhoneButton();
}

function refreshPhone() {
  $('phoneFrame').contentWindow?.postMessage({ source: 'lsr-room', type: 'refresh' }, location.origin);
}

function clampPhoto(n, lo, hi) {
  return Math.max(lo, Math.min(hi, n));
}

function applyPhotoViewTransform() {
  const m = $('roomMount');
  if (!m) return;
  if (photoMode) {
    m.style.transform = `translate(${photoView.x}px, ${photoView.y}px) scale(${photoView.z})`;
    m.style.transformOrigin = '50% 50%';
  } else {
    m.style.transform = '';
    m.style.transformOrigin = '';
  }
}

function setPhotoMode(active) {
  photoMode = !!active;
  if (!photoMode) {
    photoView = { x: 0, y: 0, z: 1 };
    photoPointers.clear();
    photoPinch0 = null;
  }
  document.body.classList.toggle('photo-mode', photoMode);
  const cap = $('photoCapture');
  if (cap) cap.hidden = !photoMode;
  applyPhotoViewTransform();
  if (photoMode) {
    setPhone(false);
    collapseChat();
    closeMap();
  }
}

function photoPinchDist() {
  const pts = [...photoPointers.values()];
  if (pts.length < 2) return null;
  return Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y) || null;
}

/** Portrait crop (3:4) centered on the viewport; pan/zoom on #roomMount chooses the composition. */
function portraitCropRect() {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  let pw = Math.min(vw * 0.78, 340);
  let ph = (pw * 4) / 3;
  if (ph > vh * 0.88) {
    ph = vh * 0.88;
    pw = (ph * 3) / 4;
  }
  return new DOMRect((vw - pw) / 2, (vh - ph) / 2, pw, ph);
}

async function captureRoomPhoto() {
  if (!room3d?.captureRect) {
    lastNotice = '3D room is required to take a photo.';
    renderMessages();
    return;
  }
  const cropped = room3d.captureRect(portraitCropRect());
  if (!cropped) {
    lastNotice = 'Could not read the room view.';
    renderMessages();
    return;
  }
  const stamp = String(state.clock?.timeLabel || 'shot').replace(':', '');
  const rel = `photos/room-${stamp}.jpg`;
  const name = `Room ${state.clock?.timeLabel || stamp}`;
  try {
    const { dataUrl } = encodePhotoCanvas(cropped);
    const data = await api('tool', {
      tool: 'file.write',
      rel,
      name,
      text: dataUrl,
      kind: 'image',
    });
    if (data.result?.ok === false) throw Error(data.result.reason || 'Could not save photo.');
    state = data.state;
    autosave();
    setPhotoMode(false);
    $('phoneFrame').contentWindow?.postMessage(
      {
        source: 'lsr-room',
        type: 'photo-saved',
        rel,
        file: { name, rel, kind: 'image', owned: true, text: dataUrl, href: `/api/handset-file?rel=${encodeURIComponent(rel)}` },
      },
      location.origin,
    );
    refreshPhone();
    render();
  } catch (e) {
    lastNotice = e.message;
    renderMessages();
  }
}

function cancelPhotoMode() {
  if (!photoMode) return;
  setPhotoMode(false);
  $('phoneFrame').contentWindow?.postMessage({ source: 'lsr-room', type: 'photo-cancel' }, location.origin);
}

window.addEventListener('message', async e => {
  if (e.origin !== location.origin || e.data?.source !== 'lsr-phone') return;
  if (e.data.type === 'close') setPhone(false);
  if (e.data.type === 'photo-mode') setPhotoMode(!!e.data.active);
  if (e.data.type === 'phone-overlay' && state?.labAccessActive) setPhone(!!e.data.open);
  if (e.data.type === 'unread') {
    phoneUnread = !!e.data.unread;
    renderPhoneButton();
  }
  if (e.data.type === 'changed') {
    state = await api('state');
    render();
    autosave();
  }
});

function transcriptSpeakerKey(m) {
  return m.role === 'player' ? 'player' : `npc:${m.npc || ''}`;
}

function transcriptSpeakerLabel(m) {
  return m.role === 'player' ? 'You' : esc(state.actors[m.npc]?.name || 'NPC');
}

function groupTranscriptLines(messages) {
  const groups = [];
  for (const m of messages) {
    const key = transcriptSpeakerKey(m);
    const tail = groups[groups.length - 1];
    if (tail && tail.key === key) tail.messages.push(m);
    else groups.push({ key, messages: [m] });
  }
  return groups;
}

function splitTranscriptSentences(text) {
  const t = String(text || '').trim();
  if (!t) return [];
  const parts = t.split(/(?<=[.!?…])\s+/).map(s => s.trim()).filter(Boolean);
  return parts.length ? parts : [t];
}

function buildTranscriptSentences(messages) {
  const items = [];
  for (const m of messages) {
    for (const sentence of splitTranscriptSentences(m.text)) {
      items.push({ role: m.role, npc: m.npc, text: sentence });
    }
  }
  return items;
}

function groupTranscriptSentenceItems(items) {
  const groups = [];
  for (const item of items) {
    const key = item.role === 'player' ? 'player' : `npc:${item.npc || ''}`;
    const tail = groups[groups.length - 1];
    if (tail && tail.key === key) tail.items.push(item);
    else groups.push({ key, items: [item] });
  }
  return groups;
}

function stopTranscriptReveal() {
  if (transcriptRevealTimer) clearTimeout(transcriptRevealTimer);
  transcriptRevealTimer = null;
  transcriptRevealActive = false;
}

function scrollTranscript(smooth) {
  const box = $('messages');
  if (!box) return;
  box.scrollTo({ top: box.scrollHeight, behavior: smooth ? 'smooth' : 'auto' });
}

function paintTranscript(sentenceItems, { includeNotice = false } = {}) {
  const groups = groupTranscriptSentenceItems(sentenceItems);
  $('messages').innerHTML = groups.length
    ? groups
        .map(g => {
          const role = g.items[0].role === 'player' ? 'player' : 'npc';
          const lines = g.items.map(it => `<div class="transcript-line">${esc(it.text)}</div>`).join('');
          const speakerMsg = { role: g.items[0].role, npc: g.items[0].npc };
          return `<div class="transcript-group ${role}"><div class="transcript-speaker">${transcriptSpeakerLabel(speakerMsg)}</div><div class="transcript-bubbles">${lines}</div></div>`;
        })
        .join('')
    : '';
  if (includeNotice && lastNotice) $('messages').innerHTML += `<div class="notice">${esc(lastNotice)}</div>`;
}

function revealTranscriptSentences(target) {
  if (transcriptDisplayedCount >= target.length) {
    stopTranscriptReveal();
    paintTranscript(target, { includeNotice: true });
    scrollTranscript(false);
    return;
  }
  while (transcriptDisplayedCount < target.length && target[transcriptDisplayedCount].role === 'player') {
    transcriptDisplayedCount++;
    paintTranscript(target.slice(0, transcriptDisplayedCount));
    scrollTranscript(true);
  }
  if (transcriptDisplayedCount >= target.length) {
    stopTranscriptReveal();
    paintTranscript(target, { includeNotice: true });
    scrollTranscript(true);
    return;
  }
  transcriptRevealTimer = setTimeout(() => {
    transcriptDisplayedCount++;
    paintTranscript(target.slice(0, transcriptDisplayedCount));
    scrollTranscript(true);
    revealTranscriptSentences(target);
  }, TRANSCRIPT_SENTENCE_MS);
}

function renderMessages({ animate = false } = {}) {
  const recent = (state.previous || []).slice(-14);
  const target = buildTranscriptSentences(recent);

  if (!animate) {
    stopTranscriptReveal();
    transcriptDisplayedCount = target.length;
    paintTranscript(target, { includeNotice: true });
    scrollTranscript(false);
    return;
  }

  stopTranscriptReveal();
  transcriptRevealActive = true;
  paintTranscript(target.slice(0, transcriptDisplayedCount));
  scrollTranscript(true);
  revealTranscriptSentences(target);
}

function resizeUtterance() {
  const ta = $('utterance');
  if (!ta) return;
  ta.style.height = 'auto';
  ta.style.height = `${Math.min(ta.scrollHeight, 120)}px`;
}

function renderContext() {
  $('context').innerHTML =
    (state.previous || [])
      .slice(-4)
      .map(m => `<div class="context-item"><b>${m.role === 'player' ? 'You' : state.actors[m.npc]?.name || 'NPC'}:</b> ${esc(m.text.slice(0, 190))}</div>`)
      .join('') || '<div class="muted small">No previous utterances yet.</div>';
}

function renderInspector() {
  $('parsed').textContent = JSON.stringify(parse || { pending: 'Analyzing typed language…' }, null, 2);
  $('parseStatus').textContent = parse
    ? parse.source === 'completion'
      ? 'From selected completions'
      : parse.source === 'llm'
        ? 'Model-interpreted typing'
        : 'Locally recognized prefix'
    : 'Parsing partial input…';
  $('confidence').textContent = parse ? `${Math.round((parse.confidence || 0) * 100)}% confidence` : '…';
  $('trace').innerHTML = trace.length
    ? trace
        .slice(-9)
        .map(
          t =>
            `<div class="trace-item"><span class="source">${esc(t.source)}</span> · ${esc(t.text)}${t.ref ? ` <span class="muted">(${esc(t.ref)})</span>` : ''}</div>`
        )
        .join('')
    : '<span class="muted small">Type freely or select a fragment to build a trace.</span>';
  const u = state.usage || { calls: 0, input: 0, output: 0 };
  const est = (u.input * 0.4 + u.output * 1.6) / 1e6;
  $('usage').textContent = `${u.calls} calls · ${u.input.toLocaleString()} input · ${u.output.toLocaleString()} output tokens · ~$${est.toFixed(4)} estimated`;
  $('mode').textContent = state.serverMode === 'demo' ? 'DEMO (no API calls)' : 'LIVE API';
  $('mode').title =
    state.serverMode === 'demo' ? 'Set your OPENAI_API_KEY in .env to use a real model.' : 'Parsing uses the model configured in .env.';
}

function renderSuggestions() {
  const moreBtn = $('showMore');
  if (!parse) {
    $('suggestions').innerHTML = '<div class="empty">Interpreting the typed prefix…</div>';
    $('suggestions').appendChild(moreBtn);
    moreBtn.hidden = true;
    return;
  }
  const alone = !presentIds().length;
  suggestions = getCandidates({
    state, parse, text: $('utterance').value,
    addressees: alone ? [] : presentIds(),
    channel: alone ? 'think' : 'person',
  });
  const page = suggestions.slice(0, visibleCount);
  $('suggestions').innerHTML = page.length
    ? page
        .map((c, i) => `<button type="button" class="suggestion" data-choice="${i}"><span>${esc(c.phrase)}</span><span>↵</span></button>`)
        .join('')
    : '<div class="empty">Continue typing freely, or send this utterance.</div>';
  $('suggestions').appendChild(moreBtn);
  document.querySelectorAll('[data-choice]').forEach(btn => btn.onclick = () => choose(suggestions[Number(btn.dataset.choice)]));
  moreBtn.hidden = suggestions.length <= visibleCount;
  moreBtn.textContent = `Show more (${suggestions.length - visibleCount}) ↓`;
  $('parserIndicator').textContent =
    parse.source === 'llm' ? 'Model-resolved prefix' : parse.source === 'local' ? 'Local prefix' : 'Semantic grammar';
}

function render() {
  document.body.classList.toggle('test', testParam || uiHarness);
  renderClock();
  renderScenePanel();
  renderNPC();
  renderThought();
  renderMoreLink();
  renderEnding();
  renderMessages({ animate: transcriptAnimateOnRender });
  transcriptAnimateOnRender = false;
  renderContext();
  renderInspector();
  renderSuggestions();
  if (floorplanOpen()) syncFloorplan(mapView(), mapHandlers());
  renderMapButton();
  renderCoaches();
  refreshPhone();
  resizeUtterance();
  syncTranscriptChrome();
  trackNewLearnedFacts();
  if (notebookPromptFact) renderNotebookPrompt();
}

function choose(option) {
  if (!option) return;
  requestVersion++;
  clearTimeout(debounce);
  activeRequest?.abort();
  activeRequest = null;
  const before = $('utterance').value;
  $('utterance').value = insertFragment(before, option, parse?.unfinished);
  parse = { ...option.parse, source: 'completion' };
  parseText = $('utterance').value;
  lastAnchoredParse = { ...parse };
  trace.push({ source: 'completion', text: option.phrase, ref: option.entityId });
  visibleCount = 5;
  renderInspector();
  renderSuggestions();
  resizeUtterance();
  $('utterance').focus();
  $('utterance').setSelectionRange(parseText.length, parseText.length);
}

function typed() {
  requestVersion++;
  clearTimeout(debounce);
  activeRequest?.abort();
  activeRequest = null;
  const input = $('utterance').value;
  if (!input.startsWith(parseText)) lastAnchoredParse = null;
  const local = localPrefixParse(input);
  trace.push({ source: 'typed', text: input.slice(-72) });
  if (trace.length > 22) trace = trace.slice(-22);
  visibleCount = 5;
  if (local) {
    parse = local;
    parseText = input;
    renderInspector();
    renderSuggestions();
    return;
  }
  parse = null;
  renderInspector();
  renderSuggestions();
  debounce = setTimeout(() => parseNow(requestVersion), 560);
  resizeUtterance();
}

async function parseNow(version) {
  const text = $('utterance').value;
  if (!text.trim()) {
    parse = makeParse();
    renderInspector();
    renderSuggestions();
    return;
  }
  const ctrl = new AbortController();
  activeRequest = ctrl;
  try {
    const data = await api('parse', { text, previousParse: lastAnchoredParse, constructionTrace: trace.slice(-8) });
    if (version !== requestVersion) return;
    state = data.state;
    applySceneOverlayFromState();
    parse = data.parse;
    parseText = text;
    renderInspector();
    renderSuggestions();
    renderContext();
  } catch (err) {
    if (version !== requestVersion) return;
    parse = makeParse({ kind: 'unintelligible', relation: 'open', open_slot: 'none', open_content: text, confidence: 0, source: 'llm' });
    $('parserIndicator').textContent = 'Parser error';
    lastNotice = `Parser request failed: ${err.message}. Check your API key or try demo mode.`;
    renderInspector();
    renderSuggestions();
    renderMessages();
  }
}

async function send() {
  clearTimeout(debounce);
  const text = $('utterance').value.trim();
  if (!text && !['think', 'commit'].includes(parse?.kind)) return;
  if (!parse || parseText !== $('utterance').value) {
    const version = ++requestVersion;
    await parseNow(version);
  }
  if (!parse) return;
  composerBusy = true;
  focusComposer();
  $('send').disabled = true;
  const transcriptBeforeSend = buildTranscriptSentences((state.previous || []).slice(-14)).length;
  try {
    const data = await api('respond', { text, parse, addressee: npcId() || null });
    state = data.state;
    applySceneOverlayFromState();
    lastNotice = data.effects?.length ? data.effects.join(' · ') : '';
    if (data.thought) lastNotice = '';
    autosave();
    $('utterance').value = '';
    parse = makeParse();
    parseText = '';
    lastAnchoredParse = null;
    trace = [];
    visibleCount = 5;
    transcriptDisplayedCount = transcriptBeforeSend;
    transcriptAnimateOnRender = true;
    expandChat(false);
    render();
  } catch (err) {
    lastNotice = err.message;
    renderMessages();
  } finally {
    $('send').disabled = false;
    composerBusy = false;
    focusComposer();
  }
}

async function move(room) {
  try {
    const data = await api('go', { room });
    state = data.state;
    if (data.scene) sceneOverlay = data.scene;
    applySceneOverlayFromState();
    lastNotice = '';
    addressee = null;
    autosave();
    resetComposer();
    render();
  } catch (e) {
    lastNotice = e.message;
    renderMessages();
    floorplanNotice(room, e.message);
  }
}

async function examine(id) {
  try {
    const data = await api('inspect', { id });
    state = data.state;
    applySceneOverlayFromState();
    lastNotice = `${data.title}: ${data.body}`;
    const kept = (data.terminal?.files || []).some(f => f.rel === `notes/${data.id}.txt`);
    if (data.copy && data.id && !kept) offerCardCopy({ id: data.id, title: data.title, text: data.body });
    autosave();
    expandChat(false);
    render();
  } catch (e) {
    lastNotice = e.message;
    renderMessages();
  }
}

/** O-31: local storage keeps the last event log; Save downloads the same JSON. */
async function autosave() {
  if (uiHarness) return;
  try {
    const res = await fetch('/api/export');
    if (res.ok) localStorage.setItem(SAVE_KEY, await res.text());
  } catch { /* storage full or offline */ }
}

async function downloadSave() {
  const res = await fetch('/api/export');
  const blob = new Blob([await res.text()], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `last-safety-review-${(state.clock?.timeLabel || '').replace(':', '')}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
}

async function loadSave(text) {
  try {
    const data = await api('import', JSON.parse(text));
    state = data.state;
    resetNotebookTracking();
    resetComposer();
    addressee = null;
    lastNotice = 'Save loaded.';
    render();
  } catch (e) {
    lastNotice = `Load failed: ${e.message}`;
    renderMessages();
  }
}

function resetComposer() {
  $('utterance').value = '';
  parse = makeParse();
  parseText = '';
  lastAnchoredParse = null;
  trace = [];
  visibleCount = 5;
  clearTimeout(debounce);
  requestVersion++;
  resizeUtterance();
}

async function setCamera(mode) {
  cameraMode = mode === 'surveillance' ? 'surveillance' : 'play';
  if (uiHarness) {
    try {
      const data = await api('dev/camera', { camera: cameraMode });
      if (data.scene) sceneOverlay = data.scene;
    } catch {
      /* ignore */
    }
  }
  renderScenePanel();
}

$('transcriptDock').addEventListener(
  'pointerdown',
  e => {
    if (e.target.closest('#utterance')) return;
    if (e.target.closest('.transcript-scroll, .dock-npc, #suggestions, .suggestion, #showMore, .dock-input, #send')) {
      expandChat(e.target.closest('#utterance') != null);
    }
  },
  true,
);
$('roomMount').addEventListener('pointerdown', () => collapseChat(), { capture: true });
document.addEventListener(
  'pointerdown',
  e => {
    if (e.target.closest('#transcriptDock, #phoneOverlay, #phoneBtn')) return;
    collapseChat();
  },
  true,
);
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  if (photoMode) cancelPhotoMode();
  else if (phoneOpen) setPhone(false);
  else if (notebookPromptFact) dismissNotebookPrompt();
});

function onPhotoPointerDown(e) {
  if (!photoMode || e.target.closest('#photoShutter')) return;
  $('photoCapture')?.setPointerCapture?.(e.pointerId);
  photoPointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  photoPinch0 = photoPointers.size === 2 ? photoPinchDist() : null;
}

function onPhotoPointerMove(e) {
  if (!photoMode || !photoPointers.has(e.pointerId)) return;
  const prev = photoPointers.get(e.pointerId);
  photoPointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (photoPointers.size === 1) {
    photoView.x = clampPhoto(photoView.x + (e.clientX - prev.x), -320, 320);
    photoView.y = clampPhoto(photoView.y + (e.clientY - prev.y), -240, 240);
    applyPhotoViewTransform();
  } else if (photoPointers.size >= 2 && photoPinch0) {
    const d = photoPinchDist();
    if (d) photoView.z = clampPhoto(photoView.z * (d / photoPinch0), 1, 3);
    photoPinch0 = d;
    applyPhotoViewTransform();
  }
}

function onPhotoPointerUp(e) {
  photoPointers.delete(e.pointerId);
  photoPinch0 = photoPointers.size >= 2 ? photoPinchDist() : null;
}

const photoCap = $('photoCapture');
photoCap?.addEventListener('pointerdown', onPhotoPointerDown);
photoCap?.addEventListener('pointermove', onPhotoPointerMove);
photoCap?.addEventListener('pointerup', onPhotoPointerUp);
photoCap?.addEventListener('pointercancel', onPhotoPointerUp);
$('photoShutter')?.addEventListener('click', e => {
  e.stopPropagation();
  captureRoomPhoto();
});
narrowMq.addEventListener('change', () => {
  if (!narrowMq.matches) {
    chatExpanded = false;
    document.body.classList.remove('transcript-collapsed', 'transcript-expanded');
  } else syncTranscriptChrome();
});
$('utterance').addEventListener('focus', () => expandChat(false));
$('transcriptDock').addEventListener('focusout', e => {
  if (composerBusy) return;
  const dock = $('transcriptDock');
  if (e.relatedTarget && dock.contains(e.relatedTarget)) return;
  requestAnimationFrame(() => {
    if (composerBusy) return;
    if (dock.contains(document.activeElement)) return;
    collapseChat();
  });
});
$('utterance').addEventListener('input', typed);
$('utterance').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});
$('send').addEventListener('mousedown', e => e.preventDefault());
$('send').onclick = send;
$('showMore').onclick = () => {
  visibleCount += 5;
  renderSuggestions();
};
$('reset').onclick = async () => {
  const r = await api('reset', {});
  state = r.state;
  if (r.scene) sceneOverlay = r.scene;
  applySceneOverlayFromState();
  resetComposer();
  lastNotice = '';
  addressee = null;
  clearPhoneCoach();
  clearMapCoach();
  setPhone(false);
  resetNotebookTracking();
  try { localStorage.removeItem(SAVE_KEY); } catch { /* ignore */ }
  render();
  showIntro();
};
$('phoneBtn').onclick = () => setPhone(!phoneOpen);
$('notebookAdd').onclick = () => confirmNotebookPrompt();
$('notebookSkip').onclick = () => dismissNotebookPrompt();
$('menuBtn').onclick = () => setMenu($('menu').hidden);
document.addEventListener('click', e => { if (!$('menu').hidden && !e.target.closest('#menu, #menuBtn')) setMenu(false); });
$('menu').addEventListener('click', e => { if (e.target.closest('button, a')) setMenu(false); });
for (const ev of ['wheel', 'touchstart', 'touchmove']) $('roomMount').addEventListener(ev, () => (userScrollAt = performance.now()), { passive: true });
$('save').onclick = () => downloadSave().catch(e => { lastNotice = e.message; renderMessages(); });
$('load').onclick = () => $('loadFile').click();
$('loadFile').onchange = async () => {
  const f = $('loadFile').files?.[0];
  if (f) await loadSave(await f.text());
  $('loadFile').value = '';
};
$('modeMap').onclick = () => {
  dismissMapCoach();
  if (floorplanOpen()) closeMap();
  else openFloorplan(mapView(), mapHandlers());
  renderMapButton();
};
for (const btn of document.querySelectorAll('[data-act]'))
  btn.onclick = async () => {
    actPreset = btn.dataset.act;
    try {
      await api('dev/act', { act: actPreset });
    } catch {
      /* harness only */
    }
    renderScenePanel();
  };

function showIntro() {
  $('intro').hidden = false;
  $('introStart').focus();
}
$('introStart').onclick = () => { $('intro').hidden = true; $('utterance')?.focus(); };

try {
  await initRenderer();
  state = await api('state');
  applySceneOverlayFromState();
  const saved = !uiHarness && (() => { try { return localStorage.getItem(SAVE_KEY); } catch { return null; } })();
  const fresh = !state.labAccessActive && (state.previous || []).length === 0;
  if (saved && fresh && JSON.parse(saved).events?.some(e => e.kind === 'action')) await loadSave(saved);
  else {
    render();
    if (!uiHarness && fresh) showIntro();
  }
} catch (e) {
  document.body.innerHTML = `<main style="padding:30px;font-family:sans-serif"><h2>Unable to connect to local server</h2><p>${esc(e.message)}</p><p class="muted">Run <code>npm run dev:ui</code> for the graphics harness or <code>npm start</code> for the full prototype.</p></main>`;
}
