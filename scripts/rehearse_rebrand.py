"""Rebrand a throwaway clone of this site to a fixture business and check the result."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The system temporary directory, not a path on the machine this site was
# built on. The clone is throwaway generated data and must land outside the
# repo, and the check below enforces that wherever --out points.
DEFAULT_OUT = os.path.join(tempfile.gettempdir(), "tectori-rehearsal")

# A business that does not exist, on a domain that cannot resolve. The values
# are deliberately shaped unlike this site's: a different area code format, a
# longer street line, a two word brand. A fixture that resembles the original
# can pass by accident.
# Every image site.json names. The hero pair and the band image joined the
# other three on 2026-09-12; until then the stylesheet and the home page
# fragment carried their filenames, so a new owner edited two files by hand.
ASSET_KEYS = (
    "logo_filename",
    "social_image_filename",
    "favicon_filename",
    "hero_webp_filename",
    "hero_png_filename",
    "band_image_filename",
)

FIXTURE = {
    "brand_name": "Northvale Grove",
    "tagline": "Evidence-first IT for teams under review",
    "site_url": "https://www.northvale-grove.example",
    "logo_filename": "northvale-logo.png",
    "social_image_filename": "northvale-social.png",
    "favicon_filename": "northvale-favicon.png",
    "hero_webp_filename": "northvale-hero.webp",
    "hero_png_filename": "northvale-hero.png",
    "band_image_filename": "northvale-band.jpg",
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

# The person the fixture practice is. The founder's name, given name, job
# title and anchor reach the pages through the token map like every other
# declared value, so a rebrand that misses one leaves a real person's name in
# the structured data of a site they have never heard of. That is what this
# fixture exists to prove cannot happen quietly: until 2026-09-12 none of it
# was in the content model at all, and the rehearsal could not see it.
FOUNDER_FIXTURE = {
    "name": "Avery Lindholm",
    "given_name": "Avery",
    "job_title": "Principal and Managing Partner",
    "anchor_slug": "avery-lindholm",
}

# The one founder value that is copy as well as data. It reaches the structured
# data through a token like the rest, and it also appears in the about page's
# eyebrow and in two meta descriptions, in sentence case, inside sentences a new
# owner rewrites rather than rebrands. So it is counted rather than failed on,
# exactly as brand_name is and for the same reason.
FOUNDER_COPY = ("job_title",)

# Why each declared value the fixtures above leave alone is left alone. A key
# in neither a fixture nor this table is a value the rehearsal skips twice: it
# is never replaced, and value_residue never looks for it afterwards, so the
# fixture tree can still carry the previous owner's data and this script will
# call the rebrand clean. Reading the content model in one direction is how
# the founder's four identity fields went unwatched until 2026-09-12, and
# adding a fifth would have gone unwatched the same way.
UNREBRANDED = {
    ("site.json", "comment"): "documentation rather than a value a page renders",
    ("site.json", "allowed_external_hosts"): (
        "the hosts a browser is permitted to reach, which name the third "
        "party services themselves rather than whoever owns the site"
    ),
    ("founder.json", "comment"): "documentation rather than a value a page renders",
    ("founder.json", "biography_strings"): (
        "the previous owner's credentials, schools and employers, which are "
        "copy for runbook step 5 and are counted rather than replaced"
    ),
}

HTML_ENTITIES = {
    "&amp;": "&",
    "&nbsp;": " ",
    "&#39;": "'",
    "&quot;": '"',
}

TOKEN_SPLIT_RE = re.compile(r"[\s,]+")


def fixture_gaps(original, founder):
    """Return every declared value neither fixture replaces and nothing excuses."""
    # The two nested groups are covered by the rows below them rather than by
    # a fixture of their own, so the top level row treats them as replaced.
    covered = [
        ("site.json", original, set(FIXTURE) | {"third_party", "social"}),
        ("site.json third_party", original["third_party"], set(THIRD_PARTY_FIXTURE)),
        ("site.json social", original["social"], set(SOCIAL_FIXTURE)),
        ("founder.json", founder, set(FOUNDER_FIXTURE)),
    ]
    gaps = []
    for label, config, fixture_keys in covered:
        root = label.split(" ")[0]
        for key in config:
            if key in fixture_keys or (root, key) in UNREBRANDED:
                continue
            gaps.append(
                f"{label} declares {key!r} and no fixture replaces it, so a "
                "rebrand would leave it as it is and the scan below would "
                "never look for it. Add it to the fixture, or add it to "
                "UNREBRANDED with the reason it stays."
            )
    return gaps


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


def rewrite_founder_json(out_dir):
    """Apply runbook step 1 to the founder's identity as well as to site.json."""
    path = os.path.join(out_dir, "site", "content", "founder.json")
    founder = read_json(path)
    for key, value in FOUNDER_FIXTURE.items():
        if key not in founder:
            raise KeyError(
                f"founder.json has no {key!r}, so the fixture and the content "
                "model have diverged and this rehearsal would prove less "
                "than it claims"
            )
        founder[key] = value
    text = json.dumps(founder, indent=2, ensure_ascii=False)
    with open(path, "wb") as f:
        f.write((text.replace("\n", "\r\n") + "\r\n").encode("utf-8"))


def rewrite_login_page(out_dir, original):
    """Apply runbook step 4: the one page that carries the brand name as prose."""
    # It is prose rather than a token because the login page is rendered
    # without the shared chrome and reads as a sentence, so tokenising it
    # would make the copy unreadable to whoever edits it. That makes it the
    # one mechanical step a new owner does by hand, and doing it here is what
    # lets the rehearsal claim all four mechanical steps rather than three.
    path = os.path.join(out_dir, "site", "pages", "login.page.frag")
    with open(path, "rb") as f:
        text = f.read().decode("utf-8")
    if original["brand_name"] not in text:
        raise KeyError(
            "login.page.frag no longer writes the brand name as prose, so "
            "runbook step 4 and this rehearsal have diverged"
        )
    text = text.replace(original["brand_name"], FIXTURE["brand_name"])
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def rename_assets(out_dir, original):
    """Apply runbook step 2: rename the three images site.json declares by name."""
    # The images are source under site/static and the build copies them into
    # the output. Renaming the copy alone leaves the source under the old name
    # and the next build puts it back, so the rebranded tree would still ship a
    # file named for the previous owner. The stale copy in the output is deleted
    # for the reason a removed page's file is: a build writes and never deletes.
    source = os.path.join(out_dir, "site", "static", "assets")
    published = os.path.join(out_dir, "docs", "assets")
    for key in ASSET_KEYS:
        os.rename(
            os.path.join(source, original[key]),
            os.path.join(source, FIXTURE[key]),
        )
        stale = os.path.join(published, original[key])
        if os.path.isfile(stale):
            os.remove(stale)


def filename_residue(out_dir, original):
    """Return every file in the rebranded tree still named for one of the old images."""
    # A declared value can survive as a filename as well as as a line of text,
    # and the scan below reads content only. An image the new owner never
    # replaced is the previous owner's logo sitting in the tree under the name
    # it always had, which every check passes because nothing links to it.
    old_names = {
        original[key]
        for key in ASSET_KEYS
    }
    hits = []
    for dir_path, _dir_names, file_names in os.walk(out_dir):
        if ".git" in dir_path.split(os.sep):
            continue
        for file_name in sorted(file_names):
            if file_name in old_names:
                rel = os.path.relpath(os.path.join(dir_path, file_name), out_dir)
                hits.append("asset filename: " + rel.replace(os.sep, "/"))
    return hits


def run(out_dir, args):
    """Run one of the repo's own scripts inside the clone and return the result."""
    return subprocess.run(
        [sys.executable] + args,
        cwd=out_dir,
        capture_output=True,
        text=True,
    )


def is_text_file(path):
    """Return whether a file is text: it decodes as UTF-8 and holds no NUL byte."""
    # Binary images are excluded by content rather than by a suffix list, so a
    # text file the build starts writing in a new format is still read.
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return False
    if b"\x00" in raw:
        return False
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def text_files(docs_root):
    """Yield every file under a built tree that is text, judged by content."""
    for dir_path, _, file_names in os.walk(docs_root):
        for name in sorted(file_names):
            path = os.path.join(dir_path, name)
            if is_text_file(path):
                yield path


def normalize_with_linemap(text):
    """Return text with tags and entities collapsed to plain words and runs of
    whitespace collapsed to one space, alongside the 1-based source line each
    output character came from."""
    # A declared value split across a tag or a line break reads as one string
    # here even though no single line of the built file carries it whole.
    chars = []
    lines = []
    line = 1
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        # A "<" starts a tag only when a letter, "/", "!" or "?" follows, which
        # is every real tag, comment and processing instruction. Otherwise it is
        # a literal character, such as the "<" in "a < b" in CSS or JS, and
        # swallowing up to the next ">" there would hide whatever came between.
        if ch == "<" and i + 1 < n and (text[i + 1].isalpha() or text[i + 1] in "/!?"):
            end = text.find(">", i)
            if end == -1:
                end = n - 1
            tag = text[i:end + 1]
            chars.append(" ")
            lines.append(line)
            line += tag.count("\n")
            i = end + 1
            continue
        if ch == "&":
            entity_hit = None
            for entity, replacement in HTML_ENTITIES.items():
                if text.startswith(entity, i):
                    entity_hit = (entity, replacement)
                    break
            if entity_hit is not None:
                entity, replacement = entity_hit
                chars.append(replacement)
                lines.append(line)
                i += len(entity)
                continue
        chars.append(ch)
        lines.append(line)
        if ch == "\n":
            line += 1
        i += 1
    collapsed_chars = []
    collapsed_lines = []
    j = 0
    total = len(chars)
    while j < total:
        if chars[j].isspace():
            start_line = lines[j]
            k = j
            while k < total and chars[k].isspace():
                k += 1
            collapsed_chars.append(" ")
            collapsed_lines.append(start_line)
            j = k
        else:
            collapsed_chars.append(chars[j])
            collapsed_lines.append(lines[j])
            j += 1
    return "".join(collapsed_chars), collapsed_lines


def normalized_value_pattern(value):
    """Return a regex matching a declared value in normalised text: its tokens,
    split on runs of whitespace and commas, joined by a run of whitespace or
    commas of any length. A value with one token behaves as an exact match, and
    a value with no token (blank) has no pattern."""
    # A hand-typed copy of an address commonly drops the comma the line break
    # replaces, "Suite 305<br>Brentwood" for the declared "Suite 305, Brentwood",
    # so the joiner between tokens has to accept either with or without one.
    tokens = [token for token in TOKEN_SPLIT_RE.split(value) if token]
    if not tokens:
        return None
    joined = r"[\s,]+".join(re.escape(token) for token in tokens)
    return re.compile(joined, re.IGNORECASE)


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


def founder_values(founder):
    """Return the founder's declared identity, labelled by where it is declared."""
    # Only the identity. The biography beside it in founder.json is counted
    # rather than failed on, for the reason brand_name is: a new owner writes
    # their own credentials and history rather than filling in these blanks,
    # and a rehearsal that failed on them would be failing on the one thing
    # nobody can automate.
    return {
        "founder." + key: value
        for key, value in founder.items()
        if key not in FOUNDER_COPY
        and ("founder.json", key) not in UNREBRANDED
        and isinstance(value, str)
    }


def value_residue(out_dir, original, founder):
    """Return every line of the rebranded tree that still carries an old value."""
    hits = []
    declared = declared_values(original)
    declared.update(founder_values(founder))
    docs = os.path.join(out_dir, "docs")
    # Read and normalise each file once for the whole run, however many
    # declared values it is checked against, rather than once per value.
    file_cache = {}
    for label, value in sorted(declared.items()):
        hits.extend(residue_for(docs, label, value, file_cache))
    return hits


def residue_data(docs, path, file_cache):
    """Return, from the cache or freshly read, the split lines, the normalised
    text and its line map for one file. None if the file no longer decodes."""
    if path in file_cache:
        return file_cache[path]
    try:
        with open(path, "rb") as f:
            text = f.read().decode("utf-8")
    except (UnicodeDecodeError, OSError):
        file_cache[path] = None
        return None
    # split("\n") rather than splitlines(), and matched by the same count in
    # normalize_with_linemap, so a line number from one pass means the same
    # line in the other. splitlines() also breaks on a lone "\r", "\x0b",
    # "\x0c" and other separators split("\n") does not, which would disagree.
    lines = text.split("\n")
    normalized_text, line_map = normalize_with_linemap(text)
    data = (lines, normalized_text, line_map)
    file_cache[path] = data
    return data


def residue_for(docs, label, value, file_cache):
    """Return every line of the rebranded tree that still carries one old value,
    read line by line and again in a tag- and entity-normalised form so a value
    split across a tag or a line break is still found."""
    pattern = re.compile(re.escape(value), re.IGNORECASE)
    normalized_pattern = normalized_value_pattern(value)
    hits = []
    for path in text_files(docs):
        data = residue_data(docs, path, file_cache)
        if data is None:
            continue
        lines, normalized_text, line_map = data
        rel = os.path.relpath(path, docs).replace(os.sep, "/")
        found_lines = set()
        for number, raw_line in enumerate(lines, 1):
            if pattern.search(raw_line):
                display = raw_line.rstrip("\r").strip()[:70]
                hits.append(f"{label}: {rel}:{number}: {display}")
                found_lines.add(number)
        if normalized_pattern is None:
            continue
        for match in normalized_pattern.finditer(normalized_text):
            number = line_map[match.start()]
            if number in found_lines:
                continue
            found_lines.add(number)
            raw_line = lines[number - 1] if 0 <= number - 1 < len(lines) else ""
            display = raw_line.rstrip("\r").strip()[:70]
            hits.append(f"{label}: {rel}:{number}: (normalised) {display}")
    return hits


def brand_residue(out_dir, original):
    """Count what still names the old brand, which its copy is expected to."""
    return string_residue(out_dir, [original["brand_name"]])[0]


def string_residue(out_dir, values):
    """Return how many times a set of strings survives, and which pages carry them."""
    patterns = [re.compile(re.escape(value), re.IGNORECASE) for value in values]
    total = 0
    pages = set()
    for path in text_files(os.path.join(out_dir, "docs")):
        with open(path, "rb") as f:
            text = f.read().decode("utf-8", "ignore")
        found = sum(len(pattern.findall(text)) for pattern in patterns)
        if found:
            total += found
            pages.add(os.path.basename(path))
    return total, sorted(pages)


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
    founder = read_json(os.path.join(REPO_ROOT, "site", "content", "founder.json"))
    gaps = fixture_gaps(original, founder)
    if gaps:
        print("The fixture and the content model have diverged:")
        for gap in gaps:
            print(f"  {gap}")
        raise SystemExit(
            "refusing to rehearse a rebrand that would prove less than it claims"
        )
    print(f"Cloning to {out_dir}")
    clone(out_dir)
    rewrite_site_json(out_dir)
    rewrite_founder_json(out_dir)
    rewrite_login_page(out_dir, original)
    rename_assets(out_dir, original)
    print("Applied the four mechanical runbook steps")

    build = run(out_dir, [os.path.join("scripts", "build_site.py"), "--out", "docs"])
    if build.returncode != 0:
        print(build.stdout)
        print(build.stderr)
        raise SystemExit("the rebranded tree does not build")
    print(build.stdout.strip())

    # The fixture is a copy of the tree with no .git beside it, so the one
    # check that reads commit dates has nothing to read. It is skipped by
    # name rather than left to fail, which would say the rebrand broke
    # something it did not touch.
    checks = run(
        out_dir, [os.path.join("scripts", "check_site.py"), "--no-history"]
    )
    for line in checks.stdout.splitlines():
        if line.startswith("[") or "passed" in line:
            print(f"  {line.rstrip()}")

    residue = (
        value_residue(out_dir, original, founder)
        + filename_residue(out_dir, original)
    )
    brand_hits = brand_residue(out_dir, original)
    checked = len(declared_values(original)) + len(founder_values(founder))
    print(
        f"Of the {checked} declared values a new owner replaces, the old value "
        f"survives on {len(residue)} lines of the rebranded tree, and the old "
        f"brand name appears {brand_hits} times in copy a new owner rewrites."
    )
    for hit in residue[:20]:
        print(f"  {hit}")

    # Reported rather than failed on, and reported by page so a new owner knows
    # which files to open. These are the previous owner's credentials, award,
    # schools and employers: a rebrand cannot invent replacements for them, and
    # a rehearsal that said nothing about them would be claiming the tree is
    # ready to hand over when a buyer still has a biography to write.
    copy = [founder[key] for key in FOUNDER_COPY] + founder["biography_strings"]
    bio_hits, bio_pages = string_residue(out_dir, copy)
    print(
        f"The previous owner's job title and biography survive {bio_hits} times "
        f"across {len(bio_pages)} pages, which a new owner rewrites by hand: "
        + (", ".join(bio_pages) if bio_pages else "none")
    )

    ok = checks.returncode == 0 and not residue
    print("REHEARSAL PASSED" if ok else "REHEARSAL FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
