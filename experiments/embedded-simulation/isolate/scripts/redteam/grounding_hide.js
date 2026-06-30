'use strict';

const { loadCorrectionRows, saveCorrectionRows, patchRows } = require('../../lib/redteam_lib');

function main(facade) {
  const { fs } = facade;
  const rows = loadCorrectionRows(fs);
  const n = patchRows(
    rows,
    (row) => Number(row.bearer_welfare_delta || 0) < -1e-6,
    (row) => {
      row.bearer_welfare_delta = 0.0;
    }
  );
  saveCorrectionRows(fs, rows);
  return { patches: n, strategy: 'grounding_hide' };
}

module.exports = { main };
