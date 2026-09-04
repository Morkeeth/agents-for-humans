#!/usr/bin/env bash
# Bedrock live-or-BLOCKED probe — never green on empty input.
#
# Lesson this encodes (week of 2026-09-02): `grep -qv` returns 1 on empty stdin,
# so a "no AWS env" check that grepped inverted on `env | grep` passed for weeks
# during an outage. Every check below requires POSITIVE evidence, or names the
# exact missing piece.
#
# Exit codes:
#   0  LIVE — STS ok AND agent-run --model bedrock printed Bedrock MODE without DEGRADED
#   2  BLOCKED — credentials / region / model access missing (honest; no spend faked)
#   1  CONTROL FAILURE — unexpected error, or Bedrock claimed while DEGRADED
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PATH="${HOME}/.local/bin:${PATH}"

STAMP="${MAGNET_BEDROCK_STAMP:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
OUT_DIR="${MAGNET_BEDROCK_OUT:-/tmp/magnet-bedrock-probe}"
mkdir -p "$OUT_DIR"
REPORT="$OUT_DIR/probe.txt"
: >"$REPORT"

log() { printf '%s\n' "$*" | tee -a "$REPORT"; }

log "MAGNET bedrock-live-or-blocked"
log "stamp: $STAMP"
log "cwd:   $ROOT"
log "head:  $(git rev-parse HEAD 2>/dev/null || echo unknown)"
log ""

# --- 1. Positive presence of credential material (not "grep found nothing") ---
MISSING=()

# Env vars: require non-empty values. Empty string is MISSING.
if [ -n "${AWS_ACCESS_KEY_ID:-}" ]; then
  log "env AWS_ACCESS_KEY_ID: PRESENT (len=${#AWS_ACCESS_KEY_ID})"
else
  log "env AWS_ACCESS_KEY_ID: MISSING"
  MISSING+=("AWS_ACCESS_KEY_ID")
fi
if [ -n "${AWS_SECRET_ACCESS_KEY:-}" ]; then
  log "env AWS_SECRET_ACCESS_KEY: PRESENT (len=${#AWS_SECRET_ACCESS_KEY})"
else
  log "env AWS_SECRET_ACCESS_KEY: MISSING"
  MISSING+=("AWS_SECRET_ACCESS_KEY")
fi
if [ -n "${AWS_REGION:-}${AWS_DEFAULT_REGION:-}" ]; then
  log "env AWS_REGION/AWS_DEFAULT_REGION: PRESENT (${AWS_REGION:-$AWS_DEFAULT_REGION})"
else
  log "env AWS_REGION/AWS_DEFAULT_REGION: MISSING"
  MISSING+=("AWS_REGION")
fi

# Shared files / web identity / container — positive file/path checks.
HAS_ALT=0
if [ -f "${HOME}/.aws/credentials" ]; then
  log "file ~/.aws/credentials: PRESENT"
  HAS_ALT=1
else
  log "file ~/.aws/credentials: ABSENT"
fi
if [ -n "${AWS_WEB_IDENTITY_TOKEN_FILE:-}" ] && [ -f "${AWS_WEB_IDENTITY_TOKEN_FILE}" ]; then
  log "web identity token file: PRESENT"
  HAS_ALT=1
else
  log "web identity token file: ABSENT"
fi
if [ -n "${AWS_CONTAINER_CREDENTIALS_RELATIVE_URI:-}" ] || [ -n "${AWS_CONTAINER_CREDENTIALS_FULL_URI:-}" ]; then
  log "container credentials URI: PRESENT"
  HAS_ALT=1
else
  log "container credentials URI: ABSENT"
fi

# EC2/IMDS instance profile — must get a 200 with a role name, not a timeout.
IMDS_OUT="$OUT_DIR/imds.txt"
if curl -sS -m 2 -o "$IMDS_OUT" -w "%{http_code}" \
    http://169.254.169.254/latest/meta-data/iam/security-credentials/ \
    >"$OUT_DIR/imds.code" 2>"$OUT_DIR/imds.err"; then
  IMDS_CODE="$(cat "$OUT_DIR/imds.code")"
  IMDS_BODY="$(tr -d '\n' <"$IMDS_OUT")"
  if [ "$IMDS_CODE" = "200" ] && [ -n "$IMDS_BODY" ]; then
    log "IMDS instance profile: PRESENT (http $IMDS_CODE, role=${IMDS_BODY})"
    HAS_ALT=1
  else
    log "IMDS instance profile: ABSENT (http ${IMDS_CODE:-none}, body empty-or-missing)"
  fi
else
  log "IMDS instance profile: ABSENT (curl failed: $(tr -d '\n' <"$OUT_DIR/imds.err" | head -c 120))"
fi

log ""
log "missing_named_env: ${MISSING[*]:-none}"
log "alternate_cred_material: $HAS_ALT"
log ""

# --- 2. STS at the object (botocore credential chain) ---
STS_OUT="$OUT_DIR/sts.txt"
: >"$STS_OUT"
set +e
python3 - >>"$STS_OUT" 2>&1 <<'PY'
import sys
try:
    import boto3
except ImportError as e:
    print("IMPORT_FAIL:", e)
    sys.exit(3)
print("boto3", boto3.__version__)
try:
    ident = boto3.client("sts").get_caller_identity()
except Exception as e:
    print(type(e).__name__ + ":", e)
    sys.exit(2)
# Positive evidence: Account must be non-empty digits.
acct = ident.get("Account") or ""
arn = ident.get("Arn") or ""
if not acct.isdigit() or not arn:
    print("STS_SHALLOW:", ident)
    sys.exit(2)
print("Account:", acct)
print("Arn:", arn)
print("UserId:", ident.get("UserId", ""))
sys.exit(0)
PY
STS_EC=$?
set -e
sed 's/^/sts: /' "$STS_OUT" | tee -a "$REPORT"
log "sts_exit: $STS_EC"
log ""

# --- 3. Re-derive DEFAULT_BEDROCK_MODEL_ID from installed package (never carry) ---
MODEL_OUT="$OUT_DIR/model.txt"
: >"$MODEL_OUT"
set +e
python3 - >>"$MODEL_OUT" 2>&1 <<'PY'
import importlib.metadata as m
print("strands-agents=", m.version("strands-agents"))
from strands.models.bedrock import DEFAULT_BEDROCK_MODEL_ID
print("DEFAULT_BEDROCK_MODEL_ID=", DEFAULT_BEDROCK_MODEL_ID)
assert DEFAULT_BEDROCK_MODEL_ID, "empty model id"
PY
MODEL_EC=$?
set -e
sed 's/^/model: /' "$MODEL_OUT" | tee -a "$REPORT"
log "model_exit: $MODEL_EC"
log ""

# --- 4. Decide: attempt Bedrock only if STS succeeded ---
if [ "$STS_EC" -ne 0 ]; then
  log "VERDICT: BLOCKED"
  log "reason: STS did not return a caller identity (exit $STS_EC)"
  if [ "${#MISSING[@]}" -gt 0 ] && [ "$HAS_ALT" -eq 0 ]; then
    log "exact_missing: ${MISSING[*]}"
    log "unblock: set ${MISSING[*]} (or ~/.aws/credentials / IAM role) in this environment, then re-run:"
  else
    log "exact_missing: credential chain empty (STS NoCredentials or equivalent)"
    log "unblock: add AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY + AWS_REGION to Cursor cloud secrets, or aws configure on a local machine, then:"
  fi
  log "  magnet agent-run --model bedrock"
  log "  bash scripts/bedrock-live-or-blocked.sh"
  log ""
  log "NOT claimed: live Bedrock output"
  log "report: $REPORT"
  exit 2
fi

# STS worked — attempt the real loop (costs money; Oscar-authorized lane only).
AGENT_OUT="$OUT_DIR/agent-run.txt"
set +e
python3 -m magnet.cli agent-run --model bedrock >"$AGENT_OUT" 2>&1
AGENT_EC=$?
set -e
log "agent-run_exit: $AGENT_EC"
# Show MODE / DEGRADED / tools lines only (no sprawling receipt dump in summary).
grep -E 'MODE:|DEGRADED|FAILED|tools dispatched|agent turns|NoCredentials|AccessDenied|ValidationException|status' \
  "$AGENT_OUT" | sed 's/^/agent: /' | tee -a "$REPORT" || true
log "agent_full: $AGENT_OUT"
log ""

# Positive LIVE evidence: Bedrock MODE line present AND DEGRADED absent AND exit 0.
if grep -q 'Amazon Bedrock' "$AGENT_OUT" \
  && ! grep -q 'DEGRADED' "$AGENT_OUT" \
  && [ "$AGENT_EC" -eq 0 ]; then
  log "VERDICT: LIVE"
  log "evidence: MODE Amazon Bedrock present, DEGRADED absent, exit 0"
  log "report: $REPORT"
  exit 0
fi

# If we got here with STS ok but agent failed — still BLOCKED (model access?) or CONTROL FAIL.
if grep -q 'DEGRADED' "$AGENT_OUT"; then
  log "VERDICT: BLOCKED"
  log "reason: agent-run printed DEGRADED (Bedrock mode failed after STS)"
  log "exact_missing: Bedrock model access or runtime error — see $AGENT_OUT"
  log "report: $REPORT"
  exit 2
fi

log "VERDICT: CONTROL_FAILURE"
log "reason: STS ok but agent-run did not produce a clean Bedrock MODE (exit $AGENT_EC)"
log "report: $REPORT"
exit 1
