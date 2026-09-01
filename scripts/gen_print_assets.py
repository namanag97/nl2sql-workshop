#!/usr/bin/env python3
"""Generate print assets whose content depends on the dataset manifest.
Run AFTER the D-2 dataset freeze; never hand-type counts (WP7 rule).

Usage:  .venv/bin/python scripts/gen_print_assets.py
Output: assets/print/c0-card.md, assets/print/counts-handout.md
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "assets" / "print"
manifest = json.loads((ROOT / "data" / "out" / "manifest.json").read_text())
keys = json.loads((ROOT / "data" / "keys" / "keys.json").read_text())

OUTDIR.mkdir(parents=True, exist_ok=True)

table_rows = "\n".join(f"| `{t}` | {n:,} |" for t, n in manifest.items())
(OUTDIR / "c0-card.md").write_text(f"""### C0 — Smoke test (GENERATED — do not edit)
```
List every table in schema o2c with its row count. Show as a table.
```
*You should see:*

| Table | Rows |
|---|---|
{table_rows}
""")

(OUTDIR / "counts-handout.md").write_text(f"""# Meridian Trading Co. — data at a glance (GENERATED)

| Table | Rows |
|---|---|
{table_rows}

Fiscal year starts **Feb 1**. Data window: Feb 2025 – Jun 2026.
Hand this out with the glossary; card C0 must reproduce this table exactly.
""")

print("generated:")
for p in sorted(OUTDIR.glob("*.md")):
    print(f"  {p.relative_to(ROOT)}")
