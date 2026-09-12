# Generated site content model

Holds the content model and chrome templates that `scripts/build_site.py`
renders into the 24 generated pages under `docs/*.html`.

The build renders each page from one canonical chrome template plus
per-page data. It is not byte-identical to the hand-authored `docs/*.html`
(the source formatting was inconsistent from page to page), but it is
render-identical: same tags in the same order, same attributes, same text
and comments once whitespace runs are collapsed. `scripts/compare_render.py`
proves that. The build never writes into `docs/`.

## Running a build

From the repo root, using the workspace's `ai_development` venv:

```text
C:\Code\venvs\ai_development\Scripts\python.exe scripts\build_site.py --check
```

`--check` builds every page into a temporary directory and compares each one
against the matching file in `docs/` byte for byte. That comparison is
expected to report differences now that the chrome is reformatted; it exists
to prove the build is deterministic and to show exactly where formatting
diverges from the hand-authored source, not as the acceptance test. Run with
no flags to write the generated pages to the default output directory,
`C:\Code_data\tectori\reproducible\build_out\`, or pass `--out <dir>` to pick
another location.

To prove render equality against `docs/`, build to a directory, copy
`docs/login.html` into it unchanged (it is not generated), and run:

```text
C:\Code\venvs\ai_development\Scripts\python.exe scripts\compare_render.py docs\ <output-dir>
```

It exits 0 only if every one of the 25 pages present in both directories is
render-identical.

## What the content model holds

- `content/pages.json`: one entry per generated page. Each entry carries the
  head fields that vary (the leading HTML comment, title, meta description,
  robots value, og:title, og:description, og:type, og:url, og:image,
  og:image:alt, canonical href, favicon href, and stylesheet href) as plain
  values. There is exactly one canonical rendering per head field; no
  per-field wrapping variant is stored. The remaining fields are the real,
  page-specific chrome differences: `root_absolute` (true only for
  `404.html` and `thank-you.html`, whose asset and login links are
  root-absolute rather than relative), `current_nav` (which nav item, if
  any, carries `aria-current="page"`), `contact_label` (`"Contact"` except
  on `index.html` and `solutions.html`, which use `"Talk with Tectori"` on
  the desktop nav's final link), `footer_order` (`"standard"` for most
  pages, or `"about_early"` for the about/ai-governance/audit-ready-it/
  case-study/how-we-work cluster, whose footer nav genuinely orders "About"
  and "Client login" differently), and `footer_omit` (the one footer link a
  page drops for being its own self-link; six pages do this).
- `pages/<slug>.body.frag`: the raw bytes between `<main id="main-content">`
  and `</main>` for that page, copied through untouched. This is the page's
  real content and the part a person is most likely to edit.
- `pages/<slug>.jsonld.frag`: the raw `<script type="application/ld+json">`
  block for the 11 pages that carry one, verbatim.
- `fragments/`: the shared chrome, reduced to one template per piece.
  `skip-link.frag` and `tail.frag` are identical across all 24 generated
  pages and stored once, as before. `header.frag`, `footer.frag`, and
  `utility-bar.frag` are each a single canonical template with a handful of
  `{{TOKEN}}` placeholders that `build_site.py` fills in from the nav and
  footer-link tables in that script plus the per-page fields above. There is
  one header template, one footer template, and one utility-bar template,
  not 14, 10, and 4 stored formatting variants.

## Pages not generated

- `docs/login.html` shares no chrome with any other page (no utility bar,
  header, nav, footer, beacon, or pixel; it carries the tree's only CSP and
  its own skip-link target). It is out of scope for this generator by
  design, per THEORY.md.

All other 24 pages, including `docs/404.html` and `docs/thank-you.html`,
are generated and render-identical to `docs/`.
