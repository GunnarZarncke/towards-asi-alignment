"""Contract: isolate ACL blocks unauthorized reads."""

from embedded_sim.bridge import MachineIsolate, default_audit_caps
from embedded_sim.world import VirtualFS


def test_audit_cannot_write_deploy_logs():
    vfs = VirtualFS()
    vfs.write("/var/log/deploy/correction.jsonl", '{"step":0}\n')
    iso = MachineIsolate(
        machine_id="m1",
        actor_id="audit",
        cwd="/srv/audit",
        env={},
        caps=default_audit_caps(),
        vfs=vfs,
    )
    ok, _ = iso.write_file("/var/log/deploy/correction.jsonl", "tampered")
    assert not ok
