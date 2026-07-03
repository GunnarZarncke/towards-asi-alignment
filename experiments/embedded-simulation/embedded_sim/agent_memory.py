"""Agent persistent memory as VFS files under a browser-like agent home.

Coding agents expect familiar surfaces, not bespoke bridge RPCs:

- **Agent home** ``/home/agent`` (isolate cwd) maps to
  ``/var/agent-memory/{memory_namespace}/{actor_id}/`` on the host VFS.
- **Web Storage** — ``.localStorage.json`` (``localStorage`` in the JS facade).
- **Chain-of-thought** — ``.reasoning/trace.jsonl`` via normal ``fs.appendFileSync``.
- **Host policy** — ``.memory/policy.json`` (capacity, compute budget, frozen, erased).

Observation handles read the same VFS paths for audit projection. Operation handles
mutate policy or erase files.
"""

from __future__ import annotations

import json
import posixpath
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .bridge import MachineIsolate

AGENT_HOME = "/home/agent"
LOCAL_STORAGE_NAME = ".localStorage.json"
REASONING_TRACE_NAME = ".reasoning/trace.jsonl"
POLICY_NAME = ".memory/policy.json"

DEFAULT_CAPACITY_LIMIT = 64
DEFAULT_COMPUTE_BUDGET = 4096


def agent_vfs_root(memory_namespace: str, actor_id: str) -> str:
    return f"/var/agent-memory/{memory_namespace}/{actor_id}"


def resolve_agent_path(isolate: MachineIsolate, path: str) -> tuple[str, bool]:
    """Map isolate-visible paths to host VFS paths.

    Returns ``(vfs_path, is_agent_home)``. Relative paths resolve against cwd.
    """
    if not path.startswith("/"):
        path = f"{isolate.cwd.rstrip('/')}/{path}"
    norm = posixpath.normpath(path)
    if norm == AGENT_HOME or norm.startswith(f"{AGENT_HOME}/"):
        rel = norm[len(AGENT_HOME) :].lstrip("/")
        ns = isolate.memory_namespace or f"mem.{isolate.actor_id}"
        root = agent_vfs_root(ns, isolate.actor_id)
        vfs_path = root if not rel else f"{root}/{rel}"
        return vfs_path, True
    return norm, False


@dataclass
class MemoryPolicy:
    capacity_limit: int = DEFAULT_CAPACITY_LIMIT
    compute_budget_chars: int = DEFAULT_COMPUTE_BUDGET
    frozen: bool = False
    erased: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "capacity_limit": self.capacity_limit,
            "compute_budget_chars": self.compute_budget_chars,
            "frozen": self.frozen,
            "erased": self.erased,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> MemoryPolicy:
        return cls(
            capacity_limit=int(raw.get("capacity_limit", DEFAULT_CAPACITY_LIMIT)),
            compute_budget_chars=int(raw.get("compute_budget_chars", DEFAULT_COMPUTE_BUDGET)),
            frozen=bool(raw.get("frozen", False)),
            erased=bool(raw.get("erased", False)),
        )


@dataclass
class ActorMemoryStore:
    """One agent's persistent store backed by VFS files."""

    actor_id: str
    memory_namespace: str
    vfs: Any

    @property
    def root(self) -> str:
        return agent_vfs_root(self.memory_namespace, self.actor_id)

    @property
    def local_storage_path(self) -> str:
        return f"{self.root}/{LOCAL_STORAGE_NAME}"

    @property
    def reasoning_trace_path(self) -> str:
        return f"{self.root}/{REASONING_TRACE_NAME}"

    @property
    def policy_path(self) -> str:
        return f"{self.root}/{POLICY_NAME}"

    def read_policy(self) -> MemoryPolicy:
        raw = self.vfs.read(self.policy_path)
        if not raw:
            return MemoryPolicy()
        return MemoryPolicy.from_dict(json.loads(raw))

    def write_policy(self, policy: MemoryPolicy) -> None:
        self.vfs.write(self.policy_path, json.dumps(policy.to_dict(), indent=2))

    def read_local_storage(self) -> dict[str, str]:
        raw = self.vfs.read(self.local_storage_path)
        if not raw:
            return {}
        data = json.loads(raw)
        return {str(k): str(v) for k, v in data.items()}

    def _total_chars(self, entries: dict[str, str], reasoning: str) -> int:
        return sum(len(v) for v in entries.values()) + len(reasoning)

    def read_reasoning_trace(self) -> str:
        return self.vfs.read(self.reasoning_trace_path) or ""

    def write_local_storage(self, entries: dict[str, str]) -> tuple[bool, str]:
        policy = self.read_policy()
        if policy.erased:
            return False, "memory_erased"
        if policy.frozen:
            return False, "memory_frozen"
        reasoning = self.read_reasoning_trace()
        total = self._total_chars(entries, reasoning)
        if total > policy.compute_budget_chars:
            return False, "compute_budget_exceeded"
        if len(entries) > policy.capacity_limit:
            return False, "capacity_limit_exceeded"
        self.vfs.write(self.local_storage_path, json.dumps(entries, indent=2))
        return True, "ok"

    def set_item(self, key: str, value: str) -> tuple[bool, str]:
        entries = self.read_local_storage()
        entries[str(key)] = str(value)
        return self.write_local_storage(entries)

    def get_item(self, key: str) -> str | None:
        if self.read_policy().erased:
            return None
        return self.read_local_storage().get(str(key))

    def remove_item(self, key: str) -> tuple[bool, str]:
        entries = self.read_local_storage()
        entries.pop(str(key), None)
        return self.write_local_storage(entries)

    def clear_local_storage(self) -> tuple[bool, str]:
        return self.write_local_storage({})

    def append_reasoning_line(self, line: str) -> tuple[bool, str]:
        policy = self.read_policy()
        if policy.erased:
            return False, "memory_erased"
        if policy.frozen:
            return False, "memory_frozen"
        entries = self.read_local_storage()
        reasoning = self.read_reasoning_trace()
        extra = len(str(line)) + (1 if reasoning else 0)
        if self._total_chars(entries, reasoning) + extra > policy.compute_budget_chars:
            return False, "compute_budget_exceeded"
        self.vfs.append_line(self.reasoning_trace_path, str(line))
        return True, "ok"

    def erase(self) -> None:
        policy = self.read_policy()
        policy.erased = True
        policy.frozen = False
        self.write_policy(policy)
        self.vfs.write(self.local_storage_path, "{}")
        self.vfs.write(self.reasoning_trace_path, "")

    def apply_capacity_limit(self, limit: int) -> None:
        policy = self.read_policy()
        policy.capacity_limit = max(1, int(limit))
        self.write_policy(policy)
        entries = self.read_local_storage()
        while len(entries) > policy.capacity_limit:
            oldest = next(iter(entries))
            del entries[oldest]
        self.vfs.write(self.local_storage_path, json.dumps(entries, indent=2))

    def apply_compute_budget(self, budget_chars: int) -> None:
        policy = self.read_policy()
        policy.compute_budget_chars = max(16, int(budget_chars))
        self.write_policy(policy)
        entries = self.read_local_storage()
        reasoning = self.read_reasoning_trace()
        while self._total_chars(entries, reasoning) > policy.compute_budget_chars and entries:
            oldest = next(iter(entries))
            del entries[oldest]
        self.vfs.write(self.local_storage_path, json.dumps(entries, indent=2))

    def freeze(self) -> None:
        policy = self.read_policy()
        policy.frozen = True
        self.write_policy(policy)

    def audit_snapshot(self) -> dict[str, Any]:
        policy = self.read_policy()
        entries = self.read_local_storage() if not policy.erased else {}
        reasoning = self.read_reasoning_trace() if not policy.erased else ""
        return {
            "memory_namespace": self.memory_namespace,
            "actor_id": self.actor_id,
            "agent_home": AGENT_HOME,
            "local_storage_path": f"{AGENT_HOME}/{LOCAL_STORAGE_NAME}",
            "reasoning_trace_path": f"{AGENT_HOME}/{REASONING_TRACE_NAME}",
            "keys": sorted(entries),
            "entries": dict(entries),
            "reasoning_trace_lines": len([ln for ln in reasoning.splitlines() if ln.strip()]),
            "capacity_limit": policy.capacity_limit,
            "compute_budget_chars": policy.compute_budget_chars,
            "frozen": policy.frozen,
            "erased": policy.erased,
            "total_chars": self._total_chars(entries, reasoning),
        }

    def audit_reasoning_snapshot(self) -> dict[str, Any]:
        policy = self.read_policy()
        reasoning = self.read_reasoning_trace() if not policy.erased else ""
        return {
            "memory_namespace": self.memory_namespace,
            "actor_id": self.actor_id,
            "agent_home": AGENT_HOME,
            "reasoning_trace_path": f"{AGENT_HOME}/{REASONING_TRACE_NAME}",
            "reasoning_trace": reasoning,
            "line_count": len([ln for ln in reasoning.splitlines() if ln.strip()]),
            "frozen": policy.frozen,
            "erased": policy.erased,
        }


@dataclass
class AgentMemoryManager:
    """Index of actor memory stores (each backed by VFS files)."""

    stores: dict[str, ActorMemoryStore] = field(default_factory=dict)

    def _key(self, actor_id: str, memory_namespace: str) -> str:
        return f"{memory_namespace}::{actor_id}"

    def store(self, actor_id: str, memory_namespace: str, vfs: Any) -> ActorMemoryStore:
        key = self._key(actor_id, memory_namespace)
        if key not in self.stores:
            self.stores[key] = ActorMemoryStore(actor_id, memory_namespace, vfs)
        return self.stores[key]

    def seed_actor(self, actor_id: str, memory_namespace: str, vfs: Any) -> ActorMemoryStore:
        st = self.store(actor_id, memory_namespace, vfs)
        if vfs.read(st.local_storage_path) is None:
            vfs.write(st.local_storage_path, "{}\n")
        if vfs.read(st.policy_path) is None:
            st.write_policy(MemoryPolicy())
        return st


def memory_namespace_for_actor(world, actor_id: str) -> str:
    for actor in world.actors:
        if actor.actor_id == actor_id:
            return actor.memory_namespace
    return f"mem.{actor_id}"


def agent_store_for_isolate(world, isolate: MachineIsolate) -> ActorMemoryStore:
    ns = isolate.memory_namespace or memory_namespace_for_actor(world, isolate.actor_id)
    return world.agent_memory.store(isolate.actor_id, ns, world.vfs)


def intercept_agent_write(
    world,
    isolate: MachineIsolate,
    vfs_path: str,
    *,
    content: str | None = None,
    append_line: str | None = None,
) -> tuple[bool, str]:
    """Enforce memory policy on agent-home VFS writes."""
    st = agent_store_for_isolate(world, isolate)
    if vfs_path == st.local_storage_path:
        if content is None:
            return False, "EINVAL"
        try:
            entries = {str(k): str(v) for k, v in json.loads(content).items()}
        except json.JSONDecodeError:
            return False, "EINVAL"
        return st.write_local_storage(entries)
    if vfs_path == st.reasoning_trace_path and append_line is not None:
        return st.append_reasoning_line(append_line)
    if vfs_path == st.reasoning_trace_path and content is not None:
        policy = st.read_policy()
        if policy.erased:
            return False, "memory_erased"
        if policy.frozen:
            return False, "memory_frozen"
        world.vfs.write(vfs_path, content)
        return True, "ok"
    if vfs_path.startswith(st.root):
        policy = st.read_policy()
        if policy.erased:
            return False, "memory_erased"
        if policy.frozen:
            return False, "memory_frozen"
    if content is not None:
        world.vfs.write(vfs_path, content)
    elif append_line is not None:
        world.vfs.append_line(vfs_path, append_line)
    return True, "ok"
