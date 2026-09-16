"""Check that the egress manifest names exactly the hosts the site declares."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
MANIFEST = REPO_ROOT / "PERMISSIONS.md"
SITE_CONFIG = REPO_ROOT / "site" / "content" / "site.json"

SECTION_HEADING = "## Network egress"
# The sentence that makes the two lists one promise. Read from the manifest so
# that withdrawing the promise and dropping this check stay one action.
CLAIM = (
    "Every host above is declared in `site/content/site.json` with the reason "
    "it is there"
)
# A hostname as any prose can write it: bare, inside backticks or bold, or
# inside a URL. Labels are alnum and hyphen, the last label is letters only
# and at least two of them, and the match cannot start or continue mid-word,
# so `docs/login.html`, `e.g.` and `v1.2` never look like one on their own;
# what still reads as a file (`site.json`, `verify.yml`) is dropped below by
# its extension instead of by a hard-coded name.
HOST_RE = re.compile(
    r"(?<![\w.-])"
    r"((?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})"
    r"(?![a-zA-Z0-9-])"
)


def repo_file_extensions() -> set[str]:
    """Return every file extension present under the repo tree, lower case."""
    extensions: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        for filename in filenames:
            if "." in filename:
                extensions.add(filename.rsplit(".", 1)[1].lower())
    return extensions


def manifest_hosts(text: str) -> set[str]:
    """Return every hostname named in the network egress section."""
    start = text.index(SECTION_HEADING)
    rest = text[start + len(SECTION_HEADING) :]
    end = rest.find("\n## ")
    section = rest if end == -1 else rest[:end]
    extensions = repo_file_extensions()
    found: set[str] = set()
    for match in HOST_RE.finditer(section):
        host = match.group(1).lower()
        if host.rsplit(".", 1)[1] in extensions:
            continue
        found.add(host)
    return found


def main() -> int:
    text = MANIFEST.read_text(encoding="utf-8")
    site = json.loads(SITE_CONFIG.read_text(encoding="utf-8"))
    declared = set(site["allowed_external_hosts"])
    problems: list[str] = []

    if " ".join(text.split()).count(" ".join(CLAIM.split())) != 1:
        problems.append(
            f"PERMISSIONS.md no longer states {CLAIM!r} exactly once, so "
            "either the sentence was reworded, in which case update this "
            "check, or the promise was withdrawn, in which case say what the "
            "manifest's host list now means"
        )

    named = manifest_hosts(text)
    for host in sorted(declared - named):
        problems.append(
            f"{host} is declared in site.json and is not in the manifest's "
            "egress section, so a buyer building a firewall rule from this "
            "document blocks it"
        )
    for host in sorted(named - declared):
        problems.append(
            f"{host} is named in the manifest's egress section and is not "
            "declared in site.json, so nothing checks the tree against it"
        )

    endpoint_host = (
        site["third_party"]["formspree_endpoint"].split("://", 1)[1].split("/")[0]
    )
    if endpoint_host not in named:
        problems.append(
            f"the contact form posts to {endpoint_host}, which the manifest's "
            "egress section does not name"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the egress manifest and the declared "
        f"hosts are one list: {len(named)} hosts named, {len(declared)} "
        f"declared, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
