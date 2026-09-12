# Tectori Website

Tectori is the source project for the public business website at
[www.tectori.com](https://www.tectori.com/).

The site presents Tectori's IT and security consulting services and is built as
a static website for low-cost hosting.

## Quick Start

Run `python scripts/serve_docs.py --port 8000` from the repository root, then open `http://127.0.0.1:8000/` to review the site locally. Internal links use extensionless paths, so do not review by opening the HTML file directly.

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
- `scripts/check_llms_drift.py` compares every `docs/llms.txt` page
  description, and the file's summary paragraph, against the corresponding
  page's meta description. `llms.txt` copies them with no generator behind
  it and drifts silently. `--fix` rewrites the drifted lines from the pages.
- `scripts/verify_site.py` checks that a built site tree is internally
  consistent: internal links resolve, head tags are singular, the sitemap
  and `llms.txt` cover the same pages with matching descriptions, only the
  two documented pages are noindex, the contact details are character for
  character, the analytics tags are on every page except `login.html`, and
  no ratings markup or Qualified Security Assessor claim appears. It takes
  `--dir` so it can verify a generated build as well as `docs/`, and exits
  non-zero on any failure so it can gate a deploy.
- `SEARCH_SETUP.md` covers Google, Bing, and search-grounded assistant setup.
- `THEORY.md` holds the working mental model: the invariants, the
  constraints the site is bent around, and the changes that look like fixes
  but are not. Read it before changing anything.
- `WORK_BOARD.md` tracks active project work.
- `CHANGELOG.md` records completed changes.

## Configuration

No local secrets or runtime settings are required. Hosting setup notes live in
`docs/hosting.md`.
