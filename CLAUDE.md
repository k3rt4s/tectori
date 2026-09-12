# CLAUDE.md

Instructions for an AI session working in this repository.

Read `README.md` before changing anything. It describes the build, the
content model, and which check catches which kind of mistake.

`docs/` is build output with no exceptions. Never hand edit a file in it.
Change `site/` and rebuild with `python scripts/build_site.py --out docs`.

Run `python scripts/check_site.py` before a change and after it, and confirm
`git diff --stat -- docs/` is empty when a change was not meant to reach the
site. A push to `main` is the go-live, gated by those same checks.

Nothing installs. The build and every check use the standard library only.

This file named an absolute path on the author's machine until 2026-09-12,
which is the one thing a repository meant to change hands cannot do. A
session with its own workspace rules loads them from above this directory.
