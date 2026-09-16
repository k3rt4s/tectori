"""Check that a built Tectori site tree is internally consistent without knowing its history."""

from __future__ import annotations

import argparse
import html as html_lib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import check_llms_drift  # noqa: E402  (reused for the llms.txt drift comparison, see report)

# One declaration of who the site is for, read rather than repeated here. A
# phone number or domain hard-coded in this file would let the check keep
# passing against the previous owner's values after a rebrand, which is the
# one failure a consistency check exists to prevent.
SITE_CONFIG_PATH = SCRIPT_DIR.parent / "site" / "content" / "site.json"
SITE = json.loads(SITE_CONFIG_PATH.read_text(encoding="utf-8"))
FOUNDER_CONFIG_PATH = SCRIPT_DIR.parent / "site" / "content" / "founder.json"
FOUNDER = json.loads(FOUNDER_CONFIG_PATH.read_text(encoding="utf-8"))

SITE_PREFIX = SITE["site_url"]
NOINDEX_ALLOWED = {"404.html", "thank-you.html"}
# The displayed form of the site URL is the bare host. The scheme appears in
# canonicals and JSON-LD, which are markup rather than visible text, so the
# full site_url would match nothing here and this arm would pass on an empty
# set, which is what it did until 2026-09-12.
CONTACT_STRINGS = {
    "phone number": SITE["phone_display"],
    "site host": SITE["site_url"].split("://", 1)[1].rstrip("/"),
    "mailing address": SITE["postal_address"],
}
# Matched as patterns rather than as one spelling. `"@type":"Review"` with no
# space after the colon is valid JSON, is what a compact formatter emits, and as
# a literal string it is simply a different string from the one this tuple held
# until 2026-09-12. The label beside each pattern is what a failure names.
FORBIDDEN_MARKUP = (
    ("AggregateRating", re.compile(rb"AggregateRating")),
    ('"@type": "Review"', re.compile(rb'"@type"\s*:\s*"Review"')),
    ('"offers"', re.compile(rb'"offers"')),
)
FORBIDDEN_TEXT = ("Qualified Security Assessor",)

TITLE_RE = re.compile(rb"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
CANONICAL_RE = re.compile(
    rb'<link[^>]*?rel=(["\'])canonical\1[^>]*?>', re.IGNORECASE | re.DOTALL
)
ROBOTS_RE = re.compile(
    rb'<meta[^>]*?name=(["\'])robots\1[^>]*?content=(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)
ATTR_RE = re.compile(r'(?:href|src)\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)
# Anchors only, for the reachability check. Every page carries a canonical
# link element pointing at itself and a stylesheet link pointing at a file,
# so counting every href would make each page reach itself and prove nothing.
ANCHOR_RE = re.compile(
    r'<a\b[^>]*?href\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL
)
SRCSET_RE = re.compile(r'srcset\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)
SCRIPT_BLOCK_RE = re.compile(rb"<script\b.*?</script>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(rb"<[^>]+>")
BEACON_MARKER = b"cloudflareinsights.com/beacon.min.js"
PIXEL_MARKER = b"static.scarf.sh"
URL_HOST_RE = re.compile(r"https?://([A-Za-z0-9.-]+)")
LDJSON_RE = re.compile(
    rb'<script[^>]*?type=(["\'])application/ld\+json\1[^>]*?>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)

# Pages whose JSON-LD is a single top-level object; its "name" mirrors the
# page's <title> and its "description" mirrors the page's meta description.
JSONLD_TOP_LEVEL_MIRROR_PAGES = {"about.html", "contact.html"}
# Pages whose JSON-LD is an "@graph" array holding a node whose "name" and
# "description" mirror the page's <title> and meta description.
JSONLD_GRAPH_MIRROR_NODE_TYPE = {"services.html": "CollectionPage"}
# The six service-*.html pages: an "@graph" array holding a "Service" node.
# Its "name" and "serviceType" deliberately name the service, not the page
# title, so they are a documented exception and are never compared to the
# title here. Its "description" is still required to mirror the page's meta
# description.
JSONLD_GRAPH_SERVICE_DESCRIPTION_PAGES = {
    "service-agentic-ai.html",
    "service-cloud-architecture.html",
    "service-compliance-risk.html",
    "service-cybersecurity.html",
    "service-fractional-leadership.html",
    "service-it-operations.html",
}
# index.html and faq.html carry JSON-LD too, but neither keeps a verbatim
# mirror of the title/description today: index.html's Organization node has
# "name": "Tectori", not the full <title>, and its "description" reads
# differently from the page's meta description by design; faq.html's
# FAQPage node has no top-level "name" or "description" at all (only nested
# Question/Answer text). Inventing a comparison for either would be enforcing
# a rule the tree does not actually follow, so both are intentionally left
# unchecked here. They are named rather than skipped silently, because a page
# carrying JSON-LD that appears in none of these tables is a gap in the check
# rather than a page with nothing to verify, and is reported as a problem.
JSONLD_NO_MIRROR_PAGES = {"index.html", "faq.html"}


def html_pages(root: Path) -> list[Path]:
    """Return every .html file under root, sorted for stable output."""
    return sorted(root.rglob("*.html"))


def canonical_path(raw: bytes) -> str | None:
    """Return the site-relative path from a page's canonical href, or None if absent."""
    match = CANONICAL_RE.search(raw)
    if match is None:
        return None
    href_match = re.search(rb'href=(["\'])(.*?)\1', match.group(0), re.IGNORECASE | re.DOTALL)
    if href_match is None:
        return None
    href = href_match.group(2).decode("utf-8")
    if href.startswith(SITE_PREFIX):
        href = href[len(SITE_PREFIX) :]
    return href or "/"


def resolve_internal(url_value: str, current_file: Path, docs_root: Path):
    """Classify an href/src value and return (kind, resolved_path_or_None).

    kind is one of "fragment" (points at the current page), "internal"
    (resolved_path is the file that must exist), or "external" (a scheme,
    domain, or protocol this check does not verify).
    """
    if url_value == "" or url_value.startswith("#"):
        return "fragment", current_file
    if url_value.startswith(("mailto:", "tel:", "javascript:", "data:", "//")):
        return "external", None
    if url_value.startswith("http://") or url_value.startswith("https://"):
        if not url_value.startswith(SITE_PREFIX):
            return "external", None
        path = url_value[len(SITE_PREFIX) :]
    else:
        path = url_value

    path = path.split("#", 1)[0]
    path = path.split("?", 1)[0]
    if path == "":
        return "fragment", current_file

    if path.startswith("/"):
        base = docs_root
        rel = path.lstrip("/")
    else:
        base = current_file.parent
        rel = path

    if rel == "" or rel.endswith("/"):
        candidate = base / rel / "index.html"
    else:
        suffix = Path(rel).suffix
        candidate = base / rel if suffix else base / (rel + ".html")
    return "internal", candidate


def path_case_matches(target: Path, root: Path) -> bool:
    """Return True only if target is a file whose case matches root's listing exactly.

    Path.is_file() answers a question a case-insensitive filesystem gets
    wrong: it says yes for a file that exists under a different case, which
    is every Windows run of this check. GitHub Pages serves case
    sensitively, so a stated or linked URL spelled with the wrong case
    passes here and 404s for a visitor. This walks target's path under root
    component by component against the real directory listing, so a case
    mismatch anywhere along it fails instead of passing.
    """
    if not target.is_file():
        return False
    normalized_target = Path(os.path.normpath(target))
    normalized_root = Path(os.path.normpath(root))
    try:
        relative = normalized_target.relative_to(normalized_root)
    except ValueError:
        return False
    current = normalized_root
    for part in relative.parts:
        try:
            names = {entry.name for entry in current.iterdir()}
        except OSError:
            return False
        if part not in names:
            return False
        current = current / part
    return True


def link_values(text: str):
    """Yield every URL a page points at, including each candidate in a srcset.

    A srcset is a comma separated list of candidates, each a URL followed by
    an optional width or density descriptor. Nothing scanned them until
    2026-09-12, and the home page serves its hero as a webp that way, so a
    renamed or deleted file behind it would have shipped as a broken image to
    every browser that prefers webp while all ten checks passed.
    """
    text = HTML_COMMENT_RE.sub("", text)
    for match in ATTR_RE.finditer(text):
        yield match.group(2)
    for match in SRCSET_RE.finditer(text):
        for candidate in match.group(2).split(","):
            candidate = candidate.strip()
            if candidate:
                yield candidate.split()[0]


def check_links(pages: list[Path], docs_root: Path) -> bool:
    """Every href and src that points inside the site resolves to a file that exists."""
    checked = 0
    broken = 0
    external = 0
    skipped = 0
    broken_examples: list[str] = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for raw in link_values(text):
            value = html_lib.unescape(raw).strip()
            try:
                kind, target = resolve_internal(value, page, docs_root)
            except Exception:
                skipped += 1
                continue
            if kind == "external":
                external += 1
            elif kind == "fragment":
                checked += 1
            else:
                checked += 1
                if not path_case_matches(target, docs_root):
                    broken += 1
                    broken_examples.append(f"{page.name}: {value!r} -> {target}")
    ok = broken == 0 and skipped == 0
    print(
        f"[{'PASS' if ok else 'FAIL'}] internal links resolve: "
        f"{checked} checked, {broken} broken, {external} external skipped, "
        f"{skipped} unparsed skipped"
    )
    for example in broken_examples[:20]:
        print(f"       broken: {example}")
    return ok


def check_pages_are_reachable(pages: list[Path], docs_root: Path) -> bool:
    """Every indexed page can be reached from the home page by following links."""
    # check_links asks whether the links point at pages that exist. This asks
    # the other direction, whether a visitor who arrives at the home page can
    # get to a page at all. A page added to pages.json and never put in the
    # nav or a footer builds cleanly, resolves, and appears in the sitemap and
    # llms.txt, so it is indexed and unreachable at the same time while every
    # other check passes.
    #
    # Counting incoming links instead, which is what this did until 2026-09-12,
    # is the weaker question and passes a tree that is wrong: two new pages
    # that link to each other and to nothing else each supply the other's only
    # incoming link, so both look linked to while neither is reachable from
    # anywhere a visitor starts. Walking out from the home page is the only
    # form of the question a page cannot answer on its own behalf.
    home = (docs_root / "index.html").resolve()
    known = {page.resolve() for page in pages}
    names = {page.resolve(): page.name for page in pages}

    edges: dict[Path, set[Path]] = {}
    for page in pages:
        text = page.read_text(encoding="utf-8")
        text = HTML_COMMENT_RE.sub("", text)
        out: set[Path] = set()
        for match in ANCHOR_RE.finditer(text):
            value = html_lib.unescape(match.group(2)).strip()
            try:
                kind, target = resolve_internal(value, page, docs_root)
            except Exception:
                continue
            if kind != "internal" or target is None:
                continue
            resolved = target.resolve()
            # A page linking to itself is the nav, and it carries nobody.
            if resolved in known and resolved != page.resolve():
                out.add(resolved)
        edges[page.resolve()] = out

    reached: set[Path] = set()
    queue = [home] if home in known else []
    while queue:
        current = queue.pop()
        if current in reached:
            continue
        reached.add(current)
        queue.extend(edges.get(current, ()))

    # The two noindex pages are reached by a redirect and by a 404, not by a
    # link, which is why they are the two the sitemap check also exempts.
    expected = {path for path in known if names[path] not in NOINDEX_ALLOWED}
    unreachable = sorted(names[path] for path in expected - reached)
    ok = not unreachable and home in known
    print(
        f"[{'PASS' if ok else 'FAIL'}] every indexed page is reachable from the "
        f"home page: {len(expected)} pages, {len(unreachable)} reachable from nothing"
    )
    if home not in known:
        print("       there is no index.html, so nothing has a starting point")
    for name in unreachable[:20]:
        print(f"       {name}: no path of links from the home page reaches it")
    return ok


def check_head_tags(pages: list[Path]) -> bool:
    """Every page has exactly one title, one meta description, and at most one canonical."""
    problems: list[str] = []
    for page in pages:
        raw = page.read_bytes()
        titles = len(TITLE_RE.findall(raw))
        descriptions = len(check_llms_drift.META_DESCRIPTION.findall(raw))
        canonicals = len(CANONICAL_RE.findall(raw))
        if titles != 1:
            problems.append(f"{page.name}: {titles} <title> elements")
        if descriptions != 1:
            problems.append(f"{page.name}: {descriptions} meta descriptions")
        if canonicals > 1:
            problems.append(f"{page.name}: {canonicals} canonical links")
    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] one title, one meta description, at most one canonical: "
          f"{len(pages)} pages checked, {len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_noindex_and_navigation(pages: list[Path], docs_root: Path) -> bool:
    """404.html and thank-you.html are the only noindex pages, and no page links to them."""
    problems: list[str] = []
    noindex_found = set()
    for page in pages:
        raw = page.read_bytes()
        match = ROBOTS_RE.search(raw)
        if match and b"noindex" in match.group(3).lower():
            noindex_found.add(page.name)
    if noindex_found != NOINDEX_ALLOWED:
        unexpected = noindex_found - NOINDEX_ALLOWED
        missing = NOINDEX_ALLOWED - noindex_found
        if unexpected:
            problems.append(f"unexpected noindex on: {sorted(unexpected)}")
        if missing:
            problems.append(f"missing noindex on: {sorted(missing)}")

    # Resolved rather than compared against a list of spellings. The list held
    # here until 2026-09-12 carried `/404.html` but not `/thank-you.html`, so the
    # one spelling a footer link is most likely to use was the one it could not
    # see, and a link straight to the thank-you page would have shipped.
    forbidden = {(docs_root / name).resolve() for name in NOINDEX_ALLOWED}
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for raw in link_values(text):
            value = html_lib.unescape(raw).strip()
            try:
                kind, target = resolve_internal(value, page, docs_root)
            except Exception:
                continue
            if kind != "internal" or target is None:
                continue
            resolved = target.resolve()
            if resolved in forbidden and resolved != page.resolve():
                problems.append(f"{page.name}: links to {target.name}")

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] only 404.html and thank-you.html are noindex, "
          f"and neither is linked from any page: {len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_sitemap(pages: list[Path], docs_root: Path) -> bool:
    """sitemap.xml lists every indexed page once, by its own canonical path, with no noindex page and no duplicate <loc>."""
    sitemap = docs_root / "sitemap.xml"
    problems: list[str] = []
    if not sitemap.is_file():
        print("[FAIL] sitemap.xml lists every indexed page: sitemap.xml not found")
        return False

    sitemap_paths = set()
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap.read_text(encoding="utf-8"))
    for loc, count in sorted(Counter(locs).items()):
        if count > 1:
            problems.append(f"sitemap.xml: <loc>{loc}</loc> appears {count} times")
    for loc in locs:
        if not loc.startswith(SITE_PREFIX):
            problems.append(f"sitemap.xml: <loc>{loc}</loc> is not on the site domain")
            continue
        sitemap_paths.add(loc[len(SITE_PREFIX) :] or "/")

    expected_paths = set()
    declaring: dict[str, list[str]] = {}
    for page in pages:
        if page.name in NOINDEX_ALLOWED:
            continue
        path = canonical_path(page.read_bytes())
        if path is None:
            problems.append(f"{page.name}: no canonical href to derive its sitemap path from")
            continue
        declaring.setdefault(path, []).append(page.name)
        expected_paths.add(path)

    # Two pages declaring one canonical collapse into a single element of the set
    # above, and the sitemap then matches a set that is one page short while both
    # pages ship. A page begun by copying another and never having its canonical
    # changed is the ordinary way that happens, and nothing else here reads what
    # a canonical says, only that a page has one of them.
    for path, names in sorted(declaring.items()):
        if len(names) > 1:
            problems.append(
                f"{len(names)} pages declare the canonical {path!r}: {sorted(names)}"
            )

    missing = expected_paths - sitemap_paths
    extra = sitemap_paths - expected_paths
    for path in sorted(missing):
        problems.append(f"sitemap.xml is missing indexed page {path!r}")
    for path in sorted(extra):
        problems.append(f"sitemap.xml lists {path!r}, which is not an indexed page")

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] sitemap.xml matches the indexed pages' own canonicals: "
          f"{len(sitemap_paths)} sitemap entries, {len(expected_paths)} expected, "
          f"{len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_llms_txt(docs_root: Path) -> bool:
    """llms.txt covers the sitemap's page set once each and repeats each page's meta description."""
    llms_file = docs_root / "llms.txt"
    sitemap = docs_root / "sitemap.xml"
    problems: list[str] = []
    if not llms_file.is_file() or not sitemap.is_file():
        print("[FAIL] llms.txt matches the sitemap's page set and descriptions: file(s) missing")
        return False

    sitemap_paths = {
        loc[len(SITE_PREFIX) :] or "/"
        for loc in re.findall(r"<loc>(.*?)</loc>", sitemap.read_text(encoding="utf-8"))
        if loc.startswith(SITE_PREFIX)
    }

    # check_llms_drift.entries() and .LLMS_FILE are hard-coded to this repo's own
    # docs/llms.txt, so they are reused only for the parts that already take a
    # Path argument (meta_description) or a plain regex (LLMS_ENTRY). The
    # page-set comparison to the sitemap below is not something
    # check_llms_drift does at all, so it is written fresh here.
    text = llms_file.read_text(encoding="utf-8")
    llms_paths = set()
    llms_lines = []
    for number, line in enumerate(text.splitlines(), start=1):
        match = check_llms_drift.LLMS_ENTRY.match(line)
        if match:
            llms_paths.add(match.group(1))
            llms_lines.append((number, match.group(1), " ".join(match.group(2).split())))

    for url_path, count in sorted(Counter(path for _, path, _ in llms_lines).items()):
        if count > 1:
            problems.append(f"llms.txt: {url_path!r} appears {count} times")

    # The sitemap lists absolute https://www.tectori.com URLs and llms.txt
    # lists site-relative paths. That format difference is expected and is
    # normalized away above; the two page sets themselves must be identical.
    missing = sitemap_paths - llms_paths
    extra = llms_paths - sitemap_paths
    for path in sorted(missing):
        problems.append(f"llms.txt is missing sitemap page {path!r}")
    for path in sorted(extra):
        problems.append(f"llms.txt lists {path!r}, which is not in the sitemap")

    drift = 0
    for number, url_path, described in llms_lines:
        name = url_path.strip("/") or "index"
        if not name.endswith(".html"):
            name += ".html"
        page = docs_root / name
        if not page.is_file():
            problems.append(f"llms.txt:{number}: {url_path} names no page in {docs_root}")
            continue
        current = check_llms_drift.meta_description(page)
        if current is None:
            problems.append(f"llms.txt:{number}: {page.name} has no meta description")
            continue
        if current != described:
            drift += 1
            problems.append(f"llms.txt:{number}: {url_path} description has drifted from {page.name}")

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] llms.txt matches the sitemap's page set and descriptions: "
          f"{len(llms_lines)} entries, {drift} drifted, {len(problems) - drift} other problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def visible_text(raw: bytes) -> str:
    """Return a page's rendered text: script/style blocks and tags stripped, entities decoded."""
    raw = SCRIPT_BLOCK_RE.sub(b" ", raw)
    raw = TAG_RE.sub(b" ", raw)
    return html_lib.unescape(raw.decode("utf-8"))


SEPARATOR_CLASS = r"[^A-Za-z0-9]{0,4}"


def near_miss_pattern(exact: str) -> re.Pattern:
    """Return a pattern matching a declared contact string and its likely reformattings.

    Built from the declared value rather than written out beside it, so a
    rebrand cannot leave this looking for a previous owner's phone number,
    finding nothing, and reporting a pass on an empty set.

    The relaxations are the two ways a contact string gets reformatted in
    practice. Punctuation and spacing between the parts is free, which is how
    "(615) 829-6802" becomes "615-829-6802". A word may grow a suffix, which
    is how "Dr" becomes "Drive". Digits stay exact, because a changed digit is
    a different phone number rather than a reformatting.
    """
    tokens = re.findall(r"[A-Za-z0-9]+|[^A-Za-z0-9]+", exact)
    parts = []
    for token in tokens:
        if not token[0].isalnum():
            parts.append(SEPARATOR_CLASS)
        elif token[0].isdigit():
            parts.append(re.escape(token))
        else:
            parts.append(re.escape(token) + r"[A-Za-z]*")
    return re.compile("".join(parts), re.IGNORECASE)


def check_contact_details(pages: list[Path]) -> bool:
    """Contact details appear character for character wherever they show up as visible text."""
    near_miss = {
        label: near_miss_pattern(exact)
        for label, exact in CONTACT_STRINGS.items()
    }
    checked = 0
    found_labels = {label: 0 for label in near_miss}
    problems: list[str] = []
    for page in pages:
        text = " ".join(visible_text(page.read_bytes()).split())
        for label, pattern in near_miss.items():
            for match in pattern.finditer(text):
                checked += 1
                found_labels[label] += 1
                found = match.group(0).strip()
                exact = CONTACT_STRINGS[label]
                if found != exact:
                    problems.append(f"{page.name}: {label} reads {found!r}, not {exact!r}")

    # A pattern that matches nothing is the failure this check exists to avoid,
    # so it is reported rather than passing quietly on an empty set.
    for label, count in found_labels.items():
        if not count:
            problems.append(
                f"the declared {label} appears nowhere in the visible text, "
                f"so nothing was compared against it"
            )

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] contact details match character for character: "
          f"{checked} occurrences checked, {len(problems)} mismatched")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


TEL_HREF_RE = re.compile(r'href\s*=\s*(["\'])(tel:[^"\']*)\1', re.IGNORECASE)


def digits(value: str) -> str:
    """Return only the digits of a string, which is the phone number inside it."""
    return "".join(character for character in value if character.isdigit())


FORM_RE = re.compile(r"<form\b.*?</form>", re.IGNORECASE | re.DOTALL)
CONTROL_RE = re.compile(r"<(input|textarea|select)\b([^>]*)>", re.IGNORECASE)
FORM_ATTR_RE = re.compile(r'([A-Za-z_:][-\w:.]*)\s*=\s*(["\'])(.*?)\2', re.DOTALL)
LABEL_FOR_RE = re.compile(r'<label[^>]*?\bfor\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)
WRAPPER_CLASS_RE = re.compile(r'<div[^>]*?\bclass\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)

# The fields the business reads. A form that posts without one of them sends
# an inquiry with no way to answer it, or no question in it.
REQUIRED_FIELDS = ("name", "email", "message")
# Formspree discards a submission whose spam trap was filled in. The trap only
# works while it is invisible, and a visitor who can see it fills it in.
HONEYPOT_FIELD = "_gotcha"
# A honeypot is invisible to a visitor only if the cascade's winning
# declarations end in display: none, visibility: hidden, opacity: 0, or a
# clip-path: inset(50%) or larger, none of which need a position, or an
# absolute or fixed position combined with one of: a negative left or top,
# a clip: rect(...) whose four lengths are all zero, or a width and height
# each at most 1px paired with overflow: hidden. These are the properties
# class_is_hidden tracks to decide which one applies.
CASCADE_HIDING_PROPERTIES = (
    "display",
    "visibility",
    "position",
    "left",
    "top",
    "clip",
    "clip-path",
    "width",
    "height",
    "overflow",
    "opacity",
)
OFF_SCREEN_POSITIONS = ("absolute", "fixed")


def attributes(tag_body: str) -> dict:
    """Return a tag's attributes, lowercased by name, as written."""
    return {
        match.group(1).lower(): match.group(3)
        for match in FORM_ATTR_RE.finditer(tag_body)
    }


META_CONTENT_RE = re.compile(
    r'<meta[^>]*?\bcontent\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL
)


def stated_urls(value, prefix: str):
    """Yield every string in a JSON-LD value that names something on this site."""
    if isinstance(value, str):
        if value.startswith(prefix) or value.startswith("/"):
            yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from stated_urls(item, prefix)
    elif isinstance(value, list):
        for item in value:
            yield from stated_urls(item, prefix)


SKIP_LINK_RE = re.compile(
    r'<a[^>]*?\bclass\s*=\s*(["\'])[^"\']*\bskip-link\b[^"\']*\1[^>]*?>',
    re.IGNORECASE,
)
HREF_RE = re.compile(r'\bhref\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)
IMG_RE = re.compile(r"<img\b([^>]*)>", re.IGNORECASE | re.DOTALL)
# The attribute name must stand alone, so data-alt or x-alt is not it;
# an unquoted value counts, matching the house shape in
# NAV_ARIA_LABEL_RE.
ALT_ATTR_RE = re.compile(
    r'(?<![\w:.-])alt\s*=\s*'
    r'(?:(["\'])(.*?)\1|([^\s"\'<>=`]+))',
    re.IGNORECASE | re.DOTALL,
)
NAV_RE = re.compile(r"<nav\b([^>]*)>", re.IGNORECASE | re.DOTALL)
# The attribute name must stand alone, so data-aria-label or x-aria-label
# is not it; an unquoted value counts.
NAV_ARIA_LABEL_RE = re.compile(
    r'(?<![\w:.-])aria-label\s*=\s*'
    r'(?:(["\'])(.*?)\1|([^\s"\'<>=`]+))',
    re.IGNORECASE | re.DOTALL,
)
ID_ATTR_RE = re.compile(r'\bid\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)

# A commented-out element renders nothing, so an id or a reference to one
# inside a comment is not part of the page a visitor sees. Every check that
# collects ids or scans for references to them strips comments first.
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

# The sentences on the accessibility page that a tree can be measured against.
# Each is read from the page itself, so a claim that is reworded or withdrawn
# fails here rather than leaving a check enforcing a promise the site no longer
# makes, and a promise made with no check behind it is the thing this repository
# keeps finding.
ACCESSIBILITY_CLAIMS = (
    "Every page starts with a skip to content link.",
    "Images carry text alternatives.",
    "Pages use semantic HTML with landmarks, headings, and labeled navigation.",
)


# Elements whose URL the browser fetches on its own, which is what the privacy
# policy is about. A form action is not one of them: nothing is sent until a
# visitor fills the form in and presses the button, and the policy says so
# separately.
RESOURCE_RE = re.compile(
    r"<(script|link|img|iframe|source|video|audio|embed|object)\b([^>]*)>",
    re.IGNORECASE | re.DOTALL,
)
RESOURCE_URL_RE = re.compile(
    r'\b(?:src|href|data|srcset)\s*=\s*(["\'])(.*?)\1',
    re.IGNORECASE | re.DOTALL,
)
ABSOLUTE_HOST_RE = re.compile(r"^https?://([^/]+)", re.IGNORECASE)

# CSS also fetches: an @import brings in a whole second stylesheet and a
# url() loads a font, an image or anything else a browser resolves the way
# it resolves a source attribute, but neither sits inside a tag the scan
# above looks at, so a <style> block, a style="" attribute or a .css file
# could name a third party host and every check here still pass.
STYLE_ELEMENT_RE = re.compile(
    r"<style\b[^>]*>(.*?)</style\s*>", re.IGNORECASE | re.DOTALL
)
STYLE_ATTR_RE = re.compile(
    r'\bstyle\s*=\s*([\"\'])(.*?)\1', re.IGNORECASE | re.DOTALL
)
CSS_URL_FUNC_RE = re.compile(
    r'\burl\(\s*([\"\']?)(.*?)\1\s*\)', re.IGNORECASE | re.DOTALL
)
CSS_IMPORT_STRING_RE = re.compile(
    r'@import\s+([\"\'])(.*?)\1', re.IGNORECASE | re.DOTALL
)
# http(s):// or the protocol-relative //host a browser also fetches from.
# data: URIs and same-host or relative paths have no leading // and never
# match, so they are never counted as a fetch here either.
CSS_ABS_HOST_RE = re.compile(r"^(?:https?:)?//([^/?#]+)", re.IGNORECASE)


def css_fetch_urls(css_text: str):
    """Yield every url() or @import target in a block of CSS text.

    Comments are stripped first, with the same regex the palette reader
    uses below, so a commented-out @import is not a live fetch.
    """
    css_text = CSS_COMMENT_RE.sub(" ", css_text)
    for match in CSS_URL_FUNC_RE.finditer(css_text):
        yield match.group(2).strip()
    for match in CSS_IMPORT_STRING_RE.finditer(css_text):
        yield match.group(2).strip()


def css_fetch_problems(name: str, css_text: str, is_disclosed):
    """Return (fetch count, problem strings) for the url()/@import targets in one CSS source.

    Shared by the per-page style scan and the standalone .css file scan
    below, so the host test and the failure wording live in one place.
    """
    count = 0
    css_problems: list[str] = []
    for candidate in css_fetch_urls(css_text):
        host = CSS_ABS_HOST_RE.match(candidate)
        if not host:
            continue
        count += 1
        if not is_disclosed(host.group(1)):
            css_problems.append(
                f"{name}: a CSS fetch loads from "
                f"{host.group(1)!r}, which the privacy policy does "
                "not tell a visitor about"
            )
    return count, css_problems


# Ways a page keeps something on a visitor's machine. The policy says it does
# none of them, which is a sentence no check read.
STORAGE_MARKERS = (
    "document.cookie",
    "localStorage",
    "sessionStorage",
    "indexedDB",
)

# Read from the page, so withdrawing a promise and dropping the check that
# enforces it stay one action.
PRIVACY_CLAIMS = (
    "It sets no cookies.",
    "It stores nothing on your device.",
    "It loads no fonts and no other resources from third party services.",
)


ROBOTS_LINE_RE = re.compile(r"^([A-Za-z-]+)\s*:\s*(.*)$")

# The sentence the file opens with, read from the file rather than repeated
# here, so narrowing the policy on purpose fails this check instead of leaving
# it enforcing a promise the file stopped making.
ROBOTS_CLAIM = (
    "robots policy permits every named crawler, covering search, "
    "answer-engine, user-directed retrieval, and model training."
)


def robots_groups(text: str):
    """Return robots.txt as (user agents, rules) groups, plus its other lines."""
    groups: list[tuple[list[str], list[tuple[str, str]]]] = []
    other: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        match = ROBOTS_LINE_RE.match(line)
        if not match:
            continue
        field, value = match.group(1).lower(), match.group(2).strip()
        if field == "user-agent":
            # Consecutive user-agent lines share the rules that follow them,
            # so a new group starts only once a rule has been seen.
            if groups and not groups[-1][1]:
                groups[-1][0].append(value)
            else:
                groups.append(([value], []))
        elif field in ("allow", "disallow"):
            if groups:
                groups[-1][1].append((field, value))
        else:
            other.append((field, value))
    return groups, other


def robots_disallow_pattern(value: str) -> re.Pattern[str]:
    """Compile a robots.txt Disallow value into the match RFC 9309 defines.

    `path.startswith(value)` treats `*` and a trailing `$` as the literal
    characters they are in a Disallow value, so `/*`, `/*.html` and
    `/about$` match nothing this check ever tests them against while the
    crawler that actually reads robots.txt treats `*` as any run of
    characters and a trailing `$` as an end anchor. This compiles the same
    rule: `*` becomes `.*`, a trailing `$` anchors the end, everything else
    is matched literally, and the match still starts at the beginning of
    the path per the spec's prefix rule.
    """
    anchored = value.endswith("$")
    body = value[:-1] if anchored else value
    escaped = ".*".join(re.escape(part) for part in body.split("*"))
    return re.compile("^" + escaped + ("$" if anchored else ""))


NAME_ANCHOR_RE = re.compile(
    r'<a[^>]*?\bname\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL
)


def anchor_targets(text: str) -> set[str]:
    """Return every name a fragment on this page can legitimately point at."""
    text = HTML_COMMENT_RE.sub("", text)
    names = {match.group(2) for match in ID_ATTR_RE.finditer(text)}
    names.update(match.group(2) for match in NAME_ANCHOR_RE.finditer(text))
    return names


ID_REFERENCE_RE = re.compile(
    r'\s(aria-labelledby|aria-describedby|aria-controls|aria-owns|for|list)'
    r'\s*=\s*(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)


def check_id_references(pages: list[Path]) -> bool:
    """Every attribute that names another element finds it on the same page.

    The check above reads the half of a link that says which section. This
    reads the same relationship where it is invisible: a heading that names
    the section it labels, a label that names its input, a control that names
    what it opens. A renamed id leaves the markup valid, the page reachable
    and the build byte identical, and takes the accessible name off the
    element, so a screen reader announces an unlabelled region and a sighted
    visitor sees nothing at all. This site publishes an accessibility
    statement, which makes the silent version the expensive one.
    """
    problems: list[str] = []
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        text = HTML_COMMENT_RE.sub("", text)
        ids = {match.group(2) for match in ID_ATTR_RE.finditer(text)}
        for match in ID_REFERENCE_RE.finditer(text):
            attribute = match.group(1).lower()
            for name in match.group(3).split():
                checked += 1
                if name in ids:
                    continue
                problems.append(
                    f"{page.name}: {attribute}=\"{name}\" names an element "
                    "this page does not carry, so the label, the description "
                    "or the control it points at is silently nothing"
                )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] every attribute that names an element "
        f"finds it: {checked} checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_fragments_resolve(pages: list[Path], docs_root: Path) -> bool:
    """Every link to a place on a page lands on something that is there.

    The link check drops the fragment before resolving, by design: it asks
    whether the file exists. So a link to a section of another page is only
    ever checked as far as the page, and the part of it that says which
    section is read by nothing. A heading renamed in a copy edit takes its id
    with it, every check still passes, and the visitor who followed a link to
    one service on the hub page arrives at the top of a long page with no sign
    that anything went wrong, which is worse than an error because they blame
    themselves for not finding it.
    """
    problems: list[str] = []
    targets: dict[Path, set[str]] = {}
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        text = HTML_COMMENT_RE.sub("", text)
        for match in ANCHOR_RE.finditer(text):
            value = html_lib.unescape(match.group(2)).strip()
            if "#" not in value:
                continue
            fragment = value.split("#", 1)[1]
            if not fragment:
                # A bare `#` is a link to the top of the page, which is a
                # place that always exists.
                continue
            kind, target = resolve_internal(value, page, docs_root)
            if kind == "external" or target is None:
                continue
            if not path_case_matches(target, docs_root):
                # A target file that does not exist is the link check's.
                continue
            checked += 1
            if target not in targets:
                targets[target] = anchor_targets(
                    target.read_text(encoding="utf-8")
                )
            if fragment not in targets[target]:
                where = "this page" if target == page else target.name
                problems.append(
                    f"{page.name}: links to {value!r}, and nothing on "
                    f"{where} carries that id, so the visitor lands at the "
                    "top of the page instead"
                )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] a link to a place on a page lands "
        f"there: {checked} checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_robots_policy(pages: list[Path], docs_root: Path) -> bool:
    """robots.txt permits every page the site wants found, and points at the sitemap.

    This is the one file that can take the whole business off the internet
    without changing a page. Nothing here read it. Every check in this suite
    treats the tree as a set of pages that link to each other, and all of them
    keep passing against a tree whose robots.txt carries a single `Disallow: /`
    line, which is what a copied template, a staging file promoted by mistake,
    or a crawler group edited to exclude one path most often looks like. The
    site is then perfectly consistent, perfectly deployed, and absent from
    every search result and every answer engine, and the only signal is that
    nobody calls.
    """
    problems: list[str] = []
    robots = docs_root / "robots.txt"
    if not robots.is_file():
        print("[FAIL] robots.txt lets the site be found: robots.txt is missing")
        return False
    text = robots.read_text(encoding="utf-8")
    if text.count(ROBOTS_CLAIM) != 1:
        problems.append(
            f"robots.txt no longer states {ROBOTS_CLAIM!r} exactly once, so "
            "either the sentence was reworded, in which case update this "
            "check, or the policy was narrowed on purpose, in which case say "
            "so in the file and change what this check requires"
        )

    groups, other = robots_groups(text)
    if not groups:
        problems.append("robots.txt names no crawler at all")

    # What a crawler is being asked to fetch: the path of every page that is
    # not noindex, which is the set the sitemap check already treats as the
    # site proper. A crawler can request a page by its file path or by its
    # canonical path, so a Disallow rule is tested against both; a rule
    # naming only the one a page does not use would otherwise pass unseen.
    requested: list[tuple[str, set[str]]] = []
    for page in pages:
        if page.name in NOINDEX_ALLOWED:
            continue
        file_path = "/" + page.relative_to(docs_root).as_posix()
        page_paths = {file_path}
        canon = canonical_path(page.read_bytes())
        if canon:
            page_paths.add(canon if canon.startswith("/") else "/" + canon)
        requested.append((file_path, page_paths))
    wanted = sorted(file_path for file_path, _ in requested)
    for agents, rules in groups:
        for field, value in rules:
            if field != "disallow" or not value:
                continue
            pattern = robots_disallow_pattern(value)
            blocked = [
                file_path
                for file_path, page_paths in requested
                if any(pattern.match(path) for path in page_paths)
            ]
            if value == "/" or blocked:
                problems.append(
                    f"robots.txt tells {', '.join(agents)} to stay out of "
                    f"{value!r}, which covers "
                    f"{len(blocked) or len(wanted)} of the site's "
                    f"{len(wanted)} pages"
                )
        if not any(field == "allow" for field, _ in rules):
            problems.append(
                f"robots.txt names {', '.join(agents)} and then gives that "
                "group no Allow rule, so the group says nothing"
            )

    catch_all = [agents for agents, _ in groups if "*" in agents]
    if not catch_all:
        problems.append(
            "robots.txt has no `User-agent: *` group, so a crawler the file "
            "does not name by hand is left to guess"
        )

    sitemaps = [value for field, value in other if field == "sitemap"]
    expected = SITE["site_url"].rstrip("/") + "/sitemap.xml"
    if len(sitemaps) != 1:
        problems.append(
            f"robots.txt carries {len(sitemaps)} Sitemap lines rather than one"
        )
    elif sitemaps[0] != expected:
        problems.append(
            f"robots.txt points a crawler at {sitemaps[0]!r}, and this site is "
            f"published at {expected!r}"
        )
    elif not (docs_root / "sitemap.xml").is_file():
        problems.append(
            f"robots.txt points a crawler at {sitemaps[0]!r}, and this tree "
            "publishes no sitemap.xml"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] robots.txt lets the site be found: "
        f"{len(groups)} crawler groups and {len(wanted)} pages checked, "
        f"{len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_privacy_statement(pages: list[Path], docs_root: Path) -> bool:
    """The privacy policy's checkable claims are true of the tree it describes.

    The identity check reads every host the tree names and requires it to be
    allowed by site.json, which is a question about whose accounts these are.
    This is a different question with a different answer: the policy tells a
    visitor that two named companies see a request and nobody else does, and
    a host added to the allowlist for a good reason satisfies that check while
    falsifying this page. A web font, an embedded map, a hosted icon set or a
    line of script that remembers something in localStorage each turn a
    published privacy policy into a false statement, quietly, in an edit that
    looks like an improvement.
    """
    problems: list[str] = []
    policy = docs_root / "privacy.html"
    if not policy.is_file():
        print("[FAIL] the privacy policy is true: privacy.html is missing")
        return False
    text = " ".join(policy.read_text(encoding="utf-8").split())
    for claim in PRIVACY_CLAIMS:
        if text.count(claim) != 1:
            problems.append(
                f"privacy.html no longer states {claim!r} exactly once, so "
                "either the promise was reworded, in which case update this "
                "check, or it was withdrawn, in which case delete the part of "
                "this check that enforces it"
            )

    own_host = SITE["site_url"].split("://", 1)[1].rstrip("/")
    # The two the policy names, taken from the markers the tracking check
    # already uses, so a tracker that moves host cannot be allowed here by
    # spelling it a second time.
    disclosed = {
        BEACON_MARKER.decode("utf-8").split("/", 1)[0],
        PIXEL_MARKER.decode("utf-8"),
    }

    def is_disclosed(host: str) -> bool:
        """Say whether a host is the site's own or one the policy names."""
        if host == own_host:
            return True
        # A subdomain of a named service, because the beacon marker names the
        # company's domain and the script is served from a host under it.
        return any(
            host == domain or host.endswith("." + domain) for domain in disclosed
        )

    fetched = 0
    for page in pages:
        page_text = page.read_text(encoding="utf-8")
        for element in RESOURCE_RE.finditer(page_text):
            for attribute in RESOURCE_URL_RE.finditer(element.group(2)):
                for candidate in attribute.group(2).split(","):
                    url = candidate.strip().split(" ")[0]
                    host = ABSOLUTE_HOST_RE.match(url)
                    if not host:
                        continue
                    fetched += 1
                    if not is_disclosed(host.group(1)):
                        problems.append(
                            f"{page.name}: a <{element.group(1).lower()}> "
                            f"loads from {host.group(1)!r}, which the privacy "
                            "policy does not tell a visitor about"
                        )

        # CSS is invisible to RESOURCE_RE: a <style> block or a style=""
        # attribute can @import or url() a third party host with no tag
        # the scan above matches. A browser decodes entities in an
        # attribute value before its CSS parser sees it, so &quot; still
        # fetches; <style> element text is not decoded, so it is left raw.
        for element in STYLE_ELEMENT_RE.finditer(page_text):
            count, css_problems = css_fetch_problems(
                page.name, element.group(1), is_disclosed
            )
            fetched += count
            problems.extend(css_problems)
        for element in STYLE_ATTR_RE.finditer(page_text):
            css_text = html_lib.unescape(element.group(2))
            count, css_problems = css_fetch_problems(
                page.name, css_text, is_disclosed
            )
            fetched += count
            problems.extend(css_problems)

    # A stylesheet does not have to be inlined in a page to fetch from a
    # third party; every .css file under the built tree gets the same read.
    for css_path in sorted(docs_root.rglob("*.css")):
        css_text = css_path.read_text(encoding="utf-8", errors="ignore")
        count, css_problems = css_fetch_problems(
            css_path.name, css_text, is_disclosed
        )
        fetched += count
        problems.extend(css_problems)

    stored = sorted(
        path
        for path in docs_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".js"}
    )
    for path in stored:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for marker in STORAGE_MARKERS:
            if marker in content:
                problems.append(
                    f"{path.name}: uses {marker}, and the policy says this "
                    "site stores nothing on a visitor's device"
                )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the privacy policy is true where it is "
        f"checkable: {fetched} fetched URLs and {len(stored)} files checked, "
        f"{len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


# The two accessibility claims the check above leaves alone, because they are
# about how a page behaves rather than how it is marked up.
KEYBOARD_CLAIM = "Navigation, including the mobile menu, works with a keyboard."
LABEL_CLAIM = "Form fields on the login preview have visible labels."
# The mobile menu is a details element with a summary, which a browser opens
# from the keyboard on its own. A button and a script would look the same to
# every other check here and to anyone using a mouse.
MENU_RE = re.compile(
    r'<details[^>]*\bclass\s*=\s*(["\'])[^"\']*\bnav-menu\b[^"\']*\1[^>]*>'
    r"(.*?)</details>",
    re.IGNORECASE | re.DOTALL,
)
ANY_TAG_RE = re.compile(r"<[a-zA-Z][^>]*>", re.DOTALL)
INLINE_HANDLER_RE = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)
TABINDEX_RE = re.compile(r'\btabindex\s*=\s*["\']?(-?\d+)', re.IGNORECASE)
FIELD_RE = re.compile(r"<(input|select|textarea)\b([^>]*)>", re.IGNORECASE | re.DOTALL)
LABEL_RE = re.compile(r"<label\b([^>]*)>(.*?)</label\s*>", re.IGNORECASE | re.DOTALL)
# Field types a visitor does not type into, which carry their own name.
UNLABELLED_TYPES = ("hidden", "submit", "button", "reset", "image")
# Class names that take a label out of the page while leaving it in the
# markup. The claim is that the labels are visible, not that they exist.
HIDDEN_LABEL_CLASSES = ("sr-only", "visually-hidden", "screen-reader-only", "hidden")
# The attribute name must stand alone, so data-class or x-class is not
# it; an unquoted value counts, matching the house shape in
# NAV_ARIA_LABEL_RE.
LABEL_CLASS_RE = re.compile(
    r'(?<![\w:.-])class\s*=\s*'
    r'(?:(["\'])(.*?)\1|([^\s"\'<>=`]+))',
    re.IGNORECASE | re.DOTALL,
)
LABEL_STYLE_RE = re.compile(
    r'(?<![\w:.-])style\s*=\s*'
    r'(?:(["\'])(.*?)\1|([^\s"\'<>=`]+))',
    re.IGNORECASE | re.DOTALL,
)
# A boolean "hidden" attribute on a label. Matched against a copy of
# the attribute string with every quoted value blanked out first (see
# the call site), so it catches hidden, hidden="" and hidden="hidden"
# without also matching the word inside a class list or inside another
# attribute's quoted value, such as aria-label="field hidden text".
LABEL_HIDDEN_ATTR_RE = re.compile(r"(?:^|\s)hidden(?:\s|=|$)", re.IGNORECASE)
# login.html is rendered without the shared header, so it has no mobile menu
# to operate. Naming it here rather than skipping every page without one is
# what stops the menu disappearing from all twenty-four of the others.
NO_MENU = "login.html"


CONTRAST_CLAIM = "Text and background colors are chosen for contrast and readability."
# The statement names a standard, and the standard carries a number. Reading
# the level out of the page rather than writing 4.5 here is what makes the
# threshold the one the site actually promises: raising the target to AAA
# raises this check with it, and lowering it is a change to a published
# sentence rather than to a constant nobody would notice.
WCAG_LEVEL_RE = re.compile(
    r"Web Content Accessibility Guidelines \(WCAG\) (\d+\.\d+) level (A+)"
)
WCAG_MINIMUM = {"A": 3.0, "AA": 4.5, "AAA": 7.0}
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
CSS_VAR_RE = re.compile(r"--([a-z0-9-]+)\s*:\s*([^;}]+)")
CSS_VAR_USE_RE = re.compile(r"var\(\s*--([a-z0-9-]+)\s*\)$")
CSS_HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")
CSS_RGBA_RE = re.compile(r"rgba?\(([^)]*)\)$")
CSS_IMPORTANT_RE = re.compile(r"!\s*important\s*$", re.IGNORECASE)

# The surfaces the site paints text on. Four, because the palette is four
# opaque colours wide, and each is confirmed below to still be used as a
# background somewhere.
CONTRAST_SURFACES = {
    "the page": "var(--white)",
    "a dark band": "var(--charcoal)",
    "the resilience band": "var(--gold)",
    "a primary button": "var(--orange)",
}

# Which surface each text colour is read on. Stated rather than derived,
# because working it out from the tree means resolving the cascade against
# the markup and nothing here does that. The table is kept honest in both
# directions: a colour the stylesheet uses and this table does not name fails,
# and so does a colour named here that the stylesheet no longer uses, so the
# list cannot drift into describing a stylesheet that no longer exists.
CONTRAST_READ_ON = {
    "var(--ink)": ("the page",),
    "var(--muted)": ("the page",),
    "var(--orange-text)": ("the page",),
    "var(--charcoal)": ("the page", "the resilience band", "a primary button"),
    "var(--white)": ("a dark band",),
    "var(--gold)": ("a dark band",),
    "rgba(254, 255, 254, 0.7)": ("a dark band",),
    "rgba(254, 255, 254, 0.76)": ("a dark band",),
    "rgba(254, 255, 254, 0.78)": ("a dark band",),
    "rgba(254, 255, 254, 0.82)": ("a dark band",),
    "rgba(254, 255, 254, 0.84)": ("a dark band",),
    "rgba(254, 255, 254, 0.86)": ("a dark band",),
    "rgba(39, 49, 56, 0.82)": ("the resilience band",),
}
# A colour that says to use whatever the element inherits, which is one of the
# values above by the time it is painted.
CONTRAST_IGNORED = ("inherit", "currentColor", "transparent")


def css_palette(css: str) -> dict[str, str]:
    """Return the custom properties declared on :root."""
    root = re.search(r":root\s*\{(.*?)\}", css, re.DOTALL)
    if not root:
        return {}
    return {name: value.strip() for name, value in CSS_VAR_RE.findall(root.group(1))}


def css_colour(value: str, palette: dict[str, str], depth: int = 0):
    """Return a colour as red, green, blue and alpha, or None if it is not one."""
    value = value.strip()
    if depth > 4:
        return None
    used = CSS_VAR_USE_RE.match(value)
    if used:
        return css_colour(palette.get(used.group(1), ""), palette, depth + 1)
    written = CSS_HEX_RE.match(value)
    if written:
        digits = written.group(1)
        if len(digits) == 3:
            digits = "".join(digit * 2 for digit in digits)
        return (
            int(digits[0:2], 16),
            int(digits[2:4], 16),
            int(digits[4:6], 16),
            1.0,
        )
    channels = CSS_RGBA_RE.match(value)
    if channels:
        parts = [part.strip() for part in channels.group(1).split(",")]
        if len(parts) not in (3, 4):
            return None
        try:
            red, green, blue = (float(part) for part in parts[:3])
            alpha = float(parts[3]) if len(parts) == 4 else 1.0
        except ValueError:
            return None
        return (red, green, blue, alpha)
    return None


def composite(colour, background):
    """Return what a partly transparent colour looks like painted on a surface."""
    return tuple(
        colour[3] * colour[index] + (1 - colour[3]) * background[index]
        for index in range(3)
    ) + (1.0,)


def relative_luminance(colour) -> float:
    """Return the WCAG relative luminance of an opaque colour."""

    def channel(value: float) -> float:
        value = value / 255
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * channel(colour[0])
        + 0.7152 * channel(colour[1])
        + 0.0722 * channel(colour[2])
    )


def contrast_ratio(text, background) -> float:
    """Return the WCAG contrast ratio between two opaque colours."""
    first, second = relative_luminance(text), relative_luminance(background)
    return (max(first, second) + 0.05) / (min(first, second) + 0.05)


def check_colour_contrast(docs_root: Path) -> bool:
    """Every colour the stylesheet paints text in reaches the ratio the site targets.

    The accessibility statement says the colours are chosen for contrast and
    names WCAG 2.1 level AA as the target, which is a number: 4.5 to 1 for
    ordinary text. Nothing computed it, and a palette is one line to edit. On
    2026-09-12 the body text on the gold band sat at 4.40, so the statement had
    been promising a standard the tree missed, and every other check passed
    because a colour that is too light is still a valid page that builds,
    renders, links and reads the same as any other.
    """
    problems: list[str] = []
    statement = docs_root / "accessibility.html"
    stylesheet = docs_root / "styles.css"
    for path in (statement, stylesheet):
        if not path.is_file():
            print(
                f"[FAIL] every text colour meets the contrast the statement "
                f"targets: {path.name} is not in the tree"
            )
            return False

    statement_text = " ".join(statement.read_text(encoding="utf-8").split())
    if statement_text.count(CONTRAST_CLAIM) != 1:
        problems.append(
            f"accessibility.html no longer states {CONTRAST_CLAIM!r} exactly "
            "once, so either the promise was reworded, in which case update "
            "this check, or it was withdrawn, in which case say what a visitor "
            "who needs contrast gets instead"
        )
    target = WCAG_LEVEL_RE.search(statement_text)
    if not target or target.group(2) not in WCAG_MINIMUM:
        print(
            "[FAIL] every text colour meets the contrast the statement "
            "targets: accessibility.html names no WCAG level, so there is no "
            "number to measure against"
        )
        return False
    version, level = target.group(1), target.group(2)
    minimum = WCAG_MINIMUM[level]

    css = CSS_COMMENT_RE.sub(" ", stylesheet.read_text(encoding="utf-8"))
    palette = css_palette(css)
    used_as_text: set[str] = set()
    used_as_background: set[str] = set()
    for _selector, body in CSS_RULE_RE.findall(css):
        for declaration in body.split(";"):
            if ":" not in declaration:
                continue
            name, value = declaration.split(":", 1)
            name, value = name.strip().lower(), value.strip()
            if name == "color":
                used_as_text.add(value)
            elif name in ("background", "background-color"):
                used_as_background.add(value.split()[0] if value else "")

    for value in sorted(used_as_text):
        if value in CONTRAST_IGNORED or value in CONTRAST_READ_ON:
            continue
        problems.append(
            f"styles.css paints text in {value!r} and nothing here says which "
            "surface that is read on, so its contrast went unmeasured"
        )
    for value in sorted(CONTRAST_READ_ON):
        if value not in used_as_text:
            problems.append(
                f"{value!r} is listed here as a text colour and styles.css no "
                "longer paints anything in it, so this list has drifted from "
                "the stylesheet"
            )
    for name, value in sorted(CONTRAST_SURFACES.items()):
        if value not in used_as_background:
            problems.append(
                f"{name} is listed here as a surface and styles.css no longer "
                f"paints anything {value!r}, so this list has drifted from the "
                "stylesheet"
            )

    measured = 0
    for value, surfaces in sorted(CONTRAST_READ_ON.items()):
        text_colour = css_colour(value, palette)
        if not text_colour:
            problems.append(f"{value!r} is not a colour this check can read")
            continue
        for name in surfaces:
            surface = css_colour(CONTRAST_SURFACES[name], palette)
            if not surface:
                problems.append(
                    f"{CONTRAST_SURFACES[name]!r} is not a colour this check can read"
                )
                continue
            measured += 1
            ratio = contrast_ratio(composite(text_colour, surface), surface)
            if ratio < minimum:
                problems.append(
                    f"{value} on {name} is {ratio:.2f} to 1, and WCAG {version} "
                    f"level {level} asks for {minimum} to 1 for ordinary text, "
                    "which the accessibility statement says this site targets"
                )

    # The table above only measures the fixed pairs it names, so a rule that
    # sets its own color and background together, on a selector the table
    # has never heard of, passes unmeasured. Pairing is per selector rather
    # than per rule, because a selector can gain its color from one rule and
    # its background from another, but only within the same cascade context:
    # an @media or @supports block, found by matching braces after ruling
    # out an at-rule statement (a semicolon before the next unquoted brace,
    # such as @charset or @import, which has no block and is left in the
    # base rather than swallowing whatever rule follows it), changes what a
    # browser paints without touching what the rest of the stylesheet
    # paints outside it. The base context is the stylesheet with every such
    # block removed, folded and measured on its own. Each block is then
    # folded twice: once starting from a copy of the base fold alone, and
    # once cumulatively, starting from the base plus every earlier block in
    # source order, because a desktop-first stylesheet can split a pair
    # across two narrowing breakpoints that only ever apply together, and
    # each block folded on the base alone never sees the other. The
    # cumulative fold can pair blocks that never apply on screen together,
    # for instance one breakpoint printed alongside another, but that only
    # ever produces a failure to double-check by eye, never a pass this
    # check is trusting, so the false positive it risks is the safe one.
    # Within any one fold, each rule's selector list is split on commas,
    # whitespace is normalised, and every selector's color and
    # background/background-color declarations are folded in source order,
    # a later declaration winning unless the earlier one is !important and
    # the later one is not, the same rule a browser applies within one
    # rule's own duplicate declarations. A selector and value pair already
    # measured once, in the base or in any earlier fold, is not measured or
    # reported again, so the two folds per block and the source order never
    # double-report or double-count the same pair. @keyframes and @font-face
    # hold no selectors, so both are ignored rather than treated as
    # contexts. A selector is only skipped, not failed, when its folded
    # background does not resolve to one opaque colour: a gradient,
    # currentColor, transparent, an image, or a translucent colour whose
    # rendered result depends on whatever sits behind it.
    ignored_at_rules = {
        "@keyframes",
        "@-webkit-keyframes",
        "@-moz-keyframes",
        "@-o-keyframes",
        "@font-face",
    }

    def skip_quoted(text: str, pos: int) -> int:
        # text[pos] is a quote character; returns the index just past its
        # matching close, honouring backslash escapes, or len(text) if the
        # string never closes. Shared by every scan below so a "}" or "{"
        # or ";" inside a quoted string, such as content: "}"; on a rule,
        # is never read as structure.
        quote = text[pos]
        j = pos + 1
        n = len(text)
        while j < n:
            if text[j] == "\\":
                j += 2
                continue
            if text[j] == quote:
                return j + 1
            j += 1
        return n

    def find_at_rule_blocks(text: str):
        # Top-level @rule { ... } blocks, found by matching braces rather
        # than by regex alone, since a block nests its inner rules one
        # level deep and CSS_RULE_RE cannot balance that on its own. Every
        # scan here skips quoted strings with skip_quoted, in the main
        # depth count, the at-rule prelude scan and the block-end brace
        # match alike, because a quoted brace desyncs whichever of the
        # three does not skip it, and CSS_RULE_RE already mis-reads a
        # selector with one on its own, which is a wider, pre-existing gap
        # this function cannot close from inside check_colour_contrast. An
        # at-rule whose first unquoted "{" or ";" is the ";" has no block
        # at all, for example @charset "UTF-8"; or @import url(x.css); or
        # @layer base, site;, so it is skipped as a statement rather than
        # read as the start of a block, and the rule that follows it stays
        # in the base instead of being swallowed as that block's body.
        blocks = []
        depth = 0
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch in ("'", '"'):
                i = skip_quoted(text, i)
                continue
            if depth == 0 and ch == "@":
                j = i
                brace_pos = None
                semi_pos = None
                while j < n:
                    c = text[j]
                    if c in ("'", '"'):
                        j = skip_quoted(text, j)
                        continue
                    if c == "{":
                        brace_pos = j
                        break
                    if c == ";":
                        semi_pos = j
                        break
                    j += 1
                if brace_pos is None and semi_pos is None:
                    break
                if semi_pos is not None and (brace_pos is None or semi_pos < brace_pos):
                    i = semi_pos + 1
                    continue
                prelude = text[i:brace_pos]
                d = 1
                j = brace_pos + 1
                while j < n and d > 0:
                    c = text[j]
                    if c in ("'", '"'):
                        j = skip_quoted(text, j)
                        continue
                    if c == "{":
                        d += 1
                    elif c == "}":
                        d -= 1
                    j += 1
                blocks.append((i, j, prelude, text[brace_pos + 1 : j - 1]))
                i = j
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            i += 1
        return blocks

    def fold_rules(rules, colour, background):
        # Folds (selector, body) rules onto the given per-selector colour
        # and background dicts in place, in source order, with the same
        # precedence a browser applies within one rule's own duplicate
        # declarations. Returns the selectors touched here, in the order
        # first touched.
        touched: list[str] = []
        for selector, body in rules:
            text_value = None
            text_important = False
            background_value = None
            background_important = False
            for declaration in body.split(";"):
                if ":" not in declaration:
                    continue
                name, value = declaration.split(":", 1)
                name = name.strip().lower()
                raw_value = value.strip()
                is_important = bool(CSS_IMPORTANT_RE.search(raw_value))
                value = CSS_IMPORTANT_RE.sub("", value).strip()
                if name == "color":
                    if text_value is not None and text_important and not is_important:
                        continue
                    text_value = value
                    text_important = is_important
                elif name in ("background", "background-color"):
                    # Whichever of the two properties is written last in
                    # the rule is what a browser paints, so the later one
                    # overwrites the earlier one here too, regardless of
                    # which name it used, unless an !important declaration
                    # already set this slot and this one is not itself
                    # !important, in which case a browser keeps the
                    # important value and this later one is ignored.
                    if (
                        background_value is not None
                        and background_important
                        and not is_important
                    ):
                        continue
                    background_value = value
                    background_important = is_important
            if text_value is None and background_value is None:
                continue
            for raw_selector in selector.split(","):
                single = re.sub(r"\s+", " ", raw_selector.strip())
                if not single:
                    continue
                if single not in touched:
                    touched.append(single)
                if text_value is not None:
                    prior = colour.get(single)
                    if prior is not None and prior[1] and not text_important:
                        pass
                    else:
                        colour[single] = (text_value, text_important)
                if background_value is not None:
                    prior = background.get(single)
                    if prior is not None and prior[1] and not background_important:
                        pass
                    else:
                        background[single] = (background_value, background_important)
        return touched

    counted_pairs: set[tuple[str, str, str]] = set()

    def measure_pair(single, colour, background, condition):
        # Measures one selector's folded pair in one context, returning
        # "measured", "skipped", or None when the selector is not fully
        # paired here or this exact selector and value pair was already
        # measured in an earlier context.
        text_entry = colour.get(single)
        background_entry = background.get(single)
        if not text_entry or not background_entry:
            return None
        text_value, background_value = text_entry[0], background_entry[0]
        key = (single, text_value, background_value)
        if key in counted_pairs:
            return None
        counted_pairs.add(key)
        text_colour = css_colour(text_value, palette)
        background_colour = css_colour(background_value, palette)
        if not text_colour or not background_colour or background_colour[3] != 1.0:
            return "skipped"
        ratio = contrast_ratio(composite(text_colour, background_colour), background_colour)
        if ratio < minimum:
            where = f" inside {condition}" if condition else ""
            problems.append(
                f"{single!r}{where} paints {text_value!r} on "
                f"{background_value!r} at {ratio:.2f} to 1, and WCAG {version} "
                f"level {level} asks for {minimum} to 1 for ordinary text, "
                "which the accessibility statement says this site targets"
            )
        return "measured"

    at_rule_blocks = find_at_rule_blocks(css)
    pieces = []
    last = 0
    contexts: list[tuple[str, str]] = []
    for start, end, prelude, inner in at_rule_blocks:
        name_match = re.match(r"@[-a-zA-Z]+", prelude.strip())
        name = name_match.group(0).lower() if name_match else ""
        pieces.append(css[last:start])
        last = end
        if name in ignored_at_rules:
            continue
        condition = re.sub(r"\s+", " ", prelude.strip())
        contexts.append((condition, inner))
    pieces.append(css[last:])
    base_css = "".join(pieces)

    base_colour: dict[str, tuple[str, bool]] = {}
    base_background: dict[str, tuple[str, bool]] = {}
    base_order = fold_rules(CSS_RULE_RE.findall(base_css), base_colour, base_background)

    selector_measured = 0
    selector_skipped = 0
    for single in base_order:
        result = measure_pair(single, base_colour, base_background, None)
        if result == "measured":
            selector_measured += 1
        elif result == "skipped":
            selector_skipped += 1

    context_count = 1
    cumulative_colour = dict(base_colour)
    cumulative_background = dict(base_background)
    for condition, inner in contexts:
        context_count += 1
        rules = CSS_RULE_RE.findall(inner)

        colour = dict(base_colour)
        background = dict(base_background)
        touched = fold_rules(rules, colour, background)
        for single in touched:
            result = measure_pair(single, colour, background, condition)
            if result == "measured":
                selector_measured += 1
            elif result == "skipped":
                selector_skipped += 1

        # Folded again cumulatively, on top of every earlier block in
        # source order rather than the base alone, so a pair split across
        # two stacking breakpoints is still caught.
        stacked = fold_rules(rules, cumulative_colour, cumulative_background)
        stacked_condition = f"{condition} after earlier @media blocks"
        for single in stacked:
            result = measure_pair(single, cumulative_colour, cumulative_background, stacked_condition)
            if result == "measured":
                selector_measured += 1
            elif result == "skipped":
                selector_skipped += 1

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] every text colour meets the contrast "
        f"the statement targets: {len(CONTRAST_READ_ON)} colours on "
        f"{measured} surfaces at {minimum} to 1 for WCAG {version} level "
        f"{level}, {selector_measured} selector pairs with their own color "
        f"and background measured directly across {context_count} contexts, "
        f"{selector_skipped} skipped, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_keyboard_operable(pages: list[Path], docs_root: Path) -> bool:
    """The menu opens and the login form is labelled without a mouse in the room.

    The accessibility statement says the navigation including the mobile menu
    works with a keyboard, and that the login preview's fields have visible
    labels. Both are true because of a choice that is invisible once made: the
    menu is a details element the browser opens on its own, and the labels are
    ordinary text beside the inputs. Replacing the details with a div and a
    click handler, or moving the labels into placeholder attributes, would
    leave the page valid, reachable, byte identical to the build and passing
    every other check here, while the statement went on promising something
    the page had stopped doing.
    """
    problems: list[str] = []
    statement = docs_root / "accessibility.html"
    if not statement.is_file():
        print(
            "[FAIL] the menu and the login form work without a mouse: "
            "accessibility.html is missing, so the promises cannot be read"
        )
        return False

    statement_text = " ".join(statement.read_text(encoding="utf-8").split())
    for claim in (KEYBOARD_CLAIM, LABEL_CLAIM):
        if statement_text.count(claim) != 1:
            problems.append(
                f"accessibility.html no longer states {claim!r} exactly once, "
                "so either the promise was reworded, in which case update this "
                "check, or it was withdrawn, in which case say what a visitor "
                "without a mouse gets instead"
            )

    menus = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        found = MENU_RE.findall(text)
        if page.name == NO_MENU:
            if found:
                problems.append(
                    f"{page.name}: carries a mobile menu, and this check "
                    "expects none here because the page is rendered without "
                    "the shared header; decide which is true"
                )
        elif len(found) != 1:
            problems.append(
                f"{page.name}: has {len(found)} mobile menus built from a "
                "details element rather than one, so the menu either went "
                "missing or is now something a keyboard may not open"
            )
        else:
            menus += 1
            inside = found[0][1]
            for element in ("<summary", "<nav"):
                if element not in inside.lower():
                    problems.append(
                        f"{page.name}: the mobile menu has no {element}> "
                        "inside it, so there is nothing for a keyboard to "
                        "open or to move through"
                    )

        for tag in ANY_TAG_RE.findall(text):
            if INLINE_HANDLER_RE.search(tag):
                problems.append(
                    f"{page.name}: an element carries an inline event handler, "
                    "so part of the page works only when script runs and only "
                    "for whichever events it was given"
                )
                break
        for match in TABINDEX_RE.finditer(text):
            if int(match.group(1)) > 0:
                problems.append(
                    f"{page.name}: an element has tabindex {match.group(1)}, "
                    "which moves it ahead of everything else and reorders the "
                    "page for anyone moving through it by keyboard"
                )

    fields = 0
    login = docs_root / NO_MENU
    if not login.is_file():
        problems.append(f"{NO_MENU} is not in the tree, so its form cannot be read")
    else:
        login_text = login.read_text(encoding="utf-8")
        login_css = docs_root / "styles.css"
        if login_css.is_file():
            login_stylesheet = CSS_COMMENT_RE.sub(
                " ", login_css.read_text(encoding="utf-8")
            )
        else:
            login_stylesheet = ""
            problems.append(
                f"{NO_MENU}: styles.css is not in the tree, so the login "
                "labels' classes cannot be read"
            )
        labels = {}
        for attributes, inner in LABEL_RE.findall(login_text):
            target = re.search(r'\bfor\s*=\s*(["\'])(.*?)\1', attributes, re.IGNORECASE)
            if target:
                labels[target.group(2)] = (attributes, inner)
        for element, attributes in FIELD_RE.findall(login_text):
            kind = re.search(r'\btype\s*=\s*(["\'])(.*?)\1', attributes, re.IGNORECASE)
            if kind and kind.group(2).lower() in UNLABELLED_TYPES:
                continue
            fields += 1
            identifier = re.search(
                r'\bid\s*=\s*(["\'])(.*?)\1', attributes, re.IGNORECASE
            )
            if not identifier:
                problems.append(
                    f"{NO_MENU}: a <{element}> has no id, so no label can name it"
                )
                continue
            if identifier.group(2) not in labels:
                problems.append(
                    f"{NO_MENU}: nothing labels {identifier.group(2)!r}, so the "
                    "visitor is told what to type by the box's position alone"
                )
                continue
            label_attributes, inner = labels[identifier.group(2)]
            if not re.sub(r"<[^>]*>", "", inner).strip():
                problems.append(
                    f"{NO_MENU}: the label for {identifier.group(2)!r} has no text"
                )
            classes = LABEL_CLASS_RE.search(label_attributes)
            if classes:
                class_value = classes.group(2) if classes.group(1) else classes.group(3)
            else:
                class_value = ""
            named = set(class_value.split())
            hidden = named.intersection(HIDDEN_LABEL_CLASSES)
            if hidden:
                problems.append(
                    f"{NO_MENU}: the label for {identifier.group(2)!r} carries "
                    f"{sorted(hidden)}, which takes it out of the page, and the "
                    "statement promises a visible one"
                )
            style_attribute = LABEL_STYLE_RE.search(label_attributes)
            if style_attribute:
                style_value = (
                    style_attribute.group(2)
                    if style_attribute.group(1)
                    else style_attribute.group(3)
                )
            else:
                style_value = ""
            if style_value and style_is_hidden(style_value):
                problems.append(
                    f"{NO_MENU}: the label for {identifier.group(2)!r} is "
                    "hidden by its inline style, and the statement promises "
                    "a visible one"
                )
            attrs_without_quoted_values = re.sub(
                r'(["\']).*?\1', '""', label_attributes, flags=re.DOTALL
            )
            if LABEL_HIDDEN_ATTR_RE.search(attrs_without_quoted_values):
                problems.append(
                    f"{NO_MENU}: the label for {identifier.group(2)!r} is "
                    "hidden by its hidden attribute, and the statement "
                    "promises a visible one"
                )
            for name in sorted(named - hidden):
                if class_is_hidden(
                    login_stylesheet, name, assume_hidden_when_unsure=True
                ):
                    problems.append(
                        f"{NO_MENU}: the label for {identifier.group(2)!r} is "
                        f"hidden by its {name!r} class in styles.css, and the "
                        "statement promises a visible one"
                    )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the menu and the login form work "
        f"without a mouse: {menus} menus across {len(pages)} pages and "
        f"{fields} login fields checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_accessibility_statement(pages: list[Path], docs_root: Path) -> bool:
    """The accessibility page's checkable claims are true of every page.

    This page is a public statement about how the site treats people who use
    assistive technology, and it is the one page here whose sentences carry a
    promise to a visitor rather than a description of a service. Nothing
    measured it. An image added without an alt attribute, a heading level
    removed in a copy edit, or a skip link whose target id was renamed each
    leaves the statement saying something the tree stopped doing, and the
    visitor who finds out is the one who could least afford it.
    """
    problems: list[str] = []
    statement = docs_root / "accessibility.html"
    if not statement.is_file():
        print("[FAIL] the accessibility statement is true: accessibility.html is missing")
        return False
    text = " ".join(
        HTML_COMMENT_RE.sub("", statement.read_text(encoding="utf-8")).split()
    )
    for claim in ACCESSIBILITY_CLAIMS:
        if text.count(claim) != 1:
            problems.append(
                f"accessibility.html no longer states {claim!r} exactly once, "
                "so either the promise was reworded, in which case update this "
                "check, or it was withdrawn, in which case delete the part of "
                "this check that enforces it"
            )

    images = 0
    for page in pages:
        page_text = HTML_COMMENT_RE.sub("", page.read_text(encoding="utf-8"))
        identifiers = {
            match.group(2) for match in ID_ATTR_RE.finditer(page_text)
        }

        skip = SKIP_LINK_RE.search(page_text)
        if not skip:
            problems.append(f"{page.name}: has no skip link")
        else:
            href = HREF_RE.search(skip.group(0))
            target = href.group(2) if href else ""
            if not target.startswith("#"):
                problems.append(
                    f"{page.name}: the skip link points at {target!r} rather "
                    "than at a place on this page"
                )
            elif target[1:] not in identifiers:
                problems.append(
                    f"{page.name}: the skip link points at {target!r}, and "
                    "nothing on the page carries that id, so it skips nowhere"
                )

        for match in IMG_RE.finditer(page_text):
            images += 1
            if not ALT_ATTR_RE.search(match.group(1)):
                problems.append(
                    f"{page.name}: an <img> has no alt attribute, so a screen "
                    "reader reads its filename to the visitor"
                )

        if not re.search(r"<main\b", page_text, re.IGNORECASE):
            problems.append(f"{page.name}: has no <main> landmark")
        headings = len(re.findall(r"<h1\b", page_text, re.IGNORECASE))
        if headings != 1:
            problems.append(
                f"{page.name}: has {headings} <h1> headings rather than one"
            )
        for match in NAV_RE.finditer(page_text):
            label = NAV_ARIA_LABEL_RE.search(match.group(1))
            if not label:
                problems.append(
                    f"{page.name}: a <nav> has no aria-label, so a visitor "
                    "moving between landmarks cannot tell which one it is"
                )
                continue
            value = label.group(2) if label.group(1) else label.group(3)
            if not html_lib.unescape(value).strip():
                problems.append(
                    f"{page.name}: a <nav> has an empty aria-label, so a "
                    "visitor moving between landmarks cannot tell which "
                    "one it is"
                )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the accessibility statement is true "
        f"where it is checkable: {len(pages)} pages and {images} images "
        f"checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_stated_urls_resolve(pages: list[Path], docs_root: Path) -> bool:
    """Every URL a page states in a meta tag or its JSON-LD names a file that exists.

    The link check reads href and src, which is what a visitor clicks. These
    are the URLs nobody clicks: the social card image, og:url, and the image,
    url and @id values inside the structured data. They are read by a crawler
    and by whatever renders a link in a chat window, and they fail out of
    sight. The social image is the plain case, because it is named in a meta
    tag on all 24 pages and nowhere else: renaming that one file leaves every
    check here passing and every share of this site blank.
    """
    prefix = SITE["site_url"].rstrip("/")
    problems: list[str] = []
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        values = {match.group(2) for match in META_CONTENT_RE.finditer(text)}
        for match in LDJSON_RE.finditer(page.read_bytes()):
            try:
                data = json.loads(match.group(2).decode("utf-8"))
            except ValueError:
                # The JSON-LD mirror check owns unparseable structured data.
                continue
            values.update(stated_urls(data, prefix))
        for value in sorted(values):
            if not (value.startswith(prefix) or value.startswith("/")):
                continue
            checked += 1
            kind, target = resolve_internal(value, page, docs_root)
            if kind != "internal" or target is None or not path_case_matches(target, docs_root):
                problems.append(
                    f"{page.name}: states {value!r}, which is not a file this "
                    "site publishes"
                )
    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] every URL stated outside a link "
        f"resolves: {checked} checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


# A negative length starts with a minus sign and is not a zero value, so
# "-0", "-0px" and "-0%" do not count as pulling an element off screen.
NEGATIVE_LENGTH_RE = re.compile(r"^-(\d*\.?\d+)")


def is_negative_length(value: str) -> bool:
    """True if a CSS length is negative and not a zero-valued negative."""
    match = NEGATIVE_LENGTH_RE.match(value.strip())
    return bool(match) and float(match.group(1)) != 0


# A CSS length or plain number that resolves to zero regardless of sign or
# unit, "0", "0px", "-0%" and "0.0" alike. Anchored to the whole value: a
# browser drops a declaration whose value carries anything past a bare
# signed number and, at most, one recognized unit, "0 important" (a missing
# !) and "0foo" included, so this must not read either as zero. Used to
# read each of clip: rect(...)'s four offsets, which are lengths and may
# carry any of these units; opacity is not a length and reads with
# is_zero_opacity instead.
ZERO_LENGTH_RE = re.compile(
    r"^[+-]?(\d*\.?\d+)"
    r"(px|%|em|rem|ex|ch|vw|vh|vmin|vmax|pt|pc|cm|mm|in|q)?$",
    re.IGNORECASE,
)


def is_zero_length(value: str) -> bool:
    """True if a CSS length or plain number is zero, false for anything the value carries beyond a number and a unit."""
    match = ZERO_LENGTH_RE.match(value.strip())
    return bool(match) and float(match.group(1)) == 0


# opacity takes an <alpha-value>, a plain number or a percentage, and
# nothing else: a length unit like "0px" is not a valid opacity and a
# browser drops the declaration, so it must not read as zero either.
# Anchored to the whole value the same way ZERO_LENGTH_RE is.
ZERO_OPACITY_RE = re.compile(r"^[+-]?(\d*\.?\d+)%?$")


def is_zero_opacity(value: str) -> bool:
    """True if an opacity value is a signed number, with an optional %, that is zero."""
    match = ZERO_OPACITY_RE.match(value.strip())
    return bool(match) and float(match.group(1)) == 0


CLIP_RECT_RE = re.compile(r"rect\(\s*([^)]*)\)", re.IGNORECASE)


def clip_rect_is_zero(value: str) -> bool:
    """True if a clip: rect(...) value's four lengths are all zero.

    The legacy rect() syntax separates its four offsets with commas or,
    non-standard but still shipped by browsers, with plain whitespace.
    Anything other than exactly four lengths, or any of the four not zero,
    is not hidden.
    """
    match = CLIP_RECT_RE.search(value)
    if not match:
        return False
    parts = [part for part in re.split(r"[\s,]+", match.group(1).strip()) if part]
    return len(parts) == 4 and all(is_zero_length(part) for part in parts)


CLIP_PATH_INSET_RE = re.compile(r"inset\(\s*([^)]*)\)", re.IGNORECASE)


ROUND_KEYWORD_RE = re.compile(r"\bround\b", re.IGNORECASE)


def inset_side_value(part: str):
    """Read one inset() argument as a percentage, or None if it is not one.

    A percentage parses as its number. A bare zero, the one length CSS
    lets through without a unit, parses as 0. Anything else, a length with
    a unit such as "10px", a unitless non-zero number, or unparseable
    text, is not a percentage and returns None.
    """
    if part.endswith("%"):
        try:
            return float(part[:-1])
        except ValueError:
            return None
    try:
        if float(part) == 0:
            return 0.0
    except ValueError:
        pass
    return None


def clip_path_is_full_inset(value: str) -> bool:
    """True if a clip-path: inset(...) collapses the box to nothing wide or tall.

    Reads one to four percentage values and expands them the way CSS
    expands inset()'s own shorthand: one value applies to all four sides;
    two are top/bottom then left/right; three are top, left/right, then
    bottom; four are top, right, bottom, left. Anything from a round
    keyword onward, the corner-rounding syntax, is ignored first. Hidden
    when the top and bottom insets add to 100% or more, or the left and
    right insets do, either of which collapses the box's height or width
    to nothing. A value that is not a percentage, a length with a unit
    such as "10px" included, means not hidden, and so does anything
    malformed: more than four values, no values, or text that does not
    parse as a percentage or a bare zero.
    """
    match = CLIP_PATH_INSET_RE.search(value)
    if not match:
        return False
    inside = match.group(1)
    keyword = ROUND_KEYWORD_RE.search(inside)
    if keyword:
        inside = inside[: keyword.start()]
    parts = inside.split()
    if not parts or len(parts) > 4:
        return False
    sides = [inset_side_value(part) for part in parts]
    if any(side is None for side in sides):
        return False
    if len(sides) == 1:
        top = right = bottom = left = sides[0]
    elif len(sides) == 2:
        top = bottom = sides[0]
        right = left = sides[1]
    elif len(sides) == 3:
        top = sides[0]
        right = left = sides[1]
        bottom = sides[2]
    else:
        top, right, bottom, left = sides
    return top + bottom >= 100 or left + right >= 100


# The screen-reader-only pattern shrinks an element to at most a pixel
# rather than moving it off screen: a unitless 0, or a non-negative number
# in px that is at most 1, "0.5px", "1.0px" and ".5px" included. A plain
# "1" with no unit, anything over 1px, any other unit, a percentage, auto
# and calc() are all not hidden by size.
TINY_DIMENSION_RE = re.compile(r"^(\d*\.\d+|\d+\.?\d*)(px)?$")


def is_tiny_dimension(value: str) -> bool:
    """True for a unitless 0, or a non-negative px length at most 1px."""
    match = TINY_DIMENSION_RE.match(value.strip().lower())
    if not match:
        return False
    number = float(match.group(1))
    if match.group(2) == "px":
        return 0 <= number <= 1
    return number == 0


def declarations_are_hidden(winning_value: dict[str, str]) -> bool:
    """True if a resolved set of cascade declarations hides its element.

    display: none, visibility: hidden, opacity: 0, and clip-path:
    inset(50%) or larger hide an element on their own, position included
    or not: clip-path applies to any box, not only an absolutely
    positioned one. The remaining three only take an element off screen
    when it is also positioned absolute or fixed: a negative left or top,
    a clip: rect(...) whose four lengths are all zero, since clip only
    applies to an absolutely positioned box, and a width and height each
    at most 1px paired with overflow: hidden, since shrinking the box does
    nothing to an element still sitting in normal flow. This is the one
    place style_is_hidden and class_is_hidden both read to turn a resolved
    set of declarations into a yes or no.
    """
    if winning_value.get("display") == "none":
        return True
    if winning_value.get("visibility") == "hidden":
        return True
    if is_zero_opacity(winning_value.get("opacity", "1")):
        return True
    if clip_path_is_full_inset(winning_value.get("clip-path", "")):
        return True
    if winning_value.get("position") in OFF_SCREEN_POSITIONS:
        if is_negative_length(winning_value.get("left", "")) or is_negative_length(
            winning_value.get("top", "")
        ):
            return True
        if clip_rect_is_zero(winning_value.get("clip", "")):
            return True
        if (
            winning_value.get("overflow") == "hidden"
            and is_tiny_dimension(winning_value.get("width", ""))
            and is_tiny_dimension(winning_value.get("height", ""))
        ):
            return True
    return False


def style_is_hidden(style_text: str) -> bool:
    """Decide whether an inline style attribute hides its element outright.

    Folds the style attribute's own declarations in source order the same
    way class_is_hidden folds a stylesheet's cascade: the last value
    written for each of CASCADE_HIDING_PROPERTIES wins, unless an earlier
    declaration carries !important and the later one does not, in which
    case the !important declaration keeps winning until a later
    !important replaces it. Hidden for display: none, visibility: hidden,
    opacity: 0, or clip-path: inset(50%) or larger regardless of position,
    or an absolute or fixed position combined with a negative left or top
    or a clip: rect(...) whose four lengths are all zero, or a width and
    height each at most 1px paired with overflow: hidden, which is
    declarations_are_hidden's definition, shared with class_is_hidden.
    """
    winning_value: dict[str, str] = {}
    winning_important: dict[str, bool] = {}
    for declaration in style_text.split(";"):
        if ":" not in declaration:
            continue
        name, value = declaration.split(":", 1)
        name = name.strip().lower()
        if name not in CASCADE_HIDING_PROPERTIES:
            continue
        important = value.strip().lower().endswith("!important")
        if important:
            value = value.rsplit("!", 1)[0]
        value = value.strip().lower()
        if winning_important.get(name) and not important:
            continue
        winning_value[name] = value
        winning_important[name] = important
    return declarations_are_hidden(winning_value)


def class_is_hidden(
    stylesheet: str, class_name: str, assume_hidden_when_unsure: bool = False
) -> bool:
    """Decide whether a class ends up hidden after the cascade resolves it.

    Walks every rule whose selector list names the class. A selector that,
    stripped, is exactly the bare class selector ("." + class_name) joins
    the ordered cascade in source order and keeps the last value written
    for each property in CASCADE_HIDING_PROPERTIES, which is how
    equal-specificity rules resolve: a later declaration beats an earlier
    one, unless the earlier one carries !important and the later one does
    not, in which case the !important declaration keeps winning until a
    later !important replaces it. CSS_RULE_RE already reads through an
    @media wrapper to the plain rules inside it, so a rule inside one is
    checked the same as a top-level rule: this does not evaluate the media
    condition, so it treats every @media rule as though it might apply,
    which is the safe assumption for a check.

    Any other selector naming the class, a compound, descendant, attribute
    or pseudo-class selector, cannot be ranked against the bare selector by
    this function, since it does not know that selector's specificity
    relative to the bare one. What happens with that uncertainty depends on
    assume_hidden_when_unsure, because unsure is safe in opposite directions
    for a spam trap and for a visible label.

    With assume_hidden_when_unsure left at its default, False, any such
    selector that declares a CASCADE_HIDING_PROPERTIES property makes this
    function return False immediately instead of joining the cascade: in a
    browser that selector could win over the bare one and put the element
    back on screen, and this function will not vouch for the class being
    hidden when it cannot tell. This is the honeypot's direction: unsure
    means assume visible, so the spam-trap check fails rather than trust a
    class that might not hide anything.

    With assume_hidden_when_unsure True, the question flips from "is it
    certainly hidden" to "could it plausibly still be hidden": this
    function resolves the bare-selector fold exactly as above and returns
    True if that alone is hidden; otherwise it walks the non-bare rules
    that name the class and declare a CASCADE_HIDING_PROPERTIES property,
    in source order, overlaying each one's declarations onto the bare
    fold in turn, on the assumption that a non-bare rule outranks a bare
    one unless the bare declaration carries !important and the non-bare
    one does not, and returns True the moment any of those overlaid
    states is hidden. This is the label's direction: unsure means assume
    hidden, so a label is flagged rather than trusted as visible on the
    strength of a bare rule some other selector might override into
    something that still hides it. A rule whose selector list contains
    both the bare class and such a selector counts as both.

    A resolved set of declarations counts as hidden under
    declarations_are_hidden's definition: display: none, visibility:
    hidden, opacity: 0, or clip-path: inset(50%) or larger on their own,
    or an absolute or fixed position together with one of: a winning left
    or top that is a negative length, a clip: rect(...) whose four
    lengths are all zero, or a width and height each at most 1px combined
    with overflow: hidden. A position: absolute on its own is not enough,
    since an element can be absolutely positioned and still sit on
    screen.

    This is not a CSS engine. It does not rank selectors by specificity
    beyond the one assumption named above, it does not resolve
    combinators or pseudo-classes beyond that, it does not see inline
    styles, and it does not add left or top to the element's own size and
    position to know whether a small negative offset still leaves part of
    the element visible.
    """
    selector_pattern = re.compile(
        r"(?<![\w-])\." + re.escape(class_name) + r"(?![\w-])"
    )
    bare_selector = "." + class_name
    winning_value: dict[str, str] = {}
    winning_important: dict[str, bool] = {}
    non_bare_declarations: list[list[list[str]]] = []
    for selectors, body in CSS_RULE_RE.findall(stylesheet):
        matching = [
            selector
            for selector in selectors.split(",")
            if selector_pattern.search(selector)
        ]
        if not matching:
            continue
        bare_match = any(selector.strip() == bare_selector for selector in matching)
        other_match = any(selector.strip() != bare_selector for selector in matching)
        declarations = [
            declaration.split(":", 1)
            for declaration in body.split(";")
            if ":" in declaration
        ]
        if other_match and any(
            name.strip().lower() in CASCADE_HIDING_PROPERTIES
            for name, _ in declarations
        ):
            if not assume_hidden_when_unsure:
                return False
            non_bare_declarations.append(declarations)
        if not bare_match:
            continue
        for name, value in declarations:
            name = name.strip().lower()
            if name not in CASCADE_HIDING_PROPERTIES:
                continue
            important = value.strip().lower().endswith("!important")
            if important:
                value = value.rsplit("!", 1)[0]
            value = value.strip().lower()
            if winning_important.get(name) and not important:
                continue
            winning_value[name] = value
            winning_important[name] = important

    if declarations_are_hidden(winning_value):
        return True
    if not assume_hidden_when_unsure:
        return False

    overlay_value = dict(winning_value)
    overlay_important = dict(winning_important)
    for declarations in non_bare_declarations:
        for name, value in declarations:
            name = name.strip().lower()
            if name not in CASCADE_HIDING_PROPERTIES:
                continue
            important = value.strip().lower().endswith("!important")
            if important:
                value = value.rsplit("!", 1)[0]
            value = value.strip().lower()
            if overlay_important.get(name) and not important:
                continue
            overlay_value[name] = value
            overlay_important[name] = important
        if declarations_are_hidden(overlay_value):
            return True
    return False


def check_contact_form(pages: list[Path], docs_root: Path) -> bool:
    """The contact form posts to the declared endpoint and carries every field it needs.

    Nothing else here reads the form. The identity check confirms the endpoint
    string is somewhere in the tree, which it would be even if the form were
    not posting to it, and every other check treats the page as text. A form
    fails silently by construction: the visitor fills it in, the browser posts
    it, the thank-you page loads, and the field whose name attribute was lost
    in an edit simply is not in the mail. An inquiry that arrives with no
    email address and a spam trap that has become visible both look exactly
    like nobody writing in, which is the one failure a business cannot notice
    from the outside.
    """
    problems: list[str] = []
    # Forms that post somewhere. The login page carries a second form on
    # purpose: it has no action and none of its inputs has a name, so a submit
    # sends nothing anywhere, which is the point of a demonstration sign-in.
    forms = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for match in FORM_RE.finditer(text):
            opening = match.group(0)[: match.group(0).index(">") + 1]
            if attributes(opening).get("action"):
                forms.append((page, match.group(0)))

    if len(forms) != 1:
        print(
            f"[FAIL] the contact form can deliver a message: {len(forms)} forms "
            "post somewhere rather than one"
        )
        for page, _ in forms:
            print(f"       {page.name}")
        return False

    page, form = forms[0]
    opening = form[: form.index(">") + 1]
    attrs = attributes(opening)

    endpoint = SITE["third_party"]["formspree_endpoint"]
    if attrs.get("action") != endpoint:
        problems.append(
            f"{page.name}: the form posts to {attrs.get('action')!r}, not to "
            f"the declared endpoint {endpoint!r}"
        )
    if attrs.get("method", "").upper() != "POST":
        problems.append(
            f"{page.name}: the form's method is {attrs.get('method')!r}; a GET "
            "puts the message in the URL and delivers nothing"
        )

    labelled = {match.group(2) for match in LABEL_FOR_RE.finditer(form)}
    names = []
    for match in CONTROL_RE.finditer(form):
        control = attributes(match.group(2))
        if control.get("type", "").lower() == "submit":
            continue
        field = control.get("name")
        if not field:
            problems.append(
                f"{page.name}: a <{match.group(1).lower()}> in the form has no "
                "name attribute, so whatever a visitor types in it is never sent"
            )
            continue
        names.append(field)
        if control.get("type", "").lower() == "hidden":
            continue
        identifier = control.get("id")
        if not identifier or identifier not in labelled:
            problems.append(
                f"{page.name}: the field named {field!r} has no label pointing "
                "at it, so a screen reader cannot say what it is for"
            )

    for field in REQUIRED_FIELDS:
        if field not in names:
            problems.append(
                f"{page.name}: the form has no field named {field!r}, so an "
                "inquiry arrives without it"
            )
    if HONEYPOT_FIELD not in names:
        problems.append(
            f"{page.name}: the form has no {HONEYPOT_FIELD!r} field, so the "
            "spam trap is gone"
        )
    else:
        offset = form.index(HONEYPOT_FIELD)
        wrappers = WRAPPER_CLASS_RE.findall(form[:offset])
        stylesheet = CSS_COMMENT_RE.sub(
            " ", (docs_root / "styles.css").read_text(encoding="utf-8")
        )
        hidden = False
        for _quote, classes in wrappers[-1:]:
            for name in classes.split():
                if class_is_hidden(stylesheet, name):
                    hidden = True
        if not hidden:
            problems.append(
                f"{page.name}: nothing in styles.css reliably hides the element "
                f"holding the {HONEYPOT_FIELD!r} field, so a visitor might see it "
                "and fill it in, and every submission that does is discarded"
            )

    redirect = None
    for match in CONTROL_RE.finditer(form):
        control = attributes(match.group(2))
        if control.get("name") == "_next":
            redirect = control.get("value")
    if redirect is None:
        problems.append(
            f"{page.name}: the form has no _next field, so a visitor who sends "
            "a message lands on the form service's own page"
        )
    else:
        kind, target = resolve_internal(redirect, page, docs_root)
        if kind != "internal" or target is None or not path_case_matches(target, docs_root):
            problems.append(
                f"{page.name}: _next points at {redirect!r}, which is not a "
                "page of this site"
            )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the contact form can deliver a message: "
        f"{len(names)} fields checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_cname(docs_root: Path) -> bool:
    """docs/CNAME names the declared host, and carries it as a single bare LF line.

    Every other check reads pages. This one file is read by GitHub Pages
    itself to decide which domain serves the tree, and no check read it at all:
    the identity check scans .html, .xml and .txt, and CNAME has no extension.
    A tree whose CNAME still names the previous owner's domain passes every
    other check here and then either serves nothing or serves someone else's
    domain. The line ending matters as much as the host, because Pages reads
    the file literally and a CRLF makes the host a different string.
    """
    host = SITE["site_url"].split("://", 1)[1].rstrip("/")
    path = docs_root / "CNAME"
    problems: list[str] = []
    if not path.is_file():
        problems.append("docs/CNAME is missing, so the custom domain is unset")
    else:
        raw = path.read_bytes()
        if b"\r" in raw:
            problems.append(
                "CNAME carries a carriage return; GitHub Pages reads the file "
                "literally and would take the host to be a different string"
            )
        if raw != (host + "\n").encode("utf-8"):
            problems.append(
                f"CNAME reads {raw!r}, not the declared host {host!r} "
                "followed by one newline"
            )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] CNAME names the declared host: "
        f"{len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_phone_is_one_number(pages: list[Path], docs_root: Path) -> bool:
    """The three declared forms of the phone number are the same number, and every tel: link uses it.

    site.json declares the phone three times: as it is displayed, as a tel:
    URI, and in the form schema.org wants. Nothing made them agree. A new
    owner who changed the displayed number and missed the other two published
    a site whose visible number was theirs and whose every Call button dialled
    the previous owner, with all ten checks green. The visible text check
    cannot see it, because a tel: href is an attribute rather than text.
    """
    problems: list[str] = []
    display, tel_uri = SITE["phone_display"], SITE["phone_tel_uri"]
    schema = SITE["phone_schema"]
    if digits(tel_uri) != digits(schema):
        problems.append(
            f"phone_tel_uri {tel_uri!r} and phone_schema {schema!r} are "
            "different numbers"
        )
    if not digits(tel_uri).endswith(digits(display)):
        problems.append(
            f"phone_display {display!r} is not the number phone_tel_uri "
            f"{tel_uri!r} dials"
        )

    # Every file a visitor can fetch, not only the pages: a tel: link in the
    # sitemap or llms.txt would be as wrong and as invisible.
    found = 0
    for path in sorted(docs_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for _quote, href in TEL_HREF_RE.findall(text):
            found += 1
            if href != tel_uri:
                problems.append(
                    f"{path.name}: a Call link dials {href!r}, not the declared "
                    f"{tel_uri!r}"
                )
    if not found:
        problems.append(
            "no page carries a tel: link, so nothing was compared against the "
            "declared number"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the phone number is one number everywhere: "
        f"{found} Call links checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


CSP_META_RE = re.compile(
    r'<meta[^>]*?http-equiv\s*=\s*(["\'])Content-Security-Policy\1[^>]*?'
    r'content\s*=\s*(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)
FORM_TAG_RE = re.compile(r"<form\b([^>]*)>", re.IGNORECASE | re.DOTALL)
SCRIPT_START_TAG_RE = re.compile(r"<script\b([^>]*)>", re.IGNORECASE | re.DOTALL)
SCRIPT_ELEMENT_RE = re.compile(
    r"<script\b([^>]*)>(.*?)</script>", re.IGNORECASE | re.DOTALL
)
# The lookbehind is what keeps this from matching data-src or any other
# attribute that merely ends in "src". The unquoted branch is what an owner
# who leaves the quotes off still gets read; group(2) is the quoted value,
# group(3) is the unquoted one, and exactly one of them is set. Named apart
# from SRC_ATTR_RE below, which is the image checks' quoted-only version and
# is left alone.
SCRIPT_SRC_ATTR_RE = re.compile(
    r'(?<![\w:.-])src\s*=\s*(?:(["\'])(.*?)\1|([^\s"\'<>=`]+))',
    re.IGNORECASE | re.DOTALL,
)
LOGIN_PROMISE = "transmits or stores nothing entered into it"
# The directives that make the promise true rather than merely intended. A
# form with no action posts to its own URL, so 'none' is what stops it.
REQUIRED_CSP = {
    "default-src": "'self'",
    "connect-src": "'none'",
    "form-action": "'none'",
    "object-src": "'none'",
    "base-uri": "'none'",
}
# What the page's own script must not contain. The page has no other script,
# and a CSP is a browser's rule rather than a reason not to read the code.
FORBIDDEN_IN_SCRIPT = (
    "fetch(", "XMLHttpRequest", "navigator.sendBeacon", "localStorage",
    "sessionStorage", "document.cookie", "indexedDB", "WebSocket",
)


def csp_directives(content: str) -> dict[str, str]:
    """Return the policy as a mapping of directive to its value."""
    directives: dict[str, str] = {}
    for part in content.split(";"):
        name, _, value = part.strip().partition(" ")
        if name:
            directives[name.lower()] = value.strip()
    return directives


def check_login_promise(docs_root: Path) -> bool:
    """The login page says it sends and keeps nothing, and the markup has to agree.

    It is the one page that asks a visitor for a password, and the sentence at
    the top of its source says what happens to it. Nothing read that sentence.
    A form that gained an action attribute, a policy that lost form-action
    'none', or a script that gained a fetch would each turn a page that keeps
    credentials on the machine into one that sends them somewhere, and every
    other check here would pass: the page would still be valid, reachable,
    byte identical to the build, and free of the analytics tags the login
    check already forbids.

    A script element is read the same way, whatever it points at. One with a
    src on another host, absolute or protocol-relative, is a second delivery
    path for exactly what the CSP and the fetch scan below exist to stop, so
    it fails here rather than relying on a browser to enforce the policy. The
    promise names what happens to what a visitor types, not only what the
    named site.js does, so an inline script counts too: it is scanned for the
    same forbidden calls as an external one. A script inside an HTML comment
    loads nowhere, so comments are stripped before any of this runs.
    """
    problems: list[str] = []
    page = docs_root / "login.html"
    if not page.is_file():
        print(
            "[FAIL] the login page sends and keeps nothing: login.html is not "
            "in the tree, so the promise cannot be read"
        )
        return False

    text = page.read_text(encoding="utf-8")
    if text.count(LOGIN_PROMISE) != 1:
        problems.append(
            f"login.html no longer states {LOGIN_PROMISE!r} exactly once, so "
            "either the sentence was reworded, in which case update this "
            "check, or the promise was withdrawn, in which case say what the "
            "page now does with what a visitor types"
        )

    meta = CSP_META_RE.search(text)
    if not meta:
        problems.append(
            "login.html carries no Content-Security-Policy, which is the only "
            "one in the tree and the thing that stops the form posting"
        )
    else:
        directives = csp_directives(html_lib.unescape(meta.group(3)))
        for name, expected in REQUIRED_CSP.items():
            actual = directives.get(name)
            if actual != expected:
                problems.append(
                    f"login.html: the policy says {name} {actual!r} rather "
                    f"than {expected!r}, so the page no longer enforces what "
                    "its own first sentence promises"
                )

    for attributes in FORM_TAG_RE.findall(text):
        if re.search(r"\baction\s*=", attributes, re.IGNORECASE):
            problems.append(
                "login.html: the form carries an action attribute, so what a "
                "visitor types is sent somewhere"
            )

    for name in sorted(p.name for p in docs_root.glob("*.js")):
        if f'src="{name}' not in text and f"src='{name}" not in text:
            continue
        script_text = (docs_root / name).read_text(encoding="utf-8")
        for token in FORBIDDEN_IN_SCRIPT:
            if token in script_text:
                problems.append(
                    f"{name} is loaded by login.html and contains {token!r}, "
                    "which sends or keeps what a visitor types"
                )

    # site.json declares the site's own host once; a script element pointing
    # anywhere else is a second delivery path for what a visitor types,
    # whatever the byte-string tracking markers elsewhere do or do not match.
    # Compared lower-cased on both sides, so an uppercase spelling of either
    # is not a false fail or a false pass.
    own_host = SITE["site_url"].split("://", 1)[1].rstrip("/").lower()
    scannable = HTML_COMMENT_RE.sub(" ", text)

    def script_src_host(src: str) -> str | None:
        if src.startswith("//"):
            return src[2:].split("/", 1)[0].lower()
        scheme_match = re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://([^/]+)", src)
        return scheme_match.group(1).lower() if scheme_match else None

    # Read from every script start tag, not only ones with a closing tag, so
    # an unclosed <script src=...> still counts; the inline body scan below
    # needs a complete element and stays separate.
    for attributes in SCRIPT_START_TAG_RE.findall(scannable):
        src_match = SCRIPT_SRC_ATTR_RE.search(attributes)
        if not src_match:
            continue
        raw_src = src_match.group(2) if src_match.group(1) else src_match.group(3)
        src = html_lib.unescape(raw_src).strip()
        host = script_src_host(src)
        if host is not None and host != own_host:
            problems.append(
                f"login.html: a script element loads {src!r}, whose host "
                f"is not the site's own {own_host!r}, so what a visitor "
                "types can be sent wherever that host wants"
            )

    for attributes, body in SCRIPT_ELEMENT_RE.findall(scannable):
        if SCRIPT_SRC_ATTR_RE.search(attributes):
            continue
        for token in FORBIDDEN_IN_SCRIPT:
            if token in body:
                problems.append(
                    f"login.html: an inline script contains {token!r}, "
                    "which sends or keeps what a visitor types"
                )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the login page sends and keeps "
        f"nothing: {len(REQUIRED_CSP)} policy directives and every script it "
        f"loads checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_login_tracking(pages: list[Path]) -> bool:
    """login.html carries no analytics beacon or tracking pixel; every other page carries both."""
    problems: list[str] = []
    beacon_host = BEACON_MARKER.decode("utf-8")
    pixel_host = PIXEL_MARKER.decode("utf-8")
    for page in pages:
        raw = page.read_bytes()
        if page.name == "login.html":
            has_beacon = BEACON_MARKER in raw
            has_pixel = PIXEL_MARKER in raw
            if has_beacon or has_pixel:
                problems.append(f"login.html: carries {'a beacon' if has_beacon else ''}"
                                 f"{' and ' if has_beacon and has_pixel else ''}"
                                 f"{'a tracking pixel' if has_pixel else ''}")
            continue

        # A commented-out element renders nothing, so the beacon and the
        # pixel are read from the src attribute of a live start tag only,
        # never from raw bytes that could sit inside a comment or a prose
        # mention of the host. SCRIPT_SRC_ATTR_RE is what keeps a
        # renamed data-src attribute from counting.
        text = HTML_COMMENT_RE.sub("", raw.decode("utf-8"))
        has_beacon = False
        for match in SCRIPT_START_TAG_RE.finditer(text):
            src_match = SCRIPT_SRC_ATTR_RE.search(match.group(1))
            if not src_match:
                continue
            value = src_match.group(2) if src_match.group(2) is not None else src_match.group(3)
            if value and beacon_host in value:
                has_beacon = True
                break
        has_pixel = False
        for match in IMG_RE.finditer(text):
            src_match = SCRIPT_SRC_ATTR_RE.search(match.group(1))
            if not src_match:
                continue
            value = src_match.group(2) if src_match.group(2) is not None else src_match.group(3)
            if value and pixel_host in value:
                has_pixel = True
                break
        if not has_beacon or not has_pixel:
            missing = []
            if not has_beacon:
                missing.append("beacon")
            if not has_pixel:
                missing.append("tracking pixel")
            problems.append(f"{page.name}: missing {' and '.join(missing)}")

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] login.html has no analytics tag, every other page has both: "
          f"{len(pages)} pages checked, {len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_no_forbidden_claims(pages: list[Path]) -> bool:
    """No page carries Review/AggregateRating/offers markup or the wrong security credential.

    Justified directly by THEORY.md: the site claims no clients, testimonials,
    ratings, prices, or results, and carries no Review, AggregateRating, or
    offers markup, and the credential is Internal Security Assessor (ISA),
    never Qualified Security Assessor. Both are exact, mechanically checkable
    strings, not a restated style preference.

    The forbidden phrase is checked two ways: as decoded, whitespace-collapsed,
    casefolded markup, which still catches it inside an attribute value where
    there is no rendered text; and as `visible_text`, which also catches a
    split inline tag. A page matching either is reported once.
    """
    problems: list[str] = []
    for page in pages:
        raw = page.read_bytes()
        for label, pattern in FORBIDDEN_MARKUP:
            if pattern.search(raw):
                problems.append(f"{page.name}: contains {label!r}")
        markup_text = " ".join(html_lib.unescape(raw.decode("utf-8")).split()).casefold()
        visible = " ".join(visible_text(raw).split()).casefold()
        for marker in FORBIDDEN_TEXT:
            folded = marker.casefold()
            if folded in markup_text or folded in visible:
                problems.append(f"{page.name}: contains {marker!r}")

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] no Review/AggregateRating/offers markup, "
          f"no 'Qualified Security Assessor': {len(pages)} pages checked, {len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def page_title(raw: bytes) -> str | None:
    """Return a page's <title> text as a single collapsed, entity-decoded line, or None."""
    match = TITLE_RE.search(raw)
    if match is None:
        return None
    return " ".join(html_lib.unescape(match.group(1).decode("utf-8")).split())


def find_graph_nodes(data, node_type: str) -> list:
    """Return every node in data["@graph"] whose "@type" equals node_type."""
    # Every one of them, because returning the first was the hole. A node
    # duplicated while restructuring the JSON-LD leaves a stale copy behind it,
    # and comparing only the first compares the correct node and never sees the
    # wrong one, which is the defect class this file exists to close.
    if not isinstance(data, dict):
        return []
    graph = data.get("@graph")
    if not isinstance(graph, list):
        return []
    return [
        node
        for node in graph
        if isinstance(node, dict) and node.get("@type") == node_type
    ]


# The size a link preview is rendered at. Carried here rather than read from a
# page, because no sentence on this site promises it: it is what Facebook,
# LinkedIn, Slack and X each ask for, and a smaller file is either upscaled or
# dropped for a blank card. Nothing else in the tree states it.
SOCIAL_IMAGE_SIZE = (1200, 630)

IMG_ATTRS_RE = re.compile(r"<img\b([^>]*)>", re.IGNORECASE | re.DOTALL)
META_TAG_RE = re.compile(r"<meta\b([^>]*)>", re.IGNORECASE | re.DOTALL)
PICTURE_RE = re.compile(r"<picture\b[^>]*>(.*?)</picture\s*>", re.IGNORECASE | re.DOTALL)
SOURCE_RE = re.compile(r"<source\b([^>]*)>", re.IGNORECASE | re.DOTALL)
WIDTH_ATTR_RE = re.compile(r'\bwidth\s*=\s*["\']?(\d+)', re.IGNORECASE)
HEIGHT_ATTR_RE = re.compile(r'\bheight\s*=\s*["\']?(\d+)', re.IGNORECASE)
SRC_ATTR_RE = re.compile(r'\bsrc\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)
SRCSET_ATTR_RE = re.compile(r'\bsrcset\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)
SVG_VIEWBOX_RE = re.compile(
    r'viewBox\s*=\s*(["\'])\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)\s*\1',
    re.IGNORECASE,
)


def image_size(path: Path):
    """Return an image file's pixel size, or None with the reason it could not be read.

    build_site.py imports this to render the og:image width and height from
    the card's real size instead of a literal, which is why it stays a plain
    function rather than a method on something else.
    """
    raw = path.read_bytes()
    if raw[:8] == b"\x89PNG\r\n\x1a\n" and raw[12:16] == b"IHDR":
        return (
            int.from_bytes(raw[16:20], "big"),
            int.from_bytes(raw[20:24], "big"),
        ), None
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        chunk = raw[12:16]
        if chunk == b"VP8X":
            return (
                int.from_bytes(raw[24:27], "little") + 1,
                int.from_bytes(raw[27:30], "little") + 1,
            ), None
        if chunk == b"VP8 ":
            return (
                int.from_bytes(raw[26:28], "little") & 0x3FFF,
                int.from_bytes(raw[28:30], "little") & 0x3FFF,
            ), None
        if chunk == b"VP8L" and raw[20:21] == b"\x2f":
            bits = int.from_bytes(raw[21:25], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1), None
        return None, "its WebP chunk type is one this check does not read"
    if raw[:2] == b"\xff\xd8":
        offset = 2
        while offset + 9 < len(raw):
            if raw[offset] != 0xFF:
                break
            marker = raw[offset + 1]
            length = int.from_bytes(raw[offset + 2 : offset + 4], "big")
            # Every start-of-frame marker but the four that are not frames.
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC, 0xD8):
                return (
                    int.from_bytes(raw[offset + 7 : offset + 9], "big"),
                    int.from_bytes(raw[offset + 5 : offset + 7], "big"),
                ), None
            offset += 2 + length
        return None, "its JPEG frame header could not be found"
    if path.suffix.lower() == ".svg":
        box = SVG_VIEWBOX_RE.search(raw.decode("utf-8", errors="ignore"))
        if box is None:
            return None, "the SVG declares no viewBox to take a shape from"
        return (float(box.group(2)), float(box.group(3))), None
    return None, "its format is one this check does not read"


def check_image_dimensions(pages: list[Path], docs_root: Path) -> bool:
    """A declared image size is the file's real size, and a picture's halves are one shape.

    width and height on an image are a statement about the file, and the
    browser believes them before the file arrives: they are what reserves the
    space so the page does not jump once it does. Nothing read them, and on
    2026-09-12 five of the six solution marks declared 640 by 640 for files
    that are 300 by 300, because the sixth is an SVG whose viewBox really is
    640 and the other five were copied from it. A declared shape that does not
    match the file is the one thing here a visitor sees rather than a crawler:
    the wrong ratio distorts the image, and the wrong size reserves a hole of
    the wrong height that the page collapses out of when the image loads.

    The same question applies to the two halves of a picture element and to the
    social card. A WebP and the PNG behind it that are different shapes swap
    the layout for whoever's browser takes the fallback, and a card image below
    the size a link preview is rendered at is upscaled or dropped, which is
    visible everywhere the site is shared and nowhere on the site.

    The og:image:width and og:image:height a page states are read by the same
    crawlers before the file arrives, so a card swapped for one of a different
    shape leaves them false even though the file itself is large enough.
    """
    problems: list[str] = []
    sizes: dict[Path, tuple] = {}

    def measure(value: str, page: Path, what: str):
        """Return the pixel size of an image a page names, or None."""
        kind, target = resolve_internal(value, page, docs_root)
        if kind != "internal" or target is None or not path_case_matches(target, docs_root):
            # The stated-URL and link checks own an image that is not there.
            return None
        if target not in sizes:
            size, reason = image_size(target)
            if size is None:
                problems.append(f"{target.name}: {reason}, so {what} went unchecked")
            sizes[target] = size
        return sizes[target]

    declared = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for match in IMG_ATTRS_RE.finditer(text):
            attrs = match.group(1)
            src = SRC_ATTR_RE.search(attrs)
            width = WIDTH_ATTR_RE.search(attrs)
            height = HEIGHT_ATTR_RE.search(attrs)
            if not (src and width and height):
                continue
            size = measure(src.group(2), page, "its declared size")
            if size is None:
                continue
            declared += 1
            stated = (float(width.group(1)), float(height.group(1)))
            if stated != tuple(float(part) for part in size):
                problems.append(
                    f"{page.name}: declares {src.group(2)} as "
                    f"{width.group(1)} by {height.group(1)} and the file is "
                    f"{size[0]:g} by {size[1]:g}, so the space the browser "
                    "reserves for it is the wrong shape"
                )

        for picture in PICTURE_RE.finditer(text):
            body = picture.group(1)
            fallback = IMG_ATTRS_RE.search(body)
            src = SRC_ATTR_RE.search(fallback.group(1)) if fallback else None
            if src is None:
                problems.append(
                    f"{page.name}: a <picture> has no <img> inside it, so a "
                    "browser that takes none of the sources shows nothing"
                )
                continue
            base = measure(src.group(2), page, "the picture it falls back to")
            for source in SOURCE_RE.finditer(body):
                srcset = SRCSET_ATTR_RE.search(source.group(1))
                if srcset is None:
                    continue
                for candidate in srcset.group(2).split(","):
                    url = candidate.strip().split(" ")[0]
                    if not url:
                        continue
                    size = measure(url, page, "a picture source")
                    if base and size and tuple(size) != tuple(base):
                        problems.append(
                            f"{page.name}: {url} is {size[0]:g} by {size[1]:g} "
                            f"and the {src.group(2)} behind it is {base[0]:g} "
                            f"by {base[1]:g}, so which one a browser can read "
                            "changes the shape of the page"
                        )

    card = SITE.get("social_image_filename")
    if card:
        target = docs_root / "assets" / card
        if path_case_matches(target, docs_root):
            size, reason = image_size(target)
            if size is None:
                problems.append(f"{card}: {reason}, so the card size went unchecked")
            elif size[0] < SOCIAL_IMAGE_SIZE[0] or size[1] < SOCIAL_IMAGE_SIZE[1]:
                problems.append(
                    f"{card} is {size[0]:g} by {size[1]:g} and a link preview "
                    f"is rendered at {SOCIAL_IMAGE_SIZE[0]} by "
                    f"{SOCIAL_IMAGE_SIZE[1]}, so every share of this site "
                    "shows it upscaled or shows nothing"
                )
        else:
            problems.append(f"{card} is declared as the card image and is not in assets/")

    for page in pages:
        text = page.read_text(encoding="utf-8")
        og_image = None
        widths: list[str] = []
        heights: list[str] = []
        for match in META_TAG_RE.finditer(text):
            attrs = attributes(match.group(1))
            prop = attrs.get("property")
            if prop == "og:image":
                og_image = attrs.get("content")
            elif prop == "og:image:width":
                widths.append(attrs.get("content"))
            elif prop == "og:image:height":
                heights.append(attrs.get("content"))
        if og_image is None:
            continue
        if len(widths) != 1 or len(heights) != 1:
            problems.append(
                f"{page.name}: og:image is declared and og:image:width/height "
                f"appear {len(widths)}/{len(heights)} times, not once each"
            )
            continue
        size = measure(html_lib.unescape(og_image), page, "its og:image declaration")
        if size is None:
            continue
        try:
            stated_wh = (float(widths[0]), float(heights[0]))
        except (TypeError, ValueError):
            problems.append(
                f"{page.name}: og:image:width/height is {widths[0]!r} by "
                f"{heights[0]!r}, which is not a number"
            )
            continue
        declared += 1
        if stated_wh != tuple(float(part) for part in size):
            problems.append(
                f"{page.name}: declares og:image as {widths[0]} by "
                f"{heights[0]} and the file is {size[0]:g} by {size[1]:g}, so "
                "a crawler reads a false card size"
            )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] a declared image size is the file's "
        f"real size: {declared} declarations and {len(sizes)} image files "
        f"read, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_jsonld_mirrors_title(pages: list[Path]) -> bool:
    """Where the tree already mirrors it, every JSON-LD block's name/description match the title/meta description.

    See the JSONLD_* tables above check_links for exactly which pages and
    nodes this covers, and why index.html and faq.html are intentionally
    excluded rather than checked against an invented rule. The build writes
    at most one application/ld+json block per page (see jsonld_fragment in
    build_site.py), so a page carrying more than one is a stale block left
    behind by an edit, and this check reads every block on the page and
    fails that on its own before it fails on what the extra block says.
    Every block on every page that carries one is parsed here, including
    index.html and faq.html, which are excused from the mirror rule but not
    from being valid JSON: this is the only check that owns a block that
    fails to parse.
    """
    problems: list[str] = []
    checked = 0
    for page in pages:
        name = page.name
        raw = page.read_bytes()
        matches = list(LDJSON_RE.finditer(raw))

        if len(matches) > 1:
            problems.append(
                f"{name}: {len(matches)} application/ld+json script blocks. The "
                "build writes one per page, so the rest are a stale block an "
                "edit left behind"
            )

        parsed: list[dict] = []
        for match in matches:
            try:
                parsed.append(json.loads(match.group(2).decode("utf-8")))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                problems.append(f"{name}: JSON-LD did not parse ({exc})")

        in_top = name in JSONLD_TOP_LEVEL_MIRROR_PAGES
        graph_node_type = JSONLD_GRAPH_MIRROR_NODE_TYPE.get(name)
        in_service = name in JSONLD_GRAPH_SERVICE_DESCRIPTION_PAGES
        if not (in_top or graph_node_type or in_service):
            if name in JSONLD_NO_MIRROR_PAGES:
                continue
            if matches:
                problems.append(
                    f"{name}: carries JSON-LD but no rule covers it. Add it to one of the"
                    " JSONLD_ tables, or to JSONLD_NO_MIRROR_PAGES with the reason."
                )
            continue

        if not matches:
            problems.append(f"{name}: no application/ld+json script block found")
            continue

        title = page_title(raw)
        description = check_llms_drift.meta_description(page)

        page_checked = False
        for data in parsed:
            if in_top:
                nodes = [data]
            else:
                wanted = graph_node_type or "Service"
                nodes = find_graph_nodes(data, wanted)
                if not nodes:
                    problems.append(f"{name}: no {wanted!r} node found in @graph")
                    continue
                if len(nodes) > 1:
                    problems.append(
                        f"{name}: {len(nodes)} {wanted!r} nodes in @graph. One of them is "
                        "stale, and reading only the first is how it stays"
                    )

            page_checked = True
            for node in nodes:
                if in_top or graph_node_type:
                    if title is not None and node.get("name") != title:
                        problems.append(
                            f"{name}: JSON-LD name {node.get('name')!r} does not match "
                            f"<title> {title!r}"
                        )
                if description is not None and node.get("description") != description:
                    problems.append(
                        f"{name}: JSON-LD description {node.get('description')!r} does not "
                        f"match meta description {description!r}"
                    )
        if page_checked:
            checked += 1

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] JSON-LD name/description mirror the title/meta description "
          f"where the tree keeps them in sync: {checked} pages checked, {len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


# A hostname written as plain prose rather than inside a URL. The visible
# sentences on privacy.html, terms.html and login.html name the domain this
# way, so a rebrand that fixed every href would still ship a page telling the
# reader to go to the previous owner's site. The TLD list is deliberately
# short: it covers what this tree uses and keeps ordinary prose from matching.
BARE_HOST_RE = re.compile(
    r'(?<![A-Za-z0-9._/-])'
    r'((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:com|net|org|io|dev|gov|edu|co|ai|app))'
    r'(?![A-Za-z0-9-])'
)

# Stripped before the bare-host scan so an ordinary link is not reported as a
# plain-text mention; the URL hosts are already checked by URL_HOST_RE.
ABSOLUTE_URL_RE = re.compile(r'https?://[^\s"<>)]+')


# A node that carries an @id based on this page and a url pointing at another
# page, which is correct rather than a mistake. The table is held to the tree in
# both directions: an unlisted node whose url points elsewhere fails, and a row
# here that no longer describes a node in the tree fails too, so an excuse
# cannot outlive the thing it excused.
JSONLD_URL_ELSEWHERE = {
    # Keyed on the declared anchor rather than on the slug it currently holds,
    # because the slug is a value a rebrand replaces: writing it here would
    # leave this row describing the previous owner's node and the new owner's
    # node excused by nothing.
    ("index.html", "#" + FOUNDER["anchor_slug"]): (
        "the founder is defined once, beside the organization that declares "
        "him, and the page about him is the about page rather than the home "
        "page the node sits on"
    ),
}


def jsonld_nodes(node):
    """Yield every object inside a parsed JSON-LD document."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from jsonld_nodes(value)
    elif isinstance(node, list):
        for value in node:
            yield from jsonld_nodes(value)


def check_jsonld_identifies_its_own_page(pages: list[Path], docs_root: Path) -> bool:
    """Structured data a page defines names that page, and every reference in it resolves.

    The mirror check reads name and description, and the stated-URL check reads
    whether a URL names a file that exists. Neither asks whose page it is. Six
    service pages carry near identical structured data, and a seventh begun by
    copying one of them ships a Service node whose @id, url and breadcrumb tail
    all name the page it was copied from: the name and description are edited
    because they are visible in the copy, the identifiers are not because
    nothing renders them. Every URL in it resolves, so every check passes, and a
    crawler is told two pages are the same thing while a visitor sees two.

    The reference half is the same defect from the other side. A node that is
    only an @id points at something defined elsewhere in the tree, and renaming
    the thing it points at leaves a dangling reference that no parser complains
    about and no page shows.

    A page can carry more than one application/ld+json block only if an edit
    left a stale one behind, since the build writes at most one, so this reads
    every block on the page rather than the first: a node copied whole into a
    second block still defines an @id, and a duplicate definition or a url
    naming another page is caught the same way whichever block it is in. The
    mirror check is the one that fails on the block count itself.
    """
    problems: list[str] = []
    defined: dict[str, str] = {}
    referenced: dict[str, str] = {}
    excused: set[tuple[str, str]] = set()
    checked = 0

    for page in pages:
        raw = page.read_bytes()
        matches = list(LDJSON_RE.finditer(raw))
        if not matches:
            continue
        path = canonical_path(raw)
        if path is None:
            problems.append(
                f"{page.name}: carries structured data and no canonical link, "
                "so there is nothing to say which page the data is about"
            )
            continue
        canonical = SITE_PREFIX.rstrip("/") + path

        parsed = []
        for match in matches:
            try:
                data = json.loads(match.group(2).decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # The mirror check owns structured data that does not parse.
                continue
            parsed.append(data)

        for data in parsed:
            for node in jsonld_nodes(data):
                identifier = node.get("@id")
                if isinstance(identifier, str):
                    if set(node) - {"@id"}:
                        checked += 1
                        owner = defined.get(identifier)
                        if owner is not None:
                            problems.append(
                                f"{page.name}: defines {identifier!r}, which "
                                f"{owner} already defines, so one of the two is a "
                                "copy nobody edited and a crawler reading both "
                                "cannot tell which is meant"
                            )
                        defined[identifier] = page.name
                        base, _, fragment = identifier.partition("#")
                        if base != canonical:
                            problems.append(
                                f"{page.name}: defines {identifier!r}, which names "
                                f"{base!r} rather than {canonical!r}, the page it "
                                "is published on"
                            )
                        else:
                            url = node.get("url")
                            key = (page.name, "#" + fragment)
                            if key in JSONLD_URL_ELSEWHERE:
                                excused.add(key)
                                if isinstance(url, str) and url == canonical:
                                    problems.append(
                                        f"{page.name}: {identifier!r} is excused "
                                        "here for naming another page, and it now "
                                        "names its own, so the excuse is stale"
                                    )
                            elif isinstance(url, str) and url != canonical:
                                problems.append(
                                    f"{page.name}: {identifier!r} gives its url as "
                                    f"{url!r} rather than {canonical!r}, the page "
                                    "it is published on"
                                )
                    else:
                        referenced.setdefault(identifier, page.name)

                if node.get("@type") == "BreadcrumbList":
                    items = node.get("itemListElement")
                    if not isinstance(items, list) or not items:
                        problems.append(f"{page.name}: a BreadcrumbList lists nothing")
                        continue
                    last = items[-1]
                    item = last.get("item") if isinstance(last, dict) else None
                    if item != canonical:
                        problems.append(
                            f"{page.name}: its breadcrumb ends at {item!r} rather "
                            f"than at {canonical!r}, so the trail a search result "
                            "shows is for a different page"
                        )

    for identifier, page_name in sorted(referenced.items()):
        if identifier not in defined:
            problems.append(
                f"{page_name}: points at {identifier!r}, which nothing in this "
                "site defines, so the reference resolves to nothing"
            )
    for key in sorted(set(JSONLD_URL_ELSEWHERE) - excused):
        problems.append(
            f"{key[1]!r} on {key[0]} is excused here for naming another page "
            "and no node in the tree matches it, so this list has drifted from "
            "the pages"
        )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] structured data names the page it is "
        f"published on: {checked} defined nodes and {len(referenced)} "
        f"references checked, {len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_declared_identity(pages: list[Path], docs_root: Path) -> bool:
    """Third-party ids in the tree are the declared ones, and every external host is allowed.

    The other checks confirm the analytics tags and the contact form are
    present, never that they point at this business. A beacon token or a form
    endpoint left over from another site would ship silently, send this site's
    traffic and its inbound mail somewhere else, and pass every other check
    here. The comparison is against site.json, which is also what the build
    renders from, so the two cannot disagree without one of them being wrong.
    Each declared host must also still be found in the tree, so a vendor
    retired from every page but left in the declaration fails too.
    """
    third_party = SITE["third_party"]
    expected_ids = {
        "Cloudflare beacon token": third_party["cloudflare_beacon_token"],
        "Scarf pixel id": third_party["scarf_pixel_id"],
        "Formspree endpoint": third_party["formspree_endpoint"],
    }
    # The site's own host is allowed because it is declared in site_url, not
    # because it is listed here. Listing it would mean a rebrand left the old
    # domain allowed, and a page that kept a stale absolute URL would pass.
    own_host = SITE["site_url"].split("://", 1)[1].rstrip("/")
    allowed_hosts = set(SITE["allowed_external_hosts"]) | {own_host}
    # Prose names the domain without its www, which is the same site and not a
    # second identity, so the apex form is allowed wherever the full host is.
    allowed_bare = allowed_hosts | {own_host.split("www.", 1)[-1]}

    # A social profile lives on a host the site links to for other reasons:
    # tools.html links seven repositories under the declared GitHub account,
    # and resources.html links GitHub's own documentation. So the host being
    # allowed proves nothing about whose account it is. Requiring every URL on
    # a profile's host to sit under the declared profile is what catches a page
    # still pointing at the previous owner's account after a rebrand, which
    # every other check here would pass.
    social = {
        "LinkedIn profile": SITE["social"]["linkedin"],
        "GitHub profile": SITE["social"]["github"],
    }
    social_hosts = {
        label: url.split("://", 1)[1].split("/", 1)[0] for label, url in social.items()
    }
    found_social = {label: 0 for label in social}
    # A host is declared for a reason named in site.json; if nothing in the
    # tree still links or loads it, the declaration is the leftover.
    found_declared_hosts = {host: 0 for host in SITE["allowed_external_hosts"]}

    problems: list[str] = []
    found_ids = {label: 0 for label in expected_ids}

    # Every file a visitor or a crawler can fetch, not only the pages: the
    # sitemap, llms.txt and robots.txt all carry absolute URLs too.
    scanned = sorted(
        path
        for path in docs_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".xml", ".txt"}
    )
    for path in scanned:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{path.name}: not valid UTF-8")
            continue
        for label, value in expected_ids.items():
            found_ids[label] += text.count(value)
        for host in URL_HOST_RE.findall(text):
            if host not in allowed_hosts:
                problems.append(
                    f"{path.name}: links to {host!r}, which site.json does not allow"
                )
            elif host in found_declared_hosts:
                found_declared_hosts[host] += 1
        for url in ABSOLUTE_URL_RE.findall(text):
            url = url.rstrip('".,)')
            for label, profile in social.items():
                if not url.startswith("https://" + social_hosts[label] + "/"):
                    continue
                if url == profile:
                    found_social[label] += 1
                elif not url.startswith(profile + "/"):
                    problems.append(
                        f"{path.name}: links to {url!r}, which is not under the "
                        f"declared {label} {profile!r}"
                    )
        for host in set(BARE_HOST_RE.findall(ABSOLUTE_URL_RE.sub(" ", text))):
            if host not in allowed_bare:
                problems.append(
                    f"{path.name}: names {host!r} as text, which site.json does not allow"
                )

    # The beacon token and the pixel id ride on every page but login.html; the
    # form endpoint appears once, on contact.html. Requiring a count rather
    # than mere presence is what catches a page that kept a stale id beside
    # the current one.
    page_count = len([page for page in pages if page.name != "login.html"])
    expected_counts = {
        "Cloudflare beacon token": page_count,
        "Scarf pixel id": page_count,
        "Formspree endpoint": 1,
    }
    for label, expected in expected_counts.items():
        if found_ids[label] != expected:
            problems.append(
                f"the declared {label} appears {found_ids[label]} times, expected {expected}"
            )
    # Counted rather than merely allowed, because a profile that vanished from
    # the footer would otherwise leave this check passing on an empty set.
    for label, count in found_social.items():
        if not count:
            problems.append(
                f"the declared {label} {social[label]!r} is linked from nowhere "
                "in the tree"
            )
    # Counted rather than merely present in site.json, because a vendor
    # removed from every page still passes if only the declaration is checked.
    for host, count in found_declared_hosts.items():
        if not count:
            problems.append(
                f"site.json allows {host!r}, which nothing in the tree links to "
                "or loads"
            )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] third-party ids and external hosts match site.json: "
        f"{len(scanned)} files scanned, {len(allowed_hosts)} hosts allowed, "
        f"{len(problems)} problems"
    )
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default=None,
        help="the built site directory to verify (default: docs/ next to this script)",
    )
    args = parser.parse_args()

    docs_root = Path(args.dir).resolve() if args.dir else (SCRIPT_DIR.parent / "docs")
    if not docs_root.is_dir():
        print(f"no such directory: {docs_root}")
        return 2

    pages = html_pages(docs_root)
    if not pages:
        print(f"no .html files found under {docs_root}")
        return 2

    results = [
        check_links(pages, docs_root),
        check_pages_are_reachable(pages, docs_root),
        check_head_tags(pages),
        check_sitemap(pages, docs_root),
        check_llms_txt(docs_root),
        check_noindex_and_navigation(pages, docs_root),
        check_contact_details(pages),
        check_fragments_resolve(pages, docs_root),
        check_id_references(pages),
        check_robots_policy(pages, docs_root),
        check_privacy_statement(pages, docs_root),
        check_accessibility_statement(pages, docs_root),
        check_keyboard_operable(pages, docs_root),
        check_colour_contrast(docs_root),
        check_stated_urls_resolve(pages, docs_root),
        check_image_dimensions(pages, docs_root),
        check_contact_form(pages, docs_root),
        check_cname(docs_root),
        check_phone_is_one_number(pages, docs_root),
        check_login_tracking(pages),
        check_login_promise(docs_root),
        check_no_forbidden_claims(pages),
        check_jsonld_mirrors_title(pages),
        check_jsonld_identifies_its_own_page(pages, docs_root),
        check_declared_identity(pages, docs_root),
    ]

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} checks passed against {docs_root}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
