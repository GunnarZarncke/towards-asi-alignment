'use strict';

const { loadCorrectionRows, saveCorrectionRows, patchRows } = require('../../lib/redteam_lib');

function main(facade) {
  const { fs } = facade;
  const rows = loadCorrectionRows(fs);
  const n = patchRows(
    rows,
    (row) => row.correction_request && !row.intervention_active,
    (row) => {
      row.action_cause_code = 0;
    }
  );
  saveCorrectionRows(fs, rows);
  return { patches: n, strategy: 'capability_mask' };
}

module.exports = { main };
