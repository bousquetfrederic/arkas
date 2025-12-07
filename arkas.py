#!/usr/bin/env python3
import sys
from datetime import datetime

def convert_entry(entry: str) -> list[str]:
    entry = entry.strip()
    if not entry or entry.startswith("#") or entry.startswith("!"):
        return []

    # --- Discussion ID filter ---
    if entry.startswith("$"):
        discussion_id = entry[1:]
        if discussion_id.isdigit():
            return [f"lowendtalk.com##li#Discussion_{discussion_id}"]
        return []

    # --- Category filters ---
    if entry.startswith("%"):
        category = entry[1:]
        return [f"lowendtalk.com##li.ItemDiscussion:has(.Category.Category-{category})"]

    # --- User filters ---
    if entry.endswith(":c"):
        user = entry[:-2]
        # Hide entire comment blocks by this user
        return [f"lowendtalk.com##.Comment:has(.Username[href='/profile/{user}'])"]

    elif entry.endswith(":d"):
        user = entry[:-2]
        # Hide entire discussion tiles started by this user
        return [f"lowendtalk.com##li.ItemDiscussion:has(.DiscussionAuthor a[href='/profile/{user}'])"]

    else:
        user = entry
        # Hide both comments and discussions by this user
        return [
            f"lowendtalk.com##.Comment:has(.Username[href='/profile/{user}'])",
            f"lowendtalk.com##li.ItemDiscussion:has(.DiscussionAuthor a[href='/profile/{user}'])"
        ]

def main():
    if len(sys.argv) < 2:
        print("Usage: arkas.py <filterfile>")
        sys.exit(1)

    filterfile = sys.argv[1]
    with open(filterfile, "r", encoding="utf-8") as f:
        entries = f.readlines()

    # Print header with timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"! Arkas blocklist generated on {now}")

    for entry in entries:
        rules = convert_entry(entry)
        for rule in rules:
            print(rule)

    # Footer
    print("! End of blocklist")

if __name__ == "__main__":
    main()