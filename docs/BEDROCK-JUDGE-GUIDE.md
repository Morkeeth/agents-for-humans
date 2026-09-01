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
magnet agent-run --model bedrock
```

**Expected:** `MODE: strands agent loop · Amazon Bedrock` and tool dispatch from the model (not scripted).

**Costs money.** Not run in CI. Not required for cold demo.

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
