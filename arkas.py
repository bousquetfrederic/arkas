#!/usr/bin/env python3
"""
Generate an AdGuard blocklist for lowendtalk.com
from a file filter.txt containing a list of usernames (one per line, without /profile/).
"""

def generate_blocklist(input_file="filter.txt", output_file="lowendtalk-blocklist.txt"):

    # Read usernames from filter.txt
    with open(input_file, "r", encoding="utf-8") as f:
        users = [line.strip() for line in f if line.strip()]

    rules = []
    rules.append("! LowEndTalk blocklist - automatically generated")
    rules.append("! Each user appears once per section")
    rules.append("")

    # Comment section
    rules.append("! --- Comments ---")
    for user in users:
        rules.append(f'lowendtalk.com##.Comment:has(.Username[href="/profile/{user}"])')
    rules.append("")

    # Discussion section
    rules.append("! --- Discussions ---")
    for user in users:
        rules.append(f'lowendtalk.com##.ItemDiscussion:has(.DiscussionAuthor a[href="/profile/{user}"])')

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(rules))

    print(f"Blocklist generated in {output_file}")


if __name__ == "__main__":
    generate_blocklist()
