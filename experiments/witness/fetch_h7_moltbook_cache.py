#!/usr/bin/env python3
"""Download jscmp4/Moltbook 2026-07-03 parquet pin into data/moltbook/.

Protocol: drafts/plans/witness-v2-moltbook-mb7a.md (h7-moltbook-mb7a-v1.0.0).
Writes merged posts.parquet and comments.parquet for collect_h7_moltbook_mb7a.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "moltbook"
REPO_ID = "jscmp4/Moltbook"
POST_GLOB = "parquet/posts/*.parquet"
COMMENT_GLOB = "parquet/comments/*.parquet"


def _require_deps() -> None:
    try:
        import pandas  # noqa: F401
        import pyarrow  # noqa: F401
        from huggingface_hub import HfApi, hf_hub_download  # noqa: F401
    except ImportError as exc:
        print(
            "Missing dependency. Install with:\n"
            "  pip install pandas pyarrow huggingface_hub",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc


def _list_parquet_files(api: "HfApi", pattern_prefix: str) -> list[str]:
    files = api.list_repo_files(REPO_ID, repo_type="dataset")
    return sorted(f for f in files if f.startswith(pattern_prefix) and f.endswith(".parquet"))


def _download_and_concat(
    api: "HfApi",
    hf_hub_download,
    pd,
    paths: list[str],
    out_path: Path,
    label: str,
) -> int:
    from huggingface_hub import hf_hub_download as dl

    if out_path.exists():
        print(f"  skip {out_path.name} (exists)")
        return int(len(pd.read_parquet(out_path)))

    if not paths:
        print(f"  FAIL no parquet files for {label}")
        return 0

    frames = []
    n = len(paths)
    for i, rel in enumerate(paths, 1):
        print(f"  [{i}/{n}] download {rel}")
        local = dl(repo_id=REPO_ID, filename=rel, repo_type="dataset")
        frames.append(pd.read_parquet(local))
    print(f"  concat {n} shards → {out_path.name}")
    merged = pd.concat(frames, ignore_index=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(out_path, index=False)
    return int(len(merged))


def main() -> int:
    _require_deps()
    import pandas as pd
    from huggingface_hub import HfApi, hf_hub_download

    print(f"[1/3] list parquet shards in {REPO_ID}")
    api = HfApi()
    post_files = _list_parquet_files(api, "parquet/posts/")
    comment_files = _list_parquet_files(api, "parquet/comments/")
    print(f"  posts={len(post_files)} comments={len(comment_files)}")
    if not post_files or not comment_files:
        print("FAIL: expected monthly parquet under parquet/posts and parquet/comments")
        return 1

    print("[2/3] posts")
    n_posts = _download_and_concat(
        api, hf_hub_download, pd, post_files, DATA / "posts.parquet", "posts"
    )
    print("[3/3] comments")
    n_comments = _download_and_concat(
        api, hf_hub_download, pd, comment_files, DATA / "comments.parquet", "comments"
    )
    print(f"done posts={n_posts:,} comments={n_comments:,} → {DATA}")
    return 0 if n_posts and n_comments else 1


if __name__ == "__main__":
    raise SystemExit(main())
