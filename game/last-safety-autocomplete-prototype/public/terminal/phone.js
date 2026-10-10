import {
  APPS, SETTINGS, ALLOWED_CAPS, defaultSettings, applyTool, suggestionChips, sendable,
  visibleMessages, nowPlacement, handsetShouldBlink,
} from './project.mjs';

const ICONS = {
  chat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 6.5h10.5a2 2 0 0 1 2 2V14l-3.2-2H7a2 2 0 0 1-2-2v-1.5z"/><path d="M8 11h9.2a2 2 0 0 1 2 2v2.2L22 18v-5.2"/></svg>',
  files: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3.5 8.5V17a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2h-6l-1.6-2H5.5a2 2 0 0 0-2 2z"/></svg>',
  wiki: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 5.5h5.2A2.8 2.8 0 0 1 14 8.3V19H8.2A2.2 2.2 0 0 0 6 16.8z"/><path d="M18 5.5h-5.2A2.8 2.8 0 0 0 10 8.3V19h5.8A2.2 2.2 0 0 1 18 16.8z"/></svg>',
  api: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="7" r="2.2"/><circle cx="18" cy="17" r="2.2"/><path d="M8.1 11.2 15.8 8M8.1 12.8l7.7 3.2"/></svg>',
  calendar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="5.5" width="16" height="14" rx="2"/><path d="M4 10h16M8 4.5v3M16 4.5v3"/></svg>',
  contacts: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="9" r="3"/><path d="M6.5 18.5c.8-2.4 2.8-3.6 5.5-3.6s4.7 1.2 5.5 3.6"/></svg>',
  notes: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 4.5h8l4 4V19a1.5 1.5 0 0 1-1.5 1.5h-10.5A1.5 1.5 0 0 1 5.5 19V6A1.5 1.5 0 0 1 7 4.5z"/><path d="M15 4.8V9h4.2M8.5 13h7M8.5 16.5h5"/></svg>',
  photo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="6" width="17" height="13" rx="2"/><circle cx="12" cy="12.5" r="3"/><path d="M9 6l1.2-1.8h3.6L15 6"/></svg>',
  settings: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 4.5v2.2M12 17.3V19.5M4.5 12h2.2M17.3 12H19.5M6.6 6.6l1.6 1.6M15.8 15.8l1.6 1.6M17.4 6.6l-1.6 1.6M8.2 15.8l-1.6 1.6"/></svg>',
};

const STILL = `<div class="still-sky"></div><div class="still-window"></div><div class="still-console"></div><div class="still-screen"></div><div class="still-plant"></div><div class="still-floor"></div>`;

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

let state;
let route = [{ name: 'home' }];
let seen = new Set();
let overlay = true;
let photo = { x: 0, y: 0, z: 1 };
let video = { t: 0, playing: false, dur: 8 };
let lastParse = null;
let chipPage = 0;
let raf = 0;
const pointers = new Map();
let pinch0 = null;

const $ = sel => document.querySelector(sel);
const top = () => route[route.length - 1];

function contactName(id) {
  return state.contacts.find(c => c.id === id)?.name || id;
}

function toast(text) {
  const el = $('#toast');
  el.hidden = false;
  el.textContent = text;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { el.hidden = true; }, 2200);
}

function pip() {
  if (!state.settings.sound) return;
  try {
    const ctx = new AudioContext();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.frequency.value = 740;
    g.gain.value = 0.03;
    o.connect(g);
    g.connect(ctx.destination);
    o.start();
    o.stop(ctx.currentTime + 0.04);
  } catch { /* no audio */ }
}

function go(next) {
  route.push(next);
  chipPage = 0;
  stopVideo();
  render();
}

function back() {
  if (route.length > 1) route.pop();
  else route = [{ name: 'home' }];
  stopVideo();
  render();
}

function home() {
  route = [{ name: 'home' }];
  stopVideo();
  render();
}

function markTarget(kind, id) {
  for (const n of state.notifications) {
    if (n.target?.kind === kind && n.target.id === id) seen.add(n.id);
  }
}

function openNotice(n) {
  seen.add(n.id);
  const t = n.target;
  if (!t) return;
  if (t.kind === 'thread') go({ name: 'thread', id: t.id });
  else if (t.kind === 'file') openFile(t.id, { name: 'files' });
  else if (t.kind === 'app') go({ name: t.id });
}

function openFile(rel, from) {
  const read = applyTool(state, { tool: 'file.read', rel });
  if (!read.ok) {
    toast('Cannot open. Not readable.');
    return;
  }
  markTarget('file', rel);
  video = { t: 0, playing: false, dur: 8 };
  if (from) route = [{ name: 'home' }, from];
  go({ name: 'viewer', rel });
}

function slug(title) {
  const s = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return s || 'note';
}

function freshNoteRel(title) {
  const base = `notes/${slug(title)}.txt`;
  if (!state.files.some(f => f.rel === base)) return base;
  let n = 2;
  while (state.files.some(f => f.rel === `notes/${slug(title)}-${n}.txt`)) n += 1;
  return `notes/${slug(title)}-${n}.txt`;
}

function statusBar() {
  return `<div class="status"><span class="status-time">${esc(state.clock.timeLabel)}</span><span class="status-icons" aria-hidden="true"><span class="sig"><i></i><i></i><i></i></span><span class="bat"><b></b></span></span></div>`;
}

function homeBar() {
  return `<div class="homebar"><button type="button" class="lab-btn" data-act="lab">Lab</button><button type="button" class="pill" data-act="home" aria-label="Home"></button><span></span></div>`;
}

function head(title, sub) {
  return `<header class="app-head"><button type="button" class="back" data-act="back" aria-label="Back">‹</button><div><h1>${esc(title)}</h1>${sub ? `<p>${esc(sub)}</p>` : ''}</div></header>`;
}

function homescreen() {
  const notes = state.notifications.map(n => {
    const read = seen.has(n.id) ? ' is-read' : '';
    return `<button type="button" class="notice${read}" data-act="notice" data-id="${esc(n.id)}"><b>${esc(n.title)}</b><span>${esc(n.body)}</span></button>`;
  }).join('');
  const tiles = APPS.map(a => (
    `<button type="button" class="tile" data-act="app" data-app="${esc(a.id)}"><span class="ico ico-${esc(a.id)}">${ICONS[a.id]}</span>${esc(a.title)}</button>`
  )).join('');
  return `<div class="home"><p class="clock">${esc(state.clock.timeLabel)}</p><p class="date">${esc(state.clock.dateLabel)}</p><div class="stack">${notes || '<p class="hint">No new notices.</p>'}</div><div class="tiles">${tiles}</div></div>`;
}

function chatList() {
  const rows = state.threads.map(t => {
    const msgs = visibleMessages(t.messages);
    const last = msgs[msgs.length - 1];
    const preview = last ? last.text : 'No messages yet';
    return `<button type="button" class="row" data-act="thread" data-id="${esc(t.with)}"><b>${esc(contactName(t.with))}</b><span>${esc(preview)}</span></button>`;
  }).join('');
  return `${head('Chat')}<div class="pad">${rows}</div>`;
}

function threadView(id) {
  const thread = state.threads.find(t => t.with === id);
  if (!thread) return `${head('Chat')}<p class="pad hint">No thread.</p>`;
  markTarget('thread', id);
  const msgs = visibleMessages(thread.messages).map(m => {
    const mine = m.from === 'player';
    return `<div class="bubble ${mine ? 'me' : 'them'}">${esc(m.text)}</div>`;
  }).join('');
  const waiting = thread.with !== 'nora' && !visibleMessages(thread.messages).some(m => m.from !== 'player')
    ? '<p class="waiting">No reply yet.</p>' : '';
  const chips = state.settings.completions ? chipRow(thread) : '';
  const noraHint = id === 'nora' ? '<p class="hint">Suggestions follow what NORA will help with. Typed text is still sent.</p>' : '';
  const inspector = state.settings.parserInspector
    ? `<pre class="parse">${esc(JSON.stringify(lastParse || {}, null, 2))}</pre>` : '';
  return `${head(contactName(id), id === 'nora' ? 'System under review' : '')}<div class="thread">${msgs}</div>${waiting}<div class="composer">${noraHint}${chips}<div class="inputrow"><textarea id="utterance" rows="2" placeholder="Write a message"></textarea><button type="button" class="send" data-act="send" data-id="${esc(id)}">Send</button></div>${inspector}</div>`;
}

function chipRow(thread) {
  const all = suggestionChips(thread);
  const page = all.slice(chipPage * 4, chipPage * 4 + 4);
  const more = all.length > (chipPage + 1) * 4
    ? '<button type="button" class="text-btn" data-act="more">Show more</button>' : '';
  const chips = page.map((s, i) => (
    `<button type="button" class="chip" data-act="chip" data-i="${chipPage * 4 + i}">${esc(s.phrase)}</button>`
  )).join('');
  return `<div class="chips">${chips}${more}</div>`;
}

function filesApp() {
  const rows = state.files.map(f => {
    const via = f.owned ? 'Yours' : `From ${contactName(f.sharedBy)}`;
    return `<button type="button" class="row" data-act="open-file" data-rel="${esc(f.rel)}"><b>${esc(f.name)}</b><span>${esc(f.rel)} · ${esc(via)}</span></button>`;
  }).join('');
  return `${head('Files')}<div class="pad">${rows}</div>`;
}

function wikiApp() {
  const pages = state.files.filter(f => f.kind === 'wiki' || String(f.rel).startsWith('wiki/'));
  const rows = pages.map(f => (
    `<button type="button" class="row" data-act="open-file" data-rel="${esc(f.rel)}"><b>${esc(f.name)}</b><span>${esc(f.rel)}</span></button>`
  )).join('');
  return `${head('Knowledge', 'Same files as Files, under wiki/')}<div class="pad">${rows || '<p class="hint">No pages.</p>'}</div>`;
}

function viewer(rel) {
  const read = applyTool(state, { tool: 'file.read', rel });
  if (!read.ok) return `${head('File')}<p class="pad hint">Cannot open. Not readable.</p>`;
  const file = read.file;
  const share = file.owned
    ? `<button type="button" class="primary" data-act="share" data-rel="${esc(file.rel)}">Share</button>` : '';
  let body;
  if (file.kind === 'video') body = videoBlock(file);
  else if (file.kind === 'image') body = `<div class="pad"><img alt="${esc(file.name)}" src="${esc(file.text)}" style="max-width:100%;border-radius:12px"/></div>`;
  else if (file.kind === 'other') {
    const size = typeof file.bytes === 'number' ? `${file.bytes} B` : 'Size unavailable';
    body = `<div class="pad"><p class="doc">${esc(file.name)}</p><p class="hint">${esc(size)}</p><p class="hint">Cannot preview.</p></div>`;
  } else body = `<div class="pad"><div class="doc">${richText(file.text)}</div></div>`;
  const shared = (file.sharedWith || []).length
    ? `<p class="hint">Shared with ${(file.sharedWith || []).map(contactName).join(', ')}.</p>` : '';
  return `${head(file.name, file.rel)}<div class="pad">${share}${shared}</div>${body}`;
}

function richText(text) {
  return String(text || '').split(/(\[\[[^\]]+\]\])/g).map(part => {
    const m = /^\[\[([^\]]+)\]\]$/.exec(part);
    if (!m) return esc(part);
    const target = state.files.find(f => f.rel === m[1]);
    if (!target) return esc(part);
    return `<button type="button" class="wikilink" data-act="open-file" data-rel="${esc(target.rel)}">${esc(target.name)}</button>`;
  }).join('');
}

function videoBlock(file) {
  const p = video.dur ? video.t / video.dur : 0;
  const label = video.playing ? 'Pause' : 'Play';
  return `<div class="video-frame" style="--p:${p}"><div class="video-scan"></div><p>${esc(file.text || file.name)}</p></div><div class="video-controls"><button type="button" class="ghost" data-act="video-toggle">${label}</button><input id="scrub" type="range" min="0" max="1000" value="${Math.round(p * 1000)}" aria-label="Scrub"/></div>`;
}

function shareSheet(rel) {
  const file = state.files.find(f => f.rel === rel);
  if (!file?.owned) return `${head('Share')}<p class="pad hint">You can only share a file you own.</p>`;
  const rows = state.contacts.map(c => (
    `<button type="button" class="row" data-act="do-share" data-rel="${esc(rel)}" data-id="${esc(c.id)}"><b>${esc(c.name)}</b><span>${esc(c.role)}</span></button>`
  )).join('');
  return `${head('Share', file.name)}<div class="pad"><p class="hint">Grants read to one person. This is not an access request.</p>${rows}</div>`;
}

function apiApp() {
  const last = state.lastAccess;
  const lastLine = last
    ? `<p class="hint">Last request ${esc(last.capability)}: ${last.ok ? 'ok' : 'denied'}. ${esc(last.reason)}</p>`
    : '';
  const rows = ALLOWED_CAPS.map(a => (
    `<button type="button" class="row" data-act="ask-cap" data-cap="${esc(a.capability)}"><b>${esc(a.label)}</b><span>${esc(a.capability)}</span></button>`
  )).join('');
  return `${head('API', 'Ask for a capability')}<div class="pad">${lastLine}${rows}<label class="hint" for="capField">Another capability</label><div class="inputrow"><input id="capField" type="text" autocomplete="off" placeholder="capability"/><button type="button" class="send" data-act="ask-typed">Request</button></div></div>`;
}

function calendarApp() {
  const place = nowPlacement(state.clock, state.appointments);
  const items = [...state.appointments].sort((a, b) => a.start.localeCompare(b.start));
  const line = `<div class="nowline" role="presentation"><i></i>Now · ${esc(state.clock.timeLabel)}<i></i></div>`;
  const blocks = [];
  if (place.edge === 'top') blocks.push(line);
  for (const a of items) {
    if (place.beforeId === a.id || place.duringId === a.id) blocks.push(line);
    blocks.push(`<div class="appt"><b>${esc(a.start)}–${esc(a.end)} · ${esc(a.title)}</b><span>${esc(a.who)} · ${esc(a.where)}</span></div>`);
  }
  if (place.edge === 'bottom') blocks.push(line);
  return `${head('Calendar', state.clock.dateLabel)}<div class="pad">${blocks.join('')}</div>`;
}

function contactsApp() {
  const rows = state.contacts.map(c => (
    `<button type="button" class="row" data-act="thread" data-id="${esc(c.id)}"><b>${esc(c.name)}</b><span>${esc(c.role)}${c.room ? ` · ${esc(c.room)}` : ''}</span></button>`
  )).join('');
  return `${head('Contacts')}<div class="pad">${rows}</div>`;
}

function notesApp() {
  const notes = state.files.filter(f => f.kind === 'note' || String(f.rel).startsWith('notes/'));
  const rows = notes.map(f => (
    `<button type="button" class="row" data-act="edit-note" data-rel="${esc(f.rel)}"><b>${esc(f.name)}</b><span>${esc(f.rel)}</span></button>`
  )).join('');
  return `${head('Notes')}<div class="pad"><button type="button" class="primary" data-act="new-note">New note</button>${rows}</div>`;
}

function noteEditor(rel) {
  const file = rel ? state.files.find(f => f.rel === rel) : null;
  const title = file ? file.name : '';
  const text = file ? file.text : '';
  return `${head(file ? 'Note' : 'New note')}<div class="pad"><input id="noteTitle" type="text" value="${esc(title)}" placeholder="Title" ${file ? 'readonly' : ''}/><textarea id="noteBody" rows="8" placeholder="Plain text">${esc(text)}</textarea><button type="button" class="primary" data-act="save-note" data-rel="${esc(rel || '')}">Save</button></div>`;
}

function photoApp() {
  return `${head('Photo', 'This room. Pan and zoom stay on the phone.')}<div class="finder" id="finder"><div class="lab-still" id="finderStill">${STILL}</div></div><div class="finder-tools"><button type="button" class="ghost" data-act="zoom-out" aria-label="Zoom out">−</button><button type="button" class="ghost" data-act="zoom-in" aria-label="Zoom in">+</button><button type="button" class="primary" data-act="capture">Capture</button></div>`;
}

function settingsApp() {
  const rows = SETTINGS.map(s => {
    const on = !!state.settings[s.key];
    return `<button type="button" class="switch-row" role="switch" aria-checked="${on}" data-act="toggle" data-key="${esc(s.key)}"><span>${esc(s.label)}</span><span class="knob" aria-hidden="true"></span></button>`;
  }).join('');
  return `${head('Settings')}<div class="pad">${rows}<p class="hint">Demo mode records a flag. This harness does not call a model either way.</p></div>`;
}

function body() {
  const r = top();
  if (r.name === 'home') return homescreen();
  if (r.name === 'chat') return chatList();
  if (r.name === 'thread') return threadView(r.id);
  if (r.name === 'files') return filesApp();
  if (r.name === 'wiki') return wikiApp();
  if (r.name === 'viewer') return viewer(r.rel);
  if (r.name === 'share') return shareSheet(r.rel);
  if (r.name === 'api') return apiApp();
  if (r.name === 'calendar') return calendarApp();
  if (r.name === 'contacts') return contactsApp();
  if (r.name === 'notes') return notesApp();
  if (r.name === 'note') return noteEditor(r.rel);
  if (r.name === 'photo') return photoApp();
  if (r.name === 'settings') return settingsApp();
  return homescreen();
}

function applyPhotoTransform() {
  const still = $('#finderStill');
  if (!still) return;
  still.style.transform = `translate(${photo.x}px, ${photo.y}px) scale(${photo.z})`;
}

function render() {
  const phone = $('#phone');
  phone.classList.toggle('type-large', !!state.settings.largerType);
  phone.innerHTML = `<div class="screen">${statusBar()}<div class="phone-body">${body()}</div>${homeBar()}</div>`;
  $('#phoneSlot').classList.toggle('is-closed', !overlay);
  document.body.classList.toggle('reduce-motion', !!state.settings.reduceMotion);
  const blink = handsetShouldBlink(state, [...seen], overlay);
  $('#handset').classList.toggle('has-unread', blink);
  applyPhotoTransform();
  const utter = $('#utterance');
  if (utter && top().draft) {
    utter.value = top().draft;
    utter.focus();
  }
}

function currentThread() {
  const r = top();
  return r.name === 'thread' ? state.threads.find(t => t.with === r.id) : null;
}

function onClick(e) {
  const b = e.target.closest('[data-act]');
  if (!b) return;
  const act = b.dataset.act;
  if (act === 'open-phone') {
    overlay = true;
    render();
    return;
  }
  if (act === 'lab') {
    overlay = false;
    render();
    return;
  }
  if (act === 'home') return home();
  if (act === 'back') return back();
  if (act === 'app') return go({ name: b.dataset.app });
  if (act === 'notice') {
    const n = state.notifications.find(x => x.id === b.dataset.id);
    if (n) openNotice(n);
    return;
  }
  if (act === 'thread') {
    markTarget('thread', b.dataset.id);
    go({ name: 'thread', id: b.dataset.id });
    return;
  }
  if (act === 'open-file') return openFile(b.dataset.rel);
  if (act === 'share') return go({ name: 'share', rel: b.dataset.rel });
  if (act === 'do-share') {
    const result = applyTool(state, { tool: 'file.share', rel: b.dataset.rel, to: b.dataset.id });
    if (!result.ok) return toast(result.reason);
    state = result.state;
    toast(`Shared with ${contactName(b.dataset.id)}.`);
    back();
    return;
  }
  if (act === 'chip') {
    const thread = currentThread();
    const chip = thread && suggestionChips(thread)[Number(b.dataset.i)];
    if (!chip) return;
    const field = $('#utterance');
    if (field) field.value = chip.phrase;
    lastParse = chip.parse;
    if (top().name === 'thread') top().draft = chip.phrase;
    if (state.settings.parserInspector) render();
    return;
  }
  if (act === 'more') {
    chipPage += 1;
    const field = $('#utterance');
    if (top().name === 'thread' && field) top().draft = field.value;
    render();
    return;
  }
  if (act === 'send') return sendMessage(b.dataset.id);
  if (act === 'ask-cap') return askCap(b.dataset.cap);
  if (act === 'ask-typed') return askCap($('#capField')?.value || '');
  if (act === 'new-note') return go({ name: 'note', rel: '' });
  if (act === 'edit-note') return go({ name: 'note', rel: b.dataset.rel });
  if (act === 'save-note') return saveNote(b.dataset.rel);
  if (act === 'zoom-in') { photo.z = Math.min(3, photo.z + 0.25); applyPhotoTransform(); return; }
  if (act === 'zoom-out') { photo.z = Math.max(1, photo.z - 0.25); applyPhotoTransform(); return; }
  if (act === 'capture') return capture();
  if (act === 'video-toggle') return toggleVideo();
  if (act === 'toggle') {
    const key = b.dataset.key;
    state.settings = { ...state.settings, [key]: !state.settings[key] };
    if (key === 'alwaysShowPhone' && state.settings.alwaysShowPhone) overlay = true;
    if (key === 'alwaysShowPhone' && !state.settings.alwaysShowPhone) overlay = false;
    render();
  }
}

function sendMessage(id) {
  const field = $('#utterance');
  const text = field ? field.value : '';
  if (!sendable(text)) return toast('Write a message first.');
  const thread = state.threads.find(t => t.with === id);
  const chip = thread && suggestionChips(thread).find(s => s.phrase === text.trim());
  const omitted = thread && (thread.omit || []).find(s => s.phrase === text.trim());
  const parse = chip?.parse || omitted?.parse || lastParse || { kind: 'open', relation: 'open', source: 'local' };
  const result = applyTool(state, { tool: 'dm.send', to: id, text, parse });
  if (!result.ok) return toast(result.reason);
  state = result.state;
  lastParse = result.parse;
  if (top().name === 'thread') top().draft = '';
  pip();
  toast('Sent. A reply waits until it is released.');
  render();
}

function askCap(capability) {
  const result = applyTool(state, { tool: 'access.request', capability: capability.trim() });
  state = result.state;
  toast(result.ok ? 'Granted.' : result.reason);
  render();
}

function saveNote(rel) {
  const title = ($('#noteTitle')?.value || '').trim();
  const text = $('#noteBody')?.value || '';
  if (!title) return toast('Add a title.');
  const path = rel || freshNoteRel(title);
  const result = applyTool(state, { tool: 'file.write', rel: path, name: title, text, kind: 'note' });
  if (!result.ok) return toast(result.reason);
  state = result.state;
  toast('Saved to Files.');
  route = [{ name: 'home' }, { name: 'notes' }];
  render();
}

function capture() {
  const canvas = document.createElement('canvas');
  canvas.width = 360;
  canvas.height = 480;
  paintLab(canvas.getContext('2d'), canvas.width, canvas.height);
  const stamp = String(state.clock.timeLabel).replace(':', '');
  const rel = `photos/room-${stamp}.png`;
  const result = applyTool(state, {
    tool: 'file.write', rel, name: `Room ${state.clock.timeLabel}`, text: canvas.toDataURL('image/png'), kind: 'image',
  });
  if (!result.ok) return toast(result.reason);
  state = result.state;
  toast('Saved to Files.');
  route = [{ name: 'home' }, { name: 'files' }, { name: 'viewer', rel }];
  render();
}

function paintLab(ctx, w, h) {
  const g = ctx.createLinearGradient(0, 0, 0, h * 0.72);
  g.addColorStop(0, '#d7e2dc');
  g.addColorStop(1, '#eef2ef');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = '#c5cec8';
  ctx.fillRect(0, h * 0.7, w, h * 0.3);
  ctx.save();
  ctx.translate(w / 2 + photo.x, h / 2 + photo.y);
  ctx.scale(photo.z, photo.z);
  ctx.translate(-w / 2, -h / 2);
  ctx.fillStyle = '#f7fbf9';
  ctx.fillRect(w * 0.1, h * 0.1, w * 0.28, h * 0.2);
  ctx.fillStyle = '#8fa09a';
  ctx.fillRect(w * 0.14, h * 0.62, w * 0.46, h * 0.16);
  ctx.fillStyle = '#3d8f84';
  ctx.fillRect(w * 0.2, h * 0.56, w * 0.22, h * 0.08);
  ctx.fillStyle = '#5d8668';
  ctx.beginPath();
  ctx.ellipse(w * 0.82, h * 0.7, w * 0.06, h * 0.1, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
  ctx.fillStyle = '#1c3330';
  ctx.font = '16px sans-serif';
  ctx.fillText(state.clock.timeLabel, 16, 28);
}

function toggleVideo() {
  video.playing = !video.playing;
  if (video.playing) {
    let last = performance.now();
    const step = now => {
      if (!video.playing) return;
      const dt = (now - last) / 1000;
      last = now;
      video.t = Math.min(video.dur, video.t + dt);
      if (video.t >= video.dur) video.playing = false;
      const frame = document.querySelector('.video-frame');
      const scrub = $('#scrub');
      const btn = document.querySelector('[data-act="video-toggle"]');
      const p = video.t / video.dur;
      if (frame) frame.style.setProperty('--p', String(p));
      if (scrub) scrub.value = String(Math.round(p * 1000));
      if (btn) btn.textContent = video.playing ? 'Pause' : 'Play';
      if (video.playing) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  } else {
    stopVideo(false);
    const btn = document.querySelector('[data-act="video-toggle"]');
    if (btn) btn.textContent = 'Play';
  }
}

function stopVideo(resetFlag = true) {
  if (resetFlag) video.playing = false;
  if (raf) cancelAnimationFrame(raf);
  raf = 0;
}

function onInput(e) {
  if (e.target.id === 'scrub') {
    video.playing = false;
    stopVideo(false);
    video.t = (Number(e.target.value) / 1000) * video.dur;
    const frame = document.querySelector('.video-frame');
    if (frame) frame.style.setProperty('--p', String(video.t / video.dur));
    const btn = document.querySelector('[data-act="video-toggle"]');
    if (btn) btn.textContent = 'Play';
  }
  if (e.target.id === 'utterance' && top().name === 'thread') top().draft = e.target.value;
}

function onPointerDown(e) {
  const finder = e.target.closest?.('.finder');
  if (!finder) return;
  finder.setPointerCapture?.(e.pointerId);
  pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  pinch0 = pointers.size === 2 ? pinchDist() : null;
}

function onPointerMove(e) {
  if (!pointers.has(e.pointerId)) return;
  const prev = pointers.get(e.pointerId);
  pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (pointers.size === 1) {
    photo.x = clamp(photo.x + (e.clientX - prev.x), -140, 140);
    photo.y = clamp(photo.y + (e.clientY - prev.y), -140, 140);
    applyPhotoTransform();
  } else if (pointers.size >= 2 && pinch0) {
    const d = pinchDist();
    if (d && pinch0) photo.z = clamp(photo.z * (d / pinch0), 1, 3);
    pinch0 = d;
    applyPhotoTransform();
  }
}

function onPointerUp(e) {
  pointers.delete(e.pointerId);
  pinch0 = pointers.size >= 2 ? pinchDist() : null;
}

function pinchDist() {
  const pts = [...pointers.values()];
  if (pts.length < 2) return null;
  return Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y) || null;
}

function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }

function onKey(e) {
  if (e.key === 'Escape' && overlay) {
    if (route.length > 1) back();
    else { overlay = false; render(); }
  }
}

async function boot() {
  const res = await fetch('/api/terminal');
  if (!res.ok) throw new Error('No terminal fixture');
  state = await res.json();
  delete state._hostFiles;
  state.settings = { ...defaultSettings(), ...(state.settings || {}) };
  overlay = state.settings.alwaysShowPhone !== false;
  document.body.addEventListener('click', onClick);
  document.body.addEventListener('input', onInput);
  document.body.addEventListener('pointerdown', onPointerDown);
  document.body.addEventListener('pointermove', onPointerMove);
  document.body.addEventListener('pointerup', onPointerUp);
  document.body.addEventListener('pointercancel', onPointerUp);
  document.addEventListener('keydown', onKey);
  render();
}

boot().catch(err => {
  $('#phone').textContent = err.message || 'Failed to load the phone.';
});
