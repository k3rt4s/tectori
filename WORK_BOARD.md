# WORK_BOARD

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
  `C:\Code_data\tectori\lanes\status\`. Lane 1 made 14 unpushed commits on
  `feature/board-2026-09-06-site`. Lanes 2 through 8 made no repo changes.

## In Progress

- **REVIEW-GO-LIVE, review the feature branch before merge.** Show Jon the
  `feature/board-2026-09-06-site` diff and the copy log at
  `C:\Code_data\tectori\lanes\out\LANE_1_SPECS_2026-09-06.md`. Decide whether
  to fix MOBILE-HERO-CLIPPING before merge, whether to replace the Formspree
  placeholder before merge, and whether to run pre-push review. The merge to
  `main` is the go-live and nothing pushes without Jon's explicit yes asked as
  its own question after review.
  `score: kind=ops gain=4/15/45 p=0.8 hours=0.25/0.5/1 rev=one-way conf=assessed id=review-go-live`
  `return: likelihood 1 in 1 before this release can ship, 1 occasion now, from Lane 1 completing 14 unpushed feature-branch commits; impact without review the branch either stays unmerged or ships copy, a Formspree placeholder and a known mobile clipping residual without Jon's go-live gate, worth 4 to 45 h of avoided rework and public correction; evidence C:\Code_data\tectori\lanes\out\LANE_1_REPORT_2026-09-06.md, C:\Code_data\tectori\lanes\out\LANE_1_SPECS_2026-09-06.md, and git branch feature/board-2026-09-06-site`

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

- **MOBILE-HERO-CLIPPING, fix 390px page-hero text clipping.** Lane 1 found
  existing right-edge clipping in 390px screenshots for `index.html`,
  `solutions.html`, and `contact.html`. This is independent of the SEO lane
  items and should be fixed before go-live if Jon wants the branch visually
  clean on mobile. Inspect the screenshots under
  `C:\Code_data\tectori\stats\seo04_lighthouse_2026-09-08\` and
  `C:\Code_data\tectori\stats\seo16_contact_2026-09-08\`, patch the shared hero
  layout rather than per-page text, and verify at 390px, 768px, 1366px and
  1920px before merge.
  `score: kind=bug gain=1/4/12 p=1 hours=0.5/1/2 rev=two-way conf=measured id=mobile-hero-clipping`
  `return: likelihood already observed in 390px screenshots on 3 public pages during Lane 1 verification, so once now; impact without it mobile visitors can see clipped hero copy on high-value public pages, 1 to 12 h of lost trust or cleanup if shipped and noticed later; evidence Lane 1 report and screenshots under C:\Code_data\tectori\stats\seo04_lighthouse_2026-09-08\ and C:\Code_data\tectori\stats\seo16_contact_2026-09-08\`
  - worker: haiku 1/2/4 h; candidate before merge

- **SEO-17-KEYWORD-SIGNALS, align homepage keywords across tags.** After Lane 4
  reports POSITIONING and KEYWORD-BASELINE, pick the homepage's owning terms and
  revise only the title, meta description, H1/H2/H3 text and first-screen body
  copy needed to make those terms appear naturally. New copy is reviewed before
  any merge to `main`.
  `score: kind=feature gain=1/4/15 p=0.3 hours=0.5/1.5/3 rev=two-way conf=assessed id=seo-17-keyword-signals`
  `return: likelihood 1 in 3 that aligning the homepage to the chosen owning terms changes how a search or LLM result interprets the page this year, 1 occasion this year, so about once in three years, estimated because the audit reports tag distribution but no traffic volume; impact without it the homepage keeps signaling mostly brand and generic evidence/review/work terms instead of the terms Jon chooses to own, 1 to 15 h if that loses an inquiry; evidence Audit for Tectori (1).pdf pages 6 to 7, the 2026-09-08 extracted text at C:\Code_data\tectori\audit_for_tectori_1_text_2026-09-08.txt, and Lane 4's pending keyword-intent work`
  - worker: sonnet 1.5/3/6 h; depends on Lane 4

- **SEO-18-CONTENT-DEPTH, add substance where the audit finds thin content.**
  After Lane 5 reports COMPETITORS and CONTENT-PLAN, measure word counts for all
  23 indexable pages and add only buyer-useful sections where the plan
  identifies a real gap. Start with the homepage, which the audit measured at
  584 words while still flagging low text volume. New copy is reviewed before
  any merge to `main`.
  `score: kind=feature gain=2/8/30 p=0.25 hours=1/2/4 rev=two-way conf=assessed id=seo-18-content-depth`
  `return: likelihood 1 in 4 that adding substantive content to a thin or under-answering page wins an impression or keeps a buyer on the page this year, 1 occasion this year, so about once in four years, estimated because the audit flags thin content but the measured homepage count is already 584 words; impact without it the homepage and any similarly thin page keep answering at summary depth while competitor pages may answer the buyer's next question, 2 to 30 h if that costs an inquiry; evidence Audit for Tectori (1).pdf page 7, the 2026-09-08 extracted text at C:\Code_data\tectori\audit_for_tectori_1_text_2026-09-08.txt, and Lane 5's pending competitor/content-plan work`
  - worker: sonnet 2/4/8 h; depends on Lane 5

## Questions for Jon

1. **Local versus national targeting.** Lane 4 kept Nashville as location proof
   only and did not make Nashville-modified keywords page targets. Decide later
   whether Tectori should target local Nashville search terms or stay national
   except for NAP/location proof.
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
