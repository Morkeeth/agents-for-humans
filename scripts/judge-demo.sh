#!/usr/bin/env bash
# Judge path — 60-second proof of all 5 Devpost criteria. No keys, no network after pip install.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "MAGNET judge demo — installing..."
pip install -e ".[dev]" -q
export PATH="${HOME}/.local/bin:${PATH}"

# Subprocess may inherit PYTEST_CURRENT_TEST when this script is tested from pytest.
unset PYTEST_CURRENT_TEST

if [ -n "${MAGNET_JUDGE_QUICK:-}" ]; then
  echo "(quick mode — magnet steps skipped; used from pytest)"
  echo ""
  echo "=== 4/8 · Technical: docs drift gate ==="
  magnet check-docs
else
  echo ""
  echo "=== 1/8 · Design + Impact: embarrassing case (naive helped vs magnet baseline) ==="
  magnet demo

  echo ""
  echo "=== 2/8 · Creativity: eval arms (silent_null vs naive vs magnet) ==="
  magnet eval

  echo ""
  echo "=== 3/8 · Technical: Strands agent loop (4 tools dispatched) ==="
  magnet agent-run

  echo ""
  echo "=== 4/8 · Technical: docs drift gate ==="
  magnet check-docs

  echo ""
  echo "=== 4b/8 · Technical: drift demo (Qwen lesson) ==="
  magnet drift-demo

  echo ""
  echo "=== 5/8 · Impact: production probe (pytest-pass-rate adopt) ==="
  magnet adopt skill production-eval-demo "all tests still pass" \
    --probe pytest-pass-rate --reset --no-simulate

  echo ""
  echo "=== 6/8 · Design: adoption timeline ==="
  magnet history | head -25

  echo ""
  echo "=== 7/8 · Impact: stack inventory + bakeoff vs marketplace proxies ==="
  magnet stack
  magnet bakeoff --no-write
fi

echo ""
echo "=== 8/8 · Technical: test suite ==="
if [ -n "${MAGNET_JUDGE_QUICK:-}" ]; then
  python3 -m pytest -q --tb=no tests/test_reporter.py tests/test_demo.py
else
  python3 -m pytest -q --tb=no
fi

echo ""
echo "JUDGE DEMO OK — see docs/JUDGE-SCORECARD-2026-09-02.md for criterion mapping"
