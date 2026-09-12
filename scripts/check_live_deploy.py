#!/usr/bin/env python3
"""Fetch every file in docs/ from the live site and report any that differs from what was published."""

# Nothing else answers whether a deploy landed. The six checks read the tree
# about to be deployed and say nothing about the host, and the workflow that
# publishes it reports that the artifact was accepted, not that the domain and
# the certificate answer with it. A build can be perfect, the push can
# succeed, the deploy can go green, and the site can still be serving last
# week because a cache is stale or the domain moved. This is the only check
# that reads what a visitor actually gets, so it needs the network and is not
# part of check_site.py.

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

# Every file in docs/ is expected to come back byte for byte, CNAME included.
# It was exempt until 2026-09-12, when the deploy moved from branch publishing
# to the workflow: branch publishing consumed CNAME and 404d it, and the
# workflow uploads the tree as an artifact and serves all of it. The exemption
# read a 200 there as proof the host was serving files literally, which the
# extensionless probe below now proves directly and better.
TIMEOUT_SECONDS = 30

# Every internal link and every canonical in the tree is extensionless, and
# nothing in the files says whether the host resolves one. A host that serves
# the tree literally returns all 43 files correctly and 404s on every link on
# every page, so checking the files alone would report a healthy site nobody
# can navigate. 404.html is excluded because a missing path is how it is
# served, which makes its own extensionless path meaningless.
EXTENSIONLESS_EXEMPT = {"404.html"}


def site_url():
    """Return the site's own base URL, from the one file that declares it."""
    path = os.path.join(REPO_ROOT, "site", "content", "site.json")
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))["site_url"].rstrip("/")


def digest(data):
    return hashlib.sha256(data).hexdigest()[:16]


def fetch(url):
    """Return the response body and status, or None and the status for an error response."""
    request = urllib.request.Request(url, headers={"User-Agent": "tectori-deploy-check"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.read(), response.status
    except urllib.error.HTTPError as error:
        return None, error.code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=None,
        help="base URL to check, defaulting to site_url in site/content/site.json",
    )
    args = parser.parse_args()
    base = (args.base or site_url()).rstrip("/")

    published = []
    for dir_path, _dir_names, file_names in os.walk(DOCS_DIR):
        for file_name in sorted(file_names):
            rel = os.path.relpath(
                os.path.join(dir_path, file_name), DOCS_DIR
            ).replace(os.sep, "/")
            published.append(rel)
    published.sort()

    problems = []
    matched = 0
    links = 0
    for rel in published:
        with open(os.path.join(DOCS_DIR, rel), "rb") as f:
            local = f.read()
        body, status = fetch(f"{base}/{rel}")
        if body is None:
            problems.append(f"{rel}: status {status}")
            continue
        if body != local:
            problems.append(
                f"{rel}: live copy differs, live {digest(body)} ({len(body)} bytes), "
                f"published {digest(local)} ({len(local)} bytes)"
            )
            continue
        matched += 1

        if not rel.endswith(".html") or rel in EXTENSIONLESS_EXEMPT:
            continue
        path = "" if rel == "index.html" else rel[: -len(".html")]
        link_body, link_status = fetch(f"{base}/{path}")
        if link_body is None:
            problems.append(
                f"/{path}: status {link_status}, though {rel} is served. Every "
                "internal link in the tree uses this form."
            )
        elif link_body != local:
            problems.append(
                f"/{path}: served, and not the same bytes as {rel}"
            )
        else:
            links += 1

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] {base} serves what docs/ holds: "
        f"{matched} of {len(published)} files identical, {links} extensionless "
        f"paths resolve to the same bytes, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    if not ok:
        print(
            "       A difference here is the deploy, not the tree. Check that the "
            "commit is on main and that Pages finished building it."
        )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
