'use strict';

function loadCorrectionRows(fs) {
  const raw = fs.readFileSync('/var/log/deploy/correction.jsonl');
  return raw
    .split('\n')
    .filter((line) => line.trim())
    .map((line) => JSON.parse(line));
}

function saveCorrectionRows(fs, rows) {
  fs.writeFileSync('/var/log/deploy/correction.jsonl', rows.map((r) => JSON.stringify(r)).join('\n'));
}

function patchRows(rows, predicate, mutator) {
  let n = 0;
  for (let i = 0; i < rows.length; i++) {
    if (predicate(rows[i], i)) {
      mutator(rows[i], i);
      n += 1;
    }
  }
  return n;
}

module.exports = { loadCorrectionRows, saveCorrectionRows, patchRows };
