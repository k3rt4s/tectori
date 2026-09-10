"""Check that every llms.txt page description still matches that page's meta description."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"
LLMS_FILE = DOCS_ROOT / "llms.txt"
LINE_END = b"\r\n"

# The opening quote is captured and the same quote is required to close, so an
# apostrophe inside the description does not truncate the match.
META_DESCRIPTION = re.compile(
    rb'<meta[^>]*?name=(["\'])description\1[^>]*?content=(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)
LLMS_ENTRY = re.compile(r"^- (/\S*): (.+)$")


def page_for(url_path: str) -> Path:
    """Return the docs file that GitHub Pages serves for a site-relative URL path."""
    name = url_path.strip("/") or "index"
    if not name.endswith(".html"):
        name += ".html"
    return DOCS_ROOT / name


def meta_description(page: Path) -> str | None:
    """Return the page's meta description as a single collapsed line, or None if it has none."""
    match = META_DESCRIPTION.search(page.read_bytes())
    if match is None:
        return None
    return " ".join(match.group(3).decode("utf-8").split())


def entries() -> list[tuple[int, str, str]]:
    """Return every llms.txt page entry as a line number, URL path, and description."""
    found = []
    text = LLMS_FILE.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), start=1):
        match = LLMS_ENTRY.match(line)
        if match:
            found.append((number, match.group(1), " ".join(match.group(2).split())))
    return found


def summary() -> tuple[int, str] | None:
    """Return the line number and text of the llms.txt summary paragraph under the title."""
    for number, line in enumerate(LLMS_FILE.read_text(encoding="utf-8").splitlines(), start=1):
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            return None
        if line.strip():
            return number, " ".join(line.split())
    return None


def rewrite_summary(description: str) -> None:
    """Replace the llms.txt summary paragraph, preserving CRLF line endings."""
    found = summary()
    if found is None:
        raise SystemExit("could not find the llms.txt summary paragraph")
    number, current = found
    raw = LLMS_FILE.read_bytes()
    old = current.encode("utf-8") + LINE_END
    if raw.count(old) != 1:
        raise SystemExit(f"llms.txt:{number}: the summary text is not unique in the file")
    raw = raw.replace(old, description.encode("utf-8") + LINE_END, 1)
    if b"\n" in raw.replace(LINE_END, b""):
        raise SystemExit("refusing to write: the rewrite introduced a bare newline")
    LLMS_FILE.write_bytes(raw)


def rewrite(fixes: dict[str, str]) -> None:
    """Replace the named llms.txt entries with fresh descriptions, preserving CRLF line endings."""
    raw = LLMS_FILE.read_bytes()
    for url_path, description in fixes.items():
        pattern = re.compile(
            rb"^- " + re.escape(url_path.encode()) + rb": .*?\r?\n",
            re.MULTILINE | re.DOTALL,
        )
        replacement = b"- " + url_path.encode() + b": " + description.encode("utf-8") + b"\r\n"
        raw, count = pattern.subn(replacement, raw, count=1)
        if count != 1:
            raise SystemExit(f"could not rewrite the entry for {url_path}")
    if b"\n" in raw.replace(b"\r\n", b""):
        raise SystemExit("refusing to write: the rewrite introduced a bare newline")
    LLMS_FILE.write_bytes(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="rewrite drifted entries from the pages' current meta descriptions",
    )
    args = parser.parse_args()

    drifted: dict[str, str] = {}
    problems = 0
    checked = 0

    for number, url_path, described in entries():
        page = page_for(url_path)
        if not page.is_file():
            print(f"llms.txt:{number}: {url_path} names no page in docs/")
            problems += 1
            continue
        current = meta_description(page)
        if current is None:
            print(f"llms.txt:{number}: {page.name} has no meta description")
            problems += 1
            continue
        checked += 1
        if current != described:
            drifted[url_path] = current
            print(f"llms.txt:{number}: {url_path} has drifted")
            print(f"  llms.txt:  {described}")
            print(f"  {page.name}: {current}")

    # The summary paragraph under the title repeats the homepage meta
    # description, so it drifts the same way the page entries do.
    home = meta_description(page_for("/"))
    found = summary()
    summary_drift = False
    if home is None or found is None:
        print("llms.txt: could not compare the summary paragraph to the homepage")
        problems += 1
    else:
        number, described = found
        checked += 1
        if described != home:
            summary_drift = True
            print(f"llms.txt:{number}: the summary paragraph has drifted")
            print(f"  llms.txt:   {described}")
            print(f"  index.html: {home}")

    if args.fix and (drifted or summary_drift):
        fixed = len(drifted) + (1 if summary_drift else 0)
        if drifted:
            rewrite(drifted)
            drifted = {}
        if summary_drift:
            rewrite_summary(home)
            summary_drift = False
        noun = "line" if fixed == 1 else "lines"
        print(f"\nrewrote {fixed} {noun} from the pages' meta descriptions")

    stale = len(drifted) + (1 if summary_drift else 0)
    print(f"\nchecked {checked} lines, {stale} drifted, {problems} other problems")
    return 1 if stale or problems else 0


if __name__ == "__main__":
    sys.exit(main())
