# Changelog

Tectori website changes are recorded here.

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
  the 2026-09-04 orchestrator brief.

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
