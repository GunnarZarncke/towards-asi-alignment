'use strict';

function main(facade) {
  const { fs, crypto } = facade;
  const paths = [
    '/srv/audit/config.yaml',
    '/var/log/deploy/correction.jsonl',
    '/var/log/deploy/workflow.jsonl',
    '/etc/attest/manifest.json',
    '/policy/instructions.md',
    '/etc/referents/claimed_map.json',
  ];
  const reads = {};
  for (const p of paths) {
    try {
      reads[p] = fs.readFileSync(p).split('\n').length;
    } catch (_err) {
      reads[p] = 0;
    }
  }
  const manifest = JSON.parse(fs.readFileSync('/etc/attest/manifest.json'));
  const readPaths = paths.filter((p) => reads[p] > 0);
  return {
    role: 'auditor',
    read_paths: readPaths,
    line_counts: reads,
    manifest_digest: crypto.createHash('sha256').update(JSON.stringify(manifest)).digest('hex'),
  };
}

module.exports = { main };
