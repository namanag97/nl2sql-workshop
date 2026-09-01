#!/usr/bin/env python3
"""Run quirk_checks.sql against the generated CSVs; exit 1 on any failure.

Usage: python3 run_checks.py
"""
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compute_keys import SCHEMA, load  # noqa: E402

CHECKS = Path(__file__).resolve().parent / "quirk_checks.sql"


def main():
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA)
    load(db)

    text = CHECKS.read_text()
    blocks = re.split(r"\n(?=-- @check)", text)
    results = []
    for block in blocks:
        m = re.match(r"-- @check (QK-\d+) expect (\d+):(\d+)\s+(.*)", block)
        if not m:
            continue
        qid, lo, hi, desc = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        sql = "\n".join(l for l in block.splitlines()
                        if not l.strip().startswith("--")).strip()
        if not sql:
            # structural checks delegated to the runner
            got = structural_check(qid, db)
        else:
            got = db.execute(sql).fetchone()[0]
        ok = lo <= int(got) <= hi
        results.append((ok, qid, got, f"{lo}..{hi}", desc))

    width = max(len(r[4]) for r in results) + 2
    fails = 0
    for ok, qid, got, expect, desc in results:
        print(f"{'PASS' if ok else 'FAIL'}  {qid}  got={got:<6} want {expect:<8} {desc}")
        fails += 0 if ok else 1
    print(f"\n{len(results) - fails}/{len(results)} quirk proofs passed")
    sys.exit(1 if fails else 0)


def structural_check(qid, db):
    if qid == "QK-14":
        cols = [r[1] for r in db.execute("PRAGMA table_info(orders)")]
        return sum(1 for c in cols if "region" in c.lower())
    raise ValueError(f"no structural check defined for {qid}")


if __name__ == "__main__":
    main()
