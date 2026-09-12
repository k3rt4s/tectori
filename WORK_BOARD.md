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
- `docs/llms.txt` is generated from the same meta descriptions the pages
  are rendered from, so it can no longer drift and needs no separate step.
  `scripts/check_llms_drift.py` still runs inside `scripts/check_site.py`
  as a second opinion. This line said the opposite until 2026-09-12.
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

Every repo item that was on this board has shipped, and the productization
lane PROD-1 through PROD-8 shipped tonight. What each one changed is in
`CHANGELOG.md`; the working notes are in `BOARD_ARCHIVE_2026.md` under the
2026-09-12 heading. Nothing below there is a next action.

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

The next step this thread is taking is to give `scripts/check_site.py` a
`--full` mode that also runs the rebrand rehearsal. Today the repository
proves two different things with two different commands, and only one of
them is the one a reader is told to run before deploying. The rehearsal is
slower and writes outside the repo, so it should stay off the default path
and be one flag away rather than a thing you have to know about.

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

Each is a decision only Jon can make inside a third-party interface. The
original numbering is kept because other records cite it; question 1, the
national versus local targeting call, was closed on 2026-09-11.

- **Question 2, Google Business Profile category.** Lane 2 could not verify
  whether `Computer Security Service`, `Computer Consultant`, or `Business
  Management Consultant` are categories Google currently offers. In the
  Google interface, choose only from categories Google actually offers.
- **Question 3, Google Business Profile video verification.** Lane 2
  included the video rule from a lower-confidence source and marked
  home-business specifics unresolved. Follow whatever verification method
  Google offers in the GBP interface.
- **Question 4, LinkedIn personal headline.** Lane 8 did not write a
  paste-ready personal profile headline because the source marked the
  current headline as `CONFIRM`. The default it would take if confirmed is
  to append `PCI, HIPAA, SOC 2, HITRUST, ISO 42001, NIST AI RMF` to the
  existing headline.
