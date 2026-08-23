# WORK_BOARD

ACTIVE THREAD: 2026-08-23 12:50

## In Progress

- Site analytics, branch `feature/site-analytics`, built and waiting on two IDs.
  Decided by Jon 2026-08-23, against the recommendation on Scarf, and
  reconfirmed in plain terms before anything was written. Research and the
  numbers behind the options are at
  `C:\Code_data\tectori\stats\analytics_options_research_2026-08-23.md`.
  - Built at ea9bdad: the Cloudflare Web Analytics beacon and the Scarf pixel
    on all fourteen public pages, plus the privacy.html rewrite in the same
    commit. `docs/login.html` has neither and its CSP is untouched. Verified
    15 of 15 pages for coverage, exclusion, and tag balance.
  - YOUR NEXT ACTION: get the two IDs from Jon and swap them in. Cloudflare
    dashboard, Analytics, Web Analytics, Add a site for the `www.tectori.com`
    hostname, which yields a site token. Scarf, the app dashboard at
    `app.scarf.sh`, create a pixel, which yields a pixel id. Replace `CF_BEACON_TOKEN` and `SCARF_PIXEL_ID` on all
    fourteen pages. This branch must not reach main with a placeholder in it,
    because main is the live site.
  - Then, in order: ask Jon whether to run pre_push_review.py, report the
    triage, ask separately for an explicit push, log to CHANGELOG.md, and
    check the live pages actually fire both requests before calling it done.
  - Jon will export the Search Console and Bing reports later; they land in
    `C:\Code_data\tectori\stats\` with the export date in the filename.

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

## Pending

- Add individual service pages, a Resources page, and a Trust page in a later
  content release. Privacy, Terms, and Accessibility shipped on 2026-08-06 and
  are no longer part of this item.

## Questions for Jon

- None.
