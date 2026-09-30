#!/usr/bin/env python3
"""Extract a LessWrong user's posts and comments from the HF lesswrong_260509 dump."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.parquet as pq

USERNAME = "Gunnar_Zarncke"


def comment_username(comment: dict) -> str | None:
    user = comment.get("user")
    if not user:
        return None
    return user.get("username")


def post_username(post: dict) -> str | None:
    user = post.get("user")
    if not user:
        return None
    return user.get("username")


def build_comment_index(comments: list[dict]) -> dict[str, dict]:
    return {c["_id"]: c for c in comments if c.get("_id")}


def extract_from_shard(path: Path, username: str) -> tuple[list[dict], list[dict]]:
    table = pq.read_table(path)
    rows = table.to_pylist()

    posts_out: list[dict] = []
    comments_out: list[dict] = []

    for row in rows:
        post = row["post"]
        comments = row.get("comments") or []
        comment_by_id = build_comment_index(comments)
        post_url = post.get("pageUrl")
        post_title = post.get("title")

        if post_username(post) == username:
            posts_out.append(
                {
                    "type": "post",
                    "url": post_url,
                    "timestamp": post.get("postedAt"),
                    "title": post_title,
                    "body": post.get("htmlBody"),
                }
            )

        for comment in comments:
            if comment_username(comment) != username:
                continue

            parent_id = comment.get("parentCommentId")
            if parent_id:
                parent = comment_by_id.get(parent_id)
                reply_to = {
                    "kind": "comment",
                    "parent_comment_id": parent_id,
                    "parent_comment_url": parent.get("pageUrl") if parent else None,
                    "parent_comment_text": parent.get("htmlBody") if parent else None,
                }
            else:
                reply_to = {
                    "kind": "post",
                    "post_url": post_url,
                }

            comments_out.append(
                {
                    "type": "comment",
                    "url": comment.get("pageUrl"),
                    "timestamp": comment.get("postedAt"),
                    "title": post_title,
                    "body": comment.get("htmlBody"),
                    "post_url": post_url,
                    "reply_to": reply_to,
                }
            )

    return posts_out, comments_out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dump-dir",
        type=Path,
        default=Path("data/lesswrong/lesswrong_260509/data/raw"),
        help="Directory containing train-*.parquet shards",
    )
    parser.add_argument(
        "--username",
        default=USERNAME,
        help="LessWrong username to extract",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/lesswrong/gunnar_zarncke_lw_content.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    shards = sorted(args.dump_dir.glob("train-*.parquet"))
    if not shards:
        raise SystemExit(f"No parquet shards found in {args.dump_dir}")

    all_posts: list[dict] = []
    all_comments: list[dict] = []

    for i, shard in enumerate(shards, start=1):
        print(f"[{i}/{len(shards)}] scanning {shard.name} ...", flush=True)
        posts, comments = extract_from_shard(shard, args.username)
        all_posts.extend(posts)
        all_comments.extend(comments)
        print(
            f"  cumulative: {len(all_posts)} posts, {len(all_comments)} comments",
            flush=True,
        )

    all_posts.sort(key=lambda x: x["timestamp"] or "")
    all_comments.sort(key=lambda x: x["timestamp"] or "")

    payload = {
        "username": args.username,
        "source_dataset": "x65617379/lesswrong_260509",
        "snapshot": "2026-05-06 posts / 2026-05-09 comments",
        "counts": {
            "posts": len(all_posts),
            "comments": len(all_comments),
        },
        "posts": all_posts,
        "comments": all_comments,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {args.output} ({len(all_posts)} posts, {len(all_comments)} comments)")


if __name__ == "__main__":
    main()
