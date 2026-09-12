# WORK_BOARD

ACTIVE THREAD: 2026-09-12 02:40. An orchestrator session is live in this
working copy and is running unattended. Do not work this tree until the
marker is cleared.

## Current state

Records, not work. Nothing here is dispatchable.

- GitHub Pages deploys this site from `main` and `docs/`. A push to `main`
  is the go-live. Allow about three minutes before checking a live URL.
- Every scored item from the 2026-09-06 scoring run and the 2026-09-08
  eight-lane run has shipped and has been verified on the live site. The
  remediation brief at
  `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-09-05_remediation.md`
  is a record now rather than a live specification. Releases 1 to 4 are done.
- The evidence behind every shipped item, closed research question and
  recorded decision through 2026-09-11 is in `BOARD_ARCHIVE_2026.md`. Read
  it to find out what was already verified or decided, never to find work.
- `scripts/check_llms_drift.py` must be run after any meta description
  change. `docs/llms.txt` copies all 24 descriptions with no generator
  behind it and drifts silently otherwise. `--fix` repairs it.
- Decided on 2026-09-11 by Jon, closing question 1. Tectori stays
  nationally targeted. No location pages, no LocalBusiness schema, no
  Nashville modified keyword targets across the site, and the nationwide
  wording on all 24 pages stands. Nashville was added to the title and meta
  description of `contact`, `about` and `service-fractional-leadership`,
  and to each of those pages' mirrored JSON-LD, because Jon asked for the
  city to appear in some keyword bearing fields. Reopen the targeting
  question only if the Search Console export shows real local query volume.

## In Progress

Jon set this session unattended on 2026-09-11 at about 23:10. Standing
instruction for the night: do not prompt him, take the recommended path, use
workers, merge and push as needed, do not stop until he stops it, and do no
work that does not score well enough to be worth doing. The approval covers
this night only and expires with it. The objective he named is to finish the
board so the site can become a reproducible product that can be sold or
hosted.

Every repo item that was on this board has shipped. The reproducibility lane
shipped on 2026-09-12 and is recorded in CHANGELOG.md, so the work below is
the productization layer he named, not leftover board work.

- **The reproducibility lane shipped and is live.** Merged at 5c5d0ca and
  pushed to `main`, which is the go-live. All 24 generated pages plus
  `login.html` were fetched from `https://www.tectori.com` afterwards and
  `scripts/compare_render.py` found all 25 render-identical to the repo tree.
  `docs/` is now the output of `scripts/build_site.py`, so a nav or footer
  change is one edit rather than 14. `scripts/check_site.py` runs all five
  checks in one command; run it before any deploy. Nothing here is
  dispatchable, it is the record of what changed under you.
- **PROD-1 shipped.** The survey at
  `C:\Code_data\tectori\reproducible\identity_constants_2026-09-12.md` is a record
  now, not a specification. Its own conclusion was that a full templating
  layer is not worth building, because the files carrying configuration are
  mostly the same files carrying the content a new owner must rewrite anyway.
  What was worth building is the narrow part: the third-party identifiers now
  live in `site/content/site.json` and `verify_site.py` checks a built tree
  against them, so a stale analytics token or form endpoint fails a check
  instead of shipping. Merged at 96bdee7 and pushed.
- **PROD-2 shipped.** `PERMISSIONS.md` is at the repo root, written to the
  framework standard. `docs/hosting.md` is gone; it was an operations note
  living inside the published site and served at a live URL.

- **PROD-3 shipped.** The rebrand rehearsal measured what a config change
  actually reaches. Its one finding worth acting on was structural: `CNAME`,
  `robots.txt`, `sitemap.xml` and `llms.txt` were copied from `docs/` byte for
  byte, so they could not follow a `site.json` change at all.
- **PROD-4 shipped.** Those four files are now generated from the content
  model, with the public page list in the new
  `site/content/public_pages.json` driving both the sitemap and llms.txt. The
  build stayed byte-identical, 28 of 28. Mutation tested by swapping the site
  URL for a fictional domain and changing one meta description: all four
  files followed and none kept the old domain.

- **PROD-5 shipped.** The domain is one value. Nothing under `site/` spells
  `www.tectori.com` out except `site_url` in `site.json`, down from 143
  occurrences. Canonicals and og:url are site relative paths the build
  prefixes; fragments carry `{{SITE_URL}}` and `{{SITE_HOST}}`; og:image, its
  alt text and the favicon href are derived rather than stored 24 times each.
  Measured against a fictional domain: 166 occurrences follow the one value.
  The only file left behind is the hand-authored `docs/login.html`, and
  `verify_site.py` now fails on it because the site's own host is derived
  from `site_url` rather than listed among the external hosts.

- **PROD-6 shipped, and its answer was mostly no.** The brand name appears
  about 430 times under `site/`, but the breakdown is 96 in `pages.json`
  titles and descriptions, 92 in body copy and 24 in JSON-LD names, all of
  which a new owner rewrites anyway. Tokenizing those would be work with no
  return. The structural remainder is small and already declared: the three
  asset filenames live in `site.json`, and the three occurrences left in
  `build_site.py` are a docstring, a default output path under the data root
  and a temp-directory prefix, none of which reach the site.
- **What the measurement did find was a defect in a checker.** The contact
  details check carried its near-miss patterns written out beside the values
  they check, so a rebrand would have left it looking for a previous owner's
  phone number. Worse, its site URL arm was matching zero occurrences and
  passing, because the full URL never appears as visible text. Both are
  fixed and mutation tested; the arm now checks two occurrences instead of
  none.

- **PROD-7 shipped, and it was proved rather than written.** `README.md`
  now carries a make-this-site-yours runbook: six ordered steps ending in
  the rebuild and the checks. Rather than describe the steps and trust
  them, this thread executed them on a clone at
  `C:\Code_data\tectori\reproducible\northvale\`, rebranding the site to a
  fictional business. The clone passes all ten checks and holds no trace of
  the previous owner. Two defects surfaced that no amount of reading would
  have: `--out docs` crashed on copying a file onto itself, so there was no
  supported way to rebuild the published tree in place, and the identity
  check ignored hostnames written as prose, which is how `login.html` names
  the domain in its link home. Both are fixed and the second is mutation
  tested on the clone.

The board holds no dispatchable item and no unshipped repo work. What is
left is the part a session cannot decide alone: whether this becomes a
product someone buys, a template repository, or a hosted service, which
changes what gets built next. Until Jon says which, the useful work is
hardening what exists.

- **The `THEORY.md` audit is done.** Every claim in it was checked against
  the tree. One was wrong, the line-ending invariant, which named
  `docs/CNAME` as the only non-CRLF file when three at the repo root are
  pure LF too. Two were stale. It is 88 lines now rather than 98, still
  over the framework's 60-line guidance, and the rest is load-bearing.

The next step this thread is taking is PROD-8, turning tonight's rebrand
rehearsal into a script anything can run. The rehearsal proved the product
is reproducible once, by hand, on 2026-09-12, and that proof decays with
the next change to the build. A `scripts/rehearse_rebrand.py` that clones
to the data root, rewrites every declared value to a fixture business,
rebuilds and runs the checks turns a claim a buyer has to take on trust
into one the repo re-proves on demand. It found two real defects the first
time it was run by hand, which is the argument for running it again.

## Owner-Only Tasks

- **EXPORT-GSC, get the Search Console export.** Verify the property at
  search.google.com/search-console for `www.tectori.com`, export Performance
  (queries, pages, 16 months) and Links, and drop both in
  `C:\Code_data\tectori\stats\` with the export date in the filename. Bing
  Webmaster export the same way if the property exists. This needs Jon's Google
  account and blocks the volume half of KEYWORD-BASELINE plus the profile half
  of BACKLINK-CHANNELS.
  `score: kind=ops gain=3/10/30 p=0.8 hours=0.25/0.5/1 rev=two-way conf=assessed id=export-gsc`
  `return: likelihood 1 in 1 per request, 1 occasion, so about once now, from the four board items that name it as their blocker; impact without it KEYWORD-BASELINE, BACKLINK-CHANNELS, MEASURE-BASELINE and the vendor's 0-ranked-keywords claim all stall or produce estimates Jon has already refused, 3 to 30 h of research that cannot be graded above opinion; evidence the four items below that cite it, the brief Step 5 item 1, and C:\Code_data\tectori\stats\ read on 2026-09-06 holding no export`
  - worker: none, owner task, 0.25/0.5/1 h
  - Jon steps:
    1. Open `C:\Code_data\tectori\stats\EXPORT_SPEC_2026-09-06.md`.
    2. Export Google Search Console Performance queries, Performance pages and
       Links for `www.tectori.com`.
    3. Save the files in `C:\Code_data\tectori\stats\` with the export date in
       each filename.
    4. Export the same Bing Webmaster files if the Bing property exists.

- **ANALYTICS-CHECK, confirm the beacon and pixel in a browser.** Open a public
  page and `login.html` with the network tab showing. Confirm the Cloudflare
  beacon and Scarf pixel fire on the public page and neither fires on
  `login.html`. Fetching deployed HTML already proved the tags ship and both
  endpoints answer, so this is a browser confirmation, not a suspected problem.
  `score: kind=ops gain=0.5/2/8 p=0.4 hours=0.15/0.25/0.5 rev=two-way conf=assessed id=analytics-check`
  `return: likelihood 1 in 1 per check, 1 occasion this year, so about once, from the single unverified claim left in the 2026-08-23 analytics deploy; impact if the beacon does not fire, every number MEASURE-BASELINE reports is empty and nobody knows why, 0.5 to 8 h of chasing a measurement gap that is really a deploy gap; evidence the 2026-08-23 deploy at 1f6b705, the deployed HTML fetch confirming both tags on 22 pages, and login.html confirmed carrying neither`
  - worker: none, owner task, 0.25/0.25/0.5 h

- **EVIDENCE-PILOT, run the Evidence Readiness Baseline with the first buyer.**
  Use one defined review boundary and test whether the scope, evidence inventory,
  findings and prioritized action list are useful without a maturity score. The
  brief is `C:\Code_data\tectori\EVIDENCE_READINESS_BASELINE_OFFER_2026-08-30.md`.
  Blocked on a qualified buyer.
  `score: kind=feature gain=20/80/300 p=0.2 hours=2/6/16 rev=two-way conf=opinion id=evidence-pilot flags=external,blocked`
  `return: likelihood 1 in 5 that a qualified buyer appears and takes the pilot this year, 1 occasion this year, so about once in five years at the current inbound rate, estimated because the site has produced no recorded inquiry; impact the offer stays unpriced and untested, so the first real buyer becomes the experiment, worth 20 to 300 h across a mispriced or misscoped first engagement; evidence the 2026-08-30 offer brief, the site changes verified live on 2026-08-31, and no inquiry recorded in the Cloudflare or Scarf data since 2026-08-23`
  - worker: none, owner task, 6/12/24 h

## Post-Lane Queue

No pending items. Every scored lane feature has shipped.

## Questions for Jon

2. **Google Business Profile category.** Lane 2 could not verify whether
   `Computer Security Service`, `Computer Consultant`, or `Business Management
   Consultant` are categories Google currently offers. In the Google interface,
   choose only from categories Google actually offers.
3. **Google Business Profile video verification.** Lane 2 included the video
   rule from a lower-confidence source and marked home-business specifics
   unresolved. Follow whatever verification method Google offers in the GBP
   interface.
4. **LinkedIn personal headline.** Lane 8 did not write a paste-ready personal
   profile headline because the source marked the current headline as
   `CONFIRM`. Default it would take if confirmed: append `PCI, HIPAA, SOC 2,
   HITRUST, ISO 42001, NIST AI RMF` to the existing headline.
5. The five resumes outside this repo say Internal PCI Qualified Security
  Assessor. PCI SSC issues Internal Security Assessor (ISA) to employees and
  reserves Qualified Security Assessor for external assessor companies. The
  site says ISA. The resumes should be corrected to match, which is work in
  another folder, not in this repo.
6. The executive resume claims a client outcome delivered through an MSP
  partner, a 140,000 email index cut 80 percent and 37 percent in license
  savings. The site claims no client results anywhere and case-study.html
  says so explicitly. Jon chose on 2026-08-23 to leave it off the site.
  Recorded so a later thread does not rediscover it as a gap.
