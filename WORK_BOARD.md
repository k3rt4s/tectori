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

## In Progress

Review the SEO-17 homepage copy with Jon, then merge or drop it. The work is
finished and verified on `feature/seo17-homepage-keyword-signals`, which is
pushed to origin and rebased on `main`. Nothing about it is live. Show Jon the
two-file diff (`git diff main..feature/seo17-homepage-keyword-signals`), which
changes only the homepage meta description, the hero paragraph and the two
`docs/llms.txt` lines that copy the description. The board item requires his
read before any merge to `main`. If he approves, fast-forward merge, push
`main`, and confirm the live homepage description changed. If he does not,
delete the branch here and on origin; nothing needs reverting.

Ask him at the same time about question 7 below, the H1 brand tagline, because
it is the part of SEO-17 that was deliberately not done.

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
7. **Homepage H1 versus the site-wide brand tagline.** SEO-17 proposed changing
   the homepage H1 from "IT that holds up under audit and scales with your
   ambition." to "Audit-ready IT that scales with your ambition." so the exact
   title-tag phrase appears in an H1. It was not done, because that sentence is
   the brand tagline in the footer and the social image alt text of all 25
   pages, so the homepage would say one thing at the top and another at the
   bottom. Three options: leave it as it is, change it on the homepage only and
   accept the divergence, or change the tagline across all 25 pages. The third
   is a brand change, not an SEO edit.
