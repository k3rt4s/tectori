# WORK_BOARD

ACTIVE THREAD: 2026-09-06 11:26

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

- **Dispatch the eight lane sessions.** Confirm with Jon, then paste one prompt
  per lane from `C:\Code_data\tectori\lanes\PROMPTS_2026-09-06.md` into eight
  separate sessions. Start Lane 1 first because it cuts
  `feature/board-2026-09-06-site`; after that, lanes 2 through 8 may run
  concurrently. Do not run the lanes in this thread unless Jon explicitly asks.
  When every lane has reported to `C:\Code_data\tectori\lanes\out\` and
  `C:\Code_data\tectori\lanes\status\`, run the morning-session prompt from
  `PROMPTS_2026-09-06.md`: fold the lane reports into this board and
  `CHANGELOG.md`, clear the `ACTIVE THREAD` marker, remove the `## Lanes`
  section once closed out, and show Jon the
  `feature/board-2026-09-06-site` diff plus the new copy listed in
  `LANE_1_SPECS_2026-09-06.md` before anything merges to `main`.
  `score: kind=ops gain=4/15/45 p=0.8 hours=0.1/0.25/0.5 rev=two-way conf=assessed id=dispatch-lanes`
  `return: likelihood 1 in 1 per lane run, 1 occasion this cycle, so about once now, from the eight approved dispatch prompts already written and waiting; impact without dispatch the scored 31-item remediation set remains prepared but unrun, delaying the one-night concurrent lane plan back into serial follow-up work worth 4 to 45 h of Jon's attention; evidence C:\Code_data\tectori\lanes\PROMPTS_2026-09-06.md, the empty out and status directories checked 2026-09-08, and board_review_2026-09-06.md showing the eight-lane dependency split`

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
