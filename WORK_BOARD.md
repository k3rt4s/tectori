# WORK_BOARD

ACTIVE THREAD: 2026-08-23 evening

## In Progress

- Resume alignment pass on the site copy, branch
  `feature/resume-alignment-site-copy`, not yet pushed. Compared the five
  resumes Jon keeps outside this repo against the live copy and applied what
  Jon approved on 2026-08-23:
  - 19 years to 20 years in four places, the about.html meta description, the
    about.html prose line, the about.html stat tile, and the index.html proof
    strip. All five resumes say 20 plus years.
  - The PCI credential on about.html keeps its original name, Internal Security
    Assessor (ISA), and now names where it was held, Ingo Money. Jon first said
    QSA, matching the resumes, and changed to ISA when pre_push_review pointed
    out that PCI SSC issues ISA to internal employees and reserves QSA for
    external assessor companies. Open item for Jon, not for this repo: all five
    resumes say Internal PCI Qualified Security Assessor and should be
    corrected.
  - Added SANS SEC545, GenAI and LLM Application Security, 2026, and the
    2022 Nashville Security Leader of the Year Top 3 finalist line to the
    credentials list. Its aria-label widened to cover training and recognition.
  - Added an HCA Healthcare paragraph to the founder narrative, named, with
    the same not-a-Tectori-client sentence the Ncontracts paragraph carries.
  - Boot camp schools now match the resumes: Vanderbilt, Columbia, NYU, Penn,
    Georgia Tech.
  - No CSS or JS changed, so no `?v=` bump. No new pages, so no sitemap, nav,
    or footer change. No third party resources touched, so privacy.html is
    untouched.
  - Left alone deliberately: the exec resume claims a client outcome through
    an MSP partner, a 140,000 email index cut 80 percent and 37 percent in
    license savings. The site claims no client results anywhere and
    case-study.html says so explicitly. Putting that number on the site is
    Jon's call and a confidentiality question. Not raised with him yet.
  - Next action for you: ask Jon whether to run pre_push_review.py, run it if
    he says yes, report the triage, then ask separately for the push. The
    merge to main is the deploy.

- Next thread brief: `C:\Code_data\tectori\WEBSITE_PROMPT_2026-08-24.md`.
  Read it before starting. It carries the scope, what shipped on 2026-08-23,
  the open items in order, and the review and push sequence.

- Site analytics is deployed. Pushed to main at 1f6b705 on 2026-08-23 and
  confirmed serving on the live site. The Cloudflare Web Analytics beacon and
  the Scarf pixel are on all fourteen public pages, `docs/login.html` has
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

- Add individual service pages, a Resources page, and a Trust page in a later
  content release. Privacy, Terms, and Accessibility shipped on 2026-08-06 and
  are no longer part of this item.

## Questions for Jon

- None.
