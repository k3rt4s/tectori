"""Check that the local server and the rebrand rehearsal refuse paths outside the trees they own."""

from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import rehearse_rebrand  # noqa: E402
import serve_docs  # noqa: E402

DOCS = serve_docs.DOCS_ROOT

# Paths a request can carry that must not leave docs/. Each is the shape of a
# real escape: an encoded dot-dot, a drive letter a path join treats as a new
# root, an encoded backslash, two plain climbs, and docs/ itself, whose .html
# rewrite would be the sibling file docs.html.
HOSTILE = (
    "/%2e%2e/%2e%2e/README.md",
    "/C:/Windows/win.ini",
    "/..%5c..%5cREADME.md",
    "/../README.md",
    "/docs/../README.md",
    "/.",
)


def serve_problems() -> list[str]:
    """Return what the server's path translation gets wrong."""
    problems = []
    translate = serve_docs.CleanUrlHandler.translate_path
    for request in HOSTILE:
        resolved = Path(translate(None, request)).resolve()
        if DOCS not in resolved.parents:
            problems.append(f"{request} resolves to {resolved}, outside docs/")
    expected = {"/about": DOCS / "about.html", "/": DOCS / "index.html"}
    for request, want in expected.items():
        got = Path(translate(None, request))
        if got != want:
            problems.append(f"{request} resolves to {got}, not {want}")
    if not (DOCS / "404.html").exists() or Path(translate(None, "/nope-page")).exists():
        problems.append("a missing page no longer falls through to the 404 page")
    return problems


# A pretend repo and an unrelated directory; the guard is judged without
# touching the disk, so neither needs to exist.
REPO = os.path.abspath(os.path.join(os.sep, "work", "site"))
OUTSIDE = os.path.abspath(os.path.join(os.sep, "scratch", "rehearsal"))
# (name, out_dir, exists, is_empty, has_marker, refused)
GUARD_CASES = (
    ("equal", REPO, True, False, False, True),
    ("parent", os.path.dirname(REPO), True, False, False, True),
    ("grandparent", os.path.abspath(os.sep), True, False, False, True),
    ("child", os.path.join(REPO, "out"), False, False, False, True),
    ("sibling, non-empty, unmarked", os.path.join(os.path.dirname(REPO), "other"), True, False, False, True),
    ("unrelated, non-empty, unmarked", OUTSIDE, True, False, False, True),
    ("unrelated, non-empty, marked", OUTSIDE, True, False, True, False),
    ("parent, marked", os.path.dirname(REPO), True, False, True, True),
    ("parent, empty", os.path.dirname(REPO), True, True, False, True),
    ("unrelated, empty", OUTSIDE, True, True, False, False),
    ("unrelated, missing", OUTSIDE, False, False, False, False),
)


def guard_problems() -> list[str]:
    """Return what the rehearsal's --out guard gets wrong, judged without touching the disk."""
    problems = []
    for name, out_dir, exists, is_empty, has_marker, refused in GUARD_CASES:
        reason = rehearse_rebrand.out_dir_refusal(out_dir, REPO, exists, is_empty, has_marker)
        if bool(reason) != refused:
            want = "refused" if refused else "allowed"
            problems.append(f"{name}: expected {want}, got {reason!r}")
    return problems


def main() -> int:
    problems = serve_problems() + guard_problems()
    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the server and the rehearsal refuse "
        f"paths outside their trees: {len(HOSTILE)} hostile requests, "
        f"{len(GUARD_CASES)} --out cases, {len(problems)} problems"
    )
    for item in problems:
        print(f"       {item}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
