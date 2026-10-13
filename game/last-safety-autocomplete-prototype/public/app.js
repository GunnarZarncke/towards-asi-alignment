import { makeParse } from '../lib/grammar.mjs';
import { getCandidates, insertFragment, localPrefixParse } from '/grammar.js';
import { buildSceneView, mountScene } from './render/scene-view.mjs';
import { ROOM_META, VISITOR_CLEARANCE, doorsOn } from './render/rooms.mjs';
import { closeFloorplan, floorplanNotice, floorplanOpen, openFloorplan, syncFloorplan } from './render/floorplan-view.mjs';

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
const SAVE_KEY = 'lsr-save';
/** Debug panels (parser inspector, trace, usage, server mode) show only in test mode or the dev-ui harness. */
const testParam = new URLSearchParams(location.search).has('test');
let userScrollAt = 0;

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
  $('modePlay').classList.toggle('active', cameraMode === 'play');
  $('modeSurveillance').classList.toggle('active', cameraMode === 'surveillance');
  $('modePlay').setAttribute('aria-pressed', cameraMode === 'play' ? 'true' : 'false');
  $('modeSurveillance').setAttribute('aria-pressed', cameraMode === 'surveillance' ? 'true' : 'false');
  $('sceneNote').textContent =
    cameraMode === 'surveillance'
      ? 'Belief overlays — compare with play view before trusting labels'
      : room3d
        ? 'Click the floor to walk · click a person to move them · doors and records walk you there'
        : 'Tap hotspots — doors, records, people';
  $('actSwitch').hidden = !uiHarness;
  for (const btn of document.querySelectorAll('[data-act]')) btn.classList.toggle('active', btn.dataset.act === actPreset);

  const handlers = {
    onGo: room => move(room),
    onInspect: id => examine(id),
    onTerminal: () => {
      if (uiHarness || !state.labAccessActive) return;
      setPhone(true);
    },
    onFocusActor: id => {
      if (id && state.actors[id]) addressee = id;
      renderNPC();
      renderSuggestions();
      $('utterance').focus({ preventScroll: true });
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
  const m = $('roomMount');
  const max = m.scrollWidth - m.clientWidth;
  if (max <= 1 || performance.now() - userScrollAt < 2500) return;
  const p = room3d.playerScreen();
  if (!p) return;
  const target = Math.max(0, Math.min(max, p.x - m.clientWidth / 2));
  const d = target - m.scrollLeft;
  if (Math.abs(d) > 1) m.scrollLeft += d * 0.12;
}

function setDrawer(open) {
  $('drawer').hidden = !open;
  $('drawerBtn').setAttribute('aria-expanded', open ? 'true' : 'false');
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

function renderMapButton() {
  const open = floorplanOpen();
  $('modeMap').classList.toggle('active', open);
  $('modeMap').setAttribute('aria-pressed', open ? 'true' : 'false');
}

function renderSidebar() {
  const clearance = state.clearance ?? VISITOR_CLEARANCE;
  const doors = doorsOn(state.room);
  $('rooms').innerHTML = doors.length
    ? doors
        .map(d => {
          const gated = d.required > clearance;
          const who = Object.values(state.actors).find(a => a.room === d.to)?.name || '';
          return `<button class="room-btn${gated ? ' gated' : ''}" data-room="${d.to}"><span class="room-ico">${gated ? '⊘' : '→'}</span><span><b>${esc(roomNames[d.to] || d.to)}</b><small>${who ? esc(who) : gated ? 'Higher clearance' : 'Open'}</small></span></button>`;
        })
        .join('')
    : '<p class="small muted">No doors from here.</p>';
  $('evidence').innerHTML = state.evidence
    .map(
      e =>
        `<button class="record-btn" data-evidence="${e.id}" ${e.room !== state.room ? 'disabled title="Travel to ' + roomNames[e.room] + '"' : ''}><span class="icon ${e.examined ? 'done' : ''}">${e.examined ? '✓' : '▤'}</span><span>${e.title}${e.examined ? ' · examined' : ''}</span></button>`
    )
    .join('');
  $('knowledge').innerHTML = state.learnedFacts.length
    ? state.learnedFacts.map(f => `<span class="prov-${esc(f.provenance)}" title="${esc(f.text)} (${esc(f.provenance.replaceAll('_', ' '))})">${esc(f.id.replaceAll('_', ' '))}</span>`).join('')
    : '<span>Nothing learned yet</span>';
  for (const btn of $('rooms').querySelectorAll('[data-room]')) btn.onclick = () => move(btn.dataset.room);
  for (const btn of document.querySelectorAll('[data-evidence]')) btn.onclick = () => examine(btn.dataset.evidence);
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
      }).join('') + `<span class="available">${here.length > 1 ? 'SPEAKING TO ' + esc(state.actors[current].name.split(' ')[0].toUpperCase()) : 'AVAILABLE'}</span>`
    : '<div class="npc-name muted">No one present</div><span class="available">EMPTY · THINK IS OPEN</span>';
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
  $('labClock').textContent = `LABORATORY · ${c.dateLabel || ''} · ${c.timeLabel || ''}`.toUpperCase();
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
  const c = state.conceptLinksEnabled ? state.conceptMoreLink : null;
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

function setPhone(open) {
  if (!state?.labAccessActive) open = false;
  phoneOpen = open;
  const frame = $('phoneFrame');
  if (state?.labAccessActive && !frame.src) frame.src = '/terminal/index.html?embed=1';
  $('phoneOverlay').hidden = !open;
  renderPhoneButton();
}

function renderPhoneButton() {
  const on = !!state?.labAccessActive;
  $('phoneBtn').hidden = !on;
  $('phoneBtn').classList.toggle('blink', on && !phoneOpen && phoneUnread);
  $('phoneBtn').setAttribute('aria-pressed', phoneOpen ? 'true' : 'false');
  if (on && !$('phoneFrame').src) $('phoneFrame').src = '/terminal/index.html?embed=1';
}

function refreshPhone() {
  $('phoneFrame').contentWindow?.postMessage({ source: 'lsr-room', type: 'refresh' }, location.origin);
}

window.addEventListener('message', async e => {
  if (e.origin !== location.origin || e.data?.source !== 'lsr-phone') return;
  if (e.data.type === 'close') setPhone(false);
  if (e.data.type === 'unread') {
    phoneUnread = !!e.data.unread;
    renderPhoneButton();
  }
  if (e.data.type === 'changed') {
    state = await api('state');
    render();
  }
});

function renderMessages() {
  const convo = state.previous || [];
  $('messages').innerHTML = convo.length
    ? convo.slice(-10).map(
        m =>
          `<div class="bubble ${m.role === 'player' ? 'player' : 'npc'}"><div class="bubble-note">${m.role === 'player' ? 'YOU' : esc(state.actors[m.npc]?.name || 'NPC')}</div>${esc(m.text)}</div>`
      ).join('')
    : '';
  if (lastNotice) $('messages').innerHTML += `<div class="notice">${esc(lastNotice)}</div>`;
  $('messages').scrollTop = $('messages').scrollHeight;
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
  if (!parse) {
    $('suggestions').innerHTML = '<div class="empty">Interpreting the typed prefix…</div>';
    $('showMore').hidden = true;
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
  document.querySelectorAll('[data-choice]').forEach(btn => btn.onclick = () => choose(suggestions[Number(btn.dataset.choice)]));
  $('showMore').hidden = suggestions.length <= visibleCount;
  $('showMore').textContent = `Show more (${suggestions.length - visibleCount}) ↓`;
  $('parserIndicator').textContent =
    parse.source === 'llm' ? 'Model-resolved prefix' : parse.source === 'local' ? 'Local prefix' : 'Semantic grammar';
}

function render() {
  document.body.classList.toggle('test', testParam || uiHarness);
  renderClock();
  renderSidebar();
  renderScenePanel();
  renderNPC();
  renderThought();
  renderMoreLink();
  renderEnding();
  renderMessages();
  renderContext();
  renderInspector();
  renderSuggestions();
  if (floorplanOpen()) syncFloorplan(mapView(), mapHandlers());
  renderMapButton();
  renderPhoneButton();
  refreshPhone();
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
  $('send').disabled = true;
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
    render();
  } catch (err) {
    lastNotice = err.message;
    renderMessages();
  } finally {
    $('send').disabled = false;
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
    autosave();
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

$('utterance').addEventListener('input', typed);
$('utterance').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});
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
  setPhone(false);
  try { localStorage.removeItem(SAVE_KEY); } catch { /* ignore */ }
  render();
};
$('phoneBtn').onclick = () => setPhone(!phoneOpen);
$('drawerBtn').onclick = () => setDrawer($('drawer').hidden);
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
$('modePlay').onclick = () => setCamera('play');
$('modeSurveillance').onclick = () => setCamera('surveillance');
$('modeMap').onclick = () => {
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

try {
  await initRenderer();
  state = await api('state');
  applySceneOverlayFromState();
  const saved = !uiHarness && (() => { try { return localStorage.getItem(SAVE_KEY); } catch { return null; } })();
  const fresh = !state.labAccessActive && (state.previous || []).length === 0;
  if (saved && fresh && JSON.parse(saved).events?.some(e => e.kind === 'action')) await loadSave(saved);
  else render();
} catch (e) {
  document.body.innerHTML = `<main style="padding:30px;font-family:sans-serif"><h2>Unable to connect to local server</h2><p>${esc(e.message)}</p><p class="muted">Run <code>npm run dev:ui</code> for the graphics harness or <code>npm start</code> for the full prototype.</p></main>`;
}
