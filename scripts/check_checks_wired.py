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


def called_scripts(path: Path) -> set[str]:
    """Return every script name the runner passes to its script() helper."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "script"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            names.add(node.args[0].value)
    return names


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
    for path in sorted(SCRIPT_DIR.glob("check_*.py")):
        name = path.name
        if name in wired:
            continue
        if name not in EXPECTED_UNWIRED:
            problems.append(
                f"{name} is a check that check_site.py does not run, so it "
                "passes or fails where nobody looks. Either add it to the "
                "runner or say in this check why it cannot be run there"
            )
            continue
        reason, sentence = EXPECTED_UNWIRED[name]
        if sentence and not re.search(" ".join(sentence.split()), readme):
            problems.append(
                f"{name} is left out of the runner because it {reason}, and "
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
