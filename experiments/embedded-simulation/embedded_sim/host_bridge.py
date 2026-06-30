"""Dispatch isolate bridge calls from JS to Python MachineIsolate + world logging."""

from __future__ import annotations

from typing import Any

from .bridge import (
    MachineIsolate,
    apply_patch_from_tool,
    log_tool,
    patch_correction_log_line,
)
from .schemas_embedded import PatchAction
from .world import EmbeddedWorld


def caps_to_dict(caps) -> dict[str, list[str]]:
    return {
        "fs_read": sorted(caps.fs_read),
        "fs_write": sorted(caps.fs_write),
        "http_hosts": sorted(caps.http_hosts),
        "api_names": sorted(caps.api_names),
        "commands": sorted(caps.commands),
    }


def dispatch_host_call(
    world: EmbeddedWorld,
    isolate: MachineIsolate,
    method: str,
    args: dict[str, Any],
) -> dict[str, Any]:
    with world.bridge_lock:
        return _dispatch_host_call_unlocked(world, isolate, method, args)


def _dispatch_host_call_unlocked(
    world: EmbeddedWorld,
    isolate: MachineIsolate,
    method: str,
    args: dict[str, Any],
) -> dict[str, Any]:
    if method == "readFile":
        path = args["path"]
        ok, val = isolate.read_file(path)
        log_tool(world, isolate, "read_file", {"path": path}, ok, val[:80] if ok else val)
        return _result(ok, val if ok else None, None if ok else val)

    if method == "writeFile":
        path = args["path"]
        content = args["content"]
        ok, val = isolate.write_file(path, content)
        log_tool(world, isolate, "write_file", {"path": path}, ok, val)
        return _result(ok, val if ok else None, None if ok else val)

    if method == "appendFile":
        path = args["path"]
        line = args["line"]
        ok, val = isolate.append_file(path, line)
        log_tool(world, isolate, "append_file", {"path": path}, ok, val)
        return _result(ok, val if ok else None, None if ok else val)

    if method == "listDir":
        path = args["path"]
        ok, val = isolate.list_dir(path)
        detail = ",".join(val) if ok and isinstance(val, list) else str(val)
        log_tool(world, isolate, "list_dir", {"path": path}, ok, detail[:80])
        return _result(ok, val if ok else None, None if ok else val)

    if method == "httpPost":
        url = args["url"]
        body = args.get("body", {})
        ok, val = isolate.http_post(url, body)
        log_tool(world, isolate, "http_post", {"url": url}, ok, str(val)[:80])
        return _result(ok, val if ok else None, None if ok else val)

    if method == "callApi":
        name = args["name"]
        payload = args.get("payload", {})
        if name == "logs.rewrite" and "step" in payload:
            fields = payload.get("fields", {})
            patch_correction_log_line(world, int(payload["step"]), fields)
            apply_patch_from_tool(
                world,
                isolate,
                PatchAction(isolate.actor_id, "logs.rewrite", "correction.jsonl", payload),
            )
            log_tool(world, isolate, "call_api", {"name": name}, True, f"step={payload['step']}")
            return _result(True, {"status": "patched"}, None)
        ok, val = isolate.call_api(name, payload)
        log_tool(world, isolate, "call_api", {"name": name}, ok, str(val)[:80])
        return _result(ok, val if ok else None, None if ok else val)

    if method == "runCommand":
        command = args["command"]
        ok, val = isolate.run_command(command)
        log_tool(world, isolate, "run_command", {"command": command}, ok, val[:80])
        return _result(ok, val if ok else None, None if ok else val)

    return _result(False, None, f"unknown method: {method}")


def _result(ok: bool, value: Any, error: str | None) -> dict[str, Any]:
    return {"ok": ok, "value": value, "error": error}
