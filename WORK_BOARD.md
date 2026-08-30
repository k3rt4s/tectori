# WORK_BOARD

## In Progress

- YOUR NEXT ACTION. Read the orchestrator brief at
  `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-08-24_B.md` before
  anything else. It is written for you and it replaces the two briefs
  before it, which are finished. It tells you what shipped, how to verify
  anything on the live site, and which board items are Jon's browser work
  rather than yours.
  The short version: Pending holds one small optional item and nothing
  else, and there is no FUTURE_FEATURES.md in this repo, so there is no
  backlog to pull from. Do not invent a release. Confirm with Jon through
  the interactive question tool what he wants built, and work from his
  answer. The brief names two things worth putting in front of him when
  you ask.

- 404 page and structured data shipped and confirmed live. Merged to main
  at 9cd55be on 2026-08-24. `docs/404.html` now serves for any missing
  address, including deep paths, and JSON-LD is on all eleven pages that
  should have it. Every one of the nine new blocks parses from the live
  site and matches its repo copy once line endings are normalized. Logged
  in CHANGELOG.md. The brief this ran from is
  `C:\Code_data\tectori\ORCHESTRATOR_PROMPT_2026-08-24.md` and it is
  finished. The JSON-LD spec the workers built to, which is what a later
  change to any of these blocks should match, is at
  `C:\Code_data\tectori\jsonld_spec_2026-08-24.md`.

- Content release shipped and confirmed live. Merged to main at b46c238 on
  2026-08-24 and serving on www.tectori.com. Six service pages, plus
  resources.html and trust.html, all returning 200 and matching the repo
  copies byte for byte once line endings are normalized. services.html keeps
  all six anchored sections and each links out to its page, so no inbound
  anchor link broke. Resources and Trust are footer only, the top navigation
  is unchanged at nine items, and the sitemap carries 23 urls. No styles or
  scripts changed, so the cache versions stay at v=20260822 and v=20260820.
  The facts on trust.html, where engagement material lives, the 30 day return
  or destroy window, the four practice security controls, and the 48 hour
  email response with a phone path for urgent reports, came from Jon on
  2026-08-24. If any of them stops being true, that page has to change.

- Site analytics is deployed. Pushed to main at 1f6b705 on 2026-08-23 and
  confirmed serving on the live site. The Cloudflare Web Analytics beacon and
  the Scarf pixel are on every public page, twenty two of them after the
  2026-08-24 content release, `docs/login.html` has
  neither and its CSP is untouched, and privacy.html was rewritten in the same
  commit as the tracking. The options research is at
  `C:\Code_data\tectori\stats\analytics_options_research_2026-08-23.md` and
  Jon's account setup notes, including the two Cloudflare wizard traps, are at
  `C:\Code_data\tectori\Tectori_Analytics_Setup.md`.
  - Only owner check left: open a public page and the login page in a browser
    with the network tab showing, confirm the beacon and the pixel fire on the
    first and neither fires on the second. Fetching the deployed HTML already
    confirms the tags ship and both endpoints answer, so this is a browser
    confirmation, not a suspected problem.
  - One Scarf hit on 2026-08-23 came from this workstation's verification
    request, not a visitor. Ignore the first datapoint.
  - Jon will export the Search Console and Bing reports later; they land in
    `C:\Code_data\tectori\stats\` with the export date in the filename. The
    brief flags eight pages reported discovered but not indexed on 2026-08-10,
    so check whether that count moved.

- Discovery and demand session, brief at `C:\Code_data\tectori\MORNING_PROMPT.md`.
  Jon confirmed on 2026-08-22: GBP first, then LinkedIn edits and the launch
  post while verification pends, then the examiner-questions checklist asset.
  He also approved a prominent call path on contact.html and the hero CTAs.
  - Step 1: Google Business Profile. Owner task, Jon works from the written
    instructions in `Tectori_Search_Setup.md`. Started 2026-08-22, video
    verification pending until Google completes it.
  - Step 2: LinkedIn company page (5 items) and personal profile (6 items) as
    paste-ready copy from the checklist. The HCA line is Jon's to confirm,
    nothing unconfirmed goes on a public profile.
  - Step 3: publish the launch post from `Posts for Tectori.txt` to the company
    page, Jon reshares from his personal profile the same day, then feature it.
    The Fortivra announcement is the second page post.
  - Step 4: checklist asset drafted in `C:\Code_data\tectori\Paste_Copy_2026-08-22.md`
    section 6, approved by Jon 2026-08-22. Owner task: post it from the
    company page after the launch post has had a few weeks, then feature it.
  - Shipped 2026-08-22: the call path on contact.html and every hero and
    cta-band, main at bdf6e80, logged in CHANGELOG.md.
  - Confirmed live 2026-08-23: `www.tectori.com/solutions.html` serves the
    d4a0b29 Fortivra rewrite byte for byte, and the deployed styles.css matches
    the repo copy. Below 620px the call and email buttons go full width and
    stack, they clear the 46px touch target, and nothing on the page can
    overflow the 390px floor in ui-standards.md. Read from the deployed CSS and
    markup, not rendered in a browser, so a font-driven wrap is the one thing
    this check cannot see.

## Pending

- Pilot the Evidence Readiness Baseline with the first qualified buyer. The
  offer and delivery brief were built on 2026-08-30, but the site changes are
  not deployed. The pilot should keep one defined review boundary and test
  whether the scope, evidence inventory, findings, and prioritized action list
  are useful without a maturity score. After the pilot, decide duration,
  sample size, fixed price, payment terms, and whether the offer remains
  standalone. Delivery brief:
  `C:\Code_data\tectori\EVIDENCE_READINESS_BASELINE_OFFER_2026-08-30.md`.
- Optional, small: two pages carry structured data with no `@id`. The
  `FAQPage` node in `docs/faq.html` and the founder `Person` node nested in
  the `docs/index.html` Organization block both lack one. Neither is a
  defect and neither breaks anything today. Giving the index.html founder
  an `@id` would let `about.html#person` reference one canonical Person
  instead of declaring its own, which is the shape Jon considered and set
  aside on 2026-08-24 to keep that release inside its nine pages. Found by
  the verification pass on 2026-08-24, both pre-existing, both deliberately
  left alone.

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
