#!/usr/bin/env bash
# Open an independent stack MAGNET did not author.
# Clones anthropics/skills (public) and runs magnet stack / coverage / fit.
# Requires network once; no AWS keys; no Oscar credentials.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${MAGNET_FOREIGN_STACK:-/tmp/magnet-foreign-skills}"
REPO="${MAGNET_FOREIGN_REPO:-https://github.com/anthropics/skills.git}"

echo "== magnet foreign-stack =="
echo "repo: $REPO"
echo "dest: $DEST"

if [ ! -d "$DEST/skills" ]; then
  rm -rf "$DEST"
  git clone --depth 1 "$REPO" "$DEST"
else
  echo "(reusing existing clone)"
fi

export PATH="${HOME}/.local/bin:${PATH}"
cd "$ROOT"

python3 -m magnet.cli stack --stack "$DEST"
python3 -m magnet.cli probe stack-coverage --stack "$DEST"

# Fit against THEIR gaps (re-derived — do not carry fixture gaps).
python3 - <<PY
from magnet.stack import fit_one, gaps, inventory

stack = "$DEST"
g = gaps(inventory(stack))
print("")
print("FOREIGN gaps (re-derived):")
print("  empty     ", ", ".join(g["empty_surfaces"]) or "—")
print("  uncovered ", ", ".join(g["uncovered"]) or "—")
print("")
# Candidates aimed at foreign gaps — and one noise control.
cases = [
    ("sql-migrator", "SQL dataframe ETL schema migration for the warehouse"),
    ("secrets-gate", "Block credential and secret leaks; sandbox injection attacks"),
    ("plan-slicer", "Decompose a roadmap into slices of work"),
    ("code-reviewer", "Review and critique a pull request; lint the diff"),
    ("pdb-navigator", "Debug a failing test by driving pdb and bisecting the stack trace"),
    ("wine-pairing", "Suggest a wine to pair with dinner"),
]
print("FIT against foreign stack (not our fixture):")
for name, desc in cases:
    f = fit_one(name, desc, stack)
    fills = ",".join(f["fills"]) if f["fills"] else "—"
    print(f"  {f['label']:<20} {name:<16} fills={fills}")
print("")
print("FINDING  fixture gaps ≠ foreign gaps — pdb-navigator fills debug on")
print("FINDING  fixtures/stack but is no-signal on anthropics/skills (debug already covered).")
print("FINDING  wine-pairing is no-signal on both — noise stays noise.")
print("  repro      bash scripts/foreign-stack.sh")
PY

echo ""
echo "== foreign-stack OK =="
