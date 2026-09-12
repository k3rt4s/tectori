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

SHAPE_TEMPLATES = {
    "meta_description": {
        "inline": '    <meta name="description" content="{v}">' + CRLF,
        "wrap_attached": '    <meta' + CRLF + '      name="description"' + CRLF + '      content="{v}">' + CRLF,
        "wrap_ownline": '    <meta' + CRLF + '      name="description"' + CRLF + '      content="{v}"' + CRLF + '    >' + CRLF,
    },
    "robots": {
        "inline": '    <meta name="robots" content="{v}">' + CRLF,
        "wrap_attached": '    <meta' + CRLF + '      name="robots"' + CRLF + '      content="{v}">' + CRLF,
    },
    "og_description": {
        "inline": '    <meta property="og:description" content="{v}">' + CRLF,
        "wrap_attached": '    <meta' + CRLF + '      property="og:description"' + CRLF + '      content="{v}">' + CRLF,
    },
    "og_image": {
        "inline": '    <meta property="og:image" content="{v}">' + CRLF,
        "wrap_attached": '    <meta' + CRLF + '      property="og:image"' + CRLF + '      content="{v}">' + CRLF,
    },
    "og_image_alt": {
        "inline": '    <meta property="og:image:alt" content="{v}">' + CRLF,
        "wrap_attached": '    <meta' + CRLF + '      property="og:image:alt"' + CRLF + '      content="{v}">' + CRLF,
    },
}


def render_field(field, spec):
    tmpl = SHAPE_TEMPLATES[field][spec["shape"]]
    return tmpl.format(v=spec["value"]).encode("utf-8")


def load_fragment(rel_path):
    with open(os.path.join(SITE_DIR, rel_path), "rb") as f:
        return f.read()


def load_pages():
    path = os.path.join(SITE_DIR, "content", "pages.json")
    with open(path, "rb") as f:
        raw = f.read()
    return json.loads(raw.decode("utf-8"))


def render_page(entry, cache):
    def cached_fragment(kind, name):
        key = (kind, name)
        if key not in cache:
            cache[key] = load_fragment(os.path.join("fragments", kind, name + ".frag"))
        return cache[key]

    out = []
    out.append(b"<!DOCTYPE html>" + CRLF.encode())
    out.append(("<!-- " + entry["comment"] + " -->" + CRLF).encode("utf-8"))
    out.append(('<html lang="en">' + CRLF).encode("utf-8"))
    out.append(("  <head>" + CRLF).encode("utf-8"))
    out.append(('    <meta charset="utf-8">' + CRLF).encode("utf-8"))
    out.append(('    <meta name="viewport" content="width=device-width, initial-scale=1">' + CRLF).encode("utf-8"))
    out.append(("    <title>" + entry["title"] + "</title>" + CRLF).encode("utf-8"))
    out.append(render_field("meta_description", entry["description"]))
    out.append(render_field("robots", entry["robots"]))
    out.append(('    <meta property="og:title" content="' + entry["og_title"] + '">' + CRLF).encode("utf-8"))
    out.append(render_field("og_description", entry["og_description"]))
    out.append(('    <meta property="og:type" content="' + entry["og_type"] + '">' + CRLF).encode("utf-8"))
    out.append(('    <meta property="og:url" content="' + entry["og_url"] + '">' + CRLF).encode("utf-8"))
    out.append(render_field("og_image", entry["og_image"]))
    out.append(('    <meta property="og:image:width" content="1200">' + CRLF).encode("utf-8"))
    out.append(('    <meta property="og:image:height" content="630">' + CRLF).encode("utf-8"))
    out.append(render_field("og_image_alt", entry["og_image_alt"]))
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
    out.append(cached_fragment("chrome-single", "skip-link"))
    out.append(cached_fragment("utility-bar", entry["utility_bar_variant"]))
    out.append(cached_fragment("header", entry["header_variant"]))
    if entry["blank_line_before_main"]:
        out.append(CRLF.encode())
    out.append(('    <main id="main-content">' + CRLF).encode("utf-8"))
    out.append(load_fragment(entry["body_fragment"]))
    out.append(("    </main>" + CRLF).encode("utf-8"))
    if entry["blank_line_before_footer"]:
        out.append(CRLF.encode())
    out.append(cached_fragment("footer", entry["footer_variant"]))
    out.append(cached_fragment("chrome-single", "tail"))
    return b"".join(out)


def load_fragment_single(name):
    return load_fragment(os.path.join("fragments", name + ".frag"))


def build(out_dir):
    entries = load_pages()
    cache = {}
    # chrome-single fragments (skip-link, tail) live directly under fragments/, not a subdirectory
    cache[("chrome-single", "skip-link")] = load_fragment_single("skip-link")
    cache[("chrome-single", "tail")] = load_fragment_single("tail")
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
