#!/usr/bin/env bash
# Stranger pass — one command, cold clone, no keys.
# Usage: curl -sSL … | bash   OR   ./scripts/stranger-pass.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== magnet stranger pass =="
echo "repo: $ROOT"
echo ""

python3 -m pip install -e ".[dev]" -q
export PATH="${HOME}/.local/bin:${PATH}"

# Subprocess may inherit PYTEST_CURRENT_TEST when this script is tested from pytest.
unset PYTEST_CURRENT_TEST

if [ -n "${MAGNET_STRANGER_QUICK:-}" ]; then
  # Used when this script is invoked from pytest (avoids nested full-suite runs).
  python3 -m pytest -q tests/test_reporter.py tests/test_demo.py
else
  python3 -m magnet.cli probe pytest-pass-rate   # real eval — one pytest run
fi
python3 -m magnet.cli demo
python3 -m magnet.cli eval
python3 -m magnet.cli agent-run
python3 -m magnet.cli list-probes
python3 -m magnet.cli stack
python3 -m magnet.cli bakeoff --no-write
python3 -m magnet.cli replicate
python3 -m magnet.cli coverage-delta \
  --name pdb-navigator \
  --text "Debug a failing test by driving pdb and bisecting the stack trace" \
  --stack fixtures/stack-cursor
python3 -m magnet.cli drift-demo
python3 -m magnet.cli check-docs
python3 -m magnet.cli history

echo ""
echo "== stranger pass OK =="
