/** Browser-safe speech vs command-line detection (shared with lib/text/tab-complete.mjs). */

export const CONSOLE_COMMANDS = new Set([
  'help', '?', 'look', 'l', 'exits', 'doors', 'go', 'walk', 'read', 'inspect', 'x', 'records',
  'to', 'face', 'who', 's', 'suggest', 'think', 'keep', 'close', 'know', 'k', 'file', 'commit',
  'phone', 'p', 'files', 'open', 'msg', 'dm', 'access', 'request', 'note', 'share', 'contacts',
  'calendar', 'status', 'quit', 'save', 'load', 'reset',
]);

/** @returns {{ utterance: string, prefix: string } | null} */
export function utteranceSlice(line) {
  const raw = String(line ?? '');
  const say = raw.match(/^say\s+(.*)$/i);
  if (say) return { utterance: say[1], prefix: raw.slice(0, raw.length - say[1].length) };
  const trimmed = raw.trimStart();
  const verb = trimmed.match(/^(\S+)/)?.[1]?.toLowerCase();
  if (verb && CONSOLE_COMMANDS.has(verb)) return null;
  if (/^\d+$/.test(trimmed)) return null;
  return { utterance: raw, prefix: '' };
}
