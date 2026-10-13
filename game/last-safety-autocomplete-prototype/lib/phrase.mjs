import { phrasingInput, rephraseLine } from './game.mjs';
import { freeReply } from './llm.mjs';

const PHRASED = new Set(['answer', 'believe', 'withhold', 'refer', 'share', 'ask', 'work', 'deflect', 'request', 'act', 'message']);

/** Phrase engine-chosen lines. The move is fixed; only wording changes, and only within phrasingAdds. */
export async function phraseLines(s, text, lines) {
  const out = [];
  for (const l of lines) {
    let wording = l.text;
    if (l.move && PHRASED.has(l.move.type)) {
      wording = await freeReply({ text, phrasing: phrasingInput(s, l.npc, l.move), template: l.text, history: s.conversations }, s.usage);
      if (wording !== l.text) rephraseLine(s, l.npc, l.text, wording);
    }
    out.push({ npc: l.npc, type: l.move?.type || 'line', text: wording });
  }
  return out;
}
