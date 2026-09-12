# WORK_BOARD

ACTIVE THREAD: 2026-09-11 23:15. An orchestrator session is live in this
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
instruction for the night: do not prompt him, take the recommended path,
use workers, merge and push as needed, do not stop until he stops it, and
do no work that does not score well enough to be worth doing. The approval
covers this night only and expires with it.

The objective he named is to finish the board so the site can become a
reproducible product that can be sold or hosted. Every repo item on this
board has shipped, so the night's work is the reproducibility layer.

- **REPRO lane, all five items done, on `feature/repro-generator`, not yet
  merged.** The lane is complete as built. Its evidence, its rollback and the
  one thing left to do are below. If you are the thread that picks this up,
  your next action is the merge and push named at the end of this section.
  - REPRO-1 measured the duplication. 84,011 of 289,004 bytes, 29.1 percent of
    the tree, were repeated chrome. The report is at
    `C:\Code_data\tectori\reproducible\duplication_survey_2026-09-11.md`.
  - REPRO-2 built the generator. `site/` holds the content model, `scripts/
    build_site.py` renders it. Committed at 00425f0.
  - REPRO-3 built `scripts/verify_site.py`, one command, now nine checks.
    Committed at 4ba4a9b.
  - REPRO-4 tied the JSON-LD mirror to the page as that ninth check, with the
    exempt pages named so an uncovered page is reported rather than skipped.
    Committed at f386b54.
  - REPRO-5 collapsed the 28 stored chrome formatting variants to one template
    per piece and made `docs/` the generator's own output, so a nav or footer
    change is one edit rather than 14. Committed at 2e4f6dc. Hardened at
    03f13ab after a pre-push review: the content model is validated with the
    offending page and field named, interpolated values are escaped, and a
    build copies every file `docs/` carries that it does not generate, so the
    output is a complete deployable tree rather than pages alone.
  - Verified four ways, none of them the scripts' own passing run.
    `build_site.py --check` reports 24 of 24 pages byte-identical to `docs/`,
    `verify_site.py` passes 9 of 9, `check_llms_drift.py` reports no drift, and
    `compare_render.py` finds the built tree render-identical. The full built
    tree compares byte-identical to `docs/` across all 44 files. Every new
    check was tested by mutation against a scratch copy.
  - The pre-push review log for 2e4f6dc is at
    `C:\Code_data\tectori\reviews\pre_push_2026-09-12_normalization.md`.
  - Rollback: `docs/` differs from what was deployed only in whitespace, and
    reverting 2e4f6dc restores the hand-authored bytes. Everything else on the
    branch is additive.

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
