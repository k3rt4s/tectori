# Changelog

Tectori website changes are recorded here.

## 2026-09-12

- `verify_site.py` measures the privacy policy against the tree. The policy
  tells a visitor that the site sets no cookies, stores nothing on their
  device and loads nothing from a third party beyond the two companies it
  names. The identity check reads the same hosts to answer a different
  question, whose accounts these are, so a host added to the allowlist for a
  good reason passes it while making this page a false statement. The new
  check reads every URL the browser fetches on its own and every file for
  cookie and storage calls. The three sentences are read from the page, so
  rewording or withdrawing a promise fails rather than leaving a check
  enforcing something the site no longer says. Proved against a copy with a
  web font linked, the font host allowed in `site.json` and one
  `localStorage` write added: the committed checks passed it 16 of 16, this
  one names both.

- `verify_site.py` measures the accessibility page against the tree. That
  page is a public statement about how the site treats people using
  assistive technology, it is the only page here whose sentences promise a
  visitor something rather than describe a service, and nothing checked it.
  Three of its claims are measurable and now are: every page carries a skip
  link whose target id exists on that page, every `<img>` carries an alt
  attribute, and every page has a `<main>`, exactly one `<h1>` and an
  aria-label on each `<nav>`. The three sentences are read from the page
  itself, so rewording or withdrawing a promise fails rather than leaving a
  check enforcing something the site no longer says. Proved against a copy
  with one alt attribute deleted, one skip link retargeted at an id that
  does not exist and one claim reworded: the committed checks passed it 15
  of 15, this one names all three.

- `verify_site.py` resolves the URLs a page states outside a link. The link
  check reads `href` and `src`, which is what a visitor clicks; the social
  card image, `og:url` and the `image`, `url` and `@id` values inside the
  structured data are read by a crawler and by whatever renders a link in a
  chat window, and they fail out of sight. The social image is named in a
  meta tag on all 24 pages and nowhere else, so renaming that one file left
  every check passing and every share of this site blank. 99 stated URLs are
  now resolved. Proved by renaming it in a copy of `docs/`: the committed
  checks passed 14 of 14, this one names all 24 pages.

- `verify_site.py` reads the contact form, which nothing did. The identity
  check confirms the Formspree endpoint appears in the tree, which it would
  even if the form were not posting to it, and every other check treats the
  page as text. A form fails silently by construction: the visitor fills it
  in, the browser posts it, the thank-you page loads, and the field whose
  name attribute was lost in an edit is simply not in the mail. The new
  check requires the form to post to the declared endpoint by POST, every
  control to have a name and a label, the name, email and message fields to
  exist, the `_gotcha` spam trap to exist and to be hidden by a rule in
  styles.css, and `_next` to name a page of this site. Proved against a copy
  with the email field's name removed, the honeypot's wrapper class changed
  to a visible one and `_next` pointed off site: the committed checks passed
  it 13 of 13, and this one names all four faults. A visible honeypot is the
  worst of them, because Formspree discards every submission that fills it
  in and the site looks like nobody is writing.

- `scripts/check_stdlib_only.py` reads every script's imports and requires
  each to name a standard library module, and `check_site.py` runs it.
  `PERMISSIONS.md` promises a clone runs on a machine with nothing
  installed, and says the missing `requirements.txt` is deliberate rather
  than an oversight. Nothing verified either half. Every check here runs on
  a machine that has had packages installed into it, so one convenient
  import would have passed the whole suite and failed for the first buyer to
  clone the repository. The check reads the promise as well as the imports,
  so withdrawing one without the other fails. Proved against a copy with an
  `import requests` added and a `requirements.txt` beside it: both were
  named.

- `build_site.py` requires each content entry's canonical and og:url to name
  the page that entry writes. A canonical copied from the entry beside it
  tells a search engine the page is a different page, which drops it from the
  index and credits its content elsewhere, and the tree that ships looks
  right because the link resolves. The build did refuse it, one stage later
  and for the wrong reason: llms.txt could not find a description for the
  output path and reported that the page was not in the content model, which
  is the one thing it was. Proved by pointing tools.html's canonical at
  /thank-you and confirming the committed build blamed the content model
  while this one names the canonical.

- `build_site.py` refuses a content model where two entries write the same
  file. Copying an entry to start a new page and leaving `output` unchanged
  deletes the first page by overwriting it, and every count still matched:
  43 files written, 43 published, no orphans, because nothing counted the
  entries against the files. The tree was caught downstream, by two pages
  then declaring one canonical, which is the symptom rather than the cause.
  The build now names the two entries and writes nothing.

- `scripts/check_source_only_build.py` builds from the source files git
  carries rather than from the working directory, and says which of the two
  it used. What a new owner receives is a clone, so a source file that was
  written but never added is absent from what they get; copying the working
  directory proved this machine can build the site, which nobody doubted.
  A local run before a push was the case that mattered, because the workflow
  checks out a clean tree and would have failed after the push instead.
  Proved by untracking one content file and watching the previous version
  pass and this one fail. Inside the rebrand rehearsal's clone, which has no
  git history on purpose, it falls back to the working copy and says so, and
  it refuses to answer with a parent repository's file list.
- `THEORY.md` records that `compare_render.py` compares the top level of each
  directory only. Every page here is at the top level and the build creates
  no directory under its output, so nothing is uncompared today; the
  assumption was undocumented, which is how it would survive the change that
  made it wrong.

- `scripts/check_doc_claims.py` reads the twelve countable claims `README.md`
  and `PERMISSIONS.md` make about this tree and compares each against the
  tree, and `check_site.py` runs it. Every other check reads the site; this
  one reads what the repository says about the site, which is what a new
  owner follows and what three fixes today were correcting by hand. It found
  two counts already wrong: the README said the live deploy check was not one
  of six when there were seven, and that `--full` adds the rehearsal as a
  seventh check when it is the eighth. A claim whose sentence it cannot find
  is a failure rather than a pass, so a rewording that removes a claim is
  caught in the same way a wrong number is.
- The rebrand rehearsal applies runbook step 4 as well, rewriting the brand
  name in `site/pages/login.page.frag`, which is the one page carrying it as
  prose rather than through a token. It applies all four mechanical steps
  now. The prompt for it was the new documentation check failing inside the
  rebranded clone: the README's count of brand-name occurrences on that page
  was right for this owner and wrong for a half-rebranded one, which is a
  fair thing for a check to object to.

- The runbook in `README.md` gained the founder's identity as step 2, between
  the business values and the images, and the steps after it are renumbered.
  A new owner following the old list in order rebranded the business and
  shipped a site whose home page still carried the previous owner's name in
  its Person node. The biography strings are named there as explicitly not
  part of that step: there is nothing to substitute, they belong to the copy
  step, and the rehearsal reports how many survive and which files hold them.
- `PERMISSIONS.md` called GitHub Actions best-effort and said Pages deployed
  from the branch whether the workflow ran or not. That was true until the
  deploy moved into the workflow on 2026-09-12 and is now the opposite of
  true: Actions is the only route to the site, and disabling it stops every
  deploy rather than costing the checks alone. The Pages entry also now says
  what the site needs from any host, which is one behaviour rather than a
  product: links and canonicals are extensionless, so a host that serves
  files literally returns all 43 correctly and 404s on every link on every
  page while every check in the repository still passes.

- The founder's identity is declared content. `site/content/founder.json` holds
  the name, the given name, the job title and the structured-data anchor, and
  the build exposes all four as tokens the way `site.json`'s values already
  are, so the home page's JSON-LD, the about page's heading and prose, the FAQ
  page's answer and two meta descriptions all read from one place. Before this
  a real person's name was written into six source files, outside the content
  model entirely, which meant `rehearse_rebrand.py` could not see it: the
  rehearsal printed REHEARSAL PASSED while the rebranded fixture site still
  named him, with his certifications and employers, in its structured data.
  `python scripts/build_site.py --check` reports 43 identical and 0 differing,
  so the live site is unchanged.
- The rebrand rehearsal now rewrites `founder.json` with a fixture identity
  alongside `site.json`, fails on any name, given name or anchor that survives,
  and counts the job title and the eleven biography strings the way it already
  counts the brand name, reporting which pages carry them. The job title is
  counted rather than failed on because it appears in sentence case inside
  prose a new owner rewrites. Proved by putting the founder's name back into
  one fragment as a literal and confirming the rehearsal fails and names the
  page and the line.

- Three checks stopped passing a tree that is wrong, found by asking each
  check in `verify_site.py` what such a tree would look like. The noindex
  check compared links against a hand written list of spellings that held
  `/404.html` but not `/thank-you.html`, so a link to the thank-you page in
  the spelling a footer is most likely to use was invisible; it now resolves
  each link the way the link checker does. The forbidden markup check held
  `"@type": "Review"` as a literal string, so the same JSON written compact
  passed; it is a pattern now. The JSON-LD mirror check read the first node of
  its type in a graph, so a stale duplicate left behind by an edit was never
  compared; it reads every one and says so when there is more than one. Each
  was proved by mutating a copy of `docs/`, running the previous version of
  the file against it to confirm it passed, and the new version to confirm it
  fails.
- The sitemap check now names two pages that declare the same canonical. It
  already failed on that tree through the arm that reports a sitemap entry
  with no indexed page behind it, which is the symptom rather than the cause,
  and the message sent a reader looking at the sitemap instead of at the two
  pages. Not a hole, a diagnosis.

- The reachability check now walks out from `index.html` instead of
  collecting incoming links. The earlier form asserted each indexed page
  appeared somewhere as a link target, which two new pages that link only to
  each other satisfy while neither can be reached from anywhere a visitor
  starts. Proved on a copy of `docs/` carrying that pair: the check fails and
  names both. A missing `index.html` now fails too, where the old form read
  it as an empty starting set and passed.
- The deploy gate check now reads the deploy job's condition rather than
  looking for the word `pull_request` inside it. `github.event_name ==
  'pull_request'` holds the same word and means the opposite, and an
  `always()` added to the condition leaves the `needs` line in place while
  deploying after a failed check. All three mutations, the inverted
  comparison, the added `always()`, and the deleted condition, were applied to
  the workflow and caught by name, and the workflow restored byte identical.
- Page weight measured across every page and left alone. The home page is
  about 646 KB across 11 files and `solutions` is 555 KB. A naive count reads
  the home page as 2.1 MB by adding the 1.5 MB hero PNG, which no browser
  fetches: it sits behind a `picture` element as the fallback for an 85 KB
  WebP. The remainder is six lazy loaded solution marks below the fold. Re-
  encoding would mean an image library the build refuses to depend on and a
  change to `docs/` that cannot be reviewed without a browser, so nothing
  changed. Recorded so the measurement is not repeated.
- `CLAUDE.md` and `.gitignore` still named absolute paths on this machine, a
  day after the board recorded that nothing did. `CLAUDE.md` was one line
  pointing at a rule file no one else has, so it is now instructions a session
  in this repository can actually follow: read the README, never hand edit
  `docs/`, run the checks either side of a change, nothing installs. The
  `.gitignore` comment names no directory, because the build writes wherever
  `--out` points. The board bullet was too broad and now says what is true:
  nothing a new owner would read or run names this machine, while the board
  and the two history files still cite report paths as records.
- `serve_docs.py` answers a missing path with `docs/404.html` and a 404
  status, which the live host does and the preview did not. The one page a
  new owner most wants to preview was the one page the preview could not
  show them. Found by pointing the new 404 probe at the preview server, which
  reported it; the preview now passes `check_live_deploy.py` with exactly the
  result the live site gives, so the two are equivalent rather than similar.
- `fetch` in `check_live_deploy.py` returned no body for an error response,
  so the 404 probe compared `None` against the page and failed on a correct
  site. An error response's body is the interesting part. It now returns both
  and the two callers that read a missing body test the status instead.
- `check_live_deploy.py` asks the live site for a path no file answers and
  requires `docs/404.html` back with a 404 status. It already exempted
  `404.html` from the extensionless probe on the grounds that a missing path
  is how that page is served, and then never checked it, which is the same
  shape as every other defect found in this tree. The status matters as much
  as the body: a missing path answering 200 tells a crawler the page exists
  and gets every typo and dead inbound link indexed.
- `scripts/check_deploy_gate.py` reads the workflow and confirms the deploy
  job still waits for the verify job, still uploads `docs/`, and still
  refuses pull requests. Every other check reads the built tree; none of them
  reads how that tree reaches the site, and the deploy job is now the only
  route there. Deleting the one line that makes it wait would leave every
  check passing, every run green, and a broken tree shipping on the next
  push, which is the state this repository was in earlier the same day.
  Mutation tested against four edits to the workflow, dropping the `needs`
  line, uploading a different directory, letting pull requests deploy, and
  removing the deploy step; all four fail and name what is wrong. The other
  half of the gate is a repository setting that cannot be read offline, and
  getting it wrong fails the deploy job loudly rather than shipping quietly.
- The guides no longer count the checks. `README.md` and `PERMISSIONS.md`
  said six of six and the workflow step was named for the number, so adding
  one meant finding every place the old count was written down. `check_site.py`
  already printed the count it actually ran.
- The checks now gate the deploy. GitHub Pages published `main` and `docs/`
  on its own, so `verify.yml` ran alongside the go-live rather than in front
  of it and a red run meant a broken tree was already being served. The
  workflow gained a deploy job that uploads `docs/` and needs the verify job,
  and the repository was switched from branch publishing to Actions
  publishing so that job is the only route to the site. A pull request runs
  the checks and deploys nothing. Deploys are serialized and never cancelled
  in flight, because a cancelled one leaves whichever tree was mid-upload.
- `check_live_deploy.py` no longer exempts `CNAME`. It caught the switch on
  the first run against the live site: branch publishing consumed the file and
  returned 404, and the workflow serves the artifact whole, so the exemption
  turned a correct deploy into a failure. It read a 200 there as evidence the
  host was serving files literally, which the extensionless probe added the
  same day proves directly. `CNAME` is now compared byte for byte like every
  other file. The file itself is kept and kept correct so publishing from the
  branch still works if anyone switches back.
- `verify_site.py` has a thirteenth check: every indexed page is linked to
  from some page that is not itself. The existing link check asks whether
  links point at pages that exist, which is the opposite direction. A page
  added to `pages.json` and never put in the nav or a footer builds cleanly,
  resolves, and appears in the sitemap and `llms.txt`, so it would be indexed
  and unreachable at once with every check passing. Self links do not count,
  because each page's nav links to that page. The two noindex pages are
  exempt, and a separate check already requires that nothing links to them.
  Mutation tested on a copy of `docs/` with every link to one page rewritten,
  which fails naming that page.
- Three sentences in the guides were false and are fixed. `SEARCH_SETUP.md`
  said no AI text file is used, which stopped being true when `llms.txt`
  shipped and was never revisited. `README.md` step 1 told a new owner to
  rewrite the three asset filenames in `site.json`, contradicting a sentence
  seven lines later saying all six reach the pages from there. `README.md`
  and `PERMISSIONS.md` both attributed the third-party identifier check to
  `verify_site.py`'s tenth check when it is the twelfth and last, which sends
  a reader chasing the wrong failure. Found by auditing every factual claim
  in the five guide files against the tree; `THEORY.md` and `site/README.md`
  came back clean.
- `scripts/check_live_deploy.py` reads what a visitor actually gets. Nothing
  did before: the checks read the tree about to be deployed, and the workflow
  reports on a commit without gating Pages, which serves whatever is on `main`
  whether anything passed or not. A build can be right, a push can succeed,
  and the site can still be serving last week. It fetches all 43 files and
  compares them byte for byte, and it also fetches the extensionless path of
  every page, because every internal link and canonical in the tree uses that
  form and a host that serves files literally returns all 43 files correctly
  while 404ing on every link on every page. `CNAME` is expected to 404, since
  Pages consumes it. Run against the live site on 2026-09-12: 42 of 42 served
  files identical, 24 extensionless paths resolving to the same bytes.
  Mutation tested against a plain file server on localhost, which reports all
  43 files present, 24 dead links, and `CNAME` served when it should not be.
- `scripts/check_source_only_build.py` is a sixth check and asks whether the
  source is sufficient on its own. Every other check reads a tree that
  already contains `docs/`, so none of them could see that `docs/` was an
  input to its own build; the proof that it no longer is was a measurement
  taken by hand once. This copies `site/` and `scripts/` somewhere else,
  builds there, and requires all 43 files to match `docs/` byte for byte.
  Mutation tested by moving `site/static/styles.css` aside, which fails
  naming the file.
- `THEORY.md` records what the tree needs from a host. Every internal link and
  canonical is extensionless, which GitHub Pages resolves and a literal file
  server does not, so moving the site to an S3 bucket or a default nginx would
  404 on every link while every file was present and every check passed.
- `build_site.py --check` names any file in `docs/` the build did not write.
  It walked the list of files the build produced and compared each against
  `docs/`, which is a check for presence and cannot see a file that stopped
  being generated. A build writes and never deletes, so dropping a page from
  `pages.json` or renaming an image in `site.json` left the old file in place,
  at its old URL, serving the previous owner's content, and every check passed.
  Two places in `README.md` told the reader to delete such a file by hand and
  nothing verified they had. Mutation tested by putting a stray page in
  `docs/`, which the check names and exits 1 on.
- The paths of the machine this site was built on are out of the product.
  `scripts/build_site.py` defaulted `--out` to a directory under this
  workstation's data root, so a new owner running the build with no flags
  either wrote a site somewhere they had never heard of or failed with an
  error naming a drive letter that meant nothing to them. `--out` is required
  now, with an error naming the two real choices, and every caller already
  passed it. `scripts/rehearse_rebrand.py` kept the same kind of default and
  now uses the system temporary directory, which exists everywhere and is
  still outside the repo, so its guard against cloning into the tree is
  unchanged. `site/README.md` told the reader to run the scripts through a
  virtual environment on this machine; they import only the standard library,
  so it says `python` now. `PERMISSIONS.md` no longer declares the old default
  output directory as a path the product writes to.
- `site/README.md` also said a build writes the generated pages plus every
  other file `docs/` carries, copied unchanged. Neither half is true since the
  static files moved out of `docs/` and the stylesheet and script became
  rendered output. It names the 43 files and how each kind is produced.
- The last three images a new owner had to rename by hand are declared values
  now. The hero pair and the band image were written as filenames in
  `site/pages/index.body.frag` and `site/static/styles.css`, so runbook step 2
  told a new owner to edit two files, and the rehearsal could not fail on a
  name they missed. `site.json` declares all six images, the stylesheet and
  the script are rendered through the same token substitution as a fragment
  rather than copied, and the rehearsal renames all six. 18 declared values,
  zero residue in a rebranded clone. Mutation tested by restoring one literal
  filename to the stylesheet, which fails with the file, the line and the
  value named.
- Rendering the stylesheet made it output, so `--check` compares it. The byte
  comparison covered the 29 generated files and nothing else, which left a
  third of the published tree unverified. It compares all 43 now, including
  the images. Mutation tested by adding one space to `docs/styles.css`.
- The stylesheet, the script and the twelve images moved from `docs/` to
  `site/static/`, which was the last source living inside the build output.
  The build had been walking `docs/`, skipping what it had just generated and
  copying the rest, which made the output directory an input to its own build.
  Two things followed from that and both are gone. A clone without `docs/`
  built 29 files and no stylesheet, script or images, and said nothing was
  wrong: it printed that there was nothing to copy because it wrote into the
  directory it reads them from, which was false in that tree. And a hand edit
  to `docs/styles.css` survived every rebuild while `README.md` said, in its
  first paragraph, that `docs/` has no exceptions and a hand edit there is
  overwritten. That sentence is true now. The same clone builds 43 files.
- `docs/` is byte identical, so the live site is untouched, and a build into a
  scratch directory reproduces all 43 files exactly.
- Moving the images exposed a gap in the rebrand rehearsal. Its runbook step 2
  renamed the three declared images inside `docs/assets/`, which is the copy
  rather than the source, so after the move the next build would have put the
  previous owner's filenames straight back. It renames the source now and
  deletes the stale copy, and a new scan fails on any file in the rebranded
  tree still named for one of the old images. A declared value can survive as
  a filename as well as as a line of text, and the residue scan reads content
  only, so nothing would have caught the previous owner's logo sitting in the
  tree under its own name. Mutation tested: leaving the stale copy fails the
  rehearsal and names all three files.
- `WORK_BOARD.md` split at 268 lines, against the 200 line threshold at which
  a board stops being read. The 132 lines of completed work in In Progress
  moved verbatim into `BOARD_ARCHIVE_2026.md`, which leaves the board at 144.
  Three things were carried across rather than archived with the bullets that
  stated them, because each is a standing decision a fresh thread would
  otherwise reopen: that `THEORY.md` stops above 60 lines on purpose, that a
  push to `main` runs the checks on a clean machine without gating the deploy,
  and that the buyer read is a finished record rather than a repeatable task.
  Read for buried questions, the archived sections held one, the service page
  copy read, and it was already on the board as COPY-SERVICE.
- `THEORY.md` cut from 107 lines to 88. The standard is 60, and the file had
  grown every time a session learned something. The test applied per bullet
  was whether it states a constraint a session could break without noticing,
  or restates something a check now enforces and prints on failure. Four
  things went for the second reason: the list of what `site.json` declares,
  which is the file itself; that the contact strings are never reformatted;
  that `404.html` and `thank-you.html` are the only `noindex` pages; and that
  `login.html` carries no tracking tags. The JSON-LD mirroring rule went too,
  because the check fails any page carrying JSON-LD that no table covers, so a
  new page cannot be authored past it silently.
- The rest of the cut was narrative and counts: how each defect was found now
  lives here rather than there, and the occurrence counts, 166 for the domain
  and 50 for the tagline, were dropped because a number in a file nothing
  recomputes goes stale without anyone noticing. It stops at 88 rather than
  60. Everything left states something no check can see, and cutting further
  would mean removing a live constraint to reach a number.
- A new check reads `docs/CNAME`, which no check read before. The identity
  check scans `.html`, `.xml` and `.txt`, and CNAME has no extension, so the
  one file GitHub Pages reads itself to decide which domain serves the tree
  was the only file in the output nothing verified. It must name the declared
  host and end in a single bare LF, because Pages reads it literally and a
  CRLF makes the host a different string. Mutation tested both ways.
- Read the remaining six checks for the same defect class and found nothing
  worth adding. Recorded why rather than leaving it looking unexamined: a
  canonical pointing at the wrong page is already caught, because
  `sitemap.xml` is generated from `public_pages.json` independently of the
  canonicals the check compares it against, so the two disagree. The
  forbidden-claims check is a fixed list of strings and cannot be made to
  read prose. The link check skips external URLs, and fetching them would
  make the run depend on other people's servers.
- A new check: the phone number is one number everywhere. `site.json`
  declares the phone three times, as it is displayed, as a `tel:` URI and in
  the form schema.org wants, and nothing made the three agree. A new owner
  who changed the displayed number and missed the other two would have
  published a site showing their own number with every Call button dialling
  the previous owner, and all ten checks would have passed. The visible text
  check cannot see it, because a `tel:` href is an attribute rather than
  text. The check compares the digits of the three declared forms and every
  `tel:` link in the tree against the declared one. 60 Call links checked.
- The identity check now reads the two social profiles. Their hosts were
  allowed, which proved nothing about whose account they were: `tools.html`
  links seven repositories under the declared GitHub account and
  `resources.html` links GitHub's own documentation, so the host is allowed
  for reasons unrelated to the profile. Every URL on a profile's host must
  now sit under the declared profile, and each profile must be linked from
  somewhere, so a page left pointing at the previous owner's account fails.
- Mutation tested all four arms: a `tel:` URI that dials a different number
  from the displayed one, a page whose Call link disagrees with the declared
  URI, a repository link under another account, and a declared profile linked
  from nowhere. Each fails with the file and the value named.
- `login.html` is generated now. It was a hand-authored source file living
  inside `docs/`, the build output, which is the one place the project's own
  rules say source never goes. A rebrand reached it only through a list of
  substitutions written out by hand in `rehearse_rebrand.py` and repeated as
  step 3 of the README runbook, and nothing failed when either fell behind.
  It now lives at `site/pages/login.page.frag` and is rendered through the
  same token substitution as every other fragment, without the shared chrome
  it has never had. `docs/login.html` is byte identical.
- Added `{{SITE_APEX}}` and `{{FAVICON_FILENAME}}`, the two values that page
  needed and no other fragment had asked for. The apex is the domain without
  its `www`, which reads as prose in the link home and was the substitution
  easiest to forget.
- Dropped `rewrite_login` from the rehearsal and step 3 from the runbook.
  Mutation tested by restoring the literal domain in the link home: the
  rehearsal names the value, the file and the line, and exits 1. What the
  rehearsal proves is larger for the removal, because it no longer rebrands
  that page itself before measuring whether the build did.
- Tokenized 48 hard-coded identity values across 13 fragments. The phone
  number, the mailing address, the LinkedIn and GitHub profiles and the logo
  filename were written as literals in the page bodies while only the footer
  and the utility bar used the tokens, so a new owner who changed
  `site/content/site.json` published a site showing the previous owner's
  phone number on eleven pages and address on three, and linking to their
  profiles from every page. Measured against a rebranded clone, not
  inferred. `docs/` is byte identical before and after.
- The build now resolves tokens in `site/content/pages.json` too, which let
  the tagline in the homepage H1 and the `og:description` come from the
  declared value. The JSON-LD postal address is derived from the one
  declared string by `address_parts` rather than declared a second time in
  four schema.org fields.
- Widened the rehearsal's residue scan from the domain alone to all fifteen
  values a new owner replaces, and gave the fixture the two social URLs it
  never changed. That gap is why the profiles read as clean: the scan was
  not looking and the fixture was not changing them. Mutation tested by
  restoring one literal phone number, which the scan reports by value and
  line and which fails the rehearsal, `check_site.py --full` and the
  workflow.
- The Formspree endpoint is declared once now. It was in
  `site/content/site.json` and hard-coded again in
  `site/pages/contact.body.frag`, so a new owner who changed the declared
  value, as `THEORY.md` and the runbook both told them to, got a contact form
  still posting to the previous owner's inbox. Two of the three third-party
  values were already tokenized; this was the one that was missed. The
  fragment now carries `{{FORMSPREE_ENDPOINT}}` and the build resolves it.
  `docs/` is byte identical before and after.
- The failure was loud rather than silent, which is why it was still here:
  changing only `site.json` fails the identity check with "the declared
  Formspree endpoint appears 0 times, expected 1". Nothing shipped wrong.
  What was wrong was the claim that the value lived in one place.
- Extended `rehearse_rebrand.py` to rebrand the three `third_party` values
  too, so the claim is tested rather than asserted. Mutation tested by
  restoring the hard-coded endpoint: the rehearsal prints REHEARSAL FAILED
  and exits 1, which fails `check_site.py --full` and the workflow.
- Corrected step 7 of the grant runbook in `PERMISSIONS.md`. It told a new
  owner to put the endpoint in `docs/contact.html`, which is build output the
  next build overwrites.
- Added `.github/workflows/verify.yml`, so the checks run somewhere that is
  not the author's laptop. Every push and pull request runs the five checks,
  then the rebrand rehearsal, on a clean Linux machine. It adds one check
  that did not exist: `docs/` must be byte identical to what the build
  produces, where `check_site.py` proves only that it renders identically.
  Mutation tested by inserting one space before a `</body>` tag, which the
  render check passes and the byte check fails. Nothing in it gates the
  deploy; Pages publishes from `main` and `docs/` either way.
- Cut `THEORY.md` from 95 lines to 87 by removing what the checks already
  enforce in their own output and the incident narrative this file now
  carries. It is still over the 60 line standard, and the remainder was not
  cut because every bullet left is a constraint a session could break
  without noticing.
- Added `.gitattributes`, so line endings are a property of this repository
  rather than of whoever clones it. The tree had none, and this working copy
  set `core.autocrlf` locally, which is why the CRLF invariant held here and
  nowhere else. Measured on a clone with `core.autocrlf` unset, which is what
  Linux, macOS and most CI runners give you: checkout produced LF, the build
  wrote CRLF, and a rebuild that changed nothing produced a 1700 line diff
  across 26 files with all five checks passing. A clone on this machine
  produced `docs/CNAME` with CRLF, and GitHub Pages reads that file itself to
  resolve the custom domain. The live site was never affected, because Pages
  reads the stored blob rather than a working copy. Verified after the fix:
  the same clone rebuilds to an empty diff, `CNAME` stays one bare LF, and
  all 12 binary assets hash identically to this tree. Stored blobs are
  unchanged, `git add --renormalize` stages nothing.
- Gave `scripts/check_site.py` a `--full` flag that adds the rebrand
  rehearsal as a sixth check. The repository proved two different things
  with two different commands, and only one of them was the command a
  reader is told to run. The rehearsal stays off the default path because
  it clones the tree outside the repo and takes about a minute, which is
  worth waiting for when the build or the content model changes and not
  worth making every deploy wait for. Verified that a failing rehearsal
  fails the run.
- Fixed a gap in the link check. It matched `href` and `src` only, so the
  home page hero, which is offered as a webp through a `srcset` with a png
  behind it, was never checked. A renamed or deleted webp would have shipped
  as a broken image to every browser that prefers the format while all ten
  checks passed. Both scans now read srcset candidates, which took the link
  count from 1190 to 1191, and the check fires when the target is renamed.
- Rewrote the README opening after a cold read of the repository found that
  the most important fact arrives 43 lines too late. A reader who stops
  after the quick start does not yet know `docs/` is generated output, so
  the first thing they edit is the thing the next build overwrites. That
  paragraph is now the third one on the page.
- Corrected two things the runbook got wrong or left out. The hero is two
  files rather than one, and step 4 sent the reader to find the nine
  mirrored pages in the checker's source instead of naming them.
- Made the build say what it counted. It reported 28 pages written when 24
  are pages and four are `CNAME`, `robots.txt`, `sitemap.xml` and
  `llms.txt`, and it reported copying zero static files during an in-place
  rebuild without saying why that number differs from the usual 15.
- Added `scripts/rehearse_rebrand.py`, which turns the reproducibility
  claim into something the repository re-proves on demand. It clones the
  tree to the data root, rebrands it to a fixture business by the runbook's
  three mechanical steps, rebuilds, runs all fifteen checks, and fails if a
  single occurrence of the old domain survives. Mutation tested by removing
  one `{{SITE_URL}}` token from a fragment: the run fails and names the
  file and line that kept the old domain.
- Audited every claim in `THEORY.md` against the tree and rewrote it. One
  was wrong: the line-ending invariant named `docs/CNAME` as the only file
  that is not CRLF, and three more at the repo root are pure LF. Two were
  stale, describing a drift check that can no longer fail and a generated
  file set that has since grown. The file went from 98 lines to 88 by
  removing repetition rather than constraints, which is still over the
  framework's 60-line guidance; what is left is load-bearing, and cutting
  further would mean dropping something a session needs to know.
- Added a make-this-site-yours runbook to `README.md`: six ordered steps
  covering the declared values, the images, the one hand-authored page, the
  copy, the rebuild and the hosting setup, ending in the checks that prove
  the result. The steps were rehearsed against a clone rather than reasoned
  about. A fictional business replacing every declared value reaches a tree
  that passes all ten checks and names the previous owner nowhere.
- Made `python scripts/build_site.py --out docs` rebuild the published tree
  in place. The static-file copy raised when a file was its own destination,
  so there had been no supported way to regenerate `docs/` without a
  scratch directory and a manual copy back.
- Widened the declared-identity check to hostnames written as prose rather
  than inside a URL. The rehearsal found one: the link back to the home page
  on `login.html` names the domain in lowercase with no `www`, so a rebrand
  that fixed every href would still have shipped a page sending readers to
  the previous owner's site. Mutation tested on the rehearsal clone, where
  it is the only failure the tenth check reports.
- Fixed the contact-details check, which had one arm comparing nothing. Its
  near-miss patterns were written out beside the values they check, so they
  would have gone on looking for a previous owner's phone number after a
  rebrand and passed on an empty set. They are now built from the declared
  strings, a pattern that matches nothing anywhere in the tree is reported as
  a failure, and the site URL arm compares the displayed host rather than the
  full URL, which never appears as visible text. That arm had been checking
  zero occurrences; it now checks two. Mutation tested on a reformatted phone
  number, a recased host and 'Dr' expanded to 'Drive'; each one fires, and so
  does removing the phone number from every page.

- Made the domain a single value. Canonicals and og:url are stored in
  `site/content/pages.json` as site relative paths that the build prefixes;
  the JSON-LD and body fragments carry `{{SITE_URL}}` and `{{SITE_HOST}}`;
  and og:image, its alt text and the favicon href, which were identical on
  all 24 pages, are derived from `site.json` rather than stored 24 times.
  Nothing under `site/` spells the domain out except `site_url`. The build
  stayed byte-identical throughout.
- Stopped listing the site's own host among the allowed external hosts in
  `site.json` and derived it from `site_url` instead. Measured by rebuilding
  against a fictional domain: 166 occurrences follow the one value, the
  hand-authored `docs/login.html` is the only file left behind, and
  `verify_site.py` now fails on it instead of letting the stale domain ship.

- Generated `docs/CNAME`, `docs/robots.txt`, `docs/sitemap.xml` and
  `docs/llms.txt` from the content model instead of copying them across.
  The domain now comes from `site/content/site.json` and the public page
  list from the new `site/content/public_pages.json`, which both the sitemap
  and llms.txt are built from, so the two cannot disagree about which pages
  the site has. The build is byte-identical to the shipped tree, 28 of 28.
- Ended the `llms.txt` drift hazard rather than continuing to report it.
  Each line now carries the page's own meta description, taken from the same
  field the page is rendered from. `scripts/check_llms_drift.py` is kept as a
  second opinion but can no longer fail.
- Mutation tested the four generated files by rewriting the site URL to a
  fictional domain and changing one meta description. CNAME, the robots
  sitemap line, all 23 sitemap locations and the changed llms.txt line all
  followed, with zero occurrences of the old domain in any of the four.
- Declared the site's identity in `site/content/site.json`: brand name,
  tagline, site URL, logo filename, the three contact strings, the Cloudflare
  beacon token, the Scarf pixel id, the Formspree endpoint, the social URLs,
  and an allowlist of every external host the tree may reference with the
  reason each is there. `build_site.py` renders the chrome from those values
  and refuses to finish a page that still holds an unresolved placeholder.
- Added a tenth check to `scripts/verify_site.py`. The third-party
  identifiers in a built tree must equal the declared ones at the expected
  count, and no file may reference a host outside the allowlist. Its contact
  strings and site prefix now come from the same file instead of being
  hard-coded, so the checks cannot keep validating a previous owner's values
  after a rebrand. Mutation tested against a wrong beacon token, a stale form
  endpoint, an unlisted host and a changed phone number; each one fires.
- Added `PERMISSIONS.md`, the rollup of everything the site needs to build,
  deploy, and serve: runtime, filesystem paths, every outbound host and which
  page causes it, the operator accounts that hold credentials, the DNS
  records, a from-scratch runbook, and the verification to run afterwards.
  It records that the repository holds no secrets and that the build scripts
  import only the standard library.
- Removed `docs/hosting.md`. It was an internal operations note living inside
  the published site, so it was served at a live URL while appearing in no
  sitemap and no navigation. Its content is in `PERMISSIONS.md` now.
- Made `docs/` generated output. `site/` holds the content model and one
  canonical template per piece of chrome, and `scripts/build_site.py` renders
  the 24 generated pages from them. Changing the nav or the footer is now one
  edit rather than 14. The 28 stored chrome formatting variants are gone, and
  `docs/login.html` is unchanged because it shares no chrome with any page and
  carries the tree's only CSP.
- Added `scripts/compare_render.py`, which compares two directories of pages as
  rendered documents rather than as bytes: tag order, attributes as an
  order-insensitive mapping, comments, and whitespace-collapsed text. It was
  the acceptance test for the reformatting, since reindenting chrome changes
  bytes on purpose. It reports a page present in one directory and not the
  other as a difference, which it did not do until that case was tested by
  deleting a page from a copy and watching it exit 0.
- Hardened the generator. It validates every content-model entry before
  rendering, naming the page and the offending field instead of failing with a
  bare KeyError; it escapes values interpolated into titles and attributes,
  using a narrower escape than the standard library's quoted mode, which
  rewrites the apostrophe six page titles carry; and a build now copies every
  file `docs/` carries that it does not generate, so the output is a complete
  deployable tree rather than pages alone.
- Verified four ways. `build_site.py --check` reports 24 of 24 pages identical
  to `docs/`, `verify_site.py` passes 9 of 9 checks, `check_llms_drift.py`
  reports no drift, and the full built tree compares byte-identical to `docs/`
  across all 44 files. Every new check was tested by mutation against a scratch
  copy rather than by its own passing run.

## 2026-09-11

- Added `scripts/verify_site.py`, one command that verifies a built site
  tree without knowing its history. Eight checks: internal links resolve,
  each page has one title, one description and at most one canonical, the
  sitemap matches each page's own canonical, `llms.txt` covers the same
  page set with descriptions that have not drifted, only `404.html` and
  `thank-you.html` are noindex and neither is linked, the phone number,
  address and site URL appear character for character, `login.html` carries
  no analytics while every other page carries both tags, and no ratings
  markup or Qualified Security Assessor claim exists anywhere. It takes
  `--dir` so it can verify a generated build as well as `docs/`, and exits
  non-zero on any failure. All eight pass against the current tree, which
  proves little on its own, so they were tested by mutation against a
  scratch copy in the data root: a broken internal link, a reformatted
  phone number, a drifted `llms.txt` description and an injected Review
  type were each caught. Not yet merged to `main`; it sits on
  `feature/repro-generator` with the generator work.
- Verified the Nashville change on the live site after the GitHub Pages
  deploy. `/contact`, `/about` and `/service-fractional-leadership` each
  serve the new title and meta description and the matching JSON-LD copy,
  two occurrences per page, and the live `llms.txt` carries the three
  updated lines. The first check was written badly and passed on the word
  Nashville alone, which every page already carried in its utility line, so
  it was replaced with a check on the exact new strings.
- Added Nashville to the title and meta description of `contact`, `about`
  and `service-fractional-leadership`, and to the JSON-LD `name` and
  `description` that mirror them on those pages. Nashville had appeared only
  in the per-page utility line, the postal address, the 2022 award line and
  the teaching mention, and in no title, description or H1 anywhere on the
  site. The fractional page's JSON-LD `name` and `serviceType` were left as
  "Fractional CIO and CISO leadership", because they name the service and
  not the page. The about description drops "teaching," to stay inside the
  display length; that credential is still in the page body and the awards
  list. `docs/llms.txt` was regenerated by `scripts/check_llms_drift.py
  --fix` for the three changed descriptions and the check reports 24 lines,
  0 drifted.
- Decided by Jon, closing board question 1. Tectori stays nationally
  targeted. No location pages, no LocalBusiness schema, no Nashville
  modified keyword targets, and the nationwide wording on all 24 pages
  stands. The three pages above are a deliberate exception so the city
  appears in some keyword bearing fields. The question reopens only if the
  Search Console export shows real local query volume.
- Trimmed `WORK_BOARD.md` from 184 lines to 102. The Current state records
  were archived verbatim to `BOARD_ARCHIVE_2026.md` under a 2026-09-11
  heading, and the live facts a session still needs were carried forward:
  the deploy path, the spent remediation brief, the drift check rule and the
  targeting decision. Owner-only tasks, the queue and the remaining
  questions were left as they were.
- Recorded in `THEORY.md` that a page's JSON-LD name and description repeat
  its visible title and meta description, so the two change together. The
  first attempt at this change edited only the visible tags and would have
  left every page describing itself two ways.

## 2026-09-10

- Verified the tagline change on the live site after the GitHub Pages deploy.
  The homepage H1 reads "Audit-ready IT that scales with your ambition.", the
  eyebrow reads "Built to be reviewed", `og:description` matches the tagline,
  and the footer line is correct on `/about`, `/services` and `/contact`. The
  old line returns zero matches on all six pages checked. SEO-17 is live too:
  the deployed meta description, the llms.txt summary and the llms.txt `/`
  entry all carry the new audience wording.

- Replaced the brand tagline across the site. "IT that holds up under audit and
  scales with your ambition." became "Audit-ready IT that scales with your
  ambition." in all 50 places it appears: the footer line and the social image
  alt text on each of the 24 content pages, 48 occurrences, and two more in
  the homepage H1 and its `og:description`. `login.html` never carried it. Jon
  chose the new line and chose to change it everywhere rather than on the
  homepage alone, so the site states one tagline instead of two.
- Changed the homepage eyebrow from "Audit-ready technology" to "Built to be
  reviewed", because the H1 directly below it now opens with "Audit-ready" and
  the first screen would otherwise say the word twice in two lines.
- Merged SEO-17 after review. The homepage meta description and hero paragraph
  now name "regulated and growing organizations," the audience the page's
  Organization schema has always described, and the description uses "governed
  AI," the site's own term, in place of "responsible AI work." The pre-push
  review raised only its recurring objection to a data-root path in the
  changelog, which CORE-01 requires, so it was rejected.

## 2026-09-09

- Completed SEO-18 content depth work: added a compact homepage buyer-path
  section for exam readiness, cloud review, fractional leadership, and AI
  governance. The approximate homepage word count rose from 605 to 766;
  copy-review and verification artifacts live under
  `C:\Code_data\tectori\seo18_content_depth_2026-09-09\`.
- Wired the public contact form to the live Formspree endpoint and removed the
  placeholder language from Contact and Privacy. The site stays on plain HTML
  form POSTs, which matches the GitHub Pages hosting model without adding a
  JavaScript dependency. The pre-push review follow-up made the honeypot input
  explicitly hidden to assistive technology and added the phone fallback to the
  Accessibility report path.
- Fixed the measured 390px mobile hero clipping residual on the homepage,
  Solutions and Contact by tightening the shared mobile hero layout and
  full-width button behavior. Browser verification covered 390x844, 768x1024,
  1366x768 and 1920x1080, with artifacts under
  `C:\Code_data\tectori\stats\mobile_hero_form_2026-09-09\`.
- Ran the pre-push review over `origin/main..HEAD`. The first pass produced two
  useful Formspree/accessibility follow-ups, both fixed above. The rerun's
  remaining extensionless URL concern was rejected after all sitemap URLs on the
  live GitHub Pages site returned 200. Review logs and the live URL check live
  under `C:\Code_data\tectori\reviews\`.
- Merged `feature/board-2026-09-06-site` into `main` and pushed `main` to
  origin on Jon's explicit go-live approval. GitHub Pages deploys from `main`
  and `docs/`.
- Refreshed the two stale `docs/llms.txt` page descriptions for `/privacy`
  and `/accessibility`. Both lines were generated before the Formspree form
  landed and before the Accessibility report path changed, so the privacy
  line still told LLM crawlers the site had no forms that transmit data.
  Each line is now regenerated from that page's own meta description, and a
  re-check of all 23 described pages shows zero remaining drift.
- SEO-17: named the homepage's audience the same way its Organization schema
  always has. The schema said "regulated and growing organizations" while the
  meta description said only "regulated organizations" and the first
  paragraph of body copy said "the business," so the growth buyer who is not
  yet audited had nothing to recognize on the page they land on first. The
  description also moved from "responsible AI work" to "governed AI," the
  term the site already uses ten times across nine pages. The title tag, the
  H1 and the eyebrow are unchanged: the H1 is the brand tagline repeated in
  the footer and social image alt text of all 25 pages, so rewording it is a
  brand decision rather than a keyword one. The proposal and the term
  analysis live at
  `C:\Code_data\tectori\seo17_keyword_signals_proposal_2026-09-09.md`.
- Added `scripts/check_llms_drift.py` so the `llms.txt` drift that was fixed
  above cannot recur unnoticed. `llms.txt` copies every page's meta
  description with no generator behind it, so it goes stale silently whenever
  a description changes. The script compares all 24 copied lines, the 23 page
  entries plus the file's summary paragraph, against the pages and exits
  non-zero on any mismatch. `--fix` rewrites the drifted lines from the pages
  themselves. The summary paragraph was added to the check after the first
  real use found it holding a second stale copy of the homepage description.
  README documents the script under Layout.
- Sent successful contact form submissions to a Tectori confirmation page
  instead of the generic Formspree page. `docs/thank-you.html` is new, built
  on the 404 template, marked `noindex, follow`, and deliberately absent from
  `sitemap.xml` and `llms.txt`. The form gained a `_next` hidden field. The
  site keeps its plain HTML POST with no JavaScript dependency.
- Replaced the entity-encoded displayed phone number with plain characters.
  All 57 occurrences across 23 pages used `&nbsp;` and `&#8209;`, so a
  visitor copying the number received U+00A0 and U+2011 rather than a space
  and a hyphen, which some dialers and CRM fields reject. Each occurrence is
  now `(615) 829-6802` inside a `nowrap` span, so the rendered result and the
  line-break behavior are unchanged and the copied text matches the written
  number exactly. Every `tel:` link was already correct and is untouched.

## 2026-09-08

- Cleaned and reorganized `WORK_BOARD.md` for the lane run: removed stale
  dispatch-era detail from the live Pending section, recorded the 2026-09-08
  ISKPRO audit review, added SEO-17 and SEO-18 for the two audit findings not
  already covered, and kept the board under the active-work surface limit.
- Dispatched and closed the eight lane sessions from
  `C:\Code_data\tectori\lanes\PROMPTS_2026-09-06.md`. Lane outputs landed under
  `C:\Code_data\tectori\lanes\out\` and status files under
  `C:\Code_data\tectori\lanes\status\`.
- Built the SEO site lane on `feature/board-2026-09-06-site`, unpushed and not
  merged: address and Organization PostalAddress, longer meta descriptions,
  Scarf style cleanup, `llms.txt`, image weight reduction and lazy loading,
  richer Person JSON-LD, canonical JSON-LD IDs, root home links, on-page audit
  residue, Formspree placeholder contact form, existing social profile links,
  and extensionless public URLs. The copy/spec log is
  `C:\Code_data\tectori\lanes\out\LANE_1_SPECS_2026-09-06.md`.
- Wrote non-repo lane deliverables: Google Business Profile checklist, link
  earning plan, measurement routine and export spec, positioning recommendation,
  keyword intent map, competitor gap list, content plan, backlink channel
  classification, social channel decision, before-crawl results, and LinkedIn
  copy packs.
- Folded lane reports back into the board, cleared the active thread marker,
  removed the lane dispatch table, and added the measured mobile hero clipping
  residual as a pre-merge candidate. Nothing was pushed; merging to `main`
  remains the go-live gate.

## 2026-09-06

- Scored every unshipped item on the board and in the remediation brief with
  `ai_development/docs/board-scoring.md`, 31 items, `--strict` clean. Added a
  `## Scored index` to the top of the remediation brief so the brief's SEO
  features carry blocks, archived the shipped work, closed research and
  decision records to `BOARD_ARCHIVE_2026.md`, and rewrote the board as
  Current state, In Progress, Pending and Questions for Jon. The developer
  review list is at `C:\Code_data\tectori\board_review_2026-09-06.md`.
  Nothing under `docs/` changed and nothing moved on the strength of a score.

- Grouped the 31 scored items into eight lanes that can run concurrently and
  wrote one dispatch brief per lane under `C:\Code_data\tectori\lanes\`, with the shared
  rules in `LANE_RULES_2026-09-06.md`. Only Lane 1 writes to this repo; the
  other seven read it and write to the data root, which is what makes eight
  concurrent lanes safe. Recorded the run decisions in a Lanes section on the
  board: nothing is pushed, Formspree for SEO-16 with a placeholder form ID,
  SEO-15 deferred, SEO-13 limited to the two profiles already in the tree.

## 2026-09-03

- Researched the 2026-09-03 SEO sales call before any site change. Seven
  reports under `C:\Code_data\tectori\seo_research_2026-09-03\`. The
  vendor's 14.5 second load is real for the homepage on simulated slow
  mobile only (median 14.0 s, image weight); every other page loads in
  2.4 to 3.4 s. The 9 percent duplicate content reproduces at 8.6 percent
  and is the designed hub summaries. Backlink, keyword and traffic claims
  stay unconfirmed until the Search Console export lands. Google's policy
  text was captured verbatim from dated Wayback snapshots. No file under
  `docs/` changed. Decisions recorded on the board; remediation follows
  the 2026-09-05 remediation brief, four releases.

## 2026-08-30

- Built the Evidence Readiness Baseline as a manually delivered,
  fixed-scope service offer. One examiner request, customer diligence cycle,
  business process, system, or security-program area defines the review
  boundary. The offer checks an agreed sample for named owners and current
  operating records, then separates verified, missing, stale, and unassessed
  items.
- Added the offer to `docs/service-compliance-risk.html` with its three-step
  public path, deliverables, limitations, and contact link. It assigns no
  maturity score and makes no audit, assessment-opinion, certification, or
  legal-advice claim.
- Added a bridge from `docs/tools.html` so the free Security Program Templates
  remain ungated while buyers who need their records checked can reach the
  fixed-scope offer. No commercial promotion was added to a client
  deliverable.
- Wrote the delivery brief at
  `C:\Code_data\tectori\EVIDENCE_READINESS_BASELINE_OFFER_2026-08-30.md` with
  scope, delivery flow, deliverables, exclusions, intake questions, and pilot
  acceptance criteria. Price, duration, and sample size stay unset until a
  manually delivered pilot provides evidence for them.
- Updated only the Tools and Compliance and risk management sitemap dates to
  2026-08-30. No page, navigation item, style, script, analytics service, or
  client claim was added.
- Verified both changed pages locally. They return 200, all local references
  and the cross-page fragment resolve, JSON-LD still parses, IDs remain unique,
  and the browser console is clean. At 1920, 1366, and 390 pixels the new
  content has no horizontal overflow; the three offer steps stay in one row on
  desktop and laptop and stack at phone width. Nothing was pushed or deployed.

## 2026-08-29

- Completed market and offer research on Certified Information Security's
  free assessment platform. The useful lesson is its low-friction progression
  from a capable free asset to short paid labs and larger training, not its
  assessment design. Tectori should preserve its operating-evidence,
  explicit-coverage, and no-certification distinctions.
- Added a service-offer backlog item for a fixed-scope, practitioner-led
  Evidence Readiness Baseline. The supporting content candidate is an original
  `A score is not evidence` article or worksheet. No public-site or Fortivra
  change was made or approved. The research note is at
  `C:\Code_data\tectori\certified_information_security_assessment_positioning_2026-08-29.md`.

## 2026-08-24

- Shipped a branded 404 page. `docs/404.html` did not exist, so GitHub Pages
  served its own unbranded 404 to anyone hitting a stale or mistyped link. The
  page reuses components already shipping, carries both analytics tags like
  every other public page, and routes the visitor to Services, Free tools, or
  Contact. It is noindex and follow, out of `sitemap.xml`, and out of the
  navigation. Its links and assets are root-absolute, because Pages also serves
  404.html for deep paths and relative paths would resolve against the missing
  directory and render the page unstyled. Confirmed live: a request to a deep
  missing path returns 404 and the served body matches the repo copy once line
  endings are normalized.
- Added JSON-LD structured data to the nine pages that had none. Each
  `service-*.html` page gained a `Service` node and a `BreadcrumbList` of Home,
  Services, this page. `services.html` gained a `CollectionPage` whose
  `mainEntity` is an `ItemList` of the six services in page order, plus its own
  `BreadcrumbList`. `about.html` gained an `AboutPage` with a `Person` node for
  the founder, and `contact.html` a `ContactPage`. Jon chose the shape on
  2026-08-24, including having about.html declare its own Person at
  `about.html#person` so `index.html` did not have to change.
- Every node references the organization by `@id` at
  `https://www.tectori.com/#organization` rather than repeating it, matching
  the convention `index.html` set. Every value comes from that page's own
  title, meta description, or visible text. No `Review`, `AggregateRating`,
  `offers`, price, or testimonial markup appears anywhere, because the site
  claims no client results and `case-study.html` says so explicitly.
- Verified by extracting and parsing every `application/ld+json` block across
  `docs/`, in the repo and again from the live site: eleven pages carry a
  block, all parse, none has two, no `@id` conflicts with its page canonical,
  and every file is still CRLF. Two pre-existing gaps outside this release were
  found and deliberately left alone: `faq.html`'s `FAQPage` and the
  `index.html` founder `Person` carry no `@id`.
- Insert only. No styles, scripts, navigation, footer, or prose changed, so the
  cache versions stay at `v=20260822` and `v=20260820`. Merged to main at
  9cd55be and confirmed live on www.tectori.com, with all nine pages matching
  their repo copies byte for byte once line endings are normalized.

- Shipped the content release. Eight new pages: six individual service pages,
  one per service line, plus a Resources page and a Trust page. Jon chose the
  hub shape, so `services.html` keeps all six anchored sections exactly as they
  were and each one now links out to its page. No existing anchor link breaks,
  which matters because GitHub Pages has no redirects.
- The six service pages follow one template: hero, who this is for, what the
  work includes, deliverables expanded a line each, how it supports audit
  readiness, what the service line is not, and a call to action. The what it is
  not block is new to the site and states the boundary in public, for example
  that the compliance service line prepares for the assessor and does not issue
  an opinion, and that cloud architecture is not a managed service.
- Every claim on the six pages traces to text already on `services.html`.
  Nothing new was asserted about experience, clients, or results.
- Resources indexes what already exists rather than adding assets. Three
  reading paths by situation, a pointer to Free tools rather than a second copy
  of it, and a fourteen term plain-language glossary of the vocabulary the rest
  of the site uses.
- Trust states how the practice itself operates, since the site claims no
  client results anywhere. Who you are engaging, where engagement material
  lives and when it is returned or destroyed, the practice's own security
  controls, the three third parties this site uses with privacy.html carrying
  the detail, and how to report a problem. Jon confirmed each of those facts on
  2026-08-24; none were inferred.
- Navigation: Resources and Trust are footer only, on Jon's call. The top
  navigation stays at nine items. Privacy, Terms, and Accessibility set that
  precedent. The footer on all fourteen existing pages gained both links.
  `login.html` has no footer and was not touched.
- `docs/sitemap.xml` gained the eight new pages and every changed page's
  lastmod moved to 2026-08-24. The login.html entry kept 2026-08-20 because
  that page did not change.
- No styles or scripts changed, so the cache versions stay at `v=20260822` and
  `v=20260820`. The new pages reuse layout components already shipping on
  services.html and audit-ready-it.html, so no new CSS was needed.
- No third party resource was added or removed anywhere, so `docs/privacy.html`
  needed no change in this release.
- The pre-push review raised five findings. One was real and pre-existing, the
  `docs/solutions.html` footer omitted its own Solutions link, now fixed. The
  README layout section gained a line for the new pages. The rest were the two
  known false positives plus checks that passed on inspection: canonical and
  og:url match on every page, and privacy.html already reads "Every page except
  the client login page", which covers the new pages without a change.
- Merged to main at b46c238 and confirmed live on www.tectori.com. All eight
  new pages return 200 and match the repo copies byte for byte once line
  endings are normalized. The six services.html anchors still resolve.

## 2026-08-23

- Brought the About and Home copy in line with the current resumes. The stated
  experience count moved from 19 years to 20 years in four places, the About
  meta description, the founder paragraph, the About statistic tile, and the
  Home proof strip. All five resumes state 20 plus years.
- Added a paragraph on the HCA Healthcare security architect and AI automation
  role to the founder narrative, the most recent employment and the closest one
  to the work this site sells. It carries the same sentence the Ncontracts
  paragraph uses, that the company is part of the work history and is not
  represented as a Tectori client.
- Added two items to the credentials list, SANS SEC545, GenAI and LLM
  Application Security, 2026, which supports the AI governance pages and
  appeared nowhere on the site, and the 2022 Nashville Security Leader of the
  Year Top 3 finalist recognition. The PCI internal assessor entry now names
  where it was held, Ingo Money, and keeps the name PCI SSC issues, Internal
  Security Assessor. The list label widened to cover training and recognition.
- Corrected the boot camp school list to match the resumes: Vanderbilt,
  Columbia, NYU, the University of Pennsylvania, and Georgia Tech.
- No styles or scripts changed, so the cache versions are unchanged. No pages
  were added, so the sitemap, navigation, and footer are unchanged. Nothing in
  this change talks to a third party, so the privacy policy is unchanged.
- Started counting visitors. Every public page now loads two things from other
  companies: the Cloudflare Web Analytics beacon, which reports page views,
  top pages, referrers, countries, and browsers without cookies or any storage
  on the visitor's device, and the Scarf pixel, an image request that sends the
  visitor's IP address to Scarf so Scarf can name the organization that address
  belongs to. The pixel sends only the site's own address as the referrer, so
  Scarf learns that a visit happened and who it came from, not which page was
  read. The client login page loads neither and its content security policy is
  untouched.
- Rewrote the privacy policy in the same change, because three of its sentences
  became false the moment the first request fired. It no longer claims the site
  runs no analytics, uses no tracking scripts, or loads nothing from third
  party services. It names both companies, describes what each receives, states
  plainly that a visitor reading from a workplace network may have their
  employer's name reach Tectori, and adds a section covering Do Not Track,
  third party blocking, and how to request access or deletion. New effective
  date, August 23, 2026.

## 2026-08-22

- Rewrote the Fortivra description on the solutions page from the product's
  README: Fortivra Discover as the first release, the full list of what
  authorized read-only collection identifies and reports, and the OWASP GenAI
  LLM Top 10 for 2026 named as the assessment roadmap's risk taxonomy across
  all ten areas, stated as coverage being built rather than as certification
  or proof that a control works.
- Added a call path for visitors who would rather ring than write: the contact
  page now leads with a call button beside the email button and says a call is
  the fastest path, and every hero and closing call to action that offered a
  conversation by email now offers the phone beside it. Contact details stay
  character for character what the footer already carried.
- Corrected the Legal Self-Help Kit card to cover all fifty states and the
  District of Columbia, after the kit shipped its all-states expansion the same
  morning and left the card understating it by forty-nine states.

## 2026-08-20

- Added Landing Gear and the Legal Self-Help Kit as the sixth and seventh free
  tools, each linked to its GitHub repository with its language and license.
- Corrected the Landing Gear card to describe the finished twelve-chapter
  manual, covering interviewing and offers instead of a chapter it does not
  have.
- Reduced the largest heading size on every page so a page title no longer
  outweighs the tagline beneath it.
- Gave every interior page header the hero image treatment, rolling off the
  band image highlights so the graphic reads through a lighter gradient and
  still clears WCAG contrast.
- Made the client login page indexable and hardened it with a content security
  policy that permits no connections, no form submission, and no third party
  resources.
- Scoped the login privacy claim to Tectori, since a visitor's own browser or
  password manager can still save what they type.
- Versioned the stylesheet and script URLs so a returning visitor gets the
  current design rather than a cached one, which is the only cache control
  GitHub Pages allows.

## 2026-08-10

- Allowed `Google-Extended` so the site is eligible for citation in Gemini
  answers, accepting Gemini training use because Google covers both with one
  token.
- Allowed `GPTBot` and `ClaudeBot`, making the crawler policy permit every
  named crawler including model training.
- Added a Free tools page listing the five public open source repositories,
  each linked to GitHub with its language and license, and put Free tools in
  the navigation and footer on every page.
- Moved Ops Toolkit off the solutions portfolio and onto the Free tools page,
  since it is genuinely free and open rather than a proprietary product brand,
  and licensed its repository MIT so the claim holds.

## 2026-08-09

- Added Fortivra, the AI security discovery and reporting toolkit, to the
  solutions portfolio, homepage, and FAQ with a new brand mark.

## 2026-08-08

- Named ISO/IEC 42001 and the NIST AI Risk Management Framework on the agentic
  AI service line, the AI governance page, and the homepage Organization data,
  phrased as applied engagement scope.

## 2026-08-07

- Peer-reviewed the live site with an external model review and a verified
  multi-agent re-review, then fixed every confirmed finding.
- Met WCAG contrast and focus minimums: a darker on-white accent color,
  high-contrast focus outlines, and a visible focus style on the login inputs.
- Hardened the client login so nothing typed is transmitted even without
  JavaScript, and presented it as an operational portal gate with a plain
  logon-failed message.
- Unified the navigation order and footers on every page and restored the How
  we work link to all desktop menus.
- Removed one-person practice wording site-wide, named the frameworks the
  compliance service line covers, and completed the FAQ structured data.
- Set the effective dates on the privacy, terms, and accessibility pages.

## 2026-08-06

- Added a Services page detailing six consulting service lines with anchored
  sections, deliverables, and audit-readiness framing, placed first in the
  navigation on every page.
- Added privacy policy, terms of use, and accessibility pages written against
  the site's actual data collection, with footer links sitewide and effective
  date placeholders pending owner and attorney review.
- Rebuilt the contact page around direct email with a one business day response
  promise and a LinkedIn link, keeping the phone in the utility bar and footer.
- Reframed the product portfolio as founder-built product brands and working
  reference implementations, not offered for sale, and removed the development
  status labels.
- Expanded the featured credentials to full official names and named FFIEC and
  HIPAA in the audit-readiness copy.
- Fixed CSS browser compatibility warnings and grew the sitemap to thirteen
  canonical pages.
- Replaced the public personal email address with `contact@tectori.com`, added
  the public business number, and added dedicated Contact and FAQ pages.
- Added Organization and FAQ structured data, richer sharing metadata, explicit
  search crawler rules, and accurate sitemap modification dates.
- Added a setup guide for Google Search Console, Bing Webmaster Tools, and
  search-grounded assistant discovery.
- Reworked the public site around Tectori's orange, gold, charcoal, and warm
  white palette with a proof-oriented homepage and consistent navigation.
- Added a Solutions page for Compliance Compass, MailSweep, FileIQ, Architect
  Copilot, Lumenwatch, and Ops Toolkit with accurate development status labels.
- Added six original solution marks, a recolored hero image, and a branded
  social sharing image.
- Added a static portal preview that clears entries locally and displays an
  invalid credential message without storage, authentication, or network use.
- Added compliance-first resilience content covering protected records,
  recovery testing, controlled access, and predictable operations.

## 2026-08-05

- Expanded the public site with About Tectori, Audit-ready IT, AI governance,
  Azure reference implementation, and How We Work pages.
- Updated the homepage with the approved tagline, regulated-market positioning,
  six service names, and links to the new public content.
- Added responsive sitewide navigation, page metadata, a sitemap, and a public
  robots policy.
- Created the initial static Tectori website project.
- Added the official Tectori logo and a generated hero visual.
- Published the source to GitHub and enabled GitHub Pages from `docs/`.
