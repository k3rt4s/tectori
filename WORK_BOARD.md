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

The next step this thread is taking is this board, which is 259 lines against
the 200 line threshold at which a board stops being read. Split it the way
the framework rule says: move every completed or superseded section verbatim
into `BOARD_ARCHIVE_2026.md`, which already exists and already opens with a
line saying it is a record and not instructions. Two things matter more than
the line count and are the reason for doing it. Carry everything still live
across explicitly rather than assuming it survives the move, and read every
section you archive for a question that was asked and never answered, because
a long board hides open decisions by burying them. Anything you find that is
Jon's to decide goes under Questions for Jon, not into the archive.

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
- **Question 4, LinkedIn personal headline.** Lane 8 did not write a
  paste-ready personal profile headline because the source marked the
  current headline as `CONFIRM`. The default it would take if confirmed is
  to append `PCI, HIPAA, SOC 2, HITRUST, ISO 42001, NIST AI RMF` to the
  existing headline.
