# WORK_BOARD

ACTIVE THREAD: 2026-09-16, unattended hunt run per C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-09-16.md

## Current state

Records, not work. Nothing here is dispatchable.

- GitHub Pages publishes the artifact the workflow uploads, not the branch.
  A push to `main` runs every check and deploys `docs/` only if they pass,
  so a push is still the go-live but a red run now ships nothing. Allow
  about three minutes before checking a live URL. This said Pages deployed
  from `main` and `docs/` until 2026-09-12, which was true and was the
  defect: the checks reported on a tree visitors were already being served.
- `check_live_deploy.py` asks only about the files `docs/` holds, so a file
  the live site serves and `docs/` no longer contains is invisible to it.
  That is the declared-only shape every other defect here has had, and it
  was looked at on 2026-09-12 and deliberately left. The deploy replaces the
  whole Pages artifact on every successful run, so an ordinary content edit
  cannot leave a stale file behind; only a partial rollout or CDN lag could,
  and neither is something this repository can cause or fix. Closing it
  would mean listing the live tree, which Pages offers no way to do.
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
- `verify_site.py` runs 25 checks and `check_site.py` runs 15, or 16 with
  `--full`, which adds the rebrand rehearsal. Four defects that were live on
  the published site were found and fixed on 2026-09-12 by asking what a tree
  would look like that passes the existing checks while being wrong: the
  founder's identity surviving a rebrand in structured data, body text on the
  gold band at 4.40 to 1 against a stated 4.5, structured data that names the
  page it was copied from, and five image declarations claiming a size the
  files are not. Each is in `CHANGELOG.md` with the tree that proved it.
- Decided on 2026-09-11 by Jon, closing question 1. Tectori stays
  nationally targeted. No location pages, no LocalBusiness schema, no
  Nashville modified keyword targets across the site, and the nationwide
  wording on all 24 pages stands. Nashville was added to the title and meta
  description of `contact`, `about` and `service-fractional-leadership`,
  and to each of those pages' mirrored JSON-LD, because Jon asked for the
  city to appear in some keyword bearing fields. Reopen the targeting
  question only if the Search Console export shows real local query volume.
- Decided on 2026-09-14 by Jon, closing question 5. The repository is
  licensed in two halves: `LICENSE` publishes the generator, checks, chrome
  and runbooks for review only, with a commercial license by written
  agreement, and `NOTICE` reserves the copy, images, declared values and the
  founder outright and names what no license grants. The inventory and the
  three options he chose from are at `C:\Code_data\tectori\license\`. A paid
  agreement with a buyer still needs a lawyer; reopen only when one exists.

## In Progress

Checkpoint, 2026-09-16 run: the documented-commands scope fix is on branch
`feature/hunt-documented-commands-all-docs`. Gates: check_site --full, then
the pre-push review, then PR, verify, merge. If `main` does not yet carry
that change, check that branch and `gh pr list` first. Open gaps queued
behind it, each proven by probe: `check_doc_claims.py` not covering the
README Configuration counts, the img arm skipping an img with no size, a
future sitemap `lastmod`, and a declared host no page uses. Probe log:
`C:\Code_data\tectori\hunt_2026-09-16\probes.md`.

You have no next action here. The board is finished, and that is the
answer rather than a gap to fill: ask Jon what he wants before starting
anything. The unattended run of 2026-09-11 to 09-12 is closed and its
standing instruction expired with it, so do not read it as authority to
work unprompted.

Every repo item that was on this board has shipped, and the productization
lane PROD-1 through PROD-8 shipped tonight. What each one changed is in
`CHANGELOG.md`; the working notes are in `BOARD_ARCHIVE_2026.md` under the
2026-09-12 heading. Nothing below there is a next action.

Everything shipped after that point came from hunting one defect class rather
than from this board, and the entries are in `CHANGELOG.md` under the same
date. The class is stated in `THEORY.md`: a check that confirms a declared
thing is present cannot see a thing that should not be there. Every defect
found in this tree has been an instance of it, and the way to find the next
one is to take a check and ask what a tree would look like that passes it
while being wrong. That question is what produced the stale-file report, the
reachability check, the source-only build, the live deploy check, the deploy
gate, the 404 probe, and the two machine paths nobody had noticed.

The hunt is still productive and is the obvious thing to resume if Jon wants
more of it. It has not run dry: the last four passes each found something
live rather than only guarding against something. It is also no longer the
highest-value thing available, because what is left on this board needs Jon
rather than another check.

The nine record bullets that stood here are in `BOARD_ARCHIVE_2026.md` under `## Archived 2026-09-16: In Progress records`.

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
  `score: kind=feature gain=1/4/12 p=0.5 hours=0.5/1/2 rev=two-way conf=opinion id=copy-service`
  `return: likelihood 1 in 2 that a reader of service-fractional-leadership notices the stock wording or the solo-delivery sentence, estimated, no traffic data by page yet; impact the page most worth rewriting keeps its weakest copy and one sentence stays in tension with the no-one-person rule, 1 to 12 h of lost positioning value; evidence C:\Code_data\tectori\reproducible\service_copy_read_2026-09-12.md and the THEORY.md Invariants bullet on one-person framing`
  - worker: sonnet 1/1.5/2 h

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
national versus local targeting call, was closed on 2026-09-11, and question
5, the license, on 2026-09-14. Both are recorded under Current state.

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
