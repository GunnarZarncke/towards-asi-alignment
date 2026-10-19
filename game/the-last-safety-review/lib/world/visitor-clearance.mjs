/**
 * Visitor badge levels (SEC-ARCH-04 §4): inactive handset → commons only;
 * host confirmation → hub; introduction or stated review reason → north spine + invited wings.
 */
import { START_CLEARANCE, HUB_CLEARANCE, VISITOR_CLEARANCE } from '../floorplan.mjs';
import { evaluate } from './predicates.mjs';
import { makeCtx } from './npcs.mjs';

const NORTH_SPINE =
  'or(event(visitor_introduced_justine), told(justine, any, by=player))';

/** Recompute `s.clearance` from Lab Access activation and trust predicates. */
export function syncVisitorClearance(s) {
  if (!s.labAccessActive) {
    s.clearance = START_CLEARANCE;
    return;
  }
  const ctx = makeCtx(s, 'player');
  s.clearance = evaluate(NORTH_SPINE, ctx) ? VISITOR_CLEARANCE : HUB_CLEARANCE;
}
