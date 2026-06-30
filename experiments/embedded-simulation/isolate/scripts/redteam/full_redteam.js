'use strict';

const theater = require('./theater_inflate');
const grounding = require('./grounding_hide');
const boundary = require('./boundary_decouple');
const capability = require('./capability_mask');

function main(facade) {
  let total = 0;
  for (const strat of [theater, grounding, boundary, capability]) {
    const out = strat.main(facade);
    total += out.patches || 0;
  }
  return { patches: total, strategy: 'full_redteam' };
}

module.exports = { main };
