# THEORY

What a session needs to believe before it changes anything in this repo.

## Invariants

- `docs/` is generated output, not source. Every page except `docs/login.html`
  is rendered by `scripts/build_site.py` from `site/`, and so are `CNAME`,
  `robots.txt`, `sitemap.xml` and `llms.txt`. Edit the content model or a
  fragment and rebuild with `--out docs`; a hand edit is overwritten by the
  next build. Run `scripts/check_site.py` before any deploy.
- Line endings belong to the repository, not to whoever clones it.
  `.gitattributes` pins them: blobs are LF, working copies are CRLF except
  `.gitignore`, `.env.example`, `CLAUDE.md`, `docs/CNAME`, which GitHub Pages
  reads itself, and the one `.svg`, which the build copies rather than renders.
  A scripted edit that writes LF elsewhere corrupts the diff for the whole
  file, so confirm the bare-LF count after any splice.
- The values that belong to the business rather than to the site are declared
  once in `site/content/site.json`: brand name, tagline, domain, asset
  filenames, the three contact strings, the social URLs and the three
  third-party identifiers. The build renders from it and `verify_site.py`
  checks a built tree against it, so the site and its checks cannot be changed
  one without the other. The contact strings appear character for character
  and are never reformatted. Each of them reaches a page through a token and
  never as a literal. A fragment that writes the value out instead is the
  defect class that made "declared once" untrue until 2026-09-12, and no
  check can see it: the built tree is correct for this owner either way. Only
  `rehearse_rebrand.py` catches it, by changing all fifteen and failing on any
  built line still carrying an old one. Tokens resolve in `pages.json` too,
  after it is parsed rather than on its raw text, and the JSON-LD address is
  derived from the one declared string by `address_parts`.
- The brand name is the one declared value a rebrand is not expected to
  clear. It is body copy a new owner rewrites, so the rehearsal counts it
  rather than failing on it, and tokenizing it in prose would make the copy
  unreadable to whoever edits it.
- The site claims no clients, client counts, testimonials, ratings, prices or
  results. Copy never implies employees beyond the founder, and never frames
  the practice as one person either. The credential is Internal Security
  Assessor (ISA); Qualified Security Assessor is a different thing and is not
  Tectori's. `verify_site.py` catches the markup and the wrong credential. It
  cannot read prose, so the rest of this holds only if a writer keeps it.
- `docs/login.html` carries no tracking tags and holds the tree's only CSP.
  `docs/404.html` and `docs/thank-you.html` are the only `noindex` pages and
  stay out of `sitemap.xml`, `llms.txt` and the navigation.

## Load-bearing constraints

- GitHub Pages serves both `/page` and `/page.html` with 200. Canonicals are
  extensionless and old `.html` inbound links still resolve, so Search Console
  reporting "Alternate page with proper canonical tag" is that behavior rather
  than a defect to chase.
- The domain is one value. Nothing under `site/` spells it out but `site_url`:
  canonicals and og:url are stored as site-relative paths and the fragments
  carry `{{SITE_URL}}` and `{{SITE_HOST}}`. Changing it moves 166 occurrences.
  The one file it cannot reach is the hand-authored `docs/login.html`, which
  names the domain in a canonical and again as prose in its link home;
  `verify_site.py` fails on both rather than letting a stale domain ship.
- Each page's JSON-LD `name` and `description` repeat the visible title and
  meta description word for word, so a one-line edit to either is a two-line
  edit. A service page is the deliberate exception: its `name` and
  `serviceType` name the service rather than the page.
- The contact form is a plain HTML POST to Formspree with no JavaScript, which
  is what static hosting supports. Its `_next` field needs an absolute URL.
- `scripts/compare_render.py` proves render equality, not byte equality, and
  is sound only because every chrome container is a flex or grid box in
  `docs/styles.css`, where whitespace-only text generates no boxes, and
  because no page contains a `pre`. Break either assumption and reformatting
  needs a different proof.
- The hero uses `min-height`, so copy that wraps grows it rather than clipping.

## Decisions that look wrong

- "Audit-ready IT that scales with your ambition." is the brand tagline, not
  homepage copy. It is the footer line and the social image alt text on all 24
  content pages, plus the homepage H1 and og:description, 50 occurrences from
  one value. Changing it is a brand call, not a copy edit.
- The homepage eyebrow reads "Built to be reviewed" rather than naming
  audit-readiness, because the H1 below it already opens with "Audit-ready".
- The displayed phone number is plain characters inside a `nowrap` span. The
  `&nbsp;` and `&#8209;` entities put U+00A0 and U+2011 into text a visitor
  copies, which some dialers and CRM fields reject, and the span already
  prevents the line break they were added to fix.
- Tectori is nationally targeted and Nashville is location proof, decided on
  2026-09-11 by Jon Bowker, who owns the practice and the site. No location
  pages, no LocalBusiness schema, no Nashville-modified keyword targets, and
  the nationwide wording stands. `contact`, `about` and
  `service-fractional-leadership` name Nashville in their title and meta
  description, which is proof rather than drift. Reopen only if Search Console
  shows local query volume.
- `docs/404.html` deliberately has no canonical, and its links and assets are
  root-absolute so it renders when Pages serves it for a deep path, which is
  why reviewing it needs a local server rather than a `file://` open.

## Known soft spots

- Nothing about the analytics beacon or the Scarf pixel has been observed in a
  browser. What is verified is that the tags ship on public pages, that they
  are absent from `login.html`, and that both endpoints answer.
