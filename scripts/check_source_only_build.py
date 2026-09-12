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


def main():
    work = tempfile.mkdtemp(prefix="tectori-source-only-")
    try:
        source = os.path.join(work, "source")
        os.makedirs(source)
        for name in SOURCE_DIRS:
            shutil.copytree(
                os.path.join(REPO_ROOT, name), os.path.join(source, name)
            )
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
            print("[FAIL] the source alone builds the site: the build failed")
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
        f"{len(built)} files built, {len(published)} published, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
