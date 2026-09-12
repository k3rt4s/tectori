#!/usr/bin/env python3
"""Render the Tectori site's generated pages from site/ templates and content model into an output directory."""

import argparse
import json
import os
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


def load_fragment(rel_path):
    with open(os.path.join(SITE_DIR, rel_path), "rb") as f:
        return f.read()


def load_pages():
    path = os.path.join(SITE_DIR, "content", "pages.json")
    with open(path, "rb") as f:
        raw = f.read()
    return json.loads(raw.decode("utf-8"))


def render_head_field_inline(name_or_property, key, value):
    return ("    <meta " + key + '="' + name_or_property + '" content="' + value + '">' + CRLF).encode("utf-8")


def render_meta_description(value):
    return (
        "    <meta" + CRLF
        + '      name="description"' + CRLF
        + '      content="' + value + '"' + CRLF
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
    logo_src = "/assets/tectori-logo.png" if entry["root_absolute"] else "assets/tectori-logo.png"
    tmpl = tmpl.replace("{{BRAND_CURRENT}}", brand_current)
    tmpl = tmpl.replace("{{LOGO_SRC}}", logo_src)
    tmpl = tmpl.replace("{{DESKTOP_NAV_ITEMS}}", render_desktop_nav(entry, "        "))
    tmpl = tmpl.replace("{{MOBILE_NAV_ITEMS}}", render_mobile_nav(entry, "          "))
    return tmpl.encode("utf-8")


def render_footer(entry):
    tmpl = load_fragment("fragments/footer.frag").decode("utf-8")
    logo_src = "/assets/tectori-logo.png" if entry["root_absolute"] else "assets/tectori-logo.png"
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
    out.append(("    <title>" + entry["title"] + "</title>" + CRLF).encode("utf-8"))
    out.append(render_meta_description(entry["description"]))
    out.append(render_head_field_inline("robots", "name", entry["robots"]))
    out.append(render_head_field_inline("og:title", "property", entry["og_title"]))
    out.append(render_head_field_inline("og:description", "property", entry["og_description"]))
    out.append(render_head_field_inline("og:type", "property", entry["og_type"]))
    out.append(render_head_field_inline("og:url", "property", entry["og_url"]))
    out.append(render_head_field_inline("og:image", "property", entry["og_image"]))
    out.append(('    <meta property="og:image:width" content="1200">' + CRLF).encode("utf-8"))
    out.append(('    <meta property="og:image:height" content="630">' + CRLF).encode("utf-8"))
    out.append(render_head_field_inline("og:image:alt", "property", entry["og_image_alt"]))
    out.append(('    <meta property="og:site_name" content="Tectori">' + CRLF).encode("utf-8"))
    out.append(('    <meta name="twitter:card" content="summary_large_image">' + CRLF).encode("utf-8"))
    if entry["canonical"]:
        out.append(('    <link rel="canonical" href="' + entry["canonical"] + '">' + CRLF).encode("utf-8"))
    out.append(('    <link rel="icon" href="' + entry["favicon_href"] + '">' + CRLF).encode("utf-8"))
    out.append(('    <link rel="stylesheet" href="' + entry["stylesheet_href"] + '">' + CRLF).encode("utf-8"))
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
    return b"".join(out)


def build(out_dir):
    entries = load_pages()
    cache = {}
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for entry in entries:
        data = render_page(entry, cache)
        out_path = os.path.join(out_dir, entry["output"])
        with open(out_path, "wb") as f:
            f.write(data)
        written.append(entry["output"])
    return written


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


if __name__ == "__main__":
    main()
