#!/usr/bin/env python3
"""
Generate an AdGuard blocklist for lowendtalk.com
from a filter file containing usernames (one per line).
- Lines starting with '#' are treated as comments and ignored.
- Optional suffixes:
    :c → block only comments
    :d → block only discussions
    (no suffix) → block both
"""

import sys
import os

def generate_blocklist(input_file):
    # Derive output filename: same base name + .blocklist.txt
    base, _ = os.path.splitext(input_file)
    output_file = base + ".blocklist.txt"

    # Read usernames from filter file
    with open(input_file, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    users = []
    for line in raw_lines:
        if line.startswith("#"):
            continue  # skip comments
        users.append(line)

    rules = []
    rules.append("! LowEndTalk blocklist - automatically generated")
    rules.append("")

    # Generate rules
    for entry in users:
        if entry.endswith(":c"):
            user = entry[:-2]
            rules.append(f'lowendtalk.com##.Comment:has(.Username[href="/profile/{user}"])')
        elif entry.endswith(":d"):
            user = entry[:-2]
            rules.append(f'lowendtalk.com##.ItemDiscussion:has(.DiscussionAuthor a[href="/profile/{user}"])')
        else:
            user = entry
            rules.append(f'lowendtalk.com##.Comment:has(.Username[href="/profile/{user}"])')
            rules.append(f'lowendtalk.com##.ItemDiscussion:has(.DiscussionAuthor a[href="/profile/{user}"])')

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(rules))

    print(f"Blocklist generated in {os.path.abspath(output_file)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 arkas.py <filter_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    generate_blocklist(input_file)
