#!/usr/bin/env python3
"""Extract only the submitted attempts from a cbc-scraper all_attempts.txt dump.

Output: one attempt per line, grouped under a "# taskN" heading, with a blank
line between tasks. Attempts keep their original (oldest first) order.

Usage:
    python3 extract_attempts.py all_attempts.txt              # print to screen
    python3 extract_attempts.py all_attempts.txt -o out.txt   # write a file
    python3 extract_attempts.py all_attempts.txt --unique     # drop repeats per task
    python3 extract_attempts.py all_attempts.txt --no-headers # bare lines only
"""
import argparse
import re
import sys

HEADER = re.compile(r"^--- (?P<task>.+?) #\d+ \| .+ UTC ---$", re.M)


def extract(text):
    """Return {task: [attempt, ...]} in file order."""
    tasks = {}
    matches = list(HEADER.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[match.end():end]
        start = block.find("Submission:\n")
        stop = block.rfind("\nAPI response:\n")
        if start == -1 or stop == -1 or stop < start:
            continue
        attempt = block[start + len("Submission:\n"):stop]
        # Keep one attempt per line even if it contained line breaks.
        attempt = attempt.replace("\r", "").replace("\n", "\\n")
        tasks.setdefault(match.group("task"), []).append(attempt)
    return tasks


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("infile")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    ap.add_argument("--unique", action="store_true", help="drop repeated attempts within a task")
    ap.add_argument("--no-headers", action="store_true", help="omit the '# taskN' lines")
    args = ap.parse_args()

    with open(args.infile, encoding="utf-8", errors="replace") as handle:
        tasks = extract(handle.read())

    out = []
    for task, attempts in tasks.items():
        if args.unique:
            attempts = list(dict.fromkeys(attempts))
        if not args.no_headers:
            out.append(f"# {task}")
        out.extend(attempts)
        out.append("")
    text = "\n".join(out)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(text)
        total = sum(len(v) for v in tasks.values())
        print(f"Wrote {total} attempts across {len(tasks)} tasks to {args.output}", file=sys.stderr)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
