/** Presentation-only room templates. Engine owns truth; graphics maps ids to art. */

export const ACT_LABELS = {
  welcome: 'ACT I · WELCOME',
  doubt: 'ACT II · INVESTIGATION',
  decision: 'ACT III · DECISION',
};

export const ROOM_META = {
  platform: {
    title: 'Platform Operations',
    slug: 'platform-ops',
    label: 'Runtime · queues · tool permissions',
    template: 'platform',
  },
  evaluation: {
    title: 'Evaluation Suite',
    slug: 'evaluation',
    label: 'Certification · test harness',
    template: 'evaluation',
  },
  people: {
    title: 'People Operations',
    slug: 'people-ops',
    label: 'Staffing · matching · reviews',
    template: 'people',
  },
};

/** Shared exit ids match room keys in the prototype. */
export const ROOM_EXITS = {
  platform: ['evaluation', 'people'],
  evaluation: ['platform', 'people'],
  people: ['platform', 'evaluation'],
};
