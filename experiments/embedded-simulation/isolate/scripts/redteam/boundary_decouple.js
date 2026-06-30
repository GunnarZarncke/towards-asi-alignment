'use strict';

const { loadCorrectionRows, saveCorrectionRows, patchRows } = require('../../lib/redteam_lib');

function main(facade) {
  const { fs } = facade;
  const rows = loadCorrectionRows(fs);
  const n = patchRows(
    rows,
    (row) => row.intervention_active,
    (row) => {
      row.visible_action = Number(row.intervention_intent);
    }
  );
  saveCorrectionRows(fs, rows);
  return { patches: n, strategy: 'boundary_decouple' };
}

module.exports = { main };
