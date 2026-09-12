"""Serve the Tectori docs site locally the way GitHub Pages serves it."""

# The point of this server is that a preview and the live site answer a
# request the same way, so the two things Pages does beyond handing back
# files both have to be here: it resolves an extensionless path to the .html
# file, and it answers a path no file matches with docs/404.html and a 404
# status. Without the second, the one page a new owner most wants to preview
# is the one page this server could not show them.

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

    def send_error(self, code: int, message=None, explain=None) -> None:
        """Answer a missing path with docs/404.html, as the live host does."""
        not_found = DOCS_ROOT / "404.html"
        if code != 404 or not not_found.exists():
            super().send_error(code, message, explain)
            return
        body = not_found.read_bytes()
        self.send_response(404, message)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve docs/ with clean URLs.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), CleanUrlHandler)
    print(f"Serving {DOCS_ROOT} at http://127.0.0.1:{args.port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
