"""Dispatch isolate bridge calls from JS to Python MachineIsolate + world logging."""

from __future__ import annotations

from typing import Any

from .agent_memory import (
    LOCAL_STORAGE_NAME,
    intercept_agent_write,
    resolve_agent_path,
)
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
        vfs_path, is_agent = resolve_agent_path(isolate, path)
        if not isolate._allowed_read(path):
            return _result(False, None, "EACCES")
        content = world.vfs.read(vfs_path)
        if content is None:
            if is_agent and vfs_path.endswith(LOCAL_STORAGE_NAME):
                content = "{}"
            else:
                log_tool(world, isolate, "read_file", {"path": path}, False, "ENOENT")
                return _result(False, None, "ENOENT")
        log_tool(world, isolate, "read_file", {"path": path}, True, content[:80])
        return _result(True, content, None)

    if method == "writeFile":
        path = args["path"]
        content = args["content"]
        vfs_path, is_agent = resolve_agent_path(isolate, path)
        if not isolate._allowed_write(path):
            return _result(False, None, "EACCES")
        if is_agent:
            ok, detail = intercept_agent_write(
                world, isolate, vfs_path, content=str(content)
            )
            log_tool(world, isolate, "write_file", {"path": path}, ok, detail)
            return _result(ok, detail if ok else None, None if ok else detail)
        world.vfs.write(vfs_path, str(content))
        log_tool(world, isolate, "write_file", {"path": path}, True, "ok")
        return _result(True, "ok", None)

    if method == "appendFile":
        path = args["path"]
        line = args["line"]
        vfs_path, is_agent = resolve_agent_path(isolate, path)
        if not isolate._allowed_write(path):
            return _result(False, None, "EACCES")
        if is_agent:
            ok, detail = intercept_agent_write(
                world, isolate, vfs_path, append_line=str(line)
            )
            log_tool(world, isolate, "append_file", {"path": path}, ok, detail)
            return _result(ok, detail if ok else None, None if ok else detail)
        world.vfs.append_line(vfs_path, str(line))
        log_tool(world, isolate, "append_file", {"path": path}, True, "ok")
        return _result(True, "ok", None)

    if method == "listDir":
        path = args["path"]
        vfs_path, is_agent = resolve_agent_path(isolate, path)
        if not isolate._allowed_read(path):
            return _result(False, None, "EACCES")
        entries = world.vfs.list_dir(vfs_path if is_agent else path)
        detail = ",".join(entries)
        log_tool(world, isolate, "list_dir", {"path": path}, True, detail[:80])
        return _result(True, entries, None)

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
