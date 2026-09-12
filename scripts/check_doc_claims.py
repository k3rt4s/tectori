"""Check that the countable claims the documentation makes about this tree are still true."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"
SITE_DIR = PROJECT_ROOT / "site"
SCRIPT_DIR = Path(__file__).resolve().parent

# Written-out numbers, because the prose spells them. Digits are read as
# digits, so a claim may use either.
WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "twenty-one": 21, "twenty-two": 22, "twenty-three": 23,
    "twenty-four": 24, "twenty-five": 25,
}
ORDINALS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
    "eleventh": 11, "twelfth": 12, "thirteenth": 13,
}
SPELLINGS = {**WORDS, **ORDINALS}
NUMBER = r"(?P<n>\d+|[a-z]+(?:-[a-z]+)?)"


def read_json(path: Path):
    """Return the parsed contents of a UTF-8 JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


SITE = read_json(SITE_DIR / "content" / "site.json")
FOUNDER = read_json(SITE_DIR / "content" / "founder.json")


def parse_number(text: str) -> int | None:
    """Return the integer a claim's number is, whether it is spelled or written."""
    if text.isdigit():
        return int(text)
    return SPELLINGS.get(text.lower())


def function_named(path: Path, name: str) -> ast.FunctionDef:
    """Return one top-level function of a script, parsed rather than imported."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise LookupError(f"{path.name} has no {name}()")


def verify_site_checks() -> int:
    """Return how many checks verify_site.py runs, counted from its own list."""
    for node in ast.walk(function_named(SCRIPT_DIR / "verify_site.py", "main")):
        if (
            isinstance(node, ast.Assign)
            and any(
                isinstance(t, ast.Name) and t.id == "results" for t in node.targets
            )
            and isinstance(node.value, ast.List)
        ):
            return len(node.value.elts)
    raise LookupError("verify_site.py main() no longer builds a results list")


def check_site_checks() -> tuple[int, int]:
    """Return how many checks check_site.py runs by default, and with --full."""
    main = function_named(SCRIPT_DIR / "check_site.py", "main")
    optional = 0
    for node in ast.walk(main):
        if isinstance(node, ast.If) and "args.full" in ast.unparse(node.test):
            optional += sum(
                1 for child in ast.walk(node) if is_results_append(child)
            )
    total = sum(1 for node in ast.walk(main) if is_results_append(node))
    return total - optional, total


def is_results_append(node: ast.AST) -> bool:
    """Say whether a node is a results.append(...) call."""
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "append"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "results"
    )


def published_files() -> int:
    """Return how many files the site publishes, counted in docs/."""
    # docs/ rather than a build, because two other checks already prove the
    # two are the same tree byte for byte and a build here would cost a
    # minute to learn nothing new.
    return sum(1 for path in DOCS_ROOT.rglob("*") if path.is_file())


def modelled_pages() -> int:
    """Return how many pages the content model declares."""
    return len(read_json(SITE_DIR / "content" / "pages.json"))


def service_pages() -> int:
    """Return how many individual service line pages the tree publishes."""
    return len(list(DOCS_ROOT.glob("service-*.html")))


def image_filenames() -> int:
    """Return how many image filenames site.json declares."""
    return sum(1 for key in SITE if key.endswith("_filename"))


def brand_in_login() -> int:
    """Return how many times the login page writes the brand name as prose."""
    page = (SITE_DIR / "pages" / "login.page.frag").read_text(encoding="utf-8")
    return page.count(SITE["brand_name"])


def founder_tokens() -> int:
    """Return how many founder values reach the pages through a token."""
    return sum(
        1
        for key, value in FOUNDER.items()
        if isinstance(value, str) and key != "comment"
    )


# Each claim is a sentence a reader acts on, and a number only the tree knows.
# The regex has to match exactly once: a claim that has been reworded away is
# a failure rather than a pass, because a check that only reads what it finds
# is the defect class this repository exists to hunt.
CLAIMS = (
    (
        "README.md",
        rf"passes all {NUMBER} checks",
        verify_site_checks,
        "checks verify_site.py runs",
    ),
    (
        "README.md",
        rf"{NUMBER} checks of its own that read the built tree",
        verify_site_checks,
        "checks verify_site.py runs",
    ),
    (
        "README.md",
        rf"adds the rehearsal as an? {NUMBER} check",
        lambda: check_site_checks()[1],
        "checks check_site.py --full runs",
    ),
    (
        "README.md",
        rf"it is not one of the {NUMBER}\.",
        lambda: check_site_checks()[0],
        "checks check_site.py runs by default",
    ),
    (
        "README.md",
        rf"returns all {NUMBER} files correctly",
        published_files,
        "files published under docs/",
    ),
    (
        "PERMISSIONS.md",
        rf"returns all {NUMBER} files correctly",
        published_files,
        "files published under docs/",
    ),
    (
        "README.md",
        rf"renders them into the {NUMBER} generated pages",
        modelled_pages,
        "pages the content model declares",
    ),
    (
        "README.md",
        rf"are the {NUMBER} individual service line pages",
        service_pages,
        "service-*.html pages in docs/",
    ),
    (
        "README.md",
        rf"the {NUMBER} image filenames, the three contact strings",
        image_filenames,
        "image filenames site.json declares",
    ),
    (
        "README.md",
        rf"which carries it {NUMBER} times as prose",
        brand_in_login,
        "brand name occurrences in login.page.frag",
    ),
    (
        "README.md",
        rf"the {NUMBER} biography strings",
        lambda: len(FOUNDER["biography_strings"]),
        "biography strings founder.json declares",
    ),
    (
        "README.md",
        rf"and the anchor slug\. These {NUMBER} reach",
        founder_tokens,
        "founder values that reach a page through a token",
    ),
)


def main() -> int:
    problems: list[str] = []
    checked = 0
    for file_name, pattern, truth, description in CLAIMS:
        path = PROJECT_ROOT / file_name
        text = path.read_text(encoding="utf-8")
        # Every claim is wrapped prose, so a sentence this check reads may be
        # split across a line and an indent. Each space in a pattern matches
        # any run of whitespace for that reason.
        matches = list(
            re.finditer(pattern.replace(" ", r"\s+"), text, re.IGNORECASE)
        )
        if len(matches) != 1:
            problems.append(
                f"{file_name}: the sentence this check reads matches "
                f"{len(matches)} times rather than once: {pattern!r}. Either "
                "the claim about the "
                f"{description} was reworded, in which case update this check, "
                "or it was deleted, in which case delete this check"
            )
            continue
        checked += 1
        claimed = parse_number(matches[0].group("n"))
        actual = truth()
        line = text[: matches[0].start()].count("\n") + 1
        if claimed is None:
            problems.append(
                f"{file_name}:{line}: {matches[0].group('n')!r} is not a "
                "number this check can read, so the claim about the "
                f"{description} cannot be compared against the tree"
            )
        elif claimed != actual:
            problems.append(
                f"{file_name}:{line}: says {matches[0].group('n')}, but there "
                f"are {actual} {description}"
            )

    for problem in problems:
        print(problem)
    print(
        f"\nchecked {checked} documented counts against the tree, "
        f"{len(problems)} problems"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
