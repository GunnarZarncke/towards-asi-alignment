#!/usr/bin/env python3
"""Fetch LessWrong wiki/tag objects via the public GraphQL API.

Uses the ``allPublicTags`` selector (tags plus wiki-only pages). The API caps
``offset`` at 2000; ``--all`` paginates with ``excludedTagIds`` after the first
three 1000-item pages so the full corpus can be retrieved with the same query.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

GRAPHQL_URL = "https://www.lesswrong.com/graphql"
USER_AGENT = "LW_user_Gunnar_Zarncke"
DEFAULT_LIMIT = 1000
MAX_OFFSET = 2000

TAGS_QUERY = """
query FetchPublicTags(
  $limit: Int
  $offset: Int
  $excludedTagIds: [String!]
  $enableTotal: Boolean
) {
  tags(
    selector: { allPublicTags: { excludedTagIds: $excludedTagIds } }
    limit: $limit
    offset: $offset
    enableTotal: $enableTotal
  ) {
    totalCount
    results {
      _id
      name
      slug
      wikiOnly
      postCount
      core
      wikiGrade
      isArbitalImport
      createdAt

      description {
        html
        plaintextDescription
        version
        editedAt
      }

      parentTag {
        _id
        name
        slug
      }

      subTags {
        _id
        name
        slug
      }
    }
  }
}
""".strip()


def graphql_request(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {"query": query}
    if variables is not None:
        payload["variables"] = variables

    req = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} from LessWrong GraphQL: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error calling LessWrong GraphQL: {exc}") from exc

    if body.get("errors"):
        raise SystemExit(f"GraphQL errors: {json.dumps(body['errors'], indent=2)}")

    return body


def fetch_tags_page(
    *,
    limit: int,
    offset: int,
    excluded_tag_ids: list[str] | None = None,
    enable_total: bool = False,
) -> dict[str, Any]:
    variables: dict[str, Any] = {
        "limit": limit,
        "offset": offset,
        "excludedTagIds": excluded_tag_ids or [],
        "enableTotal": enable_total,
    }
    body = graphql_request(TAGS_QUERY, variables)
    return body["data"]["tags"]


def fetch_all_tags(*, page_size: int = DEFAULT_LIMIT) -> tuple[list[dict[str, Any]], int | None]:
    all_tags: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    excluded_tag_ids: list[str] = []
    total_count: int | None = None
    page_num = 0

    while True:
        offset = min(page_num * page_size, MAX_OFFSET) if not excluded_tag_ids else 0
        page_num += 1
        print(
            f"[page {page_num}] limit={page_size} offset={offset} "
            f"excluded={len(excluded_tag_ids)} fetched={len(all_tags)} ...",
            flush=True,
        )

        page = fetch_tags_page(
            limit=page_size,
            offset=offset,
            excluded_tag_ids=excluded_tag_ids,
            enable_total=total_count is None,
        )
        if total_count is None:
            total_count = page.get("totalCount")

        results = page.get("results") or []
        if not results:
            break

        new_results: list[dict[str, Any]] = []
        for tag in results:
            tag_id = tag["_id"]
            if tag_id in seen_ids:
                continue
            seen_ids.add(tag_id)
            new_results.append(tag)

        if not new_results:
            break

        all_tags.extend(new_results)
        excluded_tag_ids.extend(tag["_id"] for tag in new_results)

        print(
            f"  got {len(new_results)} new tags "
            f"({len(all_tags)}/{total_count or '?'} cumulative)",
            flush=True,
        )

        if total_count is not None and len(all_tags) >= total_count:
            break
        if len(results) < page_size:
            break

        time.sleep(1)

    return all_tags, total_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Page size (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help=f"Offset for a single request (max {MAX_OFFSET})",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch the full public tag/wiki corpus (paginates automatically)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write JSON here (default: stdout unless --all)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON",
    )
    args = parser.parse_args()

    if args.all:
        tags, total_count = fetch_all_tags(page_size=args.limit)
        payload = {
            "source": GRAPHQL_URL,
            "selector": "allPublicTags",
            "user_agent": USER_AGENT,
            "total_count": total_count,
            "fetched_count": len(tags),
            "tags": tags,
        }
        default_output = Path("data/lesswrong/lw_wiki_tags.json")
    else:
        if args.offset > MAX_OFFSET:
            raise SystemExit(
                f"offset {args.offset} exceeds API maximum {MAX_OFFSET}; use --all for full dump"
            )
        page = fetch_tags_page(
            limit=args.limit,
            offset=args.offset,
            enable_total=True,
        )
        payload = {
            "source": GRAPHQL_URL,
            "selector": "allPublicTags",
            "user_agent": USER_AGENT,
            "limit": args.limit,
            "offset": args.offset,
            "total_count": page.get("totalCount"),
            "fetched_count": len(page.get("results") or []),
            "tags": page.get("results") or [],
        }
        default_output = None

    output_path = args.output or default_output
    indent = 2 if args.pretty or output_path is not None else None
    rendered = json.dumps(payload, ensure_ascii=False, indent=indent)
    if rendered and not rendered.endswith("\n"):
        rendered += "\n"

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {output_path} ({payload['fetched_count']} tags)", flush=True)
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
