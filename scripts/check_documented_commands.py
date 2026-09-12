"""Check that every command the documentation tells a reader to run would work."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
# The documents a new owner reads and types from. A command in any of them is
# an instruction, not an illustration.
DOCUMENTS = ("README.md", "PERMISSIONS.md", "SEARCH_SETUP.md")

COMMAND_RE = re.compile(r"python\s+(scripts/[A-Za-z0-9_]+\.py)([^\n`]*)")
FLAG_RE = re.compile(r"(--[a-z][a-z0-9-]*)")


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

    for document in DOCUMENTS:
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
        f"{len(DOCUMENTS)} documents, {len(problems)} problems"
    )
    for item in problems[:20]:
        print(f"       {item}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
