# THEORY

What a session needs to believe before it changes anything in this repo.

## Invariants

- `docs/*.html` is generated output, not source. Every page except
  `docs/login.html` is rendered by `scripts/build_site.py` from `site/`. Edit
  the content model or a fragment and rebuild; a hand edit to `docs/` is
  overwritten by the next build and is caught by `scripts/check_site.py`,
  which is the one command to run before any deploy.
- Every file uses CRLF except `docs/CNAME`, which ends in one bare LF
  because GitHub Pages reads it directly. A scripted edit that writes LF
  anywhere else corrupts the diff for the whole file. After any splice,
  confirm the bare-LF count is zero.
- Contact details appear character for character and are never reformatted:
  `(615) 829-6802`, `https://www.tectori.com`, and
  `201 Summit View Dr, Suite 305, Brentwood, TN 37027`. Those three strings,
  the brand name, the tagline, the social URLs and the three third-party
  identifiers are declared once in `site/content/site.json`. The build renders
  the chrome from it and `scripts/verify_site.py` checks a built tree against
  it, so neither the site nor its checks can be changed alone.
- The site claims no clients, client counts, testimonials, ratings, prices or
  results, and carries no `Review`, `AggregateRating` or `offers` markup.
- Copy never implies employees beyond the founder, and never frames the
  practice as one person either.
- The credential is Internal Security Assessor (ISA). Qualified Security
  Assessor is a different thing and is not Tectori's.
- `docs/login.html` carries no tracking tags and holds the tree's only CSP.
- The only `noindex` pages are `docs/404.html` and `docs/thank-you.html`, and
  both stay out of `docs/sitemap.xml`, `docs/llms.txt` and the navigation.

## Load-bearing constraints

- GitHub Pages serves both `/page` and `/page.html` with 200. Canonicals are
  extensionless, and old `.html` inbound links still resolve. Search Console
  reporting "Alternate page with proper canonical tag" is that behavior, not a
  defect to chase.
- `docs/CNAME`, `docs/robots.txt`, `docs/sitemap.xml` and `docs/llms.txt` are
  generated too, from `site/content/site.json` and
  `site/content/public_pages.json`. That ended the silent drift
  `scripts/check_llms_drift.py` was written to catch; the drift check still
  runs but can no longer fail, since byte equality already covers the file.
- The domain is one value. Nothing under `site/` spells it out except
  `site_url` in `site.json`: canonicals and og:url are stored as site
  relative paths, and the fragments carry `{{SITE_URL}}` and `{{SITE_HOST}}`.
  Changing that one value moves 166 occurrences across the built tree. The
  one file it cannot reach is `docs/login.html`, which is hand authored, and
  `verify_site.py` now fails on it rather than letting the stale domain ship:
  the site's own host is allowed because it is derived from `site_url`, not
  because it is listed among the external hosts.
- The contact form is a plain HTML POST to Formspree with no JavaScript, which
  is what the static hosting supports. Its `_next` field needs an absolute URL.
- Each page's JSON-LD `name` and `description` repeat the visible title and
  meta description word for word. They change together or the page starts
  describing itself two ways, which is the defect SEO-17 was merged to fix.
  A one line edit to a title or a description is therefore a two line edit.
  The exception is a service page, whose JSON-LD `name` and `serviceType`
  name the service rather than the page.
- Render equality, not byte equality, is what `scripts/compare_render.py`
  proves, and it is sound here only because every chrome container is a flex
  or grid box in `docs/styles.css`, where whitespace-only text between
  children generates no boxes, and because no page contains a `pre` element.
  A change that breaks either assumption invalidates that gate, so reformatting
  must then be proved some other way.
- The hero uses `min-height`, not `height`, so copy that wraps to another line
  grows the hero rather than being clipped.

## Decisions that look wrong

- "Audit-ready IT that scales with your ambition." is the brand tagline, not
  homepage copy. It is the footer line and the social image alt text on all
  24 content pages, 48 occurrences in the built tree but one value in
  `site.json`, and the homepage adds two more in its H1 and `og:description`.
  Changing it is a brand call, not a copy edit.
- The homepage eyebrow reads "Built to be reviewed" rather than naming
  audit-readiness, because the H1 directly below it already opens with
  "Audit-ready".
- The displayed phone number is plain characters inside a `nowrap` span rather
  than `&nbsp;` and `&#8209;`. Those entities put U+00A0 and U+2011 into text a
  visitor copies, which some dialers and CRM fields reject. Do not reintroduce
  them as a line-break fix; the span already prevents the break.
- Tectori is nationally targeted and Nashville is location proof, decided by
  Jon on 2026-09-11. There are no location pages, no LocalBusiness schema and
  no Nashville modified keyword targets, and the nationwide wording on all 24
  pages stands. Three pages are a deliberate exception: `contact`, `about`
  and `service-fractional-leadership` name Nashville in their title and meta
  description. That is not drift toward local targeting. Reopen the question
  only if the Search Console export shows real local query volume.
- `docs/404.html` deliberately has no canonical, and its links and assets are
  root-absolute so it renders when Pages serves it for a deep path. That is why
  it needs a local server rather than a `file://` open to review.

## Known soft spots

- Nothing about the analytics beacon or the Scarf pixel has been observed in a
  browser. What is verified is that the tags ship on public pages, that they
  are absent from `login.html`, and that both endpoints answer.
