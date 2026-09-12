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
STATIC_DIR = os.path.join(REPO_ROOT, "site", "static")

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


def load_founder():
    """Return the founder's declared identity and the biography strings beside it."""
    path = os.path.join(SITE_DIR, "content", "founder.json")
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


FOUNDER = load_founder()


def address_parts(postal_address):
    """Return the street, locality, region and postal code of a US mailing address."""
    # The JSON-LD asks for the address in four fields and site.json declares it
    # as one string. Splitting here rather than declaring both is what stops the
    # two disagreeing: a new owner changes one value and every form of the
    # address follows. The shape assumed is a comma separated US address ending
    # in a two word state and ZIP, with any unit line folded into the street, so
    # both three part and four part addresses parse.
    parts = [part.strip() for part in postal_address.split(",")]
    if len(parts) < 3:
        raise ValueError(
            "postal_address " + repr(postal_address) + " has fewer than three "
            "comma separated parts, so the street, city and state cannot be told "
            "apart and the JSON-LD address would be wrong."
        )
    tail = parts[-1].split()
    if len(tail) != 2:
        raise ValueError(
            "the last part of postal_address is " + repr(parts[-1]) + ", which is "
            "not a state and ZIP such as 'TN 37027'."
        )
    return ", ".join(parts[:-2]), parts[-2], tail[0], tail[1]


ADDRESS_STREET, ADDRESS_LOCALITY, ADDRESS_REGION, ADDRESS_POSTAL_CODE = (
    address_parts(SITE["postal_address"])
)

# Every value below appears on all 24 generated pages, so declaring it once is
# what stops the same phone number or analytics id existing in 24 places that
# can disagree. verify_site.py checks a built tree against the same file, so a
# value that is wrong here fails a check rather than shipping quietly.
SITE_TOKENS = {
    "{{BRAND_NAME}}": SITE["brand_name"],
    "{{TAGLINE}}": SITE["tagline"],
    "{{SITE_URL}}": SITE["site_url"],
    "{{SITE_HOST}}": SITE["site_url"].split("://", 1)[1].rstrip("/"),
    "{{SITE_APEX}}": SITE["site_url"].split("://", 1)[1].rstrip("/").split("www.", 1)[-1],
    "{{FAVICON_FILENAME}}": SITE["favicon_filename"],
    "{{HERO_WEBP_FILENAME}}": SITE["hero_webp_filename"],
    "{{HERO_PNG_FILENAME}}": SITE["hero_png_filename"],
    "{{BAND_IMAGE_FILENAME}}": SITE["band_image_filename"],
    "{{PHONE_DISPLAY}}": SITE["phone_display"],
    "{{PHONE_TEL_URI}}": SITE["phone_tel_uri"],
    "{{POSTAL_ADDRESS}}": SITE["postal_address"],
    "{{ADDRESS_STREET}}": ADDRESS_STREET,
    "{{ADDRESS_LOCALITY}}": ADDRESS_LOCALITY,
    "{{ADDRESS_REGION}}": ADDRESS_REGION,
    "{{ADDRESS_POSTAL_CODE}}": ADDRESS_POSTAL_CODE,
    "{{LOGO_FILENAME}}": SITE["logo_filename"],
    "{{PHONE_SCHEMA}}": SITE["phone_schema"],
    "{{LINKEDIN_URL}}": SITE["social"]["linkedin"],
    "{{GITHUB_URL}}": SITE["social"]["github"],
    "{{CLOUDFLARE_BEACON_TOKEN}}": SITE["third_party"]["cloudflare_beacon_token"],
    "{{SCARF_PIXEL_ID}}": SITE["third_party"]["scarf_pixel_id"],
    "{{FORMSPREE_ENDPOINT}}": SITE["third_party"]["formspree_endpoint"],
    # The founder's identity recurs in structured data, in a heading, in prose
    # and in a meta description. Declaring it once is what stops a rebrand
    # replacing four of those five and shipping the fifth.
    "{{FOUNDER_NAME}}": FOUNDER["name"],
    "{{FOUNDER_GIVEN_NAME}}": FOUNDER["given_name"],
    "{{FOUNDER_JOB_TITLE}}": FOUNDER["job_title"],
    "{{FOUNDER_ANCHOR}}": FOUNDER["anchor_slug"],
}


def load_fragment(rel_path):
    with open(os.path.join(SITE_DIR, rel_path), "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    for token, value in SITE_TOKENS.items():
        text = text.replace(token, value)
    return text.encode("utf-8")


def resolve_tokens(value):
    """Return the value with every site token in its strings replaced, at any depth."""
    if isinstance(value, str):
        for token, replacement in SITE_TOKENS.items():
            value = value.replace(token, replacement)
        return value
    if isinstance(value, dict):
        return {key: resolve_tokens(item) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_tokens(item) for item in value]
    return value


def load_pages():
    path = os.path.join(SITE_DIR, "content", "pages.json")
    with open(path, "rb") as f:
        raw = f.read()
    # Substituted after parsing rather than before, so a declared value holding
    # a quote or a backslash cannot turn valid page metadata into invalid JSON.
    return resolve_tokens(json.loads(raw.decode("utf-8")))


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


# Fields whose whole purpose is to carry words onto the page. A required key
# check asks whether the key is there, which is a different question from
# whether it says anything, and an entry that carries `"description": ""` has
# every required key.
MUST_CARRY_TEXT = (
    "output", "comment", "title", "description", "robots", "og_title",
    "og_description", "og_type", "og_url", "stylesheet_href",
    "body_fragment", "contact_label", "footer_order", "slug",
)
# The four that may be absent by design: a page with no canonical, no place in
# the navigation, no structured data, or no footer link to leave out. Null is
# how the model says so. An empty string is not, because it renders as an
# empty attribute rather than as nothing at all.
MAY_BE_NULL = ("canonical", "current_nav", "jsonld_fragment", "footer_omit")


# Fields that tell a reader, or a search engine, which page this is. Two
# entries carrying one value is what copying an entry and editing half of it
# produces, and the tree that results is valid in every other way: both pages
# exist, both resolve, both are linked to. `contact_label` is deliberately
# shared, because most pages offer the same call to action, so it is not here.
UNIQUE_ACROSS_ENTRIES = (
    "title", "description", "og_title", "og_description", "body_fragment",
    "slug",
)


def output_paths(entry):
    """Return the site relative paths that name an entry's own page, or None."""
    output = entry.get("output")
    if not isinstance(output, str) or not output.endswith(".html"):
        return None
    if output == "index.html":
        return ("/",)
    # Both spellings, because the site serves extensionless URLs and one page
    # is linked with its extension.
    return ("/" + output[: -len(".html")], "/" + output)


def validate(entries):
    """Fail with the offending page and field named, rather than a KeyError mid render."""
    problems = []
    # Two entries writing one file is the failure a copied entry produces: the
    # second render overwrites the first and the page that lost simply is not
    # there. Every count still matches, because nothing counts the entries
    # against the files, and the tree is caught downstream only because two
    # pages then declare one canonical. Refusing here names the two entries
    # instead of the symptom.
    seen = {}
    for index, entry in enumerate(entries):
        output = entry.get("output")
        if output is not None:
            if output in seen:
                problems.append(
                    f"{output}: entries {seen[output]} and {index} both write "
                    "it, so one of the two pages would not exist"
                )
            seen[output] = index
    # The copied entry, caught on what the copy kept rather than on what it
    # changed. An editor duplicating a page entry changes the output, the
    # title and the canonical, because those are the fields a page is thought
    # of by; the description and the body fragment are the ones left behind.
    # Two pages then carry one description, which is a search engine picking
    # one of them and dropping the other, or one body fragment, which is the
    # same page published at two addresses. Nothing downstream can tell,
    # because each page is individually correct.
    for key in UNIQUE_ACROSS_ENTRIES:
        first: dict = {}
        for index, entry in enumerate(entries):
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                continue
            where = entry.get("output") or f"entry {index}"
            if value in first:
                problems.append(
                    f"{where}: {key} {value!r} is already used by "
                    f"{first[value]}, and this field has to tell the two "
                    "pages apart"
                )
            else:
                first[value] = where
    for index, entry in enumerate(entries):
        where = entry.get("output") or f"entry {index}"
        for key in REQUIRED_ENTRY_KEYS:
            if key not in entry:
                problems.append(f"{where}: missing required field {key!r}")
        # A field that is present and blank. The build has no default to fall
        # back on, so it renders the blank: an empty title, an empty
        # description, an empty og:title. Every check downstream counts the
        # tag and finds one, because there is one. The one place this is
        # caught today is an empty description, and only by accident: the
        # llms.txt renderer treats the empty string as a missing entry and
        # blames the page for not being in the content model, one stage away
        # from the field that is actually wrong.
        for key in MUST_CARRY_TEXT:
            if key not in entry:
                continue
            value = entry[key]
            if not isinstance(value, str) or not value.strip():
                problems.append(
                    f"{where}: {key} is {value!r}, and this field is written "
                    "onto the page, so it has to say something"
                )
        for key in MAY_BE_NULL:
            value = entry.get(key)
            if value is None:
                continue
            if not isinstance(value, str) or not value.strip():
                problems.append(
                    f"{where}: {key} is {value!r}; leave it null to mean this "
                    "page has none, rather than blank"
                )
        if "root_absolute" in entry and not isinstance(
            entry["root_absolute"], bool
        ):
            problems.append(
                f"{where}: root_absolute is {entry['root_absolute']!r} rather "
                "than true or false"
            )
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
                continue
            # And it has to name the file this entry writes. A canonical
            # copied from the entry beside it tells a search engine this page
            # is that page, which drops it from the index and credits its
            # content elsewhere, and the tree that ships looks correct: the
            # link resolves, because it points at a page that exists. The
            # build already refuses this one, but only by accident and one
            # stage later, where llms.txt cannot find a description for the
            # output path and blames the page for not being in the content
            # model. Saying it here names the field that is actually wrong.
            if value and output_paths(entry) and value not in output_paths(entry):
                problems.append(
                    f"{where}: {key} {value!r} does not name this page, which "
                    f"is written to {entry['output']!r}"
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

# Pages rendered from a fragment of their own rather than assembled from the
# shared chrome. login.html shares no header, navigation or footer with any
# other page and carries the tree's only Content-Security-Policy, so the
# content model has nothing to say about it. It still goes through the token
# substitution every other fragment goes through, which is the whole reason it
# lives here rather than being hand maintained inside the output directory:
# until 2026-09-12 it was a source file sitting in docs/, and a rebrand
# reached it only through a hand written list of substitutions kept in
# rehearse_rebrand.py that nothing checked.
VERBATIM_PAGES = (
    ("login.html", os.path.join("pages", "login.page.frag")),
)


def render_verbatim_pages():
    """Return each verbatim page's output name mapped to its rendered bytes."""
    return {name: load_fragment(source) for name, source in VERBATIM_PAGES}


def static_page_description(path, verbatim):
    """Return the meta description of a verbatim page, read from its rendered markup.

    login.html has no entry in the content model, so its own markup is the only
    source of truth for its description. Reading it here is what keeps llms.txt
    from carrying a second, silently diverging copy.
    """
    name = path.lstrip("/") or "index.html"
    if not name.endswith(".html"):
        name += ".html"
    raw = verbatim.get(name)
    if raw is None:
        raise ValueError(
            f"{name} is in public_pages.json but is neither in the content "
            "model nor a verbatim page, so llms.txt has no description for it"
        )
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


def render_llms(public_pages, entries, verbatim):
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
        description = by_path.get(path) or static_page_description(path, verbatim)
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

    verbatim = render_verbatim_pages()
    for name, data in verbatim.items():
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(data)
        written.append(name)

    # The four non-HTML files that carry the site's own domain or repeat its
    # page descriptions. Generating them is what makes the domain a one value
    # change and what stops llms.txt drifting from the pages it describes.
    public_pages = load_public_pages()
    for name, data in (
        ("CNAME", render_cname()),
        ("robots.txt", render_robots()),
        ("sitemap.xml", render_sitemap(public_pages)),
        ("llms.txt", render_llms(public_pages, entries, verbatim)),
    ):
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(data)
        written.append(name)
    return written


# Substituted rather than copied, so a filename the stylesheet carries reaches
# it from site.json like every other declared value. Anything else is copied
# byte for byte: the images are binary, and the one .svg is stored as it ships.
RENDERED_STATIC_SUFFIXES = (".css", ".js")


def copy_static_files(out_dir):
    """Render or copy every file under site/static, so the output is a deployable tree."""
    # These are source. They used to live in docs/ and be copied from there to
    # there, which made the output directory an input to its own build: a clone
    # without docs/ shipped no styling and said nothing was wrong.
    rendered, copied = [], []
    for dir_path, _dir_names, file_names in os.walk(STATIC_DIR):
        rel_dir = os.path.relpath(dir_path, STATIC_DIR)
        for file_name in sorted(file_names):
            rel = file_name if rel_dir == os.curdir else os.path.join(rel_dir, file_name)
            source = os.path.join(dir_path, file_name)
            destination = os.path.join(out_dir, rel)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            if file_name.endswith(RENDERED_STATIC_SUFFIXES):
                data = load_fragment(os.path.relpath(source, SITE_DIR))
                if b"{{" in data:
                    offset = data.index(b"{{")
                    context = data[max(0, offset - 40):offset + 40].decode(
                        "utf-8", "replace"
                    )
                    raise SystemExit(
                        f"{rel}: unresolved placeholder near: {context.strip()}"
                    )
                with open(destination, "wb") as f:
                    f.write(data)
                rendered.append(rel.replace(os.sep, "/"))
            else:
                shutil.copyfile(source, destination)
                copied.append(rel)
    return sorted(rendered), sorted(copied)


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


def orphans(written):
    """Return every file under docs/ the build did not write, newest build first."""
    # compare() walks the list of files the build produced, so a file that
    # stopped being generated is invisible to it: a build writes files and
    # never deletes them. Remove a page from pages.json or rename an image in
    # site.json and the old file stays in docs/, keeps its URL, and keeps
    # serving the previous content. Every check passed while that was true.
    expected = set(written)
    stale = []
    for dir_path, _dir_names, file_names in os.walk(DOCS_DIR):
        for file_name in sorted(file_names):
            rel = os.path.relpath(
                os.path.join(dir_path, file_name), DOCS_DIR
            ).replace(os.sep, "/")
            if rel not in expected:
                stale.append(rel)
    return sorted(stale)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="output directory for the built site")
    parser.add_argument("--check", action="store_true", help="build to a temporary directory and compare against docs/, writing nothing persistent")
    args = parser.parse_args()
    # No default. It used to be a directory on the machine this site was
    # built on, which is not a path anyone else has, so a new owner running
    # the build with no flags wrote a site into a directory they had never
    # heard of, or failed with an error about it.
    if not args.check and not args.out:
        parser.error(
            "--out is required: pass --out docs to rebuild the published tree "
            "in place, or a directory of your own to build a copy"
        )

    if args.check:
        tmp_dir = tempfile.mkdtemp(prefix="tectori-build-check-")
        try:
            written = build(tmp_dir)
            # The stylesheet and the script are rendered too, and the images
            # are copied, so comparing only the pages would leave a third of
            # the published tree unverified.
            rendered, copied = copy_static_files(tmp_dir)
            written += rendered + [name.replace(os.sep, "/") for name in copied]
            identical, differing = compare(tmp_dir, written)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"Files compared: {len(written)}, the 24 modelled pages, login.html, CNAME, robots.txt, sitemap.xml, llms.txt, and the static files")
        print(f"Identical to docs/: {identical}")
        print(f"Differing from docs/: {len(differing)}")
        for name, reason in differing:
            print(f"  DIFFERS: {name}: {reason}")
        stale = orphans(written)
        print(f"In docs/ but not written by this build: {len(stale)}")
        for name in stale:
            print(
                f"  ORPHAN: {name}: no longer generated, delete it by hand"
            )
        sys.exit(0 if not differing and not stale else 1)
    else:
        written = build(args.out)
        print(f"Wrote {len(written)} files to {args.out}, the 24 modelled pages, login.html, and CNAME, robots.txt, sitemap.xml and llms.txt")
        rendered, copied = copy_static_files(args.out)
        print(
            f"Rendered {len(rendered)} static files from site/static and copied "
            f"{len(copied)} more"
        )


if __name__ == "__main__":
    main()
