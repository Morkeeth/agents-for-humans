# FILM-SCOUT-COMMANDS · MAGNET · 5 min Devpost video

**Open with the repetitive task (judges require this):**  
*"Every time you change a prompt, model, or skill, you re-run evals and guess if it helped. MAGNET automates that loop — and refuses to lie with one reading."*

Record terminal + optional slides. No camera required.

---

## 0:00–0:30 · Problem

**Say:** "You changed a skill last Tuesday. Did it help? Most tools say `helped` after one reading. That's not science — that's optimism."

**Slide (optional):** Professional Agents · too many skills, no adoption memory

---

## 0:30–1:30 · Demo · embarrassing case

```bash
cd agents-for-humans
pip install -e .
magnet demo
```

**Point at screen:** After 1 reading — naive verdict `helped`, magnet verdict `baseline`.  
**Say:** "MAGNET refuses to trend until it has two measured readings."

---

## 1:30–2:30 · Eval harness

```bash
magnet eval
```

**Point at:** `silent_null` beats naive on some scenarios.  
**Say:** "We ship the baseline arm that embarrasses us — not just the happy path."

---

## 2:30–3:30 · Strands agent loop

```bash
magnet agent-run
```

**Point at:** `MODE: strands agent loop` + tool dispatch list (5 tools).  
**Say:** "Real Strands Agents SDK — model chooses tools. Default is local scripted for CI; Bedrock path for live AWS."

---

## 3:30–4:15 · Docs drift + adopt loop

```bash
magnet check-docs
magnet adopt --change-type skill --description "film-scout-skill" --prediction "pass rate +1" --probe demo-pass-rate
magnet history
```

**Say:** "README numbers are re-derived — drift exits non-zero. Adoption history is the product."

---

## 4:15–5:00 · Close

**Say:** "MAGNET is magnet to **your** stack — not a marketplace. MIT repo, cold clone, no keys for demo. Professional developers deserve receipts, not vibes."

**Show:** https://github.com/Morkeeth/agents-for-humans  
**Optional:** Agent Grinder as future social layer — agentgrinder.vercel.app

---

## Pre-flight

```bash
bash scripts/stranger-pass.sh   # must exit 0 before filming
python3 -m pytest -q            # 63 passed
```

---

## Bedrock B-roll (Oscar · verified local 2026-09-02)

Live run succeeded on Oscar machine — see `docs/BEDROCK-LIVE-RECEIPT-2026-09-02.md`. Cloud VM has no AWS creds; film on a machine with secrets.

```bash
export AWS_REGION=us-east-1
magnet agent-run --model bedrock
```

**Point at:** `MODE: strands agent loop · Amazon Bedrock` + tools dispatched by the model (not scripted).  
**Say:** "Same four tools — this time a language model on Bedrock chose the sequence."

If filming without AWS creds, use local mode in section 2:30–3:30 and cite the receipt for honest status.
