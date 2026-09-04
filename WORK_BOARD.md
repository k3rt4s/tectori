# WORK_BOARD

## In Progress

- YOUR NEXT ACTION. Read the orchestrator brief at
  `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-09-04.md` before anything
  else. It replaces every brief before it. You are a review and planning
  thread: verify all 18 recommendations in the ISKPRO audit (archived
  beside the research reports), board one feature per finding, put the
  open decisions and the four business-address questions to Jon through
  the interactive question tool, then write the remediation orchestrator's
  prompt. Nothing under docs/ changes in your thread.

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

## Pending

- Pilot the Evidence Readiness Baseline with the first qualified buyer. The
  offer and delivery brief were built on 2026-08-30 and the site changes went
  live on 2026-08-31, verified on the deployed page. The pilot should keep one
  defined review boundary and test whether the scope, evidence inventory,
  findings, and prioritized action list are useful without a maturity score.
  After the pilot, decide duration,
  sample size, fixed price, payment terms, and whether the offer remains
  standalone. Delivery brief:
  `C:\Code_data\tectori\EVIDENCE_READINESS_BASELINE_OFFER_2026-08-30.md`.
- Optional, small: two pages carry structured data with no `@id`. The
  `FAQPage` node in `docs/faq.html` and the founder `Person` node nested in
  the `docs/index.html` Organization block both lack one. Neither is a
  defect and neither breaks anything today. Giving the index.html founder
  an `@id` would let `about.html#person` reference one canonical Person
  instead of declaring its own, which is the shape Jon considered and set
  aside on 2026-08-24 to keep that release inside its nine pages. Found by
  the verification pass on 2026-08-24, both pre-existing, both deliberately
  left alone.

## Questions for Jon

- The five resumes outside this repo say Internal PCI Qualified Security
  Assessor. PCI SSC issues Internal Security Assessor (ISA) to employees and
  reserves Qualified Security Assessor for external assessor companies. The
  site says ISA. The resumes should be corrected to match, which is work in
  another folder, not in this repo.
- The executive resume claims a client outcome delivered through an MSP
  partner, a 140,000 email index cut 80 percent and 37 percent in license
  savings. The site claims no client results anywhere and case-study.html
  says so explicitly. Jon chose on 2026-08-23 to leave it off the site.
  Recorded so a later thread does not rediscover it as a gap.
