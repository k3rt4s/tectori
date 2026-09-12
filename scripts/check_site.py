#!/usr/bin/env python3
"""Run every site check in one command and report which passed, which failed, and why."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DOCS_DIR = os.path.join(REPO_ROOT, "docs")


def script(name):
    return os.path.join(SCRIPT_DIR, name)


def run(title, argv):
    """Run one check to completion and return its title, exit code and combined output."""
    completed = subprocess.run(
        [sys.executable] + argv,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return title, completed.returncode, completed.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print only the summary, not each check's own output",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help=(
            "also rehearse a rebrand, which clones the tree outside the repo "
            "and takes about a minute"
        ),
    )
    args = parser.parse_args()

    results = []
    results.append(run(
        "build reproduces docs/ byte for byte",
        [script("build_site.py"), "--check"],
    ))
    results.append(run(
        "llms.txt has not drifted from the meta descriptions",
        [script("check_llms_drift.py")],
    ))
    results.append(run(
        "the tree is internally consistent as a site",
        [script("verify_site.py")],
    ))
    # Every check above reads a tree that already contains docs/, so none of
    # them can tell whether the source is sufficient on its own. This one
    # builds from a copy of site/ and scripts/ with no docs/ anywhere.
    results.append(run(
        "the source alone reproduces docs/",
        [script("check_source_only_build.py")],
    ))

    # The render comparison needs a real built tree, so build one into a
    # temporary directory rather than the default output location, which a
    # person may be holding output in.
    tmp_dir = tempfile.mkdtemp(prefix="tectori-check-site-")
    try:
        results.append(run(
            "a full build writes a complete tree",
            [script("build_site.py"), "--out", tmp_dir],
        ))
        results.append(run(
            "the built tree renders identically to docs/",
            [script("compare_render.py"), DOCS_DIR, tmp_dir],
        ))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Off the default path on purpose. The six checks above read the tree
    # that is about to deploy and are what a deploy should wait for. The
    # rehearsal answers a different question, whether someone else could make
    # this site theirs, and it writes a whole clone outside the repo to do it.
    # That is worth running when the build or the content model changes, and
    # not worth making every deploy wait for.
    if args.full:
        results.append(run(
            "a new owner could rebrand the site and it would still pass",
            [script("rehearse_rebrand.py")],
        ))

    if not args.quiet:
        for title, code, output in results:
            print("=" * 72)
            print(f"{title}")
            print("=" * 72)
            print(output.rstrip())
            print()

    failed = [title for title, code, _output in results if code != 0]
    print("-" * 72)
    for title, code, _output in results:
        print(f"[{'PASS' if code == 0 else 'FAIL'}] {title}")
    print("-" * 72)
    if failed:
        print(f"{len(failed)} of {len(results)} checks failed. Re-run without --quiet to see why.")
        sys.exit(1)
    print(f"{len(results)}/{len(results)} checks passed against {DOCS_DIR}")


if __name__ == "__main__":
    main()
