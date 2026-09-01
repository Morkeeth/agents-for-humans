# _NIGHT-SCOPE.md · MAGNET judge-winning night · 2026-09-02

**Repo:** Morkeeth/agents-for-humans · **branch:** main  
**Contract:** `hack.md` · `_HACK-CONTRACT.md`

**EYES ruling:** MAGNET submits. Agent Grinder is a separate product — do not touch agentgrinder repo.

---

## Kill bar

```bash
git clone https://github.com/Morkeeth/agents-for-humans.git
cd agents-for-humans
bash scripts/judge-demo.sh   # must print JUDGE DEMO OK
```

If this fails on cold clone, the night failed.

---

## Repetitive task (say everywhere)

> After every prompt, model, or skill change, developers manually re-run evals and guess if it helped — MAGNET's Strands agent automates that loop and refuses to lie with one reading.

---

## Phase 1 · Judge path (no AWS spend)

```bash
git pull --rebase
bash scripts/stranger-pass.sh
bash scripts/judge-demo.sh
python3 -m pytest -q
```

All must exit 0. Cold clone required after push.

---

## Phase 2 · Bedrock live (AWS spend — Oscar authorized)

```bash
python3 -c "import boto3; print(boto3.client('sts').get_caller_identity()['Account'])"
magnet agent-run --model bedrock
```

- **Creds work:** receipt in `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`
- **No creds (cloud VM):** BLOCKED — do not fake output

---

## Judging criteria → proof command

| Criterion | Judge asks | Proof |
|-----------|------------|-------|
| Technical | Real Strands? AWS? | `magnet agent-run` · `pytest -q` · Bedrock receipt |
| Design | Complete product? | `magnet demo` · `magnet history` |
| Impact | Real problem? | DEVPOST problem paragraph · `magnet adopt` |
| Creativity | Non-obvious use? | `magnet eval` (silent_null arm) |
| Presentation | Video + pitch? | `docs/FILM-SCOUT-COMMANDS.md` (Oscar films) |

---

## Do NOT

- Submit Devpost · publish builder.aws · fake Bedrock output
- Touch agentgrinder · score 5/5 without evidence

---

## Oscar gates (outward acts)

- Film 5-min video (+ Bedrock B-roll if creds)
- Paste DEVPOST-DESCRIPTION
- Submit before Sep 14 5pm PDT

## Ship gate

```bash
git push origin main
```
