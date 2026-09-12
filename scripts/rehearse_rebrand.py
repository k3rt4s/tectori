"""Rebrand a throwaway clone of this site to a fixture business and check the result."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(
    "C:" + chr(92) + "Code_data", "tectori", "reproducible", "rehearsal"
)

# A business that does not exist, on a domain that cannot resolve. The values
# are deliberately shaped unlike this site's: a different area code format, a
# longer street line, a two word brand. A fixture that resembles the original
# can pass by accident.
FIXTURE = {
    "brand_name": "Northvale Grove",
    "tagline": "Evidence-first IT for teams under review",
    "site_url": "https://www.northvale-grove.example",
    "logo_filename": "northvale-logo.png",
    "social_image_filename": "northvale-social.png",
    "favicon_filename": "northvale-favicon.png",
    "phone_display": "(312) 555-0148",
    "phone_tel_uri": "tel:+13125550148",
    "phone_schema": "+1-312-555-0148",
    "postal_address": "8800 North Wacker Drive, Suite 1200, Chicago, IL 60606",
}

# The accounts a new owner opens in their own name. These are nested under
# "third_party" rather than declared at the top level, which is the only
# reason they are a second dict. They matter more than they look: the form
# endpoint decides whose inbox a visitor's message lands in, so a rebrand
# that misses it sends the new owner's enquiries to the previous one.
THIRD_PARTY_FIXTURE = {
    "cloudflare_beacon_token": "0123456789abcdef0123456789abcdef",
    "scarf_pixel_id": "00000000-0000-4000-8000-000000000000",
    "formspree_endpoint": "https://formspree.io/f/xnorthvale",
}

# The profiles the footer links from every page. Nested under "social" for the
# same reason the block above is nested, and missed for longer: until the
# residue scan below covered every declared value, a rebrand left the previous
# owner's LinkedIn and GitHub on all 24 pages and every check still passed.
SOCIAL_FIXTURE = {
    "linkedin": "https://www.linkedin.com/company/northvale-grove",
    "github": "https://github.com/northvale-grove",
}

TEXT_SUFFIXES = {".html", ".xml", ".txt", ".css", ".js", ""}


def clone(out_dir):
    """Copy the repo tree to a scratch directory, without its git history."""
    shutil.rmtree(out_dir, ignore_errors=True)
    shutil.copytree(
        REPO_ROOT, out_dir, ignore=shutil.ignore_patterns(".git", "__pycache__")
    )


def read_json(path):
    """Return the parsed contents of a UTF-8 JSON file."""
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def host_of(site_url):
    """Return the hostname a site URL carries."""
    return site_url.split("://", 1)[1].rstrip("/")


def apex_of(site_url):
    """Return the hostname without its leading www, which prose uses."""
    return host_of(site_url).split("www.", 1)[-1]


def rewrite_site_json(out_dir):
    """Apply runbook step 1: replace every declared value with the fixture's."""
    path = os.path.join(out_dir, "site", "content", "site.json")
    config = read_json(path)
    for key, value in FIXTURE.items():
        if key not in config:
            raise KeyError(
                f"site.json has no {key!r}, so the fixture and the content "
                "model have diverged and this rehearsal would prove less "
                "than it claims"
            )
        config[key] = value
    for key, value in THIRD_PARTY_FIXTURE.items():
        if key not in config["third_party"]:
            raise KeyError(
                f"site.json declares no third_party.{key!r}, so the fixture "
                "and the content model have diverged and this rehearsal would "
                "prove less than it claims"
            )
        config["third_party"][key] = value
    for key, value in SOCIAL_FIXTURE.items():
        if key not in config["social"]:
            raise KeyError(
                f"site.json declares no social.{key!r}, so the fixture and "
                "the content model have diverged and this rehearsal would "
                "prove less than it claims"
            )
        config["social"][key] = value
    text = json.dumps(config, indent=2, ensure_ascii=False)
    with open(path, "wb") as f:
        f.write((text.replace("\n", "\r\n") + "\r\n").encode("utf-8"))


def rename_assets(out_dir, original):
    """Apply runbook step 2: rename the three images site.json declares by name."""
    assets = os.path.join(out_dir, "docs", "assets")
    for key in ("logo_filename", "social_image_filename", "favicon_filename"):
        os.rename(
            os.path.join(assets, original[key]),
            os.path.join(assets, FIXTURE[key]),
        )


def run(out_dir, args):
    """Run one of the repo's own scripts inside the clone and return the result."""
    return subprocess.run(
        [sys.executable] + args,
        cwd=out_dir,
        capture_output=True,
        text=True,
    )


def text_files(docs_root):
    """Yield every file under a built tree that a reader or a crawler can read."""
    for dir_path, _, file_names in os.walk(docs_root):
        for name in sorted(file_names):
            if os.path.splitext(name)[1].lower() in TEXT_SUFFIXES:
                yield os.path.join(dir_path, name)


def declared_values(original):
    """Return every value a new owner replaces, labelled by where it is declared."""
    # The brand name is the one declared value left out, by design: most of its
    # occurrences are body copy a new owner rewrites rather than rebrands, so it
    # is counted below rather than failed on. Everything else reaches the pages
    # through the build's token map, which means one occurrence of the old value
    # in a built page is a page the token never reached.
    values = {"site_url apex": apex_of(original["site_url"])}
    for key, value in original.items():
        if isinstance(value, str) and key not in ("comment", "brand_name"):
            values[key] = value
    for group in ("third_party", "social"):
        for key, value in original[group].items():
            values[group + "." + key] = value
    return values


def value_residue(out_dir, original):
    """Return every line of the rebranded tree that still carries an old value."""
    hits = []
    for label, value in sorted(declared_values(original).items()):
        hits.extend(residue_for(out_dir, label, value))
    return hits


def residue_for(out_dir, label, value):
    """Return every line of the rebranded tree that still carries one old value."""
    pattern = re.compile(re.escape(value), re.IGNORECASE)
    docs = os.path.join(out_dir, "docs")
    hits = []
    for path in text_files(docs):
        try:
            with open(path, "rb") as f:
                text = f.read().decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                rel = os.path.relpath(path, docs)
                hits.append(f"{label}: {rel}:{number}: {line.strip()[:70]}")
    return hits


def brand_residue(out_dir, original):
    """Count what still names the old brand, which its copy is expected to."""
    pattern = re.compile(re.escape(original["brand_name"]), re.IGNORECASE)
    total = 0
    for path in text_files(os.path.join(out_dir, "docs")):
        with open(path, "rb") as f:
            total += len(pattern.findall(f.read().decode("utf-8", "ignore")))
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help="where to build the throwaway clone, which must be outside the repo",
    )
    args = parser.parse_args()
    out_dir = os.path.abspath(args.out)
    if os.path.commonpath([out_dir, REPO_ROOT]) == REPO_ROOT:
        # The clone is generated data and a rewritten copy of every page. Letting
        # it land inside the repo would put a second, wrong copy of the site
        # under version control.
        raise SystemExit(f"refusing to write the clone inside the repo: {out_dir}")

    original = read_json(os.path.join(REPO_ROOT, "site", "content", "site.json"))
    print(f"Cloning to {out_dir}")
    clone(out_dir)
    rewrite_site_json(out_dir)
    rename_assets(out_dir, original)
    print("Applied the two mechanical runbook steps")

    build = run(out_dir, [os.path.join("scripts", "build_site.py"), "--out", "docs"])
    if build.returncode != 0:
        print(build.stdout)
        print(build.stderr)
        raise SystemExit("the rebranded tree does not build")
    print(build.stdout.strip())

    checks = run(out_dir, [os.path.join("scripts", "check_site.py")])
    for line in checks.stdout.splitlines():
        if line.startswith("[") or "passed" in line:
            print(f"  {line.rstrip()}")

    residue = value_residue(out_dir, original)
    brand_hits = brand_residue(out_dir, original)
    checked = len(declared_values(original))
    print(
        f"Of the {checked} declared values a new owner replaces, the old value "
        f"survives on {len(residue)} lines of the rebranded tree, and the old "
        f"brand name appears {brand_hits} times in copy a new owner rewrites."
    )
    for hit in residue[:20]:
        print(f"  {hit}")

    ok = checks.returncode == 0 and not residue
    print("REHEARSAL PASSED" if ok else "REHEARSAL FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
