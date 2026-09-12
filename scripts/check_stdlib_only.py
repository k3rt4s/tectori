"""Check that every script imports only the standard library, which is what the manifest promises."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent

# The sentence this check exists to keep true. It is read rather than assumed,
# so deleting the promise and deleting the check stay one action instead of
# two, and a reworded promise fails here rather than passing unnoticed.
CLAIM = "The scripts import only the standard library"


def imported_modules(path: Path) -> set[str]:
    """Return the top level module name of every import a script makes."""
    names = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            # A relative import is this directory, which is not a dependency.
            if node.level == 0 and node.module:
                names.add(node.module.split(".")[0])
    return names


def main() -> int:
    problems: list[str] = []

    manifest = PROJECT_ROOT / "PERMISSIONS.md"
    text = manifest.read_text(encoding="utf-8")
    if text.count(CLAIM) != 1:
        problems.append(
            f"PERMISSIONS.md no longer says {CLAIM!r} exactly once, so either "
            "the promise was reworded, in which case update this check, or it "
            "was withdrawn, in which case delete this check"
        )

    # A file beside the scripts is importable by them, and a module the tree
    # carries is not a dependency however it is spelled.
    local = {path.stem for path in SCRIPT_DIR.glob("*.py")}
    allowed = set(sys.stdlib_module_names) | local

    scripts = sorted(SCRIPT_DIR.glob("*.py"))
    for path in scripts:
        for name in sorted(imported_modules(path) - allowed):
            problems.append(
                f"{path.name}: imports {name!r}, which is not in the standard "
                "library, so a clone of this repository no longer runs on a "
                "machine with nothing installed"
            )

    requirements = PROJECT_ROOT / "requirements.txt"
    if requirements.is_file():
        problems.append(
            "requirements.txt exists, and PERMISSIONS.md says there is none "
            "on purpose rather than by oversight; one of the two is wrong"
        )

    for problem in problems:
        print(problem)
    ok = not problems
    print(
        f"\n[{'PASS' if ok else 'FAIL'}] every script runs on a machine with "
        f"nothing installed: {len(scripts)} scripts read, {len(problems)} problems"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
