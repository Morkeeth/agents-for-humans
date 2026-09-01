# Night scope · MAGNET · Bedrock live + judge proof · 2026-09-02

**Repo:** Morkeeth/agents-for-humans · **branch:** main  
**Contract:** `hack.md` · `_HACK-CONTRACT.md`

---

## Mission

Run the full judge path on cloud, then attempt **live Amazon Bedrock** Strands loop. Push proof to main.

**Done when:** `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md` exists with real `magnet agent-run --model bedrock` output — or honest BLOCKED with exact error.

---

## Phase 1 · Judge path (no AWS spend)

```bash
git pull --rebase
bash scripts/stranger-pass.sh
bash scripts/judge-demo.sh
python3 -m pytest -q
```

All must exit 0.

---

## Phase 2 · Bedrock live (AWS spend — Oscar authorized)

```bash
python3 -c "import boto3; print(boto3.client('sts').get_caller_identity()['Account'])"
```

- **Creds work:** `export AWS_REGION=us-east-1` · `magnet agent-run --model bedrock`
- **No creds:** BLOCKED receipt · do not fake output

---

## Phase 3 · Film-ready capture

- `docs/FILM-SCOUT-COMMANDS.md` — Bedrock B-roll block if Phase 2 succeeded
- `docs/SCREENSHOTS.md` — optional screenshot #5 from bedrock run
- README For Judges — link bedrock receipt

---

## Do not

- Devpost submit · builder.aws publish · AgentCore deploy
- Fake Bedrock transcript
- Spend beyond one bedrock attempt (+ one retry if transient)
- Touch agentgrinder repo

---

## Ship gate

```bash
git push origin main
```
