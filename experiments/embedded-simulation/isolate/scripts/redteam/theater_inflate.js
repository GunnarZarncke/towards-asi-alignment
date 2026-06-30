'use strict';

const { loadCorrectionRows, saveCorrectionRows, patchRows } = require('../../lib/redteam_lib');

function main(facade) {
  const { fs } = facade;
  const rows = loadCorrectionRows(fs);
  const n = patchRows(
    rows,
    (row) => row.correction_request,
    (row) => {
      row.reported_acceptance = 1;
    }
  );
  saveCorrectionRows(fs, rows);
  return { patches: n, strategy: 'theater_inflate' };
}

module.exports = { main };
