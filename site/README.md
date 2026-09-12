# Generated site content model

Holds the content model and chrome templates that `scripts/build_site.py`
renders into the 24 generated pages under `docs/*.html`.

The build reproduces those pages byte for byte. It does not define new
content, and it never writes into `docs/`.

## Running a build

From the repo root, using the workspace's `ai_development` venv:

```text
C:\Code\venvs\ai_development\Scripts\python.exe scripts\build_site.py --check
```

`--check` builds every page into a temporary directory, compares each one
against the matching file in `docs/`, prints the identical and differing
counts, and writes nothing outside the temp directory. Run it with no flags
to write the generated pages to the default output directory,
`C:\Code_data\tectori\reproducible\build_out\`, or pass `--out <dir>` to pick
another location. The build never writes into `docs/`.

## What the content model holds

- `content/pages.json`: one entry per generated page, holding only what is
  unique to that page: the seven head fields that vary (the leading HTML
  comment, title, meta description, og:title, og:description, og:url, and
  the canonical href), the `og:type` value, the robots value, whether a
  canonical link is present, whether the page's asset links are relative or
  root-absolute, and which raw formatting variant of the utility bar,
  header, and footer chrome it uses. Several head fields (meta description,
  robots, og:description, og:image, og:image:alt) can be written inline on
  one line or wrapped across several; `shape` on each of those fields names
  which of the finite set of wrapping variants actually found in `docs/`
  this page uses. There is no algorithm that derives the wrapping from the
  text; it is inconsistent in the source and is captured as data, not
  reformatted.
- `pages/<slug>.body.frag`: the raw bytes between `<main id="main-content">`
  and `</main>` for that page. This is the page's real content and the part
  a person is most likely to edit.
- `pages/<slug>.jsonld.frag`: the raw `<script type="application/ld+json">`
  block for the 11 pages that carry one, verbatim.
- `fragments/`: the shared chrome the pages assemble from. `skip-link.frag`
  and `tail.frag` (the analytics beacon, the Scarf pixel, and the closing
  body markup) are identical across all 24 generated pages and stored once.
  `header/`, `footer/`, and `utility-bar/` hold the raw formatting variants
  that actually exist for those blocks. The header and footer are not
  reducible to a handful of variants by content alone, because indentation
  and line-wrapping differ page to page even where the visible nav is the
  same; each stored fragment is a real, verified-byte-identical group of one
  or more pages, named for the page(s) that use it (for example
  `h-shared-no-active.frag` is the header used by the 8 pages that are not
  themselves a primary nav destination, and `h-about.frag` is about.html's
  own header, distinct from every other page's by formatting alone).

## Pages not generated

- `docs/login.html` shares no chrome with any other page (no utility bar,
  header, nav, footer, beacon, or pixel; it carries the tree's only CSP and
  its own skip-link target). It is out of scope for this generator by
  design, per THEORY.md.

All other 24 pages, including `docs/404.html` and `docs/thank-you.html`,
are generated and verified byte-identical to `docs/`.
