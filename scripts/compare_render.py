#!/usr/bin/env python3
"""Compare two directories of HTML files as rendered documents, tolerating pure formatting differences."""

import argparse
import os
import re
import sys
from html.parser import HTMLParser

WHITESPACE_RE = re.compile(r"\s+")


def collapse_whitespace(text):
    return WHITESPACE_RE.sub(" ", text).strip()


class RenderEventParser(HTMLParser):
    """Parses one HTML document into a flat list of comparable render events."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events = []

    def _attrs_map(self, attrs):
        return tuple(sorted((name, value if value is not None else "") for name, value in attrs))

    def handle_starttag(self, tag, attrs):
        self.events.append(("start", tag, self._attrs_map(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.events.append(("startend", tag, self._attrs_map(attrs)))

    def handle_endtag(self, tag):
        self.events.append(("end", tag, None))

    def handle_data(self, data):
        collapsed = collapse_whitespace(data)
        if collapsed:
            self.events.append(("text", collapsed, None))

    def handle_comment(self, data):
        self.events.append(("comment", collapse_whitespace(data), None))


def parse_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    parser = RenderEventParser()
    parser.feed(text)
    parser.close()
    return parser.events


def describe_event(ev):
    kind, a, b = ev
    if kind in ("start", "startend"):
        return f"{kind} tag <{a}> attrs={dict(b)}"
    if kind == "end":
        return f"end tag </{a}>"
    if kind == "text":
        return f"text {a!r}"
    if kind == "comment":
        return f"comment {a!r}"
    return repr(ev)


def compare_events(events_a, events_b):
    """Return None if identical, else a description of the first difference."""
    n = min(len(events_a), len(events_b))
    for i in range(n):
        if events_a[i] != events_b[i]:
            return (
                f"event #{i} differs: "
                f"left={describe_event(events_a[i])} "
                f"right={describe_event(events_b[i])}"
            )
    if len(events_a) != len(events_b):
        longer = events_a if len(events_a) > len(events_b) else events_b
        side = "left" if len(events_a) > len(events_b) else "right"
        return (
            f"event count differs: left has {len(events_a)}, right has {len(events_b)}; "
            f"{side} has extra event #{n}: {describe_event(longer[n])}"
        )
    return None


def find_common_html_files(dir_a, dir_b):
    names_a = {n for n in os.listdir(dir_a) if n.lower().endswith(".html")}
    names_b = {n for n in os.listdir(dir_b) if n.lower().endswith(".html")}
    return sorted(names_a & names_b), sorted(names_a - names_b), sorted(names_b - names_a)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir_a", help="first directory")
    parser.add_argument("dir_b", help="second directory")
    args = parser.parse_args()

    common, only_a, only_b = find_common_html_files(args.dir_a, args.dir_b)

    # A page present on one side and not the other is a difference, not a note.
    # Reporting it without failing would let a build that silently dropped a
    # page compare clean, and the comparison is the gate that decides whether
    # generated output may replace the live tree.
    any_diff = False
    if only_a:
        print(f"Only in {args.dir_a}: {', '.join(only_a)}")
        any_diff = True
    if only_b:
        print(f"Only in {args.dir_b}: {', '.join(only_b)}")
        any_diff = True
    for name in common:
        path_a = os.path.join(args.dir_a, name)
        path_b = os.path.join(args.dir_b, name)
        try:
            events_a = parse_file(path_a)
            events_b = parse_file(path_b)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"{name}: ERROR parsing ({exc})")
            any_diff = True
            continue
        diff = compare_events(events_a, events_b)
        if diff is None:
            print(f"{name}: identical")
        else:
            print(f"{name}: DIFFERS: {diff}")
            any_diff = True

    sys.exit(1 if any_diff else 0)


if __name__ == "__main__":
    main()
