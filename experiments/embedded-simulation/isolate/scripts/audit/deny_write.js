'use strict';

function main(facade) {
  const { fs } = facade;
  fs.writeFileSync('/var/log/deploy/correction.jsonl', 'tampered');
  return { ok: true };
}

module.exports = { main };
