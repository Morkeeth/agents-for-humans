# Bedrock path · for judges with AWS credentials

MAGNET's default `magnet agent-run` uses a **real Strands agent loop** with a local scripted model (no AWS, no spend). This is intentional for CI and cold clone.

For **Technical Implementation** scoring, judges with AWS access can run the same loop with a language model genuinely choosing tools via Amazon Bedrock.

---

## Prerequisites

1. AWS account with [Amazon Bedrock](https://aws.amazon.com/bedrock/) model access  
2. Model enabled in your region (e.g. Claude on Bedrock in `us-east-1`)  
3. AWS credentials configured (`aws configure` or env vars)

---

## Environment

```bash
export AWS_REGION=us-east-1   # or your Bedrock region
export AWS_ACCESS_KEY_ID=...    # or use aws configure / IAM role
export AWS_SECRET_ACCESS_KEY=...
# Strands/Bedrock may also read standard AWS credential chain
```

---

## Run

```bash
pip install -e ".[dev]"
# Positive-evidence gate (exit 0 LIVE / 2 BLOCKED / 1 control failure):
bash scripts/bedrock-live-or-blocked.sh
# Or direct:
magnet agent-run --model bedrock
```

**Expected LIVE:** `MODE: strands agent loop · Amazon Bedrock` and tool dispatch from the model (not scripted), process exit 0, no `DEGRADED` banner.

**Expected BLOCKED (no creds):** `DEGRADED` banner + process exit **1** (fixed 2026-09-04; previously lied exit 0). The preflight script exits 2 and names exact missing env.

**Costs money.** Not run in CI. Not required for cold demo.

---

## Verified live (2026-09-02)

Oscar ran `magnet agent-run --model bedrock` on local machine — exit 0, 5 tools dispatched via Strands event loop. Full output: `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`.

---

## If Bedrock fails

The CLI prints the failure loudly and does not fake success. Fall back to:

```bash
magnet agent-run --model local   # real Strands loop, scripted plan
magnet agent-run --model none    # deterministic chain, no agent
```

Code path for Bedrock: `magnet/agent_run.py` mode `bedrock`. Tests: `tests/test_agent_loop.py` (mocked, no network).

---

## AgentCore (optional · not deployed)

Deploy prep only — Oscar click. See `docs/AGENTCORE-DEPLOY-PREP.md` if present.

---

## Honesty for video

If filming without AWS creds: show `magnet agent-run` (local mode) and state Bedrock path exists for judges with credentials. Do not imply Bedrock ran if it did not.

---

## Verified on cloud · 2026-09-04

**Status: BLOCKED** — no AWS credentials in Cursor cloud agent VM.

| Check | Command | Result |
|-------|---------|--------|
| Positive env presence | `bash scripts/bedrock-live-or-blocked.sh` | exit 2 · `exact_missing: AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_REGION` |
| STS identity | `python3 -c "import boto3; print(boto3.client('sts').get_caller_identity())"` | `NoCredentialsError: Unable to locate credentials` |
| Bedrock attempt | `python3 -m magnet.cli agent-run --model bedrock` | `DEGRADED` + exit **1** (exit was 0 before 2026-09-04 fix) |
| Judge path | `bash scripts/judge-demo.sh` | exit 0 · `JUDGE DEMO OK` |
| Stranger path | `bash scripts/stranger-pass.sh` | exit 0 · `stranger pass OK` |

Full receipt: `docs/BEDROCK-LIVE-RECEIPT-2026-09-04.md`  
Prior local LIVE (Oscar machine): `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`

**To unblock:** add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` to Cursor cloud agent secrets, then re-run `bash scripts/bedrock-live-or-blocked.sh` until it prints `VERDICT: LIVE`.

---

## Verified on cloud · 2026-09-02

**Status: BLOCKED** — no AWS credentials in Cursor cloud agent VM.

| Check | Command | Result |
|-------|---------|--------|
| STS identity | `python3 -c "import boto3; print(boto3.client('sts').get_caller_identity()['Account'])"` | `NoCredentialsError: Unable to locate credentials` |
| Env vars | `env \| grep -i aws` | none |

Full receipt: `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`

**To unblock:** add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` to Cursor cloud agent secrets, then re-run `magnet agent-run --model bedrock`.
