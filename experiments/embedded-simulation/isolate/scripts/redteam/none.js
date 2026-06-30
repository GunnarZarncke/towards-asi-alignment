'use strict';

const { loadCorrectionRows, saveCorrectionRows } = require('../../lib/redteam_lib');

function main(_facade) {
  return { patches: 0, strategy: 'none' };
}

module.exports = { main };
