# Changelog

Tectori website changes are recorded here.

## 2026-08-23

- Started counting visitors. Every public page now loads two things from other
  companies: the Cloudflare Web Analytics beacon, which reports page views,
  top pages, referrers, countries, and browsers without cookies or any storage
  on the visitor's device, and the Scarf pixel, an image request that sends the
  visitor's IP address to Scarf so Scarf can name the organization that address
  belongs to. The client login page loads neither and its content security
  policy is untouched.
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
