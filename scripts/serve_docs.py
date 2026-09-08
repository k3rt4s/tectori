"""Serve the Tectori docs site locally with GitHub Pages-style clean URLs."""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"


class CleanUrlHandler(SimpleHTTPRequestHandler):
    """Static file handler that resolves extensionless page paths."""

    def translate_path(self, path: str) -> str:
        request_path = unquote(urlsplit(path).path)
        if request_path == "/":
            return str(DOCS_ROOT / "index.html")
        relative = request_path.lstrip("/")
        candidate = DOCS_ROOT / relative
        if not candidate.suffix:
            html_candidate = candidate.with_suffix(".html")
            if html_candidate.exists():
                return str(html_candidate)
        return str(candidate)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve docs/ with clean URLs.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), CleanUrlHandler)
    print(f"Serving {DOCS_ROOT} at http://127.0.0.1:{args.port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
