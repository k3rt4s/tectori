# BOARD_ARCHIVE_2026

This file is a record, not instructions. Nothing in it is a next action. It
holds board sections archived verbatim from `WORK_BOARD.md` so the evidence
behind a decision stays readable after the board is trimmed. Read it to find
out what was already verified, decided or shipped, never to find work.

## Archived 2026-09-06: shipped work, closed research and decision records

Archived from the In Progress section on 2026-09-06 during the board scoring
run. The remediation brief at
`C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-09-05_remediation.md` remains
the live specification for Releases 1 to 4; its scored index carries the
unshipped features.

- YOUR NEXT ACTION. Read the orchestrator brief at
  `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-09-05_remediation.md` before
  anything else. It replaces every brief before it. You are the build
  thread: four releases on their own branches, every decision already
  taken by Jon on 2026-09-05 and listed there. Its Step 0 is your first
  move: write the thread marker, then ask Jon through the interactive
  question tool whether to start Release 1. Jon's standing instruction:
  do what the SEO audit recommends, then do the research; privacy is not
  a constraint here; the framework governs how the work is engineered.

- ISKPRO audit remediation, opened 2026-09-05. Decisions taken by Jon on
  2026-09-05 through the question tool, recorded in full in the brief:
  address is 201 Summit View Dr, Suite 305, Brentwood, TN 37027 (verified
  on Google Maps 2026-09-05); coworking without signage, reception and
  presence, so the profile is service-area with the address hidden; full
  address on contact page, every footer and Organization PostalAddress,
  utility bar unchanged; copy limited to meta description lengths; all
  five items I recommended declining are built after Jon read the
  reasons (home links to /, social profiles, contact form via a form
  service, Facebook pixel, extensionless URLs), with the house rules and
  privacy page amended; solution-ops-toolkit.png deleted. Releases:
  1 feature/seo1-business-address (SEO-01, 03, 07, 08, 09, plus the GBP
  checklist and link-earning documents); 2 feature/seo2-page-weight-and-
  entity (SEO-04, 05, 06); 3 feature/seo3-contact-form-pixel-social
  (SEO-13, 15, 16, blocked on Jon's endpoint, pixel ID and profile URLs);
  4 feature/seo4-extensionless-urls (SEO-14). Verified, no action: SPF
  exists; analytics exists (Cloudflare beacon); title, canonical, robots,
  sitemap, HTTPS, OG and X cards all present.
  Then Step 5, the in-house SEO research program for this site only.
  Backlog: startup and vCISO positioning divergence (3.3); PageSpeed API
  key for field data; Search Console export and call screenshots not
  landed.

- SEO call research, opened 2026-09-03. Source: the 46 minute inbound sales
  call from Digital Guider at `C:\Code_Data\workspace\website_call_20260903\`.
  The transcript is single-speaker merged, so the words are reliable and the
  attribution is not. Jon settled three things on 2026-09-03 before dispatch:
  no Google Business Profile was ever created, so the 2026-08-22 note under
  the discovery item was wrong; the keyword research maps both buyer sets,
  the regulated organizations the site is written for and the Series A to B
  startups and growth SMBs described on the call, and reports where they
  diverge; no vendor quote has arrived. Jon also has screenshots of the
  vendor's screen share, landing in `...\website_call_20260903\screenshots\`.
  Rule for every item: a vendor claim is a hypothesis until measured here.
  Vendor claims and their status:
  - 14.5 second page load: confirmed for the homepage on slow mobile only
    (3.1b); image weight, not code.
  - 9 percent duplicate content: reproduced at 8.6 percent body-only (3.2);
    it is the designed hub summaries, not a duplicate page.
  - 0 ranked keywords, 0 organic traffic, 41 spam backlinks: need Jon's
    Search Console export, which is not in `stats\` yet. Unconfirmed.
  - Authority score 2 of 100: a vendor tool's metric, not a Google one.
  - Search volume over 3000 a month: no keyword named. Unusable as stated.
  - 100 mile local radius: the vendor's line after Jon said entire US twice.
    Not a decision.
  Research dispatches, none changes a file in docs/, reports land in
  `C:\Code_data\tectori\seo_research_2026-09-03\`:
  - 3.1 page speed: report in. Assets and headers measured; the keyless
    PageSpeed API refused every call (daily quota 0), so no load time yet.
    3.1b report in at 3.1b_lighthouse_local.md: Lighthouse 13.4.1, 24 runs.
    Homepage on simulated slow mobile: median LCP 14.0 s, one run 16.9 s,
    so the vendor's 14.5 s is real for that one page and profile. Cause is
    3.6 MB page weight, hero PNG 1.67 MB plus six 640x640 portfolio PNGs
    shown small. Every other page 2.4 to 3.4 s mobile; desktop all under
    2.6 s, scores 87 to 100. Field data still needs a PageSpeed API key.
  - 3.2 duplicate content: report in. Body-only overlap 5.2 percent at
    8-word shingles, 8.6 at 5-word (the vendor's 9); 19.7 with chrome. All
    of it is the hub restating its six service pages by design. Redirects
    and canonicals correct; / and /index.html both 200, canonical only.
  - 3.3 keywords: report in at 3.3_keywords.md. Both buyer sets mapped;
    divergence is exam language, the compliance page's FFIEC/HIPAA lead,
    the absent vCISO term, and the Nashville modifier. No volume numbers.
  - 3.4 backlinks: report in at 3.4_backlinks.md. Nothing measurable
    without the Search Console Links export. Medium, Quora and Tumblr all
    nofollow outbound links, the same class the vendor called spam. Honest
    link sources ranked; most are Jon's to earn, not the site's to add.
  - 3.5 reputation and reviews: report in at 3.5_reputation_reviews.md.
    Review and rating markup ban confirmed by Google's self-serving rule
    and the FTC's 2024 rule. Person node could carry credentials, award,
    alumniOf and sameAs from facts already on about.html; spec change.
    Google's own text bounds a service-area profile near 2 hours' drive.
  - 3.6 business address and Google Business Profile: report in at
    3.6_address_gbp.md. Options only. A profile needs a real address even
    when hidden; service areas are named places near a 2 hour drive, no
    radius control, 20 max; virtual offices and PO boxes ineligible.
    LocalBusiness markup requires a complete address, so Organization
    with areaServed United States stays the honest node.
  - Every policy quote in 3.4 and 3.5 is snippet-sourced: the WebFetch
    allowlist blocks google.com, ftc.gov and web.archive.org for workers
    and orchestrator alike (3.4_policy_check.md). A shell fetch of Wayback
    snapshots does work: 3.7_policy_quotes.md holds all ten pages from
    dated snapshots (2025-12-30 to 2026-08-11), verbatim. The 2 hour
    service-area guidance, the virtual-office and PO box bar, the
    LocalBusiness address requirement and the link-spam text are all
    primary now. Research complete; decisions are with Jon.
  Jon's decisions, 2026-09-03, through the question tool:
  - Google Business Profile: create it now. New fact: Tectori has a
    business address. This comes first, together with putting the address
    on the website. The research assumed no address; the profile options
    in 3.6 are re-read against the quotes in 3.7 once the address type is
    known (office operated from, staffed coworking, or mailbox).
  - Digital Guider: not hiring. Jon wants workers to research and replicate
    what such a vendor does, for this site only, never as a service.
    Backlog item, after the address work.
  - In-house remediation approved for one spec, after the address work:
    image weight, Person JSON-LD from about.html facts (spec amendment
    first), internal home links to the canonical /.
  - Positioning: backlog the startup and vCISO divergence from 3.3; no
    public copy change now.
  Research closed 2026-09-03, logged in CHANGELOG.md. Open work, in order:
  1. Address questions to Jon (brief Step 1). Unanswered.
  2. Google Business Profile checklist for Jon (brief Step 2). Jon creates
     the profile; record here only when he says it is verified.
  3. Address on the site, branch feature/seo1-business-address (Step 3).
  4. Image weight, Person JSON-LD, home links, branch
     feature/seo2-page-weight-and-entity (Step 4).
  5. Backlog items (Step 5), placed once Jon says where the backlog lives.
  Not landed: Jon's Search Console export and his call screenshots.
  Added 2026-09-04: an ISKPRO automated audit of the homepage (grade B, 18
  recommendations, performance graded A, one backlink seen) archived at
  `seo_research_2026-09-03\Audit_for_Tectori_ISKPRO_2026-09-04.pdf` with a
  text extract. The brief's Step 1 verifies every recommendation; its
  "no SPF record" is already refuted by nslookup (v=spf1 exists).

- 404 page and structured data shipped and confirmed live. Merged to main
  at 9cd55be on 2026-08-24. `docs/404.html` now serves for any missing
  address, including deep paths, and JSON-LD is on all eleven pages that
  should have it. Every one of the nine new blocks parses from the live
  site and matches its repo copy once line endings are normalized. Logged
  in CHANGELOG.md. The brief this ran from is
  `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-08-24.md` and it is
  finished. The JSON-LD spec the workers built to, which is what a later
  change to any of these blocks should match, is at
  `C:\Code_data\tectori\jsonld_spec_2026-08-24.md`.

- Content release shipped and confirmed live. Merged to main at b46c238 on
  2026-08-24 and serving on www.tectori.com. Six service pages, plus
  resources.html and trust.html, all returning 200 and matching the repo
  copies byte for byte once line endings are normalized. services.html keeps
  all six anchored sections and each links out to its page, so no inbound
  anchor link broke. Resources and Trust are footer only, the top navigation
  is unchanged at nine items, and the sitemap carries 23 urls. No styles or
  scripts changed, so the cache versions stay at v=20260822 and v=20260820.
  The facts on trust.html, where engagement material lives, the 30 day return
  or destroy window, the four practice security controls, and the 48 hour
  email response with a phone path for urgent reports, came from Jon on
  2026-08-24. If any of them stops being true, that page has to change.

- Site analytics is deployed. Pushed to main at 1f6b705 on 2026-08-23 and
  confirmed serving on the live site. The Cloudflare Web Analytics beacon and
  the Scarf pixel are on every public page, twenty two of them after the
  2026-08-24 content release, `docs/login.html` has
  neither and its CSP is untouched, and privacy.html was rewritten in the same
  commit as the tracking. The options research is at
  `C:\Code_data\tectori\stats\analytics_options_research_2026-08-23.md` and
  Jon's account setup notes, including the two Cloudflare wizard traps, are at
  `C:\Code_data\tectori\Tectori_Analytics_Setup.md`.
  - Only owner check left: open a public page and the login page in a browser
    with the network tab showing, confirm the beacon and the pixel fire on the
    first and neither fires on the second. Fetching the deployed HTML already
    confirms the tags ship and both endpoints answer, so this is a browser
    confirmation, not a suspected problem.
  - One Scarf hit on 2026-08-23 came from this workstation's verification
    request, not a visitor. Ignore the first datapoint.
  - Jon will export the Search Console and Bing reports later; they land in
    `C:\Code_data\tectori\stats\` with the export date in the filename. The
    brief flags eight pages reported discovered but not indexed on 2026-08-10,
    so check whether that count moved.

- Discovery and demand session, brief at `C:\Code_data\tectori\MORNING_PROMPT.md`.
  Jon confirmed on 2026-08-22: GBP first, then LinkedIn edits and the launch
  post while verification pends, then the examiner-questions checklist asset.
  He also approved a prominent call path on contact.html and the hero CTAs.
  - Step 1: Google Business Profile. Not done. Jon confirmed on 2026-09-03
    that no profile was ever created; the earlier note that it was started
    on 2026-08-22 with verification pending was wrong. Whether to create one
    is now a decision inside the SEO call research item above.
  - Step 2: LinkedIn company page (5 items) and personal profile (6 items) as
    paste-ready copy from the checklist. The HCA line is Jon's to confirm,
    nothing unconfirmed goes on a public profile.
  - Step 3: publish the launch post from `Posts for Tectori.txt` to the company
    page, Jon reshares from his personal profile the same day, then feature it.
    The Fortivra announcement is the second page post.
  - Step 4: checklist asset drafted in `C:\Code_data\tectori\Paste_Copy_2026-08-22.md`
    section 6, approved by Jon 2026-08-22. Owner task: post it from the
    company page after the launch post has had a few weeks, then feature it.
  - Shipped 2026-08-22: the call path on contact.html and every hero and
    cta-band, main at bdf6e80, logged in CHANGELOG.md.
  - Confirmed live 2026-08-23: `www.tectori.com/solutions.html` serves the
    d4a0b29 Fortivra rewrite byte for byte, and the deployed styles.css matches
    the repo copy. Below 620px the call and email buttons go full width and
    stack, they clear the 46px touch target, and nothing on the page can
    overflow the 390px floor in ui-standards.md. Read from the deployed CSS and
    markup, not rendered in a browser, so a font-driven wrap is the one thing
    this check cannot see.


## Archived 2026-09-06: the Digital Guider follow-up email record

Archived from the Pending section on 2026-09-06. Items 4.1 to 4.6 became the
scored board items ONPAGE-AUDIT, KEYWORD-BASELINE, BACKLINK-CHANNELS,
SOCIAL-CHANNELS, CRAWL-HEALTH and MEASURE-BASELINE. Item 4.7 was a claim about
the vendor's team, recorded here and not investigated.

- Digital Guider follow-up email, items for investigation, added 2026-09-05.
  Source saved verbatim at
  `C:\Code_Data\workspace\website_call_20260903\vendor_followup_email.md`.
  Jon's 2026-09-03 decision stands: not hiring; research and replicate for
  this site only. These items feed Step 5 of the remediation brief, the
  in-house SEO research program, and run after Releases 1 to 4. Same rule
  as the call research: a vendor claim is a hypothesis until measured here.
  No item changes a file in docs/; reports land in
  `C:\Code_data\tectori\seo_research_2026-09-03\` numbered 4.x.
  The vendor's seven deliverables, each mapped to what this site already
  has or needs:
  - 4.1 On-page audit: metas, alt attributes, H1s, XML sitemap, schema,
    robots.txt. Most confirmed present on 2026-09-05 (title, canonical,
    robots, sitemap, OG cards, JSON-LD on eleven pages). Investigate what
    remains: alt text coverage on every image, one H1 per page, meta
    description lengths, and whether the sitemap lists all 23 urls with
    correct lastmod.
  - 4.2 Keyword intent split: informational, navigational, commercial,
    transactional. 3.3_keywords.md mapped both buyer sets without volume.
    Investigate a free volume source (Search Console impressions once the
    export lands, or Bing Webmaster keyword research) and classify the 3.3
    phrases by intent, then map each intent to a page that should own it.
  - 4.3 Backlinks by channel: blogs, articles, classified ads, social
    bookmarking, micro-blogging. 3.4_backlinks.md already flagged Medium,
    Quora and Tumblr as nofollow, the class the vendor called spam.
    Investigate which of the vendor's listed channels pass link equity at
    all, and which Google's link-spam text in 3.7_policy_quotes.md names
    as a violation. Expected result: most of this list is what to avoid.
  - 4.4 Social media optimization: Twitter, LinkedIn, Pinterest, Instagram,
    Facebook, infographic per service plus transcript and hashtags.
    Investigate which channels the regulated buyer actually uses (the
    discovery brief already settled on LinkedIn), and what a one-page
    per-service graphic would cost to produce in-house. Release 3 adds
    the social profile links; this item decides which profiles exist.
  - 4.5 "Google standards" and error removal: overlaps Release 2 and the
    ISKPRO audit. Investigate only what neither covers: broken internal
    and outbound links (crawl the 23 pages), mobile usability, and Core
    Web Vitals field data once the PageSpeed API key exists.
  - 4.6 Monthly progress report: define the in-house equivalent. Which
    numbers, from which free sources (Search Console, Bing Webmaster,
    Cloudflare analytics, Scarf), on what cadence, written to `stats\`
    with the export date in the filename. Sets the baseline before any
    of the above changes anything.
  - 4.7 Team of 5 to 6 (seven roles listed): no investigation, recorded as
    a claim. The roles map to the personas and workers this framework
    already runs.
  The vendor's authority-score roadmap (on-page, technical, off-page,
  content marketing, local SEO) is generic and every line of it is already
  covered by 4.1 to 4.6, 3.5, 3.6 or the remediation releases. Do not
  research it as a separate item.
  The vendor's own claims, for due diligence only, since Jon is not hiring:
  - Google Partner agency ID 8609367258: verifiable on Google's Partners
    directory. A Partner badge is a Google Ads spend and certification
    status, not an SEO credential.
  - Ranks for "Best SMO and SEO Company in USA" and similar: the vendor
    chose the terms; check the terms' actual volume before treating the
    ranking as evidence of anything.
  - 30 to 60 percent traffic increase in 4 to 6 months, guaranteed: from a
    stated base of 0 organic traffic any increase is a large percentage.
    Record the base first (4.6).
  - Address 30 N Gould St #6573, Sheridan, WY: a registered-agent and
    virtual-mailbox address, the type 3.6 and 3.7 found ineligible for a
    Google Business Profile. Note the contrast with Jon's coworking
    address decision; no action.
  - Trustpilot, Google and Clutch reviews: read before any future call,
    not needed now.
  - Pricing page https://digitalguider.com/pricing/seo-pricing/: capture
    the published package prices once as the cost baseline the in-house
    program is measured against.
  Open decision, for Jon, when Step 5 starts: which of 4.1 to 4.6 to run
  first. Recommendation: 4.6 first, because every other item needs the
  baseline it defines, and it is blocked on the Search Console export.

## Archived 2026-09-11: the Current state records from the board

Archived verbatim from the WORK_BOARD.md Current state section on
2026-09-11, when the board was trimmed. Every line below is a record of
work already shipped, research already closed or a decision already taken.
None of it is a next action. The live facts a session still needs were
carried forward to the board at the same time.

## Current state

Records, not work. Nothing here is dispatchable.

- The lane was scored on 2026-09-06 with `ai_development/docs/board-scoring.md`.
  The scored index for the unshipped SEO remediation features lives at the top
  of `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-09-05_remediation.md`, which
  remains the build brief for Releases 1 to 4. The review the developer reads is
  `C:\Code_data\tectori\board_review_2026-09-06.md`.
- Shipped work and closed research were archived verbatim to
  `BOARD_ARCHIVE_2026.md` on 2026-09-06: the 404 and structured data release,
  the content release, the analytics deploy, the 2026-09-03 SEO call research,
  the ISKPRO decision record, the discovery and demand session, and the Digital
  Guider follow-up email record. Read it for evidence, never for instructions.
- Verified on 2026-09-05, no action: SPF exists, analytics exists (Cloudflare
  beacon), and title, canonical, robots, sitemap, HTTPS, OG and X cards are all
  present. Those were audit findings SEO-10 and SEO-11; they have no items.
- Reviewed `C:\Users\JDBow\Downloads\Audit for Tectori (1).pdf` on
  2026-09-08. Its 18 recommendations are covered by existing lane items except
  the homepage keyword consistency finding and the page text-depth finding,
  now tracked as SEO-17 and SEO-18. The extracted text is
  `C:\Code_data\tectori\audit_for_tectori_1_text_2026-09-08.txt`.
- The eight-lane run completed on 2026-09-08. Reports and generated artifacts
  live under `C:\Code_data\tectori\lanes\out\`; status files live under
  `C:\Code_data\tectori\lanes\status\`. Lane 1's repo changes shipped through
  `feature/board-2026-09-06-site`. Lanes 2 through 8 made no repo changes.
- Pre-push review ran on 2026-09-09 over `origin/main..HEAD`. The first pass
  raised two small Formspree/accessibility follow-ups that were fixed and
  committed; the rerun's remaining extensionless URL concern was rejected after
  every sitemap URL on the live GitHub Pages site returned 200. Logs live under
  `C:\Code_data\tectori\reviews\`.
- Go-live completed on 2026-09-09: `feature/board-2026-09-06-site` was
  fast-forward merged into `main` and `main` was pushed to origin. GitHub Pages
  deploys from `main` and `docs/`.
- SEO-18 completed on 2026-09-09: the homepage now includes a buyer-path
  section for exam readiness, cloud review, fractional leadership, and AI
  governance. The approximate homepage word count rose from 605 to 766.
  Copy-review and verification artifacts live under
  `C:\Code_data\tectori\seo18_content_depth_2026-09-09\`.
- SEO-18 pre-push review ran on 2026-09-09 over `main..HEAD`. The
  root-relative link and mobile grid notes were triaged as non-blocking against
  the custom-domain deploy and shared `.path-grid` mobile rule. The review log
  and triage note live under `C:\Code_data\tectori\reviews\`.

- Peer review of the 2026-09-08 lane changes ran on 2026-09-09 over the
  merged tree, not a diff: 1142 internal links resolved with none broken, all
  30 fetched live URLs returned 200, and every canonical resolved correctly,
  including the old `.html` forms that still answer for inbound links. The
  predicted SEO-14 defect did not occur, because `sitemap.xml` moved to the
  extensionless URLs together with the canonicals. Exactly one live `noindex`
  exists, `404.html`, which is deliberate and is in neither `sitemap.xml` nor
  `llms.txt`. Three real findings came out of it, all now closed: the stale
  `llms.txt` descriptions, the Formspree landing page, and the phone number
  character encoding.
- Decided on 2026-09-09, both by Jon: a successful contact form submission
  lands on a Tectori confirmation page rather than Formspree's, and the
  displayed phone number uses plain characters inside a `nowrap` span rather
  than `&nbsp;` and `&#8209;`. Recorded so a later thread does not reopen
  either as a defect or reintroduce the entities as a line-break fix.
- The ten spent lane briefs were archived on 2026-09-09 to
  `C:\Code_data\tectori\lanes\spent_2026-09-09\` with a README saying the
  folder is a record and not instructions, and the dead lane PID file was
  removed. Nothing in `lanes/` is dispatchable now.
- SEO-17 completed on 2026-09-09 and held for review, not merged. The homepage
  Organization schema has always said "regulated and growing organizations"
  while the meta description said only "regulated organizations" and the first
  body paragraph said "the business." Both now name the same audience, and the
  description moved from "responsible AI work" to "governed AI," the term the
  site already uses ten times across nine pages against one use of the other.
  The work sits on `feature/seo17-homepage-keyword-signals`, pushed to origin.
  The item's own rule is that new copy is reviewed before any merge to `main`.
  The worker also proposed an H1 rewrite, rejected on evidence and recorded as
  question 7 below: that sentence is the brand tagline in the footer and social
  image alt text of all 25 pages. Proposal:
  `C:\Code_data\tectori\seo17_keyword_signals_proposal_2026-09-09.md`.
- `scripts/check_llms_drift.py` shipped on 2026-09-09 as the root-cause fix for
  the stale `llms.txt` descriptions. `llms.txt` copies every page's meta
  description with no generator behind it, so it drifts silently whenever a
  description changes. The script compares all 24 copied lines against the
  pages and exits non-zero on any mismatch; `--fix` rewrites them. Run it after
  any meta description change. Its first real use caught a second stale copy of
  the homepage description in the file's summary paragraph, which the first
  version did not read, so the check now covers that line too.
- Rollback for tonight's work, per action. `aeb8928` and `b291bb2` add a script
  plus README and CHANGELOG text and change no page, so reverting either alters
  nothing a visitor sees. The SEO-17 branch is unmerged, so dropping it needs
  no revert: delete the branch here and on origin. If it is merged and Jon then
  wants it out, reverting its two commits restores the previous description,
  hero paragraph and `llms.txt` lines exactly.
- SEO-17 merged to `main` and pushed on 2026-09-10 after Jon's review. The
  homepage meta description and hero paragraph now name "regulated and growing
  organizations," and the description uses "governed AI" rather than
  "responsible AI work." The pre-push review's only flag was its recurring
  objection to a data-root path in the changelog, which CORE-01 requires.
- Decided on 2026-09-10 by Jon, closing question 7: the brand tagline is
  "Audit-ready IT that scales with your ambition." It replaced "IT that holds
  up under audit and scales with your ambition." in all 50 places: the footer
  line and social image alt text on each of the 24 content pages, 48 of those
  occurrences, and two more in the homepage H1 and its `og:description`. Jon
  chose site-wide over homepage-only so the site states one tagline. The
  homepage eyebrow became "Built to be reviewed" in the same change, because
  the H1 below it now opens with "Audit-ready." Recorded so a later thread
  does not read the new line as drift from the old one.

## Archived 2026-09-12: the productization lane and two closed records

Archived from `WORK_BOARD.md` at the end of the unattended 2026-09-12
session, when the board reached 215 lines and its In Progress section had
become a log. Everything below shipped and is recorded in `CHANGELOG.md`.
Nothing here is a next action.

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

- **PROD-8 shipped.** `scripts/rehearse_rebrand.py` runs the rebrand
  rehearsal end to end: clone to the data root, apply the runbook's three
  mechanical steps against a fixture business, rebuild, run all fifteen
  checks, and measure what survived. It fails on a single surviving
  occurrence of the old domain and counts the old brand name rather than
  failing on it, because the second is body copy a new owner rewrites and
  the first is not. Mutation tested by un-tokenizing one fragment: it fails
  and names the file and line.

The next step this thread is taking is to read the site as a buyer would
rather than as its builder. Every check in this repo answers whether the
tree is internally consistent; none answers whether a stranger handed the
repository could get it running. The specific question is what the first
hour looks like for someone who clones it with no context: whether the
README's opening actually says what this is, whether the runbook's step 4
gives enough to rewrite the copy safely, and whether anything assumes a
reader who was here tonight. That is a reading task with a written result,
not a build, and it is the last thing between the current state and a
product that can change hands.

### Moved out of Questions for Jon on 2026-09-12

Neither was a question. Both were records of a decision already taken, and
a Questions section that holds records stops being read as a list of things
waiting on Jon.

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

## Archived 2026-09-12: the overnight reproducibility work

Archived from the In Progress section on 2026-09-12, at the end of the
unattended night Jon started on 2026-09-11. Every bullet below is work that
shipped and was verified; each one's change is in `CHANGELOG.md`. The one
item in it that was not finished here is the service page copy read, which
is a copy judgment and sits on the board under Owner-Only Tasks as
COPY-SERVICE. Nothing else here is waiting on anyone.

- **The buyer read is done and its findings are fixed.** A worker with no
  context read the repository as someone who had just bought it. Its report
  is at
  `C:\Code_data\tectori\reproducible\buyer_read_2026-09-12.md`. Five findings, all
  real, all fixed: the README buried the one fact that stops a new owner
  losing work, the runbook described the hero as one file when it is two,
  step 4 sent the reader into the checker's source, the build's own output
  said 28 pages when 24 are pages, and `THEORY.md` named Jon without ever
  saying who he is. The read also surfaced a defect no document could:
  the link check never looked at `srcset`, so the home page hero's webp was
  unverified.

- **`check_site.py --full` shipped.** It adds the rebrand rehearsal as a
  sixth check, off the default path because it clones the tree outside the
  repo and takes about a minute. A failing rehearsal fails the run.

- **The service page copy read is done and is waiting on Jon.** A worker read
  all six service page fragments against what THEORY.md says the site may
  claim. The report is at
  `C:\Code_data\tectori\reproducible\service_copy_read_2026-09-12.md`.
  Nothing crosses a line: no client, count, testimonial, rating, price or
  result appears anywhere, and the QSA credential is never named. It found
  five sentences that would describe any consultancy in the country, a
  weakest sentence on each page with a replacement, and two disclaimers said
  twice in different words. Three of its line citations were checked against
  the fragments and all three were exact. It is listed under Owner-Only Tasks
  below because every item in it is a copy judgment, which is Jon's.
- **Line endings are pinned to the repository now.** The tree had no
  `.gitattributes`, so they came from whoever cloned it, and this working
  copy's local `core.autocrlf` was the only thing holding the invariant up.
  A clone without it rebuilt to a 1700 line diff across 26 files having
  changed nothing, with all five checks passing, and a clone on this machine
  produced `docs/CNAME` with CRLF, which is the file GitHub Pages reads to
  resolve the custom domain. The live site was never affected. After the fix
  the same clone rebuilds to an empty diff. THEORY.md carried the invariant
  as a repository property when it was a machine property; that is corrected.

- **The checks run somewhere other than this laptop now.**
  `.github/workflows/verify.yml` runs the five checks and the rebrand
  rehearsal on a clean Linux machine for every push and pull request, and
  adds one check that did not exist: `docs/` must be byte identical to what
  the build produces, where `check_site.py` proves only that it renders
  identically. Mutation tested by inserting one space before a `</body>`,
  which the render check passes and the byte check fails. The whole sequence
  was run in a clean clone before it was committed. Nothing in it gates the
  deploy: Pages publishes from `main` and `docs/` either way.
- **THEORY.md was cut from 95 lines to 87 and stopped there.** The framework
  standard is 60. What came out was the incident narrative that belongs in
  `CHANGELOG.md` and the restatements of mechanics the checks already print
  in their own output. What is left is a constraint per bullet that a session
  could break without noticing, so reaching 60 would have meant deleting one.
  Treat the gap as a decision, not a task still open.

- **The workflow ran and passed, twice.** Run 34678242856 went green on a
  Linux runner in five seconds with all five checks, the byte comparison and
  the rebrand rehearsal. It annotated itself with a Node 20 deprecation for
  `actions/checkout@v4` and `actions/setup-python@v5`, so both moved to the
  majors running on Node 24 and run 34678296950 went green with no
  annotation. A workflow that has never run is a file, not a check; this one
  has run.
- **The Formspree endpoint was declared twice and is declared once now.** The
  contact fragment hard-coded the URL alongside the declared value in
  `site/content/site.json`, so a new owner following the runbook got a form
  still posting to the previous owner's inbox. It failed loudly rather than
  shipping wrong, which is why it survived: the identity check already
  catches the mismatch. What was wrong was `THEORY.md`'s claim that the value
  lived in one place. The fragment carries a token now, `docs/` is byte
  identical, and `rehearse_rebrand.py` rebrands all three `third_party`
  values so the claim is tested. Mutation tested both ways.
- **The from-scratch deployment runbook already existed.** The note above
  said nothing told a new owner how to stand up their own copy. That was
  wrong: `PERMISSIONS.md` carries a ten step grant runbook covering Pages,
  DNS, HTTPS, the form and the analytics accounts. Reading it is what found
  the endpoint defect, because its step 7 named a generated file.

- **Eight of the fifteen declared values never reached the pages, and all
  fifteen do now.** The reading task above turned into a measurement: a
  rebranded clone still showed the previous owner's phone number on eleven
  pages, their address on three, and their LinkedIn and GitHub on every page,
  with all six checks green. Only the footer and the utility bar used the
  tokens; the page bodies wrote the literals out. 48 occurrences across 13
  fragments now carry tokens, `docs/` is byte identical, and a rebranded clone
  measures zero residue across all fifteen.
- **The rehearsal was measuring the domain and nothing else.** Its residue
  scan covered the old domain alone, so the seven values that are not derived
  from the domain could not fail it, and its fixture never changed the two
  social URLs at all. Both are fixed: the scan now covers every declared value
  and reports the value, file and line of each survivor. Mutation tested by
  restoring one literal phone number, which fails the rehearsal,
  `check_site.py --full` and the workflow.
- **THEORY.md is 98 lines, up from 87.** The declared-values bullet absorbed
  a constraint that did not exist before: a value must reach the page through
  a token, and no check can see a violation because the tree is correct for
  this owner either way. The incident narrative went to `CHANGELOG.md`.

- **The login page is generated and the rehearsal no longer special-cases**
  **it.** It was source living inside the build output, rebranded by a hand
  written list of substitutions in `rehearse_rebrand.py` that duplicated the
  build's own token map and that nothing checked. It is now
  `site/pages/login.page.frag`, rendered through the same substitution as
  every other fragment but without the shared chrome it never had, which is
  what `VERBATIM_PAGES` is for. Its CSP and its absence of analytics tags are
  unchanged and still checked. `docs/login.html` is byte identical.

- **Two gaps found by that reading, both now checked.** The phone number is
  declared three times in `site.json` and nothing made the three agree, so a
  new owner who changed the displayed number and missed the `tel:` URI would
  have shipped a site showing their number with every Call button dialling
  the previous owner, all ten checks green. And the two social profiles were
  never read at all: their hosts were allowed for unrelated reasons, so a
  page left pointing at the previous owner's account passed. `verify_site.py`
  runs eleven checks now. Mutation tested on all four arms.

- **The six remaining checks were read and none needed changing.** The two
  suspected before reading both hold up: the forbidden-claims check is a
  fixed list of strings and no rewrite of it would read prose, and fetching
  the external URLs the link check skips would make the run depend on other
  people's servers. The canonical worry was wrong: `sitemap.xml` is generated
  from `public_pages.json` independently of the canonicals the check compares
  it against, so a page canonicalised to the wrong path already fails.
- **What the reading did find was a file no check read at all.** `docs/CNAME`
  has no extension, and the identity check scans `.html`, `.xml` and `.txt`.
  It is the file GitHub Pages reads itself to decide which domain serves the
  tree, so a stale one serves nothing or serves someone else's domain, and it
  passed everything. `verify_site.py` runs twelve checks now.

- **`THEORY.md` is 88 lines, down from 107.** Five bullets went because a
  check now enforces and prints what they said, and the rest of the cut was
  narrative moved to the changelog and occurrence counts that nothing
  recomputes. It stops above 60 deliberately: what is left states things no
  check can see, and the earlier attempt that cut to a number had to put a
  constraint back.
