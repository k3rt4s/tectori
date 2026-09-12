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
    parser.add_argument(
        "--no-history",
        action="store_true",
        help=(
            "skip the sitemap date check, for a copy of the tree that carries "
            "no commit history to read"
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
    # Dates are the one thing in this tree that nothing can derive: the build
    # has no history to read, and a rebuild from source alone must produce the
    # same bytes, so the sitemap's dates are hand written and decay in silence.
    # This check is the only one here that reads git rather than the tree.
    # Skipped only where there is provably nothing to read: a copy of
    # the tree made outside a repository. It is never skipped because the
    # answer is inconvenient, and the check itself refuses to pass on a clone
    # whose history is too shallow to answer the question.
    if not args.no_history:
        results.append(run(
            "the sitemap's dates match the pages",
            [script("check_lastmod.py")],
        ))
    # The check above proves the source is sufficient on this machine, which
    # has a Python that has had things installed into it. A dependency added
    # to a script is invisible to it, and to every other check here, until a
    # buyer clones the repository onto a machine that has nothing.
    results.append(run(
        "the scripts need nothing installed",
        [script("check_stdlib_only.py")],
    ))
    # And every check above reads the tree rather than what the repository
    # says about it. A README that names the wrong count is what a new owner
    # follows, and nothing else here reads a sentence.
    results.append(run(
        "the documentation's counts match the tree",
        [script("check_doc_claims.py")],
    ))
    # That one reads counts. The permissions manifest makes a different kind
    # of claim, a list of the hosts this site talks to, and a buyer builds a
    # firewall rule from it. Nothing read it, so the manifest and the config
    # could disagree and every check would still pass.
    results.append(run(
        "the egress manifest names the declared hosts",
        [script("check_permissions_hosts.py")],
    ))
    # That reads the hosts a visitor's browser reaches. The other half of the
    # same promise is what the repository itself contacts, and the standard
    # library check permits urllib, so a script could start fetching and
    # every check here would still pass.
    results.append(run(
        "only the named scripts reach the network",
        [script("check_no_network_calls.py")],
    ))
    # And every check above runs because a line here says so. A check written
    # and never added to this list, or a function in verify_site.py never put
    # in its results, reports nothing and looks exactly like one that passes.
    results.append(run(
        "every check here is run by something",
        [script("check_checks_wired.py")],
    ))
    # Every check so far reads the markup as structure. A class name is the
    # half of the markup that only the stylesheet gives meaning to, and a
    # class nothing defines renders as nothing while the page stays valid,
    # reachable, byte identical and wrong.
    results.append(run(
        "every class a page uses is defined",
        [script("check_class_names.py")],
    ))
    # And every check reads the tree, not how the tree reaches the site. The
    # deploy job is the only route there, and deleting the one line that makes
    # it wait would leave every check passing while a red run shipped again.
    results.append(run(
        "the deploy waits for the checks",
        [script("check_deploy_gate.py")],
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

    # Off the default path on purpose. The checks above read the tree that
    # is about to deploy and are what a deploy should wait for. The
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
