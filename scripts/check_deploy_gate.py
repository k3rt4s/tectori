#!/usr/bin/env python3
"""Confirm the workflow still deploys only after the checks pass.

The deploy job's ``needs`` list is parsed as GitHub Actions parses it
(scalar, flow list, or block list) and matched against the verify job's
id exactly, not as a substring, so a decoy job such as ``verify-real``
does not count. The verify job's steps are parsed too: the check, build
diff and rebrand scripts must each be run by a step that cannot be skipped
or have its failure ignored, not merely be mentioned somewhere in the job.
The deploy job's own condition must name both the event and the branch, so a
manual run on a feature branch deploys nothing, and the ``pages``
concurrency group must sit on the deploy job alone, never cancelling, never
shared with the verify job or placed on the whole workflow.
"""

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
# What the deploy job's own condition has to say: exactly these two clauses,
# joined by && in either order. Matching whole clauses rather than looking for
# the word `pull_request` in it is the point: the inverted form contains the
# same word. The second clause is what keeps a workflow_dispatch run on a
# feature branch from deploying, which would otherwise rest on a Pages
# environment rule that lives outside this tree.
EXPECTED_CLAUSES = frozenset(
    {"github.event_name != 'pull_request'", "github.ref == 'refs/heads/main'"}
)
EXPECTED_CONDITION = (
    "github.event_name != 'pull_request' && github.ref == 'refs/heads/main'"
)
# The one concurrency group a deploy may use.
DEPLOY_GROUP = "pages"
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


def _strip_comment(text):
    """Drop a trailing ``#comment`` from a YAML scalar.

    YAML ends an unquoted value at a comment marker that is either the
    very start of the (stripped) text or preceded by whitespace, a
    space or a tab, and a job id never contains `#`, so truncating at
    the first such marker is exact rather than a heuristic.
    """
    match = re.search(r"(?:^|[ \t])#", text)
    return text[:match.start()] if match else text


def needs_job_ids(body):
    """Return the job ids listed in a job's ``needs:`` key.

    GitHub Actions accepts a scalar (``needs: verify``), a flow list
    (``needs: [verify, other]``), or a block list (``needs:`` followed by
    indented ``- verify`` lines), each optionally quoted and each
    optionally followed by an unquoted `` #`` comment. Matching any of
    these against a single job id, rather than searching the raw text for
    the id as a substring, is the point: a word-boundary search on
    ``\\bverify\\b`` still matches inside ``verify-real``, because a hyphen
    is a word boundary too.
    """
    lines = body.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^(\s*)needs:\s*(.*)$", line)
        if not match:
            continue
        indent = match.group(1)
        rest = _strip_comment(match.group(2)).strip()
        if not rest:
            # Block list: the more-indented `- name` lines that follow.
            ids = []
            for later in lines[i + 1:]:
                stripped_later = later.strip()
                if not stripped_later or stripped_later.startswith("#"):
                    # Blank line or comment-only line between items:
                    # keep reading rather than treating it as the end
                    # of the block list.
                    continue
                candidate = _strip_comment(later).rstrip()
                if not candidate.strip():
                    continue
                item = re.match(
                    r"^(\s*)-\s*[\'\"]?([A-Za-z0-9_-]+)[\'\"]?\s*$", candidate
                )
                if item and len(item.group(1)) > len(indent):
                    ids.append(item.group(2))
                    continue
                break
            return ids
        if rest.startswith("["):
            # Flow list. GitHub allows it to wrap onto later lines, so
            # keep reading until the closing bracket shows up.
            text = rest
            j = i
            while "]" not in text and j + 1 < len(lines):
                j += 1
                text += " " + _strip_comment(lines[j]).strip()
            text = text[: text.index("]") + 1] if "]" in text else text
            inner = text.strip("[]")
            return [
                item.strip().strip("'\"")
                for item in inner.split(",")
                if item.strip()
            ]
        # Scalar.
        return [rest.strip("'\"")]
    return []


def condition_clauses(text):
    """Return a condition's clauses as a set, or None if it is not a plain && chain.

    Any ``||``, parenthesis, negation or expression wrapper makes the
    condition something other than two required clauses, so it is rejected
    here rather than guessed at.
    """
    if "||" in text or "(" in text or "${{" in text:
        return None
    return {part.strip() for part in text.split("&&")}


def job_concurrency(body):
    """Return a job's own ``concurrency`` as (group, cancel), or None if it has none.

    Only the job-level key (four spaces in) counts, and a commented-out
    block is not a block. Values are returned as written, unquoted and
    without trailing comments; a missing key comes back as None.
    """
    lines = body.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^    concurrency:\s*(.*)$", line)
        if not match:
            continue
        if _strip_comment(match.group(1)).strip():
            # Scalar or flow form: not the block this gate reads.
            return ("", None)
        group = cancel = None
        for later in lines[i + 1:]:
            if not later.strip() or later.lstrip().startswith("#"):
                continue
            if len(later) - len(later.lstrip()) <= 4:
                break
            pair = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", later)
            if pair:
                value = _unquote(_strip_comment(pair.group(2)))
                if pair.group(1) == "group":
                    group = value
                elif pair.group(1) == "cancel-in-progress":
                    cancel = value.lower()
        return (group, cancel)
    return None


def workflow_level_concurrency(text):
    """Say whether an uncommented ``concurrency`` key sits at the workflow level.

    YAML key order carries no meaning, so the whole file is read, not only the
    text before ``jobs:``; a quoted key and a space before the colon are
    accepted too, since GitHub reads both.
    """
    return (
        re.search(r"""^["']?concurrency["']?\s*:""", text, re.MULTILINE)
        is not None
    )


# What the verify job's steps must run. Each entry is a script and the
# extra command (if any) that must also run, unescaped, in the same step.
GATING_STEPS = (
    ("scripts/check_site.py", None),
    ("scripts/build_site.py", "git diff --exit-code"),
    ("scripts/rehearse_rebrand.py", None),
)
# A command followed by one of these cannot fail the step.
SWALLOWED = re.compile(r"(?:\|\||;)\s*(?::|true|exit\s+0)\s*(?:$|[;&|)])")


def job_steps(body):
    """Return the job's steps, each a dict of its keys mapped to raw values.

    A step is a ``- `` item under ``steps:``. Keys are read at the step's own
    indent; a ``|`` or ``>`` block scalar's lines are returned joined by
    newlines, backslash continuations folded, and full-line YAML comments
    outside a block scalar are ignored, so a commented ``# run: ...`` is not
    a step key.
    """
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*steps:\s*(?:#.*)?$", line):
            start = i + 1
            steps_indent = len(line) - len(line.lstrip())
            break
    if start is None:
        return []
    items = []
    item_indent = None
    for line in lines[start:]:
        if not line.strip() or line.lstrip().startswith("#"):
            if items:
                items[-1].append(line)
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= steps_indent:
            break
        if line.lstrip().startswith("- ") and (
            item_indent is None or indent == item_indent
        ):
            item_indent = indent
            items.append([line])
        elif items:
            items[-1].append(line)
    steps = []
    for item in items:
        first = item[0]
        dash = len(first) - len(first.lstrip())
        item = [" " * (dash + 2) + first.lstrip()[2:]] + item[1:]
        key_indent = dash + 2
        step = {}
        i = 0
        while i < len(item):
            line = item[i]
            i += 1
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if len(line) - len(line.lstrip()) != key_indent:
                continue
            match = re.match(r"^\s*([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not match:
                continue
            key, value = match.group(1), match.group(2)
            if re.match(r"^[|>][+-]?\d*\s*(?:#.*)?$", value):
                block = []
                while i < len(item) and (
                    not item[i].strip()
                    or len(item[i]) - len(item[i].lstrip()) > key_indent
                ):
                    block.append(item[i].strip())
                    i += 1
                step[key] = "\n".join(block)
            else:
                step[key] = _strip_comment(value).strip()
        steps.append(step)
    return steps


def _commands(run):
    """Split a run value into shell lines: continuations joined, comments dropped."""
    joined = re.sub(r"\\[ \t]*\n\s*", " ", run)
    out = []
    for line in joined.splitlines():
        line = _strip_comment(line).strip()
        if line:
            out.append(line)
    return out


def _unquote(value):
    return value.strip().strip("'\"").strip()


def step_runs(step, script, also):
    """Say why a step does not really run ``script``, or return None if it does."""
    if _unquote(step.get("continue-on-error", "false")).lower() not in (
        "false", "${{ false }}"
    ):
        return "has continue-on-error set, so its failure is ignored"
    condition = step.get("if")
    if condition is not None:
        text = _unquote(condition)
        if text.startswith("${{") and text.endswith("}}"):
            text = text[3:-2].strip()
        if text.lower() in ("false", "0", "null", "''", '""', "!true"):
            return "has an if that is always false, so it never runs"
    run = step.get("run")
    if run is None:
        return "has no run command"
    # The command must start the line or follow &&, so an echo or a string
    # argument that merely names the script is not a run of it.
    invoke = re.compile(
        r"(?:^|&&)\s*python[\d.]*\s+(?:-[\w-]+\s+)*['\"]?(?:\./)?"
        + re.escape(script) + r"(?![\w.])"
    )
    wanted = [invoke] + (
        [re.compile(r"(?:^|&&)\s*" + re.escape(also) + r"(?![\w-])")]
        if also else []
    )
    for pattern in wanted:
        hits = [(c, m) for c in _commands(run) for m in [pattern.search(c)] if m]
        if not hits:
            return "does not invoke " + (also if pattern is not invoke else script)
        # Any || after the command runs something else when it fails, which
        # makes the step pass whatever that something is.
        if all(SWALLOWED.search(c) or "||" in c[m.end():] for c, m in hits):
            return "swallows the failure of " + (
                also if pattern is not invoke else script
            )
    return None


def verify_problems(body):
    """Return the problems with how the verify job runs its gating scripts."""
    steps = job_steps(body)
    problems = []
    for script, also in GATING_STEPS:
        reasons = []
        ok = False
        for step in steps:
            why = step_runs(step, script, also)
            if why is None:
                ok = True
                break
            if "run" in step and script in step["run"]:
                reasons.append(why)
        if not ok:
            detail = f" (a step mentioning it {reasons[0]})" if reasons else ""
            problems.append(
                f"the {VERIFY_JOB} job has no step that runs {script} and "
                f"fails when it fails{detail}"
            )
    return problems


def main():
    problems = []
    if not os.path.exists(WORKFLOW):
        print(f"[FAIL] the deploy waits for the checks: {WORKFLOW} is missing")
        return 1

    with open(WORKFLOW, encoding="utf-8") as f:
        text = f.read()
    found = jobs(text)

    if workflow_level_concurrency(text):
        problems.append(
            "the workflow has a concurrency block of its own at the top, so "
            "every job, including a pull request's checks, shares one group "
            "and a pull request can displace a pending deploy of main"
        )

    if VERIFY_JOB not in found:
        problems.append(f"no {VERIFY_JOB} job, so nothing runs the checks")
    else:
        problems.extend(verify_problems(found[VERIFY_JOB]))

    if DEPLOY_JOB not in found:
        problems.append(
            f"no {DEPLOY_JOB} job. Pages then publishes nothing, or publishes "
            "from the branch without waiting for anything"
        )
    else:
        body = found[DEPLOY_JOB]
        needed = needs_job_ids(body)
        if VERIFY_JOB not in needed:
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
        else:
            written = _strip_comment(condition.group(1)).strip()
            if condition_clauses(written) != EXPECTED_CLAUSES:
                problems.append(
                    f"the {DEPLOY_JOB} job's condition is {written!r} "
                    f"rather than {EXPECTED_CONDITION!r} (both clauses, joined "
                    "by &&), so a manual run on a feature branch can deploy"
                )
        deploy_conc = job_concurrency(body)
        if deploy_conc is None:
            problems.append(
                f"the {DEPLOY_JOB} job has no concurrency block, so deploys "
                "are not serialised"
            )
        elif deploy_conc != (DEPLOY_GROUP, "false"):
            problems.append(
                f"the {DEPLOY_JOB} job's concurrency is group "
                f"{deploy_conc[0]!r} with cancel-in-progress {deploy_conc[1]!r}"
                f" rather than group {DEPLOY_GROUP!r} with cancel-in-progress "
                "false, so a deploy can be cancelled mid-upload"
            )
        if VERIFY_JOB in found:
            verify_conc = job_concurrency(found[VERIFY_JOB])
            if verify_conc is None or not verify_conc[0]:
                problems.append(
                    f"the {VERIFY_JOB} job has no concurrency group of its own"
                )
        # No other job may share the deploy's group: a pull request or a
        # feature-branch run of that job would take the one pending slot that
        # a deploy of main is waiting for. Group names are compared folded,
        # which is how GitHub compares them.
        taken = {DEPLOY_GROUP.lower()}
        if deploy_conc is not None and deploy_conc[0]:
            taken.add(deploy_conc[0].lower())
        for name, other in found.items():
            if name == DEPLOY_JOB:
                continue
            other_conc = job_concurrency(other)
            if other_conc is None or not other_conc[0]:
                continue
            # Text left once every ${{ }} is removed is in the group name
            # whatever the expression evaluates to, so a group with any such
            # text can never equal the deploy's; a bare expression could.
            literal = re.sub(r"\$\{\{.*?\}\}", "", other_conc[0]).strip()
            if other_conc[0].lower() in taken or not literal:
                problems.append(
                    f"the {name} job's concurrency group {other_conc[0]!r} is "
                    f"the {DEPLOY_JOB} job's group, or an expression that could "
                    "evaluate to it, so a pull request event can displace a "
                    "pending deploy of main"
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
