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


def iter_py_files(root: Path) -> list[Path]:
    """Return every .py file under root, recursively, skipping build artifacts."""
    paths = []
    for candidate in root.rglob("*.py"):
        relative = candidate.relative_to(root)
        if any(
            part == "__pycache__" or part.startswith(".")
            for part in relative.parts[:-1]
        ):
            continue
        paths.append(candidate)
    return sorted(paths)


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

    # Every .py file under scripts/ is importable by the tree: a top level
    # script by its own filename, and anything inside a directory holding
    # Python files (with or without __init__.py) by that directory's name.
    # A script can also import a sibling in its own directory by bare name.
    # Neither is a dependency however it is spelled. __pycache__ and any
    # dotted directory are build artifacts, not scripts.
    scripts = iter_py_files(SCRIPT_DIR)
    local_files = {path.stem for path in scripts if path.parent == SCRIPT_DIR}
    local_packages = {
        path.relative_to(SCRIPT_DIR).parts[0]
        for path in scripts
        if path.parent != SCRIPT_DIR
    }
    allowed = set(sys.stdlib_module_names) | local_files | local_packages
    for path in scripts:
        rel = path.relative_to(SCRIPT_DIR).as_posix()
        siblings = {p.stem for p in scripts if p.parent == path.parent}
        for name in sorted(imported_modules(path) - allowed - siblings):
            problems.append(
                f"{rel}: imports {name!r}, which is not in the standard "
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
