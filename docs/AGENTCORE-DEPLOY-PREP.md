# AgentCore deploy prep · Oscar click only

**Status:** NOT deployed. Prep for optional Technical Implementation bonus.

---

## Why

Devpost criteria: *"A live demo and/or AWS AgentCore deployment will strengthen this score."*

MAGNET is CLI-first. AgentCore would host the Strands agent as a service. **Not required** for submission — Bedrock local run may suffice.

---

## If Oscar deploys (outline)

1. Package `magnet/` as container with Strands + tools
2. AgentCore runtime with Bedrock model access
3. Expose `POST /adopt` → agent-run → receipt JSON
4. Document URL in Devpost "Try it" field

---

## Minimum for judges without deploy

- `bash scripts/judge-demo.sh` on cold clone
- Optional: `magnet agent-run --model bedrock` with Oscar AWS creds on film

**Do not claim AgentCore deployment unless URL is live.**
