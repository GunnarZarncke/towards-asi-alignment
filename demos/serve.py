#!/usr/bin/env python3
"""Serve experimental chapter demos from demos/."""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import mimetypes
import os
import re
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
SKIP_DIR_NAMES = frozenset({"node_modules", "__pycache__"})
DEFAULT_PORT = 8765
BACKEND_PORT = 8766


def load_repo_env() -> None:
    """Load repo-root ``.env`` into ``os.environ`` (setdefault; does not override)."""
    env_path = ROOT.parent / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def posthog_settings() -> tuple[str, str]:
    token = (
        os.environ.get("POSTHOG_PROJECT_TOKEN")
        or os.environ.get("POSTHOG_API_KEY")
        or ""
    ).strip()
    host = (os.environ.get("POSTHOG_HOST") or "https://eu.i.posthog.com").strip()
    return token, host


def is_demo_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and re.match(r"^(ch\d+|app[A-Za-z])", path.name) is not None
        and path.name not in SKIP_DIR_NAMES
        and (path / "index.html").is_file()
    )


def demo_entrypoints() -> list[tuple[Path, Path]]:
    """Return (typescript, javascript) pairs for each demo main module."""
    pairs: list[tuple[Path, Path]] = []
    for demo_dir in sorted(p for p in ROOT.iterdir() if is_demo_dir(p)):
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
    return sorted(p for p in ROOT.iterdir() if is_demo_dir(p))


def backend_demos() -> list[tuple[Path, dict]]:
    """Return (demo_dir, backend.json) for Python backend demos."""
    configs: list[tuple[Path, dict]] = []
    for demo_dir in sorted(p for p in ROOT.iterdir() if is_demo_dir(p)):
        backend_file = demo_dir / "backend.json"
        app_file = demo_dir / "app.py"
        if not backend_file.is_file() or not app_file.is_file():
            continue
        cfg = json.loads(backend_file.read_text(encoding="utf-8"))
        configs.append((demo_dir, cfg))
    return configs


def agency_detect_root() -> Path:
    """Sibling checkout used by coalition_detect (override with AGENCY_DETECT_PATH)."""
    env = os.environ.get("AGENCY_DETECT_PATH")
    if env:
        return Path(env).resolve()
    return ROOT.parent.parent / "agency-detect"


def start_backend_servers(
    configs: list[tuple[Path, dict]],
) -> list[tuple[subprocess.Popen[bytes], Path, int]]:
    procs: list[tuple[subprocess.Popen[bytes], Path, int]] = []
    agency_root = agency_detect_root()
    backend_env = os.environ.copy()
    path_prefixes = [str(ROOT)]
    if agency_root.is_dir():
        path_prefixes.insert(0, str(agency_root))
    existing = backend_env.get("PYTHONPATH", "")
    merged = os.pathsep.join(path_prefixes + ([existing] if existing else []))
    backend_env["PYTHONPATH"] = merged
    for demo_dir, cfg in configs:
        port = int(cfg.get("port", BACKEND_PORT))
        module = str(cfg.get("module", "app:app"))
        try:
            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    module,
                    "--app-dir",
                    str(demo_dir),
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(port),
                ],
                cwd=str(ROOT),
                env=backend_env,
            )
        except FileNotFoundError:
            sys.exit(
                f"Could not start backend demo {demo_dir.name}. "
                "Install dependencies:\n"
                f"  pip install -r {demo_dir.relative_to(ROOT)}/requirements.txt"
            )
        procs.append((proc, demo_dir, port))
    return procs


def stop_backend_servers(procs: list[tuple[subprocess.Popen[bytes], Path, int]]) -> None:
    for proc, _demo_dir, _port in procs:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


class DemoHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "application/javascript",
        ".mjs": "application/javascript",
        ".ts": "text/plain",
    }

    def __init__(
        self,
        *args,
        posthog_token: str = "",
        posthog_host: str = "",
        **kwargs,
    ) -> None:
        self._posthog_token = posthog_token
        self._posthog_host = posthog_host
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write(
            "%s - [%s] %s\n"
            % (self.address_string(), self.log_date_time_string(), format % args)
        )

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/posthog-config.js":
            config = {
                "token": self._posthog_token,
                "host": self._posthog_host,
                "isDevelopment": os.environ.get("NODE_ENV") != "production",
            }
            payload = json.dumps(config)
            body = f"window.__POSTHOG_CONFIG__={payload};".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path.startswith("/vendor/posthog/"):
            rel = unquote(path.removeprefix("/vendor/posthog/"))
            if ".." in rel or rel.startswith("/"):
                self.send_error(403)
                return
            file_path = ROOT / "node_modules" / "posthog-js" / "dist" / rel
            if not file_path.is_file():
                self.send_error(404)
                return
            data = file_path.read_bytes()
            ctype = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-p", "--port", type=int, default=DEFAULT_PORT, help=f"Port (default {DEFAULT_PORT})"
    )
    parser.add_argument("--no-open", action="store_true", help="Do not open a browser tab")
    parser.add_argument("--no-build", action="store_true", help="Skip TypeScript build check")
    args = parser.parse_args()

    load_repo_env()

    if not args.no_build:
        ensure_built()

    demos = list_demos()
    if not demos:
        sys.exit(f"No demos found under {ROOT}/ (need chNN-*/index.html folders).")

    backend_configs = backend_demos()
    backend_procs = start_backend_servers(backend_configs) if backend_configs else []

    posthog_token, posthog_host = posthog_settings()
    handler = functools.partial(
        DemoHandler,
        directory=str(ROOT),
        posthog_token=posthog_token,
        posthog_host=posthog_host,
    )
    with socketserver.TCPServer(("", args.port), handler) as httpd:
        url = f"http://127.0.0.1:{args.port}/"
        print(f"Serving chapter demos at {url}")
        for demo in demos:
            print(f"  {url}{demo.relative_to(ROOT).as_posix()}/")
        for _proc, demo_dir, port in backend_procs:
            print(f"  http://127.0.0.1:{port}/  ({demo_dir.name} backend)")
        print("Press Ctrl+C to stop.")
        if not args.no_open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            stop_backend_servers(backend_procs)


if __name__ == "__main__":
    main()
