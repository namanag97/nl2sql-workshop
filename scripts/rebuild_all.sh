#!/usr/bin/env bash
# One-command rebuild — the D-2 freeze procedure.
# Regenerates EVERYTHING from source and runs every gate. Run this after
# any generator change, and once more at the freeze; the room runs only
# what this script last produced.
set -euo pipefail
cd "$(dirname "$0")/.."

PY="${PYTHON:-.venv/bin/python}"
command -v "$PY" >/dev/null || PY=python3

echo "== 1/8 dataset (seed 42) =="            && "$PY" data/gen/generate.py
echo "== 2/8 keys + envelopes =="             && "$PY" data/keys/compute_keys.py
echo "== 3/8 quirk proofs =="                 && "$PY" data/keys/run_checks.py
echo "== 4/8 duckdb fallback + parity =="     && "$PY" data/fallback/build_duckdb.py
echo "== 5/8 magic-moment proof =="           && "$PY" data/fallback/verify_arcs.py
echo "== 6/8 simulated agent pass =="         && "$PY" scripts/simulate_agent.py
echo "== 7/8 intern answers + print assets =="&& "$PY" scripts/gen_intern_answers.py && "$PY" scripts/gen_print_assets.py
echo "== 8/8 rerun-at-home kit =="            && "$PY" scripts/build_kit.py

echo ""
echo "ALL GATES GREEN — dataset frozen. Print assets and kit are current."
echo "Next: print packs/ + assets/print/, seal envelopes from data/keys/envelopes/."
