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

function npcId() {
  return Object.entries(state.actors).find(([, a]) => a.room === state.room)?.[0];
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
  return {
    act: actPreset,
    camera: cameraMode,
    lightingPreset: actPreset,
    annotations: base.annotations,
    cameraId: base.cameraId,
    timestamp: base.timestamp,
  };
}

function renderScenePanel() {
  const scene = buildSceneView(state, sceneOptions());
  $('roomTitle').textContent = scene.roomTitle.toUpperCase();
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
      lastNotice = uiHarness
        ? 'Terminal lane is separate — use npm start once /api/terminal exists.'
        : 'Workstation terminal opens in the terminal lane (not wired in this build yet).';
      renderMessages();
    },
    onFocusActor: () => $('utterance').focus({ preventScroll: true }),
  };
  if (room3d) room3d.update(scene, handlers);
  else mountScene($('roomMount'), scene, handlers);
}

async function initRenderer() {
  try {
    const { RoomRenderer, webglAvailable } = await import('./render/three-scene.mjs');
    if (!webglAvailable()) throw Error('WebGL is not available in this browser');
    room3d = new RoomRenderer($('roomMount'));
  } catch (err) {
    console.warn('[scene] 3D renderer unavailable, using CSS room:', err);
    lastNotice = `3D room unavailable (${err.message}). Run npm install in the game folder, or use a WebGL browser.`;
  }
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
    ? state.learnedFacts.map(f => `<span title="${esc(f.text)}">${esc(f.id.replaceAll('_', ' '))}</span>`).join('')
    : '<span>No documents inspected yet</span>';
  for (const btn of $('rooms').querySelectorAll('[data-room]')) btn.onclick = () => move(btn.dataset.room);
  for (const btn of document.querySelectorAll('[data-evidence]')) btn.onclick = () => examine(btn.dataset.evidence);
}

function renderNPC() {
  const id = npcId();
  const n = state.actors[id];
  if (!n) {
    $('npcName').textContent = 'No one present';
    $('npcRole').textContent = '—';
    $('avatar').textContent = '—';
    $('npcStatus').textContent = 'EMPTY';
    return;
  }
  $('npcName').textContent = n.name;
  $('npcRole').textContent = n.role;
  $('avatar').textContent = n.initials;
  $('npcStatus').textContent = 'AVAILABLE';
}

function renderMessages() {
  const convo = state.previous || [];
  const messages = convo.length ? convo.slice(-10) : [{ role: 'npc', text: 'The model shut down. That’s what the test established.' }];
  $('messages').innerHTML = messages
    .map(
      m =>
        `<div class="bubble ${m.role === 'player' ? 'player' : 'npc'}"><div class="bubble-note">${m.role === 'player' ? 'YOU' : esc(state.actors[m.npc]?.name || state.actors[npcId()]?.name || 'NPC')}</div>${esc(m.text)}</div>`
    )
    .join('');
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
  suggestions = getCandidates({ state, parse, text: $('utterance').value });
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
  renderSidebar();
  renderScenePanel();
  renderNPC();
  renderMessages();
  renderContext();
  renderInspector();
  renderSuggestions();
  if (floorplanOpen()) syncFloorplan(mapView(), mapHandlers());
  renderMapButton();
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
  if (!text) return;
  if (!parse || parseText !== $('utterance').value) {
    const version = ++requestVersion;
    await parseNow(version);
  }
  if (!parse) return;
  $('send').disabled = true;
  try {
    const data = await api('respond', { text, parse });
    state = data.state;
    applySceneOverlayFromState();
    lastNotice = data.effects?.length ? data.effects.join(' · ') : '';
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
    render();
  } catch (e) {
    lastNotice = e.message;
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
  render();
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
  render();
} catch (e) {
  document.body.innerHTML = `<main style="padding:30px;font-family:sans-serif"><h2>Unable to connect to local server</h2><p>${esc(e.message)}</p><p class="muted">Run <code>npm run dev:ui</code> for the graphics harness or <code>npm start</code> for the full prototype.</p></main>`;
}
