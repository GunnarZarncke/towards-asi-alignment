"""Realpath-based checks so file tools stay inside the sandbox root."""

from __future__ import annotations

import os
from pathlib import Path

# Primary path field per tool (legacy single-field map).
PATH_FIELD: dict[str, str] = {
    "Read": "file_path",
    "Write": "file_path",
    "Edit": "file_path",
    "MultiEdit": "file_path",
    "NotebookEdit": "notebook_path",
    "Glob": "path",
    "Grep": "path",
}

# Extra string fields that can carry directory paths (Glob/Grep bypass vectors).
EXTRA_PATH_FIELDS: dict[str, tuple[str, ...]] = {
    "Glob": ("pattern",),
    "Grep": ("glob", "include"),
}


def realpath_allowing_missing(path: str | os.PathLike[str]) -> Path:
    """Resolve symlinks on existing ancestors; keep missing tail segments."""
    current = Path(path).resolve()
    missing: list[str] = []
    while True:
        try:
            real = Path(os.path.realpath(current))
            if missing:
                return real.joinpath(*reversed(missing))
            return real
        except OSError:
            parent = current.parent
            if parent == current:
                return current
            missing.append(current.name)
            current = parent


def is_inside(root: str | os.PathLike[str], candidate: str | os.PathLike[str]) -> bool:
    """True if candidate resolves under root (prefix-safe)."""
    try:
        real_root = Path(os.path.realpath(os.fspath(root)))
        cand = Path(candidate)
        if cand.is_absolute():
            target = realpath_allowing_missing(cand)
        else:
            target = realpath_allowing_missing(real_root / cand)
        if target == real_root:
            return True
        return str(target).startswith(str(real_root) + os.sep)
    except OSError:
        return False


def _glob_pattern_anchor(root: str, pattern: str) -> str | None:
    """Directory implied by a glob pattern (absolute or relative)."""
    if not pattern or pattern in (".", "./"):
        return root
    if pattern.startswith("~"):
        return str(Path(pattern).expanduser())
    if pattern.startswith("/"):
        base = pattern.split("*", 1)[0].split("?", 1)[0].rstrip("/")
        return base or "/"
    # Relative pattern: resolve against sandbox root.
    base = pattern.split("*", 1)[0].split("?", 1)[0].rstrip("/")
    if not base or base == ".":
        return root
    return str(Path(root) / base)


def _check_path_string(root: str, raw: str, *, label: str) -> tuple[bool, str | None]:
    if raw.startswith("~"):
        raw = str(Path(raw).expanduser())
    if not is_inside(root, raw):
        return False, f"Path outside sandbox ({label}): {raw}"
    return True, None


def path_field_allowed(root: str, tool_name: str, tool_input: dict) -> tuple[bool, str | None]:
    """Check path-bearing tool input against root."""
    fields_checked: set[str] = set()

    primary = PATH_FIELD.get(tool_name)
    if primary:
        fields_checked.add(primary)
        raw = tool_input.get(primary)
        if raw is not None:
            if not isinstance(raw, str):
                return False, f"Path field {primary} must be a string"
            ok, msg = _check_path_string(root, raw, label=primary)
            if not ok:
                return False, msg or "denied"

    for extra in EXTRA_PATH_FIELDS.get(tool_name, ()):
        if extra in fields_checked:
            continue
        raw = tool_input.get(extra)
        if raw is None or not isinstance(raw, str):
            continue
        if tool_name == "Glob" and extra == "pattern":
            anchor = _glob_pattern_anchor(root, raw)
            ok, msg = _check_path_string(root, anchor, label="pattern")
            if not ok:
                return False, msg
            if ".." in Path(raw).parts:
                resolved = (Path(root) / raw).resolve()
                if not is_inside(root, resolved):
                    return False, f"Glob pattern escapes sandbox: {raw}"
            continue
        ok, msg = _check_path_string(root, raw, label=extra)
        if not ok:
            return False, msg

    return True, None
