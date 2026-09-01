#!/usr/bin/env bash
# Judge path — 60-second proof of all 5 Devpost criteria. No keys, no network after pip install.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "MAGNET judge demo — installing..."
pip install -e ".[dev]" -q

echo ""
echo "=== 1/6 · Design + Impact: embarrassing case (naive helped vs magnet baseline) ==="
magnet demo

echo ""
echo "=== 2/6 · Creativity: eval arms (silent_null vs naive vs magnet) ==="
magnet eval

echo ""
echo "=== 3/6 · Technical: Strands agent loop (4 tools dispatched) ==="
magnet agent-run

echo ""
echo "=== 4/6 · Technical: docs drift gate ==="
magnet check-docs

echo ""
echo "=== 5/6 · Design: adoption timeline ==="
magnet history | head -25

echo ""
echo "=== 6/6 · Technical: test suite ==="
python3 -m pytest -q --tb=no

echo ""
echo "JUDGE DEMO OK — see docs/JUDGE-SCORECARD-2026-09-02.md for criterion mapping"
