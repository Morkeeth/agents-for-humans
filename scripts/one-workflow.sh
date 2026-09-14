#!/usr/bin/env bash
# One workflow — change a prompt, MAGNET re-runs YOUR eval, grades recovers.
# Uses the Devpost prediction text ("pass rate recovers by 1"), not a synonym.
# Cold path: no keys, no network after install. Exit 0 only when restore grades.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
export PATH="${HOME}/.local/bin:${PATH}"
unset PYTEST_CURRENT_TEST

if [ -n "${MAGNET_ONE_WORKFLOW_QUICK:-}" ]; then
  echo "MAGNET one-workflow — quick mode (script presence only)"
  echo "ONE WORKFLOW OK (quick)"
  exit 0
fi

# Prefer editable checkout code via -m so sed edits are measured.
M=(python3 -m magnet.cli --log .magnet/demo-one.db)
DB=".magnet/demo-one.db"
rm -f "$DB"
mkdir -p .magnet

# Capture for sidecars when MAGNET_ONE_WORKFLOW_CAPTURE=1
OUT="${MAGNET_ONE_WORKFLOW_OUT:-/tmp/magnet-one-workflow.out}"
: >"$OUT"

log() {
  echo "$@" | tee -a "$OUT"
}

log "### 0  clock $(date -u +%Y-%m-%dT%H:%M:%SZ)  git $(git rev-parse --short HEAD)  magnet from ./magnet (this checkout)"
log ""

# Ensure clean SYSTEM_PROMPT before start
git checkout -- magnet/tools.py 2>/dev/null || true

log "### 1  \$ python3 -m magnet.cli --log .magnet/demo-one.db record pytest-pass-rate"
"${M[@]}" record pytest-pass-rate 2>&1 | tee -a "$OUT"
log ""

log "### 2  \$ sed -i 's/ — never invent a trend from one reading//' magnet/tools.py"
sed -i 's/ — never invent a trend from one reading//' magnet/tools.py
log "(SYSTEM_PROMPT never-invent rule dropped)"
log ""

log "### 3  \$ python3 -m magnet.cli --log .magnet/demo-one.db adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' 'pass rate unchanged' --probe pytest-pass-rate --no-simulate"
"${M[@]}" adopt prompt 'drop the never-invent rule from SYSTEM_PROMPT' \
  'pass rate unchanged' --probe pytest-pass-rate --no-simulate 2>&1 | tee -a "$OUT"
log ""

log "### 4  \$ git checkout -- magnet/tools.py"
git checkout -- magnet/tools.py
log ""

log "### 5  \$ python3 -m magnet.cli --log .magnet/demo-one.db adopt prompt 'restore the never-invent rule' 'pass rate recovers by 1' --probe pytest-pass-rate --no-simulate"
"${M[@]}" adopt prompt 'restore the never-invent rule' \
  'pass rate recovers by 1' --probe pytest-pass-rate --no-simulate 2>&1 | tee -a "$OUT"
log ""

log "### 6  \$ python3 -m magnet.cli --log .magnet/demo-one.db history"
"${M[@]}" history 2>&1 | tee -a "$OUT"
log ""

# Gate: restore step must grade rise + not no-direction
if ! grep -q "pass rate recovers by 1" "$OUT"; then
  echo "ONE WORKFLOW FAIL: recover prediction missing from output" >&2
  exit 1
fi
if ! grep -A6 "pass rate recovers by 1" "$OUT" | grep -q "intent     rise"; then
  echo "ONE WORKFLOW FAIL: recover prediction did not grade as rise" >&2
  grep -A12 "pass rate recovers by 1" "$OUT" >&2 || true
  exit 1
fi
if grep -A8 "pass rate recovers by 1" "$OUT" | grep -q "no-direction"; then
  echo "ONE WORKFLOW FAIL: recover still no-direction (Slice 32 defect)" >&2
  exit 1
fi
# Hurt then helped must appear
if ! grep -q "verdict    hurt" "$OUT"; then
  echo "ONE WORKFLOW FAIL: expected hurt after dropping the rule" >&2
  exit 1
fi
if ! grep -q "verdict    helped" "$OUT"; then
  echo "ONE WORKFLOW FAIL: expected helped after restore" >&2
  exit 1
fi

if [ "${MAGNET_ONE_WORKFLOW_CAPTURE:-}" = "1" ]; then
  mkdir -p docs/screenshots
  {
    echo "\$ bash scripts/one-workflow.sh"
    echo ""
    cat "$OUT"
    echo "# exit=0"
  } > docs/screenshots/one-workflow.txt
  echo "captured → docs/screenshots/one-workflow.txt"
fi

echo "ONE WORKFLOW OK"
echo "# exit=0" | tee -a "$OUT"
exit 0
