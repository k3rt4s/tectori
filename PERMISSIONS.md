# Tectori Website Permissions

Authoritative list of every permission and prerequisite this site needs to
build, deploy, and serve.

Keep this current. When a change adds a permission or prerequisite that is not
listed here, add the row in the same change, naming the file that needs it and
the reason. `site/content/site.json` is the per-value source of truth for the
third-party identifiers and the external host allowlist, and
`scripts/verify_site.py` fails if a built tree disagrees with it. This file is
the consolidated rollup.

Two things make this manifest shorter than most. The published site is static,
so no application code runs on the server. And the build scripts import only
the Python standard library, so there is no dependency tree to grant anything
to.

---

## How the site authenticates

It does not. The published site has no accounts, no sessions, no cookies set
by the site, and no server-side code. `docs/login.html` is a static page with
no form action; it is a placeholder for a future client portal and submits
nowhere. It is also the one page that carries a Content Security Policy, and
that policy denies connections, objects, framing bases, and form actions
outright.

Credentials exist only in the operator accounts listed under Operator
accounts below, never in this repository.

---

## Runtime and services

- **Python**: required, used by everything in `scripts/`. Verified against
  3.13.5. The scripts import only the standard library, so no virtual
  environment and no `requirements.txt` are needed. There is no
  `requirements.txt` for that reason, not by oversight.
- **git and a GitHub account**: required, used to deploy. A push to `main` is
  the go-live.
- **GitHub Pages**: required, serves the site. Free tier is sufficient.
- **A registrar that can set A, AAAA, and CNAME records**: required, points
  the custom domain at Pages. The current registrar is Dynadot.
- **markdownlint-cli2 via npx**: best-effort, lints Markdown only. Skipping it
  degrades nothing at runtime; the site builds and deploys without Node
  installed.
- **GitHub Actions**: best-effort, runs the checks on every push and pull
  request from `.github/workflows/verify.yml`. It needs `contents: read` and
  no secrets, and it pulls `actions/checkout` and `actions/setup-python` from
  the Actions marketplace at run time. Disabling Actions costs the checks on
  a clean machine and nothing else: Pages deploys from `main` and `docs/`
  whether the workflow passed, failed, or never ran.

---

## Filesystem

- **The repository tree**: read and write, required, used by every script.
  `scripts/build_site.py` writes only to the directory `--out` names. That
  is normally `docs/`, which it rewrites in place with an identical tree.
- **Any directory passed to `--out`**: write and create, required.
  `--out` has no default, so nothing is written anywhere until a build names
  a destination.
- **The system temporary directory**: write and create, required, used by
  `scripts/build_site.py --check` and `scripts/check_site.py`, each of which
  builds into a temporary tree and deletes it afterwards.

No path outside those three is read or written. Nothing needs a grant beyond
the ordinary rights of the user running the command.

---

## Network egress

Nothing in this repository makes a network call. The egress below is either a
visitor's browser acting on the published markup, or the operator pushing.

What a published page causes a visitor's browser to fetch, all on port 443
over HTTPS:

- **static.cloudflareinsights.com**: best-effort, the page view beacon, on
  all 24 public pages and never on `docs/login.html`. Blocked or failing, the
  page renders normally and the visit goes uncounted.
- **static.scarf.sh**: best-effort, the page view pixel, same 24 pages and
  the same exclusion, same degradation.
- **formspree.io**: required for the contact form only, the POST target of
  the form on `docs/contact.html`. Unreachable, the form cannot submit and
  the phone number on the same page is the fallback path.

Hosts the pages link to but never fetch automatically, so no egress happens
unless a visitor clicks: `www.linkedin.com`, `github.com`, `docs.github.com`,
`genai.owasp.org`, `www.cloudflare.com`, and `about.scarf.sh`. The last two
are the two analytics vendors' own privacy pages, linked from
`docs/privacy.html`.

Two more hostnames appear in the markup as XML and JSON-LD namespaces rather
than as anything fetched: `schema.org` and `www.sitemaps.org`.

Every host above is declared in `site/content/site.json` with the reason it is
there, and `scripts/verify_site.py` fails if the tree references a host that
is not on that list. Adding an outbound link to a new domain is therefore a
deliberate act that updates this manifest and that file together.

What the operator's own machine contacts:

- **github.com**: required, port 443, `git push`. This is the deploy.

Ingress: `scripts/serve_docs.py` listens on port 8000 for local review only.
It binds loopback and serves `docs/` read-only. It is a preview aid and is
never part of a deploy.

---

## Secrets and config

The repository holds no secrets and needs none. `.env.example` exists only to
say so, and `.gitignore` excludes `.env` and `.env.*` regardless.

The three third-party identifiers in `site/content/site.json` are not
credentials. A beacon token, a pixel id, and a form endpoint are all published
in the page source of every site that uses them, and none of them grants
access to anything. They are declared in one place so a rebrand cannot leave a
previous owner's identifier collecting this site's traffic, which is a
correctness problem rather than a secrecy one.

### Operator accounts

These hold real credentials, none of which belong in this repository:

- **GitHub**: required, owns the repository and the Pages deployment.
- **The domain registrar**: required, holds the DNS records below.
- **Formspree**: required only if the contact form is used, owns the form
  endpoint and receives the submissions.
- **Cloudflare**: best-effort, owns the Web Analytics site and its beacon
  token.
- **Scarf**: best-effort, owns the pixel and its id.

---

## Cloud IAM, RBAC, API scopes, and OAuth

None. The site calls no cloud API and requests no OAuth scope. The only
account-level right the deploy needs is administrative access to the GitHub
repository, which is what enabling Pages and setting the custom domain
requires.

---

## Elevation and OS rights

None. No administrator or root rights, no scheduled task, no registry access,
no firewall rule, and no service installation. Every script runs as an
ordinary user.

---

## Agent capabilities

None. The site ships no agent and calls no model at runtime.

---

## DNS records

Set these at the registrar after GitHub Pages is enabled. The CNAME sends the
canonical `www` hostname to Pages; the A and AAAA records let the apex
redirect to it.

| Type  | Host | Value               |
| ----- | ---- | ------------------- |
| CNAME | www  | k3rt4s.github.io    |
| A     | @    | 185.199.108.153     |
| A     | @    | 185.199.109.153     |
| A     | @    | 185.199.110.153     |
| A     | @    | 185.199.111.153     |
| AAAA  | @    | 2606:50c0:8000::153 |
| AAAA  | @    | 2606:50c0:8001::153 |
| AAAA  | @    | 2606:50c0:8002::153 |
| AAAA  | @    | 2606:50c0:8003::153 |

`docs/CNAME` holds `www.tectori.com`. The custom domain now lives in the
repository's Pages settings, because the deploy runs from the workflow rather
than from the branch, and only branch publishing reads the file. It is kept
and kept correct so that publishing from the branch still works if anyone
switches back. Changing the domain means changing that file, the Pages
setting, `site_url` in `site/content/site.json`, and these records together.

---

## Grant runbook

On a fresh environment, in order.

1. Install Python and git. Clone the repository. Nothing else installs.
2. Run `python scripts/check_site.py` from the repository root and confirm
   six of six checks pass before changing anything.
3. Create the GitHub repository and push `main`. Pages needs the repository to
   exist before it can serve from it.
4. In the repository settings, enable Pages with source GitHub Actions, then
   set the custom domain to the hostname in `docs/CNAME`. The source matters:
   with `main` and `/docs` instead, Pages publishes every push whether the
   checks passed or not, and this workflow's deploy job fails.
5. Add the DNS records above at the registrar. Allow for propagation before
   expecting the custom domain to answer.
6. Enable HTTPS enforcement in the Pages settings once the certificate is
   issued. Then run `python scripts/check_live_deploy.py`, which fetches
   every file from the live site and compares it against `docs/`. Until it
   passes, nothing has confirmed the deploy landed: a green workflow says the
   artifact was accepted, not that the domain and the certificate answer.
7. If the contact form is wanted, create the Formspree form and put its
   endpoint in `third_party.formspree_endpoint` in `site/content/site.json`.
   That is the only place it is written. This step told you to also edit the
   form action on `docs/contact.html` until 2026-09-12, which was wrong twice
   over: `docs/` is build output and the next build overwrites it, and the
   value was genuinely in two places because the fragment hard-coded it.
8. If page view counting is wanted, create the Cloudflare Web Analytics site
   and the Scarf pixel, then put the beacon token and the pixel id in
   `third_party` in `site/content/site.json` and rebuild, so every page picks
   up the new values.
9. Run `python scripts/check_site.py` again. The identity check compares the
   built tree against the values just entered, so a typo fails here rather
   than after the deploy.
10. Push to `main`. That is the go-live. Allow about three minutes.

---

## Verification

After the runbook, two checks.

```text
python scripts/check_site.py
```

Six of six must pass. The third of those runs `scripts/verify_site.py`,
whose last check confirms the beacon token, the pixel id, and the form
endpoint in the built tree are the declared ones at the expected count, and
that no page references a host outside the allowlist.

Then open the live site and confirm the custom domain answers over HTTPS,
that the certificate names the hostname in `docs/CNAME`, and that a browser's
network panel shows the beacon and pixel firing on a public page and neither
firing on `login.html`.
