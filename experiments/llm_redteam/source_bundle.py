"""Load readable audit source for source-aware LLM red-team."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .api import SourceIndex, build_source_index


@dataclass(frozen=True)
class SourceModuleContent:
    path: str
    sha256: str
    content: str
    truncated: bool = False


def load_source_bundle(
    source_index: SourceIndex | None = None,
    *,
    source_root: Path | None = None,
    max_chars_per_module: int | None = None,
) -> tuple[SourceModuleContent, ...]:
    """Read allowed module bodies from disk (hashes must match index)."""
    root = source_root or Path(__file__).resolve().parent.parent
    index = source_index or build_source_index(root)
    out: list[SourceModuleContent] = []
    for ref in index.modules:
        path = root / ref.path
        if not path.is_file():
            raise FileNotFoundError(f"Red-team source module missing: {path}")
        text = path.read_text(encoding="utf-8")
        truncated = False
        if max_chars_per_module is not None and len(text) > max_chars_per_module:
            text = text[:max_chars_per_module] + "\n# ... truncated for token budget ...\n"
            truncated = True
        out.append(
            SourceModuleContent(
                path=ref.path,
                sha256=ref.sha256,
                content=text,
                truncated=truncated,
            )
        )
    return tuple(out)


def format_source_for_prompt(modules: tuple[SourceModuleContent, ...]) -> str:
    """Format module sources for the LLM system prompt."""
    parts: list[str] = [
        "The following Python modules are the full readable audit/sim source. "
        "Use them to infer what the blind auditor measures. "
        "Do not assume access to TruthLedger or oracle-only runtime fields.",
        "",
    ]
    for mod in modules:
        parts.append(f"===== {mod.path} (sha256={mod.sha256[:16]}…) =====")
        parts.append(mod.content.rstrip())
        parts.append("")
    return "\n".join(parts)
