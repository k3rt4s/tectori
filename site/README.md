# Generated site content model

Holds the content model and chrome templates that `scripts/build_site.py`
renders into the 24 generated pages under `docs/*.html`.

Each page is rendered from one canonical chrome template plus per-page data.
`docs/` holds the output of that build, so the generator reproduces the live
tree byte for byte. It does not define new content, and it never writes into
`docs/`.

## Running a build

From the repo root, using the workspace's `ai_development` venv:

```text
C:\Code\venvs\ai_development\Scripts\python.exe scripts\build_site.py --check
```

`--check` builds every page into a temporary directory, compares each one
against the matching file in `docs/` byte for byte, deletes the temporary
tree, and exits non-zero on any difference. Since `docs/` now holds generator
output, that comparison is expected to pass, and it is the everyday gate: any
content change should show up in `docs/` only after the generator puts it
there.

Run with no flags to write the site to the default output directory,
`C:\Code_data\tectori\reproducible\build_out\`, or pass `--out <dir>` to pick
another location. Either way the output is a complete deployable tree: the 24
generated pages plus every other file `docs/` carries, copied unchanged.

## Which gate applies when

Two gates exist because two kinds of change need two different questions
answered.

- **Everyday content and data changes** use `--check`. Editing a title, a
  meta description, a body fragment, or a nav entry should reproduce `docs/`
  byte for byte once `docs/` is rebuilt, so any unexplained byte difference
  is a defect.
- **Deliberate reformatting of the templates** uses `scripts/compare_render.py`.
  Reindenting a chrome template or rewrapping an attribute changes bytes on
  purpose, and byte equality would report a failure that is not one. Render
  equality is the right question there. It compares tag order, attributes
  as an order-insensitive mapping, comments, and whitespace-collapsed text
  across every page present in both directories, and exits non-zero on any
  difference or on any page present in one directory and not the other.
  Build with `--out` first. The output tree already contains `login.html`,
  so nothing needs copying by hand.

```text
C:\Code\venvs\ai_development\Scripts\python.exe `
  scripts\compare_render.py docs\ <output-dir>
```

Render equality is sound for this site only because every chrome container
is a flex or grid box in `styles.css`, where whitespace-only text between
children generates no boxes, and because no page contains a `<pre>` element.
A change that breaks either of those assumptions invalidates the gate.

A meta description change now flows into `docs/llms.txt` on the next build,
so `scripts\check_llms_drift.py` no longer has to be run by hand.
Run `scripts\verify_site.py`, which checks the built tree as a site
rather than as a set of files. `scripts\check_site.py` runs the build, the
drift check, the verifier and both gates in one command.

## What the content model holds

- `content/site.json`: the values that belong to the business rather than to
  the site's structure. Brand name, tagline, site URL, logo filename, the
  three contact strings, the Cloudflare beacon token, the Scarf pixel id,
  the Formspree endpoint, the social URLs, and the allowlist of external
  hosts the tree may reference, each with the reason it is there.
  `build_site.py` renders the chrome from these and `verify_site.py` checks
  a built tree against them, so a stale value fails a check instead of
  shipping quietly. Changing one here changes every page it appears on.
- `content/public_pages.json`: the ordered list of public pages, each with
  the date it last changed meaningfully. `sitemap.xml` and `llms.txt` are
  both built from this one list, in this order, so the two files cannot
  disagree about which pages the site has. A new page is added here once.
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
- `fragments/robots.frag`: the robots.txt body, with the brand name and the
  sitemap URL left as tokens so both follow `site.json`.
- `fragments/`: the shared chrome, reduced to one template per piece.
  `skip-link.frag` and `tail.frag` are identical across all 24 generated
  pages and stored once, as before. `header.frag`, `footer.frag`, and
  `utility-bar.frag` are each a single canonical template with a handful of
  `{{TOKEN}}` placeholders that `build_site.py` fills in from `site.json`,
  from the nav and footer-link tables in that script, and from the per-page
  fields above. A placeholder left unresolved fails the build. There is
  one header template, one footer template, and one utility-bar template,
  not 14, 10, and 4 stored formatting variants.

## Pages not generated

- `docs/login.html` shares no chrome with any other page (no utility bar,
  header, nav, footer, beacon, or pixel; it carries the tree's only CSP and
  its own skip-link target). It is out of scope for this generator by
  design, per THEORY.md. A build copies it into the output unchanged, so
  the output is still a complete site.

All other 24 pages, including `docs/404.html` and `docs/thank-you.html`,
are generated and byte-identical to `docs/`. So are the four non-page
files that carry the domain or repeat the page descriptions: `CNAME`,
`robots.txt`, `sitemap.xml` and `llms.txt`. `CNAME` is the one file the
build writes with a bare LF, because GitHub Pages reads it directly.
Everything else in `docs/`, the stylesheet, the script, the images and
`login.html`, is copied across unchanged.
