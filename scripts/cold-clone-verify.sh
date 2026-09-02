#!/usr/bin/env bash
# Cold-clone kill-bar — clone from GitHub (or any URL), run judge-demo, exit 0.
# Usage: bash scripts/cold-clone-verify.sh [repo-url]
set -euo pipefail

REPO_URL="${1:-https://github.com/Morkeeth/agents-for-humans.git}"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "cold-clone-verify: cloning $REPO_URL → $WORKDIR/repo"
git clone --depth 1 "$REPO_URL" "$WORKDIR/repo"
cd "$WORKDIR/repo"

echo ""
bash scripts/judge-demo.sh

echo ""
echo "COLD CLONE OK — $REPO_URL"
echo "  full judge-demo (no quick): unset MAGNET_JUDGE_QUICK && bash scripts/cold-clone-verify.sh"
