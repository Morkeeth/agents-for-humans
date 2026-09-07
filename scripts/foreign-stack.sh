#!/usr/bin/env bash
# Open an independent stack MAGNET did not author.
# Clones anthropics/skills (public) by default and runs magnet external-stack.
# Requires network once; no AWS keys; no Oscar credentials.
# Cold path without network: use the offline receipt in docs/EXTERNAL-STACK-RECEIPT.md
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

python3 -m magnet.cli external-stack --stack "$DEST"
python3 -m magnet.cli probe stack-coverage --stack "$DEST"

echo ""
echo "== foreign-stack OK =="
