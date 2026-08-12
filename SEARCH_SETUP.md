# Search Discovery Setup

Search account setup completes the website's technical discovery work for
Google Search, Bing, and search-grounded assistants.

## Before Submission

1. Create and test the `contact@tectori.com` alias.
2. Confirm that a message sent from an unrelated account reaches the intended
   inbox and that replies use the preferred sender address.
3. Open `https://www.tectori.com/robots.txt` and
   `https://www.tectori.com/sitemap.xml` after the release is published.

## Google Search Console

1. Open [Google Search Console](https://search.google.com/search-console/).
2. Add `tectori.com` as a Domain property.
3. Add the TXT verification record Google provides to the domain's DNS.
4. Wait for verification, then submit
   `https://www.tectori.com/sitemap.xml` under Sitemaps.
5. Inspect `https://www.tectori.com/` and request indexing once.
6. Inspect the Coverage, Page indexing, Enhancements, and Performance reports
   after Google begins crawling the site.

## Bing Webmaster Tools

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters/).
2. Add `https://www.tectori.com/` and complete site verification. Importing a
   verified Google Search Console property is acceptable when Bing offers it.
3. Submit `https://www.tectori.com/sitemap.xml` under Sitemaps.
4. Review Site Explorer and URL Inspection after Bing processes the sitemap.
5. Add IndexNow only when the site begins publishing frequent updates. The
   sitemap is sufficient for the current low-change static site.

## Search-Grounded Assistants

- `OAI-SearchBot` and `ChatGPT-User` are allowed for ChatGPT discovery and
  user-directed retrieval. `GPTBot`, the training crawler, is also allowed.
- `Claude-SearchBot` and `Claude-User` are allowed for Claude discovery and
  user-directed retrieval. `ClaudeBot`, the training crawler, is also allowed.
- Training access does not affect whether the site appears in assistant
  answers, which the search and retrieval crawlers govern. It is allowed so
  the site can inform future models directly.
- Googlebot is allowed for Google Search, AI Overviews, and AI Mode.
  `Google-Extended` is allowed so Tectori can be cited inside the Gemini app.
  Google does not separate Gemini grounding from Gemini training, so this one
  token covers both, and the owner accepted training use to gain the
  visibility.
- Bingbot is allowed for Bing Search and Bing Copilot discovery.

No special AI text file is used. Search providers currently emphasize normal
indexing, accessible semantic HTML, internal links, accurate structured data,
and useful textual content.

## Ongoing Maintenance

1. Update each sitemap `lastmod` value only when that page receives a
   significant content, structured data, or internal-link change.
2. Keep the Organization and FAQ structured data consistent with visible
   claims.
3. Add substantive resources or case studies when real material is available.
4. Review search queries and indexing errors monthly during the first quarter,
   then quarterly once discovery is stable.
