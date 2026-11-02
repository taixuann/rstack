#!/usr/bin/env python3
"""Append one row to a decision-log TSV. Usage: log.py LOG PHASE DECISION WHY EVIDENCE RESULT"""
import sys, os, datetime

HEADER = ["ts", "phase", "decision", "why", "evidence", "result"]

def clean(s):
    s = " ".join(str(s).replace("\t", " ").replace("\r", " ").replace("\n", " ").split())
    return "'" + s if s[:1] in "=+-@" else s

def main():
    if len(sys.argv) != 7:
        sys.exit(__doc__)
    log, *cells = sys.argv[1:]
    new = not os.path.exists(log) or os.path.getsize(log) == 0
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(os.path.abspath(log)), exist_ok=True)
    with open(log, "a") as f:
        if new:
            f.write("\t".join(HEADER) + "\n")
        f.write("\t".join([ts] + [clean(c) for c in cells]) + "\n")

main()
