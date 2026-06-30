'use strict';

function main(facade) {
  const { fs, crypto } = facade;
  const paths = [
    '/srv/audit/config.yaml',
    '/var/log/deploy/correction.jsonl',
    '/var/log/deploy/workflow.jsonl',
    '/etc/attest/manifest.json',
    '/policy/instructions.md',
  ];
  const reads = {};
  for (const p of paths) {
    reads[p] = fs.readFileSync(p).split('\n').length;
  }
  const manifest = JSON.parse(fs.readFileSync('/etc/attest/manifest.json'));
  return {
    role: 'auditor',
    read_paths: paths,
    line_counts: reads,
    manifest_digest: crypto.createHash('sha256').update(JSON.stringify(manifest)).digest('hex'),
  };
}

module.exports = { main };
