#!/usr/bin/env python3
"""Print the dedupe key for a lead.

    python3 checks/dedupe_key.py --employer "..." --title "..." --location "..."

Matches dedupeKey_() in collector/src/Util.gs (rules in shared/tracker.md).
"""
import argparse

import lib


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--employer", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--location", default="")
    a = ap.parse_args()
    print(lib.dedupe_key(a.employer, a.title, a.location))


if __name__ == "__main__":
    main()
