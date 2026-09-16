"""Check that every check in this repository is actually run by something."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
RUNNER = SCRIPT_DIR / "check_site.py"
VERIFIER = SCRIPT_DIR / "verify_site.py"
README = REPO_ROOT / "README.md"

# A check script the runner does not call, with the reason it does not, and the
# sentence in README.md that has to still say so. A check left out of the
# runner is a check that never runs, which is the one thing worse than not
# having written it, so the exceptions are named here and nowhere else.
EXPECTED_UNWIRED = {
    "check_site.py": (
        "is the runner itself",
        None,
    ),
    "check_live_deploy.py": (
        "reads the published site rather than the tree, so it needs the network",
        r"It needs the network, so it is not one of the",
    ),
}


def iter_check_files(root: Path) -> list[Path]:
    """Return every check_*.py file under root, recursively, skipping build artifacts."""
    paths = []
    for candidate in root.rglob("check_*.py"):
        relative = candidate.relative_to(root)
        if any(
            part == "__pycache__" or part.startswith(".")
            for part in relative.parts[:-1]
        ):
            continue
        paths.append(candidate)
    return sorted(paths)


def _is_script_call(node: ast.AST) -> bool:
    """Return whether node is a call to the script() helper with a literal name."""
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "script"
        and bool(node.args)
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    )


def _scan_scope(stmts: list, calls: set, names: set) -> None:
    """Collect script() calls and referenced names from one scope.

    Follows control flow (if/for/while/try/with) inside the given statements
    but does not step into a nested function, lambda or class body, since that
    is a separate scope that only runs when something calls or references it
    by name.
    """

    def walk(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(
                child,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef),
            ):
                continue
            if _is_script_call(child):
                calls.add(child.args[0].value)
            if isinstance(child, ast.Name):
                names.add(child.id)
            elif isinstance(child, ast.Attribute):
                names.add(child.attr)
            walk(child)

    for stmt in stmts:
        walk(stmt)


def called_scripts(path: Path) -> set[str]:
    """Return every script name reachable when the runner actually runs.

    Reachable means module-level code, including the if __name__ block, plus
    any function that reachable code calls or passes by name (as a callback
    or inside a list, for example), applied the same way to nested functions
    and methods. This is a name match over the source, not a trace of
    execution: a script() call that only sits inside a function nothing
    reachable ever names by that name does not count.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    functions_by_name: dict = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions_by_name.setdefault(node.name, []).append(node)

    calls: set[str] = set()
    seed = [
        stmt
        for stmt in tree.body
        if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    names_found: set = set()
    _scan_scope(seed, calls, names_found)

    visited_functions: set = set()
    to_expand = list(names_found)
    while to_expand:
        name = to_expand.pop()
        for func in functions_by_name.get(name, []):
            if id(func) in visited_functions:
                continue
            visited_functions.add(id(func))
            new_names: set = set()
            _scan_scope(func.body, calls, new_names)
            to_expand.extend(new_names)

    return calls


def verifier_checks(path: Path) -> tuple[set[str], set[str]]:
    """Return the check functions defined in the verifier and the ones it runs."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    defined = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("check_")
    }
    main = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "main"
        ),
        None,
    )
    called: set[str] = set()
    if main is not None:
        for node in ast.walk(main):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id.startswith("check_")
            ):
                called.add(node.func.id)
    return defined, called


def main() -> int:
    problems: list[str] = []

    wired = called_scripts(RUNNER)
    readme = " ".join(README.read_text(encoding="utf-8").split())
    for path in iter_check_files(SCRIPT_DIR):
        # check_site.py passes the runner a name relative to SCRIPT_DIR, its
        # own directory, so a top level script is wired by its filename and a
        # nested one only by the same relative path the runner would need to
        # pass to reach it. EXPECTED_UNWIRED still keys on the plain filename,
        # because every exception in it names a top level script.
        rel = path.relative_to(SCRIPT_DIR).as_posix()
        name = path.name
        if rel in wired:
            continue
        if name not in EXPECTED_UNWIRED:
            problems.append(
                f"{rel} is a check that check_site.py does not run, so it "
                "passes or fails where nobody looks. Either add it to the "
                "runner or say in this check why it cannot be run there"
            )
            continue
        reason, sentence = EXPECTED_UNWIRED[name]
        if sentence and not re.search(" ".join(sentence.split()), readme):
            problems.append(
                f"{rel} is left out of the runner because it {reason}, and "
                "README.md no longer carries the sentence saying so, so a "
                "reader counting the checks is counting a different number"
            )

    for name in sorted(EXPECTED_UNWIRED):
        if not (SCRIPT_DIR / name).exists():
            problems.append(
                f"{name} is named here as a check the runner deliberately "
                "leaves out and no longer exists, so this exception is stale"
            )
        elif name in wired and EXPECTED_UNWIRED[name][1]:
            problems.append(
                f"{name} is now run by check_site.py and is still listed here "
                "as an exception, so the reason above is no longer true"
            )

    defined, called = verifier_checks(VERIFIER)
    for name in sorted(defined - called):
        problems.append(
            f"verify_site.py defines {name} and main() never calls it, so it "
            "is a check that was written and does not run"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] every check here is run by something: "
        f"{len(wired)} scripts wired into the runner, {len(called)} checks "
        f"inside verify_site.py, {len(problems)} problems"
    )
    for item in problems[:20]:
        print(f"       {item}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
