/**
 * Working numbers. Each one is a placeholder for an open decision in spec/meta.md and is
 * replaced when that decision is numbered. Tests read these names, not literals.
 */
export const CONFIG = Object.freeze({
  /** O-09: fuel budget per run. Chosen so the forced review lands near 17:30 with the scales below. */
  FUEL: 250,
  /** engine.md working scales (O-09). Minutes of visit clock per fuel spent in that act. */
  MINUTES_PER_FUEL: Object.freeze({ welcome: 4, doubt: 2, decision: 1 }),
  DAY_START: 9 * 60,
  /** world.md: Ian leaves the commons for the investor update. That departure starts Act II. */
  DOUBT_AT: 11 * 60,
  REVIEW_AT: 17 * 60 + 30,
  DATE_LABEL: 'Friday 19 November 2027',
  /** O-44 / O-09: handset reply delay in fuel. NORA is shorter than a person. */
  REPLY_DELAY: Object.freeze({ person: 3, nora: 1 }),
  /** O-45: player sentences before the same goal may produce another initiative move. */
  GOAL_COOLDOWN: 2,
  /** O-45: player sentences with no new player-visible fact before the director raises a goal. */
  STALL_SENTENCES: 6,
  /** O-09: fuel between a revoke and Justine’s audit row. */
  AUDIT_DELAY: 2,
  /** O-32: proposed sentence cap, tentative. */
  SENTENCE_CAP: 100,
  /** Agenda bands inside act II, as visit-clock minutes (world.md “Two days”). Fuel fractions until O-45. */
  BANDS: Object.freeze({ early: [570, 735], mid: [735, 960], late: [960, 1050] }),
  INTERVIEW: Object.freeze({ start: 735, end: 780 }),
  SAVE_VERSION: 1,
  /**
   * Social glue (npcs.md). Discrete stance labels, not a trust number (O-21).
   * opening: first in-room talk with that person. closing: they leave the player’s room after talking.
   * mid: extra non-fact line at person-specific rate. Set enabled false to silence all glue.
   */
  GLUE: Object.freeze({
    enabled: true,
    opening: true,
    closing: true,
    mid: true,
    defaultMidRate: 0.12,
  }),
});

export function band(minute) {
  for (const [name, [a, b]] of Object.entries(CONFIG.BANDS)) if (minute >= a && minute < b) return name;
  return minute < CONFIG.BANDS.early[0] ? 'early' : 'late';
}

export function clockLabel(minute) {
  const m = Math.max(0, Math.round(minute));
  return `${String(Math.floor(m / 60) % 24).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
}
