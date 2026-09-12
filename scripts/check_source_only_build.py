#!/usr/bin/env python3
"""Build the site from a copy of site/ and scripts/ alone and compare the result against docs/."""

# The question this answers is whether the source is sufficient. Until
# 2026-09-12 it was not: the stylesheet, the script and the twelve images lived
# in docs/ and the build copied them from there to there, so the output
# directory was an input to its own build. A clone without docs/ produced 29
# files, no styling and no images, and printed that there was nothing to copy.
# Every other check passed, because every other check reads a tree that already
# has docs/ in it. This one deletes that assumption: it copies site/ and
# scripts/ somewhere else, builds there, and requires the result to be docs/
# byte for byte.

import os
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

SOURCE_DIRS = ("site", "scripts")


def tree(root):
    """Return every file under root as a set of forward-slash relative paths."""
    found = set()
    for dir_path, _dir_names, file_names in os.walk(root):
        for file_name in file_names:
            rel = os.path.relpath(os.path.join(dir_path, file_name), root)
            found.add(rel.replace(os.sep, "/"))
    return found


def tracked_files():
    """Return the source files git carries, or None where there is no git tree."""
    # What a new owner receives is a clone, which holds what git carries and
    # nothing else. Copying the working directory instead would prove that
    # this machine can build the site, which nobody doubts: a new source file
    # that was never added builds here and is absent from the clone, and this
    # check is the one that is supposed to say so.
    try:
        # Asked first, because a tree with no history of its own can sit
        # inside someone else's repository, and listing that one's files
        # would answer a question nobody asked.
        root = subprocess.run(
            ["git", "-C", REPO_ROOT, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        )
        if root.returncode != 0:
            return None
        if os.path.realpath(root.stdout.strip()) != os.path.realpath(REPO_ROOT):
            return None
        result = subprocess.run(
            ["git", "-C", REPO_ROOT, "ls-files", "-z", "--"] + list(SOURCE_DIRS),
            capture_output=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return [
        name.decode("utf-8")
        for name in result.stdout.split(b"\0")
        if name
    ]


def copy_source(source):
    """Copy the source into a bare directory and say what was copied from."""
    names = tracked_files()
    if names is None:
        # The rebrand rehearsal runs this check inside a clone with no git
        # history, which is deliberate: it is a copy of the tree, not a
        # repository. There is nothing to be tracked there, so the working
        # copy is the only answer available and the line below says so.
        for name in SOURCE_DIRS:
            shutil.copytree(
                os.path.join(REPO_ROOT, name), os.path.join(source, name)
            )
        return "the working copy, because this tree has no git history"
    for name in names:
        target = os.path.join(source, name.replace("/", os.sep))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(os.path.join(REPO_ROOT, name), target)
    return f"the {len(names)} source files git carries"


def main():
    work = tempfile.mkdtemp(prefix="tectori-source-only-")
    try:
        source = os.path.join(work, "source")
        os.makedirs(source)
        copied_from = copy_source(source)
        out_dir = os.path.join(work, "out")
        result = subprocess.run(
            [
                sys.executable,
                os.path.join(source, "scripts", "build_site.py"),
                "--out",
                out_dir,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(
                "[FAIL] the source alone builds the site: the build failed, "
                f"from {copied_from}"
            )
            print(result.stdout.rstrip())
            print(result.stderr.rstrip())
            return 1

        built = tree(out_dir)
        published = tree(DOCS_DIR)
        problems = []
        for rel in sorted(published - built):
            problems.append(f"{rel}: in docs/ and not built from the source alone")
        for rel in sorted(built - published):
            problems.append(f"{rel}: built from the source alone and not in docs/")
        for rel in sorted(built & published):
            with open(os.path.join(out_dir, rel), "rb") as f:
                a = f.read()
            with open(os.path.join(DOCS_DIR, rel), "rb") as f:
                b = f.read()
            if a != b:
                problems.append(
                    f"{rel}: differs from docs/ ({len(a)} bytes built, {len(b)} published)"
                )
    finally:
        shutil.rmtree(work, ignore_errors=True)

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] site/ and scripts/ alone reproduce docs/: "
        f"{len(built)} files built from {copied_from}, "
        f"{len(published)} published, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
