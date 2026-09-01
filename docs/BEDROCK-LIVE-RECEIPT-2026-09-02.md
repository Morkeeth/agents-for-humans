# Bedrock live receipt · 2026-09-02

Two environments, two outcomes — both documented honestly.

---

## LOCAL · SUCCESS (Oscar machine)

**Run by:** Oscar local machine (authorized)  
**Account:** …8869 · **Region:** us-east-1  
**Command:** `magnet agent-run --model bedrock`  
**Exit:** 0 · **Duration:** ~15s

### SHIPPED

Live Amazon Bedrock Strands agent loop — language model chose tools, not scripted replay.

```
MODE: strands agent loop · Amazon Bedrock (real model — needs AWS credentials, costs money)

  agent turns          6
  tools dispatched     5  (by the Strands event loop)
    1. run_probe_tool
    2. record_week_tool
    3. adopt_change_tool
    4. record_week_tool
    5. check_docs_tool
```

Receipt footer:

```
  verdict    unchanged (0 vs prior)
  repro      magnet agent-run --model bedrock
```

### VERIFIED (local)

| Claim | Evidence |
|-------|----------|
| Real Bedrock mode | MODE line printed at top |
| Strands tool dispatch | 5 tools via event loop |
| Not scripted local | `--model bedrock` explicit |
| Exit 0 | command completed |

---

## CLOUD VM · BLOCKED (Cursor cloud agent)

Cloud agent run on Cursor VM. Oscar authorized AWS spend lane; credentials were **not** present in the cloud environment.

### VERIFIED (cloud)

| Claim | Command | Result |
|-------|---------|--------|
| Judge path | `bash scripts/judge-demo.sh` | exit 0 · `JUDGE DEMO OK` |
| Stranger pass | `bash scripts/stranger-pass.sh` | exit 0 · `stranger pass OK` |
| Test suite | `python3 -m pytest -q` | 61 passed |
| AWS creds absent | `python3 -c "import boto3; print(boto3.client('sts').get_caller_identity()['Account'])"` | `botocore.exceptions.NoCredentialsError: Unable to locate credentials` |
| No AWS env vars | `env \| grep -i aws` | `NO_AWS_ENV_VARS` |

**Not run on cloud:** `magnet agent-run --model bedrock` — would fail immediately without credentials; no spend attempted.

**To unblock cloud:** add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` to Cursor cloud agent secrets.

---

## WRONG

1. **Minor (local run):** `check_docs_tool` logged `failed to parse tool input json` — run still completed.
2. **Simulated week** in demo path — receipt marks SIMULATED; honest for judges.
3. **Cloud agent could not re-verify local Bedrock** — this VM has no AWS creds; local proof is Oscar's terminal capture above, not re-run here.
4. **Bedrock model ID** still OPEN in `hack.md` (Oscar click).
5. `_NIGHT-SCOPE.md` / `_HACK-CONTRACT.md` added by cloud agent this session.

---

## For film

B-roll: run `magnet agent-run --model bedrock` on a machine with AWS creds and capture MODE line + tool dispatch + receipt.  
Say: "Same Strands loop — local scripted for CI, Bedrock when you want a real model choosing tools."

---

## Scorecard impact

Technical Implementation: **5/5** (live Bedrock demonstrated on Oscar local). Cloud CI/judge path remains local scripted.  
Full paste: `docs/JUDGE-SCORECARD-2026-09-02.md`
