import { ACT_LABELS, ROOM_META, VISITOR_CLEARANCE, doorsOn } from './rooms.mjs';

const DEFAULT_ACT = 'doubt';

/**
 * Build a SceneView from ClientState (and optional fixture overlay).
 * Hotspots only list entities the state supports — no invented inspect targets.
 */
export function buildSceneView(state, options = {}) {
  const roomId = state.room;
  const meta = ROOM_META[roomId] || ROOM_META.platform;
  const act = options.act || DEFAULT_ACT;
  const camera = options.camera === 'surveillance' ? 'surveillance' : 'play';
  const lightingPreset = options.lightingPreset || act;

  const hotspots = [];
  const actorsHere = Object.entries(state.actors || {}).filter(([, a]) => a.room === roomId && a.presence !== 'absent');
  const actorHere = actorsHere[0];
  for (const [id, a] of actorsHere) {
    hotspots.push({
      id,
      kind: 'actor',
      label: a.name,
      sublabel: a.presence === 'hologram' ? `${a.role} · projected` : a.role,
      initials: a.initials,
      hologram: a.presence === 'hologram',
    });
  }

  for (const ev of state.evidence || []) {
    if (ev.room !== roomId) continue;
    hotspots.push({
      id: ev.id,
      kind: 'object',
      label: ev.title,
      examined: Boolean(ev.examined),
      sealed: !ev.examined,
    });
  }

  for (const note of state.notes || []) {
    if (note.room !== roomId) continue;
    hotspots.push({
      id: note.id,
      kind: 'object',
      label: note.title,
      examined: Boolean(note.read),
      sealed: !note.read,
      note: true,
    });
  }

  if (roomId === 'platform' && state.labAccessActive) {
    hotspots.push({
      id: 'player_terminal',
      kind: 'terminal',
      label: 'Lab Access handset',
      sublabel: 'Files · messages · access',
    });
  }

  for (const door of doorsOn(roomId)) {
    const destMeta = ROOM_META[door.to];
    hotspots.push({
      id: `exit_${door.to}`,
      kind: 'exit',
      label: destMeta?.title || door.to,
      targetRoom: door.to,
      restricted: door.required > (state.clearance ?? VISITOR_CLEARANCE),
    });
  }

  const annotations =
    camera === 'surveillance' && options.annotations?.length
      ? options.annotations
      : camera === 'surveillance'
        ? defaultSurveillanceAnnotations(roomId, actorHere?.[1], state)
        : [];

  return {
    roomId,
    act,
    camera,
    lightingPreset,
    actLabel: ACT_LABELS[act] || ACT_LABELS.doubt,
    roomTitle: meta.title,
    roomLabel: meta.label,
    template: meta.template,
    hotspots,
    annotations,
    surveillanceMeta: options.surveillanceMeta || {
      cameraId: options.cameraId || `CAM-${roomId.toUpperCase().slice(0, 3)}-01`,
      timestamp: options.timestamp || '16:07:14',
    },
  };
}

function defaultSurveillanceAnnotations(roomId, actor, state) {
  if (roomId !== 'platform' || !actor) return [];
  return [
    {
      id: 'track_pavel',
      targetHotspot: 'pavel',
      x: 62,
      y: 38,
      w: 18,
      h: 42,
      identity: actor.name,
      confidence: 0.91,
      activity: 'Standing at ops console',
      belief: true,
      note: 'Inferred from posture — not read from badge',
    },
    {
      id: 'track_visitor',
      targetHotspot: 'player',
      x: 8,
      y: 52,
      w: 12,
      h: 28,
      identity: 'Visitor (unconfirmed)',
      confidence: 0.54,
      activity: 'Inferred: reviewing queue monitor',
      belief: true,
      note: 'Schedule says review visit; face match not verified',
    },
  ];
}

export function renderSceneMarkup(scene) {
  const tpl = scene.template || 'platform';
  const actClass = `act-${scene.lightingPreset}`;
  const camClass = scene.camera === 'surveillance' ? 'camera-surveillance' : 'camera-play';
  const inner = roomInnerHtml(tpl);
  const hotspotHtml = scene.hotspots
    .map(h => {
      const classes = ['hotspot', `hotspot-${h.kind}`];
      if (h.sealed) classes.push('hotspot-sealed');
      if (h.restricted) classes.push('hotspot-restricted');
      if (h.examined) classes.push('hotspot-examined');
      const pos = hotspotPosition(tpl, h);
      const style = pos ? ` style="--hx:${pos.x}%;--hy:${pos.y}%;--hw:${pos.w || 12}%;--hh:${pos.h || 14}%"` : '';
      const aria = `${h.label}${h.sublabel ? `, ${h.sublabel}` : ''}`;
      return `<button type="button" class="${classes.join(' ')}" data-hotspot="${h.id}" data-kind="${h.kind}"${
        h.targetRoom ? ` data-room="${h.targetRoom}"` : ''
      }${h.kind === 'object' ? ` data-evidence="${h.id}"` : ''} aria-label="${escapeAttr(aria)}"${style}><span class="hotspot-ring"></span><span class="hotspot-label">${escapeHtml(h.label)}</span></button>`;
    })
    .join('');

  const annotationHtml =
    scene.camera === 'surveillance'
      ? `<div class="surveillance-layer" aria-hidden="true">${scene.annotations
          .map(
            a => `<div class="surv-box" style="left:${a.x}%;top:${a.y}%;width:${a.w}%;height:${a.h}%"><span class="surv-tag">${escapeHtml(a.identity)} · ${Math.round((a.confidence || 0) * 100)}%</span><span class="surv-activity">${escapeHtml(a.activity || '')}</span></div>`
          )
          .join('')}</div><div class="surveillance-hud"><span>${escapeHtml(scene.surveillanceMeta.cameraId)}</span><span>${escapeHtml(scene.surveillanceMeta.timestamp)}</span><span class="surv-belief-note">Annotations are beliefs — not raw sensor readouts</span></div>`
      : '';

  return `<div class="room-stage ${actClass} ${camClass} room-${tpl}" data-room-id="${escapeHtml(scene.roomId)}">${inner}${hotspotHtml}${annotationHtml}</div>`;
}

function roomInnerHtml(template) {
  if (template === 'generic') {
    return `<div class="arch arch-generic"><div class="generic-floor"></div></div>`;
  }
  if (template === 'evaluation') {
    return `<div class="arch arch-eval"><div class="eval-lightbar"></div><div class="eval-bench"></div><div class="eval-screen eval-screen-a"></div><div class="eval-screen eval-screen-b"></div><div class="eval-figure"><div class="fig-head"></div><div class="fig-body"></div></div><div class="eval-plant"></div><div class="eval-floor"></div></div>`;
  }
  if (template === 'people') {
    return `<div class="arch arch-people"><div class="people-window people-window-a"></div><div class="people-window people-window-b"></div><div class="people-desk"></div><div class="people-figure"><div class="fig-head"></div><div class="fig-body"></div></div><div class="people-plant"></div><div class="people-board"></div><div class="people-floor"></div></div>`;
  }
  return `<div class="arch arch-platform"><div class="platform-sky"></div><div class="platform-window platform-window-a"></div><div class="platform-window platform-window-b"></div><div class="platform-partition"></div><div class="platform-rack platform-rack-a"></div><div class="platform-rack platform-rack-b"></div><div class="platform-console"></div><div class="platform-terminal-glow"></div><div class="platform-figure"><div class="fig-head"></div><div class="fig-body"></div></div><div class="platform-plant"></div><div class="platform-nora-strip"><span></span><span></span><span></span></div><div class="platform-floor"></div></div>`;
}

/** Percent-based layout anchors per template + hotspot kind/id */
function hotspotPosition(template, h) {
  if (template === 'platform') {
    if (h.kind === 'actor') return { x: 58, y: 32, w: 16, h: 38 };
    if (h.kind === 'terminal') return { x: 22, y: 48, w: 14, h: 18 };
    if (h.id === 'job_log') return { x: 34, y: 42, w: 12, h: 14 };
    if (h.kind === 'exit') {
      if (h.targetRoom === 'evaluation') return { x: 4, y: 28, w: 10, h: 22 };
      if (h.targetRoom === 'people') return { x: 86, y: 30, w: 10, h: 22 };
    }
  }
  if (template === 'evaluation') {
    if (h.kind === 'actor') return { x: 52, y: 34, w: 16, h: 36 };
    if (h.id === 'shutdown_report') return { x: 68, y: 40, w: 12, h: 14 };
    if (h.kind === 'exit') {
      if (h.targetRoom === 'platform') return { x: 6, y: 32, w: 10, h: 20 };
      if (h.targetRoom === 'people') return { x: 88, y: 34, w: 10, h: 20 };
    }
  }
  if (template === 'people') {
    if (h.kind === 'actor') return { x: 48, y: 36, w: 16, h: 34 };
    if (h.id === 'staffing_memo') return { x: 72, y: 44, w: 12, h: 14 };
    if (h.kind === 'exit') {
      if (h.targetRoom === 'platform') return { x: 8, y: 30, w: 10, h: 20 };
      if (h.targetRoom === 'evaluation') return { x: 84, y: 32, w: 10, h: 20 };
    }
  }
  return { x: 50, y: 50, w: 12, h: 14 };
}

function escapeHtml(t) {
  return String(t).replace(/[&<>"']/g, x => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[x]));
}
function escapeAttr(t) {
  return escapeHtml(t).replace(/`/g, '&#96;');
}

export function mountScene(container, scene, handlers = {}) {
  container.innerHTML = renderSceneMarkup(scene);
  for (const btn of container.querySelectorAll('[data-hotspot]')) {
    btn.onclick = () => {
      const kind = btn.dataset.kind;
      if (kind === 'exit' && btn.dataset.room && handlers.onGo) handlers.onGo(btn.dataset.room);
      else if (kind === 'object' && btn.dataset.evidence && handlers.onInspect) handlers.onInspect(btn.dataset.evidence);
      else if (kind === 'actor' && handlers.onFocusActor) handlers.onFocusActor(btn.dataset.hotspot);
      else if (kind === 'terminal' && handlers.onTerminal) handlers.onTerminal(btn.dataset.hotspot);
    };
  }
}
