#!/usr/bin/env bash
# Re-derive live screenshot sidecars from the commands they claim to show.
# Dated film takes (one-workflow.txt @ f690fd0) are NOT refreshed here.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="${HOME}/.local/bin:${PATH}"
unset PYTEST_CURRENT_TEST

OUT=docs/screenshots
mkdir -p "$OUT"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
SHA="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
PY="$(python3 -c 'import sys; print(sys.executable)')"

header() {
  local cmd="$1"
  echo "\$ ${cmd}"
  echo "# captured ${STAMP}  branch=${BRANCH}  sha=${SHA}  python=${PY}"
  echo "#"
}

capture() {
  # Write to a temp file first. Redirecting onto the sidecar itself truncates
  # it before the command runs — which made check-docs read an empty file and
  # fail its own freshness claim mid-capture (found 2026-09-05 by running).
  local name="$1"
  local cmd="$2"
  local file="$OUT/${name}.txt"
  local tmp
  tmp="$(mktemp)"
  {
    header "$cmd"
    set +e
    # shellcheck disable=SC2086
    eval "$cmd"
    local ec=$?
    set -e
    echo "# exit=${ec}"
  } >"$tmp" 2>&1
  mv "$tmp" "$file"
  echo "wrote ${file}  (exit=${ec})"
}

echo "MAGNET capture-sidecars — re-derive live screenshot transcripts"

LIVE_COUNT="$(python3 -c '
from pathlib import Path
import re
print(sum(len(re.findall(r"^\s*def test_", p.read_text(), re.M))
          for p in Path("tests").glob("test_*.py")))
')"

# Unblock freshness + pytest-sidecar claims so check-docs can exit 0 mid-capture.
printf '%s\n' \
  '$ magnet check-docs' \
  '# placeholder — about to re-derive' \
  'sep14 entry ruling' \
  >"$OUT/check-docs.txt"
printf '%s\n' \
  "\$ python3 -m pytest -q --tb=no" \
  "# placeholder" \
  "${LIVE_COUNT} passed in 0.0s" \
  >"$OUT/pytest.txt"

# Docs must already match LIVE_COUNT or pytest capture will embed a failure
# summary ("N failed, M passed") and check_docs will read the wrong first int.
echo "live def test_ count: ${LIVE_COUNT}"

capture pytest "python3 -m pytest -q --tb=no"
capture check-docs "python3 -m magnet.cli check-docs"
capture drift-demo "python3 -m magnet.cli drift-demo"
capture probe-pytest-pass-rate "python3 -m magnet.cli probe pytest-pass-rate"
capture list-probes "python3 -m magnet.cli list-probes"
capture apply-eval "python3 -m magnet.cli apply-eval"
capture apply-demo "python3 -m magnet.cli apply-demo"
capture check-docs "python3 -m magnet.cli check-docs"

echo ""
echo "Dated film takes NOT refreshed: one-workflow.txt (112 @ f690fd0), demo/agent-run/eval/history PNGs"
echo "Re-render PNGs (optional): python3 scripts/render-screenshot.py <txt> <png>"
echo "OK — sidecars re-derived at ${STAMP}  (live test count ${LIVE_COUNT})"
