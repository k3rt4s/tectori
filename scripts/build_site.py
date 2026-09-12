#!/usr/bin/env python3
"""Render the Tectori site's generated pages from site/ templates and content model into an output directory."""

import argparse
import json
import os
import re
import shutil
import sys
import tempfile

CRLF = chr(13) + chr(10)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SITE_DIR = os.path.join(REPO_ROOT, "site")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
DEFAULT_OUT = r"C:\Code_data\tectori\reproducible\build_out"

# Desktop nav order, shared by every page. The trailing "Contact" link is
# handled separately below because its label and href-class differ from the
# other items.
DESKTOP_NAV_ITEMS = [
    ("services", "/services", "Services"),
    ("solutions", "/solutions", "Solutions"),
    ("tools", "/tools", "Free tools"),
    ("audit_ready_it", "/audit-ready-it", "Audit-ready IT"),
    ("ai_governance", "/ai-governance", "AI governance"),
    ("case_study", "/case-study", "Case study"),
    ("about", "/about", "About"),
    ("how_we_work", "/how-we-work", "How we work"),
]

# Mobile nav order, shared by every page. "faq" is only reachable from the
# mobile menu. "login" and the trailing "contact" are handled separately
# because the login href depends on root_absolute.
MOBILE_NAV_ITEMS = [
    ("home", "/", "Home"),
    ("services", "/services", "Services"),
    ("solutions", "/solutions", "Solutions"),
    ("tools", "/tools", "Free tools"),
    ("audit_ready_it", "/audit-ready-it", "Audit-ready IT"),
    ("ai_governance", "/ai-governance", "AI governance"),
    ("case_study", "/case-study", "Case study"),
    ("about", "/about", "About"),
    ("how_we_work", "/how-we-work", "How we work"),
    ("faq", "/faq", "FAQ"),
]

# Footer link label/href table, keyed the same way as current_nav/footer_omit.
FOOTER_LINKS = {
    "home": ("/", "Home"),
    "services": ("/services", "Services"),
    "solutions": ("/solutions", "Solutions"),
    "tools": ("/tools", "Free tools"),
    "resources": ("/resources", "Resources"),
    "audit_ready_it": ("/audit-ready-it", "Audit-ready IT"),
    "ai_governance": ("/ai-governance", "AI governance"),
    "case_study": ("/case-study", "Case study"),
    "about": ("/about", "About"),
    "how_we_work": ("/how-we-work", "How we work"),
    "faq": ("/faq", "FAQ"),
    "contact": ("/contact", "Contact"),
    "login": (None, "Client login"),  # href depends on root_absolute
    "trust": ("/trust", "Trust"),
    "privacy": ("/privacy", "Privacy"),
    "terms": ("/terms", "Terms"),
    "accessibility": ("/accessibility", "Accessibility"),
}

# The two real footer link orderings used across the site. "standard" is the
# order used by most pages. "about_early" is used by the about/ai-governance/
# audit-ready-it/case-study/how-we-work cluster, where "about" sits right
# after "resources" and "login" sits right after the topic links instead of
# after "contact". Per page, footer_omit drops that page's own self-link.
FOOTER_ORDER_STANDARD = [
    "home", "services", "solutions", "tools", "resources",
    "audit_ready_it", "ai_governance", "case_study", "about", "how_we_work",
    "faq", "contact", "login", "trust", "privacy", "terms", "accessibility",
]
FOOTER_ORDER_ABOUT_EARLY = [
    "home", "services", "solutions", "tools", "resources",
    "about", "audit_ready_it", "ai_governance", "case_study", "how_we_work",
    "login", "faq", "contact", "trust", "privacy", "terms", "accessibility",
]
FOOTER_ORDERS = {
    "standard": FOOTER_ORDER_STANDARD,
    "about_early": FOOTER_ORDER_ABOUT_EARLY,
}


def load_site_config():
    path = os.path.join(SITE_DIR, "content", "site.json")
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


SITE = load_site_config()

# Every value below appears on all 24 generated pages, so declaring it once is
# what stops the same phone number or analytics id existing in 24 places that
# can disagree. verify_site.py checks a built tree against the same file, so a
# value that is wrong here fails a check rather than shipping quietly.
SITE_TOKENS = {
    "{{BRAND_NAME}}": SITE["brand_name"],
    "{{TAGLINE}}": SITE["tagline"],
    "{{SITE_URL}}": SITE["site_url"],
    "{{SITE_HOST}}": SITE["site_url"].split("://", 1)[1].rstrip("/"),
    "{{PHONE_DISPLAY}}": SITE["phone_display"],
    "{{PHONE_TEL_URI}}": SITE["phone_tel_uri"],
    "{{POSTAL_ADDRESS}}": SITE["postal_address"],
    "{{LINKEDIN_URL}}": SITE["social"]["linkedin"],
    "{{GITHUB_URL}}": SITE["social"]["github"],
    "{{CLOUDFLARE_BEACON_TOKEN}}": SITE["third_party"]["cloudflare_beacon_token"],
    "{{SCARF_PIXEL_ID}}": SITE["third_party"]["scarf_pixel_id"],
}


def load_fragment(rel_path):
    with open(os.path.join(SITE_DIR, rel_path), "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    for token, value in SITE_TOKENS.items():
        text = text.replace(token, value)
    return text.encode("utf-8")


def load_pages():
    path = os.path.join(SITE_DIR, "content", "pages.json")
    with open(path, "rb") as f:
        raw = f.read()
    return json.loads(raw.decode("utf-8"))


def attr(value):
    """Return a content-model string safe to place inside a double quoted HTML attribute."""
    # Deliberately not the standard library helper, whose quoted mode also
    # rewrites the apostrophe. Six page titles carry one, and rewriting it would
    # change the shipped bytes of pages that are otherwise unchanged. Inside a
    # double quoted attribute only these three characters can end the value or
    # begin a new markup construct.
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace('"', "&quot;")
    )


def text(value):
    """Return a content-model string safe to place in HTML text content."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_head_field_inline(name_or_property, key, value):
    return ("    <meta " + key + '="' + name_or_property + '" content="' + attr(value) + '">' + CRLF).encode("utf-8")


def render_meta_description(value):
    return (
        "    <meta" + CRLF
        + '      name="description"' + CRLF
        + '      content="' + attr(value) + '"' + CRLF
        + "    >" + CRLF
    ).encode("utf-8")


def nav_link(href, label, current_nav, key, extra_class=None):
    attrs = ""
    if extra_class:
        attrs += ' class="' + extra_class + '"'
    attrs += ' href="' + href + '"'
    if current_nav == key:
        attrs += ' aria-current="page"'
    return "<a" + attrs + ">" + label + "</a>"


def render_desktop_nav(entry, indent):
    lines = []
    for key, href, label in DESKTOP_NAV_ITEMS:
        lines.append(indent + nav_link(href, label, entry["current_nav"], key))
    contact_label = entry["contact_label"]
    lines.append(indent + nav_link("/contact", contact_label, entry["current_nav"], "contact", extra_class="nav-contact"))
    return CRLF.join(lines)


def render_mobile_nav(entry, indent):
    login_href = "/login.html" if entry["root_absolute"] else "login.html"
    lines = []
    for key, href, label in MOBILE_NAV_ITEMS:
        lines.append(indent + nav_link(href, label, entry["current_nav"], key))
    lines.append(indent + nav_link(login_href, "Client login", entry["current_nav"], "login"))
    lines.append(indent + nav_link("/contact", "Contact", entry["current_nav"], "contact"))
    return CRLF.join(lines)


def render_header(entry):
    tmpl = load_fragment("fragments/header.frag").decode("utf-8")
    brand_current = ' aria-current="page"' if entry["current_nav"] == "home" else ""
    logo_src = ("/assets/" if entry["root_absolute"] else "assets/") + SITE["logo_filename"]
    tmpl = tmpl.replace("{{BRAND_CURRENT}}", brand_current)
    tmpl = tmpl.replace("{{LOGO_SRC}}", logo_src)
    tmpl = tmpl.replace("{{DESKTOP_NAV_ITEMS}}", render_desktop_nav(entry, "        "))
    tmpl = tmpl.replace("{{MOBILE_NAV_ITEMS}}", render_mobile_nav(entry, "          "))
    return tmpl.encode("utf-8")


def render_footer(entry):
    tmpl = load_fragment("fragments/footer.frag").decode("utf-8")
    logo_src = ("/assets/" if entry["root_absolute"] else "assets/") + SITE["logo_filename"]
    login_href = "/login.html" if entry["root_absolute"] else "login.html"
    order = FOOTER_ORDERS[entry["footer_order"]]
    omit = entry["footer_omit"]
    lines = []
    for key in order:
        if key == omit:
            continue
        href, label = FOOTER_LINKS[key]
        if key == "login":
            href = login_href
        lines.append("        " + "<a href=\"" + href + "\">" + label + "</a>")
    tmpl = tmpl.replace("{{LOGO_SRC}}", logo_src)
    tmpl = tmpl.replace("{{FOOTER_LINK_ITEMS}}", CRLF.join(lines))
    return tmpl.encode("utf-8")


def render_utility_bar(entry):
    tmpl = load_fragment("fragments/utility-bar.frag").decode("utf-8")
    login_href = "/login.html" if entry["root_absolute"] else "login.html"
    tmpl = tmpl.replace("{{LOGIN_HREF}}", login_href)
    return tmpl.encode("utf-8")


def site_absolute(path):
    """Return a site relative path as the absolute URL the head tags need."""
    return SITE["site_url"] + path


def favicon_href(entry):
    """Return the favicon href, which differs only in whether it is root absolute."""
    prefix = "/assets/" if entry["root_absolute"] else "assets/"
    return prefix + SITE["favicon_filename"]


def social_image_url():
    """Return the og:image URL, which is the same card on all 24 pages."""
    return SITE["site_url"] + "/assets/" + SITE["social_image_filename"]


def social_image_alt():
    """Return the og:image alt text, which reads as the brand and its tagline."""
    # Stored as a derivation rather than 24 copies of one string, for the same
    # reason the URL above is: a rebrand should not have to find it.
    return SITE["brand_name"] + ", " + SITE["tagline"]


def render_page(entry, cache):
    def cached_fragment(name):
        if name not in cache:
            cache[name] = load_fragment(os.path.join("fragments", name + ".frag"))
        return cache[name]

    out = []
    out.append(b"<!DOCTYPE html>" + CRLF.encode())
    out.append(("<!-- " + entry["comment"] + " -->" + CRLF).encode("utf-8"))
    out.append(('<html lang="en">' + CRLF).encode("utf-8"))
    out.append(("  <head>" + CRLF).encode("utf-8"))
    out.append(('    <meta charset="utf-8">' + CRLF).encode("utf-8"))
    out.append(('    <meta name="viewport" content="width=device-width, initial-scale=1">' + CRLF).encode("utf-8"))
    out.append(("    <title>" + text(entry["title"]) + "</title>" + CRLF).encode("utf-8"))
    out.append(render_meta_description(entry["description"]))
    out.append(render_head_field_inline("robots", "name", entry["robots"]))
    out.append(render_head_field_inline("og:title", "property", entry["og_title"]))
    out.append(render_head_field_inline("og:description", "property", entry["og_description"]))
    out.append(render_head_field_inline("og:type", "property", entry["og_type"]))
    out.append(render_head_field_inline("og:url", "property", site_absolute(entry["og_url"])))
    out.append(render_head_field_inline("og:image", "property", social_image_url()))
    out.append(('    <meta property="og:image:width" content="1200">' + CRLF).encode("utf-8"))
    out.append(('    <meta property="og:image:height" content="630">' + CRLF).encode("utf-8"))
    out.append(render_head_field_inline("og:image:alt", "property", social_image_alt()))
    out.append(('    <meta property="og:site_name" content="' + attr(SITE["brand_name"]) + '">' + CRLF).encode("utf-8"))
    out.append(('    <meta name="twitter:card" content="summary_large_image">' + CRLF).encode("utf-8"))
    if entry["canonical"]:
        canonical = site_absolute(entry["canonical"])
        out.append(('    <link rel="canonical" href="' + attr(canonical) + '">' + CRLF).encode("utf-8"))
    out.append(('    <link rel="icon" href="' + attr(favicon_href(entry)) + '">' + CRLF).encode("utf-8"))
    out.append(('    <link rel="stylesheet" href="' + attr(entry["stylesheet_href"]) + '">' + CRLF).encode("utf-8"))
    if entry["jsonld_fragment"]:
        out.append(load_fragment(entry["jsonld_fragment"]))
    out.append(("  </head>" + CRLF).encode("utf-8"))
    out.append(("  <body>" + CRLF).encode("utf-8"))
    out.append(cached_fragment("skip-link"))
    out.append(render_utility_bar(entry))
    out.append(render_header(entry))
    out.append(CRLF.encode())
    out.append(('    <main id="main-content">' + CRLF).encode("utf-8"))
    out.append(load_fragment(entry["body_fragment"]))
    out.append(("    </main>" + CRLF).encode("utf-8"))
    out.append(CRLF.encode())
    out.append(render_footer(entry))
    out.append(cached_fragment("tail"))
    page = b"".join(out)
    # A mistyped placeholder would otherwise render as literal braces on a live
    # page and pass every other check, since nothing else in the tree uses this
    # syntax. Checking the finished page catches both the site tokens filled in
    # load_fragment and the chrome placeholders filled after it.
    if b"{{" in page:
        offset = page.index(b"{{")
        context = page[max(0, offset - 40):offset + 40].decode("utf-8", "replace")
        raise ValueError(
            f"{entry['output']}: unresolved placeholder near: {context.strip()}"
        )
    return page


REQUIRED_ENTRY_KEYS = (
    "output", "comment", "title", "description", "robots", "og_title",
    "og_description", "og_type", "og_url",
    "canonical", "stylesheet_href", "jsonld_fragment",
    "body_fragment", "current_nav", "contact_label", "footer_order",
    "footer_omit", "root_absolute",
)


def validate(entries):
    """Fail with the offending page and field named, rather than a KeyError mid render."""
    problems = []
    for index, entry in enumerate(entries):
        where = entry.get("output") or f"entry {index}"
        for key in REQUIRED_ENTRY_KEYS:
            if key not in entry:
                problems.append(f"{where}: missing required field {key!r}")
        order = entry.get("footer_order")
        if order is not None and order not in FOOTER_ORDERS:
            problems.append(f"{where}: footer_order {order!r} is not one of {sorted(FOOTER_ORDERS)}")
        omit = entry.get("footer_omit")
        if omit and omit not in dict(FOOTER_LINKS):
            problems.append(f"{where}: footer_omit {omit!r} is not a footer link key")
        # canonical and og:url are stored site relative so the domain lives in
        # site.json alone. A value that still carries a scheme would render as
        # a doubled URL, which is the one way this storage form goes wrong.
        for key in ("canonical", "og_url"):
            value = entry.get(key)
            if value and not value.startswith("/"):
                problems.append(
                    f"{where}: {key} {value!r} must be a site relative path "
                    f"beginning with /, not an absolute URL"
                )
    if problems:
        print("The content model is not valid, so nothing was built:")
        for problem in problems:
            print(f"  {problem}")
        sys.exit(2)


def load_public_pages():
    """Return the ordered public page list that sitemap.xml and llms.txt are both built from."""
    path = os.path.join(SITE_DIR, "content", "public_pages.json")
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


STATIC_PAGE_DESCRIPTION = re.compile(
    rb'name="description"\s*content="(.*?)"', re.DOTALL
)


def static_page_description(path):
    """Return the meta description of a page the generator does not render, read from docs/.

    login.html is hand authored and has no entry in the content model, so its
    own markup is the only source of truth for its description. Reading it here
    is what keeps llms.txt from carrying a second, silently diverging copy.
    """
    name = path.lstrip("/") or "index.html"
    if not name.endswith(".html"):
        name += ".html"
    with open(os.path.join(DOCS_DIR, name), "rb") as f:
        raw = f.read()
    match = STATIC_PAGE_DESCRIPTION.search(raw)
    if match is None:
        raise ValueError(f"{name}: no meta description for its llms.txt line")
    return " ".join(match.group(1).decode("utf-8").split())


CANONICAL_ORIGIN = re.compile(r"^https?://[^/]+")


def descriptions_by_path(entries):
    """Map each generated page's site-relative canonical path to its meta description."""
    # Strip whatever origin the canonical carries rather than only the
    # configured one. The canonicals in pages.json still spell the domain out,
    # so matching on site_url alone would silently produce an empty map the
    # moment site_url changed, and llms.txt would lose every description it
    # should have kept.
    by_path = {}
    for entry in entries:
        canonical = entry.get("canonical")
        if not canonical:
            continue
        path = CANONICAL_ORIGIN.sub("", canonical)
        by_path[path or "/"] = entry["description"]
    return by_path


def render_cname():
    """Return the CNAME file: the site URL's hostname alone."""
    # One bare LF, not CRLF. GitHub Pages reads this file itself, and it is the
    # one file in the tree that is not CRLF, which is a good reason to generate
    # it rather than leave it to a hand edit that would normalize it.
    host = SITE["site_url"].split("://", 1)[1].rstrip("/")
    return (host + chr(10)).encode("utf-8")


def render_robots():
    """Return robots.txt with the brand name and the sitemap URL filled in."""
    return load_fragment(os.path.join("fragments", "robots.frag"))


def render_sitemap(public_pages):
    """Return sitemap.xml listing every public page in the declared order."""
    brand = SITE["brand_name"]
    site_url = SITE["site_url"]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<!-- {brand}'s sitemap lists canonical public pages and their latest significant update. -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in public_pages:
        lines.append("  <url>")
        lines.append(f'    <loc>{site_url}{page["path"]}</loc>')
        lines.append(f'    <lastmod>{page["lastmod"]}</lastmod>')
        lines.append("  </url>")
    lines.append("</urlset>")
    return (CRLF.join(lines) + CRLF).encode("utf-8")


def render_llms(public_pages, entries):
    """Return llms.txt, one line per public page carrying that page's own meta description."""
    # This file was maintained by hand and drifted silently, which is what
    # scripts/check_llms_drift.py exists to catch. Building it from the same
    # descriptions the pages are rendered from removes the drift rather than
    # reporting it.
    by_path = descriptions_by_path(entries)
    if "/" not in by_path:
        raise ValueError(
            "llms.txt: no page canonical resolves to /, so the file would have "
            "no site description; check the canonical on the home page entry"
        )
    lines = [
        f"# {SITE['brand_name']}",
        "",
        by_path["/"],
        "",
        "## Pages",
    ]
    for page in public_pages:
        path = page["path"]
        description = by_path.get(path) or static_page_description(path)
        lines.append(f"- {path}: {description}")
    return (CRLF.join(lines) + CRLF).encode("utf-8")


def build(out_dir):
    entries = load_pages()
    validate(entries)
    cache = {}
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for entry in entries:
        data = render_page(entry, cache)
        out_path = os.path.join(out_dir, entry["output"])
        with open(out_path, "wb") as f:
            f.write(data)
        written.append(entry["output"])

    # The four non-HTML files that carry the site's own domain or repeat its
    # page descriptions. Generating them is what makes the domain a one value
    # change and what stops llms.txt drifting from the pages it describes.
    public_pages = load_public_pages()
    for name, data in (
        ("CNAME", render_cname()),
        ("robots.txt", render_robots()),
        ("sitemap.xml", render_sitemap(public_pages)),
        ("llms.txt", render_llms(public_pages, entries)),
    ):
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(data)
        written.append(name)
    return written


def copy_static_files(out_dir, written):
    """Copy every file in docs/ the generator does not produce, so the output is a deployable tree."""
    # Listing the exceptions instead of the inclusions is what keeps this from
    # decaying. A stylesheet, an image or a font added to docs/ later is
    # carried across without anyone remembering to name it here. login.html is
    # among them: it shares no chrome with any page and carries the only CSP, so
    # the generator does not model it, and an output tree missing it is not a
    # site.
    generated = set(written)
    copied = []
    for dir_path, _dir_names, file_names in os.walk(DOCS_DIR):
        rel_dir = os.path.relpath(dir_path, DOCS_DIR)
        for file_name in file_names:
            rel = file_name if rel_dir == os.curdir else os.path.join(rel_dir, file_name)
            if rel.replace(os.sep, '/') in generated:
                continue
            source = os.path.join(dir_path, file_name)
            destination = os.path.join(out_dir, rel)
            # Building with --out docs is how the published tree is updated in
            # place, and every static file is then its own destination. Copying
            # a file onto itself raises rather than doing nothing, so skip it.
            if os.path.exists(destination) and os.path.samefile(source, destination):
                continue
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copyfile(source, destination)
            copied.append(rel)
    return sorted(copied)


def compare(out_dir, written):
    identical = 0
    differing = []
    for name in written:
        gen_path = os.path.join(out_dir, name)
        doc_path = os.path.join(DOCS_DIR, name)
        with open(gen_path, "rb") as f:
            gen = f.read()
        if not os.path.isfile(doc_path):
            differing.append((name, "no such file in docs/"))
            continue
        with open(doc_path, "rb") as f:
            doc = f.read()
        if gen == doc:
            identical += 1
        else:
            n = min(len(gen), len(doc))
            pos = next((i for i in range(n) if gen[i] != doc[i]), n)
            differing.append((name, f"first differing byte at offset {pos} (generated {len(gen)} bytes, docs {len(doc)} bytes)"))
    return identical, differing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT, help="output directory for generated pages")
    parser.add_argument("--check", action="store_true", help="build to a temporary directory and compare against docs/, writing nothing persistent")
    args = parser.parse_args()

    if args.check:
        tmp_dir = tempfile.mkdtemp(prefix="tectori-build-check-")
        try:
            written = build(tmp_dir)
            identical, differing = compare(tmp_dir, written)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"Pages generated: {len(written)}")
        print(f"Identical to docs/: {identical}")
        print(f"Differing from docs/: {len(differing)}")
        for name, reason in differing:
            print(f"  DIFFERS: {name}: {reason}")
        sys.exit(0 if not differing else 1)
    else:
        written = build(args.out)
        print(f"Wrote {len(written)} pages to {args.out}")
        copied = copy_static_files(args.out, written)
        print(f"Copied {len(copied)} files docs/ carries that the generator does not build")


if __name__ == "__main__":
    main()
