"""Check that only the scripts the permissions manifest names can reach the network."""

from __future__ import annotations

import ast
import re
import shlex
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
MANIFEST = REPO_ROOT / "PERMISSIONS.md"

# Standard library modules that open a socket, listen on one, or hand the work
# to something that does. check_stdlib_only.py permits every one of them,
# because they are all standard library, which is exactly why this is a
# separate question from that one.
NETWORK_MODULES = {
    "asyncio", "ftplib", "http", "imaplib", "nntplib", "poplib", "smtplib",
    "socket", "socketserver", "ssl", "telnetlib", "urllib", "webbrowser",
    "wsgiref", "xmlrpc",
}
# Programs that fetch, run through subprocess, where the import scan sees only
# subprocess and would report the script as offline.
NETWORK_PROGRAMS = {
    "curl", "wget", "Invoke-WebRequest", "Invoke-RestMethod", "scp", "sftp",
    "ssh", "rsync",
}

# A string constant can also be a shell command line, as os.system, os.popen
# and subprocess with shell=True all take one. Split it into commands on the
# shell separators below and read only the first word of each: a network
# program named later in the line is an argument or a path, not the command
# being run, and reading past the first word would also catch the program
# name inside ordinary prose that only mentions it. The comparison against
# NETWORK_PROGRAMS stays case-sensitive for the same reason, so a sentence
# that opens with a capitalised word does not match the lowercase command it
# only refers to. Before taking that word, skip any leading shell assignment
# (FOO=1) and any leading wrapper command (env, sudo, nohup, exec, command,
# time, nice) together with that wrapper's own option flags, since none of
# those is the program actually being run.
COMMAND_SPLIT_RE = re.compile(r"&&|\|\||[;|&\n]")
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
WRAPPER_COMMANDS = {"env", "sudo", "nohup", "exec", "command", "time", "nice"}


def command_words(value: str) -> list[str]:
    """Return the command word of each shell command segment found in value."""
    words = []
    for segment in COMMAND_SPLIT_RE.split(value):
        stripped = segment.strip()
        try:
            tokens = shlex.split(stripped, posix=True)
        except ValueError:
            tokens = stripped.split()
        seen_wrapper = False
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if ASSIGNMENT_RE.match(token):
                index += 1
                continue
            if token in WRAPPER_COMMANDS:
                seen_wrapper = True
                index += 1
                continue
            if seen_wrapper and token.startswith("-"):
                index += 1
                continue
            break
        if index >= len(tokens):
            continue
        word = tokens[index]
        # shlex.split already removes matched quotes; this still strips them
        # from the plain-split fallback path above.
        if len(word) >= 2 and word[0] == word[-1] and word[0] in "\"'":
            word = word[1:-1]
        words.append(word)
    return words


CLAIM_RE = re.compile(
    r"Two\s+scripts\s+here\s+can\s+reach\s+the\s+network\s+and\s+nothing"
    r"\s+else\s+can:(.*?)\n\s*\n",
    re.DOTALL,
)
SCRIPT_RE = re.compile(r"`(scripts/[A-Za-z0-9_/]+\.py)`")


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


def network_reasons(path: Path) -> list[str]:
    """Return every way this script could reach the network, as plain phrases."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    # In this file the fetching program names above are data rather than
    # behaviour, so its string constants are not read. The import half still
    # measures it: this script cannot open a socket without failing itself.
    read_strings = path.resolve() != Path(__file__).resolve()
    reasons: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in NETWORK_MODULES:
                    reasons.append(f"imports {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in NETWORK_MODULES:
                reasons.append(f"imports from {node.module}")
        elif (
            read_strings
            and isinstance(node, ast.Constant)
            and isinstance(node.value, str)
        ):
            name = node.value.split("/")[-1].split("\\")[-1]
            if name in NETWORK_PROGRAMS or name.removesuffix(".exe") in NETWORK_PROGRAMS:
                reasons.append(f"runs {node.value}")
            else:
                for word in command_words(node.value):
                    word_name = word.split("/")[-1].split("\\")[-1]
                    if (
                        word_name in NETWORK_PROGRAMS
                        or word_name.removesuffix(".exe") in NETWORK_PROGRAMS
                    ):
                        reasons.append(f"runs {word}")
    return sorted(set(reasons))


def claimed_scripts(text: str) -> tuple[set[str], str | None]:
    """Return the scripts the manifest names as the exceptions, and any problem."""
    matches = CLAIM_RE.findall(text)
    if len(matches) != 1:
        return set(), (
            "PERMISSIONS.md no longer says 'Two scripts here can reach the "
            "network and nothing else can:' exactly once, so either the "
            "sentence was reworded, in which case update this check, or the "
            "claim was withdrawn, in which case say what a buyer should now "
            "expect this repository to contact"
        )
    return set(SCRIPT_RE.findall(matches[0])), None


def main() -> int:
    text = MANIFEST.read_text(encoding="utf-8")
    named, problem = claimed_scripts(text)
    problems: list[str] = [problem] if problem else []

    found: dict[str, list[str]] = {}
    scripts = iter_py_files(SCRIPT_DIR)
    for path in scripts:
        reasons = network_reasons(path)
        if reasons:
            rel = path.relative_to(SCRIPT_DIR).as_posix()
            found[f"scripts/{rel}"] = reasons

    for name in sorted(set(found) - named):
        problems.append(
            f"{name} can reach the network ({', '.join(found[name])}) and "
            "PERMISSIONS.md does not name it, so an operator reading that "
            "document does not know this repository contacts anything"
        )
    for name in sorted(named - set(found)):
        problems.append(
            f"PERMISSIONS.md names {name} as one of the scripts that reach "
            "the network and it no longer does, so the manifest overstates "
            "what has to be allowed through"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] only the named scripts can reach the "
        f"network: {len(scripts)} scripts read, {len(found)} reach it, "
        f"{len(problems)} problems"
    )
    for item in problems[:20]:
        print(f"       {item}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
