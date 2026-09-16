"""Check that every command the documentation tells a reader to run would work."""

from __future__ import annotations

import ast
import fnmatch
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# Top-level directories that are never a document a reader types from: the
# generated site (an output, not an input, per THEORY.md) and git's own
# store. Anchored to the top level so a page that happens to sit under
# site/docs/ is still read; the tree has no such page today, but the name
# should not silently exempt one if it ever does.
EXCLUDED_DIRECTORIES = ("docs", ".git")

# Dated records. A reader consults these as history, and they quote retired
# commands on purpose, so reading them as instructions would fail this check
# on every rename or retired flag the project has ever made.
EXCLUDED_RECORDS = ("CHANGELOG.md", "WORK_BOARD.md", "BOARD_ARCHIVE_*.md")

# The sentence in README.md that promises this scope. Read rather than
# assumed, so a reworded promise and a reworded exclusion list cannot drift
# apart. Matched inside the bullet for this script only, since the record
# names also appear elsewhere in the README describing what each one is.
README = REPO_ROOT / "README.md"
BULLET_START = "`scripts/check_documented_commands.py`"

COMMAND_RE = re.compile(r"python\s+(scripts/[A-Za-z0-9_]+\.py)([^\n`]*)")
FLAG_RE = re.compile(r"(--[a-z][a-z0-9-]*)")


def discover_documents() -> list[str]:
    """Return every Markdown document a reader types commands from."""
    documents = []
    for path in REPO_ROOT.rglob("*.md"):
        relative = path.relative_to(REPO_ROOT)
        if len(relative.parts) > 1 and relative.parts[0] in EXCLUDED_DIRECTORIES:
            continue
        if any(fnmatch.fnmatch(relative.name, pattern) for pattern in EXCLUDED_RECORDS):
            continue
        documents.append(relative.as_posix())
    return sorted(documents)


def readme_bullet() -> str | None:
    """Return the bullet paragraph in README.md describing this script, or
    None if README.md is missing or no longer describes it."""
    if not README.is_file():
        return None
    text = README.read_text(encoding="utf-8")
    start = text.find(BULLET_START)
    if start == -1:
        return None
    end = text.find("\n- `scripts/", start)
    return text[start : end if end != -1 else len(text)]


def accepted_flags(path: Path) -> set[str]:
    """Return every long option this script's parser is built to accept."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    flags: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_argument"
        ):
            for argument in node.args:
                if (
                    isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                    and argument.value.startswith("--")
                ):
                    flags.add(argument.value)
    return flags


def main() -> int:
    problems: list[str] = []
    commands = 0
    flags_checked = 0

    documents = discover_documents()
    if "README.md" not in documents:
        problems.append(
            "README.md is the document every new owner reads first and is "
            "not among the documents this check found, so either the tree "
            "moved or this check is reading nothing"
        )

    bullet = readme_bullet()
    if bullet is None:
        problems.append(
            "README.md no longer describes check_documented_commands.py, so "
            "the promise this check reads about its own scope is gone"
        )
    else:
        for record in EXCLUDED_RECORDS:
            if record not in bullet:
                problems.append(
                    f"README.md's bullet about check_documented_commands.py does "
                    f"not name {record}, so the sentence and the exclusion list "
                    "in this script can drift apart without either failing"
                )

    for document in documents:
        path = REPO_ROOT / document
        if not path.is_file():
            problems.append(
                f"{document} is named here as a document a new owner reads "
                "and is not in the tree, so either it was renamed or this "
                "check is reading nothing"
            )
            continue
        text = path.read_text(encoding="utf-8")
        for match in COMMAND_RE.finditer(text):
            commands += 1
            relative, tail = match.group(1), match.group(2)
            script = REPO_ROOT / relative
            if not script.is_file():
                problems.append(
                    f"{document} tells a reader to run {relative}, which is "
                    "not in the tree, so the first thing they type fails"
                )
                continue
            accepted = accepted_flags(script)
            for flag in FLAG_RE.findall(tail):
                flags_checked += 1
                if flag not in accepted:
                    problems.append(
                        f"{document} runs {relative} with {flag}, which its "
                        "parser does not accept, so the command exits with a "
                        "usage error rather than doing what the sentence says"
                    )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the documented commands would run: "
        f"{commands} commands and {flags_checked} options read across "
        f"{len(documents)} documents, {len(problems)} problems"
    )
    for item in problems[:20]:
        print(f"       {item}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
