# THEORY

What a session needs to believe before it changes anything in this repo.

## Invariants

- `docs/` is generated output, not source. `scripts/build_site.py` renders every
  page from `site/`, and `CNAME`, `robots.txt`, `sitemap.xml` and `llms.txt`
  with them. A hand edit is overwritten by the next build. Rebuild with
  `--out docs` and run `scripts/check_site.py` before any deploy.
- Line endings belong to the repository, not to whoever clones it.
  `.gitattributes` pins them: blobs LF, working copies CRLF except
  `.gitignore`, `.env.example`, `CLAUDE.md`, `docs/CNAME` and the one `.svg`. A
  scripted edit that writes LF elsewhere corrupts the diff for the whole file,
  so count bare LFs after any splice.
- The values that belong to the business rather than to the site are declared
  once in `site/content/site.json`, and each reaches a page through a token,
  never as a literal. A fragment that writes one out instead is invisible to
  every check, because the built tree is correct for this owner either way;
  only `rehearse_rebrand.py` catches it, by changing all fifteen and failing on
  any built line still carrying an old one. Tokens resolve in `pages.json`
  after it is parsed rather than on its raw text, and the JSON-LD address is
  derived from the one declared string by `address_parts`.
- The brand name is the exception. It is body copy a new owner rewrites, so the
  rehearsal counts it rather than failing on it, and tokenizing it in prose
  would make the copy unreadable to whoever edits it.
- A check that confirms a declared value is present cannot see the same value
  in a second place it should not be, and that is where every defect found in
  this tree has been. When adding a check, ask what a tree would look like that
  passes it while being wrong, and whether a new owner could produce that tree.
- The site claims no clients, client counts, testimonials, ratings, prices or
  results. Copy never implies employees beyond the founder, and never frames
  the practice as one person either. The credential is Internal Security
  Assessor (ISA), never Qualified Security Assessor. `verify_site.py` reads the
  markup and the credential but cannot read prose, so the rest of this holds
  only if a writer keeps it.
- `login.html` holds the tree's only CSP and is rendered from
  `site/pages/login.page.frag` without the shared chrome, which is what
  `VERBATIM_PAGES` in the build is for. The content model has nothing to say
  about it, but it still goes through token substitution.

## Load-bearing constraints

- GitHub Pages serves both `/page` and `/page.html` with 200. Canonicals are
  extensionless and old `.html` links still resolve, so Search Console
  reporting "Alternate page with proper canonical tag" is that behavior rather
  than a defect to chase.
- The domain is one value. Nothing under `site/` spells it out but `site_url`:
  canonicals and og:url are stored site-relative, the fragments carry
  `{{SITE_URL}}`, `{{SITE_HOST}}` and `{{SITE_APEX}}`, and changing it reaches
  every file.
- The contact form is a plain HTML POST to Formspree with no JavaScript, which
  is what static hosting supports. Its `_next` field needs an absolute URL.
- `scripts/compare_render.py` proves render equality, not byte equality, and is
  sound only because every chrome container is a flex or grid box in
  `docs/styles.css`, where whitespace-only text generates no boxes, and because
  no page contains a `pre`. Break either assumption and reformatting needs a
  different proof.
- The hero uses `min-height`, so copy that wraps grows it rather than clipping.

## Decisions that look wrong

- "Audit-ready IT that scales with your ambition." is the brand tagline, not
  homepage copy. One declared value renders it as the footer line, the social
  image alt text, the homepage H1 and the homepage og:description, so changing
  it is a brand call rather than a copy edit.
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
