# WORK_BOARD

ACTIVE THREAD: 2026-09-12 08:30. An orchestrator session is live in this
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

- **`THEORY.md` stops above the 60 line standard on purpose.** It is 88
  lines. Every bullet left states a constraint no check can see, so reaching
  60 would mean deleting one, and an earlier attempt at that did exactly
  that and had to put it back. Treat the gap as a decision, not a task.
- **A push to `main` runs the checks, and only then deploys.**
  `.github/workflows/verify.yml` runs `verify_site.py`, `check_site.py`, the
  rebrand rehearsal and a byte comparison of `docs/` against what the build
  produces, then a second job uploads `docs/` to Pages. The repository
  publishes from the workflow, not from the branch, so a red run deploys
  nothing and the site that is already up keeps serving. It published either
  way until 2026-09-12, when a red run meant a broken tree was already live.
- **Nothing a new owner would read or run names this machine.**
  `build_site.py` requires `--out` rather than defaulting to a directory under
  the data root, the rehearsal clones into the system temporary directory, and
  the READMEs call the interpreter `python`. `CLAUDE.md` and `.gitignore` both
  still carried an absolute path until 2026-09-12; this bullet claimed
  otherwise for a day. What remains is this board and the two history files,
  which cite report paths under the data root on purpose, as records.
- **`--check` fails on a file `docs/` carries that the build did not write.**
  A build writes and never deletes, so a dropped page or a renamed image used
  to leave a live file that every check passed over.
- **`docs/` is output with no exceptions, and that is now literally true.**
  The stylesheet, the script and the images are source under `site/static/`.
  A tree with no `docs/` at all builds a complete deployable site; before
  2026-09-12 it built the pages and silently shipped no styling.
- **Page weight was measured on 2026-09-12 and needs nothing.** The heaviest
  page is the home page at about 646 KB across 11 files, and `solutions` is
  555 KB. The hero ships through a `picture` element, so a browser fetches the
  85 KB WebP and never the 1.5 MB PNG beside it, and counting the fallback is
  what makes a naive measurement read 2.1 MB. Most of the rest is six solution
  marks at about 78 KB each, all of them lazy loaded and below the fold. The
  only heavy thing above the fold is the 118 KB logo. Re-encoding any of it
  would mean an image library, which the build refuses on purpose, and a
  change to `docs/` that cannot be reviewed without a browser, so none of it
  was done. Treat this as measured rather than as a task.
- **The buyer read of the repository is done and its findings are fixed.**
  The report is at
  `C:\Code_data\tectori\reproducible\buyer_read_2026-09-12.md`. It is a
  record; a second read would be new work, not a repeat of this one.

Nothing on this board is dispatchable. Every repo item has shipped, and what
remains under Owner-Only Tasks and Questions for Jon needs Jon's account, his
judgment on copy, or a buyer who does not exist yet. If you are a fresh
thread with no instruction from Jon, that is the answer: the board is done,
say so and ask him what he wants rather than inventing work from the archive.

## Owner-Only Tasks

- **COPY-SERVICE, decide what to change on the six service pages.** The read
  is done and the findings are at
  `C:\Code_data\tectori\reproducible\service_copy_read_2026-09-12.md`.
  Every item is a copy judgment, so none of it was applied. Two are worth
  Jon's attention before the rest. The first is
  `service-fractional-leadership`, which the read names as the page most
  worth rewriting: its heading, its opening premise and its accountability
  line are all stock fractional-CIO wording. The second is one sentence on
  that page, "Every engagement is delivered directly by Tectori's founder",
  which states solo delivery outright where THEORY.md says the copy must not
  frame the practice as one person. The read judged it acceptable because it
  separates the offer from a staffing placement. That call is Jon's, and it
  is the only place in the six pages where a stated commitment and the
  shipped words point different ways.

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
- **Question 5, what a buyer is licensed to do with the tree.** The
  repository carries no LICENSE and no statement of what is being sold. The
  generator, the checks and the runbooks are the part with resale value; the
  copy, the case study, the images and the three third-party identifiers are
  this business and are not. Which of those a buyer receives, and under what
  terms, is a decision with legal weight and no default worth guessing, so
  nothing was written. The rebrand rehearsal already proves the two halves
  separate cleanly, which is the evidence a split license would rest on.
- **Question 4, LinkedIn personal headline.** Lane 8 did not write a
  paste-ready personal profile headline because the source marked the
  current headline as `CONFIRM`. The default it would take if confirmed is
  to append `PCI, HIPAA, SOC 2, HITRUST, ISO 42001, NIST AI RMF` to the
  existing headline.
