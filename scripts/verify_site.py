"""Check that a built Tectori site tree is internally consistent without knowing its history."""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
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
FORBIDDEN_MARKUP = ("AggregateRating", '"@type": "Review"', '"offers"')
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


def link_values(text: str):
    """Yield every URL a page points at, including each candidate in a srcset.

    A srcset is a comma separated list of candidates, each a URL followed by
    an optional width or density descriptor. Nothing scanned them until
    2026-09-12, and the home page serves its hero as a webp that way, so a
    renamed or deleted file behind it would have shipped as a broken image to
    every browser that prefers webp while all ten checks passed.
    """
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
                if not target.is_file():
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


def check_noindex_and_navigation(pages: list[Path]) -> bool:
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

    link_targets = {"404.html", "thank-you.html", "/404", "/404.html", "/thank-you"}
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for raw in link_values(text):
            value = html_lib.unescape(raw).strip().split("#", 1)[0].split("?", 1)[0]
            if value in link_targets:
                problems.append(f"{page.name}: links to {value!r}")

    ok = not problems
    print(f"[{'PASS' if ok else 'FAIL'}] only 404.html and thank-you.html are noindex, "
          f"and neither is linked from any page: {len(problems)} problems")
    for problem in problems[:20]:
        print(f"       {problem}")
    return ok


def check_sitemap(pages: list[Path], docs_root: Path) -> bool:
    """sitemap.xml lists every indexed page, by its own canonical path, and no noindex page."""
    sitemap = docs_root / "sitemap.xml"
    problems: list[str] = []
    if not sitemap.is_file():
        print("[FAIL] sitemap.xml lists every indexed page: sitemap.xml not found")
        return False

    sitemap_paths = set()
    for loc in re.findall(r"<loc>(.*?)</loc>", sitemap.read_text(encoding="utf-8")):
        if not loc.startswith(SITE_PREFIX):
            problems.append(f"sitemap.xml: <loc>{loc}</loc> is not on the site domain")
            continue
        sitemap_paths.add(loc[len(SITE_PREFIX) :] or "/")

    expected_paths = set()
    for page in pages:
        if page.name in NOINDEX_ALLOWED:
            continue
        path = canonical_path(page.read_bytes())
        if path is None:
            problems.append(f"{page.name}: no canonical href to derive its sitemap path from")
            continue
        expected_paths.add(path)

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
    """llms.txt covers the sitemap's page set and repeats each page's meta description."""
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


def check_login_tracking(pages: list[Path]) -> bool:
    """login.html carries no analytics beacon or tracking pixel; every other page carries both."""
    problems: list[str] = []
    for page in pages:
        raw = page.read_bytes()
        has_beacon = BEACON_MARKER in raw
        has_pixel = PIXEL_MARKER in raw
        if page.name == "login.html":
            if has_beacon or has_pixel:
                problems.append(f"login.html: carries {'a beacon' if has_beacon else ''}"
                                 f"{' and ' if has_beacon and has_pixel else ''}"
                                 f"{'a tracking pixel' if has_pixel else ''}")
        else:
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
    """
    problems: list[str] = []
    for page in pages:
        raw = page.read_bytes()
        for marker in FORBIDDEN_MARKUP:
            if marker.encode("utf-8") in raw:
                problems.append(f"{page.name}: contains {marker!r}")
        for marker in FORBIDDEN_TEXT:
            if marker.encode("utf-8") in raw:
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


def find_graph_node(data, node_type: str):
    """Return the first node in data["@graph"] whose "@type" equals node_type, or None."""
    if not isinstance(data, dict):
        return None
    graph = data.get("@graph")
    if not isinstance(graph, list):
        return None
    for node in graph:
        if isinstance(node, dict) and node.get("@type") == node_type:
            return node
    return None


def check_jsonld_mirrors_title(pages: list[Path]) -> bool:
    """Where the tree already mirrors it, JSON-LD name/description match the title/meta description.

    See the JSONLD_* tables above check_links for exactly which pages and
    nodes this covers, and why index.html and faq.html are intentionally
    excluded rather than checked against an invented rule.
    """
    problems: list[str] = []
    checked = 0
    for page in pages:
        name = page.name
        in_top = name in JSONLD_TOP_LEVEL_MIRROR_PAGES
        graph_node_type = JSONLD_GRAPH_MIRROR_NODE_TYPE.get(name)
        in_service = name in JSONLD_GRAPH_SERVICE_DESCRIPTION_PAGES
        if not (in_top or graph_node_type or in_service):
            if name in JSONLD_NO_MIRROR_PAGES:
                continue
            if LDJSON_RE.search(page.read_bytes()) is not None:
                problems.append(
                    f"{name}: carries JSON-LD but no rule covers it. Add it to one of the"
                    " JSONLD_ tables, or to JSONLD_NO_MIRROR_PAGES with the reason."
                )
            continue

        raw = page.read_bytes()
        match = LDJSON_RE.search(raw)
        if match is None:
            problems.append(f"{name}: no application/ld+json script block found")
            continue
        try:
            data = json.loads(match.group(2).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            problems.append(f"{name}: JSON-LD did not parse ({exc})")
            continue

        title = page_title(raw)
        description = check_llms_drift.meta_description(page)

        if in_top:
            node = data
        elif graph_node_type:
            node = find_graph_node(data, graph_node_type)
            if node is None:
                problems.append(f"{name}: no {graph_node_type!r} node found in @graph")
                continue
        else:
            node = find_graph_node(data, "Service")
            if node is None:
                problems.append(f"{name}: no 'Service' node found in @graph")
                continue

        checked += 1
        if in_top or graph_node_type:
            if title is not None and node.get("name") != title:
                problems.append(
                    f"{name}: JSON-LD name {node.get('name')!r} does not match <title> {title!r}"
                )
        if description is not None and node.get("description") != description:
            problems.append(
                f"{name}: JSON-LD description {node.get('description')!r} does not match "
                f"meta description {description!r}"
            )

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


def check_declared_identity(pages: list[Path], docs_root: Path) -> bool:
    """Third-party ids in the tree are the declared ones, and every external host is allowed.

    The other checks confirm the analytics tags and the contact form are
    present, never that they point at this business. A beacon token or a form
    endpoint left over from another site would ship silently, send this site's
    traffic and its inbound mail somewhere else, and pass every other check
    here. The comparison is against site.json, which is also what the build
    renders from, so the two cannot disagree without one of them being wrong.
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
        check_head_tags(pages),
        check_sitemap(pages, docs_root),
        check_llms_txt(docs_root),
        check_noindex_and_navigation(pages),
        check_contact_details(pages),
        check_phone_is_one_number(pages, docs_root),
        check_login_tracking(pages),
        check_no_forbidden_claims(pages),
        check_jsonld_mirrors_title(pages),
        check_declared_identity(pages, docs_root),
    ]

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} checks passed against {docs_root}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
