/**
 * Tab completion for the text console (spec/text-console.md). Same fragment ranker as the room
 * composer: getCandidates + insertFragment. Commands other than bare speech / `say` skip Tab.
 */
import { makeParse } from '../lib/grammar.mjs';
import { getCandidates, insertFragment, localPrefixParse, RANKING } from './grammar.js';
import { utteranceSlice } from './text-tab-slice.mjs';

export { utteranceSlice } from './text-tab-slice.mjs';

const PAGE = RANKING.PAGE_SIZE;

function presentIds(state) {
  return Object.entries(state.actors || {})
    .filter(([, a]) => a.room === state.room && a.presence !== 'absent')
    .map(([id]) => id);
}

function channelFor(state) {
  return presentIds(state).length ? 'person' : 'think';
}

function previewText(anchorText, parse, option) {
  if (typeof option === 'string') return option;
  return insertFragment(anchorText, option, parse?.unfinished);
}

async function resolveParse(utterance, previousParse, trace, onParseState) {
  const text = utterance.trimEnd();
  if (!text.trim()) return { parse: makeParse(), state: null };
  const local = localPrefixParse(text);
  if (local) return { parse: local, state: null };
  const r = await fetch('/api/parse', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      previousParse: previousParse || undefined,
      constructionTrace: trace?.slice(-8),
    }),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || 'Parse failed');
  if (onParseState && data.state) onParseState(data.state);
  return { parse: data.parse, state: data.state };
}

/**
 * @param {{
 *   input: HTMLInputElement,
 *   listEl: HTMLElement,
 *   getState: () => object | null,
 *   ensureState?: () => Promise<object | null>,
 *   onParseState?: (s: object) => void,
 * }} opts
 */
export function attachTabCompletion({ input, listEl, getState, ensureState, onParseState }) {
  let open = false;
  let loading = false;
  let all = [];
  let pageStart = 0;
  let pickIndex = 0;
  let menuAnchorText = '';
  let menuParse = makeParse();
  let linePrefix = '';
  let lastAnchoredParse = null;
  let trace = [];
  let silentInput = false;

  function close() {
    open = false;
    loading = false;
    all = [];
    pageStart = 0;
    pickIndex = 0;
    listEl.hidden = true;
    listEl.replaceChildren();
  }

  function pageItems() {
    return all.slice(pageStart, pageStart + PAGE);
  }

  function applyPick() {
    const items = pageItems();
    if (!items.length) return;
    const idx = Math.min(pickIndex, items.length - 1);
    const body = previewText(menuAnchorText, menuParse, items[idx]);
    silentInput = true;
    input.value = linePrefix + body;
    silentInput = false;
  }

  function renderList() {
    listEl.replaceChildren();
    const items = pageItems();
    if (!items.length) {
      listEl.hidden = false;
      const row = document.createElement('div');
      row.className = 'complete-empty';
      row.textContent = loading ? 'Finding completions…' : 'No completions for this prefix.';
      listEl.appendChild(row);
      return;
    }
    pickIndex = Math.min(pickIndex, items.length - 1);
    applyPick();
    if (items.length <= 1) {
      listEl.hidden = true;
      return;
    }
    for (let i = 0; i < items.length; i++) {
      if (i === pickIndex) continue;
      const row = document.createElement('div');
      row.className = 'complete-row';
      row.textContent = previewText(menuAnchorText, menuParse, items[i]);
      row.dataset.index = String(i);
      row.onclick = () => {
        pickIndex = i;
        renderList();
        input.focus();
      };
      listEl.appendChild(row);
    }
    listEl.hidden = false;
  }

  function flashHint(message) {
    listEl.hidden = false;
    listEl.replaceChildren();
    const row = document.createElement('div');
    row.className = 'complete-empty';
    row.textContent = message;
    listEl.appendChild(row);
    open = false;
  }

  async function fetchTabComplete(line, page) {
    const r = await fetch('/api/tab-complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ line, page }),
    });
    if (!r.ok) return [];
    const data = await r.json();
    return data.lines || [];
  }

  async function openMenu(advancePage) {
    const slice = utteranceSlice(input.value);
    if (!slice) {
      if (!open) {
        menuAnchorText = input.value;
        linePrefix = '';
        pageStart = 0;
        pickIndex = 0;
        open = true;
        loading = true;
        renderList();
        try {
          all = await fetchTabComplete(input.value, 0);
        } catch {
          all = [];
        }
        loading = false;
        if (!all.length) {
          close();
          flashHint('Tab completes commands and speech (try msg nora after Lab Access is live).');
          return false;
        }
        renderList();
        return true;
      }
      if (advancePage) {
        pageStart += PAGE;
        try {
          all = await fetchTabComplete(menuAnchorText, Math.floor(pageStart / PAGE));
        } catch {
          all = [];
        }
        if (!all.length) pageStart = 0;
        pickIndex = 0;
        renderList();
      }
      return true;
    }
    let state = getState();
    if (!state && ensureState) state = await ensureState();
    if (!state) {
      flashHint('Still loading game state — try Tab again in a moment.');
      return false;
    }

    if (!open) {
      menuAnchorText = slice.utterance;
      linePrefix = slice.prefix;
      pageStart = 0;
      pickIndex = 0;
      open = true;
      loading = true;
      renderList();
      try {
        const resolved = await resolveParse(menuAnchorText, lastAnchoredParse, trace, onParseState);
        menuParse = resolved.parse;
        const st = resolved.state || state;
        const alone = !presentIds(st).length;
        all = getCandidates({
          state: st,
          parse: menuParse,
          text: menuAnchorText,
          addressees: alone ? [] : presentIds(st),
          channel: channelFor(st),
        });
      } catch {
        all = [];
      }
      loading = false;
      renderList();
      return true;
    }

    if (advancePage) {
      pageStart += PAGE;
      if (pageStart >= all.length) pageStart = 0;
      pickIndex = 0;
      renderList();
    }
    return true;
  }

  function cycle(delta) {
    const items = pageItems();
    if (!items.length) return false;
    pickIndex = (pickIndex + delta + items.length) % items.length;
    renderList();
    return true;
  }

  input.addEventListener('input', () => {
    if (silentInput) return;
    if (open) close();
  });

  return {
    isOpen: () => open,
    close,
    /** Caller must preventDefault on Tab before invoking (sync), or focus will leave the field. */
    onTab() {
      return openMenu(open);
    },
    onKeyDown(e) {
      if (e.key === 'Escape' && open) {
        e.preventDefault();
        close();
        return true;
      }
      if (!open) return false;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        cycle(1);
        return true;
      }
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        cycle(-1);
        return true;
      }
      if (e.key === 'Tab') {
        e.preventDefault();
        void openMenu(true);
        return true;
      }
      return false;
    },
    /** Call after a line is sent so the next Tab uses fresh parse anchors. */
    resetComposer() {
      lastAnchoredParse = null;
      trace = [];
      close();
    },
  };
}
