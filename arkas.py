#!/usr/bin/env python3
import sys

def convert_entry(entry: str) -> list[str]:
    entry = entry.strip()
    if not entry or entry.startswith("#"):
        return []

    # --- Discussion ID filter ---
    if entry.startswith("$"):
        discussion_id = entry[1:]
        if discussion_id.isdigit():
            # Cosmetic rule (listings) and network rule (discussion pages)
            return [
                f"lowendtalk.com##li#Discussion_{discussion_id}",
                f"||lowendtalk.com/discussion/{discussion_id}/^"
            ]
        return []

    # --- User filters ---
    if entry.endswith(":c"):
        user = entry[:-2]
        return [f"lowendtalk.com##.Comment .Username[href='/profile/{user}']"]
    elif entry.endswith(":d"):
        user = entry[:-2]
        return [f"lowendtalk.com##.ItemDiscussion .DiscussionAuthor a[href='/profile/{user}']"]
    else:
        user = entry
        return [
            f"lowendtalk.com##.Comment .Username[href='/profile/{user}']",
            f"lowendtalk.com##.ItemDiscussion .DiscussionAuthor a[href='/profile/{user}']"
        ]

def main():
    if len(sys.argv) < 2:
        print("Usage: Arkas.py <filterfile>")
        sys.exit(1)

    filterfile = sys.argv[1]
    with open(filterfile, "r", encoding="utf-8") as f:
        entries = f.readlines()

    for entry in entries:
        rules = convert_entry(entry)
        for rule in rules:
            print(rule)

if __name__ == "__main__":
    main()