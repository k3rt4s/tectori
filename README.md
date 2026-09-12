# Tectori Website

Tectori is the source project for the public business website at
[www.tectori.com](https://www.tectori.com/).

The site presents Tectori's IT and security consulting services and is built as
a static website for low-cost hosting.

Read this before editing anything. `docs/` is the last build's output, not
the source, and it has no exceptions: every file in it is either generated
or copied from elsewhere. You edit `site/`, then rebuild. A hand edit under
`docs/` is overwritten by the next build with no warning at the time you
make it.

## Quick Start

Run `python scripts/serve_docs.py --port 8000` from the repository root,
then open `http://127.0.0.1:8000/` to review the site locally. Internal
links use extensionless paths, so do not review by opening the HTML file
directly.

## Layout

- `docs/` contains the public website files served by GitHub Pages.
- `docs/assets/` contains website-owned image assets.
- `docs/solutions.html` presents the incubated Tectori solution portfolio.
- `docs/service-*.html` are the six individual service line pages, one per
  anchored section on `docs/services.html`, which remains the hub.
- `docs/resources.html` indexes the site reference material and defines the
  terms used across it. `docs/trust.html` states how the practice operates,
  how client material is handled, and how to report a problem.
- `docs/contact.html` and `docs/faq.html` provide direct conversion and
  answer-oriented search pages.
- `docs/login.html` is a static portal preview with no authentication, storage,
  or network submission.
- `docs/404.html` is the not found page GitHub Pages serves for any address
  that does not exist. It is noindex and stays out of `docs/sitemap.xml` and the
  navigation. Its links and assets are root-absolute so the page still renders
  when Pages serves it for a deep path, which means it needs a server rather
  than a `file://` open to review locally.
- `docs/thank-you.html` is the page the contact form redirects to after a
  successful submission. It is noindex and stays out of `docs/sitemap.xml`,
  `docs/llms.txt`, and the navigation, and is reached only through the form.
- `.github/workflows/verify.yml` runs those checks on a clean Linux machine
  for every push and pull request, and adds one they cannot make on their
  own: that `docs/` is byte identical to what the build produces, not merely
  render identical to it. A hand edit to whitespace, an entity or a line
  ending renders the same and fails there. Nothing in it gates the deploy.
  GitHub Pages publishes from `main` and `docs/` whether or not it passes,
  so it reports rather than blocks.
- `scripts/check_site.py` runs every check below in one command and prints a
  pass or fail line for each, exiting non-zero if any failed. It is the entry
  point to use before a deploy; the individual scripts are there for when one
  of them fails and you want its output alone. `--full` adds the rebrand
  rehearsal described below, which is off the default path because it clones
  the tree outside the repository and takes about a minute. `--quiet` prints
  the summary
  without each check's own output.
- `site/` holds the content model and chrome templates, and
  `scripts/build_site.py` renders them into the 24 generated pages under
  `docs/`, along with `CNAME`, `robots.txt`, `sitemap.xml` and `llms.txt`.
  `docs/` is that build's output, so `--check` reproduces it byte for
  byte. Run with `--out <dir>` to write a complete deployable tree, pages plus
  every other file `docs/` carries. `site/README.md` explains the content model
  and which gate applies to which kind of change.
- `scripts/compare_render.py` compares two directories of pages as rendered
  documents rather than as bytes: tag order, attributes as an
  order-insensitive mapping, comments, and whitespace-collapsed text. Use it
  when a change reformats the templates on purpose and byte equality would
  report a failure that is not one.
- `scripts/check_llms_drift.py` compares every `docs/llms.txt` page
  description, and the file's summary paragraph, against the corresponding
  page's meta description. It predates the generator and is kept as a
  second opinion; now that `llms.txt` is built from those same
  descriptions, byte equality already covers it.
- `scripts/verify_site.py` checks that a built site tree is internally
  consistent: internal links resolve, head tags are singular, the sitemap
  and `llms.txt` cover the same pages with matching descriptions, only the
  two documented pages are noindex, the contact details are character for
  character, the analytics tags are on every page except `login.html`, and
  no ratings markup or Qualified Security Assessor claim appears. Its tenth
  check compares the third-party identifiers and every external host in the
  tree against `site/content/site.json`, so a stale analytics token or form
  endpoint fails here rather than shipping. It takes
  `--dir` so it can verify a generated build as well as `docs/`, and exits
  non-zero on any failure so it can gate a deploy.
- `scripts/rehearse_rebrand.py` proves the site is reproducible instead of
  claiming it. It clones the tree to the data root, applies the three
  mechanical steps of the runbook below against a fixture business, rebuilds,
  runs every check, and then reports how much of the original identity
  survived. It fails if the old domain appears even once, because the domain
  is derived from one declared value everywhere. It counts rather than fails
  on the old brand name, because most of those are body copy a new owner
  rewrites. Nothing in the repository is modified by a run.
- `PERMISSIONS.md` lists everything the site needs to build, deploy, and
  serve: runtime, filesystem paths, every outbound host, the operator
  accounts, the DNS records, and a from-scratch deploy runbook. It replaced
  `docs/hosting.md`, which was an operations note published as part of the
  live site.
- `SEARCH_SETUP.md` covers Google, Bing, and search-grounded assistant setup.
- `THEORY.md` holds the working mental model: the invariants, the
  constraints the site is bent around, and the changes that look like fixes
  but are not. Read it before changing anything.
- `WORK_BOARD.md` tracks active project work.
- `CHANGELOG.md` records completed changes.

## Configuration

No local secrets or runtime settings are required. The values that belong to
the business rather than to the site's structure, the brand name, the tagline,
the contact strings, the domain, the logo, social card and favicon filenames,
and the three third-party identifiers, are declared once in
`site/content/site.json`. The domain in particular is a single value:
changing `site_url` moves 166 occurrences across a rebuilt tree, and there is
no file it cannot reach. `PERMISSIONS.md` covers hosting, DNS, and the
from-scratch deploy.

## Making this site yours

In order. Steps 1 to 3 are mechanical and the checks catch a mistake in any
of them. Step 4 is the real work and no tool can do it. These steps were
rehearsed against a clone on 2026-09-12: a fictional business replacing every
declared value reaches a tree that passes all eleven checks and names the
previous owner nowhere.

1. Rewrite every value in `site/content/site.json`: the brand name, tagline,
   site URL, the three asset filenames, the three contact strings, the
   Cloudflare beacon token, the Scarf pixel id, the Formspree endpoint, the
   social URLs, and the external host allowlist. Delete an entry from
   `third_party` only by also removing what emits it, or a check will fail
   on the count.
2. Replace the images in `docs/assets/` and name them to match step 1. The
   logo, social card and favicon are the three the build reads from
   `site.json`. The band image and both hero files are referenced by name
   from `site/pages/index.body.frag` and `docs/styles.css` instead, so those
   two files need editing if you rename them. The hero is two files, a
   `.webp` offered through a `srcset` and a `.png` behind it, and a browser
   that prefers webp never loads the png.
3. Rewrite the brand name in `site/pages/login.page.frag`, which carries it
   five times as prose. Nothing else on that page needs touching: the
   filenames and both forms of the domain come from `site.json` like
   everywhere else. Until 2026-09-12 this page was hand authored inside
   `docs/` and this step was a list of substitutions to make by hand. The
   page still holds the only Content-Security-Policy in the tree.
4. Rewrite the copy. It lives in `site/pages/<slug>.body.frag` for the visible
   text, `site/pages/<slug>.jsonld.frag` for the structured data, and the
   title, description and og fields in `site/content/pages.json`. On nine
   pages the JSON-LD `name` and `description` repeat the title and meta
   description word for word and a check enforces it, so those change
   together: `about`, `contact`, `services` and the six `service-*` pages.
   The service pages are a partial exception, with their JSON-LD naming the
   service rather than the page. `index` and `faq` are deliberately
   unchecked. Adding or removing a page means editing
   `site/content/public_pages.json` too, and deleting a removed page's file
   from `docs/` by hand, because a rebuild writes files and never deletes
   them.
5. Rebuild in place with `python scripts/build_site.py --out docs`, then run
   `python scripts/check_site.py`. All five must pass before the tree is
   worth deploying. One of the five is `scripts/verify_site.py`, which is
   eleven checks of its own that read the built tree as a site rather than as
   a set of files, and it is the one that catches a value you missed. To
   see steps 1 to 3 and this one run end to end before you do them
   yourself, run `python scripts/check_site.py --full`, which adds the
   rehearsal as a sixth check.
6. Follow the runbook in `PERMISSIONS.md` for the repository, the Pages
   settings, the DNS records and the accounts behind the three third-party
   services.

What the checks cannot tell you is whether the copy is true of your business.
Several constraints in `THEORY.md` are commitments this site made about what
it will not claim, and `verify_site.py` enforces some of them literally. Read
that file before you decide which ones you are keeping.
