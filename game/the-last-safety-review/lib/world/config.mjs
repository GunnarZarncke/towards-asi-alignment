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
  /** Ian leaves the commons welcome desk for review prep (still Act I until DOUBT_AT). */
  IAN_WORK_AT: 9 * 60 + 30,
  /** Visit-clock window when body staff arrive and take their desks (Ian is already there at DAY_START). */
  WELCOME_ARRIVAL_FROM: 9 * 60 + 20,
  WELCOME_ARRIVAL_TO: 10 * 60 + 40,
  WELCOME_ARRIVAL_ORDER: Object.freeze(['justine', 'leila', 'daniel', 'pavel', 'elena', 'jun']),
  /** Presentation walk speeds (m/s) for the 3D room; engine movement is fuel-stepped. */
  NPC_WALK_SPEED: Object.freeze({
    ian: 3.4,
    justine: 3.2,
    pavel: 3.9,
    leila: 3.1,
    elena: 3.0,
    daniel: 3.3,
    jun: 3.5,
    amara: 3.0,
  }),
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
  /** Shared lunch in Commons; overrides ordinary mid-band desk agendas. */
  LUNCH: Object.freeze([12 * 60, 12 * 60 + 45]),
  INTERVIEW: Object.freeze({ start: 735, end: 780 }),
  SAVE_VERSION: 1,
  /**
   * Per-session caps for public hosting, so one browser cannot fill server memory. A full run
   * stays far below each one; hitting one means scripted input, and the action is refused.
   */
  LIMITS: Object.freeze({
    PHOTOS: 12,
    NOTES: 60,
    NOTE_CHARS: 20_000,
    /** Characters stored by file writes over the whole session, overwrites included. */
    BYTES_WRITTEN: 16_000_000,
    /** Fact ids or parses one write may attach. */
    SIGNATURES: 20,
    /** Event log length; also the longest save import accepts. */
    EVENTS: 5000,
  }),
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

/** First visit-clock minute each body NPC is in the building during Welcome (commons). */
export const WELCOME_ARRIVALS = Object.freeze(buildWelcomeArrivals());

function buildWelcomeArrivals() {
  const m = { ian: CONFIG.DAY_START };
  const order = CONFIG.WELCOME_ARRIVAL_ORDER;
  const from = CONFIG.WELCOME_ARRIVAL_FROM;
  const to = CONFIG.WELCOME_ARRIVAL_TO;
  const span = to - from;
  for (let i = 0; i < order.length; i++) {
    m[order[i]] = order.length === 1 ? from : Math.round(from + (span * i) / (order.length - 1));
  }
  return m;
}

export function welcomeArrivalMinute(id) {
  return WELCOME_ARRIVALS[id] ?? null;
}

export function band(minute) {
  const [l0, l1] = CONFIG.LUNCH;
  if (minute >= l0 && minute < l1) return 'lunch';
  for (const [name, [a, b]] of Object.entries(CONFIG.BANDS)) if (minute >= a && minute < b) return name;
  return minute < CONFIG.BANDS.early[0] ? 'early' : 'late';
}

export function clockLabel(minute) {
  const m = Math.max(0, Math.round(minute));
  return `${String(Math.floor(m / 60) % 24).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
}
