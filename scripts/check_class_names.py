"""Check that every class a published page uses is defined in the stylesheet."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
STYLESHEET = REPO_ROOT / "site" / "static" / "styles.css"
DOCS = REPO_ROOT / "docs"

CLASS_ATTR_RE = re.compile(r'class\s*=\s*"([^"]*)"', re.IGNORECASE)
# A class the stylesheet names, anywhere in any selector, including inside a
# media query and as part of a compound selector.
CLASS_RULE_RE = re.compile(r"\.([A-Za-z_-][A-Za-z0-9_-]*)")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def defined_classes(css: str) -> set[str]:
    """Return every class name the stylesheet defines a rule for."""
    without_comments = COMMENT_RE.sub(" ", css)
    # Only the selector half of each rule declares a class; a decimal in a
    # declaration such as "margin: .5rem" is not one.
    selectors = " ".join(
        block.split("}")[-1] for block in without_comments.split("{")[:-1]
    )
    return set(CLASS_RULE_RE.findall(selectors))


def main() -> int:
    defined = defined_classes(STYLESHEET.read_text(encoding="utf-8"))
    used: dict[str, set[str]] = {}
    pages = sorted(DOCS.glob("*.html"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for attribute in CLASS_ATTR_RE.finditer(text):
            for name in attribute.group(1).split():
                used.setdefault(name, set()).add(page.name)

    problems = []
    for name in sorted(set(used) - defined):
        where = sorted(used[name])
        shown = ", ".join(where[:3]) + (" and others" if len(where) > 3 else "")
        problems.append(
            f"class {name!r} is on {len(where)} page(s) ({shown}) and the "
            "stylesheet defines no rule for it, so the markup asks for a "
            "presentation nothing supplies and every other check passes"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] every class a page uses is defined: "
        f"{len(used)} classes across {len(pages)} pages, {len(defined)} "
        f"defined, {len(problems)} problems"
    )
    for item in problems[:20]:
        print(f"       {item}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
