# WORK_BOARD

ACTIVE THREAD: 2026-09-06 07:50

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

## Lanes

Records and pointers, not work. The 2026-09-06 grouping run split the 31 scored
items into eight lanes that can run at the same time. The dispatch brief for
each lane is a separate file; the brief carries the worker-ready detail, the
board carries the score and the pointer, so the board stays a working surface.

Every lane inherits `C:\Code_data\tectori\lanes\LANE_RULES_2026-09-06.md`.
Lane reports land in `C:\Code_data\tectori\lanes\out\`.

| Lane                       | Brief                               | Items                                                                                                                                                                                                                               |
| -------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1, site build              | `LANE_1_SITE.md`                    | seo-01-address, seo-03-jsonld-address, seo-07-descriptions, seo-09-scarf-style, seo-08-llmstxt, seo-04-images, seo-05-person, jsonld-ids, seo-06-home-links, onpage-audit, seo-16-contact-form, seo-13-social, seo-14-extensionless |
| 2, GBP and links           | `LANE_2_GBP_AND_LINKS.md`           | seo-02-gbp, seo-12-link-earning                                                                                                                                                                                                     |
| 3, measurement             | `LANE_3_MEASUREMENT.md`             | measure-baseline, plus the export spec that unblocks export-gsc                                                                                                                                                                     |
| 4, positioning             | `LANE_4_POSITIONING.md`             | positioning, keyword-baseline classification half                                                                                                                                                                                   |
| 5, competitors and content | `LANE_5_COMPETITORS_AND_CONTENT.md` | competitors, content-plan                                                                                                                                                                                                           |
| 6, channels                | `LANE_6_CHANNELS.md`                | backlink-channels, social-channels                                                                                                                                                                                                  |
| 7, crawl health            | `LANE_7_CRAWL_HEALTH.md`            | crawl-health, the before-crawl                                                                                                                                                                                                      |
| 8, LinkedIn copy           | `LANE_8_LINKEDIN.md`                | li-profiles, li-launch-post, li-checklist-asset, copy only                                                                                                                                                                          |

Not dispatchable, Jon's own: EXPORT-GSC, ANALYTICS-CHECK, EVIDENCE-PILOT.

Only Lane 1 writes to this repo. Lanes 2 to 8 read it and write only to
`C:\Code_data\tectori\`. That is what makes eight concurrent lanes safe: the
2026-09-06 measurement found `docs/index.html` touched by eleven separate items,
25 "Nashville, Tennessee" lines across 24 files, 67 `href="index.html"`, 117
`contact@tectori.com` across 23 pages and 39 to 50 `.html` hrefs per page, so the
repo work cannot be parallelized and everything else does not touch the repo.

No lane edits this board or `CHANGELOG.md`. The session that reads the lane
reports folds them into both.

### Decisions taken on 2026-09-06, do not re-open

- Push gate: nothing is pushed. A merge to `main` deploys through GitHub Pages,
  so a push is a go-live. Lane 1 commits to `feature/board-2026-09-06-site` and
  stops; Jon reads the diff before anything reaches the site.
- SEO-16 form service: Formspree, built against the literal placeholder
  `https://formspree.io/f/REPLACE_WITH_FORM_ID`. The form is inert until Jon
  creates the form and supplies the ID. Recommended over Web3Forms as the more
  established of the two free options; both give a third party sight of every
  inquiry, which is the cost of a static site with no server.
- SEO-15 Meta pixel: deferred. It scored 1.3, the lowest of the three blocked
  items, and it puts a third-party tracker on all 23 public pages for a campaign
  that is not planned.
- SEO-13 social links: limited to the two profiles already in the tree,
  `https://www.linkedin.com/company/tectori` (in the `index.html` sameAs) and
  `https://github.com/k3rt4s` (host of the seven repos linked from
  `tools.html`). No Facebook, X, Instagram or YouTube until SOCIAL-CHANNELS
  answers whether they should exist. No personal profile URL; none is recorded
  in the tree.
- Copy approval: worker-written copy is committed to the branch tonight rather
  than held for review, and every new sentence is listed in the Lane 1 spec file
  for Jon to read with the diff. The no-push gate is what makes this safe.
- Commit grouping: one commit per item, message citing the SEO ID.
- A worker whose work fails verification twice stops that item; the lane records
  what it found and the default it would have taken, and continues.

## In Progress

- **Score and group the lane.** Score every unshipped item, group the items by
  dependency into lanes that can run concurrently, and write one dispatch brief
  per lane. Phase 1 is the scored list. Phase 2 writes the briefs after the
  developer replies with the groups he approves.
  `score: kind=ops gain=4/15/45 p=0.8 hours=0.5/1/2 rev=two-way conf=assessed id=score-and-group`
  `return: likelihood 1 in 1 per scoring run, 1 occasion this year, so about once, from the single 305-line board this ran over; impact without it the 30 unshipped items run in the brief's four-release sequence at one lane, which is about 6 weeks of evenings instead of one night, and the developer picks by whichever item was described most persuasively; evidence the 2026-09-06 run of score_board.py over WORK_BOARD.md and the remediation brief, and the file-collision map in board_review_2026-09-06.md`
  - worker: none, orchestrator task, 1/2/3 h

## Pending

- **EXPORT-GSC, get the Search Console export.** Four items cannot be measured
  without it. Jon verifies the property at search.google.com/search-console for
  `www.tectori.com`, exports Performance (queries, pages, 16 months) and Links,
  and drops both in `C:\Code_data\tectori\stats\` with the export date in the
  filename. Bing Webmaster export the same way if the property exists. No worker
  can do this; it needs Jon's Google account.
  `score: kind=ops gain=3/10/30 p=0.8 hours=0.25/0.5/1 rev=two-way conf=assessed id=export-gsc`
  `return: likelihood 1 in 1 per request, 1 occasion (the export is pulled once), so about once now, from the four board items that name it as their blocker; impact without it KEYWORD-BASELINE, BACKLINK-CHANNELS, MEASURE-BASELINE and the vendor's 0-ranked-keywords claim all stall or produce estimates Jon has already refused, 3 to 30 h of research that cannot be graded above opinion; evidence the four items below that cite it, the brief Step 5 item 1, and C:\Code_data\tectori\stats\ read on 2026-09-06 holding no export`
  - worker: none, owner task, 0.25/0.5/1 h

- **MEASURE-BASELINE, define the monthly measurement routine.** Digital Guider
  4.6 plus brief Step 5 topic 6. Which numbers, from which free sources (Search
  Console, Bing Webmaster, Cloudflare Web Analytics, Scarf), on what cadence,
  written to `C:\Code_data\tectori\stats\` with the export date in the filename,
  and a twenty minute runbook Jon can follow. Sets the before-number for every
  remediation item.
  `score: kind=ops gain=3/12/40 p=0.6 hours=0.5/1/2 rev=two-way conf=assessed id=measure-baseline`
  `return: likelihood 1 in 1 per measurement cycle, about 12 cycles a year if the routine is monthly, so about 12 a year, from the four free sources already live on the site; impact without a baseline the 16 remediation items ship on faith, a win and noise look identical, and the vendor's 30 to 60 percent traffic claim has no base to be measured against, 3 to 40 h of misdirected work over the year; evidence brief Step 5 topic 6, the archived Digital Guider 4.6 record, and the Cloudflare beacon plus Scarf pixel confirmed live on 22 pages in the 2026-08-23 deploy`
  - worker: sonnet 1/2/4 h

- **ONPAGE-AUDIT, close the on-page audit residue.** Digital Guider 4.1. Most of
  it was measured on 2026-09-06 and is clean: alt text on 53 of 53 images, exactly
  one H1 on all 24 pages, 23 sitemap loc elements. What remains is meta description
  length (SEO-07 covers the four under 120 characters, this item covers privacy.html
  at 189 over the 160 truncation point) and whether every sitemap lastmod matches
  the file's real last change.
  `score: kind=docs gain=0.5/2/6 p=0.5 hours=0.25/0.5/1 rev=two-way conf=measured id=onpage-audit`
  `return: likelihood 1 in 1 per audit, 1 occasion this year, so about once, from the 2026-09-06 sweep of all 24 pages in docs/; impact the residue is one over-length description and unverified lastmod values, 0.5 to 6 h if found later inside a larger regression instead of now; evidence the 2026-09-06 measurement over C:\Code\projects\tectori\docs counting 53 of 53 images with alt, one H1 per page, 23 parsed sitemap locs, and description lengths from 98 to 189 characters`
  - worker: haiku 0.5/1/2 h

- **KEYWORD-BASELINE, rank and intent baseline.** Digital Guider 4.2 plus brief
  Step 5 topic 2. Classify the 3.3 phrases as informational, navigational,
  commercial or transactional, map each intent to the page that should own it,
  and record which queries the site already appears for and at what position.
  Blocked on EXPORT-GSC; the free volume alternatives are Search Console
  impressions and Bing Webmaster keyword research, nothing paid.
  `score: kind=feature gain=5/18/60 p=0.35 hours=0.5/1.5/3 rev=two-way conf=opinion id=keyword-baseline flags=blocked`
  `return: likelihood 1 in 3 that the intent map changes which page owns a term and that change earns an impression, 1 occasion this year, so about once in three years on current inputs, estimated because no volume number exists for any phrase; impact without it the site keeps competing with itself on the compliance terms and the vCISO term stays absent, worth 5 to 60 h of Jon's attention if a term he could own goes to someone else; evidence 3.3_keywords.md which mapped both buyer sets and reported no volume numbers, and the empty stats directory read 2026-09-06`
  - worker: sonnet 1.5/3/6 h

- **BACKLINK-CHANNELS, classify link channels and the existing profile.**
  Digital Guider 4.3 plus brief Step 5 topic 4. Which of the vendor's listed
  channels (blogs, articles, classified ads, social bookmarking, micro-blogging)
  pass link equity at all and which Google's link-spam text in 3.7 names as a
  violation. The classification runs now; the profile half needs EXPORT-GSC.
  Expected result: most of the vendor's list is what to avoid.
  `score: kind=docs gain=2/8/25 p=0.4 hours=0.5/1/2 rev=two-way conf=assessed id=backlink-channels`
  `return: likelihood 1 in 1 per channel decision, about 5 channel decisions a year as Jon is offered link services, so about 5 a year, from the five channels the vendor named in the follow-up email; impact one wrong channel choice buys links Google's own text calls spam, 2 to 25 h to unwind through a disavow plus the ranking cost while it stands; evidence 3.4_backlinks.md which already found Medium, Quora and Tumblr nofollow, and the verbatim link-spam quotes in 3.7_policy_quotes.md from Wayback snapshots dated 2025-12-30 to 2026-08-11`
  - worker: sonnet 1/2/4 h

- **SOCIAL-CHANNELS, decide which social profiles exist.** Digital Guider 4.4.
  Which channels the regulated buyer actually uses, what a one-page per-service
  graphic costs to produce in-house, and therefore which of Facebook, X, Instagram
  and YouTube are worth creating. The discovery brief already settled on LinkedIn.
  This item decides the profile set that SEO-13 then links.
  `score: kind=docs gain=1/5/20 p=0.35 hours=0.25/0.75/1.5 rev=two-way conf=opinion id=social-channels`
  `return: likelihood 1 in 3 that the answer changes which profiles Jon creates, 1 occasion this year, so about once in three years, estimated because no audience data for this site exists yet; impact creating four profiles nobody in the regulated buyer set reads costs 1 to 20 h of setup and upkeep and leaves four dead sameAs links on the Organization node; evidence the archived Digital Guider 4.4 record naming six channels, and the discovery brief's LinkedIn decision of 2026-08-22`
  - worker: sonnet 0.75/1.5/3 h

- **CRAWL-HEALTH, crawl the site for broken links and mobile usability.**
  Digital Guider 4.5, limited to what Release 2 and the ISKPRO audit do not
  already cover: broken internal and outbound links across the 23 indexable
  pages, mobile usability at the three widths in ui-standards.md, and Core Web
  Vitals field data once a PageSpeed API key exists. Run it once before Release
  4 and once after, because Release 4 rewrites every internal href.
  `score: kind=prevent gain=0.5/3/12 freq=1 p=0.3 hours=0.25/0.75/1.5 rev=two-way conf=assessed id=crawl-health`
  `return: likelihood about 1 broken link a year across roughly 1000 internal hrefs, from the 2026-09-06 count of 39 to 50 .html hrefs on each of 24 pages, with p 0.3 that one is already broken since no crawl has ever run and the two verification passes on 2026-08-24 and 2026-08-31 are too few trials to bound; impact a dead link costs a visitor the page they came for and costs 0.5 to 12 h to notice and repair, at the high end if it sits on a service page for a quarter; evidence the 2026-09-06 href count over C:\Code\projects\tectori\docs, and Release 4 in the remediation brief which rewrites every one of them`
  - worker: haiku 1/2/4 h

- **POSITIONING, resolve the startup and vCISO divergence.** From 3.3. The site
  is written for regulated organizations; the sales call described Series A to B
  startups and growth SMBs; the term vCISO appears nowhere on the site. Decide
  whether the site serves one buyer or both, and if both, which pages carry which
  language. A proposal for Jon, no public copy changes in this item.
  `score: kind=feature gain=5/20/80 p=0.3 hours=0.5/2/4 rev=two-way conf=opinion id=positioning`
  `return: likelihood 1 in 3 that a positioning change wins a buyer the current copy loses, 1 occasion this year, so about once in three years, estimated because the site has no traffic baseline; impact the wrong buyer reads every page, and the most searched term for the fractional service is missing from the site entirely, worth 5 to 80 h of Jon's attention if a fractional engagement goes elsewhere; evidence 3.3_keywords.md sections on the two buyer sets, the FFIEC and HIPAA lead on service-compliance-risk.html, and a 2026-09-06 grep finding no occurrence of vCISO in docs/`
  - worker: sonnet 2/4/8 h

- **EVIDENCE-PILOT, run the Evidence Readiness Baseline with the first buyer.**
  Keep one defined review boundary and test whether the scope, evidence inventory,
  findings and prioritized action list are useful without a maturity score. After
  the pilot, decide duration, sample size, fixed price, payment terms, and whether
  the offer stays standalone. Brief at
  `C:\Code_data\tectori\EVIDENCE_READINESS_BASELINE_OFFER_2026-08-30.md`. Blocked
  on a qualified buyer; no worker can start it.
  `score: kind=feature gain=20/80/300 p=0.2 hours=2/6/16 rev=two-way conf=opinion id=evidence-pilot flags=external,blocked`
  `return: likelihood 1 in 5 that a qualified buyer appears and takes the pilot this year, 1 occasion this year, so about once in five years at the current inbound rate, estimated because the site has produced no recorded inquiry; impact the offer stays unpriced and untested, so the first real buyer becomes the experiment, worth 20 to 300 h across a mispriced or misscoped first engagement; evidence the 2026-08-30 offer brief, the site changes verified live on 2026-08-31, and no inquiry recorded in the Cloudflare or Scarf data since 2026-08-23`
  - worker: none, owner task, 6/12/24 h

- **JSONLD-IDS, give the two nodes without an @id one.** The `FAQPage` node in
  `docs/faq.html` and the founder `Person` node nested in the `docs/index.html`
  Organization block both lack an `@id`. Neither is a defect. Giving the index
  founder an `@id` lets `about.html#person` reference one canonical Person instead
  of declaring its own. Jon considered and set this aside on 2026-08-24 to keep
  that release inside its nine pages. Spec amendment first.
  `score: kind=debt gain=0.5/1.5/5 p=0.3 freq=2 hours=0.25/0.5/1 rev=two-way conf=assessed id=jsonld-ids`
  `return: likelihood about 2 touches of the JSON-LD a year, from the four releases in the current brief that each amend a node, with p 0.3 that a touch actually trips over the missing @id; impact a second Person declaration drifts from the first, so a crawler sees two people, 0.5 to 5 h to notice and reconcile; evidence the 2026-08-24 verification pass that found both, and jsonld_spec_2026-08-24.md which governs all eleven pages carrying JSON-LD`
  - worker: haiku 0.5/1/2 h

- **ANALYTICS-CHECK, confirm the beacon and pixel in a browser.** Open a public
  page and `login.html` with the network tab showing. Confirm the Cloudflare beacon
  and the Scarf pixel fire on the first and neither fires on the second. Fetching
  the deployed HTML already proved the tags ship and both endpoints answer, so this
  is a browser confirmation, not a suspected problem. Ignore the 2026-08-23 Scarf
  hit; it came from this workstation.
  `score: kind=ops gain=0.5/2/8 p=0.4 hours=0.15/0.25/0.5 rev=two-way conf=assessed id=analytics-check`
  `return: likelihood 1 in 1 per check, 1 occasion this year, so about once, from the single unverified claim left in the 2026-08-23 analytics deploy; impact if the beacon does not fire, every number MEASURE-BASELINE reports is empty and nobody knows why, 0.5 to 8 h of chasing a measurement gap that is really a deploy gap; evidence the 2026-08-23 deploy at 1f6b705, the deployed HTML fetch confirming both tags on 22 pages, and login.html confirmed carrying neither`
  - worker: none, owner task, 0.25/0.25/0.5 h

- **LI-PROFILES, publish the LinkedIn company page and personal profile edits.**
  Five company page items and six personal profile items as paste-ready copy from
  `C:\Code_data\tectori\Paste_Copy_2026-08-22.md`. The HCA line is Jon's to confirm
  and uses the March 2026 layoff framing, never "engagement concluded". Nothing
  unconfirmed goes on a public profile.
  `score: kind=feature gain=5/20/60 p=0.5 hours=0.5/1.5/3 rev=two-way conf=opinion id=li-profiles flags=external`
  `return: likelihood 1 in 2 that a complete company page is what a referred buyer checks before contacting, about 5 checks a year at the current referral rate, so about 2 a year, estimated because LinkedIn page views are not yet recorded; impact an empty company page reads as an inactive practice to the one buyer who looks, 5 to 60 h if it costs a referred engagement; evidence Paste_Copy_2026-08-22.md sections for the eleven items, and the archived discovery brief where Jon approved the sequence on 2026-08-22`
  - worker: sonnet 1/2/4 h

- **LI-LAUNCH-POST, publish the launch post and reshare it.** Post from
  `C:\Code_data\tectori\Posts for Tectori.txt` to the company page, Jon reshares
  from his personal profile the same day, then features it. The Fortivra
  announcement is the second page post. Runs after LI-PROFILES; a launch post on an
  empty page wastes the launch.
  `score: kind=feature gain=3/12/40 p=0.5 hours=0.25/0.75/1.5 rev=one-way conf=opinion id=li-launch-post flags=external`
  `return: likelihood 1 in 2 that the post reaches someone in Jon's network who becomes a conversation, 1 occasion this year, so about once every two years, estimated because no post has been published from the page; impact the practice stays unannounced to the network that already knows Jon, 3 to 40 h if the first inbound conversation is what it would have started; evidence Posts for Tectori.txt drafted 2026-08-19, and the archived discovery brief Step 3 approved by Jon on 2026-08-22`
  - worker: haiku 0.5/1/2 h

- **LI-CHECKLIST-ASSET, publish the examiner-questions checklist.** Drafted in
  `C:\Code_data\tectori\Paste_Copy_2026-08-22.md` section 6 and approved by Jon on
  2026-08-22. Post it from the company page a few weeks after the launch post, then
  feature it. Runs after LI-LAUNCH-POST.
  `score: kind=feature gain=2/10/40 p=0.4 hours=0.25/0.75/1.5 rev=one-way conf=opinion id=li-checklist-asset flags=external`
  `return: likelihood 1 in 3 that a checklist post earns a saved or shared response that reaches a buyer, about 1 post a year, so about once in three years, estimated because the page has no engagement history; impact the one genuinely useful asset the practice has stays unpublished, 2 to 40 h if it is what would have started an audit-readiness conversation; evidence Paste_Copy_2026-08-22.md section 6, approved by Jon 2026-08-22 and recorded in the archived discovery item`
  - worker: haiku 0.5/1/2 h

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
