"""Check that every class a published page uses is defined in the stylesheet."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
STYLESHEET = REPO_ROOT / "site" / "static" / "styles.css"
DOCS = REPO_ROOT / "docs"

# Matches double-quoted, single-quoted or unquoted class attribute values,
# any case of "class" and whitespace around "=". A negative lookbehind
# stops it from matching inside "data-class=" or "subclass=", where the
# character right before "class" is a word character or a hyphen.
CLASS_ATTR_RE = re.compile(
    r'(?<![\w-])class\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s\"\'=<>`]+))',
    re.IGNORECASE,
)
# A class the stylesheet names, anywhere in any selector, including inside a
# media query and as part of a compound selector. ":not(.x)" and ":is(.x)"
# still match here; only attribute-selector brackets and quoted strings are
# stripped before this runs, so ".pdf" inside a[href$=".pdf"] is not a class.
CLASS_RULE_RE = re.compile(r"\.([A-Za-z_-][A-Za-z0-9_-]*)")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
# An attribute selector, with its bracket contents, including a quoted string
# that may itself contain "]" or "[". Stripped whole so a value such as
# a[href$=".pdf"] or a[data-kind="x.brochure"] never reaches CLASS_RULE_RE.
ATTR_SELECTOR_RE = re.compile(r'\[(?:"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|[^\[\]])*\]')
# A quoted string, honouring backslash escapes and never crossing a line,
# stripped so a value inside it is never read as a class.
QUOTED_STRING_RE = re.compile(r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'')
# A build token such as "{{BAND_IMAGE_FILENAME}}", the shape build_site.py
# substitutes (see SITE_TOKENS there). Its own braces would otherwise split
# a declaration value into what looks like a selector fragment below.
TOKEN_PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")


def defined_classes(css: str) -> set[str]:
    """Return every class name the stylesheet defines a rule for.

    Reads selector text only, never declaration values, so url(...) content
    is never scanned. Attribute selectors (including their quoted values)
    and any other quoted strings are stripped before matching, so they are
    not read as classes; ":not(.x)" and ":is(.x)" are read normally because
    they still count as class references.
    """
    without_comments = COMMENT_RE.sub(" ", css)
    # Build placeholders like "{{BAND_IMAGE_FILENAME}}" are neutralized first,
    # because their own braces would otherwise split a declaration value.
    without_tokens = TOKEN_PLACEHOLDER_RE.sub("TOKEN", without_comments)
    # Quoted strings go before the split, so a brace inside one, as in
    # content: "{", cannot cut a rule in the wrong place.
    without_tokens = ATTR_SELECTOR_RE.sub(" ", without_tokens)
    without_tokens = QUOTED_STRING_RE.sub(" ", without_tokens)
    # Only the selector half of each rule declares a class; a decimal in a
    # declaration such as "margin: .5rem" is not one.
    fragments = [
        block.split("}")[-1] for block in without_tokens.split("{")[:-1]
    ]
    # Stripped per fragment, before joining, so a leftover quote or bracket
    # in one fragment cannot consume text belonging to another.
    cleaned = [
        QUOTED_STRING_RE.sub(" ", ATTR_SELECTOR_RE.sub(" ", fragment))
        for fragment in fragments
    ]
    selectors = " ".join(cleaned)
    return set(CLASS_RULE_RE.findall(selectors))


def main() -> int:
    defined = defined_classes(STYLESHEET.read_text(encoding="utf-8"))
    used: dict[str, set[str]] = {}
    pages = sorted(DOCS.glob("*.html"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for attribute in CLASS_ATTR_RE.finditer(text):
            value = next(
                group for group in attribute.groups() if group is not None
            )
            for name in value.split():
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
