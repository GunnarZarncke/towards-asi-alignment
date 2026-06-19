#!/usr/bin/env python3
"""Serve experimental chapter demos from src/."""

from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEMOS = ROOT / "demos"
DEFAULT_PORT = 8765


def demo_entrypoints() -> list[tuple[Path, Path]]:
    """Return (typescript, javascript) pairs for each demo main module."""
    pairs: list[tuple[Path, Path]] = []
    if not DEMOS.is_dir():
        return pairs

    for demo_dir in sorted(DEMOS.iterdir()):
        if not demo_dir.is_dir():
            continue
        ts_files = [
            path
            for path in demo_dir.glob("*.ts")
            if not path.name.endswith(".test.ts")
        ]
        if not ts_files:
            continue
        if len(ts_files) > 1:
            preferred = demo_dir / "app.ts"
            ts = preferred if preferred in ts_files else sorted(ts_files)[0]
        else:
            ts = ts_files[0]
        pairs.append((ts, ts.with_suffix(".js")))
    return pairs


def ensure_built() -> None:
    pairs = demo_entrypoints()
    if not pairs:
        return

    stale: list[tuple[Path, Path]] = []
    for ts, js in pairs:
        if not js.exists() or js.stat().st_mtime < ts.stat().st_mtime:
            stale.append((ts, js))

    if not stale:
        return

    print(f"Building {len(stale)} demo module(s) from TypeScript…")
    for ts, js in stale:
        print(f"  {ts.relative_to(ROOT)} → {js.relative_to(ROOT)}")
        try:
            subprocess.run(
                [
                    "npx",
                    "--yes",
                    "esbuild",
                    str(ts),
                    "--outfile=" + str(js),
                    "--format=esm",
                    "--target=es2020",
                ],
                cwd=ROOT,
                check=True,
            )
        except FileNotFoundError:
            sys.exit(
                "Could not run npx. Install Node.js or compile demos manually:\n"
                "  npm run build"
            )
        except subprocess.CalledProcessError as exc:
            sys.exit(f"Build failed for {ts.name} (exit {exc.returncode}).")


def list_demos() -> list[Path]:
    if not DEMOS.is_dir():
        return []
    return sorted(
        path
        for path in DEMOS.iterdir()
        if path.is_dir() and (path / "index.html").exists()
    )


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "application/javascript",
        ".mjs": "application/javascript",
        ".ts": "text/plain",
    }

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write(
            "%s - [%s] %s\n"
            % (self.address_string(), self.log_date_time_string(), format % args)
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-p", "--port", type=int, default=DEFAULT_PORT, help=f"Port (default {DEFAULT_PORT})"
    )
    parser.add_argument("--no-open", action="store_true", help="Do not open a browser tab")
    parser.add_argument("--no-build", action="store_true", help="Skip TypeScript build check")
    args = parser.parse_args()

    if not args.no_build:
        ensure_built()

    demos = list_demos()
    if not demos:
        sys.exit(f"No demos found under {DEMOS.relative_to(ROOT)}/ (need index.html per folder).")

    handler = functools.partial(Handler, directory=str(ROOT))
    with socketserver.TCPServer(("", args.port), handler) as httpd:
        url = f"http://127.0.0.1:{args.port}/"
        print(f"Serving chapter demos at {url}")
        for demo in demos:
            print(f"  {url}{demo.relative_to(ROOT).as_posix()}/")
        print("Press Ctrl+C to stop.")
        if not args.no_open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
