"""Check that every sitemap lastmod date is at least as recent as the page's own source."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = REPO_ROOT / "site" / "content"

# login.html has no entry in the content model, so its source is named here the
# way build_site.py names it.
VERBATIM_SOURCES = {"/login.html": "pages/login.page.frag"}


def page_sources() -> dict[str, str]:
    """Return each published path mapped to the repository file its words live in."""
    entries = json.loads(
        (CONTENT_DIR / "pages.json").read_text(encoding="utf-8")
    )
    sources = dict(VERBATIM_SOURCES)
    for entry in entries:
        output = entry["output"]
        path = "/" if output == "index.html" else "/" + output[: -len(".html")]
        sources[path] = entry["body_fragment"]
    return sources


def last_changed(relative: str) -> str | None:
    """Return the date of the last commit that changed a file, or None."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ad", "--date=short", "--", relative],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def main() -> int:
    public_pages = json.loads(
        (CONTENT_DIR / "public_pages.json").read_text(encoding="utf-8")
    )
    sources = page_sources()
    problems: list[str] = []
    checked = 0

    # A repository cloned one commit deep answers every one of these questions
    # with the same date, which would pass this check while measuring nothing.
    # Refusing to run is the only honest answer.
    depth = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if depth.returncode != 0:
        print("[FAIL] sitemap dates match the pages: this is not a git repository")
        return 1
    if int(depth.stdout.strip() or 0) < 2:
        print(
            "[FAIL] sitemap dates match the pages: this clone carries "
            f"{depth.stdout.strip()} commit of history, so the dates cannot be "
            "checked. Clone with full history, or fetch-depth: 0 in CI."
        )
        return 1

    for item in public_pages:
        path, stated = item["path"], item["lastmod"]
        source = sources.get(path)
        if source is None:
            problems.append(
                f"{path}: is in the sitemap and nothing in the content model "
                "writes it, so there is no source to date it against"
            )
            continue
        relative = "site/" + source
        if not (REPO_ROOT / relative).is_file():
            problems.append(f"{path}: {relative} does not exist")
            continue
        changed = last_changed(relative)
        if changed is None:
            problems.append(
                f"{path}: {relative} has never been committed, so the date "
                f"{stated} in the sitemap rests on nothing"
            )
            continue
        checked += 1
        if changed > stated:
            problems.append(
                f"{path}: the sitemap says this page last changed {stated}, "
                f"and its words were rewritten on {changed}"
            )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the sitemap's dates are not older than "
        f"the pages: {checked} pages checked, {len(problems)} problems"
    )
    for problem in problems[:30]:
        print(f"       {problem}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
