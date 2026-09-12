#!/usr/bin/env python3
"""Confirm the workflow still deploys only after the checks pass."""

# The deploy job is the only route to the site, so it is the one thing in this
# repository whose removal is silent. Delete the `needs` line and every check
# still passes, every run still goes green, and a broken tree ships on the next
# push, which is exactly the state this repository was in until 2026-09-12.
# Nothing else reads the workflow: the other checks read the built tree.
#
# Only the file half is checkable here. The other half is a repository setting,
# Pages publishing from GitHub Actions rather than from a branch, and there is
# no way to read it without the network and a token. It is step 4 of the grant
# runbook in PERMISSIONS.md, and getting it wrong fails this workflow's deploy
# job loudly rather than shipping quietly.

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(REPO_ROOT, ".github", "workflows", "verify.yml")

# The job that runs the checks, and the job that publishes docs/.
VERIFY_JOB = "verify"
DEPLOY_JOB = "deploy"
# What the deploy job's own condition has to say, character for character.
# Matching the whole thing rather than looking for the word `pull_request`
# in it is the point: the inverted form contains the same word.
EXPECTED_CONDITION = "github.event_name != 'pull_request'"
# Any of these in the deploy job makes it run whatever the verify job did,
# which leaves the `needs` line in place and decorative.
OVERRIDES = ("always()", "failure()", "cancelled()")


def jobs(text):
    """Return each job in the workflow as a name mapped to its own block of lines."""
    lines = text.splitlines()
    try:
        start = lines.index("jobs:") + 1
    except ValueError:
        return {}
    found = {}
    current = None
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if match:
            current = match.group(1)
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return {name: "\n".join(body) for name, body in found.items()}


def main():
    problems = []
    if not os.path.exists(WORKFLOW):
        print(f"[FAIL] the deploy waits for the checks: {WORKFLOW} is missing")
        return 1

    with open(WORKFLOW, encoding="utf-8") as f:
        text = f.read()
    found = jobs(text)

    if VERIFY_JOB not in found:
        problems.append(f"no {VERIFY_JOB} job, so nothing runs the checks")
    elif "check_site.py" not in found[VERIFY_JOB]:
        problems.append(f"the {VERIFY_JOB} job does not run check_site.py")

    if DEPLOY_JOB not in found:
        problems.append(
            f"no {DEPLOY_JOB} job. Pages then publishes nothing, or publishes "
            "from the branch without waiting for anything"
        )
    else:
        body = found[DEPLOY_JOB]
        if not re.search(rf"^\s*needs:.*\b{VERIFY_JOB}\b", body, re.MULTILINE):
            problems.append(
                f"the {DEPLOY_JOB} job does not need {VERIFY_JOB}, so a failing "
                "check no longer stops the deploy"
            )
        if "deploy-pages" not in body:
            problems.append(f"the {DEPLOY_JOB} job does not deploy to Pages")
        if not re.search(r"^\s*path:\s*docs\s*$", body, re.MULTILINE):
            problems.append(
                f"the {DEPLOY_JOB} job does not upload docs/, so it publishes "
                "something other than the tree every other check read"
            )
        # Read for what the condition says, not for the words it contains.
        # `github.event_name == 'pull_request'` holds the same word and means
        # the opposite, and a four space indent is the job's own condition
        # rather than a step's.
        condition = re.search(r"^    if:\s*(.+?)\s*$", body, re.MULTILINE)
        if condition is None:
            problems.append(
                f"the {DEPLOY_JOB} job has no condition of its own, so a pull "
                "request deploys and an unmerged branch reaches the site"
            )
        elif condition.group(1) != EXPECTED_CONDITION:
            problems.append(
                f"the {DEPLOY_JOB} job's condition is {condition.group(1)!r} "
                f"rather than {EXPECTED_CONDITION!r}"
            )
        for override in OVERRIDES:
            if override in body:
                problems.append(
                    f"the {DEPLOY_JOB} job uses {override}, so it runs whatever "
                    f"{VERIFY_JOB} did and the needs line above it decides nothing"
                )

    ok = not problems
    print(
        f"[{'PASS' if ok else 'FAIL'}] the deploy waits for the checks: "
        f"{len(found)} jobs, {len(problems)} problems"
    )
    for problem in problems:
        print(f"       {problem}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
